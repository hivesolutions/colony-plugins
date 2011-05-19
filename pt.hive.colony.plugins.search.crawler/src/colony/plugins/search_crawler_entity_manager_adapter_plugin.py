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
import colony.base.decorators

class SearchCrawlerEntityManagerAdapterPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Search Crawler Entity Manager Adapter plugin.
    """

    id = "pt.hive.colony.plugins.search.crawler.entity_manager_adapter"
    name = "Search Crawler Entity Manager Adapter Plugin"
    short_name = "Search Crawler Entity Manager Adapter"
    description = "Search Crawler Entity Manager Adapter Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/search_crawler/entity_manager_adapter/resources/baf.xml"
    }
    capabilities = [
        "search_crawler_adapter.entity_manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "search_provider.entity_manager"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.data.entity_manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.business.helper", "1.0.0")
    ]
    main_modules = [
        "search_crawler.entity_manager_adapter.search_crawler_entity_manager_adapter_exceptions",
        "search_crawler.entity_manager_adapter.search_crawler_entity_manager_adapter_system"
    ]

    search_crawler_entity_manager_adapter = None
    """ The search crawler entity manager adapter """

    search_provider_entity_manager_plugins = []
    """ The search provider entity manager plugins """

    entity_manager_plugin = None
    """ The entity manager plugin """

    business_helper_plugin = None
    """ The business helper plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import search_crawler.entity_manager_adapter.search_crawler_entity_manager_adapter_system
        self.search_crawler_entity_manager_adapter = search_crawler.entity_manager_adapter.search_crawler_entity_manager_adapter_system.SearchCrawlerEntityManagerAdapter(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.search.crawler.entity_manager_adapter", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.search.crawler.entity_manager_adapter", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.search.crawler.entity_manager_adapter", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_type(self):
        return self.search_crawler_entity_manager_adapter.get_type()

    def get_tokens(self, properties):
        return self.search_crawler_entity_manager_adapter.get_tokens(properties)

    @colony.base.decorators.load_allowed_capability("search_provider.entity_manager")
    def search_provider_entity_manager_load_allowed(self, plugin, capability):
        self.search_provider_entity_manager_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("search_provider.entity_manager")
    def search_provider_entity_manager_unload_allowed(self, plugin, capability):
        self.search_provider_entity_manager_plugins.remove(plugin)

    def get_entity_manager_plugin(self):
        return self.entity_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.data.entity_manager")
    def set_entity_manager_plugin(self, entity_manager_plugin):
        self.entity_manager_plugin = entity_manager_plugin

    def get_business_helper_plugin(self):
        return self.business_helper_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.business.helper")
    def set_business_helper_plugin(self, business_helper_plugin):
        self.business_helper_plugin = business_helper_plugin
