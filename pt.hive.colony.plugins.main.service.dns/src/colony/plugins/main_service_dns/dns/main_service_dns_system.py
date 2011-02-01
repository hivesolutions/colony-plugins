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

import struct

import colony.libs.map_util
import colony.libs.string_buffer_util

import main_service_dns_exceptions

CONNECTION_TYPE = "connectionless"
""" The connection type """

BIND_HOST = ""
""" The bind host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 10
""" The request timeout """

RESPONSE_TIMEOUT = 10
""" The response timeout """

MESSAGE_MAXIMUM_SIZE = 512
""" The message maximum size """

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

DEFAULT_PORT = 53
""" The default port """

MESSAGE_HEADER_SIZE = 12
""" The size of the dns message header (in bytes) """

NORMAL_REQUEST_VALUE = 0x0100
""" The normal request value """

NORMAL_RESPONSE_VALUE = 0x8180
""" The normal response value """

NO_ERROR_MASK_VALUE = 0x0000
""" The no error mask value """

FORMAT_ERROR_MASK_VALUE = 0x0001
""" The format error mask value """

SERVER_FAILURE_ERROR_MASK_VALUE = 0x0002
""" The server failure error mask value """

NOT_IMPLEMENTED_ERROR_MASK_VALUE = 0x0004
""" The not implemented error mask value """

REFUSED_ERROR_MASK_VALUE = 0x0008
""" The refused error mask value """

CACHE_MASK_VALUE = 0xc000
""" The cache mask value """

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
    """ The dns service handler plugins map """

    dns_service = None
    """ The dns service reference """

    dns_service_configuration = {}
    """ The dns service configuration """

    def __init__(self, main_service_dns_plugin):
        """
        Constructor of the class.

        @type main_service_dns_plugin: MainServiceDnsPlugin
        @param main_service_dns_plugin: The main service dns plugin.
        """

        self.main_service_dns_plugin = main_service_dns_plugin

        self.dns_service_handler_plugin_map = {}
        self.dns_service_configuration = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the main service utils plugin
        main_service_utils_plugin = self.main_service_dns_plugin.main_service_utils_plugin

        # generates the parameters
        service_parameters = self._generate_service_parameters(parameters)

        # generates the dns service using the given service parameters
        self.dns_service = main_service_utils_plugin.generate_service(service_parameters)

        # starts the dns service
        self.dns_service.start_service()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to stop the service.
        """

        # destroys the parameters
        self._destroy_service_parameters(parameters)

        # starts the dns service
        self.dns_service.stop_service()

    def dns_service_handler_load(self, dns_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = dns_service_handler_plugin.get_handler_name()

        self.dns_service_handler_plugins_map[handler_name] = dns_service_handler_plugin

    def dns_service_handler_unload(self, dns_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = dns_service_handler_plugin.get_handler_name()

        del self.dns_service_handler_plugins_map[handler_name]

    def set_service_configuration_property(self, service_configuration_property):
        # retrieves the service configuration
        service_configuration = service_configuration_property.get_data()

        # cleans the dns service configuration
        colony.libs.map_util.map_clean(self.dns_service_configuration)

        # copies the service configuration to the dns service configuration
        colony.libs.map_util.map_copy(service_configuration, self.dns_service_configuration)

    def unset_service_configuration_property(self):
        # cleans the dns service configuration
        colony.libs.map_util.map_clean(self.dns_service_configuration)

    def _get_service_configuration(self):
        """
        Retrieves the service configuration map.

        @rtype: Dictionary
        @return: The service configuration map.
        """

        return self.dns_service_configuration

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
        pool_configuration = {"name" : "dns pool",
                              "description" : "pool to support dns client connections",
                              "number_threads" : number_threads,
                              "scheduling_algorithm" : scheduling_algorithm,
                              "maximum_number_threads" : maximum_number_threads,
                              "maximum_number_works_thread" : maximum_number_work_threads,
                              "work_scheduling_algorithm" : work_scheduling_algorithm}

        # creates the extra parameters map
        extra_parameters = {}

        # creates the parameters map
        parameters = {"type" : CONNECTION_TYPE,
                      "service_plugin" : self.main_service_dns_plugin,
                      "service_handling_task_class" : DnsClientServiceHandler,
                      "end_points" : end_points,
                      "socket_provider" : socket_provider,
                      "bind_host" : BIND_HOST,
                      "port" : port,
                      "socket_parameters" : socket_parameters,
                      "chunk_size" : MESSAGE_MAXIMUM_SIZE,
                      "service_configuration" : service_configuration,
                      "extra_parameters" :  extra_parameters,
                      "pool_configuration" : pool_configuration,
                      "client_connection_timeout" : client_connection_timeout,
                      "connection_timeout" : connection_timeout,
                      "request_timeout" : request_timeout,
                      "response_timeout" : response_timeout}

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

class DnsClientServiceHandler:
    """
    The dns client service handler class.
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

    def handle_request(self, service_connection):
        # retrieves the dns service handler plugins map
        dns_service_handler_plugins_map = self.service_plugin.main_service_dns.dns_service_handler_plugins_map

        try:
            # retrieves the request
            request = self.retrieve_request(service_connection)
        except main_service_dns_exceptions.MainServiceDnsException:
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

            # retrieves the handler properties
            handler_properties = service_configuration.get("handler_properties", {})

            # retrieves the handler arguments
            handler_arguments = handler_properties.get("arguments", {})

            # in case no handler name is defined (request not handled)
            if not handler_name:
                # raises an dns no handler exception
                raise main_service_dns_exceptions.DnsNoHandlerException("no handler defined for current request")

            # in case the handler is not found in the handler plugins map
            if not handler_name in dns_service_handler_plugins_map:
                # raises an dns handler not found exception
                raise main_service_dns_exceptions.DnsHandlerNotFoundException("no handler found for current request: " + handler_name)

            # retrieves the dns service handler plugin
            dns_service_handler_plugin = dns_service_handler_plugins_map[handler_name]

            # handles the request by the request handler
            dns_service_handler_plugin.handle_request(request, handler_arguments)

            try:
                # sends the request to the client (response)
                self.send_request(service_connection, request)
            except main_service_dns_exceptions.MainServiceDnsException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending request" % str(service_connection))

                # returns false (connection closed)
                return False

        except Exception, exception:
            # prints info message about exception
            self.service_plugin.info("There was an exception handling the request: " + unicode(exception))

            try:
                # sends the exception
                self.send_exception(service_connection, request, exception)
            except main_service_dns_exceptions.MainServiceDnsException:
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
        @rtype: AbeculaRequest
        @return: The request from the received message.
        """

        # receives the data
        data = service_connection.receive()

        # retrieves the data length
        data_length = len(data)

        # in case the data length is bigger than the
        # message maximum size
        if data_length > MESSAGE_MAXIMUM_SIZE:
            # raises the dns invalid data exception
            raise main_service_dns_exceptions.DnsInvalidDataException("message data overflow")

        # creates a new dns request
        request = DnsRequest({})

        # processes the request
        request.process_data(data)

        # returns the request
        return request

    def send_exception(self, service_connection, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type request: DnsRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # resets the response value (deletes answers)
        request.reset_response()

        # checks if the error contains a dns failure mask
        if hasattr(exception, "dns_failure_mask"):
            # sets the flags out (response) with
            # the dns failure mask
            request.flags_out |= exception.dns_failure_mask
        # in case there is no status code defined in the error
        else:
            # sets the flags out (response) with
            # the dns failure mask
            request.flags_out |= SERVER_FAILURE_ERROR_MASK_VALUE

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

            # raises the dns data sending exception
            raise main_service_dns_exceptions.DnsDataSendingException("problem sending data")

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        @type request: DnsRequest
        @param request: The request to be used in the resolution
        of the service configuration.
        @rtype: Dictionary
        @return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # returns the service configuration
        return service_configuration

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

    flags = NORMAL_REQUEST_VALUE
    """ The flags byte """

    flags_out = NORMAL_RESPONSE_VALUE
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

    def __repr__(self):
        return "(%s, 0x%04x, %s)" % (self.transaction_id, self.flags, str(self.queries))

    def process_data(self, data):
        """
        Processes the given data creating the request
        information values.

        @type data: String
        @param data: The data to be processed to create
        the request.
        """

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

        # validates the current request
        self.validate()

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

    def validate(self):
        """
        Validates the current request, raising exception
        in case validation fails.
        """

        pass

    def reset_response(self):
        """
        Resets the response value, clearing all
        the response data structures.
        """

        self.answers = []
        self.authority_resource_records = []
        self.additional_resource_records = []

    def get_queries(self):
        """
        Retrieves the queries.

        @rtype: List
        @return: The queries.
        """

        return self.queries

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

                # "ors" the name item index with the "cache marker"
                name_item_index |= CACHE_MASK_VALUE

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

                # "ors" the name item index with the "cache marker"
                name_item_index |= CACHE_MASK_VALUE

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
            # plus the byte containing the name length
            current_index += name_item_length + 1

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
