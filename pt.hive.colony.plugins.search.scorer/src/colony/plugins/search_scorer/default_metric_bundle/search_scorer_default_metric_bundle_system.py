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

TERM_FREQUENCY_SCORER_METRIC_IDENTIFIER = "term_frequency_scorer_metric"
""" The term frequency metric identifier """

DOCUMENT_HITS_SCORER_METRIC_IDENTIFIER = "document_hits_scorer_metric"
""" The identifier for the document hits metric """

WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER = "word_document_frequency_scorer_metric"
""" The identifier for the word document frequency metric """

HIT_DISTANCE_TO_TOP_SCORER_METRIC_IDENTIFIER = "hit_distance_to_top_scorer_metric"
""" The identifier for the hit distance to top scorer metric """

WORD_LEVEL = "word_level"
""" The word-wide scorer metric level """

DOCUMENT_LEVEL = "document_level"
""" The document scorer metric level """

WORD_DOCUMENT_LEVEL = "word_document_level"
""" The word document scorer metric level """

HIT_LEVEL = "hit_level"
""" The hit scorer metric level """

DOCUMENT_ID_VALUE = "document_id"
""" The key that retrieves the document id from the search result map"""

HITS_VALUE = "hits"
""" The key that retrieves the set of results, contained in an arbitrary index level """

METRICS_VALUE = "metrics"
""" The key that retrieves the metrics map, contained in an arbitrary index level """

POSITION_VALUE = "position"
""" The key that retrieves the hit position, in the hit information map """

class SearchScorerDefaultMetricBundle:
    """
    The search scorer default metric bundle class.
    """

    search_scorer_default_metric_bundle_plugin = None
    """ The search scorer default metric bundle plugin """

    metrics_map = None
    """ The map of metrics provided by the bundle. """

    def __init__(self, search_scorer_default_metric_bundle_plugin):
        """
        Constructor of the class.

        @type search_scorer_default_metric_bundle_plugin: SearchScorerDefaultMetricBundlePlugin
        @param search_scorer_default_metric_bundle_plugin: The search scorer default metric bundle plugin.
        """

        # retrieves the search scorer default metric bundle plugin
        self.search_scorer_default_metric_bundle_plugin = search_scorer_default_metric_bundle_plugin

        # initializes the metrics map that will keep the bundle's metrics
        self.metrics_map = {}

        # retrieves the search scorer metric repository plugin
        self.search_scorer_default_metric_bundle_plugin = search_scorer_default_metric_bundle_plugin.get_search_scorer_metric_repository_plugin()

        term_frequency_scorer_metric = TermFrequencyScorerMetric()
        self.metrics_map[TERM_FREQUENCY_SCORER_METRIC_IDENTIFIER] = term_frequency_scorer_metric

        word_document_frequency_scorer_metric = WordDocumentFrequencyScorerMetric()
        self.metrics_map[WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER] = word_document_frequency_scorer_metric

        document_hits_scorer_metric = DocumentHitsScorerMetric()
        self.metrics_map[DOCUMENT_HITS_SCORER_METRIC_IDENTIFIER] = document_hits_scorer_metric

        hit_distance_to_top_metric = HitDistanceToTopScorerMetric()
        self.metrics_map[HIT_DISTANCE_TO_TOP_SCORER_METRIC_IDENTIFIER] = hit_distance_to_top_metric

    def get_metrics_map(self):
        """
        Retrieves a map with the available metrics map

        @rtype: Dictionary
        @return: The map of metrics provided by the bundle.
        """

        return self.metrics_map

class DefaultBundleMetric:
    """
    The base class for all the metrics in the bundle.
    """

    identifier = "none"
    """ The identifier for the metric """

    level = "none"
    """ The index level for which the metric is computed """

    def get_identifier(self):
        """
        Returns the identifier for the current scorer metric.

        @rtype: String
        @return: Returns the scorer metric identifier.
        """

        return self.identifier

    def get_level(self):
        """
        Returns the index level at which to store the current metric.

        @rtype: String
        @return: Returns the index level for the metric.
        """

        return self.level

    def compute(self, search_results, search_index, properties):
        """
        The main entry point for the metric object. Method that implements the metric computation for a set of search results.
        This method is reserved for query time execution.

        @type search_results: List
        @param search_results: The list of search results to score using the metric.
        @type search_index: SearchIndex
        @param search_index: The index where the results were obtained.
        @type properties: Dictionary
        @param properties: The properties to configure the scoring metric behavior.
        @rtype: List
        @return: A list of metric values, one for each search result.
        """

        pass

    def compute_for_index(self, search_index, properties):
        """
        The main entry point for the metric object. Method that implements the metric computation for a search index.
        This method is required for pre-calculated metrics to allow index time computation.

        @type search_index: SearchIndex
        @param search_index: The index to analyze obtained.
        @type properties: Dictionary
        @param properties: The properties to configure the scoring metric behavior.
        @rtype: List
        @return: A list of metric values, one for each search result.
        """

        pass

