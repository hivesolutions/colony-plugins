#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import time
import select

import colony.libs.map_util
import colony.libs.string_buffer_util

import main_client_utils_exceptions

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

CONNECTION_TYPE_VALUE = "connection"
""" The connection type value """

CONNECTIONLESS_TYPE_VALUE = "connectionless"
""" The connectionless type value """

DEFAULT_TYPE = CONNECTION_TYPE_VALUE
""" The default type client """

class MainClientUtils:
    """
    The main client utils class.
    """

    main_client_utils_plugin = None
    """ The main client utils plugin """

    socket_provider_plugins_map = {}
    """ The socket provider plugins map """

    socket_upgrader_plugins_map = {}
    """ The socket upgrader plugins map """

    def __init__(self, main_client_utils_plugin):
        """
        Constructor of the class.

        @type main_client_utils_plugin: MainClientUtilsPlugin
        @param main_client_utils_plugin: The main client utils plugin.
        """

        self.main_client_utils_plugin = main_client_utils_plugin

        self.socket_provider_plugins_map = {}
        self.socket_upgrader_plugins_map = {}

    def generate_client(self, parameters):
        """
        Generates a new client for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for client generation.
        @rtype: AbstractClient
        @return: The generated client.
        """

        return AbstractClient(self, self.main_client_utils_plugin, parameters)

    def socket_provider_load(self, socket_provider_plugin):
        """
        Loads a socket provider plugin.

        @type socket_provider_plugin: Plugin
        @param socket_provider_plugin: The socket provider plugin
        to be loaded.
        """

        # retrieves the plugin provider name
        provider_name = socket_provider_plugin.get_provider_name()

        # sets the socket provider plugin in the socket provider plugins map
        self.socket_provider_plugins_map[provider_name] = socket_provider_plugin

    def socket_provider_unload(self, socket_provider_plugin):
        """
        Unloads a socket provider plugin.

        @type socket_provider_plugin: Plugin
        @param socket_provider_plugin: The socket provider plugin
        to be unloaded.
        """

        # retrieves the plugin provider name
        provider_name = socket_provider_plugin.get_provider_name()

        # removes the socket provider plugin from the socket provider plugins map
        del self.socket_provider_plugins_map[provider_name]

    def socket_upgrader_load(self, socket_upgrader_plugin):
        """
        Loads a socket upgrader plugin.

        @type socket_upgrader_plugin: Plugin
        @param socket_upgrader_plugin: The socket upgrader plugin
        to be loaded.
        """

        # retrieves the plugin upgrader name
        upgrader_name = socket_upgrader_plugin.get_upgrader_name()

        # sets the socket upgrader plugin in the socket upgrader plugins map
        self.socket_upgrader_plugins_map[upgrader_name] = socket_upgrader_plugin

    def socket_upgrader_unload(self, socket_upgrader_plugin):
        """
        Unloads a socket upgrader plugin.

        @type socket_upgrader_plugin: Plugin
        @param socket_upgrader_plugin: The socket upgrader plugin
        to be unloaded.
        """

        # retrieves the plugin upgrader name
        upgrader_name = socket_upgrader_plugin.get_upgrader_name()

        # removes the socket upgrader plugin from the socket upgrader plugins map
        del self.socket_upgrader_plugins_map[upgrader_name]

