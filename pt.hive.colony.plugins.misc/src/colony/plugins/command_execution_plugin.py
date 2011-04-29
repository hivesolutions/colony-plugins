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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class CommandExecutionPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Command Execution plugin.
    """

    id = "pt.hive.colony.plugins.misc.command_execution"
    name = "Command Execution Plugin"
    short_name = "Command Execution"
    description = "A plugin to manage the command execution"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/command_execution/resources/baf.xml"
    }
    capabilities = [
        "command_execution",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PackageDependency("Win32 Extensions for Python", "win32con", "b202", "http://starship.python.net/crew/mhammond/win32", conditions_list = [colony.base.plugin_system.OperativeSystemCondition("windows")])
    ]
    main_modules = [
        "misc.command_execution.command_execution_system"
    ]

    command_execution = None
    """ The command execution """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.command_execution.command_execution_system
        self.command_execution = misc.command_execution.command_execution_system.CommandExecution(self)

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

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def execute_command(self, command, arguments):
        """
        Executes the command in the default shell execution environment
        using the given arguments.
        The returned value is an object that can be used to control the
        resulting process.

        @type command: String
        @param command: The command name to be executed.
        @type arguments: List
        @param arguments: The list of argument to be sent to the command.
        @rtype: Process
        @return: An object representing the created process.
        """

        return self.command_execution.execute_command(command, arguments)

    def execute_command_logger(self, command, arguments, logger):
        """
        Executes the command in the default shell execution environment
        using the given arguments.
        The logger object represents the logger that will hold the
        standard output and error information.
        The returned value is an object that can be used to control the
        resulting process.

        @type command: String
        @param command: The command name to be executed.
        @type arguments: List
        @param arguments: The list of argument to be sent to the command.
        @type logger: Logger
        @param logger: The logger object to hold the standard output
        and error information.
        @rtype: Process
        @return: An object representing the created process.
        """

        return self.command_execution.execute_command_logger(command, arguments, logger)

    def execute_command_logger_execution_directory(self, command, arguments, logger, execution_directory):
        """
        Executes the command in the default shell execution environment
        using the given arguments.
        The logger object represents the logger that will hold the
        standard output and error information.
        The returned value is an object that can be used to control the
        resulting process.

        @type command: String
        @param command: The command name to be executed.
        @type arguments: List
        @param arguments: The list of argument to be sent to the command.
        @type logger: Logger
        @param logger: The logger object to hold the standard output
        and error information.
        @type execution_directory: String
        @param execution_directory:  The directory in which the command is going
        to be executed.
        @rtype: Process
        @return: An object representing the created process.
        """

        return self.command_execution.execute_command_logger_execution_directory(command, arguments, logger, execution_directory)

    def execute_command_parameters(self, parameters):
        """
        Executes the command in the default shell execution environment
        using the given parameters.
        The returned value is an object that can be used to control the
        resulting process.

        @type parameters: Dictionary
        @param parameters: The parameters for command execution.
        @rtype: Process
        @return: An object representing the created process.
        """

        return self.command_execution.execute_command_parameters(parameters)
