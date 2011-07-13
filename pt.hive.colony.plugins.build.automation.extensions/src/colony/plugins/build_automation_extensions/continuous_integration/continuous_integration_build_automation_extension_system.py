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

import colony.libs.map_util
import colony.libs.path_util

TARGET_DIRECTORY_VALUE = "target_directory"
""" The target directory value """

DEPLOYMENT_PATH_VALUE = "deployment_path"
""" The deployment path value """

VERSION_FILE_PATH_VALUE = "version_file_path"
""" The version file path value """

RELEASE_FILE_PATH_VALUE = "release_file_path"
""" The release file path value """

RELEASE_VALUE = "release"
""" The release value """

INTEGRATION_VERSION_VALUE = "integration_version"
""" The integration version value """

ZIP_VALUE = "zip"
""" The zip value """

LATEST_FILE_NAME = "LATEST.version"
""" The latest file name """

LATEST_SUCCESS_FILE_NAME = "LATEST_SUCCESS.version"
""" The latest success file name """

LATEST_RELEASE_FILE_NAME = "LATEST.release"
""" The latest release file name """

LATEST_SUCCESS_RELEASE_FILE_NAME = "LATEST_SUCCESS.release"
""" The latest success release file name """

LATEST_DIRECTORY_NAME = "LATEST"
""" The latest directory name """

LATEST_SUCCESS_DIRECTORY_NAME = "LATEST_SUCCESS"
""" The latest success directory name """

ZIP_EXTENSION = ".zip"
""" The zip extension value """