class AbstractClient:
    """
    The abstract client class.
    """

    main_client_utils = None
    """ The main client utils """

    main_client_utils_plugin = None
    """ The main client utils plugin """

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

    def __init__(self, main_client_utils, main_client_utils_plugin, parameters = {}):
        """
        Constructor of the class.

        @type main_client_utils: MainClientUtils
        @param main_client_utils: The main client utils.
        @type main_client_utils_plugin: MainClientUtilsPlugin
        @param main_client_utils_plugin: The main client utils plugin.
        @type parameters: Dictionary
        @param parameters: The parameters
        """

        self.main_client_utils = main_client_utils
        self.main_client_utils_plugin = main_client_utils_plugin

        self.client_type = parameters.get("type", DEFAULT_TYPE)
        self.client_plugin = parameters.get("client_plugin", None)
        self.chunk_size = parameters.get("chunk_size", CHUNK_SIZE)
        self.client_configuration = parameters.get("client_configuration", {})
        self.client_connection_timeout = parameters.get("client_connection_timeout", CLIENT_CONNECTION_TIMEOUT)
        self.connection_timeout = parameters.get("connection_timeout", CONNECTION_TIMEOUT)
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
        for _connection_tuple, client_connection in self.client_connections_map.items():
            # closes the client connection
            client_connection.close()

    def get_client_connection(self, connection_tuple, open_connection = True):
        """
        Retrieves the client connection for the given
        connection tuple.

        @type connection_tuple: Tuple
        @param connection_tuple: The tuple containing
        the connection reference.
        @type open_connection: bool
        @param open_connection: If the connection should be opened
        in case the connection is going to be created.
        @rtype: ClientConnection
        @return: The retrieved client connection.
        """

        # generates an hashable connection tuple from the original
        # connection tuple
        connection_tuple_hashable = self._generate_connection_tuple_hashable(connection_tuple)

        # tries to retrieve the current client connection
        client_connection = self.client_connections_map.get(connection_tuple_hashable, None)

        # in case the connection tuple is not present in the
        # client connections map or the current client connection
        # is not open
        if not client_connection or not client_connection.is_open():
            # creates the a new client connection for the given connection
            # tuple and with the open connection option
            client_connection = self._create_client_connection(connection_tuple, open_connection)

            # sets the client connection in the client connections map
            self.client_connections_map[connection_tuple_hashable] = client_connection

        # retrieves the client connection for the client
        # connections map
        client_connection = self.client_connections_map[connection_tuple_hashable]

        # returns the client connection
        return client_connection

    def _create_client_connection(self, connection_tuple, open_connection = True):
        """
        Creates the client connection for the given
        connection tuple.

        @type connection_tuple: Tuple
        @param connection_tuple: The tuple containing
        the connection reference.
        @type open_connection: bool
        @param open_connection: If the connection should be opened
        in case the connection is going to be created.
        @rtype: ClientConnection
        @return: The created client connection.
        """

        # retrieves the host, the port, the socket name and
        # the socket parameters from the connection tuple
        host, port, socket_name, socket_parameters = connection_tuple

        # creates the address tuple
        address = (host, port)

        # creates a socket for the client with
        # the given socket name
        client_connection_socket = self._get_socket(socket_name, socket_parameters)

        # retrieves the client connection
        client_connection = ClientConnection(self.client_plugin, self, client_connection_socket, address, socket_name, socket_parameters, self.request_timeout, self.response_timeout, self.chunk_size)

        # in case the connection should be opened
        if open_connection:
            # opens the client connection
            client_connection.open()

        # returns the client connection
        return client_connection

    def _get_socket(self, socket_name = "normal", socket_parameters = {}):
        """
        Retrieves the socket for the given socket name
        using the socket provider plugins.

        @type socket_name: String
        @param socket_name: The name of the socket to be retrieved.
        @type socket_parameters: Dictionary
        @param socket_parameters: The parameters of the socket to be retrieved.
        @rtype: Socket
        @return: The socket for the given socket name.
        """

        # retrieves the socket provider plugins map
        socket_provider_plugins_map = self.main_client_utils.socket_provider_plugins_map

        # in case the socket name is available in the socket
        # provider plugins map
        if socket_name in socket_provider_plugins_map:
            # retrieves the socket provider plugin from the socket provider plugins map
            socket_provider_plugin = socket_provider_plugins_map[socket_name]

            # the parameters for the socket provider
            parameters = {}

            # copies the socket parameters to the parameters map
            colony.libs.map_util.map_copy(socket_parameters, parameters)

            # creates a new socket with the socket provider plugin
            socket = socket_provider_plugin.provide_socket_parameters(parameters)

            # returns the created socket
            return socket
        else:
            # raises the socket provider not found exception
            raise main_client_utils_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_name)

    def _generate_connection_tuple_hashable(self, connection_tuple):
        """
        Generates an hashable connection tuple from
        the original connection tuple.

        @type connection_tuple: Tuple
        @param connection_tuple: The connection tuple to be converted
        to hashable.
        @rtype: Tuple
        @return: The hashable connection tuple.
        """

        # copies the connection tuple as the connection tuple hashable
        connection_tuple_hashable = list(connection_tuple)

        # sets the last element of the connection tuple hashable as the
        # items tuple instead of the dictionary in order to avoid unhashable problems
        connection_tuple_hashable[3] = tuple(connection_tuple_hashable[3].items())

        # converts the connection tuple hashable into a tuple
        # in order to hashable
        connection_tuple_hashable = tuple(connection_tuple_hashable)

        # returns the connection tuple hashable
        return connection_tuple_hashable

