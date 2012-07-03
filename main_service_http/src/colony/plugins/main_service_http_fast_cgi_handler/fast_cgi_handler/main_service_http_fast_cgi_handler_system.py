#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import struct
import socket
import threading

import colony.libs.string_buffer_util

import main_service_http_fast_cgi_handler_exceptions

HANDLER_NAME = "fast_cgi"
""" The handler name """

HANDLER_TYPE_VALUE = "handler_type"
""" The handler type value """

BASE_PATH_VALUE = "base_path"
""" The base path value """

CONNECTION_TYPE_VALUE = "connection_type"
""" The connection type value """

CONNECTION_ARGUMENTS_VALUE = "connection_arguments"
""" The connection arguments value """

CONTENT_TYPE_HEADER_VALUE = "Content-Type"
""" The content type value """

CONTENT_LENGTH_HEADER_VALUE = "Content-Length"
""" The content length value """

STATUS_VALUE = "Status"
""" The status value """

GATEWAY_INTERFACE = "CGI/1.0"
""" The gateway interface """

SERVER_SOFTWARE_VALUE = "SERVER_SOFTWARE"
""" The server software value """

SERVER_NAME_VALUE = "SERVER_NAME"
""" The server name value """

GATEWAY_INTERFACE_VALUE = "GATEWAY_INTERFACE"
""" The gateway interface value """

SERVER_PROTOCOL_VALUE = "SERVER_PROTOCOL"
""" The server protocol value """

SERVER_PORT_VALUE = "SERVER_PORT"
""" The server port value """

REQUEST_METHOD_VALUE = "REQUEST_METHOD"
""" The request method value """

PATH_INFO_VALUE = "PATH_INFO"
""" The path info value """

PATH_TRANSLATED_VALUE = "PATH_TRANSLATED"
""" The path translated value """

SCRIPT_NAME_VALUE = "SCRIPT_NAME"
""" The script name value """

QUERY_STRING_VALUE = "QUERY_STRING"
""" The query string value """

REMOTE_HOST_VALUE = "REMOTE_HOST"
""" The remote host value """

REMOTE_ADDR_VALUE = "REMOTE_ADDR"
""" The remote addr value """

CONTENT_TYPE_VALUE = "CONTENT_TYPE"
""" The content type value """

CONTENT_LENGTH_VALUE = "CONTENT_LENGTH"
""" The content length value """

PYTHONPATH_VALUE = "PYTHONPATH"
""" The pythonpath value """

DEFAULT_CONTENT_TYPE = "text/plain"
""" The default content type """

DEFAULT_APPLICATION_CONTENT_TYPE = "application/x-www-form-urlencoded"
""" The default application content type """

DEFAULT_CONTENT_LENGTH = "0"
""" The default content length """

DEFAULT_STATUS = 200
""" The default status """

FCGI_VERSION_1_VALUE = 1
""" The fcgi version one value """

FCGI_BEGIN_REQUEST_VALUE = 1
""" The fcgi begin request value """

FCGI_ABORT_REQUEST_VALUE = 2
""" The fcgi abort request value """

FCGI_END_REQUEST_VALUE = 3
""" The fcgi end request value """

FCGI_PARAMS_VALUE = 4
""" The fcgi params value """

FCGI_STDIN_VALUE = 5
""" The fcgi stdin value """

FCGI_STDOUT_VALUE = 6
""" The fcgi stdout value """

FCGI_STDERR_VALUE = 7
""" The fcgi stderr value """

FCGI_DATA_VALUE = 8
""" The fcgi data value """

FCGI_GET_VALUES_VALUE = 9
""" The fcgi get values value """

FCGI_GET_VALUES_RESULT_VALUE = 10
""" The fcgi get values result value """

FCGI_UNKNOWN_TYPE_VALUE = 11
""" The fcgi unknown type value """

FCGI_MAXTYPE_VALUE = FCGI_UNKNOWN_TYPE_VALUE
""" The fcgi maxtype value """

