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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class JavascriptManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Javascript Manager plugin
    """

    id = "pt.hive.colony.plugins.javascript.manager"
    name = "Javascript Manager Plugin"
    short_name = "Javascript Manager"
    description = "Javascript Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/javascript_manager/manager/resources/baf.xml"
    }
    capabilities = [
        "rpc_service",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.resources.resource_manager", "1.0.0")
    ]
    main_modules = [
        "javascript_manager.manager.javascript_manager_exceptions",
        "javascript_manager.manager.javascript_manager_parser",
        "javascript_manager.manager.javascript_manager_system"
    ]

    javascript_manager = None
    """ The javascript manager """

    resource_manager_plugin = None
    """ The resource manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import javascript_manager.manager.javascript_manager_system
        self.javascript_manager = javascript_manager.manager.javascript_manager_system.JavascriptManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.javascript_manager.set_plugin_search_directories()
        self.javascript_manager.index_plugin_search_directories()
        self.javascript_manager.load_plugin_files()
        self.javascript_manager.start_auto_index_plugin_search_directories()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.javascript_manager.stop_auto_index_plugin_search_directories()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.plugin_call(True)
    def get_service_id(self):
        return "javascript_manager"

    @colony.base.decorators.plugin_call(True)
    def get_service_alias(self):
        return [
            "pluginManagerAccess"
        ]

    @colony.base.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return [
            self.get_plugin_descriptor,
            self.get_plugin_file,
            self.get_plugins_files,
            self.get_available_plugins,
            self.get_available_plugin_descriptors
        ]

    @colony.base.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return {
            self.get_plugin_descriptor : ["getPluginDescriptor"],
            self.get_plugin_file : ["getPluginFile"],
            self.get_plugins_files : ["getPluginsFiles"],
            self.get_available_plugins : ["getAvailablePlugins"],
            self.get_available_plugin_descriptors : ["getAvailablePluginDescriptors"]
        }

    def get_plugin_descriptor(self, plugin_id):
        return self.javascript_manager.get_plugin_descriptor(plugin_id)

    def get_plugin_file(self, plugin_id):
        return self.javascript_manager.get_plugin_file(plugin_id)

    def get_plugins_files(self, plugin_id_list):
        return self.javascript_manager.get_plugins_files(plugin_id_list)

    def get_plugin_payload(self, plugin_id):
        return self.javascript_manager.get_plugin_payload(plugin_id)

    def get_plugins_payload(self, plugin_id_list):
        return self.javascript_manager.get_plugins_payload(plugin_id_list)

    def get_plugin_file_payload(self, plugin_id):
        return self.javascript_manager.get_plugin_file_payload(plugin_id)

    def get_plugins_files_payload(self, plugin_id_list):
        return self.javascript_manager.get_plugins_files_payload(plugin_id_list)

    def get_available_plugins(self):
        return self.javascript_manager.get_available_plugins()

    def get_available_plugin_descriptors(self):
        return self.javascript_manager.get_available_plugin_descriptors()

    def get_file_full_path(self, relative_file_path):
        return self.javascript_manager.get_file_full_path(relative_file_path)

    def get_plugin_search_directories_list(self):
        return self.javascript_manager.get_plugin_search_directories_list()

    def get_plugin_search_directories_map(self):
        return self.javascript_manager.get_plugin_search_directories_map()

    def get_plugin_descriptor_parser(self):
        return self.javascript_manager.get_plugin_descriptor_parser()

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin
