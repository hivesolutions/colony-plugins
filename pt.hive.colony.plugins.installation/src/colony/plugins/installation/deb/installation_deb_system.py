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

import installation_deb_exceptions

import colony.libs.path_util
import colony.libs.map_util

ADAPTER_NAME = "deb"
""" The adapter name """

FILE_PATH_VALUE = "file_path"
""" The file path value """

RESOURCES_PATH = "installation/deb/resources"
""" The resources path """

class InstallationDeb:
    """
    The installation deb class.
    """

    installation_deb_plugin = None
    """ The installation deb plugin """

    def __init__(self, installation_deb_plugin):
        """
        Constructor of the class.

        @type installation_deb_plugin: InstallationDebPlugin
        @param installation_deb_plugin: The installation deb plugin.
        """

        self.installation_deb_plugin = installation_deb_plugin

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

        # retrieves the plugin manager
        plugin_manager = self.installation_deb_plugin.manager

        # retrieves the packaging deb plugin
        packaging_deb_plugin = self.installation_deb_plugin.packaging_deb_plugin

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise installation_deb_exceptions.MissingParameter(FILE_PATH_VALUE)

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE]

        # retrieves the temporary plugin generated path
        temporary_plugin_generated_path = plugin_manager.get_temporary_plugin_generated_path_by_id(self.installation_deb_plugin.id)

        # in case the temporary path does not exists
        if not os.path.exists(temporary_plugin_generated_path):
            # creates the directories to the temporary path
            os.makedirs(temporary_plugin_generated_path)

        # generates the various control files
        control_file_contents = self._generate_control_file(parameters)
        config_file_contents = self._generate_config_file(parameters)
        prerm_file_contents = self._generate_prerm_file(parameters)
        postrm_file_contents = self._generate_postrm_file(parameters)
        postinst_file_contents = self._generate_postinst_file(parameters)

        # writes the various control files to the file system
        self._write_file_contents(temporary_plugin_generated_path, "control", control_file_contents)
        self._write_file_contents(temporary_plugin_generated_path, "config", config_file_contents)
        self._write_file_contents(temporary_plugin_generated_path, "prerm", prerm_file_contents)
        self._write_file_contents(temporary_plugin_generated_path, "postrm", postrm_file_contents)
        self._write_file_contents(temporary_plugin_generated_path, "postinst", postinst_file_contents)

        # creates the deb file parameters map
        deb_file_parameters = {"file_path" : file_path,
                               "file_format" : "tar_gz",
                               "deb_file_arguments" : {"control" : os.path.join(temporary_plugin_generated_path, "control"),
                                                       "config" : os.path.join(temporary_plugin_generated_path, "config"),
                                                       "prerm" : os.path.join(temporary_plugin_generated_path, "prerm"),
                                                       "postrm" : os.path.join(temporary_plugin_generated_path, "postrm"),
                                                       "postinst" : os.path.join(temporary_plugin_generated_path, "postinst")}}

        # creates the deb file
        deb_file = packaging_deb_plugin.create_file(deb_file_parameters)

        # opens the deb file
        deb_file.open("wb+")

        try:
            # processes the contents for the deb file
            self._process_contents(deb_file, parameters)
        finally:
            # closes the deb file
            deb_file.close()

        # removes the used directory
        colony.libs.path_util.remove_directory(temporary_plugin_generated_path)

    def _process_contents(self, deb_file, parameters):
        # retrieves the contents map from the parameters
        contents = parameters["contents"]

        # retrieves the content references
        directories = contents.get("directory", [])
        files = contents.get("file", [])
        links = contents.get("link", [])

        # iterates over all the directories
        # to write their contents into the deb files
        for directory in directories:
            # retrieves the file path
            directory_path = directory.get("path", None)

            # retrieves the directory recursive value
            directory_recursive = directory.get("recursive", True)

            # retrieves the file target
            directory_target = directory["parameters"]["deb"]["target"]

            # writes the file to the deb file
            self._process_directory_contents(deb_file, directory_path, directory_target, directory_recursive)

        # iterates over all the (simple) files
        # to write them into the deb file
        for file in files:
            # retrieves the file path
            file_path = file["path"]

            # retrieves the file target
            file_target = file["parameters"]["deb"]["target"]

            # writes the file to the deb file
            deb_file.write(file_path, file_target)

        # iterates over all the links
        # to put them into the deb file
        for link in links:
            # retrieves the link source
            link_source = link["parameters"]["deb"]["source"]

            # retrieves the link source
            link_target = link["parameters"]["deb"]["target"]

            # writes the file to the deb file
            deb_file.write_string_value("", link_source, {"file_properties" : {"type" : "link",
                                                                               "link_name" : link_target}})

    def _process_directory_contents(self, deb_file, directory_path, directory_target, recursive = True):
        # writes the directory registry in the deb file
        deb_file.write_string_value("", directory_target, {"file_properties" : {"type" : "directory"}})

        # in case no directory path is defined
        if not directory_path:
            # returns immediately
            return

        # retrieves the directory contents
        directory_contents = os.listdir(directory_path)

        import re

        # @todo: GENERALIZE THESE CONTENTS
        exclusion_regex = re.compile("(.*.svn$)|(.*.pyc$)")

        # iterates over the directory contents
        for directory_item in directory_contents:
            if exclusion_regex.match(directory_item):
                continue

            directory_item_path = directory_path + "/" + directory_item

            directory_item_target = directory_target + "/" + directory_item

            # in case the directory item is a directory
            if os.path.isdir(directory_item_path):
                # in case the recursive flag is active processes the inner directory
                recursive and self._process_directory_contents(deb_file, directory_item_path, directory_item_target, recursive)
            else:
                # writes the directory item (file) to the deb file
                deb_file.write(directory_item_path, directory_item_target)

    def _write_file_contents(self, temporary_path, file_name, file_contents):
        # create the complete file path by append the file name
        complete_file_path = temporary_path + "/" + file_name

        # normalizes the complete file path
        complete_file_path_normalized = colony.libs.path_util.normalize_path(complete_file_path)

        # opens the file
        file = open(complete_file_path_normalized, "wb")

        try:
            # writes the file contents to the file
            file.write(file_contents)
        finally:
            # closes the file
            file.close()

    def _generate_config_file(self, parameters):
        return self._process_template_file("config.tpl", {})

    def _generate_prerm_file(self, parameters):
        return self._process_template_file("prerm.tpl", {})

    def _generate_postrm_file(self, parameters):
        return self._process_template_file("postrm.tpl", {})

    def _generate_postinst_file(self, parameters):
        return self._process_template_file("postinst.tpl", {})

    def _generate_control_file(self, parameters):
        # retrieves the package parameters from the parameters
        package_parameters = parameters.get("package", {})

        # checks the mandatory package parameters
        colony.libs.map_util.map_check_parameters(package_parameters, ("package_name", "package_version"), installation_deb_exceptions.MissingParameter)

        # retrieves the mandatory attributes
        package_name = package_parameters["package_name"]
        package_version = package_parameters["package_version"]

        # retrieves the conditional attributes
        pacakge_section = package_parameters.get("package_section", "devel")
        pacakge_priority = package_parameters.get("package_priority", "optional")
        package_architecture = package_parameters.get("package_architecture", "all")
        package_essential = package_parameters.get("package_essential", "no")
        package_dependencies = package_parameters.get("package_dependencies", "")
        package_pre_dependencies = package_parameters.get("package_pre_dependencies", "bash")
        package_installed_size = package_parameters.get("package_installed_size", "0")
        package_maintainer = package_parameters.get("package_maintainer", "Hive Solutions <development@hive.pt>")
        package_provides = package_parameters.get("package_provides", package_name)
        package_replaces = package_parameters.get("package_replaces", "")
        package_description = package_parameters.get("package_description", "")

        # creates the parameters map
        parameters_map = {"package" : {"name" : package_name,
                                       "version" : package_version,
                                       "section" : pacakge_section,
                                       "priority" : pacakge_priority,
                                       "architecture" : package_architecture,
                                       "essential" : package_essential,
                                       "dependencies" : package_dependencies,
                                       "pre_dependencies" : package_pre_dependencies,
                                       "installed_size" : package_installed_size,
                                       "maintainer" : package_maintainer,
                                       "provides" : package_provides,
                                       "replaces" : package_replaces,
                                       "description" : package_description}}

        return self._process_template_file("control.tpl", parameters_map)

    def _process_template_file(self, template_file_name, parameters_map):
        # retrieves the plugin manager
        plugin_manager = self.installation_deb_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.installation_deb_plugin.template_engine_manager_plugin

        # retrieves the installation plugin path
        installation_deb_plugin_path = plugin_manager.get_plugin_path_by_id(self.installation_deb_plugin.id)

        # creates the full template file path
        template_file_path = installation_deb_plugin_path + "/" + RESOURCES_PATH + "/control_file_templates/" + template_file_name

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path(template_file_path)

        for parameter_name, parameter_value in parameters_map.items():
            # assigns the parameter to the template file
            template_file.assign(parameter_name, parameter_value)

        # processes the template file
        processed_template_file = template_file.process()

        # decodes the processed template file into a unicode object
        processed_template_file_decoded = processed_template_file.decode("Cp1252")

        # returns the processed template file decoded
        return processed_template_file_decoded