class TermFrequencyScorerMetric(DefaultBundleMetric):

    def __init__(self):
        """
        Constructor of the class.

        @type search_scorer_metric_repository_plugin: SearchScorerDefaultMetricBundlePlugin
        @param search_scorer_metric_repository_plugin: The search scorer default metric bundle plugin.
        """

        # sets the identifier for the scorer metric
        self.identifier = TERM_FREQUENCY_SCORER_METRIC_IDENTIFIER

        # sets the metric level to word level
        self.level = WORD_LEVEL

    def compute(self, search_results, search_index, properties):
        # the metric values
        metric_values = {}

        # check if the metric has been computed for the specified index
        if TERM_FREQUENCY_SCORER_METRIC_IDENTIFIER in search_index.metrics and search_index.metrics[TERM_FREQUENCY_SCORER_METRIC_IDENTIFIER]:
            # retrieves the inverted index map
            inverted_index_map = search_index.inverted_index_map

            # gather the relevant metrics for the search results from the index
            for search_result in search_results:
                # get the document hits in the search result, to retrieve all the hit words
                document_hits = search_result[HITS_VALUE]

                # loops over all the document hit words, getting the word level metric from the index
                for word_id, word_information_map in document_hits.items():
                    word_information_map = inverted_index_map[word_id]
                    word_metrics = word_information_map[METRICS_VALUE]
                    term_frequency = word_metrics[TERM_FREQUENCY_SCORER_METRIC_IDENTIFIER]
                    # TODO: stop setting the metric value for the same word id several times
                    metric_values[word_id] = term_frequency
        else:
            # compute the metric
            metric_values = self.compute_for_index(search_index, properties)

        return metric_values

    def compute_for_index(self, search_index, properties):
        # the metric_values
        metric_values = {}

        # retrieves the inverted index map from the index
        inverted_index_map = search_index.inverted_index_map

        # for each word in the index
        for word_id, word_information_map in inverted_index_map.items():
            # retrieves the hit list for the current word
            word_hit_list = word_information_map[HITS_VALUE]

            # initializes the count for the current word
            count = 0

            # count the word's hits, in each document where it appears
            for _document_id, word_document_information_map in word_hit_list.items():
                # retrieves the hit list for the word document information map
                word_document_hit_list = word_document_information_map[HITS_VALUE]

                # updates the count with the number of hits
                count += len(word_document_hit_list)

            # increment the count for the word, with the count from all the documents
            metric_values[word_id] = count

        # returns a map with the count for each word id
        return metric_values