FIRST_RELEASE_NUMBER = 0
""" The first release number """

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

        # retrieves the release file path
        release_file_path = parameters[RELEASE_FILE_PATH_VALUE]

        # retrieves the zip values
        zips = colony.libs.map_util.map_get_values(parameters, ZIP_VALUE)

        try:
            # retrieves the version (hash) from the version file path
            version = self._get_version_hash(version_file_path)
        except:
            # invalidates the version
            version = None

        # in case the version is invalid
        if not version:
            # prints an info message
            logger.info("Skipping continuous integration, invalid version file")

            # sets the skipped flag in the build automation structure runtime
            build_automation_structure_runtime.skipped = True

            # returns true (success)
            return True

        try:
            # retrieves the release from the release file path
            release = self._get_release(release_file_path)
        except:
            # sets the "default" first release
            release = FIRST_RELEASE_NUMBER

        # increments the release number (new release)
        release += 1

        # converts the release to string
        release_string = str(release)

        # creates the deployment release path, representing the
        # path to the directory to the current release
        deployment_release_path = deployment_path + "/" + release_string

        # in case the deployment release path does not exist
        if not os.path.exists(deployment_release_path):
            # creates the directories for the deployment release path
            os.makedirs(deployment_release_path)

        # creates the latest file paths
        latest_version_path = deployment_path + "/" + LATEST_FILE_NAME
        latest_release_path = deployment_path + "/" + LATEST_RELEASE_FILE_NAME

        # creates the latest success file paths
        latest_success_version_path = deployment_path + "/" + LATEST_SUCCESS_FILE_NAME
        latest_success_release_path = deployment_path + "/" + LATEST_SUCCESS_RELEASE_FILE_NAME

        # retrieves the current version (to check for changes)
        current_version = self._get_version_hash(latest_version_path)

        # in case the current version is the same (no changes in repository)
        if version == current_version:
            # prints an info message
            logger.info("Skipping continuous integration, no changes in repository")

            # sets the skipped flag in the build automation structure runtime
            build_automation_structure_runtime.skipped = True

            # returns true (success)
            return True

        # prints an info message
        logger.info("Updating continuous integration, for release %s" % release_string)

        # writes the version hash and the release number to
        # the latest files
        self._write_version_hash(latest_version_path, version)
        self._write_release_number(latest_release_path, release)

        # in case the build is successful, updates the success files
        if build_automation_structure_runtime.success:
            # writes the version hash and the release number
            # to the success files
            self._write_version_hash(latest_success_version_path, version)
            self._write_release_number(latest_success_release_path, release)

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the target directory
        target_directory = build_properties[TARGET_DIRECTORY_VALUE]

        # copies the target directory to the deployment release path (directory)
        colony.libs.path_util.copy_directory(target_directory, deployment_release_path)

        # retrieves the zip plugin
        zip_plugin = self.continuous_integration_build_automation_extension_plugin.zip_plugin

        # iterates over all the zip to create the zip file
        for zip in zips:
            # creates the zip file path
            zip_file_path = deployment_release_path + "/" + zip + ZIP_EXTENSION

            # creates the zip directory path
            zip_directory_path = deployment_release_path + "/" + zip

            # creates the zip file for the zip directory
            zip_plugin.zip(zip_file_path, zip_directory_path)

        # creates the latest version path
        latest_version_path = deployment_path + "/" + LATEST_DIRECTORY_NAME

        # creates the latest success version path
        latest_success_version_path = deployment_path + "/" + LATEST_SUCCESS_DIRECTORY_NAME

        # updates the latest version path (link)
        self._update_link(deployment_release_path, latest_version_path)

        # in case the build is successful, updates the latest success version path (link)
        build_automation_structure_runtime.success and self._update_link(deployment_release_path, latest_success_version_path)

        # sets the build automation structure runtime properties
        build_automation_structure_runtime.local_properties[RELEASE_VALUE] = release
        build_automation_structure_runtime.local_properties[INTEGRATION_VERSION_VALUE] = version

        # returns true (success)
        return True

    def _update_link(self, target_path, link_path):
        """
        Updates the given link values.
        Testing for link and directory mode.

        @type target_path: String
        @param target_path: The target path to the link.
        @type link_path: String
        @param link_path: The path to the link.
        """

        # in case there is an existent link in the link path
        if os.path.islink(link_path):
            # removes the link path
            os.remove(link_path)
        # in case there is an existent directory in the link path
        elif os.path.isdir(link_path):
            # removes the link path (directory)
            colony.libs.path_util.remove_directory(link_path)

        # creates a symbolic link between the target
        # path and the link path
        colony.libs.path_util.link(target_path, link_path)

    def _write_version_hash(self, version_file_path, version_hash):
        """
        Writes the given version hash into the file in the given
        path.

        @type version_file_path: String
        @param version_file_path: The path to the file that will
        hold the version hash.
        @type version_hash: String
        @param version_hash: The version hash to be written.
        """

        # opens the version file
        version_file = open(version_file_path, "wb")

        try:
            # writes the version hash
            version_file.write(version_hash)
        finally:
            # closes the version file
            version_file.close()

    def _get_version_hash(self, version_file_path):
        """
        Retrieves the current version hash using the given
        version file path.

        @type version_file_path: String
        @param version_file_path: The file path to the
        version file.
        @rtype: String
        @return: The version hash value.
        """

        # in case the version file path does not exist
        if not os.path.exists(version_file_path):
            # returns invalid
            return None

        # opens the version file
        version_file = open(version_file_path, "rb")

        try:
            # reads the revision hash string value
            revision_hash_string = version_file.read()

            # strips the revision hash string
            revision_hash_string = revision_hash_string.strip()
        finally:
            # closes the version file
            version_file.close()

        # returns the revision hash string
        return revision_hash_string

    def _write_release_number(self, release_file_path, release_number):
        """
        Writes the given release number into the file in the given
        path.

        @type release_file_path: String
        @param release_file_path: The path to the file that will
        hold the release number.
        @type release_number: int
        @param release_number: The release number to be written.
        """

        # converts the release number to a string
        release_number_string = str(release_number)

        # opens the release file
        release_file = open(release_file_path, "wb")

        try:
            # writes the release number string value
            release_file.write(release_number_string)
        finally:
            # closes the release file
            release_file.close()

    def _get_release(self, release_file_path):
        """
        Retrieves the current release using the given
        release file path.

        @type release_file_path: String
        @param release_file_path: The file path to the
        release file.
        @rtype: int
        @return: The release number.
        """

        # in case the release file path does not exist
        if not os.path.exists(release_file_path):
            # returns (default first value)
            return FIRST_RELEASE_NUMBER

        # opens the release file
        release_file = open(release_file_path, "rb")

        try:
            # reads the release number string value
            release_number_string = release_file.read()

            # strips the release number string
            release_number_string = release_number_string.strip()

            # converts the release number string to integer
            release_number = int(release_number_string)
        finally:
            # closes the release file
            release_file.close()

        # returns the release number
        return release_number
