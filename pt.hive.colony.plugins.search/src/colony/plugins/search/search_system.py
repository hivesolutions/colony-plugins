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

import gc
import time

import search_exceptions

TYPE_VALUE = "type"
""" The type value """

PERSISTENCE_TYPE_VALUE = "persistence_type"
""" The persistence type value """

QUERY_EVALUATOR_TYPE_VALUE = "query_evaluator_type"
""" The key for the properties map, to access the query evaluator type """

SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE = "search_scorer_function_identifier"
""" The key for the properties map, to access the search scorer function identifier """

DEFAULT_INDEX_TYPE = "file_system"
""" The default index type """

DEFAULT_SEARCH_SCORER_FUNCTION_IDENTIFIER = "term_frequency_scorer_function"
""" The identifier of the default search scorer function """

DEFAULT_QUERY_EVALUATOR_TYPE = "query_parser"
""" The default value for the query evaluator type """

SORT_ORDER_VALUE = "sort_order"
""" The key to retrieve the sort order from the properties map """

class Search:
    """
    The search class.
    """

    search_plugin = None
    """ The search plugin """

    def __init__(self, search_plugin):
        """
        Constructor of the class.

        @type search_plugin: SearchPlugin
        @param search_plugin: The search plugin.
        """

        self.search_plugin = search_plugin

    def create_index(self, properties):
        """
        Creates the search index for the given properties.

        @type properties: Dictionary
        @param properties: The properties to create the search index.
        @rtype: SearchIndex
        @return: The search index for the given properties.
        """

        # in case type value is not defined in properties
        if not TYPE_VALUE in properties:
            properties[TYPE_VALUE] = DEFAULT_INDEX_TYPE

        # retrieves the search crawler plugins
        search_crawler_plugin = self.search_plugin.search_crawler_plugin

        # retrieves the search interpreter plugin
        search_interpreter_plugin = self.search_plugin.search_interpreter_plugin

        # retrieves the search indexer plugin
        search_indexer_plugin = self.search_plugin.search_indexer_plugin

        # retrieves the type of index
        index_type = properties[TYPE_VALUE]

        start_time = time.time()

        # retrieves the tokens list
        tokens_list = search_crawler_plugin.get_tokens(properties)

        end_time = time.time()
        duration = end_time - start_time
        self.search_plugin.debug("Crawling finished in %f s" % duration)

        start_time = time.time()

        # processes the tokens list (modifying it) and retrieves the used interpreter adapters list
        used_interpreter_adapter_list = search_interpreter_plugin.process_tokens_list(tokens_list, properties)

        end_time = time.time()
        duration = end_time - start_time
        self.search_plugin.debug("Processing tokens finished in %f s" % duration)

        start_time = time.time()

        # creates the search index with the given tokens list and properties
        search_index = search_indexer_plugin.create_index(tokens_list, properties)

        end_time = time.time()
        duration = end_time - start_time
        self.search_plugin.debug("Build index finished in %f s" % duration)

        # returns the search index
        return search_index

    def create_index_with_identifier(self, search_index_identifier, properties):
        search_index_repository_plugin = self.search_plugin.search_index_repository_plugin

        search_index = self.create_index(properties)

        search_index_repository_plugin.add_index(search_index, search_index_identifier)

        return search_index

    def remove_index_with_identifier(self, search_index_identifier, properties):
        """
        Remove an index from the repository.

        @type search_index_identifier: String
        @param search_index_identifier: The index identifier in the repository.
        @type properties: Dictionary
        @param properties: The properties to configure the removal operation.
        """

        search_index_repository_plugin = self.search_plugin.search_index_repository_plugin

        search_index_repository_plugin.remove_index(search_index_identifier)

    def persist_index(self, search_index, properties):
        """
        Persists the specified search index using the selected available persistence type.

        @type search_index: SearchIndex
        @param search_index: The search index to be persisted.
        @type properties: Dictionary
        @param properties: The properties to create the search index.
        @rtype: boolean
        @return: The success of the persistence operation.
        """

        # in case the persistence type value is not defined in the properties
        if not PERSISTENCE_TYPE_VALUE in properties:
            raise search_exceptions.MissingProperty(PERSISTENCE_TYPE_VALUE)

        # retrieves the search index persistence plugin
        search_index_persistence_plugin = self.search_plugin.search_index_persistence_plugin

        # persists the index
        persistence_success = search_index_persistence_plugin.persist_index(search_index, properties)

        # returns with the success status signaled by the persist operation
        return persistence_success

    def load_index(self, properties):
        """
        Loads an index from a given location using the specified persistence type.

        @type properties: Dictionary
        @param properties: The properties to load the search index.
        @rtype: SearchIndex
        @return: The loaded search index
        """

        # in case the persistence type value is not defined in the properties
        if not PERSISTENCE_TYPE_VALUE in properties:
            raise search_exceptions.MissingProperty(PERSISTENCE_TYPE_VALUE)

        # retrieves the search index persistence plugins
        search_index_persistence_plugin = self.search_plugin.search_index_persistence_plugin

        # loads the index
        search_index = search_index_persistence_plugin.load_index(properties)

        # returns the retrieved search index
        return search_index

    def load_index_with_identifier(self, search_index_identifier, properties):
        """
        Loads an index from a given location using the specified persistence type, and
        stores it in the index repository under the specified index identifier.

        @type properties: Dictionary
        @param properties: The properties to load the search index.
        @rtype: SearchIndex
        @return: The loaded search index
        """

        # retrieves the search index repository plugin
        search_index_repository_plugin = self.search_plugin.search_index_repository_plugin

        # loads the index using the persistence type specified in the properties
        search_index = self.load_index(properties)

        # inserts the index in the repository
        search_index_repository_plugin.add_index(search_index, search_index_identifier)

        return search_index

    def query_index(self, search_index, search_query, properties):
        """
        Queries the provided index, using an available search_query_evaluator plugin for the query type specified in the properties.

        @type search_index: SearchIndex
        @param search_index: The index to use in the query.
        @type search_query: String
        @param search_query: The query to search against the index.
        @type properties: Dictionary
        @param properties: The properties to to query the search index.
        @rtype: List
        @return: The result set for the query in the search index, as a list of (document id, search result information) tuples.
        """

        # in case the persistence type value is not defined in the properties
        if not QUERY_EVALUATOR_TYPE_VALUE in properties:
            properties[QUERY_EVALUATOR_TYPE_VALUE] = DEFAULT_QUERY_EVALUATOR_TYPE

        # retrieves the query evaluator plugin
        search_query_evaluator_plugin = self.search_plugin.search_query_evaluator_plugin

        # evaluates the query and retrieves the results using the available query evaluator plugin
        search_results = search_query_evaluator_plugin.evaluate_query(search_index, search_query, properties)

        return search_results

    def query_index_by_identifier(self, search_index_identifier, search_query, properties):
        """
        Call the query_index method for the index identified (in the index repository) by the provided search index identifier.
        """

        # retrieves the reference for the index repository
        search_index_repository_plugin = self.search_plugin.search_index_repository_plugin

        # retrieves the search index from the repository
        search_index = search_index_repository_plugin.get_index(search_index_identifier)

        # queries the index with the search query
        search_results = self.query_index(search_index, search_query, properties)

        # return the final scored and sorted results
        return search_results

    def search_index(self, search_index, search_query, properties):
        """
        Queries the provided index, using an available search_query_evaluator plugin
        for the query type specified in the properties;
        Scores the results, using the injected search scorer plugin with the function
        specified in the properties;
        Sorts the results by score.

        @type search_index: SearchIndex
        @param search_index: The index to use in the query.
        @type search_query: String
        @param search_query: The query to search against the index.
        @type properties: Dictionary
        @param properties: The properties to to query the search index.
        @rtype: List
        @return: The result set for the query in the search index, as a list of
        (document id, search result information) tuples sorted by score.
        """

        # in case the search scorer function is not defined in the properties
        if not SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE in properties:
            properties[SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE] = DEFAULT_SEARCH_SCORER_FUNCTION_IDENTIFIER

        # retrieves the search scorer plugins
        search_scorer_plugin = self.search_plugin.search_scorer_plugin

        # retrieves the search sorter plugins
        search_sorter_plugin = self.search_plugin.search_sorter_plugin

        # retrieves the search scorer formula type specified in the properties parameter
        search_scorer_function_identifier = properties[SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE]

        # if there was no search scorer plugin available
        if not search_scorer_function_identifier in search_scorer_plugin.get_function_identifiers():
            raise search_exceptions.InvalidFunctionRequested(search_scorer_function_identifier)

        # performs the search using own query_index method
        start_time = time.time()

        # disable the garbage collector during parsing, to improve performance
        gc.disable()

        # wrapping the query operation in a try-finally block to force the garbage collector to become enabled
        try:
            search_results = self.query_index(search_index, search_query, properties)
        finally:
            # re-enable the garbage collector
            gc.enable()

        end_time = time.time()
        duration = end_time - start_time
        self.search_plugin.debug("Querying index finished in %f s" % duration)

        if search_results:
            # scores the results using the available search scorer plugin
            start_time = time.time()

            scored_search_results = search_scorer_plugin.score_results(search_results, search_index, properties)

            end_time = time.time()
            duration = end_time - start_time
            self.search_plugin.debug("Scoring results finished in %f s" % duration)

            # gets the search scorer function repository plugin
            search_scorer_function_repository_plugin = self.search_plugin.search_scorer_function_repository_plugin

            # retrieves the top level scorer function
            search_scorer_function = search_scorer_function_repository_plugin.get_function(search_scorer_function_identifier)

            # sorts the search results using the score
            start_time = time.time()

            sorted_search_results = search_sorter_plugin.sort_results(scored_search_results, properties)

            end_time = time.time()
            duration = end_time - start_time
            self.search_plugin.debug("Sorting results finished in %f s" % duration)
        else:
            # an empty result set is sorted by nature
            sorted_search_results = search_results

        return sorted_search_results

    def search_index_by_identifier(self, search_index_identifier, search_query, properties):
        """
        Calls the query_index method for the index identified (in the index repository) by the provided search index identifier.
        """

        # retrieves the reference for the index repository
        search_index_repository_plugin = self.search_plugin.search_index_repository_plugin

        # retrieves the search index from the repository
        search_index = search_index_repository_plugin.get_index(search_index_identifier)

        # queries the index with the search query
        # requesting scoring and sorting services
        sorted_search_results = self.search_index(search_index, search_query, properties)

        # return the final scored and sorted results
        return sorted_search_results

    def get_indexes_metadata(self):
        """
        Retrieves the metadata for all the indexes in the index repository.
        """

        # retrieves the reference for the index repository
        search_index_repository_plugin = self.search_plugin.search_index_repository_plugin

        # retrieves all the index metadata
        indexes_metadata = search_index_repository_plugin.get_indexes_metadata()

        return indexes_metadata
