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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

ADAPTER_NAME = "mdns"
""" The adapter name """

COLONY_SERVICE_ID = "_colony._tcp.local"
""" The colony service id """

A_TYPE = "A"
""" The a type """

TXT_TYPE = "TXT"
""" The txt type """

PTR_TYPE = "PTR"
""" The ptr type """

IN_CLASS = "IN"
""" The in class """

TCP_VALUE = "tcp"
""" The tcp value """

COLONY_VALUE = "colony"
""" The colony value """

ADDRESS_IP4_VALUE = "address_ip4"
""" The address ip4 value value """

CALLBACK_FUNCTION_VALUE = "callback_function"
""" The callback function value """

CALLBACK_TIMEOUT_VALUE = "callback_timeout"
""" The callback timeout value """

ANSWERS_VALUE = "answers"
""" The answers value """

ADDITIONAL_RESOURCE_RECORDS_VALUE = "additional_resource_records"
""" The additional resource records value """

DEFAULT_TIMEOUT_VALUE = -1
""" The default timeout value """

DEFAULT_TTL_VALUE = 10
""" The default ttl value """

DEFAULT_IP4_VALUE = "0.0.0.0"
""" The default ip4 value """

class DistributionMdnsAdvertising:
    """
    The distribution mdns advertising class.
    """

    distribution_mdns_advertising_plugin = None
    """ The distribution mdns advertising plugin """

    def __init__(self, distribution_mdns_advertising_plugin):
        """
        Constructor of the class.

        @type distribution_mdns_advertising_plugin: DistributionMdnsAdvertisingPlugin
        @param distribution_mdns_advertising_plugin: The distribution mdns advertising plugin.
        """

        self.distribution_mdns_advertising_plugin = distribution_mdns_advertising_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def handle_advertise(self, arguments):
        """
        Handles a (distribution) advertising.

        @type arguments: Dictionary
        @param arguments: The arguments to the
        (distribution) advertising.
        """

        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_mdns_advertising_plugin.distribution_registry_plugin

        # retrieves the main client mdns plugin
        main_client_mdns_plugin = self.distribution_mdns_advertising_plugin.main_client_mdns_plugin

        # retrieves the "current" list of registry entries for the colony type
        registry_entries_list = distribution_registry_plugin.get_registry_entries_type(COLONY_VALUE)

        # iterates over all the list of registry entries to "advertise"
        # the distribution information
        for registry_entry in registry_entries_list:
            # creates the main client mdns client
            mdns_client = main_client_mdns_plugin.create_client({})

            # opens the mdns client
            mdns_client.open({})

            try:
                # retrieves the registry entry attributes
                registry_entry_hostname = registry_entry.hostname
                registry_entry_metadata = registry_entry.metadata

                # retrieves the address attributes
                registry_entry_address_ip4 = registry_entry_metadata.get(ADDRESS_IP4_VALUE, DEFAULT_IP4_VALUE)

                # creates the metadata key value set in text format
                metadata_key_value_set_text = self._create_key_value_set_text(registry_entry_metadata)

                # creates the parameters for the queries resolution
                parameters = {
                    CALLBACK_FUNCTION_VALUE : self._advertising_callback,
                    CALLBACK_TIMEOUT_VALUE : DEFAULT_TIMEOUT_VALUE,
                    ANSWERS_VALUE : [
                        (COLONY_SERVICE_ID, PTR_TYPE, IN_CLASS, DEFAULT_TTL_VALUE, registry_entry_hostname)
                    ],
                    ADDITIONAL_RESOURCE_RECORDS_VALUE : [
                        (registry_entry_hostname, A_TYPE, IN_CLASS, DEFAULT_TTL_VALUE, registry_entry_address_ip4),
                        (registry_entry_hostname, TXT_TYPE, IN_CLASS, DEFAULT_TTL_VALUE, metadata_key_value_set_text)
                    ]
                }

                # resolves the queries
                mdns_client.resolve_queries([(COLONY_SERVICE_ID, PTR_TYPE, IN_CLASS)], parameters)
            finally:
                # closes the mdns client
                mdns_client.close({})

    def _create_key_value_set_text(self, key_value_map):
        # creates the list to hold the text values
        text_values = []

        # retrieves the key value map items
        key_value_map_items = key_value_map.items()

        # iterates over all the key value map items
        for key, value in key_value_map_items:
            # converts the value into a string
            value_string = str(value)

            # creates the key value string by appending
            # the key and the value string with a separator
            key_value_string = key + "=" + value_string

            # adds the key value string to the list
            # of text values
            text_values.append(key_value_string)

        # returns the (list) text values
        return text_values

    def _advertising_callback(self, query, response):
        pass
