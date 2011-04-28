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

import search_scorer_exceptions

SCORER_FUNCTION_IDENTIFIER_VALUE = "search_scorer_function_identifier"
""" The identifier for the main scoring function in the scorer function repository """

INDEX_TIME_METRIC_TYPE = "index_time"
""" The identifier for the index time metric type """

SEARCH_TIME_METRIC_TYPE = "search_time"
""" The identifier for the search time metric type """

SCORE_VALUE = "score"
""" The score value key in the search result dictionary """

SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE = "search_scorer_function_identifier"
""" The key to retrieve the search scorer function identifier, used to compute the score, in the search result map """

DOCUMENT_ID_VALUE = "document_id"
""" The key to retrieve the document id, in the search result map """

METRICS_VALUE = "metrics"
""" The metrics value key in the search result dictionary """

HITS_VALUE = "hits"
""" The key that retrieves the set of results, contained in an arbitrary level """

DOCUMENT_LEVEL_VALUE = "document_level"
""" The key that retrieves the metrics values from the document level metrics """

WORD_LEVEL_VALUE = "word_level"
""" The key that retrieves the metrics values from the word level metrics """

WORD_DOCUMENT_LEVEL_VALUE = "word_document_level"
""" The key that retrieves the metrics values from the word document level metrics """

HIT_LEVEL_VALUE = "hit_level"
""" The key that retrieves the metrics values from the hit level metrics """

