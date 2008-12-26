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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Lu�s Martinho <lmartinho@hive.pt>"
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

SCORE_VALUE = "score"
""" The key to retrieve the score from the search result map """

class SearchSorter:
    """
    The search sorter class.
    """

    search_sorter_plugin = None
    """ The search sorter plugin """

    def __init__(self, search_sorter_plugin):
        """
        Constructor of the class.
        
        @type search_sorter_plugin: SearchSorterPlugin
        @param search_sorter_plugin: The search sorter plugin.
        """

        self.search_sorter_plugin = search_sorter_plugin

    def sort_results(self, search_results, properties):
        """
        Sorts result sets according to previously computed scores.
        
        @type search_results: List
        @param search_results: The list of search results
        @rtype: List
        @return: A list made up of the search results sorted according to score.
        """

        # build a list of SortableSearchResult's from the original scored_search_results list
        sortable_search_result_list = [SortableSearchResult(search_result, search_result[SCORE_VALUE]) for search_result in search_results]

        # the wrapping class is used to leverage list sorting
        sortable_search_result_list.sort()

        # the list should be sorted in reverse order (the top ranking results first) 
        sortable_search_result_list.reverse()

        # unwrap the search results from the SortableSearchResult objects
        sorted_search_results = [sortable_search_result.search_result for sortable_search_result in sortable_search_result_list]

        return sorted_search_results

class SortableSearchResult:
    """
    The sortable search result class.
    """

    search_result = None
    """ The search result object """

    score = 0
    """ The search result score """

    def __init__(self, search_result, score):
        self.search_result = search_result
        self.score = score
 
    def __cmp__(self, other):
        # retrieves the other position
        other_score = other.score

        # compares both positions
        return self.score - other_score
