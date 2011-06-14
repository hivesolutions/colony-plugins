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

ADAPTER_NAME = "local"
""" The adapter name """

COLONY_VALUE = "colony"
""" The colony value """

TCP_VALUE = "tcp"
""" The tcp value """

ADDRESS_IP4_VALUE = "address_ip4"
""" The address ip4 value value """

ADDRESS_IP6_VALUE = "address_ip6"
""" The address ip6 value value """

class DistributionLocalDiscovery:
    """
    The distribution local discovery class.
    """

    distribution_local_discovery_plugin = None
    """ The distribution local discovery plugin """

    def __init__(self, distribution_local_discovery_plugin):
        """
        Constructor of the class.

        @type distribution_local_discovery_plugin: DistributionLocalDiscoveryPlugin
        @param distribution_local_discovery_plugin: The distribution local discovery plugin.
        """

        self.distribution_local_discovery_plugin = distribution_local_discovery_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def handle_discover(self, arguments):
        """
        Handles a (distribution) discovery.

        @type arguments: Dictionary
        @param arguments: The arguments to the
        (distribution) discovery.
        """

        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_local_discovery_plugin.distribution_registry_plugin

        # retrieves the "local" host name
        hostname_local = colony.libs.host_util.get_hostname_local()

        # retrieves the "preferred" addresses
        address_ip4 = colony.libs.host_util.get_address_ip4_all()
        address_ip6 = colony.libs.host_util.get_address_ip6_all()

        # creates the list of endpoints
        endpoints = [(address_ip4, TCP_VALUE)]

        # creates the map that represents the metadata
        metadata = {
            ADDRESS_IP4_VALUE : address_ip4,
            ADDRESS_IP6_VALUE : address_ip6
        }

        # registers the "remote" entry in the distribution registry
        distribution_registry_plugin.register_entry(hostname_local, COLONY_VALUE + "@" + hostname_local, COLONY_VALUE, endpoints, metadata)
