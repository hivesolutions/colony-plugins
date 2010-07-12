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

import main_service_http_websocket_handler_exceptions

HANDLER_NAME = "websocket"
""" The handler name """

class MainServiceHttpWebsocketHandler:
    """
    The main service http webdav handler class.
    """

    main_service_http_websocket_handler_plugin = None
    """ The main service http websocket handler plugin """

    def __init__(self, main_service_http_websocket_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_websocket_handler_plugin: MainServiceHttpWebsocketHandlerPlugin
        @param main_service_http_websocket_handler_plugin: The main service http websocket handler plugin.
        """

        self.main_service_http_websocket_handler_plugin = main_service_http_websocket_handler_plugin

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

        # creates a new websocket connection
        websocket_connection = WebSocketConnection(request)

        # opens the websocket connection
        websocket_connection.open()

class WebSocketConnection:
    """
    Web socket connection representing a websocket
    connection.
    """

    request = None
    """ The http request object """

    http_client_service_handler = None
    """ The http client service handler """

    service_connection = None
    """ The service connection """

    def __init__(self, request):
        """
        Constructor of the class.

        @type request: HttpRequest
        @param request: The http request associated with the
        opening of the websocket.
        """

        self.request = request

        self.http_client_service_handler = request.http_client_service_handler
        self.service_connection = request.service_connection

    def open(self):
        """
        Opens the websocket by proceeding with the handshake.
        """

        # retrieves the host header
        host = self.request.get_header("Host")
        origin = self.request.get_header("Origin")
        base_path = self.request.base_path

        # in case the host, origin or base path is not available
        if not host or not origin or not base_path:
            # raises the invalid handshake data exception
            raise main_service_http_websocket_handler_exceptions.InvalidHandshakeData("not enough handshake data available")

        # sets the upgrade mode in the request
        self.request.set_upgrade_mode("WebSocket")

        # sets the connection mode in the request
        self.request.set_connection_mode("Upgrade")

        # unsets the contains message flag to avoid
        # unnecessary header values
        self.request.set_contains_message(False)

        # sets the headers in the request
        self.request.set_header("WebSocket-Origin", origin)
        self.request.set_header("WebSocket-Location", "ws://%s%s" % (host, base_path))

        # sets the request status code
        self.request.status_code = 101
        self.request.status_message = "Web Socket Protocol Handshake"

        # sets the request handler for the http client service handler
        # this step upgrades the protocol interpretation
        self.http_client_service_handler.set_service_connection_request_handler(self.service_connection, self.websocket_request_handler)

    def close(self):
        """
        Closes the websocket, cleaning the remaining changes.
        """

        # sets the request handler for the http client service handler
        # as the original (http) request handler, this step downgrades
        # the protocol interpretation (back to http)
        self.http_client_service_handler.unset_service_connection_request_handler(self.service_connection)

    def websocket_request_handler(self, service_connection, request_timeout):
        # retrieves the data
        data = service_connection.retrieve_data(request_timeout)

        # prints the data
        print(data)

        # returns true (connection remains open)
        return True
