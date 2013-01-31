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
import types
import select

import colony.base.system

UPGRADER_NAME = "ssl"
""" The upgrader name """

KEY_FILE_PATH = "key_file_path"
""" The key file path value """

CERTIFICATE_FILE_PATH = "certificate_file_path"
""" The certificate file path value """

SERVER_SIDE_VALUE = "server_side"
""" The server side value """

SSL_VERSION_VALUE = "ssl_version"
""" The ssl version value """

DO_HANDSHAKE_ON_CONNECT_VALUE = "do_handshake_on_connect"
""" The do handshake on connect value """

SSL_ERROR_WANT_READ = 2
""" The ssl error want read value """

SSL_VERSIONS = {
    "ssl2" : ssl.PROTOCOL_SSLv2 if hasattr(ssl, "PROTOCOL_SSLv2") else -1,
    "ssl3" : ssl.PROTOCOL_SSLv3 if hasattr(ssl, "PROTOCOL_SSLv3") else -1,
    "ssl23" : ssl.PROTOCOL_SSLv23 if hasattr(ssl, "PROTOCOL_SSLv23") else -1,
    "tls1" : ssl.PROTOCOL_TLSv1 if hasattr(ssl, "PROTOCOL_TLSv1") else -1
}
""" The map associating the string based description
values for the various ssl protocols with the corresponding
constants in the ssl infra-structure """

class SslSocketUpgrader(colony.base.system.System):
    """
    The ssl socket upgrader class.
    """

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
        self.plugin.debug("Upgrading a socket to ssl")

        # retrieves the plugin manager
        manager = self.plugin.manager

        # retrieves the plugin base path and uses it to retrieve the plugin
        # resources path (relative to the plugin path)
        plugin_path = manager.get_plugin_path_by_id(self.plugin.id)
        plugin_resources_path = plugin_path + "/main_service_ssl_socket_provider/ssl_socket_provider/resources"

        # retrieves the dummy ssl key and certificate paths
        # so that they can be used as the default values
        dummy_ssl_key_path = plugin_resources_path + "/dummy.key"
        dummy_ssl_certificate_path = plugin_resources_path + "/dummy.crt"

        # tries to retrieve the key and certificate file paths,
        # falling back to the dummy certificate values
        key_file_path = parameters.get(KEY_FILE_PATH, dummy_ssl_key_path)
        certificate_file_path = parameters.get(CERTIFICATE_FILE_PATH, dummy_ssl_certificate_path)

        # resolves both file paths using the plugin manager, in case
        # their refers logical references their are converted into absolute paths
        key_file_path = manager.resolve_file_path(key_file_path)
        certificate_file_path = manager.resolve_file_path(certificate_file_path)

        # tries to retrieve the server side value
        server_side = parameters.get(SERVER_SIDE_VALUE, False)

        # tries to retrieve the do handshake on connect value
        do_handshake_on_connect = parameters.get(DO_HANDSHAKE_ON_CONNECT_VALUE, True)

        # tries to retrieve the server side value, that will
        # control the accepted versions of the protocol
        ssl_version = parameters.get(SSL_VERSION_VALUE, None)
        ssl_version = SSL_VERSIONS.get(ssl_version, ssl.PROTOCOL_SSLv23)

        # warps the socket into an ssl socket
        ssl_socket = self._wrap_socket(
            socket,
            key_file_path,
            certificate_file_path,
            server_side,
            ssl_version = ssl_version,
            do_handshake_on_connect = do_handshake_on_connect
        )

        # returns the ssl socket
        return ssl_socket

    def _wrap_socket(self, base_socket, key_file_path, certificate_file_path, server_side = False, ssl_version = ssl.PROTOCOL_SSLv23, do_handshake_on_connect = True):
        """
        Wraps the base socket into an ssl socket using the given
        key file, certificate file and attributes.

        Note that the version of the ssl implementation may be
        controlled and in some cases it's required to be controlled
        for security purposes.

        @type base_socket: Socket
        @param base_socket: The base socket to be used for wrapping.
        @type key_file_path: String
        @param key_file_path: The path to the key file.
        @type certificate_file_path: String
        @param certificate_file_path: The path to the certificate file.
        @type server_side: bool
        @param server_side: If the socket should be created for a server.
        @type ssl_version: int
        @param ssl_version: The version  of the ssl protocol stack that
        is allowed to be executed for the socket to wrapped.
        @type do_handshake_on_connect: bool
        @param do_handshake_on_connect: If a handshake should be done on connect.
        @rtype: Socket
        @return: The wrapped (ssl) socket.
        """

        # warps the base socket into an ssl socket
        ssl_socket = ssl.wrap_socket(
            base_socket,
            key_file_path,
            certificate_file_path,
            server_side,
            ssl_version = ssl_version,
            do_handshake_on_connect = False
        )

        # does the handshake (on connect)
        do_handshake_on_connect and self._do_handshake(ssl_socket)

        # wraps the ssl socket with new methods
        wrap_socket(ssl_socket)

        # returns the ssl socket
        return ssl_socket

    def _do_handshake(self, ssl_socket):
        """
        Does the handshake for the given ssl socket.
        This method of handshake is proof to non blocking sockets.

        @type ssl_socket: SslSocket
        @param ssl_socket: The ssl socket to be used in the handshake.
        """

        # iterates continuously
        while True:
            try:
                # does the ssl socket handshake
                ssl_socket.do_handshake()

                # breaks the loop
                break
            except ssl.SSLError, exception:
                # retrieves the exception value
                exception_value = exception[0]

                # in case it's an ssl want read exception
                if exception_value == ssl.SSL_ERROR_WANT_READ:
                    # select the ssl socket for read
                    select.select([ssl_socket], [], [])
                # in case it's an ssl want write exception
                elif exception_value == ssl.SSL_ERROR_WANT_WRITE:
                    # select the ssl socket for write
                    select.select([], [ssl_socket], [])
                # otherwise it must be a different kind of exception
                else:
                    # re-raises the exception
                    raise

def wrap_socket(ssl_socket):
    # creates the bound accept method for the ssl socket
    _accept = types.MethodType(accept, ssl_socket, ssl.SSLSocket)

    # creates the bound process exception method for the ssl socket
    _process_exception = types.MethodType(process_exception, ssl_socket, ssl.SSLSocket)

    # sets the old accept method in the ssl socket with
    # a different name
    ssl_socket._accept = ssl_socket.accept

    # sets the new accept bound method in the ssl socket
    ssl_socket.accept = _accept

    # sets the extra secure attribute, to indicate
    # that this socket is of type secure
    ssl_socket._secure = True

    # sets the new process exception bound method in the ssl socket
    ssl_socket.process_exception = _process_exception

def accept(self):
    # accepts the connection, retrieving
    # the return value
    return_value = self._accept()

    # unpacks the return value into
    # connection and address
    connection, _address = return_value

    # wraps the (ssl) connection with new methods
    wrap_socket(connection)

    # returns the return value
    return return_value

def process_exception(self, exception):
    # in case the exception is of type ssl error
    # and the error number is ssl error want read
    if exception.__class__ == ssl.SSLError and exception.errno == SSL_ERROR_WANT_READ:
        # return false (exception
        # must can be ignored)
        return True

    # return false (exception
    # must be processed)
    return False
