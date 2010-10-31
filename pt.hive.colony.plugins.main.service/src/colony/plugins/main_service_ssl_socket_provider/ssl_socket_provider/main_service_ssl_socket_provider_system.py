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

import socket

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

RESOURCES_PATH = "main_service_ssl_socket_provider/ssl_socket_provider/resources"
""" The resources path """

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

        # warps the normal socket into an ssl socket
        ssl_socket = self._wrap_socket(normal_socket, key_file_path, certificate_file_path, server_side, do_handshake_on_connect = do_handshake_on_connect)

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

        try:
            import ssl
        except ImportError:
            return self._old_wrap_socket(base_socket, key_file_path, certificate_file_path, server_side, do_handshake_on_connect)

        # warps the base socket into an ssl socket
        ssl_socket = ssl.wrap_socket(base_socket, key_file_path, certificate_file_path, server_side, do_handshake_on_connect = do_handshake_on_connect)

        # returns the ssl socket
        return ssl_socket

    def _old_wrap_socket(self, base_socket, key_file_path, certificate_file_path, server_side = False, do_handshake_on_connect = True):
        """
        Wraps the base socket into an ssl socket using the given
        key file, certificate file and attributes.
        This method provides wrapping for the old ssl abstraction.

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

        # in case server side flag is set
        if server_side:
            # raises the system error
            raise SystemError("No ssl support available for server side")

        # warps the base socket into an ssl socket
        ssl_socket = socket.ssl(base_socket, key_file_path, certificate_file_path)

        # wrapps the ssl socket
        ssl_socket_wrapped = SslWrapper(base_socket, ssl_socket)

        # returns the ssl socket wrapped
        return ssl_socket_wrapped

class SslWrapper:
    """
    The ssl wrapper class, used to create
    wrapping object for the old ss implementation.
    """

    old_base_socket = None
    """" The old base socket """

    old_ssl_object = None
    """ The "old" ssl object to be used as base """

    def __init__(self, old_base_socket, old_ssl_object):
        """
        Constructor of the class.

        @type old_base_socket: Socket
        @param old_base_socket: The old base socket.
        @type old_ssl_object: SslObject
        @param old_ssl_object: The "old" ssl object to be
        used as base.
        """

        self.old_base_socket = old_base_socket
        self.old_ssl_object = old_ssl_object

        self._initialize_wrapping()

    def __getattr__(self, name):
        if hasattr(self.old_ssl_object, name):
            return getattr(self.old_ssl_object, name)

        if hasattr(self.old_base_socket, name):
            return getattr(self.old_base_socket, name)

    def sendall(self, data):
        """
        The send all method, that send all the
        data, avoiding the normal problem in output
        buffers.

        @type data: String
        @param data: The data to be sent.
        """

        # iterates while there is
        # data left to be send
        while(len(data) > 0):
            # sends the data string, retrieving the sent bytes
            bytes_sent = self.send(data)

            # sets the new data string
            data = data[bytes_sent:]

    def _initialize_wrapping(self):
        """
        Initializes the wrapping of the ssl object.
        """

        # sets the recv method as the read method
        # in the ssl object
        self.recv = self.old_ssl_object.read

        # sets the send method as the write method
        # in the ssl object
        self.send = self.old_ssl_object.write
