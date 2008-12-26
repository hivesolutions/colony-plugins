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

import search_scorer_default_metric_bundle_exceptions
import colony.plugins.search_scorer.metric_repository.search_scorer_metric_repository_system

TERM_FREQUENCY_METRIC_IDENTIFIER = "term_frequency_metric"
""" The term frequency metric identifier """

METRICS_MAP_VALUE = "metrics_map"

TERM_LIST_VALUE = "terms_list"

HIT_LIST_VALUE = "hit_list"
""" The key to retrieves the hit list value from a search result map """

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

        # retrieves the search scorer default function bundle plugin
        self.search_scorer_default_function_bundle_plugin = search_scorer_default_metric_bundle_plugin

        metrics_map = {}

        term_frequency_scorer_metric = TermFrequencyScorerMetric()
        metrics_map[TERM_FREQUENCY_SCORER_FUNCTION_IDENTIFIER] = term_frequency_scorer_metric 

    def get_metrics_map(self):
        """
        Retrieves a map with the available metrics map
        
        @rtype: Dictionary
        @return: The map of metrics provided by the bundle.
        """

        return self.metrics_map


class TermFrequencyMetric(colony.plugins.search_scorer.metric_repository.search_scorer_metric_repository_system.SearchScorerMetric):

    def __init__(self, search_scorer_metric_repository):
        """
        Constructor of the class.
        
        @type search_scorer_metric_repository_plugin: SearchScorerDefaultMetricBundlePlugin
        @param search_scorer_metric_repository_plugin: The search scorer default metric bundle plugin.
        """

        # call the parent class constructor
        SearchScorerMetric = colony.plugins.search_scorer.metric_repository.search_scorer_metric_repository_system.SearchScorerMetric
        SearchScorerMetric.__init__(search_scorer_metric_repository)
        
        # initialize the required metrics list for the metric object
        required_metrics_identifiers = [TERM_FREQUENCY_METRIC_IDENTIFIER]

    def compute_for_results(self, search_results, search_index, properties):
        metric_values = []
        for search_result in search_results:
            hit_list = search_result[HIT_LIST_VALUE]
            count = len(hit_list)
            metric_values.append(count)
        return metric_values

    def compute_for_index(self, search_index, properties):
        pass