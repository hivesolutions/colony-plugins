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

SCORER_FORMULA_TYPE_VALUE = "search_scorer_formula_type"
""" The score formula type value for the properties map """

SCORE_INFORMATION_MAP_VALUE = "score_information_map"
""" The key for the search result map, that retrieves the score information map,  """

SCORE_VALUE = "score"
""" The key for the score information map, that retrieves the score value """

import search_scorer_exceptions

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

    def get_formula_types(self):
        """
        Returns the available search scorer formula types.
        
        @rtype: List
        @return: Available search scorer formula types list.
        """

        # the return value
        formula_types = []

        # retrieves the available formula plugins
        search_scorer_formula_bundle_plugins = self.search_scorer_plugin.search_scorer_formula_bundle_plugins

        for search_scorer_formula_bundle_plugin in search_scorer_formula_bundle_plugins:
            search_scorer_formula_bundle_plugin_formula_types = search_scorer_formula_bundle_plugin.get_formula_types()
            formula_types.append(search_scorer_formula_bundle_plugin_formula_types)

        return formula_types 

    def score_search_results(self, search_index, search_results, properties):
        """
        The method to start the search scorer.
        
        @type search_results: List
        @param search_results: The list of (document id, search result) tuples determined by query evaluation.
        @type search_index: SearchIndex
        @param search_index: The search index used to perform the search.
        @type properties: Dictionary
        @param properties: The map of properties for the result scoring.
        @rtype: List
        @return: The scored result set as a list of (document id, scored search result) tuples.
        """

        # in case the score formula type value is not defined in the properties raises an exception
        if not SCORER_FORMULA_TYPE_VALUE in properties:
            raise search_scorer_exceptions.MissingProperty(SCORER_FORMULA_TYPE_VALUE)

        # retrieves the type of formula
        search_scorer_formula_type = properties[SCORER_FORMULA_TYPE_VALUE]

        # retrieves the available formula plugins
        search_scorer_formula_bundle_plugins = self.search_scorer_plugin.search_scorer_formula_bundle_plugins

        # the formula plugin used to compute the overall score
        formula_bundle_plugin = None

        # retrieves the first formula plugin which provides the intended formula type
        for search_scorer_formula_bundle_plugin in search_scorer_formula_bundle_plugins:
            # retrieves the formula types provided by the current formula plugin
            search_scorer_formula_bundle_plugin_formula_types = search_scorer_formula_bundle_plugin.get_formula_types()

            # if the current formula plugin provides the intended formula type, choose the current plugin
            # as the score computation strategy
            if search_scorer_formula_type in search_scorer_formula_bundle_plugin_formula_types:
                formula_bundle_plugin = search_scorer_formula_bundle_plugin
                break

        if not formula_bundle_plugin:
            raise search_scorer_exceptions.MissingSearchScorerFormulaBundlePlugin(search_scorer_formula_type)

        # scores each of the search results
        for document_id, search_result in search_results:
            # computes the formula output for the current search result 
            search_result_score_value = formula_bundle_plugin.calculate_value(document_id, search_result, search_index, search_scorer_formula_type, properties)

            # inserts a score information map, (containing scoring information: score, formula type, etc.)
            # in the search result map (containing information about the search result: hits, etc.)
            search_result[SCORE_INFORMATION_MAP_VALUE] = {SCORE_VALUE: search_result_score_value, SCORER_FORMULA_TYPE_VALUE: search_scorer_formula_type}

        # returns the sorted search results
        return search_results

    def sort_scored_results(self, scored_search_results, properties):
        """
        Sorts result sets according to previously computed scores in the data structure.
        
        @type scored_search_results: Dictionary
        @param scored_search_results: The map of search results determined by query evaluation.
        @type properties: Dictionary
        @param properties: The map of properties for the result scoring.
        @rtype: List
        @return: A list made up of the search results sorted according to score.
        """

        # build a list of SortableSearchResult's from the original scored_search_results list
        sortable_search_result_list = [SortableSearchResult(document_id, scored_search_result) for document_id, scored_search_result in scored_search_results]

        # the wrapping class is used to leverage list sorting
        sortable_search_result_list.sort()
        
        # the list should be sorted in reverse order (the top ranking results first) 
        sortable_search_result_list.reverse()

        return sortable_search_result_list

class SortableSearchResult:
    """
    The sortable search result class.
    """

    document_id = "none"
    """ The document id """

    search_result = {}
    """ The scored search result map """

    score = 0
    """ The score """

    def __init__(self, document_id, search_result):
        self.document_id = document_id
        self.search_result = search_result

        score_information_map = search_result[SCORE_INFORMATION_MAP_VALUE]
        self.score = score_information_map[SCORE_VALUE]
 
    def __cmp__(self, other):
        # retrieves the other position
        other_score = other.score

        # compares both positions
        return self.score - other_score
