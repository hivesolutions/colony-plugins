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

DEFAULT_STATUS = 200
""" The default status """

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

        # retrieves the environment map
        enviroment_map = os.environ

        enviroment_map["SERVER_SOFTWARE"] = "colony_http"
        enviroment_map["SERVER_NAME"] = "localhost"
        enviroment_map["GATEWAY_INTERFACE"] = "CGI/1.0"
        enviroment_map["SERVER_PROTOCOL"] = "HTTP/1.1"
        enviroment_map["SERVER_PORT"] = "80"
        enviroment_map["REQUEST_METHOD"] = request.operation_type
        enviroment_map["PATH_INFO"] = ""
        enviroment_map["PATH_TRANSLATED"] = ""
        enviroment_map["SCRIPT_NAME"] = "test"
        enviroment_map["QUERY_STRING"] = ""
        enviroment_map["REMOTE_HOST"] = "localhost"
        enviroment_map["REMOTE_ADDR"] = "127.0.0.1"
        enviroment_map["CONTENT_TYPE"] = "application/x-www-form-urlencoded"
        enviroment_map["CONTENT_LENGTH"] = str(request_contents_length)

        # creates the process
        process = subprocess.Popen("C:/Programs/Python26/python.exe c:/script.cgi", stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True, env = enviroment_map)

        # retrieves the standard output data and the standard error data
        stdout_data, _stderr_data =  process.communicate(request_contents)

        # splits the standard output data
        stdout_data_splitted = stdout_data.split("\r\n\r\n")

        # retrieves the header string from the first part
        # of the standard output data
        header_string = stdout_data_splitted[0]

        # retrieves the contents joining the second part
        # of the splitted standard output data
        contents = "".join(stdout_data_splitted[1:])

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

        # raises the request not handled exception
        #raise main_service_http_cgi_handler_exceptions.RequestNotHandled("no cgi handler could handle the request")
