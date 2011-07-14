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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
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

import search_scorer_metric_repository_exceptions

class SearchScorerMetricRepository:
    """
    The search scorer metric repository.
    """

    search_scorer_metric_repository_plugin = None
    """ The search scorer metric repository plugin """

    metrics_map = {}
    """ The map of metrics instances currently injected in the repository """

    def __init__(self, search_scorer_metric_repository_plugin):
        """
        Constructor of the class.

        @type search_scorer_metric_repository_plugin: SearchScorerMetricRepositoryPlugin
        @param search_scorer_metric_repository_plugin: The search scorer metric repository plugin.
        """

        self.search_scorer_metric_repository_plugin = search_scorer_metric_repository_plugin

    def add_search_scorer_metrics_map(self, scorer_metrics_map):
        """
        Adds a set of metrics to the repository.

        @type scorer_metrics_map: Dictionary
        @param scorer_metrics_map: A dictionary with the metrics to be inserted into the repository.
        """

        # adds each metric to the repository metric map
        for metric_identifier, metric in scorer_metrics_map.items():

            # checks for duplicates insertion
            if metric_identifier in self.metrics_map:
                raise search_scorer_metric_repository_exceptions.SearchScorerMetricRepositoryException(metric_identifier)

            self.metrics_map[metric_identifier] = metric

    def remove_search_scorer_metrics_map(self, scorer_metrics_map):
        """
        Adds a set of metrics from the repository.

        @type scorer_metrics_map: Dictionary
        @param scorer_metrics_map: A dictionary with the metrics to be deleted from the repository.
        """

        # removes all the metrics made available by the plugin
        # (since no duplicates are allowed, the plugin is assumed to be the single provider of the metric)
        for metric_identifier in scorer_metrics_map:
            del self.metrics_map[metric_identifier]

    def get_metric_identifiers(self):
        """
        Retrieves the list of metric identifiers registered in the repository.

        @rtype: List
        @return: The list of metric identifiers in the repository.
        """

        return self.metrics_map.keys()

    def get_metric(self, scorer_metric_identifier):
        """
        Retrieves the metric instance for the provided metric identifier

        @type scorer_metric_identifier: String
        @param scorer_metric_identifier: The identifier for the intended metric.
        @rtype: SearchScorerMetric
        @return: The metric instance for the provided metric identifier.
        """
        if not scorer_metric_identifier in self.metrics_map:
            raise search_scorer_metric_repository_exceptions.InvalidMetricRequested(scorer_metric_identifier)

        return self.metrics_map[scorer_metric_identifier]

    def get_metrics(self, scorer_metric_identifier_list):
        """
        Retrieves the metric instance for the provided metric identifier

        @type scorer_metric_identifier: String
        @param scorer_metric_identifier: The identifier for the intended metric.
        @rtype: SearchScorerMetric
        @return: The metric instance for the provided metric identifier.
        """

        metrics = []

        for scorer_metric_identifier in scorer_metric_identifier_list:
            metrics.append(self.get_metric(scorer_metric_identifier))

        return metrics
