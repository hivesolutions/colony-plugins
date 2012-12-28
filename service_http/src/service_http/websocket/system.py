#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import struct
import hashlib

import colony.base.system

import exceptions

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

class ServiceHttpWebsocket(colony.base.system.System):
    """
    The service http webdav (handler) class.
    """

    websocket_handler_plugins_map = {}
    """ The websocket handler plugins map """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.websocket_handler_plugins_map = {}

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
        websocket_connection = WebSocketConnection(self, request)

        # opens the websocket connection
        websocket_connection.open()

        # prints a debug message
        self.plugin.debug("Handling Websocket connection: %s" % websocket_connection)

    def websocket_handler_load(self, websocket_handler_plugin):
        # retrieves the plugin handler name
        handler_name = websocket_handler_plugin.get_handler_name()

        self.websocket_handler_plugins_map[handler_name] = websocket_handler_plugin

    def websocket_handler_unload(self, websocket_handler_plugin):
        # retrieves the plugin handler name
        handler_name = websocket_handler_plugin.get_handler_name()

        del self.websocket_handler_plugins_map[handler_name]

class WebSocketConnection:
    """
    Web socket connection representing a websocket
    connection.
    """

    service_http_websocket_handler = None
    """ The service http websocket handler """

    request = None
    """ The http request object """

    service = None
    """ The service that was used to handle the
    request associated (owner service) """

    service_connection = None
    """ The service connection """

    location = None
    """ The location """

    protocol = None
    """ The protocol """

    def __init__(self, service_http_websocket_handler, request):
        """
        Constructor of the class.

        @type service_http_websocket_handler: ServiceHttpWebsocketHandler
        @param service_http_websocket_handler: The service http websocket handler.
        @type request: HttpRequest
        @param request: The http request associated with the
        opening of the websocket.
        """

        self.service_http_websocket_handler = service_http_websocket_handler
        self.request = request

        self.service = request.service
        self.service_connection = request.service_connection

    def __repr__(self):
        return "(%s, %s, %s)" % (self.location, self.protocol, self.service_connection)

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
            raise exceptions.InvalidHandshakeData("not enough handshake data available")

        # in case the protocols is not available
        if not protocol:
            # sets the protocol as the default one
            protocol = DEFAULT_WEB_SOCKET_PROTOCOL

        # creates the location value
        location = "ws://%s%s" % (host, base_path)

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
        self.request.set_header(SEC_WEB_SOCKET_LOCATION_VALUE, location)
        self.request.set_header(SEC_WEB_SOCKET_PROTOCOL_VALUE, protocol)

        # sets the request status code
        self.request.status_code = 101
        self.request.status_message = "Web Socket Protocol Handshake"

        # writes the result value
        self.request.write(md5_digest)

        # retrieves the service connection handler for the protocol
        service_connection_handler = self._get_service_connection_handler(protocol)

        # sets the request handler for the service
        # this step upgrades the protocol interpretation
        self.service.set_service_connection_request_handler(self.service_connection, service_connection_handler)

        # sets the websocket connection values
        self.protocol = protocol
        self.location = location

    def close(self):
        """
        Closes the websocket, cleaning the remaining changes.
        """

        # sets the request handler for the service as the original
        # (http) request handler, this step "downgrades" the protocol
        # interpretation (back to http)
        self.service.unset_service_connection_request_handler(self.service_connection)

    def websocket_service_connection_handler(self, service_connection):
        # receives the data
        data = service_connection.receive()

        # sends the data back
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

    def _get_service_connection_handler(self, protocol):
        # retrieves the websocket handler plugins map
        websocket_handler_plugins_map = self.service_http_websocket_handler.websocket_handler_plugins_map

        # in case the protocol is the default one
        if protocol == DEFAULT_WEB_SOCKET_PROTOCOL:
            # sets the service connection handler as the websocket
            # service connection handler method
            service_connection_handler = self.websocket_service_connection_handler
        else:
            # retrieves the websocket handler plugin
            websocket_handler_plugin = websocket_handler_plugins_map.get(protocol, None)

            # in case the websocket handler plugin is defined
            if not websocket_handler_plugin:
                # raises the websocket handler not found exception
                raise exceptions.WebsocketHandlerNotFoundException(protocol)

            # sets the service connection handler as the handle service connection
            # method of the websocket handler plugins
            service_connection_handler = websocket_handler_plugin.handle_service_connection

        # returns the service connection handler
        return service_connection_handler
