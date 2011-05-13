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
import traceback

import colony.libs.map_util
import colony.libs.string_buffer_util

import main_service_pop_exceptions

CONNECTION_TYPE = "connection"
""" The connection type """

BIND_HOST = ""
""" The host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 60
""" The request timeout """

RESPONSE_TIMEOUT = 60
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

NUMBER_THREADS = 15
""" The number of threads """

MAXIMUM_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

MAXIMUM_NUMBER_WORKS_THREAD = 5
""" The maximum number of works per thread """

WORK_SCHEDULING_ALGORITHM = 1
""" The work scheduling algorithm """

DEFAULT_PORT = 110
""" The default port """

END_TOKEN_VALUE = "\r\n"
""" The end token value """

END_MULTILINE_TOKEN_VALUE = "."
""" The end multiline token value """

SOCKET_UPGRADER_NAME = "ssl"
""" The socket upgrader name """

VALID_VALUE = "valid"
""" The valid value """

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

    pop_service = None
    """ The pop service reference """

    pop_service_configuration = {}
    """ The pop service configuration """

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
        self.pop_service_configuration = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the main service utils plugin
        main_service_utils_plugin = self.main_service_pop_plugin.main_service_utils_plugin

        # generates the parameters
        service_parameters = self._generate_service_parameters(parameters)

        # generates the pop service using the given service parameters
        self.pop_service = main_service_utils_plugin.generate_service(service_parameters)

        # starts the pop service
        self.pop_service.start_service()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to stop the service.
        """

        # destroys the parameters
        self._destroy_service_parameters(parameters)

        # starts the pop service
        self.pop_service.stop_service()

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

    def set_service_configuration_property(self, service_configuration_property):
        # retrieves the service configuration
        service_configuration = service_configuration_property.get_data()

        # cleans the pop service configuration
        colony.libs.map_util.map_clean(self.pop_service_configuration)

        # copies the service configuration to the pop service configuration
        colony.libs.map_util.map_copy(service_configuration, self.pop_service_configuration)

    def unset_service_configuration_property(self):
        # cleans the pop service configuration
        colony.libs.map_util.map_clean(self.pop_service_configuration)

    def _get_service_configuration(self):
        """
        Retrieves the service configuration map.

        @rtype: Dictionary
        @return: The service configuration map.
        """

        return self.pop_service_configuration

    def _generate_service_parameters(self, parameters):
        """
        Retrieves the service parameters map from the base parameters
        map.

        @type parameters: Dictionary
        @param parameters: The base parameters map to be used to build
        the final service parameters map.
        @rtype: Dictionary
        @return: The final service parameters map.
        """

        # retrieves the end points value
        end_points = parameters.get("end_points", [])

        # retrieves the socket provider value
        socket_provider = parameters.get("socket_provider", None)

        # retrieves the port value
        port = parameters.get("port", DEFAULT_PORT)

        # retrieves the socket parameters value
        socket_parameters = parameters.get("socket_parameters", {})

        # retrieves the service configuration
        service_configuration = self._get_service_configuration()

        # retrieves the end points configuration value
        end_points = service_configuration.get("default_end_points", end_points)

        # retrieves the socket provider configuration value
        socket_provider = service_configuration.get("default_socket_provider", socket_provider)

        # retrieves the port configuration value
        port = service_configuration.get("default_port", port)

        # retrieves the socket parameters configuration value
        socket_parameters = service_configuration.get("default_socket_parameters", socket_parameters)

        # retrieves the socket parameters configuration value
        socket_parameters = service_configuration.get("default_socket_parameters", socket_parameters)

        # retrieves the client connection timeout parameters configuration value
        client_connection_timeout = service_configuration.get("default_client_connection_timeout", CLIENT_CONNECTION_TIMEOUT)

        # retrieves the connection timeout parameters configuration value
        connection_timeout = service_configuration.get("default_connection_timeout", REQUEST_TIMEOUT)

        # retrieves the request timeout parameters configuration value
        request_timeout = service_configuration.get("default_request_timeout", REQUEST_TIMEOUT)

        # retrieves the response timeout parameters configuration value
        response_timeout = service_configuration.get("default_response_timeout", RESPONSE_TIMEOUT)

        # retrieves the number threads configuration value
        number_threads = service_configuration.get("default_number_threads", NUMBER_THREADS)

        # retrieves the scheduling algorithm configuration value
        scheduling_algorithm = service_configuration.get("default_scheduling_algorithm", SCHEDULING_ALGORITHM)

        # retrieves the maximum number threads configuration value
        maximum_number_threads = service_configuration.get("default_maximum_number_threads", MAXIMUM_NUMBER_THREADS)

        # retrieves the maximum number work threads configuration value
        maximum_number_work_threads = service_configuration.get("default_maximum_number_work_threads", MAXIMUM_NUMBER_WORKS_THREAD)

        # retrieves the work scheduling algorithm configuration value
        work_scheduling_algorithm = service_configuration.get("default_work_scheduling_algorithm", WORK_SCHEDULING_ALGORITHM)

        # creates the pool configuration map
        pool_configuration = {
            "name" : "pop pool",
            "description" : "pool to support pop client connections",
            "number_threads" : number_threads,
            "scheduling_algorithm" : scheduling_algorithm,
            "maximum_number_threads" : maximum_number_threads,
            "maximum_number_works_thread" : maximum_number_work_threads,
            "work_scheduling_algorithm" : work_scheduling_algorithm
        }

        # creates the extra parameters map
        extra_parameters = {}

        # creates the parameters map
        parameters = {
            "type" : CONNECTION_TYPE,
            "service_plugin" : self.main_service_pop_plugin,
            "service_handling_task_class" : PopClientServiceHandler,
            "end_points" : end_points,
            "socket_provider" : socket_provider,
            "bind_host" : BIND_HOST,
            "port" : port,
            "socket_parameters" : socket_parameters,
            "chunk_size" : CHUNK_SIZE,
            "service_configuration" : service_configuration,
            "extra_parameters" :  extra_parameters,
            "pool_configuration" : pool_configuration,
            "client_connection_timeout" : client_connection_timeout,
            "connection_timeout" : connection_timeout,
            "request_timeout" : request_timeout,
            "response_timeout" : response_timeout
        }

        # returns the parameters
        return parameters

    def _destroy_service_parameters(self, parameters):
        """
        Destroys the service parameters map from the base parameters
        map.

        @type parameters: Dictionary
        @param parameters: The base parameters map to be used to destroy
        the final service parameters map.
        """

        pass

