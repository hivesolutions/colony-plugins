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

import threading
import subprocess

import colony.libs.os_util
import colony.libs.map_util

import command_execution_build_automation_extension_exceptions

class CommandExecutionBuildAutomationExtension:
    """
    The command execution build automation extension class.
    """

    command_execution_build_automation_extension_plugin = None
    """ The command execution build automation extension plugin """

    def __init__(self, command_execution_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type command_execution_build_automation_extension_plugin: CommandExecutionBuildAutomationExtensionPlugin
        @param command_execution_build_automation_extension_plugin: The command execution build automation extension plugin.
        """

        self.command_execution_build_automation_extension_plugin = command_execution_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the command execution plugin
        command_execution_plugin = self.command_execution_build_automation_extension_plugin.command_execution_plugin

        # retrieves the command
        command = parameters["command"]

        # retrieves the arguments from the parameters
        arguments = parameters.get("arguments", {})
        _arguments = colony.libs.map_util.map_get_values(arguments, "argument")

        # retrieves the shell value from the parameters
        shell = parameters.get("shell", False) == "true"

        # retrieves the timeout value from the parameters
        timeout = int(parameters.get("timeout", "0"))

        # creates the parameters map for the execution command
        parameters = {"command" : command,
                      "arguments" : _arguments,
                      "stdin" : subprocess.PIPE,
                      "stdout" : subprocess.PIPE,
                      "stderr" : subprocess.PIPE,
                      "shell" : shell}

        # prints an info message
        logger.info("Running command '%s' with arguments %s in shell" % (command, str(_arguments)))

        # executes the command, retrieving the process object
        process = command_execution_plugin.execute_command_parameters(parameters)

        # starts the cancel timer for the given process
        cancel_timer = self._start_cancel_timer(process, timeout)

        # waits for the process to terminate
        stdout_data, stderr_data = process.communicate()

        # cancels the cancel timer
        cancel_timer.cancel()

        # prints the standard output information
        logger.info("Process standard output (stdout)")
        logger.info(stdout_data)

        # prints the standard error information
        logger.info("Process standard error (stderr)")
        logger.info(stderr_data)

        # retrieves the process return code
        process_return_code = process.returncode

        # in case the return code is not valid
        if process_return_code:
            # raises the command execution build automation extension exception
            raise command_execution_build_automation_extension_exceptions.CommandExecutionBuildAutomationExtensionException("Process returned error code: %i" % process_return_code)

        # returns true (success)
        return True

    def _start_cancel_timer(self, process, timeout):
        """
        Starts the cancel timer for the given process and
        using the given timeout.

        @type process: Process
        @param process: The process to start the cancel timer.
        @type timeout: float
        @param timeout: The timeout value to be used.
        @rtype: Timer
        @return: The started cancel timer.
        """

        # in case the timeout is invalid
        if timeout == 0:
            # returns immediately
            return

        # creates the cancel process lambda function
        cancel_process = lambda: process.returncode == None and colony.libs.os_util.kill_process(process.pid)

        # creates the new timer to cancel the connection
        cancel_timer = threading.Timer(timeout, cancel_process)

        # starts the timer
        cancel_timer.start()

        # returns the created cancel time
        return cancel_timer
