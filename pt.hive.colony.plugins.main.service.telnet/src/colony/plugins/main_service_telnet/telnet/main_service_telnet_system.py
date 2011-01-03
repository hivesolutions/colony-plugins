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

import main_service_telnet_exceptions

CONNECTION_TYPE = "connection"
""" The connection type """

BIND_HOST = ""
""" The bind host value """

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

DEFAULT_PORT = 23
""" The default port """

class MainServiceTelnet:
    """
    The main service telnet class.
    """

    main_service_telnet_plugin = None
    """ The main service telnet plugin """

    telnet_service_handler_plugins_map = {}
    """ The telnet service handler plugins map """

    telnet_service = None
    """ The telnet service reference """

    telnet_service_configuration = {}
    """ The telnet service configuration """

    def __init__(self, main_service_telnet_plugin):
        """
        Constructor of the class.

        @type main_service_telnet_plugin: MainServiceTelnetPlugin
        @param main_service_telnet_plugin: The main service telnet plugin.
        """

        self.main_service_telnet_plugin = main_service_telnet_plugin

        self.telnet_service_handler_plugin_map = {}
        self.telnet_service_configuration = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the main service utils plugin
        main_service_utils_plugin = self.main_service_telnet_plugin.main_service_utils_plugin

        # generates the parameters
        service_parameters = self._generate_service_parameters(parameters)

        # generates the telnet service using the given service parameters
        self.telnet_service = main_service_utils_plugin.generate_service(service_parameters)

        # starts the telnet service
        self.telnet_service.start_service()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to stop the service.
        """

        # starts the telnet service
        self.telnet_service.stop_service()

    def telnet_service_handler_load(self, telnet_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = telnet_service_handler_plugin.get_handler_name()

        self.telnet_service_handler_plugins_map[handler_name] = telnet_service_handler_plugin

    def telnet_service_handler_unload(self, telnet_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = telnet_service_handler_plugin.get_handler_name()

        del self.telnet_service_handler_plugins_map[handler_name]

    def set_service_configuration_property(self, service_configuration_property):
        # retrieves the service configuration
        service_configuration = service_configuration_property.get_data()

        # cleans the telnet service configuration
        colony.libs.map_util.map_clean(self.telnet_service_configuration)

        # copies the service configuration to the telnet service configuration
        colony.libs.map_util.map_copy(service_configuration, self.telnet_service_configuration)

    def unset_service_configuration_property(self):
        # cleans the http service configuration
        colony.libs.map_util.map_clean(self.telnet_service_configuration)

    def _get_service_configuration(self):
        """
        Retrieves the service configuration map.

        @rtype: Dictionary
        @return: The service configuration map.
        """

        return self.telnet_service_configuration

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
        pool_configuration = {"name" : "telnet pool",
                              "description" : "pool to support telnet client connections",
                              "number_threads" : number_threads,
                              "scheduling_algorithm" : scheduling_algorithm,
                              "maximum_number_threads" : maximum_number_threads,
                              "maximum_number_works_thread" : maximum_number_work_threads,
                              "work_scheduling_algorithm" : work_scheduling_algorithm}

        # creates the extra parameters map
        extra_parameters = {}

        # creates the parameters map
        parameters = {"type" : CONNECTION_TYPE,
                      "service_plugin" : self.main_service_telnet_plugin,
                      "service_handling_task_class" : TelnetClientServiceHandler,
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
                      "response_timeout" : response_timeout}

        # returns the parameters
        return parameters

class TelnetClientServiceHandler:
    """
    The telnet client service handler class.
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
        # receives the initial data
        service_connection.receive()

        # sends the result to the service connection
        service_connection.send("Welcome to colony telnet server\r\n")

        # creates the initial request object
        request = TelnetRequest()

        # handles the initial request by the request handler
        self.service_plugin.telnet_service_handler_plugins[0].handle_initial_request(request)

        # sends the initial request to the client (initial response)
        self.send_request(service_connection, request)

    def handle_closed(self, service_connection):
        pass

    def handle_request(self, service_connection):
        try:
            # retrieves the request
            request = self.retrieve_request(service_connection)
        except main_service_telnet_exceptions.MainServiceTelnetException:
            # prints a debug message about the connection closing
            self.service_plugin.debug("Connection: %s closed by peer, timeout or invalid request" % str(service_connection))

            # returns false (connection closed)
            return False

        try:
            # prints debug message about request
            self.service_plugin.debug("Handling request: %s" % str(request))

            # in case a close message is received
            if request.get_message() == "close":
                # returns false (connection closed)
                return False

            # handles the request by the request handler
            self.service_plugin.telnet_service_handler_plugins[0].handle_request(request)

            try:
                # sends the request to the client (response)
                self.send_request(service_connection, request)
            except main_service_telnet_exceptions.MainServiceTelnetException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending request" % str(service_connection))

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
            except main_service_telnet_exceptions.MainServiceTelnetException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending exception" % str(service_connection))

                # returns false (connection closed)
                return False

        # returns true (connection remains open)
        return True

    def retrieve_request(self, service_connection):
        """
        Retrieves the request from the received message.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @rtype: TelnetRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a request object
        request = TelnetRequest()

        # continuous loop
        while True:
            try:
                # receives the data
                data = service_connection.receive()
            except self.service_utils_exception_class:
                # raises the telnet data retrieval exception
                raise main_service_telnet_exceptions.TelnetDataRetrievalException("problem retrieving data")

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

    def send_exception(self, service_connection, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type request: PolicyRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # writes the exception message
        request.write("error: '" + str(exception) + "'\n")

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

            # raises the telnet data sending exception
            raise main_service_telnet_exceptions.TelnetDataSendingException("problem sending data")

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
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()
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