class PopClientServiceHandler:
    """
    The pop client service handler class.
    """

    service_plugin = None
    """ The service plugin """

    service_connection_handler = None
    """ The service connection handler """

    service_configuration = None
    """ The service configuration """

    service_utils_exception_class = None
    """" The service utils exception class """

    def __init__(self, service_plugin, service_connection_handler, service_configuration, service_utils_exception_class, extra_parameters):
        """
        Constructor of the class.

        @type service_plugin: Plugin
        @param service_plugin: The service plugin.
        @type service_connection_handler: AbstractServiceConnectionHandler
        @param service_connection_handler: The abstract service connection handler, that
        handles this connection.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration.
        @type main_service_utils_exception: Class
        @param main_service_utils_exception: The service utils exception class.
        @type extra_parameters: Dictionary
        @param extra_parameters: The extra parameters.
        """

        self.service_plugin = service_plugin
        self.service_connection_handler = service_connection_handler
        self.service_configuration = service_configuration
        self.service_utils_exception_class = service_utils_exception_class

    def handle_opened(self, service_connection):
        # retrieves the service connection session
        session = self._get_session(service_connection)

        # handles the request as a start session request
        self._handle_start_session_request(session, service_connection)

    def handle_closed(self, service_connection):
        pass

    def handle_request(self, service_connection):
        # retrieves the service connection session
        session = self._get_session(service_connection)

        # handles the request as a normal session request
        return self._handle_normal_session_request(session, service_connection)

    def retrieve_initial_request(self, session, service_connection):
        """
        Retrieves the initial request from the received message.

        @type session: PopSession
        @param session: The current pop session.
        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @rtype: PopRequest
        @return: The request from the received message.
        """

        # creates the initial request object
        request = PopRequest()

        # sets the session object in the request
        request.set_session(session)

        # returns the initial request
        return request

    def retrieve_request(self, session, service_connection):
        """
        Retrieves the request from the received message.

        @type session: PopSession
        @param session: The current pop session.
        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @rtype: PopRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a request object
        request = PopRequest()

        # continuous loop
        while True:
            try:
                # receives the data
                data = service_connection.receive()
            except self.service_utils_exception_class:
                # raises the pop data retrieval exception
                raise main_service_pop_exceptions.PopDataRetrievalException("problem retrieving data")

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

    def send_exception(self, service_connection, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
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
        self.send_request(service_connection, request)

    def send_request(self, service_connection, request):
        # retrieves the result from the request
        result = request.get_result()

        try:
            # sends the result to the service connection
            service_connection.send(result)
        except self.service_utils_exception_class, exception:
            # error in the client side
            self.service_plugin.error("Problem sending request: " + unicode(exception))

            # raises the pop data sending exception
            raise main_service_pop_exceptions.PopDataSendingException("problem sending data")

    def _handle_start_session_request(self, session, service_connection):
        # retrieves the pop service authentication handler plugins map
        pop_service_authentication_handler_plugins_map = self.service_plugin.main_service_pop.pop_service_authentication_handler_plugins_map

        # retrieves the pop service session handler plugins map
        pop_service_session_handler_plugins_map = self.service_plugin.main_service_pop.pop_service_session_handler_plugins_map

        # retrieves the pop service handler plugins map
        pop_service_handler_plugins_map = self.service_plugin.main_service_pop.pop_service_handler_plugins_map

        try:
            # retrieves the initial request
            request = self.retrieve_initial_request(session, service_connection)
        except main_service_pop_exceptions.MainServicePopException:
            # prints a debug message about the connection closing
            self.service_plugin.debug("Connection: %s closed by peer, timeout or invalid request" % str(service_connection))

            # returns false (connection closed)
            return False

        try:
            # retrieves the real service configuration,
            # taking the request information into account
            service_configuration = self._get_service_configuration(request)

            # retrieves the default authentication handler name
            authentication_handler_name = service_configuration.get("default_authentication_handler", None)

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

            # in case the handler is not found in the handler plugins map
            if not handler_name in pop_service_handler_plugins_map:
                # raises an pop handler not found exception
                raise main_service_pop_exceptions.PopHandlerNotFoundException("no handler found for current request: " + handler_name)

            # retrieves the pop service handler plugin
            pop_service_handler_plugin = pop_service_handler_plugins_map[handler_name]

            # handles the initial request by the request handler
            pop_service_handler_plugin.handle_initial_request(request)

            try:
                # sends the initial request to the client (initial response)
                self.send_request(service_connection, request)
            except main_service_pop_exceptions.PopRuntimeException, exception:
                # prints a warning message message
                self.service_plugin.warning("Runtime problem: %s, while sending request" % unicode(exception))

                # returns false (connection closed)
                return False
            except main_service_pop_exceptions.MainServicePopException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending request" % str(service_connection))

                # returns false (connection closed)
                return False

            # sets the session as started
            session.set_started(True)
        except Exception, exception:
            # prints info message about exception
            self.service_plugin.info("There was an exception handling the request: " + unicode(exception))

            try:
                # sends the exception
                self.send_exception(service_connection, request, exception)
            except main_service_pop_exceptions.MainServicePopException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending exception" % str(service_connection))

                # returns false (connection closed)
                return False

        # returns true (connection remains open)
        return True

    def _handle_normal_session_request(self, session, service_connection):
        # retrieves the pop service handler plugins map
        pop_service_handler_plugins_map = self.service_plugin.main_service_pop.pop_service_handler_plugins_map

        try:
            # retrieves the request
            request = self.retrieve_request(session, service_connection)
        except main_service_pop_exceptions.MainServicePopException:
            # prints a debug message about the connection closing
            self.service_plugin.debug("Connection: %s closed by peer, timeout or invalid request" % str(service_connection))

            # returns false (connection closed)
            return False

        try:
            # prints debug message about request
            self.service_plugin.debug("Handling request: %s" % str(request))

            # retrieves the real service configuration,
            # taking the request information into account
            service_configuration = self._get_service_configuration(request)

            # retrieves the default handler name
            handler_name = service_configuration.get("default_handler", None)

            # in case no handler name is defined (request not handled)
            if not handler_name:
                # raises an pop no handler exception
                raise main_service_pop_exceptions.PopNoHandlerException("no handler defined for current request")

            # in case the handler is not found in the handler plugins map
            if not handler_name in pop_service_handler_plugins_map:
                # raises an pop handler not found exception
                raise main_service_pop_exceptions.PopHandlerNotFoundException("no handler found for current request: " + handler_name)

            # retrieves the pop service handler plugin
            pop_service_handler_plugin = pop_service_handler_plugins_map[handler_name]

            # handles the request by the request handler
            pop_service_handler_plugin.handle_request(request)

            try:
                # sends the request to the client (response)
                self.send_request(service_connection, request)
            except main_service_pop_exceptions.PopRuntimeException, exception:
                # prints a warning message message
                self.service_plugin.warning("Runtime problem: %s, while sending request" % unicode(exception))

                # returns false (connection closed)
                return False
            except main_service_pop_exceptions.MainServicePopException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending request" % str(service_connection))

                # returns false (connection closed)
                return False

            # retrieves the value of the upgrade flag
            upgrade = session.get_upgrade()

            # in case the upgrade flag is set
            if upgrade:
                # upgrades the session connection (service connection)
                session.upgrade_connection(service_connection)

                # unsets the upgrade flag
                session.set_upgrade(False)

            # in case the session is closed
            if session.get_closed():
                # prints debug message about session
                self.service_plugin.debug("Session closed: %s" % str(session))

                # returns false (connection closed)
                return False

            # retrieves the request timeout from the service connection
            service_connection_request_timeout = service_connection.connection_request_timeout

            # prints a debug message
            self.service_plugin.debug("Connection: %s kept alive for %ss" % (str(service_connection), str(service_connection_request_timeout)))
        except Exception, exception:
            # prints info message about exception
            self.service_plugin.info("There was an exception handling the request: " + unicode(exception))

            try:
                # sends the exception
                self.send_exception(service_connection, request, exception)
            except main_service_pop_exceptions.MainServicePopException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending exception" % str(service_connection))

                # returns false (connection closed)
                return False

        # returns true (connection remains open)
        return True

    def _get_session(self, service_connection):
        """
        Retrieves the current pop session using
        the service connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection
        to be used to retrieve the session.
        @rtype: PopSession
        @return: The current pop session
        """

        # tries to retrieve session from the service connection
        session = service_connection.get_connection_property("session")

        # in case no session is available
        if not session:
            # creates a new session
            session = self._create_session()

            # sets the session as a connection property
            service_connection.set_connection_property("session", session)

        # returns the session
        return session

    def _create_session(self):
        """
        Creates a new pop session.

        @rtype: PopSession
        @return: The created pop session.
        """

        # creates the session object
        session = PopSession(self)

        return session

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

        # validates the current request
        self.validate()

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

    def validate(self):
        """
        Validates the current request, raising exception
        in case validation fails.
        """

        pass

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

    started = False
    """ The started flag """

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

    message_client = None
    """ The message client """

    authentication_properties = {}
    """ The authentication properties """

    session_properties = {}
    """ The session properties """

    message_id_uid_map = {}
    """ The map associating the message id with the message uid """

    message_id_uid_map_generated = False
    """ The flag controlling the generation of the messa id uid map """

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

        # retrieves the authentication result valid
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication result
        # is valid
        if authentication_result_valid:
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

    def upgrade_connection(self, service_connection):
        """
        Upgrades the connection associated with the
        current session.

        @type service_connection: ServiceConnection
        @param service_connection: The current service connection.
        """

        # the parameters for the "upgrading" of the service connection
        parameters = {
            "server_side" : True,
            "do_handshake_on_connect" : False
        }

        # upgrades the current service connection
        service_connection.upgrade(SOCKET_UPGRADER_NAME, parameters)

    def get_mailbox(self, name = None):
        """
        Returns the mailbox for the given name, or for
        the current user if none is given.

        @type name: String
        @param name: The name of the mailbox to be retrieved.
        @rtype: Mailbox
        @return: The retrieved mailbox.
        """

        # sets the mailbox name as the given name or the current user
        name = name or self.current_user

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

        # sets the mailbox name as the given name or the current user
        name = name or self.current_user

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

    def get_started(self):
        """
        Retrieves the started.

        @rtype: bool
        @return: The started.
        """

        return self.started

    def set_started(self, started):
        """
        Sets the closed.

        @type started: bool
        @param started: The started.
        """

        self.started = started

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

    def get_message_id_uid_map_generated(self):
        """
        Retrieves the message id uid map generated.

        @rtype: bool
        @return: The message id uid map generated.
        """

        return self.message_id_uid_map_generated

    def set_message_id_uid_map_generated(self, message_id_uid_map_generated):
        """
        Sets the message id uid map generated.

        @type message_id_uid_map_generated: bool
        @param message_id_uid_map_generated: The message id uid map generated.
        """

        self.message_id_uid_map_generated = message_id_uid_map_generated
