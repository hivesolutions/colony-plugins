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

import time

import search_indexer_exceptions

DOCUMENT_ID_VALUE = "document_id"
""" The key that retrieves the document id """

HITS_VALUE = "hits"
""" The key that retrieves the set of results, contained in an arbitrary index level """

METRICS_IDENTIFIERS_VALUE = "metrics_identifiers"
""" The key that retrieves the metrics identifiers from the parameters map """

DOCUMENT_LEVEL_VALUE = "document_level"
""" The key that retrieves the metrics values from the document level metrics """

WORD_LEVEL_VALUE = "word_level"
""" The key that retrieves the metrics values from the word level metrics """

WORD_DOCUMENT_LEVEL_VALUE = "word_document_level"
""" The key that retrieves the metrics values from the word document level metrics """

HIT_LEVEL_VALUE = "hit_level"
""" The key that retrieves the metrics values from the hit level metrics """

METRICS_VALUE = "metrics"
""" The key that retrieves the computed metrics at an arbitrary index level """

INDEX_SIZE_VALUE = "index_size"
""" The key that retrieves the index size from the statistics map """

DOCUMENT_COUNT_VALUE = "document_count"
""" The key that retrieves the document count from the statistics map """

class SearchIndexer:
    """
    The search indexer class.
    """

    search_indexer_plugin = None
    """ The search indexer plugin """

    def __init__(self, search_indexer_plugin):
        """
        Constructor of the class.

        @type search_indexer_plugin: SearchIndexerPlugin
        @param search_indexer_plugin: The search indexer plugin.
        """

        self.search_indexer_plugin = search_indexer_plugin

    def create_index(self, token_list, properties):
        """
        Abstract factory method for index products.

        @type token_list: List
        @param token_list: The list of tokens for the index creation.
        @type properties: Dictionary
        @param properties: The map of properties for the index creation.
        @rtype: SearchIndex
        @return: The created index.
        """

        metrics_identifiers = []
        # checks for metrics specified in the properties map
        if METRICS_IDENTIFIERS_VALUE in properties:
            metrics_identifiers = properties[METRICS_IDENTIFIERS_VALUE]

        # retrieves the metrics from the metrics repository plugin
        scorer_metrics = self.get_metrics(metrics_identifiers)

        start_time = time.time()

        # creates the forward index map
        forward_index_map = self.create_forward_index(token_list, properties)

        end_time = time.time()
        forward_index_creation_duration = end_time - start_time
        self.search_indexer_plugin.debug("Build forward index finished in %f s" % forward_index_creation_duration)

        start_time = time.time()

        # creates the inverted index map
        inverted_index_map = self.create_inverted_index(forward_index_map, properties)

        end_time = time.time()
        inverted_index_creation_duration = end_time - start_time
        self.search_indexer_plugin.debug("Build inverted index finished in %f s" % inverted_index_creation_duration)

        # creates the search index object
        search_index = SearchIndex()

        # sets the forward index map
        search_index.forward_index_map = forward_index_map

        # sets the inverted index map
        search_index.inverted_index_map = inverted_index_map

        start_time = time.time()

        # computes the specified metrics for the index
        if scorer_metrics:
            # the metrics for the search index are calculated in place, adding to the index metadata
            self.compute_metrics(scorer_metrics, search_index, properties)

        end_time = time.time()
        metrics_computation_duration = end_time - start_time
        self.search_indexer_plugin.debug("Metrics computation finished in %f s" % metrics_computation_duration)

        # calculates the index statistics
        search_index.calculate_statistics()

        # stores the durations in the index metadata
        search_index.statistics["forward_index_creation_duration"] = forward_index_creation_duration
        search_index.statistics["inverted_index_creation_duration"] = inverted_index_creation_duration
        search_index.statistics["metrics_computation_duration"] = metrics_computation_duration

        # returns the search index object
        return search_index

    def create_forward_index(self, token_list, properties):
        """
        Creates the forward index map, using the tokens list
        and the given properties.

        @type token_list: List
        @param token_list: The list of tokens.
        @type properties: Dictionary
        @param properties: The properties.
        @rtype: Dictionary
        @return: The forward index map.
        """

        # initialize the forward index data structure
        forward_index_map = {}

        # iterate through each document's token list
        for document_token_list in token_list:

            words_list, words_metadata_list, document_information_map = document_token_list

            document_id = document_information_map["document_id"]

            # initialize the document's word map, containing the list of hits for each word
            word_map = {}

            # the document information map holds all the document's metadata along with the word map with each word's hits in the document
            document_information_map[HITS_VALUE] = word_map

            # iterate through all word occurrences to generate the word_map
            length_words_list = len(words_list)
            for index in range(length_words_list):
                word = words_list[index]
                word_metadata = words_metadata_list[index]

                # the word hit structure holds the word metadata of the specific occurrence
                hit = word_metadata

                # if this is the first time the word is being inserted
                if not word in word_map:
                    # initialize the word map at position word with an empty document_word_information_map
                    word_map[word] = {}
                document_word_information_map = word_map[word]

                # if this is the first time a hit for the word in the document is being inserted
                if not HITS_VALUE in document_word_information_map:
                    document_word_information_map[HITS_VALUE] = []
                document_word_hits = document_word_information_map[HITS_VALUE]

                # add the hit to the document word hits
                document_word_hits.append(hit)

            # place the document information map in the forward index map
            forward_index_map[document_id] = document_information_map

        return forward_index_map

    def create_inverted_index(self, forward_index_map, properties):
        """
        Creates the inverted index map, using the forward index map
        and the given properties.

        @type forward_index_map: Dictionary
        @param forward_index_map: The forward index map.
        @type properties: Dictionary
        @param properties: The properties.
        @rtype: Dictionary
        @return: The inverted index map.
        """

        inverted_index_map = {}

        for document_id, document_information_map in forward_index_map.items():
            word_map = document_information_map[HITS_VALUE]

            for word_id, document_word_information_map in word_map.items():
                if not word_id in inverted_index_map:
                    inverted_index_map[word_id] = {}
                word_information_map = inverted_index_map[word_id]

                if not HITS_VALUE in word_information_map:
                    word_information_map[HITS_VALUE] = {}
                word_hits = word_information_map[HITS_VALUE]

                word_hits[document_id] = document_word_information_map

        return inverted_index_map

    def compute_metrics(self, scorer_metrics, search_index, properties):
        """
        Computes the specified metrics for the specified search index.

        @type scorer_metrics: List
        @param scorer_metrics: The list of SearchScorerMetrics to apply to the index.
        @type search_index: SearchIndex
        @param search_index: The search index to add metric information. Will be modified by operation.
        @type properties: Dictionary
        @param properties: The properties map to configure the metrics computation.
        @rtype: bool
        @return: The success of the metric computation operation.
        """

        # the computed metrics values are gathered in a map, and then applied to the search index
        # decreasing coupling between the metrics computation and the index internal structure

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

        # computes each metric for the whole index
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
            metrics_values_map[scorer_metric_identifier] = scorer_metric.compute_for_index(search_index, properties)

        # applies each computed metric to the search index, by level

        # retrieves the document level metrics
        document_level_metrics_values_map = metrics_values_level_map[DOCUMENT_LEVEL_VALUE]

        # for each document level metric
        for scorer_metric_identifier, metric_values in document_level_metrics_values_map.items():
            # for each document with a computed metric
            for document_id, value in metric_values.items():
                # store the metric value in the index
                document_information_map = search_index.forward_index_map[document_id]

                # if this is the first document level metric for the current document
                if not METRICS_VALUE in document_information_map:
                    document_information_map[METRICS_VALUE] = {}
                document_metrics = document_information_map[METRICS_VALUE]

                document_metrics[scorer_metric_identifier] = value

            # update the index level metadata to show the current metric is available
            search_index.metrics[scorer_metric_identifier] = True

        # retrieves the word level metrics
        word_level_metrics_values_map = metrics_values_level_map[WORD_LEVEL_VALUE]

        # for each word level metric
        for scorer_metric_identifier, metric_values in word_level_metrics_values_map.items():
            # for each word with a computed metric
            for word_id, value in metric_values.items():
                # store the metric value in the index
                word_information_map = search_index.inverted_index_map[word_id]

                # if this is the first word level metric for the current word
                if not METRICS_VALUE in word_information_map:
                    word_information_map[METRICS_VALUE] = {}
                word_metrics = word_information_map[METRICS_VALUE]

                word_metrics[scorer_metric_identifier] = value

            # update the index level metadata to show the current metric is available
            search_index.metrics[scorer_metric_identifier] = True

        # retrieves the word document level metrics
        word_document_level_metrics_values_map = metrics_values_level_map[WORD_DOCUMENT_LEVEL_VALUE]

        # for each word document level metric
        for scorer_metric_identifier, metric_values in word_document_level_metrics_values_map.items():
            # for each document with a computed metric
            for document_id, word_map in metric_values.items():
                # for each word with a computed metric
                for word_id, value in word_map.items():
                    # store the metric value in the index
                    word_information_map = search_index.inverted_index_map[word_id]
                    word_hits = word_information_map[HITS_VALUE]
                    word_document_information_map = word_hits[document_id]

                    # if this is the first word document level metric for the current word document combination
                    if not METRICS_VALUE in word_document_information_map:
                        word_document_information_map[METRICS_VALUE] = {}
                    word_document_metrics = word_document_information_map[METRICS_VALUE]

                    word_document_metrics[scorer_metric_identifier] = value

            # update the index level metadata to show the current metric is available
            search_index.metrics[scorer_metric_identifier] = True

        # retrieves the hit level metrics
        hit_level_metrics_values_map = metrics_values_level_map[HIT_LEVEL_VALUE]

        # for each hit level metric
        for scorer_metric_identifier, metric_values in hit_level_metrics_values_map.items():
            # for each word with a computed metric
            for document_id, word_map in metric_values.items():
                # for each document with a computed metric
                for word_id, hit_map in word_map.items():

                    word_information_map = search_index.inverted_index_map[word_id]
                    word_hits = word_information_map[HITS_VALUE]

                    word_document_information_map = word_hits[document_id]
                    word_document_hits = word_document_information_map[HITS_VALUE]

                    # for each hit for the word in the document
                    for hit_index, value in hit_map.items():
                        # store the metric value in the index
                        hit_information_map = word_document_hits[hit_index]

                        # if this is the first hit level metric for the current hit
                        if not METRICS_VALUE in hit_information_map:
                            hit_information_map[METRICS_VALUE] = {}
                        hit_metrics = hit_information_map[METRICS_VALUE]

                        hit_metrics[scorer_metric_identifier] = value
            search_index.metrics[scorer_metric_identifier] = True

        # returns the success status
        return True

    def get_metrics(self, metrics_identifiers):
        """
        Retrieves the metrics for the specified identifiers from the metrics repository.
        """

        # retrieves the first search scorer metric repository from the search indexer plugin's repository list
        search_scorer_metric_repository_plugins = self.search_indexer_plugin.search_scorer_metric_repository_plugins
        search_scorer_metric_repository_plugin = search_scorer_metric_repository_plugins[0]

        # gets the identifiers of all the metrics available in the repository
        available_metrics_identifiers = search_scorer_metric_repository_plugin.get_metric_identifiers()

        # checks if all the requested metrics are available
        for metric_identifier in metrics_identifiers:
            if not metric_identifier in available_metrics_identifiers:
                raise search_indexer_exceptions.MissingMetric(metric_identifier)

        # retrieves the required metrics from the metrics repository
        scorer_metrics = search_scorer_metric_repository_plugin.get_metrics(metrics_identifiers)

        return scorer_metrics

