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

import socket

import colony

from . import system
from . import exceptions
from . import mocks


class ClientUtilsTest(colony.Test):
    """
    The client utils infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            ClientUtilsBaseTestCase,
            AbstractClientTestCase,
            PollSocketTestCase,
            ClientConnectionTestCase,
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
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        self.assertEqual(client_utils.socket_provider_plugins_map, {})
        self.assertEqual(client_utils.socket_upgrader_plugins_map, {})

    def test_generate_client(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        client = client_utils.generate_client({})

        self.assertNotEqual(client, None)
        self.assertTrue(isinstance(client, system.AbstractClient))
        self.assertEqual(client.client_utils, client_utils)
        self.assertEqual(client.client_utils_plugin, mock_plugin)

    def test_generate_client_with_parameters(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        parameters = {
            "type": "custom",
            "chunk_size": 8192,
            "request_timeout": 60,
            "response_timeout": 120,
        }
        client = client_utils.generate_client(parameters)

        self.assertEqual(client.client_type, "custom")
        self.assertEqual(client.chunk_size, 8192)
        self.assertEqual(client.request_timeout, 60)
        self.assertEqual(client.response_timeout, 120)

    def test_socket_provider_load(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        socket_provider = mocks.MockSocketProviderPlugin("normal")
        client_utils.socket_provider_load(socket_provider)

        self.assertIn("normal", client_utils.socket_provider_plugins_map)
        self.assertEqual(
            client_utils.socket_provider_plugins_map["normal"], socket_provider
        )

    def test_socket_provider_unload(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        socket_provider = mocks.MockSocketProviderPlugin("ssl")
        client_utils.socket_provider_load(socket_provider)
        self.assertIn("ssl", client_utils.socket_provider_plugins_map)

        client_utils.socket_provider_unload(socket_provider)
        self.assertNotIn("ssl", client_utils.socket_provider_plugins_map)

    def test_socket_upgrader_load(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        socket_upgrader = mocks.MockSocketUpgraderPlugin("ssl_upgrader")
        client_utils.socket_upgrader_load(socket_upgrader)

        self.assertIn("ssl_upgrader", client_utils.socket_upgrader_plugins_map)
        self.assertEqual(
            client_utils.socket_upgrader_plugins_map["ssl_upgrader"], socket_upgrader
        )

    def test_socket_upgrader_unload(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        socket_upgrader = mocks.MockSocketUpgraderPlugin("tls_upgrader")
        client_utils.socket_upgrader_load(socket_upgrader)
        self.assertIn("tls_upgrader", client_utils.socket_upgrader_plugins_map)

        client_utils.socket_upgrader_unload(socket_upgrader)
        self.assertNotIn("tls_upgrader", client_utils.socket_upgrader_plugins_map)

    def test_multiple_socket_providers(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        providers = ["normal", "ssl", "tls"]
        for provider_name in providers:
            socket_provider = mocks.MockSocketProviderPlugin(provider_name)
            client_utils.socket_provider_load(socket_provider)

        self.assertEqual(len(client_utils.socket_provider_plugins_map), 3)
        for provider_name in providers:
            self.assertIn(provider_name, client_utils.socket_provider_plugins_map)


class AbstractClientTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Abstract Client test case"

    def test_initialization_defaults(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        client = system.AbstractClient(client_utils, mock_plugin)

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
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)

        parameters = {
            "type": "udp",
            "chunk_size": 1024,
            "client_connection_timeout": 5,
            "connection_timeout": 300,
            "request_timeout": 30,
            "response_timeout": 60,
        }

        client = system.AbstractClient(client_utils, mock_plugin, parameters)

        self.assertEqual(client.client_type, "udp")
        self.assertEqual(client.chunk_size, 1024)
        self.assertEqual(client.client_connection_timeout, 5)
        self.assertEqual(client.connection_timeout, 300)
        self.assertEqual(client.request_timeout, 30)
        self.assertEqual(client.response_timeout, 60)

    def test_start_stop_client(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)
        client = system.AbstractClient(client_utils, mock_plugin)

        client.start_client()
        client.stop_client()

    def test_generate_connection_tuple_hashable(self):
        mock_plugin = mocks.MockPlugin()
        client_utils = system.ClientUtils(mock_plugin)
        client = system.AbstractClient(client_utils, mock_plugin)

        connection_tuple = ("localhost", 8080, True, "normal", {"key": "value"})
        hashable = client._generate_connection_tuple_hashable(connection_tuple)

        test_dict = {}
        test_dict[hashable] = "test"
        self.assertEqual(test_dict[hashable], "test")

        self.assertEqual(hashable[0], "localhost")
        self.assertEqual(hashable[1], 8080)
        self.assertEqual(hashable[2], True)
        self.assertEqual(hashable[3], "normal")
        self.assertEqual(hashable[4], (("key", "value"),))


class PollSocketTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Poll Socket test case"

    def test_poll_read_no_data(self):
        # binds a server socket on a random port with no pending
        # connection so the read poll should return not readable
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()
        try:
            readable, writeable = system.poll_socket(server_fd, system.READ, 0.001)
            self.assertEqual(readable, False)
            self.assertEqual(writeable, False)
        finally:
            server.close()

    def test_poll_read_with_connection(self):
        # a client connection to the server socket triggers a read
        # event, so the poll should return readable after the connect
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]
        server_fd = server.fileno()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("127.0.0.1", port))
            readable, _writeable = system.poll_socket(server_fd, system.READ, 1.0)
            self.assertEqual(readable, True)
        finally:
            client.close()
            server.close()

    def test_poll_write_ready(self):
        # a connected non-blocking socket should immediately be
        # ready for write operations once the connection is established
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("127.0.0.1", port))
            client_fd = client.fileno()
            _readable, writeable = system.poll_socket(
                client_fd, system.READ | system.WRITE, 1.0
            )
            self.assertEqual(writeable, True)
        finally:
            client.close()
            server.close()

    def test_poll_returns_tuple(self):
        # verifies that poll_socket always returns a two-element
        # tuple of boolean values regardless of the result
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()
        try:
            result = system.poll_socket(server_fd, system.READ, 0.001)
            self.assertEqual(len(result), 2)
            self.assertTrue(isinstance(result[0], bool))
            self.assertTrue(isinstance(result[1], bool))
        finally:
            server.close()


class ClientConnectionTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Client Connection test case"

    def _create_connection(self, mock_socket=None, persistent=True):
        """
        Creates a minimal ClientConnection instance for testing
        purposes, wiring a mock socket and plugin.

        :type mock_socket: MockSocket
        :param mock_socket: The mock socket to use, or None for default.
        :type persistent: bool
        :param persistent: If the connection should be persistent.
        :rtype: ClientConnection
        :return: The created client connection instance.
        """

        mock_plugin = mocks.MockPlugin()
        mock_client_utils = system.ClientUtils(mock_plugin)
        mock_client = system.AbstractClient(mock_client_utils, mock_plugin)

        if mock_socket == None:
            mock_socket = mocks.MockSocket()

        return system.ClientConnection(
            mock_plugin,
            mock_client,
            mock_socket,
            ("127.0.0.1", 8080),
            persistent,
            "normal",
            {},
            system.REQUEST_TIMEOUT,
            system.RESPONSE_TIMEOUT,
            system.CHUNK_SIZE,
        )

    def test_initialization(self):
        mock_socket = mocks.MockSocket()
        conn = self._create_connection(mock_socket)

        self.assertEqual(conn.connection_address, ("127.0.0.1", 8080))
        self.assertEqual(conn.connection_persistent, True)
        self.assertEqual(conn.connection_socket_name, "normal")
        self.assertEqual(conn.connection_socket_parameters, {})
        self.assertEqual(conn.connection_request_timeout, system.REQUEST_TIMEOUT)
        self.assertEqual(conn.connection_response_timeout, system.RESPONSE_TIMEOUT)
        self.assertEqual(conn.connection_chunk_size, system.CHUNK_SIZE)
        self.assertEqual(conn.connection_status, False)
        self.assertEqual(conn._read_buffer, [])
        self.assertEqual(conn.connection_opened_handlers, [])
        self.assertEqual(conn.connection_closed_handlers, [])
        self.assertEqual(conn.connection_properties, {})

    def test_open_persistent(self):
        mock_socket = mocks.MockSocket()
        conn = self._create_connection(mock_socket, persistent=True)

        conn.open()

        self.assertEqual(conn.connection_status, True)
        self.assertEqual(mock_socket.blocking, False)
        self.assertEqual(conn._read_buffer, [])

    def test_open_non_persistent(self):
        # a non-persistent connection should not call connect on the socket
        # but still set non-blocking mode and mark the connection as open
        mock_socket = mocks.MockSocket()
        conn = self._create_connection(mock_socket, persistent=False)

        conn.open()

        self.assertEqual(conn.connection_status, True)
        self.assertEqual(mock_socket.blocking, False)

    def test_close(self):
        mock_socket = mocks.MockSocket()
        conn = self._create_connection(mock_socket)
        conn.connection_status = True

        conn.close()

        self.assertEqual(conn.connection_status, False)
        self.assertEqual(mock_socket._closed, True)
        self.assertEqual(conn._read_buffer, [])

    def test_close_clears_read_buffer(self):
        mock_socket = mocks.MockSocket()
        conn = self._create_connection(mock_socket)
        conn._read_buffer = [b"pending", b"data"]

        conn.close()

        self.assertEqual(conn._read_buffer, [])

    def test_cancel(self):
        import time

        conn = self._create_connection()
        delta = 10.0
        before = time.time()

        conn.cancel(delta)

        self.assertNotEqual(conn.cancel_time, None)
        self.assertTrue(conn.cancel_time >= before + delta)  # type: ignore
        self.assertTrue(conn.cancel_time <= before + delta + 1.0)  # type: ignore

    def test_is_open_initial(self):
        conn = self._create_connection()

        self.assertEqual(conn.is_open(), False)

    def test_is_open_after_open(self):
        conn = self._create_connection()
        conn.open()

        self.assertEqual(conn.is_open(), True)

    def test_is_open_after_close(self):
        conn = self._create_connection()
        conn.open()
        conn.close()

        self.assertEqual(conn.is_open(), False)

    def test_return_data(self):
        conn = self._create_connection()

        conn.return_data(b"hello")
        conn.return_data(b"world")

        self.assertEqual(conn._read_buffer, [b"hello", b"world"])

    def test_get_connection_property(self):
        conn = self._create_connection()

        # returns None for a missing property
        self.assertEqual(conn.get_connection_property("missing"), None)

    def test_set_connection_property(self):
        conn = self._create_connection()

        conn.set_connection_property("key", "value")

        self.assertEqual(conn.get_connection_property("key"), "value")

    def test_unset_connection_property(self):
        conn = self._create_connection()

        conn.set_connection_property("key", "value")
        conn.unset_connection_property("key")

        self.assertEqual(conn.get_connection_property("key"), None)

    def test_get_connection_socket(self):
        mock_socket = mocks.MockSocket()
        conn = self._create_connection(mock_socket)

        self.assertEqual(conn.get_connection_socket(), mock_socket)

    def test_get_connection_address(self):
        conn = self._create_connection()

        self.assertEqual(conn.get_connection_address(), ("127.0.0.1", 8080))

    def test_get_base_connection_socket(self):
        mock_socket = mocks.MockSocket()
        conn = self._create_connection(mock_socket)

        self.assertEqual(conn.get_base_connection_socket(), mock_socket)

    def test_connection_opened_handlers_called(self):
        conn = self._create_connection()
        called = []

        conn.connection_opened_handlers.append(lambda c: called.append(c))
        conn.open()

        self.assertEqual(len(called), 1)
        self.assertEqual(called[0], conn)

    def test_connection_closed_handlers_called(self):
        conn = self._create_connection()
        called = []

        conn.connection_closed_handlers.append(lambda c: called.append(c))
        conn.open()
        conn.close()

        self.assertEqual(len(called), 1)
        self.assertEqual(called[0], conn)

    def test_receive_from_buffer(self):
        # when data is already in the read buffer receive should
        # return it immediately without touching the socket
        conn = self._create_connection()
        conn._read_buffer = [b"buffered"]

        data = conn.receive()

        self.assertEqual(data, b"buffered")
        self.assertEqual(conn._read_buffer, [])

    def test_receive_buffer_larger_than_chunk(self):
        # when a buffered element exceeds the chunk size only the
        # first chunk_size bytes are returned; the remainder (even
        # if empty due to the existing slicing order) is re-inserted
        conn = self._create_connection()
        conn._read_buffer = [b"A" * 10]

        data = conn.receive(chunk_size=4)

        self.assertEqual(data, b"AAAA")
        # the remainder slice is taken from the already-truncated element
        # so it is always b"" — this is the current behaviour
        self.assertEqual(conn._read_buffer, [b""])

    def test_ensure_socket_fd_valid(self):
        # _ensure_socket_fd should return the fd for a valid socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        try:
            conn = self._create_connection(server)
            fd = conn._ensure_socket_fd()
            self.assertEqual(fd, server.fileno())
        finally:
            server.close()

    def test_ensure_socket_fd_invalid(self):
        # a socket that raises on fileno() should cause _ensure_socket_fd
        # to close the connection and raise RequestClosed

        class BadSocket(object):
            def fileno(self):
                raise OSError("bad fd")

            def close(self):
                pass

            def setblocking(self, v):
                pass

        conn = self._create_connection(BadSocket())
        error_raised = False
        try:
            conn._ensure_socket_fd()
        except exceptions.RequestClosed:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_receive_timeout_raises(self):
        # when poll_socket returns not readable the connection
        # should be closed and ServerRequestTimeout raised
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        try:
            conn = self._create_connection(server)
            conn.connection_status = True
            error_raised = False
            try:
                # a very short timeout with no pending data forces a timeout
                conn.receive(request_timeout=0.001)
            except exceptions.ServerRequestTimeout:
                error_raised = True
            self.assertEqual(error_raised, True)
            self.assertEqual(conn.connection_status, False)
        finally:
            server.close()

    def test_process_exception_eagain(self):
        # EAGAIN/EWOULDBLOCK are expected on non-blocking sockets
        # and should be treated as graceful (return True)
        import errno as errno_module

        conn = self._create_connection()
        exception = socket.error(errno_module.EAGAIN, "try again")

        self.assertEqual(conn._process_exception(exception), True)

    def test_process_exception_ewouldblock(self):
        import errno as errno_module

        conn = self._create_connection()
        exception = socket.error(errno_module.EWOULDBLOCK, "would block")

        self.assertEqual(conn._process_exception(exception), True)

    def test_process_exception_wsaewouldblock(self):
        conn = self._create_connection()
        exception = socket.error(system.WSAEWOULDBLOCK, "would block (windows)")

        self.assertEqual(conn._process_exception(exception), True)

    def test_process_exception_critical(self):
        # a generic exception that is not a socket error should
        # return False, meaning it is a critical error
        conn = self._create_connection()
        exception = RuntimeError("critical error")

        self.assertEqual(conn._process_exception(exception), False)

    def test_process_exception_socket_error_critical(self):
        # a socket error with an unexpected error code should
        # also return False and be treated as critical
        import errno as errno_module

        conn = self._create_connection()
        exception = socket.error(errno_module.ECONNRESET, "connection reset")

        self.assertEqual(conn._process_exception(exception), False)


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Client Utils Exceptions test case"

    def test_client_utils_exception(self):
        exception = exceptions.ClientUtilsException()
        self.assertEqual(exception.message, None)

    def test_socket_provider_not_found(self):
        exception = exceptions.SocketProviderNotFound("ssl provider")
        self.assertEqual(exception.message, "ssl provider")
        self.assertEqual(str(exception), "Socket provider not found - ssl provider")

    def test_socket_upgrader_not_found(self):
        exception = exceptions.SocketUpgraderNotFound("tls upgrader")
        self.assertEqual(exception.message, "tls upgrader")
        self.assertEqual(str(exception), "Socket upgrader not found - tls upgrader")

    def test_client_request_timeout(self):
        exception = exceptions.ClientRequestTimeout("120s timeout")
        self.assertEqual(exception.message, "120s timeout")
        self.assertEqual(str(exception), "Client request timeout - 120s timeout")

    def test_server_request_timeout(self):
        exception = exceptions.ServerRequestTimeout("30s timeout")
        self.assertEqual(exception.message, "30s timeout")
        self.assertEqual(str(exception), "Server request timeout - 30s timeout")

    def test_client_response_timeout(self):
        exception = exceptions.ClientResponseTimeout("60s timeout")
        self.assertEqual(exception.message, "60s timeout")
        self.assertEqual(str(exception), "Client response timeout - 60s timeout")

    def test_server_response_timeout(self):
        exception = exceptions.ServerResponseTimeout("45s timeout")
        self.assertEqual(exception.message, "45s timeout")
        self.assertEqual(str(exception), "Server response timeout - 45s timeout")

    def test_request_closed(self):
        exception = exceptions.RequestClosed("connection reset")
        self.assertEqual(exception.message, "connection reset")
        self.assertEqual(str(exception), "Request closed - connection reset")

    def test_exception_inheritance(self):
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
