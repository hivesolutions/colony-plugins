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

import colony.plugins.plugin_system
import colony.plugins.decorators

class JavascriptManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Javascript Manager plugin
    """

    id = "pt.hive.colony.plugins.javascript.manager"
    name = "Javascript Manager Plugin"
    short_name = "Javascript Manager"
    description = "Javascript Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["rpc_service"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    javascript_manager = None

    resource_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global javascript_manager
        import javascript_manager.manager.javascript_manager_system
        self.javascript_manager = javascript_manager.manager.javascript_manager_system.JavascriptManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.javascript_manager.set_plugin_search_directories()
        self.javascript_manager.index_plugin_search_directories()
        self.javascript_manager.load_plugin_files()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.javascript.manager", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.plugin_call(True)
    def get_service_id(self):
        return "javascript_manager"

    @colony.plugins.decorators.plugin_call(True)
    def get_service_alias(self):
        return ["pluginManagerAccess"]

    @colony.plugins.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return [self.get_available_plugins, self.get_available_plugin_descriptors, self.update_plugin_manager,
                self.get_new_plugins, self.get_new_plugin_descriptors, self.get_updated_plugins,
                self.get_updated_plugin_descriptors, self.get_removed_plugins, self.get_removed_plugin_descriptors]

    @colony.plugins.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return {self.get_available_plugins : ["getAvailablePlugins"],
                self.get_available_plugin_descriptors : ["getAvailablePluginDescriptors"],
                self.update_plugin_manager : ["updatePluginManager"],
                self.get_new_plugins : ["getNewPlugins"],
                self.get_new_plugin_descriptors : ["getNewPluginDescriptors"],
                self.get_updated_plugins : ["getUpdatedPlugins"],
                self.get_updated_plugin_descriptors : ["getUpdatedPluginDescriptors"],
                self.get_removed_plugins : ["getRemovedPlugins"],
                self.get_removed_plugin_descriptors : ["getRemovedPluginDescriptors"]}

    def get_available_plugins(self):
        return self.javascript_manager.get_available_plugins()

    def get_available_plugin_descriptors(self):
        return self.javascript_manager.get_available_plugin_descriptors()

    def update_plugin_manager(self):
        self.javascript_manager.update_plugin_manager()

    def get_new_plugins(self):
        return self.javascript_manager.get_new_plugins()

    def get_new_plugin_descriptors(self):
        return self.javascript_manager.get_new_plugin_descriptors()

    def get_updated_plugins(self):
        return self.javascript_manager.get_updated_plugins()

    def get_updated_plugin_descriptors(self):
        return self.javascript_manager.get_updated_plugin_descriptors()

    def get_removed_plugins(self):
        return self.javascript_manager.get_removed_plugins()

    def get_removed_plugin_descriptors(self):
        return self.javascript_manager.get_removed_plugin_descriptors()

    def get_plugin_search_directories_list(self):
        return self.javascript_manager.get_plugin_search_directories_list()

    def get_file_full_path(self, relative_file_path):
        return self.javascript_manager.get_file_full_path(relative_file_path)

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin
