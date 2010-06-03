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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class SearchScorerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search Scorer Plugin.
    """

    id = "pt.hive.colony.plugins.search.scorer"
    name = "Search Scorer Plugin"
    short_name = "Search Scorer"
    description = "Plugin that provides scoring services, for result sets"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/search_scorer/scorer/resources/baf.xml"}
    capabilities = ["search_scorer", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.scorer.function_repository", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.scorer.metric_repository", "1.0.0")]
    events_handled = []
    events_registrable = []

    search_scorer = None

    search_scorer_function_repository_plugin = None
    search_scorer_metric_repository_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search_scorer
        import search_scorer.scorer.search_scorer_system
        self.search_scorer = search_scorer.scorer.search_scorer_system.SearchScorer(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.search.scorer", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_function_identifiers(self):
        return self.search_scorer.get_function_identifiers()

    def score_results(self, search_results, search_index, properties):
        return self.search_scorer.score_results(search_results, search_index, properties)

    def get_search_scorer_function_repository_plugin(self):
        return self.search_scorer_function_repository_plugin

    def get_search_scorer_metric_repository_plugin(self):
        return self.search_scorer_metric_repository_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.scorer.function_repository")
    def set_search_scorer_function_repository_plugin(self, search_scorer_function_repository_plugin):
        self.search_scorer_function_repository_plugin = search_scorer_function_repository_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.scorer.metric_repository")
    def set_search_scorer_metric_repository_plugin(self, search_scorer_metric_repository_plugin):
        self.search_scorer_metric_repository_plugin = search_scorer_metric_repository_plugin