class ClientConnection:
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

    _returned_data_buffer = None
    """ The buffer of returned data """

    def __init__(self, client_plugin, client, connection_socket, connection_address, connection_socket_name, connection_socket_parameters, connection_request_timeout, connection_response_timeout, connection_chunk_size):
        """
        Constructor of the class.

        @type client_plugin: Plugin
        @param client_plugin: The client plugin.
        @type client: AbstractClient
        @param client: The client.
        @type connection_socket: Socket
        @param connection_socket: The connection socket.
        @type connection_address: Tuple
        @param connection_address: The connection address.
        @type connection_socket_name: String
        @param connection_socket_name: The connection socket name.
        @type connection_socket_parameters: String
        @param connection_socket_parameters: The connection socket parameters.
        @type connection_request_timeout: float
        @param connection_request_timeout: The connection request timeout.
        @type connection_response_timeout: float
        @param connection_response_timeout: The connection response timeout.
        @type connection_chunk_size: int
        @param connection_chunk_size: The connection chunk size.
        """

        self.client_plugin = client_plugin
        self.client = client
        self.connection_socket = connection_socket
        self.connection_address = connection_address
        self.connection_socket_name = connection_socket_name
        self.connection_socket_parameters = connection_socket_parameters
        self.connection_request_timeout = connection_request_timeout
        self.connection_response_timeout = connection_response_timeout
        self.connection_chunk_size = connection_chunk_size

        self._connection_socket = connection_socket

        self.connection_opened_handlers = []
        self.connection_closed_handlers = []
        self.connection_properties = {}

        self._returned_data_buffer = colony.libs.string_buffer_util.StringBuffer(False)

    def __repr__(self):
        return "(%s, %s)" % (self.connection_address, self.connection_socket_name)

    def open(self):
        """
        Opens the connection.
        """

        # connects the connection socket to the connection address
        self.connection_socket.connect(self.connection_address)

        # sets the socket to non blocking mode
        self.connection_socket.setblocking(0)

        # prints debug message about connection
        self.client_plugin.debug("Connected to: %s" % str(self.connection_address))

        # calls the connection opened handlers
        self._call_connection_opened_handlers()

        # sets the connection status flag
        self.connection_status = True

    def close(self):
        """
        Closes the connection.
        """

        # unsets the connection status flag
        self.connection_status = False

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

        @type delta_time: float
        @param delta_time: The amount of seconds until canceling.
        """

        # sets the cancel time
        self.cancel_time = time.clock() + delta_time

    def upgrade(self, socket_upgrader, parameters):
        """
        Upgrades the current connection socket, using
        the the upgrader with the given name and the given parameters.

        @type socket_upgrader: String
        @param socket_upgrader: The name of the socket upgrader.
        @type parameters: Dictionary
        @param parameters: The parameters to the upgrade process.
        """

        # retrieves the main client utils
        main_client_utils = self.client.main_client_utils

        # retrieves the socket upgrader plugins map
        socket_upgrader_plugins_map = main_client_utils.socket_upgrader_plugins_map

        # in case the upgrader handler is not found in the handler plugins map
        if not socket_upgrader in socket_upgrader_plugins_map:
            # raises the socket upgrader not found exception
            raise main_client_utils_exceptions.SocketUpgraderNotFound("socket upgrader %s not found" % self.socket_upgrader)

        # retrieves the socket upgrader plugin
        socket_upgrader_plugin = main_client_utils.socket_upgrader_plugins_map[socket_upgrader]

        # upgrades the current connection socket using the socket upgrader plugin
        self.connection_socket = socket_upgrader_plugin.upgrade_socket_parameters(self.connection_socket, parameters)

        # sets the socket to non blocking mode
        self.connection_socket.setblocking(0)

    def retrieve_data(self, request_timeout = None, chunk_size = None):
        """
        Retrieves the data from the current connection socket, with the
        given timeout and with a maximum size given by the chunk size.

        @type request_timeout: float
        @param request_timeout: The timeout to be used in data retrieval.
        @type chunk_size: int
        @param chunk_size: The maximum size of the chunk to be retrieved.
        @rtype: String
        @return: The retrieved data.
        """

        # retrieves the request timeout
        request_timeout = request_timeout and request_timeout or self.connection_request_timeout

        # retrieves the chunk size
        chunk_size = chunk_size and chunk_size or self.connection_chunk_size

        # in case the returned data buffer is not empty
        if not self._returned_data_buffer.is_empty():
            # returns the data buffer value
            data_buffer_value = self._returned_data_buffer.read(chunk_size)

            # in case the returned data buffer has reached the
            # end of file
            if self._returned_data_buffer.eof():
                # resets the returned data buffer
                self._returned_data_buffer.reset()

            # returns the data buffer value
            return data_buffer_value

        try:
            # runs the select in the connection socket, with timeout
            selected_values = select.select([self.connection_socket], [], [], request_timeout)
        except:
            # closes the connection
            self.close()

            # raises the request closed exception
            raise main_client_utils_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
            # closes the connection
            self.close()

            # raises the server request timeout exception
            raise main_client_utils_exceptions.ClientRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.connection_socket.recv(chunk_size)
        except Exception, exception:
            # closes the connection
            self.close()

            # raises the server request timeout exception
            raise main_client_utils_exceptions.ServerRequestTimeout("problem receiving data: " + unicode(exception))

        # returns the data
        return data

    def return_data(self, data):
        """
        Returns the given data to the connection
        internal buffer.

        @type data: String
        @param data: The data to be returned to the
        connection internal buffer.
        """

        # retrieves the data length
        data_length = len(data)

        # adds the data to the returned data buffer
        self._returned_data_buffer.write(data)

        # returns the buffer to the previous position
        self._returned_data_buffer.seek(data_length * -1, os.SEEK_CUR)

    def send(self, message, response_timeout = None):
        """
        Sends the given message to the socket.

        @type response_timeout: float
        @param response_timeout: The timeout to be used in data sending.
        @type message: String
        @param message: The message to be sent.
        """

        # retrieves the response timeout
        response_timeout = response_timeout and response_timeout or self.connection_response_timeout

        # retrieves the number of bytes in the message
        number_bytes = len(message)

        # iterates continuously
        while True:
            try:
                # runs the select in the connection socket, with timeout
                selected_values = select.select([self.connection_socket], [self.connection_socket], [self.connection_socket], 1)
            except:
                # closes the connection
                self.close()

                # raises the request closed exception
                raise main_client_utils_exceptions.RequestClosed("invalid socket")

            if not selected_values[0] == []:
                try:
                    # receives the data from the socket
                    data = self.connection_socket.recv(CHUNK_SIZE)

                    # in case the data is empty
                    if not len(data):
                        # reconnects the connection socket
                        self._reconnect_connection_socket()
                    else:
                        # returns the data back into the queue
                        self.return_data(data)
                except:
                    # reconnects the connection socket
                    self._reconnect_connection_socket()
            elif selected_values == ([], [], []):
                # closes the connection
                self.close()

                # raises the server response timeout exception
                raise main_client_utils_exceptions.ServerResponseTimeout("%is timeout" % response_timeout)
            else:
                try:
                    # sends the data in chunks
                    number_bytes_sent = self.connection_socket.send(message)
                except Exception, exception:
                    # closes the connection
                    self.close()

                    # raises the client response timeout exception
                    raise main_client_utils_exceptions.ClientResponseTimeout("problem sending data: " + unicode(exception))

                # decrements the number of bytes sent
                number_bytes -= number_bytes_sent

                # in case the number of bytes (pending)
                # is zero (the transfer is complete)
                if number_bytes == 0:
                    # breaks the cycle
                    break
                else:
                    # creates the new message
                    message = message[number_bytes * -1:]

    def is_open(self):
        """
        Retrieves if the current connection is open.

        @rtype: bool
        @return: If the current connection is open.
        """

        return self.connection_status

    def get_connection_property(self, property_name):
        """
        Retrieves the connection property for the given name.

        @type property_name: String
        @param property_name: The name of the property to
        be retrieved.
        @rtype: Object
        @return: The value of the retrieved property.
        """

        return self.connection_properties.get(property_name, None)

    def set_connection_property(self, property_name, property_value):
        """
        Sets a connection property, associating the given name
        with the given value.

        @type property_name: String
        @param property_name: The name of the property to set.
        @type property_value: Object
        @param property_value: The value of the property to set.
        """

        self.connection_properties[property_name] = property_value

    def unset_connection_property(self, property_name):
        """
        Unsets a connection property, removing it from the internal
        structures.

        @type property_name: String
        @param property_name: The name of the property to unset.
        """

        del self.connection_properties[property_name]

    def get_connection_tuple(self):
        """
        Returns a tuple representing the connection.

        @rtype: Tuple
        @return: A tuple representing the connection.
        """

        return (self._connection_socket, self.connection_address, self.connection_port)

    def get_connection_socket(self):
        """
        Retrieves the connection socket.

        @rtype: Socket
        @return: The connection socket.
        """

        return self.connection_socket

    def get_connection_address(self):
        """
        Retrieves the connection address.

        @rtype: Tuple
        @return: The connection address.
        """

        return self.connection_address

    def get_base_connection_socket(self):
        """
        Retrieves the base connection socket.

        @rtype: Socket
        @return: The base connection socket.
        """

        return self._connection_socket

    def _reconnect_connection_socket(self):
        """
        Reconnects the current connection socket.
        """

        # closes the connection socket
        self.connection_socket.close()

        # creates a socket for the client with
        # the given socket name and parameters
        self.connection_socket = self.client._get_socket(self.connection_socket_name, self.connection_socket_parameters)

        # sets the socket to blocking mode
        self.connection_socket.setblocking(1)

        # reconnects the socket to the connection address
        self.connection_socket.connect(self.connection_address)

        # sets the socket to non blocking mode
        self.connection_socket.setblocking(0)

        # prints debug message about reconnection
        self.client_plugin.debug("Reconnected to: %s" % str(self.connection_address))

    def _call_connection_opened_handlers(self):
        """
        Calls all the connection opened handlers.
        """

        # iterates over all the connection opened handler
        for connection_opened_handler in self.connection_opened_handlers:
            # calls the connection opened handler
            connection_opened_handler(self)

    def _call_connection_closed_handlers(self):
        """
        Calls all the connection closed handlers.
        """

        # iterates over all the connection closed handler
        for connection_closed_handler in self.connection_closed_handlers:
            # calls the connection closed handler
            connection_closed_handler(self)
