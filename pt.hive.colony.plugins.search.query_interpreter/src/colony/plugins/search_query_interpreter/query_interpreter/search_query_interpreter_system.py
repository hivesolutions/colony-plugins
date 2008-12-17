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

class SearchQueryInterpreter:
    """
    The search query interpreter class.
    """

    search_query_interpreter_plugin = None
    """ The search query interpreter plugin """

    def __init__(self, search_query_interpreter_plugin):
        """
        Constructor of the class.
        
        @type search_query_interpreter_plugin: SearchQueryInterpreterPlugin
        @param search_query_interpreter_plugin: The search query interpreter plugin.
        """

        self.search_query_interpreter_plugin = search_query_interpreter_plugin

    def interpret_query(self, query_string, properties):
        """
        The method to start the search query interpreter.
        
        @type query_string: String
        @param query_string: The query string with the search terms.
        @type properties: Dictionary
        @param properties: The map of properties for the query interpretation.
        @rtype: SearchQuery
        @return: A search query object created according to the search interpreter adapters available.
        """

        search_query_interpreter_adapter_plugins = self.search_query_interpreter_plugin.search_query_interpreter_adapter_plugins

        sortable_search_query_interpreter_adapter_plugins = [SortableSearchQueryInterpreterAdapterPlugin(value) for value in search_query_interpreter_adapter_plugins]
        sortable_search_query_interpreter_adapter_plugins.sort()
        sortable_search_query_interpreter_adapter_plugins.reverse()
        sorted_search_query_interpreter_adapter_plugins = [value.search_query_interpreter_adapter_plugin for value in sortable_search_query_interpreter_adapter_plugins]

        root_search_query_node = self.reduce_query_string(query_string, sorted_search_query_interpreter_adapter_plugins)

        search_query = SearchQuery()

        search_query.root_search_query_node = root_search_query_node

        return search_query

    def reduce_query_string(self, query_string, search_query_interpreter_adapter_plugins):

        index = 0

        for search_query_interpreter_adapter_plugin in search_query_interpreter_adapter_plugins:

            intepretation_result = search_query_interpreter_adapter_plugin.interpret_query(query_string)

            if intepretation_result:
                intepretation_operator, interpretation_operands = intepretation_result

                search_query_node = SearchQueryNode()

                search_query_node.operator = intepretation_operator

                for interpretation_operand in interpretation_operands:
                    operand_node = self.reduce_query_string(interpretation_operand, search_query_interpreter_adapter_plugins[index:])
                    search_query_node.operands.append(operand_node)

                return search_query_node

            index += 1

        leaf_search_query_node = LeafSearchQueryNode()

        leaf_search_query_node.operands.append(query_string)

        return leaf_search_query_node

class SortableSearchQueryInterpreterAdapterPlugin:

    search_query_interpreter_adapter_plugin = None

    def __init__(self, search_query_interpreter_adapter_plugin):    
        self.search_query_interpreter_adapter_plugin = search_query_interpreter_adapter_plugin

    def __cmp__(self, other):
        priority = self.get_priority()
        other_priority = other.get_priority()

        if priority > other_priority:
            return 1
        elif priority < other_priority:
            return -1
        else:
            return 0

    def get_priority(self):
        return search_query_interpreter_adapter_plugin.get_priority()

class SearchQuery:

    root_search_query_node = None

    def __init__(self):
        pass

class SearchQueryNode:

    operator = "none"

    operands = []

    def __init__(self):
        self.operands = []

class LeafSearchQueryNode(SearchQueryNode):

    def __init__(self):
        SearchQueryNode.__init__(self)
        self.operator = "none"
