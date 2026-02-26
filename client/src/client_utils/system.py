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
import errno
import select
import socket
import threading

import colony

from . import exceptions

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 120
""" The request timeout """

RESPONSE_TIMEOUT = 120
""" The response timeout """

CONNECTION_TIMEOUT = 600
""" The connection timeout """

CHUNK_SIZE = 4096
""" The chunk size """

RECEIVE_RETRIES = 3
""" The receive retries """

SEND_RETRIES = 3
""" The send retries """

RECONNECT_RETRIES = 3
""" The reconnect retries """

_EPOLLIN = 0x001
_EPOLLOUT = 0x004
_EPOLLERR = 0x008
_EPOLLHUP = 0x010
""" The various constant values that are going to be
used in the detection of errors and states for the
non blocking connection states """

READ = _EPOLLIN
""" Condition to be used for the read operation on a
certain fd, alias to an existing epoll value """

WRITE = _EPOLLOUT
""" Write condition flag that may be used by one trying
to register for write operation notifications """

ERROR = _EPOLLERR | _EPOLLHUP
""" The error condition that gathers all the possible
errors from the epoll strategy """

WSAEWOULDBLOCK = 10035
""" Windows based value for the error raised when a non
blocking connection is not able to read/write more, this
error should be raised constantly in no blocking connections """

SELECT_MAX_FD = 1024
""" The maximum file descriptor value for select, above
this value the select call is going to raise an error on
most Linux based systems (FD_SETSIZE) """

DEFAULT_TYPE = "connection"
""" The default type client """


def poll_socket(socket_fd, operations, timeout):
    """
    Polls a single socket file descriptor for the given operations
    using the best available polling mechanism on the current platform.

    Uses epoll on Linux, kqueue on BSD/macOS, poll as a portable
    Unix fallback, and select as the final Windows-compatible fallback.
    Unlike select, epoll/kqueue/poll have no file descriptor limit.

    :type socket_fd: int
    :param socket_fd: The socket file descriptor to poll.
    :type operations: int
    :param operations: The bitmask of operations to poll for (READ, WRITE).
    :type timeout: float
    :param timeout: The maximum time in seconds to wait for events.
    :rtype: tuple
    :return: A tuple of (readable, writeable) boolean values.
    """

    # uses epoll on Linux, which has no file descriptor limit
    # and is more efficient than select for large numbers of fds
    if hasattr(select, "epoll"):
        epoll = select.epoll()
        try:
            event_mask = 0
            if operations & READ:
                event_mask |= _EPOLLIN
            if operations & WRITE:
                event_mask |= _EPOLLOUT
            epoll.register(socket_fd, event_mask)
            try:
                events = epoll.poll(timeout)
            finally:
                epoll.unregister(socket_fd)
        finally:
            epoll.close()
        readable = any(mask & _EPOLLIN for _fd, mask in events)
        writeable = any(mask & _EPOLLOUT for _fd, mask in events)
        return readable, writeable

    # uses kqueue on BSD/macOS, which also has no file descriptor limit
    # and is the native mechanism on those platforms
    if hasattr(select, "kqueue"):
        kqueue = select.kqueue()
        try:
            changelist = []
            if operations & READ:
                changelist.append(
                    select.kevent(
                        socket_fd,
                        filter=select.KQ_FILTER_READ,
                        flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
                    )
                )
            if operations & WRITE:
                changelist.append(
                    select.kevent(
                        socket_fd,
                        filter=select.KQ_FILTER_WRITE,
                        flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
                    )
                )
            events = kqueue.control(changelist, len(changelist), timeout)
        finally:
            kqueue.close()
        readable = any(e.filter == select.KQ_FILTER_READ for e in events)
        writeable = any(e.filter == select.KQ_FILTER_WRITE for e in events)
        return readable, writeable

    # uses poll as a portable Unix fallback, which also has no
    # file descriptor limit unlike select (available on most Unix systems)
    if hasattr(select, "poll"):
        poll_instance = select.poll()
        event_mask = 0
        if operations & READ:
            event_mask |= _EPOLLIN
        if operations & WRITE:
            event_mask |= _EPOLLOUT
        poll_instance.register(socket_fd, event_mask)
        events = poll_instance.poll(timeout * 1000)
        poll_instance.unregister(socket_fd)
        readable = any(mask & _EPOLLIN for _fd, mask in events)
        writeable = any(mask & _EPOLLOUT for _fd, mask in events)
        return readable, writeable

    # falls back to select, which is portable across all platforms
    # including Windows but is limited to file descriptors below 1024
    # (FD_SETSIZE) on Linux — rejects any fd that would cause select to fail
    if socket_fd >= SELECT_MAX_FD:
        raise exceptions.RequestClosed(
            "invalid socket: filedescriptor %d out of range for select" % socket_fd
        )
    read_fds = [socket_fd] if operations & READ else []
    write_fds = [socket_fd] if operations & WRITE else []
    readable_fds, writeable_fds, _errors = select.select(
        read_fds, write_fds, [], timeout
    )
    return bool(readable_fds), bool(writeable_fds)


