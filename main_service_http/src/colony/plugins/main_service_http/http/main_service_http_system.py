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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import sys
import time
import copy
import types
import base64
import datetime
import traceback

import colony.libs.map_util
import colony.libs.file_util
import colony.libs.quote_util
import colony.libs.structures_util
import colony.libs.string_buffer_util

import main_service_http_exceptions

RESOLUTION_ORDER_ITEMS = (
    "virtual_servers",
    "redirections",
    "contexts"
)
""" The items to be used in the resolution order """

PREFIX_VALUE = "http://"
""" The prefix to be used for default connections """

SECURE_PREFIX_VALUE = "https://"
""" The prefix to be used for the secure connections """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

MULTIPART_FORM_DATA_VALUE = "multipart/form-data"
""" The multipart form data value """

WWW_FORM_URLENCODED_VALUE = "application/x-www-form-urlencoded"
""" The www form urlencoded value """

OCTET_STREAM_VALUE = "application/octet-stream"
""" The octet stream value """

CONNECTION_TYPE = "connection"
""" The connection type """

BIND_HOST = ""
""" The bind host value """

SERVICE_TYPE = "async"
""" The service type """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 3
""" The request timeout """

RESPONSE_TIMEOUT = 3
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

SERVER_NAME = "Hive-Colony-Web"
""" The server name """

SERVER_VERSION = "1.0.0"
""" The server version """

ENVIRONMENT_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
""" The environment version """

SERVER_IDENTIFIER = SERVER_NAME + "/" + SERVER_VERSION + " (python/" + sys.platform + "/" + ENVIRONMENT_VERSION + ")"
""" The server identifier """

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

DEFAULT_PORT = 8080
""" The default port """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_VALUE = "default"
""" The default value """

VALID_VALUE = "valid"
""" The valid value """

STATUS_CODE_VALUES = {
    100 : "Continue",
    101 : "Switching Protocols",
    200 : "OK",
    201 : "Created",
    202 : "Accepted",
    203 : "Non-Authoritative Information",
    204 : "No Content",
    205 : "Reset Content",
    206 : "Partial Content",
    207 : "Multi-Status",
    301 : "Moved permanently",
    302 : "Found",
    303 : "See Other",
    304 : "Not Modified",
    305 : "Use Proxy",
    306 : "(Unused)",
    307 : "Temporary Redirect",
    400 : "Bad Request",
    401 : "Unauthorized",
    402 : "Payment Required",
    403 : "Forbidden",
    404 : "Not Found",
    405 : "Method Not Allowed",
    406 : "Not Acceptable",
    407 : "Proxy Authentication Required",
    408 : "Request Timeout",
    409 : "Conflict",
    410 : "Gone",
    411 : "Length Required",
    412 : "Precondition Failed",
    413 : "Request Entity Too Large",
    414 : "Request-URI Too Long",
    415 : "Unsupported Media Type",
    416 : "Requested Range Not Satisfiable",
    417 : "Expectation Failed",
    500 : "Internal Server Error",
    501 : "Not Implemented",
    502 : "Bad Gateway",
    503 : "Service Unavailable",
    504 : "Gateway Timeout",
    505 : "HTTP Version Not Supported"
}
""" The status code values map """

DEFAULT_STATUS_CODE_VALUE = "Invalid"
""" The default status code value """

HOST_VALUE = "Host"
""" The host value """

DATE_VALUE = "Date"
""" The date value """

ETAG_VALUE = "ETag"
""" The etag value """

EXPIRES_VALUE = "Expires"
""" The expires value """

LOCATION_VALUE = "Location"
""" The location value """

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

AUTHORIZATION_VALUE = "Authorization"
""" The authorization value """

IF_MODIFIED_SINCE_VALUE = "If-Modified-Since"
""" The if modified since value """

IF_NONE_MATCH_VALUE = "If-None-Match"
""" The if none match value """

WWW_AUTHENTICATE_VALUE = "WWW-Authenticate"
""" The www authenticate value """

CHUNKED_VALUE = "chunked"
""" The chunked value """

KEEP_ALIVE_LOWER_VALUE = "keep-alive"
""" The keep alive lower value """

UPGRADE_LOWER_VALUE = "upgrade"
""" The upgrade lower value """

KEEP_ALIVE_VALUE = "Keep-Alive"
""" The keep alive value """

CACHE_CONTROL_VALUE = "Cache-Control"
""" The cache control value """

CONTENT_DISPOSITION_VALUE = "Content-Disposition"
""" The content disposition value """

WEB_SOCKET_VALUE = "WebSocket"
""" The web socket """

NAME_VALUE = "name"
""" The name value """

CONTENTS_VALUE = "contents"
""" The contents value """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

MAX_AGE_FORMAT = "max-age=%d"
""" The template describing the max age cache value """

ENCODING_VALUE = "encoding"
""" The encoding value """

ENCODING_HANDLER_VALUE = "encoding_handler"
""" The encoding handler value """

LOG_FILE_VALUE = "log_file"
""" The log file value """

RESOLUTION_ORDER_VALUE = "resolution_order"
""" The resolution order value """

RESOLUTION_ORDER_REGEX_VALUE = "resolution_order_regex"
""" The resolution order regex value """

DEFAULT_CONTENT_TYPE_CHARSET_VALUE = "default_content_type_charset"
""" The default content type charset value """

DEFAULT_CACHE_CONTROL_VALUE = "no-cache, must-revalidate"
""" The default cache control value """

UPGRADE_MESSAGE_SIZE_MAP = {
    WEB_SOCKET_VALUE : 8
}
""" The upgrade message size map """

