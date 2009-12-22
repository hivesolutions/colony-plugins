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
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.crawler", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.interpreter", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.indexer", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.index_repository", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.index_persistence", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.query_evaluator", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.scorer", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.scorer.function_repository", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search.sorter", "1.0.0")]

    events_handled = []
    events_registrable = []
    main_modules = ["search.search_system", "search.search_exceptions", "search.search_test"]

    search = None

    search_crawler_plugin = None
    search_interpreter_plugin = None
    search_indexer_plugin = None
    search_index_repository_plugin = None
    search_index_persistence_plugin = None
    search_query_evaluator_plugin = None
    search_scorer_plugin = None
    search_scorer_function_repository_plugin = None
    search_sorter_plugin = None

    search_test = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search
        import search.search_system
        import search.search_test
        self.search = search.search_system.Search(self)
        self.search_test = search.search_test.SearchTest(self)

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

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.search", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_index(self, properties):
        return self.search.create_index(properties)

    def create_index_with_identifier(self, search_index_identifier, properties):
        return self.search.create_index_with_identifier(search_index_identifier, properties)

    def remove_index_with_identifier(self, search_index_identifier, properties):
        return self.search.remove_index_with_identifier(search_index_identifier, properties)

    def persist_index(self, search_index, properties):
        return self.search.persist_index(search_index, properties)

    def persist_index_with_identifier(self, search_index_identifier, properties):
        return self.search.persist_index_with_identifier(search_index_identifier, properties)

    def load_index(self, properties):
        return self.search.load_index(properties)

    def load_index_with_identifier(self, search_index_identifier, properties):
        return self.search.load_index_with_identifier(search_index_identifier, properties)

    def query_index(self, search_index, search_query, properties):
        return self.search.query_index(search_index, search_query, properties)

    def query_index_by_identifier(self, search_index_identifier, search_query, properties):
        return self.query_index_by_identifier(search_index_identifier, search_query, properties)

    def search_index(self, search_index, search_query, properties):
        return self.search.search_index(search_index, search_query, properties)

    def search_index_by_identifier(self, search_index_identifier, search_query, properties):
        return self.search.search_index_by_identifier(search_index_identifier, search_query, properties)

    def get_index_by_identifier(self, search_index_identifier):
        return self.search.get_index_by_identifier(search_index_identifier)

    def get_index_identifiers(self):
        return self.search.get_index_identifiers()

    def get_index_metadata(self, search_index_identifier):
        return self.search.get_index_metadata(search_index_identifier)

    def get_indexes_metadata(self):
        return self.search.get_indexes_metadata()

    def get_search_crawler_adapter_types(self):
        return self.search.get_search_crawler_adapter_types()

    def get_search_index_persistence_adapter_types(self):
        return self.search.get_search_index_persistence_adapter_types()

    def get_plugin_test_case_bundle(self):
        return self.search_test.get_plugin_test_case_bundle()

    def get_search_crawler_plugin(self):
        return self.search_crawler_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.crawler")
    def set_search_crawler_plugin(self, search_crawler_plugin):
        self.search_crawler_plugin = search_crawler_plugin

    def get_search_interpreter_plugin(self):
        return self.search_interpreter_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.interpreter")
    def set_search_interpreter_plugin(self, search_interpreter_plugin):
        self.search_interpreter_plugin = search_interpreter_plugin

    def get_search_indexer_plugin(self):
        return self.search_indexer_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.indexer")
    def set_search_indexer_plugin(self, search_indexer_plugin):
        self.search_indexer_plugin = search_indexer_plugin

    def get_search_index_repository_plugin(self):
        return self.search_index_repository_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.index_repository")
    def set_search_index_repository_plugin(self, search_index_repository_plugin):
        self.search_index_repository_plugin = search_index_repository_plugin

    def get_search_scorer_plugin(self):
        return self.search_scorer_plugin

    def get_search_index_persistence_plugin(self):
        return self.search_index_persistence_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.index_persistence")
    def set_search_index_persistence_plugin(self, search_index_persistence_plugin):
        self.search_index_persistence_plugin = search_index_persistence_plugin

    def get_search_query_evaluator_plugin(self):
        return self.search_query_evaluator_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.query_evaluator")
    def set_search_query_evaluator_plugin(self, search_query_evaluator_plugin):
        self.search_query_evaluator_plugin = search_query_evaluator_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.scorer")
    def set_search_scorer_plugin(self, search_scorer_plugin):
        self.search_scorer_plugin = search_scorer_plugin

    def get_search_scorer_function_repository_plugin(self):
        return self.search_scorer_function_repository_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.scorer.function_repository")
    def set_search_scorer_function_repository_plugin(self, search_scorer_function_repository_plugin):
        self.search_scorer_function_repository_plugin = search_scorer_function_repository_plugin

    def get_search_sorter_plugin(self):
        return self.search_sorter_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search.sorter")
    def set_search_sorter_plugin(self, search_sorter_plugin):
        self.search_sorter_plugin = search_sorter_plugin
