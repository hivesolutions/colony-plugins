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

__revision__ = "$LastChangedRevision: 7618 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-19 08:32:46 +0000 (sex, 19 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainConsoleInterfacePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Console Interface Main plugin.
    """

    id = "pt.hive.colony.plugins.main.console.interface"
    name = "Console Interface Main Plugin"
    short_name = "Console Interface Main"
    description = "The main console plugin that controls the console interface"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_console/interface/resources/baf.xml"
    }
    capabilities = [
        "main",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.console", "1.0.0")
    ]
    main_modules = [
        "main_console.interface.main_console_interface_exceptions",
        "main_console.interface.main_console_interface_system",
        "main_console.interface.main_console_interface_unix",
        "main_console.interface.main_console_interface_win32"
    ]

    console_interface = None
    """ The console interface """

    main_console_plugin = None
    """ The main console plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        self.console_command_plugins = []
        import main_console.interface.main_console_interface_system
        self.console_interface = main_console.interface.main_console_interface_system.MainConsoleInterface(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # loads the console
        self.console_interface.load_console()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

        # unloads the console
        self.console_interface.unload_console()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_main_console_plugin(self):
        return self.main_console_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.console")
    def set_main_console_plugin(self, main_console_plugin):
        self.main_console_plugin = main_console_plugin
