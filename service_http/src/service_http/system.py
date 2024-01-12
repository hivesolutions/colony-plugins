#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import re
import sys
import time
import copy
import base64
import datetime
import traceback

import colony

from . import exceptions

RESOLUTION_ORDER_ITEMS = ("virtual_servers", "redirections", "contexts")
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
""" The chunk size to be used for the reading/writing
operations, should be chosen taking into account a
different set of factors (eg: page size or disk blocks) """

SERVER_NAME = "Hive-Colony-Web"
""" The server name used as the main part of the
identification process of the server """

SERVER_VERSION = "1.0.1"
""" The server version, this value should be coherent
with the current plugin's version """

ENVIRONMENT_VERSION = (
    str(sys.version_info[0])
    + "."
    + str(sys.version_info[1])
    + "."
    + str(sys.version_info[2])
    + "-"
    + str(sys.version_info[3])
)
""" The environment version, that should somehow identity
the currently running environment  """

SERVER_IDENTIFIER = (
    SERVER_NAME
    + "/"
    + SERVER_VERSION
    + " (python-"
    + sys.platform
    + " "
    + ENVIRONMENT_VERSION
    + ")"
)
""" The server identifier, this value will be presented
in the server's identification areas (eg: HTTP headers) """

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

STATUS_MESSAGES = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    301: "Moved permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "(Unused)",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
}
""" The status code messages map """

DEFAULT_STATUS_MESSAGE = "Invalid"
""" The default status message """

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

UPGRADE_MESSAGE_SIZE_MAP = {WEB_SOCKET_VALUE: 8}
""" The upgrade message size map """


class ServiceHTTP(colony.System):
    """
    The service HTTP class.
    """

    http_service_handler_plugins_map = {}
    """ The HTTP service handler plugins map """

    http_service_encoding_plugins_map = {}
    """ The HTTP service encoding plugins map """

    http_service_authentication_handler_plugins_map = {}
    """ The HTTP service authentication handler plugins map """

    http_service_error_handler_plugins_map = {}
    """ The HTTP service error handler plugins map """

    http_service = None
    """ The HTTP service reference """

    http_log_file = None
    """ The log file """

    http_service_configuration = {}
    """ The HTTP service configuration """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.http_service_handler_plugin_map = {}
        self.http_service_encoding_plugins_map = {}
        self.http_service_authentication_handler_plugins_map = {}
        self.http_service_error_handler_plugins_map = {}
        self.http_service_configuration = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        :type parameters: Dictionary
        :param parameters: The parameters to start the service.
        """

        # retrieves the service utils plugin
        service_utils_plugin = self.plugin.service_utils_plugin

        # generates the parameters
        service_parameters = self._generate_service_parameters(parameters)

        # generates the HTTP service using the given service parameters
        self.http_service = service_utils_plugin.generate_service(service_parameters)

        # starts the HTTP service
        self.http_service.start_service()

    def stop_service(self, parameters):
        """
        Stops the service.

        :type parameters: Dictionary
        :param parameters: The parameters to stop the service.
        """

        # destroys the parameters
        self._destroy_service_parameters(parameters)

        # starts the HTTP service
        self.http_service.stop_service()

    def http_service_handler_load(self, http_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = http_service_handler_plugin.get_handler_name()

        self.http_service_handler_plugins_map[
            handler_name
        ] = http_service_handler_plugin

    def http_service_handler_unload(self, http_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = http_service_handler_plugin.get_handler_name()

        del self.http_service_handler_plugins_map[handler_name]

    def http_service_encoding_load(self, http_service_encoding_plugin):
        # retrieves the plugin encoding name
        encoding_name = http_service_encoding_plugin.get_encoding_name()

        self.http_service_encoding_plugins_map[
            encoding_name
        ] = http_service_encoding_plugin

    def http_service_encoding_unload(self, http_service_encoding_plugin):
        # retrieves the plugin encoding name
        encoding_name = http_service_encoding_plugin.get_encoding_name()

        del self.http_service_encoding_plugins_map[encoding_name]

    def http_service_authentication_handler_load(
        self, http_service_authentication_handler_plugin
    ):
        # retrieves the plugin handler name
        handler_name = http_service_authentication_handler_plugin.get_handler_name()

        self.http_service_authentication_handler_plugins_map[
            handler_name
        ] = http_service_authentication_handler_plugin

    def http_service_authentication_handler_unload(
        self, http_service_authentication_handler_plugin
    ):
        # retrieves the plugin handler name
        handler_name = http_service_authentication_handler_plugin.get_handler_name()

        del self.http_service_authentication_handler_plugins_map[handler_name]

    def http_service_error_handler_load(self, http_service_error_handler_plugin):
        # retrieves the plugin error handler name
        error_handler_name = http_service_error_handler_plugin.get_error_handler_name()

        self.http_service_error_handler_plugins_map[
            error_handler_name
        ] = http_service_error_handler_plugin

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
            resolution_order_item_value = service_configuration.get(
                resolution_order_item, None
            )

            # in case the resolution order item value is not set
            # nothing to be done, continues the loop
            if not resolution_order_item_value:
                continue

            # retrieves the resolution order values
            resolution_order = resolution_order_item_value.get(
                RESOLUTION_ORDER_VALUE,
                colony.legacy.iterkeys(resolution_order_item_value),
            )

            # creates the regex buffer
            regex_buffer = colony.StringBuffer()

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

            # retrieves the regex value, compiles it and sets the resolution
            # order regex value in the resolution order item value map
            regex_value = regex_buffer.get_value()
            regex = re.compile(regex_value)
            resolution_order_item_value[RESOLUTION_ORDER_REGEX_VALUE] = regex

        # cleans the HTTP service configuration
        colony.map_clean(self.http_service_configuration)

        # copies the service configuration to the HTTP service configuration
        colony.map_copy(service_configuration, self.http_service_configuration)

    def unset_service_configuration_property(self):
        # cleans the HTTP service configuration
        colony.map_clean(self.http_service_configuration)

    def _get_service_configuration(self):
        """
        Retrieves the service configuration map.

        :rtype: Dictionary
        :return: The service configuration map.
        """

        return self.http_service_configuration

    def _get_encoding_handler(self, encoding):
        # in case no encoding is defined returns an invalid value
        # to the caller method (could not find anything)
        if not encoding:
            return None

        # in case the encoding is not found in the HTTP service
        # encoding handler plugins map raises an exception
        if not encoding in self.http_service_encoding_plugins_map:
            raise exceptions.EncodingNotFound("encoding %s not found" % encoding)

        # retrieves the HTTP service encoding handler plugin
        http_service_encoding_plugin = self.http_service_encoding_plugins_map[encoding]

        # retrieves the encode contents method as the encoding handler
        encoding_handler = http_service_encoding_plugin.encode_contents

        # returns the encoding handler
        return encoding_handler

    def _generate_service_parameters(self, parameters):
        """
        Retrieves the service parameters map from the base parameters
        map.

        :type parameters: Dictionary
        :param parameters: The base parameters map to be used to build
        the final service parameters map.
        :rtype: Dictionary
        :return: The final service parameters map.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the various parameter values that are going to
        # be used as the basis for the (new) parameters creation
        end_points = parameters.get("end_points", [])
        socket_provider = parameters.get("socket_provider", None)
        port = parameters.get("port", DEFAULT_PORT)
        encoding = parameters.get("encoding", None)
        socket_parameters = parameters.get("socket_parameters", {})

        # retrieves the service configuration
        service_configuration = self._get_service_configuration()

        # retrieves the various service configuration values using
        # the default values for each of the configuration items
        end_points = service_configuration.get("default_end_points", end_points)
        socket_provider = service_configuration.get(
            "default_socket_provider", socket_provider
        )
        port = service_configuration.get("default_port", port)
        encoding = service_configuration.get("default_encoding", encoding)
        socket_parameters = service_configuration.get(
            "default_socket_parameters", socket_parameters
        )
        service_type = service_configuration.get("default_service_type", SERVICE_TYPE)
        client_connection_timeout = service_configuration.get(
            "default_client_connection_timeout", CLIENT_CONNECTION_TIMEOUT
        )
        connection_timeout = service_configuration.get(
            "default_connection_timeout", REQUEST_TIMEOUT
        )
        request_timeout = service_configuration.get(
            "default_request_timeout", REQUEST_TIMEOUT
        )
        response_timeout = service_configuration.get(
            "default_response_timeout", RESPONSE_TIMEOUT
        )
        number_threads = service_configuration.get(
            "default_number_threads", NUMBER_THREADS
        )
        scheduling_algorithm = service_configuration.get(
            "default_scheduling_algorithm", SCHEDULING_ALGORITHM
        )
        maximum_number_threads = service_configuration.get(
            "default_maximum_number_threads", MAXIMUM_NUMBER_THREADS
        )
        maximum_number_work_threads = service_configuration.get(
            "default_maximum_number_work_threads", MAXIMUM_NUMBER_WORKS_THREAD
        )
        work_scheduling_algorithm = service_configuration.get(
            "default_work_scheduling_algorithm", WORK_SCHEDULING_ALGORITHM
        )
        http_log_file_path = service_configuration.get("log_file_path", None)

        # uses the global configuration to try to configure some of the
        # parameters for the configuration to be created
        bind_host = colony.conf("SERVER_HOST", BIND_HOST)
        port = colony.conf("SERVER_PORT", port, cast=int)
        ssl = colony.conf("SERVER_SSL", False, cast=bool)

        # creates the proper string definition of the connection type
        # and uses it to create the (full) end point definition tuple
        connection_s = "ssl" if ssl else "normal"
        end_point = (connection_s, bind_host, port, {})

        # verifies if the configuration endpoint should be overridden,
        # this should happen when at least one global wide configuration
        # value is defined, if that's the case the end points are re-written
        override = True if colony.conf("SERVER_HOST") else False
        override = True if colony.conf("SERVER_PORT") else override
        override = True if colony.conf("SERVER_SSL") else override
        if override:
            end_points = (end_point,)

        # resolves the HTTP log file path using the plugin manager,
        # this path will be used for the writing of the log files, then
        # creates the HTTP log file (using a file rotator) and then
        # opens it to be able to start writing in it
        http_log_file_path = plugin_manager.resolve_file_path(
            http_log_file_path, True, True
        )
        self.http_log_file = (
            http_log_file_path and colony.FileRotator(http_log_file_path) or None
        )
        self.http_log_file and self.http_log_file.open()

        # retrieves the encoding handler for the given encoding
        encoding_handler = self._get_encoding_handler(encoding)

        # creates the pool configuration map
        pool_configuration = dict(
            name="HTTP pool",
            description="pool to support HTTP client connections",
            number_threads=number_threads,
            scheduling_algorithm=scheduling_algorithm,
            maximum_number_threads=maximum_number_threads,
            maximum_number_works_thread=maximum_number_work_threads,
            work_scheduling_algorithm=work_scheduling_algorithm,
        )

        # creates the extra parameters map
        extra_parameters = dict(
            encoding=encoding,
            encoding_handler=encoding_handler,
            log_file=self.http_log_file,
        )

        # creates the parameters map
        parameters = dict(
            type=CONNECTION_TYPE,
            service_plugin=self.plugin,
            service_handling_task_class=HTTPClientServiceHandler,
            end_points=end_points,
            socket_provider=socket_provider,
            bind_host=bind_host,
            port=port,
            socket_parameters=socket_parameters,
            chunk_size=CHUNK_SIZE,
            service_configuration=service_configuration,
            extra_parameters=extra_parameters,
            pool_configuration=pool_configuration,
            service_type=service_type,
            client_connection_timeout=client_connection_timeout,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
            response_timeout=response_timeout,
        )

        # returns the parameters
        return parameters

    def _destroy_service_parameters(self, parameters):
        """
        Destroys the service parameters map from the base parameters
        map.

        :type parameters: Dictionary
        :param parameters: The base parameters map to be used to destroy
        the final service parameters map.
        """

        # closes the HTTP log file
        self.http_log_file and self.http_log_file.close()