class ClientUtils(colony.System):
    """
    The client utilities class, responsible for providing a centralized
    management system for client socket connections within the Colony
    framework.

    This class serves as the main entry point for creating and configuring
    network clients. It manages socket provider and upgrader plugins,
    allowing dynamic registration and lookup of different socket types
    (e.g., normal, SSL/TLS) and connection upgraders.

    The class maintains two plugin maps:
    - socket_provider_plugins_map: Maps socket provider names (e.g., "normal",
      "ssl") to their respective plugins, enabling socket creation through
      a unified interface.
    - socket_upgrader_plugins_map: Maps socket upgrader names to their
      respective plugins, allowing connection upgrades (e.g., upgrading
      a plain connection to SSL/TLS).

    Typical usage involves:
    1. Loading socket provider/upgrader plugins via the load methods.
    2. Generating client instances using generate_client() with the
       desired configuration parameters.
    3. Using the generated AbstractClient to create and manage connections.

    :see: AbstractClient
    :see: ClientConnection
    """

    socket_provider_plugins_map = {}
    """ The socket provider plugins map, containing the mapping between
    socket provider names and their corresponding plugin instances """

    socket_upgrader_plugins_map = {}
    """ The socket upgrader plugins map, containing the mapping between
    socket upgrader names and their corresponding plugin instances """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.socket_provider_plugins_map = {}
        self.socket_upgrader_plugins_map = {}

    def generate_client(self, parameters):
        """
        Generates a new client for the given parameters.

        :type parameters: Dictionary
        :param parameters: The parameters for client generation.
        :rtype: AbstractClient
        :return: The generated client.
        """

        return AbstractClient(self, self.plugin, parameters)

    def socket_provider_load(self, socket_provider_plugin):
        """
        Loads a socket provider plugin.

        :type socket_provider_plugin: Plugin
        :param socket_provider_plugin: The socket provider plugin
        to be loaded.
        """

        # retrieves the plugin provider name and then sets the socket
        # provider plugin in the socket provider plugins map
        provider_name = socket_provider_plugin.get_provider_name()
        self.socket_provider_plugins_map[provider_name] = socket_provider_plugin

    def socket_provider_unload(self, socket_provider_plugin):
        """
        Unloads a socket provider plugin.

        :type socket_provider_plugin: Plugin
        :param socket_provider_plugin: The socket provider plugin
        to be unloaded.
        """

        # retrieves the plugin provider name and then removes the
        # socket provider plugin from the socket provider plugins map
        provider_name = socket_provider_plugin.get_provider_name()
        del self.socket_provider_plugins_map[provider_name]

    def socket_upgrader_load(self, socket_upgrader_plugin):
        """
        Loads a socket upgrader plugin.

        :type socket_upgrader_plugin: Plugin
        :param socket_upgrader_plugin: The socket upgrader plugin
        to be loaded.
        """

        # retrieves the plugin upgrader name
        upgrader_name = socket_upgrader_plugin.get_upgrader_name()

        # sets the socket upgrader plugin in the socket upgrader plugins map
        self.socket_upgrader_plugins_map[upgrader_name] = socket_upgrader_plugin

    def socket_upgrader_unload(self, socket_upgrader_plugin):
        """
        Unloads a socket upgrader plugin.

        :type socket_upgrader_plugin: Plugin
        :param socket_upgrader_plugin: The socket upgrader plugin
        to be unloaded.
        """

        # retrieves the plugin upgrader name
        upgrader_name = socket_upgrader_plugin.get_upgrader_name()

        # removes the socket upgrader plugin from the socket upgrader plugins map
        del self.socket_upgrader_plugins_map[upgrader_name]


