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


class MockPlugin(object):
    def __init__(self):
        self.rest_encoder_plugins = []
        self.rest_service_plugins = []
        self.rpc_service_plugins = []
        self.random_plugin = MockRandomPlugin()
        self.resources_manager_plugin = MockResourcesManagerPlugin()
        self.manager = MockManager()

    def debug(self, message):
        pass

    def info(self, message):
        pass


class MockManager(object):
    def __init__(self):
        self.container = "default"


class MockRandomPlugin(object):
    def __init__(self):
        self._counter = 0

    def generate_random_md5_string(self):
        self._counter += 1
        return "mock_session_id_%d" % self._counter


class MockResourcesManagerPlugin(object):
    def __init__(self):
        self._resources = {}

    def get_resource(self, name):
        return self._resources.get(name, None)

    def set_resource(self, name, value):
        self._resources[name] = value


class MockResource(object):
    def __init__(self, data):
        self.data = data


class MockRequest(object):
    def __init__(self):
        self.uri = "/dynamic/rest/test/path"
        self.original_path = "/dynamic/rest/test/path"
        self.operation_type = "GET"
        self.status_code = 200
        self.content_type = None
        self.content_type_charset = "utf-8"
        self.headers = {}
        self.attributes_map = {}
        self.allow_cookies = True
        self.last_modified_timestamp = None
        self.delayed = False
        self._write_buffer = []
        self._flushed = False
        self._service = MockService()
        self._service_connection = MockServiceConnection()

    def get_method(self):
        return self.operation_type

    def get_header(self, header_name):
        return self.headers.get(header_name, None)

    def set_header(self, header_name, header_value):
        self.headers[header_name] = header_value

    def append_header(self, header_name, header_value):
        if header_name in self.headers:
            self.headers[header_name] = self.headers[header_name] + "; " + header_value
        else:
            self.headers[header_name] = header_value

    def get_attribute(self, attribute_name, default=None):
        return self.attributes_map.get(attribute_name, default)

    def set_attribute(self, attribute_name, attribute_value):
        self.attributes_map[attribute_name] = attribute_value

    def get_attributes_list(self):
        return list(self.attributes_map.keys())

    def is_secure(self):
        return False

    def allow_cookies(self):
        self.allow_cookies = True

    def deny_cookies(self):
        self.allow_cookies = False

    def set_max_age(self, max_age):
        self.max_age = max_age

    def read(self):
        return ""

    def write(self, data):
        self._write_buffer.append(data)

    def flush(self):
        self._flushed = True

    def parse_post_attributes(self):
        pass

    def execute_background(self, callable, retries=0, timeout=0.0, timestamp=None):
        callable()

    def get_service(self):
        return self._service

    def get_service_connection(self):
        return self._service_connection


class MockService(object):
    def __init__(self):
        pass

    def process_request(self, request, service_connection):
        pass


class MockServiceConnection(object):
    def __init__(self):
        self.connection_address = ("127.0.0.1", 8080)


class MockRESTServicePlugin(object):
    def __init__(self, plugin_id, routes):
        self.id = plugin_id
        self._routes = routes

    def get_routes(self):
        return self._routes

    def handle_rest_request(self, rest_request):
        pass


class MockRESTEncoderPlugin(object):
    def __init__(self, encoder_name, content_type):
        self._encoder_name = encoder_name
        self._content_type = content_type

    def get_encoder_name(self):
        return self._encoder_name

    def get_content_type(self):
        return self._content_type

    def encode_value(self, value):
        return str(value)


class MockRPCServicePlugin(object):
    def __init__(self, service_id, service_alias=None):
        self._service_id = service_id
        self._service_alias = service_alias or []
        self._methods = []
        self._methods_alias = {}
        self._metadata = {}

    def get_service_id(self):
        return self._service_id

    def get_service_alias(self):
        return self._service_alias

    def get_available_rpc_methods(self):
        return self._methods

    def get_rpc_methods_alias(self):
        return self._methods_alias

    def contains_metadata_key(self, key):
        return key in self._metadata

    def get_metadata_key(self, key):
        return self._metadata.get(key, [])

    def add_method(self, method, alias=None):
        self._methods.append(method)
        self._methods_alias[method] = alias or []
