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

import os
import sys
import subprocess
import logging

NT_PLATFORM_VALUE = "nt"
""" The nt platform value """

class CommandExecution:
    """
    The command execution class.
    """

    command_execution_plugin = None
    """ The command execution plugin """

    normalized_environament_map = None
    """ The normalized environment map (no unicode strings) """

    def __init__(self, command_execution_plugin):
        """
        Constructor of the class.

        @type command_execution_plugin: CommandExecutionPlugin
        @param command_execution_plugin: The command execution plugin.
        """

        self.command_execution_plugin = command_execution_plugin

        self.normalized_environament_map = self._normalize_environment_map()

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

        # creates the call list
        call_list = self.create_call_list(command, arguments)

        # retrieves the startup info
        startup_info = self.get_startup_info()

        # executes the command and retrieves the process object
        process = subprocess.Popen(call_list, startupinfo = startup_info)

        # returns the process object
        return process

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

        # creates the call list
        call_list = self.create_call_list(command, arguments)

        # retrieves the logger file
        logger_file = self.get_logger_file(logger)

        # retrieves the startup info
        startup_info = self.get_startup_info()

        # opens the subprocess and retrieves the process object
        process = subprocess.Popen(call_list, stdin = logger_file, stdout = logger_file, stderr = logger_file, env = self.normalized_environament_map, startupinfo = startup_info)

        # returns the process object
        return process

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

        # creates the call list
        call_list = self.create_call_list(command, arguments)

        # retrieves the logger file
        logger_file = self.get_logger_file(logger)

        # retrieves the startup info
        startup_info = self.get_startup_info()

        # opens the subprocess and retrieves the process object
        process = subprocess.Popen(call_list, stdin = logger_file, stdout = logger_file, stderr = logger_file, cwd = execution_directory, env = self.normalized_environament_map, startupinfo = startup_info)

        # returns the process object
        return process

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

        # retrieves the various parameters values
        command = parameters.get("command", "")
        arguments = parameters.get("arguments", [])
        bufsize = parameters.get("bufsize", 0)
        executable = parameters.get("executable", None)
        stdin = parameters.get("stdin", None)
        stdout = parameters.get("stdout", None)
        stderr = parameters.get("stderr", None)
        preexec_fn = parameters.get("preexec_fn", None)
        close_fds = parameters.get("close_fds", False)
        shell = parameters.get("shell", False)
        cwd = parameters.get("cwd", None)
        env = parameters.get("env", None)
        universal_newlines = parameters.get("universal_newlines", False)
        startupinfo = parameters.get("startupinfo", self.get_startup_info())
        creationflags = parameters.get("creationflags", 0)

        # sets the shell mode only in windows
        shell = shell and os.name == NT_PLATFORM_VALUE

        # creates the call list
        call_list = self.create_call_list(command, arguments)

        # opens the subprocess and retrieves the process object
        process = subprocess.Popen(call_list, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags)

        # returns the process object
        return process

    def create_call_list(self, command, arguments):
        """
        Creates the call list for the given command and
        arguments.

        @type command: String
        @param command: The command execution value.
        @type parameters: List
        @param parameters: The list of parameters to be used
        in the call.
        @rtype: List
        @return: The created call list.
        """

        # constructs the call list
        call_list = []

        # extends the call list with the command list
        call_list.extend([command])

        # extends the call list with the arguments
        call_list.extend(arguments)

        return call_list

    def get_logger_file(self, logger):
        """
        Retrieves the file (stream) for the given logger
        object.

        @type logger: Logger
        @param logger: The logger object to retrieve the file
        (stream).
        @rtype: File
        @return: The file (stream) for the given logger
        object.
        """

        # sets the default logger file
        logger_file = sys.stdout

        # retrieves the logger handlers
        logger_handlers = logger.handlers

        # in case the logger contains handlers
        if logger_handlers:
            # retrieves the logger default handler
            handler = logger_handlers[0]

            # in case the handler instance is of type StreamHandler
            if handler.__class__ == logging.StreamHandler:
                # retrieves the stream handler stream
                logger_file = handler.stream

        # returns the logger file
        return logger_file

    def get_startup_info(self):
        """
        Retrieves the startup info for the current
        environment.

        @rtype: StartupInfo
        @return: The startup info for the current
        environment.
        """

        # in case the current os is windows
        if os.name == NT_PLATFORM_VALUE:
            import win32con
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW #@UndefinedVariable
            startup_info.wShowWindow = win32con.SW_HIDE
        # otherwise it must be a different os
        else:
            # sets the startup info to none
            startup_info = None

        # returns the startup info
        return startup_info

    def _normalize_environment_map(self):
        """
        Normalizes the environment variables map.
        The process of normalization consists in the
        decoding of the encoded string (unicode).

        @rtype: Dictionary
        @return: The normalized environment map.
        """

        # creates the normalized environment map
        normalized_environment_map = {}

        # iterates over all the environment items
        for environment_key, environment_value in os.environ.items():
            # sets the environment value in the normalized environment map
            normalized_environment_map[environment_key] = str(environment_value)

        # returns the normalized environment map
        return normalized_environment_map
