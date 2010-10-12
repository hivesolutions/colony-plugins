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

DEPLOYMENT_PATH_VALUE = "deployment_path"
""" The deployment path value """

VERSION_FILE_PATH_VALUE = "version_file_path"
""" The version file path value """

INTEGRATION_VERSION_VALUE = "integration_version"
""" The integration version value """

ZIP_VALUE = "zip"
""" The zip value """

LATEST_FILE_NAME = "LATEST.version"
""" The latest file name """

LATEST_DIRECTORY_NAME = "LATEST"
""" The latest file name """

ZIP_EXTENSION = ".zip"
""" The zip extension value """

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

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the deployment path
        deployment_path = parameters[DEPLOYMENT_PATH_VALUE]

        # retrieves the version file path
        version_file_path = parameters[VERSION_FILE_PATH_VALUE]

        # retrieves the zip values
        zips = parameters[ZIP_VALUE]

        # retrieves the version from the version file path
        version = self._get_version(version_file_path)

        # converts the version to string
        version_string = str(version)

        # creates the deployment version path, representing the
        # path to the directory to the current version
        deployment_version_path = deployment_path + "/" + version_string

        # in case the deployment version path does not exist
        if not os.path.exists(deployment_version_path):
            # creates the directories for the deployment version path
            os.makedirs(deployment_version_path)

        # creates the latest version path
        latest_version_path = deployment_path + "/" + LATEST_FILE_NAME

        # retrieves the current version (to check for changes)
        current_version = self._get_version(latest_version_path)

        # in case the current version is the same (no changes in repository)
        if version == current_version:
            # prints an info message
            logger.info("Skipping continuous integration, no changes in repository")

            # sets the skipped flag in the build automation structure runtime
            build_automation_structure_runtime.skipped = True

            # returns true (success)
            return True

        # writes the version number
        self._write_version_number(latest_version_path, version)

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the target directory
        target_directory = build_properties[TARGET_DIRECTORY_VALUE]

        # copies the target directory to the deployment version path (directory)
        colony.libs.path_util.copy_directory(target_directory, deployment_version_path)

        # retrieves the zip plugin
        zip_plugin = self.continuous_integration_build_automation_extension_plugin.zip_plugin

        # iterates over all the zip to create the zip file
        for zip in zips:
            # creates the zip file path
            zip_file_path = deployment_version_path + "/" + zip + ZIP_EXTENSION

            # creates the zip directory path
            zip_directory_path = deployment_version_path + "/" + zip

            # creates the zip file for the zip directory
            zip_plugin.zip(zip_file_path, zip_directory_path)

        # creates the latest version path
        latest_version_path = deployment_path + "/" + LATEST_DIRECTORY_NAME

        # in case there is an existent link in the latest path
        if os.path.islink(latest_version_path):
            # removes the latest version path
            os.remove(latest_version_path)
        # in case there is an existent directory in the latest path
        elif os.path.isdir(latest_version_path):
            # removes the latest version path (directory)
            colony.libs.path_util.remove_directory(latest_version_path)

        # creates a symbolic link between the deployment version path and the latest
        # version path
        colony.libs.path_util.link(deployment_version_path, latest_version_path)

        # sets the build automation structure runtime properties
        build_automation_structure_runtime.properties[INTEGRATION_VERSION_VALUE] = version

        # returns true (success)
        return True

    def _write_version_number(self, version_file_path, version_number):
        """
        Writes the given version number into the file in the given
        path.

        @type version_file_path: String
        @param version_file_path: The path to the file that will
        hold the version number.
        @type version_number: int
        @param version_number: The version number to be written.
        """

        # converts the version number to a string
        version_number_string = str(version_number)

        # opens the version file
        version_file = open(version_file_path, "wb")

        try:
            # writes the version number string value
            version_file.write(version_number_string)
        finally:
            # closes the version file
            version_file.close()

    def _get_version(self, version_file_path):
        """
        Retrieves the current version using the given
        version file path.

        @type version_file_path: String
        @param version_file_path: The file path to the
        version file.
        @rtype: int
        @return: The version (revision) number.
        """

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
