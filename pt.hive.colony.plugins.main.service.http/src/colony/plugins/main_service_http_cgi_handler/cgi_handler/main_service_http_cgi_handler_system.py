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

CONTENT_TYPE_VALUE = "Content-type"
""" The content type value """

STATUS_VALUE = "Status"
""" The status value """

DEFAULT_CONTENT_TYPE = "text/plain"
""" The default content type """

DEFAULT_APPLICATION_CONTENT_TYPE = "application/x-www-form-urlencoded"
""" The default application content type """

DEFAULT_STATUS = 200
""" The default status """

DEFAULT_PATH = "~/cgi-bin"
""" The default path """

WINDOWS_CONTENT_HANDLERS_MAP = {"py" : "python.exe"}
""" The windows content handlers map """

GATEWAY_INTERFACE_VALUE = "CGI/1.0"
""" The gateway interface value """

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
        # reads the request contents
        request_contents = request.read()

        # retrieves the request contents length
        request_contents_length = len(request_contents)

        # retrieves the request file name
        request_filename = request.filename

        # retrieves the request http client service task
        request_http_client_service_task = request.http_client_service_task

        # retrieves the request operation type
        request_operation_type = request.operation_type

        # retrieves the request protocol version
        request_protocol_version = request.protocol_version

        # retrieves the request arguments
        request_arguments = request.arguments

        # retrieves the request http address
        request_http_address = request_http_client_service_task.http_address

        # retrieves the client hostname and port
        client_http_address, _client_http_port = request_http_address

        # retrieves the operative system name
        os_name = os.name

        # in case the operative system is windows
        if os_name == "nt" or os_name == "dos":
            # retrieves the request file extension
            request_file_extension = request_filename.split(".")[-1]

            # sets the windows content handler
            handler = WINDOWS_CONTENT_HANDLERS_MAP.get(request_file_extension, "")
        else:
            # sets the empty handler (default)
            handler = ""

        # sets the base directory for file search
        base_directory = request.properties.get("base_path", DEFAULT_PATH)

        # retrieves the real base directory
        real_base_directory = self.main_service_http_cgi_handler_plugin.resource_manager_plugin.get_real_string_value(base_directory)

        # constructs the complete path
        complete_path = real_base_directory + "/" + request_filename

        # creates the complete command
        complete_command = handler + " " + complete_path

        # in case the path exists
        if os.path.exists(complete_path):
            # retrieves the environment map
            environment_map = os.environ

            environment_map["SERVER_SOFTWARE"] = "colony_http"
            environment_map["SERVER_NAME"] = "localhost"
            environment_map["GATEWAY_INTERFACE"] = GATEWAY_INTERFACE_VALUE
            environment_map["SERVER_PROTOCOL"] = "HTTP/" + request_protocol_version
            environment_map["SERVER_PORT"] = "80"
            environment_map["REQUEST_METHOD"] = request_operation_type
            environment_map["PATH_INFO"] = request_filename
            environment_map["PATH_TRANSLATED"] = request_filename
            environment_map["SCRIPT_NAME"] = request_filename
            environment_map["QUERY_STRING"] = request_arguments
            environment_map["REMOTE_HOST"] = client_http_address
            environment_map["REMOTE_ADDR"] = client_http_address
            environment_map["CONTENT_TYPE"] = DEFAULT_APPLICATION_CONTENT_TYPE
            environment_map["CONTENT_LENGTH"] = str(request_contents_length)

            # resets the python path to avoid collisions
            environment_map["PYTHONPATH"] = ""

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

            # in case there is contents in the standard error data
            if not stderr_data == "":
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
            content_type = headers_map.get(CONTENT_TYPE_VALUE, DEFAULT_CONTENT_TYPE)

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