FCGI_KEEP_CONN_VALUE = 1
""" The fcgi keep conn value """

FCGI_RESPONDER_VALUE = 1
""" The fcgi responder value """

FCGI_AUTHORIZER_VALUE = 2
""" The fcgi authorizer value """

FCGI_FILTER_VALUE = 3
""" The fcgi filter value """

FCGI_HEADER_LENGTH = 8
""" The fcgi header length """

FCGI_HEADER_STRUCT = "!BBHHBx"
""" The fcgi header struct """

FCGI_BEGIN_REQUEST_BODY_STRUCT = "!HB5x"
""" The fcgi begin header body struct """

FCGI_END_REQUEST_BODY_STRUCT = "!LB3x"
""" The fcgi request body struct """

FCGI_UNKNOWN_TYPE_BODY_STRUCT = "!B7x"
""" The fcgi unknown type body struct """

FCGI_PARAMS_LENGTH_STRUCT = "!II"
""" The fcgi params length struct """

INTERNET_CONNECTION_TYPE = 1
""" The internet connection type """

UNIX_CONNECTION_TYPE = 2
""" The unix connection type """

META_HEADER_NAME_PREFIX = "HTTP_"
""" The meta header name prefix """

DEFAULT_HANDLER_TYPE = "local"
""" The default handler type """

DEFAULT_PATH = "~/fastcgi-bin"
""" The default path """

DEFAULT_CONNECTION_TYPE = INTERNET_CONNECTION_TYPE
""" The default connection type """

DEFAULT_CONNECTION_ARGUMENTS = (
    "127.0.0.1",
    9000
)
""" The default connection arguments type """