class AbstractClient(object):
    """
    The abstract client class.
    """

    client_utils = None
    """ The client """

    client_utils_plugin = None
    """ The client plugin """

    client_type = None
    """ The client type """

    client_plugin = None
    """ The client plugin """

    chunk_size = CHUNK_SIZE
    """ The chunk size """

    client_configuration = {}
    """ The client configuration """

    client_connection_timeout = CLIENT_CONNECTION_TIMEOUT
    """ The client connection timeout """

    connection_timeout = CONNECTION_TIMEOUT
    """ The connection timeout """

    request_timeout = REQUEST_TIMEOUT
    """ The request timeout """

    response_timeout = RESPONSE_TIMEOUT
    """ The response timeout """

    client_connections_map = {}
    """ The map containing the client connections """

    def __init__(self, client_utils, client_utils_plugin, parameters={}):
        """
        Constructor of the class.

        :type client_utils: ClientUtils
        :param client_utils: The client.
        :type client_utils_plugin: ClientUtilsPlugin
        :param client_utils_plugin: The client plugin.
        :type parameters: Dictionary
        :param parameters: The parameters
        """

        self.client_utils = client_utils
        self.client_utils_plugin = client_utils_plugin

        self.client_type = parameters.get("type", DEFAULT_TYPE)
        self.client_plugin = parameters.get("client_plugin", None)
        self.chunk_size = parameters.get("chunk_size", CHUNK_SIZE)
        self.client_configuration = parameters.get("client_configuration", {})
        self.client_connection_timeout = parameters.get(
            "client_connection_timeout", CLIENT_CONNECTION_TIMEOUT
        )
        self.connection_timeout = parameters.get(
            "connection_timeout", CONNECTION_TIMEOUT
        )
        self.request_timeout = parameters.get("request_timeout", REQUEST_TIMEOUT)
        self.response_timeout = parameters.get("response_timeout", RESPONSE_TIMEOUT)

        self.client_connections_map = {}

    def start_client(self):
        """
        Starts the client.
        """

        pass

    def stop_client(self):
        """
        Stops the client.
        """

        # iterates over all the client connections, to closes them
        for _connection_tuple, client_connection in colony.legacy.items(
            self.client_connections_map
        ):
            # closes the client connection
            client_connection.close()

    def get_client_connection(self, connection_tuple, open_connection=True):
        """
        Retrieves the client connection for the given
        connection tuple.

        :type connection_tuple: Tuple
        :param connection_tuple: The tuple containing
        the connection reference.
        :type open_connection: bool
        :param open_connection: If the connection should be opened
        in case the connection is going to be created.
        :rtype: ClientConnection
        :return: The retrieved client connection.
        """

        # generates an hashable connection tuple from the original
        # connection tuple
        connection_tuple_hashable = self._generate_connection_tuple_hashable(
            connection_tuple
        )

        # tries to retrieve the current client connection
        client_connection = self.client_connections_map.get(
            connection_tuple_hashable, None
        )

        # in case the connection tuple is not present in the
        # client connections map or the current client connection
        # is not open, then we need to run proper close diligence
        if not client_connection or not client_connection.is_open():
            # in case there's an existing (closed) client connection
            # closes it explicitly to release the underlying socket
            # file descriptor preventing accumulation of stale sockets
            if client_connection:
                try:
                    client_connection.close()
                except Exception:
                    pass

            # creates the a new client connection for the given connection tuple
            # and sets the client connection in the client connections map
            client_connection = self._create_client_connection(connection_tuple)
            self.client_connections_map[connection_tuple_hashable] = client_connection

        # retrieves the client connection for the client
        # connections map and then in case the connection should
        # be opened and the client  connection is not open, opens
        # the client connection
        client_connection = self.client_connections_map[connection_tuple_hashable]
        if open_connection and not client_connection.is_open():
            client_connection.open()

        # returns the client connection
        return client_connection

    def _create_client_connection(self, connection_tuple):
        """
        Creates the client connection for the given
        connection tuple.

        :type connection_tuple: Tuple
        :param connection_tuple: The tuple containing
        the connection reference.
        :rtype: ClientConnection
        :return: The created client connection.
        """

        # retrieves the host, the port, the persistent, the socket name and
        # the socket parameters from the connection tuple
        host, port, persistent, socket_name, socket_parameters = connection_tuple

        # creates the address tuple
        address = (host, port)

        # creates a socket for the client with
        # the given socket name
        client_connection_socket = self._get_socket(socket_name, socket_parameters)

        # retrieves the client connection
        client_connection = ClientConnection(
            self.client_plugin,
            self,
            client_connection_socket,
            address,
            persistent,
            socket_name,
            socket_parameters,
            self.request_timeout,
            self.response_timeout,
            self.chunk_size,
        )

        # returns the client connection
        return client_connection

    def _get_socket(self, socket_name="normal", socket_parameters={}):
        """
        Retrieves the socket for the given socket name
        using the socket provider plugins.

        :type socket_name: String
        :param socket_name: The name of the socket to be retrieved.
        :type socket_parameters: Dictionary
        :param socket_parameters: The parameters of the socket to be retrieved.
        :rtype: Socket
        :return: The socket for the given socket name.
        """

        # retrieves the socket provider plugins map
        socket_provider_plugins_map = self.client_utils.socket_provider_plugins_map

        # in case the socket name is available in the socket
        # provider plugins map
        if socket_name in socket_provider_plugins_map:
            # retrieves the socket provider plugin from the socket provider plugins map
            socket_provider_plugin = socket_provider_plugins_map[socket_name]

            # creates the parameters for the socket provider, the
            # handshake process in case it's required must be forced
            # then copies the socket parameters to the parameters map
            parameters = {"do_handshake_on_connect": True}
            colony.map_copy(socket_parameters, parameters)

            # creates a new socket with the socket provider plugin
            # and returns the created socket to the caller method
            socket = socket_provider_plugin.provide_socket_parameters(parameters)
            return socket
        else:
            # raises the socket provider not found exception
            raise exceptions.SocketProviderNotFound(
                "socket provider %s not found" % socket_name
            )

    def _generate_connection_tuple_hashable(self, connection_tuple):
        """
        Generates an hashable connection tuple from
        the original connection tuple.

        :type connection_tuple: Tuple
        :param connection_tuple: The connection tuple to be converted
        to hashable.
        :rtype: Tuple
        :return: The hashable connection tuple.
        """

        # copies the connection tuple as the connection tuple hashable
        connection_tuple_hashable = list(connection_tuple)

        # sets the last element of the connection tuple hashable as the
        # items tuple instead of the dictionary in order to avoid unhashable problems
        connection_tuple_hashable[4] = tuple(
            colony.legacy.items(connection_tuple_hashable[4])
        )

        # converts the connection tuple hashable into a tuple
        # in order to hashable
        connection_tuple_hashable = tuple(connection_tuple_hashable)

        # returns the connection tuple hashable
        return connection_tuple_hashable


