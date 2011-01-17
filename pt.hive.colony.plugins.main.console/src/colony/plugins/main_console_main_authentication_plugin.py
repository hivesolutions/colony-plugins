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

__revision__ = "$LastChangedRevision: 12728 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-15 16:11:37 +0000 (sÃ¡b, 15 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainConsoleMainAuthenticationPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Console Main Main Authentication Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.console.main_authentication_handler"
    name = "Console Main Main Authentication Handler Plugin"
    short_name = "Console Main Main Authentication Handler"
    description = "The main console plugin that controls the console authentication"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_console/console/resources/baf.xml"}
    capabilities = ["console_authentication_handler", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_console.console.main_console_system"]

    console_authentication = None
    console_test_case_class = None

    console_command_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        self.console_command_plugins = []
        global main_console
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

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.main.console", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.main.console", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def execute_command_line(self, command_line):
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

    def get_command_line_alternatives(self, command, arguments):
        """
        Processes the given command line, with the given output method.
        Retrieves the alternative (possible) values for the given command
        and arguments.

        @type command: String
        @param command: The command to be retrieve the alternatives.
        @type arguments: String
        @param arguments: The list of arguments
        @rtype: Tuple
        @return: A tuple containing the list of alternatives for the given
        command line and the current best match.
        """

        return self.console.get_command_line_alternatives(command, arguments)

    def split_command_line(self, command_line):
        """
        Splits the given command line into command and arguments.

        @type command_line: String
        @param command_line: The command line to be splitted.
        @rtype: Tuple
        @return: A tuple containing the command and the arguments.
        """

        return self.console.split_command_line(command_line)

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        @rtype: Method
        @return: The default output method for console.
        """

        return self.console.get_default_output_method()

    def create_console_interface_character(self, console_handler):
        """
        Creates a new console interface character based
        from the given console handler.

        @type console_handler: ConsoleHandler
        @param console_handler: The console handler to be used.
        @rtype: ConsoleInterfaceCharacter
        @return: The create console interface character.
        """

        return self.console.create_console_interface_character(console_handler)
