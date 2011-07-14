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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
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

import search_index_persistence_exceptions

SEARCH_PERSISTENCE_TYPE_VALUE = "search_persistence_type"
""" The persistence type value """

class SearchIndexPersistence:
    """
    The search index persistence class.
    """

    search_index_persistence_plugin = None
    """ The search index persistence plugin """

    search_index_persistence_adapter_plugins_map = {}
    """ The map of search index persistence adapter plugins """

    def __init__(self, search_index_persistence_plugin):
        """
        Constructor of the class.

        @type search_index_persistence_plugin: SearchIndexPersistencePlugin
        @param search_index_persistence_plugin: The search index persistence plugin.
        """

        self.search_index_persistence_plugin = search_index_persistence_plugin

        self.search_index_persistence_adapter_plugins_map = {}

    def persist_index(self, search_index, properties):
        """
        Stores a specified index to a storage location using a persistence adapter.

        @type search_index: SearchIndex
        @param search_index: The search index to persist.
        @type properties: Dictionary
        @param properties: The map to guide the persistence operation.
        """

        if SEARCH_PERSISTENCE_TYPE_VALUE not in properties:
                search_index_persistence_exceptions.MissingProperty(SEARCH_PERSISTENCE_TYPE_VALUE)

        search_index_persistence_adapter_type = properties[SEARCH_PERSISTENCE_TYPE_VALUE]

        # retrieves the index persistence adapter plugin to use in the persistence operation
        search_index_persistence_adapter_plugin = self.get_search_index_persistence_adapter_plugin(search_index_persistence_adapter_type)

        # uses the selected adapter to persist the index
        return search_index_persistence_adapter_plugin.persist_index(search_index, properties)

    def load_index(self, properties):
        """
        Loads an index using a persistence adapter from a storage location.

        @type properties: Dictionary
        @param properties: The map to guide the load operation.
        """

        if SEARCH_PERSISTENCE_TYPE_VALUE not in properties:
                search_index_persistence_exceptions.MissingProperty(SEARCH_PERSISTENCE_TYPE_VALUE)

        search_index_persistence_adapter_type = properties[SEARCH_PERSISTENCE_TYPE_VALUE]

        # retrieves the index persistence adapter plugin to use in the load operation
        search_index_persistence_adapter_plugin = self.get_search_index_persistence_adapter_plugin(search_index_persistence_adapter_type)

        # uses the selected adapter to load the index
        return search_index_persistence_adapter_plugin.load_index(properties)

    def get_search_index_persistence_adapter_types(self):
        """
        Returns a list with the types of all the loaded search index persistence adapter plugins.

        @rtype: list
        @return: List of search index persistence adapter types.
        """

        # gets the type of each search index persistence adapter plugin loaded into the Search Index Persistence
        search_index_persistence_adapter_types = self.search_index_persistence_adapter_plugins_map.keys()

        return search_index_persistence_adapter_types

    def get_search_index_persistence_adapter_plugin(self, search_index_persistence_adapter_type):
        """
        Retrieves the loaded search index persistence adapter plugin for the specified adapter type.

        @type search_index_persistence_adapter_type: String
        @param search_index_persistence_adapter_type: The index persistence adapter type of the plugin to retrieve.
        @rtype: SearchIndexPersistenceAdapterPlugin
        @return: The loaded plugin for the adapter type
        """

        # checks for invalid plugin type
        if not search_index_persistence_adapter_type in self.search_index_persistence_adapter_plugins_map:
            raise search_index_persistence_exceptions.MissingSearchIndexPersistenceAdapterPlugin(search_index_persistence_adapter_type)

        return self.search_index_persistence_adapter_plugins_map[search_index_persistence_adapter_type]

    def add_search_index_persistence_adapter_plugin(self, plugin):
        """
        Inserts the search index_persistence adapter plugin in the Search Index Persistence's internal structures.

        @type plugin: SearchIndexPersistenceAdapterPlugin
        @param plugin: The search index persistence adapter plugin to remove.
        """

        # retrieve the search index persistence adapter plugin type
        plugin_type = plugin.get_type()

        # update the search index persistence adapter plugins map with the new plugin
        self.search_index_persistence_adapter_plugins_map[plugin_type] = plugin

    def remove_search_index_persistence_adapter_plugin(self, plugin):
        """
        Removes the search index persistence adapter plugin from the Search Index Persistence's internal structures.

        @type plugin: SearchIndexPersistenceAdapterPlugin
        @param plugin: The search index_persistence adapter plugin to remove.
        """

        # retrieves the search index persistence adapter plugin type
        plugin_type = plugin.get_type()

        # checks for invalid plugin type
        if not plugin_type in self.search_index_persistence_adapter_plugins_map:
            raise search_index_persistence_exceptions.MissingSearchIndexPersistenceAdapterPlugin(plugin_type)

        # removes the plugin from the search index persistence adapter plugins map
        del self.search_index_persistence_adapter_plugins_map[plugin_type]
