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
__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
__license__ = "Apache License, Version 2.0"

from . import system


class MockManager(object):
    def __init__(self, plugin_path="."):
        self.plugin_path = plugin_path

    def get_plugin_path_by_id(self, plugin_id):
        return self.plugin_path


class MockPlugin(object):
    def __init__(self, plugin_path="."):
        self.id = "pt.hive.colony.plugins.api.at"
        self.ssl_plugin = None
        self.client_http_plugin = None
        self.manager = MockManager(plugin_path=plugin_path)
        self.messages = []

    def debug(self, message):
        self.messages.append(message)


class MockHTTPResponse(object):
    def __init__(self, received_message="", status_code=200):
        self.received_message = received_message
        self.status_code = status_code


class MockHTTPClient(object):
    def __init__(self, received_message="", status_code=200):
        self.received_message = received_message
        self.status_code = status_code
        self.requests = []
        self.opened = False

    def is_open(self):
        return self.opened

    def open(self):
        self.opened = True

    def fetch_url(
        self, url, method, parameters, content_type_charset=None, contents=None
    ):
        self.requests.append((url, method, contents))
        return MockHTTPResponse(
            received_message=self.received_message, status_code=self.status_code
        )


class MockClientHTTPPlugin(object):
    def __init__(self, http_client=None):
        self.http_client = MockHTTPClient() if http_client is None else http_client

    def create_client(self, parameters):
        return self.http_client


class MockATClient(system.ATClient):
    def _gen_envelope_v1(self, document_payload, namespace=None):
        return document_payload

    def _gen_envelope_v2(self, document_payload, namespace=None):
        return document_payload
