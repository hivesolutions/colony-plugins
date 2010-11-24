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

PROVIDER_NAME = "datagram"
""" The provider name """

FAMILY_VALUE = "family"
""" The family value """

class MainServiceDatagramSocketProvider:
    """
    The main service datagram socket provider class.
    """

    main_service_datagram_socket_provider_plugin = None
    """ The main service datagram socket provider plugin """

    def __init__(self, main_service_datagram_socket_provider_plugin):
        """
        Constructor of the class.

        @type main_service_datagram_socket_provider_plugin: MainServiceDatagramSocketProviderPlugin
        @param main_service_datagram_socket_provider_plugin: The main service datagram socket provider plugin.
        """

        self.main_service_datagram_socket_provider_plugin = main_service_datagram_socket_provider_plugin

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

        # creates the datagram socket
        datagram_socket = self.provide_socket_parameters()

        # returns the datagram socket
        return datagram_socket

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
        self.main_service_ssl_socket_provider_plugin.debug("Providing a datagram socket")

        # tries to retrieve the socket family
        socket_family = parameters.get(FAMILY_VALUE, socket.AF_INET)

        # creates the datagram socket
        datagram_socket = socket.socket(socket_family, socket.SOCK_DGRAM)

        # returns the datagram socket
        return datagram_socket
