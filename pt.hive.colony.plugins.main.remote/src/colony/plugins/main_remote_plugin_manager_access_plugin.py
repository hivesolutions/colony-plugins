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

__revision__ = "$LastChangedRevision: 2119 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:55:58 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class MainRemotePluginManagerAccessPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Remote Plugin Manager Access Main plugin
    """

    id = "pt.hive.colony.plugins.main.remote.plugin_manager_access"
    name = "Remote Plugin Manager Access Main Plugin"
    short_name = "Remote Plugin Manager Access Main"
    description = "Remote Plugin Manager Access Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["thread", "plugin_manager_access"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.ice_helper", "1.0.0")]
    events_handled = []
    events_registrable = []

    main_remote_plugin_manager_access = None    

    ice_helper_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_remote
        import main_remote.plugin_manager_access.main_remote_plugin_manager_access_system
        self.main_remote_plugin_manager_access = main_remote.plugin_manager_access.main_remote_plugin_manager_access_system.MainRemotePluginManagerAccess(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

        self.main_remote_plugin_manager_access.start_registry()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.main_remote_plugin_manager_access.stop_registry()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.main.remote.plugin_manager_access", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def set_ice_helper_plugin(self):
        return self.ice_helper_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.ice_helper")
    def set_ice_helper_plugin(self, ice_helper_plugin):
        self.ice_helper_plugin = ice_helper_plugin
