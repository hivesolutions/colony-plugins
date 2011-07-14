#!/usr/bin/python
# -*- coding: utf-8 -*-

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

CONSOLE_EXTENSION_NAME = "autoloader"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### AUTOLOADER HELP ###\n\
config_autoloader <config-option> - configures the autoloader"
""" The help text """

class ConsoleAutoloader:
    """
    The console autoloader class.
    """

    autoloader_plugin = None
    """ The autoloader plugin """

    commands = [
        "config_autoloader"
    ]
    """ The commands list """

    def __init__(self, autoloader_plugin):
        """
        Constructor of the class.

        @type autoloader_plugin: AutoloaderPlugin
        @param autoloader_plugin: The autoloader plugin.
        """

        self.autoloader_plugin = autoloader_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_config_autoloader(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        output_method("configuring autoloader")
