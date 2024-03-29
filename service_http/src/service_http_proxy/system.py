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

import colony

from . import exceptions

HANDLER_NAME = "proxy"
""" The handler name """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_PROXY_TARGET = ""
""" The default proxy target """

DEFAULT_PROXY_SERVICE_TYPE = "sync"
""" The default proxy target """

DEFAULT_ELEMENT_POOL_SIZE = 64
""" The default element pool size """

CHUNK_SIZE = 4096
""" The chunk size """

HTTP_PREFIX_VALUE = "http://"
""" The HTTP prefix value """

HTTPS_PREFIX_VALUE = "https://"
""" The HTTPS prefix value """

DEFAULT_HOST_VALUE = "unknown"
""" The default host value """

PROXY_TYPE_VALUE = "proxy_type"
""" The proxy type value """

PROXY_TARGET_VALUE = "proxy_target"
""" The proxy target value """

PROXY_SERVICE_TYPE_VALUE = "proxy_service_type"
""" The proxy service type value """

FORWARD_VALUE = "forward"
""" The forward value """

REVERSE_VALUE = "reverse"
""" The reverse value """

HEADERS_VALUE = "headers"
""" The headers value """

MESSAGE_DATA_VALUE = "message_data"
""" The message data value """

SYNC_VALUE = "sync"
""" The sync value """

ASYNC_VALUE = "async"
""" The async value """

VIA_VALUE = "Via"
""" The via value """

HOST_VALUE = "Host"
""" The host value """

LOCATION_VALUE = "Location"
""" The location value """

CONTENT_LENGTH_VALUE = "Content-Length"
""" The content length value """

CONTENT_LENGTH_LOWER_VALUE = "Content-length"
""" The content length lower value """

HTTP_PROTOCOL_PREFIX_VALUE = "HTTP/"
""" The HTTP protocol prefix value """

REMOVAL_HEADERS = (HOST_VALUE,)
""" The removal headers list """

TRANSFER_ENCODING_VALUE = "Transfer-Encoding"
""" The transfer encoding value """

REMOVAL_RESPONSE_HEADERS = (TRANSFER_ENCODING_VALUE,)
""" The removal response headers list """


