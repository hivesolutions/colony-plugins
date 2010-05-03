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

class MainServicePopPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Pop Service Main plugin.
    """

    id = "pt.hive.colony.plugins.main.service.pop"
    name = "Pop Service Main Plugin"
    short_name = "Pop Service Main"
    description = "The plugin that offers the pop service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT]
    capabilities = ["service.pop"]
    capabilities_allowed = ["pop_service_handler", "pop_service_authentication_handler", "pop_service_session_handler", "socket_provider", "socket_upgrader"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.threads.thread_pool_manager", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["main_service_pop.pop.main_service_pop_exceptions", "main_service_pop.pop.main_service_pop_system"]

    main_service_pop = None

    pop_service_handler_plugins = []
    pop_service_authentication_handler_plugins = []
    pop_service_session_handler_plugins = []
    socket_provider_plugins = []
    socket_upgrader_plugins = []

    thread_pool_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_service_pop
        import main_service_pop.pop.main_service_pop_system
        self.main_service_pop = main_service_pop.pop.main_service_pop_system.MainServicePop(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.main.service.pop", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.main.service.pop", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.main.service.pop", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def start_service(self, parameters):
        self.main_service_pop.start_service(parameters)

    def stop_service(self, parameters):
        self.main_service_pop.stop_service(parameters)

    @colony.plugins.decorators.load_allowed_capability("pop_service_handler")
    def pop_service_handler_load_allowed(self, plugin, capability):
        self.pop_service_handler_plugins.append(plugin)
        self.main_service_pop.pop_service_handler_load(plugin)

    @colony.plugins.decorators.load_allowed_capability("pop_service_authentication_handler")
    def pop_service_authentication_handler_load_allowed(self, plugin, capability):
        self.pop_service_authentication_handler_plugins.append(plugin)
        self.main_service_pop.pop_service_authentication_handler_load(plugin)

    @colony.plugins.decorators.load_allowed_capability("pop_service_session_handler")
    def pop_service_session_handler_load_allowed(self, plugin, capability):
        self.pop_service_session_handler_plugins.append(plugin)
        self.main_service_pop.pop_service_session_handler_load(plugin)

    @colony.plugins.decorators.load_allowed_capability("socket_provider")
    def socket_provider_load_allowed(self, plugin, capability):
        self.socket_provider_plugins.append(plugin)

    @colony.plugins.decorators.load_allowed_capability("socket_upgrader")
    def socket_upgrader_load_allowed(self, plugin, capability):
        self.socket_upgrader_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("pop_service_handler")
    def pop_service_handler_unload_allowed(self, plugin, capability):
        self.pop_service_handler_plugins.remove(plugin)
        self.main_service_pop.pop_service_handler_unload(plugin)

    @colony.plugins.decorators.unload_allowed_capability("pop_service_authentication_handler")
    def pop_service_authentication_handler_unload_allowed(self, plugin, capability):
        self.pop_service_authentication_handler_plugins.remove(plugin)
        self.main_service_pop.pop_service_authentication_handler_unload(plugin)

    @colony.plugins.decorators.unload_allowed_capability("pop_service_session_handler")
    def pop_service_session_handler_unload_allowed(self, plugin, capability):
        self.pop_service_session_handler_plugins.remove(plugin)
        self.main_service_pop.pop_service_session_handler_unload(plugin)

    @colony.plugins.decorators.unload_allowed_capability("socket_provider")
    def socket_provider_unload_allowed(self, plugin, capability):
        self.socket_provider_plugins.remove(plugin)

    @colony.plugins.decorators.unload_allowed_capability("socket_upgrader")
    def socket_upgrader_unload_allowed(self, plugin, capability):
        self.socket_upgrader_plugins.remove(plugin)

    def get_thread_pool_manager_plugin(self):
        return self.thread_pool_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.threads.thread_pool_manager")
    def set_thread_pool_manager_plugin(self, thread_pool_manager_plugin):
        self.thread_pool_manager_plugin = thread_pool_manager_plugin
