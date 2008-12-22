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
import colony.plugins.decorators

class SearchPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search plugin.
    """

    id = "pt.hive.colony.plugins.search"
    name = "Search Plugin"
    short_name = "Search"
    description = "Search Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["search", "plugin_test_case_bundle"]
    capabilities_allowed = ["search_crawler", "search_index_persistence", "search_query_evaluator", "search_scorer"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.interpreter", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.indexer", "1.0.0")]
    events_handled = []
    events_registrable = []

    search_system = None

    search_crawler_plugins = []
    search_index_persistence_plugins = []
    search_query_evaluator_plugins = []
    search_scorer_plugins = []

    search_interpreter_plugin = None
    search_indexer_plugin = None

    search_test = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search
        import search.search_system
        import search.search_test
        self.search_system = search.search_system.Search(self)
        self.search_test = search.search_test.SearchTest(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.search", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.search", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.search", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_index(self, properties):
        return self.search_system.create_index(properties)

    def persist_index(self, search_index, properties):
        return self.search_system.persist_index(search_index, properties)

    def load_index(self, properties):
        return self.search_system.load_index(properties)

    def query_index(self, search_index, search_query, properties):
        return self.search_system.query_index(search_index, search_query, properties)

    def query_index_sort_results(self, search_index, search_query, properties):
        return self.search_system.query_index_sort_results(search_index, search_query, properties)

    def get_plugin_test_case_bundle(self):
        return self.search_test.get_plugin_test_case_bundle()

    @colony.plugins.decorators.load_allowed_capability("search_crawler")
    def search_crawler_load_allowed(self, plugin, capability):
        self.search_crawler_plugins.append(plugin)

    @colony.plugins.decorators.load_allowed_capability("search_index_persistence")
    def search_persistence_load_allowed(self, plugin, capability):
        self.search_index_persistence_plugins.append(plugin)

    @colony.plugins.decorators.load_allowed_capability("search_query_evaluator")
    def search_query_evaluator_load_allowed(self, plugin, capability):
        self.search_query_evaluator_plugins.append(plugin)

    @colony.plugins.decorators.load_allowed_capability("search_scorer")
    def search_scorer_load_allowed(self, plugin, capability):
        self.search_scorer_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("search_crawler")
    def search_crawler_unload_allowed(self, plugin, capability):
        self.search_crawler_plugins.remove(plugin)

    @colony.plugins.decorators.unload_allowed_capability("search_index_persistence")
    def search_persistence_unload_allowed(self, plugin, capability):
        self.search_index_persistence_plugins.remove(plugin)

    def get_search_interpreter_plugin(self):
        return self.search_interpreter_plugin

    @colony.plugins.decorators.unload_allowed_capability("search_query_evaluator")
    def search_query_evaluator_unload_allowed(self, plugin, capability):
        self.search_query_evaluator_plugins.remove(plugin)

    @colony.plugins.decorators.unload_allowed_capability("search_scorer")
    def search_scorer_unload_allowed(self, plugin, capability):
        self.search_scorer_plugins.remove(plugin)

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.interpreter")
    def set_search_interpreter_plugin(self, search_interpreter_plugin):
        self.search_interpreter_plugin = search_interpreter_plugin

    def get_search_indexer_plugin(self):
        return self.search_indexer_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.indexer")
    def set_search_indexer_plugin(self, search_indexer_plugin):
        self.search_indexer_plugin = search_indexer_plugin
