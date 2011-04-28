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

import colony.base.plugin_system

class SearchIndexerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Search Indexer plugin.
    """

    id = "pt.hive.colony.plugins.search.indexer"
    name = "Search Indexer Plugin"
    short_name = "Search Indexer"
    description = "Search Indexer Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/search_indexer/indexer/resources/baf.xml"
    }
    capabilities = [
        "search_indexer",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "search_scorer_metric_repository"
    ]
    main_modules = [
        "search_indexer.indexer.search_indexer_exceptions",
        "search_indexer.indexer.search_indexer_system"
    ]

    search_indexer = None
    """ The search indexer """

    search_scorer_metric_repository_plugins = []
    """ The search scorer metric repository plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global search_indexer
        import search_indexer.indexer.search_indexer_system
        self.search_indexer = search_indexer.indexer.search_indexer_system.SearchIndexer(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.search.indexer", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.search.indexer", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_index(self, tokens_list, properties):
        return self.search_indexer.create_index(tokens_list, properties)

    @colony.base.decorators.load_allowed_capability("search_scorer_metric_repository")
    def search_scorer_metric_repository_load_allowed(self, plugin, capability):
        self.search_scorer_metric_repository_plugins.append(plugin)
