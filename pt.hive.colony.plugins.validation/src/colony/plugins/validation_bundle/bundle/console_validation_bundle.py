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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

BUNDLE_ID_VALUE = "bundle_id"
""" The bundle id value """

BUNDLE_VERSION_VALUE = "bundle_version"
""" The bundle version value """

BUNDLE_MESSAGE_VALUE = "message"
""" The bundle message value """

CONSOLE_EXTENSION_NAME = "validation_bundle"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### BUNDLE VALIDATION HELP ###\n\
validate_bundle - validates bundles"
""" The help text """

class ConsoleValidationBundle:
    """
    The console validation bundle class.
    """

    validation_bundle_plugin = None
    """ The validation bundle plugin """

    commands = ["validate_bundle"]
    """ The commands list """

    def __init__(self, validation_bundle_plugin):
        """
        Constructor of the class.

        @type validation_bundle_plugin: ValidationBundlePlugin
        @param validation_bundle_plugin: The validation bundle plugin.
        """

        self.validation_bundle_plugin = validation_bundle_plugin

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

    def process_validate_bundle(self, args, output_method):
        # validates the bundles
        validation_errors = self.validation_bundle_plugin.validate_bundles([])

        # outputs the validation errors
        for validation_error in validation_errors:
            # retrieves the validation error bundle id
            validation_error_bundle_id = validation_error[BUNDLE_ID_VALUE]

            # retrieves the validation error bundle version
            validation_error_bundle_version = validation_error[BUNDLE_VERSION_VALUE]

            # retrieves the validation error message
            validation_error_message = validation_error[BUNDLE_MESSAGE_VALUE]

            # creates a validation error message
            validation_error_message = "[%s (%s)] %s" % (validation_error_bundle_id, validation_error_bundle_version, validation_error_message)

            # prints the validation error message
            output_method(validation_error_message)
