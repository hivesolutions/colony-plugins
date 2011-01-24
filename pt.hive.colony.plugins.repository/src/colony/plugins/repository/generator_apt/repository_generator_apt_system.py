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

__revision__ = "$LastChangedRevision: 8461 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-05-12 06:45:34 +0100 (qua, 12 Mai 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import gzip
import hashlib

import colony.libs.map_util
import colony.libs.path_util
import colony.libs.string_buffer_util

DEFAULT_ENCODING = "Cp1252"
""" The default encoding """

BUFFER_SIZE = 4096
""" The buffer size """

ADAPTER_NAME = "apt"
""" The adapter name """

SOURCE_VALUE = "source"
""" The source value """

TARGET_VALUE = "target"
""" The target value """

CONTENTS_VALUE = "contents"
""" The contents value """

FILE_VALUE = "file"
""" The file value """

NAME_VALUE = "name"
""" The name value """

VERSION_VALUE = "version"
""" The version value """

ARCHITECTURE_VALUE = "architecture"
""" The architecture value """

NAME_SEPARATION_TOKEN = "_"
""" The name separation token """

FILE_EXTENSION_VALUE = ".deb"
""" The file extension value """

RESOURCES_PATH = "repository/generator_apt/resources"
""" The resources path """

DEFAULT_FILE_FORMAT = "tar_gz"
""" The default file format """

