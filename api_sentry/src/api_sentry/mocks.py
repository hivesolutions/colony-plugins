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

import json


class MockPlugin(object):
    def __init__(self, client_http_plugin=None, json_plugin=None):
        self.client_http_plugin = client_http_plugin or MockClientHTTPPlugin()
        self.json_plugin = json_plugin or MockJSONPlugin()


class MockJSONPlugin(object):
    def dumps(self, object):
        return json.dumps(object, sort_keys=True)


class MockClientHTTPPlugin(object):
    def __init__(self, http_client=None):
        self._http_client = http_client or MockHTTPClient()

    def create_client(self, parameters):
        return self._http_client


class MockHTTPClient(object):
    def __init__(self, responses=None):
        self.responses = responses or []
        self.requests = []
        self.opened = False
        self.closed = False

    def open(self, parameters):
        self.opened = True

    def close(self, parameters):
        self.closed = True

    def fetch_url(self, url, method, **kwargs):
        self.requests.append(dict(url=url, method=method, **kwargs))
        if not self.responses:
            return MockHTTPResponse()
        return self.responses.pop(0)


class MockHTTPResponse(object):
    def __init__(self, status_code=200, headers_map=None, received_message=""):
        self.status_code = status_code
        self.headers_map = headers_map or {}
        self.received_message = received_message


class MockRaisingHTTPClient(MockHTTPClient):
    def fetch_url(self, url, method, **kwargs):
        MockHTTPClient.fetch_url(self, url, method, **kwargs)
        raise RuntimeError("no connection")
