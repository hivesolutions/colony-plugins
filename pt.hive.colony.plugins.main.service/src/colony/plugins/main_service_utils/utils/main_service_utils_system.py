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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import time
import socket
import select
import threading

import main_service_utils_exceptions

BIND_HOST = ""
""" The bind host """

PORT = 0
""" The bind host """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

POOL_NAME = "default pool"
""" The name of the pool """

POOL_DESCRIPTION = "pool to support service client connections"
""" The description of the pool """

NUMBER_THREADS = 15
""" The number of threads """

MAXIMUM_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

MAXIMUM_NUMBER_WORKS_THREAD = 10
""" The maximum number of works per thread """

WORK_SCHEDULING_ALGORITHM = 1
""" The work scheduling algorithm """

POLL_TIMEOUT = 1
""" The poll timeout """

REQUEST_TIMEOUT = 100
""" The request timeout """

RESPONSE_TIMEOUT = 10
""" The response timeout """

CONNECTION_TIMEOUT = 600
""" The connection timeout """

CHUNK_SIZE = 1024
""" The chunk size """

SERVER_SIDE_VALUE = "server_side"
""" The server side value """

DO_HANDSHAKE_ON_CONNECT_VALUE = "do_handshake_on_connect"
""" The do handshake on connect value """

PORT_RANGES = ((38001, 39999), (40001, 42999))
""" The ranges of port available for services """

LOCAL_HOST = "127.0.0.1"
""" The local host value """

DUMMY_MESSAGE_VALUE = "_"
""" the dummy message value """

EPOLL_VALUE = "epoll"
""" The poll value """

CONNECTION_TYPE_VALUE = "connection"
""" The connection type value """

CONNECTIONLESS_TYPE_VALUE = "connectionless"
""" The connectionless type value """

DEFAULT_TYPE = CONNECTION_TYPE_VALUE
""" The default type service """

# in case the current system supports epoll
if hasattr(select, "epoll"):
    EPOLL_SUPPORT = True
else:
    EPOLL_SUPPORT = False

if EPOLL_SUPPORT:
    NEW_VALUE_MASK = select.EPOLLIN | select.EPOLLPRI | select.EPOLLHUP #@UndefinedVariable
    """ The new value received mask value """

    REGISTER_MASK = NEW_VALUE_MASK | select.EPOLLET #@UndefinedVariable
    """ The register mask value """

class MainServiceUtils:
    """
    The main service utils class.
    """

    main_service_utils_plugin = None
    """ The main service utils plugin """

    socket_provider_plugins_map = {}
    """ The socket provider plugins map """

    socket_upgrader_plugins_map = {}
    """ The socket upgrader plugins map """

    port_generation_lock = None
    """ The lock to protect port generation """

    current_port_range_index = 0
    """ The current port range index being used """

    current_port = None
    """ The current port """

    def __init__(self, main_service_utils_plugin):
        """
        Constructor of the class.

        @type main_service_utils_plugin: MainServiceUtilsPlugin
        @param main_service_utils_plugin: The main service utils plugin.
        """

        self.main_service_utils_plugin = main_service_utils_plugin

        self.socket_provider_plugins_map = {}
        self.socket_upgrader_plugins_map = {}
        self.port_generation_lock = threading.Lock()

        # resets the port value
        self._reset_port()

    def generate_service(self, parameters):
        """
        Generates a new service for the given parameters.
        The generated service includes the creation of a new pool.

        @type parameters: Dictionary
        @param parameters: The parameters for service generation.
        @rtype: AbstractService
        @return: The generated service.
        """

        return AbstractService(self, self.main_service_utils_plugin, parameters)

    def generate_service_port(self, parameters):
        """
        Generates a new service port for the current
        host, avoiding collisions.

        @type parameters: Dictionary
        @param parameters: The parameters for service port generation.
        @rtype: int
        @return: The newly generated port.
        """

        # acquires the port generation lock
        self.port_generation_lock.acquire()

        # increments the current port number
        self.current_port += 1

        # retrieves the initial and final port of the current
        # port range
        _initial_port, final_port = PORT_RANGES[self.current_port_range_index]

        # in case the current port is bigger than the final port
        if self.current_port > final_port:
            # increments the current port range index
            self.current_port_range_index += 1

            # in case the limit of port ranges has been reached
            if self.current_port_range_index == len(PORT_RANGES):
                # raises the port starvation reached exception
                raise main_service_utils_exceptions.PortStarvationReached("no more ports available")
            else:
                # resets the current port value
                self._reset_port()

                # increments the current port value
                self.current_port += 1

        # releases the port generation lock
        self.port_generation_lock.release()

        # returns the current port
        return self.current_port

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

    def _reset_port(self):
        """
        Resets the current port value to the initial
        value of the current port range.
        """

        # retrieves the initial and final port of the current
        # port range
        initial_port, _final_port = PORT_RANGES[self.current_port_range_index]

        # sets the current port as the initial port of
        # the port range (minus one)
        self.current_port = initial_port - 1

