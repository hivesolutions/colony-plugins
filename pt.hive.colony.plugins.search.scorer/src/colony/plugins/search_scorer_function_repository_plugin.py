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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class SearchScorerFunctionRepositoryPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search Scorer Function Repository Plugin.
    """

    id = "pt.hive.colony.plugins.search.scorer.function_repository"
    name = "Search Scorer Function Repository Plugin"
    short_name = "Search Scorer Function Repository"
    description = "Plugin that provides directory services to discover available function types for scoring purposes"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["search_scorer_function_repository"]
    capabilities_allowed = ["search_scorer_function_bundle"]
    dependencies = []
    events_handled = []
    events_registrable = []

    search_scorer_function_repository = None

    search_scorer_function_bundle_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search_scorer
        import search_scorer.function_repository.search_scorer_function_repository_system
        self.search_scorer_function_repository = search_scorer.function_repository.search_scorer_function_repository_system.SearchScorerFunctionRepository(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.search.scorer.function_repository", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.search.scorer.function_repository", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_function_identifiers(self):
        return self.search_scorer_function_repository.get_function_identifiers()

    def get_function(self, scorer_function_identifier):
        return self.search_scorer_function_repository.get_function(scorer_function_identifier)

    @colony.plugins.decorators.load_allowed_capability("search_scorer_function_bundle")
    def search_scorer_function_bundle_load_allowed(self, plugin, capability):
        self.search_scorer_function_bundle_plugins.append(plugin)

        plugin_functions_map = plugin.get_functions_map()
        self.search_scorer_function_repository.add_search_scorer_functions_map(plugin_functions_map)

    @colony.plugins.decorators.unload_allowed_capability("search_scorer_function_bundle")
    def search_scorer_function_bundle_unload_allowed(self, plugin, capability):
        self.search_scorer_function_bundle_plugins.remove(plugin)

        plugin_functions_map = plugin.get_functions_map()
        self.search_scorer_function_repository.remove_search_scorer_functions_map(plugin_functions_map)
