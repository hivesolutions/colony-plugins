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

import sys
import types

import colony.libs.string_buffer_util

import main_service_abecula_exceptions

CONNECTION_TYPE = "connection"
""" The connection type """

BIND_HOST = ""
""" The bind host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 100
""" The request timeout """

CHUNK_SIZE = 4096
""" The chunk size """

SERVER_NAME = "Hive-Colony-Abecula"
""" The server name """

SERVER_VERSION = "1.0.0"
""" The server version """

ENVIRONMENT_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
""" The environment version """

SERVER_IDENTIFIER = SERVER_NAME + "/" + SERVER_VERSION + " (Python/" + sys.platform + "/" + ENVIRONMENT_VERSION + ")"
""" The server identifier """

NUMBER_THREADS = 10
""" The number of threads """

MAXIMUM_NUMBER_THREADS = 2
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

MAXIMUM_NUMBER_WORKS_THREAD = 5
""" The maximum number of works per thread """

WORK_SCHEDULING_ALGORITHM = 1
""" The work scheduling algorithm """

DEFAULT_PORT = 7676
""" The default port """

STATUS_CODE_VALUES = {100 : "Continue", 101 : "Switching Protocols",
                      200 : "OK", 207 : "Multi-Status",
                      301 : "Moved permanently", 302 : "Found", 303 : "See Other", 304 : "Not Modified",
                      305 : "Use Proxy", 306 : "(Unused)", 307 : "Temporary Redirect",
                      403 : "Forbidden", 404 : "Not Found",
                      500 : "Internal Server Error"}
""" The status code values map """

DEFAULT_STATUS_CODE_VALUE = "Invalid"
""" The default status code value """

CONTENT_LENGTH_VALUE = "Content-Length"
""" The content length value """

CONTENT_LENGTH_LOWER_VALUE = "Content-length"
""" The content length lower value """

SERVER_VALUE = "Server"
""" The server value """

class MainServiceAbecula:
    """
    The main service abecula class.
    """

    main_service_abecula_plugin = None
    """ The main service abecula plugin """

    abecula_service_handler_plugins_map = {}
    """ The abecula service handler plugins map """

    abecula_service = None
    """ The abecula service reference """

    def __init__(self, main_service_abecula_plugin):
        """
        Constructor of the class.

        @type main_service_abecula_plugin: MainServiceAbeculaPlugin
        @param main_service_abecula_plugin: The main service abecula plugin.
        """

        self.main_service_abecula_plugin = main_service_abecula_plugin

        self.abecula_service_handler_plugin_map = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the main service utils plugin
        main_service_utils_plugin = self.main_service_abecula_plugin.main_service_utils_plugin

        # generates the parameters
        service_parameters = self._generate_service_parameters(parameters)

        # generates the abecula service using the given service parameters
        self.abecula_service = main_service_utils_plugin.generate_service(service_parameters)

        # starts the abecula service
        self.abecula_service.start_service()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to stop the service.
        """

        # starts the abecula service
        self.abecula_service.stop_service()

    def abecula_service_handler_load(self, abecula_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = abecula_service_handler_plugin.get_handler_name()

        self.abecula_service_handler_plugins_map[handler_name] = abecula_service_handler_plugin

    def abecula_service_handler_unload(self, abecula_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = abecula_service_handler_plugin.get_handler_name()

        del self.abecula_service_handler_plugins_map[handler_name]

    def _get_service_configuration(self):
        # retrieves the service configuration property
        service_configuration_property = self.main_service_abecula_plugin.get_configuration_property("server_configuration")

        # in case the service configuration property is defined
        if service_configuration_property:
            # retrieves the service configuration
            service_configuration = service_configuration_property.get_data()
        else:
            # sets the service configuration as an empty map
            service_configuration = {}

        return service_configuration

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

        # retrieves the socket provider value
        socket_provider = parameters.get("socket_provider", None)

        # retrieves the port value
        port = parameters.get("port", DEFAULT_PORT)

        # retrieves the service configuration
        service_configuration = self._get_service_configuration()

        # retrieves the socket provider configuration value
        socket_provider = service_configuration.get("default_socket_provider", socket_provider)

        # retrieves the port configuration value
        port = service_configuration.get("default_port", port)

        # creates the pool configuration map
        pool_configuration = {"name" : "abecula pool",
                              "description" : "pool to support abecula client connections",
                              "number_threads" : NUMBER_THREADS,
                              "scheduling_algorithm" : SCHEDULING_ALGORITHM,
                              "maximum_number_threads" : MAXIMUM_NUMBER_THREADS,
                              "maximum_number_works_thread" : MAXIMUM_NUMBER_WORKS_THREAD,
                              "work_scheduling_algorithm" : WORK_SCHEDULING_ALGORITHM}

        # creates the extra parameters map
        extra_parameters = {}

        # creates the parameters map
        parameters = {"type" : CONNECTION_TYPE,
                      "service_plugin" : self.main_service_abecula_plugin,
                      "service_handling_task_class" : AbeculaClientServiceHandler,
                      "socket_provider" : socket_provider,
                      "bind_host" : BIND_HOST,
                      "port" : port,
                      "chunk_size" : CHUNK_SIZE,
                      "service_configuration" : service_configuration,
                      "extra_parameters" :  extra_parameters,
                      "pool_configuration" : pool_configuration,
                      "client_connection_timeout" : CLIENT_CONNECTION_TIMEOUT}

        # returns the parameters
        return parameters

class AbeculaClientServiceHandler:
    """
    The abecula client service handler class.
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
        pass

    def handle_closed(self, service_connection):
        pass

    def handle_request(self, service_connection, request_timeout = REQUEST_TIMEOUT):
        # retrieves the abecula service handler plugins map
        abecula_service_handler_plugins_map = self.service_plugin.main_service_abecula.abecula_service_handler_plugins_map

        try:
            # retrieves the request
            request = self.retrieve_request(service_connection, request_timeout)
        except main_service_abecula_exceptions.MainServiceAbeculaException:
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

            # processes the handler part of the request and retrieves
            # the handler name
            handler_name = self._process_handler(request, service_configuration)

            # in case the request was not already handled
            if not handler_name:
                # retrieves the default handler name
                handler_name = service_configuration.get("default_handler", None)

                # sets the handler path
                request.handler_path = None

            # in case no handler name is defined (request not handled)
            if not handler_name:
                # raises an abecula no handler exception
                raise main_service_abecula_exceptions.AbeculaNoHandlerException("no handler defined for current request")

            # in case the handler is not found in the handler plugins map
            if not handler_name in abecula_service_handler_plugins_map:
                # raises an abecula handler not found exception
                raise main_service_abecula_exceptions.AbeculaHandlerNotFoundException("no handler found for current request: " + handler_name)

            # retrieves the abecula service handler plugin
            abecula_service_handler_plugin = abecula_service_handler_plugins_map[handler_name]

            # handles the request by the request handler
            abecula_service_handler_plugin.handle_request(request)

            # sends the request to the client (response)
            self.send_request(service_connection, request)
        except Exception, exception:
            # prints info message about exception
            self.service_plugin.info("There was an exception handling the request: " + str(exception))

            # sends the exception
            self.send_exception(service_connection, request, exception)

        # returns true (connection remains open)
        return True

    def retrieve_request(self, service_connection, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: AbeculaRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a request object
        request = AbeculaRequest({"service_handler" : self,
                                  "service_connection" : service_connection})

        # creates the start line loaded flag
        start_line_loaded = False

        # creates the header loaded flag
        header_loaded = False

        # creates the message loaded flag
        message_loaded = False

        # creates the message offset index, representing the
        # offset byte to the initialization of the message
        message_offset_index = 0

        # creates the message size value
        message_size = 0

        # creates the received data size (counter)
        received_data_size = 0

        # continuous loop
        while True:
            try:
                # retrieves the data
                data = service_connection.retrieve_data(request_timeout)
            except self.service_utils_exception_class:
                # raises the abecula data retrieval exception
                raise main_service_abecula_exceptions.AbeculaDataRetrievalException("problem retrieving data")

            # retrieves the data length
            data_length = len(data)

            # in case no valid data was received
            if data_length == 0:
                # raises the abecula invalid data exception
                raise main_service_abecula_exceptions.AbeculaInvalidDataException("empty data received")

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
                # finds the first new line value
                start_line_index = message_value.find("\r\n")

                # in case there is a new line value found
                if not start_line_index == -1:
                    # retrieves the start line
                    start_line = message_value[:start_line_index]

                    # splits the start line in spaces
                    start_line_splitted = start_line.split(" ")

                    # retrieves the start line splitted length
                    start_line_splitted_length = len(start_line_splitted)

                    # in case the length of the splitted line is not three
                    if not start_line_splitted_length == 4:
                        # raises the abecula invalid data exception
                        raise main_service_abecula_exceptions.AbeculaInvalidDataException("invalid data received: " + start_line)

                    # retrieve the operation type the target and the protocol version
                    # from the start line splitted
                    operation_id, operation_type, target, protocol_version = start_line_splitted

                    # sets the request operation id
                    request.set_operation_id(operation_id)

                    # sets the request operation type
                    request.set_operation_type(operation_type)

                    # sets the target
                    request.set_target(target)

                    # sets the request protocol version
                    request.set_protocol_version(protocol_version)

                    # sets the start line loaded flag
                    start_line_loaded = True

            # in case the header is not loaded
            if not header_loaded:
                # retrieves the end header index (two new lines)
                end_header_index = message_value.find("\r\n\r\n")

                # in case the end header index is found
                if not end_header_index == -1:
                    # sets the message offset index as the end header index
                    # plus the two sequences of newlines (four characters)
                    message_offset_index = end_header_index + 4

                    # sets the header loaded flag
                    header_loaded = True

                    # retrieves the start header index
                    start_header_index = start_line_index + 2

                    # retrieves the headers part of the message
                    headers = message_value[start_header_index:end_header_index]

                    # splits the headers by line
                    headers_splitted = headers.split("\r\n")

                    # iterates over the headers lines
                    for header_splitted in headers_splitted:
                        # finds the header separator
                        division_index = header_splitted.find(":")

                        # retrieves the header name
                        header_name = header_splitted[:division_index].strip()

                        # retrieves the header value
                        header_value = header_splitted[division_index + 1:].strip()

                        # sets the header in the headers map
                        request.headers_map[header_name] = header_value

                    # in case the content length is defined in the headers map
                    if CONTENT_LENGTH_VALUE in request.headers_map:
                        # retrieves the message size
                        message_size = int(request.headers_map[CONTENT_LENGTH_VALUE])
                    elif CONTENT_LENGTH_LOWER_VALUE in request.headers_map:
                        # retrieves the message size
                        message_size = int(request.headers_map[CONTENT_LENGTH_LOWER_VALUE])
                    # in case there is no content length defined in the headers map
                    else:
                        # returns the request
                        return request

            # in case the message is not loaded and the header is loaded
            if not message_loaded and header_loaded:
                # retrieves the start message size
                start_message_index = end_header_index + 4

                # calculates the message value message length
                message_value_message_length = len(message_value) - start_message_index

                # in case the length of the message value message is the same
                # as the message size
                if message_value_message_length == message_size:
                    # retrieves the message part of the message value
                    message_value_message = message_value[start_message_index:]

                    # sets the message loaded flag
                    message_loaded = True

                    # sets the received message
                    request.received_message = message_value_message

                    # decodes the request if necessary
                    #self.decode_request(request)

                    # returns the request
                    return request

    def send_exception(self, service_connection, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type request: AbeculaRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

#        # resets the response value (deletes answers)
#        request.reset_response()

        # sends the request to the client (response)
        self.send_request(service_connection, request)

    def send_request(self, service_connection, request):
        # retrieves the result from the request
        result = request.get_result()

        # sends the result to the service connection
        service_connection.send(result)

    def create_response(self):
        """
        Creates a new response an returns it.

        @rtype: AbeculaResponse
        @return: The created response.
        """

        # creates a new abecula response
        abecula_response = AbeculaResponse({})

        # sets the protocol version in the abecula response
        abecula_response.set_protocol_version("ABECULA/1.0")

        return abecula_response

    def send_response(self, service_connection, response):
        """
        Sends the given response to the socket.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type response: AbeculaResponse
        @param response: The response to be sent.
        """

        # retrieves the result from the request
        result = response.get_result()

        # sends the result to the service connection
        service_connection.send(result)

    def _process_handler(self, request, service_configuration):
        """
        Processes the handler stage of the abecula request.

        @type request: AbeculaRequest
        @param request: The request to be processed.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        @rtype: String
        @return: The processed handler name.
        """

        # retrieves the handler name as the target of the request
        handler_name = request.get_target()

        # returns the handler name
        return handler_name

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        @type request: AbeculaRequest
        @param request: The request to be used in the resolution
        of the service configuration.
        @rtype: Dictionary
        @return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # returns the service configuration
        return service_configuration

class AbeculaResponse:
    """
    The abecula response class.
    """

    operation_id = None
    """ The operation id """

    operation_type = None
    """ The operation type """

    target = None
    """ The target """

    protocol_version = None
    """ The protocol version """

    headers_map = {}
    """ The headers map """

    message_stream = None
    """ The message stream """

    parameters = {}
    """ The parameters """

    def __init__(self, parameters):
        """
        Constructor of the class.

        @type parameters: Dictionary
        @param parameters: The response parameters.
        """

        self.parameters = parameters

        self.headers_map = {}
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()

    def __repr__(self):
        return "(%s, %s, %s)" % (self.operation_id, self.operation_type, self.protocol_version)

    def write(self, message, flush = 1, encode = True):
        # writes the message to the message stream
        self.message_stream.write(message)

    def flush(self):
        pass

    def get_result(self):
        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # retrieves the result string value
        message = self.message_stream.get_value()

        # writes the abecula command in the string buffer (operation id, operation type, target and protocol version)
        result.write(self.operation_id + " " + self.operation_type + " " + self.target + " " + self.protocol_version + "\r\n")

        # writes the main headers
        result.write(SERVER_VALUE + ": " + SERVER_IDENTIFIER + "\r\n")

        # iterates over all the "extra" header values to be sent
        for header_name, header_value in self.headers_map.items():
            # writes the extra header value in the result
            result.write(header_name + ": " + header_value + "\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write("\r\n")
        result.write(message)

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def set_operation_id(self, operation_id):
        """
        Sets the operation id.

        @type opration_id: String
        @param opration_id: The operation id.
        """

        self.operation_id = operation_id

    def set_operation_type(self, operation_type):
        """
        Sets the operation type.

        @type opration_type: String
        @param opration_type: The operation type.
        """

        self.operation_type = operation_type

    def set_target(self, target):
        """
        Sets the target.

        @type target: String
        @param target: The target.
        """

        self.target = target

    def set_protocol_version(self, protocol_version):
        """
        Sets the protocol version.

        @type protocol_version: String
        @param protocol_version: The protocol version.
        """

        self.protocol_version = protocol_version

class AbeculaRequest:
    """
    The abecula request class.
    """

    service_handler = None
    """ The service handler """

    service_connection = None
    """ The service connection """

    operation_id = None
    """ The operation id """

    operation_type = None
    """ The operation type """

    target = None
    """ The target """

    protocol_version = None
    """ The protocol version """

    headers_map = {}
    """ The headers map """

    response_headers_map = {}
    """ The response headers map """

    received_message = "none"
    """ The received message """

    message_stream = None
    """ The message stream """

    status_code = None
    """ The status code """

    status_message = None
    """ The status message """

    parameters = {}
    """ The parameters """

    def __init__(self, parameters):
        """
        Constructor of the class.

        @type parameters: Dictionary
        @param parameters: The request parameters.
        """

        self.parameters = parameters

        self.service_handler = parameters.get("service_handler", None)
        self.service_connection = parameters.get("service_connection", None)

        self.headers_map = {}
        self.response_headers_map = {}
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()

    def __repr__(self):
        return "(%s, %s, %s, %s)" % (self.operation_id, self.operation_type, self.target, self.protocol_version)

    def read(self):
        return self.received_message

    def write(self, message, flush = 1, encode = True):
        # retrieves the message type
        message_type = type(message)

        # in case the message type is unicode
        if message_type == types.UnicodeType and encode:
            # encodes the message with the defined content type charset
            message = message.encode(self.content_type_charset)

        # writes the message to the message stream
        self.message_stream.write(message)

    def flush(self):
        pass

    def get_result(self):
        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # retrieves the result string value
        message = self.message_stream.get_value()

        # in case the request is encoded
        #if self.encoded:
        #    if self.mediated:
#                self.mediated_handler.encode_file(self.encoding_handler, self.encoding_type)
#            elif self.chunked_encoding:
#                self.chunk_handler.encode_file(self.encoding_handler, self.encoding_type)
#            else:
#                message = self.encoding_handler(message)

        # retrieves the value for the status code
        status_code_value = self.get_status_code_value()

        # writes the abecula command in the string buffer (version, status code and status value)
        result.write(self.protocol_version + " " + self.operation_id + " " + str(self.status_code) + " " + status_code_value + "\r\n")

        # writes the main headers
        result.write(SERVER_VALUE + ": " + SERVER_IDENTIFIER + "\r\n")

        # iterates over all the "extra" header values to be sent
        for header_name, header_value in self.response_headers_map.items():
            # writes the extra header value in the result
            result.write(header_name + ": " + header_value + "\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write("\r\n")
        result.write(message)

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def get_service_handler(self):
        """
        Retrieves the service handler.

        @rtype: ServiceHandler
        @return: The service handler.
        """

        return self.service_handler

    def get_service_connection(self):
        """
        Retrieves the service connection.

        @rtype: ServiceConnection
        @return: The service connection.
        """

        return self.service_connection

    def set_operation_id(self, operation_id):
        """
        Sets the operation id.

        @type opration_id: String
        @param opration_id: The operation id.
        """

        self.operation_id = operation_id

    def get_operation_type(self):
        """
        Retrieves the operation type.

        @rtype: String
        @return: The operation type.
        """

        return self.operation_type

    def set_operation_type(self, operation_type):
        """
        Sets the operation type.

        @type opration_type: String
        @param opration_type: The operation type.
        """

        self.operation_type = operation_type

    def get_target(self):
        """
        Retrieves the target.

        @rtype: String
        @return: The target.
        """

        return self.target

    def set_target(self, target):
        """
        Sets the target.

        @type target: String
        @param target: The target.
        """

        self.target = target

    def set_protocol_version(self, protocol_version):
        """
        Sets the protocol version.

        @type protocol_version: String
        @param protocol_version: The protocol version.
        """

        self.protocol_version = protocol_version

    def get_status_code_value(self):
        """
        Retrieves the current status code value.
        The method returns the defined status code value,
        or the default in case none is defined.

        @rtype: String
        @return: The status code value.
        """

        # in case a status message is defined
        if self.status_message:
            # sets the defined status message as the
            # status code value
            status_code_value = self.status_message
        else:
            # retrieves the value for the status code
            status_code_value = STATUS_CODE_VALUES.get(self.status_code, DEFAULT_STATUS_CODE_VALUE)

        # returns the status code value
        return status_code_value
