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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

class ConsoleSystemUpdater:
    """
    The console system updater class.
    """

    system_updater_plugin = None
    """ The system updater plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, system_updater_plugin):
        """
        Constructor of the class.

        @type system_updater_plugin: SystemUpdaterPlugin
        @param system_updater_plugin: The system updater plugin.
        """

        self.system_updater_plugin = system_updater_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_list_repositories(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the list repositories command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the repositories list
        repositories_list = system_updater.get_repositories()

        # prints the repository information
        for repository in repositories_list:
            self.print_repository_info(repository, output_method)

    def process_list_repository_packages(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the list repository packages command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the repository name
        repository_name = arguments_map["repository_name"]

        # retrieves the package information list
        package_information_list = system_updater.get_package_information_list_by_repository_name(repository_name)

        # prints the package information
        for package_information in package_information_list:
            self.print_package_info(package_information, output_method)

    def process_list_repository_bundles(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the list repository bundles command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        pass

    def process_list_repository_plugins(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the list repository plugins command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the repository name
        repository_name = arguments_map["repository_name"]

        # retrieves the plugin information list
        plugin_information_list = system_updater.get_plugin_information_list_by_repository_name(repository_name)

        # prints the plugin information
        for plugin_information in plugin_information_list:
            self.print_plugin_info(plugin_information, output_method)

    def process_install(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the install command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        pass

    def process_install_package(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the install package command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the package identifier
        package_id = arguments_map["package_id"]

        # retrieves the package version
        package_version = arguments_map.get("package_version", None)

        # installs the package
        if package_version:
            system_updater.install_package(package_id, package_version)
        else:
            system_updater.install_package(package_id)

    def process_install_bundle(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the install bundle command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the bundle identifier
        bundle_id = arguments_map["bundle_id"]

        # retrieves the bundle version
        bundle_version = arguments_map.get("bundle_version", None)

        # installs the bundle
        if bundle_version:
            system_updater.install_bundle(bundle_id, bundle_version)
        else:
            system_updater.install_bundle(bundle_id)

    def process_install_plugin(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the install plugin command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the plugin identifier
        plugin_id = arguments_map["plugin_id"]

        # retrieves the plugin version
        plugin_version = arguments_map.get("plugin_version", None)

        # installs the plugin
        if plugin_version:
            system_updater.install_plugin(plugin_id, plugin_version)
        else:
            system_updater.install_plugin(plugin_id)

    def print_repository_info(self, repository_information, output_method):
        output_method("name:        " + repository_information.name)
        output_method("description: " + repository_information.description)
        output_method("addresses:   " + str(repository_information.addresses))

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

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "list_repositories" : {
                "handler" : self.process_list_repositories,
                "description" : "lists the current available repositories"
            },
            "list_repository_packages" : {
                "handler" : self.process_list_repository_packages,
                "description" : "lists the packages for the given repository",
                "arguments" : [
                    {
                        "name" : "repository_name",
                        "description" : "the name of the repository from where to list the packages",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            },
            "list_repository_bundles" : {
                "handler" : self.process_list_repository_bundles,
                "description" : "lists the bundles for the given repository"
            },
            "list_repository_plugins" : {
                "handler" : self.process_list_repository_plugins,
                "description" : "lists the plugins for the given repository",
                "arguments" : [
                    {
                        "name" : "repository_name",
                        "description" : "the name of the repository from where to list the plugins",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            },
            "install" : {
                "handler" : self.process_install,
                "description" : "installs the package, bundle or plugin with the given id and version"
            },
            "install_package" : {
                "handler" : self.process_install_package,
                "description" : "installs the package with the given id and version",
                "arguments" : [
                    {
                        "name" : "package_id",
                        "description" : "the id of the package to install",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "package_version",
                        "description" : "the version of the package to install",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "install_bundle" : {
                "handler" : self.process_install_bundle,
                "description" : "installs the bundle with the given id and version",
                "arguments" : [
                    {
                        "name" : "bundle_id",
                        "description" : "the id of the bundle to install",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "bundle_version",
                        "description" : "the version of the bundle to install",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "install_plugin" : {
                "handler" : self.process_install_plugin,
                "description" : "installs the plugin with the given id and version",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to install",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "plugin_version",
                        "description" : "the version of the plugin to install",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
