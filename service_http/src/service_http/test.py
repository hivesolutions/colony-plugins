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

import colony

from .system import ServiceHTTP
from .system import STATUS_MESSAGES
from .system import DEFAULT_PORT
from .system import SERVER_IDENTIFIER
from .exceptions import ServiceHTTPException
from .exceptions import EncodingNotFound
from .exceptions import ClientRequestSecurityViolation
from .exceptions import HTTPRuntimeException
from .exceptions import HTTPInvalidDataException
from .exceptions import HTTPNoHandlerException
from .exceptions import HTTPHandlerNotFoundException
from .exceptions import HTTPAuthenticationHandlerNotFoundException
from .exceptions import HTTPInvalidMultipartRequestException
from .exceptions import HTTPDataRetrievalException
from .exceptions import HTTPDataSendingException
from .exceptions import UnauthorizedException


class ServiceHTTPTest(colony.Test):
    """
    The service HTTP infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            ServiceHTTPBaseTestCase,
            StatusMessagesTestCase,
            ExceptionsTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class ServiceHTTPBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Service HTTP Base test case"

    def setUp(self):
        # clears class-level maps to ensure test isolation
        ServiceHTTP.http_service_handler_plugins_map = {}
        ServiceHTTP.http_service_encoding_plugins_map = {}
        ServiceHTTP.http_service_authentication_handler_plugins_map = {}
        ServiceHTTP.http_service_error_handler_plugins_map = {}

    def test_initialization(self):
        # creates a mock plugin and initializes the service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # verifies the instance is created with proper attributes
        self.assertEqual(service.http_service_configuration, {})

    def test_handler_load(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates and loads a mock handler
        handler = MockHandlerPlugin("file")
        service.http_service_handler_load(handler)

        # verifies it was registered
        self.assertIn("file", service.http_service_handler_plugins_map)
        self.assertEqual(service.http_service_handler_plugins_map["file"], handler)

    def test_handler_unload(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates, loads and unloads a handler
        handler = MockHandlerPlugin("proxy")
        service.http_service_handler_load(handler)
        self.assertIn("proxy", service.http_service_handler_plugins_map)

        service.http_service_handler_unload(handler)
        self.assertNotIn("proxy", service.http_service_handler_plugins_map)

    def test_encoding_load(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates and loads a mock encoding plugin
        encoding = MockEncodingPlugin("gzip")
        service.http_service_encoding_load(encoding)

        # verifies it was registered
        self.assertIn("gzip", service.http_service_encoding_plugins_map)
        self.assertEqual(service.http_service_encoding_plugins_map["gzip"], encoding)

    def test_encoding_unload(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates, loads and unloads an encoding
        encoding = MockEncodingPlugin("deflate")
        service.http_service_encoding_load(encoding)
        self.assertIn("deflate", service.http_service_encoding_plugins_map)

        service.http_service_encoding_unload(encoding)
        self.assertNotIn("deflate", service.http_service_encoding_plugins_map)

    def test_authentication_handler_load(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates and loads a mock authentication handler
        auth_handler = MockAuthHandlerPlugin("basic")
        service.http_service_authentication_handler_load(auth_handler)

        # verifies it was registered
        self.assertIn("basic", service.http_service_authentication_handler_plugins_map)
        self.assertEqual(
            service.http_service_authentication_handler_plugins_map["basic"],
            auth_handler,
        )

    def test_authentication_handler_unload(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates, loads and unloads an authentication handler
        auth_handler = MockAuthHandlerPlugin("digest")
        service.http_service_authentication_handler_load(auth_handler)
        self.assertIn(
            "digest", service.http_service_authentication_handler_plugins_map
        )

        service.http_service_authentication_handler_unload(auth_handler)
        self.assertNotIn(
            "digest", service.http_service_authentication_handler_plugins_map
        )

    def test_error_handler_load(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates and loads a mock error handler
        error_handler = MockErrorHandlerPlugin("template")
        service.http_service_error_handler_load(error_handler)

        # verifies it was registered
        self.assertIn("template", service.http_service_error_handler_plugins_map)
        self.assertEqual(
            service.http_service_error_handler_plugins_map["template"], error_handler
        )

    def test_error_handler_unload(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates, loads and unloads an error handler
        error_handler = MockErrorHandlerPlugin("json")
        service.http_service_error_handler_load(error_handler)
        self.assertIn("json", service.http_service_error_handler_plugins_map)

        service.http_service_error_handler_unload(error_handler)
        self.assertNotIn("json", service.http_service_error_handler_plugins_map)

    def test_configuration_property(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # creates a configuration property
        config = MockConfigurationProperty(
            {"virtual_servers": {}, "redirections": {}, "contexts": {}}
        )

        # sets and verifies configuration
        service.set_service_configuration_property(config)
        self.assertNotEqual(service.http_service_configuration, {})

        # unsets and verifies configuration
        service.unset_service_configuration_property()
        self.assertEqual(service.http_service_configuration, {})

    def test_multiple_handlers(self):
        # creates a mock plugin and service
        mock_plugin = MockPlugin()
        service = ServiceHTTP(mock_plugin)

        # loads multiple handlers
        handlers = ["file", "proxy", "cgi", "wsgi"]
        for handler_name in handlers:
            handler = MockHandlerPlugin(handler_name)
            service.http_service_handler_load(handler)

        # verifies all were registered
        self.assertEqual(len(service.http_service_handler_plugins_map), 4)
        for handler_name in handlers:
            self.assertIn(handler_name, service.http_service_handler_plugins_map)


class StatusMessagesTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "HTTP Status Messages test case"

    def test_status_messages_defined(self):
        # verifies common status codes are defined
        self.assertIn(200, STATUS_MESSAGES)
        self.assertIn(201, STATUS_MESSAGES)
        self.assertIn(301, STATUS_MESSAGES)
        self.assertIn(302, STATUS_MESSAGES)
        self.assertIn(400, STATUS_MESSAGES)
        self.assertIn(401, STATUS_MESSAGES)
        self.assertIn(403, STATUS_MESSAGES)
        self.assertIn(404, STATUS_MESSAGES)
        self.assertIn(500, STATUS_MESSAGES)
        self.assertIn(502, STATUS_MESSAGES)
        self.assertIn(503, STATUS_MESSAGES)

    def test_status_messages_values(self):
        # verifies common status message values
        self.assertEqual(STATUS_MESSAGES[200], "OK")
        self.assertEqual(STATUS_MESSAGES[201], "Created")
        self.assertEqual(STATUS_MESSAGES[204], "No Content")
        self.assertEqual(STATUS_MESSAGES[301], "Moved permanently")
        self.assertEqual(STATUS_MESSAGES[302], "Found")
        self.assertEqual(STATUS_MESSAGES[400], "Bad Request")
        self.assertEqual(STATUS_MESSAGES[401], "Unauthorized")
        self.assertEqual(STATUS_MESSAGES[403], "Forbidden")
        self.assertEqual(STATUS_MESSAGES[404], "Not Found")
        self.assertEqual(STATUS_MESSAGES[500], "Internal Server Error")

    def test_default_port(self):
        # verifies the default port value
        self.assertEqual(DEFAULT_PORT, 8080)

    def test_server_identifier(self):
        # verifies server identifier is defined
        self.assertNotEqual(SERVER_IDENTIFIER, None)
        self.assertTrue(len(SERVER_IDENTIFIER) > 0)
        self.assertIn("Hive-Colony-Web", SERVER_IDENTIFIER)


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Service HTTP Exceptions test case"

    def test_service_http_exception(self):
        # creates a base exception
        exception = ServiceHTTPException()
        self.assertEqual(exception.message, None)

    def test_encoding_not_found(self):
        # creates exception with message
        exception = EncodingNotFound("brotli")
        self.assertEqual(exception.message, "brotli")
        self.assertEqual(str(exception), "Encoding not found - brotli")

    def test_client_request_security_violation(self):
        # creates exception with message
        exception = ClientRequestSecurityViolation("path traversal detected")
        self.assertEqual(exception.message, "path traversal detected")
        self.assertEqual(
            str(exception), "Client request security violation - path traversal detected"
        )

    def test_http_runtime_exception(self):
        # creates exception with message
        exception = HTTPRuntimeException("runtime error")
        self.assertEqual(exception.message, "runtime error")
        self.assertEqual(str(exception), "HTTP runtime exception - runtime error")

    def test_http_invalid_data_exception(self):
        # creates exception with message
        exception = HTTPInvalidDataException("malformed request")
        self.assertEqual(exception.message, "malformed request")
        self.assertEqual(str(exception), "HTTP invalid data exception - malformed request")

    def test_http_no_handler_exception(self):
        # creates exception with message
        exception = HTTPNoHandlerException("no handler registered")
        self.assertEqual(exception.message, "no handler registered")
        self.assertEqual(str(exception), "HTTP no handler exception - no handler registered")

    def test_http_handler_not_found_exception(self):
        # creates exception with message
        exception = HTTPHandlerNotFoundException("custom_handler")
        self.assertEqual(exception.message, "custom_handler")
        self.assertEqual(
            str(exception), "HTTP handler not found exception - custom_handler"
        )

    def test_http_auth_handler_not_found_exception(self):
        # creates exception with message
        exception = HTTPAuthenticationHandlerNotFoundException("oauth")
        self.assertEqual(exception.message, "oauth")
        self.assertEqual(
            str(exception), "HTTP authentication handler not found exception - oauth"
        )

    def test_http_invalid_multipart_request_exception(self):
        # creates exception with message
        exception = HTTPInvalidMultipartRequestException("missing boundary")
        self.assertEqual(exception.message, "missing boundary")
        self.assertEqual(
            str(exception), "HTTP invalid multipart request exception - missing boundary"
        )

    def test_http_data_retrieval_exception(self):
        # creates exception with message
        exception = HTTPDataRetrievalException("connection reset")
        self.assertEqual(exception.message, "connection reset")
        self.assertEqual(str(exception), "HTTP data retrieval exception - connection reset")

    def test_http_data_sending_exception(self):
        # creates exception with message
        exception = HTTPDataSendingException("broken pipe")
        self.assertEqual(exception.message, "broken pipe")
        self.assertEqual(str(exception), "HTTP data sending exception - broken pipe")

    def test_unauthorized_exception(self):
        # creates exception with message and status code
        exception = UnauthorizedException("invalid credentials", 401)
        self.assertEqual(exception.message, "invalid credentials")
        self.assertEqual(exception.status_code, 401)
        self.assertEqual(str(exception), "Unauthorized - invalid credentials")

    def test_unauthorized_exception_custom_status(self):
        # creates exception with different status codes
        exception = UnauthorizedException("forbidden", 403)
        self.assertEqual(exception.status_code, 403)

    def test_exception_inheritance(self):
        # verifies all exceptions inherit from base
        exceptions = [
            EncodingNotFound("test"),
            ClientRequestSecurityViolation("test"),
            HTTPRuntimeException("test"),
            HTTPInvalidDataException("test"),
            HTTPNoHandlerException("test"),
            HTTPHandlerNotFoundException("test"),
            HTTPAuthenticationHandlerNotFoundException("test"),
            HTTPInvalidMultipartRequestException("test"),
            HTTPDataRetrievalException("test"),
            HTTPDataSendingException("test"),
            UnauthorizedException("test", 401),
        ]
        for exception in exceptions:
            self.assertTrue(isinstance(exception, ServiceHTTPException))
            self.assertTrue(isinstance(exception, colony.ColonyException))

    def test_http_runtime_exception_inheritance(self):
        # verifies runtime exceptions inherit from HTTPRuntimeException
        exceptions = [
            HTTPInvalidDataException("test"),
            HTTPNoHandlerException("test"),
            HTTPHandlerNotFoundException("test"),
            HTTPAuthenticationHandlerNotFoundException("test"),
            HTTPInvalidMultipartRequestException("test"),
            HTTPDataRetrievalException("test"),
            HTTPDataSendingException("test"),
            UnauthorizedException("test", 401),
        ]
        for exception in exceptions:
            self.assertTrue(isinstance(exception, HTTPRuntimeException))


class MockPlugin:
    def __init__(self):
        self.service_utils_plugin = None
        self.manager = None


class MockConfigurationProperty:
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data


class MockHandlerPlugin:
    def __init__(self, name):
        self._handler_name = name

    def get_handler_name(self):
        return self._handler_name


class MockEncodingPlugin:
    def __init__(self, name):
        self._encoding_name = name

    def get_encoding_name(self):
        return self._encoding_name


class MockAuthHandlerPlugin:
    def __init__(self, name):
        self._handler_name = name

    def get_handler_name(self):
        return self._handler_name


class MockErrorHandlerPlugin:
    def __init__(self, name):
        self._error_handler_name = name

    def get_error_handler_name(self):
        return self._error_handler_name
