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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class JavascriptManagerAutoloaderPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Javascript Manager Autoloader plugin.
    """

    id = "pt.hive.colony.plugins.javascript.manager.autoloader"
    name = "Javascript Manager Autoloader Plugin"
    short_name = "Javascript Manager Autloader"
    description = "Javascript Manager Autoloader Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["rpc_service"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.javascript.manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    javascript_manager_autoloader = None

    javascript_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global javascript_manager
        import javascript_manager.autoloader.javascript_manager_autoloader_system
        self.javascript_manager_autoloader = javascript_manager.autoloader.javascript_manager_autoloader_system.JavascriptManagerAutoloader(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.javascript_manager_autoloader.start_auto_update_plugin_files()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.javascript_manager_autoloader.stop_auto_update_plugin_files()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.javascript.manager.autoloader", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.plugin_call(True)
    def get_service_id(self):
        return "javascript_autoloader_manager"

    @colony.plugins.decorators.plugin_call(True)
    def get_service_alias(self):
        return ["pluginManagerAutoloaderAccess"]

    @colony.plugins.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return [self.update_plugin_manager, self.get_status_plugins]

    @colony.plugins.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return {self.update_plugin_manager : ["updatePluginManager"],
                self.get_status_plugins : ["getStatusPlugins"]}

    def update_plugin_manager(self):
        self.javascript_manager_autoloader.update_plugin_manager()

    def get_status_plugins(self, timestamp):
        return self.javascript_manager_autoloader.get_status_plugins(timestamp)

    def get_javascript_manager_plugin(self):
        return self.javascript_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.javascript.manager")
    def set_javascript_manager_plugin(self, javascript_manager_plugin):
        self.javascript_manager_plugin = javascript_manager_plugin
