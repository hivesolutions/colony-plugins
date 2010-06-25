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

import colony.libs.string_buffer_util

import main_service_policy_exceptions

BIND_HOST_VALUE = ""
""" The bind host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 5
""" The request timeout """

CHUNK_SIZE = 4096
""" The chunk size """

NUMBER_THREADS = 2
""" The number of threads """

MAX_NUMBER_THREADS = 4
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

DEFAULT_PORT = 843
""" The default port """

VALID_REQUEST_VALUE = "<policy-file-request/>"
""" The valid request value """

MAIN_SERVICE_POLICY_RESOURCES_PATH = "main_service_policy/policy/resources"
""" The web mvc manager resources path """

DEFAULT_POLICY_FILE = MAIN_SERVICE_POLICY_RESOURCES_PATH + "/default.policy"
""" The default policy file """

ERROR_POLICY_FILE = MAIN_SERVICE_POLICY_RESOURCES_PATH + "/error.policy"
""" The error policy file """

class MainServicePolicy:
    """
    The main service policy class.
    """

    main_service_becula_plugin = None
    """ The main service policy plugin """

    policy_service_handler_plugins_map = {}
    """ The policy service handler plugins map """

    policy_socket = None
    """ The policy socket """

    policy_connection_active = False
    """ The policy connection active flag """

    policy_client_thread_pool = None
    """ The policy client thread pool """

    policy_connection_close_event = None
    """ The policy connection close event """

    policy_connection_close_end_event = None
    """ The policy connection close end event """

    def __init__(self, main_service_policy_plugin):
        """
        Constructor of the class.

        @type main_service_policy_plugin: MainServicePolicyPlugin
        @param main_service_policy_plugin: The main service policy plugin.
        """

        self.main_service_policy_plugin = main_service_policy_plugin

        self.policy_service_handler_plugin_map = {}
        self.policy_connection_close_event = threading.Event()
        self.policy_connection_close_end_event = threading.Event()

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the socket provider value
        socket_provider = parameters.get("socket_provider", None)

        # retrieves the port value
        port = parameters.get("port", DEFAULT_PORT)

        # retrieves the service configuration property
        service_configuration_property = self.main_service_policy_plugin.get_configuration_property("server_configuration")

        # in case the service configuration property is defined
        if service_configuration_property:
            # retrieves the service configuration
            service_configuration = service_configuration_property.get_data()
        else:
            # sets the service configuration as an empty map
            service_configuration = {}

        # retrieves the socket provider configuration value
        socket_provider = service_configuration.get("default_socket_provider", socket_provider)

        # retrieves the port configuration value
        port = service_configuration.get("default_port", port)

        # start the server for the given socket provider, port and encoding
        self.start_server(socket_provider, port, service_configuration)

        # clears the policy connection close event
        self.policy_connection_close_event.clear()

        # sets the policy connection close end event
        self.policy_connection_close_end_event.set()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        self.stop_server()

    def start_server(self, socket_provider, port, service_configuration):
        """
        Starts the server in the given port.

        @type socket_provider: String
        @param socket_provider: The name of the socket provider to be used.
        @type port: int
        @param port: The port to start the server.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        """

        # retrieves the thread pool manager plugin
        thread_pool_manager_plugin = self.main_service_policy_plugin.thread_pool_manager_plugin

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates the policy client thread pool
        self.policy_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool("policy pool",
                                                                                           "pool to support policy client connections",
                                                                                            NUMBER_THREADS, SCHEDULING_ALGORITHM, MAX_NUMBER_THREADS)

        # starts the policy client thread pool
        self.policy_client_thread_pool.start_pool()

        # sets the policy connection active flag as true
        self.policy_connection_active = True

        # in case the socket provider is defined
        if socket_provider:
            # retrieves the socket provider plugins
            socket_provider_plugins = self.main_service_policy_plugin.socket_provider_plugins

            # iterates over all the socket provider plugins
            for socket_provider_plugin in socket_provider_plugins:
                # retrieves the provider name from the socket provider plugin
                socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

                # in case the names are the same
                if socket_provider_plugin_provider_name == socket_provider:
                    # the parameters for the socket provider
                    parameters = {"server_side" : True, "do_handshake_on_connect" : False}

                    # creates a new policy socket with the socket provider plugin
                    self.policy_socket = socket_provider_plugin.provide_socket_parameters(parameters)

            # in case the socket was not created, no socket provider found
            if not self.policy_socket:
                raise main_service_policy_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
        else:
            # creates the policy socket
            self.policy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # sets the socket to be able to reuse the socket
        self.policy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the policy socket
        self.policy_socket.bind((BIND_HOST_VALUE, port))

        # start listening in the policy socket
        self.policy_socket.listen(5)

        # loops while the policy connection is active
        while not self.policy_connection_close_event.isSet():
            try:
                # sets the socket to non blocking mode
                self.policy_socket.setblocking(0)

                # starts the select values
                selected_values = ([], [], [])

                # iterates while there is no selected values
                while selected_values == ([], [], []):
                    # in case the connection is closed
                    if self.policy_connection_close_event.isSet():
                        # closes the policy socket
                        self.policy_socket.close()

                        return

                    # selects the values
                    selected_values = select.select([self.policy_socket], [], [], CLIENT_CONNECTION_TIMEOUT)

                # sets the socket to blocking mode
                self.policy_socket.setblocking(1)
            except:
                # prints info message about connection
                self.main_service_policy_plugin.info("The socket is not valid for selection of the pool")

                return

            # in case the connection is closed
            if self.policy_connection_close_event.isSet():
                # closes the policy socket
                self.policy_socket.close()

                return

            try:
                # accepts the connection retrieving the policy connection object and the address
                policy_connection, policy_address = self.policy_socket.accept()

                # creates a new policy client service task, with the given policy connection, policy address, encoding and encoding handler
                policy_client_service_task = PolicyClientServiceTask(self.main_service_policy_plugin, policy_connection, policy_address, port, service_configuration)

                # creates a new task descriptor
                task_descriptor = task_descriptor_class(start_method = policy_client_service_task.start,
                                                        stop_method = policy_client_service_task.stop,
                                                        pause_method = policy_client_service_task.pause,
                                                        resume_method = policy_client_service_task.resume)

                # inserts the new task descriptor into the policy client thread pool
                self.policy_client_thread_pool.insert_task(task_descriptor)

                # prints a debug message about the number of threads in pool
                self.main_service_policy_plugin.debug("Number of threads in pool: %d" % self.policy_client_thread_pool.current_number_threads)
            except Exception, exception:
                # prints an error message about the problem accepting the connection
                self.main_service_policy_plugin.error("Error accepting connection: " + str(exception))

        # closes the policy socket
        self.policy_socket.close()

    def stop_server(self):
        """
        Stops the server.
        """

        # sets the policy connection active flag as false
        self.policy_connection_active = False

        # sets the policy connection close event
        self.policy_connection_close_event.set()

        # waits for the policy connection close end event
        self.policy_connection_close_end_event.wait()

        # clears the policy connection close end event
        self.policy_connection_close_end_event.clear()

        # stops all the pool tasks
        self.policy_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.policy_client_thread_pool.stop_pool()

    def policy_service_handler_load(self, policy_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = policy_service_handler_plugin.get_handler_name()

        self.policy_service_handler_plugins_map[handler_name] = policy_service_handler_plugin

    def policy_service_handler_unload(self, policy_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = policy_service_handler_plugin.get_handler_name()

        del self.policy_service_handler_plugins_map[handler_name]

class PolicyClientServiceTask:
    """
    The policy client service task class.
    """

    main_service_policy_plugin = None
    """ The main service policy plugin """

    policy_connection = None
    """ The policy connection """

    policy_address = None
    """ The policy address """

    port = None
    """ The policy port """

    service_configuration = None
    """ The service configuration """

    current_request_handler = None
    """ The current request handler being used """

    def __init__(self, main_service_policy_plugin, policy_connection, policy_address, port, service_configuration):
        self.main_service_policy_plugin = main_service_policy_plugin
        self.policy_connection = policy_connection
        self.policy_address = policy_address
        self.port = port
        self.service_configuration = service_configuration

        self.current_request_handler = self.policy_request_handler

    def start(self):
        # retrieves the policy service handler plugins map
        policy_service_handler_plugins_map = self.main_service_policy_plugin.main_service_policy.policy_service_handler_plugins_map

        # prints debug message about connection
        self.main_service_policy_plugin.debug("Connected to: %s" % str(self.policy_address))

        # sets the request timeout
        request_timeout = REQUEST_TIMEOUT

        # iterates indefinitely
        while True:
            # handles the current request if it returns false
            # the connection was closed or is meant to be closed
            if not self.current_request_handler(request_timeout, policy_service_handler_plugins_map):
                # breaks the cycle to close the policy connection
                break

        # closes the policy connection
        self.policy_connection.close()

    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def policy_request_handler(self, request_timeout, policy_service_handler_plugins_map):
        try:
            # retrieves the request
            request = self.retrieve_request(request_timeout)
        except main_service_policy_exceptions.MainServicePolicyException:
            # prints a debug message about the connection closing
            self.main_service_policy_plugin.debug("Connection: %s closed by peer, timeout or invalid request" % str(self.policy_address))

            # returns false (connection closed)
            return False

        try:
            # prints debug message about request
            self.main_service_policy_plugin.debug("Handling request: %s" % str(request))

            # retrieves the real service configuration,
            # taking the request information into account
            service_configuration = self._get_service_configuration(request)

            # retrieves the plugin manager
            plugin_manager = self.main_service_policy_plugin.manager

            # retrieves the main service policy path
            main_service_policy_plugin_path = plugin_manager.get_plugin_path_by_id(self.main_service_policy_plugin.id)

            # retrieves the policy file path
            policy_file_path = service_configuration.get("policy_file", main_service_policy_plugin_path + "/" + DEFAULT_POLICY_FILE)

            # sets the file path in the request
            request.set_file_path(policy_file_path)

            # sends the request to the client (response)
            self.send_request(request)

            # prints a debug message
            self.main_service_policy_plugin.debug("Connection: %s kept alive for %ss" % (str(self.policy_address), str(request_timeout)))
        except Exception, exception:
            # prints info message about exception
            self.main_service_policy_plugin.info("There was an exception handling the request: " + str(exception))

            # sends the exception
            self.send_exception(request, exception)

        # returns true (connection remains open)
        return True

    def retrieve_request(self, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: PolicyRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a request object
        request = PolicyRequest({})

        # creates the start line loaded flag
        start_line_loaded = False

        # creates the header loaded flag
        header_loaded = False

        # creates the message offset index, representing the
        # offset byte to the initialization of the message
        message_offset_index = 0

        # creates the message size value
        message_size = 0

        # creates the received data size (counter)
        received_data_size = 0

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(request_timeout)

            # retrieves the data length
            data_length = len(data)

            # in case no valid data was received
            if data_length == 0:
                # raises the policy invalid data exception
                raise main_service_policy_exceptions.PolicyInvalidDataException("empty data received")

            # increments the received data size (counter)
            received_data_size += data_length

            # writes the data to the string buffer
            message.write(data)

            # in case the header is loaded or the message contents are completely loaded
            if not header_loaded or received_data_size - message_offset_index == message_size:
                # retrieves the message value from the string buffer
                message_value = message.get_value()
            # in case there's no need to inspect the message contents
            else:
                # continues with the loop
                continue

            # in case the start line is not loaded
            if not start_line_loaded:
                # finds the first end of string value
                start_line_index = message_value.find("\0")

                # in case there is a new line value found
                if not start_line_index == -1:
                    # retrieves the start line
                    start_line = message_value[:start_line_index]

                    # in case the start line is valid
                    if not start_line == VALID_REQUEST_VALUE:
                        # raises the policy invalid data exception
                        raise main_service_policy_exceptions.PolicyInvalidDataException("invalid data received: " + start_line)

                    # sets the start line loaded flag
                    start_line_loaded = True

                    # returns the request
                    return request

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.policy_connection.setblocking(0)

            # runs the select in the policy connection, with timeout
            selected_values = select.select([self.policy_connection], [], [], request_timeout)

            # sets the connection to blocking mode
            self.policy_connection.setblocking(1)
        except:
            raise main_service_policy_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
            self.policy_connection.close()
            raise main_service_policy_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.policy_connection.recv(chunk_size)
        except:
            raise main_service_policy_exceptions.ClientRequestTimeout("timeout")

        return data

    def send_exception(self, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type request: PolicyRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_service_policy_plugin.manager

        # retrieves the main service policy path
        main_service_policy_plugin_path = plugin_manager.get_plugin_path_by_id(self.main_service_policy_plugin.id)

        # retrieves the error policy file path
        error_policy_file_path = main_service_policy_plugin_path + "/" + ERROR_POLICY_FILE

        # sets the error policy file path in the request
        request.set_file_path(error_policy_file_path)

        # sends the request to the client (response)
        self.send_request(request)

    def send_request(self, request):
        # retrieves the result from the request
        result = request.get_result()

        # sends the result to the policy socket
        self.policy_connection.sendall(result)

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        @type request: PolicyRequest
        @param request: The request to be used in the resolution
        of the service configuration.
        @rtype: Dictionary
        @return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # returns the service configuration
        return service_configuration

class PolicyRequest:
    """
    The policy request class.
    """

    parameters = {}
    """ The parameters """

    file_path = None
    """ The file path of the policy """

    def __init__(self, parameters):
        """
        Constructor of the class.

        @type parameters: Dictionary
        @param parameters: The request parameters.
        """

        self.parameters = parameters

    def __repr__(self):
        return "(%s)" % self.file_path

    def get_result(self):
        """
        Retrieves the result value for the current request.

        @rtype: String
        @return: The result value for the current request.
        """

        # opens the file path
        file = open(self.file_path, "rb")

        # reads the file contents
        file_contents = file.read()

        # appends the extra "zero" character
        file_contents += "\0"

        # returns the file contents as the result
        return file_contents

    def set_file_path(self, file_path):
        """
        Sets the file path.

        @type file_path: String
        @param file_path:  The file path.
        """

        self.file_path = file_path
