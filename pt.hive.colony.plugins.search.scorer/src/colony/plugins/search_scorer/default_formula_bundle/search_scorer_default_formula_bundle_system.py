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

TERM_FREQUENCY_FORMULA_TYPE = "term_frequency_formula_type"
""" The formula type for the term frequency formula """

TERM_FREQUENCY_INVERSE_DOCUMENT_FREQUENCY_FORMULA_TYPE = "term_frequency_inverse_document_frequency_formula_type"
""" The formula type for the term frequency-inverse document frequency formula """

HIT_LIST_VALUE = "hit_list"
""" The key for the search result dictionary that retrieves the search result hit list """

import search_scorer_default_formula_bundle_exceptions

class SearchScorerDefaultFormulaBundle:
    """
    The search interpreter class.
    """

    search_scorer_default_formula_bundle_plugin = None
    """ The search interpreter plugin """
    
    search_scorer_formula_types = [TERM_FREQUENCY_FORMULA_TYPE, TERM_FREQUENCY_INVERSE_DOCUMENT_FREQUENCY_FORMULA_TYPE]
    """ The formula types provided by the bundle """

    def __init__(self, search_scorer_default_formula_bundle_plugin):
        """
        Constructor of the class.
        
        @type search_scorer_default_formula_bundle_plugin: SearchScorerDefaultFormulaBundlePlugin
        @param search_scorer_default_formula_bundle_plugin: The search scorer default formula bundle plugin.
        """

        self.search_scorer_default_formula_bundle_plugin = search_scorer_default_formula_bundle_plugin

    def get_formula_types(self):
        """
        Retrieves the provided formula types of the bundle.
        
        @rtype: List
        @return: The list of formula types provided by the bundle
        """

        return self.search_scorer_formula_types

    def calculate_value(self, search_result, search_index, search_scorer_formula_type, properties):
        """
        Computes the value for the specified formula type.
        
        @type search_results: Dictionary
        @param search_results: The search result dictionary containing a hit list.
        @type search_index: SearchIndex
        @param search_index: The search index used in the search.
        @type search_scorer_formula_type: String
        @param search_scorer_formula_type: The formula type to be used in the value calculation.
        @type properties: Dictionary
        @param properties: The properties dictionary.
        @rtype: float
        @return: The computed value for the specified search result using the specified formula type.
        """

        if not search_scorer_formula_type in self.search_scorer_formula_types:
            raise search_scorer_default_formula_bundle_exceptions.InvalidFormulaType(search_scorer_formula_type)

        if search_scorer_formula_type == TERM_FREQUENCY_FORMULA_TYPE:
            calculated_value = self.calculate_term_frequency(search_result, search_index, properties)
        elif search_scorer_formula_type == TERM_FREQUENCY_INVERSE_DOCUMENT_FREQUENCY_FORMULA_TYPE:
            calculated_value = self.calculate_term_frequency_inverse_document_frequency(search_result, search_index, properties)

        return calculated_value

    def calculate_term_frequency(self, search_result, search_index, properties):
        """
        Compute the value for the score using the term frequency (tf) approach.
        
        @type search_results: Dictionary
        @param search_results: The search result dictionary containing a hit list.
        @type search_scorer_formula_type: String
        @type search_index: SearchIndex
        @param search_index: The search index used in the search.
        @param search_scorer_formula_type: The formula type to be used in the value calculation.
        @type properties: Dictionary
        @param properties: The properties dictionary.
        """

        # determines the size of the hit list
        search_result_hit_list = search_result[HIT_LIST_VALUE]
        search_result_hit_list_length = len(search_result_hit_list)

        # the score value is the number of hits for the query
        return search_result_hit_list_length

    def calculate_term_frequency_inverse_document_frequency(self, search_result, search_index, properties):
        """
        Compute the value for the score using the term frequency-inverse document frequency (tf-idf) approach.

        @type search_results: Dictionary
        @param search_results: The search result dictionary containing a hit list.
        @type search_index: SearchIndex
        @param search_index: The search index used in the search.
        @type search_scorer_formula_type: String
        @param search_scorer_formula_type: The formula type to be used in the value calculation.
        @type properties: Dictionary
        @param properties: The properties dictionary.
        """

        return 0
