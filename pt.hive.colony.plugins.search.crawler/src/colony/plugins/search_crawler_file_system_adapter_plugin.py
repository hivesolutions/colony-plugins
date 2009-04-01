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
import colony.plugins.decorators

class SearchCrawlerFileSystemAdapterPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search Crawler File System Adapter plugin.
    """

    id = "pt.hive.colony.plugins.search.crawler.file_system_adapter"
    name = "Search Crawler File System Adapter Plugin"
    short_name = "Search Crawler File System Adapter"
    description = "Search Crawler File System Adapter Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["search_crawler_adapter.file_system"]
    capabilities_allowed = ["search_provider.file_system"]
    dependencies = []
    events_handled = []
    events_registrable = []

    search_crawler_file_system_adapter = None

    search_provider_file_system_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search_crawler
        import search_crawler.file_system_adapter.search_crawler_file_system_adapter_system
        self.search_crawler_file_system_adapter = search_crawler.file_system_adapter.search_crawler_file_system_adapter_system.SearchCrawlerFileSystemAdapter(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.search.crawler.file_system_adapter", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.search.crawler.file_system_adapter", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_type(self):
        return self.search_crawler_file_system_adapter.get_type()

    def get_tokens(self, properties):
        return self.search_crawler_file_system_adapter.get_tokens(properties)

    @colony.plugins.decorators.load_allowed_capability("search_provider.file_system")
    def search_provider_file_system_load_allowed(self, plugin, capability):
        self.search_provider_file_system_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("search_provider.file_system")
    def search_provider_file_system_unload_allowed(self, plugin, capability):
        self.search_provider_file_system_plugins.remove(plugin)