class AbstractService:
    """
    The abstract service class.
    """

    main_service_utils = None
    """ The main service utils """

    main_service_utils_plugin = None
    """ The main service utils plugin """

    service_socket = None
    """ The service socket """

    service_connection_active = False
    """ The service connection active flag """

    service_client_pool = None
    """ The service client pool """

    service_connection_close_event = None
    """ The service connection close event """

    service_connection_close_end_event = None
    """ The service connection close end event """

    service_type = None
    """ The service type """

    service_plugin = None
    """ The service plugin """

    service_handling_task_class = None
    """ The service handling task class """

    socket_provider = None
    """ The socket provider """

    bind_host = BIND_HOST
    """ The bind host value """

    port = PORT
    """ The service port """

    chunk_size = CHUNK_SIZE
    """ The chunk size """

    service_configuration = {}
    """ The service configuration """

    extra_parameters = {}
    """ The extra parameters """

    pool_configuration = {}
    """ The pool configuration """

    client_connection_timeout = CLIENT_CONNECTION_TIMEOUT
    """ The client connection timeout """

    connection_timeout = CONNECTION_TIMEOUT
    """ The connection timeout """

    def __init__(self, main_service_utils, main_service_utils_plugin, parameters = {}):
        """
        Constructor of the class.

        @type main_service_utils: MainServiceUtils
        @param main_service_utils: The main service utils.
        @type main_service_utils_plugin: MainServiceUtilsPlugin
        @param main_service_utils_plugin: The main service utils plugin.
        @type parameters: Dictionary
        @param parameters: The parameters
        """

        self.main_service_utils = main_service_utils
        self.main_service_utils_plugin = main_service_utils_plugin

        self.service_type = parameters.get("type", DEFAULT_TYPE)
        self.service_plugin = parameters.get("service_plugin", None)
        self.service_handling_task_class = parameters.get("service_handling_task_class", None)
        self.socket_provider = parameters.get("socket_provider", None)
        self.bind_host = parameters.get("bind_host", BIND_HOST)
        self.port = parameters.get("port", PORT)
        self.chunk_size = parameters.get("chunk_size", CHUNK_SIZE)
        self.service_configuration = parameters.get("service_configuration", {})
        self.extra_parameters = parameters.get("extra_parameters", {})
        self.pool_configuration = parameters.get("pool_configuration", {})
        self.client_connection_timeout = parameters.get("client_connection_timeout", CLIENT_CONNECTION_TIMEOUT)
        self.connection_timeout = parameters.get("connection_timeout", CONNECTION_TIMEOUT)

        self.service_connection_close_event = threading.Event()
        self.service_connection_close_end_event = threading.Event()

    def start_service(self):
        """
        Starts the service.
        """

        try:
            # creates the work pool
            self._create_pool()

            # creates and sets the service socket
            self._create_service_socket()

            # activates and listens the service socket
            self._activate_service_socket()

            # in case the service type is connection
            if self.service_type == CONNECTION_TYPE_VALUE:
                # runs the loop for connection type
                self._loop_connection()
            # in case the service type is connectionless
            elif self.service_type == CONNECTIONLESS_TYPE_VALUE:
                # runs the loop for connectionless type
                self._loop_connectionless()
        except:
            # sets the service connection active flag as false
            self.service_connection_active = False
        finally:
            # disables the service socket
            self._disable_service_socket()

            # clears the service connection close event
            self.service_connection_close_event.clear()

            # sets the service connection close end event
            self.service_connection_close_end_event.set()

    def stop_service(self):
        """
        Stops the service.
        """

        # sets the service connection active flag as false
        self.service_connection_active = False

        # sets the service connection close event
        self.service_connection_close_event.set()

        # waits for the service connection close end event
        self.service_connection_close_end_event.wait()

        # clears the service connection close end event
        self.service_connection_close_end_event.clear()

        # stops all the pool tasks
        self.service_client_pool.stop_pool_tasks()

        # stops the pool
        self.service_client_pool.stop_pool()

    def _create_pool(self):
        """
        Creates the work pool according to the
        service configuration.
        """

        # retrieves the work pool manager plugin
        work_pool_manager_plugin = self.main_service_utils_plugin.work_pool_manager_plugin

        # retrieves the work pool configuration parameters
        pool_name = self.pool_configuration.get("name", POOL_NAME)
        pool_description = self.pool_configuration.get("description", POOL_DESCRIPTION)
        number_threads = self.pool_configuration.get("number_threads", NUMBER_THREADS)
        scheduling_algorithm = self.pool_configuration.get("scheduling_algorithm", SCHEDULING_ALGORITHM)
        maximum_number_threads = self.pool_configuration.get("maximum_number_threads", MAXIMUM_NUMBER_THREADS)
        maximum_number_works_thread = self.pool_configuration.get("maximum_number_works_thread", MAXIMUM_NUMBER_WORKS_THREAD)
        work_scheduling_algorithm = self.pool_configuration.get("work_scheduling_algorithm", WORK_SCHEDULING_ALGORITHM)

        # retrieves the current service handler class
        service_handler_class = self._get_service_handler_class()

        # creates the service connection handler arguments
        service_connection_handler_arguments = (self, self.service_plugin, self.service_configuration, self.connection_timeout, self.chunk_size, self.service_handling_task_class, self.extra_parameters)

        # creates the service client pool
        self.service_client_pool = work_pool_manager_plugin.create_new_work_pool(pool_name, pool_description, service_handler_class, service_connection_handler_arguments, number_threads, scheduling_algorithm, maximum_number_threads, maximum_number_works_thread, work_scheduling_algorithm)

        # start the service client pool
        self.service_client_pool.start_pool()

        # sets the service connection active flag as true
        self.service_connection_active = True

    def _create_service_socket(self):
        """
        Creates the service socket according to the
        service configuration.
        """

        # in case the socket provider is defined
        if self.socket_provider:
            # retrieves the socket provider plugins map
            socket_provider_plugins_map = self.main_service_utils.socket_provider_plugins_map

            # in case the socket provider is available in the socket
            # provider plugins map
            if self.socket_provider in socket_provider_plugins_map:
                # retrieves the socket provider plugin from the socket provider plugins map
                socket_provider_plugin = socket_provider_plugins_map[self.socket_provider]

                # the parameters for the socket provider
                parameters = {SERVER_SIDE_VALUE : True, DO_HANDSHAKE_ON_CONNECT_VALUE : False}

                # creates a new service socket with the socket provider plugin
                self.service_socket = socket_provider_plugin.provide_socket_parameters(parameters)

                # sets the service socket to non blocking
                self.service_socket.setblocking(0)

                # returns immediately
                return
            else:
                # raises the socket provider not found exception
                raise main_service_utils_exceptions.SocketProviderNotFound("socket provider %s not found" % self.socket_provider)
        else:
            # creates the service socket
            self.service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _loop_connection(self):
        # loops while the service connection is active
        while not self.service_connection_close_event.isSet():
            # polls the service socket to check if there
            # is a new connection available
            poll_return_value = self._poll_service_socket()

            # in case the poll return value is not valid or
            # the connection is closed
            if not poll_return_value or self.service_connection_close_event.isSet():
                # breaks the cycle
                break

            # accepts the new client connection
            self._accept_service_socket()

    def _loop_connectionless(self):
        # loops while the service connection is active
        while not self.service_connection_close_event.isSet():
            # polls the service socket to check if there
            # is a new connection available
            poll_return_value = self._poll_service_socket()

            # in case the poll return value is not valid or
            # the connection is closed
            if not poll_return_value or self.service_connection_close_event.isSet():
                # breaks the cycle
                break

            # reads from the service socket and creates
            # the client connection
            self._read_service_socket()

    def _poll_service_socket(self):
        """
        Polls the service socket for changes
        and returns the resulting value (if successful).

        @rtype: bool
        @return: If the pool was successful.
        """

        try:
            # starts the select values
            selected_values = ([], [], [])

            # iterates while there is no selected values
            while selected_values == ([], [], []):
                # in case the connection is closed
                if self.service_connection_close_event.isSet():
                    return False

                # selects the values
                selected_values = select.select([self.service_socket], [], [], self.client_connection_timeout)

            return True
        except BaseException, exception:
            # prints info message about connection
            self.main_service_utils_plugin.info("The socket is not valid for selection of the pool: " + unicode(exception))

            return False

    def _accept_service_socket(self):
        """
        Accepts the client connection in
        the service socket.
        """

        try:
            # accepts the connection retrieving the service connection object and the address
            service_connection, service_address = self.service_socket.accept()

            # sets the service connection to non blocking mode
            service_connection.setblocking(0)

            # inserts the connection and address into the pool
            self._insert_connection_pool(service_connection, service_address)
        except Exception, exception:
            # prints an error message about the problem accepting the socket
            self.main_service_utils_plugin.error("Error accepting socket: " + unicode(exception))

    def _read_service_socket(self):
        """
        Reads data from the client connection
        in the service socket.
        """

        try:
            # reads some data from the service socket
            service_data, service_address = self.service_socket.recvfrom(self.chunk_size)

            # inserts the data and address into the pool
            self._insert_data_pool(service_data, service_address)
        except Exception, exception:
            # prints an error message about the problem reading from socket
            self.main_service_utils_plugin.error("Error reading from socket: " + unicode(exception))

    def _activate_service_socket(self):
        """
        Activates the service socket.
        """

        # sets the socket to be able to reuse the socket
        self.service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the service socket
        self.service_socket.bind((self.bind_host, self.port))

        # in case the service type is connection
        if self.service_type == CONNECTION_TYPE_VALUE:
            # start listening in the service socket
            self.service_socket.listen(5)

    def _disable_service_socket(self):
        """
        Disables the service socket.
        """

        # closes the service socket
        self.service_socket.close()

    def _insert_connection_pool(self, service_connection, service_address):
        """
        Inserts the given service connection into the connection pool.
        This process takes into account the pool usage and the current
        available task.

        @type service_connection: Socket
        @param service_connection: The service connection to be inserted.
        @type service_address: Tuple
        @param service_address: A tuple containing the address information
        of the connection.
        """

        # creates the work reference tuple
        work_reference = (service_connection, service_address, self.port)

        # inserts the work into the service client pool
        self.service_client_pool.insert_work(work_reference)

    def _insert_data_pool(self, service_data, service_address):
        """
        Inserts the given data in to the connection pool.
        This process takes into account the pool usage and the current
        available task.

        @type service_data: String
        @param service_data: The data to be inserted.
        @type service_address: Tuple
        @param service_address: A tuple containing the address information
        of the connection.
        """

        # creates the work reference tuple
        work_reference = (service_data, self.service_socket, service_address, self.port)

        # inserts the work into the service client pool
        self.service_client_pool.insert_work(work_reference)

    def _get_service_handler_class(self):
        """
        Retrieves the service handler class for
        the current configuration.

        @rtype: Class
        @return: The service handler class for
        the current configuration.
        """

        # in case the current service type is connection
        if self.service_type == CONNECTION_TYPE_VALUE:
            service_handler_class = AbstractServiceConnectionHandler
        # in case the current service type is connectionless
        elif self.service_type == CONNECTIONLESS_TYPE_VALUE:
            service_handler_class = AbstractServiceConnectionlessHandler

        # returns the service handler class
        return service_handler_class

