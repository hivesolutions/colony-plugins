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

import colony.base.decorators
import colony.base.plugin_system

class SearchQueryEvaluatorPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Search Query Evaluator plugin.
    """

    id = "pt.hive.colony.plugins.search.query_evaluator"
    name = "Search Query Evaluator Plugin"
    short_name = "Search Query Evaluator"
    description = "Plugin that provides query evaluation services, using an available index"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/search_query_evaluator/query_evaluator/resources/baf.xml"
    }
    capabilities = [
        "search_query_evaluator",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "search_query_evaluator_adapter"
    ]
    main_modules = [
        "search_query_evaluator.query_evaluator.search_query_evaluator_exceptions",
        "search_query_evaluator.query_evaluator.search_query_evaluator_system"
    ]

    search_query_evaluator = None
    """ The search query evaluator """

    search_query_evaluator_adapter_plugins = []
    """ The search query evaluator adapter plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import search_query_evaluator.query_evaluator.search_query_evaluator_system
        self.search_query_evaluator = search_query_evaluator.query_evaluator.search_query_evaluator_system.SearchQueryEvaluator(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def evaluate_query(self, search_index, query, properties):
        return self.search_query_evaluator.evaluate_query(search_index, query, properties)

    def get_search_query_evaluator_adapter_types(self):
        return self.search_query_evaluator.get_search_query_evaluator_adapter_types()

    @colony.base.decorators.load_allowed_capability("search_query_evaluator_adapter")
    def search_query_evaluator_adapter_load_allowed(self, plugin, capability):
        self.search_query_evaluator_adapter_plugins.append(plugin)
        self.search_query_evaluator.add_search_query_evaluator_adapter_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("search_query_evaluator_adapter")
    def search_query_evaluator_adapter_unload_allowed(self, plugin, capability):
        self.search_query_evaluator_adapter_plugins.remove(plugin)
        self.search_query_evaluator.remove_search_query_evaluator_adapter_plugin(plugin)
