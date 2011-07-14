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

import izpack_build_automation_extension_exceptions

class IzpackBuildAutomationExtension:
    """
    The izpack build automation extension class.
    """

    izpack_build_automation_extension_plugin = None
    """ The izpack build automation extension plugin """

    def __init__(self, izpack_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type izpack_build_automation_extension_plugin: IzpackBuildAutomationExtensionPlugin
        @param izpack_build_automation_extension_plugin: The izpack build automation extension plugin.
        """

        self.izpack_build_automation_extension_plugin = izpack_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the plugin manager
        manager = self.izpack_build_automation_extension_plugin.manager

        # retrieves the resource manager plugin
        resource_manager_plugin = self.izpack_build_automation_extension_plugin.resource_manager_plugin

        # retrieves the execution environment plugin
        execution_environment_plugin = self.izpack_build_automation_extension_plugin.execution_environment_plugin

        # retrieves the command execution plugin
        command_execution_plugin = self.izpack_build_automation_extension_plugin.command_execution_plugin

        # retrieves the izpack home path resource
        izpack_home_path_resource = resource_manager_plugin.get_resource("system.path.izpack_home")

        # in case the izpack_home resource is not defined
        if not izpack_home_path_resource:
            raise izpack_build_automation_extension_exceptions.IzpackNotFoundException("izpack configuration not found")

        # retrieves the izpack home path value
        izpack_home_path = izpack_home_path_resource.data

        # in case the path does not exists
        if not os.path.exists(izpack_home_path):
            raise izpack_build_automation_extension_exceptions.IzpackNotFoundException("izpack home directory not found")

        # retrieves the current operative system
        current_operative_system = execution_environment_plugin.get_operative_system()

        # in case the current environment is windows
        if current_operative_system == "windows":
            # creates the execution command
            izpack_execution_command = izpack_home_path + "/compile.bat"
        # in case the current environment is mac
        elif current_operative_system == "mac":
            # creates the execution command
            izpack_execution_command = izpack_home_path + "/compile"
        # in case the current environment is unix
        elif current_operative_system == "unix":
            # creates the execution command
            izpack_execution_command = izpack_home_path + "/compile"

        # retrieves the base directory path from the given parameters
        base_directory_path = parameters["base_directory"]

        # retrieves the install file path from the given parameters
        install_file_path = parameters["install_file"]

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the target directory path value
        target_directory_path = build_properties["target_directory"]

        # creates the output file full path
        output_file_full_path = target_directory_path + "/installer.jar"

        # converts the output file path to absolute value
        output_file_full_absolute_path = os.path.abspath(output_file_full_path)

        # retrieves the main logger
        logger = manager.logger

        # executes the compilation command
        command_execution_plugin.execute_command_logger_execution_directory(izpack_execution_command, [install_file_path, "-o", output_file_full_absolute_path], logger, base_directory_path)

        # returns true (success)
        return True
