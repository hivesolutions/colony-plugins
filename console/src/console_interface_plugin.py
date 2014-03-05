#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class ConsoleInterfacePlugin(colony.base.system.Plugin):
    """
    The main class for the Console Interface plugin.
    """

    id = "pt.hive.colony.plugins.console.interface"
    name = "Console Interface"
    description = "The console plugin that controls the console interface"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "main"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.console")
    ]
    main_modules = [
        "console.interface.exceptions",
        "console.interface.system",
        "console.interface.interface_unix",
        "console.interface.interface_win32"
    ]

    console_interface = None
    """ The console interface """

    console_plugin = None
    """ The console plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        self.console_command_plugins = []
        import console.interface.system
        self.console_interface = console.interface.system.ConsoleInterface(self)
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)
        self.console_interface.load_console()

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)
        self.console_interface.unload_console()

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)
        self.release_ready_semaphore()

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.system.Plugin.unset_configuration_property(self, property_name)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.console")
    def set_console_plugin(self, console_plugin):
        self.console_plugin = console_plugin

    @colony.base.decorators.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.console_interface.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.console_interface.unset_configuration_property()
