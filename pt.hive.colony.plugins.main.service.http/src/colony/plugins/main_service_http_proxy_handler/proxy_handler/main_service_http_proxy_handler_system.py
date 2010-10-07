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


HANDLER_NAME = "proxy"
""" The handler name """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_PROXY_TARGET = ""
""" The default proxy target """

class MainServiceHttpProxyHandler:
    """
    The main service http proxy handler class.
    """

    main_service_http_proxy_handler_plugin = None
    """ The main service http proxy handler plugin """

    def __init__(self, main_service_http_proxy_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_proxy_handler_plugin: MainServiceHttpProxyHandlerPlugin
        @param main_service_http_proxy_handler_plugin: The main service http proxy handler plugin.
        """

        self.main_service_http_proxy_handler_plugin = main_service_http_proxy_handler_plugin

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

        # retrieves the main client http plugin
        main_client_http_plugin = self.main_service_http_proxy_handler_plugin.main_client_http_plugin

        # creates the http client
        http_client = main_client_http_plugin.create_client({})

        # opens the http client
        http_client.open({})

        print "---------"
        print proxy_target
        print request.base_path
        print request.handler_path

        # calculates the real path difference
        path = request.base_path.replace(request.handler_path, "", 1)

        print path

        # reads the request contents
        contents = request.read()

        CONTENT_TYPE_VALUE = "Content-Type"
        """ The content type value """

        content_type = request.get_header(CONTENT_TYPE_VALUE) or "utf-8"

        # PRECISO DE ALTERAR O CLIENTE DE HTTP PARA TER SUPORE PARA MANDAR
        # e receber headers

        #http_client.fetch_url("http://www.sapo.pt", method = GET_METHOD_VALUE, parameters = {}, protocol_version = HTTP_1_1_VERSION, content_type = DEFAULT_CONTENT_TYPE, content_type_charset = DEFAULT_CHARSET, contents = None)

        # o problema tlx esteja no redirect :)

        a = proxy_target + path

        print "vai fazer fetch a '%s'" % a

        # fetches the contents from the url
        http_response = http_client.fetch_url(proxy_target + path, method = request.operation_type, content_type = content_type, contents = contents)

        # retrieves the status code form the http response
        status_code = http_response.status_code

        # retrieves the status message from the http response
        status_message = http_response.status_message

        # retrieves the data from the http response
        data = http_response.received_message

        # sets the request status code
        request.status_code = status_code

        # sets the request status message
        request.status_message = status_message

        # writes the (received) data to the request
        request.write(data)

        # TENHO TB DE ESCREVER OS HEADERS CERTOS

        # closes the http client
        http_client.close({})
