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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
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

import search_processor_exceptions

SEARCH_PROCESSOR_TYPE_VALUE = "search_processor_type"
""" The key to retrieve the search processor type from the properties map """

SEARCH_PROCESSOR_OPTIONS_VALUE = "search_processor_options"
""" The key to retrieve the search processor options from the properties map """

class SearchProcessor:
    """
    The search processor class.
    """

    search_processor_plugin = None
    """ The search processor plugin """

    search_processor_adapter_plugins_map = {}
    """ The search processor adapter plugins map """

    def __init__(self, search_processor_plugin):
        """
        Constructor of the class.

        @type search_processor_plugin: SearchProcessorPlugin
        @param search_processor_plugin: The search processor plugin.
        """

        self.search_processor_plugin = search_processor_plugin

        self.search_processor_adapter_plugins_map = {}

    def process_results(self, search_results, properties):
        """
        Processes the list of search results using the specified search processor adapter.

        @rtype: List
        @return: The list of tokens processor.
        """

        # in case a processor type was not specified
        if SEARCH_PROCESSOR_TYPE_VALUE not in properties:
            # returns the search results without further processing
            return search_results

        # retrieves the processor type
        search_processor_adapter_type = properties[SEARCH_PROCESSOR_TYPE_VALUE]

        # retrieves the search processor options
        search_processor_options = properties.get(SEARCH_PROCESSOR_OPTIONS_VALUE, {})

        # retrieves the processor adapter plugin
        search_processor_adapter_plugin = self.get_search_processor_adapter_plugin(search_processor_adapter_type)

        # uses the adapter plugin to process the results
        return search_processor_adapter_plugin.process_results(search_results, search_processor_options)

    def get_search_processor_adapter_types(self):
        """
        Returns a list with the types of all the loaded search processor adapter plugins.

        @rtype List
        @return List of search processor adapter types.
        """

        # gets the type of each search processor adapter plugin loaded into the Search Processor
        search_processor_adapter_types = self.search_processor_adapter_plugins_map.keys()

        return search_processor_adapter_types

    def get_search_processor_adapter_plugin(self, search_processor_adapter_type):
        """
        Retrieves the loaded search processor adapter plugin for the specified adapter type.

        @type search_processor_adapter_type: String
        @param search_processor_adapter_type: The processor adapter type of the plugin to retrieve.
        @rtype: SearchProcessorAdapterPlugin
        @return: The loaded plugin for the adapter type
        """

        # checks for invalid plugin_type
        if not search_processor_adapter_type in self.search_processor_adapter_plugins_map:
            raise search_processor_exceptions.MissingSearchProcessorAdapterPlugin(search_processor_adapter_type)

        return self.search_processor_adapter_plugins_map[search_processor_adapter_type]

    def add_search_processor_adapter_plugin(self, plugin):
        """
        Inserts the search processor adapter plugin in the Search Processor's internal structures.

        @type plugin: SearchProcessorAdapterPlugin
        @param plugin: The search processor adapter plugin to remove.
        """

        # retrieve the search processor adapter plugin type
        plugin_type = plugin.get_type()

        # update the search processor adapter plugins map with the new plugin
        self.search_processor_adapter_plugins_map[plugin_type] = plugin

    def remove_search_processor_adapter_plugin(self, plugin):
        """
        Removes the search processor adapter plugin from the Search Processor's internal structures.

        @type plugin: SearchProcessorAdapterPlugin
        @param plugin: The search processor adapter plugin to remove.
        """

        # retrieves the search processor adapter plugin type
        plugin_type = plugin.get_type()

        # checks for invalid plugin_type
        if not plugin_type in self.search_processor_adapter_plugins_map:
            raise search_processor_exceptions.MissingSearchProcessorAdapterPlugin(plugin_type)

        # removes the plugin from the search processor adapter plugins map
        del self.search_processor_adapter_plugins_map[plugin_type]
