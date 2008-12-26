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

import search_scorer_default_function_bundle_exceptions
import search_scorer.function_repository.search_scorer_function_repository_system

TERM_FREQUENCY_METRIC_IDENTIFIER = "term_frequency_metric"
""" The term frequency metric identifier """

METRICS_VALUE = "metrics"

TERM_LIST_VALUE = "terms_list"

TERM_FREQUENCY_SCORER_FUNCTION_IDENTIFIER = "term_frequency_function"
""" The term frequency function identifier """

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

        # retrieves the scorer function repository
        search_scorer_function_repository_plugin = search_scorer_default_function_bundle_plugin.search_scorer_function_repository_plugin

        # creates a new TermFrequencyFunction instance, to insert in the default functions map
        term_frequency_scorer_function = TermFrequencyFunction(search_scorer_function_repository_plugin)
        self.functions_map[TERM_FREQUENCY_SCORER_FUNCTION_IDENTIFIER] = term_frequency_scorer_function 

    def get_functions_map(self):
        """
        Retrieves a map with the available functions map
        
        @rtype: Dictionary
        @return: The map of functions provided by the bundle.
        """

        return self.functions_map


class TermFrequencyFunction(search_scorer.function_repository.search_scorer_function_repository_system.SearchScorerFunction):

    def __init__(self, search_scorer_function_repository_plugin):
        """
        Constructor of the class.
        
        @type search_scorer_function_repository_plugin: SearchScorerDefaultFormulaBundlePlugin
        @param search_scorer_function_repository_plugin: The search scorer default formula bundle plugin.
        """

        # call the parent class constructor
        SearchScorerFunction = search_scorer.function_repository.search_scorer_function_repository_system.SearchScorerFunction
        SearchScorerFunction.__init__(self, search_scorer_function_repository_plugin)
        
        # initialize the required metrics list for the function object
        required_metrics_identifiers = [TERM_FREQUENCY_METRIC_IDENTIFIER]

    def compute(self, search_results, properties):

        # the list of computed values for each search result
        computed_values = []

        for search_result in search_results:
            term_frequency_metric = search_result[METRICS_VALUE][TERM_FREQUENCY_METRIC_IDENTIFIER]
            computed_values.append(term_frequency_metric)

        return computed_values