class AbstractServiceConnectionHandler:
    """
    The abstract service connection handler.
    """

    service = None
    """ The service reference """

    service_plugin = None
    """ The service plugin """

    service_configuration = None
    """ The service configuration """

    service_connections_list = []
    """ The list of service connections """

    service_connection_sockets_list = []
    """ The list of service connection sockets """

    service_connections_map = {}
    """ The map of service connections """

    connection_socket_file_descriptor_connection_socket_map = {}
    """ The map associating the connection socket file descriptor with the connection socket """

    connection_socket_connection_socket_file_descriptor_map = {}
    """ The map associating the connection socket with the connection socket file descriptor """

    connection_timeout = CONNECTION_TIMEOUT
    """ The connection timeout """

    chunk_size = CHUNK_SIZE
    """ The chunk size """

    client_service = None
    """ The client service reference """

    wake_file = None
    """ The wake file reference """

    wake_file_port = None
    """ The wake file port """

    def __init__(self, service, service_plugin, service_configuration, connection_timeout, chunk_size, client_service_class, extra_parameters):
        """
        Constructor of the class.

        @type service: AbstractService
        @param service: The service reference.
        @type service_plugin: Plugin
        @param service_plugin: The service plugin.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration.
        @type connection_timeout: float
        @param connection_timeout: The connection timeout.
        @type chunk_size: int
        @param chunk_size: The chunk size.
        @type client_service_class: Class
        @param client_service_class: The client service class.
        @type extra_parameters: Dictionary
        @param extra_parameters: The extra parameters.
        """

        self.service = service
        self.service_plugin = service_plugin
        self.service_configuration = service_configuration
        self.connection_timeout = connection_timeout
        self.chunk_size = chunk_size

        self.service_connections_list = []
        self.service_connection_sockets_list = []
        self.service_connections_map = {}
        self.connection_socket_file_descriptor_connection_socket_map = {}
        self.connection_socket_connection_socket_file_descriptor_map = {}

        # creates the client service object
        self.client_service = client_service_class(self.service_plugin, self, service_configuration, main_service_utils_exceptions.MainServiceUtilsException, extra_parameters)

    def start(self):
        self.__start_base()
        if EPOLL_SUPPORT:
            self.__start_epoll()

    def stop(self):
        if EPOLL_SUPPORT:
            self.__stop_epoll()
        self.__stop_base()

    def __start_base(self):
        # generates a new wake "file" port
        self.wake_file_port = self.service.main_service_utils.generate_service_port({})

        # creates the wake "file" object
        self.wake_file = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # sets the socket to be able to reuse the socket
        self.wake_file.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds to the current host
        self.wake_file.bind((LOCAL_HOST, self.wake_file_port))

        # retrieves the wake file descriptor
        wake_file_descriptor = self.wake_file.fileno()

        # adds the wake "file" to the service connection sockets list
        self.service_connection_sockets_list.append(self.wake_file)

        # sets the wake file in the connection socket file descriptor connection socket map
        self.connection_socket_file_descriptor_connection_socket_map[wake_file_descriptor] = self.wake_file

    def __start_epoll(self):
        # retrieves the wake file descriptor
        wake_file_descriptor = self.wake_file.fileno()

        # creates a new epoll object
        self.epoll = select.epoll() #@UndefinedVariable

        # register the wake file in the epoll
        self.epoll.register(wake_file_descriptor, REGISTER_MASK)

    def __stop_base(self):
        # retrieves the wake file descriptor
        wake_file_descriptor = self.wake_file.fileno()

        # closes the wake "file"
        self.wake_file.close()

        # removes the wake file from the service connection sockets list
        self.service_connection_sockets_list.remove(self.wake_file)

        # removes the wake file from the connection socket file descriptor connection socket map
        self.connection_socket_file_descriptor_connection_socket_map[wake_file_descriptor]

    def __stop_epoll(self):
        # retrieves the wake file descriptor
        wake_file_descriptor = self.wake_file.fileno()

        # unregister the wake file from the epoll
        self.epoll.unregister(wake_file_descriptor)

        # stops the epoll object
        self.epoll.close()

    def process(self):
        """
        Processes a work "tick".
        The work tick consists in the polling of the connections
        and the processing of the work.
        """

        # polls the connections for canceling (in timeout)
        self.poll_cancel_connections()

        # polls the system to check for new connections
        ready_sockets = self.poll_connections(POLL_TIMEOUT)

        # iterates over all the ready sockets
        for ready_socket in ready_sockets:
            # retrieves the service connection
            # that is ready for reading
            ready_service_connection = self.service_connections_map[ready_socket]

            # handles the current request if it returns true
            # the connection is meant to remain open
            if self.client_service.handle_request(ready_service_connection):
                # sets the new cancel timeout
                ready_service_connection.cancel(self.connection_timeout)
            # otherwise the connection is meant to be closed
            else:
                # retrieves the connection tuple
                connection_tuple = ready_service_connection.get_connection_tuple()

                # removes the ready service connection (via remove work)
                self.remove_work(connection_tuple)

    def wake(self):
        """
        Wakes the current task releasing the current
        process call.
        """

        self.__wake_base()

    def work_added(self, work_reference):
        """
        Called when a work is added.

        @type work_reference: Object
        @param work_reference: The reference to the work to be added.
        """

        # unpacks the work reference retrieving the connection socket,
        # address and port
        connection_socket, connection_address, connection_port = work_reference

        try:
            # adds the connection to the current service connection handler
            self.add_connection(connection_socket, connection_address, connection_port)
        except Exception, exception:
            # prints an error for not being able to add connection
            self.service.main_service_utils_plugin.error("Problem while adding connection to service connection handler: %s" % unicode(exception))

    def work_removed(self, work_reference):
        """
        Called when a work is removed.

        @type work_reference: Object
        @param work_reference: The reference to the work to be removed.
        """

        # unpacks the work reference retrieving the connection socket,
        # address and port
        connection_socket, _connection_address, _connection_port = work_reference

        try:
            # removes the connection using the socket as reference
            self.remove_connection_socket(connection_socket)
        except Exception, exception:
            # prints an error for not being able to remove connection
            self.service.main_service_utils_plugin.error("Problem while removing connection from service connection handler: %s" % unicode(exception))

    def add_connection(self, connection_socket, connection_address, connection_port):
        """
        Adds a new connection to the service connection handler.

        @type connection_socket: Socket
        @param connection_socket: The connection socket.
        @type connection_address: Tuple
        @param connection_address: The connection address.
        @type connection_port: int
        @param connection_port: The connection port.
        @rtype: ServiceConnection
        @return: The created service connection.
        """

        # creates the new service connection
        service_connection = ServiceConnection(self.service_plugin, self, connection_socket, connection_address, connection_port, self.chunk_size)

        # opens the service connection
        service_connection.open()

        # retrieves the connection socket file descriptor
        connection_socket_file_descriptor = connection_socket.fileno()

        # adds the service connection to the service connections list
        self.service_connections_list.append(service_connection)

        # adds the connection socket to the service connection socket list
        self.service_connection_sockets_list.append(connection_socket)

        # sets the service connection in the service connections map
        self.service_connections_map[connection_socket] = service_connection

        # sets the connection socket in the connection socket file descriptor
        # connection socket map
        self.connection_socket_file_descriptor_connection_socket_map[connection_socket_file_descriptor] = connection_socket

        # sets the connection socket file descriptor in the connection socket connection
        # socket file descriptor map
        self.connection_socket_connection_socket_file_descriptor_map[connection_socket] = connection_socket_file_descriptor

        if EPOLL_SUPPORT:
            self.__add_connection_epoll(connection_socket, connection_address, connection_port)

        # sets the initial cancel timeout
        service_connection.cancel(self.connection_timeout)

        # handles the opened service connection
        self.client_service.handle_opened(service_connection)

        # returns the created service connection
        return service_connection

    def remove_connection(self, service_connection):
        """
        Removes the given service connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be removed.
        """

        # retrieves the connection socket
        connection_socket = service_connection.get_base_connection_socket()

        # retrieves the connection socket file descriptor
        connection_socket_file_descriptor = self.__get_connection_socket_file_descriptor(connection_socket)

        # handles the closed service connection
        self.client_service.handle_closed(service_connection)

        if EPOLL_SUPPORT:
            self.__remove_connection_epoll(service_connection)

        # closes the service connection
        service_connection.close()

        # removes the connection from the service connections list
        self.service_connections_list.remove(service_connection)

        # removes the connection socket from the service connection sockets list
        self.service_connection_sockets_list.remove(connection_socket)

        # removes the service connection from the service connections map
        del self.service_connections_map[connection_socket]

        # removes the connection socket from the connection socket file descriptor
        # connection socket map
        del self.connection_socket_file_descriptor_connection_socket_map[connection_socket_file_descriptor]

        # removes the connection socket file descriptor from the connection socket connection
        # socket file descriptor map
        del self.connection_socket_connection_socket_file_descriptor_map[connection_socket]

    def remove_connection_socket(self, connection_socket):
        """
        Removes the connection with the given socket.

        @type connection_socket: Socket
        @param connection_socket: The connection socket to be used
        in the removal of the connection.
        """

        # retrieves the service connection from the service connections map
        service_connection = self.service_connections_map[connection_socket]

        # removes the connection for the given service connection
        self.remove_connection(service_connection)

    def poll_cancel_connections(self):
        """
        Polls the current connection scheduled
        for canceling.
        In case a connection is found to be timed out
        the associated work is canceled and and the
        connection is closed.
        """

        # retrieves the current clock
        current_clock = time.clock()

        # iterates over all the service connections
        for service_connection in self.service_connections_list:
            # in case there is a cancel time defined and there is a timeout
            if service_connection.cancel_time and service_connection.cancel_time < current_clock:
                # retrieves the connection tuple
                connection_tuple = service_connection.get_connection_tuple()

                # removes the ready service connection (via remove work)
                self.remove_work(connection_tuple)

    def poll_connections(self, poll_timeout = POLL_TIMEOUT):
        """
        Polls the current connection to check
        if any contains new information to be read.

        @type poll_timeout: float
        @param poll_timeout: The timeout to be used in the polling.
        @rtype: List
        @return: The selected values for read (ready sockets).
        """

        if EPOLL_SUPPORT:
            return self.__poll_connections_epoll(poll_timeout)
        else:
            return self.__poll_connections_base(poll_timeout)

    def __wake_base(self):
        """
        The wake task base implementation.
        """

        # sends a "dummy" message to the wake "file" (via communication channel)
        self.wake_file.sendto(DUMMY_MESSAGE_VALUE, (LOCAL_HOST, self.wake_file_port))

    def __add_connection_epoll(self, connection_socket, connection_address, connection_port):
        # retrieves the connection socket file descriptor
        connection_socket_file_descriptor = self.__get_connection_socket_file_descriptor(connection_socket)

        # registers the connection socket in the epoll
        self.epoll.register(connection_socket_file_descriptor, REGISTER_MASK)

    def __remove_connection_epoll(self, service_connection):
        # retrieves the connection socket
        connection_socket = service_connection.get_base_connection_socket()

        # retrieves the connection socket file descriptor
        connection_socket_file_descriptor = self.__get_connection_socket_file_descriptor(connection_socket)

        # unregisters the connection socket from the epoll
        self.epoll.unregister(connection_socket_file_descriptor)

    def __poll_connections_base(self, poll_timeout):
        # in case no service connection sockets exist
        if not self.service_connection_sockets_list:
            # returns an empty list
            return []

        # runs the select in the connection socket, with timeout
        selected_values = select.select(self.service_connection_sockets_list, [], [], poll_timeout)

        # retrieves the selected values for read
        selected_values_read = selected_values[0]

        # processes the poll connections
        self.__poll_connections_process(selected_values_read)

        # returns the selected values for read
        return selected_values_read

    def __poll_connections_epoll(self, poll_timeout):
        # in case no service connection sockets exist
        if not self.service_connection_sockets_list:
            # returns an empty list
            return []

        # polls the current epoll object
        events = self.epoll.poll(poll_timeout)

        # creates the list of selected values for read
        selected_values_read = []

        # iterates over all the events
        for connection_socket_file_descriptor, event in events:
            # in case the event is not ready for input or hang-up
            if not event & NEW_VALUE_MASK:
                # resets the connection socket file descriptor status
                self.epoll.modify(connection_socket_file_descriptor, 0)

                # continues the loop
                continue

            # retrieves the connection socket, using the connection socket file descriptor
            connection_socket = self.connection_socket_file_descriptor_connection_socket_map[connection_socket_file_descriptor]

            # adds the connection socket to the selected
            # values for read list
            selected_values_read.append(connection_socket)

        # processes the poll connections
        self.__poll_connections_process(selected_values_read)

        # returns the selected values for read
        return selected_values_read

    def __poll_connections_process(self, selected_values_read):
        # checks if the wake "file" exists in the selected
        # values for read list
        if self.wake_file in selected_values_read:
            # receives one byte from the wake "file"
            self.wake_file.recv(1)

            # removes the wake "file" from the selected values
            # for read list
            selected_values_read.remove(self.wake_file)

    def __get_connection_socket_file_descriptor(self, connection_socket):
        """
        Retrieves the connection socket file descriptor from
        the given connection socket.

        @type connection_socket: Socket
        @param connection_socket: The connection socket to retrieve the
        connection socket file descriptor.
        @rtype: int
        @return: The connection socket file descriptor.
        """

        try:
            # retrieves the connection socket file descriptor
            connection_socket_file_descriptor = connection_socket.fileno()
        except:
            # retrieves the connection socket file descriptor from the map
            connection_socket_file_descriptor = self.connection_socket_connection_socket_file_descriptor_map[connection_socket]

        # returns the connection socket file descriptor
        return connection_socket_file_descriptor

