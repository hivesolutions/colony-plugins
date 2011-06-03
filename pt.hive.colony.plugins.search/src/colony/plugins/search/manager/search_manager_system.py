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

import search_manager_exceptions

SEARCH_CRAWLER_TYPE_VALUE = "search_crawler_type"
""" The type value """

SEARCH_PERSISTENCE_TYPE_VALUE = "search_persistence_type"
""" The persistence type value """

SEARCH_QUERY_EVALUATOR_TYPE_VALUE = "search_query_evaluator_type"
""" The key for the properties map, to access the query evaluator type """

SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE = "search_scorer_function_identifier"
""" The key for the properties map, to access the search scorer function identifier """

DEFAULT_INDEX_TYPE = "file_system"
""" The default index type """

DEFAULT_SEARCH_SCORER_FUNCTION_IDENTIFIER = "term_frequency_scorer_function"
""" The identifier of the default search scorer function """

DEFAULT_QUERY_EVALUATOR_TYPE = "query_parser"
""" The default value for the query evaluator type """

SEARCH_RESULTS_VALUE = "search_results"
""" The key to retrieve the actual search results list from the search results map """

SEARCH_STATISTICS_VALUE = "search_statistics"
""" The key to retrieve the statistics for the search from the search results map """

COUNT_VALUE = "count"
""" The flag to determine if the search query is to be only a count """