class SearchIndex:
    """
    The search index class.
    """

    forward_index_map = {}
    """ The forward index map """

    inverted_index_map = {}
    """ The inverted index map """

    properties = {}
    """ The properties """

    metrics = {}
    """ The map of available metrics by identifier """

    statistics = {}
    """ The map with index statistics """

    def __init__(self):
        self.forward_index_map = {}
        self.inverted_index_map = {}
        self.properties = {}
        self.metrics = {}
        self.statistics = {}

    def calculate_statistics(self):
        """
        Returns a map with several index statistics.
        """

        # count the number of words indexed
        word_count = len(self.inverted_index_map.keys())
        self.statistics[INDEX_SIZE_VALUE] = word_count

        # count the number of documents indexed
        document_count = len(self.forward_index_map.keys())
        self.statistics[DOCUMENT_COUNT_VALUE] = document_count

        return self.statistics

    def get_metadata(self):
        # defines the metadata
        metadata = {
            "properties" : self.properties,
            "metrics" : self.metrics,
            "statistics": self.statistics
        }

        # returns the metadata
        return metadata

    def get_document_information_map_metadata(self, document_id):
        """
        Returns a dictionary containing the metadata for the specified document.
        The dictionary is obtained from the document information map, without the document id and the hits.
        """

        # initializes the document information map metadata dictionary
        document_information_map_metadata = {}

        # retrieves the document information for the current document
        document_information_map = self.forward_index_map[document_id]

        # gathers the document's metadata by removing the document id and hits values
        for document_information_map_key, document_information_map_value in document_information_map.items():
            if document_information_map_key not in [DOCUMENT_ID_VALUE, HITS_VALUE]:
                document_information_map_metadata[document_information_map_key] = document_information_map_value

        # returns the retrieved document information
        return document_information_map_metadata
