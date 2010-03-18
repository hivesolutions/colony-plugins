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
import time
import types
import socket
import select
import datetime
import threading
import traceback

import string_buffer_util

import main_service_http_exceptions

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post mehtod value """

MULTIPART_FORM_DATA_VALUE = "multipart/form-data"
""" The multipart form data value """

HOST_VALUE = ""
""" The host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 3
""" The request timeout """

CHUNK_SIZE = 4096
""" The chunk size """

SERVER_NAME = "Hive-Colony-Web"
""" The server name """

SERVER_VERSION = "1.0.0"
""" The server version """

ENVIRONMENT_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
""" The environment version """

SERVER_IDENTIFIER = SERVER_NAME + "/" + SERVER_VERSION + " (Python/" + sys.platform + "/" + ENVIRONMENT_VERSION + ")"
""" The server identifier """

NUMBER_THREADS = 15
""" The number of threads """

MAX_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

DEFAULT_PORT = 8080
""" The default port """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_VALUE = "default"
""" The default value """

STATUS_CODE_VALUES = {100 : "Continue", 101 : "Switching Protocols",
                      200 : "OK", 207 : "Multi-Status",
                      301 : "Moved permanently", 302 : "Found", 303 : "See Other", 304 : "Not Modified",
                      305 : "Use Proxy", 306 : "(Unused)", 307 : "Temporary Redirect",
                      403 : "Forbidden", 404 : "Not Found",
                      500 : "Internal Server Error"}
""" The status code values map """

DEFAULT_STATUS_CODE_VALUE = "Invalid"
""" The default status code value """

DATE_VALUE = "Date"
""" The date value """

ETAG_VALUE = "ETag"
""" The etag value """

EXPIRES_VALUE = "Expires"
""" The expires value """

LAST_MODIFIED_VALUE = "Last-Modified"
""" The last modified value """

CONTENT_TYPE_VALUE = "Content-Type"
""" The content type value """

CONTENT_ENCODING_VALUE = "Content-Encoding"
""" The content encoding value """

TRANSFER_ENCODING_VALUE = "Transfer-Encoding"
""" The transfer encoding value """

CONTENT_LENGTH_VALUE = "Content-Length"
""" The content length value """

CONTENT_LENGTH_LOWER_VALUE = "Content-length"
""" The content length lower value """

UPGRADE_VALUE = "Upgrade"
""" The upgrade value """

SERVER_VALUE = "Server"
""" The server value """

CONNECTION_VALUE = "Connection"
""" The connection value """

IF_MODIFIED_SINCE_VALUE = "If-Modified-Since"
""" The if modified since value """

IF_NONE_MATCH_VALUE = "If-None-Match"
""" The if none match value """

CHUNKED_VALUE = "chunked"
""" The chunked value """

KEEP_ALIVE_VALUE = "Keep-Alive"
""" The keep alive value """

CACHE_CONTROL_VALUE = "Cache-Control"
""" The cache control value """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

DEFAULT_CONTENT_TYPE_CHARSET_VALUE = "default_content_type_charset"
""" The default content type charset value """

DEFAULT_CACHE_CONTROL_VALUE = "no-cache, must-revalidate"
""" The default cache control value """

