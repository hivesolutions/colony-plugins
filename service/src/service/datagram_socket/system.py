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

import socket

import colony.base.system
import colony.libs.host_util

PROVIDER_NAME = "datagram"
""" The provider name """

FAMILY_VALUE = "family"
""" The family value """

MULTICAST_ADDRESS_VALUE = "multicast_address"
""" The multicast address value """

MULTICAST_PARAMETERS_VALUE = "multicast_parameters"
""" The multicast parameters value """

SO_REUSEPORT_VALUE = "SO_REUSEPORT"
""" The so reuseport value """

TTL_VALUE = "ttl"
""" The ttl value """

DEFAULT_MULTICAST_TTL = 255
""" The default multicast ttl """

class DatagramSocket(colony.base.system.System):
    """
    The datagram socket (provider) class.
    """

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
        self.plugin.debug("Providing a datagram socket")

        # tries to retrieve the socket family
        socket_family = parameters.get(FAMILY_VALUE, socket.AF_INET)

        # tries to retrieve the multicast value
        multicast_address = parameters.get(MULTICAST_ADDRESS_VALUE, None)

        # tries to retrieve the multicast parameters
        multicast_parameters = parameters.get(MULTICAST_PARAMETERS_VALUE, {})

        # creates the datagram socket
        datagram_socket = socket.socket(socket_family, socket.SOCK_DGRAM)

        # wraps the socket for multicast
        multicast_address and self._wrap_socket_multicast(datagram_socket, multicast_address, multicast_parameters)

        # returns the datagram socket
        return datagram_socket

    def _wrap_socket_multicast(self, base_socket, multicast_address, multicast_parameters):
        """
        Wraps the given base socket in to a multicast supported layer.

        @type base_socket: Socket
        @param base_socket: The base socket to be wrapped.
        @type multicast_address: Tuple
        @param multicast_address: The multicast address to be used.
        @type multicast_parameters: Dictionary
        @param multicast_parameters: The parameters for multicast.
        """

        # unpacks the multicast address into host and port
        multicast_host, _multicast_port = multicast_address

        # retrieves the multicast parameters
        multicast_ttl = multicast_parameters.get(TTL_VALUE, DEFAULT_MULTICAST_TTL)

        # sets the socket for reuse
        base_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        hasattr(socket, SO_REUSEPORT_VALUE) and base_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #@UndefinedVariable

        # sets the datagram socket options
        base_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, multicast_ttl)
        base_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        # retrieves the addresses ip4
        address_ip4 = colony.libs.host_util.get_address_ip4_all()

        # converts the addresses to network mode
        address_ip4_network = socket.inet_aton(address_ip4)
        multicast_host_network = socket.inet_aton(multicast_host)

        # sets the membership for the multicasting paradigm
        base_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, address_ip4_network)
        base_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_host_network + address_ip4_network);
