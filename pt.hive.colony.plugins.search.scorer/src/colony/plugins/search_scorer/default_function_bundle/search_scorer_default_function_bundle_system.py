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

WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER = "word_document_frequency_scorer_metric"
""" The identifier for the word document frequency metric """

TERM_FREQUENCY_SCORER_FUNCTION_IDENTIFIER = "term_frequency_scorer_function"
""" The term frequency function identifier """

WORD_FREQUENCY_SCORER_FUNCTION_IDENTIFIER = "word_frequency_scorer_function"
""" The word frequency function identifier """

DOCUMENT_LOCATION_SCORER_FUNCTION_IDENTIFIER = "document_location_scorer_function"
""" The document location function identifier """

WORD_DISTANCE_SCORER_FUNCTION_IDENTIFIER = "word_distance_scorer_function"
""" The word distance function identifier """

FREQUENCY_LOCATION_DISTANCE_FUNCTION_IDENTIFIER = "frequency_location_distance_scorer_function"
""" The frequency location distance function identifier """

METRICS_VALUE = "metrics"
""" The key to retrieve the hits at an arbitrary index level """

HITS_VALUE = "hits"
""" The key to retrieve the hits at an arbitrary index level """

ASCENDING_SORT_ORDER = "ascending"
""" The sort order for functions which score the top results with the lower values """

POSITION_VALUE = "position"
""" The key to retrieve the position from the hit information map """

FREQUENCY_LOCATION_DISTANCE_FUNCTION_PARAMETERS_VALUE = "frequency_location_distance_scorer_function_parameters"
""" The key to retrieve the parameters for the frequency location distance function from the properties map """

DEFAULT_FREQUENCY_LOCATION_DISTANCE_FUNCTION_PARAMETERS = {
    WORD_FREQUENCY_SCORER_FUNCTION_IDENTIFIER: 1.0,
    DOCUMENT_LOCATION_SCORER_FUNCTION_IDENTIFIER: 1.0,
    WORD_DISTANCE_SCORER_FUNCTION_IDENTIFIER: 1.0
}
""" The default parameters for the frequency location distance function """

ASCENDING_SORT_ORDER = "ascending"
""" The ascending sort order value """

DESCENDING_SORT_ORDER = "descending"
""" The descending sort order value """

DEFAULT_SORT_ORDER = DESCENDING_SORT_ORDER
""" The default sort order is descending: assumes higher scores should come first """

MINIMUM_PRECISION = 0.000001
""" The reference threshold for the normalization function: to avoid division by zero """

class SearchScorerDefaultFunctionBundle:
    """
    The search scorer default function bundle class.
    """

    search_scorer_default_function_bundle_plugin = None
    """ The search scorer default function bundle plugin """

    functions_map = None

    def __init__(self, search_scorer_default_function_bundle_plugin):
        """
        Constructor of the class.

        @type search_scorer_default_formula_bundle_plugin: SearchScorerDefaultFormulaBundlePlugin
        @param search_scorer_default_formula_bundle_plugin: The search scorer default formula bundle plugin.
        """

        # initializes the functions dictionary
        self.functions_map = {}

        # retrieves the function bundle plugin
        self.search_scorer_default_function_bundle_plugin = search_scorer_default_function_bundle_plugin

    def init_bundle(self):
        """
        Instantiates the functions and places them on the functions map
        """

        # retrieves the scorer function repository
        search_scorer_function_repository_plugin = self.search_scorer_default_function_bundle_plugin.search_scorer_function_repository_plugin

        # creates a new TermFrequencyFunction instance, to insert in the default functions map
        term_frequency_scorer_function = TermFrequencyFunction(search_scorer_function_repository_plugin)
        self.functions_map[TERM_FREQUENCY_SCORER_FUNCTION_IDENTIFIER] = term_frequency_scorer_function

        # creates a new WordFrequencyFunction instance, to insert in the default functions map
        word_frequency_scorer_function = WordFrequencyFunction(search_scorer_function_repository_plugin)
        self.functions_map[WORD_FREQUENCY_SCORER_FUNCTION_IDENTIFIER] = word_frequency_scorer_function

        # creates a new DocumentLocationFunction instance, to insert in the default functions map
        document_location_scorer_function = DocumentLocationFunction(search_scorer_function_repository_plugin)
        self.functions_map[DOCUMENT_LOCATION_SCORER_FUNCTION_IDENTIFIER] = document_location_scorer_function

        # creates a new WordDistance instance, to insert in the default functions map
        word_distance_scorer_function = WordDistanceFunction(search_scorer_function_repository_plugin)
        self.functions_map[WORD_DISTANCE_SCORER_FUNCTION_IDENTIFIER] = word_distance_scorer_function

        # creates a new FrequencyLocationDistanceFunction instance, to insert in the default functions map
        frequency_location_distance_scorer_function = FrequencyLocationDistanceFunction(search_scorer_function_repository_plugin)
        self.functions_map[FREQUENCY_LOCATION_DISTANCE_FUNCTION_IDENTIFIER] = frequency_location_distance_scorer_function

    def get_functions_map(self):
        """
        Retrieves a map with the available functions map

        @rtype: Dictionary
        @return: The map of functions provided by the bundle.
        """

        return self.functions_map

