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
import re

import installation_deb_exceptions

import colony.libs.map_util
import colony.libs.path_util
import colony.libs.string_buffer_util

DEFAULT_ENCODING = "Cp1252"
""" The default encoding """

ADAPTER_NAME = "deb"
""" The adapter name """

FILE_EXTENSION_VALUE = ".deb"
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

RESOURCES_PATH = "installation/deb/resources"
""" The resources path """

EMPTY_REGEX_VALUE = "$"
""" The empty regex value """

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

        # retrieves the package from the parameters
        package = parameters[PACKAGE_VALUE]

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE] + NAME_SEPARATION_TOKEN + package[PACKAGE_VERSION_VALUE] + NAME_SEPARATION_TOKEN + package[PACKAGE_ARCHITECTURE_VALUE] + FILE_EXTENSION_VALUE

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

        # retrieves the exclusions list
        exclusions = contents.get("exclusions", {})
        exclusions_list = colony.libs.map_util.map_get_values(exclusions, "exclusion")

        # retrieves the content references
        directories = colony.libs.map_util.map_get_values(contents, "directory")
        files = colony.libs.map_util.map_get_values(contents, "file")
        links = colony.libs.map_util.map_get_values(contents, "link")

        # processes the exclusion regex from the exclusions list
        exclusion_regex = self._process_exclusion_regex(exclusions_list)

        # iterates over all the directories
        # to write their contents into the deb files
        for directory in directories:
            # retrieves the parameters
            directory_parameters = directory.get("parameters", {})

            # retrieves the parameters deb
            directory_parameters_deb = directory_parameters.get("deb", {})

            # retrieves the file path
            directory_path = directory.get("path", directory_parameters_deb.get("path", None))

            # retrieves the directory recursive value
            directory_recursive = directory.get("recursive", True)

            # retrieves the directory owner value
            directory_owner = int(directory.get("owner", "0"))

            # retrieves the directory group value
            directory_group = int(directory.get("group", "0"))

            # retrieves the directory mode value
            directory_mode = int(directory.get("mode", "0"), 8)

            # retrieves the file target
            directory_target = directory_parameters_deb["target"]

            # writes the file to the deb file
            self._process_directory_contents(deb_file, directory_path, directory_target, directory_recursive, directory_owner, directory_group, directory_mode, exclusion_regex)

        # iterates over all the (simple) files
        # to write them into the deb file
        for file in files:
            # retrieves the parameters
            file_parameters = file.get("parameters", {})

            # retrieves the parameters deb
            file_parameters_deb = file_parameters.get("deb", {})

            # retrieves the file path
            file_path = file.get("path", file_parameters_deb.get("path", None))

            # retrieves the file owner value
            file_owner = int(file.get("owner", "0"))

            # retrieves the file group value
            file_group = int(file.get("group", "0"))

            # retrieves the file mode value
            file_mode = int(file.get("mode", "0"), 8)

            # retrieves the file target
            file_target = file_parameters_deb["target"]

            # writes the file to the deb file
            deb_file.write(file_path, file_target, {"file_properties" : {"owner" : file_owner,
                                                                         "group" : file_group,
                                                                         "mode" : file_mode}})

        # iterates over all the links
        # to put them into the deb file
        for link in links:
            # retrieves the link owner value
            link_owner = int(link.get("owner", "0"))

            # retrieves the link group value
            link_group = int(link.get("group", "0"))

            # retrieves the link mode value
            link_mode = int(link.get("mode", "0"), 8)

            # retrieves the link source
            link_source = link["parameters"]["deb"]["source"]

            # retrieves the link source
            link_target = link["parameters"]["deb"]["target"]

            # writes the link to the deb file
            deb_file.write_register_value(link_source, {"file_properties" : {"type" : "link",
                                                                             "link_name" : link_target,
                                                                             "owner" : link_owner,
                                                                             "group" : link_group,
                                                                             "mode" : link_mode}})

    def _process_directory_contents(self, deb_file, directory_path, directory_target, recursive = True, directory_owner = 0, directory_group = 0, directory_mode = 0, exclusion_regex = None):
        # writes the directory register in the deb file
        deb_file.write_register_value(directory_target, {"file_properties" : {"type" : "directory",
                                                                              "owner" : directory_owner,
                                                                              "group" : directory_group,
                                                                              "mode" : directory_mode}})

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
                recursive and self._process_directory_contents(deb_file, directory_item_path, directory_item_target, recursive, directory_owner, directory_group, directory_mode, exclusion_regex)
            else:
                # writes the directory item (file) to the deb file
                deb_file.write(directory_item_path, directory_item_target, {"file_properties" : {"owner" : directory_owner,
                                                                                                 "group" : directory_group,
                                                                                                 "mode" : directory_mode}})

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
        return self._process_template_file("config.tpl.sh", {})

    def _generate_prerm_file(self, parameters):
        # retrieves the package parameters from the parameters
        package_parameters = parameters.get("package", {})

        # retrieves the package parameters from the package parameters
        package_parameters_parameters = package_parameters.get("parameters", {})

        # retrieves the package parameters deb from the package parameters
        package_parameters_deb_parameters = package_parameters_parameters.get("deb", {})

        # retrieves the prerm value
        postinst = package_parameters_deb_parameters.get("prerm", "")

        return self._process_template_file("prerm.tpl.sh", {"prerm" : postinst})

    def _generate_postrm_file(self, parameters):
        return self._process_template_file("postrm.tpl.sh", {})

    def _generate_postinst_file(self, parameters):
        # retrieves the package parameters from the parameters
        package_parameters = parameters.get("package", {})

        # retrieves the package parameters from the package parameters
        package_parameters_parameters = package_parameters.get("parameters", {})

        # retrieves the package parameters deb from the package parameters
        package_parameters_deb_parameters = package_parameters_parameters.get("deb", {})

        # retrieves the postinst value
        postinst = package_parameters_deb_parameters.get("postinst", "")

        return self._process_template_file("postinst.tpl.sh", {"postinst" : postinst})

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
        package_maintainer = package_parameters.get("package_maintainer", "")
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

        return self._process_template_file("control.tpl.sh", parameters_map)

    def _process_template_file(self, template_file_name, parameters_map):
        # retrieves the plugin manager
        plugin_manager = self.installation_deb_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.installation_deb_plugin.template_engine_manager_plugin

        # retrieves the installation deb plugin path
        installation_deb_plugin_path = plugin_manager.get_plugin_path_by_id(self.installation_deb_plugin.id)

        # creates the full template file path
        template_file_path = installation_deb_plugin_path + "/" + RESOURCES_PATH + "/control_file_templates/" + template_file_name

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path_variable_encoding(template_file_path, DEFAULT_ENCODING, None)

        # iterates over all the parameters in the parameters map to
        # assign them to the template
        for parameter_name, parameter_value in parameters_map.items():
            # assigns the parameter to the template file
            template_file.assign(parameter_name, parameter_value)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.decode(DEFAULT_ENCODING)

        # returns the processed template file encoded
        return processed_template_file_encoded

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
