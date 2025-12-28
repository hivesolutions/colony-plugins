#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import io


class MockPlugin(object):
    def __init__(self):
        self.manager = MockManager()
        self.rest_plugin = MockRESTPlugin()

    def debug(self, message):
        pass

    def info(self, message):
        pass

    def warning(self, message):
        pass


class MockManager(object):
    def __init__(self):
        self._version = "1.0.0"
        self._environment = "test"
        self._development = True

    def get_version(self):
        return self._version

    def get_environment(self):
        return self._environment

    def is_development(self):
        return self._development


class MockRESTPlugin(object):
    def __init__(self):
        self.handled_requests = []
        self.raise_exception = False
        self.exception = None

    def handle_request(self, request):
        self.handled_requests.append(request)
        if self.raise_exception:
            raise self.exception or Exception("Mock exception")


class MockStartResponse(object):
    def __init__(self):
        self.status = None
        self.response_headers = None
        self.exc_info = None

    def __call__(self, status, response_headers, exc_info=None):
        self.status = status
        self.response_headers = response_headers
        self.exc_info = exc_info


class MockMediatedHandler(object):
    def __init__(self, data, chunk_size=4096):
        self.data = data
        self.chunk_size = chunk_size
        self.offset = 0

    def get_size(self):
        return len(self.data)

    def get_chunk(self, size):
        if self.offset >= len(self.data):
            return None
        chunk = self.data[self.offset : self.offset + size]
        self.offset += size
        return chunk


def create_environ(
    method="GET",
    path="/test",
    query_string="",
    content_type="",
    content_length=0,
    body=b"",
    headers=None,
    script_name="",
    url_scheme="http",
):
    """
    Creates a WSGI environ dictionary for testing.

    :param method: HTTP method (GET, POST, etc.)
    :param path: Request path
    :param query_string: Query string without leading ?
    :param content_type: Content-Type header
    :param content_length: Content-Length header
    :param body: Request body as bytes
    :param headers: Dictionary of additional headers
    :param script_name: SCRIPT_NAME value
    :param url_scheme: wsgi.url_scheme (http or https)
    :return: WSGI environ dictionary
    """
    headers = headers or {}

    environ = {
        "REQUEST_METHOD": method,
        "SCRIPT_NAME": script_name,
        "PATH_INFO": path,
        "QUERY_STRING": query_string,
        "CONTENT_TYPE": content_type,
        "CONTENT_LENGTH": str(content_length) if content_length else "",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": url_scheme,
        "wsgi.input": io.BytesIO(body),
        "wsgi.errors": io.StringIO(),
        "wsgi.multithread": True,
        "wsgi.multiprocess": True,
        "wsgi.run_once": False,
    }

    for key, value in headers.items():
        header_key = "HTTP_" + key.upper().replace("-", "_")
        environ[header_key] = value

    return environ


def create_multipart_body(fields, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW"):
    """
    Creates a multipart/form-data body for testing.

    :param fields: List of tuples (name, value) or (name, filename, content, content_type)
    :param boundary: Boundary string
    :return: Tuple of (body bytes, content_type string)
    """
    body_parts = []

    for field in fields:
        if len(field) == 2:
            name, value = field
            part = (
                b"--"
                + boundary.encode()
                + b"\r\n"
                + b'Content-Disposition: form-data; name="'
                + name.encode()
                + b'"\r\n\r\n'
                + value.encode()
                + b"\r\n"
            )
        else:
            name, filename, content, content_type = field
            if isinstance(content, str):
                content = content.encode()
            part = (
                b"--"
                + boundary.encode()
                + b"\r\n"
                + b'Content-Disposition: form-data; name="'
                + name.encode()
                + b'"; filename="'
                + filename.encode()
                + b'"\r\n'
                + b"Content-Type: "
                + content_type.encode()
                + b"\r\n\r\n"
                + content
                + b"\r\n"
            )
        body_parts.append(part)

    body = b"".join(body_parts) + b"--" + boundary.encode() + b"--\r\n"
    content_type = "multipart/form-data; boundary=" + boundary

    return body, content_type