class SearchScorer:
    """
    The search scorer class.
    """

    search_scorer_plugin = None
    """ The search scorer plugin """

    def __init__(self, search_scorer_plugin):
        """
        Constructor of the class.

        @type search_scorer_plugin: SearchScorerPlugin
        @param search_scorer_plugin: The search scorer plugin.
        """

        self.search_scorer_plugin = search_scorer_plugin

    def get_function_identifiers(self):

        # retrieves the current function repository
        search_scorer_function_repository_plugin = self.search_scorer_plugin.search_scorer_function_repository_plugin

        # gets the identifiers of the available functions from the repository
        available_function_identifiers = search_scorer_function_repository_plugin.get_function_identifiers()

        return available_function_identifiers


    def score_results(self, search_results, search_index, properties):
        """
        The method to compute the score for a list of search results.

        @type search_results: List
        @param search_results: The list of search results.
        @type search_index: SearchIndex
        @param search_index: The search index used to perform the search.
        @type properties: Dictionary
        @param properties: The properties to configure the scoring process.
        @rtype: List
        @return: The list of search results with the computed scores attached.
        """

        # retrieves the current function repository
        search_scorer_function_repository_plugin = self.search_scorer_plugin.search_scorer_function_repository_plugin

        # retrieves the current metric repository
        search_scorer_metric_repository_plugin = self.search_scorer_plugin.search_scorer_metric_repository_plugin

        # determines top level scoring function according to properties
        if not SCORER_FUNCTION_IDENTIFIER_VALUE in properties:
            raise search_scorer_exceptions.MissingProperty(SCORER_FUNCTION_IDENTIFIER_VALUE)

        scorer_function_identifier = properties[SCORER_FUNCTION_IDENTIFIER_VALUE]

        # retrieves the top level scorer function
        scorer_function = search_scorer_function_repository_plugin.get_function(scorer_function_identifier)

        # gets the metrics required by the scorer function
        required_metrics_identifiers_list = scorer_function.get_required_metrics_identifiers()

        # retrieves the required metrics from the metrics repository
        scorer_metrics = search_scorer_metric_repository_plugin.get_metrics(required_metrics_identifiers_list)

        # computes the specified metrics for the index
        if scorer_metrics:
            # the metrics for the search results are calculated in place, adding to the index metadata
            self.compute_metrics(scorer_metrics, search_results, search_index, properties)

        # computes the top level function using the gathered metrics and the coefficients specified in the properties map
        search_results_scores = scorer_function.compute(search_results, properties)

        # sets the search result scores in the existing search results metadata
        # (decouples function computation from search result structure details)
        search_result_index = 0
        for search_result in search_results:
            search_result[SCORE_VALUE] = search_results_scores[search_result_index]
            search_result[SEARCH_SCORER_FUNCTION_IDENTIFIER_VALUE] = scorer_function_identifier
            search_result_index += 1

        # returns a list of scores for each search result
        return search_results

    def compute_metrics(self, scorer_metrics, search_results, search_index, properties):
        """
        Computes the specified metrics for the specified search results.

        @type scorer_metrics: List
        @param scorer_metrics: The list of SearchScorerMetrics to apply to the search results.
        @type search_results: List
        @param search_results: The list of search results to add metric information. Will be modified by operation.
        @type search_index: SearchIndex
        @param search_index: The search index to gather available index time metrics or to compute query time ones.
        Will be modified by operation.
        @type properties: Dictionary
        @param properties: The properties map to configure the metrics computation.
        @rtype: bool
        @return: The success of the metric computation operation.
        """

        # the computed metrics values are gathered in a map, and then applied to the search results
        # decreasing coupling between the metrics computation and from the search results internal structure

        # the map holds the computed metrics for each metric level:
        # - document level: metrics that apply to a document as a whole
        # - word level: metrics that apply to a word across all documents
        # - word in document level: metrics that apply to a word in a specific document
        # - hit level: metrics that apply to a specific hit of a specific word in a specific document
        metrics_values_level_map = {
            DOCUMENT_LEVEL_VALUE : {},
            WORD_LEVEL_VALUE : {},
            WORD_DOCUMENT_LEVEL_VALUE : {},
            HIT_LEVEL_VALUE : {}
        }

        # computes each metric for the search results
        for scorer_metric in scorer_metrics:
            scorer_metric_identifier = scorer_metric.get_identifier()
            scorer_metric_level = scorer_metric.get_level()

            # in case this is the first metric with this level,
            # inserts a new map for the level
            if scorer_metric_level not in metrics_values_level_map:
                metrics_values_level_map[scorer_metric_level] = {}

            # retrieves the metrics for the specified level
            metrics_values_map = metrics_values_level_map[scorer_metric_level]

            # computes the metric
            metrics_values_map[scorer_metric_identifier] = scorer_metric.compute(search_results, search_index, properties)

        # applies each computed metric to the search results, by level

        # retrieves the document level metrics
        document_level_metrics_values_map = metrics_values_level_map[DOCUMENT_LEVEL_VALUE]

        # for each document level metric
        for scorer_metric_identifier, metric_values in document_level_metrics_values_map.items():
            # for each document with a computed metric
            for search_result in search_results:
                # get the document id for the current search result
                document_id = search_result[DOCUMENT_ID_VALUE]

                # retrieve the metrics value for the document if
                value = metric_values[document_id]

                # get the metrics map for the document search result
                if not METRICS_VALUE in search_result:
                    search_result[METRICS_VALUE] = {}

                # retrieves the document metrics
                document_metrics = search_result[METRICS_VALUE]

                # set the current metric in the search result metrics
                document_metrics[scorer_metric_identifier] = value

        # retrieves the word level metrics
        word_level_metrics_values_map = metrics_values_level_map[WORD_LEVEL_VALUE]

        # for each word level metric
        for scorer_metric_identifier, metric_values in word_level_metrics_values_map.items():

            for search_result in search_results:
                # get the document id for the current search result
                document_id = search_result[DOCUMENT_ID_VALUE]

                # get the document hits
                document_hits = search_result[HITS_VALUE]

                # for each word in the document hits
                for word_id, word_information_map in document_hits.items():
                    # retrieve the metrics value
                    value = metric_values[word_id]

                    # store the word level metric in the search result
                    if not METRICS_VALUE in word_information_map:
                        word_information_map[METRICS_VALUE] = {}

                    word_metrics = word_information_map[METRICS_VALUE]
                    word_metrics[scorer_metric_identifier] = value

        # retrieves the word document level metrics
        word_document_level_metrics_values_map = metrics_values_level_map[WORD_DOCUMENT_LEVEL_VALUE]

        # for each word document level metric
        for scorer_metric_identifier, metric_values in word_document_level_metrics_values_map.items():

            for search_result in search_results:
                # get the document id for the current search result
                document_id = search_result[DOCUMENT_ID_VALUE]

                # get the document hits
                document_hits = search_result[HITS_VALUE]

                document_metrics_values = metric_values[document_id]

                # for each word in the document hits
                for word_id, word_information_map in document_hits.items():
                    # retrieve the metrics value
                    value = document_metrics_values[word_id]

                    # store the word level metric in the search result
                    if not METRICS_VALUE in word_information_map:
                        word_information_map[METRICS_VALUE] = {}
                    word_document_metrics = word_information_map[METRICS_VALUE]
                    word_document_metrics[scorer_metric_identifier] = value

        # retrieves the hit level metrics
        hit_level_metrics_values_map = metrics_values_level_map[HIT_LEVEL_VALUE]

        # for each hit level metric
        for scorer_metric_identifier, metric_values in hit_level_metrics_values_map.items():

            for search_result in search_results:
                # get the document id for the current search result
                document_id = search_result[DOCUMENT_ID_VALUE]

                # get the document hits
                document_hits = search_result[HITS_VALUE]

                # get the hit level metrics for the current document
                document_metrics_values = metric_values[document_id]

                # for each word in the document hits
                for word_id, word_information_map in document_hits.items():
                    # get the word document hits
                    word_document_hits = word_information_map[HITS_VALUE]

                    # get the hit level metrics for the current document and current word
                    document_word_metrics_values = document_metrics_values[word_id]

                    # for each hit
                    for hit_id, hit_information_map in word_document_hits.items():
                        # retrieve the metrics value
                        value = document_word_metrics_values[hit_id]

                        # store the hit level metric in the search result
                        if not METRICS_VALUE in hit_information_map:
                            hit_information_map[METRICS_VALUE] = {}
                        hit_metrics = hit_information_map[METRICS_VALUE]
                        hit_metrics[scorer_metric_identifier] = value

        # returns the success status
        return True
