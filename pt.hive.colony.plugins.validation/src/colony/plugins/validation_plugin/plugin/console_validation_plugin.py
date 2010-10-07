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

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "validation_plugin"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### PLUGIN VALIDATION HELP ###\n\
validate_plugin [plugin_id] - validates plugin(s)"
""" The help text """

class ConsoleValidationPlugin:
    """
    The console validation plugin class.
    """

    validation_plugin_plugin = None
    """ The validation plugin plugin """

    commands = ["validate_plugin"]
    """ The commands list """

    def __init__(self, validation_plugin_plugin):
        """
        Constructor of the class.

        @type validation_plugin_plugin: ValidationPluginPlugin
        @param validation_plugin_plugin: The validation plugin plugin.
        """

        self.validation_plugin_plugin = validation_plugin_plugin

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

    def process_validate_plugin(self, args, output_method):
        # returns in case the not enough arguments were provided
        if len(args) > 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # validates all plugins
        if len(args) == 0:
            import validation_plugin_exceptions

            try:
                self.validation_plugin_plugin.validate_plugins()
            except validation_plugin_exceptions.PluginValidationFailed, exception:
                for validation_error in exception.validation_errors:
                    print validation_error["plugin_id"]
                    print validation_error["message"]
                    print "------------------------"

            return

        # retrieves the plugin's id
        plugin_id = args[0]

        # validates the specified plugin
        self.validation_plugin_plugin.validate_plugin(plugin_id)
