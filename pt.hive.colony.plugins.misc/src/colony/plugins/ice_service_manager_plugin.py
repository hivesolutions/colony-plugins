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

class IceServiceManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Ice Service Manager plugin
    """

    id = "pt.hive.colony.plugins.misc.ice_service_manager"
    name = "Ice Service Manager Plugin"
    short_name = "Ice Service Manager"
    description = "Ice Service Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda."
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["ice_service_manager", "console_command_extension"]
    capabilities_allowed = ["ice_service"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.ice_helper", "1.0.0"),
                    colony.plugins.plugin_system.PackageDependency(
                    "Win32 Extensions for Python", "win32con", "b202", "http://starship.python.net/crew/mhammond/win32") ]
    events_handled = []
    events_registrable = []

    ice_service_manager = None
    console_ice_service_manager = None

    ice_helper_plugin = None
    ice_service_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.ice_service_manager.ice_service_managing_system
        import misc.ice_service_manager.console_ice_service_manager
        self.ice_service_manager = misc.ice_service_manager.ice_service_managing_system.IceServiceManager(self)
        self.console_ice_service_manager = misc.ice_service_manager.console_ice_service_manager.ConsoleIceServiceManager(self)

        self.ice_service_plugins = []

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.ice_service_manager.unload()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

        if capability == "ice_service":
            self.ice_service_plugins.append(plugin)

        self.ice_service_manager.refresh_services()

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.misc.ice_service_manager", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_ice_service_manager.get_console_extension_name()

    def get_all_commands(self):
        return self.console_ice_service_manager.get_all_commands()

    def get_handler_command(self, command):
        return self.console_ice_service_manager.get_handler_command(command)

    def get_help(self):
        return self.console_ice_service_manager.get_help()

    def get_ice_helper_plugin(self):
        return self.ice_helper_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.ice_helper")
    def set_ice_helper_plugin(self, ice_helper_plugin):
        self.ice_helper_plugin = ice_helper_plugin
