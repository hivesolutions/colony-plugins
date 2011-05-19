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
import colony.base.decorators

class SearchRemoteServicePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Search Remote Service plugin.
    """

    id = "pt.hive.colony.plugins.search.remote_service"
    name = "Search Remote Service Plugin"
    short_name = "Search Remote Service "
    description = "Search Remote Service Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/search_remote_service/remote_service/resources/baf.xml"
    }
    capabilities = [
        "rpc_service",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.search.manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0")
    ]
    main_modules = [
        "search_remote_service.remote_service.search_remote_service_system"
    ]

    search_remote_service = None
    """ The search remote service """

    search_manager_plugin = None
    """ Search manager plugin """

    task_manager_plugin = None
    """ Task manager plugin """

    @colony.base.decorators.load_plugin("pt.hive.colony.plugins.search.remote_service", "1.0.0")
    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import search_remote_service.remote_service.search_remote_service_system
        self.search_remote_service = search_remote_service.remote_service.search_remote_service_system.SearchRemoteService(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.search.remote_service", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.plugin_call(True)
    def get_service_id(self):
        return self.search_remote_service.get_service_id()

    @colony.base.decorators.plugin_call(True)
    def get_service_alias(self):
        return self.search_remote_service.get_service_alias()

    @colony.base.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return self.search_remote_service.get_available_rpc_methods()

    @colony.base.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return self.search_remote_service.get_rpc_methods_alias()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_index_with_identifier(self, search_index_identifier, properties):
        return self.search_remote_service.create_index_with_identifier(search_index_identifier, properties)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def remove_index_with_identifier(self, search_index_identifier, properties):
        return self.search_remote_service.remove_index_with_identifier(search_index_identifier, properties)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def search_index_by_identifier(self, search_index_identifier, search_query, properties):
        return self.search_remote_service.search_index_by_identifier(search_index_identifier, search_query, properties)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_index_identifiers(self):
        return self.search_remote_service.get_index_identifiers()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_index_metadata(self, search_index_identifier):
        return self.search_remote_service.get_index_metadata(search_index_identifier)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_indexes_metadata(self):
        return self.search_remote_service.get_indexes_metadata()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_search_crawler_adapter_types(self):
        return self.search_remote_service.get_search_crawler_adapter_types()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_search_index_persistence_adapter_types(self):
        return self.search_remote_service.get_search_index_persistence_adapter_types()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def persist_index_with_identifier(self, search_index_identifier, properties):
        return self.search_remote_service.persist_index_with_identifier(search_index_identifier, properties)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def load_index_with_identifier(self, search_index_identifier, properties):
        return self.search_remote_service.load_index_with_identifier(search_index_identifier, properties)

    def get_search_manager_plugin(self):
        return self.search_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.search.manager")
    def set_search_manager_plugin(self, search_manager_plugin):
        self.search_manager_plugin = search_manager_plugin

    def get_task_manager_plugin(self):
        return self.task_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.tasks.task_manager")
    def set_task_manager_plugin(self, task_manager_plugin):
        self.task_manager_plugin = task_manager_plugin