class DefaultBundleFunction:
    """
    The base class for function classes in the bundle.
    """

    required_metrics_identifiers = []
    """ The list of metrics required by the function computation """

    required_functions_identifiers = []
    """ The list of sub-functions required by the function computation """

    search_scorer_function_repository_plugin = None
    """ The function repository plugin used to obtain other functions """

    sort_order = "none"
    """ The sort order to use in the sorter """

    def __init__(self, search_scorer_function_repository_plugin):
        """
        Constructor for search scorer function objects.

        @type search_scorer_function_repository_plugin: SearchScorerFunctionRepositoryPlugin
        @param search_scorer_function_repository_plugin: The function repository plugin used to obtain other functions.
        """

        self.search_scorer_function_repository_plugin = search_scorer_function_repository_plugin

        # default behavior on scorer functions, is to give higher scores to better results
        self.sort_order = DEFAULT_SORT_ORDER

    def get_required_metrics_identifiers(self):
        """
        Retrieves the list of required metrics for the function computation.

        @rtype: List
        @return: the list of metrics identifiers required for the function computation.
        """

        return self.required_metrics_identifiers

    def get_required_functions_identifiers(self):
        """
        Retrieves the list of identifiers of the required sub-functions for the function computation.

        @rtype: List
        @return: the list of identifiers for the sub-functions required for the function computation.
        """

        return self.required_functions_identifiers

    def normalize(self, computed_values, properties):
        """
        The normalization function to assure that the results from each scoring function is comparable and combinable.
        The function range is narrowed to 0..1, where 1 is the score of the best result.

        @type computed_values: List
        @param computed_values: The list of computed scores for a set of search results.
        @type properties: Dictionary
        @param properties: The properties to configure the scoring function behavior.
        @rtype: List
        @return: The list of normalized scores for the given search results.
        """

        # smaller is better
        if self.sort_order == ASCENDING_SORT_ORDER:
            # get the best result
            minimum_score = min(computed_values)

            # normalize the results in relation to the best result
            normalized_values = [float(minimum_score) / max(MINIMUM_PRECISION, computed_value) for computed_value in computed_values]
        # larger is better
        else:
            # get the best result
            maximum_score = max(computed_values)

            # avoid division by zero
            if maximum_score == 0:
                maximum_score = MINIMUM_PRECISION

            # normalize the results in relation to the best result
            normalized_values = [float(computed_value)/maximum_score for computed_value in computed_values]

        return normalized_values

class TermFrequencyFunction(DefaultBundleFunction):
    """
    This function scores each result according to the average frequency of the query words that brought up the result.
    Does not depend on any metrics.
    """

    def compute(self, search_results, properties):

        # the list of computed values for each search result
        computed_values = []

        for search_result in search_results:
            # for each search result, compute the average word frequency in each document for the words in the query
            search_result_hits = search_result[HITS_VALUE]

            average_word_frequency = 0
            word_count = 0
            for word_id in search_result_hits:
                # retrieves the word information map for the current word
                word_information_map = search_result_hits[word_id]

                # retrieves the hits for the word
                hits = word_information_map[HITS_VALUE]

                # updates the word count
                word_count += 1

                # counts the hits
                number_hits = len(hits)

                # updates the average word frequency
                average_word_frequency = ((average_word_frequency * (word_count - 1)) + number_hits) / word_count

            # store the computed average frequency as the computed value for the current search result
            computed_values.append(average_word_frequency)

        # normalize the results
        normalized_values = self.normalize(computed_values, properties)

        return normalized_values

