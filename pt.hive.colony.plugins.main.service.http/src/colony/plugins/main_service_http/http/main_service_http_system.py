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
import traceback

import cStringIO

import main_service_http_exceptions

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post mehtod value """

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

NUMBER_THREADS = 15
""" The number of threads """

MAX_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

STATUS_CODE_VALUES = {200 : "OK", 207 : "Multi-Status",
                      301 : "Moved permanently", 302 : "Found", 303 : "See Other",
                      403 : "Forbidden", 404 : "Not Found",
                      500 : "Internal Server Error"}
""" The status code values map """

class MainServiceHttp:
    """
    The main service http class.
    """

    main_service_http_plugin = None
    """ The main service http plugin """

    http_socket = None
    """ The http socket """

    http_connection_active = False
    """ The http connection active flag """

    def __init__(self, main_service_http_plugin):
        """
        Constructor of the class.

        @type main_service_http_plugin: MainServiceHttpPlugin
        @param main_service_http_plugin: The main service http plugin.
        """

        self.main_service_http_plugin = main_service_http_plugin

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the port value
        port = parameters["port"]

        # start the server for the given port
        self.start_server(port)

    def stop_service(self):
        """
        Stops the service.
        """

        self.stop_server()

    def start_server(self, port):
        """
        Starts the server in the given port.

        @type port: int
        @param port: The port to start the server.
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

        # creates the http socket
        self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # binds the http socket
        self.http_socket.bind((HOST_VALUE, port))

        # loops while the http connection is active
        while self.http_connection_active:
            # start listening in the http socket
            self.http_socket.listen(5)

            # starts the select values
            selected_values = ([], [], [])

            # iterates while there is no selected values
            while selected_values == ([], [], []):
                # in case the connection is disabled
                if not self.http_connection_active:
                    return
                try:
                    # selects the values
                    selected_values = select.select([self.http_socket], [], [], CLIENT_CONNECTION_TIMEOUT)
                except:
                    # prints debug message about connection
                    self.main_service_http_plugin.error("An error has occurred in the selection of the pool")
                    return

            # in case the connection is disabled
            if not self.http_connection_active:
                return

            # accepts the connection retrieving the http connection object and the address
            http_connection, http_address = self.http_socket.accept()

            # creates a new http client service task, with the given http connection and address
            http_client_service_task = HttpClientServiceTask(self.main_service_http_plugin, http_connection, http_address)

            # creates a new task descriptor
            task_descriptor = task_descriptor_class(start_method = http_client_service_task.start,
                                                    stop_method = http_client_service_task.stop,
                                                    pause_method = http_client_service_task.pause,
                                                    resume_method = http_client_service_task.resume)

            # inserts the new task descriptor into the http client thread pool
            self.http_client_thread_pool.insert_task(task_descriptor)

            self.main_service_http_plugin.debug("Number of threads in pool: %d" % self.http_client_thread_pool.current_number_threads)

    def stop_server(self):
        """
        Stops the server.
        """

        # sets the http connection active flag as false
        self.http_connection_active = False

        # closes the http socket
        self.http_socket.close()

        # stops all the pool tasks
        self.http_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.http_client_thread_pool.stop_pool()

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

    def __init__(self, main_service_http_plugin, http_connection, http_address):
        self.main_service_http_plugin = main_service_http_plugin
        self.http_connection = http_connection
        self.http_address = http_address

    def start(self):
        # retrieves the http service handler plugins
        http_service_handler_plugins = self.main_service_http_plugin.http_service_handler_plugins

        # prints debug message about connection
        self.main_service_http_plugin.debug("Connected to: %s" % str(self.http_address))

        # sets the request timeout
        request_timeout = REQUEST_TIMEOUT

        while True:
            try:
                request = self.retrieve_request(request_timeout)
            except main_service_http_exceptions.MainServiceHttpException:
                self.main_service_http_plugin.debug("Connection: %s closed" % str(self.http_address))
                return

            try:
                # prints debug message about request
                self.main_service_http_plugin.debug("Handling request: %s" % str(request))

                if request.path.find("/hive/plugins") == 0:
                    # sets the plugin handler that will handle the request
                    request.properties["plugin_handler"] = "pt.hive.colony.plugins.javascript.file_handler"

                    # handles the request
                    http_service_handler_plugins[0].handle_request(request)
                elif request.path.find("/colony_manager") == 0:
                    # handles the request
                    http_service_handler_plugins[0].handle_request(request)
                elif request.path.find("/colony_mod_python") == 0:
                    # handles the request
                    http_service_handler_plugins[0].handle_request(request)
                else:
                    # handles the request
                    http_service_handler_plugins[1].handle_request(request)

                # sends the request to the client (response)
                self.send_request(request)

                # in case the connection is meant to be kept alive
                if self.keep_alive(request):
                    self.main_service_http_plugin.debug("Connection: %s kept alive for %ss" % (str(self.http_address), str(request_timeout)))
                # in case the connection is not meant to be kept alive
                else:
                    self.main_service_http_plugin.debug("Connection: %s closed" % str(self.http_address))
                    break

            except Exception, exception:
                self.send_exception(request, exception)

        # closes the http connection
        self.http_connection.close()

    def stop(self):
        # closes the http connection
        self.http_connection.close()

    def pause(self):
        pass

    def resume(self):
        pass

    def retrieve_request(self, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: HttpRequest
        @return: The request from the received message.
        """

        # creates the string io for the message
        message = cStringIO.StringIO()

        # creates a request object
        request = HttpRequest()

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
                raise main_service_http_exceptions.HttpInvalidDataException("empty data received")

            # writes the data to the string io
            message.write(data)

            # retrieves the message value from the string io
            message_value = message.getvalue()

            # in case the start line is not loaded
            if not start_line_loaded:
                # finds the first new line value
                start_line_index = message_value.find("\r\n")

                # in case there is a new line value found
                if not start_line_index == -1:
                    # retrieves the start line
                    start_line = message_value[:start_line_index]

                    # splits the start line to retrieve the operation type the path
                    # and the protocol version
                    operation_type, path, protocol_version = start_line.split(" ")

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

                    # in case the operation type is get
                    if request.operation_type == GET_METHOD_VALUE:
                        # parses the get attributes
                        request.__parse_get_attributes__()

                        # returns the request
                        return request
                    # in case the operation type is post
                    elif request.operation_type == POST_METHOD_VALUE:
                        # in case the content length is defined in the headers map
                        if "Content-Length" in request.headers_map:
                            # retrieves the message size
                            message_size = int(request.headers_map["Content-Length"])
                        elif "Content-length" in request.headers_map:
                            # retrieves the message size
                            message_size = int(request.headers_map["Content-length"])
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

                    # returns the request
                    return request

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # runs the select in the http connection, with timeout
            selected_values = select.select([self.http_connection], [], [], request_timeout)
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

        # sets the request content type
        request.content_type = "text/plain"

        # checks if the exception contains a status code
        if hasattr(exception, "status_code"):
            # sets the status code in the request
            request.status_code = exception.status_code
        # in case there is no status code defined in the exception
        else:
            # sets the internal server error status code
            request.status_code = 500

        if not request.status_code:
            request.status_code = 500

        # retrieves the value for the status code
        status_code_value = STATUS_CODE_VALUES[request.status_code]

        # writes the header message in the message
        request.write("colony web server - " + str(request.status_code) + " " + status_code_value + "\n")

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
            return

    def send_request_mediated(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.http_connection.send(result_value)
        except:
            # error in the client side
            return

        # continuous loop
        while True:
            # retrieves the mediated value
            mediated_value = request.mediated_handler.get_chunk(CHUNK_SIZE)

            # in case the read is complete
            if not mediated_value:
                # closes the mediated file
                request.mediated_handler.close_file()
                return

            try:
                # sends the mediated value to the client
                self.http_connection.send(mediated_value)
            except:
                # error in the client side
                return

    def send_request_chunked(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.http_connection.send(result_value)
        except:
            # error in the client side
            return

        # continuous loop
        while True:
            # retrieves the chunk value
            chunk_value = request.chunk_handler.get_chunk(CHUNK_SIZE)

            # in case the read is complete
            if not chunk_value:
                return

            try:
                # sends the chunk value to the client
                self.http_connection.send(chunk_value)
            except:
                # error in the client side
                return

    def keep_alive(self, request):
        """
        Retrieves the value of the keep alive for the given request.

        @type request: HttpRequest
        @param request: The request to retrieve the keep alive value.
        @rtype: bool
        @return: The value of the keep alive for the given request.
        """

        if "Connection" in request.headers_map:
            connection_type = request.headers_map["Connection"]

            if connection_type.lower() == "keep-alive":
                return True
            else:
                return False
        else:
            return False

class HttpRequest:
    """
    The http request class.
    """

    operation_type = "none"
    """ The operation type """

    path = "none"
    """ The path """

    resource_path = "none"
    """ The resource path """

    protocol_version = "none"
    """ The protocol version """

    attributes_map = {}
    """ The attributes map """

    headers_map = {}
    """ The headers map """

    received_message = "none"
    """ The received message """

    content_type = "none"
    """ The content type """

    message_stream = cStringIO.StringIO()
    """ The message stream """

    status_code = None
    """ The status code """

    mediated = False
    """ The mediated flag """

    mediated_handler = None
    """ The mediated handler """

    chunked_encoding = False
    """ The chunked encoding """

    chunk_handler = None
    """ The chunk handler """

    properties = {}
    """ The properties """

    def __init__(self):
        self.attributes_map = {}
        self.headers_map = {}
        self.message_stream = cStringIO.StringIO()
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

        # in case there are arguments to be parsed
        if path_splitted_length < 2:
            return

        # retrieves the attribute fields list
        attribute_fields_list = path_splitted[1].split("&")

        # iterates over all the attribute fields
        for attribute_field in attribute_fields_list:
            # retrieves the attribute name and the attribute value,
            # splitting the string in the equals operator
            attribute_name, attribute_value = attribute_field.split("=")

            # sets the attribute value
            self.__setattribute__(attribute_name, attribute_value)

    def read(self):
        return self.received_message

    def write(self, message):
        self.message_stream.write(message)

    def flush(self):
        pass

    def is_mediated(self):
        return self.mediated

    def is_chunked_encoded(self):
        return self.chunked_encoding

    def get_result(self):
        result = cStringIO.StringIO()
        message = self.message_stream.getvalue()

        if self.mediated:
            content_length = self.mediated_handler.get_size()
        else:
            content_length = len(message)

        if not request.status_code:
            request.status_code = 500

        status_code_value = STATUS_CODE_VALUES[self.status_code]

        result.write(self.protocol_version + " " + str(self.status_code) + " " + status_code_value + "\r\n")
        if self.content_type:
            result.write("Content-Type: " + self.content_type + "\r\n")
        if self.chunked_encoding:
            result.write("Transfer-Encoding: chunked\r\n")
        if not self.chunked_encoding:
            result.write("Content-Length: " + str(content_length) + "\r\n")
        result.write("Server: " + SERVER_NAME + "/" + SERVER_VERSION + "\r\n")
        result.write("Connection: Keep-Alive" + "\r\n")
        result.write("\r\n")
        result.write(message)

        result_value = result.getvalue()

        return result_value

    def get_attribute(self, attribute_name):
        return self.__getattribute__(attribute_name)

    def set_attribute(self, attribute_name, attribute_value):
        self.__setattribute__(attribute_name, attribute_value)

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
        return self.resource_path
