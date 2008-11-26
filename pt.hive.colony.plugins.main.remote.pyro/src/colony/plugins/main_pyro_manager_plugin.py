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

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class MainPyroManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Pyro Manager Main plugin
    """

    id = "pt.hive.colony.plugins.main.remote.pyro.manager"
    name = "Pyro Manager Main Plugin"
    short_name = "Pyro Manager Main"
    description = "Pyro Manager Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["pyro_manager", "rpc_handler"]
    capabilities_allowed = ["rpc_service"]
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "Pyro", "Pyro", "3.8.x", "http://pyro.sourceforge.net")]
    events_handled = []
    events_registrable = []

    main_pyro_manager = None

    rpc_service_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_remote_pyro
        import main_remote_pyro.manager.main_pyro_manager_system
        self.main_pyro_manager = main_remote_pyro.manager.main_pyro_manager_system.MainPyroManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.main.remote.pyro.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.main.remote.pyro.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def is_active(self):
        return self.main_pyro_manager.is_active()

    def get_handler_name(self):
        return self.main_pyro_manager.get_handler_name()

    @colony.plugins.decorators.load_allowed_capability("rpc_service")
    def rpc_service_capability_load_allowed(self, plugin, capability):
        self.rpc_service_plugins.append(plugin)
        self.main_pyro_manager.update_service_methods(plugin)

    @colony.plugins.decorators.unload_allowed_capability("rpc_service")
    def rpc_servicer_capability_unload_allowed(self, plugin, capability):
        if plugin in self.rpc_service_plugins:
            self.rpc_service_plugins.remove(plugin)
            self.main_pyro_manager.update_service_methods()