class WordFrequencyFunction(DefaultBundleFunction):
    """
    This function scores each result according to the average frequency of the query words that brought up the result.
    Leverages the WordDocumentFrequencyMetric in the default metric bundle.
    """

    def __init__(self, search_scorer_function_repository_plugin):
        """
        Constructor of the class.

        @type search_scorer_function_repository_plugin: SearchScorerDefaultFormulaBundlePlugin
        @param search_scorer_function_repository_plugin: The search scorer default formula bundle plugin.
        """

        # call the parent class constructor
        DefaultBundleFunction.__init__(self, search_scorer_function_repository_plugin)

        # initialize the required metrics list for the function object
        self.required_metrics_identifiers = [
            WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER
        ]

    def compute(self, search_results, properties):
        # the list of computed values for each search result
        computed_values = []

        for search_result in search_results:
            # for each search result, compute the average word frequency in each document for the words in the query
            search_result_hits = search_result[HITS_VALUE]

            # initializes the average word frequency
            average_word_frequency = 0

            # initializes the word count
            word_count = 0

            # for each word in the query
            for word_id in search_result_hits:
                # retrieves the word information map for the current word
                word_information_map = search_result_hits[word_id]

                # retrieves the word level metrics
                word_metrics = word_information_map[METRICS_VALUE]

                # retrieves the word frequency in the document
                word_document_frequency = word_metrics[WORD_DOCUMENT_FREQUENCY_SCORER_METRIC_IDENTIFIER]

                # updates the word count
                word_count += 1

                # updates the average word frequency
                average_word_frequency = ((average_word_frequency * (word_count - 1)) + word_document_frequency) / word_count

            # store the computed average frequency as the computed value for the current search result
            computed_values.append(average_word_frequency)

        # normalize the results
        normalized_values = self.normalize(computed_values, properties)

        return normalized_values

class DocumentLocationFunction(DefaultBundleFunction):
    """
    This function scores each result according to the average location in the document.
    """

    def __init__(self, search_scorer_function_repository_plugin):
        """
        Constructor of the class.

        @type search_scorer_function_repository_plugin: SearchScorerDefaultFormulaBundlePlugin
        @param search_scorer_function_repository_plugin: The search scorer default formula bundle plugin.
        """

        # call the parent class constructor
        DefaultBundleFunction.__init__(self, search_scorer_function_repository_plugin)

        # set the specific sort order for the current function: a lower average location means a better result.
        self.sort_order = ASCENDING_SORT_ORDER

    def compute(self, search_results, properties):
        # the list of computed values for each search result
        computed_values = []

        for search_result in search_results:
            # for each search result, compute the average word frequency in each document for the words in the query
            search_result_hits = search_result[HITS_VALUE]

            # initializes the average documentation location
            average_document_location = 0

            # initializes the word count
            word_count = 0

            # for each word in the query
            for word_id in search_result_hits:
                # retrieves the word information map for the word
                word_information_map = search_result_hits[word_id]

                # retrieves the hits for the word
                word_hits = word_information_map[HITS_VALUE]

                # retrieves the first hit
                first_word_hit = word_hits[0]

                # retrieves the location of the first hit
                word_document_location = first_word_hit[POSITION_VALUE]

                # updates the word count
                word_count += 1

                # updates the average
                average_document_location = ((average_document_location * (word_count - 1)) + word_document_location) / word_count

            # store the computed average frequency as the computed value for the current search result
            computed_values.append(average_document_location)

        # normalize the results
        normalized_values = self.normalize(computed_values, properties)

        return normalized_values

class WordDistanceFunction(DefaultBundleFunction):
    """
    This function scores each result according to the average distance between the words in the query in each document.
    """

    def __init__(self, search_scorer_function_repository_plugin):
        """
        Constructor of the class.

        @type search_scorer_function_repository_plugin: SearchScorerDefaultFormulaBundlePlugin
        @param search_scorer_function_repository_plugin: The search scorer default formula bundle plugin.
        """

        # call the parent class constructor
        DefaultBundleFunction.__init__(self, search_scorer_function_repository_plugin)

        # set the specific sort order for the current function: a lower average distance means a better result.
        self.sort_order = ASCENDING_SORT_ORDER

    def compute(self, search_results, properties):

        # the list of computed values for each search result
        computed_values = []

        for search_result in search_results:
            # for each search result, compute the average word frequency in each document for the words in the query
            search_result_hits = search_result[HITS_VALUE]

            average_word_distance = 0
            pivot_hit_count = 0

            search_result_hits_items = search_result_hits.items()

            # pick a the first word to use as pivot for the distance computation
            _pivot_word_id, pivot_word_information_map = search_result_hits_items[0]
            pivot_word_hits = pivot_word_information_map[HITS_VALUE]

            # get the remaining words to compare with the pivot
            other_search_result_hits_items = search_result_hits_items[1:]

            # for each hit of the pivot word, compare against all the other query word hits
            for pivot_hit_information_map in pivot_word_hits:
                # retrieve the pivot hit position to compare
                pivot_hit_position = pivot_hit_information_map[POSITION_VALUE]

                # the list of distances from the pivot to the closest hit of every other query word
                pivot_hit_distances = []

                # for each remaining query word, get the closest hit distance
                for word_id, word_information_map in other_search_result_hits_items:
                    # don't compare the pivot word hits with each other
                    if word_id == pivot_word_hits:
                        continue

                    # retrieve the closest hit distance for the current word
                    minimum_distance = None
                    word_hits = word_information_map[HITS_VALUE]
                    for hit_information_map in word_hits:
                        # get the hit position
                        hit_position = hit_information_map[POSITION_VALUE]

                        # compute the distance from the pivot hit to the current hit
                        distance = abs(pivot_hit_position - hit_position)

                        # if the current distance is the minimum distance or the first comparison
                        if distance < minimum_distance or not minimum_distance:
                            minimum_distance = distance

                    # append the computed minimum distance to the pivot hit distances list
                    pivot_hit_distances.append(minimum_distance)

                # sum the hit distances together to represent the overall word distance for the first hit
                pivot_hit_distances_sum = sum(pivot_hit_distances)

                # update the average word distance with the sum of distance for the current pivot hit
                average_word_distance = ((average_word_distance * pivot_hit_count) + pivot_hit_distances_sum) / (pivot_hit_count + 1)
                pivot_hit_count += 1

            # store the computed average frequency as the computed value for the current search result
            computed_values.append(average_word_distance)

        # normalize the results
        normalized_values = self.normalize(computed_values, properties)

        return normalized_values