class MainServiceHttp:
    """
    The main service http class.
    """

    main_service_http_plugin = None
    """ The main service http plugin """

    http_service_handler_plugins_map = {}
    """ The http service handler plugin map """

    http_socket = None
    """ The http socket """

    http_connection_active = False
    """ The http connection active flag """

    http_client_thread_pool = None
    """ The http client thread pool """

    http_connection_close_event = None
    """ The http connection close event """

    http_connection_close_end_event = None
    """ The http connection close end event """

    def __init__(self, main_service_http_plugin):
        """
        Constructor of the class.

        @type main_service_http_plugin: MainServiceHttpPlugin
        @param main_service_http_plugin: The main service http plugin.
        """

        self.main_service_http_plugin = main_service_http_plugin

        self.http_service_handler_plugin_map = {}
        self.http_connection_close_event = threading.Event()
        self.http_connection_close_end_event = threading.Event()

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

        # retrieves the encoding value
        encoding = parameters.get("encoding", None)

        # retrieves the service configuration property
        service_configuration_property = self.main_service_http_plugin.get_configuration_property("server_configuration")

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

        # retrieves the encoding configuration value
        encoding = service_configuration.get("default_encoding", encoding)

        # start the server for the given socket provider, port and encoding
        self.start_server(socket_provider, port, encoding, service_configuration)

        # clears the http connection close event
        self.http_connection_close_event.clear()

        # sets the http connection close end event
        self.http_connection_close_end_event.set()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        self.stop_server()

    def start_server(self, socket_provider, port, encoding, service_configuration):
        """
        Starts the server in the given port.

        @type socket_provider: String
        @param socket_provider: The name of the socket provider to be used.
        @type port: int
        @param port: The port to start the server.
        @type encoding: String
        @param encoding: The encoding to be used in the connection.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        """

        # retrieves the thread pool manager plugin
        thread_pool_manager_plugin = self.main_service_http_plugin.thread_pool_manager_plugin

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates the http client thread pool
        self.http_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool("http pool",
                                                                                         "pool to support http client connections",
                                                                                         NUMBER_THREADS, SCHEDULING_ALGORITHM, MAX_NUMBER_THREADS)

        # starts the http client thread pool
        self.http_client_thread_pool.start_pool()

        # sets the http connection active flag as true
        self.http_connection_active = True

        # sets the encoding handler as null
        encoding_handler = None

        # in case the encoding is defined
        if encoding:
            # retrieves the http service encoding plugins
            http_service_encoding_plugins = self.main_service_http_plugin.http_service_encoding_plugins

            # iterates over all the http service encoding plugins
            for http_service_encoding_plugin in http_service_encoding_plugins:
                # retrieves the encoding name from the http service encoding plugin
                http_service_encoding_plugin_encoding_name = http_service_encoding_plugin.get_encoding_name()

                # in case the names are the same
                if http_service_encoding_plugin_encoding_name == encoding:
                    encoding_handler = http_service_encoding_plugin.encode_contents
                    break

            # in case there is no encoding handler found
            if not encoding_handler:
                raise main_service_http_exceptions.EncodingNotFound("encoding %s not found" % encoding)

        # in case the socket provider is defined
        if socket_provider:
            # retrieves the socket provider plugins
            socket_provider_plugins = self.main_service_http_plugin.socket_provider_plugins

            # iterates over all the socket provider plugins
            for socket_provider_plugin in socket_provider_plugins:
                # retrieves the provider name from the socket provider plugin
                socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

                # in case the names are the same
                if socket_provider_plugin_provider_name == socket_provider:
                    # creates a new http socket with the socket provider plugin
                    self.http_socket = socket_provider_plugin.provide_socket()

            # in case the socket was not created, no socket provider found
            if not self.http_socket:
                raise main_service_http_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
        else:
            # creates the http socket
            self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # sets the socket to be able to reuse the socket
        self.http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the http socket
        self.http_socket.bind((HOST_VALUE, port))

        # start listening in the http socket
        self.http_socket.listen(5)

        # loops while the http connection is active
        while not self.http_connection_close_event.isSet():
            try:
                # sets the socket to non blocking mode
                self.http_socket.setblocking(0)

                # starts the select values
                selected_values = ([], [], [])

                # iterates while there is no selected values
                while selected_values == ([], [], []):
                    # in case the connection is closed
                    if self.http_connection_close_event.isSet():
                        # closes the http socket
                        self.http_socket.close()

                        return

                    # selects the values
                    selected_values = select.select([self.http_socket], [], [], CLIENT_CONNECTION_TIMEOUT)

                # sets the socket to blocking mode
                self.http_socket.setblocking(1)
            except:
                # prints info message about connection
                self.main_service_http_plugin.info("The socket is not valid for selection of the pool")

                return

            # in case the connection is closed
            if self.http_connection_close_event.isSet():
                # closes the http socket
                self.http_socket.close()

                return

            try:
                # accepts the connection retrieving the http connection object and the address
                http_connection, http_address = self.http_socket.accept()

                # creates a new http client service task, with the given http connection, address, encoding and encoding handler
                http_client_service_task = HttpClientServiceTask(self.main_service_http_plugin, http_connection, http_address, port, encoding, service_configuration, encoding_handler)

                # creates a new task descriptor
                task_descriptor = task_descriptor_class(start_method = http_client_service_task.start,
                                                        stop_method = http_client_service_task.stop,
                                                        pause_method = http_client_service_task.pause,
                                                        resume_method = http_client_service_task.resume)

                # inserts the new task descriptor into the http client thread pool
                self.http_client_thread_pool.insert_task(task_descriptor)

                # prints a debug message about the number of threads in pool
                self.main_service_http_plugin.debug("Number of threads in pool: %d" % self.http_client_thread_pool.current_number_threads)
            except Exception, exception:
                # prints an error message about the problem accepting the connection
                self.main_service_http_plugin.error("Error accepting connection: " + str(exception))

        # closes the http socket
        self.http_socket.close()

    def stop_server(self):
        """
        Stops the server.
        """

        # sets the http connection active flag as false
        self.http_connection_active = False

        # sets the http connection close event
        self.http_connection_close_event.set()

        # waits for the http connection close end event
        self.http_connection_close_end_event.wait()

        # clears the http connection close end event
        self.http_connection_close_end_event.clear()

        # stops all the pool tasks
        self.http_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.http_client_thread_pool.stop_pool()

    def http_service_handler_load(self, service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = service_handler_plugin.get_handler_name()

        self.http_service_handler_plugins_map[handler_name] = service_handler_plugin

    def http_service_handler_unload(self, service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = service_handler_plugin.get_handler_name()

        del self.http_service_handler_plugins_map[handler_name]

class HttpClientServiceTask:
    """
    The http client service task class.
    """

    main_service_http_plugin = None
    """ The main service http plugin """

    http_connection = None
    """ The http connection """

    http_address = None
    """ The http address """

    port = None
    """ The http address """

    encoding = None
    """ The encoding """

    service_configuration = None
    """ The service configuration """

    encoding_handler = None
    """ The encoding handler """

    current_request_handler = None
    """ The current request handler being used """

    content_type_charset = DEFAULT_CHARSET
    """ The content type charset """

    def __init__(self, main_service_http_plugin, http_connection, http_address, port, encoding, service_configuration, encoding_handler):
        self.main_service_http_plugin = main_service_http_plugin
        self.http_connection = http_connection
        self.http_address = http_address
        self.port = port
        self.encoding = encoding
        self.service_configuration = service_configuration
        self.encoding_handler = encoding_handler

        self.current_request_handler = self.http_request_handler

        if DEFAULT_CONTENT_TYPE_CHARSET_VALUE in service_configuration:
            # sets the content type charset to be used in the responses
            self.content_type_charset = self.service_configuration[DEFAULT_CONTENT_TYPE_CHARSET_VALUE]

    def start(self):
        # retrieves the http service handler plugins map
        http_service_handler_plugins_map = self.main_service_http_plugin.main_service_http.http_service_handler_plugins_map

        # prints debug message about connection
        self.main_service_http_plugin.debug("Connected to: %s" % str(self.http_address))

        # sets the request timeout
        request_timeout = REQUEST_TIMEOUT

        # iterates indefinitely
        while True:
            # handles the current request if it returns false
            # the connection was closed or is meant to be closed
            if not self.current_request_handler(request_timeout, http_service_handler_plugins_map):
                # breaks the cycle to close the http connection
                break

        # closes the http connection
        self.http_connection.close()

    def stop(self):
        # closes the http connection
        self.http_connection.close()

    def pause(self):
        pass

    def resume(self):
        pass

    def http_request_handler(self, request_timeout, http_service_handler_plugins_map):
        try:
            # retrieves the request
            request = self.retrieve_request(request_timeout)
        except main_service_http_exceptions.MainServiceHttpException:
            # prints a debug message about the connection closing
            self.main_service_http_plugin.debug("Connection: %s closed by peer or timeout" % str(self.http_address))

            # returns false (connection closed)
            return False

        try:
            # prints debug message about request
            self.main_service_http_plugin.debug("Handling request: %s" % str(request))

            # processes the redirection information in the request
            self._process_redirection(request)

            # processes the handler part of the request and retrieves
            # the handler name
            handler_name = self._process_handler(request)

            # in case the request was not already handled
            if not handler_name:
                # retrieves the default handler name
                handler_name = self.service_configuration.get("default_handler", None)

                # sets the handler path
                request.handler_path = None

            # in case no handler name is defined (request not handled)
            if not handler_name:
                # raises an http no handler exception
                raise main_service_http_exceptions.HttpNoHandlerException("no handler defined for current request")

            # handles the request by the request handler
            http_service_handler_plugins_map[handler_name].handle_request(request)

            # sends the request to the client (response)
            self.send_request(request)

            # in case the connection is meant to be kept alive
            if self.keep_alive(request):
                self.main_service_http_plugin.debug("Connection: %s kept alive for %ss" % (str(self.http_address), str(request_timeout)))
            # in case the connection is not meant to be kept alive
            else:
                self.main_service_http_plugin.debug("Connection: %s closed" % str(self.http_address))

                # returns false (connection closed)
                return False

        except Exception, exception:
            # prints info message about exception
            self.main_service_http_plugin.info("There was an exception handling the request: " + str(exception))

            # sends the exception
            self.send_exception(request, exception)

        # returns true (connection remains open)
        return True

    def retrieve_request(self, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: HttpRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = string_buffer_util.StringBuffer()

        # creates a request object
        request = HttpRequest(self, self.content_type_charset)

        # creates the start line loaded flag
        start_line_loaded = False

        # creates the header loaded flag
        header_loaded = False

        # creates the message loaded flag
        message_loaded = False

        # creates the message size value
        message_size = 0

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(request_timeout)

            # in case no valid data was received
            if data == "":
                # raises the http invalid data exception
                raise main_service_http_exceptions.HttpInvalidDataException("empty data received")

            # writes the data to the string buffer
            message.write(data)

            # retrieves the message value from the string buffer
            message_value = message.get_value()

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
                    if not start_line_splitted_length == 3:
                        # raises the http invalid data exception
                        raise main_service_http_exceptions.HttpInvalidDataException("invalid data received: " + start_line)

                    # retrieve the operation type the path and the protocol version
                    # from the start line splitted
                    operation_type, path, protocol_version = start_line_splitted

                    # sets the request  operation type
                    request.set_operation_type(operation_type)

                    # sets the request path
                    request.set_path(path)

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
                        request.headers_in[header_name] = header_value

                    # in case the operation type is get
                    if request.operation_type == GET_METHOD_VALUE:
                        # parses the get attributes
                        request.__parse_get_attributes__()

                        # returns the request
                        return request
                    # in case the operation type is post
                    elif request.operation_type == POST_METHOD_VALUE:
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

                # retrieves the message part of the message value
                message_value_message = message_value[start_message_index:]

                # in case the length of the message value message is the same
                # as the message size
                if len(message_value_message) == message_size:
                    # sets the message loaded flag
                    message_loaded = True

                    # sets the received message
                    request.received_message = message_value_message

                    # decodes the request if necessary
                    self.decode_request(request)

                    # returns the request
                    return request

    def decode_request(self, request):
        """
        Decodes the request message for the encoding
        specified in the request.

        @type request: HttpRequest
        @param request: The request to be decoded.
        """

        # start the valid charset flag
        valid_charset = False

        # in case the content type is defined
        if CONTENT_TYPE_VALUE in request.headers_map:
            # retrieves the content type
            content_type = request.headers_map[CONTENT_TYPE_VALUE]

            # splits the content type
            content_type_splited = content_type.split(";")

            # iterates over all the items in the content type splited
            for content_type_item in content_type_splited:
                # strips the content type item
                content_type_item_stripped = content_type_item.strip()

                # in case the content is of type multipart form data
                if content_type_item_stripped.startswith(MULTIPART_FORM_DATA_VALUE):
                    return

                # in case the item is the charset definition
                if content_type_item_stripped.startswith("charset"):
                    # splits the content type item stripped
                    content_type_item_stripped_splited = content_type_item_stripped.split("=")

                    # retrieves the content type charset
                    content_type_charset = content_type_item_stripped_splited[1].lower()

                    # sets the valid charset flag
                    valid_charset = True

                    # breaks the cycle
                    break

        # in case there is no valid charset defined
        if not valid_charset:
            # sets the default content type charset
            content_type_charset = DEFAULT_CHARSET

        # retrieves the received message value
        received_message_value = request.received_message

        # decodes the message value into unicode using the given charset
        request.received_message = received_message_value.decode(content_type_charset)

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.http_connection.setblocking(0)

            # runs the select in the http connection, with timeout
            selected_values = select.select([self.http_connection], [], [], request_timeout)

            # sets the connection to blocking mode
            self.http_connection.setblocking(1)
        except:
            raise main_service_http_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
            self.http_connection.close()
            raise main_service_http_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.http_connection.recv(chunk_size)
        except:
            raise main_service_http_exceptions.ClientRequestTimeout("timeout")

        return data

    def send_exception(self, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type request: HttpRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # retrieves the preferred error handlers list
        preferred_error_handlers_list = self.service_configuration.get("preferred_error_handlers", (DEFAULT_VALUE,))

        # retrieves the http service error handler plugins
        http_service_error_handler_plugins = self.main_service_http_plugin.http_service_error_handler_plugins

        # iterates over all the preferred error handlers
        for preferred_error_handler in preferred_error_handlers_list:
            # in case the preferred error handler is the default one
            if preferred_error_handler == DEFAULT_VALUE:
                # handles the error with the default error handler
                self.default_error_handler(request, exception)

                # breaks the loop
                break
            else:
                # unsets the valid flag
                valid = False

                # iterates over all the http service error handler plugins
                for http_service_error_handler_plugin in http_service_error_handler_plugins:
                    # retrieves the http service error handler plugin error handler name
                    http_service_error_handler_plugin_error_handler_name = http_service_error_handler_plugin.get_error_handler_name()

                    # checks if the plugin is the same as the preferred error handler
                    if http_service_error_handler_plugin_error_handler_name == preferred_error_handler:
                        # calls the handle error in the http service error handler plugin
                        http_service_error_handler_plugin.handle_error(request, exception)

                        # sets the valid flag
                        valid = True

                        # breaks the loop
                        break

                # in case the valid flag is set
                if valid:
                    # breaks the loop
                    break

        # sends the request to the client (response)
        self.send_request(request)

    def send_request(self, request):
        # in case the encoding is defined
        if self.encoding:
            # sets the encoded flag
            request.encoded = True

            # sets the encoding handler
            request.set_encoding_handler(self.encoding_handler)

            # sets the encoding name
            request.set_encoding_name(self.encoding)

        if request.is_mediated():
            self.send_request_mediated(request)
        elif request.is_chunked_encoded():
            self.send_request_chunked(request)
        else:
            self.send_request_simple(request)

    def send_request_simple(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.http_connection.send(result_value)
        except:
            # error in the client side
            self.main_service_http_plugin.error("Problem sending request simple")

            # returns immediately
            return

    def send_request_mediated(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.http_connection.send(result_value)
        except:
            # error in the client side
            self.main_service_http_plugin.error("Problem sending request mediated")

            # returns immediately
            return

        # continuous loop
        while True:
            # retrieves the mediated value
            mediated_value = request.mediated_handler.get_chunk(CHUNK_SIZE)

            # in case the read is complete
            if not mediated_value:
                # closes the mediated file
                request.mediated_handler.close_file()

                # returns immediately
                return

            try:
                # sends the mediated value to the client
                self.http_connection.send(mediated_value)
            except:
                # error in the client side
                self.main_service_http_plugin.error("Problem sending request mediated")

                # returns immediately
                return

    def send_request_chunked(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.http_connection.send(result_value)
        except:
            # error in the client side
            self.main_service_http_plugin.error("Problem sending request chunked")

            # returns immediately
            return

        # continuous loop
        while True:
            # retrieves the chunk value
            chunk_value = request.chunk_handler.get_chunk(CHUNK_SIZE)

            # in case the read is complete
            if not chunk_value:
                # sends the final empty chunk
                self.http_connection.send("0\r\n\r\n")

                # returns immediately
                return

            try:
                # retrieves the length of the chunk value
                length_chunk_value = len(chunk_value)

                # sets the value for the hexadecimal length part of the chunk
                length_chunk_value_hexadecimal_string = "%X\r\n" % length_chunk_value

                # sets the message value
                message_value = length_chunk_value_hexadecimal_string + chunk_value + "\r\n"

                # sends the message value to the client
                self.http_connection.send(message_value)
            except:
                # error in the client side
                self.main_service_http_plugin.error("Problem sending request chunked")

                # returns immediately
                return

    def keep_alive(self, request):
        """
        Retrieves the value of the keep alive for the given request.

        @type request: HttpRequest
        @param request: The request to retrieve the keep alive value.
        @rtype: bool
        @return: The value of the keep alive for the given request.
        """

        # in case connection is defined in the headers map
        if "Connection" in request.headers_map:
            # retrieves the connection type
            connection_type = request.headers_map["Connection"]

            # in case the connection is meant to be kept alive
            # or in case is of type upgrade
            if connection_type.lower() in ["keep-alive", "upgrade"]:
                # returns true
                return True
            else:
                # returns false
                return False
        # in case no connection header is defined
        else:
            # returns false
            return False

    def default_error_handler(self, request, error):
        """
        The default error handler for exception sending.

        @type request: HttpRequest
        @param request: The request to send the error.
        @type exception: Exception
        @param exception: The error to be sent.
        """

        # sets the request content type
        request.content_type = "text/plain"

        # checks if the error contains a status code
        if hasattr(error, "status_code"):
            # sets the status code in the request
            request.status_code = error.status_code
        # in case there is no status code defined in the error
        else:
            # sets the internal server error status code
            request.status_code = 500

        # retrieves the value for the status code
        status_code_value = self.get_status_code_value()

        # writes the header message in the message
        request.write("colony web server - " + str(request.status_code) + " " + status_code_value + "\n")

        # writes the error message
        request.write("error: '" + str(error) + "'\n")

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
            # writes the traceback line in the request
            request.write(formated_traceback_line)

    def get_current_request_handler(self):
        """
        Retrieves the current request handler.

        @rtype: Method
        @return: The current request handler.
        """

        return self.current_request_handler

    def set_current_request_handler(self, current_request_handler):
        """
        Sets the current request handler.

        @type current_request_handler: Method
        @param current_request_handler: The current request handler.
        """

        self.current_request_handler = current_request_handler

    def _process_redirection(self, request):
        """
        Processes the redirection stage of the http request.
        Processing redirection implies matching the path against the
        rules.

        @type request: HttpRequest
        @param request: The request to be processed.
        """

        # retrieves the service configuration redirections
        service_configuration_redirections = self.service_configuration.get("redirections", {})

        # retrieves the service configuration redirections resolution order
        service_configuration_redirections_resolution_order = service_configuration_redirections.get("resolution_order", service_configuration_redirections.keys())

        # iterates over the service configuration redirection names
        for service_configuration_redirection_name in service_configuration_redirections_resolution_order:
            # in case the path is found in the request path
            if request.path.find(service_configuration_redirection_name) == 0:
                # retrieves the service configuration redirection
                service_configuration_redirection = service_configuration_redirections[service_configuration_redirection_name]

                # retrieves the target path
                target_path = service_configuration_redirection.get("target", service_configuration_redirection_name)

                # retrieves the recursive redirection option
                recursive_redirection = service_configuration_redirection.get("recursive_redirection", False)

                # retrieves the sub request path as the request from the redirection name path
                # in front
                sub_request_path = request.path[len(service_configuration_redirection_name):]

                # in case the recursive redirection is disbaled and there is a subdirectory
                # in the sub request path
                if not recursive_redirection and not sub_request_path.find("/") == -1:
                    # breaks the loop because the request is not meant to be recursivly redirected
                    # and it contains a sub-directory
                    break

                # (saves) the old path as the base path
                request.base_path = request.path

                # retrieves the new (redirected) path in the request
                request_path = request.path.replace(service_configuration_redirection_name, target_path, 1)

                # sets the new path in the request
                request.set_path(request_path)

                # sets the redirection validation flag in the request
                request.redirection_validation = True

                # sets the redirected flag in the request
                request.redirected = True

                # breaks the loop
                break

    def _process_handler(self, request):
        """
        Processes the handler stage of the http request.
        Processing handler implies matching the path against the
        various handler rules defined to retrieve the valid handler.

        @type request: HttpRequest
        @param request: The request to be processed.
        """

        # sets the default handler name
        handler_name = None

        # retrieves the service configuration contexts
        service_configuration_contexts = self.service_configuration.get("contexts", {})

        # retrieves the service configuration contexts resolution order
        service_configuration_contexts_resolution_order = service_configuration_contexts.get("resolution_order", service_configuration_contexts.keys())

        # in case the request is pending redirection validation
        if request.redirection_validation:
            # the request base path is used as the reuqest path
            # for redirection allowing purposes
            request_path = request.base_path
        # in non redirection validation iteration case
        else:
            # sets the request path as the normal (valid) request
            # path
            request_path = request.path

        # iterates over the service configuration context names
        for service_configuration_context_name in service_configuration_contexts_resolution_order:
            # in case the path is found in the request path
            if request_path.find(service_configuration_context_name) == 0:
                # retrieves the service configuration context
                service_configuration_context = service_configuration_contexts[service_configuration_context_name]

                # retrieves the allow redirection property
                allow_redirection = service_configuration_context.get("allow_redirection", True)

                # in case the request is pending redirection validation
                if request.redirection_validation:
                    # in case it does not allow redirection
                    if not allow_redirection:
                        # changes the path to the base path
                        request.set_path(request.base_path)

                        # unsets the redirected flag in the request
                        request.redirected = False

                    # unsets the redirection validation flag in the request
                    request.redirection_validation = False

                    # re-processes the request (to process the real handler)
                    return self._process_handler(request)

                # sets the request properties
                request.properties = service_configuration_context.get("request_properties", {})

                # sets the handler path
                request.handler_path = service_configuration_context_name

                # retrieves the handler name
                handler_name = service_configuration_context.get("handler", None)

                # breaks the loop
                break

        # in case the request is pending redirection validation
        if request.redirection_validation:
            # unsets the redirection validation flag in the request
            request.redirection_validation = False

            # re-processes the request (to process the real handler)
            return self._process_handler(request)

        # returns the handler name
        return handler_name

class HttpRequest:
    """
    The http request class.
    """

    http_client_service_task = None
    """ The http client service task """

    operation_type = "none"
    """ The operation type """

    path = "none"
    """ The path """

    base_path = "none"
    """ The base path """

    resource_path = "none"
    """ The resource path """

    handler_path = "none"
    """ The handler path """

    filename = "none"
    """ The filename """

    uri = "none"
    """ The uri """

    arguments = "none"
    """ The arguments """

    multipart = "none"
    """ The multipart """

    protocol_version = "none"
    """ The protocol version """

    attributes_map = {}
    """ The attributes map """

    headers_map = {}
    """ The headers map """

    response_headers_map = {}
    """ The response headers map """

    headers_in = {}
    """ The headers in value (deprecated) """

    headers_out = {}
    """ The headers out value (deprecated) """

    received_message = "none"
    """ The received message """

    content_type = None
    """ The content type """

    message_stream = None
    """ The message stream """

    status_code = None
    """ The status code """

    status_message = None
    """ The status message """

    redirected = False
    """ The redirected flag """

    redirection_validation = False
    """ The redirection validation flag """

    mediated = False
    """ The mediated flag """

    mediated_handler = None
    """ The mediated handler """

    chunked_encoding = False
    """ The chunked encoding """

    encoded = False
    """ The encoded flag """

    encoding_handler = "none"
    """ The encoding type """

    encoding_type = "none"
    """ The encoding type """

    chunk_handler = None
    """ The chunk handler """

    upgrade_mode = None
    """ The upgrade mode mode """

    connection_mode = KEEP_ALIVE_VALUE
    """ The connection mode """

    content_type_charset = None
    """ The content type charset """

    etag = None
    """ The etag """

    expiration_timestamp = None
    """ The expiration timestatmp """

    last_modified_timestamp = None
    """ The last modified timestatmp """

    contains_message = True
    """ The contains message flag """

    request_time = None
    """ The time when the request started """

    properties = {}
    """ The properties """

    def __init__(self, http_client_service_task = None, content_type_charset = DEFAULT_CHARSET):
        self.http_client_service_task = http_client_service_task
        self.content_type_charset = content_type_charset

        self.request_time = time.time()

        self.attributes_map = {}
        self.headers_map = {}
        self.response_headers_map = {}
        self.message_stream = string_buffer_util.StringBuffer()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.operation_type, self.path)

    def __getattribute__(self, attribute_name):
        return self.attributes_map.get(attribute_name, None)

    def __setattribute__(self, attribute_name, attribute_value):
        self.attributes_map[attribute_name] = attribute_value

    def __parse_get_attributes__(self):
        # splits the path to get the attributes path of the request
        path_splitted = self.path.split("?")

        # retrieves the size of the split
        path_splitted_length = len(path_splitted)

        # in case there are no arguments to be parsed
        if path_splitted_length < 2:
            return

        # retrieves the arguments from the path splitted
        self.arguments = path_splitted[1]

        # parses the arguments
        self.parse_arguments()

    def parse_post_attributes(self):
        """
        Parses the post attributes from the standard post
        syntax.
        """

        # sets the arguments as the received message
        self.arguments = self.received_message

        # parses the arguments
        self.parse_arguments()

    def parse_post_multipart(self):
        """
        Parses the post multipart from the standard post
        syntax.
        """

        # sets the multipart as the received message
        self.multipart = self.received_message

        # parses the multipart
        self.parse_multipart()

    def parse_arguments(self):
        """
        Parses the arguments, using the currently defined
        arguments string (in the request).
        The parsing of the arguments is based in the default get
        arguments parsing.
        """

        # retrieves the attribute fields list
        attribute_fields_list = self.arguments.split("&")

        # iterates over all the attribute fields
        for attribute_field in attribute_fields_list:
            # splits the attribute field in the equals operator
            attribute_field_splitted = attribute_field.split("=")

            # retrieves the attribute field splitted length
            attribute_field_splitted_length = len(attribute_field_splitted)

            # in case the attribute field splitted length is invalid
            if attribute_field_splitted_length == 0 or attribute_field_splitted_length > 2:
                continue

            # in case the attribute field splitted length is two
            if attribute_field_splitted_length == 2:
                # retrieves the attribute name and the attribute value,
                # from the attribute field splitted
                attribute_name, attribute_value = attribute_field_splitted
            # in case the attribute field splitted length is one
            elif attribute_field_splitted_length == 1:
                # retrieves the attribute name, from the attribute field splitted
                attribute_name, = attribute_field_splitted

                # sets the attribute value to none
                attribute_value = None

            # sets the attribute value
            self.__setattribute__(attribute_name, attribute_value)

    def parse_multipart(self):
        # retrieves the content type header
        content_type = self.headers_map.get(CONTENT_TYPE_VALUE, None)

        if not content_type:
            raise Exception("invalid content type")

        # splits the content type
        content_type_splitted = content_type.split(";")

        content_type_value = content_type_splitted[0].strip()

        if not content_type_value == MULTIPART_FORM_DATA_VALUE:
            raise Exception("invalid content type")

        boundary = content_type_splitted[1].strip()

        _boundary, boundary_value = boundary.split("=")

        boundary_value_length = len(boundary_value)

        current_index = boundary_value_length + 2

        while 1:
            end_index = self.multipart.find(boundary_value, current_index)

            # in case the end index is invalid
            if end_index == -1:
                break

            headers_map, contents = self._parse_multipart_part(current_index + 2, end_index - 2)

            content_disposition = headers_map.get("Content-Disposition", "")

            content_disposition_attributes = content_disposition.split(";")

            content_disposition_map = {}

            for content_disposition_attribute in content_disposition_attributes:
                content_disposition_attribute_stripped = content_disposition_attribute.strip()

                value_splitted = content_disposition_attribute_stripped.split("=")

                if len(value_splitted) == 2:
                    key, value = value_splitted

                    content_disposition_map[key] = value
                elif len(value_splitted) == 1:
                    key = value_splitted[0]

                    content_disposition_map[key] = None
                else:
                    raise Exception("invalid value")

            name = content_disposition_map["name"]

            name_stripped = name.strip("\"")

            self.__setattribute__(name_stripped, contents)

            # sets the current index as the end index
            current_index = end_index + boundary_value_length

    def _parse_multipart_part(self, start_index, end_index):
        # creates the headers map
        headers_map = {}

        # retrieves the end header index
        end_header_index = self.multipart.find("\r\n\r\n", start_index, end_index)

        # retrieves the headers from the multipart
        headers = self.multipart[start_index:end_header_index]

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
            headers_map[header_name] = header_value

        # retrieves the contents from the multipart
        contents = self.multipart[end_header_index + 4:end_index - 2]

        # returns the headers map and the contents as a tuple
        return (headers_map, contents)

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

    def is_mediated(self):
        return self.mediated

    def is_chunked_encoded(self):
        return self.chunked_encoding

    def get_header(self, header_name):
        """
        Retrieves an header value of the request,
        or none if no header is defined for the given
        header name.

        @type header_name: String
        @param header_name: The name of the header to be retrieved.
        @rtype: Object
        @return: The value of the request header.
        """

        return self.headers_map.get(header_name, None)

    def set_header(self, header_name, header_value):
        """
        Set a response header value on the request.

        @type header_name: String
        @param header_name: The name of the header to be set.
        @type header_value: Object
        @param header_value: The value of the header to be sent
        in the response.
        """

        self.response_headers_map[header_name] = header_value
        self.headers_out[header_name] = header_value

    def append_header(self, header_name, header_value):
        """
        Appends an header value to a response header.
        This method calls the set header method in case the
        header is not yet defined.

        @type header_name: String
        @param header_name: The name of the header to be appended with the value.
        @type header_value: Object
        @param header_value: The value of the header to be appended
        in the response.
        """

        # in case the header is already defined
        if header_name in self.response_headers_map:
            # retrieves the current header value
            current_header_value = self.response_headers_map[header_name]

            # creates the final header value as the appending of both the current
            # and the concatenation value
            final_header_value = current_header_value + header_value
        else:
            # sets the final header value as the header value
            final_header_value = header_value

        # sets the final header value
        self.set_header(header_name, final_header_value)

    def get_result(self):
        # retrieves the result stream
        result = string_buffer_util.StringBuffer()

        # retrieves the result string value
        message = self.message_stream.get_value()

        # in case the request is encoded
        if self.encoded:
            if self.mediated:
                self.mediated_handler.encode_file(self.encoding_handler, self.encoding_type)
            elif self.chunked_encoding:
                self.chunk_handler.encode_file(self.encoding_handler, self.encoding_type)
            else:
                message = self.encoding_handler(message)

        # in case the request is mediated
        if self.mediated:
            # retrieves the content length
            # from the mediated handler
            content_length = self.mediated_handler.get_size()
        else:
            # retrieves the content length from the
            # message content itself
            content_length = len(message)

        # retrieves the value for the status code
        status_code_value = self.get_status_code_value()

        # writes the http command in the string buffer (version, status code and status value)
        result.write(self.protocol_version + " " + str(self.status_code) + " " + status_code_value + "\r\n")

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time according to the http specification
        current_date_time_formatted = current_date_time.strftime(DATE_FORMAT)

        if self.content_type:
            result.write(CONTENT_TYPE_VALUE + ": " + self.content_type + "\r\n")
        if self.encoded:
            result.write(CONTENT_ENCODING_VALUE + ": " + self.encoding_name + "\r\n")
        if self.chunked_encoding:
            result.write(TRANSFER_ENCODING_VALUE + ": " + CHUNKED_VALUE + "\r\n")
        if not self.chunked_encoding and self.contains_message:
            result.write(CONTENT_LENGTH_VALUE + ": " + str(content_length) + "\r\n")
        if self.upgrade_mode:
            result.write(UPGRADE_VALUE + ": " + self.upgrade_mode + "\r\n")
        if self.etag:
            result.write(ETAG_VALUE + ": " + self.etag + "\r\n")
        if self.expiration_timestamp:
            # converts the expiration timestamp to date time
            expiration_date_time = datetime.datetime.fromtimestamp(self.expiration_timestamp)

            # formats the expiration date time according to the http specification
            expiration_date_time_formatted = expiration_date_time.strftime(DATE_FORMAT)

            result.write(EXPIRES_VALUE + ": " + expiration_date_time_formatted + "\r\n")
        if self.last_modified_timestamp:
            # converts the last modified timestamp to date time
            last_modified_date_time = datetime.datetime.fromtimestamp(self.last_modified_timestamp)

            # formats the last modified date time according to the http specification
            last_modified_date_time_formatted = last_modified_date_time.strftime(DATE_FORMAT)

            result.write(LAST_MODIFIED_VALUE + ": " + last_modified_date_time_formatted + "\r\n")
        result.write(CONNECTION_VALUE + ": " + self.connection_mode + "\r\n")
        result.write(DATE_VALUE + ": " + current_date_time_formatted + "\r\n")
        result.write(CACHE_CONTROL_VALUE + ": " + DEFAULT_CACHE_CONTROL_VALUE + "\r\n")
        result.write(SERVER_VALUE + ": " + SERVER_IDENTIFIER + "\r\n")

        # iterates over all the "extra" header values to be sent
        for header_name, header_value in self.response_headers_map.items():
            # writes the extra header value in the result
            result.write(header_name + ": " + header_value + "\r\n")

        result.write("\r\n")
        result.write(message)

        result_value = result.get_value()

        return result_value

    def get_attribute(self, attribute_name):
        return self.__getattribute__(attribute_name)

    def set_attribute(self, attribute_name, attribute_value):
        self.__setattribute__(attribute_name, attribute_value)

    def get_message(self):
        return self.message_stream.get_value()

    def set_message(self, message):
        self.message_stream = string_buffer_util.StringBuffer()
        self.message_stream.write(message)

    def set_encoding_handler(self, encoding_handler):
        self.encoding_handler = encoding_handler

    def get_encoding_handler(self):
        return self.encoding_handler

    def set_encoding_name(self, encoding_name):
        self.encoding_name = encoding_name

    def get_encoding_name(self):
        return self.encoding_name

    def set_operation_type(self, operation_type):
        self.operation_type = operation_type

    def set_path(self, path):
        # retrieves the resource path of the path
        resource_path = path.split("?")[0]

        self.path = path
        self.resource_path = resource_path
        self.filename = resource_path
        self.uri = resource_path

    def set_protocol_version(self, protocol_version):
        self.protocol_version = protocol_version

    def get_resource_path(self):
        """
        Retrieves the resource path.

        @rtype: String
        @return: The resource path.
        """

        return self.resource_path

    def get_handler_path(self):
        """
        Retrieves the handler path.

        @rtype: String
        @return: The handler path.
        """

        return self.handler_path

    def get_arguments(self):
        """
        Retrieves the arguments.

        @rtype: String
        @return: The arguments.
        """

        return self.arguments

    def get_upgrade_mode(self):
        return self.upgrade_mode

    def set_upgrade_mode(self, upgrade_mode):
        self.upgrade_mode = upgrade_mode

    def get_connection_mode(self):
        return self.connection_mode

    def set_connection_mode(self, connection_mode):
        self.connection_mode = connection_mode

    def get_content_type_charset(self):
        return self.content_type_charset

    def set_content_type_charset(self, content_type_charset):
        self.content_type_charset = content_type_charset

    def get_etag(self):
        return self.etag

    def set_etag(self, etag):
        self.etag = etag

    def get_expiration_timestamp(self):
        return self.expiration_timestamp

    def set_expiration_timestamp(self, expiration_timestamp):
        self.expiration_timestamp = expiration_timestamp

    def get_last_modified_timestamp(self):
        return self.last_modified_timestamp

    def set_last_modified_timestamp(self, last_modified_timestamp):
        self.last_modified_timestamp = last_modified_timestamp

    def get_contains_message(self):
        return self.contains_message

    def set_contains_message(self, contains_message):
        self.contains_message = contains_message

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

    def verify_resource_modification(self, modified_timestamp = None, etag_value = None):
        """
        Verifies the resource to check for any modification since the
        value defined in the http request.

        @type modified_timestamp: int
        @param modified_timestamp: The timestamp of the resource modification.
        @type etag_value: String
        @param etag_value: The etag value of the resource.
        @rtype: bool
        @return: The result of the resource modification test.
        """

        # retrieves the if modified header value
        if_modified_header = self.get_header(IF_MODIFIED_SINCE_VALUE)

        # in case the modified timestamp and if modified header are defined
        if modified_timestamp and if_modified_header:
            try:
                # converts the if modified header value to date time
                if_modified_header_data_time = datetime.datetime.strptime(if_modified_header, DATE_FORMAT)

                # converts the modified timestamp to date time
                modified_date_time = datetime.datetime.fromtimestamp(modified_timestamp)

                # in case the modified date time is less or the same
                # as the if modified header date time (no modification)
                if modified_date_time <= if_modified_header_data_time:
                    # returns false (not modified)
                    return False
            except:
                # prints a warning for not being able to check the modification date
                self.http_client_service_task.main_service_http_plugin.warn("Problem while checking modification date")

        # retrieves the if none match value
        if_none_match_header = self.get_header(IF_NONE_MATCH_VALUE)

        # in case the etag value and the if none header are defined
        if etag_value and if_none_match_header:
            # in case the value of the if modified header is the same
            # as the etag value of the file (no modification)
            if if_modified_header == etag_value:
                # returns false (not modified)
                return False

        # returns false (modified or no information for
        # modification test)
        return True
