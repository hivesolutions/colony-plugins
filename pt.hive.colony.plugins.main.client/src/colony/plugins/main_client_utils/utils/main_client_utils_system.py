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

import main_client_utils_exceptions

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 100
""" The request timeout """

CONNECTION_TIMEOUT = 600
""" The connection timeout """

CHUNK_SIZE = 1024
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

    client_handling_task_class = None
    """ The client handling task class """

    chunk_size = CHUNK_SIZE
    """ The chunk size """

    client_configuration = {}
    """ The client configuration """

    client_connection_timeout = CLIENT_CONNECTION_TIMEOUT
    """ The client connection timeout """

    connection_timeout = CONNECTION_TIMEOUT
    """ The connection timeout """

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

        pass

    def get_client_connection(self, connection_tuple):
        """
        Retrieves the client connection for the given
        connection tuple.

        @type connection_tuple: Tuple
        @param connection_tuple: The tuple containing
        the connection reference.
        @rtype: ClientConnection
        @return: The retrieved client connection.
        """

        ##if not connection_tuple in self.client_connections_map:
        ##    client_connection =

class ClientConnection:
    """
    The client connection class.
    Describes a client connection.
    """

    client_plugin = None
    """ The client plugin """

    client_connection_handler = None
    """ The client connection handler """

    connection_socket = None
    """ The connection socket """

    connection_address = None
    """ The connection address """

    connection_port = None
    """ The connection port """

    connection_chunk_size = None
    """ The connection chunk size """

    connection_opened_handlers = []
    """ The connection opened handlers """

    connection_closed_handlers = []
    """ The connection closed handlers """

    connection_properties = {}
    """ The connection properties map """

    cancel_time = None
    """ The cancel time """

    _connection_socket = None
    """ The original connection socket """

    def __init__(self, client_plugin, client_connection_handler, connection_socket, connection_address, connection_port, connection_chunk_size):
        """
        Constructor of the class.

        @type client_plugin: Plugin
        @param client_plugin: The client plugin.
        @type client_connection_handler: AbstractClientConnectionHandler
        @param client_connection_handler: The client connection handler.
        @type connection_socket: Socket
        @param connection_socket: The connection socket.
        @type connection_address: Tuple
        @param connection_address: The connection address.
        @type connection_port: int
        @param connection_port: The connection port.
        @type connection_chunk_size: int
        @param connection_chunk_size: The connection chunk size.
        """

        self.client_plugin = client_plugin
        self.client_connection_handler = client_connection_handler
        self.connection_socket = connection_socket
        self.connection_address = connection_address
        self.connection_port = connection_port
        self.connection_chunk_size = connection_chunk_size

        self._connection_socket = connection_socket

        self.connection_opened_handlers = []
        self.connection_closed_handlers = []
        self.connection_properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.connection_address, self.connection_port)

    def open(self):
        """
        Opens the connection.
        """

        # prints debug message about connection
        self.client_plugin.debug("Connected to: %s" % str(self.connection_address))

        # calls the connection opened handlers
        self._call_connection_opened_handlers()

    def close(self):
        """
        Closes the connection.
        """

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
        main_client_utils = self.client_connection_handler.client.main_client_utils

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

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = None):
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

        # retrieves the chunk size
        chunk_size = chunk_size and chunk_size or self.connection_chunk_size

        try:
            # sets the socket to non blocking mode
            self.connection_socket.setblocking(0)

            # runs the select in the connection socket, with timeout
            selected_values = select.select([self.connection_socket], [], [], request_timeout)

            # sets the socket to blocking mode
            self.connection_socket.setblocking(1)
        except:
            # raises the request closed exception
            raise main_client_utils_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
            # closes the connection socket
            self.connection_socket.close()

            # raises the server request timeout exception
            raise main_client_utils_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.connection_socket.recv(chunk_size)
        except:
            # raises the client request timeout exception
            raise main_client_utils_exceptions.ClientRequestTimeout("timeout")

        # returns the data
        return data

    def send(self, message):
        """
        Sends the given message to the socket.

        @type message: String
        @param message: The message to be sent.
        """

        return self.connection_socket.sendall(message)

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

class ClientConnectionless(ClientConnection):
    """
    The client connection for information
    flow based in connectionless mechanisms.
    """

    connection_data = None
    """ The connection data """

    def __init__(self, client_plugin, client_connection_handler, connection_socket, connection_address, connection_port, connection_data, connection_chunk_size):
        """
        Constructor of the class.

        @type client_plugin: Plugin
        @param client_plugin: The client plugin.
        @type client_connection_handler: AbstractClientConnectionHandler
        @param client_connection_handler: The client connection handler.
        @type connection_socket: Socket
        @param connection_socket: The connection socket.
        @type connection_address: Tuple
        @param connection_address: The connection address.
        @type connection_port: int
        @param connection_port: The connection port.
        @type connection_data: String
        @param connection_data: The connection data.
        @type connection_chunk_size: int
        @param connection_chunk_size: The connection chunk size.
        """

        ClientConnection.__init__(self, client_connection_handler, client_plugin, connection_socket, connection_address, connection_port, connection_chunk_size)

        self.connection_data = connection_data

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the data from the current connection socket.

        @type request_timeout: float
        @param request_timeout: The timeout to be used in data retrieval.
        @rtype: String
        @return: The retrieved data.
        """

        # returns the connection data
        return self.connection_data

    def send(self, message):
        """
        Sends the given message to the socket.

        @type message: String
        @param message: The message to be sent.
        """

        return self.connection_socket.sendto(message, self.connection_address)

    def get_connection_tuple(self):
        """
        Returns a tuple representing the connection.

        @rtype: Tuple
        @return: A tuple representing the connection.
        """

        return (self.connection_data, self.connection_socket, self.connection_address, self.connection_port)
