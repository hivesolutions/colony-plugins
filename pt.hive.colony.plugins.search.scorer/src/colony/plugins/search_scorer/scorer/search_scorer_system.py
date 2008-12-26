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

SCORER_FUNCTION_IDENTIFIER_VALUE = "scoring_function_identifier"
""" The identifier for the main scoring function in the scorer function repository """  

INDEX_TIME_METRIC_TYPE = "index_time"
""" The identifier for the index time metric type """ 

SEARCH_TIME_METRIC_TYPE = "search_time"
""" The identifier for the search time metric type """ 

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

        # determines top level scoring function according to properties
        if not SCORER_FUNCTION_IDENTIFIER_VALUE in properties:
            raise search_scorer_exceptions.MissingProperty(SCORER_FUNCTION_IDENTIFIER_VALUE)
        
        scorer_function_identifier = properties[SCORER_FUNCTION_IDENTIFIER_VALUE]
        
        # retrieves the top level scorer function
        scorer_function = search_scorer_function_repository_plugin.get_function(scorer_function_identifier)

        # gets the metrics required by the scorer function
        required_metrics_identifiers_list = scorer_function.get_required_metrics_identifiers()

        # retrieves the required metrics from the metrics repository
        scorer_metrics = search_scorer_metrics_repository_plugin.get_metrics(required_metrics_identifiers_list)
    
        # computes all the required metrics, for all the search results 
        for scorer_metric in scorer_metrics:           
            # computes the search time metric required by the function
            scorer_metric.calculate_metric_for_results(search_results, search_index, properties)

        # computes the top level function using the gathered metrics and the coefficients specified in the properties map
        search_results_scores = scorer_function.calculate(search_results, properties)
        
        # sets the search result scores in the existing search results metadata
        # (decouples function computation from search result structure details)

        # returns a list of scores for each search result
        return scored_search_results