class MainServiceHttp:
    """
    The main service http class.
    """

    main_service_http_plugin = None
    """ The main service http plugin """

    http_service_handler_plugins_map = {}
    """ The http service handler plugins map """

    http_service_encoding_plugins_map = {}
    """ The http service encoding plugins map """

    http_service_authentication_handler_plugins_map = {}
    """ The http service authentication handler plugins map """

    http_service_error_handler_plugins_map = {}
    """ The http service error handler plugins map """

    http_service = None
    """ The http service reference """

    http_log_file = None
    """ The log file """

    http_service_configuration = {}
    """ The http service configuration """

    def __init__(self, main_service_http_plugin):
        """
        Constructor of the class.

        @type main_service_http_plugin: MainServiceHttpPlugin
        @param main_service_http_plugin: The main service http plugin.
        """

        self.main_service_http_plugin = main_service_http_plugin

        self.http_service_handler_plugin_map = {}
        self.http_service_encoding_plugins_map = {}
        self.http_service_authentication_handler_plugins_map = {}
        self.http_service_error_handler_plugins_map = {}
        self.http_service_configuration = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the main service utils plugin
        main_service_utils_plugin = self.main_service_http_plugin.main_service_utils_plugin

        # generates the parameters
        service_parameters = self._generate_service_parameters(parameters)

        # generates the http service using the given service parameters
        self.http_service = main_service_utils_plugin.generate_service(service_parameters)

        # starts the http service
        self.http_service.start_service()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to stop the service.
        """

        # destroys the parameters
        self._destroy_service_parameters(parameters)

        # starts the http service
        self.http_service.stop_service()

    def http_service_handler_load(self, http_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = http_service_handler_plugin.get_handler_name()

        self.http_service_handler_plugins_map[handler_name] = http_service_handler_plugin

    def http_service_handler_unload(self, http_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = http_service_handler_plugin.get_handler_name()

        del self.http_service_handler_plugins_map[handler_name]

    def http_service_encoding_load(self, http_service_encoding_plugin):
        # retrieves the plugin encoding name
        encoding_name = http_service_encoding_plugin.get_encoding_name()

        self.http_service_encoding_plugins_map[encoding_name] = http_service_encoding_plugin

    def http_service_encoding_unload(self, http_service_encoding_plugin):
        # retrieves the plugin encoding name
        encoding_name = http_service_encoding_plugin.get_encoding_name()

        del self.http_service_encoding_plugins_map[encoding_name]

    def http_service_authentication_handler_load(self, http_service_authentication_handler_plugin):
        # retrieves the plugin handler name
        handler_name = http_service_authentication_handler_plugin.get_handler_name()

        self.http_service_authentication_handler_plugins_map[handler_name] = http_service_authentication_handler_plugin

    def http_service_authentication_handler_unload(self, http_service_authentication_handler_plugin):
        # retrieves the plugin handler name
        handler_name = http_service_authentication_handler_plugin.get_handler_name()

        del self.http_service_authentication_handler_plugins_map[handler_name]

    def http_service_error_handler_load(self, http_service_error_handler_plugin):
        # retrieves the plugin error handler name
        error_handler_name = http_service_error_handler_plugin.get_error_handler_name()

        self.http_service_error_handler_plugins_map[error_handler_name] = http_service_error_handler_plugin

    def http_service_error_handler_unload(self, http_service_error_handler_plugin):
        # retrieves the plugin error handler name
        error_handler_name = http_service_error_handler_plugin.get_error_handler_name()

        del self.http_service_error_handler_plugins_map[error_handler_name]

    def set_service_configuration_property(self, service_configuration_property):
        # retrieves the service configuration
        service_configuration = service_configuration_property.get_data()

        # iterates over all the resolution order items (the ones
        # that contain a resolution order field)
        for resolution_order_item in RESOLUTION_ORDER_ITEMS:
            # retrieves the resolution order item value
            resolution_order_item_value = service_configuration.get(resolution_order_item, None)

            # in case the resolution order item value is not set
            if not resolution_order_item_value:
                # continues the loop
                continue

            # retrieves the resolution order values
            resolution_order = resolution_order_item_value.get(RESOLUTION_ORDER_VALUE, resolution_order_item_value.keys())

            # creates the regex buffer
            regex_buffer = colony.libs.string_buffer_util.StringBuffer()

            # sets the is first flag
            is_first = True

            # iterates over all the resolution order items
            for resolution_order_item in resolution_order:
                # in case the is first flag
                # is set
                if is_first:
                    # unsets the is first flag
                    is_first = False
                # otherwise
                else:
                    # writes the or separator token
                    regex_buffer.write("|")

                # writes the resolution order item value
                regex_buffer.write("(" + resolution_order_item + ")")

            # retrieves the regex value
            regex_value = regex_buffer.get_value()

            # compiles the regex value
            regex = re.compile(regex_value)

            # sets the resolution order regex value in the resolution order item
            # value map
            resolution_order_item_value[RESOLUTION_ORDER_REGEX_VALUE] = regex

        # cleans the http service configuration
        colony.libs.map_util.map_clean(self.http_service_configuration)

        # copies the service configuration to the http service configuration
        colony.libs.map_util.map_copy(service_configuration, self.http_service_configuration)

    def unset_service_configuration_property(self):
        # cleans the http service configuration
        colony.libs.map_util.map_clean(self.http_service_configuration)

    def _get_service_configuration(self):
        """
        Retrieves the service configuration map.

        @rtype: Dictionary
        @return: The service configuration map.
        """

        return self.http_service_configuration

    def _get_encoding_handler(self, encoding):
        # in case no encoding is defined
        if not encoding:
            # returns none
            return None

        # in case the encoding is not found in the http service
        # encoding handler plugins map
        if not encoding in self.http_service_encoding_plugins_map:
            # raises the encoding not found exception
            raise main_service_http_exceptions.EncodingNotFound("encoding %s not found" % encoding)

        # retrieves the http service encoding handler plugin
        http_service_encoding_plugin = self.http_service_encoding_plugins_map[encoding]

        # retrieves the encode contents method as the encoding handler
        encoding_handler = http_service_encoding_plugin.encode_contents

        # returns the encoding handler
        return encoding_handler

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

        # retrieves the plugin manager
        plugin_manager = self.main_service_http_plugin.manager

        # retrieves the end points value
        end_points = parameters.get("end_points", [])

        # retrieves the socket provider value
        socket_provider = parameters.get("socket_provider", None)

        # retrieves the port value
        port = parameters.get("port", DEFAULT_PORT)

        # retrieves the encoding value
        encoding = parameters.get("encoding", None)

        # retrieves the socket parameters value
        socket_parameters = parameters.get("socket_parameters", {})

        # retrieves the service configuration
        service_configuration = self._get_service_configuration()

        # retrieves the various service configuration values using
        # the default values for each of the configuration items
        end_points = service_configuration.get("default_end_points", end_points)
        socket_provider = service_configuration.get("default_socket_provider", socket_provider)
        port = service_configuration.get("default_port", port)
        encoding = service_configuration.get("default_encoding", encoding)
        socket_parameters = service_configuration.get("default_socket_parameters", socket_parameters)
        service_type = service_configuration.get("default_service_type", SERVICE_TYPE)
        client_connection_timeout = service_configuration.get("default_client_connection_timeout", CLIENT_CONNECTION_TIMEOUT)
        connection_timeout = service_configuration.get("default_connection_timeout", REQUEST_TIMEOUT)
        request_timeout = service_configuration.get("default_request_timeout", REQUEST_TIMEOUT)
        response_timeout = service_configuration.get("default_response_timeout", RESPONSE_TIMEOUT)
        number_threads = service_configuration.get("default_number_threads", NUMBER_THREADS)
        scheduling_algorithm = service_configuration.get("default_scheduling_algorithm", SCHEDULING_ALGORITHM)
        maximum_number_threads = service_configuration.get("default_maximum_number_threads", MAXIMUM_NUMBER_THREADS)
        maximum_number_work_threads = service_configuration.get("default_maximum_number_work_threads", MAXIMUM_NUMBER_WORKS_THREAD)
        work_scheduling_algorithm = service_configuration.get("default_work_scheduling_algorithm", WORK_SCHEDULING_ALGORITHM)
        http_log_file_path = service_configuration.get("log_file_path", None)

        # resolves the http  log file path using the plugin manager
        http_log_file_path = plugin_manager.resolve_file_path(http_log_file_path, True, True)

        # creates the http log file (using a file rotator)
        self.http_log_file = http_log_file_path and colony.libs.file_util.FileRotator(http_log_file_path) or None

        # opens the http log file
        self.http_log_file and self.http_log_file.open()

        # retrieves the encoding handler for the given encoding
        encoding_handler = self._get_encoding_handler(encoding)

        # creates the pool configuration map
        pool_configuration = {
            "name" : "http pool",
            "description" : "pool to support http client connections",
            "number_threads" : number_threads,
            "scheduling_algorithm" : scheduling_algorithm,
            "maximum_number_threads" : maximum_number_threads,
            "maximum_number_works_thread" : maximum_number_work_threads,
            "work_scheduling_algorithm" : work_scheduling_algorithm
        }

        # creates the extra parameters map
        extra_parameters = {
            "encoding" : encoding,
            "encoding_handler" : encoding_handler,
            "log_file" : self.http_log_file
        }

        # creates the parameters map
        parameters = {
            "type" : CONNECTION_TYPE,
            "service_plugin" : self.main_service_http_plugin,
            "service_handling_task_class" : HttpClientServiceHandler,
            "end_points" : end_points,
            "socket_provider" : socket_provider,
            "bind_host" : BIND_HOST,
            "port" : port,
            "socket_parameters" : socket_parameters,
            "chunk_size" : CHUNK_SIZE,
            "service_configuration" : service_configuration,
            "extra_parameters" :  extra_parameters,
            "pool_configuration" : pool_configuration,
            "service_type" : service_type,
            "client_connection_timeout" : client_connection_timeout,
            "connection_timeout" : connection_timeout,
            "request_timeout" : request_timeout,
            "response_timeout" : response_timeout
        }

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

        # closes the http log file
        self.http_log_file and self.http_log_file.close()

class HttpClientServiceHandler:
    """
    The http client service handler class.
    """

    service_plugin = None
    """ The service plugin """

    service_connection_handler = None
    """ The service connection handler """

    service_configuration = None
    """ The service configuration """

    service_utils_exception_class = None
    """ The service utils exception class """

    encoding = None
    """ The encoding """

    encoding_handler = None
    """ The encoding handler """

    content_type_charset = DEFAULT_CHARSET
    """ The content type charset """

    log_file = None
    """ The log file """

    service_connection_request_handler_map = {}
    """ The map associating the service connection with the request handler (method) """

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

        self.service_connection_request_handler_map = {}

        self.encoding = extra_parameters.get(ENCODING_VALUE, None)
        self.encoding_handler = extra_parameters.get(ENCODING_HANDLER_VALUE, None)
        self.log_file = extra_parameters.get(LOG_FILE_VALUE, None)
        self.content_type_charset = self.service_configuration.get(DEFAULT_CONTENT_TYPE_CHARSET_VALUE, DEFAULT_CHARSET)

    def handle_opened(self, service_connection):
        pass

    def handle_closed(self, service_connection):
        # retrieves the current request (being handled)
        request = service_connection.request_data.get("_request", None)

        # in case the request is not defined
        # (no request pending)
        if not request:
            # returns immediately
            return

        # in case the request is mediated (there
        # must be a mediated handler)
        if request.is_mediated():
            # closes the mediated handler in order
            # to avoid possible resource leak
            request.mediated_handler.close()
        # in case the request is mediated (there
        # must be a chunk handler)
        elif request.is_chunked_encoded():
            # closes the chunk handler in order
            # to avoid possible resource leak
            request.chunk_handler.close()

    def handle_request(self, service_connection, request = None):
        # retrieves the request handler using the service connection request handler map
        request_handler = self.service_connection_request_handler_map.get(service_connection, self.default_request_handler)

        # handles the service connection with the request handler
        return request_handler(service_connection, request)

    def default_request_handler(self, service_connection, request = None):
        # retrieves the http service handler plugins map
        http_service_handler_plugins_map = self.service_plugin.main_service_http.http_service_handler_plugins_map

        try:
            # retrieves the request
            request = request or self.retrieve_request(service_connection)
        except main_service_http_exceptions.MainServiceHttpException:
            # prints a debug message about the connection closing
            self.service_plugin.debug("Connection: %s closed by peer, timeout or invalid request" % str(service_connection))

            # returns false (connection closed)
            return False

        try:
            # prints debug message about request
            self.service_plugin.debug("Handling request: %s" % str(request))

            # verifies the request information, tries to find any possible
            # security problem in it
            self._verify_request_information(request)

            # retrieves the real service configuration,
            # taking the request information into account
            service_configuration = self._get_service_configuration(request)

            # processes the authentication for the request
            self._process_authentication(request, service_configuration)

            # processes the redirection information in the request
            self._process_redirection(request, service_configuration)

            # processes the handler part of the request and retrieves
            # the handler name
            handler_name = self._process_handler(request, service_configuration)

            # processes the (force) domain and secure parts of the request, this
            # actions may trigger an automatic redirection of the request
            self._process_domain(request, service_connection, service_configuration)
            self._process_secure(request, service_connection, service_configuration)

            # in case the request was not already handled
            if not handler_name:
                # retrieves the default handler name
                handler_name = service_configuration.get("default_handler", None)

                # sets the handler path
                request.handler_path = None

            # in case no handler name is defined (request not handled)
            if not handler_name:
                # raises an http no handler exception
                raise main_service_http_exceptions.HttpNoHandlerException("no handler defined for current request")

            # in case the handler is not found in the handler plugins map
            if not handler_name in http_service_handler_plugins_map:
                # raises an http handler not found exception
                raise main_service_http_exceptions.HttpHandlerNotFoundException("no handler found for current request: " + handler_name)

            # retrieves the http service handler plugin
            http_service_handler_plugin = http_service_handler_plugins_map[handler_name]

            # handles the request by the request handler, only in case the
            # request does not already contains a status code (in such case the
            # request is considered to be already processed)
            not request.status_code and http_service_handler_plugin.handle_request(request)

            # sets the request information in the request data of
            # the service connection (provides indirect access)
            service_connection.request_data["_request"] = request

            # checks if the request is delayed
            request_delayed = request.delayed

            # in case the request is of type delayed it should be processed (contents
            # send) after
            if request_delayed:
                # processes the request as delayed, retrieving the return
                # value (connection closed value)
                return_value = self.process_delayed(request, service_connection)
            # otherwise the request is not delayed processes the request (immediately)
            else:
                # processes the request normally, retrieving the return
                # value (connection closed value)
                return_value = self.process_request(request, service_connection)
        except Exception, exception:
            # processes the exception, retrieving the return
            # value (connection closed value)
            return_value = self.process_exception(request, service_connection, exception)

        # runs the logging steps for the request
        self._log(request)

        # in case the return value is invalid the connection
        # is meant to be closed (no need to process any extra
        # information)
        if not return_value:
            # returns false (connection closed)
            return False

        # checks if the service connection is of type asynchronous
        service_connection_is_async = service_connection.is_async()

        # in case there is pending data and the service connection is of
        # type asynchronous calls the default request handler to handle the
        # remaining data (allows http pipelining)
        service_connection.pending_data() and not service_connection_is_async and self.default_request_handler(service_connection)

        # returns true (connection remains open)
        return True

    def process_delayed(self, request, service_connection):
        # retrieves the request timeout from the service connection
        service_connection_request_timeout = service_connection.connection_request_timeout

        # prints a debug message
        self.service_plugin.debug("Connection: %s kept alive for %ss for delayed request" % (str(service_connection), str(service_connection_request_timeout)))

        # returns true (connection meant to be kept alive)
        return True

    def process_request(self, request, service_connection):
        try:
            # sends the request to the client (response)
            self.send_request(service_connection, request)
        except main_service_http_exceptions.HttpRuntimeException, exception:
            # prints a warning message message
            self.service_plugin.warning("Runtime problem: %s, while sending request" % unicode(exception))

            # returns false (connection closed)
            return False
        except main_service_http_exceptions.MainServiceHttpException:
            # prints a debug message
            self.service_plugin.debug("Connection: %s closed by peer, while sending request" % str(service_connection))

            # returns false (connection closed)
            return False

        # in case the connection is not meant to be kept alive
        if not self.keep_alive(request):
            # prints a debug message
            self.service_plugin.debug("Connection: %s closed, not meant to be kept alive" % str(service_connection))

            # runs the logging steps for the request
            self._log(request)

            # returns false (connection closed)
            return False

        # retrieves the request timeout from the service connection
        service_connection_request_timeout = service_connection.connection_request_timeout

        # prints a debug message
        self.service_plugin.debug("Connection: %s kept alive for %ss" % (str(service_connection), str(service_connection_request_timeout)))

        # returns true (connection meant to be kept alive)
        return True

    def process_exception(self, request, service_connection, exception):
        # prints info message about exception
        self.service_plugin.info("There was an exception handling the request: " + unicode(exception))

        try:
            # sends the exception
            self.send_exception(service_connection, request, exception)
        except main_service_http_exceptions.MainServiceHttpException:
            # prints a debug message
            self.service_plugin.debug("Connection: %s closed by peer, while sending exception" % str(service_connection))

            # returns false (connection closed)
            return False
        except Exception, exception:
            # prints an error message
            self.service_plugin.debug("There was an exception handling the exception: " + unicode(exception))

        # returns true (connection meant to be kept alive)
        return True

    def _log(self, request):
        # in case the log file is not defined
        # or in case it's closed
        if not self.log_file or self.log_file.closed:
            # returns immediately
            return

        # retrieves the service connection
        service_connection = request.service_connection

        # retrieves the connection information
        # from the service connection
        connection_host, _connection_port =  service_connection.connection_address

        # retrieves the user id
        user_id = "-"

        # retrieves the operation type
        operation_type = request.operation_type

        # retrieves the requested resource path
        resource_path = request.get_resource_path_decoded()

        # retrieves the protocol version
        protocol_version = request.protocol_version

        # retrieves the status code
        status_code = request.status_code

        # retrieves the content length (default to minus one or invalid)
        content_length = request.content_length or 0

        # retrieves the current date time value
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time
        current_date_time_formatted = current_date_time.strftime("%d/%b/%Y:%H:%M:%S +0000")

        # creates the log line value
        log_line_value = "%s - %s [%s] \"%s %s %s\" %d %d\n" % (connection_host, user_id, current_date_time_formatted, operation_type, resource_path, protocol_version, status_code, content_length)

        # writes the log line value to the log file
        self.log_file.write(log_line_value)

    def retrieve_request(self, service_connection):
        """
        Retrieves the request from the received message.
        This method block until the complete request
        message is received.
        This method is not compatible with async communication.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @rtype: HttpRequest
        @return: The request from the received message.
        """

        # continuous loop
        while True:
            try:
                # in case there is pending data to be read
                # (the pending data buffer is not empty)
                if service_connection.pending_data():
                    # sets the data as the pending data
                    data = service_connection.pop_pending_data()
                # otherwise (read normally)
                else:
                    # receives the data
                    data = service_connection.receive()
            except self.service_utils_exception_class:
                # raises the http data retrieval exception
                raise main_service_http_exceptions.HttpDataRetrievalException("problem retrieving data")

            # in case no valid data was received
            if data == "":
                # raises the http invalid data exception
                raise main_service_http_exceptions.HttpInvalidDataException("empty data received")

            # tries to retrieve the request using the retrieved data
            request = self.retrieve_request_data(service_connection, data)

            # in case the request is not valid (not enough data for parsing)
            if not request:
                # continues the loop
                continue

            # breaks the loop
            break

        # returns the request
        return request

    def retrieve_request_data(self, service_connection, data = None):
        """
        Retrieves the request from the received message.
        This method retrieves the request using only the
        provided data value.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type String: data
        @param String: The data to be used in processing the request.
        @rtype: HttpRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = service_connection.request_data.get("message", colony.libs.string_buffer_util.StringBuffer())

        # creates a request object
        request = service_connection.request_data.get("request", HttpRequest(self, service_connection, self.content_type_charset))

        # creates the start line loaded flag
        start_line_loaded = service_connection.request_data.get("start_line_loaded", False)

        # creates the header loaded flag
        header_loaded = service_connection.request_data.get("header_loaded", False)

        # creates the message loaded flag
        message_loaded = service_connection.request_data.get("message_loaded", False)

        # creates the message offset index, representing the
        # offset byte to the initialization of the message
        message_offset_index = service_connection.request_data.get("message_offset_index", 0)

        # creates the message size value
        message_size = service_connection.request_data.get("message_size", 0)

        # creates the received data size (counter)
        received_data_size = service_connection.request_data.get("received_data_size", 0)

        # initializes the start line index
        start_line_index = service_connection.request_data.get("start_line_index", 0)

        # initializes the end header index
        end_header_index = service_connection.request_data.get("end_header_index", 0)

        # sets the "initial" return request to invalid
        return_request = None

        # sets the "continue" process flag
        process_flag = True

        # retrieves the data length
        data_length = len(data)

        # increments the received data size (counter)
        received_data_size += data_length

        # writes the data to the string buffer
        message.write(data)

        # in case the header is not loaded or the message contents are completely loaded
        if not header_loaded or received_data_size >= message_offset_index + message_size:
            # retrieves the message value from the string buffer
            message_value = message.get_value()
        # in case there's no need to inspect the message contents
        else:
            # unsets the process flag
            process_flag = False

        # in case the start line is not loaded
        if process_flag and not start_line_loaded:
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

                # in case the length of the splitted line is not valid
                if not start_line_splitted_length == 3:
                    # raises the http invalid data exception
                    raise main_service_http_exceptions.HttpInvalidDataException("invalid data received: " + start_line)

                # retrieve the operation type the path and the protocol version
                # from the start line splitted
                operation_type, path, protocol_version = start_line_splitted

                # sets the request operation type
                request.set_operation_type(operation_type)

                # sets the request path
                request.set_path(path)

                # sets the request protocol version
                request.set_protocol_version(protocol_version)

                # sets the start line loaded flag
                start_line_loaded = True

        # in case the header is not loaded
        if process_flag and not header_loaded:
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
                    request.headers_in[header_name] = header_value

                # parses the get attributes, this will load
                # the attributes associated with the url
                request.__parse_get_attributes__()

                # in case the content length is defined in the headers map
                if CONTENT_LENGTH_VALUE in request.headers_map:
                    # retrieves the message size
                    message_size = int(request.headers_map[CONTENT_LENGTH_VALUE])
                elif CONTENT_LENGTH_LOWER_VALUE in request.headers_map:
                    # retrieves the message size
                    message_size = int(request.headers_map[CONTENT_LENGTH_LOWER_VALUE])
                elif UPGRADE_VALUE in request.headers_map:
                    # retrieves the upgrade (type) value
                    upgrade = request.headers_map[UPGRADE_VALUE]

                    # in case the upgrade (type) exists in the
                    # upgrade message size map
                    if upgrade in UPGRADE_MESSAGE_SIZE_MAP:
                        # retrieves the message size for the upgrade (type)
                        message_size = UPGRADE_MESSAGE_SIZE_MAP[upgrade]
                    # otherwise
                    else:
                        # sets the message size to zero (not set)
                        message_size = 0

                        # sets the return request as the request (valid), then
                        # unsets the process flag and sets the message as loaded
                        return_request = request
                        process_flag = False
                        message_loaded = True

                # in case there is no content length defined in the headers map
                else:
                    # sets the message size to zero (not set)
                    message_size = 0

                    # sets the return request as the request (valid), then
                    # unsets the process flag and sets the message as loaded
                    return_request = request
                    process_flag = False
                    message_loaded = True

        # in case the header is not loaded
        if process_flag and not message_loaded and header_loaded:
            # retrieves the start message size
            start_message_index = end_header_index + 4

            # retrieves the message value length
            message_value_length = len(message_value)

            # calculates the message value message length
            message_value_message_length = message_value_length - start_message_index

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
                self.decode_request(request)

                # sets the return request as the request (valid), then
                # unsets the process flag and sets the message as loaded
                return_request = request
                process_flag = False
                message_loaded = True

        # in case the message is not yet loaded (not enought data)
        if not message_loaded:
            # saves the various state values representing the current
            # request parsing state
            service_connection.request_data["message"] = message
            service_connection.request_data["request"] = request
            service_connection.request_data["start_line_loaded"] = start_line_loaded
            service_connection.request_data["header_loaded"] = header_loaded
            service_connection.request_data["message_loaded"] = message_loaded
            service_connection.request_data["message_offset_index"] = message_offset_index
            service_connection.request_data["message_size"] = message_size
            service_connection.request_data["received_data_size"] = received_data_size
            service_connection.request_data["start_line_index"] = start_line_index
            service_connection.request_data["end_header_index"] = end_header_index

            # returns the empty (request)
            return return_request

        # "resets" the request data map
        service_connection.request_data = {}

        # calculates the complete message size
        complete_message_size = message_size + message_offset_index

        # in case the received data size is larger than
        # the complete message size
        if received_data_size > complete_message_size:
            # retrieves the pending data
            pending_data = message_value[complete_message_size:]

            # adds the pending data to the service connection
            service_connection.add_pending_data(pending_data)

        # returns the return request request
        return return_request

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

                # in case the content is of type octet stream
                if content_type_item_stripped.startswith(OCTET_STREAM_VALUE):
                    # returns immediately
                    return

                # in case the content is of type multipart form data
                if content_type_item_stripped.startswith(MULTIPART_FORM_DATA_VALUE):
                    # parses the request as multipart
                    request.parse_post_multipart()

                    # returns immediately
                    return

                # in case the content is of type www form urlencoded
                if content_type_item_stripped.startswith(WWW_FORM_URLENCODED_VALUE):
                    # parses the request attributes
                    request.parse_post_attributes()

                    # returns immediately
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

        try:
            # decodes the message value into unicode using the given charset
            request.received_message = received_message_value.decode(content_type_charset)
        except:
            # sets the received message as the original one (fallback procedure)
            request.received_message = received_message_value

    def send_exception(self, service_connection, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type request: HttpRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # retrieves the preferred error handlers list
        preferred_error_handlers_list = self.service_configuration.get("preferred_error_handlers", (DEFAULT_VALUE,))

        # retrieves the http service error handler plugins map
        http_service_error_handler_plugins_map = self.service_plugin.main_service_http.http_service_error_handler_plugins_map

        # iterates over all the preferred error handlers
        for preferred_error_handler in preferred_error_handlers_list:
            # in case the preferred error handler is the default one
            if preferred_error_handler == DEFAULT_VALUE:
                # handles the error with the default error handler
                self.default_error_handler(request, exception)

                # breaks the loop
                break
            else:
                # in case the preferred error handler exist in the http service
                # error handler plugins map
                if preferred_error_handler in http_service_error_handler_plugins_map:
                    # retrieves the http service error handler plugin
                    http_service_error_handler_plugin = http_service_error_handler_plugins_map[preferred_error_handler]

                    # calls the handle error in the http service error handler plugin
                    http_service_error_handler_plugin.handle_error(request, exception)

                    # breaks the loop
                    break

        # sends the request to the client (response)
        self.send_request(service_connection, request)

    def send_request(self, service_connection, request):
        # in case the encoding is defined
        if self.encoding:
            # sets the encoded flag
            request.encoded = True

            # sets the encoding handler
            request.set_encoding_handler(self.encoding_handler)

            # sets the encoding name
            request.set_encoding_name(self.encoding)

        # in case the request is mediated
        if request.is_mediated():
            self.send_request_mediated(service_connection, request)
        # in case the request is chunked encoded
        elif request.is_chunked_encoded():
            self.send_request_chunked(service_connection, request)
        # otherwise it's a simple request
        else:
            self.send_request_simple(service_connection, request)

    def send_request_simple(self, service_connection, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            service_connection.send(result_value)
        except self.service_utils_exception_class, exception:
            # error in the client side
            self.service_plugin.error("Problem sending request simple: " + unicode(exception))

            # raises the http data sending exception
            raise main_service_http_exceptions.HttpDataSendingException("problem sending data")

    def send_request_mediated(self, service_connection, request):
        # checks if the service connection is of type asynchronous
        service_connection_is_async = service_connection.is_async()

        # in case the service connection is of type asynchronous
        # (the asynchronous handler should be used)
        if service_connection_is_async:
            # sends the request mediated using the asynchronous handler
            self.send_request_mediated_async(service_connection, request)
        # otherwise the "normal" synchronous handler is used
        else:
            # sends the request mediated using the synchronous handler
            self.send_request_mediated_sync(service_connection, request)

    def send_request_mediated_async(self, service_connection, request):
        def request_mediated_writer(send_error = False):
            # in case there was an error sending
            # the data
            if send_error:
                # closes the mediated handler
                request.mediated_handler.close()

                # returns immediately
                return

            try:
                # retrieves the mediated value
                mediated_value = request.mediated_handler.get_chunk(CHUNK_SIZE)

                # in case the read is complete (time to close
                # the currently open mediated handler)
                if not mediated_value:
                    # prints a debug message
                    self.service_plugin.debug("Completed transfer of request mediated")

                    # closes the mediated handler
                    request.mediated_handler.close()

                    # returns (no more writing)
                    return

                try:
                    # sends the mediated value to the client (writes in front of the others)
                    # and sets the callback as the current writer
                    service_connection.send_callback(mediated_value, request_mediated_writer, write_front = True)
                except self.service_utils_exception_class, exception:
                    # error in the client side
                    self.service_plugin.error("Problem sending request mediated: " + unicode(exception))

                    # raises the http data sending exception
                    raise main_service_http_exceptions.HttpDataSendingException("problem sending data")
            except:
                # closes the mediated handler
                request.mediated_handler.close()

                # re-raises the exception
                raise

        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client and sets the request
            # mediated writer as the callback handler
            service_connection.send_callback(result_value, request_mediated_writer)
        except self.service_utils_exception_class, exception:
            # error in the client side
            self.service_plugin.error("Problem sending request mediated: " + unicode(exception))

            # closes the mediated handler
            request.mediated_handler.close()

            # raises the http data sending exception
            raise main_service_http_exceptions.HttpDataSendingException("problem sending data")

    def send_request_mediated_sync(self, service_connection, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            service_connection.send(result_value)
        except self.service_utils_exception_class, exception:
            # error in the client side
            self.service_plugin.error("Problem sending request mediated: " + unicode(exception))

            # closes the mediated handler
            request.mediated_handler.close()

            # raises the http data sending exception
            raise main_service_http_exceptions.HttpDataSendingException("problem sending data")

        # continuous loop
        while True:
            try:
                # retrieves the mediated value
                mediated_value = request.mediated_handler.get_chunk(CHUNK_SIZE)

                # in case the read is complete (time to close
                # the currently open mediated handler)
                if not mediated_value:
                    # prints a debug message
                    self.service_plugin.debug("Completed transfer of request mediated")

                    # closes the mediated handler
                    request.mediated_handler.close()

                    # breaks the cycle
                    break

                try:
                    # sends the mediated value to the client
                    service_connection.send(mediated_value)
                except self.service_utils_exception_class, exception:
                    # error in the client side
                    self.service_plugin.error("Problem sending request mediated: " + unicode(exception))

                    # raises the http data sending exception
                    raise main_service_http_exceptions.HttpDataSendingException("problem sending data")
            except:
                # closes the mediated handler
                request.mediated_handler.close()

                # re-raises the exception
                raise

    def send_request_chunked(self, service_connection, request):
        # checks if the service connection is of type asynchronous
        service_connection_is_async = service_connection.is_async()

        # in case the service connection is of type asynchronous
        # (the asynchronous handler should be used)
        if service_connection_is_async:
            # sends the request chunked using the asynchronous handler
            self.send_request_chunked_async(service_connection, request)
        # otherwise the "normal" synchronous handler is used
        else:
            # sends the request chunked using the synchronous handler
            self.send_request_chunked_sync(service_connection, request)

    def send_request_chunked_async(self, service_connection, request):
        def request_chunked_writer(send_error = False):
            # in case there was an error sending
            # the data
            if send_error:
                # closes the chunk handler
                request.chunk_handler.close()

                # returns immediately
                return

            try:
                # retrieves the chunk value
                chunk_value = request.chunk_handler.get_chunk(CHUNK_SIZE)

                # in case the read is complete (time to close
                # the currently open chunk handler)
                if not chunk_value:
                    # closes the chunk handler
                    request.chunk_handler.close()

                    try:
                        # sends the final empty chunk
                        service_connection.send("0\r\n\r\n")
                    except self.service_utils_exception_class, exception:
                        # error in the client side
                        self.service_plugin.error("Problem sending request chunked (final chunk): " + unicode(exception))

                        # raises the http data sending exception
                        raise main_service_http_exceptions.HttpDataSendingException("problem sending data")

                    # returns immediately
                    return

                try:
                    # retrieves the length of the chunk value
                    length_chunk_value = len(chunk_value)

                    # sets the value for the hexadecimal length part of the chunk
                    length_chunk_value_hexadecimal_string = "%X\r\n" % length_chunk_value

                    # sets the message value
                    message_value = length_chunk_value_hexadecimal_string + chunk_value + "\r\n"

                    # sends the message value to the client (writes in front of the others)
                    # and sets the callback as the current writer
                    service_connection.send_callback(message_value, request_chunked_writer, write_front = True)
                except self.service_utils_exception_class, exception:
                    # error in the client side
                    self.service_plugin.error("Problem sending request chunked: " + unicode(exception))

                    # raises the http data sending exception
                    raise main_service_http_exceptions.HttpDataSendingException("problem sending data")
            except:
                # closes the chunk handler
                request.chunk_handler.close()

                # re-raises the exception
                raise

        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client and sets the request
            # chunked writer as the callback handler
            service_connection.send_callback(result_value, request_chunked_writer)
        except self.service_utils_exception_class, exception:
            # error in the client side
            self.service_plugin.error("Problem sending request chunked: " + unicode(exception))

            # closes the chunk handler
            request.chunk_handler.close()

            # raises the http data sending exception
            raise main_service_http_exceptions.HttpDataSendingException("problem sending data")

        # calls the initial request chunked writer
        # for the initial writing (start of loop)
        request_chunked_writer()

    def send_request_chunked_sync(self, service_connection, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            service_connection.send(result_value)
        except self.service_utils_exception_class, exception:
            # error in the client side
            self.service_plugin.error("Problem sending request chunked: " + unicode(exception))

            # closes the chunk handler
            request.chunk_handler.close()

            # raises the http data sending exception
            raise main_service_http_exceptions.HttpDataSendingException("problem sending data")

        # continuous loop
        while True:
            try:
                # retrieves the chunk value
                chunk_value = request.chunk_handler.get_chunk(CHUNK_SIZE)

                # in case the read is complete (time to close
                # the currently open chunk handler)
                if not chunk_value:
                    # closes the chunk handler
                    request.chunk_handler.close()

                    try:
                        # sends the final empty chunk
                        service_connection.send("0\r\n\r\n")
                    except self.service_utils_exception_class, exception:
                        # error in the client side
                        self.service_plugin.error("Problem sending request chunked (final chunk): " + unicode(exception))

                        # raises the http data sending exception
                        raise main_service_http_exceptions.HttpDataSendingException("problem sending data")

                    # breaks the cycle
                    break

                try:
                    # retrieves the length of the chunk value
                    length_chunk_value = len(chunk_value)

                    # sets the value for the hexadecimal length part of the chunk
                    length_chunk_value_hexadecimal_string = "%X\r\n" % length_chunk_value

                    # sets the message value
                    message_value = length_chunk_value_hexadecimal_string + chunk_value + "\r\n"

                    # sends the message value to the client
                    service_connection.send(message_value)
                except self.service_utils_exception_class, exception:
                    # error in the client side
                    self.service_plugin.error("Problem sending request chunked: " + unicode(exception))

                    # raises the http data sending exception
                    raise main_service_http_exceptions.HttpDataSendingException("problem sending data")
            finally:
                # closes the chunk handler
                request.chunk_handler.close()

                # re-raises the exception
                raise

    def keep_alive(self, request):
        """
        Retrieves the value of the keep alive for the given request.

        @type request: HttpRequest
        @param request: The request to retrieve the keep alive value.
        @rtype: bool
        @return: The value of the keep alive for the given request.
        """

        # in case connection is defined in the headers map
        if CONNECTION_VALUE in request.headers_map:
            # retrieves the connection type
            connection_type = request.headers_map[CONNECTION_VALUE]

            # retrieves the connection type fields, by splitting
            # the connection type and stripping the values
            connection_type_fields = [value.strip() for value in connection_type.split(",")]

            # iterates over all the connection type fields
            for connection_type_field in connection_type_fields:
                # in case the connection is meant to be kept alive
                # or in case is of type upgrade
                if connection_type_field.lower() in (KEEP_ALIVE_LOWER_VALUE, UPGRADE_LOWER_VALUE):
                    # returns true
                    return True

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
        status_code_value = request.get_status_code_value()

        # writes the header message in the message
        request.write("colony web server - " + str(request.status_code) + " " + status_code_value + "\n")

        # writes the error message
        request.write("error: '" + unicode(error) + "'\n")

        # writes the traceback message in the request
        request.write("traceback:\n")

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            # creates the (initial) formated traceback
            formated_traceback = traceback.format_tb(traceback_list)

            # retrieves the file system encoding
            file_system_encoding = sys.getfilesystemencoding()

            # decodes the traceback values using the file system encoding
            formated_traceback = [value.decode(file_system_encoding) for value in formated_traceback]
        # otherwise there is no traceback list
        else:
            # sets an empty formated traceback
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

    def set_service_connection_request_handler(self, service_connection, request_handler_method):
        """
        Sets a "custom" request handler method for the given service connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to have the
        "custom" request handler method associated.
        @type request_handler_method: Method
        @param request_handler_method: The method to be used in the handling
        of the request.
        """

        self.service_connection_request_handler_map[service_connection] = request_handler_method

    def unset_service_connection_request_handler(self, service_connection, request_handler_method):
        """
        Unsets a "custom" request handler method for the given service connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to have the "custom"
        request handler method association removed.
        """

        del self.service_connection_request_handler_map[service_connection]

    def _process_redirection(self, request, service_configuration):
        """
        Processes the redirection stage of the http request.
        Processing redirection implies matching the path against the
        rules.

        @type request: HttpRequest
        @param request: The request to be processed.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        """

        # retrieves the service configuration redirections
        service_configuration_redirections = service_configuration.get("redirections", {})

        # retrieves the service configuration redirections resolution order
        service_configuration_redirections_resolution_order = service_configuration_redirections.get(RESOLUTION_ORDER_VALUE, service_configuration_redirections.keys())

        # (saves) the old path as the base path
        request.set_base_path(request.path)

        # unsets the request handler base path
        request.handler_base_path = None

        # iterates over the service configuration redirection names
        for service_configuration_redirection_name in service_configuration_redirections_resolution_order:
            # in case the path is found in the request path
            if request.path.find(service_configuration_redirection_name) == 0:
                # sets the handler base path
                request.handler_base_path = service_configuration_redirection_name

                # retrieves the service configuration redirection
                service_configuration_redirection = service_configuration_redirections[service_configuration_redirection_name]

                # retrieves the target path and the recursive redirection
                # flag value for context resolution
                target_path = service_configuration_redirection.get("target", service_configuration_redirection_name)
                recursive_redirection = service_configuration_redirection.get("recursive_redirection", False)

                # retrieves the sub request path as the request from the redirection name path
                # in front
                sub_request_path = request.path[len(service_configuration_redirection_name):]

                # in case the recursive redirection is disabled and there is a subdirectory
                # in the sub request path
                if not recursive_redirection and not sub_request_path.find("/") == -1:
                    # breaks the loop because the request is not meant to be recursively redirected
                    # and it contains a sub-directory
                    break

                # retrieves the new (redirected) path in the request
                # strips both parts of the path to avoid problems with duplicated slashes
                request_path = target_path.rstrip("/") + "/" + sub_request_path.lstrip("/")

                # sets the new path in the request, avoids the overriding
                # of the original path by unsetting the flag
                request.set_path(request_path, set_original_path = False)

                # sets the redirect configuration in the request as the current
                # service configuration (still pending redirect confirmation, it
                # will be confirmed in the process redirection)
                request.redirect_configuration = service_configuration_redirection

                # sets the redirection validation flag and the the
                # redirected flag in the request
                request.redirection_validation = True
                request.redirected = True

                # breaks the loop
                break

    def _process_domain(self, request, service_connection, service_configuration):
        """
        Processes the forcing of the connection to be made in the defined
        domain, running this method allows the connection to be redirected
        to a certain domain in case such behavior is required.

        @type request: HttpRequest
        @param request: The request to be processed.
        @type service_connection: ServiceConnection
        @param service_connection: The service connection currently in use.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        """

        # retrieves the service configuration context name and value from the request and the service configuration
        _service_configuration_context_name, service_configuration_context = self._get_request_service_configuration_context(request, service_configuration)

        # retrieves the "default" value for the force domain
        # from the service configuration and then "joins"
        # them with the "context" specific values
        force_domain = service_configuration.get("force_domain", None)
        force_domain = service_configuration_context.get("force_domain", force_domain)

        # in case the request was redirected and the redirect configuration
        # is currently set in the request, need to to retrieve the domain
        # information from the redirect configuration
        if request.redirected and request.redirect_configuration:
            # retrieves the redirect configuration map from the request
            # in order to process its values
            redirect_configuration = request.redirect_configuration

            # tries to retrieve the force domain information from the
            # redirect configuration
            force_domain = redirect_configuration.get("force_domain", force_domain)

        # in case the force domain value is not set no need to
        # proceed with the processing of it, returns immediately
        if not force_domain: return

        # checks if the current service connection is secure (encrypted)
        # then uses it to retrieve the proper prefix value for the location
        is_secure = service_connection.is_secure()
        prefix = is_secure and SECURE_PREFIX_VALUE or PREFIX_VALUE

        # retrieves the original (raw) path to be used in the construction
        # of the new (domain processed) url
        original_path = request.original_path

        # construct the url (new location) with the prefix and using the
        # port part of the value in case a non default secure port is defined
        location = service_connection.connection_port in (80, 443) and prefix + force_domain + original_path or prefix + force_domain + ":" + str(service_connection.connection_port) + original_path

        # sets the status code in the request and then sets the location header
        # (using the location value)
        request.status_code = 302
        request.set_header(LOCATION_VALUE, location)

    def _process_secure(self, request, service_connection, service_configuration):
        """
        Processes the forcing of the connection as secure, running
        this method allows the connection to be redirected to a secure
        channel in case such behavior is required.

        @type request: HttpRequest
        @param request: The request to be processed.
        @type service_connection: ServiceConnection
        @param service_connection: The service connection currently in use.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        """

        # retrieves the service configuration context name and value from the request and the service configuration
        _service_configuration_context_name, service_configuration_context = self._get_request_service_configuration_context(request, service_configuration)

        # retrieves the "default" values for the force secure and
        # secure port from the service configuration and then "joins"
        # them with the "context" specific values
        force_secure = service_configuration.get("force_secure", False)
        secure_port = service_configuration.get("secure_port", 443)
        force_secure = service_configuration_context.get("force_secure", force_secure)
        secure_port = service_configuration_context.get("secure_port", secure_port)

        # in case the request was redirected and the redirect configuration
        # is currently set in the request, need to to retrieve the secure
        # information from the redirect configuration
        if request.redirected and request.redirect_configuration:
            # retrieves the redirect configuration map from the request
            # in order to process its values
            redirect_configuration = request.redirect_configuration

            # tries to retrieve the force secure and the secure port information
            # from the redirect configuration
            force_secure = redirect_configuration.get("force_secure", force_secure)
            secure_port = redirect_configuration.get("secure_port", secure_port)

        # in case the force secure flag is not set no need to process the
        # redirection process, returns immediately
        if not force_secure: return

        # in case the service connection port is the same as the port defined
        # as secure, no need to process the redirection the connection is
        # already considered as secure
        if service_connection.connection_port == secure_port: return

        # retrieves the host value from the request headers
        # in order to be able to construct the new full secure
        # address
        host = request.headers_map.get(HOST_VALUE, None)

        # in case the host is not defined, it's not possible
        # to construct the secure url
        if not host:
            # raises the client request security violation exception
            raise main_service_http_exceptions.ClientRequestSecurityViolation("host not defined")

        # retrieves the "hostname" from the host (removing the port part
        # of the name) then retrieves the original (raw) path to be used in the
        # construction of the secure url
        hostname = host.rsplit(":", 1)[0]
        original_path = request.original_path

        # construct the secure url (new location) with the secure prefix and
        # using the port part of the value in case a non default secure port
        # is defined
        location = secure_port == 443 and SECURE_PREFIX_VALUE + hostname + original_path or SECURE_PREFIX_VALUE + hostname + ":" + str(secure_port) + original_path

        # sets the status code in the request and then sets the location header
        # (using the location value)
        request.status_code = 302
        request.set_header(LOCATION_VALUE, location)

    def _get_request_service_configuration_context(self, request, service_configuration):
        # retrieves the service configuration contexts
        service_configuration_contexts = service_configuration.get("contexts", {})

        # retrieves the service configuration contexts resolution order
        service_configuration_contexts_resolution_order = service_configuration_contexts.get(RESOLUTION_ORDER_VALUE, service_configuration_contexts.keys())

        # retrieves the service configuration contexts resolution order regex
        service_configuration_contexts_resolution_order_regex = service_configuration_contexts.get(RESOLUTION_ORDER_REGEX_VALUE, None)

        # in case the request is pending redirection validation
        if request.redirection_validation:
            # the request base path is used as the request path
            # for redirection allowing purposes
            request_path = request.base_path
        # in non redirection validation iteration case
        else:
            # sets the request path as the normal (valid) request
            # path
            request_path = request.path

        # sets the default service configuration context
        service_configuration_context = {}

        # sets the default service configuration context name
        service_configuration_context_name = None

        # in case the service configuration contexts resolution order regex
        # is defined and valid
        if service_configuration_contexts_resolution_order_regex:
            # tries to match the request path with the regex
            request_path_match = service_configuration_contexts_resolution_order_regex.match(request_path)
        else:
            # sets the request path match ad invalid
            request_path_match = None

        # in case there is a valid request path match
        if request_path_match:
            # retrieves the group index from the request path match
            group_index = request_path_match.lastindex

            # retrieves the service configuration context name
            service_configuration_context_name = service_configuration_contexts_resolution_order[group_index - 1]

            # retrieves the service configuration context
            service_configuration_context = service_configuration_contexts[service_configuration_context_name]

        # returns the service configuration context name and value
        return service_configuration_context_name, service_configuration_context

    def _process_handler(self, request, service_configuration):
        """
        Processes the handler stage of the http request.
        Processing handler implies matching the path against the
        various handler rules defined to retrieve the valid handler.

        @type request: HttpRequest
        @param request: The request to be processed.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        @rtype: String
        @return: The processed handler name.
        """

        # retrieves the service configuration context name and value from the request and the service configuration
        service_configuration_context_name, service_configuration_context = self._get_request_service_configuration_context(request, service_configuration)

        # retrieves the allow redirection property
        allow_redirection = service_configuration_context.get("allow_redirection", True)

        # in case the request is pending redirection validation
        if request.redirection_validation:
            # in case it does not allow redirection
            if not allow_redirection:
                # changes the path to the base path, avoids the overriding
                # of the original path by unsetting the flag
                request.set_path(request.base_path, set_original_path = False)

                # unsets the request handler base path
                request.handler_base_path = None

                # unsets the redirected flag in the request
                request.redirected = False

            # unsets the redirection validation flag in the request
            request.redirection_validation = False

            # re-processes the request (to process the real handler)
            return self._process_handler(request, service_configuration)

        # sets the request properties
        request.properties = service_configuration_context.get("request_properties", {})

        # sets the handler path
        request.handler_path = service_configuration_context_name

        # retrieves the handler name
        handler_name = service_configuration_context.get("handler", None)

        # in case the request is pending redirection validation
        if request.redirection_validation:
            # unsets the redirection validation flag in the request
            request.redirection_validation = False

            # re-processes the request (to process the real handler)
            return self._process_handler(request, service_configuration)

        # returns the handler name
        return handler_name

    def _process_authentication(self, request, service_configuration):
        # retrieves the service configuration context name and value from the request and the service configuration
        _service_configuration_context_name, service_configuration_context = self._get_request_service_configuration_context(request, service_configuration)

        # retrieves the authentication handler
        authentication_handler = service_configuration_context.get("authentication_handler", None)

        # in case no authentication handler is defined (no
        # authentication is required)
        if not authentication_handler:
            # returns immediately
            return

        # retrieves the authentication properties
        authentication_properties = service_configuration_context.get("authentication_properties", {})

        # retrieves the authentication realm
        authentication_realm = authentication_properties.get("authentication_realm", "default")

        # retrieves the authorization from the request headers
        authorization = request.headers_map.get(AUTHORIZATION_VALUE, None)

        # in case no authorization is defined
        if not authorization:
            # sets the location header
            request.set_header(WWW_AUTHENTICATE_VALUE, "Basic realm=\"" + authentication_realm + "\"")

            # raises the unauthorized exception
            raise main_service_http_exceptions.UnauthorizedException("authentication required", 401)

        # retrieves the authorization type and value
        _authorization_type, authorization_value = authorization.split(" ", 1)

        # decodes the authorization value
        authorization_value_decoded = base64.b64decode(authorization_value)

        # split the authorization value retrieving the username and password
        username, password = authorization_value_decoded.split(":", 1)

        # retrieves the http service authentication handler plugins map
        http_service_authentication_handler_plugins_map = self.service_plugin.main_service_http.http_service_authentication_handler_plugins_map

        # in case the authentication handler is not found in the http service authentication
        # handler plugins map
        if not authentication_handler in http_service_authentication_handler_plugins_map:
            # raises the http authentication handler not found exception
            raise main_service_http_exceptions.HttpAuthenticationHandlerNotFoundException("no authentication handler found for current request: " + authentication_handler)

        # retrieves the http service authentication handler plugin
        http_service_authentication_handler_plugin = http_service_authentication_handler_plugins_map[authentication_handler]

        # uses the authentication handler to try to authenticate
        authentication_result = http_service_authentication_handler_plugin.handle_authentication(username, password, authentication_properties)

        # retrieves the authentication result valid
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication result is not valid
        if not authentication_result_valid:
            # sets the location header
            request.set_header(WWW_AUTHENTICATE_VALUE, "Basic realm=\"Secure Area\"")

            # raises the unauthorized exception
            raise main_service_http_exceptions.UnauthorizedException("user is not permitted: " + username, 401)

    def _verify_request_information(self, request):
        """
        Verifies the request information, checking if there is
        any possible security problems associated.

        @type request: HttpRequest
        @param request: The request to be verified.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # retrieves the verify request flag
        verify_request = service_configuration.get("verify_request", True)

        # in case the request is not meant to be verified
        if not verify_request:
            # returns immediately
            return

        # retrieves the host value from the request headers
        host = request.headers_map.get(HOST_VALUE, None)

        # in case the host is not defined
        if not host:
            # raises the client request security violation exception
            raise main_service_http_exceptions.ClientRequestSecurityViolation("host not defined")

        # retrieves the allowed host map
        allowed_hosts = service_configuration.get("allowed_hosts", {})

        # retrieves the "hostname" from the host
        hostname = host.rsplit(":", 1)[0]

        # tries to retrieve the host from the allowed hosts map
        host_allowed = allowed_hosts.get(hostname, False)

        # in case the host is not allowed
        if not host_allowed:
            # raises the client request security violation exception
            raise main_service_http_exceptions.ClientRequestSecurityViolation("host not allowed: " + hostname)

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        @type request: HttpRequest
        @param request: The request to be used in the resolution
        of the service configuration.
        @rtype: Dictionary
        @return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # retrieves the host value from the request headers
        host = request.headers_map.get(HOST_VALUE, None)

        # in case the host is defined
        if host:
            # retrieves the virtual servers map
            service_configuration_virtual_servers = service_configuration.get("virtual_servers", {})

            # retrieves the service configuration virtual servers resolution order
            service_configuration_virtual_servers_resolution_order = service_configuration_virtual_servers.get(RESOLUTION_ORDER_VALUE, service_configuration_virtual_servers.keys())

            # splits the host value (to try
            # to retrieve hostname and port)
            host_splitted = host.split(":")

            # retrieves the host splitted length
            host_splitted_length = len(host_splitted)

            # in case the host splitted length is two
            if host_splitted_length == 2:
                # retrieves the hostname and the port
                hostname, _port = host_splitted
            else:
                # sets the hostname as the host (size one)
                hostname = host

            # in case the hostname exists in the service configuration virtual servers map
            if hostname in service_configuration_virtual_servers:
                # iterates over the service configuration virtual server names
                for service_configuration_virtual_server_name in service_configuration_virtual_servers_resolution_order:
                    # in case this is the hostname
                    if hostname == service_configuration_virtual_server_name:
                        # retrieves the service configuration virtual server value
                        service_configuration_virtual_server_value = service_configuration_virtual_servers[service_configuration_virtual_server_name]

                        # merges the service configuration map with the service configuration virtual server value,
                        # to retrieve the final service configuration for this request
                        service_configuration = self._merge_values(service_configuration, service_configuration_virtual_server_value)

                        # breaks the loop
                        break

        # returns the service configuration
        return service_configuration

    def _merge_values(self, target_value, source_value):
        """
        Merges two values into one, the type of the values
        is taken into account and the merge only occurs when
        the type is list or dictionary.

        @type target_list: Object
        @param target_list: The target value to be used.
        @type source_list: Object
        @param source_list: The source value to be used.
        @rtype: Object
        @return: The final resulting value.
        """

        # retrieves the types for both the target and
        # the source values
        target_value_type = type(target_value)
        source_value_type = type(source_value)

        # in case both types are the same (no conflict)
        if target_value_type == source_value_type:
            # in case the type is dictionary
            if target_value_type == types.DictType:
                # merges both maps
                return self._merge_maps(target_value, source_value)
            # in case the type is list
            elif target_value_type == types.ListType or target_value_type == types.TupleType:
                # merges both list
                return self._merge_lists(target_value, source_value)
            # in case it's a different type
            else:
                # returns the source value (no possible merge)
                return source_value
        else:
            # returns the source value (no possible merge)
            return source_value

    def _merge_lists(self, target_list, source_list):
        """
        Merges two lists into one, the source list is made
        prioritaire, and is taken into account first.

        @type target_list: List
        @param target_list: The target list to be used.
        @type source_list: List
        @param source_list: The source list to be used.
        @rtype: List
        @return: The final resulting list.
        """

        # creates the final list
        final_list = []

        # extends the list with both lists
        final_list.extend(source_list)
        final_list.extend(target_list)

        # returns the final list
        return final_list

    def _merge_maps(self, target_map, source_map):
        """
        Merges two maps into one, the source map is made
        prioritaire, and is taken into account first.

        @type target_map: Dictionary
        @param target_map: The target map to be used.
        @type source_map: List
        @param source_map: The source map to be used.
        @rtype: List
        @return: The final resulting map.
        """

        # copies the target map as the final map
        final_map = copy.copy(target_map)

        # iterates over all the source map values
        for source_key, source_value in source_map.items():
            # in case the source key exists in the
            # final map, merge is required
            if source_key in final_map:
                # retrieves the target value
                target_value = final_map[source_key]

                # merges both maps returning the final value
                final_value = self._merge_values(target_value, source_value)

                # sets the ginal value in the final map
                final_map[source_key] = final_value
            # otherwise no merge is required
            else:
                # sets the source value in the final map
                final_map[source_key] = source_value

        # returns the final map
        return final_map

class HttpRequest:
    """
    The http request class.
    """

    http_client_service_handler = None
    """ The http client service handler """

    service_connection = None
    """ The service connection """

    operation_type = "none"
    """ The operation type """

    path = "none"
    """ The path """

    original_path = "none"
    """ The original path (without unquoting) """

    base_path = "none"
    """ The base path (before redirection) """

    resource_path = "none"
    """ The resource path """

    resource_base_path = "none"
    """ The resource base path (before redirection) """

    handler_path = "none"
    """ The handler path """

    handler_base_path = "none"
    """ The handler base path (before redirection) """

    filename = "none"
    """ The filename """

    uri = "none"
    """ The uri """

    query_string = ""
    """ The query string value """

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

    received_message = None
    """ The received message """

    content_type = None
    """ The content type """

    message_stream = None
    """ The message stream """

    status_code = None
    """ The status code """

    status_message = None
    """ The status message """

    delayed = False
    """ The delayed flag """

    redirect_configuration = None
    """ The configuration map for the current redirection """

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

    content_length = None
    """ The content length """

    encoding_name = "none"
    """ The encoding name """

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

    max_age = None
    """ The max age cache value """

    expiration_timestamp = None
    """ The expiration timestamp """

    last_modified_timestamp = None
    """ The last modified timestamp """

    contains_message = True
    """ The contains message flag """

    request_time = None
    """ The time when the request started """

    allow_cookies = True
    """ If the setting of cookies through the set cookie header
    is allowed for the current rest request context """

    properties = {}
    """ The properties """

    def __init__(self, http_client_service_handler = None, service_connection = None, content_type_charset = DEFAULT_CHARSET):
        self.http_client_service_handler = http_client_service_handler
        self.service_connection = service_connection
        self.content_type_charset = content_type_charset

        self.request_time = time.time()

        self.attributes_map = colony.libs.structures_util.OrderedMap(True)
        self.headers_map = {}
        self.response_headers_map = {}
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.operation_type, self.path)

    def __getattribute__(self, attribute_name):
        """
        Retrieves the attribute from the attributes map.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        @rtype: Object
        @return: The retrieved attribute.
        """

        return self.attributes_map.get(attribute_name, None)

    def __setattribute__(self, attribute_name, attribute_value):
        """
        Sets the given attribute in the request. The referenced
        attribute is the http request attribute and the setting takes
        into account a possible duplication of the values.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to be set.
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to be set.
        """

        # in case the attribute name is already defined
        # in the attributes map (duplicated reference), it
        # requires a list structure to be used
        if attribute_name in self.attributes_map:
            # retrieves the attribute value reference from the attributes map
            attribute_value_reference = self.attributes_map[attribute_name]

            # retrieves the attribute value reference type
            attribute_value_reference_type = type(attribute_value_reference)

            # in case the attribute value reference type is (already)
            # a list
            if attribute_value_reference_type == types.ListType:
                # adds the attribute value to the attribute value reference
                attribute_value_reference.append(attribute_value)
            # otherwise the attributes is not a list and it must be created
            # for the first time
            else:
                # sets the list with the previously defined attribute reference
                # and the attribute value
                self.attributes_map[attribute_name] = [
                    attribute_value_reference,
                    attribute_value
                ]
        # otherwise the attribute is not defined and a normal
        # set must be done
        else:
            # sets the attribute value in the attributes map
            self.attributes_map[attribute_name] = attribute_value

    def __parse_get_attributes__(self):
        # splits the (original) path to get the attributes path of the request
        path_splitted = self.original_path.split("?")

        # retrieves the size of the split
        path_splitted_length = len(path_splitted)

        # in case there are no arguments to be parsed
        if path_splitted_length < 2:
            return

        # retrieves the query string from the path splitted
        self.query_string = path_splitted[1]

        # sets the arguments as the query string
        self.arguments = self.query_string

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
            attribute_field_splitted = attribute_field.split("=", 1)

            # retrieves the attribute field splitted length
            attribute_field_splitted_length = len(attribute_field_splitted)

            # in case the attribute field splitted length is invalid
            if attribute_field_splitted_length == 0 or attribute_field_splitted_length > 2:
                # continues the loops
                continue

            # in case the attribute field splitted length is two
            if attribute_field_splitted_length == 2:
                # retrieves the attribute name and the attribute value,
                # from the attribute field splitted
                attribute_name, attribute_value = attribute_field_splitted

                # "unquotes" the attribute value from the url encoding
                attribute_value = colony.libs.quote_util.unquote_plus(attribute_value)
            # in case the attribute field splitted length is one
            elif attribute_field_splitted_length == 1:
                # retrieves the attribute name, from the attribute field splitted
                attribute_name, = attribute_field_splitted

                # sets the attribute value to none
                attribute_value = None

            # "unquotes" the attribute name from the url encoding
            attribute_name = colony.libs.quote_util.unquote_plus(attribute_name)

            # sets the attribute value
            self.__setattribute__(attribute_name, attribute_value)

    def parse_multipart(self):
        """
        Parses the multipart using the currently defined multipart value.
        The processing of multipart is done according the standard
        specifications and rfqs.
        """

        # retrieves the content type header
        content_type = self.headers_map.get(CONTENT_TYPE_VALUE, None)

        # in case no content type is defined
        if not content_type:
            # raises the http invalid multipart request exception
            raise main_service_http_exceptions.HttpInvalidMultipartRequestException("no content type defined")

        # splits the content type
        content_type_splitted = content_type.split(";")

        # retrieves the content type value
        content_type_value = content_type_splitted[0].strip()

        # in case the content type value is not valie
        if not content_type_value == MULTIPART_FORM_DATA_VALUE:
            # raises the http invalid multipart request exception
            raise main_service_http_exceptions.HttpInvalidMultipartRequestException("invalid content type defined: " + content_type_value)

        # retrieves the boundary value
        boundary = content_type_splitted[1].strip()

        # splits the boundary
        boundary_splitted = boundary.split("=")

        # in case the length of the boundary is not two (invalid)
        if not len(boundary_splitted) == 2:
            # raises the http invalid multipart request exception
            raise main_service_http_exceptions.HttpInvalidMultipartRequestException("invalid boundary value: " + boundary)

        # retrieves the boundary reference and the boundary value
        _boundary, boundary_value = boundary_splitted

        # retrieves the boundary value length
        boundary_value_length = len(boundary_value)

        # sets the initial index as the as the boundary value length
        # plus the base boundary value of two (equivalent to: --)
        current_index = boundary_value_length + 2

        # iterates indefinitely
        while True:
            # retrieves the end index (boundary start index)
            end_index = self.multipart.find(boundary_value, current_index)

            # in case the end index is invalid (end of multipart)
            if end_index == -1:
                # breaks the cycle
                break

            # parses the multipart part retrieving the headers map and the contents
            # the sent indexes avoid the extra newline values incrementing and decrementing
            # the value of two at the end and start
            headers_map, contents = self._parse_multipart_part(current_index + 2, end_index - 2)

            # parses the content disposition header retrieving the content
            # disposition map and list (with the attributes order)
            content_disposition_map = self._parse_content_disposition(headers_map)

            # sets the contents in the content disposition map
            content_disposition_map[CONTENTS_VALUE] = contents

            # retrieves the name from the content disposition map
            name = content_disposition_map[NAME_VALUE]

            # sets the attribute
            self.__setattribute__(name, content_disposition_map)

            # sets the current index as the end index
            current_index = end_index + boundary_value_length

    def execute_background(self, callable):
        """
        Executes the given callable object in a background
        thread.
        This method is useful for avoid blocking the request
        handling method in non critic tasks.

        @type callable: Callable
        @param callable: The callable to be called in background.
        """

        self.service_connection.execute_background(callable)

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

    def allow_cookies(self):
        self.allow_cookies = True

    def deny_cookies(self):
        self.allow_cookies = False

    def is_mediated(self):
        return self.mediated

    def is_chunked_encoded(self):
        return self.chunked_encoding

    def is_secure(self):
        """
        Checks if the current request is being transmitted over a secure
        channel, the verification is made at a connection abstraction
        level (down socket verification).

        @rtype: bool
        @return: If the current request is being transmitted over a secure
        channel (secure request).
        """

        return self.service_connection.is_secure()

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

    def set_header(self, header_name, header_value, encode = True):
        """
        Set a response header value on the request.

        @type header_name: String
        @param header_name: The name of the header to be set.
        @type header_value: Object
        @param header_value: The value of the header to be sent
        in the response.
        @type encode: bool
        @param encode: If the header value should be encoded in
        case the type is unicode.
        """

        # retrieves the header value type
        header_value_type = type(header_value)

        # in case the header value type is unicode
        # and the encode flag is set
        if header_value_type == types.UnicodeType and encode:
            # encodes the header value with the content type charset
            header_value = header_value.encode(self.content_type_charset)

        # sets the header value in the headers map
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
        """
        Retrieves the result string value of
        the request.

        @rtype: String
        @return: The result string value of
        the request.
        """

        # validates the current request
        self.validate()

        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

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
            self.content_length = self.mediated_handler.get_size()
        else:
            # retrieves the content length from the
            # message content itself
            self.content_length = len(message)

        # retrieves the value for the status code
        status_code_value = self.get_status_code_value()

        # writes the http command in the string buffer (version, status code and status value)
        result.write(self.protocol_version + " " + str(self.status_code) + " " + status_code_value + "\r\n")

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time according to the http specification
        current_date_time_formatted = current_date_time.strftime(DATE_FORMAT)

        # creates the ordered map to hold the header values
        headers_ordered_map = colony.libs.structures_util.OrderedMap()

        if self.content_type:
            headers_ordered_map[CONTENT_TYPE_VALUE] = self.content_type
        if self.encoded:
            headers_ordered_map[CONTENT_ENCODING_VALUE] = self.encoding_name
        if self.chunked_encoding:
            headers_ordered_map[TRANSFER_ENCODING_VALUE] = CHUNKED_VALUE
        if not self.chunked_encoding and self.contains_message and not self.content_length == None:
            headers_ordered_map[CONTENT_LENGTH_VALUE] = str(self.content_length)
        if self.upgrade_mode:
            headers_ordered_map[UPGRADE_VALUE] = self.upgrade_mode
        if self.etag:
            headers_ordered_map[ETAG_VALUE] = self.etag
        if self.max_age:
            headers_ordered_map[CACHE_CONTROL_VALUE] = MAX_AGE_FORMAT % self.max_age
        if self.expiration_timestamp:
            # converts the expiration timestamp to date time and formats it
            # according to the http specification setting it in the headers map
            expiration_date_time = datetime.datetime.fromtimestamp(self.expiration_timestamp)
            expiration_date_time_formatted = expiration_date_time.strftime(DATE_FORMAT)
            headers_ordered_map[EXPIRES_VALUE] = expiration_date_time_formatted
        if self.last_modified_timestamp:
            # converts the last modified timestamp to date time and formats it
            # according to the http specification setting it in the headers map
            last_modified_date_time = datetime.datetime.fromtimestamp(self.last_modified_timestamp)
            last_modified_date_time_formatted = last_modified_date_time.strftime(DATE_FORMAT)
            headers_ordered_map[LAST_MODIFIED_VALUE] = last_modified_date_time_formatted

        # sets the default cache values in the unset header values
        # this should populate all the mandatory fields
        if not CACHE_CONTROL_VALUE in headers_ordered_map:
            headers_ordered_map[CACHE_CONTROL_VALUE] = DEFAULT_CACHE_CONTROL_VALUE

        # sets the base response header values
        headers_ordered_map[CONNECTION_VALUE] = self.connection_mode
        headers_ordered_map[DATE_VALUE] = current_date_time_formatted
        headers_ordered_map[SERVER_VALUE] = SERVER_IDENTIFIER

        # extends the headers ordered map with the response headers map
        headers_ordered_map.extend(self.response_headers_map)

        # iterates over all the header values to be sent
        for header_name, header_value in headers_ordered_map.items():
            # writes the header value in the result
            result.write(header_name + ": " + header_value + "\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write("\r\n")
        result.write(message)

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def validate(self):
        """
        Validates the current request, raising exception
        in case validation fails.
        """

        # checks if the request contains a status code
        if not self.status_code:
            # raises the http runtime exception
            raise main_service_http_exceptions.HttpRuntimeException("status code not defined")

    def get_server_identifier(self):
        """
        Retrieves a string describing the server.

        @rtype: String
        @return: A string describing the server.
        """

        return SERVER_IDENTIFIER

    def get_service_connection(self):
        """
        Returns a the service connection object, that
        contains the connection information.

        @rtype: ServiceConnection
        @return: The service connection to be used.
        """

        return self.service_connection

    def get_attributes_list(self):
        """
        Retrieves the list of attribute names in the
        current attributes map.

        @rtype: List
        @return: The list of attribute names in the
        current attributes map.
        """

        return self.attributes_map.keys()

    def get_attribute(self, attribute_name):
        return self.__getattribute__(attribute_name)

    def set_attribute(self, attribute_name, attribute_value):
        self.__setattribute__(attribute_name, attribute_value)

    def get_message(self):
        return self.message_stream.get_value()

    def set_message(self, message):
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()
        self.message_stream.write(message)

    def set_encoding_handler(self, encoding_handler):
        self.encoding_handler = encoding_handler

    def get_encoding_handler(self):
        return self.encoding_handler

    def set_encoding_name(self, encoding_name):
        self.encoding_name = encoding_name

    def get_encoding_name(self):
        return self.encoding_name

    def get_operation_type(self):
        return self.operation_type

    def get_method(self):
        """
        Retrieves the method used in the current request
        object for the current request.
        This method is an alias to the retrieval of the
        operation type.

        @rtype: String
        @return: The method used in the current request
        context.
        """

        return self.get_operation_type()

    def set_operation_type(self, operation_type):
        self.operation_type = operation_type

    def set_path(self, path, set_original_path = True):
        """
        Sets the path in the request.
        The paths is set by processing it, creating
        the resources path.

        An optional set original path flag may be unset
        to allow overriding the original path.

        @type path: String
        @param path: The path to be set in the request.
        @type set_original_path: bool
        @param set_original_path: If the original path
        should be saved in the original path variable for
        later "raw" retrieval (must only be used once).
        """

        # "saves" the original path value
        # without unquoting (in case the flag is set)
        if set_original_path: self.original_path = path

        # "unquotes" the path value
        path = colony.libs.quote_util.unquote(path)

        # retrieves the resource path of the path
        resource_path = path.split("?")[0]

        self.path = path
        self.resource_path = resource_path
        self.filename = resource_path
        self.uri = resource_path

    def set_base_path(self, base_path):
        """
        Sets the base path in the request.
        The base paths is set by processing it, creating
        the resources path.

        @type path: String
        @param path: The base path to be set in the request.
        """

        # "unquotes" the base path value
        base_path = colony.libs.quote_util.unquote(base_path)

        # retrieves the resource path of the base path
        resource_base_path = base_path.split("?")[0]

        self.base_path = base_path
        self.resource_base_path = resource_base_path

    def set_protocol_version(self, protocol_version):
        """
        Sets the protocol version.

        @type protocol_version: String
        @param protocol_version: The protocol version.
        """

        self.protocol_version = protocol_version

    def get_resource_path(self):
        """
        Retrieves the resource path.

        @rtype: String
        @return: The resource path.
        """

        return self.resource_path

    def get_resource_path_decoded(self):
        """
        Retrieves the resource path in decoded format.

        @rtype: String
        @return: The resource path in decoded format.
        """

        # decodes the resources path
        resource_path_decoded = self.resource_path.decode(DEFAULT_CHARSET)

        return resource_path_decoded

    def get_resource_base_path_decoded(self):
        """
        Retrieves the resource base path in decoded format.

        @rtype: String
        @return: The resource base path in decoded format.
        """

        # decodes the resources base path
        resource_base_path_decoded = self.resource_base_path.decode(DEFAULT_CHARSET)

        return resource_base_path_decoded

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
                self.http_client_service_handler.service_plugin.warning("Problem while checking modification date")

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

    def _parse_multipart_part(self, start_index, end_index):
        """
        Parses a "part" of the whole multipart content bases on the
        interval of send indexes.

        @type start_index: int
        @param start_index: The start index of the "part" to be processed.
        @type end_index: int
        @param end_index: The end index of the "part" to be processed.
        @rtype: Tuple
        @return: A Tuple with a map of header for the "part" and the content of the "part".
        """

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
        return (
            headers_map,
            contents
        )

    def _parse_content_disposition(self, headers_map):
        """
        Parses the content disposition value from the headers map.
        This method returns a map containing associations of key and value
        of the various content disposition values.

        @type headers_map: Dictionary
        @param headers_map: The map containing the headers and the values.
        @rtype: Dictionary
        @return: The map containing the various disposition values in a map.
        """

        # retrieves the content disposition header
        content_disposition = headers_map.get(CONTENT_DISPOSITION_VALUE, None)

        # in case no content disposition is defined
        if not content_disposition:
            # raises the http invalid multipart request exception
            raise main_service_http_exceptions.HttpInvalidMultipartRequestException("missing content disposition in multipart value")

        # splits the content disposition to obtain the attributes
        content_disposition_attributes = content_disposition.split(";")

        # creates the content disposition map
        content_disposition_map = {}

        # iterates over all the content disposition attributes
        # the content disposition attributes are not stripped
        for content_disposition_attribute in content_disposition_attributes:
            # strips the content disposition attribute
            content_disposition_attribute_stripped = content_disposition_attribute.strip()

            # splits the content disposition attribute
            content_disposition_attribute_splitted = content_disposition_attribute_stripped.split("=")

            # retrieves the lenght of the content disposition attribute splitted
            content_disposition_attribute_splitted_length = len(content_disposition_attribute_splitted)

            # in case the length is two (key and value)
            if content_disposition_attribute_splitted_length == 2:
                # retrieves the key and the value
                key, value = content_disposition_attribute_splitted

                # strips the value from the string items
                value_stripped = value.strip("\"")

                # sets the key with value in the
                # content disposition map
                content_disposition_map[key] = value_stripped
            # in case the length is one (just key with no value)
            elif content_disposition_attribute_splitted_length == 1:
                # retrieves the key value
                key = content_disposition_attribute_splitted[0]

                # sets the key with invalid value in the
                # content disposition map
                content_disposition_map[key] = None
            # invalid state
            else:
                # raises the http invalid multipart request exception
                raise main_service_http_exceptions.HttpInvalidMultipartRequestException("invalid content disposition value in multipart value: " + content_disposition_attribute_stripped)

        # returns the content disposition map
        return content_disposition_map
