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

TARGET_VALUE = "target"
""" The target value """

class PluginRepositoryGeneratorBuildAutomationExtension:
    """
    The plugin repository generator build automation extension class.
    """

    plugin_repository_generator_build_automation_extension_plugin = None
    """ The plugin repository generator build automation extension plugin """

    def __init__(self, plugin_repository_generator_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type plugin_repository_generator_build_automation_extension_plugin: PluginRepositoryGeneratorBuildAutomationExtensionPlugin
        @param plugin_repository_generator_build_automation_extension_plugin: The plugin repository generator build automation extension plugin.
        """

        self.plugin_repository_generator_build_automation_extension_plugin = plugin_repository_generator_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure):
        # retrieves the plugin manager
        plugin_manager = self.plugin_repository_generator_build_automation_extension_plugin.manager

        # retrieves the repository descriptor generator plugin
        repository_descriptor_generator_plugin = self.plugin_repository_generator_build_automation_extension_plugin.repository_descriptor_generator_plugin

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the target directory
        target_directory = build_properties[TARGET_DIRECTORY_VALUE]

        # retrieves the repository name
        repository_name = parameters["repository_name"]

        # retrieves the repository description
        repository_description = parameters["repository_description"]

        # retrieves the repository layout
        repository_layout = parameters["repository_layout"]

        plugins = parameters.get("plugins", {})
        _plugins = plugins.get("plugin", [{"id" : value.id, "version" : value.version} for value in plugin_manager.get_all_loaded_plugins()])

        # retrieves the target
        target = parameters.get(TARGET_VALUE, target_directory)

        # creates the full target directory appending the colony plugins
        # suffix value
        full_target_directory = target + "/colony_plugins"

        # creates the full plugins directory
        full_plugins_directory = full_target_directory + "/plugins"

        if not os.path.exists(full_target_directory):
            os.makedirs(full_target_directory)

        if not os.path.exists(full_plugins_directory):
            os.makedirs(full_plugins_directory)

        # creates the repository descriptor file path
        repository_descriptor_file_path = full_target_directory + "/repository_descriptor.xml"

        # generates the repository descriptor file
        repository_descriptor_generator_plugin.generate_repository_descriptor_file(repository_descriptor_file_path, repository_name, repository_description, repository_layout)

        # iterates over all the plugins to copy the files
        for plugin in _plugins:
            # retrieves the plugin id and version
            plugin_id = plugin["id"]
            plugin_version = plugin["version"]

            # creates the plugin file name from the plugin id and version
            plugin_file_name = plugin_id + "_" + plugin_version + ".cpx"

            # in case the source plugin path does not exists
            if not os.path.exists(target_directory + "/" + plugin_file_name):
                # continues the loop
                continue

            colony.libs.path_util.copy_file(target_directory + "/" + plugin_file_name, full_plugins_directory + "/" + plugin_file_name)
