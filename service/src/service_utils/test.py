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

import select
import socket

import colony

from . import asynchronous
from . import exceptions
from . import mocks


class ServiceUtilsTest(colony.Test):
    """
    The service utils infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            SelectPollingTestCase,
            EpollPollingTestCase,
            Epoll2PollingTestCase,
            KqueuePollingTestCase,
            AbstractServiceTestCase,
            ExceptionsTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class SelectPollingTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Select Polling test case"

    def _skip_if_no_select(self):
        """
        Returns true if select is not available on the
        current platform (select is universally available).
        """

        return not hasattr(select, "select")

    def test_initialization(self):
        polling = asynchronous.SelectPolling()

        self.assertEqual(polling.readable_socket_list, set())
        self.assertEqual(polling.writeable_socket_list, set())
        self.assertEqual(polling.errors_socket_list, set())

    def test_register_read(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.READ)

        self.assertIn(10, polling.readable_socket_list)
        self.assertNotIn(10, polling.writeable_socket_list)

    def test_register_write(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.WRITE)

        self.assertIn(10, polling.writeable_socket_list)
        self.assertNotIn(10, polling.readable_socket_list)

    def test_register_error(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.ERROR)

        self.assertIn(10, polling.errors_socket_list)
        # error registration also adds to readable list
        # as closed connections are reported as read in select
        self.assertIn(10, polling.readable_socket_list)

    def test_register_combined(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.READ | asynchronous.ERROR)

        self.assertIn(10, polling.readable_socket_list)
        self.assertIn(10, polling.errors_socket_list)

    def test_unregister(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.READ | asynchronous.ERROR)
        polling.unregister(10)

        self.assertNotIn(10, polling.readable_socket_list)
        self.assertNotIn(10, polling.errors_socket_list)

    def test_unregister_partial(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.READ)
        polling.register(10, asynchronous.WRITE)
        polling.unregister(10, asynchronous.READ)

        self.assertNotIn(10, polling.readable_socket_list)
        self.assertIn(10, polling.writeable_socket_list)

    def test_unregister_not_registered(self):
        polling = asynchronous.SelectPolling()

        # should not raise for unregistered fd's
        polling.unregister(999)

    def test_modify(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.READ)
        polling.modify(10, asynchronous.WRITE)

        self.assertNotIn(10, polling.readable_socket_list)
        self.assertIn(10, polling.writeable_socket_list)

    def test_poll_with_real_socket(self):
        if self._skip_if_no_select():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.SelectPolling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)

        # poll with a very short timeout, no connections
        # pending so the result should be empty
        events = polling.poll(0.001)
        events_list = list(events)

        self.assertEqual(events_list, [])

        polling.unregister(server_fd)
        server.close()

    def test_multiple_fds(self):
        polling = asynchronous.SelectPolling()

        polling.register(10, asynchronous.READ)
        polling.register(20, asynchronous.READ)
        polling.register(30, asynchronous.WRITE)

        self.assertIn(10, polling.readable_socket_list)
        self.assertIn(20, polling.readable_socket_list)
        self.assertIn(30, polling.writeable_socket_list)

        self.assertEqual(len(polling.readable_socket_list), 2)
        self.assertEqual(len(polling.writeable_socket_list), 1)


class EpollPollingTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Epoll Polling test case"

    def _skip_if_no_epoll(self):
        """
        Returns true if epoll is not available on the
        current platform (not Linux).
        """

        return not hasattr(select, "epoll")

    def test_initialization(self):
        if self._skip_if_no_epoll():
            return

        polling = asynchronous.EpollPolling()

        self.assertEqual(polling.registered_map, {})

    def test_register_read(self):
        if self._skip_if_no_epoll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.EpollPolling()
        polling.register(server_fd, asynchronous.READ)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_register_combined(self):
        if self._skip_if_no_epoll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.EpollPolling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_unregister(self):
        if self._skip_if_no_epoll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.EpollPolling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)
        polling.unregister(server_fd)

        self.assertNotIn(server_fd, polling.registered_map)

        server.close()

    def test_unregister_not_registered(self):
        if self._skip_if_no_epoll():
            return

        polling = asynchronous.EpollPolling()

        # should not raise for unregistered fd's
        polling.unregister(999)

    def test_modify(self):
        if self._skip_if_no_epoll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.EpollPolling()
        polling.register(server_fd, asynchronous.READ)
        polling.modify(server_fd, asynchronous.WRITE)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_poll_empty(self):
        if self._skip_if_no_epoll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.EpollPolling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)

        # poll with a very short timeout, no connections
        # pending so the result should be empty
        events = polling.poll(0.001)
        events_list = list(events)

        self.assertEqual(events_list, [])

        polling.unregister(server_fd)
        server.close()

    def test_incremental_register(self):
        if self._skip_if_no_epoll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.EpollPolling()
        polling.register(server_fd, asynchronous.READ)
        polling.register(server_fd, asynchronous.WRITE)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()


class Epoll2PollingTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Epoll2 Polling test case"

    def _skip_if_no_poll(self):
        """
        Returns true if poll is not available on the
        current platform (not available on Windows).
        """

        return not hasattr(select, "poll")

    def test_initialization(self):
        if self._skip_if_no_poll():
            return

        polling = asynchronous.Epoll2Polling()

        self.assertEqual(polling.registered_map, {})

    def test_register_read(self):
        if self._skip_if_no_poll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.Epoll2Polling()
        polling.register(server_fd, asynchronous.READ)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_register_combined(self):
        if self._skip_if_no_poll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.Epoll2Polling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_unregister(self):
        if self._skip_if_no_poll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.Epoll2Polling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)
        polling.unregister(server_fd)

        self.assertNotIn(server_fd, polling.registered_map)

        server.close()

    def test_unregister_partial(self):
        if self._skip_if_no_poll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.Epoll2Polling()
        polling.register(server_fd, asynchronous.READ)
        polling.register(server_fd, asynchronous.WRITE)
        polling.unregister(server_fd, asynchronous.READ)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_unregister_not_registered(self):
        if self._skip_if_no_poll():
            return

        polling = asynchronous.Epoll2Polling()

        # should not raise for unregistered fd's
        polling.unregister(999)

    def test_modify(self):
        if self._skip_if_no_poll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.Epoll2Polling()
        polling.register(server_fd, asynchronous.READ)
        polling.modify(server_fd, asynchronous.WRITE)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_poll_empty(self):
        if self._skip_if_no_poll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.Epoll2Polling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)

        # poll with a very short timeout, no connections
        # pending so the result should be empty
        events = polling.poll(0.001)
        events_list = list(events)

        self.assertEqual(events_list, [])

        polling.unregister(server_fd)
        server.close()

    def test_incremental_register(self):
        if self._skip_if_no_poll():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.Epoll2Polling()
        polling.register(server_fd, asynchronous.READ)
        polling.register(server_fd, asynchronous.WRITE)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()


class KqueuePollingTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Kqueue Polling test case"

    def _skip_if_no_kqueue(self):
        """
        Returns true if kqueue is not available on the
        current platform (not BSD/macOS).
        """

        return not hasattr(select, "kqueue")

    def test_initialization(self):
        if self._skip_if_no_kqueue():
            return

        polling = asynchronous.KqueuePolling()

        self.assertEqual(polling.registered_map, {})

    def test_register_read(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_register_combined(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_unregister(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)
        polling.unregister(server_fd)

        self.assertNotIn(server_fd, polling.registered_map)

        server.close()

    def test_unregister_partial(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ)
        polling.register(server_fd, asynchronous.WRITE)
        polling.unregister(server_fd, asynchronous.READ)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_unregister_not_registered(self):
        if self._skip_if_no_kqueue():
            return

        polling = asynchronous.KqueuePolling()

        # should not raise for unregistered fd's
        polling.unregister(999)

    def test_modify(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ)
        polling.modify(server_fd, asynchronous.WRITE)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_poll_empty(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ | asynchronous.ERROR)

        # poll with a very short timeout, no connections
        # pending so the result should be empty
        events = polling.poll(0.001)
        events_list = list(events)

        self.assertEqual(events_list, [])

        polling.unregister(server_fd)
        server.close()

    def test_incremental_register(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ)
        polling.register(server_fd, asynchronous.WRITE)

        self.assertIn(server_fd, polling.registered_map)

        polling.unregister(server_fd)
        server.close()

    def test_poll_with_connection(self):
        if self._skip_if_no_kqueue():
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]
        server_fd = server.fileno()

        polling = asynchronous.KqueuePolling()
        polling.register(server_fd, asynchronous.READ)

        # creates a client connection to trigger a read event
        # on the server socket (incoming connection)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))

        # poll should now return the server fd as readable
        events = polling.poll(1.0)
        events_list = list(events)

        self.assertTrue(len(events_list) > 0)

        # verifies that the server fd is in the events
        event_fds = [fd for fd, _mask in events_list]
        self.assertIn(server_fd, event_fds)

        polling.unregister(server_fd)
        client.close()
        server.close()


class AbstractServiceTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Abstract Service test case"

    def test_add_remove_socket(self):
        mock_plugin = mocks.MockPlugin()
        mock_socket = mocks.MockSocket(10)

        service = self._create_service(mock_plugin)

        service.add_socket(mock_socket, ("127.0.0.1", 12345), 8080)

        self.assertIn(10, service.socket_fd_map)
        self.assertIn(mock_socket, service.client_connection_map)

        service.remove_socket(mock_socket)

        self.assertNotIn(10, service.socket_fd_map)
        self.assertNotIn(mock_socket, service.client_connection_map)
        self.assertTrue(mock_socket._closed)

    def test_remove_socket_resilient(self):
        mock_plugin = mocks.MockPlugin()
        mock_socket = mocks.MockSocket(10)

        service = self._create_service(mock_plugin)

        service.add_socket(mock_socket, ("127.0.0.1", 12345), 8080)

        # manually remove the client connection to simulate
        # a partial registration state
        del service.client_connection_map[mock_socket]

        # remove_socket should still close the socket without
        # raising even if the client connection is missing
        service.remove_socket(mock_socket)

        self.assertNotIn(10, service.socket_fd_map)
        self.assertTrue(mock_socket._closed)

    def test_add_socket_cleanup_on_error(self):
        mock_plugin = mocks.MockPlugin()
        mock_socket = mocks.MockSocket(10)

        service = self._create_service(mock_plugin)

        # save the original add_handler to restore later
        _original_add_handler = service.add_handler

        # make add_handler raise to simulate registration failure
        def failing_add_handler(socket_fd, callback, operation):
            raise RuntimeError("test error")

        service.add_handler = failing_add_handler

        # add_socket should clean up partially registered state
        error_raised = False
        try:
            service.add_socket(mock_socket, ("127.0.0.1", 12345), 8080)
        except RuntimeError:
            error_raised = True

        self.assertTrue(error_raised)
        self.assertNotIn(10, service.socket_fd_map)
        self.assertNotIn(mock_socket, service.client_connection_map)

        service.add_handler = _original_add_handler

    def test_add_remove_handler(self):
        mock_plugin = mocks.MockPlugin()

        service = self._create_service(mock_plugin)

        def handler(socket):
            pass

        service.add_handler(10, handler, asynchronous.READ)

        tuple_key = (10, asynchronous.READ)
        self.assertIn(tuple_key, service.handlers_map)
        self.assertIn(handler, service.handlers_map[tuple_key])

        service.remove_handler(10, handler, asynchronous.READ)

        self.assertNotIn(tuple_key, service.handlers_map)

    def test_call_handlers_tuple_missing_fd(self):
        mock_plugin = mocks.MockPlugin()

        service = self._create_service(mock_plugin)

        # calling handlers for a non-existent fd should
        # not raise an exception
        service.call_handlers_tuple((999, asynchronous.READ))

    def test_call_handlers_tuple_exception_closes_socket(self):
        mock_plugin = mocks.MockPlugin()
        mock_socket = mocks.MockSocket(10)

        service = self._create_service(mock_plugin)
        service.socket_fd_map[10] = mock_socket

        def failing_handler(socket):
            raise RuntimeError("test error")

        service.add_handler(10, failing_handler, asynchronous.READ)

        # the handler exception should cause the socket to be
        # closed directly since there is no client connection
        service.call_handlers_tuple((10, asynchronous.READ))

        self.assertTrue(mock_socket._closed)

    def _create_service(self, mock_plugin):
        """
        Creates a minimal abstract service instance for
        testing purposes.

        :type mock_plugin: MockPlugin
        :param mock_plugin: The mock plugin.
        :rtype: AbstractService
        :return: The created service instance.
        """

        service = asynchronous.AbstractService.__new__(asynchronous.AbstractService)
        service.service_plugin = mock_plugin
        service.time_events = []
        service.service_sockets = []
        service.service_socket_end_point_map = {}
        service.handlers_map = {}
        service.socket_fd_map = {}
        service.address_fd_map = {}
        service.pending_fd_map = {}
        service.client_connection_map = {}
        service.poll_instance = asynchronous.SelectPolling()
        service.service_execution_thread = None
        return service


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Service Utils Exceptions test case"

    def test_service_utils_exception(self):
        exception = exceptions.ServiceUtilsException()
        self.assertEqual(exception.message, None)

    def test_socket_provider_not_found(self):
        exception = exceptions.SocketProviderNotFound("ssl provider")
        self.assertEqual(exception.message, "ssl provider")
        self.assertEqual(str(exception), "Socket provider not found - ssl provider")

    def test_socket_upgrader_not_found(self):
        exception = exceptions.SocketUpgraderNotFound("tls upgrader")
        self.assertEqual(exception.message, "tls upgrader")
        self.assertEqual(str(exception), "Socket upgrader not found - tls upgrader")

    def test_server_request_timeout(self):
        exception = exceptions.ServerRequestTimeout("30s timeout")
        self.assertEqual(exception.message, "30s timeout")
        self.assertEqual(str(exception), "Server request timeout - 30s timeout")

    def test_client_request_timeout(self):
        exception = exceptions.ClientRequestTimeout("120s timeout")
        self.assertEqual(exception.message, "120s timeout")
        self.assertEqual(str(exception), "Client request timeout - 120s timeout")

    def test_server_response_timeout(self):
        exception = exceptions.ServerResponseTimeout("45s timeout")
        self.assertEqual(exception.message, "45s timeout")
        self.assertEqual(str(exception), "Server response timeout - 45s timeout")

    def test_client_response_timeout(self):
        exception = exceptions.ClientResponseTimeout("60s timeout")
        self.assertEqual(exception.message, "60s timeout")
        self.assertEqual(str(exception), "Client response timeout - 60s timeout")

    def test_request_closed(self):
        exception = exceptions.RequestClosed("connection reset")
        self.assertEqual(exception.message, "connection reset")
        self.assertEqual(str(exception), "Request closed - connection reset")

    def test_port_starvation_reached(self):
        exception = exceptions.PortStarvationReached("no ports available")
        self.assertEqual(exception.message, "no ports available")
        self.assertEqual(str(exception), "Port starvation reached - no ports available")

    def test_connection_change_failure(self):
        exception = exceptions.ConnectionChangeFailure("upgrade failed")
        self.assertEqual(exception.message, "upgrade failed")
        self.assertEqual(str(exception), "Connection change failure - upgrade failed")

    def test_exception_inheritance(self):
        exception_list = [
            exceptions.SocketProviderNotFound("test"),
            exceptions.SocketUpgraderNotFound("test"),
            exceptions.ServerRequestTimeout("test"),
            exceptions.ClientRequestTimeout("test"),
            exceptions.ServerResponseTimeout("test"),
            exceptions.ClientResponseTimeout("test"),
            exceptions.RequestClosed("test"),
            exceptions.PortStarvationReached("test"),
            exceptions.ConnectionChangeFailure("test"),
        ]
        for exception in exception_list:
            self.assertTrue(isinstance(exception, exceptions.ServiceUtilsException))
            self.assertTrue(isinstance(exception, colony.ColonyException))
