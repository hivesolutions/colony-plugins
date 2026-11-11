"""
Throwaway probe of the netius ASGI server modes (native and asyncio),
checking what the Omni design relies on: asyncio sleeps, thread pool
offload, per-request context variables and an asyncio MySQL driver.
"""

import time
import asyncio
import contextvars
import concurrent.futures
import urllib.parse

import aiomysql

REQUEST_ID = contextvars.ContextVar("request_id", default=None)
EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=16)
POOL = None


async def get_pool():
    global POOL
    if POOL == None:
        POOL = await aiomysql.create_pool(
            host="127.0.0.1",
            port=33071,
            user="root",
            password="root",
            db="omni_proto",
            minsize=1,
            maxsize=16,
        )
    return POOL


async def app(scope, receive, send):
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
    path = scope["path"]
    query = dict(urllib.parse.parse_qsl(scope.get("query_string", b"").decode()))
    ms = int(query.get("ms", "1000"))
    start = time.time()
    if path == "/fast":
        body = "fast"
    elif path == "/sleep":
        await asyncio.sleep(ms / 1000.0)
        body = "slept"
    elif path == "/thread":
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(EXECUTOR, time.sleep, ms / 1000.0)
        body = "threaded"
    elif path == "/ctx":
        value = query.get("id", "none")
        REQUEST_ID.set(value)
        await asyncio.sleep(ms / 1000.0)
        seen = REQUEST_ID.get()
        body = "ctx %s %s" % (value, "ok" if seen == value else "LEAK saw %s" % seen)
    elif path == "/db":
        pool = await get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "select sleep(%f), connection_id()" % (ms / 1000.0)
                )
                row = await cursor.fetchone()
        body = "db connection %d" % row[1]
    else:
        body = "unknown"
    body = "%s %.0fms\n" % (body, (time.time() - start) * 1000.0)
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send({"type": "http.response.body", "body": body.encode()})
