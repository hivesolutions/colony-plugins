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

from . import system
from . import exceptions


class ClientUtilsTest(colony.Test):
    """
    The client utils infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            ClientUtilsBaseTestCase,
            AbstractClientTestCase,
            ExceptionsTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class ClientUtilsBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Client Utils Base test case"

    def test_initialization(self):
        # creates a mock plugin and initializes the client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # verifies the maps are initialized empty
        self.assertEqual(client_utils.socket_provider_plugins_map, {})
        self.assertEqual(client_utils.socket_upgrader_plugins_map, {})

    def test_generate_client(self):
        # creates a mock plugin and client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # generates a client with empty parameters
        client = client_utils.generate_client({})

        # verifies the client was created correctly
        self.assertNotEqual(client, None)
        self.assertTrue(isinstance(client, system.AbstractClient))
        self.assertEqual(client.client_utils, client_utils)
        self.assertEqual(client.client_utils_plugin, mock_plugin)

    def test_generate_client_with_parameters(self):
        # creates a mock plugin and client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # generates a client with custom parameters
        parameters = {
            "type": "custom",
            "chunk_size": 8192,
            "request_timeout": 60,
            "response_timeout": 120,
        }
        client = client_utils.generate_client(parameters)

        # verifies custom parameters were applied
        self.assertEqual(client.client_type, "custom")
        self.assertEqual(client.chunk_size, 8192)
        self.assertEqual(client.request_timeout, 60)
        self.assertEqual(client.response_timeout, 120)

    def test_socket_provider_load(self):
        # creates a mock plugin and client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # creates a mock socket provider plugin
        socket_provider = MockSocketProviderPlugin("normal")

        # loads the socket provider
        client_utils.socket_provider_load(socket_provider)

        # verifies it was registered
        self.assertIn("normal", client_utils.socket_provider_plugins_map)
        self.assertEqual(
            client_utils.socket_provider_plugins_map["normal"], socket_provider
        )

    def test_socket_provider_unload(self):
        # creates a mock plugin and client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # creates and loads a mock socket provider
        socket_provider = MockSocketProviderPlugin("ssl")
        client_utils.socket_provider_load(socket_provider)

        # verifies it was registered
        self.assertIn("ssl", client_utils.socket_provider_plugins_map)

        # unloads the socket provider
        client_utils.socket_provider_unload(socket_provider)

        # verifies it was removed
        self.assertNotIn("ssl", client_utils.socket_provider_plugins_map)

    def test_socket_upgrader_load(self):
        # creates a mock plugin and client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # creates a mock socket upgrader plugin
        socket_upgrader = MockSocketUpgraderPlugin("ssl_upgrader")

        # loads the socket upgrader
        client_utils.socket_upgrader_load(socket_upgrader)

        # verifies it was registered
        self.assertIn("ssl_upgrader", client_utils.socket_upgrader_plugins_map)
        self.assertEqual(
            client_utils.socket_upgrader_plugins_map["ssl_upgrader"], socket_upgrader
        )

    def test_socket_upgrader_unload(self):
        # creates a mock plugin and client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # creates and loads a mock socket upgrader
        socket_upgrader = MockSocketUpgraderPlugin("tls_upgrader")
        client_utils.socket_upgrader_load(socket_upgrader)

        # verifies it was registered
        self.assertIn("tls_upgrader", client_utils.socket_upgrader_plugins_map)

        # unloads the socket upgrader
        client_utils.socket_upgrader_unload(socket_upgrader)

        # verifies it was removed
        self.assertNotIn("tls_upgrader", client_utils.socket_upgrader_plugins_map)

    def test_multiple_socket_providers(self):
        # creates a mock plugin and client utils
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # loads multiple socket providers
        providers = ["normal", "ssl", "tls"]
        for provider_name in providers:
            socket_provider = MockSocketProviderPlugin(provider_name)
            client_utils.socket_provider_load(socket_provider)

        # verifies all were registered
        self.assertEqual(len(client_utils.socket_provider_plugins_map), 3)
        for provider_name in providers:
            self.assertIn(provider_name, client_utils.socket_provider_plugins_map)


class AbstractClientTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Abstract Client test case"

    def test_initialization_defaults(self):
        # creates mock objects
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # creates a client with default parameters
        client = system.AbstractClient(client_utils, mock_plugin)

        # verifies default values
        self.assertEqual(client.client_type, "connection")
        self.assertEqual(client.chunk_size, system.CHUNK_SIZE)
        self.assertEqual(
            client.client_connection_timeout, system.CLIENT_CONNECTION_TIMEOUT
        )
        self.assertEqual(client.connection_timeout, system.CONNECTION_TIMEOUT)
        self.assertEqual(client.request_timeout, system.REQUEST_TIMEOUT)
        self.assertEqual(client.response_timeout, system.RESPONSE_TIMEOUT)
        self.assertEqual(client.client_connections_map, {})

    def test_initialization_custom_parameters(self):
        # creates mock objects
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        # creates custom parameters
        parameters = {
            "type": "udp",
            "chunk_size": 1024,
            "client_connection_timeout": 5,
            "connection_timeout": 300,
            "request_timeout": 30,
            "response_timeout": 60,
        }

        # creates a client with custom parameters
        client = system.AbstractClient(client_utils, mock_plugin, parameters)

        # verifies custom values were applied
        self.assertEqual(client.client_type, "udp")
        self.assertEqual(client.chunk_size, 1024)
        self.assertEqual(client.client_connection_timeout, 5)
        self.assertEqual(client.connection_timeout, 300)
        self.assertEqual(client.request_timeout, 30)
        self.assertEqual(client.response_timeout, 60)

    def test_start_stop_client(self):
        # creates mock objects
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)
        client = system.AbstractClient(client_utils, mock_plugin)

        # verifies start does not raise
        client.start_client()

        # verifies stop does not raise
        client.stop_client()

    def test_generate_connection_tuple_hashable(self):
        # creates mock objects
        mock_plugin = MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)
        client = system.AbstractClient(client_utils, mock_plugin)

        # creates a connection tuple with dictionary
        connection_tuple = ("localhost", 8080, True, "normal", {"key": "value"})

        # generates the hashable version
        hashable = client._generate_connection_tuple_hashable(connection_tuple)

        # verifies it can be used as a dictionary key (is hashable)
        test_dict = {}
        test_dict[hashable] = "test"
        self.assertEqual(test_dict[hashable], "test")

        # verifies the structure
        self.assertEqual(hashable[0], "localhost")
        self.assertEqual(hashable[1], 8080)
        self.assertEqual(hashable[2], True)
        self.assertEqual(hashable[3], "normal")
        # the dictionary becomes a tuple of items
        self.assertEqual(hashable[4], (("key", "value"),))


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Client Utils Exceptions test case"

    def test_client_utils_exception(self):
        # creates a base exception
        exception = exceptions.ClientUtilsException()
        self.assertEqual(exception.message, None)

    def test_socket_provider_not_found(self):
        # creates exception with message
        exception = exceptions.SocketProviderNotFound("ssl provider")
        self.assertEqual(exception.message, "ssl provider")
        self.assertEqual(str(exception), "Socket provider not found - ssl provider")

    def test_socket_upgrader_not_found(self):
        # creates exception with message
        exception = exceptions.SocketUpgraderNotFound("tls upgrader")
        self.assertEqual(exception.message, "tls upgrader")
        self.assertEqual(str(exception), "Socket upgrader not found - tls upgrader")

    def test_client_request_timeout(self):
        # creates exception with message
        exception = exceptions.ClientRequestTimeout("120s timeout")
        self.assertEqual(exception.message, "120s timeout")
        self.assertEqual(str(exception), "Client request timeout - 120s timeout")

    def test_server_request_timeout(self):
        # creates exception with message
        exception = exceptions.ServerRequestTimeout("30s timeout")
        self.assertEqual(exception.message, "30s timeout")
        self.assertEqual(str(exception), "Server request timeout - 30s timeout")

    def test_client_response_timeout(self):
        # creates exception with message
        exception = exceptions.ClientResponseTimeout("60s timeout")
        self.assertEqual(exception.message, "60s timeout")
        self.assertEqual(str(exception), "Client response timeout - 60s timeout")

    def test_server_response_timeout(self):
        # creates exception with message
        exception = exceptions.ServerResponseTimeout("45s timeout")
        self.assertEqual(exception.message, "45s timeout")
        self.assertEqual(str(exception), "Server response timeout - 45s timeout")

    def test_request_closed(self):
        # creates exception with message
        exception = exceptions.RequestClosed("connection reset")
        self.assertEqual(exception.message, "connection reset")
        self.assertEqual(str(exception), "Request closed - connection reset")

    def test_exception_inheritance(self):
        # verifies all exceptions inherit from base
        exception_list = [
            exceptions.SocketProviderNotFound("test"),
            exceptions.SocketUpgraderNotFound("test"),
            exceptions.ClientRequestTimeout("test"),
            exceptions.ServerRequestTimeout("test"),
            exceptions.ClientResponseTimeout("test"),
            exceptions.ServerResponseTimeout("test"),
            exceptions.RequestClosed("test"),
        ]
        for exception in exception_list:
            self.assertTrue(isinstance(exception, exceptions.ClientUtilsException))
            self.assertTrue(isinstance(exception, colony.ColonyException))


class MockPlugin:
    def __init__(self):
        self.manager = None

    def debug(self, message):
        pass


class MockSocketProviderPlugin:
    def __init__(self, name):
        self._provider_name = name

    def get_provider_name(self):
        return self._provider_name

    def provide_socket_parameters(self, parameters):
        return MockSocket()


class MockSocketUpgraderPlugin:
    def __init__(self, name):
        self._upgrader_name = name

    def get_upgrader_name(self):
        return self._upgrader_name

    def upgrade_socket_parameters(self, socket, parameters):
        return socket


class MockSocket:
    def __init__(self):
        self.blocking = True

    def connect(self, address):
        pass

    def close(self):
        pass

    def setblocking(self, blocking):
        self.blocking = blocking

    def recv(self, size):
        return b""

    def send(self, data):
        return len(data)

    def sendto(self, data, address):
        return len(data)
