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

import colony.libs.map_util

HANDLER_NAME = "proxy"
""" The handler name """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_PROXY_TARGET = ""
""" The default proxy target """

DEFAULT_ELEMENT_POOL_SIZE = 10
""" The default element pool size """

DEFAULT_HOST_VALUE = "unknown"
""" The default host value """

VIA_VALUE = "Via"
""" The via value """

HOST_VALUE = "Host"
""" The host value """

TRANSFER_ENCODING_VALUE = "Transfer-Encoding"
""" The transer encoding value """

HTTP_PROTOCOL_PREFIX_VALUE = "HTTP/"
""" The http protocol prefix value """

REMOVAL_HEADERS = (HOST_VALUE,)
""" The removal headers list """

REMOVAL_RESPONSE_HEADERS = (TRANSFER_ENCODING_VALUE,)
""" The removal response headers list """

class MainServiceHttpProxyHandler:
    """
    The main service http proxy handler class.
    """

    main_service_http_proxy_handler_plugin = None
    """ The main service http proxy handler plugin """

    http_clients_pool = None
    """ The the pool http clients to be used """

    def __init__(self, main_service_http_proxy_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_proxy_handler_plugin: MainServiceHttpProxyHandlerPlugin
        @param main_service_http_proxy_handler_plugin: The main service http proxy handler plugin.
        """

        self.main_service_http_proxy_handler_plugin = main_service_http_proxy_handler_plugin

    def load_handler(self):
        """
        Handler called uppon load.
        """

        # retrieves the element pool manager plugin
        element_pool_manager_plugin = self.main_service_http_proxy_handler_plugin.element_pool_manager_plugin

        # creates a new http clients pool
        self.http_clients_pool = element_pool_manager_plugin.create_new_element_pool(self._create_http_client, self._destroy_http_client, DEFAULT_ELEMENT_POOL_SIZE)

        # starts the http clients pool
        self.http_clients_pool.start({})

    def unload_handler(self):
        """
        Handler called uppon unload.
        """

        # stops the http clients pool
        self.http_clients_pool.stop({})

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

        # retrieves the proxy target
        proxy_target = request.properties.get("proxy_target", DEFAULT_PROXY_TARGET)

        # calculates the real path difference
        path = request.base_path.replace(request.handler_path, "", 1)

        # creates the request headers from the request
        request_headers = self._create_request_headers(request)

        # reads the request contents
        request_contents = request.read()

        # creates the complete path from the proxy
        # target and the path
        complete_path = proxy_target + path

        # retrieves the http client from the http clients pool
        http_client = self.http_clients_pool.pop()

        try:
            # fetches the contents from the url
            http_response = http_client.fetch_url(complete_path, method = request.operation_type, headers = request_headers, content_type_charset = DEFAULT_CHARSET, contents = request_contents)
        finally:
            # puts the http client back into the http clients pool
            self.http_clients_pool.put(http_client)

        # retrieves the status code form the http response
        status_code = http_response.status_code

        # retrieves the status message from the http response
        status_message = http_response.status_message

        # retrieves the data from the http response
        data = http_response.received_message

        # creates the headers map from the http response
        headers_map = self._create_headers_map(request, http_response)

        # sets the request status code
        request.status_code = status_code

        # sets the request status message
        request.status_message = status_message

        # sets the response headers map
        request.response_headers_map = headers_map

        # writes the (received) data to the request
        request.write(data)

    def _create_http_client(self, arguments):
        # retrieves the main client http plugin
        main_client_http_plugin = self.main_service_http_proxy_handler_plugin.main_client_http_plugin

        # creates the http client
        http_client = main_client_http_plugin.create_client({})

        # opens the http client
        http_client.open(arguments)

        # returns the http client
        return http_client

    def _destroy_http_client(self, http_client, arguments):
        # closes the http client
        http_client.close(arguments)

    def _create_request_headers(self, request):
        # creates a new map for the request headers
        request_headers = {}

        # copies the original request headers to the request headers
        colony.libs.map_util.map_copy(request.headers_map, request_headers)

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

    def _create_headers_map(self, request, http_response):
        # creates a new map for the headers map
        headers_map = {}

        # copies the original request headers to the request headers
        colony.libs.map_util.map_copy(http_response.headers_map, headers_map)

        # iterates over all the response headers to be removed
        for removal_response_header in REMOVAL_RESPONSE_HEADERS:
            # in case the removal response header does not exist
            # in the headers map, no need to continue
            if not removal_response_header in headers_map:
                # continues the loop
                continue

            # removes the response header from the headers map
            del headers_map[removal_response_header]

        # retrieves the protocol version number from the protocol
        # version string
        protocol_version_number = request.protocol_version.strip(HTTP_PROTOCOL_PREFIX_VALUE)

        # retrieves the host value from the request
        host = request.headers_map.get(HOST_VALUE, DEFAULT_HOST_VALUE)

        # retrieves the server identifier
        server_identifier = request.get_server_identifier()

        # sets the via header in the headers map
        headers_map[VIA_VALUE] = protocol_version_number  + " " + host + " (" +  server_identifier + ")"

        # returns the headers map
        return headers_map
