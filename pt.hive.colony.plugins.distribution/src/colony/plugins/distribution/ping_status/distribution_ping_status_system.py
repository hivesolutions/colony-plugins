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

ADAPTER_NAME = "ping"
""" The adapter name """

COLONY_VALUE = "colony"
""" The colony value """

class DistributionPingStatus:
    """
    The distribution ping status class.
    """

    distribution_ping_status_plugin = None
    """ The distribution ping status plugin """

    def __init__(self, distribution_ping_status_plugin):
        """
        Constructor of the class.

        @type distribution_ping_status_plugin: DistributionPingStatusPlugin
        @param distribution_ping_status_plugin: The distribution ping status plugin.
        """

        self.distribution_ping_status_plugin = distribution_ping_status_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def handle_status(self, arguments):
        """
        Handles a (distribution) status.

        @type arguments: Dictionary
        @param arguments: The arguments to the
        (distribution) status.
        """

        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_ping_status_plugin.distribution_registry_plugin

        # retrieves the main client http plugin
        main_client_http_plugin = self.distribution_ping_status_plugin.main_client_http_plugin

        # retrieves the "current" list of registry entries for the colony type
        registry_entries_list = distribution_registry_plugin.get_registry_entries_type(COLONY_VALUE)

#        # iterates over all the list of registry entries to "advertise"
#        # the distribution information
#        for registry_entry in registry_entries_list:
#            # creates the main client ping client
#            ping_client = main_client_ping_plugin.create_client({})
#
#            # opens the ping client
#            ping_client.open({})
#
#            try:
#                # retrieves the registry entry attributes
#                registry_entry_hostname = registry_entry.hostname
#                registry_entry_metadata = registry_entry.metadata
#
#                # retrieves the address attributes
#                registry_entry_address_ip4 = registry_entry_metadata.get(ADDRESS_IP4_VALUE, DEFAULT_IP4_VALUE)
#
#                # creates the parameters for the queries resolution
#                parameters = {
#                    CALLBACK_FUNCTION_VALUE : self._status_callback,
#                    CALLBACK_TIMEOUT_VALUE : DEFAULT_TIMEOUT_VALUE,
#                    ANSWERS_VALUE : [(COLONY_SERVICE_ID, PTR_TYPE, IN_CLASS, DEFAULT_TTL_VALUE, registry_entry_hostname)],
#                    ADDITIONAL_RESOURCE_RECORDS_VALUE : [(registry_entry_hostname, A_TYPE, IN_CLASS, DEFAULT_TTL_VALUE, registry_entry_address_ip4)]
#                }
#
#                # resolves the queries
#                ping_client.resolve_queries([(COLONY_SERVICE_ID, PTR_TYPE, IN_CLASS)], parameters)
#            finally:
#                # closes the ping client
#                ping_client.close({})
