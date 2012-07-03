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

import colony.base.plugin_system
import colony.base.decorators

class MainConsolePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Console Main plugin.
    """

    id = "pt.hive.colony.plugins.main.console"
    name = "Console Main Plugin"
    short_name = "Console Main"
    description = "The main console plugin that controls the console"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_console/console/resources/baf.xml"
    }
    capabilities = [
        "main_console",
        "test_case",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "_console_command_extension",
        "console_authentication_handler"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.authentication", "1.x.x")
    ]
    main_modules = [
        "main_console.console.main_console_authentication",
        "main_console.console.main_console_exceptions",
        "main_console.console.main_console_interfaces",
        "main_console.console.main_console_system",
        "main_console.console.main_console_test"
    ]

    console = None
    """ The console """

    console_test_case_class = None
    """ The console test case class """

    console_command_plugins = []
    """ The console command plugins """

    main_authentication_plugin = None
    """ The main authentication plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        self.console_command_plugins = []
        import main_console.console.main_console_system
        import main_console.console.main_console_test
        self.console = main_console.console.main_console_system.MainConsole(self)
        self.console_test_case_class = main_console.console.main_console_test.MainConsoleTestCase

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def create_console_context(self):
        """
        Creates a new console context for third party usage.

        @rtype: ConsoleContext
        @return: The creates console context.
        """

        return self.console.create_console_context()

    def create_console_interface_character(self, console_handler, console_context):
        """
        Creates a new console interface character based
        from the given console handler.

        @type console_handler: ConsoleHandler
        @param console_handler: The console handler to be used.
        @type console_context: ConsoleContext
        @param console_context: The console context to be used.
        @rtype: ConsoleInterfaceCharacter
        @return: The create console interface character.
        """

        return self.console.create_console_interface_character(console_handler, console_context)

    def execute_command_line(self, command_line):
        """
        Executes the given command line using the default
        output method.

        @type command_line: String
        @param command_line: The command line to be executed.
        @rtype: bool
        @return: If the execution of the command line was successful.
        """

        return self.console.process_command_line(command_line, None)

    def process_command_line(self, command_line, output_method):
        """
        Processes the given command line, with the given output method.

        @type command_line: String
        @param command_line: The command line to be processed.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @rtype: bool
        @return: If the processing of the command line was successful.
        """

        return self.console.process_command_line(command_line, output_method)

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        @rtype: Method
        @return: The default output method for console.
        """

        return self.console.get_default_output_method()

    def get_test_case(self):
        """
        Retrieves the test case.

        @rtype: TestCase
        @return: The test case.
        """

        return self.console_test_case_class

    @colony.base.decorators.load_allowed_capability("_console_command_extension")
    def console_command_extension_load_allowed(self, plugin, capability):
        self.console_command_plugins.append(plugin)
        self.console.console_command_extension_load(plugin)

    @colony.base.decorators.unload_allowed_capability("_console_command_extension")
    def console_command_extension_unload_allowed(self, plugin, capability):
        self.console_command_plugins.remove(plugin)
        self.console.console_command_extension_unload(plugin)

    def get_main_authentication_plugin(self):
        return self.main_authentication_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.authentication")
    def set_main_authentication_plugin(self, main_authentication_plugin):
        self.main_authentication_plugin = main_authentication_plugin

    @colony.base.decorators.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.console.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.console.unset_configuration_property()
