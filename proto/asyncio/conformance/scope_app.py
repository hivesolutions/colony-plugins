"""
Bare ASGI application that records what the server hands to it (the
scope, the body messages, the lifespan events), so that the servers
can be compared against the ASGI specification and against each other.
"""

import os
import json

TRACE = os.environ.get("TRACE", "/tmp/scope_trace.jsonl")


def _record(kind, value):
    with open(TRACE, "a") as file:
        file.write(json.dumps(dict(kind=kind, value=value), default=repr) + "\n")


def _scope(scope):
    value = dict()
    for key, item in scope.items():
        if key == "headers":
            item = [
                (name.decode("latin-1"), data.decode("latin-1")) for name, data in item
            ]
        elif isinstance(item, bytes):
            item = item.decode("latin-1")
        elif key == "state":
            item = sorted(item.keys())
        value[key] = item
    return value


async def app(scope, receive, send):
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            _record("lifespan", message["type"])
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
    if scope["type"] == "websocket":
        message = await receive()
        _record("websocket", dict(scope=_scope(scope), first=message["type"]))
        await send({"type": "websocket.accept"})
        message = await receive()
        await send(
            {"type": "websocket.send", "text": "echo:" + message.get("text", "")}
        )
        await send({"type": "websocket.close", "code": 1000})
        return
    chunks = []
    while True:
        message = await receive()
        chunks.append(len(message.get("body", b"")))
        if not message.get("more_body", False):
            break
    _record(
        "http",
        dict(scope=_scope(scope), body_messages=len(chunks), body_bytes=sum(chunks)),
    )
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain"), (b"x-probe", b"1")],
        }
    )
    await send({"type": "http.response.body", "body": b"x" * 2048, "more_body": True})
    await send({"type": "http.response.body", "body": b"y" * 2048})
