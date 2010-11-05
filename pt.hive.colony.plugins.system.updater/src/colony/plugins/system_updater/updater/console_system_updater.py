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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "system_updater"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### SYSTEM UPDATER HELP ###\n\
list_repositories                              - lists the current available repositories\n\
list_repository_packages <repository-name>     - lists the packages for the given repository\n\
list_repository_bundles <repository-name>      - lists the bundles for the given repository\n\
list_repository_plugins <repository-name>      - lists the plugins for the given repository\n\
install <id> [version]                         - installs the package, bundle or plugin with the given id and version\n\
install_package <package-id> [package-version] - installs the package with the given id and version\n\
install_bundle <bundle-id> [bundle-version]    - installs the bundle with the given id and version\n\
install_plugin <plugin-id> [plugin-version]    - installs the plugin with the given id and version"
""" The help text """

class ConsoleSystemUpdater:
    """
    The console system updater class.
    """

    system_updater_plugin = None
    """ The system updater plugin """

    commands = ["list_repositories", "list_repository_packages", "list_repository_plugins", "install_package", "install_plugin"]
    """ The commands list """

    def __init__(self, system_updater_plugin):
        """
        Constructor of the class.

        @type system_updater_plugin: SystemUpdaterPlugin
        @param system_updater_plugin: The system updater plugin.
        """

        self.system_updater_plugin = system_updater_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_list_repositories(self, args, output_method):

        repositories_list = self.system_updater_plugin.system_updater.get_repositories()

        for repository in repositories_list:
            self.print_repository_info(repository, output_method)

    def process_list_repository_packages(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        repository_name = args[0]

        package_information_list = self.system_updater_plugin.system_updater.get_package_information_list_by_repository_name(repository_name)

        for package_information in package_information_list:
            self.print_package_info(package_information, output_method)

    def process_list_repository_plugins(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        repository_name = args[0]

        plugin_information_list = self.system_updater_plugin.system_updater.get_plugin_information_list_by_repository_name(repository_name)

        for plugin_information in plugin_information_list:
            self.print_plugin_info(plugin_information, output_method)

    def process_install_package(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        package_identifier = args[0]

        if len(args) == 1:
            self.system_updater_plugin.system_updater.install_package(package_identifier)
        else:
            package_version = args[1]
            self.system_updater_plugin.system_updater.install_package(package_identifier, package_version)

    def process_install_plugin(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_identifier = args[0]

        if len(args) == 1:
            self.system_updater_plugin.system_updater.install_plugin(plugin_identifier)
        else:
            plugin_version = args[1]
            self.system_updater_plugin.system_updater.install_plugin(plugin_identifier, plugin_version)

    def print_repository_info(self, repository, output_method):
        output_method("name:        " + repository.name)
        output_method("description: " + repository.description)
        output_method("addresses:   " + str(repository.addresses))

    def print_package_info(self, package_information, output_method):
        output_method("name:    " + package_information.name)
        output_method("type:    " + package_information.package_type)
        output_method("id:      " + package_information.id)
        output_method("version: " + package_information.version)
        output_method("plugins: " + str(package_information.plugins))

    def print_plugin_info(self, plugin_information, output_method):
        output_method("name:          " + plugin_information.name)
        output_method("type:          " + plugin_information.plugin_type)
        output_method("id:            " + plugin_information.id)
        output_method("version:       " + plugin_information.version)
        output_method("main_module:   " + plugin_information.main_module)
        output_method("main_class:    " + plugin_information.main_class)
        output_method("file_name:     " + plugin_information.file_name)
        output_method("contents_file: " + plugin_information.contents_file)

        for dependency_information in plugin_information.dependencies:
            output_method("dependency")
            self.print_dependency_info(dependency_information, output_method)

    def print_dependency_info(self, dependency_information, output_method):
        output_method("id:            " + dependency_information.id)
        output_method("version:       " + dependency_information.version)