class MainServiceHttpFastCgiHandler:
    """
    The main service http fast cgi handler class.
    """

    main_service_http_fast_cgi_handler_plugin = None
    """ The main service http fast cgi handler plugin """

    connection_map = {}
    """ The connection map """

    def __init__(self, main_service_http_fast_cgi_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_fast_cgi_handler_plugin: MainServiceHttpFastCgiHandlerPlugin
        @param main_service_http_fast_cgi_handler_plugin: The main service http fast cgi handler plugin.
        """

        self.main_service_http_fast_cgi_handler_plugin = main_service_http_fast_cgi_handler_plugin
        self.connection_map = {}

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        # reads the request contents
        request_contents = request.read()

        # retrieves the request server identifier protocol version
        request_server_identifier = request.get_server_identifier()

        # retrieves the request file name
        request_filename = request.filename

        # retrieves the request http service connection
        request_service_connection = request.service_connection

        # retrieves the request operation type
        request_operation_type = request.operation_type

        # retrieves the request protocol version
        request_protocol_version = request.protocol_version

        # retrieves the request query string
        request_query_string = request.query_string

        # retrieves the request connection address
        request_connection_address = request_service_connection.connection_address

        # retrieves the request connection port
        request_connection_port = request_service_connection.connection_port

        # retrieves the request content type
        request_content_type = request.get_header(CONTENT_TYPE_HEADER_VALUE) or DEFAULT_APPLICATION_CONTENT_TYPE

        # retrieves the request content length
        request_content_length = request.get_header(CONTENT_LENGTH_HEADER_VALUE) or DEFAULT_CONTENT_LENGTH

        # retrieves the client hostname and port
        client_http_address, _client_http_port = request_connection_address

        # sets the handler type
        handler_type = request.properties.get(HANDLER_TYPE_VALUE, DEFAULT_HANDLER_TYPE)

        # sets the base path
        base_path = request.properties.get(BASE_PATH_VALUE, DEFAULT_PATH)

        # retrieves the connection type
        connection_type = request.properties.get(CONNECTION_TYPE_VALUE, DEFAULT_CONNECTION_TYPE)

        # retrieves the connection arguments
        connection_arguments = request.properties.get(CONNECTION_ARGUMENTS_VALUE, DEFAULT_CONNECTION_ARGUMENTS)

        # retrieves the connection
        connection = self._get_connection(connection_type, connection_arguments)

        # increments the current request id of the connection
        # and retrieves the current request id
        request_id = connection.increment_request_id()

        # constructs the begin record data
        begin_record_data = struct.pack(FCGI_BEGIN_REQUEST_BODY_STRUCT, FCGI_RESPONDER_VALUE, FCGI_KEEP_CONN_VALUE)

        # adds the begin record to the connection
        connection.add_record(request_id, FCGI_BEGIN_REQUEST_VALUE, begin_record_data)

        # creates the environment map
        environment_map = {}

        # sets the cgi properties in the environment map
        environment_map[SERVER_SOFTWARE_VALUE] = request_server_identifier
        environment_map[SERVER_NAME_VALUE] = ""
        environment_map[GATEWAY_INTERFACE_VALUE] = GATEWAY_INTERFACE
        environment_map[SERVER_PROTOCOL_VALUE] = request_protocol_version
        environment_map[SERVER_PORT_VALUE] = str(request_connection_port)
        environment_map[REQUEST_METHOD_VALUE] = request_operation_type
        environment_map[PATH_INFO_VALUE] = request_filename
        environment_map[PATH_TRANSLATED_VALUE] = request_filename
        environment_map[SCRIPT_NAME_VALUE] = request_filename
        environment_map[QUERY_STRING_VALUE] = request_query_string
        environment_map[REMOTE_HOST_VALUE] = client_http_address
        environment_map[REMOTE_ADDR_VALUE] = client_http_address
        environment_map[CONTENT_TYPE_VALUE] = request_content_type
        environment_map[CONTENT_LENGTH_VALUE] = request_content_length

        # iterates over all the request headers
        for header_name, header_value in request.headers_map.items():
            # normalizes the header name to be in accordance with
            # the specification
            normalized_header_name = header_name.upper().replace("-", "_")

            # creates the complete header name prepending the meta
            # header name prefix to it
            complete_header_name = META_HEADER_NAME_PREFIX + normalized_header_name

            # sets the header value in the environment map
            environment_map[complete_header_name] = header_value

        # initializes the params record data buffer
        params_record_data_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates over the environment map items
        for header, header_value in environment_map.items():
            # retrieves the header length
            header_length = len(header)

            # retrieves the header value length
            header_value_length = len(header_value)

            # retrieves the params length data
            params_length_data = struct.pack(FCGI_PARAMS_LENGTH_STRUCT, header_length | 0x80000000, header_value_length | 0x80000000)

            # writes the values to the params record data buffer
            params_record_data_buffer.write(params_length_data)
            params_record_data_buffer.write(header)
            params_record_data_buffer.write(header_value)

        # retrieves the params record data
        params_record_data = params_record_data_buffer.get_value()

        # adds the params record to the connection
        connection.add_record(request_id, FCGI_PARAMS_VALUE, params_record_data)

        # adds the params record to the connection
        connection.add_record(request_id, FCGI_PARAMS_VALUE, "")

        # adds the stdin record to the connection
        connection.add_record(request_id, FCGI_STDIN_VALUE, request_contents)

        # initializes the standard output buffer
        stdout_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates indefinitely
        while True:
            # retrieves a record for the given request id
            record = connection.get_record(request_id)

            # retrieves the record values
            _version, type, _request_id, _content_length, _padding_length, contents = record

            # in case the type of the request is stdout
            if type == FCGI_STDOUT_VALUE:
                stdout_buffer.write(contents)
            # in case the type of the request is end request
            if type == FCGI_END_REQUEST_VALUE:
                break

        # retrieves the standard output data
        stdout_data = stdout_buffer.get_value()

        try:
            # splits the standard output data
            stdout_data_splitted = stdout_data.split("\r\n\r\n")

            # retrieves the header string from the first part
            # of the standard output data
            header_string = stdout_data_splitted[0]

            # retrieves the contents joining the second part
            # of the splitted standard output data
            contents = "".join(stdout_data_splitted[1:])
        except:
            # raises the invalid cgi data exception
            raise main_service_http_fast_cgi_handler_exceptions.InvalidFastCgiData("problem parsing the fast cgi data")

        try:
            # splits the header string retrieving the headers list
            headers_list = header_string.split("\r\n")

            # creates the headers map
            headers_map = {}

            # iterates over all the headers in the headers list
            for header in headers_list:
                # retrieves the header name and value spliting the header
                header_name, header_value = header.split(":")

                # strips the header name
                header_name_stripped = header_name.strip()

                # strips the header value
                header_value_stripped = header_value.strip()

                # sets the header value in the headers map
                headers_map[header_name_stripped] = header_value_stripped
        except:
            # raises the invalid cgi header exception
            raise main_service_http_fast_cgi_handler_exceptions.InvalidFastCgiHeader("problem parsing the fast cgi header")

        # retrieves the content type
        content_type = headers_map.get(CONTENT_TYPE_HEADER_VALUE, DEFAULT_CONTENT_TYPE)

        # retrieves the status
        status = headers_map.get(STATUS_VALUE, DEFAULT_STATUS)

        # writes the contents to the request
        request.write(contents)

        # sets the request content type
        request.content_type = content_type

        # sets the request status code
        request.status_code = status

        # raises the request not handled exception
        #raise main_service_http_fast_cgi_handler_exceptions.RequestNotHandled("no fast cgi handler could handle the request")

    def _get_connection(self, connection_type, connection_arguments):
        """
        Retrieves the connection, creating it if necessary.

        @type connection_type: int
        @param connection_type: The connection type.
        @type connection_arguments: Object
        @param connection_arguments: The connection arguments.
        """

        # creates the connection id tuple
        connection_id_tuple = (
            connection_type,
            connection_arguments
        )

        # in case the connection id tuples does not exists
        # in the connection map
        if not connection_id_tuple in self.connection_map:
            # creates a new fast cgi connection
            connection = FastCgiConnection(connection_type, connection_arguments)

            # establishes the connection
            connection.establish_connection()

            # adds the connection to the connection map
            self.connection_map[connection_id_tuple] = connection

        # retrieves the connection
        connection = self.connection_map[connection_id_tuple]

        # returns the connection
        return connection

class FastCgiConnection:
    """
    The fast cgi connection class.
    """

    connection_type = INTERNET_CONNECTION_TYPE
    """ The connection type """

    connection_arguments = ()
    """ The connection arguments """

    socket = None
    """ The established connection socket """

    request_id = 1
    """ The current request id """

    record_lock = None
    """ The record lock """

    record_buffer_map = {}
    """ The record buffer map """

    def __init__(self, connection_type = INTERNET_CONNECTION_TYPE, connection_arguments = ()):
        """
        Constructor of the class.

        @type connection_type: int
        @param connection_type: The connection type.
        @type connection_arguments: Object
        @param connection_arguments: The connection arguments.
        """

        self.connection_type = connection_type
        self.connection_arguments = connection_arguments

        self.record_lock = threading.Lock()
        self.record_buffer_map = {}

    def establish_connection(self):
        """
        Establishes the connection with the host.
        """

        # in case the connection is of type internet
        if self.connection_type == INTERNET_CONNECTION_TYPE:
            # creates the socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # in case the connection is of type unix
        elif self.connection_type == UNIX_CONNECTION_TYPE:
            # creates the socket
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) #@UndefinedVariable

        # connects the socket using the connection arguments
        self.socket.connect(self.connection_arguments)

    def add_record(self, request_id, request_type, record_data):
        # retrieves the record data length
        record_data_length = len(record_data)

        # constructs the header data
        header_data = struct.pack(FCGI_HEADER_STRUCT, FCGI_VERSION_1_VALUE, request_type, request_id, record_data_length, 0)

        # sends the record
        self.socket.sendall(header_data + record_data)

    def get_record(self, request_id):
        """
        Retrieves a record for the given request id.

        @type request_id: int
        @param request_id: The request id to retrieve the record.
        """

        # acquire the record lock
        self.record_lock.acquire()

        # retrieves the record list from the record buffer map
        record_list = self.record_buffer_map.get(request_id, None)

        # in case the record list is valid
        if record_list:
            # retrieves the last record from the record list
            record = record_list.pop()
        else:
            # retrieves a record for the given request id
            record = self._get_record(request_id)

        # releases the record lock
        self.record_lock.release()

        # returns the record
        return record

    def _get_record(self, target_request_id):
        """
        Retrieves a record from the socket

        @type target_request_id: int
        @param target_request_id: The target request id of the record.
        @rtype: Tuple
        @return: The record tuple.
        """

        # iterates indefinitely
        while True:
            # retrieves the header data
            header_data = self.socket.recv(FCGI_HEADER_LENGTH)

            # unpacks the header data
            version, type, request_id, content_length, padding_length = struct.unpack(FCGI_HEADER_STRUCT, header_data)

            # retrieves the contents
            contents = self.socket.recv(content_length)

            # in case there is padding
            if padding_length:
                # retrieves the padding
                self.socket.recv(padding_length)

            # creates the record as a tuple
            record = (
                version,
                type,
                request_id,
                content_length,
                padding_length,
                contents
            )

            # in case the request id is the same as the target
            # request id
            if request_id == target_request_id:
                # breaks the cycle
                break
            else:
                # inserts the record into the buffer
                self._insert_record_in_buffer(record, request_id)

        # returns the record
        return record

    def increment_request_id(self):
        """
        Increments the requst id.
        """

        # increments the request id
        self.request_id += 1

        # returns the current request id
        return self.request_id

    def get_connection_type(self):
        """
        Retrieves the connection type.

        @rtype: int
        @return: The connection type.
        """

        return self.connection_type

    def set_connection_type(self, connection_type):
        """
        Sets the connection type.

        @type connection_type: int
        @param connection_type: The connection type.
        """

        self.connection_type = connection_type

    def get_connection_arguments(self):
        """
        Retrieves the connection arguments.

        @rtype: Object
        @return: The connection arguments.
        """

        return self.connection_arguments

    def set_connection_arguments(self, connection_arguments):
        """
        Sets the connection arguments.

        @type connection_arguments: Object
        @param connection_arguments: The connection arguments.
        """

        self.connection_arguments = connection_arguments

    def get_socket(self):
        """
        Retrieves the established connection socket.

        @rtype: Socket
        @return: The established connection socket.
        """

        return self.socket

    def set_socket(self, socket):
        """
        Sets the established connection socket.

        @type socket: Socket
        @param socket: The established connection socket.
        """

        self.socket = socket

    def get_request_id(self):
        """
        Retrieves the current request id.

        @rtype: int
        @return: The current request id.
        """

        return self.request_id

    def set_request_id(self, request_id):
        """
        Sets the current request id.

        @type request_id: int
        @param request_id: The current request id.
        """

        self.request_id = request_id

    def _insert_record_in_buffer(self, record, request_id):
        """
        Inserts a record in buffer, for the given request id.

        @type record: Tuple
        @param record: The record to be inserted.
        @type request_id: int
        @param request_id: The id of the request to be inserted.
        """

        # in case the request id is not defined in the record
        # buffer map
        if not request_id in self.record_buffer_map:
            # creates a new record list in the record buffer map
            self.record_buffer_map[request_id] = []

        # retrieves the record list for the request id
        record_list = self.record_buffer_map[request_id]

        # inserts the record in the record list
        record_list.insert(0, record)
