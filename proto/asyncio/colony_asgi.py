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

It is a plain ASGI application, so any ASGI server runs it, either
through the SERVER variable (netius, uvicorn or hypercorn, as with
colony_wsgi) or directly through the server's own command line, with
CHILDREN setting the number of worker processes for every server:

    $ SERVER=netius PORT=8080 python colony_asgi.py
    $ SERVER=uvicorn CHILDREN=4 PORT=8080 python colony_asgi.py
    $ uvicorn colony_asgi:application --port 8080 --workers 4
    $ hypercorn colony_asgi:application --bind 127.0.0.1:8080
"""

import io
import os
import re
import sys
import json
import time
import zlib
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

ENCODING = colony.conf("SERVER_ENCODING", None)
""" The encoding of the responses (gzip compresses them), applied by the
application itself so that every ASGI server serves the same bytes (the
same variable that today makes netius compress them) """

COMPRESSED_LIMIT = colony.conf("COMPRESSED_LIMIT", 5242880, cast=int)
""" The maximum size of a response that is compressed (as in netius) """

EXECUTOR = concurrent.futures.ThreadPoolExecutor(
    max_workers=WORKERS, thread_name_prefix="colony-asgi"
)

WEBSOCKETS = None


def load_plugins():
    """
    Loads every plugin up front, as Colony loads most of them lazily on
    their first use, so that the first request of a worker is not delayed,
    a worker that is first reached by a WebSocket has its handlers and the
    workers forked after the import (netius, gunicorn preload) share the
    loaded plugins instead of loading them one by one.
    """

    for plugin in plugin_manager.get_all_plugins():
        if plugin.is_loaded():
            continue
        plugin_manager.load_plugin(plugin.id, type="full_load")


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
            await system_a.close_a()
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
    headers, body = encode(scope, status, list(response["headers"]), b"".join(result))
    headers = [
        (name.lower().encode("latin-1"), str(value).encode("latin-1"))
        for name, value in headers
    ]
    await send(dict(type="http.response.start", status=status, headers=headers))
    await send(dict(type="http.response.body", body=body, more_body=False))


def encode(scope, status, headers, body):
    """
    Compresses the response in the application, with the rules netius
    applies today: gzip accepted by the client, HTTP/1.1 or newer, a non
    empty body up to the limit and no ranges (as their offsets refer to
    the uncompressed content).
    """

    if not ENCODING == "gzip":
        return headers, body
    if not body or status in (204, 304) or len(body) > COMPRESSED_LIMIT:
        return headers, body
    if scope.get("http_version", "1.1") in ("0.9", "1.0"):
        return headers, body
    names = dict((name.lower(), value) for name, value in headers)
    if "content-encoding" in names or "content-range" in names:
        return headers, body
    if names.get("accept-ranges", None) == "bytes":
        return headers, body
    accept = get_header(scope, b"accept-encoding") or ""
    encodings = [value.split(";", 1)[0].strip() for value in accept.split(",")]
    if not "gzip" in encodings:
        return headers, body
    compressor = zlib.compressobj(6, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    body = compressor.compress(body) + compressor.flush()
    headers = [item for item in headers if not item[0].lower() == "content-length"]
    headers.append(("Content-Encoding", "gzip"))
    headers.append(("Content-Length", str(len(body))))
    headers.append(("Vary", "Accept-Encoding"))
    return headers, body


def get_header(scope, name):
    for _name, value in scope.get("headers", []):
        if _name.lower() == name:
            return value.decode("latin-1")
    return None


def get_scheme(scope, default="http"):
    """
    Resolves the scheme of the request from the forwarded protocol, as
    netius does today for the WSGI runtime, never from what the server
    may or may not have applied (servers differ, the key is optional).
    """

    forwarded = get_header(scope, b"x-forwarded-proto")
    if forwarded:
        forwarded = forwarded.split(",", 1)[0].strip().lower()
    if forwarded and scope["type"] == "websocket":
        return "wss" if forwarded == "https" else "ws"
    return forwarded or scope.get("scheme", None) or default


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
    environ["wsgi.url_scheme"] = get_scheme(scope)
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
        self.scheme = get_scheme(scope, default="ws")
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


load_plugins()


def serve(server="netius", host="127.0.0.1", port=8080, children=0):
    _globals = globals()
    method = _globals.get("serve_" + server, None)
    if not method:
        raise colony.PluginSystemException("ASGI server '%s' not supported" % server)
    version_method = _globals.get("version_" + server, None)
    server_version = version_method() if version_method else None
    sys.stderr.write(
        "Starting Colony ASGI with '%s' version '%s' ...\n" % (server, server_version)
    )
    method(host, port, children=children)


def serve_netius(host, port, children=0):
    import netius.servers

    # the asyncio mode is the only one that runs real asyncio tasks, the
    # (short) poll timeout works around the stepping of its asyncio loop
    poll_timeout = colony.conf("POLL_TIMEOUT", 0.002, cast=float)
    server = netius.servers.ASGIServer(
        app=application,
        asyncio=True,
        poll_timeout=poll_timeout,
        children=children,
        level=logging.WARNING,
    )
    server.serve(host=host, port=port, env=True)


def serve_uvicorn(host, port, children=0):
    import uvicorn

    # multiple workers are spawned (not forked) by uvicorn and import
    # the application by its name, so each one loads its own plugins
    app = "colony_asgi:application" if children > 1 else application
    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=children or None,
        proxy_headers=False,
        log_level="warning",
        access_log=False,
    )


def serve_hypercorn(host, port, children=0):
    import hypercorn.run
    import hypercorn.config
    import hypercorn.asyncio

    config = hypercorn.config.Config()
    config.bind = ["%s:%d" % (host, port)]
    config.accesslog = None
    config.loglevel = "WARNING"
    if children > 1:
        config.workers = children
        config.application_path = "colony_asgi:application"
        hypercorn.run.run(config)
    else:
        asyncio.run(hypercorn.asyncio.serve(application, config))


def version_netius():
    import netius

    return netius.VERSION


def version_uvicorn():
    import uvicorn

    return uvicorn.__version__


def version_hypercorn():
    import importlib.metadata

    return importlib.metadata.version("hypercorn")


def main():
    server = colony.conf("SERVER", "netius")
    host = colony.conf("HOST", "127.0.0.1")
    port = colony.conf("PORT", 8080, cast=int)
    children = colony.conf("CHILDREN", 0, cast=int)
    serve(server=server, host=host, port=port, children=children)


if __name__ == "__main__":
    main()
