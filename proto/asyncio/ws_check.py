"""
Checks the WebSocket endpoints of the prototype: the progress of a
long sync job and the POS stock events, while plain requests keep
being answered by the same process.
"""

import time
import json
import asyncio
import urllib.request

import websockets

BASE = "127.0.0.1:18700"


def get(path):
    start = time.time()
    with urllib.request.urlopen("http://%s%s" % (BASE, path), timeout=10) as response:
        response.read()
    return (time.time() - start) * 1000.0


async def progress():
    start = time.time()
    async with websockets.connect("ws://%s/ws/progress?steps=10" % BASE) as socket:
        async for message in socket:
            print("  progress +%4.0fms %s" % ((time.time() - start) * 1000.0, message))
            if json.loads(message).get("done"):
                break


async def fast_requests(count=20):
    loop = asyncio.get_running_loop()
    timings = []
    for _index in range(count):
        timings.append(await loop.run_in_executor(None, get, "/omni_proto/fast.json"))
        await asyncio.sleep(0.1)
    print(
        "  %d fast requests during the job: max %.1fms, avg %.1fms"
        % (count, max(timings), sum(timings) / len(timings))
    )


async def pos():
    loop = asyncio.get_running_loop()
    async with websockets.connect("ws://%s/ws/pos" % BASE) as socket:
        print("  pos %s" % await socket.recv())
        for delta in (-1, -2):
            start = time.time()
            await loop.run_in_executor(
                None, get, "/omni_proto/stock_bump.json?id=405&delta=%d" % delta
            )
            message = await socket.recv()
            print("  pos +%.1fms %s" % ((time.time() - start) * 1000.0, message))


async def main():
    print("== long task progress (sync job in the pool, socket on the loop)")
    await asyncio.gather(progress(), fast_requests())
    print("== live POS events")
    await pos()


asyncio.run(main())
