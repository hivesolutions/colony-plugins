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
import struct
import select
import threading

import colony.libs.string_buffer_util

import main_service_dns_exceptions

BIND_HOST_VALUE = ""
""" The bind host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 10
""" The request timeout """

MESSAGE_MAXIMUM_SIZE = 512
""" The message maximum size """

NUMBER_THREADS = 15
""" The number of threads """

MAX_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

DEFAULT_PORT = 53
""" The default port """

MESSAGE_HEADER_SIZE = 12
""" The size of the dns message header (in bytes) """

TYPES_MAP = {"A" : 0x01, "NS" : 0x02, "MD" : 0x03, "MF" : 0x04, "CNAME" : 0x05,
             "SOA" : 0x06, "MB" : 0x07, "MG" : 0x08, "MR" : 0x09, "NULL" : 0x0a,
             "WKS" : 0x0b, "PTR" : 0x0c, "HINFO" : 0x0d, "MINFO" : 0x0e, "MX" : 0x0f,
             "TXT" : 0x10}
""" The map associating the type string with the integer value """

TYPES_REVERSE_MAP = {0x01 : "A", 0x02 : "NS", 0x03 : "MD", 0x04 : "MF", 0x05 : "CNAME",
                     0x06 : "SOA", 0x07 : "MB", 0x08 : "MG", 0x09 : "MR", 0x0a : "NULL",
                     0x0b : "WKS", 0x0c : "PTR", 0x0d : "HINFO", 0x0e : "MINFO", 0x0f : "MX",
                     0x10 : "TXT"}
""" The map associating the type integer with the string value """

CLASSES_MAP = {"IN" : 0x01, "CS" : 0x02, "CH" : 0x03, "HS" : 0x04}
""" The map associating the class string with the integer value """

CLASSES_REVERSE_MAP = {0x01 : "IN", 0x02 : "CS", 0x03 : "CH", 0x04 : "HS"}
""" The map associating the class integer with the string value """

class MainServiceDns:
    """
    The main service dns class.
    """

    main_service_dns_plugin = None
    """ The main service dns plugin """

    dns_service_handler_plugins_map = {}
    """ The dns service handler plugin map """

    dns_socket = None
    """ The dns socket """

    dns_connection_active = False
    """ The dns connection active flag """

    dns_client_thread_pool = None
    """ The dns client thread pool """

    dns_connection_close_event = None
    """ The dns connection close event """

    dns_connection_close_end_event = None
    """ The dns connection close end event """

    def __init__(self, main_service_dns_plugin):
        """
        Constructor of the class.

        @type main_service_dns_plugin: MainServiceDnsPlugin
        @param main_service_dns_plugin: The main service dns plugin.
        """

        self.main_service_dns_plugin = main_service_dns_plugin

        self.dns_service_handler_plugin_map = {}
        self.dns_connection_close_event = threading.Event()
        self.dns_connection_close_end_event = threading.Event()

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
        service_configuration_property = self.main_service_dns_plugin.get_configuration_property("server_configuration")

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

        # clears the dns connection close event
        self.dns_connection_close_event.clear()

        # sets the dns connection close end event
        self.dns_connection_close_end_event.set()

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
        thread_pool_manager_plugin = self.main_service_dns_plugin.thread_pool_manager_plugin

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates the dns client thread pool
        self.dns_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool("dns pool",
                                                                                         "pool to support dns client connections",
                                                                                         NUMBER_THREADS, SCHEDULING_ALGORITHM, MAX_NUMBER_THREADS)

        # starts the dns client thread pool
        self.dns_client_thread_pool.start_pool()

        # sets the dns connection active flag as true
        self.dns_connection_active = True

        # in case the socket provider is defined
        if socket_provider:
            # retrieves the socket provider plugins
            socket_provider_plugins = self.main_service_dns_plugin.socket_provider_plugins

            # iterates over all the socket provider plugins
            for socket_provider_plugin in socket_provider_plugins:
                # retrieves the provider name from the socket provider plugin
                socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

                # in case the names are the same
                if socket_provider_plugin_provider_name == socket_provider:
                    # creates a new dns socket with the socket provider plugin
                    self.dns_socket = socket_provider_plugin.provide_socket()

            # in case the socket was not created, no socket provider found
            if not self.dns_socket:
                raise main_service_dns_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
        else:
            # creates the dns socket
            self.dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        # sets the socket to be able to reuse the socket
        self.dns_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the dns socket
        self.dns_socket.bind((BIND_HOST_VALUE, port))

        # loops while the dns connection is active
        while not self.dns_connection_close_event.isSet():
            # receives the dns data from the socket
            data, address = self.dns_socket.recvfrom(512)

            # creates a new dns request
            request = DnsRequest({})

            # processes the request
            request.process_data(data, address)

            # !!! the dummy answer tuple !!!
            answer = ("www.google.com", "A", "IN", 20000, "192.168.1.1")

            # adds a new answer to the request
            request.answers.append(answer)

            # retrieves the result from the request
            result = request.get_result()

            # sends the result to the dns socket
            self.dns_socket.sendto(result, address)

        # closes the dns socket
        self.dns_socket.close()

    def stop_server(self):
        """
        Stops the server.
        """

        # sets the dns connection active flag as false
        self.dns_connection_active = False

        # sets the dns connection close event
        self.dns_connection_close_event.set()

        # waits for the dns connection close end event
        self.dns_connection_close_end_event.wait()

        # clears the dns connection close end event
        self.dns_connection_close_end_event.clear()

        # stops all the pool tasks
        self.dns_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.dns_client_thread_pool.stop_pool()

    def dns_service_handler_load(self, dns_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = dns_service_handler_plugin.get_handler_name()

        self.dns_service_handler_plugins_map[handler_name] = dns_service_handler_plugin

    def dns_service_handler_unload(self, dns_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = dns_service_handler_plugin.get_handler_name()

        del self.dns_service_handler_plugins_map[handler_name]

#class DnsClientServiceTask:
#    """
#    The dns client service task class.
#    """
#
#    main_service_dns_plugin = None
#    """ The main service dns plugin """
#
#    dns_connection = None
#    """ The dns connection """
#
#    dns_address = None
#    """ The dns address """
#
#    port = None
#    """ The dns address """
#
#    encoding = None
#    """ The encoding """
#
#    service_configuration = None
#    """ The service configuration """
#
#    encoding_handler = None
#    """ The encoding handler """
#
#    current_request_handler = None
#    """ The current request handler being used """
#
#    content_type_charset = DEFAULT_CHARSET
#    """ The content type charset """
#
#    def __init__(self, main_service_dns_plugin, dns_connection, dns_address, port, encoding, service_configuration, encoding_handler):
#        self.main_service_dns_plugin = main_service_dns_plugin
#        self.dns_connection = dns_connection
#        self.dns_address = dns_address
#        self.port = port
#        self.encoding = encoding
#        self.service_configuration = service_configuration
#        self.encoding_handler = encoding_handler
#
#        self.current_request_handler = self.dns_request_handler
#
#        if DEFAULT_CONTENT_TYPE_CHARSET_VALUE in service_configuration:
#            # sets the content type charset to be used in the responses
#            self.content_type_charset = self.service_configuration[DEFAULT_CONTENT_TYPE_CHARSET_VALUE]
#
#    def start(self):
#        # retrieves the dns service handler plugins map
#        dns_service_handler_plugins_map = self.main_service_dns_plugin.main_service_dns.dns_service_handler_plugins_map
#
#        # prints debug message about connection
#        self.main_service_dns_plugin.debug("Connected to: %s" % str(self.dns_address))
#
#        # sets the request timeout
#        request_timeout = REQUEST_TIMEOUT
#
#        # iterates indefinitely
#        while True:
#            # handles the current request if it returns false
#            # the connection was closed or is meant to be closed
#            if not self.current_request_handler(request_timeout, dns_service_handler_plugins_map):
#                # breaks the cycle to close the dns connection
#                break
#
#        # closes the dns connection
#        self.dns_connection.close()
#
#    def stop(self):
#        # closes the dns connection
#        self.dns_connection.close()
#
#    def pause(self):
#        pass
#
#    def resume(self):
#        pass
#
#    def dns_request_handler(self, request_timeout, dns_service_handler_plugins_map):
#        try:
#            # retrieves the request
#            request = self.retrieve_request(request_timeout)
#        except main_service_dns_exceptions.MainServiceDnsException:
#            # prints a debug message about the connection closing
#            self.main_service_dns_plugin.debug("Connection: %s closed by peer, timeout or invalid request" % str(self.dns_address))
#
#            # returns false (connection closed)
#            return False
#
#        try:
#            # prints debug message about request
#            self.main_service_dns_plugin.debug("Handling request: %s" % str(request))
#
#            # verifies the request information, tries to find any possible
#            # security problem in it
#            self._verify_request_information(request)
#
#            # retrieves the real service configuration,
#            # taking the request information into account
#            service_configuration = self._get_service_configuration(request)
#
#            # processes the redirection information in the request
#            self._process_redirection(request, service_configuration)
#
#            # processes the handler part of the request and retrieves
#            # the handler name
#            handler_name = self._process_handler(request, service_configuration)
#
#            # in case the request was not already handled
#            if not handler_name:
#                # retrieves the default handler name
#                handler_name = service_configuration.get("default_handler", None)
#
#                # sets the handler path
#                request.handler_path = None
#
#            # in case no handler name is defined (request not handled)
#            if not handler_name:
#                # raises an dns no handler exception
#                raise main_service_dns_exceptions.DnsNoHandlerException("no handler defined for current request")
#
#            # handles the request by the request handler
#            dns_service_handler_plugins_map[handler_name].handle_request(request)
#
#            # sends the request to the client (response)
#            self.send_request(request)
#
#            # in case the connection is meant to be kept alive
#            if self.keep_alive(request):
#                self.main_service_dns_plugin.debug("Connection: %s kept alive for %ss" % (str(self.dns_address), str(request_timeout)))
#            # in case the connection is not meant to be kept alive
#            else:
#                self.main_service_dns_plugin.debug("Connection: %s closed" % str(self.dns_address))
#
#                # returns false (connection closed)
#                return False
#
#        except Exception, exception:
#            # prints info message about exception
#            self.main_service_dns_plugin.info("There was an exception handling the request: " + str(exception))
#
#            # sends the exception
#            self.send_exception(request, exception)
#
#        # returns true (connection remains open)
#        return True
#
#    def retrieve_request(self, request_timeout = REQUEST_TIMEOUT):
#        """
#        Retrieves the request from the received message.
#
#        @type request_timeout: int
#        @param request_timeout: The timeout for the request retrieval.
#        @rtype: DnsRequest
#        @return: The request from the received message.
#        """
#
#        # creates the string buffer for the message
#        message = colony.libs.string_buffer_util.StringBuffer()
#
#        # creates a request object
#        request = DnsRequest(self, self.content_type_charset)
#
#        # creates the start line loaded flag
#        start_line_loaded = False
#
#        # creates the header loaded flag
#        header_loaded = False
#
#        # creates the message loaded flag
#        message_loaded = False
#
#        # creates the message offset index, representing the
#        # offset byte to the initialization of the message
#        message_offset_index = 0
#
#        # creates the message size value
#        message_size = 0
#
#        # creates the received data size (counter)
#        received_data_size = 0
#
#        # continuous loop
#        while True:
#            # retrieves the data
#            data = self.retrieve_data(request_timeout)
#
#            # retrieves the data length
#            data_length = len(data)
#
#            # in case no valid data was received
#            if data_length == 0:
#                # raises the dns invalid data exception
#                raise main_service_dns_exceptions.DnsInvalidDataException("empty data received")
#
#            # increments the received data size (counter)
#            received_data_size += data_length
#
#            # writes the data to the string buffer
#            message.write(data)
#
#            # in case the header is loaded or the message contents are completely loaded
#            if not header_loaded or received_data_size - message_offset_index == message_size:
#                # retrieves the message value from the string buffer
#                message_value = message.get_value()
#            # in case there's no need to inspect the message contents
#            else:
#                # continues with the loop
#                continue
#
#            # in case the start line is not loaded
#            if not start_line_loaded:
#                # finds the first new line value
#                start_line_index = message_value.find("\r\n")
#
#                # in case there is a new line value found
#                if not start_line_index == -1:
#                    # retrieves the start line
#                    start_line = message_value[:start_line_index]
#
#                    # splits the start line in spaces
#                    start_line_splitted = start_line.split(" ")
#
#                    # retrieves the start line splitted length
#                    start_line_splitted_length = len(start_line_splitted)
#
#                    # in case the length of the splitted line is not three
#                    if not start_line_splitted_length == 3:
#                        # raises the dns invalid data exception
#                        raise main_service_dns_exceptions.DnsInvalidDataException("invalid data received: " + start_line)
#
#                    # retrieve the operation type the path and the protocol version
#                    # from the start line splitted
#                    operation_type, path, protocol_version = start_line_splitted
#
#                    # sets the request operation type
#                    request.set_operation_type(operation_type)
#
#                    # sets the request path
#                    request.set_path(path)
#
#                    # sets the request protocol version
#                    request.set_protocol_version(protocol_version)
#
#                    # sets the start line loaded flag
#                    start_line_loaded = True
#
#            # in case the header is not loaded
#            if not header_loaded:
#                # retrieves the end header index (two new lines)
#                end_header_index = message_value.find("\r\n\r\n")
#
#                # in case the end header index is found
#                if not end_header_index == -1:
#                    # sets the message offset index as the end header index
#                    # plus the two sequences of newlines (four characters)
#                    message_offset_index = end_header_index + 4
#
#                    # sets the header loaded flag
#                    header_loaded = True
#
#                    # retrieves the start header index
#                    start_header_index = start_line_index + 2
#
#                    # retrieves the headers part of the message
#                    headers = message_value[start_header_index:end_header_index]
#
#                    # splits the headers by line
#                    headers_splitted = headers.split("\r\n")
#
#                    # iterates over the headers lines
#                    for header_splitted in headers_splitted:
#                        # finds the header separator
#                        division_index = header_splitted.find(":")
#
#                        # retrieves the header name
#                        header_name = header_splitted[:division_index].strip()
#
#                        # retrieves the header value
#                        header_value = header_splitted[division_index + 1:].strip()
#
#                        # sets the header in the headers map
#                        request.headers_map[header_name] = header_value
#                        request.headers_in[header_name] = header_value
#
#                    # in case the operation type is get
#                    if request.operation_type == GET_METHOD_VALUE:
#                        # parses the get attributes
#                        request.__parse_get_attributes__()
#
#                        # returns the request
#                        return request
#                    # in case the operation type is post
#                    elif request.operation_type == POST_METHOD_VALUE:
#                        # in case the content length is defined in the headers map
#                        if CONTENT_LENGTH_VALUE in request.headers_map:
#                            # retrieves the message size
#                            message_size = int(request.headers_map[CONTENT_LENGTH_VALUE])
#                        elif CONTENT_LENGTH_LOWER_VALUE in request.headers_map:
#                            # retrieves the message size
#                            message_size = int(request.headers_map[CONTENT_LENGTH_LOWER_VALUE])
#                        # in case there is no content length defined in the headers map
#                        else:
#                            # returns the request
#                            return request
#
#            # in case the message is not loaded and the header is loaded
#            if not message_loaded and header_loaded:
#                # retrieves the start message size
#                start_message_index = end_header_index + 4
#
#                # calculates the message value message length
#                message_value_message_length = len(message_value) - start_message_index
#
#                # in case the length of the message value message is the same
#                # as the message size
#                if message_value_message_length == message_size:
#                    # retrieves the message part of the message value
#                    message_value_message = message_value[start_message_index:]
#
#                    # sets the message loaded flag
#                    message_loaded = True
#
#                    # sets the received message
#                    request.received_message = message_value_message
#
#                    # decodes the request if necessary
#                    self.decode_request(request)
#
#                    # returns the request
#                    return request
#
#    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = MESSAGE_MAXIMUM_SIZE):
#        try:
#            # sets the connection to non blocking mode
#            self.dns_connection.setblocking(0)
#
#            # runs the select in the dns connection, with timeout
#            selected_values = select.select([self.dns_connection], [], [], request_timeout)
#
#            # sets the connection to blocking mode
#            self.dns_connection.setblocking(1)
#        except:
#            raise main_service_dns_exceptions.RequestClosed("invalid socket")
#
#        if selected_values == ([], [], []):
#            self.dns_connection.close()
#            raise main_service_dns_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
#        try:
#            # receives the data in chunks
#            data = self.dns_connection.recv(chunk_size)
#        except:
#            raise main_service_dns_exceptions.ClientRequestTimeout("timeout")
#
#        return data
#
#    def send_exception(self, request, exception):
#        """
#        Sends the exception to the given request for the given exception.
#
#        @type request: DnsRequest
#        @param request: The request to send the exception.
#        @type exception: Exception
#        @param exception: The exception to be sent.
#        """
#
#        pass
#
#    def send_request(self, request):
#        pass
#
#
#






