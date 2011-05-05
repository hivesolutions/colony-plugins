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

    def __init__(self, distribution_registry_plugin):
        """
        Constructor of the class.

        @type distribution_registry_plugin: DistributionRegistryPlugin
        @param distribution_registry_plugin: The distribution registry plugin.
        """

        self.distribution_registry_plugin = distribution_registry_plugin

        self.registry_entries = []
        self.name_registry_entries_map = {}

    def load_registry(self, properties):
        """
        Loads the registry with the given properties.

        @type properties: List
        @param properties: The list of properties for the load of the registry.
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
        @param endpoints: The metadata map.
        """

        # creates a new registry entry
        registry_entry = RegistryEntry()

        # sets the registry entry hostname
        registry_entry.hostname = hostname

        # sets the registry entry name
        registry_entry.name = name

        # sets the registry entry type
        registry_entry.type = type

        # sets the registry entry endpoints
        registry_entry.endpoints = endpoints

        # sets the registry entry metadata
        registry_entry.metadata = metadata

        # adds the registry entry to the list of registry entries
        self.add_registry_entry(registry_entry)

    def unregister_entry(self, hostname, name):
        """
        Unregisters an entry from the registry.

        @type hostname: String
        @param hostname: The hostname.
        @type name: String
        @param param: The name.
        """

        # creates the registry entry id tuple
        registry_entry_id = (
            hostname,
            name
        )

        if not registry_entry_id in self.name_registry_entries_map:
            return

        # retrieves the registry entry
        registry_entry = self.name_registry_entries_map[registry_entry_id]

        del self.name_registry_entries_map[registry_entry_id]

        if registry_entry in self.registry_entries:
            self.registry_entries.remove(registry_entry)

    def get_all_registry_entries(self):
        """
        Retrieves all the available registry entries.

        @rtype: List
        @return: All the available registry entries.
        """

        return self.registry_entries

    def add_registry_entry(self, registry_entry):
        # retrieves the registry entry hostname
        registy_entry_hostname = registry_entry.hostname

        # retrieves the registry entry name
        registy_entry_name = registry_entry.name

        # creates the registry entry id tuple
        registry_entry_id = (
            registy_entry_hostname,
            registy_entry_name
        )

        self.registry_entries.append(registry_entry)
        self.name_registry_entries_map[registry_entry_id] = registry_entry

class RegistryEntry:
    """
    The registry entry class.
    User to represent an entry in the distribution registry.
    """

    hostname = "none"
    """ The hostname """

    name = "none"
    """ The name """

    type = "none"
    """ The type """

    endpoints = []
    """ The list of endpoints """

    metadata = {}
    """ The metadata map """

    def __init__(self, hostname = "none", name = "none", type = "none"):
        self.hostname = hostname
        self.name = name
        self.type = type
        self.endpoints = []
        self.metadata = {}
