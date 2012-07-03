#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import errno
import types
import socket

import colony.base.plugin_system_exceptions

PROVIDER_NAME = "ssl"
""" The provider name """

FAMILY_VALUE = "family"
""" The family value """

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

WSAEWOULDBLOCK = 10035
""" The wsa would block error code """

class MainServiceSslSocketProvider:
    """
    The main service ssl socket provider class.
    """

    main_service_ssl_socket_provider_plugin = None
    """ The main service ssl socket provider plugin """

    def __init__(self, main_service_ssl_socket_provider_plugin):
        """
        Constructor of the class.

        @type main_service_ssl_socket_provider_plugin: MainServiceSslSocketProviderPlugin
        @param main_service_ssl_socket_provider_plugin: The main service ssl socket provider plugin.
        """

        self.main_service_ssl_socket_provider_plugin = main_service_ssl_socket_provider_plugin

    def get_provider_name(self):
        """
        Retrieves the socket provider name.

        @rtype: String
        @return: The socket provider name.
        """

        return PROVIDER_NAME

    def provide_socket(self):
        """
        Provides a new socket, configured with
        the default parameters.

        @rtype: Socket
        @return: The provided socket.
        """

        # creates the ssl socket
        ssl_socket = self.provide_socket_parameters()

        # returns the ssl socket
        return ssl_socket

    def provide_socket_parameters(self, parameters = {}):
        """
        Provides a new socket, configured with
        the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for socket configuration.
        @rtype: Socket
        @return: The provided socket.
        """

        # prints a debug message
        self.main_service_ssl_socket_provider_plugin.debug("Providing an ssl socket")

        # retrieves the plugin manager
        manager = self.main_service_ssl_socket_provider_plugin.manager

        # retrieves the main service ssl socket provicer plugin base path
        main_service_ssl_socket_provicer_plugin_path = manager.get_plugin_path_by_id(self.main_service_ssl_socket_provider_plugin.id)

        # sets the main service ssl socket provicer plugin resources path
        main_service_ssl_socket_provicer_plugin_resources_path = main_service_ssl_socket_provicer_plugin_path + "/main_service_ssl_socket_provider/ssl_socket_provider/resources"

        # tries to retrieve the socket family
        socket_family = parameters.get(FAMILY_VALUE, socket.AF_INET)

        # creates the normal socket
        normal_socket = socket.socket(socket_family, socket.SOCK_STREAM)

        # retrieves the dummy ssl key and certificate paths
        # so that they can be used as the default values
        dummy_ssl_key_path = main_service_ssl_socket_provicer_plugin_resources_path + "/dummy.key"
        dummy_ssl_certificate_path = main_service_ssl_socket_provicer_plugin_resources_path + "/dummy.crt"

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
        do_handshake_on_connect = parameters.get(DO_HANDSHAKE_ON_CONNECT_VALUE, False)

        # warps the normal socket into an ssl socket
        ssl_socket = self._wrap_socket(normal_socket, key_file_path, certificate_file_path, server_side, do_handshake_on_connect = do_handshake_on_connect)

        # returns the ssl socket
        return ssl_socket

    def _wrap_socket(self, base_socket, key_file_path, certificate_file_path, server_side = False, do_handshake_on_connect = False):
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

        # wraps the ssl socket with new methods
        wrap_socket(ssl_socket)

        # returns the ssl socket
        return ssl_socket

def wrap_socket(ssl_socket):
    # creates the bound accept and handshake methods for
    # the ssl socket
    _accept = types.MethodType(accept, ssl_socket, ssl.SSLSocket)
    _handshake = types.MethodType(handshake, ssl_socket, ssl.SSLSocket)
    _set_option = types.MethodType(set_option, ssl_socket, ssl.SSLSocket)

    # creates the bound process exception method for the ssl socket
    _process_exception = types.MethodType(process_exception, ssl_socket, ssl.SSLSocket)

    # sets the old accept method in the ssl socket with
    # a different name
    ssl_socket._accept = ssl_socket.accept

    # sets the new accept and handshake bound methods in
    # the ssl socket
    ssl_socket.accept = _accept
    ssl_socket.handshake = _handshake
    ssl_socket.set_option = _set_option

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
    connection, address = return_value

    try:
        # wraps the (ssl) connection with new methods
        wrap_socket(connection)

        # sets the connection to non blocking mode in case
        # the blocking flag is not set in the current socket
        hasattr(self, "blocking") and not self.blocking and connection.setblocking(0)

        # tries to archive the proper handshake on the ssl
        # connection, asynchronous handshake
        connection.do_handshake()
    except socket.error, error:
        # in case the exception is normal, the operation did not
        # complete or the socket would block nothing should be done
        # and the handshake operation must be deferred to the next data
        # receiving "event"
        if error.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EPERM, errno.ENOENT, WSAEWOULDBLOCK):
            # creates the error and populates it with the connection and the address
            # then raises it to the upper levels
            error = colony.base.plugin_system_exceptions.OperationNotComplete("no handshake was possible")
            error.socket = connection
            error.connection = connection
            error.address = address
            raise error
        # otherwise it's a different kind of error and the connection
        # state is considered to be erroneous (must be closed)
        else:
            # closes the client connection (it's currently in an erroneous
            # state) and then re-raises the exception
            connection.close()
            raise
    except:
        # closes the client connection (it's currently in an erroneous
        # state) and then re-raises the exception
        connection.close()
        raise

    # returns the return value
    return return_value

def handshake(self):
    self.do_handshake()

def set_option(self, name, value):
    setattr(self, name, value)

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
