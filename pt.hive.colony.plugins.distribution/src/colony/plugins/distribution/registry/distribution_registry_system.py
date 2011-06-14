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

import colony.libs.map_util
import colony.libs.list_util

STATUS_VALUE = "status"
""" The status value """

UNKNOWN_VALUE = "unknown"
""" The unknown value """

class DistributionRegistry:
    """
    The distribution registry class.
    """

    distribution_registry_plugin = None
    """ The distribution registry plugin """

    registry_entries = []
    """ The list of registry entries """

    entry_id_registry_entries_map = []
    """ The map relating the entry id and the registry entry """

    type_registry_entries_map = []
    """ The map relating the type and the registry entry """

    def __init__(self, distribution_registry_plugin):
        """
        Constructor of the class.

        @type distribution_registry_plugin: DistributionRegistryPlugin
        @param distribution_registry_plugin: The distribution registry plugin.
        """

        self.distribution_registry_plugin = distribution_registry_plugin

        self.registry_entries = []
        self.entry_id_registry_entries_map = {}
        self.type_registry_entries_map = {}

    def load_registry(self, properties):
        """
        Loads the registry with the given properties.

        @type properties: List
        @param properties: The list of properties for the load of the registry.
        """

        pass

    def unload_registry(self, properties):
        """
        Unloads the registry with the given properties.

        @type properties: List
        @param properties: The list of properties for the unload of the registry.
        """

        pass

    def register_entry(self, hostname, name, type, endpoints, metadata):
        """
        Registers an entry in the registry.

        @type hostname: String
        @param hostname: The hostname.
        @type name: String
        @param param: The name.
        @type type: String
        @param type: The type.
        @type endpoints: List
        @param endpoints: The list of endpoints.
        @type metadata: Dictionary
        @param metadata: The metadata map.
        """

        # creates the registry entry id tuple
        registry_entry_id = (hostname, name)

        # in case the registry entry already exists in the registry
        if registry_entry_id in self.entry_id_registry_entries_map:
            # "only" updates the existent entry
            self._update_entry(hostname, name, type, endpoints, metadata)
        # otherwise the entry does not exists
        else:
            # registers the entry in the registry
            self._register_entry(hostname, name, type, endpoints, metadata)

    def unregister_entry(self, hostname, name):
        """
        Unregisters an entry from the registry.

        @type hostname: String
        @param hostname: The hostname.
        @type name: String
        @param param: The name.
        """

        self._unregister_entry(hostname, name)

    def get_registry_entries_type(self, registy_entry_type):
        """
        Retrieves the list of registry entries for the
        given registry entry type.

        @type registy_entry_type: String
        @param registy_entry_type: Tyhe type of registry
        entries to be retrieved.
        @rtype: List
        @return: The list of registry entries for the
        given registry entry type.
        """

        # retrieves the list of registry entries for the type
        type_registry_entries_list = self.type_registry_entries_map.get(registy_entry_type, [])

        # returns the list of registry entries for the type
        return type_registry_entries_list

    def get_all_registry_entries(self):
        """
        Retrieves all the available registry entries.

        @rtype: List
        @return: All the available registry entries.
        """

        return self.registry_entries

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        @rtype: Dictionary
        @return: The system information map.
        """

        # creates the distribution registry information map
        distribution_registry_information = {}

        # iterates over all the registry entries to construct
        # the distribution registry information map
        for registry_entry in self.registry_entries:
            distribution_registry_information[registry_entry.name] = (
                registry_entry.hostname,
                registry_entry.endpoints or None,
                registry_entry.metadata.get(STATUS_VALUE, UNKNOWN_VALUE)
            )

        # defines the distribution registry item columns
        distribution_registry_item_columns = [
            {
                "type" : "name",
                "value" : "Name"
            },
            {
                "type" : "value",
                "value" : "Hostname"
            },
            {
                "type" : "value",
                "value" : "Endpoints"
            },
            {
                "type" : "value",
                "value" : "Status"
            }
        ]

        # creates the distribution registry item
        distribution_registry_item = {}

        # sets the distribution registry item values
        distribution_registry_item["type"] = "map"
        distribution_registry_item["columns"] = distribution_registry_item_columns
        distribution_registry_item["values"] = distribution_registry_information

        # creates the system information (item)
        system_information = {}

        # sets the system information (item) values
        system_information["name"] = "Distribution Registry"
        system_information["items"] = [
            distribution_registry_item
        ]

        # returns the system information
        return system_information

    def add_registry_entry(self, registry_entry):
        # retrieves the registry entry hostname
        registy_entry_hostname = registry_entry.hostname

        # retrieves the registry entry name and type
        registy_entry_name = registry_entry.name
        registy_entry_type = registry_entry.type

        # creates the registry entry id tuple
        registry_entry_id = (registy_entry_hostname, registy_entry_name)

        # adds the registry entry to the entry id registry entries map
        # and to the registry entries list
        self.entry_id_registry_entries_map[registry_entry_id] = registry_entry
        self.registry_entries.append(registry_entry)

        # adds the registry entry to the type registry entries
        # list for the given registry entry type
        type_registry_entries_list = self.type_registry_entries_map.get(registy_entry_type, [])
        type_registry_entries_list.append(registry_entry)
        self.type_registry_entries_map[registy_entry_type] = type_registry_entries_list

    def _register_entry(self, hostname, name, type, endpoints, metadata):
        # creates a new registry entry
        registry_entry = RegistryEntry(hostname, name, type)

        # sets the registry entry endpoints
        registry_entry.endpoints = endpoints

        # sets the registry entry metadata
        registry_entry.metadata = metadata

        # adds the registry entry to the list of registry entries
        self.add_registry_entry(registry_entry)

    def _unregister_entry(self, hostname, name):
        # creates the registry entry id tuple
        registry_entry_id = (hostname, name)

        # retrieves the registry entry
        registry_entry = self.entry_id_registry_entries_map.get(registry_entry_id, None)

        # in case the register entry is not found
        if not registry_entry:
            # returns immediately
            return

        # retrieves the registry entry type
        registy_entry_type = registry_entry.type

        # removes the register entry from the entry id registry entries map
        del self.entry_id_registry_entries_map[registry_entry_id]

        # removes the registry entry from the registry entries list
        self.registry_entries.remove(registry_entry)

        # removes the registry entry from the type registry entries
        # list for the given registry entry type
        type_registry_entries_list = self.type_registry_entries_map.get(registy_entry_type, [])
        type_registry_entries_list.remove(registry_entry)

    def _update_entry(self, hostname, name, type, endpoints, metadata):
        # creates the registry entry id tuple
        registry_entry_id = (hostname, name)

        # tries to retrieve the registry entry
        register_entry = self.entry_id_registry_entries_map.get(registry_entry_id, None)

        # in case the registry entry is not defined
        if not register_entry:
            # returns immediately
            return

        # updates the registry entry attributes
        register_entry.hostname = hostname
        register_entry.name = name
        register_entry.type = type

        # updates the registry entry structure attributes
        colony.libs.list_util.list_extend(register_entry.endpoints, endpoints, copy_base_list = True)
        colony.libs.map_util.map_extend(register_entry.metadata, metadata, copy_base_map = False)

class RegistryEntry:
    """
    The registry entry class.
    User to represent an entry in the distribution registry.
    """

    hostname = None
    """ The hostname that represents the entry """

    name = None
    """ The name that describes the entry """

    type = None
    """ The type of entry """

    endpoints = []
    """ The list of endpoints  for the entry """

    metadata = {}
    """ The metadata map for custom references """

    def __init__(self, hostname, name, type):
        """
        Constructor of the class.

        @type hostname: String
        @param hostname: The hostname.
        @type name: String
        @param name: The name.
        @type type: String
        @param type: The type.
        """

        self.hostname = hostname
        self.name = name
        self.type = type

        self.endpoints = []
        self.metadata = {}