class AbstractServiceConnectionlessHandler:
    """
    The abstract service connectionless handler.
    """

    service = None
    """ The service reference """

    service_plugin = None
    """ The service plugin """

    service_configuration = None
    """ The service configuration """

    service_connections_list = []
    """ The list of service connections """

    service_connections_map = {}
    """ The map of service connections """

    connection_timeout = CONNECTION_TIMEOUT
    """ The connection timeout """

    chunk_size = CHUNK_SIZE
    """ The connection chunk size """

    client_service = None
    """ The client service reference """

    def __init__(self, service, service_plugin, service_configuration, connection_timeout, chunk_size, client_service_class, extra_parameters):
        """
        Constructor of the class.

        @type service: AbstractService
        @param service: The service reference.
        @type service_plugin: Plugin
        @param service_plugin: The service plugin.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration.
        @type connection_timeout: float
        @param connection_timeout: The connection timeout.
        @type chunk_size: int
        @param chunk_size: The chunk size.
        @type client_service_class: Class
        @param client_service_class: The client service class.
        @type extra_parameters: Dictionary
        @param extra_parameters: The extra parameters.
        """

        self.service = service
        self.service_plugin = service_plugin
        self.service_configuration = service_configuration
        self.connection_timeout = connection_timeout
        self.chunk_size = chunk_size

        self.service_data_list = []
        self.service_connections_map = {}

        # creates the client service object
        self.client_service = client_service_class(self.service_plugin, self, service_configuration, main_service_utils_exceptions.MainServiceUtilsException, extra_parameters)

    def start(self):
        pass

    def stop(self):
        pass

    def process(self):
        """
        Processes a work "tick".
        The work tick consists in the processing of the currently
        available data.
        """

        # iterates over all the available service
        # connections
        for service_connection in self.service_connections_list:
            # handles the current request
            self.client_service.handle_request(service_connection)

            # retrieves the connection tuple
            connection_tuple = service_connection.get_connection_tuple()

            # removes the ready service connection (via remove work)
            self.remove_work(connection_tuple)

    def wake(self):
        """
        Wakes the current task releasing the current
        process call.
        """

        pass

    def work_added(self, work_reference):
        """
        Called when a work is added.

        @type work_reference: Object
        @param work_reference: The reference to the work to be added.
        """

        # unpacks the work reference retrieving the connection data, socket,
        # address and port
        connection_data, connection_socket, connection_address, connection_port = work_reference

        # adds the connection to the current service connectionless handler
        self.add_connection(connection_data, connection_socket, connection_address, connection_port)

    def work_removed(self, work_reference):
        """
        Called when a work is removed.

        @type work_reference: Object
        @param work_reference: The reference to the work to be removed.
        """

        # unpacks the work reference retrieving the connection data, socket,
        # address and port
        _connection_data, connection_socket, connection_address, _connection_port = work_reference

        # removes the connection using the socket and address as reference
        self.remove_connection_socket_address(connection_socket, connection_address)

    def add_connection(self, connection_data, connection_socket, connection_address, connection_port):
        """
        Adds a new connection to the service connection handler.

        @type connection_data: String
        @param connection_data: The connection data.
        @type connection_socket: Socket
        @param connection_socket: The connection socket.
        @type connection_address: Tuple
        @param connection_address: The connection address.
        @type connection_port: int
        @param connection_port: The connection port.
        @rtype: ServiceConnection
        @return: The created service connection.
        """

        # creates the new service connection
        service_connection = ServiceConnectionless(self.service_plugin, self, connection_socket, connection_address, connection_port, connection_data, self.chunk_size)

        # creates the connection tuple
        connection_tuple = (connection_socket, connection_address)

        # adds the service connection to the service connections list
        self.service_connections_list.append(service_connection)

        # sets the service connection in the service connections map
        self.service_connections_map[connection_tuple] = service_connection

        # handles the opened service connection
        self.client_service.handle_opened(service_connection)

        # returns the created service connection
        return service_connection

    def remove_connection(self, service_connection):
        """
        Removes the given service connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be removed.
        """

        # retrieves the connection socket
        connection_socket = service_connection.get_base_connection_socket()

        # retrieves the connection address
        connection_address = service_connection.get_connection_address()

        # creates the connection tuple
        connection_tuple = (connection_socket, connection_address)

        # handles the closed service connection
        self.client_service.handle_closed(service_connection)

        # removes the connection from the service connections list
        self.service_connections_list.remove(service_connection)

        # removes the service connection from the service connections map
        del self.service_connections_map[connection_tuple]

    def remove_connection_socket_address(self, connection_socket, connection_address):
        """
        Removes the connection with the given socket and address.

        @type connection_socket: Socket
        @param connection_socket: The connection socket to be used
        in the removal of the connection.
        @type connection_address: Tuple
        @param connection_address: The connection address tuple to be
        used in the removal of the connection.
        """

        # creates the connection tuple
        connection_tuple = (connection_socket, connection_address)

        # retrieves the service connection from the service connections map
        service_connection = self.service_connections_map[connection_tuple]

        # removes the connection for the given service connection
        self.remove_connection(service_connection)

