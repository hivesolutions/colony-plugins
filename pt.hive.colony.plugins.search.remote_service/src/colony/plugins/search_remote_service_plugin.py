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

class SearchRemoteServicePlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search Remote Service plugin.
    """

    id = "pt.hive.colony.plugins.search.remote_service"
    name = "Search Remote Service Plugin"
    short_name = "Search Remote Service "
    description = "Search Remote Service Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["rpc_service"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.search", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0"),]
    events_handled = []
    events_registrable = []

    search_remote_service = None

    search_plugin = None
    """ Search plugin """
    task_manager_plugin = None
    """ Task manager plugin """

    @colony.plugins.decorators.load_plugin("pt.hive.colony.plugins.search.remote_service", "1.0.0")
    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search_remote_service
        import search_remote_service.remote_service.search_remote_service_system
        self.search_remote_service = search_remote_service.remote_service.search_remote_service_system.SearchRemoteService(self)

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

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.search.remote_service", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.plugin_call(True)
    def get_service_id(self):
        return self.search_remote_service.get_service_id()

    @colony.plugins.decorators.plugin_call(True)
    def get_service_alias(self):
        return self.search_remote_service.get_service_alias()

    @colony.plugins.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return self.search_remote_service.get_available_rpc_methods()

    @colony.plugins.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return self.search_remote_service.get_rpc_methods_alias()

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_index_with_identifier(self, search_index_identifier, properties):
        return self.search_remote_service.create_index_with_identifier(search_index_identifier, properties)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def remove_index_with_identifier(self, search_index_identifier, properties):
        return self.search_remote_service.remove_index_with_identifier(search_index_identifier, properties)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def search_index(self, search_index_identifier, search_query, properties):
        return self.search_remote_service.search_index(search_index_identifier, search_query, properties)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_indexes_metadata(self):
        return self.search_remote_service.get_indexes_metadata()

    def get_search_plugin(self):
        return self.search_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.search")
    def set_search_plugin(self, search_plugin):
        self.search_plugin = search_plugin

    def get_task_manager_plugin(self):
        return self.task_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.tasks.task_manager")
    def set_task_manager_plugin(self, task_manager_plugin):
        self.task_manager_plugin = task_manager_plugin
