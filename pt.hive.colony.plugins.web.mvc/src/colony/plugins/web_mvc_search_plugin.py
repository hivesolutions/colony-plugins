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

class WebMvcSearchPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Web Mvc Search plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.search"
    name = "Web Mvc Search Plugin"
    short_name = "Web Mvc Search"
    description = "Web Mvc Search Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/web_mvc_search/mvc_search/resources/baf.xml"
    }
    capabilities = [
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.data.entity_manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.search.manager", "1.0.0")
    ]
    main_modules = [
        "web_mvc_search.mvc_search.web_mvc_search_system"
    ]

    web_mvc_search = None
    """ The web mvc search """

    entity_manager_plugin = None
    """ The entity manager plugin """

    search_manager_plugin = None
    """ The search manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import web_mvc_search.mvc_search.web_mvc_search_system
        self.web_mvc_search = web_mvc_search.mvc_search.web_mvc_search_system.WebMvcSearch(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.web.mvc.search", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_index_configuration_map(self, index_configuration_map):
        return self.web_mvc_search.load_index_configuration_map(index_configuration_map)

    def create_search_index_controller(self, search_index_identifier, search_index_configuration_map, entity_models_modules):
        return self.web_mvc_search.create_search_index_controller(search_index_identifier, search_index_configuration_map, entity_models_modules)

    def update_index(self, index_identifier):
        return self.web_mvc_search.update_index(index_identifier)

    def search_index(self, index_identifier, query_string):
        return self.web_mvc_search.search_index(index_identifier, query_string)

    def search_index_options(self, index_identifier, query_string, options):
        return self.web_mvc_search.search_index_options(index_identifier, query_string, options)

    def get_entity_manager_plugin(self):
        return self.entity_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.data.entity_manager")
    def set_entity_manager_plugin(self, entity_manager_plugin):
        self.entity_manager_plugin = entity_manager_plugin

    def get_search_manager_plugin(self):
        return self.search_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.search.manager")
    def set_search_manager_plugin(self, search_manager_plugin):
        self.search_manager_plugin = search_manager_plugin
