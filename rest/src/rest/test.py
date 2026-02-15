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

import time

import colony

from . import system
from . import exceptions
from . import mocks


class RESTTest(colony.Test):
    """
    The REST infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            RESTSystemTestCase,
            RESTRequestTestCase,
            RESTSessionTestCase,
            CookieTestCase,
            ExceptionsTestCase,
            RegressionTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class RESTSystemTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "REST System test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self._saved_storage = system.RESTSession.STORAGE
        system.RESTSession.STORAGE = {}

    def tearDown(self):
        system.RESTSession.STORAGE = self._saved_storage

    def test_initialization(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        self.assertEqual(rest.matching_regex_list, [])
        self.assertEqual(rest.matching_regex_base_values_map, {})
        self.assertEqual(rest.rest_service_routes_map, {})
        self.assertEqual(rest.plugin_id_plugin_map, {})
        self.assertEqual(rest.regex_index_plugin_id_map, {})
        self.assertEqual(rest.service_methods, [])
        self.assertEqual(rest.service_methods_map, {})

    def test_get_handler_name(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        self.assertEqual(rest.get_handler_name(), "rest")

    def test_get_handler_port(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        self.assertEqual(rest.get_handler_port(), 80)

    def test_get_handler_properties(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        properties = rest.get_handler_properties()
        self.assertEqual(properties["handler_base_filename"], "/dynamic/rest/")
        self.assertEqual(properties["handler_extension"], "py")

    def test_is_request_handler(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        mock_request = mocks.MockRequest()
        mock_request.uri = "/dynamic/rest/test/path"
        self.assertEqual(rest.is_request_handler(mock_request), True)

        mock_request.uri = "/other/path"
        self.assertEqual(rest.is_request_handler(mock_request), False)

        mock_request.uri = "/dynamic/other"
        self.assertEqual(rest.is_request_handler(mock_request), False)

    def test_load_rest_service_plugin(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        service_plugin = mocks.MockRESTServicePlugin(
            "test.plugin.id", ["test/.*", "other/.*"]
        )
        rest.load_rest_service_plugin(service_plugin)

        self.assertIn("test.plugin.id", rest.rest_service_routes_map)
        self.assertEqual(
            rest.rest_service_routes_map["test.plugin.id"], ["test/.*", "other/.*"]
        )
        self.assertEqual(rest.plugin_id_plugin_map["test.plugin.id"], service_plugin)

    def test_unload_rest_service_plugin(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        service_plugin = mocks.MockRESTServicePlugin(
            "test.plugin.id", ["test/.*", "other/.*"]
        )
        rest.load_rest_service_plugin(service_plugin)
        self.assertIn("test.plugin.id", rest.rest_service_routes_map)

        rest.unload_rest_service_plugin(service_plugin)
        self.assertNotIn("test.plugin.id", rest.rest_service_routes_map)
        self.assertNotIn("test.plugin.id", rest.plugin_id_plugin_map)

    def test_clear_sessions(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        session_c = rest.session_c
        initial_count = session_c.count()
        session_c.new("test_session_clear")
        self.assertEqual(session_c.count(), initial_count + 1)

        rest.clear_sessions()
        self.assertEqual(session_c.count(), 0)

    def test_get_session(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        session_c = rest.session_c
        session_c.new("test_session_get")
        retrieved = rest.get_session("test_session_get")
        self.assertEqual(retrieved.session_id, "test_session_get")

        missing = rest.get_session("nonexistent")
        self.assertEqual(missing, None)


class RESTRequestTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "REST Request test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self._saved_storage = system.RESTSession.STORAGE
        system.RESTSession.STORAGE = {}

    def tearDown(self):
        system.RESTSession.STORAGE = self._saved_storage

    def test_initialization(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()

        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.rest, rest)
        self.assertEqual(rest_request.request, mock_request)
        self.assertEqual(rest_request.flushed, False)
        self.assertEqual(rest_request.redirected, False)
        self.assertEqual(rest_request.rest_encoder_plugins, [])
        self.assertEqual(rest_request.rest_encoder_plugins_map, {})
        self.assertEqual(rest_request.parameters_map, {})

    def test_resource_name(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_resource_name("mvc")
        self.assertEqual(rest_request.get_resource_name(), "mvc")

    def test_path_list(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_path_list(["users", "123"])
        self.assertEqual(rest_request.get_path_list(), ["users", "123"])

    def test_encoder_name(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_encoder_name("json")
        self.assertEqual(rest_request.get_encoder_name(), "json")

    def test_content_type(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_content_type("application/json")
        self.assertEqual(rest_request.get_content_type(), "application/json")

    def test_status_code(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_status_code(404)
        self.assertEqual(rest_request.get_status_code(), 404)

    def test_is_get(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.operation_type = "GET"
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.is_get(), True)
        self.assertEqual(rest_request.is_post(), False)

    def test_is_post(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.operation_type = "POST"
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.is_post(), True)
        self.assertEqual(rest_request.is_get(), False)

    def test_get_method(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.operation_type = "PUT"
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.get_method(), "PUT")

    def test_get_path(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.original_path = "/dynamic/rest/test/path?query=value"
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.get_path(), "/dynamic/rest/test/path")

    def test_attributes(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_attribute("key1", "value1")
        self.assertEqual(rest_request.get_attribute("key1"), "value1")
        self.assertEqual(rest_request.get_attribute("missing", "default"), "default")

    def test_parameters(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_parameter("param1", "value1")
        self.assertEqual(rest_request.get_parameter("param1"), "value1")
        self.assertEqual(rest_request.get_parameter("missing"), None)

    def test_headers(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.headers["Content-Type"] = "application/json"
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.get_header("Content-Type"), "application/json")
        self.assertEqual(rest_request.get_header("Missing"), None)

        rest_request.set_header("X-Custom", "custom-value")
        self.assertEqual(rest_request.get_header("X-Custom"), "custom-value")

    def test_result_translated(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_result_translated('{"key": "value"}')
        self.assertEqual(rest_request.get_result_translated(), '{"key": "value"}')

    def test_redirect(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.redirect("/new/location")

        self.assertEqual(rest_request.is_redirected(), True)
        self.assertEqual(mock_request.status_code, 302)
        self.assertEqual(mock_request.headers.get("Location"), "/new/location")

    def test_redirect_custom_status(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.redirect("/new/location", status_code=301)

        self.assertEqual(rest_request.is_redirected(), True)
        self.assertEqual(mock_request.status_code, 301)

    def test_flush(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.set_content_type("text/plain")
        rest_request.set_result_translated("Hello, World!")
        rest_request.flush()

        self.assertEqual(rest_request.is_flushed(), True)
        self.assertEqual(mock_request._flushed, True)
        self.assertEqual(mock_request.content_type, "text/plain")

    def test_start_session(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        session = rest_request.start_session()

        self.assertNotEqual(session, None)
        self.assertNotEqual(session.session_id, None)
        self.assertEqual(rest_request.get_session(block=False), session)

    def test_start_session_with_id(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        session = rest_request.start_session(session_id="custom_session_id")

        self.assertEqual(session.session_id, "custom_session_id")

    def test_start_session_no_duplicate(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        session1 = rest_request.start_session()
        session2 = rest_request.start_session()

        self.assertEqual(session1, session2)

    def test_start_session_force(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        session1 = rest_request.start_session()
        session2 = rest_request.start_session(force=True)

        self.assertNotEqual(session1.session_id, session2.session_id)

    def test_session_attributes(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.start_session()

        rest_request.set_s("username", "testuser")
        self.assertEqual(rest_request.get_s("username"), "testuser")
        self.assertEqual(rest_request.get_s("missing", "default"), "default")

        rest_request.unset_s("username")
        self.assertEqual(rest_request.get_s("username"), None)

    def test_get_session_attributes_map(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        session = rest_request.start_session()
        session.set_attribute("key1", "value1")
        session.set_attribute("key2", "value2")

        attrs = rest_request.get_session_attributes_map()
        self.assertEqual(attrs["key1"], "value1")
        self.assertEqual(attrs["key2"], "value2")

    def test_touch(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        session = rest_request.start_session(timeout=100)
        original_expire = session.expire_time

        time.sleep(0.1)
        rest_request.touch()

        self.assertTrue(session.expire_time >= original_expire)

    def test_update_session_from_cookie(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        session = system.RESTSession.new("existing_session_id")
        session.set_attribute("test_key", "test_value")

        mock_request = mocks.MockRequest()
        mock_request.headers["Cookie"] = "session_id=existing_session_id"
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.update_session()

        self.assertNotEqual(rest_request.get_session(block=False), None)
        self.assertEqual(
            rest_request.get_session(block=False).session_id, "existing_session_id"
        )
        self.assertEqual(rest_request.get_s("test_key"), "test_value")

    def test_update_session_from_attribute(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        session = system.RESTSession.new("attr_session_id")
        session.set_attribute("user", "john")

        mock_request = mocks.MockRequest()
        mock_request.attributes_map["session_id"] = "attr_session_id"
        rest_request = system.RESTRequest(rest, mock_request)

        rest_request.update_session()

        self.assertNotEqual(rest_request.get_session(block=False), None)
        self.assertEqual(rest_request.get_s("user"), "john")

    def test_ensure_session(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        result = rest_request.ensure_session()
        self.assertEqual(result, None)

        session = rest_request.start_session()
        result = rest_request.ensure_session()
        self.assertEqual(result, session)

    def test_session_property(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.session, None)

        session = rest_request.start_session()
        self.assertEqual(rest_request.session, session)

    def test_get_connection_address(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address(resolve=False, cleanup=False)
        self.assertEqual(address, "127.0.0.1")
        self.assertEqual(port, 8080)

    def test_get_connection_address_resolve_forwarded(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.headers["X-Forwarded-For"] = "203.0.113.50"
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address()
        self.assertEqual(address, "203.0.113.50")
        self.assertEqual(port, 8080)

    def test_get_connection_address_resolve_client_ip(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.headers["X-Client-IP"] = "198.51.100.10"
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address()
        self.assertEqual(address, "198.51.100.10")
        self.assertEqual(port, 8080)

    def test_get_connection_address_resolve_real_ip(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.headers["X-Real-IP"] = "10.0.0.1"
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address()
        self.assertEqual(address, "10.0.0.1")
        self.assertEqual(port, 8080)

    def test_get_connection_address_resolve_priority(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.headers["X-Forwarded-For"] = "203.0.113.50"
        mock_request.headers["X-Client-IP"] = "198.51.100.10"
        mock_request.headers["X-Real-IP"] = "10.0.0.1"
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address()
        self.assertEqual(address, "10.0.0.1")
        self.assertEqual(port, 8080)

    def test_get_connection_address_forwarded_multiple(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.headers["X-Forwarded-For"] = "203.0.113.50, 70.41.3.18, 150.172.238.178"
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address()
        self.assertEqual(address, "203.0.113.50")
        self.assertEqual(port, 8080)

    def test_get_connection_address_cleanup_ipv6_mapped(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request._service_connection.connection_address = ("::ffff:192.168.1.1", 9090)
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address(resolve=False)
        self.assertEqual(address, "192.168.1.1")
        self.assertEqual(port, 9090)

    def test_get_connection_address_no_cleanup(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request._service_connection.connection_address = ("::ffff:192.168.1.1", 9090)
        rest_request = system.RESTRequest(rest, mock_request)

        address, port = rest_request.get_connection_address(resolve=False, cleanup=False)
        self.assertEqual(address, "::ffff:192.168.1.1")
        self.assertEqual(port, 9090)

    def test_get_address(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.get_address(resolve=False, cleanup=False), "127.0.0.1")

    def test_get_address_with_resolve(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        mock_request.headers["X-Forwarded-For"] = "203.0.113.50"
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.get_address(), "203.0.113.50")

    def test_get_port(self):
        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)
        mock_request = mocks.MockRequest()
        rest_request = system.RESTRequest(rest, mock_request)

        self.assertEqual(rest_request.get_port(), 8080)


class RESTSessionTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "REST Session test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self._saved_storage = system.RESTSession.STORAGE
        system.RESTSession.STORAGE = {}
        system.RESTSession.GC_PENDING = True

    def tearDown(self):
        system.RESTSession.STORAGE = self._saved_storage

    def test_initialization(self):
        session = system.RESTSession("test_session", timeout=100, maximum_timeout=1000)

        self.assertEqual(session.session_id, "test_session")
        self.assertEqual(session.timeout, 100)
        self.assertEqual(session.maximum_timeout, 1000)
        self.assertEqual(session.dirty, True)
        self.assertEqual(session.attributes_map, {})
        self.assertNotEqual(session.expire_time, None)

    def test_new_session(self):
        session = system.RESTSession.new("new_session_id")

        self.assertEqual(session.session_id, "new_session_id")
        self.assertIn("new_session_id", system.RESTSession.STORAGE)

    def test_get_session(self):
        system.RESTSession.new("get_test_session")

        session = system.RESTSession.get_s("get_test_session")
        self.assertNotEqual(session, None)
        self.assertEqual(session.session_id, "get_test_session")

        missing = system.RESTSession.get_s("nonexistent")
        self.assertEqual(missing, None)

    def test_expire_session(self):
        system.RESTSession.new("expire_test_session")
        self.assertIn("expire_test_session", system.RESTSession.STORAGE)

        system.RESTSession.expire("expire_test_session")
        self.assertNotIn("expire_test_session", system.RESTSession.STORAGE)

    def test_count_sessions(self):
        self.assertEqual(system.RESTSession.count(), 0)

        system.RESTSession.new("session1")
        self.assertEqual(system.RESTSession.count(), 1)

        system.RESTSession.new("session2")
        self.assertEqual(system.RESTSession.count(), 2)

    def test_clear_sessions(self):
        system.RESTSession.new("session1")
        system.RESTSession.new("session2")
        self.assertEqual(system.RESTSession.count(), 2)

        system.RESTSession.clear()
        self.assertEqual(system.RESTSession.count(), 0)

    def test_set_attribute(self):
        session = system.RESTSession("attr_test")

        session.set_attribute("username", "john")
        self.assertEqual(session.get_attribute("username"), "john")
        self.assertEqual(session.is_dirty(), True)

    def test_get_attribute_default(self):
        session = system.RESTSession("default_test")

        self.assertEqual(session.get_attribute("missing"), None)
        self.assertEqual(session.get_attribute("missing", "fallback"), "fallback")

    def test_unset_attribute(self):
        session = system.RESTSession("unset_test")

        session.set_attribute("key", "value")
        self.assertEqual(session.get_attribute("key"), "value")

        session.unset_attribute("key")
        self.assertEqual(session.get_attribute("key"), None)

    def test_unset_missing_attribute(self):
        session = system.RESTSession("unset_missing_test")

        session.unset_attribute("nonexistent")

    def test_attributes_map(self):
        session = system.RESTSession("map_test")

        session.set_attributes_map({"key1": "value1", "key2": "value2"})
        attrs = session.get_attributes_map()

        self.assertEqual(attrs["key1"], "value1")
        self.assertEqual(attrs["key2"], "value2")

    def test_is_expired(self):
        session = system.RESTSession("expired_test", timeout=0.1)

        self.assertEqual(session.is_expired(), False)

        time.sleep(0.2)
        self.assertEqual(session.is_expired(), True)

    def test_get_expired_session_returns_none(self):
        system.RESTSession.new("expire_check", timeout=0.1)
        self.assertNotEqual(system.RESTSession.get_s("expire_check"), None)

        time.sleep(0.2)
        self.assertEqual(system.RESTSession.get_s("expire_check"), None)

    def test_dirty_flag(self):
        session = system.RESTSession("dirty_test")

        self.assertEqual(session.is_dirty(), True)

        session.mark(dirty=False)
        self.assertEqual(session.is_dirty(), False)

        session.mark()
        self.assertEqual(session.is_dirty(), True)

    def test_flush(self):
        session = system.RESTSession("flush_test")

        self.assertEqual(session.is_dirty(), True)
        session.flush()
        self.assertEqual(session.is_dirty(), False)

    def test_lock_and_release(self):
        session = system.RESTSession("lock_test")

        session.lock()
        session.release()

    def test_start_session(self):
        session = system.RESTSession("start_test")

        session.start(domain="example.com")

        self.assertNotEqual(session.cookie, None)
        self.assertEqual(session.cookie.get_attribute("session_id"), "start_test")
        self.assertEqual(session.cookie.get_attribute("lang"), "en")
        self.assertNotEqual(session.cookie.get_attribute("expires"), None)

    def test_start_session_localhost(self):
        session = system.RESTSession("localhost_test")

        session.start(domain="localhost")

        self.assertNotEqual(session.cookie, None)
        self.assertEqual(session.cookie.get_attribute("path"), "/")
        self.assertEqual(session.cookie.get_attribute("domain"), None)

    def test_start_session_include_subdomain(self):
        session = system.RESTSession("subdomain_test")

        session.start(domain="example.com", include_sub_domain=True)

        self.assertEqual(session.cookie.get_attribute("domain"), ".example.com")

    def test_start_session_secure(self):
        session = system.RESTSession("secure_test")

        session.start(domain="example.com", secure=True)

        self.assertEqual(session.cookie.get_attribute("secure"), None)

    def test_stop_session(self):
        session = system.RESTSession("stop_test")

        session.stop(domain="example.com")

        self.assertEqual(session.session_id, None)
        self.assertNotEqual(session.cookie, None)
        self.assertEqual(session.cookie.get_attribute("session_id"), "")
        self.assertEqual(
            session.cookie.get_attribute("expires"), "Thu, 01 Jan 1970 00:00:00 GMT"
        )

    def test_update_expire_time(self):
        session = system.RESTSession("update_expire_test", timeout=1000)
        original_expire = session.expire_time

        session.mark(dirty=False)
        session.update_expire_time(dirty_interval=0)

        self.assertTrue(session.expire_time >= original_expire)
        self.assertEqual(session.is_dirty(), True)

    def test_get_remaining(self):
        session = system.RESTSession("remaining_test", timeout=1000)

        remaining = session.get_remaining()
        self.assertTrue(remaining > 0)
        self.assertTrue(remaining <= 1000)

    def test_get_name(self):
        session = system.RESTSession("name_test")

        self.assertEqual(session.get_name(), "RESTSession")

    def test_getstate_setstate(self):
        session = system.RESTSession(
            "serialize_test", timeout=100, maximum_timeout=1000
        )
        session.set_attribute("user", "test")

        state = session.__getstate__()

        new_session = system.RESTSession.__new__(system.RESTSession)
        new_session.__setstate__(state)

        self.assertEqual(new_session.session_id, "serialize_test")
        self.assertEqual(new_session.timeout, 100)
        self.assertEqual(new_session.maximum_timeout, 1000)
        self.assertEqual(new_session.get_attribute("user"), "test")


class CookieTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Cookie test case"

    def test_initialization(self):
        cookie = system.Cookie()

        self.assertEqual(cookie.string_value, None)
        self.assertEqual(cookie.main_attribute_name, None)
        self.assertEqual(cookie.attributes_map, {})

    def test_initialization_with_value(self):
        cookie = system.Cookie("session_id=abc123")

        self.assertEqual(cookie.string_value, "session_id=abc123")

    def test_parse_simple(self):
        cookie = system.Cookie("session_id=abc123")
        cookie.parse()

        self.assertEqual(cookie.get_attribute("session_id"), "abc123")

    def test_parse_multiple(self):
        cookie = system.Cookie("session_id=abc123; lang=en; theme=dark")
        cookie.parse()

        self.assertEqual(cookie.get_attribute("session_id"), "abc123")
        self.assertEqual(cookie.get_attribute("lang"), "en")
        self.assertEqual(cookie.get_attribute("theme"), "dark")

    def test_parse_with_spaces(self):
        cookie = system.Cookie("  session_id=abc123  ;   lang=en  ")
        cookie.parse()

        self.assertEqual(cookie.get_attribute("session_id"), "abc123")
        self.assertEqual(cookie.get_attribute("lang"), "en")

    def test_parse_single_value(self):
        cookie = system.Cookie("session_id=abc123; secure")
        cookie.parse()

        self.assertEqual(cookie.get_attribute("session_id"), "abc123")
        self.assertEqual(cookie.get_attribute("secure"), None)

    def test_parse_invalid(self):
        cookie = system.Cookie(None)

        self.assertRaises(exceptions.InvalidCookie, cookie.parse)

    def test_set_attribute(self):
        cookie = system.Cookie()

        cookie.set_attribute("key", "value")
        self.assertEqual(cookie.get_attribute("key"), "value")

    def test_set_attribute_no_value(self):
        cookie = system.Cookie()

        cookie.set_attribute("secure")
        self.assertEqual(cookie.get_attribute("secure"), None)

    def test_get_attribute_default(self):
        cookie = system.Cookie()

        self.assertEqual(cookie.get_attribute("missing"), None)
        self.assertEqual(cookie.get_attribute("missing", "default"), "default")

    def test_set_main_attribute_name(self):
        cookie = system.Cookie()

        cookie.set_main_attribute_name("session_id")
        self.assertEqual(cookie.main_attribute_name, "session_id")

    def test_serialize_simple(self):
        cookie = system.Cookie()
        cookie.set_attribute("session_id", "abc123")

        serialized = cookie.serialize()
        self.assertIn("session_id=abc123;", serialized)

    def test_serialize_with_main_attribute(self):
        cookie = system.Cookie()
        cookie.set_main_attribute_name("session_id")
        cookie.set_attribute("session_id", "abc123")
        cookie.set_attribute("lang", "en")

        serialized = cookie.serialize()
        self.assertTrue(serialized.startswith("session_id=abc123;"))
        self.assertIn("lang=en;", serialized)

    def test_serialize_singleton_attribute(self):
        cookie = system.Cookie()
        cookie.set_attribute("secure")

        serialized = cookie.serialize()
        self.assertIn("secure;", serialized)


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "REST Exceptions test case"

    def test_service_exception(self):
        exception = exceptions.ServiceException()
        self.assertEqual(exception.message, None)

    def test_invalid_number_arguments(self):
        exception = exceptions.InvalidNumberArguments("expected 2, got 3")
        self.assertEqual(exception.message, "expected 2, got 3")
        self.assertEqual(
            str(exception), "Invalid number of arguments - expected 2, got 3"
        )

    def test_invalid_method(self):
        exception = exceptions.InvalidMethod("unknown_method")
        self.assertEqual(exception.message, "unknown_method")
        self.assertEqual(str(exception), "Invalid Method - unknown_method")

    def test_invalid_encoder(self):
        exception = exceptions.InvalidEncoder("xml")
        self.assertEqual(exception.message, "xml")
        self.assertEqual(str(exception), "Invalid Encoder - xml")

    def test_rest_request_error(self):
        exception = exceptions.RESTRequestError("request failed")
        self.assertEqual(exception.message, "request failed")
        self.assertEqual(str(exception), "REST Request Error - request failed")

    def test_rest_request_not_handled(self):
        exception = exceptions.RESTRequestNotHandled("no handler found")
        self.assertEqual(exception.message, "no handler found")
        self.assertEqual(str(exception), "REST Request Not handled - no handler found")

    def test_invalid_path(self):
        exception = exceptions.InvalidPath("missing segment")
        self.assertEqual(exception.message, "missing segment")
        self.assertEqual(str(exception), "Invalid path - missing segment")

    def test_invalid_session(self):
        exception = exceptions.InvalidSession("session expired")
        self.assertEqual(exception.message, "session expired")
        self.assertEqual(str(exception), "Invalid session - session expired")

    def test_invalid_cookie(self):
        exception = exceptions.InvalidCookie("malformed cookie")
        self.assertEqual(exception.message, "malformed cookie")
        self.assertEqual(str(exception), "Invalid cookie - malformed cookie")

    def test_exception_inheritance(self):
        exception_list = [
            exceptions.ServiceRequestNotTranslatable(),
            exceptions.BadServiceRequest(),
            exceptions.InvalidNumberArguments("test"),
            exceptions.InvalidMethod("test"),
            exceptions.InvalidEncoder("test"),
            exceptions.RESTRequestError("test"),
            exceptions.RESTRequestNotHandled("test"),
            exceptions.InvalidPath("test"),
            exceptions.InvalidSession("test"),
            exceptions.InvalidCookie("test"),
        ]
        for exception in exception_list:
            self.assertTrue(isinstance(exception, exceptions.ServiceException))
            self.assertTrue(isinstance(exception, colony.ColonyException))

    def test_bad_service_request_inheritance(self):
        exception_list = [
            exceptions.InvalidNumberArguments("test"),
            exceptions.InvalidMethod("test"),
            exceptions.InvalidEncoder("test"),
            exceptions.RESTRequestError("test"),
            exceptions.RESTRequestNotHandled("test"),
            exceptions.InvalidPath("test"),
        ]
        for exception in exception_list:
            self.assertTrue(isinstance(exception, exceptions.BadServiceRequest))


class RegressionTestCase(colony.ColonyTestCase):
    """
    Regression tests for critical bug fixes in the REST system.
    These tests ensure that previously identified issues don't resurface.
    """

    @staticmethod
    def get_description():
        return "REST Regression test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self._saved_storage = system.RESTSession.STORAGE
        system.RESTSession.STORAGE = {}
        system.RESTSession.GC_PENDING = True

    def tearDown(self):
        system.RESTSession.STORAGE = self._saved_storage

    def test_gc_does_not_raise_on_expired_sessions(self):
        """
        Regression test for dictionary iteration bug in gc().

        Previously, gc() would iterate over the storage dictionary
        while simultaneously deleting expired entries, causing:
        RuntimeError: dictionary changed size during iteration

        Fixed by collecting expired session IDs first, then deleting.
        """

        session1 = system.RESTSession.new("gc_test_1", timeout=0.01)
        session2 = system.RESTSession.new("gc_test_2", timeout=0.01)
        session3 = system.RESTSession.new("gc_test_3", timeout=1000)

        time.sleep(0.05)

        try:
            system.RESTSession.gc()
        except RuntimeError as e:
            if "dictionary changed size during iteration" in str(e):
                self.fail(
                    "gc() raised RuntimeError due to dictionary modification during iteration"
                )
            raise

        self.assertNotIn("gc_test_1", system.RESTSession.STORAGE)
        self.assertNotIn("gc_test_2", system.RESTSession.STORAGE)
        self.assertIn("gc_test_3", system.RESTSession.STORAGE)

    def test_gc_handles_none_session(self):
        """
        Test that gc() handles None sessions gracefully.

        The gc() method should skip any None entries in the storage
        without raising an AttributeError.
        """

        system.RESTSession.new("valid_session", timeout=1000)
        system.RESTSession.STORAGE["none_session"] = None

        try:
            system.RESTSession.gc()
        except AttributeError:
            self.fail("gc() raised AttributeError when encountering None session")

        self.assertIn("valid_session", system.RESTSession.STORAGE)

    def test_gc_with_all_expired_sessions(self):
        """
        Test gc() when all sessions are expired.

        This is an edge case where the entire storage would be cleared
        during iteration, which previously would cause an error.
        """

        system.RESTSession.new("expired_1", timeout=0.01)
        system.RESTSession.new("expired_2", timeout=0.01)
        system.RESTSession.new("expired_3", timeout=0.01)

        time.sleep(0.05)

        try:
            system.RESTSession.gc()
        except RuntimeError:
            self.fail("gc() raised RuntimeError when all sessions expired")

        self.assertEqual(system.RESTSession.count(), 0)

    def test_gc_with_empty_storage(self):
        """
        Test gc() when storage is empty.

        Should complete without error.
        """

        self.assertEqual(system.RESTSession.count(), 0)

        try:
            system.RESTSession.gc()
        except Exception as e:
            self.fail("gc() raised exception on empty storage: %s" % str(e))

    def test_translate_result_returns_value_without_encoder(self):
        """
        Regression test for missing return statement in translate_result().

        Previously, when encoder_name was not provided, the function
        would execute `"text/plain", str(result)` without returning,
        causing None to be returned or the function to continue
        and raise an InvalidEncoder exception.

        Fixed by adding the missing return keyword.
        """

        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        result = rest.translate_result({"key": "value"}, encoder_name=None)

        self.assertNotEqual(result, None)
        self.assertEqual(len(result), 2)
        content_type, data = result
        self.assertEqual(content_type, "text/plain")
        self.assertIn("key", data)

    def test_translate_result_with_string_result(self):
        """
        Test `translate_result()` with a simple string when no encoder specified.
        """

        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        result = rest.translate_result("hello world", encoder_name=None)

        self.assertEqual(result, ("text/plain", "hello world"))

    def test_translate_result_with_number_result(self):
        """
        Test `translate_result()` with a number when no encoder specified.
        """

        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        result = rest.translate_result(42, encoder_name=None)

        self.assertEqual(result, ("text/plain", "42"))

    def test_translate_result_with_empty_encoder_name(self):
        """
        Test `translate_result()` with empty string encoder name.

        Empty string is falsy, so should behave like None.
        """

        mock_plugin = mocks.MockPlugin()
        rest = system.REST(mock_plugin, session_c=system.RESTSession)

        result = rest.translate_result("test", encoder_name="")

        self.assertEqual(result, ("text/plain", "test"))