class ClientConnection(object):
    """
    The client connection class.
    Describes a client connection.
    """

    client_plugin = None
    """ The client plugin """

    client = None
    """ The client """

    connection_socket = None
    """ The connection socket """

    connection_address = None
    """ The connection address """

    connection_persistent = True
    """ The connection persistent """

    connection_socket_name = None
    """ The connection socket name """

    connection_socket_parameters = None
    """ The connection socket parameters """

    connection_request_timeout = None
    """ The connection request timeout """

    connection_response_timeout = None
    """ The connection response timeout """

    connection_chunk_size = None
    """ The connection chunk size """

    connection_opened_handlers = []
    """ The connection opened handlers """

    connection_closed_handlers = []
    """ The connection closed handlers """

    connection_properties = {}
    """ The connection properties map """

    connection_status = False
    """ The connection status flag """

    cancel_time = None
    """ The cancel time """

    _connection_socket = None
    """ The original connection socket """

    _read_buffer = []
    """ The read buffer """

    _read_lock = None
    """ The read lock """

    _write_lock = None
    """ The write lock """

    def __init__(
        self,
        client_plugin,
        client,
        connection_socket,
        connection_address,
        connection_persistent,
        connection_socket_name,
        connection_socket_parameters,
        connection_request_timeout,
        connection_response_timeout,
        connection_chunk_size,
    ):
        """
        Constructor of the class.

        :type client_plugin: Plugin
        :param client_plugin: The client plugin.
        :type client: AbstractClient
        :param client: The client.
        :type connection_socket: Socket
        :param connection_socket: The connection socket.
        :type connection_address: Tuple
        :param connection_address: The connection address.
        :type connection_persistent: bool
        :param connection_persistent: If the connection meant to be persistent.
        :type connection_socket_name: String
        :param connection_socket_name: The connection socket name.
        :type connection_socket_parameters: String
        :param connection_socket_parameters: The connection socket parameters.
        :type connection_request_timeout: float
        :param connection_request_timeout: The connection request timeout.
        :type connection_response_timeout: float
        :param connection_response_timeout: The connection response timeout.
        :type connection_chunk_size: int
        :param connection_chunk_size: The connection chunk size.
        """

        self.client_plugin = client_plugin
        self.client = client
        self.connection_socket = connection_socket
        self.connection_address = connection_address
        self.connection_persistent = connection_persistent
        self.connection_socket_name = connection_socket_name
        self.connection_socket_parameters = connection_socket_parameters
        self.connection_request_timeout = connection_request_timeout
        self.connection_response_timeout = connection_response_timeout
        self.connection_chunk_size = connection_chunk_size

        self._connection_socket = connection_socket

        self.connection_opened_handlers = []
        self.connection_closed_handlers = []
        self.connection_properties = {}

        self._read_buffer = []
        self._read_lock = threading.RLock()
        self._write_lock = threading.RLock()

    def __repr__(self):
        return "(%s, %s)" % (self.connection_address, self.connection_socket_name)

    def open(self):
        """
        Opens the connection, effectively making it ready for
        data transfer operations.
        """

        # connects the connection socket to the connection address
        # the connection is only created in case the connection is persistent
        if self.connection_persistent:
            self.connection_socket.connect(self.connection_address)

        # sets the socket to non blocking mode
        self.connection_socket.setblocking(0)

        # prints debug message about connection
        self.client_plugin.debug("Connected to: %s" % str(self.connection_address))

        # calls the connection opened handlers
        self._call_connection_opened_handlers()

        # resets the read buffer
        self._read_buffer = []

        # sets the connection status flag
        self.connection_status = True

    def close(self):
        """
        Closes the connection, disabling any further data
        transfer operations.
        """

        # unsets the connection status flag
        self.connection_status = False

        # resets the read buffer
        self._read_buffer = []

        # closes the connection socket
        self.connection_socket.close()

        # calls the connection closed handlers
        self._call_connection_closed_handlers()

        # prints debug message about connection
        self.client_plugin.debug("Disconnected from: %s" % str(self.connection_address))

    def cancel(self, delta_time):
        """
        Cancels (closes) the given connection in
        the given amount of seconds.

        :type delta_time: float
        :param delta_time: The amount of seconds until canceling.
        """

        # sets the cancel time
        self.cancel_time = time.time() + delta_time

    def upgrade(self, socket_upgrader, parameters):
        """
        Upgrades the current connection socket, using
        the the upgrader with the given name and the given parameters.

        :type socket_upgrader: String
        :param socket_upgrader: The name of the socket upgrader.
        :type parameters: Dictionary
        :param parameters: The parameters to the upgrade process.
        """

        # retrieves the client
        client_utils = self.client.client_utils

        # retrieves the socket upgrader plugins map
        socket_upgrader_plugins_map = client_utils.socket_upgrader_plugins_map

        # in case the upgrader handler is not found in the handler plugins map
        # raises the socket upgrader not found exception
        if not socket_upgrader in socket_upgrader_plugins_map:
            raise exceptions.SocketUpgraderNotFound(
                "socket upgrader %s not found" % self.socket_upgrader
            )

        # retrieves the socket upgrader plugin
        socket_upgrader_plugin = client_utils.socket_upgrader_plugins_map[
            socket_upgrader
        ]

        # upgrades the current connection socket using the socket upgrader plugin
        self.connection_socket = socket_upgrader_plugin.upgrade_socket_parameters(
            self.connection_socket, parameters
        )

        # sets the socket to non blocking mode
        self.connection_socket.setblocking(0)

    def receive(self, request_timeout=None, chunk_size=None, retries=RECEIVE_RETRIES):
        """
        Receives the data from the current connection socket, with the
        given timeout and with a maximum size given by the chunk size.

        :type request_timeout: float
        :param request_timeout: The timeout to be used in data receiving.
        :type chunk_size: int
        :param chunk_size: The maximum size of the chunk to be received.
        :type retries: int
        :param retries: The number of retries to be used.
        :rtype: String
        :return: The received data.
        """

        self._read_lock.acquire()
        try:
            return_value = self._receive(request_timeout, chunk_size, retries)
        finally:
            self._read_lock.release()
        return return_value

    def send(self, message, response_timeout=None, retries=SEND_RETRIES):
        """
        Sends the given message to the socket.
        Raises an exception in case there is a problem sending
        the message.

        :type message: String
        :param message: The message to be sent.
        :type request_timeout: float
        :param request_timeout: The timeout to be used in data sending.
        :type retries: int
        :param retries: The number of retries to be used.
        """

        self._write_lock.acquire()
        try:
            self._send(message, response_timeout, retries)
        finally:
            self._write_lock.release()

    def return_data(self, data):
        """
        Returns the given data to the connection
        internal buffer.

        :type data: String
        :param data: The data to be returned to the
        connection internal buffer.
        """

        self._read_buffer.append(data)

    def is_open(self):
        """
        Retrieves if the current connection is open.

        :rtype: bool
        :return: If the current connection is open.
        """

        return self.connection_status

    def get_connection_property(self, property_name):
        """
        Retrieves the connection property for the given name.

        :type property_name: String
        :param property_name: The name of the property to
        be retrieved.
        :rtype: Object
        :return: The value of the retrieved property.
        """

        return self.connection_properties.get(property_name, None)

    def set_connection_property(self, property_name, property_value):
        """
        Sets a connection property, associating the given name
        with the given value.

        :type property_name: String
        :param property_name: The name of the property to set.
        :type property_value: Object
        :param property_value: The value of the property to set.
        """

        self.connection_properties[property_name] = property_value

    def unset_connection_property(self, property_name):
        """
        Unsets a connection property, removing it from the internal
        structures.

        :type property_name: String
        :param property_name: The name of the property to unset.
        """

        del self.connection_properties[property_name]

    def get_connection_tuple(self):
        """
        Returns a tuple representing the connection.

        :rtype: Tuple
        :return: A tuple representing the connection.
        """

        return (self._connection_socket, self.connection_address, self.connection_port)

    def get_connection_socket(self):
        """
        Retrieves the connection socket.

        :rtype: Socket
        :return: The connection socket.
        """

        return self.connection_socket

    def get_connection_address(self):
        """
        Retrieves the connection address.

        :rtype: Tuple
        :return: The connection address.
        """

        return self.connection_address

    def get_base_connection_socket(self):
        """
        Retrieves the base connection socket.

        :rtype: Socket
        :return: The base connection socket.
        """

        return self._connection_socket

    def _receive(self, request_timeout, chunk_size, retries):
        """
        Receives the data from the current connection socket, with the
        given timeout and with a maximum size given by the chunk size.
        This method is not thread safe.

        :type request_timeout: float
        :param request_timeout: The timeout to be used in data receiving.
        :type chunk_size: int
        :param chunk_size: The maximum size of the chunk to be received.
        :type retries: int
        :param retries: The number of retries to be used.
        :rtype: String
        :return: The received data.
        """

        # retrieves the request timeout
        request_timeout = (
            request_timeout and request_timeout or self.connection_request_timeout
        )

        # retrieves the chunk size
        chunk_size = chunk_size and chunk_size or self.connection_chunk_size

        # in case the read buffer is not empty
        if self._read_buffer:
            # retrieves the read buffer element
            read_buffer_element = self._read_buffer.pop(0)

            # retrieves the read buffer element length
            read_buffer_element_length = len(read_buffer_element)

            # in case the read buffer element length is greater
            # than the chunk size
            if read_buffer_element_length > chunk_size:
                # retrieves the (sub) read buffer element
                read_buffer_element = read_buffer_element[:chunk_size]

                # retrieves the read buffer element remaining
                read_buffer_element_remaining = read_buffer_element[chunk_size:]

                # inserts the read buffer element remaining in the read buffer
                self._read_buffer.insert(0, read_buffer_element_remaining)

            # returns the read buffer element
            return read_buffer_element

        # unsets the read flag
        read_flag = False

        # iterates continuously
        while True:
            # retrieves the file descriptor for the current connection
            # socket, raising in case the socket is invalid or closed
            file_descriptor = self._ensure_socket_fd()

            try:
                # polls the connection socket for read readiness using
                # the best available polling mechanism on this platform
                readable, _writeable = poll_socket(
                    file_descriptor, READ, request_timeout
                )
            except Exception as exception:
                # closes the connection and then raises the
                # request closed exception
                self.close()
                raise exceptions.RequestClosed(
                    "invalid socket: %s" % colony.legacy.UNICODE(exception)
                )

            if not readable:
                # closes the connection and then raises the
                # server request timeout exception
                self.close()
                raise exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
            try:
                # iterates continuously
                while True:
                    # receives the data in chunks and adds the received
                    # data to the read buffer sequence, then sets the read
                    # flag meaning that at least one value has been read
                    data = self.connection_socket.recv(chunk_size)
                    self._read_buffer.append(data)
                    read_flag = True

                    # in case no data is received (end of connection)
                    # must break the current loop
                    if not data:
                        break

            except Exception as exception:
                # in case there was at least one successful read
                # breaks the current loop (read complete)
                if read_flag:
                    break

                # tries to process the exception, meaning that the
                # exception is going to be tested against a series
                # of validation and in case it's considered valid
                # it's ignored and the loop continues
                if self._process_exception(exception):
                    continue

                # in case the number of retries (available)
                # is greater than zero, decrements the retries value
                # and then continues the current loop
                if retries > 0:
                    retries -= 1
                    continue

                # otherwise an exception should be raised as this is considered
                # a critical exception and top level must be notified
                else:
                    # closes the connection meaning that no more data is going
                    # to be sent through the connection and socket
                    self.close()

                    # raises the client request timeout exception so that the
                    # top layers are properly notified about the issue
                    raise exceptions.ClientRequestTimeout(
                        "problem receiving data: " + colony.legacy.UNICODE(exception)
                    )
            except:
                # closes the current client and then raises the exception
                # to the upper layers for proper processing
                self.close()
                raise

            # breaks the loop
            break

        # pops the element from the read buffer
        data = self._read_buffer.pop(0)

        # returns the data
        return data

    def _send(self, message, response_timeout=None, retries=SEND_RETRIES):
        """
        Sends the given message to the socket.
        Raises an exception in case there is a problem sending
        the message.
        This method is not thread safe.

        :type message: String
        :param message: The message to be sent.
        :type request_timeout: float
        :param request_timeout: The timeout to be used in data sending.
        :type retries: int
        :param retries: The number of retries to be used.
        """

        # retrieves the response timeout
        response_timeout = (
            response_timeout and response_timeout or self.connection_response_timeout
        )

        # retrieves the number of bytes in the message
        number_bytes = len(message)

        # sets the initial number of reconnection retries available
        # to be used to limit the number of reconnection attempts
        reconnect_retries = RECONNECT_RETRIES

        # iterates over all the read buffer data read from the client
        # to make decisions on either reconnect or not
        for data in self._read_buffer:
            # in case the data is invalid meaning that the connection
            # has been dropped for some reason a reconnection attempt
            # must be performed to retry the client
            if not data:
                self.client_plugin.debug(
                    "Received empty data (in read buffer), reconnecting socket"
                )
                self._reconnect_connection_socket()
                reconnect_retries -= 1
                break

        # iterates continuously, trying to poll
        while True:
            # retrieves the file descriptor for the current connection
            # socket, raising in case the socket is invalid or closed
            file_descriptor = self._ensure_socket_fd()

            try:
                # polls the connection socket for both read and write
                # readiness using the best available polling mechanism
                readable, writeable = poll_socket(
                    file_descriptor, READ | WRITE, response_timeout
                )
            except Exception as exception:
                # closes the connection and raises a request closed exception
                # meaning that there was a problem in the connection selection
                self.close()
                raise exceptions.RequestClosed(
                    "invalid socket: %s" % colony.legacy.UNICODE(exception)
                )

            # in case there is pending data to be received
            if readable:
                try:
                    # receives the data from the socket
                    data = self.connection_socket.recv(CHUNK_SIZE)

                    # in case the data is invalid it means the connection has
                    # been dropped and a re-connection is required
                    if not data:
                        # in case there are no more reconnection retries available
                        # closes the connection and raises an exception
                        if reconnect_retries <= 0:
                            self.close()
                            raise exceptions.RequestClosed(
                                "max reconnection retries reached"
                            )

                        # prints a debug message and then runs the re-connection
                        # operation to try to send the data
                        self.client_plugin.debug(
                            "Received empty data, reconnecting socket"
                        )
                        self._reconnect_connection_socket()
                        reconnect_retries -= 1

                    # otherwise there are contents in it
                    else:
                        # prints a debug message and then returns the data back
                        # into the queue to be handled latter
                        self.client_plugin.debug("Received extra data, returning it")
                        self.return_data(data)
                except (
                    exceptions.RequestClosed,
                    exceptions.ClientUtilsException,
                ):
                    raise
                except Exception as exception:
                    # in case there are no more reconnection retries available
                    # closes the connection and raises an exception
                    if reconnect_retries <= 0:
                        self.close()
                        raise exceptions.RequestClosed(
                            "max reconnection retries reached: "
                            + colony.legacy.UNICODE(exception)
                        )

                    # prints a debug message and then reconnects the connection socket
                    self.client_plugin.debug(
                        "Problem while receiving pending data: "
                        + colony.legacy.UNICODE(exception)
                    )
                    self._reconnect_connection_socket()
                    reconnect_retries -= 1

            # in case there are no events the timeout has been reached
            # (reason for unblocking) and the connection must be closed
            elif not readable and not writeable:
                # closes the connection, and then raises the server
                # response timeout exception
                self.close()
                raise exceptions.ServerResponseTimeout("%is timeout" % response_timeout)

            # in case the socket is ready to have data
            # sent through it
            elif writeable:
                try:
                    # checks if the connection is of type persistent
                    # this check changes the way the data is sent
                    if self.connection_persistent:
                        # sends the data in chunks, the send command is used for
                        # a connection oriented connection
                        number_bytes_sent = self.connection_socket.send(message)

                    # otherwise the connection is not persistent (no connection)
                    # and a "datagram" oriented operation must be performed
                    else:
                        # sends the data in chunks, the send to command is used for
                        # a non connection oriented connection
                        number_bytes_sent = self.connection_socket.sendto(
                            message, self.connection_address
                        )
                except Exception as exception:
                    # tries to process the exception, meaning that the
                    # exception is going to be tested against a series
                    # of validation and in case it's considered valid
                    # it's ignored and the loop continues
                    if self._process_exception(exception):
                        continue

                    # in case the number of retries (available) is greater than
                    # zero must decrement the value and continue the loop as this
                    # considered a graceful error
                    if retries > 0:
                        retries -= 1
                        continue

                    # otherwise an exception should be raised indicating that there
                    # was an issue while sending data to the peer
                    else:
                        # closes the connection current connection effectively disabling
                        # any more access to the connection and socket
                        self.close()

                        # raises the client response timeout exception so that the top
                        # layers are properly notified about the issue
                        raise exceptions.ClientResponseTimeout(
                            "problem sending data: " + colony.legacy.UNICODE(exception)
                        )

                # decrements the number of bytes sent
                number_bytes -= number_bytes_sent

                # in case the number of bytes (pending)
                # is zero (the transfer is complete)
                if number_bytes == 0:
                    break
                else:
                    message = message[number_bytes * -1 :]

    def _reconnect_connection_socket(self):
        """
        Reconnects the current connection socket.
        """

        # closes the connection socket
        self.connection_socket.close()

        # resets the read buffer
        self._read_buffer = []

        # creates a socket for the client with
        # the given socket name and parameters
        self.connection_socket = self.client._get_socket(
            self.connection_socket_name, self.connection_socket_parameters
        )

        # updates the base connection socket reference to avoid
        # holding a stale reference to the old (closed) socket
        self._connection_socket = self.connection_socket

        # reconnects the socket to the connection address
        self.connection_socket.connect(self.connection_address)

        # sets the socket to non blocking mode, so that not network
        # relates operation is going to blow flow of control
        self.connection_socket.setblocking(0)

        # prints a debug message about reconnection
        self.client_plugin.debug("Reconnected to: %s" % str(self.connection_address))

    def _ensure_socket_fd(self):
        """
        Retrieves the file descriptor for the current connection socket,
        raising an exception in case the socket is invalid or closed.

        :rtype: int
        :return: The file descriptor for the current connection socket.
        """

        # retrieves the file descriptor for the current connection
        # socket, raises in case the socket is invalid or closed
        try:
            file_descriptor = self.connection_socket.fileno()
        except Exception:
            self.close()
            raise exceptions.RequestClosed(
                "invalid socket: unable to retrieve file descriptor"
            )

        return file_descriptor

    def _process_exception(self, exception):
        """
        Processes the exception taking into account the severity of it,
        as for some exception a graceful handling is imposed.

        :type exception: Exception
        :param exception: The exception that is going to be handled/processed.
        :rtype: bool
        :return: The result of the processing, in case it's false a normal
        exception handling should be performed otherwise a graceful one is used.
        """

        # in case the current connection socket contains the process
        # exception method and the exception is process successfully
        # returns valid as the exception is not critical
        if hasattr(
            self.connection_socket, "process_exception"
        ) and self.connection_socket.process_exception(exception):
            return True

        # tries to run the verification of the exception against the
        # "valid" socket errors in case it's one of such errors the
        # returned valid is true (should be ignored)
        if isinstance(exception, socket.error) and exception.args[0] in (
            errno.EWOULDBLOCK,
            errno.EAGAIN,
            errno.EPERM,
            errno.ENOENT,
            WSAEWOULDBLOCK,
        ):
            return True

        # by default returns an invalid value meaning that the exception
        # should be handled as an error and not ignored
        return False

    def _call_connection_opened_handlers(self):
        """
        Calls all the connection opened handlers.
        """

        # iterates over all the connection opened handlers
        # and calls each of them (notification)
        for connection_opened_handler in self.connection_opened_handlers:
            connection_opened_handler(self)

    def _call_connection_closed_handlers(self):
        """
        Calls all the connection closed handlers.
        """

        # iterates over all the connection closed handlers
        # to call each of them (tell about the notification)
        for connection_closed_handler in self.connection_closed_handlers:
            connection_closed_handler(self)