class ServiceHTTPProxy(colony.System):
    """
    The service HTTP proxy (handler) class.
    """

    request_handler_methods_map = {}
    """ The request handler method map """

    forward_handler_methods_map = {}
    """ The forward handler method map """

    reverse_handler_methods_map = {}
    """ The reverse handler method map """

    http_clients_pool = None
    """ The the pool HTTP clients to be used """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)

        self.request_handler_methods_map = {
            FORWARD_VALUE: self.handle_forward_request,
            REVERSE_VALUE: self.handle_reverse_request,
        }

        self.forward_handler_methods_map = {
            SYNC_VALUE: self._handle_forward_request_sync,
            ASYNC_VALUE: self._handle_forward_request_async,
        }

        self.reverse_handler_methods_map = {
            SYNC_VALUE: self._handle_reverse_request_sync,
            ASYNC_VALUE: self._handle_reverse_request_async,
        }

    def load_handler(self):
        """
        Handler called upon load.
        """

        # retrieves the element pool manager plugin
        element_pool_manager_plugin = self.plugin.element_pool_manager_plugin

        # creates a new HTTP clients pool
        self.http_clients_pool = element_pool_manager_plugin.create_new_element_pool(
            self._create_http_client,
            self._destroy_http_client,
            DEFAULT_ELEMENT_POOL_SIZE,
        )

        # starts the HTTP clients pool
        self.http_clients_pool.start({})

    def unload_handler(self):
        """
        Handler called upon unload.
        """

        # stops the HTTP clients pool
        self.http_clients_pool.stop({})

    def get_handler_name(self):
        """
        Retrieves the handler name.

        :rtype: String
        :return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given HTTP request.

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        # retrieves the proxy type
        proxy_type = request.properties.get(PROXY_TYPE_VALUE, FORWARD_VALUE)

        # retrieves the request handler method
        request_handler_method = self.request_handler_methods_map.get(proxy_type, None)

        # in case the request handler method is not
        # defined (invalid proxy type)
        if not request_handler_method:
            # raises an invalid HTTP proxy runtime exception
            raise exceptions.HTTPProxyRuntimeException("invalid proxy type")

        # calls the request handler method
        request_handler_method(request)

    def handle_forward_request(self, request):
        """
        Handles the given "forward" request.
        Handling the "forward" request implies changing it
        and redirecting (externally) it according to the defined rules.
        Handling this "forward" request implies that the
        client defines the correct path for the request.
        The forward proxy is useful for things like traffic tracking
        publicity and other manipulations to the normal web traffic.

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        # retrieves the proxy service type
        # (type of handling strategy)
        proxy_service_type = request.properties.get(
            PROXY_SERVICE_TYPE_VALUE, DEFAULT_PROXY_SERVICE_TYPE
        )

        # retrieves the forward handler method
        forward_handler_method = self.forward_handler_methods_map.get(
            proxy_service_type, None
        )

        # in case the forward handler method is not
        # defined (invalid proxy type)
        if not forward_handler_method:
            # raises an invalid HTTP proxy runtime exception
            raise exceptions.HTTPProxyRuntimeException(
                "invalid proxy service type (for forward proxy)"
            )

        # calls the forward handler method
        forward_handler_method(request)

    def _handle_forward_request_sync(self, request):
        """
        Handles the given "forward" request using a
        synchronous strategy (more memory usage).

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        # retrieves the resource base path
        resource_base_path = request.get_resource_path_decoded()

        # calculates the real path difference
        path = resource_base_path

        # retrieves the request attributes map
        request_attributes_map = request.attributes_map

        # creates the request headers from the request
        request_headers = self._create_request_headers(request)

        # reads the request contents
        request_contents = request.read()

        # creates the complete path from the proxy path
        complete_path = path

        # retrieves the HTTP client from the HTTP clients pool
        http_client = self.http_clients_pool.pop(True)

        # in case no HTTP client is available an HTTP client
        # unavailable exception is raised
        if not http_client:
            raise exceptions.HTTPClientUnavailableException(
                "HTTP clients pool depleted", 503
            )

        try:
            # fetches the contents from the URL
            http_response = http_client.fetch_url(
                complete_path,
                method=request.operation_type,
                parameters=request_attributes_map,
                headers=request_headers,
                content_type_charset=DEFAULT_CHARSET,
                encode_path=True,
                contents=request_contents,
            )
        finally:
            # puts the HTTP client back into the HTTP clients pool
            self.http_clients_pool.put(http_client)

        # retrieves the status code form the HTTP response
        status_code = http_response.status_code

        # retrieves the status message from the HTTP response
        status_message = http_response.status_message

        # retrieves the data from the HTTP response
        data = http_response.received_message

        # retrieves the headers map from the HTTP response
        headers_map = http_response.headers_map

        # sets the request status code
        request.status_code = status_code

        # sets the request status message
        request.status_message = status_message

        # sets the response headers map
        request.response_headers_map = headers_map

        # writes the (received) data to the request
        request.write(data)

    def _handle_forward_request_async(self, request):
        """
        Handles the given "forward" request using an
        asynchronous strategy (less memory usage).

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        # retrieves the resource base path
        resource_base_path = request.get_resource_path_decoded()

        # calculates the real path difference
        path = resource_base_path

        # retrieves the request attributes map
        request_attributes_map = request.attributes_map

        # creates the request headers from the request
        request_headers = self._create_request_headers(request)

        # reads the request contents
        request_contents = request.read()

        # creates the complete path from the proxy path
        complete_path = path

        # retrieves the HTTP client from the HTTP clients pool
        http_client = self.http_clients_pool.pop(True)

        # in case no HTTP client is available an HTTP client
        # unavailable exception is raised
        if not http_client:
            raise exceptions.HTTPClientUnavailableException(
                "HTTP clients pool depleted", 503
            )

        try:
            # fetches the contents from the URL
            http_response_generator = http_client.fetch_url(
                complete_path,
                method=request.operation_type,
                parameters=request_attributes_map,
                headers=request_headers,
                content_type_charset=DEFAULT_CHARSET,
                encode_path=True,
                contents=request_contents,
                save_message=False,
                yield_response=True,
            )

            # tries to retrieve the generator value for the headers
            generator_value = self._get_generator_value(
                http_response_generator, HEADERS_VALUE
            )

            # unpacks the generator value into the value type
            # and the HTTP response
            _generator_value_type, http_response = generator_value

            # retrieves the status code form the HTTP response
            status_code = http_response.status_code

            # retrieves the status message from the HTTP response
            status_message = http_response.status_message

            # creates the headers map from the HTTP response
            headers_map = http_response.headers_map

            # sets the request status code
            request.status_code = status_code

            # sets the request status message
            request.status_message = status_message

            # sets the response headers map
            request.response_headers_map = headers_map

            # creates the handler to be used to close the sending of the response
            # this handler ensures that the client is put back to the HTTP clients
            # pool and that the connection is kept clean (avoids pipe pollution)
            def close_handler(empty_connection):
                # closes the client connection in the HTTP
                # client (avoids pipe pollution)
                http_client.client_connection.close()

                # puts the HTTP client back into the HTTP
                # clients pool
                self.http_clients_pool.put(http_client)

            # retrieves the HTTP response size by casting
            # the content length value (if possible)
            http_response_size = self._get_http_response_size(http_response)

            # creates the chunk handler to be used to send the proxy response
            # this is way it's possible to progressively send the message from the
            chunk_handler = ChunkHandler(
                http_response_generator, http_response_size, close_handler
            )

            # sets the request as mediated
            request.mediated = True

            # sets the mediated handler in the request
            request.mediated_handler = chunk_handler
        except:
            # closes the HTTP client connection, there's
            # probably data pending in the connection
            # (avoids pipe pollution)
            http_client.client_connection.close()

            # puts the HTTP client back into the HTTP clients pool
            self.http_clients_pool.put(http_client)

            # re-raises the exception
            raise

    def handle_reverse_request(self, request):
        """
        Handles the given "reverse" request.
        Handling the "reverse" request implies changing it
        and redirecting it (locally) according to the defined rules.
        Handling this "reverse" request should be considered
        transparent to the client, the client does not defines
        any additional path and it should think that the communication
        his being made with the current host.

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        # retrieves the proxy service type
        # (type of handling strategy)
        proxy_service_type = request.properties.get(
            PROXY_SERVICE_TYPE_VALUE, DEFAULT_PROXY_SERVICE_TYPE
        )

        # retrieves the reverse handler method
        reverse_handler_method = self.reverse_handler_methods_map.get(
            proxy_service_type, None
        )

        # in case the reverse handler method is not
        # defined (invalid proxy type)
        if not reverse_handler_method:
            # raises an invalid HTTP proxy runtime exception
            raise exceptions.HTTPProxyRuntimeException(
                "invalid proxy service type (for reverse proxy)"
            )

        # calls the reverse handler method
        reverse_handler_method(request)

    def _handle_reverse_request_sync(self, request):
        """
        Handles the given "reverse" request using a
        synchronous strategy (more memory usage).

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        # retrieves the (reverse) proxy target
        proxy_target = request.properties.get(PROXY_TARGET_VALUE, DEFAULT_PROXY_TARGET)

        # retrieves the resource base path
        resource_base_path = request.get_resource_path_decoded()

        # calculates the real path difference
        path = resource_base_path.replace(request.handler_path, "", 1)

        # retrieves the request attributes map
        request_attributes_map = request.attributes_map

        # creates the request headers from the request
        request_headers = self._create_request_headers(request)

        # reads the request contents
        request_contents = request.read()

        # creates the complete path from the proxy
        # target and the path
        complete_path = proxy_target + path

        # retrieves the HTTP client from the HTTP clients pool
        http_client = self.http_clients_pool.pop(True)

        # in case no HTTP client is available an HTTP client
        # unavailable exception is raised
        if not http_client:
            raise exceptions.HTTPClientUnavailableException(
                "HTTP clients pool depleted", 503
            )

        try:
            # fetches the contents from the URL
            http_response = http_client.fetch_url(
                complete_path,
                method=request.operation_type,
                parameters=request_attributes_map,
                headers=request_headers,
                content_type_charset=DEFAULT_CHARSET,
                encode_path=True,
                contents=request_contents,
            )
        finally:
            # puts the HTTP client back into the HTTP clients pool
            self.http_clients_pool.put(http_client)

        # retrieves the status code form the HTTP response
        status_code = http_response.status_code

        # retrieves the status message from the HTTP response
        status_message = http_response.status_message

        # retrieves the data from the HTTP response
        data = http_response.received_message

        # creates the headers map from the HTTP response
        headers_map = self._create_headers_map(
            request, http_response, REMOVAL_RESPONSE_HEADERS
        )

        # sets the request status code
        request.status_code = status_code

        # sets the request status message
        request.status_message = status_message

        # sets the response headers map
        request.response_headers_map = headers_map

        # writes the (received) data to the request
        request.write(data)

    def _handle_reverse_request_async(self, request):
        """
        Handles the given "reverse" request using an
        asynchronous strategy (less memory usage).

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        # retrieves the (reverse) proxy target
        proxy_target = request.properties.get(PROXY_TARGET_VALUE, DEFAULT_PROXY_TARGET)

        # retrieves the resource base path
        resource_base_path = request.get_resource_path_decoded()

        # calculates the real path difference
        path = resource_base_path.replace(request.handler_path, "", 1)

        # retrieves the request attributes map
        request_attributes_map = request.attributes_map

        # creates the request headers from the request
        request_headers = self._create_request_headers(request)

        # reads the request contents
        request_contents = request.read()

        # creates the complete path from the proxy
        # target and the path
        complete_path = proxy_target + path

        # retrieves the HTTP client from the HTTP clients pool
        http_client = self.http_clients_pool.pop(True)

        # in case no HTTP client is available an HTTP client
        # unavailable exception is raised
        if not http_client:
            raise exceptions.HTTPClientUnavailableException(
                "HTTP clients pool depleted", 503
            )

        try:
            # fetches the contents from the URL
            http_response_generator = http_client.fetch_url(
                complete_path,
                method=request.operation_type,
                parameters=request_attributes_map,
                headers=request_headers,
                content_type_charset=DEFAULT_CHARSET,
                encode_path=True,
                contents=request_contents,
                save_message=False,
                yield_response=True,
            )

            # tries to retrieve the generator value for the headers
            generator_value = self._get_generator_value(
                http_response_generator, HEADERS_VALUE
            )

            # unpacks the generator value into the value type
            # and the HTTP response
            _generator_value_type, http_response = generator_value

            # retrieves the status code form the HTTP response
            status_code = http_response.status_code

            # retrieves the status message from the HTTP response
            status_message = http_response.status_message

            # creates the headers map from the HTTP response
            headers_map = self._create_headers_map(request, http_response)

            # sets the request status code
            request.status_code = status_code

            # sets the request status message
            request.status_message = status_message

            # sets the response headers map
            request.response_headers_map = headers_map

            # creates the handler to be used to close the sending of the response
            # this handler ensures that the client is put back to the HTTP clients
            # pool and that the connection is kept clean (avoids pipe pollution)
            def close_handler(empty_connection):
                # closes the client connection in the HTTP
                # client (avoids pipe pollution)
                http_client.client_connection.close()

                # puts the HTTP client back into the HTTP
                # clients pool
                self.http_clients_pool.put(http_client)

            # retrieves the HTTP response size by casting
            # the content length value (if possible)
            http_response_size = self._get_http_response_size(http_response)

            # creates the chunk handler to be used to send the proxy response
            # this is way it's possible to progressively send the message from the
            chunk_handler = ChunkHandler(
                http_response_generator, http_response_size, close_handler
            )

            # sets the request as mediated
            request.mediated = True

            # sets the mediated handler in the request
            request.mediated_handler = chunk_handler
        except:
            # closes the HTTP client connection, there's
            # probably data pending in the connection
            # (avoids pipe pollution)
            http_client.client_connection.close()

            # puts the HTTP client back into the HTTP clients pool
            self.http_clients_pool.put(http_client)

            # re-raises the exception
            raise

    def _create_http_client(self, arguments):
        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # creates the HTTP client
        http_client = client_http_plugin.create_client({})

        # opens the HTTP client
        http_client.open(arguments)

        # disables the "auto" redirect in the HTTP client
        http_client.set_redirect(False)

        # returns the HTTP client
        return http_client

    def _destroy_http_client(self, http_client, arguments):
        # closes the HTTP client
        http_client.close(arguments)

    def _create_request_headers(self, request):
        # creates a new map for the request headers
        request_headers = {}

        # copies the original request headers to the request headers
        colony.map_copy(request.headers_map, request_headers)

        # iterates over all the headers to be removed
        for removal_header in REMOVAL_HEADERS:
            # in case the removal header does not exist
            # in the request headers, no need to continue
            if not removal_header in request_headers:
                # continues the loop
                continue

            # removes the header from the request headers
            del request_headers[removal_header]

        # returns the request headers
        return request_headers

    def _create_headers_map(self, request, http_response, removal_response_headers=()):
        # retrieves the URL parser plugin
        url_parser_plugin = self.plugin.url_parser_plugin

        # creates a new map for the headers map
        headers_map = {}

        # copies the original request headers to the request headers
        colony.map_copy(http_response.headers_map, headers_map)

        # iterates over all the response headers to be removed
        for removal_response_header in removal_response_headers:
            # in case the removal response header does not exist
            # in the headers map, no need to continue
            if not removal_response_header in headers_map:
                # continues the loop
                continue

            # removes the response header from the headers map
            del headers_map[removal_response_header]

        # in case the location value exists in the headers map
        if LOCATION_VALUE in headers_map:
            # retrieves the location from the headers map
            location = headers_map[LOCATION_VALUE]

            # retrieves the proxy target
            proxy_target = request.properties.get(
                PROXY_TARGET_VALUE, DEFAULT_PROXY_TARGET
            )

            # creates the handler path from the handler base path
            # or from the handler path (depending on the valid one)
            handler_path = request.handler_base_path or request.handler_path

            # sets the valid handler path based on the length of the path
            handler_path = not handler_path == "/" and handler_path or ""

            # in case the location starts with the HTTP prefix or
            # with the HTTPS prefix (absolute path)
            if location.startswith(HTTP_PREFIX_VALUE) or location.startswith(
                HTTPS_PREFIX_VALUE
            ):
                # replaces the proxy target for the handler path
                location = location.replace(proxy_target, handler_path)
            # in case the location starts with a slash (relative to host path)
            elif location.startswith("/"):
                # parses the URL retrieving the URL structure
                url_structure = url_parser_plugin.parse_url(proxy_target)

                # retrieves the resource reference from the URL structure
                # or sets the default one (empty) in case it's not defined
                resource_reference = url_structure.resource_reference or ""

                # removes the resource reference from the location
                location = location.replace(resource_reference, "")

                # creates the location with the handler path and the original location
                location = handler_path + location

            # sets the location in the headers map
            headers_map[LOCATION_VALUE] = location

        # retrieves the protocol version number from the protocol
        # version string
        protocol_version_number = request.protocol_version.strip(
            HTTP_PROTOCOL_PREFIX_VALUE
        )

        # retrieves the host value from the request
        host = request.headers_map.get(HOST_VALUE, DEFAULT_HOST_VALUE)

        # retrieves the server identifier
        server_identifier = request.get_server_identifier()

        # sets the via header in the headers map
        headers_map[VIA_VALUE] = (
            protocol_version_number + " " + host + " (" + server_identifier + ")"
        )

        # returns the headers map
        return headers_map

    def _get_http_response_size(self, http_response):
        """
        Retrieves the size of the response (message) based
        on the content length header value.
        In case the content length header value is not set

        :type http_response: HTTPResponse
        :param http_response: The HTTP response to retrieve
        the (target) message size.
        :rtype: int
        :return: The message size for the given HTTP response
        measured in bytes.
        """

        # retrieves the headers map from the HTTP response
        headers_map = http_response.headers_map

        # in case the content length is defined in the headers map
        if CONTENT_LENGTH_VALUE in headers_map:
            # retrieves the message size
            http_response_size = int(http_response.headers_map[CONTENT_LENGTH_VALUE])
        # in case the content length (lower case) is defined in the headers map
        elif CONTENT_LENGTH_LOWER_VALUE in headers_map:
            # retrieves the message size
            http_response_size = int(headers_map[CONTENT_LENGTH_LOWER_VALUE])
        # otherwise no size is defined in the headers
        else:
            # sets the message size as undefined
            http_response_size = None

        # returns the HTTP response size
        return http_response_size

    def _get_generator_value(self, generator, value_type):
        """
        Retrieves the generator value for the given generator
        and for the given (target) value type.

        :type generator: Generator
        :param generator: The generator to be used to
        retrieves the "target" value.
        :type value_type: String
        :param value_type: The type of the value to be retrieved.
        :rtype: Object
        :return: The retrieved object according to the value type.
        """

        # iterates continuously
        while True:
            try:
                # retrieves the "next" value from
                # the generator
                value = next(generator)
            except StopIteration:
                # returns none (nothing found)
                return None

            # retrieves the value type
            type = value[0]

            # in case the type matches the request
            # value type
            if type == value_type:
                # breaks the loop (found
                # the target item)
                break

        # returns the value
        return value


class ChunkHandler(object):
    """
    The chunk handler class.
    Used to send a progressive response
    to the client.
    """

    http_response_generator = None
    """ The generator to be used to progressively retrieve the HTTP response """

    http_response_size = 0
    """ The size of the HTTP response """

    close_handler = None
    """ The handler to be called on closing """

    _closed = False
    """ The falg that controls the close state of the chunk handler """

    _empty_connection = False
    """ The flag controlling if the connection is empty (all data parsed) """

    def __init__(self, http_response_generator, http_response_size, close_handler):
        """
        Constructor of the class.

        :type http_response_generator: Generator
        :param http_response_generator: The generator to be
        used in the HTTP response.
        :type http_response_size: int
        :param http_response_size: The size in bytes of the
        HTTP reponse.
        :type close_handler: Function
        :param close_handler: The handler to be called on
        closing.
        """

        self.http_response_generator = http_response_generator
        self.http_response_size = http_response_size
        self.close_handler = close_handler

    def get_size(self):
        """
        Retrieves the size of the response being chunked.

        :rtype: int
        :return: The size of the response being chunked.
        """

        return self.http_response_size

    def get_chunk(self, chunk_size=CHUNK_SIZE):
        """
        Retrieves the a chunk with the given size.

        :rtype: chunk_size
        :return: The size of the chunk to be retrieved.
        :rtype: String
        :return: A chunk with the given size.
        """

        # in case the chunk handler is
        # currently closed
        if self._closed:
            # returns none (nothing to be retrieved
            # from a closed chunk handler)
            return None

        # iterates continuously, searching
        # for message data
        while True:
            try:
                # retrieves the "next" value from
                # the response generator
                value = next(self.http_response_generator)
            except StopIteration:
                # set the empty connection flag
                self._empty_connection = True

                # returns none (nothing found)
                return None

            # in case an invalid value
            # was retrieved must return it
            if not value:
                return value

            # retrieves the type of the value
            # in order to check if it's valid
            value_type = type(value)

            # in case the value is not of type tuple
            # (not important for now) continues loop
            if not value_type == tuple:
                continue

            # retrieves the value type
            _type = value[0]

            # in case the type is message
            # data must break the loop
            if _type == MESSAGE_DATA_VALUE:
                break

        # retrieves the message data
        # value (buffer)
        message_data = value[2]

        # returns the message data
        return message_data

    def close(self):
        """
        Closes the chunked handler.
        """

        # in case the chunk handler is already closed
        if self._closed:
            # returns immediately
            return

        # sets the closed flag
        self._closed = True

        # calls the close handler (in case
        # the handler is set) the empty connection
        # argument ensures that the handler may take
        # measures to avoid pipe pollution
        self.close_handler and self.close_handler(self._empty_connection)
