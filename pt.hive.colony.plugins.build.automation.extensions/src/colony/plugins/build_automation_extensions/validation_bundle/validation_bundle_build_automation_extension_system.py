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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.map_util

BUNDLE_ID_VALUE = "bundle_id"
""" The bundle id value """

MESSAGE_VALUE = "message"
""" The message value """

SPECIFICATION_FILES_VALUE = "specification_files"
""" The specification files value """

SPECIFICATION_FILE_VALUE = "specification_file"
""" The specification file value """

class ValidationBundleBuildAutomationExtension:
    """
    The validation bundle build automation extension class.
    """

    validation_bundle_build_automation_extension_plugin = None
    """ The validation bundle build automation extension plugin """

    def __init__(self, validation_bundle_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type validation_bundle_build_automation_extension_plugin: ValidationBundleBuildAutomationExtensionPlugin
        @param validation_bundle_build_automation_extension_plugin: The validation bundle build automation extension plugin.
        """

        self.validation_bundle_build_automation_extension_plugin = validation_bundle_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # prints an info message
        logger.info("Running validation bundle build automation plugin")

        # retrieves the validation bundle plugin
        validation_bundle_plugin = self.validation_bundle_build_automation_extension_plugin.validation_bundle_plugin

        # retrieves the specification files group
        specification_files = parameters[SPECIFICATION_FILES_VALUE]

        # retrieves the specification files
        _specification_files = colony.libs.map_util.map_get_values(specification_files, SPECIFICATION_FILE_VALUE)

        # validates the bundles
        validation_errors = validation_bundle_plugin.validate_bundles(_specification_files)

        # retrieves the validation errors length
        validation_errors_length = len(validation_errors)

        # iterates over all the validation error
        for validation_error in validation_errors:
            # retrieves the validation error bundle id
            validation_error_bundle_id = validation_error[BUNDLE_ID_VALUE]

            # retrieves the validation error message
            validation_error_message = validation_error[MESSAGE_VALUE]

            # prints an error message
            logger.error("Error validating bundle '%s': %s" % (validation_error_bundle_id, validation_error_message))

        # retrieves the build automation success
        build_automation_success = validation_errors_length == 0

        # returns the build automation success
        return build_automation_success