class SearchManager:
    """
    The search class.
    """

    search_manager_plugin = None
    """ The search manager plugin """

    def __init__(self, search_manager_plugin):
        """
        Constructor of the class.

        @type search_manager_plugin: SearchManagerPlugin
        @param search_manager_plugin: The search manager plugin.
        """

        self.search_manager_plugin = search_manager_plugin

    def create_index(self, properties):
        """
        Creates the search index for the given properties.

        @type properties: Dictionary
        @param properties: The properties to create the search index.
        @rtype: SearchIndex
        @return: The search index for the given properties.
        """

        start_time = time.time()

        # in case type value is not defined in properties
        if not SEARCH_CRAWLER_TYPE_VALUE in properties:
            properties[SEARCH_CRAWLER_TYPE_VALUE] = DEFAULT_INDEX_TYPE

        # retrieves the search crawler plugins
        search_crawler_plugin = self.search_manager_plugin.search_crawler_plugin

        # retrieves the search interpreter plugin
        search_interpreter_plugin = self.search_manager_plugin.search_interpreter_plugin

        # retrieves the search indexer plugin
        search_indexer_plugin = self.search_manager_plugin.search_indexer_plugin

        # starts timing the crawl
        crawling_start_time = time.time()

        # retrieves the tokens list
        tokens_list = search_crawler_plugin.get_tokens(properties)

        crawling_end_time = time.time()
        crawling_duration = crawling_end_time - crawling_start_time
        self.search_manager_plugin.debug("Crawling finished in %f s" % crawling_duration)

        tokens_processing_start_time = time.time()

        # processes the tokens list (modifying it)
        search_interpreter_plugin.process_tokens_list(tokens_list, properties)

        tokens_processing_end_time = time.time()
        tokens_processing_duration = tokens_processing_end_time - tokens_processing_start_time
        self.search_manager_plugin.debug("Processing tokens finished in %f s" % tokens_processing_duration)

        indexing_start_time = time.time()

        # creates the search index with the given tokens list and properties
        search_index = search_indexer_plugin.create_index(tokens_list, properties)

        indexing_end_time = time.time()
        indexing_duration = indexing_end_time - indexing_start_time
        self.search_manager_plugin.debug("Build index finished in %f s" % indexing_duration)

        end_time = time.time()
        index_creation_duration = end_time - start_time

        # sets the retrieved durations in the index statistics
        search_index.statistics["crawling_duration"] = crawling_duration
        search_index.statistics["tokens_processing_duration"] = tokens_processing_duration
        search_index.statistics["indexing_duration"] = indexing_duration
        search_index.statistics["index_creation_duration"] = index_creation_duration

        # returns the search index
        return search_index

    def create_index_with_identifier(self, search_index_identifier, properties):
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

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

        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        search_index_repository_plugin.remove_index(search_index_identifier)

    def persist_index(self, search_index, properties):
        """
        Persists the specified search index using the selected available persistence type.

        @type search_index: SearchIndex
        @param search_index: The search index to be persisted.
        @type properties: Dictionary
        @param properties: The properties to create the search index.
        @rtype: bool
        @return: The success of the persistence operation.
        """

        # in case the persistence type value is not defined in the properties
        if not SEARCH_PERSISTENCE_TYPE_VALUE in properties:
            raise search_manager_exceptions.MissingProperty(SEARCH_PERSISTENCE_TYPE_VALUE)

        # retrieves the search index persistence plugin
        search_index_persistence_plugin = self.search_manager_plugin.search_index_persistence_plugin

        # persists the index
        persistence_success = search_index_persistence_plugin.persist_index(search_index, properties)

        # returns with the success status signaled by the persist operation
        return persistence_success

    def persist_index_with_identifier(self, search_index_identifier, properties):
        """
        Persists an index from the index repository under the specified index identifier
        to a given location using the specified persistence type and respective options.

        @type search_index_identifier: String
        @param search_index_identifier: The index identifier in the repository.
        @type properties: Dictionary
        @param properties: The properties to persist the search index.
        @rtype: SearchIndex
        @return: The loaded search index
        """

        # retrieves the reference for the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # retrieves the search index from the repository
        search_index = search_index_repository_plugin.get_index(search_index_identifier)

        # persists the index using the base method
        persistence_success = self.persist_index(search_index, properties)

        # propagates the persistence success
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
        if not SEARCH_PERSISTENCE_TYPE_VALUE in properties:
            raise search_manager_exceptions.MissingProperty(SEARCH_PERSISTENCE_TYPE_VALUE)

        # retrieves the search index persistence plugins
        search_index_persistence_plugin = self.search_manager_plugin.search_index_persistence_plugin

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
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # loads the index using the persistence type specified in the properties
        search_index = self.load_index(properties)

        # inserts the index in the repository
        search_index_repository_plugin.add_index(search_index, search_index_identifier)

        # returns the index with which the index was added to the repository
        return search_index_identifier

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
        if not SEARCH_QUERY_EVALUATOR_TYPE_VALUE in properties:
            properties[SEARCH_QUERY_EVALUATOR_TYPE_VALUE] = DEFAULT_QUERY_EVALUATOR_TYPE

        # retrieves the query evaluator plugin
        search_query_evaluator_plugin = self.search_manager_plugin.search_query_evaluator_plugin

        # evaluates the query and retrieves the results using the available query evaluator plugin
        search_results = search_query_evaluator_plugin.evaluate_query(search_index, search_query, properties)

        return search_results

    def query_index_by_identifier(self, search_index_identifier, search_query, properties):
        """
        Call the query_index method for the index identified (in the index repository) by the provided search index identifier.
        """

        # retrieves the reference for the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

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

        # retrieves the search scorer plugin
        search_scorer_plugin = self.search_manager_plugin.search_scorer_plugin

        # initializes the search statistics map
        search_statistics = {}

        # in case the search scorer function is not defined in the properties
        if not SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE in properties:
            properties[SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE] = DEFAULT_SEARCH_SCORER_FUNCTION_IDENTIFIER

        # retrieves the search scorer formula type specified in the properties parameter
        search_scorer_function_identifier = properties[SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE]

        # if the specified scorer function is not available
        if not search_scorer_function_identifier in search_scorer_plugin.get_function_identifiers():
            raise search_manager_exceptions.InvalidFunctionRequested(search_scorer_function_identifier)

        # retrieves the count property
        count = properties.get(COUNT_VALUE, False)

        # queries the search index
        search_results = self._query_index(search_index, search_query, properties, search_statistics)

        # in case a simple count is intended
        if count:
            # counts the search results
            number_search_results = len(search_results)

            # builds the search results map
            search_results_map = {
                COUNT_VALUE : number_search_results,
                SEARCH_STATISTICS_VALUE : search_statistics
            }

            # returns the search results map
            # and skips the limiting step
            return search_results_map

        # in case the search did not retrieve any results
        if not search_results:
            # builds the search results map with the empty results
            search_results_map = {
                SEARCH_RESULTS_VALUE : search_results,
                SEARCH_STATISTICS_VALUE : search_statistics
            }

            # returns the search results map
            # and skips the subsequent steps
            return search_results_map

        # scores the results using the available search scorer plugin
        scored_search_results = self.score_results(search_results, search_index, properties, search_statistics)

        # sorts the search results using the score
        sorted_search_results = self.sort_results(scored_search_results, properties, search_statistics)


        # limit search results according to start record and number of records
        limited_search_results = self.limit_results(sorted_search_results, properties, search_statistics)

        # processes the limited search results
        processed_search_results = self.process_results(limited_search_results, properties, search_statistics)

        # builds the search results map
        search_results_map = {
            SEARCH_RESULTS_VALUE : processed_search_results,
            SEARCH_STATISTICS_VALUE : search_statistics
        }

        # returns the full search results map
        return search_results_map

    def search_index_by_identifier(self, search_index_identifier, search_query, properties):
        """
        Calls the query_index method for the index identified (in the index repository) by the provided search index identifier.
        """

        # retrieves the reference for the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # retrieves the search index from the repository
        search_index = search_index_repository_plugin.get_index(search_index_identifier)

        # queries the index with the search query
        # requesting scoring and sorting services
        search_results_map = self.search_index(search_index, search_query, properties)

        # return the final scored and sorted results
        return search_results_map

    def get_index_by_identifier(self, search_index_identifier):
        """
        Retrieves the index with the specified identifier from the index repository.
        """

        # retrieves the reference for the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # retrieves the index from the repository
        return search_index_repository_plugin.get_index(search_index_identifier)

    def get_index_identifiers(self):
        """
        Retrieves a list with the identifiers for all the indexes in the index repository.
        """

        # retrieves the reference to the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # retrieves all the identifiers
        index_identifiers = search_index_repository_plugin.get_index_identifiers()

        return index_identifiers

    def get_index_metadata(self, search_index_identifier):
        """
        Retrieves the metadata for the index with the specified identifier.
        """

        # retrieves the reference to the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # retrieves the index metadata
        index_metadata = search_index_repository_plugin.get_index_metadata(search_index_identifier)

        return index_metadata

    def get_indexes_metadata(self):
        """
        Retrieves the metadata for all the indexes in the index repository.
        """

        # retrieves the reference to the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # retrieves all the index metadata
        indexes_metadata = search_index_repository_plugin.get_indexes_metadata()

        return indexes_metadata

    def has_index(self, search_index_identifier):
        """
        Determines if the provided identifier exists in the index repository
        """

        # retrieves the reference to the index repository
        search_index_repository_plugin = self.search_manager_plugin.search_index_repository_plugin

        # determines if the index exists
        has_index = search_index_repository_plugin.has_index(search_index_identifier)

        return has_index

    def get_search_crawler_adapter_types(self):
        """
        Retrieves the available crawler adapter types in the crawler plugin.
        """

        # retrieves the reference for the search crawler plugin
        search_crawler_plugin = self.search_manager_plugin.search_crawler_plugin

        # retrieves all the crawler types
        crawler_types = search_crawler_plugin.get_search_crawler_adapter_types()

        return crawler_types

    def get_search_index_persistence_adapter_types(self):
        """
        Retrieves the available search persistence adapter types in the search persistence plugin.
        """

        # retrieves the reference for the search persistence plugin
        search_index_persistence_plugin = self.search_manager_plugin.search_index_persistence_plugin

        # retrieves all the search persistence adapter types
        search_index_persistence_adapter_types = search_index_persistence_plugin.get_search_index_persistence_adapter_types()

        return search_index_persistence_adapter_types

    def _query_index(self, search_index, search_query, properties, search_statistics):
        # records the query time for the operation
        start_time = time.time()

        # disable the garbage collector during parsing, to improve performance
        gc.disable()

        # wrapping the query operation in a try-finally block to force the garbage collector to become enabled
        try:
            search_results = self.query_index(search_index, search_query, properties)
        finally:
            # re-enable the garbage collector
            gc.enable()

        # determines the elapsed querying duration
        querying_duration = time.time() - start_time

        # logs the querying duration
        self.search_manager_plugin.debug("Querying index finished in %f s" % querying_duration)

        # stores the querying duration statistic in the statistics map
        search_statistics["querying_duration"] = querying_duration

        return search_results

    def score_results(self, search_results, search_index, properties, search_statistics):
        # records the start time for the operation
        start_time = time.time()

        # retrieves the search scorer plugin
        search_scorer_plugin = self.search_manager_plugin.search_scorer_plugin

        # scores the results using the plugin
        scored_search_results = search_scorer_plugin.score_results(search_results, search_index, properties)

        # determines the elapsed scoring time
        scoring_duration = time.time() - start_time

        # logs the scoring duration
        self.search_manager_plugin.debug("Scoring results finished in %f s" % scoring_duration)

        # stores the scoring duration statistic in the statistics map
        search_statistics["scoring_duration"] = scoring_duration

        return scored_search_results

    def sort_results(self, scored_search_results, properties, search_statistics):
        # records the start time for the operation
        start_time = time.time()

        # retrieves the search sorter plugin
        search_sorter_plugin = self.search_manager_plugin.search_sorter_plugin

        # sorts the already scored search results
        sorted_search_results = search_sorter_plugin.sort_results(scored_search_results, properties)

        # determines the elapsed scoring time
        sorting_duration = time.time() - start_time

        # logs the sorting duration
        self.search_manager_plugin.debug("Sorting results finished in %f s" % sorting_duration)

        # stores the sorting duration statistic in the statistics map
        search_statistics["sorting_duration"] = sorting_duration

        return sorted_search_results

    def limit_results(self, sorted_search_results, properties, search_statistics):
        # records the start time for the operation
        start_time = time.time()

        # retrieves the start record
        start_record = properties.get("start_record", None)

        # retrieves the number of records
        number_records = properties.get("number_records", None)

        # determines the end record
        if not start_record == None and not number_records == None:
            end_record = start_record + number_records
        else:
            end_record = None

        # limits the search results
        limited_search_results = sorted_search_results[start_record:end_record]

        # determines the elapsed limiting time
        limiting_duration = time.time() - start_time

        # logs the elapsed limiting time
        self.search_manager_plugin.debug("Limiting results finished in %f s" % limiting_duration)

        # stores the limiting duration statistic in the statistics map
        search_statistics["limiting_duration"] = limiting_duration

        return limited_search_results

    def process_results(self, limited_search_results, properties, search_statistics):
        # records the start time for the operation
        start_time = time.time()

        # retrieves the search processor plugin
        search_processor_plugin = self.search_manager_plugin.search_processor_plugin

        # processes the results using the plugin
        processed_search_results = search_processor_plugin.process_results(limited_search_results, properties)

        # determines the elasped processing duration
        processing_duration = time.time() - start_time

        # logs the elapsed processing time
        self.search_manager_plugin.debug("Processing results finished in %f s" % processing_duration)

        # stores the limiting duration statistic in the statistics map
        search_statistics["processing_duration"] = processing_duration

        return processed_search_results
