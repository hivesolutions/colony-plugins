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

import search_crawler_exceptions

SEARCH_CRAWLER_TYPE_VALUE = "search_crawler_type"
""" The key to retrieve the crawler type from the properties map """

SEARCH_CRAWLER_OPTIONS_VALUE = "search_crawler_options"
""" The key to retrieves the crawler options from the properties map """

class SearchCrawler:
    """
    The search crawler class.
    """

    search_crawler_plugin = None
    """ The search crawler plugin """

    search_crawler_adapter_plugins_map = {}
    """ The search crawler adapter plugins map """

    def __init__(self, search_crawler_plugin):
        """
        Constructor of the class.

        @type search_crawler_plugin: SearchCrawlerPlugin
        @param search_crawler_plugin: The search crawler plugin.
        """

        self.search_crawler_plugin = search_crawler_plugin

        self.search_crawler_adapter_plugins_map = {}

    def get_tokens(self, properties):
        """
        Retrieves the list of tokens resulting from crawling the specified location, using the required crawler adapter.

        @rtype: List
        @return: The list of tokens crawler.
        """

        # if no type is defined, uses the default crawler adapter type
        if SEARCH_CRAWLER_TYPE_VALUE not in properties:
            raise search_crawler_exceptions.MissingProperty(SEARCH_CRAWLER_TYPE_VALUE)

        # retrieves the search crawler adapter type
        search_crawler_adapter_type = properties[SEARCH_CRAWLER_TYPE_VALUE]

        # retrieves the search crawler options
        search_crawler_options = properties.get(SEARCH_CRAWLER_OPTIONS_VALUE, {})

        # retrieves the crawler adapter plugin
        search_crawler_adapter_plugin = self.get_search_crawler_adapter_plugin(search_crawler_adapter_type)

        # uses the adapter plugin to execute the get tokens operation
        return search_crawler_adapter_plugin.get_tokens(search_crawler_options)

    def get_search_crawler_adapter_types(self):
        """
        Returns a list with the types of all the loaded search crawler adapter plugins.

        @rtype List
        @return List of search crawler adapter types.
        """

        # gets the type of each search crawler adapter plugin loaded into the Search Crawler
        search_crawler_adapter_types = self.search_crawler_adapter_plugins_map.keys()

        return search_crawler_adapter_types

    def get_search_crawler_adapter_plugin(self, search_crawler_adapter_type):
        """
        Retrieves the loaded search crawler adapter plugin for the specified adapter type.

        @type search_crawler_adapter_type: String
        @param search_crawler_adapter_type: The crawler adapter type of the plugin to retrieve.
        @rtype: SearchCrawlerAdapterPlugin
        @return: The loaded plugin for the adapter type
        """

        # checks for invalid plugin_type
        if not search_crawler_adapter_type in self.search_crawler_adapter_plugins_map:
            raise search_crawler_exceptions.MissingSearchCrawlerAdapterPlugin(search_crawler_adapter_type)

        return self.search_crawler_adapter_plugins_map[search_crawler_adapter_type]

    def add_search_crawler_adapter_plugin(self, plugin):
        """
        Inserts the search crawler adapter plugin in the Search Crawler's internal structures.

        @type plugin: SearchCrawlerAdapterPlugin
        @param plugin: The search crawler adapter plugin to remove.
        """

        # retrieve the search crawler adapter plugin type
        plugin_type = plugin.get_type()

        # update the search crawler adapter plugins map with the new plugin
        self.search_crawler_adapter_plugins_map[plugin_type] = plugin

    def remove_search_crawler_adapter_plugin(self, plugin):
        """
        Removes the search crawler adapter plugin from the Search Crawler's internal structures.

        @type plugin: SearchCrawlerAdapterPlugin
        @param plugin: The search crawler adapter plugin to remove.
        """

        # retrieves the search crawler adapter plugin type
        plugin_type = plugin.get_type()

        # checks for invalid plugin_type
        if not plugin_type in self.search_crawler_adapter_plugins_map:
            raise search_crawler_exceptions.MissingSearchCrawlerAdapterPlugin(plugin_type)

        # removes the plugin from the search crawler adapter plugins map
        del self.search_crawler_adapter_plugins_map[plugin_type]
