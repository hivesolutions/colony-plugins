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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class SearchScorerMetricRepositoryPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Search Scorer Metric Repository Plugin.
    """

    id = "pt.hive.colony.plugins.search.scorer.metric_repository"
    name = "Search Scorer Metric Repository Plugin"
    short_name = "Search Scorer Metric Repository"
    description = "Plugin that provides directory services to discover available metric types for scoring purposes"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/search_scorer/metric_repository/resources/baf.xml"
    }
    capabilities = [
        "search_scorer_metric_repository",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "search_scorer_metric_bundle"
    ]
    main_modules = [
        "search_scorer.metric_repository.search_scorer_metric_repository_exceptions",
        "search_scorer.metric_repository.search_scorer_metric_repository_system"
    ]

    search_scorer_metric_repository = None
    """ The search scorer metric repository """

    search_scorer_metric_bundle_plugins = []
    """ The search scorer metric bundle plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global search_scorer
        import search_scorer.metric_repository.search_scorer_metric_repository_system
        self.search_scorer_metric_repository = search_scorer.metric_repository.search_scorer_metric_repository_system.SearchScorerMetricRepository(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.search.scorer.metric_repository", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.search.scorer.metric_repository", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_metric_identifiers(self):
        return self.search_scorer_metric_repository.get_metric_identifiers()

    def get_metric(self, scorer_metric_identifier):
        return self.search_scorer_metric_repository.get_metric(scorer_metric_identifier)

    def get_metrics(self, scorer_metric_identifier_list):
        return self.search_scorer_metric_repository.get_metrics(scorer_metric_identifier_list)

    @colony.base.decorators.load_allowed_capability("search_scorer_metric_bundle")
    def search_scorer_metric_bundle_load_allowed(self, plugin, capability):
        # adds the plugin to the search scorer metric bundle plugins list
        self.search_scorer_metric_bundle_plugins.append(plugin)

        # retrieves the plugin metrics map
        plugin_metrics_map = plugin.get_metrics_map()

        # adds the plugin metrics
        self.search_scorer_metric_repository.add_search_scorer_metrics_map(plugin_metrics_map)

    @colony.base.decorators.unload_allowed_capability("search_scorer_metric_bundle")
    def search_scorer_metric_bundle_unload_allowed(self, plugin, capability):
        # removes the plugin from the search scorer metric bundle plugins list
        self.search_scorer_metric_bundle_plugins.remove(plugin)

        # retrieves the plugin metrics map
        plugin_metrics_map = plugin.get_metrics_map()

        # removes the plugin metrics
        self.search_scorer_metric_repository.remove_search_scorer_metrics_map(plugin_metrics_map)
