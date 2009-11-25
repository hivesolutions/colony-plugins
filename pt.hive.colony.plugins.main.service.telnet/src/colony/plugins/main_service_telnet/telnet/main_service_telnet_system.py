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

import sys
import socket
import select
import threading
import traceback

import string_buffer_util

import main_service_telnet_exceptions

HOST_VALUE = ""
""" The host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 60
""" The request timeout """

CHUNK_SIZE = 4096
""" The chunk size """

NUMBER_THREADS = 15
""" The number of threads """

MAX_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

DEFAULT_PORT = 23
""" The default port """

class MainServiceTelnet:
    """
    The main service telnet class.
    """

    main_service_telnet_plugin = None
    """ The main service telnet plugin """

    telnet_socket = None
    """ The telnet socket """

    telnet_connection_active = False
    """ The telnet connection active flag """

    telnet_client_thread_pool = None
    """ The telnet client thread pool """

    telnet_connection_close_event = None
    """ The telnet connection close event """

    telnet_connection_close_end_event = None
    """ The telnet connection close end event """

    def __init__(self, main_service_telnet_plugin):
        """
        Constructor of the class.

        @type main_service_telnet_plugin: MainServiceTelnetPlugin
        @param main_service_telnet_plugin: The main service telnet plugin.
        """

        self.main_service_telnet_plugin = main_service_telnet_plugin

        self.telnet_connection_close_event = threading.Event()
        self.telnet_connection_close_end_event = threading.Event()

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

        # retrieves the service configuration
        #service_configuration = self.main_service_telnet_plugin.get_configuration_property("server_configuration").get_data()

        service_configuration = {}

        # retrieves the socket provider configuration value
        #socket_provider = service_configuration.get("default_socket_provider", socket_provider)

        # retrieves the port configuration value
        #port = service_configuration.get("default_port", port)

        # start the server for the given socket provider, port and encoding
        self.start_server(socket_provider, port, service_configuration)

        # clears the telnet connection close event
        self.telnet_connection_close_event.clear()

        # sets the telnet connection close end event
        self.telnet_connection_close_end_event.set()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # sets the telnet connection active flag as false
        self.telnet_connection_active = False

        # sets the telnet connection close event
        self.telnet_connection_close_event.set()

        # waits for the telnet connection close end event
        self.telnet_connection_close_end_event.wait()

        # clears the telnet connection close end event
        self.telnet_connection_close_end_event.clear()

        # stops all the pool tasks
        self.telnet_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.telnet_client_thread_pool.stop_pool()

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
        thread_pool_manager_plugin = self.main_service_telnet_plugin.thread_pool_manager_plugin

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates the telnet client thread pool
        self.telnet_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool("telnet pool",
                                                                                           "pool to support telnet client connections",
                                                                                           NUMBER_THREADS, SCHEDULING_ALGORITHM, MAX_NUMBER_THREADS)

        # starts the telnet client thread pool
        self.telnet_client_thread_pool.start_pool()

        # sets the telnet connection active flag as true
        self.telnet_connection_active = True

        # in case the socket provider is defined
        if socket_provider:
            # retrieves the socket provider plugins
            socket_provider_plugins = self.main_service_telnet_plugin.socket_provider_plugins

            # iterates over all the socket provider plugins
            for socket_provider_plugin in socket_provider_plugins:
                # retrieves the provider name from the socket provider plugin
                socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

                # in case the names are the same
                if socket_provider_plugin_provider_name == socket_provider:
                    # creates a new telnet socket with the socket provider plugin
                    self.telnet_socket = socket_provider_plugin.provide_socket()

            # in case the socket was not created, no socket provider found
            if not self.telnet_socket:
                raise main_service_telnet_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
        else:
            # creates the telnet socket
            self.telnet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # sets the socket to be able to reuse the socket
        self.telnet_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the telnet socket
        self.telnet_socket.bind((HOST_VALUE, port))

        # start listening in the telnet socket
        self.telnet_socket.listen(5)

        # loops while the telnet connection is active
        while not self.telnet_connection_close_event.isSet():
            try:
                # sets the socket to non blocking mode
                self.telnet_socket.setblocking(0)

                # starts the select values
                selected_values = ([], [], [])

                # iterates while there is no selected values
                while selected_values == ([], [], []):
                    # in case the connection is closed
                    if self.telnet_connection_close_event.isSet():
                        # closes the telnet socket
                        self.telnet_socket.close()

                        return

                    # selects the values
                    selected_values = select.select([self.telnet_socket], [], [], CLIENT_CONNECTION_TIMEOUT)

                # sets the socket to blocking mode
                self.telnet_socket.setblocking(1)
            except:
                # prints debug message about connection
                self.main_service_telnet_plugin.info("The socket is not valid for selection of the pool")

                return

            # in case the connection is closed
            if self.telnet_connection_close_event.isSet():
                # closes the telnet socket
                self.telnet_socket.close()

                return

            try:
                # accepts the connection retrieving the telnet connection object and the address
                telnet_connection, telnet_address = self.telnet_socket.accept()

                # creates a new telnet client service task, with the given telnet connection, address, encoding and encoding handler
                telnet_client_service_task = TelnetClientServiceTask(self.main_service_telnet_plugin, telnet_connection, telnet_address, service_configuration)

                # creates a new task descriptor
                task_descriptor = task_descriptor_class(start_method = telnet_client_service_task.start,
                                                        stop_method = telnet_client_service_task.stop,
                                                        pause_method = telnet_client_service_task.pause,
                                                        resume_method = telnet_client_service_task.resume)

                # inserts the new task descriptor into the telnet client thread pool
                self.telnet_client_thread_pool.insert_task(task_descriptor)

                self.main_service_telnet_plugin.debug("Number of threads in pool: %d" % self.telnet_client_thread_pool.current_number_threads)
            except Exception, ex:
                print ex
                self.main_service_telnet_plugin.error("Error accepting connection")

        # closes the telnet socket
        self.telnet_socket.close()

class TelnetClientServiceTask:
    """
    The telnet client service task class.
    """

    main_service_telnet_plugin = None
    """ The main service telnet plugin """

    telnet_connection = None
    """ The telnet connection """

    telnet_address = None
    """ The telnet address """

    service_configuration = None
    """ The service configuration """

    encoding_handler = None
    """ The encoding handler """

    def __init__(self, main_service_telnet_plugin, telnet_connection, telnet_address, service_configuration):
        self.main_service_telnet_plugin = main_service_telnet_plugin
        self.telnet_connection = telnet_connection
        self.telnet_address = telnet_address
        self.service_configuration = service_configuration

    def start(self):
        # prints debug message about connection
        self.main_service_telnet_plugin.debug("Connected to: %s" % str(self.telnet_address))

        # sends the welcome message
        self.telnet_connection.send("Welcome to colony telnet server\r\n")

        # creates the initial request object
        request = TelnetRequest()

        # handles the initial request by the request handler
        self.main_service_telnet_plugin.telnet_service_handler_plugins[0].handle_initial_request(request)

        # sends the initial request to the client (initial response)
        self.send_request(request)

        # sets the request timeout
        request_timeout = REQUEST_TIMEOUT

        while True:
            try:
                # retrieves the request
                request = self.retrieve_request(request_timeout)

                # in case a close message is received
                if request.get_message() == "close":
                    break

            except main_service_telnet_exceptions.MainServiceTelnetException:
                self.main_service_telnet_plugin.debug("Connection: %s closed" % str(self.telnet_address))
                return

            try:
                # prints debug message about request
                self.main_service_telnet_plugin.debug("Handling request: %s" % str(request))

                # handles the request by the request handler
                self.main_service_telnet_plugin.telnet_service_handler_plugins[0].handle_request(request)

                # sends the request to the client (response)
                self.send_request(request)
            except Exception, exception:
                self.send_exception(request, exception)

        # closes the telnet connection
        self.telnet_connection.close()

    def stop(self):
        # closes the telnet connection
        self.telnet_connection.close()

    def pause(self):
        pass

    def resume(self):
        pass

    def retrieve_request(self, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: TelnetRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = string_buffer_util.StringBuffer()

        # creates a request object
        request = TelnetRequest()

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(request_timeout)

            # in case no valid data was received
            if data == "":
                raise main_service_telnet_exceptions.TelnetInvalidDataException("empty data received")

            # writes the data to the string buffer
            message.write(data)

            # retrieves the message value from the string buffer
            message_value = message.get_value()

            # finds the first new line value
            new_line_index = message_value.find("\r\n")

            # in case there is a new line value found
            if not new_line_index == -1:
                # retrieves the telnet message
                telnet_message = message_value[:new_line_index]

                # sets the telnet message in the request
                request.set_message(telnet_message)

                # returns the request
                return request

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.telnet_connection.setblocking(0)

            # runs the select in the telnet connection, with timeout
            selected_values = select.select([self.telnet_connection], [], [], request_timeout)

            # sets the connection to blocking mode
            self.telnet_connection.setblocking(1)
        except:
            raise main_service_telnet_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
             self.telnet_connection.close()
             raise main_service_telnet_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.telnet_connection.recv(chunk_size)
        except:
            raise main_service_telnet_exceptions.ClientRequestTimeout("timeout")

        return data

    def send_exception(self, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type request: TelnetRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # writes the exception message
        request.write("error: '" + str(exception) + "'\n")

        # writes the traceback message in the request
        request.write("traceback:\n")

        # writes the traceback in the request
        formated_traceback = traceback.format_tb(sys.exc_traceback)

        # iterates over the traceback lines
        for formated_traceback_line in formated_traceback:
            request.write(formated_traceback_line)

        # sends the request to the client (response)
        self.send_request(request)

    def send_request(self, request):
        self.send_request_simple(request)

    def send_request_simple(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.telnet_connection.send(result_value)
        except:
            # error in the client side
            return

class TelnetRequest:
    """
    The telnet request class.
    """

    message = "none"
    """ The received message """

    operation_type = "none"
    """ The operation type """

    message_stream = None
    """ The message stream """

    properties = {}
    """ The properties """

    def __init__(self):
        self.message_stream = string_buffer_util.StringBuffer()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.operation_type, self.message)

    def read(self):
        return self.message

    def write(self, message):
        self.message_stream.write(message)

    def get_result(self):
        # retrieves the result string value
        message = self.message_stream.get_value()

        # returns the return message
        return message

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
