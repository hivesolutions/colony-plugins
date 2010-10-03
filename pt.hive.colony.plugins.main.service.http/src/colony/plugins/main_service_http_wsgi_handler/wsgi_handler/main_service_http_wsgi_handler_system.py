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

HANDLER_NAME = "wsgi"
""" The handler name """

CONTENT_TYPE_HEADER_VALUE = "Content-Type"
""" The content type value """

CONTENT_LENGTH_HEADER_VALUE = "Content-Length"
""" The content length value """

WSGI_INPUT_VALUE = "wsgi.input"
""" The wsgi input value """

WSGI_ERRORS_VALUE = "wsgi.errors"
""" The wsgi errors value """

WSGI_VERSION_VALUE = "wsgi.version"
""" The wsgi version value """

WSGI_MULTITHREAD_VALUE = "wsgi.multithread"
""" The wsgi multithread value """

WSGI_MULTIPROCESS_VALUE = "wsgi.multiprocess"
""" The wsgi multiprocess value """

WSGI_RUN_ONCE_VALUE = "wsgi.run_once"
""" The wsgi run once value """

SERVER_SOFTWARE_VALUE = "SERVER_SOFTWARE"
""" The server software value """

SERVER_NAME_VALUE = "SERVER_NAME"
""" The server name value """

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

DEFAULT_CONTENT_TYPE = "text/plain"
""" The default content type """

DEFAULT_APPLICATION_CONTENT_TYPE = "application/x-www-form-urlencoded"
""" The default application content type """

DEFAULT_CONTENT_LENGTH = "0"
""" The default content length """

def hello_application(environment_map, start_response):
    """
    A simple hello world application object.

    @type environment_map: Dictionary
    @param environment_map: The map of environment settings.
    @type start_response: Method
    @param start_response: The start response function, to be called upon
    the start of the response.
    @rtype: List
    @return: The list of return values to be read.
    """

    # sets the status value
    status = "200 OK"

    # creates the response headers list
    response_headers = [(CONTENT_TYPE_HEADER_VALUE, DEFAULT_CONTENT_TYPE)]

    # starts the response
    start_response(status, response_headers)

    # returns the return values
    return ["Hello World"]

class MainServiceHttpWsgiHandler:
    """
    The main service http wsgi handler class.
    """

    main_service_http_wsgi_handler_plugin = None
    """ The main service http wsgi handler plugin """

    def __init__(self, main_service_http_wsgi_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_wsgi_handler_plugin: MainServiceHttpWsgiHandlerPlugin
        @param main_service_http_wsgi_handler_plugin: The main service http wsgi handler plugin.
        """

        self.main_service_http_wsgi_handler_plugin = main_service_http_wsgi_handler_plugin

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

        # sets the current environment items as the initial
        # environment map
        environment_map = dict(os.environ.items())

        # sets the wsgi attributes in the environment map
        environment_map[WSGI_INPUT_VALUE] = request
        environment_map[WSGI_ERRORS_VALUE] = request
        environment_map[WSGI_VERSION_VALUE] = (1, 0)
        environment_map[WSGI_MULTITHREAD_VALUE] = False
        environment_map[WSGI_MULTIPROCESS_VALUE] = True
        environment_map[WSGI_RUN_ONCE_VALUE] = True

        # sets the cgi attributes in the environment map
        environment_map[SERVER_SOFTWARE_VALUE] = request_server_identifier
        environment_map[SERVER_NAME_VALUE] = ""
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

        def start_response(status, response_headers, exc_info = None):
            #if exc_info:
            #    try:
            #        if headers_sent:
                        # Re-raise original exception if headers sent
            #            raise exc_info[0], exc_info[1], exc_info[2]
            #    finally:
            #        exc_info = None     # avoid dangling circular ref
            #elif headers_set:
            #    raise AssertionError("Headers already set!")

            # retrieves the status code string and the status message
            # splitting the status value
            status_code_string, _status_message = status.split(" ", 1)

            # converts the status code string to integer
            status_code = int(status_code_string)

            # sets the request status code
            request.status_code = status_code

            # converts the response headers map
            response_headers_map = dict(response_headers)

            # iterates over all the response
            for response_header_name, response_header_value in response_headers:
                # sets the header in the request
                request.set_header(response_header_name, response_header_value)

            # retrieves the content type
            content_type = response_headers_map.get(CONTENT_TYPE_HEADER_VALUE, DEFAULT_CONTENT_TYPE)

            # sets the request content type
            request.content_type = content_type

            # returns the default write method
            return request.write

        # calls the hello application retrieving the results
        result = hello_application(environment_map, start_response)

        # iterates over all the data in the result
        # to write it to the request
        for data in result:
            # writes the data to the request
            request.write(data)
