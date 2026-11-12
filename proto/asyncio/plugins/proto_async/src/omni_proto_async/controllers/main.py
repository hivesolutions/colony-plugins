import json
import time
import random
import asyncio
import threading

import colony

from .base import BaseController

models = colony.__import__("models")
mvc_utils = colony.__import__("mvc_utils")

SUBSCRIBERS = set()
""" The queues of the open POS WebSocket sessions, used when there's
no Redis (single process only, workers need the shared broker) """

CHANNEL = "omni:pos"
""" The Redis pub/sub channel of the POS events, shared by every worker """

REDIS = dict()
""" The Redis client of each event loop (one per worker) """


def _redis():
    url = colony.conf("REDISTOGO_URL", None)
    if not url:
        return None
    import redis.asyncio

    loop = asyncio.get_running_loop()
    client = REDIS.get(loop, None)
    if client == None:
        client = redis.asyncio.from_url(url)
        REDIS[loop] = client
    return client


class Rollback(Exception):
    pass


def _thread():
    return threading.current_thread().name


def _product_d(product):
    return dict(
        id=product.object_id,
        name=product.name,
        vat_class=product.vat_class and product.vat_class.identifier,
    )


class MainController(BaseController):

    def fast(self, request):
        self.serialize(request, dict(result="fast", thread=_thread()))

    def slow_sync(self, request):
        # a blocking external call (headless render, AT, Colony Print)
        # holds the worker thread for its whole duration
        ms = int(request.field("ms", "2000"))
        time.sleep(ms / 1000.0)
        self.serialize(request, dict(result="slow_sync", ms=ms, thread=_thread()))

    async def slow_async(self, request):
        # the same external call awaited, no thread is held while waiting
        ms = int(request.field("ms", "2000"))
        await asyncio.sleep(ms / 1000.0)
        self.serialize(request, dict(result="slow_async", ms=ms, thread=_thread()))

    def products_sync(self, request):
        products = models.Product.find(
            dict(
                eager=("vat_class",),
                start_record=0,
                number_records=20,
                order_by=(("object_id", "ascending"),),
            )
        )
        count = models.Product.count()
        self.serialize(
            request,
            dict(
                count=count,
                products=[_product_d(product) for product in products],
                thread=_thread(),
            ),
        )

    async def products_async(self, request):
        products = await models.Product.find_a(
            dict(
                eager=("vat_class",),
                start_record=0,
                number_records=20,
                order_by=(("object_id", "ascending"),),
            )
        )
        count = await models.Product.count_a()
        self.serialize(
            request,
            dict(
                count=count,
                products=[_product_d(product) for product in products],
                thread=_thread(),
            ),
        )

    async def lazy_async(self, request):
        products = await models.Product.find_a(
            dict(
                start_record=0, number_records=1, order_by=(("object_id", "ascending"),)
            )
        )
        product = products[0]
        try:
            refused = product.vat_class.identifier
        except Exception as exception:
            refused = "%s: %s" % (exception.__class__.__name__, exception)
        await product.load_a("vat_class")
        self.serialize(
            request,
            dict(
                product=product.object_id,
                implicit=refused,
                explicit=product.vat_class.identifier,
            ),
        )

    async def isolation_async(self, request):
        # concurrent tasks on the same thread, each gets its own
        # connection and transaction (bound to a context variable)
        mode = request.field("mode", "read")
        id = int(request.field("id", "405"))
        orm = request.field("orm", "0") == "1"
        entity_manager = models.Product._entity_manager
        if mode == "read":
            product = await models.Product.get_a(id)
            self.serialize(
                request, dict(mode=mode, name=product.name, thread=_thread())
            )
            return
        name = "UNCOMMITTED-%04d" % random.randint(0, 9999)
        inside = None
        error = None
        try:
            async with entity_manager.transaction_a():
                if orm:
                    product = await models.Product.get_a(id, dict(eager=("vat_class",)))
                    product.name = name
                    await product.update_a()
                else:
                    await entity_manager.execute_a(
                        "update _named_node set name = '%s' where object_id = %d"
                        % (name, id)
                    )
                inside = (await models.Product.get_a(id)).name
                await asyncio.sleep(float(request.field("hold", "1.0")))
                raise Rollback()
        except Rollback:
            pass
        except Exception as exception:
            error = "%s: %s" % (exception.__class__.__name__, exception)
        after = (await models.Product.get_a(id)).name
        self.serialize(
            request,
            dict(mode=mode, written=name, inside=inside, after=after, error=error),
        )

    async def isolation_naive(self, request):
        # what happens with the current thread bound connection when
        # the sync API is used from concurrent tasks on the loop thread
        mode = request.field("mode", "read")
        id = int(request.field("id", "405"))
        entity_manager = models.Product._entity_manager
        if mode == "read":
            product = models.Product.get(id)
            self.serialize(
                request, dict(mode=mode, name=product.name, thread=_thread())
            )
            return
        name = "UNCOMMITTED-%04d" % random.randint(0, 9999)
        entity_manager.begin()
        try:
            entity_manager.execute(
                "update _named_node set name = '%s' where object_id = %d" % (name, id)
            )
            await asyncio.sleep(float(request.field("hold", "1.0")))
        finally:
            entity_manager.rollback()
        after = models.Product.get(id).name
        self.serialize(request, dict(mode=mode, written=name, after=after))

    async def stock_bump(self, request):
        id = int(request.field("id", "405"))
        delta = int(request.field("delta", "-1"))
        event = dict(event="stock", product=id, delta=delta, timestamp=time.time())
        client = _redis()
        if client:
            notified = await client.publish(CHANNEL, json.dumps(event))
        else:
            for queue in list(SUBSCRIBERS):
                queue.put_nowait(event)
            notified = len(SUBSCRIBERS)
        self.serialize(request, dict(notified=notified))

    async def ws_progress(self, websocket):
        # a long sync job (eg: SAF-T export) runs in the thread pool and
        # reports its progress to the socket through the event loop
        await websocket.accept()
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue()
        steps = int(websocket.query.get("steps", "10"))

        def job():
            for index in range(steps):
                time.sleep(0.2)
                progress = (index + 1) * 100 // steps
                loop.call_soon_threadsafe(queue.put_nowait, dict(progress=progress))
            loop.call_soon_threadsafe(queue.put_nowait, None)

        future = loop.run_in_executor(websocket.executor, job)
        while True:
            message = await queue.get()
            if message == None:
                break
            await websocket.send_json(message)
        await future
        await websocket.send_json(dict(done=True))
        await websocket.close()

    async def ws_pos(self, websocket):
        await websocket.accept()
        queue = asyncio.Queue()
        client = _redis()
        pubsub = None
        relay = None
        if client:
            pubsub = client.pubsub()
            await pubsub.subscribe(CHANNEL)

            async def relay_events():
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        queue.put_nowait(json.loads(message["data"]))

            relay = asyncio.ensure_future(relay_events())
        else:
            SUBSCRIBERS.add(queue)
        try:
            await websocket.send_json(dict(event="subscribed"))
            receiver = asyncio.ensure_future(websocket.receive())
            while True:
                getter = asyncio.ensure_future(queue.get())
                done, _pending = await asyncio.wait(
                    (getter, receiver), return_when=asyncio.FIRST_COMPLETED
                )
                if receiver in done:
                    getter.cancel()
                    break
                await websocket.send_json(getter.result())
        finally:
            SUBSCRIBERS.discard(queue)
            if relay:
                relay.cancel()
            if pubsub:
                await pubsub.unsubscribe(CHANNEL)
                await pubsub.aclose()
