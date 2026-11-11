#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Throwaway prototype of the ASGI adapter of the Colony framework, the
async sibling of colony_wsgi (imported only under Python 3.7+).

Sync actions keep running unchanged in a bounded thread pool, so the
event loop is never blocked by them, while async (async def) actions
are awaited on the event loop between the dispatch half and the
response half of the WSGI plugin handling. WebSocket connections are
routed to the handlers exposed by the plugins.

Usage (netius in asyncio mode, the only one with real asyncio tasks):

    $ ASYNCIO=1 PORT=8080 python colony_asgi.py
"""

import io
import os
import re
import sys
import json
import time
import asyncio
import logging
import concurrent.futures
import urllib.parse

import colony
import colony_wsgi

from entity_manager import system_a

plugin_manager = colony_wsgi.plugin_manager

WORKERS = colony.conf("ASGI_WORKERS", 16, cast=int)
""" The number of threads that run the sync actions, bounds the
number of sync actions (and DB connections) in flight """

EXECUTOR = concurrent.futures.ThreadPoolExecutor(
    max_workers=WORKERS, thread_name_prefix="colony-asgi"
)

WEBSOCKETS = None


def get_wsgi_plugin():
    wsgi_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.wsgi")
    if not wsgi_plugin or not wsgi_plugin.is_loaded():
        raise colony.PluginSystemException("WSGI plugin not loaded")
    return wsgi_plugin


def get_websockets():
    global WEBSOCKETS
    if WEBSOCKETS != None:
        return WEBSOCKETS
    WEBSOCKETS = []
    for plugin in plugin_manager.get_all_plugins():
        if not plugin.is_loaded():
            continue
        if not hasattr(plugin, "get_websocket_patterns"):
            continue
        for pattern, handler in plugin.get_websocket_patterns():
            WEBSOCKETS.append((re.compile("^" + pattern + "$"), handler))
    return WEBSOCKETS


async def application(scope, receive, send):
    type = scope["type"]
    if type == "lifespan":
        return await handle_lifespan(scope, receive, send)
    if type == "websocket":
        return await handle_websocket(scope, receive, send)
    if type == "http":
        return await handle_http(scope, receive, send)


async def handle_lifespan(scope, receive, send):
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send(dict(type="lifespan.startup.complete"))
        elif message["type"] == "lifespan.shutdown":
            EXECUTOR.shutdown(wait=False)
            await send(dict(type="lifespan.shutdown.complete"))
            return


async def handle_http(scope, receive, send):
    loop = asyncio.get_running_loop()
    wsgi_plugin = get_wsgi_plugin()
    prefix = colony_wsgi.prefix
    alias = colony_wsgi.get_alias()
    rewrite = colony_wsgi.get_rewrite()

    body = await read_body(receive)
    environ = build_environ(scope, body)
    response = dict()

    def start_response(status, headers):
        response["status"] = status
        response["headers"] = headers

    def handle():
        result = wsgi_plugin.handle(environ, start_response, prefix, alias, rewrite)
        if hasattr(result, "coroutine"):
            return result
        return list(result)

    # dispatches the request in the thread pool, for a sync action this
    # runs the complete handling (as today), for an async action it stops
    # right after the routing and validation with the coroutine pending
    result = await loop.run_in_executor(EXECUTOR, handle)

    if hasattr(result, "coroutine"):
        request = result
        rest_request = request.rest_request
        error = None
        token = system_a.ASYNC.set(True)
        try:
            await request.coroutine
        except BaseException as exception:
            error = exception
            rest_request.except_handle(exception)
        else:
            rest_request.post_handle()
        finally:
            system_a.ASYNC.reset(token)
        environ["colony.asgi.request"] = request
        environ["colony.asgi.error"] = error
        result = await loop.run_in_executor(EXECUTOR, handle)

    status = int(response["status"].split(" ", 1)[0])
    headers = [
        (name.lower().encode("latin-1"), str(value).encode("latin-1"))
        for name, value in response["headers"]
    ]
    await send(dict(type="http.response.start", status=status, headers=headers))
    for chunk in result:
        if not chunk:
            continue
        await send(dict(type="http.response.body", body=chunk, more_body=True))
    await send(dict(type="http.response.body", body=b"", more_body=False))


async def handle_websocket(scope, receive, send):
    path = scope["path"]
    handler = None
    for regex, _handler in get_websockets():
        if regex.match(path):
            handler = _handler
            break
    if not handler:
        await receive()
        await send(dict(type="websocket.close", code=1008))
        return
    websocket = WebSocket(scope, receive, send)
    token = system_a.ASYNC.set(True)
    try:
        await handler(websocket)
    finally:
        system_a.ASYNC.reset(token)


async def read_body(receive):
    chunks = []
    while True:
        message = await receive()
        chunks.append(message.get("body", b""))
        if not message.get("more_body", False):
            break
    return b"".join(chunks)


def build_environ(scope, body):
    path = scope.get("path", "/")
    path = path.encode("utf-8").decode("latin-1")
    server = scope.get("server") or ("localhost", 80)
    client = scope.get("client") or ("127.0.0.1", 0)
    environ = dict(
        REQUEST_METHOD=scope["method"],
        SCRIPT_NAME="",
        PATH_INFO=path,
        QUERY_STRING=scope.get("query_string", b"").decode("latin-1"),
        CONTENT_TYPE="",
        CONTENT_LENGTH=str(len(body)),
        SERVER_NAME=server[0],
        SERVER_PORT=str(server[1]),
        SERVER_PROTOCOL="HTTP/%s" % scope.get("http_version", "1.1"),
        SERVER_SOFTWARE="colony-asgi",
        REMOTE_ADDR=client[0],
        REMOTE_PORT=str(client[1]),
    )
    environ["wsgi.version"] = (1, 0)
    environ["wsgi.url_scheme"] = scope.get("scheme", "http")
    environ["wsgi.input"] = io.BytesIO(body)
    environ["wsgi.errors"] = sys.stderr
    environ["wsgi.multithread"] = True
    environ["wsgi.multiprocess"] = False
    environ["wsgi.run_once"] = False
    environ["colony.asgi"] = True
    for name, value in scope.get("headers", []):
        name = name.decode("latin-1").upper().replace("-", "_")
        value = value.decode("latin-1")
        if name == "CONTENT_TYPE":
            environ["CONTENT_TYPE"] = value
            continue
        if name == "CONTENT_LENGTH":
            continue
        key = "HTTP_" + name
        environ[key] = environ[key] + "," + value if key in environ else value
    return environ


class WebSocket(object):

    def __init__(self, scope, receive, send):
        self.scope = scope
        self._receive = receive
        self._send = send
        self.executor = EXECUTOR
        query = scope.get("query_string", b"").decode("latin-1")
        self.query = dict(urllib.parse.parse_qsl(query))

    async def accept(self):
        message = await self._receive()
        if not message["type"] == "websocket.connect":
            raise RuntimeError("unexpected message '%s'" % message["type"])
        await self._send(dict(type="websocket.accept"))

    async def receive(self):
        message = await self._receive()
        if message["type"] == "websocket.disconnect":
            return None
        return message.get("text", message.get("bytes", None))

    async def send_text(self, text):
        await self._send(dict(type="websocket.send", text=text))

    async def send_json(self, value):
        await self.send_text(json.dumps(value))

    async def close(self, code=1000):
        await self._send(dict(type="websocket.close", code=code))


def main():
    import netius.servers

    host = colony.conf("HOST", "127.0.0.1")
    port = colony.conf("PORT", 8080, cast=int)
    poll_timeout = colony.conf("POLL_TIMEOUT", 0.002, cast=float)
    server = netius.servers.ASGIServer(
        app=application,
        asyncio=True,
        poll_timeout=poll_timeout,
        level=logging.WARNING,
    )
    server.serve(host=host, port=port, env=True)


if __name__ == "__main__":
    main()
