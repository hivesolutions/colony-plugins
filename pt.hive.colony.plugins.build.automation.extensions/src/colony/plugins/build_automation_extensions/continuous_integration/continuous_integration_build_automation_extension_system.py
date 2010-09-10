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

import colony.libs.path_util

TARGET_DIRECTORY_VALUE = "target_directory"
""" The target directory value """

class ContinuousIntegrationBuildAutomationExtension:
    """
    The continuous integration build automation extension class.
    """

    continuous_integration_build_automation_extension_plugin = None
    """ The continuous integration build automation extension plugin """

    def __init__(self, continuous_integration_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type continuous_integration_build_automation_extension_plugin: ContinuousIntegrationBuildAutomationExtensionPlugin
        @param continuous_integration_build_automation_extension_plugin: The continuous integration build automation extension plugin.
        """

        self.continuous_integration_build_automation_extension_plugin = continuous_integration_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure):
        # retrieves the deployment path
        deployment_path = parameters["deployment_path"]

        # retrieves the version file path
        version_file_path = parameters["version_file_path"]

        # retrieves the version from the version file path
        version = self._get_version(version_file_path)

        # converts the version to string
        version_string = str(version)

        deployment_version_path = deployment_path + "/" + version_string

        if not os.path.exists(deployment_version_path):
            os.makedirs(deployment_version_path)

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the target directory
        target_directory = build_properties[TARGET_DIRECTORY_VALUE]

        colony.libs.path_util.copy_directories(target_directory, deployment_version_path)

    def _get_version(self, version_file_path):
        # opens the version file
        version_file = open(version_file_path, "rb")

        try:
            # reads the revision number string value
            revision_number_string = version_file.read()

            # strips the revision number string
            revision_number_string = revision_number_string.strip()

            # converts the revision number string to integer
            revision_number = int(revision_number_string)
        finally:
            # closes the version file
            version_file.close()

        # returns the revision number
        return revision_number
