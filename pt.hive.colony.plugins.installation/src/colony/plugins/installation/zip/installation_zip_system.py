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

import os
import re
import time
import zipfile

import colony.libs.map_util

import installation_zip_exceptions

ADAPTER_NAME = "zip"
""" The adapter name """

FILE_EXTENSION_VALUE = ".zip"
""" The file extension value """

PACKAGE_VALUE = "package"
""" The package value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

PACKAGE_VERSION_VALUE = "package_version"
""" The package name value """

PACKAGE_ARCHITECTURE_VALUE = "package_architecture"
""" The package architecture value """

NAME_SEPARATION_TOKEN = "_"
""" The name separation token """

EMPTY_REGEX_VALUE = "$"
""" The empty regex value """

class InstallationZip:
    """
    The installation zip class.
    """

    installation_zip_plugin = None
    """ The installation zip plugin """

    def __init__(self, installation_zip_plugin):
        """
        Constructor of the class.

        @type installation_zip_plugin: InstallationZipPlugin
        @param installation_zip_plugin: The installation zip plugin.
        """

        self.installation_zip_plugin = installation_zip_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def generate_installation_file(self, parameters):
        """
        Generates the installation file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the installation file generation.
        """

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise installation_zip_exceptions.MissingParameter(FILE_PATH_VALUE)

        # retrieves the package from the parameters
        package = parameters[PACKAGE_VALUE]

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE] + NAME_SEPARATION_TOKEN + package[PACKAGE_VERSION_VALUE] + NAME_SEPARATION_TOKEN + package[PACKAGE_ARCHITECTURE_VALUE] + FILE_EXTENSION_VALUE

        # creates the zip file
        zip_file = zipfile.ZipFile(file_path, "w")

        try:
            # processes the contents for the zip file
            self._process_contents(zip_file, parameters)
        finally:
            # closes the zip file
            zip_file.close()

    def _process_contents(self, zip_file, parameters):
        """
        Processes the contents of the zip file using
        the given parameters map.

        @type zip_file: ZipFile
        @param zip_file: The zip file to be used for processing.
        @type parameters: Dictionary
        @param parameters: The parameters for processing.
        """

        # retrieves the contents map from the parameters
        contents = parameters["contents"]

        # retrieves the exclusions list
        exclusions = contents.get("exclusions", {})
        exclusions_list = colony.libs.map_util.map_get_values(exclusions, "exclusion")

        # retrieves the content references
        directories = colony.libs.map_util.map_get_values(contents, "directory")
        files = colony.libs.map_util.map_get_values(contents, "file")

        # processes the exclusion regex from the exclusions list
        exclusion_regex = self._process_exclusion_regex(exclusions_list)

        # iterates over all the directories
        # to write their contents into the zip files
        for directory in directories:
            # retrieves the parameters
            directory_parameters = directory.get("parameters", {})

            # retrieves the parameters zip
            directory_parameters_zip = directory_parameters.get("zip", {})

            # retrieves the file path
            directory_path = directory.get("path", directory_parameters_zip.get("path", None))

            # retrieves the directory recursive value
            directory_recursive = directory.get("recursive", "true") == "true"

            # retrieves the directory owner value
            directory_owner = int(directory.get("owner", "0"))

            # retrieves the directory group value
            directory_group = int(directory.get("group", "0"))

            # retrieves the directory mode value
            directory_mode = int(directory.get("mode", "0"), 8)

            # retrieves the file target
            directory_target = directory_parameters_zip.get("target", None)

            # writes the file to the zip file
            self._process_directory_contents(zip_file, directory_path, directory_target, directory_recursive, directory_owner, directory_group, directory_mode, exclusion_regex)

        # iterates over all the (simple) files
        # to write them into the zip file
        for file in files:
            # retrieves the parameters
            file_parameters = file.get("parameters", {})

            # retrieves the parameters zip
            file_parameters_zip = file_parameters.get("zip", {})

            # retrieves the file path
            file_path = file.get("path", file_parameters_zip.get("path", None))

            # retrieves the file target
            file_target = file_parameters_zip.get("target", None)

            # writes the file to the zip file
            zip_file.write(file_path, file_target)

    def _process_directory_contents(self, zip_file, directory_path, directory_target, recursive = True, directory_owner = 0, directory_group = 0, directory_mode = 0, exclusion_regex = None):
        # in case no target directory is defined
        if not directory_target:
            # returns immediately
            return

        # retrieves the current valid local time to update
        # the zip information
        current_time = time.time()
        current_local_time = time.localtime(current_time)
        current_valid_local_time = current_local_time[:6]

        # calculates the permission value (octal based value)
        permissions_value = directory_owner * 64 + directory_group * 8 + directory_mode

        # creates the zip info structure to hold
        # the directory entry information
        zip_info = zipfile.ZipInfo(directory_target + "/", current_valid_local_time)

        # sets the external attribute to directory
        zip_info.external_attr = 48 | permissions_value << 16

        # writes the zip info information to the zip file
        zip_file.writestr(zip_info, "")

        # in case no directory path is defined
        if not directory_path:
            # returns immediately
            return

        # retrieves the directory contents
        directory_contents = os.listdir(directory_path)

        # iterates over the directory contents
        for directory_item in directory_contents:
            # in case the directory item matches the exclusion regular
            # expression (it's invalid)
            if exclusion_regex.match(directory_item):
                # continues the loop
                continue

            # creates the directory item path (using the directory path)
            directory_item_path = directory_path + "/" + directory_item

            # creates the directory item target (using the directory target)
            directory_item_target = directory_target + "/" + directory_item

            # in case the directory item is a directory
            if os.path.isdir(directory_item_path):
                # in case the recursive flag is active processes the inner directory
                recursive and self._process_directory_contents(zip_file, directory_item_path, directory_item_target, recursive, directory_owner, directory_group, directory_mode, exclusion_regex)
            else:
                # writes the directory item (file) to the zip file
                zip_file.write(directory_item_path, directory_item_target)

    def _process_exclusion_regex(self, exclusions_list):
        # creates the exclusion regex buffer
        exclusion_regex_buffer = colony.libs.string_buffer_util.StringBuffer()

        # sets the is first flag
        is_first = True

        # iterates over all the exclusion items in the
        # exclusions list
        for exclusion_item in exclusions_list:
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the exclusions regex buffer
                exclusion_regex_buffer.write("|")

            # adds the exclusion item to the exclusion regex buffer
            exclusion_regex_buffer.write("(" + exclusion_item + ")")

        # retrieves the exclusion regex value
        exclusion_regex_value = exclusion_regex_buffer.get_value()

        # creates the (real) exclusion regex value using the empty
        # regex value as fall-back
        exclusion_regex_value = exclusion_regex_value or EMPTY_REGEX_VALUE

        # compiles the exclusion regex value, retrieving the exclusion regex
        exclusion_regex = re.compile(exclusion_regex_value)

        # returns the exclusion regex
        return exclusion_regex
