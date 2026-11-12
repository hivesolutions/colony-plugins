import sys, asyncio, websockets


async def main(port):
    results = []
    for index in range(8):
        try:
            async with websockets.connect("ws://127.0.0.1:%s/ws/pos" % port) as socket:
                await socket.recv()
                results.append("ok")
        except Exception as exception:
            results.append(
                str(
                    getattr(
                        getattr(exception, "response", None),
                        "status_code",
                        exception.__class__.__name__,
                    )
                )
            )
    print(port, " ".join(results))


asyncio.run(main(sys.argv[1]))