class RepositoryGeneratorApt:
    """
    The repository generator apt class.
    """

    repository_generator_apt_plugin = None
    """ The repository generator apt plugin """

    def __init__(self, repository_generator_apt_plugin):
        """
        Constructor of the class.

        @type repository_generator_apt_plugin: RepositoryGeneratorAptPlugin
        @param repository_generator_apt_plugin: The repository generator apt plugin.
        """

        self.repository_generator_apt_plugin = repository_generator_apt_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def generate_repository(self, parameters):
        """
        Generates a repository for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the repository generation.
        """

        # retrieves the packaging deb plugin
        packaging_deb_plugin = self.repository_generator_apt_plugin.packaging_deb_plugin

        # retrieves the source from the parameters
        source = parameters[SOURCE_VALUE]

        # retrieves the target from the parameters
        target = parameters[TARGET_VALUE]

        # creates the target (apt) directory
        target_apt = target + "/" + ADAPTER_NAME

        # in case the target (apt) path does not exist
        if not os.path.exists(target_apt):
            # creates the target (apt) directories
            os.makedirs(target_apt)

        # retrieves the contents from the parameters
        contents = parameters[CONTENTS_VALUE]

        # retrieves the file from the parameters
        files = colony.libs.map_util.map_get_values(contents, FILE_VALUE)

        # creates the list to hold the various package maps
        packages_list = []

        # iterates over all the files to process them
        for file in files:
            # retrieves the file attributes
            file_name = file[NAME_VALUE]
            file_version = file.get(VERSION_VALUE, "1.0.0")
            file_architecture = file.get(ARCHITECTURE_VALUE, "all")

            # creates the complete file name, according to the deb specification
            complete_file_name = file_name + NAME_SEPARATION_TOKEN + file_version + NAME_SEPARATION_TOKEN + file_architecture + FILE_EXTENSION_VALUE

            # creates the complete file path prepending the source path
            complete_file_path = source + "/" + complete_file_name

            # creates the complete target file name according to the adapter name directory
            complete_target_file_name = ADAPTER_NAME + "/" + complete_file_name

            # creates the complete target file path
            complete_target_file_path = target_apt + "/" + complete_file_name

            # copies the file to the complete target path
            colony.libs.path_util.copy_file(complete_file_path, complete_target_file_path)

            # creates the deb file parameters map
            deb_file_parameters = {"file_path" : complete_file_path,
                                   "file_format" : DEFAULT_FILE_FORMAT}

            # creates the deb file
            deb_file = packaging_deb_plugin.create_file(deb_file_parameters)

            # opens the deb file
            deb_file.open("rb")

            try:
                # retrieves the control map
                control_map = deb_file.get_control_map()
            finally:
                # closes the deb file
                deb_file.close()

            # retrieves the control contents from the control map
            control_contents = control_map.get("control", "")

            # decodes the control contents
            control_contents = control_contents.decode("utf-8")

            # retrieves the various lines from the control contents
            lines = [value.strip() for value in control_contents.split("\n")]

            # creates the control values map
            control_values_map = {}

            # iterates over all the lines
            for line in lines:
                # in case the line is not valid
                if not line:
                    # continues the loop
                    continue

                # splits the line around the divisor
                key, value = line.split(":")

                # strips the key and value
                key = key.strip()
                value = value.strip()

                # sets the value in the control values map
                control_values_map[key] = value

            # opens the deb file
            deb_file = open(complete_file_path, "rb")

            try:
                # seeks the deb file to the final position
                deb_file.seek(0, os.SEEK_END)

                # retrieves the deb file size
                deb_file_size = deb_file.tell()

                # returns the deb file to the initial position
                deb_file.seek(0, os.SEEK_SET)

                # creates the has objects
                deb_file_md5 = hashlib.md5()
                deb_file_sha1 = hashlib.sha1()
                deb_file_sha256 = hashlib.sha256()

                # iterates continuously
                while True:
                    # reads contents from the deb file
                    deb_file_contents = deb_file.read(BUFFER_SIZE)

                    # in case no deb file contents are
                    # read
                    if not deb_file_contents:
                        # breaks the cycle
                        break

                    # updates the hash values
                    deb_file_md5.update(deb_file_contents)
                    deb_file_sha1.update(deb_file_contents)
                    deb_file_sha256.update(deb_file_contents)
            finally:
                # closes the deb file
                deb_file.close()

            # retrieves the hash hexadecimal digest values
            deb_file_md5_digest = deb_file_md5.hexdigest()
            deb_file_sha1_digest = deb_file_sha1.hexdigest()
            deb_file_sha256_digest = deb_file_sha256.hexdigest()

            # creates the package map
            package_map = {"name" : control_values_map.get("Package", ""),
                           "version" : control_values_map.get("Version", "1.0.0"),
                           "architecture" : control_values_map.get("Architecture", "all"),
                           "essential" : control_values_map.get("Essential", "no"),
                           "maintainer" : control_values_map.get("Maintainer", ""),
                           "installed_size" : control_values_map.get("Installed-Size", "0"),
                           "pre_dependencies" : control_values_map.get("Pre-Depends", None),
                           "dependencies" : control_values_map.get("Depends", ""),
                           "replaces" : control_values_map.get("Replaces", None),
                           "provides" : control_values_map.get("Provides", None),
                           "filename" : complete_target_file_name,
                           "size" : deb_file_size,
                           "md5" : deb_file_md5_digest,
                           "sha1" : deb_file_sha1_digest,
                           "sha256" : deb_file_sha256_digest,
                           "section" : control_values_map.get("Section", None),
                           "priority" : control_values_map.get("Priority", None),
                           "description" : control_values_map.get("Description", None)}

            # adds the packages map to the packages list
            packages_list.append(package_map)

        # processes the template file, retrieving the packages contents
        packages_contents = self._process_template_file("packages.tpl", {"packages" : packages_list})

        # creates the buffer to hold the package contents compressed
        packages_contents_compressed_buffer = colony.libs.string_buffer_util.StringBuffer()

        # opens the packages file compressed
        packages_file_compressed = gzip.GzipFile("Packages", "wb", 1, packages_contents_compressed_buffer)

        try:
            # writes the packages contents to the packages
            # file compressed
            packages_file_compressed.write(packages_contents)
        finally:
            # closes the packages file
            packages_file_compressed.close()

        # retrieves the value from the buffer (compressed)
        packages_contents_compressed = packages_contents_compressed_buffer.get_value()

        # writes the packages contents to the
        # packages file
        self._write_file(target_apt + "/Packages", packages_contents)

        # writes the packages contents compressed to the
        # packages compressed file
        self._write_file(target_apt + "/Packages.gz", packages_contents_compressed)

    def _process_template_file(self, template_file_name, parameters_map):
        # retrieves the plugin manager
        plugin_manager = self.repository_generator_apt_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.repository_generator_apt_plugin.template_engine_manager_plugin

        # retrieves the repository generator apt plugin path
        repository_generator_apt_plugin_path = plugin_manager.get_plugin_path_by_id(self.repository_generator_apt_plugin.id)

        # creates the full template file path
        template_file_path = repository_generator_apt_plugin_path + "/" + RESOURCES_PATH + "/repository_templates/" + template_file_name

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path_encoding(template_file_path, DEFAULT_ENCODING)

        # iterates over all the parameters in the parameters map to
        # assign them to the template
        for parameter_name, parameter_value in parameters_map.items():
            # assigns the parameter to the template file
            template_file.assign(parameter_name, parameter_value)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.encode(DEFAULT_ENCODING)

        # returns the processed template file encoded
        return processed_template_file_encoded

    def _write_file(self, file_path, contents):
        """
        Writes the contents to the file in the given
        file path.

        @type file_path: String
        @param file_path: The path to the file to write.
        @type contents: String
        @param contents: The contents to be written.
        """

        # opens the file for writing
        file = open(file_path, "wb")

        try:
            # writes the contents
            file.write(contents)
        finally:
            # closes the file
            file.close()