class ServiceConnection:
    """
    The service connection class.
    Describes a service connection.
    """

    service_plugin = None
    """ The service plugin """

    service_connection_handler = None
    """ The service connection handler """

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

    def __init__(self, service_plugin, service_connection_handler, connection_socket, connection_address, connection_port, connection_chunk_size):
        """
        Constructor of the class.

        @type service_plugin: Plugin
        @param service_plugin: The service plugin.
        @type service_connection_handler: AbstractServiceConnectionHandler
        @param service_connection_handler: The service connection handler.
        @type connection_socket: Socket
        @param connection_socket: The connection socket.
        @type connection_address: Tuple
        @param connection_address: The connection address.
        @type connection_port: int
        @param connection_port: The connection port.
        @type connection_chunk_size: int
        @param connection_chunk_size: The connection chunk size.
        """

        self.service_plugin = service_plugin
        self.service_connection_handler = service_connection_handler
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
        self.service_plugin.debug("Connected to: %s" % str(self.connection_address))

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
        self.service_plugin.debug("Disconnected from: %s" % str(self.connection_address))

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

        # retrieves the main service utils
        main_service_utils = self.service_connection_handler.service.main_service_utils

        # retrieves the socket upgrader plugins map
        socket_upgrader_plugins_map = main_service_utils.socket_upgrader_plugins_map

        # in case the upgrader handler is not found in the handler plugins map
        if not socket_upgrader in socket_upgrader_plugins_map:
            # raises the socket upgrader not found exception
            raise main_service_utils_exceptions.SocketUpgraderNotFound("socket upgrader %s not found" % self.socket_upgrader)

        # retrieves the socket upgrader plugin
        socket_upgrader_plugin = main_service_utils.socket_upgrader_plugins_map[socket_upgrader]

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
            # runs the select in the connection socket, with timeout
            selected_values = select.select([self.connection_socket], [], [], request_timeout)
        except:
            # raises the request closed exception
            raise main_service_utils_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
            # closes the connection socket
            self.connection_socket.close()

            # raises the server request timeout exception
            raise main_service_utils_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.connection_socket.recv(chunk_size)
        except:
            # raises the client request timeout exception
            raise main_service_utils_exceptions.ClientRequestTimeout("timeout")

        # returns the data
        return data

    def send(self, message, response_timeout = RESPONSE_TIMEOUT):
        """
        Sends the given message to the socket.
        Raises an exception in case there is a problem sending
        the message.

        @type message: String
        @param message: The message to be sent.
        @type request_timeout: float
        @param request_timeout: The timeout to be used in data sending.
        """

        # retrieves the number of bytes in the message
        number_bytes = len(message)

        # iterates continuously
        while True:
            try:
                # runs the select in the connection socket, with timeout
                selected_values = select.select([], [self.connection_socket], [], response_timeout)
            except:
                # raises the request closed exception
                raise main_service_utils_exceptions.RequestClosed("invalid socket")

            if selected_values == ([], [], []):
                # closes the connection socket
                self.connection_socket.close()

                # raises the server response timeout exception
                raise main_service_utils_exceptions.ClientResponseTimeout("%is timeout" % response_timeout)
            try:
                # sends the data in chunks
                number_bytes_sent = self.connection_socket.send(message)
            except:
                # raises the client response timeout exception
                raise main_service_utils_exceptions.ServerResponseTimeout("timeout")

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

class ServiceConnectionless(ServiceConnection):
    """
    The service connection for information
    flow based in connectionless mechanisms.
    """

    connection_data = None
    """ The connection data """

    def __init__(self, service_plugin, service_connection_handler, connection_socket, connection_address, connection_port, connection_data, connection_chunk_size):
        """
        Constructor of the class.

        @type service_plugin: Plugin
        @param service_plugin: The service plugin.
        @type service_connection_handler: AbstractServiceConnectionHandler
        @param service_connection_handler: The service connection handler.
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

        ServiceConnection.__init__(self, service_connection_handler, service_plugin, connection_socket, connection_address, connection_port, connection_chunk_size)

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
