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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.host_util

HANDLER_NAME = "_colony._tcp.local"
""" The handler name """

COLONY_SERVICE_ID = "_colony._tcp.local"
""" The colony service id """

A_TYPE = "A"
""" The a type """

PTR_TYPE = "PTR"
""" The ptr type """

IN_CLASS = "IN"
""" The in class """

DEFAULT_TTL = 10
""" The default ttl (time to live) """

class DistributionMdnsHandler:
    """
    The distribution mdns handler class.
    """

    distribution_mdns_handler_plugin = None
    """ The distribution mdns handler plugin """

    def __init__(self, distribution_mdns_handler_plugin):
        """
        Constructor of the class.

        @type distribution_mdns_handler_plugin: DistributionMdnsHandlerPlugin
        @param distribution_mdns_handler_plugin: The distribution mdns handler plugin.
        """

        self.distribution_mdns_handler_plugin = distribution_mdns_handler_plugin

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request, arguments):
        """
        Handles the given mdns request.

        @type request: MdnsRequest
        @param request: The mdns request to be handled.
        @type arguments: Dictionary
        @param arguments: The arguments to the mdns handling.
        """

        # checks if the request represents a response
        request_is_response = request.is_response()

        # in case the request is in fact a response
        if request_is_response:
            # returns immediately (no response)
            return

        # retrieves the "local" host name
        hostname_local = colony.libs.host_util.get_hostname_local()

        # retrieves the "preferred" addresses
        address_ip4 = colony.libs.host_util.get_address_ip4_all()

        # creates the record tuple
        record_tuple = (
            COLONY_SERVICE_ID,
            PTR_TYPE,
            IN_CLASS,
            DEFAULT_TTL,
            hostname_local
        )

        # creates the address ip4 tuple
        address_ip4_tuple = (
            hostname_local,
            A_TYPE,
            IN_CLASS,
            DEFAULT_TTL,
            address_ip4
        )

        # adds the record tuple
        request.answers.append(record_tuple)

        # adds the ip4 and ip6 address tuples
        request.additional_resource_records.append(address_ip4_tuple)
