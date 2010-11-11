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

import re
import struct
import hashlib

import main_service_http_websocket_handler_exceptions

HANDLER_NAME = "websocket"
""" The handler name """

HOST_VALUE = "Host"
""" The host value """

ORIGIN_VALUE = "Origin"
""" The origin value """

WEB_SOCKET_VALUE = "WebSocket"
""" The web socket value """

UPGRADE_VALUE = "Upgrade"
""" The upgrade value """

SEC_WEB_SOCKET_ORIGIN_VALUE = "Sec-WebSocket-Origin"
""" The sec web socket origin value """

SEC_WEB_SOCKET_LOCATION_VALUE = "Sec-WebSocket-Location"
""" The sec web socket location value """

SEC_WEB_SOCKET_PROTOCOL_VALUE = "Sec-WebSocket-Protocol"
""" The sec web socket protocol value """

SEC_WEB_SOCKET_KEY_1 = "Sec-WebSocket-Key1"
""" The sec web socket key 1 """

SEC_WEB_SOCKET_KEY_2 = "Sec-WebSocket-Key2"
""" The sec web socket key 2 """

DEFAULT_WEB_SOCKET_PROTOCOL = "default"
""" The default web socket protocol """

DIGITS_REGEX_VALUE = "\d"
""" The digits regex value """

SPACE_REGEX_VALUE = "\s"
""" The space regex value """

DIGITS_REGEX = re.compile(DIGITS_REGEX_VALUE)
""" The digits regex """

SPACE_REGEX = re.compile(SPACE_REGEX_VALUE)
""" The spaces regex """

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

        # retrieves the websocket headers
        host = self.request.get_header(HOST_VALUE)
        origin = self.request.get_header(ORIGIN_VALUE)
        protocol = self.request.get_header(SEC_WEB_SOCKET_PROTOCOL_VALUE)
        sec_websocket_key_1 = self.request.get_header(SEC_WEB_SOCKET_KEY_1)
        sec_websocket_key_2 = self.request.get_header(SEC_WEB_SOCKET_KEY_2)

        # retrieve the message
        message = self.request.read()

        # retrieves the base path
        base_path = self.request.base_path

        # in case the host, origin or base path is not available
        if not host or not origin or not base_path:
            # raises the invalid handshake data exception
            raise main_service_http_websocket_handler_exceptions.InvalidHandshakeData("not enough handshake data available")

        # in case the protocols is not available
        if not protocol:
            # sets the protocol as the default one
            protocol = DEFAULT_WEB_SOCKET_PROTOCOL

        # calculates the number results for both the websocket keys
        number_result_1 = self._calculate_number_value(sec_websocket_key_1)
        number_result_2 = self._calculate_number_value(sec_websocket_key_2)

        # creates the response result from the number result 1, number
        # result 2 and the (8 byte) message
        result = struct.pack("!II8s", number_result_1, number_result_2, message)

        # creates the md5 hash value
        md5_hash = hashlib.md5()

        # update the md5 hash value
        md5_hash.update(result)

        # retrieves the md5 digest
        md5_digest = md5_hash.digest()

        # sets the upgrade mode in the request
        self.request.set_upgrade_mode(WEB_SOCKET_VALUE)

        # sets the connection mode in the request
        self.request.set_connection_mode(UPGRADE_VALUE)

        # unsets the contains message flag to avoid
        # unnecessary header values
        self.request.set_contains_message(False)

        # sets the headers in the request
        self.request.set_header(SEC_WEB_SOCKET_ORIGIN_VALUE, origin)
        self.request.set_header(SEC_WEB_SOCKET_LOCATION_VALUE, "ws://%s%s" % (host, base_path))
        self.request.set_header(SEC_WEB_SOCKET_PROTOCOL_VALUE, protocol)

        # sets the request status code
        self.request.status_code = 101
        self.request.status_message = "Web Socket Protocol Handshake"

        # writes the result value
        self.request.write(md5_digest)

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

    def websocket_request_handler(self, service_connection):
        # retrieves the data
        data = service_connection.retrieve_data()

        # prints the data
        print(data)

        service_connection.send(data)

        # returns true (connection remains open)
        return True

    def _calculate_number_value(self, number_string):
        # retrieves the number (integer) value
        number = int("".join((DIGITS_REGEX.findall(number_string))))

        # retrieves the space length
        space_length = len(SPACE_REGEX.findall(number_string))

        # calculates the number result by dividing the
        # number for the space length
        number_result = number / space_length

        # returns the number result
        return number_result