class DnsRequest:
    """
    The dns request class.
    """

    transaction_id = None
    """ The transaction id, identifying a unique dns request """

    queries = []
    """ The list of queries """

    answers = []
    """ The list of answers """

    authority_resource_records = []
    """ The list of authority resource records """

    additional_resource_records = []
    """ The list of additional resource records """

    parameters = {}
    """ The parameters to the dns request """

    flags = 0x0100
    """ The flags byte """

    flags_out = 0x8180
    """ The out flags byte """

    name_cache_map = {}
    """ Map to be used to cache the name value references in accordance with dns specification """

    def __init__(self, parameters):
        """
        Constructor of the class.

        @type parameters: Dictionary
        @param parameters: The request parameters.
        """

        self.parameters = parameters

        self.queries = []
        self.answers = []
        self.authority_resource_records = []
        self.additional_resource_records = []
        self.name_cache_map = {}

    def process_data(self, data, address):
        # retrieves the message header from the data
        message_header = struct.unpack_from("!HHHHHH", data)

        # unpacks the message header retrieving the transaction id, the flags, the number of queries
        # the number of authority resource records and the number of additional resource records
        transaction_id, flags, queries, answers, authority_resource_records, additional_resource_records = message_header

        # sets the transaction id and the flags
        self.transaction_id = transaction_id
        self.flags = flags

        # sets the current index as the
        # message header size (offset)
        current_index = MESSAGE_HEADER_SIZE

        # iterates over the number of queries
        for _index in range(queries):
            # retrieves the query and the current index
            query, current_index = self._get_query(data, current_index)

            # adds the query to the list of queries
            self.queries.append(query)

        # iterates over the number of answers
        for _index in range(answers):
            # retrieves the answer and the current index
            answer, current_index = self._get_answer(data, current_index)

            # adds the answer to the list of answers
            self.answers.append(answer)

        # iterates over the number of authority resource records
        for _index in range(authority_resource_records):
            # retrieves the authority resource record and the current index
            authority_resource_record, current_index = self._get_answer(data, current_index)

            # adds the authority resource record to the list of authority resource records
            self.authority_resource_records.append(authority_resource_record)

        # iterates over the number of additional resource records
        for _index in range(additional_resource_records):
            # retrieves the additional resource record and the current index
            additional_resource_record, current_index = self._get_answer(data, current_index)

            # adds the additional resource record to the list of additional resource records
            self.additional_resource_records.append(additional_resource_record)

    def get_result(self):
        """
        Retrieves the result string (serialized) value of
        the request.

        @rtype: String
        @return: The result string (serialized) value of
        the request.
        """

        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer(False)

        # retrieves the number of queries
        number_queries = len(self.queries)

        # retrieves the number of answers
        number_answers = len(self.answers)

        # retrieves the number of authority resource records
        number_authority_resource_records = len(self.authority_resource_records)

        # retrieves the number of additional resource records
        number_additional_resource_records = len(self.additional_resource_records)

        # generates the query header
        query_header = struct.pack("!HHHHHH", self.transaction_id, self.flags_out, number_queries, number_answers, number_authority_resource_records, number_additional_resource_records)

        # writes the query header to the result stream
        result.write(query_header)

        # iterates over all the queries
        for query in self.queries:
            # retrieves the current index
            current_index = result.tell()

            # serializes the query
            query_serialized = self._serialize_query(query, current_index)

            # writes the serialized query to the result stream
            result.write(query_serialized)

        # iterates over all the answers
        for answer in self.answers:
            # retrieves the current index
            current_index = result.tell()

            # serializes the answer
            answer_serialized = self._serialize_answer(answer, current_index)

            # writes the serialized answer to the result stream
            result.write(answer_serialized)

        # iterates over all the authority resource records
        for authority_resource_record in self.authority_resource_records:
            # retrieves the current index
            current_index = result.tell()

            # serializes the authority resource record
            authority_resource_record_serialized = self._serialize_answer(authority_resource_record, current_index)

            # writes the serialized authority resource record to the result stream
            result.write(authority_resource_record_serialized)

        # iterates over all the additional resource records
        for additional_resource_record in self.additional_resource_records:
            # retrieves the current index
            current_index = result.tell()

            # serializes the additional resource record
            additional_resource_record_serialized = self._serialize_answer(additional_resource_record, current_index)

            # writes the serialized additional resource record to the result stream
            result.write(additional_resource_record_serialized)

        # clears the name cache structures
        self._clear_name_cache()

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def _get_query(self, data, current_index):
        # retrieves the name for the data and current index
        name_list, current_index = self._get_name(data, current_index)

        # creates the query name by joining the name list
        query_name = ".".join(name_list)

        # retrieves the query type and the query class integer values
        query_type_integer, query_class_integer = struct.unpack_from("!HH", data, current_index)

        # increments the current index with four bytes
        current_index += 4

        # retrieves the query type (string value)
        query_type = TYPES_REVERSE_MAP[query_type_integer]

        # retrieves the query class (string value)
        query_class = CLASSES_REVERSE_MAP[query_class_integer]

        # creates the query tuple with the name, type and class of the query
        query = (query_name, query_type, query_class)

        return (query, current_index)

    def _get_answer(self, data, current_index):
        # retrieves the name for the data and current index
        answer_name, current_index = self._get_name_joined(data, current_index)

        # retrieves the answer type, answer class, time to live
        # and data length integer values
        answer_type_integer, answer_class_integer, answer_time_to_live, answer_data_length = struct.unpack_from("!HHIH", data, current_index)

        # increments the current index with ten bytes
        current_index += 10

        # processes the answer data from the answer type and the answer length
        answer_data = self._process_answer_data(data, current_index, answer_type_integer, answer_data_length)

        # increments the current index with the answer data length
        current_index += answer_data_length

        # retrieves the answer type (string value)
        answer_type = TYPES_REVERSE_MAP[answer_type_integer]

        # retrieves the answer class (string value)
        answer_class = CLASSES_REVERSE_MAP[answer_class_integer]

        # creates the answer tuple with the name, type, class,
        # time to live and data of the answer
        answer = (answer_name, answer_type, answer_class, answer_time_to_live, answer_data)

        return (answer, current_index)

    def _process_answer_data(self, data, current_index, answer_type_integer, answer_data_length):
        """
        Processes the answer data according to the dns protocol
        specification.
        The answer data is processed converting it into the most
        appropriate python representation.

        @type data: String
        @param data: The data buffer to be used.
        @type current_index: int
        @param current_index: The index to be used as base index.
        @type answer_type_integer: int
        @param answer_type_integer: The answer type in integer mode.
        @type answer_data_length: int
        @param answer_data_length: The length of the answer data.
        @rtype: Object
        @return: The "processed" answer data.
        """

        # in case the answer is of type ns or cname
        if answer_type_integer in (0x02, 0x05):
            # retrieves the answer data as a joined name
            answer_data, _current_index = self._get_name_joined(data, current_index)
        # in case the answer is of type mx
        elif answer_type_integer in (0x0f,):
            # retrieves the answer data preference
            answer_data_preference, = struct.unpack_from("!H", data, current_index)

            # retrieves the answer data name as a joined name
            answer_data_name, _current_index = self._get_name_joined(data, current_index + 2)

            # sets the answer data tuple
            answer_data = (answer_data_preference, answer_data_name)
        else:
            # in case the is ipv4 (four bytes)
            if answer_data_length == 4:
                raw_answer_data_bytes = struct.unpack_from("!" + str(answer_data_length) + "B", data, current_index)
                raw_answer_data_string = [str(value) for value in raw_answer_data_bytes]
                answer_data = ".".join(raw_answer_data_string)
            # in case the is ipv6 (sixteen bytes)
            elif answer_data_length == 16:
                raw_answer_data_shorts = struct.unpack_from("!" + str(answer_data_length / 2) + "H", data, current_index)
                raw_answer_data_string = ["%h" % value for value in raw_answer_data_shorts]
                answer_data = ":".join(raw_answer_data_string)
            else:
                # sets the answer data as the raw answer data
                answer_data = data[current_index:current_index + answer_data_length]

        # returns the answer data
        return answer_data

    def _clear_name_cache(self):
        """
        Clears the name cache structures.
        """

        # clears the map that contains the name cache
        self.name_cache_map.clear()

    def _serialize_query(self, query, current_index):
        """
        Serializes the given query into the dns binary format.

        @type query: Tuple
        @param query: A tuple with the query information.
        @type current_index: int
        @param current_index: The current index of the writing buffer.
        @rtype: String
        @return: The string containing the resource record.
        """

        # unpacks the query tuple, retrieving the name,
        # type and class
        query_name, query_type, query_class = query

        # converts the query type to integer
        query_type_integer = TYPES_MAP[query_type]

        # converts the query class to integer
        query_class_integer = CLASSES_MAP[query_class]

        # creates the string buffer to hold the stream
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the query name serialized into the string buffer
        self._write_name_serialized(query_name, string_buffer, current_index)

        # creates the query data from the query type and class
        query_data = struct.pack("!HH", query_type_integer, query_class_integer)

        # writes the query data to the string buffer
        string_buffer.write(query_data)

        # retrieves the serialized query value from the string buffer
        query_serialized = string_buffer.get_value()

        # returns the serialized query
        return query_serialized

    def _serialize_answer(self, answer, current_index):
        """
        Serializes the given answer into the dns binary format.

        @type answer: Tuple
        @param answer: A tuple with the answer information.
        @type current_index: int
        @param current_index: The current index of the writing buffer.
        @rtype: String
        @return: The string containing the resource record.
        """

        # unpacks the answer tuple, retrieving the name,
        # type, class and data
        answer_name, answer_type, answer_class, answer_time_to_live, answer_data = answer

        # converts the answer type to integer
        answer_type_integer = TYPES_MAP[answer_type]

        # converts the answer class to integer
        answer_class_integer = CLASSES_MAP[answer_class]

        # creates the string buffer to hold the stream
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the answer name into the string buffer
        self._write_name_serialized(answer_name, string_buffer, current_index)

        # serializes the answer data
        answer_data_serialized = self._serialize_answer_data(answer_name, answer_data)

        # retrieves the answer data length from the answer data serialized
        answer_data_length = len(answer_data_serialized)

        # creates the answer information from the answer type, class, time to live and data length
        answer_information = struct.pack("!HHIH", answer_type_integer, answer_class_integer, answer_time_to_live, answer_data_length)

        # writes the answer information to the string buffer
        string_buffer.write(answer_information)

        # writes the answer data serialized to the string buffer
        string_buffer.write(answer_data_serialized)

        # retrieves the serialized query value from the string buffer
        query_serialized = string_buffer.get_value()

        # returns the serialized query
        return query_serialized

    def _serialize_name(self, name):
        # creates the string buffer to hold the serialized
        # name information
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # splits the name to retrieve the name items
        name_items = name.split(".")

        # starts the index counter
        index = 0

        # iterates over all the name items
        for name_item in name_items:
            # retrieves the name item identifier, used
            # to identify the tokens and sub-tokens in the name cache map
            name_item_identifier = name_items[index:]

            # converts the name item identifier from list to tuple
            # in order to "hashable"
            name_item_identifier = tuple(name_item_identifier)

            # in case the name item identifier is found in the name
            # cache map (the name was already written in the request)
            if name_item_identifier in self.name_cache_map:
                # retrieves the name item index
                name_item_index = self.name_cache_map[name_item_identifier]

                # ors the name item index with the "cache marker"
                name_item_index |= 0xc000

                # converts the name item index to string
                name_item_index_string = struct.pack("!H", name_item_index)

                # writes the name item index string to the string buffer
                string_buffer.write(name_item_index_string)

                # returns immediately
                return

            # retrieves the name item length
            name_item_length = len(name_item)

            # retrieves the name item length in binary value
            name_item_length_character = chr(name_item_length)

            # writes the size of the name item (in binary value) and
            # the name itself
            string_buffer.write(name_item_length_character)
            string_buffer.write(name_item)

            # increments the index counter
            index += 1

        # writes the end of string in the string buffer
        string_buffer.write("\0")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value (name serialized)
        return string_value

    def _write_name_serialized(self, name, string_buffer , current_index = None):
        # splits the name to retrieve the name items
        name_items = name.split(".")

        # starts the index counter
        index = 0

        # iterates over all the name items
        for name_item in name_items:
            # retrieves the name item identifier, used
            # to identify the tokens and sub-tokens in the name cache map
            name_item_identifier = name_items[index:]

            # converts the name item identifier from list to tuple
            # in order to "hashable"
            name_item_identifier = tuple(name_item_identifier)

            # in case the name item identifier is found in the name
            # cache map (the name was already written in the request)
            if name_item_identifier in self.name_cache_map:
                # retrieves the name item index
                name_item_index = self.name_cache_map[name_item_identifier]

                # ors the name item index with the "cache marker"
                name_item_index |= 0xc000

                # converts the name item index to string
                name_item_index_string = struct.pack("!H", name_item_index)

                # writes the name item index string to the string buffer
                string_buffer.write(name_item_index_string)

                # returns immediately
                return

            # retrieves the name item length
            name_item_length = len(name_item)

            # retrieves the name item length in binary value
            name_item_length_character = chr(name_item_length)

            # writes the size of the name item (in binary value) and
            # the name itself
            string_buffer.write(name_item_length_character)
            string_buffer.write(name_item)

            # sets the current token and sub-tokens in the name cache map
            # for the current index
            self.name_cache_map[name_item_identifier] = current_index

            # increments the current index with the name item length
            current_index += name_item_length

            # increments the index counter
            index += 1

        # writes the end of string in the string buffer
        string_buffer.write("\0")

    def _serialize_answer_data(self, answer_name_integer, answer_data):
        # in case the answer is of type ns or cname
        if answer_name_integer in (0x02, 0x05):
            serialized_answer_data = self._serialize_name(answer_data)
        # in case the answer is of type mx
        elif answer_name_integer in (0x0f,):
            # unpacks the answer data into preference and name
            answer_data_preference, answer_data_name = answer_data

            # serializes (packs) the answer data preference
            answer_data_preference_serialized, = struct.pack("!H", answer_data_preference)

            # serializes the answer data name
            answer_data_name_serialized = self._serialize_name(answer_data_name)

            # sets the serializes answer data as the concatenation
            # of the answer data preference and the answer data name (both serialized)
            serialized_answer_data = answer_data_preference_serialized + answer_data_name_serialized
        else:
            # in case the is ipv4 (four bytes)
            if not answer_data.find(".") == -1:
                raw_answer_data_string = answer_data.split(".")
                raw_answer_data_bytes = [int(value) for value in raw_answer_data_string]
                raw_answer_data_bytes_length = len(raw_answer_data_bytes)
                serialized_answer_data = struct.pack("!" + str(raw_answer_data_bytes_length) + "B", *raw_answer_data_bytes)
            # in case the is ipv6 (sixteen bytes)
            elif not answer_data.find(":") == -1:
                raw_answer_data_string = answer_data.split(":")
                raw_answer_data_shorts = [int(value or "", 16) for value in raw_answer_data_string]
                raw_answer_data_shorts_length = len(raw_answer_data_shorts)
                serialized_answer_data = struct.pack("!" + raw_answer_data_shorts_length + "H", *raw_answer_data_shorts)
            else:
                # sets the serialized answer data as the raw answer data
                serialized_answer_data = answer_data

        # returns the serialized answer data
        return serialized_answer_data

    def _get_name_joined(self, data, current_index):
        """
        Retrieves the name "encoded" according to the dns
        specification in the given index.
        This method joins the resulting list in a string
        separated with dots.

        @type data: String
        @param data: The data buffer to be used.
        @type current_index: int
        @param current_index: The index to be used as base index.
        @rtype: Tuple
        @return: The "decoded" name (joined in with dots) in the given index
        and the current index encoded in a tuple.
        """

        # retrieves the name list and the "new" current index
        name_list, current_index = self._get_name(data, current_index)

        # joins the name with dots
        name_joined = ".".join(name_list)

        return (name_joined, current_index)

    def _get_name(self, data, current_index):
        """
        Retrieves the name "encoded" according to the dns
        specification in the given index.

        @type data: String
        @param data: The data buffer to be used.
        @type current_index: int
        @param current_index: The index to be used as base index.
        @rtype: Tuple
        @return: The "decoded" name (in list) in the given index
        and the current index encoded in a tuple.
        """

        # creates the name items list
        name_items = []

        # iterates while the current data item is
        # not end of string
        while not data[current_index] == "\0":
            # retrieves the length of the partial name name
            partial_name_length, = struct.unpack_from("!B", data, current_index)

            # checks if the name already exists (according to the message compression)
            existing_resource = partial_name_length & 0xc0 == 0xc0

            # in case the resource exists
            if existing_resource:
                # sets the partial name length as the
                # first offset byte
                first_offset_byte = partial_name_length

                # unpacks the second offset byte from the data
                second_offset_byte, = struct.unpack_from("!B", data, current_index + 1)

                # calculates the offset index
                offset_index = ((first_offset_byte & 0x3f) << 8) + second_offset_byte

                # updates the current index with the two bytes
                current_index += 2

                # returns the previous (cached) name items list
                extra_name_items, _current_index = self._get_name(data, offset_index)

                # extends the current name items with the previous (cached) name items
                name_items.extend(extra_name_items)

                return (name_items, current_index)
            else:
                # retrieves the partial name from the data
                partial_name = data[current_index + 1:current_index + partial_name_length + 1]

                # adds the partial name to the name items list
                name_items.append(partial_name)

                # updates the current index with the partial name length plus one
                current_index += partial_name_length + 1

        # increments the current index with the
        # end string byte
        current_index += 1

        # returns the name items list
        return (name_items, current_index)
