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

import colony.libs.string_buffer_util

import main_service_pop_exceptions

BIND_HOST_VALUE = ""
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

DEFAULT_PORT = 110
""" The default port """

END_TOKEN_VALUE = "\r\n"
""" The end token value """

END_MULTILINE_TOKEN_VALUE = "."
""" The end multiline token value """

SOCKET_UPGRADER_NAME = "ssl"
""" The socket upgrader name """

class MainServicePop:
    """
    The main service pop class.
    """

    main_service_pop_plugin = None
    """ The main service pop plugin """

    pop_service_handler_plugins_map = {}
    """ The pop service handler plugins map """

    pop_service_authentication_handler_plugins_map = {}
    """ The pop service authentication handler plugins map """

    pop_service_session_handler_plugins_map = {}
    """ The pop service session handler plugins map """

    pop_socket = None
    """ The pop socket """

    pop_connection_active = False
    """ The pop connection active flag """

    pop_client_thread_pool = None
    """ The pop client thread pool """

    pop_connection_close_event = None
    """ The pop connection close event """

    pop_connection_close_end_event = None
    """ The pop connection close end event """

    def __init__(self, main_service_pop_plugin):
        """
        Constructor of the class.

        @type main_service_pop_plugin: MainServicePopPlugin
        @param main_service_pop_plugin: The main service pop plugin.
        """

        self.main_service_pop_plugin = main_service_pop_plugin

        self.pop_service_handler_plugins_map = {}
        self.pop_service_authentication_handler_plugins_map = {}
        self.pop_service_session_handler_plugins_map = {}
        self.pop_connection_close_event = threading.Event()
        self.pop_connection_close_end_event = threading.Event()

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
        service_configuration_property = self.main_service_pop_plugin.get_configuration_property("server_configuration")

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

        # clears the pop connection close event
        self.pop_connection_close_event.clear()

        # sets the pop connection close end event
        self.pop_connection_close_end_event.set()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # sets the pop connection active flag as false
        self.pop_connection_active = False

        # sets the pop connection close event
        self.pop_connection_close_event.set()

        # waits for the pop connection close end event
        self.pop_connection_close_end_event.wait()

        # clears the pop connection close end event
        self.pop_connection_close_end_event.clear()

        # stops all the pool tasks
        self.pop_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.pop_client_thread_pool.stop_pool()

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
        thread_pool_manager_plugin = self.main_service_pop_plugin.thread_pool_manager_plugin

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates the pop client thread pool
        self.pop_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool("pop pool",
                                                                                         "pool to support pop client connections",
                                                                                         NUMBER_THREADS, SCHEDULING_ALGORITHM, MAX_NUMBER_THREADS)

        # starts the pop client thread pool
        self.pop_client_thread_pool.start_pool()

        # sets the pop connection active flag as true
        self.pop_connection_active = True

        # in case the socket provider is defined
        if socket_provider:
            # retrieves the socket provider plugins
            socket_provider_plugins = self.main_service_pop_plugin.socket_provider_plugins

            # iterates over all the socket provider plugins
            for socket_provider_plugin in socket_provider_plugins:
                # retrieves the provider name from the socket provider plugin
                socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

                # in case the names are the same
                if socket_provider_plugin_provider_name == socket_provider:
                    # the parameters for the socket provider
                    parameters = {"server_side" : True, "do_handshake_on_connect" : False}

                    # creates a new pop socket with the socket provider plugin
                    self.pop_socket = socket_provider_plugin.provide_socket_parameters(parameters)

            # in case the socket was not created, no socket provider found
            if not self.pop_socket:
                raise main_service_pop_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
        else:
            # creates the pop socket
            self.pop_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # sets the socket to be able to reuse the socket
        self.pop_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the pop socket
        self.pop_socket.bind((BIND_HOST_VALUE, port))

        # start listening in the pop socket
        self.pop_socket.listen(5)

        # loops while the pop connection is active
        while not self.pop_connection_close_event.isSet():
            try:
                # sets the socket to non blocking mode
                self.pop_socket.setblocking(0)

                # starts the select values
                selected_values = ([], [], [])

                # iterates while there is no selected values
                while selected_values == ([], [], []):
                    # in case the connection is closed
                    if self.pop_connection_close_event.isSet():
                        # closes the pop socket
                        self.pop_socket.close()

                        return

                    # selects the values
                    selected_values = select.select([self.pop_socket], [], [], CLIENT_CONNECTION_TIMEOUT)

                # sets the socket to blocking mode
                self.pop_socket.setblocking(1)
            except:
                # prints debug message about connection
                self.main_service_pop_plugin.info("The socket is not valid for selection of the pool")

                return

            # in case the connection is closed
            if self.pop_connection_close_event.isSet():
                # closes the pop socket
                self.pop_socket.close()

                return

            try:
                # accepts the connection retrieving the pop connection object and the address
                pop_connection, pop_address = self.pop_socket.accept()

                # creates a new pop client service task, with the given pop connection, address, encoding and encoding handler
                pop_client_service_task = PopClientServiceTask(self.main_service_pop_plugin, pop_connection, pop_address, service_configuration)

                # creates a new task descriptor
                task_descriptor = task_descriptor_class(start_method = pop_client_service_task.start,
                                                        stop_method = pop_client_service_task.stop,
                                                        pause_method = pop_client_service_task.pause,
                                                        resume_method = pop_client_service_task.resume)

                # inserts the new task descriptor into the pop client thread pool
                self.pop_client_thread_pool.insert_task(task_descriptor)

                self.main_service_pop_plugin.debug("Number of threads in pool: %d" % self.pop_client_thread_pool.current_number_threads)
            except Exception, exception:
                self.main_service_pop_plugin.error("Error accepting connection: " + str(exception))

        # closes the pop socket
        self.pop_socket.close()

    def pop_service_handler_load(self, pop_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = pop_service_handler_plugin.get_handler_name()

        self.pop_service_handler_plugins_map[handler_name] = pop_service_handler_plugin

    def pop_service_handler_unload(self, pop_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = pop_service_handler_plugin.get_handler_name()

        del self.pop_service_handler_plugins_map[handler_name]

    def pop_service_authentication_handler_load(self, pop_service_authentication_handler_plugin):
        # retrieves the plugin handler name
        authentication_handler_name = pop_service_authentication_handler_plugin.get_handler_name()

        self.pop_service_authentication_handler_plugins_map[authentication_handler_name] = pop_service_authentication_handler_plugin

    def pop_service_authentication_handler_unload(self, pop_service_authentication_handler_plugin):
        # retrieves the plugin handler name
        authentication_handler_name = pop_service_authentication_handler_plugin.get_handler_name()

        del self.pop_service_authentication_handler_plugins_map[authentication_handler_name]

    def pop_service_session_handler_load(self, pop_service_session_handler_plugin):
        # retrieves the plugin handler name
        session_handler_name = pop_service_session_handler_plugin.get_handler_name()

        self.pop_service_session_handler_plugins_map[session_handler_name] = pop_service_session_handler_plugin

    def pop_service_session_handler_unload(self, pop_service_session_handler_plugin):
        # retrieves the plugin handler name
        session_handler_name = pop_service_session_handler_plugin.get_handler_name()

        del self.pop_service_session_handler_plugins_map[session_handler_name]

class PopClientServiceTask:
    """
    The pop client service task class.
    """

    main_service_pop_plugin = None
    """ The main service pop plugin """

    pop_connection = None
    """ The pop connection """

    pop_address = None
    """ The pop address """

    service_configuration = None
    """ The service configuration """

    encoding_handler = None
    """ The encoding handler """

    def __init__(self, main_service_pop_plugin, pop_connection, pop_address, service_configuration):
        self.main_service_pop_plugin = main_service_pop_plugin
        self.pop_connection = pop_connection
        self.pop_address = pop_address
        self.service_configuration = service_configuration

    def start(self):
        # prints debug message about connection
        self.main_service_pop_plugin.debug("Connected to: %s" % str(self.pop_address))

        # sets the request timeout
        request_timeout = REQUEST_TIMEOUT

        # creates the session object
        session = PopSession(self)

        # retrieves the socket upgrader plugin for the socket upgrader name
        socket_upgrader_plugin = self._get_socket_upgrader_plugin(SOCKET_UPGRADER_NAME)

        # sets the upgrader handler in the session
        session.upgrader_handler = socket_upgrader_plugin.upgrade_socket_parameters

        # retrieves the initial request
        request = self.retrieve_initial_request(session, request_timeout)

        # retrieves the real service configuration,
        # taking the request information into account
        service_configuration = self._get_service_configuration(request)

        # retrieves the default authentication handler name
        authentication_handler_name = service_configuration.get("default_authentication_handler", None)

        # retrieves the pop service authentication handler plugins map
        pop_service_authentication_handler_plugins_map = self.main_service_pop_plugin.main_service_pop.pop_service_authentication_handler_plugins_map

        # in case the authentication handler is not found in the handler plugins map
        if not authentication_handler_name in pop_service_authentication_handler_plugins_map:
            # raises an pop handler not found exception
            raise main_service_pop_exceptions.PopHandlerNotFoundException("no authentication handler found for current request: " + authentication_handler_name)

        # retrieves the pop service authentication handler plugin
        pop_service_authentication_handler_plugin = pop_service_authentication_handler_plugins_map[authentication_handler_name]

        # sets the authentication handler (plugin) in the session
        session.set_authentication_handler(pop_service_authentication_handler_plugin)

        # retrieves the authentication properties
        authentication_properties = service_configuration.get("authentication_properties", {})

        # sets the authentication properties in the session
        session.set_authentication_properties(authentication_properties)

        # retrieves the default session handler name
        session_handler_name = service_configuration.get("default_session_handler", None)

        # retrieves the pop service session handler plugins map
        pop_service_session_handler_plugins_map = self.main_service_pop_plugin.main_service_pop.pop_service_session_handler_plugins_map

        # in case the session handler is not found in the handler plugins map
        if not session_handler_name in pop_service_session_handler_plugins_map:
            # raises an pop handler not found exception
            raise main_service_pop_exceptions.PopHandlerNotFoundException("no session handler found for current request: " + session_handler_name)

        # retrieves the pop service session handler plugin
        pop_service_session_handler_plugin = pop_service_session_handler_plugins_map[session_handler_name]

        # sets the session handler (plugin) in the session
        session.set_session_handler(pop_service_session_handler_plugin)

        # retrieves the session properties
        session_properties = service_configuration.get("session_properties", {})

        # sets the session properties in the session
        session.set_session_properties(session_properties)

        # retrieves the default handler name
        handler_name = service_configuration.get("default_handler", None)

        # in case no handler name is defined (request not handled)
        if not handler_name:
            # raises an pop no handler exception
            raise main_service_pop_exceptions.PopNoHandlerException("no handler defined for current request")

        # retrieves the pop service handler plugins map
        pop_service_handler_plugins_map = self.main_service_pop_plugin.main_service_pop.pop_service_handler_plugins_map

        # in case the handler is not found in the handler plugins map
        if not handler_name in pop_service_handler_plugins_map:
            # raises an pop handler not found exception
            raise main_service_pop_exceptions.PopHandlerNotFoundException("no handler found for current request: " + handler_name)

        # retrieves the pop service handler plugin
        pop_service_handler_plugin = pop_service_handler_plugins_map[handler_name]

        # handles the initial request by the request handler
        pop_service_handler_plugin.handle_initial_request(request)

        # sends the initial request to the client (initial response)
        self.send_request(request)

        while True:
            try:
                # retrieves the request
                request = self.retrieve_request(session, request_timeout)
            except main_service_pop_exceptions.MainServicePopException:
                self.main_service_pop_plugin.debug("Connection: %s closed" % str(self.pop_address))
                return

            try:
                # prints debug message about request
                self.main_service_pop_plugin.debug("Handling request: %s" % str(request))

                # handles the request by the request handler
                pop_service_handler_plugin.handle_request(request)

                # sends the request to the client (response)
                self.send_request(request)

                # retrieves the value of the upgrade flag
                upgrade = session.get_upgrade()

                # in case the upgrade flag is set
                if upgrade:
                    # upgrades the session connection
                    session.upgrade_connection()

                    # unsets the upgrade flag
                    session.set_upgrade(False)

                # in case the session is closed
                if session.get_closed():
                    # prints debug message about session
                    self.main_service_pop_plugin.debug("Session closed: %s" % str(session))

                    break

            except Exception, exception:
                self.send_exception(request, exception)

        # closes the pop connection
        self.pop_connection.close()

    def stop(self):
        # closes the pop connection
        self.pop_connection.close()

    def pause(self):
        pass

    def resume(self):
        pass

    def retrieve_initial_request(self, session, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the initial request from the received message.

        @type session: PopSession
        @param session: The current pop session.
        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: PopRequest
        @return: The request from the received message.
        """

        # creates the initial request object
        request = PopRequest()

        # sets the session object in the request
        request.set_session(session)

        # returns the initial request
        return request

    def retrieve_request(self, session, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type session: PopSession
        @param session: The current pop session.
        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: PopRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a request object
        request = PopRequest()

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(request_timeout)

            # in case no valid data was received
            if data == "":
                raise main_service_pop_exceptions.PopInvalidDataException("empty data received")

            # writes the data to the string buffer
            message.write(data)

            # in case the end token is not found in the data
            if data.find(END_TOKEN_VALUE) == -1:
                # continues the loop
                continue

            # retrieves the message value from the string buffer
            message_value = message.get_value()

            # finds the first end token value
            end_token_index = message_value.find(END_TOKEN_VALUE)

            # in case there is an end token found
            if not end_token_index == -1:
                # retrieves the pop message
                pop_message = message_value[:end_token_index]

                # splits the pop message
                pop_message_splitted = pop_message.split(" ")

                # retrieves the pop command
                pop_command = pop_message_splitted[0].lower()

                # retrieves the pop arguments
                pop_arguments = pop_message_splitted[1:]

                # sets the pop command in the request
                request.set_command(pop_command)

                # sets the pop arguments in the request
                request.set_arguments(pop_arguments)

                # sets the pop message in the request
                request.set_message(pop_message)

                # sets the session object in the request
                request.set_session(session)

                # returns the request
                return request

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.pop_connection.setblocking(0)

            # runs the select in the pop connection, with timeout
            selected_values = select.select([self.pop_connection], [], [], request_timeout)

            # sets the connection to blocking mode
            self.pop_connection.setblocking(1)
        except:
            raise main_service_pop_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
            self.pop_connection.close()
            raise main_service_pop_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.pop_connection.recv(chunk_size)
        except:
            raise main_service_pop_exceptions.ClientRequestTimeout("timeout")

        return data

    def send_exception(self, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type request: PopRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # sets the request response code
        request.set_response_code("-ERR")

        # sets the request response message
        request.set_response_message("exception occurred")

        # writes the exception message
        request.write(" - error: '" + str(exception) + "'\n")

        # writes the traceback message in the request
        request.write("traceback:\n")

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            formated_traceback = traceback.format_tb(traceback_list)
        else:
            formated_traceback = ()

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
            self.pop_connection.sendall(result_value)
        except:
            # error in the client side
            return

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        @type request: PopRequest
        @param request: The request to be used in the resolution
        of the service configuration.
        @rtype: Dictionary
        @return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # returns the service configuration
        return service_configuration

    def _get_socket_upgrader_plugin(self, socket_upgrader_name):
        # retrieves the socket upgrader plugins
        socket_upgrader_plugins = self.main_service_pop_plugin.socket_upgrader_plugins

        # iterates over all the socket upgrader plugins
        for socket_upgrader_plugin in socket_upgrader_plugins:
            # retrieves the upgrader name from the socket upgrader plugin
            socket_upgrader_plugin_upgrader_name = socket_upgrader_plugin.get_upgrader_name()

            # in case the names are the same
            if socket_upgrader_plugin_upgrader_name == socket_upgrader_name:
                return socket_upgrader_plugin

class PopRequest:
    """
    The pop request class.
    """

    message = None
    """ The received message """

    command = None
    """ The received command """

    arguments = []
    """ The received arguments """

    response_message = None
    """ The response message """

    response_messages = []
    """ The response messages """

    response_code = None
    """ The response code """

    session = None
    """ The session """

    message_stream = None
    """ The message stream """

    properties = {}
    """ The properties """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.arguments = []
        self.response_messages = []
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.command, self.message)

    def read(self):
        return self.message

    def write(self, message):
        self.message_stream.write(message)

    def get_result(self):
        """
        Retrieves the result value, processing
        the current request structure.

        @rtype: String
        @return: The result value for the current
        request structure.
        """

        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # in case the response messages
        # are defined
        if self.response_messages:
            # starts the counter value
            counter = len(self.response_messages)

            # writes the response code to the result
            result.write(self.response_code + " ")

            # iterates over all the response messages
            for response_message in self.response_messages:
                # in case the response message starts with a multiline token value
                # the first character is stuffed
                if response_message.startswith(END_MULTILINE_TOKEN_VALUE):
                    # the first character of the message is stuffed
                    response_message = END_MULTILINE_TOKEN_VALUE + response_message

                # in case the counter is one (last response message)
                if counter == 1:
                    # adds the response message to the result stream
                    result.write(response_message + END_TOKEN_VALUE)

                    # writes the end of multi line message token
                    result.write(END_MULTILINE_TOKEN_VALUE)
                else:
                    # adds the response message and the end of line
                    # to the result stream
                    result.write(response_message + END_TOKEN_VALUE)

                # decrements the counter
                counter -= 1
        else:
            # writes the response line (response code plus response message)
            # to the result stream
            result.write(self.response_code + " " + self.response_message)

        # retrieves the result string value
        message = self.message_stream.get_value()

        # in case the message is not empty
        if not message == "":
            # writes the message to the result stream
            result.write(message)

        # writes the end of mail to the result stream
        result.write(END_TOKEN_VALUE)

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def get_message(self):
        """
        Retrieves the message.

        @rtype: String
        @return: The message.
        """

        return self.message

    def set_message(self, message):
        """
        Sets the message.

        @type message: String
        @param message: The message.
        """

        self.message = message

    def get_command(self):
        """
        Retrieves the command.

        @rtype: String
        @return: The command.
        """

        return self.command

    def set_command(self, command):
        """
        Sets the command.

        @type command: String
        @param command: The command.
        """

        self.command = command

    def get_arguments(self):
        """
        Retrieves the arguments.

        @rtype: List
        @return: The arguments.
        """

        return self.arguments

    def set_arguments(self, arguments):
        """
        Sets the arguments.

        @type arguments: List
        @param arguments: The arguments.
        """

        self.arguments = arguments

    def get_response_message(self):
        """
        Retrieves the response message.

        @rtype: String
        @return: The response message.
        """

        return self.response_message

    def set_response_message(self, response_message):
        """
        Sets the response message.

        @type response_message: String
        @param response_message: The response message.
        """

        self.response_message = response_message

    def get_response_messages(self):
        """
        Retrieves the response messages.

        @rtype: List
        @return: The response messages.
        """

        return self.response_messages

    def set_response_messages(self, response_messages):
        """
        Sets the response messages.

        @type response_messages: List
        @param response_messages: The response messages.
        """

        self.response_messages = response_messages

    def get_response_code(self):
        """
        Retrieves the response code.

        @rtype: int
        @return: The response code.
        """

        return self.response_code

    def set_response_code(self, response_code):
        """
        Sets the response code.

        @type response_code: int
        @param response_code: The response code.
        """

        self.response_code = response_code

    def get_session(self):
        """
        Retrieves the session.

        @rtype: Session
        @return: The session.
        """

        return self.session

    def set_session(self, session):
        """
        Sets the session.

        @type session: Session
        @param session: The session.
        """

        self.session = session

    def get_properties(self):
        """
        Retrieves the properties.

        @rtype: Dictionary
        @return: The properties.
        """

        return self.properties

    def set_properties(self, properties):
        """
        Sets the properties.

        @type properties: Dictionary
        @param properties: The properties.
        """

        self.properties = properties

class PopSession:
    """
    The pop session class.
    """

    pop_client_service_task = None
    """ The pop client service task """

    extensions_active = False
    """ The extensions active flag """

    upgrade = False
    """ The upgrade flag """

    closed = False
    """ The closed flag """

    current_user = None
    """ The current user """

    current_password = None
    """ The current password """

    authenticated = False
    """ The authenticated flag """

    properties = {}
    """ The properties of the current session """

    authentication_handler = None
    """ The authentication handler object """

    session_handler = None
    """ The session handler object """

    upgrader_handler = None
    """ The upgrader handler """

    message_client = None
    """ The message client """

    authentication_properties = {}
    """ The authentication properties """

    session_properties = {}
    """ The session properties """

    message_id_uid_map = {}
    """ The map associating the message id with the message uid """

    def __init__(self, pop_client_service_task):
        """
        Constructor of the class.

        @type pop_client_service_task: PopClientServiceTask
        @param pop_client_service_task: The pop client service task.
        """

        self.pop_client_service_task = pop_client_service_task

        self.properties = {}
        self.authentication_properties = {}
        self.session_properties = {}
        self.message_id_uid_map = {}

    def __repr__(self):
        return "(%s)" % self.properties

    def authenticate(self, username, password):
        """
        Authenticates a user with the given username
        and password, using the current authentication handler.

        @type username: String
        @param username: The username to be used in the authentication.
        @type password: String
        @param password: The password to be used in the authentication.
        @rtype: Dictionary
        @return: The authentication map, in case of success otherwise none.
        """

        # in case no authentication handler is set
        if not self.authentication_handler:
            # returns invalid
            return None

        # uses the authentication handler to try to authenticate
        authentication_result = self.authentication_handler.handle_authentication(username, password, self.authentication_properties)

        # in case the authentication result
        # is valid
        if authentication_result:
            # sets the authenticated flag
            self.authenticated = True

        # returns the authentication result
        return authentication_result

    def handle(self):
        """
        Handles the session, using with the current
        session handler.
        """

        # in case no session handler is set
        if not self.session_handler:
            # returns invalid
            return None

        # handles the session with the session handler
        self.session_handler.handle_session(self, self.session_properties)

    def upgrade_connection(self):
        """
        Upgrades the connection associated with the
        current session.
        """

        # in case no upgrader handler is set
        if not self.upgrader_handler:
            raise main_service_pop_exceptions.PopRuntimeException("no upgrader handler defined")

        # the parameters for the upgrader handler
        parameters = {"server_side" : True, "do_handshake_on_connect" : False}

        # upgrades the pop client service task with the current upgrader handler
        self.pop_client_service_task.pop_connection = self.upgrader_handler(self.pop_client_service_task.pop_connection, parameters)

    def get_mailbox(self, name = None):
        """
        Returns the mailbox for the given name, or for
        the current user if none is given.

        @type name: String
        @param name: The name of the mailbox to be retrieved.
        @rtype: Mailbox
        @return: The retrieved mailbox.
        """

        # in case no name is given
        if not name:
            # sets the mailbox name as the current user
            name = self.current_user

        # retrieves the mailbox for the given name
        mailbox = self.message_client.get_mailbox_name(name)

        # returns the mailbox
        return mailbox

    def get_mailbox_messages(self, name = None):
        """
        Returns the mailbox (containing messages) for the given name, or for
        the current user if none is given.

        @type name: String
        @param name: The name of the mailbox to be retrieved.
        @rtype: Mailbox
        @return: The retrieved mailbox (containing messages).
        """

        # in case no name is given
        if not name:
            # sets the mailbox name as the current user
            name = self.current_user

        # retrieves the mailbox (containing messages) for the given name
        mailbox = self.message_client.get_mailbox_messages_name(name)

        # returns the mailbox
        return mailbox

    def get_message(self, message_uid):
        """
        Returns the message for the given message uid.

        @type message_uid: String
        @param message_uid: The uid of the message to be retrieved.
        @rtype: Message
        @return: The retrieved message.
        """

        # retrieves the message for the given message uid
        message = self.message_client.get_message_uid(message_uid)

        # returns the message
        return message

    def remove_message(self, message_uid):
        """
        Removes the message for the given message uid.

        @type message_uid: String
        @param message_uid: The uid of the message to be removed.
        """

        # removes the message for the given message uid
        self.message_client.remove_message(message_uid)

    def get_pop_client_service_task(self):
        """
        Retrieves the client pop client service task.

        @rtype: PopClientServiceTask
        @return: The client pop client service task.
        """

        return self.pop_client_service_task

    def set_pop_client_service_task(self, pop_client_service_task):
        """
        Sets the client pop client service task.

        @type pop_client_service_task: PopClientServiceTask
        @param pop_client_service_task: The client pop client service task.
        """

        self.pop_client_service_task = pop_client_service_task

    def get_extensions_active(self):
        """
        Retrieves the extensions active.

        @rtype: bool
        @return: The extensions active.
        """

        return self.extensions_active

    def set_extensions_active(self, extensions_active):
        """
        Sets the extensions active.

        @type extensions_active: bool
        @param extensions_active: The extensions active.
        """

        self.extensions_active = extensions_active

    def get_upgrade(self):
        """
        Retrieves the upgrade.

        @rtype: bool
        @return: The upgrade.
        """

        return self.upgrade

    def set_upgrade(self, upgrade):
        """
        Sets the upgrade.

        @type upgrade: bool
        @param upgrade: The upgrade.
        """

        self.upgrade = upgrade

    def get_closed(self):
        """
        Retrieves the closed.

        @rtype: bool
        @return: The closed.
        """

        return self.closed

    def set_closed(self, closed):
        """
        Sets the closed.

        @type closed: bool
        @param closed: The closed.
        """

        self.closed = closed

    def get_current_user(self):
        """
        Retrieves the current user.

        @rtype: String
        @return: The current user.
        """

        return self.current_user

    def set_current_user(self, current_user):
        """
        Sets the current user.

        @type current_user: String
        @param current_user: The current user.
        """

        self.current_user = current_user

    def get_current_password(self):
        """
        Retrieves the current password.

        @rtype: String
        @return: The current password.
        """

        return self.current_password

    def set_current_password(self, current_password):
        """
        Sets the current password.

        @type current_password: String
        @param current_password: The current password.
        """

        self.current_password = current_password

    def get_authenticated(self):
        """
        Retrieves the authenticated.

        @rtype: bool
        @return: The authenticated.
        """

        return self.authenticated

    def set_authenticated(self, authenticated):
        """
        Sets the authenticated.

        @type authenticated: bool
        @param authenticated: The authenticated.
        """

        self.authenticated = authenticated

    def get_messages(self):
        """
        Retrieves the messages.

        @rtype: List
        @return: The messages.
        """

        return self.messages

    def set_messages(self, messages):
        """
        Sets the messages.

        @type messages: List
        @param messages: The messages.
        """

        self.messages = messages

    def get_properties(self):
        """
        Retrieves the properties.

        @rtype: Dictionary
        @return: The properties.
        """

        return self.properties

    def set_properties(self, properties):
        """
        Sets the properties.

        @type properties: Dictionary
        @param properties: The properties.
        """

        self.properties = properties

    def get_authentication_handler(self):
        """
        Retrieves the authentication handler.

        @rtype: AuthenticationHandler
        @return: The authentication handler.
        """

        return self.authentication_handler

    def set_authentication_handler(self, authentication_handler):
        """
        Sets the authentication handler.

        @type authentication_handler: AuthenticationHandler
        @param authentication_handler: The authentication handler.
        """

        self.authentication_handler = authentication_handler

    def get_session_handler(self):
        """
        Retrieves the session handler.

        @rtype: SessionHandler
        @return: The session handler.
        """

        return self.session_handler

    def set_session_handler(self, session_handler):
        """
        Sets the session handler.

        @type session_handler: SessionHandler
        @param session_handler: The session handler.
        """

        self.session_handler = session_handler

    def get_upgrader_handler(self):
        """
        Retrieves the upgrader handler.

        @rtype: UpgraderHandler
        @return: The upgrader handler.
        """

        return self.upgrader_handler

    def set_upgrader_handler(self, upgrader_handler):
        """
        Sets the upgrader handler.

        @type upgrader_handler: UpgraderHandler
        @param upgrader_handler: The upgrader handler.
        """

        self.upgrader_handler = upgrader_handler

    def get_message_client(self):
        """
        Retrieves the message client.

        @rtype: MessageClient
        @return: The message client.
        """

        return self.message_client

    def set_message_client(self, message_client):
        """
        Sets the upgrader handler.

        @type message_client: MessageClient
        @param message_client: The message client.
        """

        self.message_client = message_client

    def get_authentication_properties(self):
        """
        Retrieves the authentication properties.

        @rtype: Dictionary
        @return: The authentication properties.
        """

        return self.authentication_properties

    def set_authentication_properties(self, authentication_properties):
        """
        Sets the authentication properties.

        @type authentication_properties: Dictionary
        @param authentication_properties: The authentication properties.
        """

        self.authentication_properties = authentication_properties

    def get_session_properties(self):
        """
        Retrieves the session properties.

        @rtype: Dictionary
        @return: The session properties.
        """

        return self.session_properties

    def set_session_properties(self, session_properties):
        """
        Sets the session properties.

        @type session_properties: Dictionary
        @param session_properties: The session properties.
        """

        self.session_properties = session_properties

    def get_message_id_uid_map(self):
        """
        Retrieves the message id uid map.

        @rtype: Dictionary
        @return: The message id uid map.
        """

        return self.message_id_uid_map

    def set_message_id_uid_map(self, message_id_uid_map):
        """
        Sets the message id uid map.

        @type message_id_uid_map: Dictionary
        @param message_id_uid_map: The message id uid map.
        """

        self.message_id_uid_map = message_id_uid_map
