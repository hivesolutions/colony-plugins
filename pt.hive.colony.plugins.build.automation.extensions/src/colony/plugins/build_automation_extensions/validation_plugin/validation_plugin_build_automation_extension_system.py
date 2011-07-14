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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class ValidationPluginBuildAutomationExtension:
    """
    The validation plugin build automation extension class.
    """

    validation_plugin_build_automation_extension_plugin = None
    """ The validation plugin build automation extension plugin """

    def __init__(self, validation_plugin_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type validation_plugin_build_automation_extension_plugin: ValidationPluginBuildAutomationExtensionPlugin
        @param validation_plugin_build_automation_extension_plugin: The validation plugin build automation extension plugin.
        """

        self.validation_plugin_build_automation_extension_plugin = validation_plugin_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # prints an info message
        logger.info("Running validation plugin build automation plugin")

        # retrieves the validation plugin plugin
        validation_plugin_plugin = self.validation_plugin_build_automation_extension_plugin.validation_plugin_plugin

        # validates the given plugin
        validation_errors = validation_plugin_plugin.validate_plugin(plugin.id)

        # retrieves the validation errors length
        validation_errors_length = len(validation_errors)

        # iterates over all the validation error
        for validation_error in validation_errors:
            # prints an error message
            logger.error("Error validating plugin '%s': %s" % (validation_error["plugin_id"], validation_error["message"]))

        # retrieves the build automation success
        build_automation_success = validation_errors_length == 0

        # returns the build automation success
        return build_automation_success
