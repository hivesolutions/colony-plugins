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
        # creates the call list
        call_list = self.create_call_list(command, arguments)

        # executes the command
        subprocess.Popen(call_list)

    def execute_command_logger(self, command, arguments, logger):
        # creates the call list
        call_list = self.create_call_list(command, arguments)

        # retrieves the logger file
        logger_file = self.get_logger_file(logger)

        # retrieves the startup info
        startup_info = self.get_startup_info()

        # opens the subprocess
        subprocess.Popen(call_list, stdin = logger_file, stdout = logger_file, stderr = logger_file, env = self.normalized_environament_map, startupinfo = startup_info)

    def execute_command_logger_execution_directory(self, command, arguments, logger, execution_directory):
        # creates the call list
        call_list = self.create_call_list(command, arguments)

        # retrieves the logger file
        logger_file = self.get_logger_file(logger)

        # retrieves the startup info
        startup_info = self.get_startup_info()

        # opens the subprocess
        subprocess.Popen(call_list, stdin = logger_file, stdout = logger_file, stderr = logger_file, cwd = execution_directory, env = self.normalized_environament_map, startupinfo = startup_info)

    def create_call_list(self, command, arguments):
        # constructs the call list
        call_list = []

        # extends the call list with the command list
        call_list.extend([command])

        # extends the call list with the arguments
        call_list.extend(arguments)

        return call_list

    def get_logger_file(self, logger):
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
        # in case the current os is windows
        if os.name == "nt":
            import win32con
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = win32con.SW_HIDE
        else:
            startup_info = None

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
