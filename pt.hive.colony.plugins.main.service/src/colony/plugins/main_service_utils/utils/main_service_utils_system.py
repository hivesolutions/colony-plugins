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

MAX_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

SERVER_SIDE_VALUE = "server_side"
""" The server side value """

DO_HANDSHAKE_ON_CONNECT_VALUE = "do_handshake_on_connect"
""" The do handshake on connect value """

class MainServiceUtils:
    """
    The main service utils class.
    """

    main_service_utils_plugin = None
    """ The main service utils plugin """

    socket_provider_plugins_map = {}
    """ The socket provider plugins map """

    def __init__(self, main_service_utils_plugin):
        """
        Constructor of the class.

        @type main_service_utils_plugin: MainServiceUtilsPlugin
        @param main_service_utils_plugin: The main service utils plugin.
        """

        self.main_service_utils_plugin = main_service_utils_plugin

        self.socket_provider_plugins_map = {}

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

    def socket_provider_load(self, socket_provider_plugin):
        # retrieves the plugin provider name
        provider_name = socket_provider_plugin.get_provider_name()

        self.socket_provider_plugins_map[provider_name] = socket_provider_plugin

    def socket_provider_unload(self, socket_provider_plugin):
        # retrieves the plugin provider name
        provider_name = socket_provider_plugin.get_provider_name()

        del self.socket_provider_plugins_map[provider_name]

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

    service_client_thread_pool = None
    """ The service client thread pool """

    service_connection_close_event = None
    """ The service connection close event """

    service_connection_close_end_event = None
    """ The service connection close end event """

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

    service_configuration = {}
    """ The service configuration """

    pool_configuration = {}
    """ The pool configuration """

    client_connection_timeout = CLIENT_CONNECTION_TIMEOUT
    """ The client connection timeout """

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

        self.service_plugin = parameters.get("service_plugin", None)
        self.service_handling_task_class = parameters.get("service_handling_task_class", None)
        self.socket_provider = parameters.get("socket_provider", None)
        self.bind_host = parameters.get("bind_host", BIND_HOST)
        self.port = parameters.get("port", PORT)
        self.service_configuration = parameters.get("service_configuration", {})
        self.pool_configuration = parameters.get("pool_configuration", {})
        self.client_connection_timeout = parameters.get("client_connection_timeout", CLIENT_CONNECTION_TIMEOUT)

        self.service_connection_close_event = threading.Event()
        self.service_connection_close_end_event = threading.Event()

    def start_service(self):
        """
        Starts the service.
        """

        # creates the thread pool
        self._create_thread_pool()

        # creates and sets the service socket
        self._create_service_socket()

        # activates and listens the service socket
        self._activate_service_socket()

        # loops while the service connection is active
        while not self.service_connection_close_event.isSet():
            # pools the service socket to check if there
            # is a new connection available
            pool_return_value = self._pool_service_socket()

            # in case the pool return value is not valid or
            # the connection is closed
            if not pool_return_value or self.service_connection_close_event.isSet():
                # breaks the cycle
                break

            # accepts the new client connection
            self._accept_service_socket()

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
        self.service_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.service_client_thread_pool.stop_pool()

    def _create_thread_pool(self):
        # retrieves the thread pool manager plugin
        thread_pool_manager_plugin = self.main_service_utils_plugin.thread_pool_manager_plugin

        # retrieves the thread pool configuration parameters
        pool_name = self.pool_configuration.get("name", POOL_NAME)
        pool_description = self.pool_configuration.get("description", POOL_DESCRIPTION)
        number_threads = self.pool_configuration.get("number_threads", NUMBER_THREADS)
        scheduling_algorithm = self.pool_configuration.get("scheduling_algorithm", SCHEDULING_ALGORITHM)
        max_number_threads = self.pool_configuration.get("max_number_threads", MAX_NUMBER_THREADS)

        # creates the service client thread pool
        self.service_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool(pool_name, pool_description, number_threads, scheduling_algorithm, max_number_threads)

        # starts the service client thread pool
        self.service_client_thread_pool.start_pool()

        # sets the service connection active flag as true
        self.service_connection_active = True

    def _create_service_socket(self):
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

                # returns immediately
                return
            else:
                # raises the socket provider not found exception
                raise main_service_utils_exceptions.SocketProviderNotFound("socket provider %s not found" % self.socket_provider)
        else:
            # creates the service socket
            self.service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _pool_service_socket(self):
        try:
            # sets the socket to non blocking mode
            self.service_socket.setblocking(0)

            # starts the select values
            selected_values = ([], [], [])

            # iterates while there is no selected values
            while selected_values == ([], [], []):
                # in case the connection is closed
                if self.service_connection_close_event.isSet():
                    return False

                # selects the values
                selected_values = select.select([self.service_socket], [], [], self.client_connection_timeout)

            # sets the socket to blocking mode
            self.service_socket.setblocking(1)

            return True
        except:
            # prints info message about connection
            self.main_service_utils_plugin.info("The socket is not valid for selection of the pool")

            return False

    def _accept_service_socket(self):
        try:
            # retrieves the thread pool manager plugin
            thread_pool_manager_plugin = self.main_service_utils_plugin.thread_pool_manager_plugin

            # retrieves the task descriptor class
            task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

            # accepts the connection retrieving the service connection object and the address
            service_connection, service_address = self.service_socket.accept()

            # insets the connection into the pool
            self._insert_connection_pool(service_connection, service_address, task_descriptor_class)
        except Exception, exception:
            # prints an error message about the problem accepting the connection
            self.main_service_utils_plugin.error("Error accepting connection: " + str(exception))

    def _activate_service_socket(self):
        # sets the socket to be able to reuse the socket
        self.service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the service socket
        self.service_socket.bind((self.bind_host, self.port))

        # start listening in the service socket
        self.service_socket.listen(5)

    def _disable_service_socket(self):
        # closes the service socket
        self.service_socket.close()

    def _insert_connection_pool(self, service_connection, service_address, task_descriptor_class):
        """
        Inserts the given service connection into the connection pool.
        This process takes into account the pool usage and the current
        available task.

        @type service_connection: Socket
        @param service_connection: The service connection to be inserted.
        @type service_address: Tuple
        @param service_address: A tuple containing the address information
        of the connection.
        @type task_descriptor_class: Class
        @param task_descriptor_class: The task descriptor class.
        """

        # creates a new service client service task, with the given service connection, service address, port and service configration
        service_client_service_task = self.service_handling_task_class(self.service_plugin, service_connection, service_address, self.port, self.service_configuration)

        # creates a new task descriptor
        task_descriptor = task_descriptor_class(start_method = service_client_service_task.start,
                                                stop_method = service_client_service_task.stop,
                                                pause_method = service_client_service_task.pause,
                                                resume_method = service_client_service_task.resume)

        # inserts the new task descriptor into the service client thread pool
        self.service_client_thread_pool.insert_task(task_descriptor)

        # prints a debug message about the number of threads in pool
        self.main_service_utils_plugin.debug("Number of threads in pool: %d" % self.service_client_thread_pool.current_number_threads)