class DocumentHitsScorerMetric(DefaultBundleMetric):
    """
    The document level metric that considers the number of hits in the size.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        # sets the identifier for the scorer metric
        self.identifier = DOCUMENT_HITS_SCORER_METRIC_IDENTIFIER

        # sets the metric level to document level
        self.level = DOCUMENT_LEVEL

    def compute(self, search_results, search_index, properties):
        # the metric values
        metric_values = {}

        # check if the metric has been computed for the specified index
        if DOCUMENT_HITS_SCORER_METRIC_IDENTIFIER in search_index.metrics and search_index.metrics[DOCUMENT_HITS_SCORER_METRIC_IDENTIFIER]:
            # gather the relevant metrics for the search results from the search results
            for search_result in search_results:
                # get the document id
                document_id = search_result[DOCUMENT_ID_VALUE]

                # retrieve the document metrics
                document_metrics = search_result[METRICS_VALUE]

                # retrieve the document hits metric
                document_hits_scorer_metric = document_metrics[DOCUMENT_HITS_SCORER_METRIC_IDENTIFIER]

                # add the metric value to the return list
                metric_values[document_id] = document_hits_scorer_metric
        else:
            # compute the metric
            metric_values = self.compute_for_index(search_index, properties)

        return metric_values


    def compute_for_index(self, search_index, properties):
        # the metric_values
        metric_values = {}

        # retrieves the forward index map from the index
        forward_index_map = search_index.forward_index_map

        # for each document in the index
        for document_id, document_information_map in forward_index_map.items():

            document_hits = document_information_map[HITS_VALUE]

            # for each word in the document
            document_hit_count = 0
            for _word_id, word_information_map in document_hits.items():

                document_word_hits = word_information_map[HITS_VALUE]

                # add the hits from the word to the overall document hits
                document_hit_count += len(document_word_hits)

            # set the hit count for the current document
            if document_id not in metric_values:
                metric_values[document_id] = {}
            metric_values[document_id] = document_hit_count

        # returns a map with the count for each word id
        return metric_values

class WordDocumentFrequencyScorerMetric(DefaultBundleMetric):
    """
    The word-document level metric that considers the frequency of a word within a given document.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        # sets the identifier for the scorer metric
        self.identifier = WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER

        # sets the metric level to word document level
        self.level = WORD_DOCUMENT_LEVEL

    def compute(self, search_results, search_index, properties):
        # the metrics values
        metric_values = {}

        # checks if the metric has been computed for the specified index
        if WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER in search_index.metrics and search_index.metrics[WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER]:
            # retrieves the forward index map
            forward_index_map = search_index.forward_index_map

            # gathers the relevant metrics for the search results from the index
            for search_result in search_results:
                document_id = search_result[DOCUMENT_ID_VALUE]
                document_hits = search_result[HITS_VALUE]
                for word_id in document_hits:
                    word_metrics = forward_index_map[document_id][HITS_VALUE][word_id][METRICS_VALUE]
                    term_frequency = word_metrics[WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER]

                    if document_id not in metric_values:
                        metric_values[document_id] = {}
                    metric_values[document_id][word_id] = term_frequency
        else:
            # the list of relevant document ids to calculate the metric for
            document_id_list = []

            # gathers the document ids of the search results
            for search_result in search_results:
                document_id = search_result[DOCUMENT_ID_VALUE]
                document_id_list.append(document_id)

            # computes the metric only for the relevant search results
            metric_values = self.compute_for_document_ids(search_index, document_id_list, properties)

        return metric_values

    def compute_for_index(self, search_index, properties):
        # the metric_values
        metric_values = {}

        # retrieves the inverted index map from the index
        inverted_index_map = search_index.inverted_index_map

        # for each word in the index
        for word_id, word_information_map in inverted_index_map.items():

            word_hits = word_information_map[HITS_VALUE]

            # for each document in which the word appears
            for document_id, word_document_information_map in word_hits.items():

                word_document_hits = word_document_information_map[HITS_VALUE]

                # count the word's hits, in each document where it appears
                count = len(word_document_hits)

                # increment the count for the word, with the count from all the documents
                if document_id not in metric_values:
                    metric_values[document_id] = {}
                metric_values[document_id][word_id] = count

        # returns a map with the count for each word id
        return metric_values

    def compute_for_document_ids(self, search_index, document_id_list, properties):
        # the metric_values
        metric_values = {}

        # retrieves the inverted index map from the index
        inverted_index_map = search_index.inverted_index_map

        # for each word in the index
        for word_id, word_information_map in inverted_index_map.items():

            word_hits = word_information_map[HITS_VALUE]

            # for each document in which the word appears

            for document_id in document_id_list:
                if document_id in word_hits:
                    word_document_information_map = word_hits[document_id]

                    word_document_hits = word_document_information_map[HITS_VALUE]

                    # count the word's hits, in each document where it appears
                    count = len(word_document_hits)

                    # increment the count for the word, with the count from all the documents
                    if document_id not in metric_values:
                        metric_values[document_id] = {}
                    metric_values[document_id][word_id] = count

        # returns a map with the count for each word id
        return metric_values

class HitDistanceToTopScorerMetric(DefaultBundleMetric):
    """
    The hit level metric that considers the distance of a particular hit to the beginning of the document.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        # sets the identifier for the scorer metric
        self.identifier = HIT_DISTANCE_TO_TOP_SCORER_METRIC_IDENTIFIER

        # sets the metric level to hit level
        self.level = HIT_LEVEL

    def compute(self, search_results, search_index, properties):
        # the metric values
        metric_values = {}

        # check if the metric has been computed for the specified index
        if self.identifier in search_index.metrics and search_index.metrics[self.identifier]:
            # retrieves the forward index map
            forward_index_map = search_index.forward_index_map

            # gather the relevant metrics for the search results from the index
            for search_result in search_results:
                document_id = search_result[DOCUMENT_ID_VALUE]
                document_hits = search_result[HITS_VALUE]
                for word_id, word_information_map in document_hits.items():
                    word_hits = word_information_map[HITS_VALUE]
                    for hit_id in word_hits:
                        hit_metrics = forward_index_map[document_id][HITS_VALUE][word_id][HITS_VALUE][hit_id][METRICS_VALUE]
                        hit_distance_to_top = hit_metrics[self.identifier]
                        metric_values[document_id][word_id][hit_id] = hit_distance_to_top
        else:
            # compute the metric
            metric_values = self.compute_for_index(search_index, properties)

        return metric_values

    def compute_for_index(self, search_index, properties):
        # the metric_values
        metric_values = {}

        # retrieves the inverted index map from the index
        inverted_index_map = search_index.inverted_index_map

        # for each word in the index
        for word_id, word_information_map in inverted_index_map.items():

            word_hits = word_information_map[HITS_VALUE]

            # for each document in which the word appears
            for document_id, word_document_information_map in word_hits.items():

                word_document_hits = word_document_information_map[HITS_VALUE]

                for hit_index in range(len(word_document_hits)):
                    # retrieves the hit information map for the hit at hit index
                    hit_information_map = word_document_hits[hit_index]

                    # computes the metric value, considering the hit position
                    metric_value = hit_information_map[POSITION_VALUE]

                    # sets the metric value in the metric values return structure
                    if document_id not in metric_values:
                        metric_values[document_id] = {}
                    if word_id not in metric_values[document_id]:
                        metric_values[document_id][word_id] = {}
                    metric_values[document_id][word_id][hit_index] = metric_value

        # returns a map with the count for each hit index
        return metric_values