class HTTPClientServiceHandler(object):
    """
    The HTTP client service handler class, responsible
    for the handling of incoming client connection and
    redirection/routing of data.
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

    def __init__(
        self,
        service_plugin,
        service_connection_handler,
        service_configuration,
        service_utils_exception_class,
        extra_parameters,
    ):
        """
        Constructor of the class.

        :type service_plugin: Plugin
        :param service_plugin: The service plugin.
        :type service_connection_handler: AbstractServiceConnectionHandler
        :param service_connection_handler: The abstract service connection handler, that
        handles this connection.
        :type service_configuration: Dictionary
        :param service_configuration: The service configuration.
        :type service_utils_exception: Class
        :param service_utils_exception: The service utils exception class.
        :type extra_parameters: Dictionary
        :param extra_parameters: The extra parameters.
        """

        self.service_plugin = service_plugin
        self.service_connection_handler = service_connection_handler
        self.service_configuration = service_configuration
        self.service_utils_exception_class = service_utils_exception_class

        self.service_connection_request_handler_map = {}

        self.encoding = extra_parameters.get(ENCODING_VALUE, None)
        self.encoding_handler = extra_parameters.get(ENCODING_HANDLER_VALUE, None)
        self.log_file = extra_parameters.get(LOG_FILE_VALUE, None)
        self.content_type_charset = self.service_configuration.get(
            DEFAULT_CONTENT_TYPE_CHARSET_VALUE, DEFAULT_CHARSET
        )

    def handle_opened(self, service_connection):
        pass

    def handle_closed(self, service_connection):
        # retrieves the current request (being handled)
        request = service_connection.request_data.get("_request", None)

        # in case the request is not defined (no request
        # pending), must return the control flow
        if not request:
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

    def handle_request(self, service_connection, request=None):
        # retrieves the request handler using the service connection request handler map
        request_handler = self.service_connection_request_handler_map.get(
            service_connection, self.default_request_handler
        )

        # handles the service connection with the request handler
        return request_handler(service_connection, request)

    def default_request_handler(self, service_connection, request=None):
        # retrieves the HTTP service handler plugins map
        http_service_handler_plugins_map = (
            self.service_plugin.system.http_service_handler_plugins_map
        )

        try:
            # retrieves the request
            request = request or self.retrieve_request(service_connection)
        except exceptions.ServiceHTTPException:
            # prints a debug message about the connection closing
            self.service_plugin.debug(
                "Connection: %s closed by peer, timeout or invalid request"
                % str(service_connection)
            )

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

            # processes the authentication and the redirection information
            # for the current request in handling
            self._process_authentication(request, service_configuration)
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
                # and sets the handler path to an invalid value
                handler_name = service_configuration.get("default_handler", None)
                request.handler_path = None

            # in case no handler name is defined (request not handled)
            if not handler_name:
                # raises an HTTP no handler exception
                raise exceptions.HTTPNoHandlerException(
                    "no handler defined for current request"
                )

            # in case the handler is not found in the handler plugins map
            if not handler_name in http_service_handler_plugins_map:
                # raises an HTTP handler not found exception
                raise exceptions.HTTPHandlerNotFoundException(
                    "no handler found for current request: " + handler_name
                )

            # retrieves the HTTP service handler plugin
            http_service_handler_plugin = http_service_handler_plugins_map[handler_name]

            # handles the request by the request handler, only in case the
            # request does not already contains a status code (in such case the
            # request is considered to be already processed)
            if not request.status_code:
                http_service_handler_plugin.handle_request(request)

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
        except Exception as exception:
            # processes the exception, retrieving the return
            # value (connection closed value)
            return_value = self.process_exception(
                request, service_connection, exception
            )

        # runs the logging steps for the request, this call is going to
        # block for a while for the io operations
        self._log(request)

        # in case the return value is invalid the connection
        # is meant to be closed (no need to process any extra
        # information), must return immediately
        if not return_value:
            return False

        # checks if the service connection is of type asynchronous
        service_connection_is_async = service_connection.is_async()

        # in case there is pending data and the service connection is of
        # type asynchronous calls the default request handler to handle the
        # remaining data (allows HTTP pipelining)
        service_connection.pending_data() and not service_connection_is_async and self.default_request_handler(
            service_connection
        )

        # returns true (connection remains open)
        return True

    def process_delayed(self, request, service_connection):
        # retrieves the request timeout from the service connection
        service_connection_request_timeout = (
            service_connection.connection_request_timeout
        )

        # prints a debug message
        self.service_plugin.debug(
            "Connection: %s kept alive for %ss for delayed request"
            % (str(service_connection), str(service_connection_request_timeout))
        )

        # returns true (connection meant to be kept alive)
        return True

    def process_request(self, request, service_connection):
        try:
            # sends the request to the client (response)
            self.send_request(service_connection, request)
        except exceptions.HTTPRuntimeException as exception:
            # prints a warning message message and returns
            # an invalid value as there was a problem handling
            # the current request
            self.service_plugin.warning(
                "Runtime problem: %s, while sending request"
                % colony.legacy.UNICODE(exception)
            )
            return False
        except exceptions.ServiceHTTPException:
            # prints a debug message and returns an invalid
            # return value as the connection has been closed
            self.service_plugin.debug(
                "Connection: %s closed by peer, while sending request"
                % str(service_connection)
            )
            return False

        # in case the connection is not meant to be kept alive
        if not self.keep_alive(request):
            # prints a debug message
            self.service_plugin.debug(
                "Connection: %s closed, not meant to be kept alive"
                % str(service_connection)
            )

            # runs the logging steps for the request
            self._log(request)

            # returns false (connection closed)
            return False

        # retrieves the request timeout from the service connection
        service_connection_request_timeout = (
            service_connection.connection_request_timeout
        )

        # prints a debug message
        self.service_plugin.debug(
            "Connection: %s kept alive for %ss"
            % (str(service_connection), str(service_connection_request_timeout))
        )

        # returns true (connection meant to be kept alive)
        return True

    def process_exception(self, request, service_connection, exception):
        # prints info message about exception so that an easy diagnostic
        # operation is possible at runtime (for debugging)
        self.service_plugin.info(
            "There was an exception handling the request (%s): "
            % exception.__class__.__name__
            + colony.legacy.UNICODE(exception)
        )
        try:
            # sends the exception
            self.send_exception(service_connection, request, exception)
        except exceptions.ServiceHTTPException:
            # prints a debug message
            self.service_plugin.debug(
                "Connection: %s closed by peer, while sending exception"
                % str(service_connection)
            )

            # returns false (connection closed)
            return False
        except Exception as exception:
            # prints an error message about the raised exception so that it's
            # possible to properly act on it at a runtime level
            self.service_plugin.debug(
                "There was an exception handling the exception (%s): "
                % exception.__class__.__name__
                + colony.legacy.UNICODE(exception)
            )

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
        connection_host, _connection_port = service_connection.connection_address

        # retrieves the user id
        user_id = "-"

        # retrieves the operation type
        operation_type = request.operation_type

        # retrieves the requested resource path
        resource_path = request.get_resource_path_decoded()

        # retrieves the protocol version
        protocol_version = request.protocol_version

        # retrieves the status code (defaults to zero,
        # one or invalid)
        status_code = request.status_code or 0

        # retrieves the content length (defaults to zero,
        # one or invalid)
        content_length = request.content_length or 0

        # retrieves the current date time value
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time
        current_date_time_formatted = current_date_time.strftime(
            "%d/%b/%Y:%H:%M:%S +0000"
        )

        # creates the log line value with all the aggregated
        # parameters, the log line will conform with the common
        # log form (according to the specification)
        log_line_value = '%s - %s [%s] "%s %s %s" %d %d\n' % (
            connection_host,
            user_id,
            current_date_time_formatted,
            operation_type,
            resource_path,
            protocol_version,
            status_code,
            content_length,
        )

        # writes the log line value to the log file, note that the
        # log line value/message may be encoded before written to
        # the file, this will use the default encoding process
        self.log_file.write(log_line_value)

    def retrieve_request(self, service_connection):
        """
        Retrieves the request from the received message.
        This method block until the complete request
        message is received.
        This method is not compatible with async communication.

        :type service_connection: ServiceConnection
        :param service_connection: The service connection to be used.
        :rtype: HTTPRequest
        :return: The request from the received message.
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
                # raises the HTTP data retrieval exception
                raise exceptions.HTTPDataRetrievalException("problem retrieving data")

            # in case no valid data was received
            if not data:
                # raises the HTTP invalid data exception
                raise exceptions.HTTPInvalidDataException("empty data received")

            # tries to retrieve the request using the retrieved data
            request = self.retrieve_request_data(service_connection, data)

            # in case the request is not valid (not enough data for parsing)
            # must continue the loop
            if not request:
                continue

            # breaks the loop
            break

        # returns the request
        return request

    def retrieve_request_data(self, service_connection, data=None):
        """
        Retrieves the request from the received message.
        This method retrieves the request using only the
        provided data value.

        :type service_connection: ServiceConnection
        :param service_connection: The service connection to be used.
        :type String: data
        :param String: The data to be used in processing the request.
        :rtype: HTTPRequest
        :return: The request from the received message.
        """

        # creates the string buffer for the message
        message = service_connection.request_data.get("message", colony.StringBuffer())

        # creates a request object
        request = service_connection.request_data.get(
            "request", HTTPRequest(self, service_connection, self.content_type_charset)
        )

        # retrieves the various values from the request data that are going
        # to be used for the parsing of the HTTP response starting them  in
        # case they are not already initialized, special note for the message
        # offset index that represents the offset byte to the initialization
        # of the message content
        start_line_loaded = service_connection.request_data.get(
            "start_line_loaded", False
        )
        header_loaded = service_connection.request_data.get("header_loaded", False)
        message_loaded = service_connection.request_data.get("message_loaded", False)
        message_offset_index = service_connection.request_data.get(
            "message_offset_index", 0
        )
        message_size = service_connection.request_data.get("message_size", 0)
        received_data_size = service_connection.request_data.get(
            "received_data_size", 0
        )
        start_line_index = service_connection.request_data.get("start_line_index", 0)
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
        if (
            not header_loaded
            or received_data_size >= message_offset_index + message_size
        ):
            # retrieves the message value from the string buffer
            message_value = message.get_value()
        # in case there's no need to inspect the message contents
        else:
            # unsets the process flag
            process_flag = False

        # in case the start line is not loaded
        if process_flag and not start_line_loaded:
            # finds the first new line value
            start_line_index = message_value.find(b"\r\n")

            # in case there is a new line value found
            if not start_line_index == -1:
                # retrieves the start line, ensures that it's represented as a
                # string value (default encoding applies) and then splits it
                # around the complete set of components (should be three)
                start_line = message_value[:start_line_index]
                start_line = colony.legacy.str(start_line)
                start_line_splitted = start_line.split(" ", 2)

                # retrieves the start line splitted length
                start_line_splitted_length = len(start_line_splitted)

                # in case the length of the splitted line is not valid
                if not start_line_splitted_length == 3:
                    # raises the HTTP invalid data exception
                    raise exceptions.HTTPInvalidDataException(
                        "invalid data received: " + start_line
                    )

                # retrieve the operation type the path and the protocol version
                # from the start line splitted and then sets these various values
                # into the current request object
                operation_type, path, protocol_version = start_line_splitted
                request.set_operation_type(operation_type)
                request.set_path(path)
                request.set_protocol_version(protocol_version)

                # sets the start line loaded flag
                start_line_loaded = True

        # in case the header is not loaded
        if process_flag and not header_loaded:
            # retrieves the end header index (two new lines)
            end_header_index = message_value.find(b"\r\n\r\n")

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
                headers_splitted = headers.split(b"\r\n")

                # iterates over the headers lines
                for header_splitted in headers_splitted:
                    # finds the header separator
                    division_index = header_splitted.find(b":")

                    # retrieves the header name and the value for it and then
                    # converts both of the values to plain based unicode values
                    header_name = header_splitted[:division_index].strip()
                    header_value = header_splitted[division_index + 1 :].strip()
                    header_name = colony.legacy.str(header_name)
                    header_value = colony.legacy.str(header_value)

                    # sets the header in the headers map so that it may be used
                    # latter for further reference operations (as required)
                    request.headers_map[header_name] = header_value
                    request.headers_in[header_name] = header_value

                # parses the get attributes, this will load
                # the attributes associated with the URL
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

        # in case the message is not yet loaded (not enough data)
        if not message_loaded:
            # saves the various state values representing the current
            # request parsing state
            service_connection.request_data["message"] = message
            service_connection.request_data["request"] = request
            service_connection.request_data["start_line_loaded"] = start_line_loaded
            service_connection.request_data["header_loaded"] = header_loaded
            service_connection.request_data["message_loaded"] = message_loaded
            service_connection.request_data[
                "message_offset_index"
            ] = message_offset_index
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

        :type request: HTTPRequest
        :param request: The request to be decoded.
        """

        # start the valid charset flag
        valid_charset = False

        # in case the content type is defined
        if CONTENT_TYPE_VALUE in request.headers_map:
            # retrieves the content type
            content_type = request.headers_map[CONTENT_TYPE_VALUE]

            # splits the content type
            content_type_splitted = content_type.split(";")

            # iterates over all the items in the content type splitted
            for content_type_item in content_type_splitted:
                # strips the content type item
                content_type_item_stripped = content_type_item.strip()

                # in case the content is of type octet stream
                if content_type_item_stripped.startswith(OCTET_STREAM_VALUE):
                    # returns immediately
                    return

                # in case the content is of type multipart form data
                if content_type_item_stripped.startswith(MULTIPART_FORM_DATA_VALUE):
                    # parses the request as multipart and
                    # returns immediately
                    request.parse_post_multipart()
                    return

                # in case the content is of type www form urlencoded
                if content_type_item_stripped.startswith(WWW_FORM_URLENCODED_VALUE):
                    # parses the request attributes and
                    # returns immediately
                    request.parse_post_attributes()
                    return

                # in case the item is the charset definition
                if content_type_item_stripped.startswith("charset"):
                    # splits the content type item stripped,
                    # retrieves the content type charset and
                    # sets the valid charset flag
                    content_type_item_stripped_splitted = (
                        content_type_item_stripped.split("=")
                    )
                    content_type_charset = content_type_item_stripped_splitted[
                        1
                    ].lower()
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
            request.received_message = received_message_value.decode(
                content_type_charset
            )
        except Exception:
            # sets the received message as the original one (fallback procedure)
            request.received_message = received_message_value

    def send_exception(self, service_connection, request, exception):
        """
        Sends the exception to the given request for the given exception.

        :type service_connection: ServiceConnection
        :param service_connection: The service connection to be used.
        :type request: HTTPRequest
        :param request: The request to send the exception.
        :type exception: Exception
        :param exception: The exception to be sent.
        """

        # retrieves the preferred error handlers list
        preferred_error_handlers_list = self.service_configuration.get(
            "preferred_error_handlers", (DEFAULT_VALUE,)
        )

        # retrieves the HTTP service error handler plugins map
        http_service_error_handler_plugins_map = (
            self.service_plugin.system.http_service_error_handler_plugins_map
        )

        # iterates over all the preferred error handlers
        for preferred_error_handler in preferred_error_handlers_list:
            # in case the preferred error handler is the default one
            if preferred_error_handler == DEFAULT_VALUE:
                # handles the error with the default error handler
                self.default_error_handler(request, exception)

                # breaks the loop
                break
            else:
                # in case the preferred error handler exist in the HTTP service
                # error handler plugins map
                if preferred_error_handler in http_service_error_handler_plugins_map:
                    # retrieves the HTTP service error handler plugin
                    http_service_error_handler_plugin = (
                        http_service_error_handler_plugins_map[preferred_error_handler]
                    )

                    # calls the handle error in the HTTP service error handler plugin
                    http_service_error_handler_plugin.handle_error(request, exception)

                    # breaks the loop
                    break

        # sends the request to the client (response)
        self.send_request(service_connection, request)

    def send_request(self, service_connection, request):
        # in case the encoding is defined for the current request
        # meaning that the default one is not going to be used
        if self.encoding:
            # sets the encoded flag, handler and the name of
            # the encoding that has been chosen for the message
            request.encoded = True
            request.set_encoding_handler(self.encoding_handler)
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
        # retrieves the result value from the request, so that
        # it's possible to send it through the proper connection
        result_value = request.get_result()

        try:
            # sends the result value to the client, so that the
            # proper network layers are used for operations
            service_connection.send(result_value)
        except self.service_utils_exception_class as exception:
            # print an error description about the error in the
            # client side and the re-raises the exception to the
            # various upper levels so that is properly handled
            self.service_plugin.error(
                "Problem sending request simple: " + colony.legacy.UNICODE(exception)
            )
            raise exceptions.HTTPDataSendingException("problem sending data")

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
        def request_mediated_writer(send_error=False):
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
                    # prints a debug message about the end of the mediated
                    # operation, then closes the mediated handler and returns
                    # the control flow to the caller method
                    self.service_plugin.debug("Completed transfer of request mediated")
                    request.mediated_handler.close()
                    return

                try:
                    # sends the mediated value to the client (writes in front of the others)
                    # and sets the callback as the current writer
                    service_connection.send_callback(
                        mediated_value, request_mediated_writer, write_front=True
                    )
                except self.service_utils_exception_class as exception:
                    # prints an error message about the error in the client side and then
                    # raises the HTTP data sending exception to the upper layers
                    self.service_plugin.error(
                        "Problem sending request mediated: "
                        + colony.legacy.UNICODE(exception)
                    )
                    raise exceptions.HTTPDataSendingException("problem sending data")
            except:
                # closes the mediated handler and then re-raises
                # the exception to the top level layers
                request.mediated_handler.close()
                raise

        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client and sets the request
            # mediated writer as the callback handler
            service_connection.send_callback(result_value, request_mediated_writer)
        except self.service_utils_exception_class as exception:
            # error in the client side
            self.service_plugin.error(
                "Problem sending request mediated: " + colony.legacy.UNICODE(exception)
            )

            # closes the mediated handler
            request.mediated_handler.close()

            # raises the HTTP data sending exception
            raise exceptions.HTTPDataSendingException("problem sending data")

    def send_request_mediated_sync(self, service_connection, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            service_connection.send(result_value)
        except self.service_utils_exception_class as exception:
            # error in the client side
            self.service_plugin.error(
                "Problem sending request mediated: " + colony.legacy.UNICODE(exception)
            )

            # closes the mediated handler
            request.mediated_handler.close()

            # raises the HTTP data sending exception
            raise exceptions.HTTPDataSendingException("problem sending data")

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
                except self.service_utils_exception_class as exception:
                    # prints the error message about the error in the client
                    # side and then raises the HTTP data sending exception
                    self.service_plugin.error(
                        "Problem sending request mediated: "
                        + colony.legacy.UNICODE(exception)
                    )
                    raise exceptions.HTTPDataSendingException("problem sending data")
            except:
                # closes the mediated handler and then
                # re-raises the exception
                request.mediated_handler.close()
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
        def request_chunked_writer(send_error=False):
            # in case there was an error sending the data must
            # close the chunk handler and return immediately
            if send_error:
                request.chunk_handler.close()
                return

            try:
                # retrieves the chunk value from the currently associated
                # handler, note that the chunk size is just for reference
                chunk_value = request.chunk_handler.get_chunk(CHUNK_SIZE)

                # in case the read is complete (time to close
                # the currently open chunk handler)
                if not chunk_value:
                    # closes the chunk handler, so that no more access is possible
                    # to be done for it (no more usage for now)
                    request.chunk_handler.close()

                    try:
                        # sends the final empty chunk of the current sequence indicating
                        # that no more chunks are going to be sent for now
                        service_connection.send(b"0\r\n\r\n")
                    except self.service_utils_exception_class as exception:
                        # logs the error coming from the client side and then raises
                        # a proper exception indicating the problem in sending data
                        self.service_plugin.error(
                            "Problem sending request chunked (final chunk): "
                            + colony.legacy.UNICODE(exception)
                        )
                        raise exceptions.HTTPDataSendingException(
                            "problem sending data"
                        )

                    # returns immediately
                    return

                try:
                    # retrieves the length of the chunk value, this value is going to be used
                    # in the basis of the chunk data creation (for message sending)
                    length_chunk_value = len(chunk_value)

                    # sets the value for the hexadecimal length part of the chunk
                    # and then joins that value with the proper chunk value for sending
                    length_chunk_value_hexadecimal_string = colony.legacy.bytes(
                        "%X\r\n" % length_chunk_value
                    )
                    message_value = (
                        length_chunk_value_hexadecimal_string + chunk_value + b"\r\n"
                    )

                    # sends the message value to the client (writes in front of the others)
                    # and sets the callback as the current writer
                    service_connection.send_callback(
                        message_value, request_chunked_writer, write_front=True
                    )
                except self.service_utils_exception_class as exception:
                    # logs the error information about the client side error and then
                    # raises the HTTP data sending exception to the upper levels
                    self.service_plugin.error(
                        "Problem sending request chunked: "
                        + colony.legacy.UNICODE(exception)
                    )
                    raise exceptions.HTTPDataSendingException("problem sending data")
            except:
                # closes the chunk handler reference and then
                # re-raises the exception to the top stack
                request.chunk_handler.close()
                raise

        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client and sets the request
            # chunked writer as the callback handler
            service_connection.send_callback(result_value, request_chunked_writer)
        except self.service_utils_exception_class as exception:
            # print an error message about the problem in the sending, then
            # closes the chunk(ed) handler and raises a new exception
            self.service_plugin.error(
                "Problem sending request chunked: " + colony.legacy.UNICODE(exception)
            )
            request.chunk_handler.close()
            raise exceptions.HTTPDataSendingException("problem sending data")

    def send_request_chunked_sync(self, service_connection, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            service_connection.send(result_value)
        except self.service_utils_exception_class as exception:
            # error in the client side
            self.service_plugin.error(
                "Problem sending request chunked: " + colony.legacy.UNICODE(exception)
            )

            # closes the chunk handler
            request.chunk_handler.close()

            # raises the HTTP data sending exception
            raise exceptions.HTTPDataSendingException("problem sending data")

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
                    except self.service_utils_exception_class as exception:
                        # error in the client side
                        self.service_plugin.error(
                            "Problem sending request chunked (final chunk): "
                            + colony.legacy.UNICODE(exception)
                        )

                        # raises the HTTP data sending exception
                        raise exceptions.HTTPDataSendingException(
                            "problem sending data"
                        )

                    # breaks the cycle
                    break

                try:
                    # retrieves the length of the chunk value
                    length_chunk_value = len(chunk_value)

                    # sets the value for the hexadecimal length part of the chunk
                    length_chunk_value_hexadecimal_string = (
                        "%X\r\n" % length_chunk_value
                    )

                    # sets the message value
                    message_value = (
                        length_chunk_value_hexadecimal_string + chunk_value + "\r\n"
                    )

                    # sends the message value to the client
                    service_connection.send(message_value)
                except self.service_utils_exception_class as exception:
                    # error in the client side
                    self.service_plugin.error(
                        "Problem sending request chunked: "
                        + colony.legacy.UNICODE(exception)
                    )

                    # raises the HTTP data sending exception
                    raise exceptions.HTTPDataSendingException("problem sending data")
            finally:
                # closes the chunk handler
                request.chunk_handler.close()

                # re-raises the exception
                raise

    def keep_alive(self, request):
        """
        Retrieves the value of the keep alive for the given request.

        :type request: HTTPRequest
        :param request: The request to retrieve the keep alive value.
        :rtype: bool
        :return: The value of the keep alive for the given request.
        """

        # in case connection is defined in the headers map
        if CONNECTION_VALUE in request.headers_map:
            # retrieves the connection type
            connection_type = request.headers_map[CONNECTION_VALUE]

            # retrieves the connection type fields, by splitting
            # the connection type and stripping the values
            connection_type_fields = [
                value.strip() for value in connection_type.split(",")
            ]

            # iterates over all the connection type fields
            for connection_type_field in connection_type_fields:
                # in case the connection is meant to be kept alive
                # or in case is of type upgrade
                if connection_type_field.lower() in (
                    KEEP_ALIVE_LOWER_VALUE,
                    UPGRADE_LOWER_VALUE,
                ):
                    # returns true
                    return True

        # returns false
        return False

    def default_error_handler(self, request, error):
        """
        The default error handler for exception sending.

        :type request: HTTPRequest
        :param request: The request to send the error.
        :type exception: Exception
        :param exception: The error to be sent.
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

        # retrieves the value for the status message, this is the message
        # that will be sent after the code
        status_message = request.get_status_message()

        # writes the header message and the initial error line
        # these values are sent as plain text values
        request.write(
            "colony web server - "
            + str(request.status_code)
            + " "
            + status_message
            + "\n"
        )
        request.write("error: '" + colony.legacy.UNICODE(error) + "'\n")

        # writes the traceback header message in the request
        request.write("traceback:\n")

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid then uses it to create
        # a properly formated traceback string ling
        if traceback_list:
            # creates the (initial) formated traceback
            formated_traceback = traceback.format_tb(traceback_list)

            # retrieves the file system encoding and uses it to
            # decode the traceback values using the file system encoding
            # in case that required (values encoded as byte strings)
            file_system_encoding = sys.getfilesystemencoding()
            formated_traceback = [
                value.decode(file_system_encoding)
                if colony.legacy.is_bytes(value)
                else value
                for value in formated_traceback
            ]
        # otherwise there is no traceback list, then
        # sets an empty formated traceback
        else:
            formated_traceback = ()

        # iterates over the traceback lines
        for formated_traceback_line in formated_traceback:
            # writes the traceback line in the request
            request.write(formated_traceback_line)

    def get_current_request_handler(self):
        """
        Retrieves the current request handler.

        :rtype: Method
        :return: The current request handler.
        """

        return self.current_request_handler

    def set_current_request_handler(self, current_request_handler):
        """
        Sets the current request handler.

        :type current_request_handler: Method
        :param current_request_handler: The current request handler.
        """

        self.current_request_handler = current_request_handler

    def set_service_connection_request_handler(
        self, service_connection, request_handler_method
    ):
        """
        Sets a "custom" request handler method for the given service connection.

        :type service_connection: ServiceConnection
        :param service_connection: The service connection to have the
        "custom" request handler method associated.
        :type request_handler_method: Method
        :param request_handler_method: The method to be used in the handling
        of the request.
        """

        self.service_connection_request_handler_map[
            service_connection
        ] = request_handler_method

    def unset_service_connection_request_handler(
        self, service_connection, request_handler_method
    ):
        """
        Unsets a "custom" request handler method for the given service connection.

        :type service_connection: ServiceConnection
        :param service_connection: The service connection to have the "custom"
        request handler method association removed.
        """

        del self.service_connection_request_handler_map[service_connection]

    def _process_redirection(self, request, service_configuration):
        """
        Processes the redirection stage of the HTTP request, this
        step may be considered computer intensive.

        Processing redirection implies matching the path against the
        rules, and then changing the "target" path in accordance
        with matched rule.

        :type request: HTTPRequest
        :param request: The request to be processed.
        :type service_configuration: Dictionary
        :param service_configuration: The service configuration map.
        """

        # retrieves the service configuration redirections
        service_configuration_redirections = service_configuration.get(
            "redirections", {}
        )

        # retrieves the service configuration redirections order
        service_configuration_redirections_order = (
            service_configuration_redirections.get(
                RESOLUTION_ORDER_VALUE,
                colony.legacy.iterkeys(service_configuration_redirections),
            )
        )

        # (saves) the old/original path as the base path, this is going
        # to be used in case no rule is matched at this stage
        request.set_base_path(request.original_path)

        # unsets the request handler base path, as by default no specific
        # handler is defined for the request until one is found
        request.handler_base_path = None

        # sets the initial (current) path value to be used at the beginning
        # of the redirection (possibly recursive) cycle
        current_path = request.original_path

        # iterates over the service configuration redirection names
        for (
            service_configuration_redirection_name
        ) in service_configuration_redirections_order:
            # in case the path is not found in the request path, skips
            # the current iteration, as there's nothing to be done
            if not current_path.find(service_configuration_redirection_name) == 0:
                continue

            # sets the handler base path as the service configuration
            # redirection name and then retrieve the proper service
            # configuration redirection specification
            request.handler_base_path = service_configuration_redirection_name
            service_configuration_redirection = service_configuration_redirections[
                service_configuration_redirection_name
            ]

            # retrieves the target path and the recursive redirection
            # flag value for context resolution
            target_path = service_configuration_redirection.get(
                "target", service_configuration_redirection_name
            )
            recursive_redirection = service_configuration_redirection.get(
                "recursive_redirection", False
            )

            # retrieves the sub request path as the request from the redirection name path
            # in front, so that only the remainder after the prefix is retrieved
            sub_request_path = current_path[
                len(service_configuration_redirection_name) :
            ]

            # in case the recursive redirection is disabled and there is a sub-directory
            # in the sub request path
            if not recursive_redirection and not sub_request_path.find("/") == -1:
                # breaks the loop because the request is not meant to be recursively redirected
                # and it contains a sub-directory
                break

            # retrieves the new (redirected) path in the request by stripping
            # both parts of the path to avoid problems with duplicated slashes
            current_path = target_path.rstrip("/") + "/" + sub_request_path.lstrip("/")

            # sets the new path in the request, avoids the overriding
            # of the original path by unsetting the flag
            request.set_path(current_path, set_original_path=False)

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

        :type request: HTTPRequest
        :param request: The request to be processed.
        :type service_connection: ServiceConnection
        :param service_connection: The service connection currently in use.
        :type service_configuration: Dictionary
        :param service_configuration: The service configuration map.
        """

        # retrieves the service configuration context name and value from the request and the service configuration
        (
            _service_configuration_context_name,
            service_configuration_context,
        ) = self._get_request_service_configuration_context(
            request, service_configuration
        )

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
        if not force_domain:
            return

        # checks if the current service connection is secure (encrypted)
        # then uses it to retrieve the proper prefix value for the location
        is_secure = service_connection.is_secure()
        prefix = is_secure and SECURE_PREFIX_VALUE or PREFIX_VALUE

        # retrieves the original (raw) path to be used in the construction
        # of the new (domain processed) URL
        original_path = request.original_path

        # construct the URL (new location) with the prefix and using the
        # port part of the value in case a non default secure port is defined
        location = (
            service_connection.connection_port in (80, 443)
            and prefix + force_domain + original_path
            or prefix
            + force_domain
            + ":"
            + str(service_connection.connection_port)
            + original_path
        )

        # sets the status code in the request and then sets the location header
        # (using the location value)
        request.status_code = 302
        request.set_header(LOCATION_VALUE, location)

    def _process_secure(self, request, service_connection, service_configuration):
        """
        Processes the forcing of the connection as secure, running
        this method allows the connection to be redirected to a secure
        channel in case such behavior is required.

        :type request: HTTPRequest
        :param request: The request to be processed.
        :type service_connection: ServiceConnection
        :param service_connection: The service connection currently in use.
        :type service_configuration: Dictionary
        :param service_configuration: The service configuration map.
        """

        # retrieves the service configuration context name and value from the request and the service configuration
        (
            _service_configuration_context_name,
            service_configuration_context,
        ) = self._get_request_service_configuration_context(
            request, service_configuration
        )

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
        if not force_secure:
            return

        # in case the service connection port is the same as the port defined
        # as secure, no need to process the redirection the connection is
        # already considered as secure
        if service_connection.connection_port == secure_port:
            return

        # retrieves the host value from the request headers
        # in order to be able to construct the new full secure
        # address
        host = request.headers_map.get(HOST_VALUE, None)

        # in case the host is not defined, it's not possible
        # to construct the secure URL
        if not host:
            # raises the client request security violation exception
            raise exceptions.ClientRequestSecurityViolation("host not defined")

        # retrieves the "hostname" from the host (removing the port part
        # of the name) then retrieves the original (raw) path to be used in the
        # construction of the secure URL
        hostname = host.rsplit(":", 1)[0]
        original_path = request.original_path

        # construct the secure URL (new location) with the secure prefix and
        # using the port part of the value in case a non default secure port
        # is defined
        location = (
            secure_port == 443
            and SECURE_PREFIX_VALUE + hostname + original_path
            or SECURE_PREFIX_VALUE + hostname + ":" + str(secure_port) + original_path
        )

        # sets the status code in the request and then sets the location header
        # (using the location value)
        request.status_code = 302
        request.set_header(LOCATION_VALUE, location)

    def _get_request_service_configuration_context(
        self, request, service_configuration
    ):
        # retrieves the service configuration contexts
        service_configuration_contexts = service_configuration.get("contexts", {})

        # retrieves the service configuration contexts resolution order
        service_configuration_contexts_resolution_order = (
            service_configuration_contexts.get(
                RESOLUTION_ORDER_VALUE,
                colony.legacy.iterkeys(service_configuration_contexts),
            )
        )

        # retrieves the service configuration contexts resolution order regex
        service_configuration_contexts_resolution_order_regex = (
            service_configuration_contexts.get(RESOLUTION_ORDER_REGEX_VALUE, None)
        )

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
            request_path_match = (
                service_configuration_contexts_resolution_order_regex.match(
                    request_path
                )
            )
        else:
            # sets the request path match ad invalid
            request_path_match = None

        # in case there is a valid request path match
        if request_path_match:
            # retrieves the group index from the request path match
            group_index = request_path_match.lastindex

            # retrieves the service configuration context name
            service_configuration_context_name = (
                service_configuration_contexts_resolution_order[group_index - 1]
            )

            # retrieves the service configuration context
            service_configuration_context = service_configuration_contexts[
                service_configuration_context_name
            ]

        # returns the service configuration context name and value
        return service_configuration_context_name, service_configuration_context

    def _process_handler(self, request, service_configuration):
        """
        Processes the handler stage of the HTTP request.
        Processing handler implies matching the path against the
        various handler rules defined to retrieve the valid handler.

        :type request: HTTPRequest
        :param request: The request to be processed.
        :type service_configuration: Dictionary
        :param service_configuration: The service configuration map.
        :rtype: String
        :return: The processed handler name.
        """

        # retrieves the service configuration context name and value from the request and the service configuration
        (
            service_configuration_context_name,
            service_configuration_context,
        ) = self._get_request_service_configuration_context(
            request, service_configuration
        )

        # retrieves the allow redirection property
        allow_redirection = service_configuration_context.get("allow_redirection", True)

        # in case the request is pending redirection validation
        if request.redirection_validation:
            # in case it does not allow redirection
            if not allow_redirection:
                # changes the path to the base path, avoids the overriding
                # of the original path by unsetting the flag
                request.set_path(request.base_path, set_original_path=False)

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
        (
            _service_configuration_context_name,
            service_configuration_context,
        ) = self._get_request_service_configuration_context(
            request, service_configuration
        )

        # retrieves the authentication handler
        authentication_handler = service_configuration_context.get(
            "authentication_handler", None
        )

        # in case no authentication handler is defined (no
        # authentication is required)
        if not authentication_handler:
            # returns immediately
            return

        # retrieves the authentication properties
        authentication_properties = service_configuration_context.get(
            "authentication_properties", {}
        )

        # retrieves the authentication realm
        authentication_realm = authentication_properties.get(
            "authentication_realm", "default"
        )

        # retrieves the authorization from the request headers
        authorization = request.headers_map.get(AUTHORIZATION_VALUE, None)

        # in case no authorization is defined
        if not authorization:
            # sets the location header
            request.set_header(
                WWW_AUTHENTICATE_VALUE, 'Basic realm="' + authentication_realm + '"'
            )

            # raises the unauthorized exception
            raise exceptions.UnauthorizedException("authentication required", 401)

        # retrieves the authorization type and value
        _authorization_type, authorization_value = authorization.split(" ", 1)

        # decodes the authorization value
        authorization_value_decoded = base64.b64decode(authorization_value)

        # split the authorization value retrieving the username and password
        username, password = authorization_value_decoded.split(":", 1)

        # retrieves the HTTP service authentication handler plugins map
        http_service_authentication_handler_plugins_map = (
            self.service_plugin.system.http_service_authentication_handler_plugins_map
        )

        # in case the authentication handler is not found in the HTTP service authentication
        # handler plugins map
        if (
            not authentication_handler
            in http_service_authentication_handler_plugins_map
        ):
            # raises the HTTP authentication handler not found exception
            raise exceptions.HTTPAuthenticationHandlerNotFoundException(
                "no authentication handler found for current request: "
                + authentication_handler
            )

        # retrieves the HTTP service authentication handler plugin
        http_service_authentication_handler_plugin = (
            http_service_authentication_handler_plugins_map[authentication_handler]
        )

        # uses the authentication handler to try to authenticate
        authentication_result = (
            http_service_authentication_handler_plugin.handle_authentication(
                username, password, authentication_properties
            )
        )

        # retrieves the authentication result valid
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication result is not valid
        if not authentication_result_valid:
            # sets the location header
            request.set_header(WWW_AUTHENTICATE_VALUE, 'Basic realm="Secure Area"')

            # raises the unauthorized exception
            raise exceptions.UnauthorizedException(
                "user is not permitted: " + username, 401
            )

    def _verify_request_information(self, request):
        """
        Verifies the request information, checking if there is
        any possible security problems associated.

        :type request: HTTPRequest
        :param request: The request to be verified.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # retrieves the verify request flag
        verify_request = service_configuration.get("verify_request", True)

        # in case the request is not meant to be verified must
        # returns immediately (avoids validation)
        if not verify_request:
            return

        # retrieves the host value from the request headers
        host = request.headers_map.get(HOST_VALUE, None)

        # in case the host is not defined it's not possible to
        # execute the security validation so it must raise the
        # client request security violation exception
        if not host:
            raise exceptions.ClientRequestSecurityViolation("host not defined")

        # retrieves the allowed host map, note that the default
        # value for the map contains permission to the access
        # from the local machine domain names
        allowed_hosts = service_configuration.get(
            "allowed_hosts", {"127.0.0.1": True, "localhost": True}
        )

        # retrieves the "hostname" from the host and uses this value
        # to check if the hostname is allowed in the allowed hosts
        # map value (security verification)
        hostname = host.rsplit(":", 1)[0]
        host_allowed = allowed_hosts.get(hostname, False)

        # in case the host is not allowed, must raise a client request
        # security violation exception to notify the system about the
        # security problem (avoids data providing)
        if not host_allowed:
            raise exceptions.ClientRequestSecurityViolation(
                "host not allowed: " + hostname
            )

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        :type request: HTTPRequest
        :param request: The request to be used in the resolution
        of the service configuration.
        :rtype: Dictionary
        :return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # retrieves the host value from the request headers
        host = request.headers_map.get(HOST_VALUE, None)

        # in case the host is defined
        if host:
            # retrieves the virtual servers map
            service_configuration_virtual_servers = service_configuration.get(
                "virtual_servers", {}
            )

            # retrieves the service configuration virtual servers resolution order
            service_configuration_virtual_servers_resolution_order = (
                service_configuration_virtual_servers.get(
                    RESOLUTION_ORDER_VALUE,
                    colony.legacy.iterkeys(service_configuration_virtual_servers),
                )
            )

            # splits the host value (to try
            # to retrieve hostname and port)
            host_splitted = host.split(":")

            # retrieves the host splitted length
            host_splitted_length = len(host_splitted)

            # in case the host splitted length is two,
            # retrieves the hostname and the port
            if host_splitted_length == 2:
                hostname, _port = host_splitted
            # otherwise sets the hostname as the host
            # (for size one)
            else:
                hostname = host

            # in case the hostname exists in the service configuration virtual servers map
            if hostname in service_configuration_virtual_servers:
                # iterates over the service configuration virtual server names
                for (
                    service_configuration_virtual_server_name
                ) in service_configuration_virtual_servers_resolution_order:
                    # in case this is the hostname
                    if hostname == service_configuration_virtual_server_name:
                        # retrieves the service configuration virtual server value
                        service_configuration_virtual_server_value = (
                            service_configuration_virtual_servers[
                                service_configuration_virtual_server_name
                            ]
                        )

                        # merges the service configuration map with the service configuration virtual server value,
                        # to retrieve the final service configuration for this request
                        service_configuration = self._merge_values(
                            service_configuration,
                            service_configuration_virtual_server_value,
                        )

                        # breaks the loop
                        break

        # returns the service configuration
        return service_configuration

    def _merge_values(self, target_value, source_value):
        """
        Merges two values into one, the type of the values
        is taken into account and the merge only occurs when
        the type is list or dictionary.

        :type target_list: Object
        :param target_list: The target value to be used.
        :type source_list: Object
        :param source_list: The source value to be used.
        :rtype: Object
        :return: The final resulting value.
        """

        # retrieves the types for both the target and
        # the source values
        target_value_type = type(target_value)
        source_value_type = type(source_value)

        # in case both types are the same (no conflict)
        if target_value_type == source_value_type:
            # in case the type is dictionary
            if target_value_type == dict:
                # merges both maps
                return self._merge_maps(target_value, source_value)
            # in case the type is list
            elif target_value_type == list or target_value_type == tuple:
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

        :type target_list: List
        :param target_list: The target list to be used.
        :type source_list: List
        :param source_list: The source list to be used.
        :rtype: List
        :return: The final resulting list.
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

        :type target_map: Dictionary
        :param target_map: The target map to be used.
        :type source_map: List
        :param source_map: The source map to be used.
        :rtype: List
        :return: The final resulting map.
        """

        # copies the target map as the final map
        final_map = copy.copy(target_map)

        # iterates over all the source map values
        for source_key, source_value in colony.legacy.items(source_map):
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


class HTTPRequest(object):
    """
    The HTTP request class.
    """

    service = None
    """ The reference to the HTTP service that
    is handling the current request (owner service) """

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
    """ The URI """

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
    is allowed for the current REST request context """

    properties = {}
    """ The properties """

    def __init__(
        self,
        service=None,
        service_connection=None,
        content_type_charset=DEFAULT_CHARSET,
    ):
        self.service = service
        self.service_connection = service_connection
        self.content_type_charset = content_type_charset

        self.request_time = time.time()

        self.attributes_map = colony.OrderedMap(True)
        self.headers_map = {}
        self.response_headers_map = {}
        self.headers_in = {}
        self.headers_out = {}
        self.message_stream = colony.StringBuffer()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.operation_type, self.path)

    def __getattributes__(self, attribute_name, default=None):
        """
        Retrieves the attribute from the attributes map.

        :type attribute_name: String
        :param attribute_name: The name of the attribute to retrieve.
        :type default: Object
        :param default: The default object value to be returned in
        case the attribute is not found.
        :rtype: Object
        :return: The retrieved attribute.
        """

        return self.attributes_map.get(attribute_name, default)

    def __setattributes__(self, attribute_name, attribute_value):
        """
        Sets the given attribute in the request. The referenced
        attribute is the HTTP request attribute and the setting takes
        into account a possible duplication of the values.

        :type attribute_name: String
        :param attribute_name: The name of the attribute to be set.
        :type attribute_value: Object
        :param attribute_value: The value of the attribute to be set.
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
            if attribute_value_reference_type == list:
                # adds the attribute value to the attribute value reference
                attribute_value_reference.append(attribute_value)
            # otherwise the attributes is not a list and it must be created
            # for the first time
            else:
                # sets the list with the previously defined attribute reference
                # and the attribute value
                self.attributes_map[attribute_name] = [
                    attribute_value_reference,
                    attribute_value,
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
        # must return the control flow immediately
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

        # sets the arguments as the received message, note that
        # the received message is converted into a string value
        # and then parses the arguments that were just set
        self.arguments = colony.legacy.str(self.received_message)
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
            if (
                attribute_field_splitted_length == 0
                or attribute_field_splitted_length > 2
            ):
                # continues the loops
                continue

            # in case the attribute field splitted length is two
            if attribute_field_splitted_length == 2:
                # retrieves the attribute name and the attribute value,
                # from the attribute field splitted
                attribute_name, attribute_value = attribute_field_splitted

                # "unquotes" the attribute value from the URL encoding
                attribute_value = colony.unquote_plus(attribute_value)
            # in case the attribute field splitted length is one
            elif attribute_field_splitted_length == 1:
                # retrieves the attribute name, from the attribute field splitted
                (attribute_name,) = attribute_field_splitted

                # sets the attribute value to none
                attribute_value = None

            # "unquotes" the attribute name from the URL encoding
            attribute_name = colony.unquote_plus(attribute_name)

            # sets the attribute value
            self.__setattributes__(attribute_name, attribute_value)

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
            # raises the HTTP invalid multipart request exception
            raise exceptions.HTTPInvalidMultipartRequestException(
                "no content type defined"
            )

        # splits the content type
        content_type_splitted = content_type.split(";")

        # retrieves the content type value
        content_type_value = content_type_splitted[0].strip()

        # in case the content type value is not valid
        if not content_type_value == MULTIPART_FORM_DATA_VALUE:
            # raises the HTTP invalid multipart request exception
            raise exceptions.HTTPInvalidMultipartRequestException(
                "invalid content type defined: " + content_type_value
            )

        # retrieves the boundary value
        boundary = content_type_splitted[1].strip()

        # splits the boundary
        boundary_splitted = boundary.split("=")

        # in case the length of the boundary is not two (invalid)
        if not len(boundary_splitted) == 2:
            # raises the HTTP invalid multipart request exception
            raise exceptions.HTTPInvalidMultipartRequestException(
                "invalid boundary value: " + boundary
            )

        # retrieves the boundary reference and the boundary value,
        # ensures byte compatibility and calculates it's length
        _boundary, boundary_value = boundary_splitted
        boundary_value = colony.legacy.bytes(boundary_value)
        boundary_value_length = len(boundary_value)

        # sets the initial index as the as the boundary value length
        # plus the base boundary value of two (equivalent to: --)
        current_index = boundary_value_length + 2

        # iterates indefinitely
        while True:
            # retrieves the end index (boundary start index)
            end_index = self.multipart.find(boundary_value, current_index)

            # in case the end index is invalid (end of multipart)
            # must break the current loop (no more parsing)
            if end_index == -1:
                break

            # parses the multipart part retrieving the headers map and the contents
            # the sent indexes avoid the extra newline values incrementing and decrementing
            # the value of two at the end and start
            headers_map, contents = self._parse_multipart_part(
                current_index + 2, end_index - 2
            )

            # parses the content disposition header retrieving the content
            # disposition map and list (with the attributes order)
            content_disposition_map = self._parse_content_disposition(headers_map)

            # sets the contents in the content disposition map
            content_disposition_map[CONTENTS_VALUE] = contents

            # retrieves the name from the content disposition map
            name = content_disposition_map[NAME_VALUE]

            # sets the attribute
            self.__setattributes__(name, content_disposition_map)

            # sets the current index as the end index
            current_index = end_index + boundary_value_length

    def execute_background(self, callable, retries=0, timeout=0.0, timestamp=None):
        """
        Executes the given callable object in a background
        thread.
        This method is useful for avoid blocking the request
        handling method in non critic tasks.

        :type callable: Callable
        :param callable: The callable to be called in background.
        :type retries: int
        :param retries: The number of times to retry executing the
        callable in case exception is raised.
        :type timeout: float
        :param timeout: The time to be set in between calls of the
        callable, used together with the retry value.
        :type timestamp: float
        :param timestamp: The unix second based timestamp for the
        first execution of the callable.
        """

        self.service_connection.execute_background(
            callable, retries=retries, timeout=timeout, timestamp=timestamp
        )

    def read(self):
        return self.received_message

    def write(self, message, flush=1, encode=True):
        # tries to verify if the message to be written is a
        # generator and if that's the case uses the special
        # version of the method for a mediation handler
        is_generator = colony.legacy.is_generator(message)
        if is_generator:
            return self.write_generator(message)

        # retrieves the message type, so that it's possible to
        # "know" if an encoding operation is required or not
        message_type = type(message)

        # in case the message type is unicode it must be encoded
        # into a plain string using the defined content type value
        if message_type == colony.legacy.UNICODE and encode:
            message = message.encode(self.content_type_charset)

        # writes the message to the message stream so that it's
        # properly sent to the client side of the connection
        message = colony.legacy.bytes(message)
        self.message_stream.write(message)

    def write_generator(self, generator):
        # sets the current request as chunked and then builds
        # the generator based chunked/mediated handler that
        # will be responsible for the mediation operation
        self.chunked_encoding = True
        self.chunk_handler = GeneratorHandler(generator)

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

        :rtype: bool
        :return: If the current request is being transmitted over a secure
        channel (secure request).
        """

        return self.service_connection.is_secure()

    def get_header(self, header_name):
        """
        Retrieves an header value of the request,
        or none if no header is defined for the given
        header name.

        :type header_name: String
        :param header_name: The name of the header to be retrieved.
        :rtype: Object
        :return: The value of the request header.
        """

        return self.headers_map.get(header_name, None)

    def set_header(self, header_name, header_value, encode=True):
        """
        Set a response header value on the request.

        :type header_name: String
        :param header_name: The name of the header to be set.
        :type header_value: Object
        :param header_value: The value of the header to be sent
        in the response.
        :type encode: bool
        :param encode: If the header value should be encoded in
        case the type is unicode.
        """

        # retrieves the header value type
        header_value_type = type(header_value)

        # in case the header value type is unicode
        # and the encode flag is set
        if header_value_type == colony.legacy.UNICODE and encode:
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

        :type header_name: String
        :param header_name: The name of the header to be appended with the value.
        :type header_value: Object
        :param header_value: The value of the header to be appended
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

        :rtype: String
        :return: The result string value of
        the request.
        """

        # validates the current request
        self.validate()

        # creates a new string buffer that will hold the partial contents
        # of the message that is going to be set to the client side
        result = colony.StringBuffer()

        # retrieves the result value from the message, meaning that a proper
        # joining operation will be performed for it as part of building
        message = self.message_stream.get_value()

        # in case the request is encoded, meaning that a special encoding
        # should be applied to the message
        if self.encoded:
            if self.mediated:
                self.mediated_handler.encode_file(
                    self.encoding_handler, self.encoding_type
                )
            elif self.chunked_encoding:
                self.chunk_handler.encode_file(
                    self.encoding_handler, self.encoding_type
                )
            else:
                message = self.encoding_handler(message)

        # in case the request is mediated, meaning that a proper
        # delegation structure is going to be used to guide sending
        if self.mediated:
            # retrieves the content length from the mediated handler
            # so that the retrieval of size is delegated
            self.content_length = self.mediated_handler.get_size()

        # otherwise it's a normal message handling situation
        # where the contents are store in a plain strings
        else:
            # retrieves the content length from the
            # message content itself (measure string)
            self.content_length = len(message)

        # retrieves the value for the status message
        status_message = self.get_status_message()

        # writes the HTTP command in the string buffer (version, status code and status message)
        command = (
            self.protocol_version
            + " "
            + str(self.status_code)
            + " "
            + status_message
            + "\r\n"
        )
        command = colony.legacy.bytes(command)
        result.write(command)

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time according to the HTTP specification
        current_date_time_formatted = current_date_time.strftime(DATE_FORMAT)

        # creates the ordered map to hold the header values
        headers_ordered_map = colony.OrderedMap()

        if self.content_type:
            headers_ordered_map[CONTENT_TYPE_VALUE] = self.content_type
        if self.encoded:
            headers_ordered_map[CONTENT_ENCODING_VALUE] = self.encoding_name
        if self.chunked_encoding:
            headers_ordered_map[TRANSFER_ENCODING_VALUE] = CHUNKED_VALUE
        if (
            not self.chunked_encoding
            and self.contains_message
            and not self.content_length == None
        ):
            headers_ordered_map[CONTENT_LENGTH_VALUE] = str(self.content_length)
        if self.upgrade_mode:
            headers_ordered_map[UPGRADE_VALUE] = self.upgrade_mode
        if self.etag:
            headers_ordered_map[ETAG_VALUE] = self.etag
        if self.max_age:
            headers_ordered_map[CACHE_CONTROL_VALUE] = MAX_AGE_FORMAT % self.max_age
        if self.expiration_timestamp:
            # converts the expiration timestamp to date time and formats it
            # according to the HTTP specification setting it in the headers map
            expiration_date_time = datetime.datetime.fromtimestamp(
                self.expiration_timestamp
            )
            expiration_date_time_formatted = expiration_date_time.strftime(DATE_FORMAT)
            headers_ordered_map[EXPIRES_VALUE] = expiration_date_time_formatted
        if self.last_modified_timestamp:
            # converts the last modified timestamp to date time and formats it
            # according to the HTTP specification setting it in the headers map
            last_modified_date_time = datetime.datetime.fromtimestamp(
                self.last_modified_timestamp
            )
            last_modified_date_time_formatted = last_modified_date_time.strftime(
                DATE_FORMAT
            )
            headers_ordered_map[LAST_MODIFIED_VALUE] = last_modified_date_time_formatted

        # sets the default cache values in the unset header values
        # this should populate all the mandatory fields
        if not CACHE_CONTROL_VALUE in headers_ordered_map:
            headers_ordered_map[CACHE_CONTROL_VALUE] = DEFAULT_CACHE_CONTROL_VALUE

        # sets the base response header values, that are going to be present
        # in every single response to be sent from this server
        headers_ordered_map[CONNECTION_VALUE] = self.connection_mode
        headers_ordered_map[DATE_VALUE] = current_date_time_formatted
        headers_ordered_map[SERVER_VALUE] = SERVER_IDENTIFIER

        # extends the headers ordered map with the response headers map
        headers_ordered_map.extend(self.response_headers_map)

        # iterates over all the header values to be sent so that they are
        # written to the target output buffer as string equivalence values
        for header_name, header_value in colony.legacy.items(headers_ordered_map):
            # verifies if the current type of the header value is unicode
            # and if that the case encodes the value using the default
            # encoding so that the value that is written to the result
            # is always a normalized string value
            is_unicode = type(header_name) == colony.legacy.UNICODE
            if is_unicode:
                header_name = header_name.encode(DEFAULT_CHARSET)
            is_unicode = type(header_value) == colony.legacy.UNICODE
            if is_unicode:
                header_value = header_value.encode(DEFAULT_CHARSET)
            result.write(header_name + b": " + header_value + b"\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write(b"\r\n")
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
            # raises the HTTP runtime exception
            raise exceptions.HTTPRuntimeException("status code not defined")

    def get_server_identifier(self):
        """
        Retrieves a string describing the server.

        :rtype: String
        :return: A string describing the server.
        """

        return SERVER_IDENTIFIER

    def get_service(self):
        """
        Returns the service associated with the request
        the one that owns the current request.

        :rtype: Service
        :return: The service that owns the current
        request (request owner/parent).
        """

        return self.service

    def get_service_connection(self):
        """
        Returns a the service connection object, that
        contains the connection information.

        :rtype: ServiceConnection
        :return: The service connection to be used.
        """

        return self.service_connection

    def get_attributes_list(self):
        """
        Retrieves the list of attribute names in the
        current attributes map.

        :rtype: List
        :return: The list of attribute names in the
        current attributes map.
        """

        return colony.legacy.keys(self.attributes_map)

    def get_attribute(self, attribute_name, default=None):
        return self.__getattributes__(attribute_name, default)

    def set_attribute(self, attribute_name, attribute_value):
        self.__setattributes__(attribute_name, attribute_value)

    def get_message(self):
        return self.message_stream.get_value()

    def set_message(self, message):
        self.message_stream = colony.StringBuffer()
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

    def set_operation_type(self, operation_type):
        self.operation_type = operation_type

    def get_method(self):
        """
        Retrieves the method used in the current request
        object for the current request.
        This method is an alias to the retrieval of the
        operation type.

        :rtype: String
        :return: The method used in the current request
        context.
        """

        return self.get_operation_type()

    def set_path(self, path, set_original_path=True):
        """
        Sets the path in the request.
        The paths is set by processing it, creating
        the resources path.

        An optional set original path flag may be unset
        to allow overriding the original path.

        :type path: String
        :param path: The path to be set in the request.
        :type set_original_path: bool
        :param set_original_path: If the original path
        should be saved in the original path variable for
        later "raw" retrieval (must only be used once).
        """

        # "saves" the original path value
        # without unquoting (in case the flag is set)
        if set_original_path:
            self.original_path = path

        # retrieves the resource path of the path, by
        # splitting the path around the separator
        resource_path = path.split("?")[0]

        # "unquotes", both the global path value and
        # the resource path one, and then sets a series
        # of values in the current request
        path = colony.unquote(path)
        resource_path = colony.unquote(resource_path)
        self.path = path
        self.resource_path = resource_path
        self.filename = resource_path
        self.uri = resource_path

    def set_base_path(self, base_path):
        """
        Sets the base path in the request.
        The base path is set by processing it, creating
        the resources path.

        :type path: String
        :param path: The base path to be set in the request,
        this string should be already unquoted.
        """

        # retrieves the resource base path value by splitting
        # the path around the split token/indicator
        resource_base_path = base_path.split("?")[0]

        # "unquotes" both the base path and the resource
        # path values into their original utf-8 values
        base_path = colony.unquote(base_path)
        resource_base_path = colony.unquote(resource_base_path)

        # sets both the base path and the resource base
        # path values into the request
        self.base_path = base_path
        self.resource_base_path = resource_base_path

    def set_protocol_version(self, protocol_version):
        """
        Sets the protocol version.

        :type protocol_version: String
        :param protocol_version: The protocol version.
        """

        self.protocol_version = protocol_version

    def get_resource_path(self):
        """
        Retrieves the resource path.

        :rtype: String
        :return: The resource path.
        """

        return self.resource_path

    def get_resource_path_decoded(self):
        """
        Retrieves the resource path in decoded format.

        :rtype: String
        :return: The resource path in decoded format.
        """

        # verifies if the data type of the resource path
        # is already unicode if that's the case returns
        # the original value as it's already decoded
        is_unicode = type(self.resource_path) == colony.legacy.UNICODE
        if is_unicode:
            return self.resource_path

        # decodes the resources path using the default
        # charset value and return the value to the caller
        resource_path_decoded = self.resource_path.decode(DEFAULT_CHARSET)
        return resource_path_decoded

    def get_resource_base_path_decoded(self):
        """
        Retrieves the resource base path in decoded format.

        :rtype: String
        :return: The resource base path in decoded format.
        """

        # verifies if the resource base path is unicode based
        # already and if that's the case returns immediately
        is_unicode = colony.legacy.is_unicode(self.resource_base_path)
        if is_unicode:
            return self.resource_base_path

        # decodes the resources base path using the currently defined
        # charset/encoding value and returns the value
        resource_base_path_decoded = self.resource_base_path.decode(DEFAULT_CHARSET)
        return resource_base_path_decoded

    def get_handler_path(self):
        """
        Retrieves the handler path.

        :rtype: String
        :return: The handler path.
        """

        return self.handler_path

    def get_arguments(self):
        """
        Retrieves the arguments.

        :rtype: String
        :return: The arguments.
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

    def get_max_age(self):
        return self.max_age

    def set_max_age(self, max_age):
        self.max_age = max_age

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

    def get_status_message(self):
        """
        Retrieves the current status message value.
        The method returns the defined status message value,
        or the default in case none is defined.

        :rtype: String
        :return: The status message as the string that
        describes the currently defined status code.
        """

        # in case a status message is defined
        if self.status_message:
            # sets the defined status message as the
            # currently set status message
            status_message = self.status_message
        else:
            # retrieves the message for the status code, defaulting
            # to the default value in case none is defined (error)
            status_message = STATUS_MESSAGES.get(
                self.status_code, DEFAULT_STATUS_MESSAGE
            )

        # returns the status message
        return status_message

    def verify_resource_modification(self, modified_timestamp=None, etag_value=None):
        """
        Verifies the resource to check for any modification since the
        value defined in the HTTP request.

        :type modified_timestamp: int
        :param modified_timestamp: The timestamp of the resource modification.
        :type etag_value: String
        :param etag_value: The etag value of the resource.
        :rtype: bool
        :return: The result of the resource modification test.
        """

        # retrieves the if modified header value and in case the
        # modified timestamp and if modified header are defined
        # the date time base modification check must be run
        if_modified_header = self.get_header(IF_MODIFIED_SINCE_VALUE)
        if modified_timestamp and if_modified_header:
            try:
                # converts the if modified header value to date time and then
                # converts the modified timestamp to date time
                if_modified_header_data_time = datetime.datetime.strptime(
                    if_modified_header, DATE_FORMAT
                )
                modified_date_time = datetime.datetime.fromtimestamp(modified_timestamp)

                # in case the modified date time is less or the same
                # as the if modified header date time (no modification)
                # must return false as there was no modification
                if modified_date_time <= if_modified_header_data_time:
                    return False
            except Exception:
                # prints a warning for not being able to check the modification date
                self.service.service_plugin.warning(
                    "Problem while checking modification date"
                )

        # retrieves the if none match value and in case it is
        # defined together with the etag value the etag based
        # checking must be performed
        if_none_match_header = self.get_header(IF_NONE_MATCH_VALUE)
        if etag_value and if_none_match_header:
            # in case the value of the if none match header is the same
            # as the etag value of the file (no modification) must
            # return false as there was no modification
            if if_none_match_header == etag_value:
                return False

        # returns true (modified or no information for
        # modification test)
        return True

    def _parse_multipart_part(self, start_index, end_index):
        """
        Parses a "part" of the whole multipart content bases on the
        interval of send indexes.

        :type start_index: int
        :param start_index: The start index of the "part" to be processed.
        :type end_index: int
        :param end_index: The end index of the "part" to be processed.
        :rtype: Tuple
        :return: A Tuple with a map of header for the "part" and the content of the "part".
        """

        # creates the headers map
        headers_map = {}

        # retrieves the end header index
        end_header_index = self.multipart.find(b"\r\n\r\n", start_index, end_index)

        # retrieves the headers from the multipart
        headers = self.multipart[start_index:end_header_index]

        # splits the headers by line
        headers_splitted = headers.split(b"\r\n")

        # iterates over the headers lines
        for header_splitted in headers_splitted:
            # finds the header separator
            division_index = header_splitted.find(b":")

            # retrieves the header name and the value for it and then
            # converts both of the values to plain based unicode values
            header_name = header_splitted[:division_index].strip()
            header_value = header_splitted[division_index + 1 :].strip()
            header_name = colony.legacy.str(header_name)
            header_value = colony.legacy.str(header_value)

            # sets the header in the headers map
            headers_map[header_name] = header_value

        # retrieves the contents from the multipart
        contents = self.multipart[end_header_index + 4 : end_index - 2]

        # returns the headers map and the contents as a tuple
        return (headers_map, contents)

    def _parse_content_disposition(self, headers_map):
        """
        Parses the content disposition value from the headers map.
        This method returns a map containing associations of key and value
        of the various content disposition values.

        :type headers_map: Dictionary
        :param headers_map: The map containing the headers and the values.
        :rtype: Dictionary
        :return: The map containing the various disposition values in a map.
        """

        # retrieves the content disposition header
        content_disposition = headers_map.get(CONTENT_DISPOSITION_VALUE, None)

        # in case no content disposition is defined
        if not content_disposition:
            # raises the HTTP invalid multipart request exception
            raise exceptions.HTTPInvalidMultipartRequestException(
                "missing content disposition in multipart value"
            )

        # splits the content disposition to obtain the attributes
        content_disposition_attributes = content_disposition.split(";")

        # creates the content disposition map
        content_disposition_map = {}

        # iterates over all the content disposition attributes
        # the content disposition attributes are not stripped
        for content_disposition_attribute in content_disposition_attributes:
            # strips the content disposition attribute
            content_disposition_attribute_stripped = (
                content_disposition_attribute.strip()
            )

            # splits the content disposition attribute
            content_disposition_attribute_splitted = (
                content_disposition_attribute_stripped.split("=")
            )

            # retrieves the length of the content disposition attribute splitted
            content_disposition_attribute_splitted_length = len(
                content_disposition_attribute_splitted
            )

            # in case the length is two (key and value)
            if content_disposition_attribute_splitted_length == 2:
                # retrieves the key and the value
                key, value = content_disposition_attribute_splitted

                # strips the value from the string items
                value_stripped = value.strip('"')

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
                # raises the HTTP invalid multipart request exception
                raise exceptions.HTTPInvalidMultipartRequestException(
                    "invalid content disposition value in multipart value: "
                    + content_disposition_attribute_stripped
                )

        # returns the content disposition map
        return content_disposition_map


class GeneratorHandler(object):
    """
    The mediated handler class that is able to encapsulate
    the logic for the generator python structure.
    """

    generator = None
    """ The generator that is going to be encapsulated
    using the current class's object """

    def __init__(self, generator):
        self.generator = generator

    def encode_file(self, encoding_handler, encoding_name):
        pass

    def get_size(self):
        return None

    def get_chunk(self, chunk_size=CHUNK_SIZE):
        try:
            return next(self.generator)
        except StopIteration:
            return None

    def close(self):
        self.generator.close()
