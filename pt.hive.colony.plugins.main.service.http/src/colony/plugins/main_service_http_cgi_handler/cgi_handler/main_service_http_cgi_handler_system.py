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

import os
import types
import subprocess

import main_service_http_cgi_handler_exceptions

HANDLER_NAME = "cgi"
""" The handler name """

BASE_PATH_VALUE = "base_path"
""" The base path value """

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

META_HEADER_NAME_PREFIX = "HTTP_"
""" The meta header name prefix """

DEFAULT_CONTENT_TYPE = "text/plain"
""" The default content type """

DEFAULT_APPLICATION_CONTENT_TYPE = "application/x-www-form-urlencoded"
""" The default application content type """

DEFAULT_CONTENT_LENGTH = "0"
""" The default content length """

DEFAULT_STATUS = 200
""" The default status """

DEFAULT_PATH = "~/cgi-bin"
""" The default path """

WINDOWS_CONTENT_HANDLERS_MAP = {
    "py" : "python.exe",
    "py.sh" : "python.exe"
}
""" The windows content handlers map """

class MainServiceHttpCgiHandler:
    """
    The main service http cgi handler class.
    """

    main_service_http_cgi_handler_plugin = None
    """ The main service http cgi handler plugin """

    def __init__(self, main_service_http_cgi_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_cgi_handler_plugin: MainServiceHttpCgiHandlerPlugin
        @param main_service_http_cgi_handler_plugin: The main service http cgi handler plugin.
        """

        self.main_service_http_cgi_handler_plugin = main_service_http_cgi_handler_plugin

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

        # retrieves the request resource path
        request_resource_path = request.get_resource_path_decoded()

        # retrieves the request server identifier protocol version
        request_server_identifier = request.get_server_identifier()

        # retrieves the request handler path
        request_handler_path = request.handler_path

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

        # retrieves the operative system name
        os_name = os.name

        # in case the operative system is windows
        if os_name == "nt" or os_name == "dos":
            # retrieves the request filename base value
            request_filename_base = os.path.basename(request_filename)

            # retrieves the request file extension
            request_file_extension = request_filename_base.split(".", 1)[-1]

            # sets the windows content handler
            handler = WINDOWS_CONTENT_HANDLERS_MAP.get(request_file_extension, "")
        else:
            # sets the empty handler (default)
            handler = ""

        # in case there is a valid handler path
        if request_handler_path:
            request_path = request_resource_path.replace(request_handler_path, "", 1)
        else:
            request_path = request_resource_path

        # retrieves the base directory for file search
        base_directory = request.properties.get(BASE_PATH_VALUE, DEFAULT_PATH)

        # retrieves the real base directory
        real_base_directory = self.main_service_http_cgi_handler_plugin.resource_manager_plugin.get_real_string_value(base_directory)

        # constructs the complete path
        complete_path = real_base_directory + "/" + request_path

        # creates the complete command
        complete_command = handler + " " + complete_path

        # in case the path exists
        if os.path.exists(complete_path):
            # retrieves the environment map
            environment_map = os.environ

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

            # resets the python path to avoid collisions
            environment_map[PYTHONPATH_VALUE] = ""

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

            # iterates over all the environment values and keys
            for environment_key, environment_value in environment_map.items():
                # retrieves the environment value type
                environment_value_type = type(environment_value)

                # in case the environment value type is not string
                if not environment_value_type == types.StringType:
                    # sets the string value in the environment map
                    environment_map[environment_key] = str(environment_value)

            # creates the process executing the command
            process = subprocess.Popen(complete_command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True, env = environment_map)

            # retrieves the standard output data and the standard error data
            stdout_data, stderr_data = process.communicate(request_contents)

            # replaces the extra carriage returns, normalizing the data
            stdout_data = stdout_data.replace("\r\r\n", "\r\n")

            # retrieves the return code
            return_code = process.returncode

            # in case there is a return code different than zero and contents in the standard error data
            if return_code and not stderr_data == "":
                # raises the cgi script error exception
                raise main_service_http_cgi_handler_exceptions.CgiScriptError(stderr_data)

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
                raise main_service_http_cgi_handler_exceptions.InvalidCgiData("problem parsing the cgi data")

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
                raise main_service_http_cgi_handler_exceptions.InvalidCgiHeader("problem parsing the cgi header")

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

            # returns
            return

        # raises the request not handled exception
        raise main_service_http_cgi_handler_exceptions.RequestNotHandled("no cgi handler could handle the request")
