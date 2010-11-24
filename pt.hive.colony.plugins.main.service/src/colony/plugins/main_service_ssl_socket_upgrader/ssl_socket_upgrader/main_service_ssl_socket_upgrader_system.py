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

import ssl
import time
import types

UPGRADER_NAME = "ssl"
""" The upgrader name """

RESOURCES_PATH = "main_service_ssl_socket_upgrader/ssl_socket_upgrader/resources"
""" The resources path """

KEY_FILE_PATH = "key_file_path"
""" The key file path value """

CERTIFICATE_FILE_PATH = "certificate_file_path"
""" The certificate file path value """

SERVER_SIDE_VALUE = "server_side"
""" The server side value """

DO_HANDSHAKE_ON_CONNECT_VALUE = "do_handshake_on_connect"
""" The do handshake on connect value """

SSL_ERROR_WANT_READ = 2
""" The ssl error want read value """

ERROR_SLEEP_TIME = 0.25
""" The time to be used between error tries """

class MainServiceSslSocketUpgrader:
    """
    The main service ssl socket upgrader class.
    """

    main_service_ssl_socket_upgrader_plugin = None
    """ The main service ssl socket upgrader plugin """

    def __init__(self, main_service_ssl_socket_upgrader_plugin):
        """
        Constructor of the class.

        @type main_service_ssl_socket_upgrader_plugin: MainServiceSslSocketUpgraderPlugin
        @param main_service_ssl_socket_upgrader_plugin: The main service ssl socket upgrader plugin.
        """

        self.main_service_ssl_socket_upgrader_plugin = main_service_ssl_socket_upgrader_plugin

    def get_upgrader_name(self):
        """
        Retrieves the socket upgrader name.

        @rtype: String
        @return: The socket upgrader name.
        """

        return UPGRADER_NAME

    def upgrade_socket(self, socket):
        """
        Upgrades the given socket, configured with
        the default parameters.

        @type socket: Socket
        @param socket: The socket to be upgraded.
        @rtype: Socket
        @return: The upgraded socket.
        """

        # upgrades the socket to ssl socket
        ssl_socket = self.upgrade_socket_parameters(socket)

        # returns the ssl socket
        return ssl_socket

    def upgrade_socket_parameters(self, socket, parameters = {}):
        """
        Upgrades the given socket, configured with
        the given parameters.

        @type socket: Socket
        @param socket: The socket to be upgraded.
        @type parameters: Dictionary
        @param parameters: The parameters for socket configuration.
        @rtype: Socket
        @return: The upgraded socket.
        """

        # prints a debug message
        self.main_service_ssl_socket_upgrader_plugin.debug("Upgrading a socket to ssl")

        # retrieves the plugin manager
        manager = self.main_service_ssl_socket_upgrader_plugin.manager

        # retrieves the main service ssl socket provicer plugin base path
        main_service_ssl_socket_provicer_plugin_path = manager.get_plugin_path_by_id(self.main_service_ssl_socket_upgrader_plugin.id)

        # sets the main service ssl socket provicer plugin resources path
        main_service_ssl_socket_provicer_plugin_resources_path = main_service_ssl_socket_provicer_plugin_path + "/main_service_ssl_socket_upgrader/ssl_socket_upgrader/resources"

        # retrieves the dummy ssl key path
        dummy_ssl_key_path = main_service_ssl_socket_provicer_plugin_resources_path + "/dummy.key"

        # retrieves the dummy ssl certificate path
        dummy_ssl_certificate_path = main_service_ssl_socket_provicer_plugin_resources_path + "/dummy.crt"

        # tries to retrieve the key file path
        key_file_path = parameters.get(KEY_FILE_PATH, dummy_ssl_key_path)

        # tries to retrieve the certificate file path
        certificate_file_path = parameters.get(CERTIFICATE_FILE_PATH, dummy_ssl_certificate_path)

        # tries to retrieve the server side value
        server_side = parameters.get(SERVER_SIDE_VALUE, False)

        # tries to retrieve the do handshake on connect value
        do_handshake_on_connect = parameters.get(DO_HANDSHAKE_ON_CONNECT_VALUE, True)

        # warps the socket into an ssl socket
        ssl_socket = self._wrap_socket(socket, key_file_path, certificate_file_path, server_side, do_handshake_on_connect = do_handshake_on_connect)

        # returns the ssl socket
        return ssl_socket

    def _wrap_socket(self, base_socket, key_file_path, certificate_file_path, server_side = False, do_handshake_on_connect = True):
        """
        Wraps the base socket into an ssl socket using the given
        key file, certificate file and attributes.

        @type base_socket: Socket
        @param base_socket: The base socket to be used for wrapping.
        @type key_file_path: String
        @param key_file_path: The path to the key file.
        @type certificate_file_path: String
        @param certificate_file_path: The path to the certificate file.
        @type server_side: bool
        @param server_side: If the socket should be created for a server.
        @type do_handshake_on_connect: bool
        @param do_handshake_on_connect: If a handshake should be done on connect.
        @rtype: Socket
        @return: The wrapped (ssl) socket.
        """

        # warps the base socket into an ssl socket
        ssl_socket = ssl.wrap_socket(base_socket, key_file_path, certificate_file_path, server_side, do_handshake_on_connect = do_handshake_on_connect)

        # creates the bound receive method for the ssl socket
        _recv = types.MethodType(recv, ssl_socket, ssl.SSLSocket)

        # sets the old receive method in the ssl socket with
        # a different name
        ssl_socket._recv = ssl_socket.recv

        # sets the new receive bound method in the ssl socket
        ssl_socket.recv = _recv

        # returns the ssl socket
        return ssl_socket

def recv(self, buffer_size, flags = 0):
    """
    Receives data from the current ssl socket.
    This method provides a way to avoid current
    runtime problems occurring in ssl sockets.

    @type buffer_size: int
    @param buffer_size: The size of the buffer to be used.
    @type flags: int
    @param flags: The flag to be used.
    @rtype: String
    @return: The received message.
    """

    # iterates continuously
    while True:
        try:
            # receives from the socket, retrieving
            # the return value
            return_value = self._recv(buffer_size, flags)

            # returns the return value
            return return_value
        except ssl.SSLError, exception:
            # in case the error is a want read
            if exception.errno == SSL_ERROR_WANT_READ:
                # sleeps for the error sleep time
                time.sleep(ERROR_SLEEP_TIME)

                # continues the loop
                continue

            # re-raises the exception
            raise