class FrequencyLocationDistanceFunction(DefaultBundleFunction):
    """
    This function scores each result according to the average frequency of the query words that brought up the result.
    Leverages the WordDocumentFrequencyMetric in the default metric bundle.
    """

    def __init__(self, search_scorer_function_repository_plugin):
        """
        Constructor of the class.

        @type search_scorer_function_repository_plugin: SearchScorerDefaultFormulaBundlePlugin
        @param search_scorer_function_repository_plugin: The search scorer default formula bundle plugin.
        """

        # calls the parent class constructor
        DefaultBundleFunction.__init__(self, search_scorer_function_repository_plugin)

        # initializes the required functions list for the function object
        self.required_functions_identifiers = [
            WORD_FREQUENCY_SCORER_FUNCTION_IDENTIFIER,
            DOCUMENT_LOCATION_SCORER_FUNCTION_IDENTIFIER,
            WORD_DISTANCE_SCORER_FUNCTION_IDENTIFIER
        ]

        # initializes the required metrics
        self.required_metrics_identifiers = []

    def get_required_metrics_identifiers(self):
        """
        Retrieves the identifiers of the required metrics for the function and its sub-functions.
        """

        self.required_metrics_identifiers = []

        for function_identifier in self.required_functions_identifiers:
            # gets each sub-function from the repository
            function = self.search_scorer_function_repository_plugin.get_function(function_identifier)

            # adds the metric identifier to the metric identifier list
            function_required_metrics_identifiers = function.required_metrics_identifiers
            self.required_metrics_identifiers.extend(function_required_metrics_identifiers)

        # removes duplicate metrics identifiers
        required_metrics_identifiers_set = set(self.required_metrics_identifiers)
        self.required_metrics_identifiers = list(required_metrics_identifiers_set)

        return self.required_metrics_identifiers

    def compute(self, search_results, properties):

        # retrieves the function computation parameters from the properties, or uses default values
        if not FREQUENCY_LOCATION_DISTANCE_FUNCTION_PARAMETERS_VALUE in properties:
            function_parameters = DEFAULT_FREQUENCY_LOCATION_DISTANCE_FUNCTION_PARAMETERS
        else:
            function_parameters = properties[FREQUENCY_LOCATION_DISTANCE_FUNCTION_PARAMETERS_VALUE]

            # sets the default parameters for all the parameters missing from the properties
            for function_identifier in self.required_functions_identifiers:
                if not function_identifier in function_parameters:
                    function_parameters[function_identifier] = DEFAULT_FREQUENCY_LOCATION_DISTANCE_FUNCTION_PARAMETERS[function_identifier]

        # retrieves the required functions from the repository
        required_functions = {}
        for function_identifier in self.required_functions_identifiers:
            # adds the function with the current identifier
            function = self.search_scorer_function_repository_plugin.get_function(function_identifier)
            required_functions[function_identifier] = function

        # the list of computed values for each search result
        computed_values = []

        # the map of computed values for each sub-function
        # each position in the map holds a list of computed values, one for each search result
        required_computed_values = {}

        # computes the score using each required function
        for function_identifier, function in required_functions.items():
            required_computed_values[function_identifier] = function.compute(search_results, properties)

        # compute the function score for all the search results
        for search_result_index in range(len(search_results)):

            total_weighted_value = 0
            # combines the scores of all the required functions to compute the final result
            for function_identifier in required_functions:
                # gets the computed value of the function for the current search result
                value = required_computed_values[function_identifier][search_result_index]

                # adds-in the weight for the function
                weighted_value = value * function_parameters[function_identifier]

                # adds the weighted value for the function
                total_weighted_value += weighted_value

            computed_values.append(total_weighted_value)

        # normalizes the results
        normalized_values = self.normalize(computed_values, properties)

        return normalized_values
