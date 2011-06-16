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

__revision__ = "$LastChangedRevision: 12604 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-11 19:52:40 +0000 (ter, 11 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainConsoleBasePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Console Base Main plugin.
    """

    id = "pt.hive.colony.plugins.main.console.base"
    name = "Console Base Main Plugin"
    short_name = "Console Base Main"
    description = "The plugin that provides the base commands for the system"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_console/base/resources/baf.xml"
    }
    capabilities = [
        "_console_command_extension",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.console", "1.0.0")
    ]
    main_modules = [
        "main_console.base.main_console_base_system"
    ]

    console_base = None
    """ The console base """

    main_console_plugin = None
    """ The main console plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_console.base.main_console_base_system
        self.console_base = main_console.base.main_console_base_system.MainConsoleBase(self)

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_base.get_console_extension_name()

    def get_commands_map(self):
        return self.console_base.get_commands_map()

    def get_main_console_plugin(self):
        return self.main_console_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.console")
    def set_main_console_plugin(self, main_console_plugin):
        self.main_console_plugin = main_console_plugin
