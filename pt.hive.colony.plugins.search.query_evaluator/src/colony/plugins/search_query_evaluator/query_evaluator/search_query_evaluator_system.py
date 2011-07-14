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

SEARCH_QUERY_EVALUATOR_TYPE_VALUE = "search_query_evaluator_type"
""" The key for the properties map, to access the query evaluator type """

import search_query_evaluator_exceptions

class SearchQueryEvaluator:
    """
    The search query evaluator class.
    """

    search_query_evaluator_plugin = None
    """ The search query evaluator plugin """

    search_query_evaluator_adapter_plugins_map = {}
    """ The search query evaluator adapter plugins map """

    def __init__(self, search_query_evaluator_plugin):
        """
        Constructor of the class.

        @type search_query_evaluator_plugin: SearchQueryEvaluatorPlugin
        @param search_query_evaluator_plugin: The search query evaluator plugin.
        """

        # gets the plugin
        self.search_query_evaluator_plugin = search_query_evaluator_plugin

        # initializes the evaluator adapter map
        self.search_query_evaluator_adapter_plugins_map = {}

    def evaluate_query(self, search_index, query, properties):
        """
        The method to start the search query evaluation using a specified query evaluator type.

        @type search_index: SearchIndex
        @param search_index: The search index to be used.
        @type query: String
        @param query: The query string with the search terms.
        @type properties: Dictionary
        @param properties: The map of properties for the query evaluation.
        @rtype: Dictionary
        @return: The result set for the query in the search index, as a map with document id keys.
        """

        if SEARCH_QUERY_EVALUATOR_TYPE_VALUE not in properties:
                search_query_evaluator_exceptions.MissingProperty(SEARCH_QUERY_EVALUATOR_TYPE_VALUE)

        search_query_evaluator_type = properties[SEARCH_QUERY_EVALUATOR_TYPE_VALUE]

        # retrieves the index persistence adapter plugin to use in the load operation
        search_query_evaluator_plugin = self.get_search_query_evaluator_adapter_plugin(search_query_evaluator_type)

        # uses the selected adapter to load the index
        return search_query_evaluator_plugin.evaluate_query(search_index, query, properties)

    def get_search_query_evaluator_adapter_types(self):
        """
        Returns a list with the types of all the loaded search query evaluator adapter plugins.

        @rtype: list
        @return: List of search query evaluator adapter types.
        """

        # gets the type of each search index persistence adapter plugin loaded into the Search Query Evaluator
        search_query_evaluator_adapter_types = self.search_query_evaluator_adapter_plugins_map.keys()

        return search_query_evaluator_adapter_types

    def get_search_query_evaluator_adapter_plugin(self, search_query_evaluator_adapter_type):
        """
        Retrieves the loaded search query evaluator adapter plugin for the specified adapter type.

        @type search_query_evaluator_adapter_type: String
        @param search_query_evaluator_adapter_type: The search query evaluator adapter type of the plugin to retrieve.
        @rtype: SearchQueryEvaluatorAdapterPlugin
        @return: The loaded plugin for the adapter type
        """

        # checks for invalid plugin type
        if not search_query_evaluator_adapter_type in self.search_query_evaluator_adapter_plugins_map:
            raise search_query_evaluator_exceptions.MissingSearchQueryEvaluatorAdapterPlugin(search_query_evaluator_adapter_type)

        return self.search_query_evaluator_adapter_plugins_map[search_query_evaluator_adapter_type]

    def add_search_query_evaluator_adapter_plugin(self, plugin):
        """
        Inserts the search query evaluator adapter plugin in the Search Query Evaluator's internal structures.

        @type plugin: SearchQueryEvaluatorAdapterPlugin
        @param plugin: The search query evaluator adapter plugin to remove.
        """

        # retrieve the search query evaluator adapter plugin type
        plugin_type = plugin.get_type()

        # update the search query evaluator adapter plugins map with the new plugin
        self.search_query_evaluator_adapter_plugins_map[plugin_type] = plugin

    def remove_search_query_evaluator_adapter_plugin(self, plugin):
        """
        Removes the search query evaluator adapter plugin, with the type of the provided plugin, from the Search Query Evaluator's internal structures.

        @type plugin: SearchQueryEvaluatorAdapterPlugin
        @param plugin: The search index_persistence adapter plugin to remove.
        """

        # retrieves the search index persistence adapter plugin type
        plugin_type = plugin.get_type()

        # checks for invalid plugin type
        if not plugin_type in self.search_query_evaluator_adapter_plugins_map:
            raise search_query_evaluator_exceptions.MissingSearchQueryEvaluatorAdapterPlugin(plugin_type)

        # removes the plugin from the search index persistence adapter plugins map
        del self.search_query_evaluator_adapter_plugins_map[plugin_type]
