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

import ssl
import struct
import select
import socket
import binascii

try: import json
except: json = None

import handler

HOST = "gateway.push.apple.com"
""" The host of the apn service to be used when
in production mode """

PORT = 2195
""" The port of the apn service to be used when
in sandbox mode """

SANDBOX_HOST = "gateway.sandbox.push.apple.com"
""" The host of the apn service to be used when
in sandbox mode """

SANDBOX_PORT = 2195
""" The port of the apn service to be used when
in sandbox mode """

KEY_FILE = "apn_key.pem"
""" The path to the (private) key file to be used
in the encrypted communication with the server """

CERT_FILE = "apn_cert.pem"
""" The path to the certificate file to be used
in the encrypted communication with the server """

MESSAGE_TEMPLATE = "{\"aps\":{\"alert\":\"%s\",\"sound\":\"%s\",\"badge\":%d}}"
""" The template to be used to create the message
in case the json plugin is currently not available """

class ApnHandler(handler.Handler):
    """
    The communication handler to be used for communications
    with the apple push notifications (apn) service.

    The communication with the service is done in a connection
    per message basis (expensive operation).

    @see: http://en.wikipedia.org/wiki/Apple_Push_Notification_Service
    """

    sockets = {}
    """ The map containing an association between a tuple of key
    and certificate file paths and a socket for the connection """

    token_string = None
    """ The string containing the token identifying the end device
    to be used for the communication, this should be an hexadecimal
    string (as described in specification) """

    key_file = None
    """ The path to the (private) key file to be used for the connection
    to be established for the apn service """

    cert_file = None
    """ The path to the certificate file to be used for the connection
    to be established for the apn service """

    sandbox = None
    """ Flag that controls if the sandbox infra-structure should
    be used instead of the production one (active by default) """

    wait = None
    """ Flag that controls if the current handler should wait
    for an answer from the server before disconnecting """

    def __init__(self, token_string, key_file = None, cert_file = None, sandbox = True, wait = False):
        handler.Handler.__init__(self)

        self.token_string = token_string
        self.key_file = key_file or KEY_FILE
        self.cert_file = cert_file or CERT_FILE
        self.sandbox = sandbox
        self.wait = wait

        # converts the current token (in hexadecimal) to a
        # string of binary data for the message
        self.token = binascii.unhexlify(token_string)

        # adds the plain filter to the current handler so that
        # plain text values are displayed
        self.add_filter(self.plain_filter)

    def _get_socket(self, key_file, cert_file):
        # creates the "identification" tuple containing both the
        # key file and the certificate file then tries to retrieve
        # the socket from the sockets map for the tuple and in case
        # the retrieval is verified returns it
        key_tuple = (key_file, cert_file)
        _socket = ApnHandler.sockets.get(key_tuple, None)
        if _socket: return _socket

        # creates the socket that will be used for the
        # communication with the remote host and
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket = ssl.wrap_socket(
            _socket,
            keyfile = self.key_file,
            certfile = self.cert_file,
            server_side = False
        )

        # creates the address using the sandbox flag as reference
        # and the uses it to connect to the remote host
        address = self.sandbox and (SANDBOX_HOST, SANDBOX_PORT) or (HOST, PORT)
        _socket.connect(address)

        # stores the socket in the socket (cache) map to be used
        # in further request and then returns the socket
        ApnHandler.sockets[key_tuple] = _socket
        return _socket

    def handle(self, message):
        # filters the message, converting it into the final
        # state (ready to be processed)
        message = self.filter(message)

        # retrieves the socket for the required key and cert files
        # (this should be able to used cached connections)
        _socket = self._get_socket(KEY_FILE, CERT_FILE)

        # creates the message structure using with the
        # message (string) as the alert and then converts
        # it into a json format (payload)
        message_s = {
           "aps" : {
                "alert" : message,
                "sound" : "default",
                "badge" : 0
            }
        }
        payload = json.dumps(message_s)
        if not json: payload = MESSAGE_TEMPLATE % (message.replace("\"", "\\\""), "default", 0).encode("utf-8")

        # sets the command with the zero value (simplified)
        # then calculates the token and payload lengths
        command = 0
        token_length = len(self.token)
        payload_length = len(payload)

        # creates the initial template for message creation by
        # using the token and the payload length for it, then
        # applies the various components of the message and packs
        # them according to the generated template
        template = "!BH%dsH%ds" % (token_length, payload_length)
        message = struct.pack(template, command, token_length, self.token, payload_length, payload)
        _socket.send(message)

        # sets the current socket in non blocking mode and then
        # runs the select operation in it to check if there's read
        # data available for reading
        _socket.setblocking(0)
        ready = self.wait and select.select([_socket], [], [], 3.0) or ((), (), ())

        # in case there are socket with read data available
        # must read it in the proper way, otherwise sets the
        # data string with an empty value
        if ready[0]: data = _socket.recv(4096)
        else: data = ""

        # in case there is data received from the server there
        # must be a problem in the communication, must raise an
        # exception indicating the problem
        if data: raise RuntimeError("Problem handling apn communication: '%s'" % data)
