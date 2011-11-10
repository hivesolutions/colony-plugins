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

    def process_update_repositories(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the update repositories command, with the given
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

        # updates the repositories, generating a flush in
        # the system updater repositories information
        system_updater.update_repositories()

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

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the repository name
        repository_name = arguments_map["repository_name"]

        # retrieves the bundle information list
        bundle_information_list = system_updater.get_bundle_information_list_by_repository_name(repository_name)

        # prints the bundle information
        for bundle_information in bundle_information_list:
            self.print_bundle_info(bundle_information, output_method)

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

    def process_list_repository_containers(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the list repository containers command, with the given
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

        # retrieves the container information list
        container_information_list = system_updater.get_container_information_list_by_repository_name(repository_name)

        # prints the container information
        for container_information in container_information_list:
            self.print_container_info(container_information, output_method)

    def process_upgrade(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the upgrade command, with the given
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

        # runs the upgrade process in the system updater, upgrading
        # all the installed objects in the system
        system_updater.upgrade()

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

        # retrieves the system updater
        system_updater = self.system_updater_plugin.system_updater

        # retrieves the object identifier and the object version and
        # uses them to install the object in the current instance
        object_id = arguments_map["object_id"]
        object_version = arguments_map.get("object_version", None)
        system_updater.install_object(object_id, object_version)

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

        # retrieves the package identifier and the package version and
        # uses them to install the package in the current instance
        package_id = arguments_map["package_id"]
        package_version = arguments_map.get("package_version", None)
        system_updater.install_package(package_id, package_version)

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

        # retrieves the bundle identifier and the bundle version and
        # uses them to install the bundle in the current instance
        bundle_id = arguments_map["bundle_id"]
        bundle_version = arguments_map.get("bundle_version", None)
        system_updater.install_bundle(bundle_id, bundle_version)

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

        # retrieves the plugin identifier and plugin version and
        # uses them to install the plugin in the current instance
        plugin_id = arguments_map["plugin_id"]
        plugin_version = arguments_map.get("plugin_version", None)
        system_updater.install_plugin(plugin_id, plugin_version)

    def process_install_container(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the install container command, with the given
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

        # retrieves the container identifier and container version and
        # uses them to install the container in the current instance
        container_id = arguments_map["container_id"]
        container_version = arguments_map.get("container_version", None)
        system_updater.install_container(container_id, container_version)

    def process_uninstall(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the uninstall command, with the given
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

        # retrieves the object identifier and the object version and
        # uses them to uninstall the object in the current instance
        object_id = arguments_map["object_id"]
        object_version = arguments_map.get("object_version", None)
        system_updater.uninstall_object(object_id, object_version)

    def process_uninstall_package(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the uninstall package command, with the given
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

        # retrieves the package identifier and the package version and
        # uses them to install the package in the current instance
        package_id = arguments_map["package_id"]
        package_version = arguments_map.get("package_version", None)
        system_updater.uninstall_package(package_id, package_version)

    def process_uninstall_bundle(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the uninstall bundle command, with the given
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

        # retrieves the bundle identifier and the bundle version and
        # uses them to install the bundle in the current instance
        bundle_id = arguments_map["bundle_id"]
        bundle_version = arguments_map.get("bundle_version", None)
        system_updater.uninstall_bundle(bundle_id, bundle_version)

    def process_uninstall_plugin(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the uninstall plugin command, with the given
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

        # retrieves the plugin identifier and the plugin version and
        # uses them to install the plugin in the current instance
        plugin_id = arguments_map["plugin_id"]
        plugin_version = arguments_map.get("plugin_version", None)
        system_updater.uninstall_plugin(plugin_id, plugin_version)

    def process_uninstall_container(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the uninstall container command, with the given
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

        # retrieves the container identifier and the container version and
        # uses them to install the container in the current instance
        container_id = arguments_map["container_id"]
        container_version = arguments_map.get("container_version", None)
        system_updater.uninstall_container(container_id, container_version)

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

    def print_bundle_info(self, bundle_information, output_method):
        output_method("name:          " + bundle_information.name)
        output_method("type:          " + bundle_information.bundle_type)
        output_method("id:            " + bundle_information.id)
        output_method("version:       " + bundle_information.version)
        output_method("contents_file: " + bundle_information.contents_file)

        for dependency_information in bundle_information.dependencies:
            output_method("dependency")
            self.print_dependency_info(dependency_information, output_method)

        for hash_digest_information in bundle_information.hash_digest_items:
            output_method("hash_digest")
            self.print_hash_digest_info(hash_digest_information, output_method)

    def print_plugin_info(self, plugin_information, output_method):
        output_method("name:          " + plugin_information.name)
        output_method("type:          " + plugin_information.plugin_type)
        output_method("id:            " + plugin_information.id)
        output_method("version:       " + plugin_information.version)
        output_method("contents_file: " + plugin_information.contents_file)

        for dependency_information in plugin_information.dependencies:
            output_method("dependency")
            self.print_dependency_info(dependency_information, output_method)

        for hash_digest_information in plugin_information.hash_digest_items:
            output_method("hash_digest")
            self.print_hash_digest_info(hash_digest_information, output_method)

    def print_container_info(self, container_information, output_method):
        output_method("name:          " + container_information.name)
        output_method("type:          " + container_information.container_type)
        output_method("id:            " + container_information.id)
        output_method("version:       " + container_information.version)
        output_method("contents_file: " + container_information.contents_file)

        for dependency_information in container_information.dependencies:
            output_method("dependency")
            self.print_dependency_info(dependency_information, output_method)

        for hash_digest_information in container_information.hash_digest_items:
            output_method("hash_digest")
            self.print_hash_digest_info(hash_digest_information, output_method)

    def print_dependency_info(self, dependency_information, output_method):
        output_method("id:            " + dependency_information.id)
        output_method("version:       " + dependency_information.version)

    def print_hash_digest_info(self, hash_digest_information, output_method):
        output_method("key:           " + hash_digest_information.key)
        output_method("value:         " + hash_digest_information.value)

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "update_repositories" : {
                "handler" : self.process_update_repositories,
                "description" : "updates the currently available repositories (fetches remote data)"
            },
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
                "description" : "lists the bundles for the given repository",
                "arguments" : [
                    {
                        "name" : "repository_name",
                        "description" : "the name of the repository from where to list the bundles",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
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
            "list_repository_containers" : {
                "handler" : self.process_list_repository_containers,
                "description" : "lists the containers for the given repository",
                "arguments" : [
                    {
                        "name" : "repository_name",
                        "description" : "the name of the repository from where to list the containers",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            },
            "upgrade" : {
                "handler" : self.process_upgrade,
                "description" : "upgrade the current colony instance using the objects in the currently available repositories"
            },
            "install" : {
                "handler" : self.process_install,
                "description" : "installs the package, bundle or plugin with the given id and version",
                "arguments" : [
                    {
                        "name" : "object_id",
                        "description" : "the id of the object to install",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "object_version",
                        "description" : "the version of the object to install",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
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
            },
            "install_container" : {
                "handler" : self.process_install_container,
                "description" : "installs the container with the given id and version",
                "arguments" : [
                    {
                        "name" : "container_id",
                        "description" : "the id of the container to install",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "container_version",
                        "description" : "the version of the container to install",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "uninstall" : {
                "handler" : self.process_uninstall,
                "description" : "uninstalls the package, bundle or plugin with the given id and version",
                "arguments" : [
                    {
                        "name" : "object_id",
                        "description" : "the id of the object to uninstall",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "object_version",
                        "description" : "the version of the object to uninstall",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "uninstall_bundle" : {
                "handler" : self.process_uninstall_package,
                "description" : "uninstalls the package with the given id and version",
                "arguments" : [
                    {
                        "name" : "package_id",
                        "description" : "the id of the package to uninstall",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "package_version",
                        "description" : "the version of the package to uninstall",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "uninstall_bundle" : {
                "handler" : self.process_uninstall_bundle,
                "description" : "uninstalls the bundle with the given id and version",
                "arguments" : [
                    {
                        "name" : "bundle_id",
                        "description" : "the id of the bundle to uninstall",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "bundle_version",
                        "description" : "the version of the bundle to uninstall",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "uninstall_plugin" : {
                "handler" : self.process_uninstall_plugin,
                "description" : "uninstalls the plugin with the given id and version",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to uninstall",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "plugin_version",
                        "description" : "the version of the plugin to uninstall",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "uninstall_container" : {
                "handler" : self.process_uninstall_container,
                "description" : "uninstalls the container with the given id and version",
                "arguments" : [
                    {
                        "name" : "container_id",
                        "description" : "the id of the container to uninstall",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "container_version",
                        "description" : "the version of the container to uninstall",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
