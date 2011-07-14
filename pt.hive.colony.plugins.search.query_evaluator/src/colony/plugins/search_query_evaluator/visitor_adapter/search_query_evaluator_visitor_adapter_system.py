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

import search_query_evaluator_visitor

QUERY_EVALUATOR_TYPE = "query_parser"
""" The default query evaluator type """

DOCUMENT_ID_VALUE = "document_id"
""" The document id value """

DOCUMENT_INFORMATION_MAP_VALUE = "document_information_map"
""" The document information map value """

class SearchQueryEvaluatorVisitorAdapter:
    """
    The search query evaluator class.
    """

    search_query_evaluator_visitor_adapter_plugin = None
    """ The search query evaluator visitor adapter plugin """

    def __init__(self, search_query_evaluator_visitor_adapter_plugin):
        """
        Constructor of the class.

        @type search_query_evaluator_visitor_adapter_plugin: SearchQueryEvaluatorVisitorAdapterPlugin
        @param search_query_evaluator_visitor_adapter_plugin: The search query evaluator visitor adapter plugin.
        """

        self.search_query_evaluator_visitor_adapter_plugin = search_query_evaluator_visitor_adapter_plugin

    def get_type(self):
        """
        Returns the type of query evaluator of the class.
        """

        return QUERY_EVALUATOR_TYPE

    def evaluate_query(self, search_index, query, properties):
        """
        The method to start the search query evaluator visitor adapter.

        @type search_index: SearchIndex
        @param search_index: The search index to be used.
        @type query: String
        @param query: The query string with the search terms.
        @type properties: Dictionary
        @param properties: The map of properties for the query evaluation.
        @rtype: Dictionary
        @return: The result set for the query in the search index, as a map with document id keys.
        """

        # retrieve the query interpreter plugin
        search_query_interpreter_plugin = self.search_query_evaluator_visitor_adapter_plugin.search_query_interpreter_plugin

        # parse the search query into a query object
        search_query = search_query_interpreter_plugin.parse_query(query, properties)

        # retrieve the root node of the query abstract syntax tree
        root_search_query_node = search_query.root_search_query_node

        # traverse the query AST in post order with the index search visitor
        index_search_visitor = search_query_evaluator_visitor.IndexSearchVisitor(search_index)

        # visit the query abstract syntax tree
        root_search_query_node.accept_post_order(index_search_visitor)

        # retrieve the index search visitor results from its stack
        index_search_visitor_results = index_search_visitor.context_stack[0]

        # the search results list will hold a search result information map for each search result
        search_results = []

        # convert the index search visitor results map
        # into a search result list of search result information maps containing the key
        for index_search_visitor_result_key, index_search_visitor_result_value in index_search_visitor_results.items():
            # create a new map from each search result map
            search_result_map = index_search_visitor_result_value

            # set the document id, using the key in the results map
            # the map with all the search results is now going to be a list
            search_result_map[DOCUMENT_ID_VALUE] = index_search_visitor_result_key

            # adds the document information for the current document
            search_result_map[DOCUMENT_INFORMATION_MAP_VALUE] = search_index.get_document_information_map_metadata(index_search_visitor_result_key)

            # add the map to the search results list
            search_results.append(search_result_map)

        return search_results
