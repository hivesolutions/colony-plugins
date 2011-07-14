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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 12670 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-13 13:08:29 +0000 (qui, 13 Jan 2011) $"
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

VALIDATION_ERROR_MESSAGE_FORMAT = "[%s (%s)] %s"
""" The validation error message format """

CONSOLE_EXTENSION_NAME = "validation_bundle"
""" The console extension name """

class ConsoleValidationBundle:
    """
    The console validation bundle class.
    """

    validation_bundle_plugin = None
    """ The validation bundle plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, validation_bundle_plugin):
        """
        Constructor of the class.

        @type validation_bundle_plugin: ValidationBundlePlugin
        @param validation_bundle_plugin: The validation bundle plugin.
        """

        self.validation_bundle_plugin = validation_bundle_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_validate_bundle(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the validate bundle command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the validation bundle
        validation_bundle = self.validation_bundle_plugin.validation_bundle

        # validates the bundles
        validation_errors = validation_bundle.validate_bundles([])

        # outputs the validation errors
        for validation_error in validation_errors:
            # retrieves the validation error bundle id
            validation_error_bundle_id = validation_error[BUNDLE_ID_VALUE]

            # retrieves the validation error bundle version
            validation_error_bundle_version = validation_error[BUNDLE_VERSION_VALUE]

            # retrieves the validation error message
            validation_error_message = validation_error[BUNDLE_MESSAGE_VALUE]

            # creates a validation error message
            validation_error_message = VALIDATION_ERROR_MESSAGE_FORMAT % (validation_error_bundle_id, validation_error_bundle_version, validation_error_message)

            # prints the validation error message
            output_method(validation_error_message)

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "validate_bundle" : {
                "handler" : self.process_validate_bundle,
                "description" : "validates all bundles"
            }
        }

        # returns the commands map
        return commands_map
