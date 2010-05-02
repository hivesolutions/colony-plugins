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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import os

import system_updating_parser
import exceptions.system_updating_exceptions

TEMP_DIRECTORY = "colony/tmp"
REPOSITORIES_FILE_PATH = "resources/repositories.xml"
REPOSITORY_DESCRIPTOR_FILE = "repository_descriptor.xml"

SIMPLE_REPOSITORY_LAYOUT_VALUE = "simple"
""" The simple repository layout value """

EXTENDED_REPOSITORY_LAYOUT_VALUE = "extended"
""" The extended repository layout value """

class SystemUpdater:

    system_updater_plugin = None

    repository_list = []
    repository_descriptor_list = []
    repository_repository_descriptor_map = {}
    repository_descriptor_repository_map = {}

    def __init__(self, system_updater_plugin):
        self.system_updater_plugin = system_updater_plugin

    def load_system_updater(self):
        """
        Loads the system updater
        """

        self.load_repositories_file()

    def load_repositories_file(self):
        """
        Loads the repositories file
        """

        repositories_file_path = os.path.join(os.path.dirname(__file__), REPOSITORIES_FILE_PATH)
        repositories_file_parser = system_updating_parser.RepositoriesFileParser(repositories_file_path)
        repositories_file_parser.parse()
        self.repository_list = repositories_file_parser.get_value()

    def load_repositories_information(self):
        """
        Loads the repository information for each of the repositories
        """

        for repository in self.repository_list:
            repository_descriptor = self.get_repository_information(repository)
            if repository_descriptor:
                self.repository_descriptor_list.append(repository_descriptor)
                self.repository_repository_descriptor_map[repository] = repository_descriptor
                self.repository_descriptor_repository_map[repository_descriptor] = repository

    def get_repositories(self):
        """
        Retrieves the list of available repositories

        @rtype: List
        @return: The list of available repositories
        """

        return self.repository_list

    def get_repository_by_repository_name(self, repository_name):
        """
        Retrieves the repository structure for the given repository name

        @type repository_name: String
        @param repository_name: The name of the repository to get the repository structure
        @rtype: Repository
        @return: The repository structure for the given repository name
        """

        # iterates over the repository list
        for repository in self.repository_list:
            if repository.name == repository_name:
                return repository

    def get_repository_information_by_repository_name(self, repository_name):
        """
        Retrieves the repository descriptor for the given repository name

        @type repository_name: String
        @param repository_name: The name of the repository to get the descriptor
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given repository name
        """

        # iterates over the repository list
        for repository in self.repository_list:
            if repository.name == repository_name:
                return self.get_repository_information(repository)

    def get_package_information_list_by_repository_name(self, repository_name):
        """
        Retrieves the list of package information for the given repository name

        @type repository_name: String
        @param repository_name: The name of the repository to get the list of package information
        @rtype: List
        @return: The list of package information for the given repository name
        """

        repository_information = self.get_repository_information_by_repository_name(repository_name)
        return repository_information.packages

    def get_plugin_information_list_by_repository_name(self, repository_name):
        """
        Retrieves the list of plugin information for the given repository name

        @type repository_name: String
        @param repository_name: The name of the repository to get the list of plugin information
        @rtype: List
        @return: The list of plugin information for the given repository name
        """

        repository_information = self.get_repository_information_by_repository_name(repository_name)
        return repository_information.plugins

    def get_repository_information(self, repository):
        """
        Retrieves the repository descriptor for the given repository

        @type repository: Repository
        @param repository: The repository to get the descriptor
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given repository
        """

        repository_descriptor_file = self.get_repository_descriptor_file(repository.addresses)
        if repository_descriptor_file:
            repository_descriptor_file_parser = system_updating_parser.RepositoryDescriptorFileParser(repository_descriptor_file)
            repository_descriptor_file_parser.parse()
            return repository_descriptor_file_parser.get_value()

    def get_repository_descriptor_file(self, repository_addresses):
        """
        Retrieves the repository descriptor file for the given repository addresses

        @type repository_addresses: List
        @param repository_addresses: The repository addresses to search
        @rtype: Stream
        @return: The stream containing the repository descriptor for the given repository addresses
        """

        downloader_plugin = self.system_updater_plugin.downloader_plugin

        # iterates over all the repositories
        for repository_address in repository_addresses:
            self.system_updater_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))
            repository_address_value = repository_address.value
            file_address = repository_address_value + "/" + REPOSITORY_DESCRIPTOR_FILE
            file_buffer = downloader_plugin.get_download_package_stream(file_address)
            # in case the download was successful
            if file_buffer:
                return file_buffer

    def install_plugin(self, plugin_id, plugin_version = None):
        """
        Install the plugin with the given id and version from a random repository

        @type plugin_id: String
        @param plugin_id: The id of the plugin to install
        @type plugin_version: String
        @param plugin_id: The version of the plugin to install
        @rtype: bool
        @return: The result of the installation (if successful or not)
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the plugin
        plugin_descriptor = self.get_plugin_descriptor(plugin_id, plugin_version)

        # in case the plugin was not found
        if not plugin_descriptor:
            raise exceptions.system_updating_exceptions.InvalidPluginException("Plugin %s v%s not found" % (plugin_id, plugin_version))

        # installs the plugin dependencies
        if not self.install_plugin_dependencies(plugin_descriptor):
            return False

        # retrieves the plugin type
        plugin_type = plugin_descriptor.plugin_type

        # retrieves a deployer for the given plugin type
        plugin_deployer = self.system_updater_plugin.get_deployer_by_deployer_type(plugin_type)

        # in case there is no deployer for the given plugin type
        if not plugin_deployer:
            return False

        # retrieves the repository descriptor from the plugin descriptor
        repository_descriptor = self.get_repository_descriptor_plugin_descriptor(plugin_descriptor)

        # retrieves the repository structure for the provided repository descriptor
        repository = self.repository_descriptor_repository_map[repository_descriptor]

        # retrieves the contents file
        contents_file = self.get_contents_file(repository.name, plugin_descriptor.name, plugin_descriptor.version, plugin_descriptor.contents_file)

        # sends the contents file to the plugin type deployer
        plugin_deployer.deploy_package(contents_file, plugin_descriptor.id, plugin_descriptor.version)

        # deletes the contents file
        self.delete_contents_file(contents_file)

        return True

    def install_plugin_dependencies(self, plugin_descriptor):
        """
        Install the plugin dependencies for the given plugin descriptor

        @type plugin_descriptor: PluginDescriptor
        @param plugin_id: The plugin descriptor of the plugin to install the dependencies
        @rtype: bool
        @return: The result of the plugin dependencies installation (if successful or not)
        """

        # retrieves the plugin dependencies
        plugin_dependencies = plugin_descriptor.dependencies

        # iterates over the plugin dependencies
        for plugin_dependency in plugin_dependencies:
            # in case the install has not been sucessfull
            if not self.install_plugin(plugin_dependency.id, plugin_dependency.version):
                return False

        # in case all the dependencies have been correctly installed
        return True

    def install_package(self, package_id, package_version = None):
        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the package
        package_descriptor = self.get_package_descriptor(package_id, package_version)

        # retrieves the package plugins
        package_plugins = package_descriptor.plugins

        # iterates over all the plugins in the plugin descriptor
        for plugin in package_plugins:
            plugin_id = plugin.id
            plugin_version = plugin.version

            self.install_plugin(plugin_id, plugin_version)

    def get_repositories_list(self):
        """
        Retrieves the list of available repositories

        @rtype: List
        @return: The list of available repositories
        """

        return self.repository_list

    def get_package_list(self):
        """
        Retrieves the list of available packages

        @rtype: List
        @return: The list of available packages
        """

        pass

    def get_plugin_list(self):
        """
        Retrieves the list of available plugins

        @rtype: List
        @return: The list of available plugins
        """

        pass

    def get_package_descriptor(self, package_id, package_version = None):
        """
        Retrieves the package descriptor for the given package id and version

        @type package_id: String
        @param package_id: The id of the package to retrieve the package descriptor
        @type package_version: String
        @param package_version: The version of the package to retrieve the package descriptor
        @rtype: PackageDescriptor
        @return: The package descriptor for the package with the given id and version
        """

        # iterates over all the repository descriptors available
        for repository_descriptor in self.repository_descriptor_list:
            package_descripton = repository_descriptor.get_package(package_id, package_version)

            # in case package descriptor exists in current repository descriptor
            if package_descripton:
                return package_descripton

    def get_plugin_descriptor(self, plugin_id, plugin_version = None):
        """
        Retrieves the plugin descriptor for the given plugin id and version

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the plugin descriptor
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve the plugin descriptor
        @rtype: PluginDescriptor
        @return: The plugin descriptor for the plugin with the given id and version
        """

        # iterates over all the repository descriptors available
        for repository_descriptor in self.repository_descriptor_list:
            plugin_descripton = repository_descriptor.get_plugin(plugin_id, plugin_version)

            # in case plugin descriptor exists in current repository descriptor
            if plugin_descripton:
                return plugin_descripton

    def get_repository_descriptor_plugin_descriptor(self, plugin_descriptor):
        """
        Retrieves the repository descriptor for the given plugin descriptor

        @type plugin_descriptor: PluginDescriptor
        @param plugin_descriptor: The plugin descriptor to get the repository descriptor
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given plugin descriptor
        """

        for repository_descriptor in self.repository_descriptor_list:
            if plugin_descriptor in repository_descriptor.plugins:
                return repository_descriptor

    def get_contents_file(self, repository_name, plugin_name, plugin_version, contents_file):
        """
        Retrieves the plugin contents file for the given repository name, plugin name, plugin version and contents file name

        @type repository_name: String
        @param repository_name: The name of the repository to use in the plugin contents file retrieval
        @type plugin_name: String
        @param plugin_name: The name of the plugin to use in the plugin contents file retrieval
        @type plugin_version: String
        @param plugin_version: The version of the plugin to use in the plugin contents file retrieval
        @type contents_file: String
        @param contents_file: The name of the plugin contents file to retrieve
        @rtype: Stream
        @return: The retrieved plugin contents file stream
        """

        # retrieves the repository structure for the given repository name
        repository = self.get_repository_by_repository_name(repository_name)

        # retrieves the repository addresses
        repository_addresses = repository.addresses

        # retrieves the repository layout
        repository_layout = repository.layout

        # downloads the contents file
        self.download_contents_file(repository_addresses, plugin_name, plugin_version, contents_file, repository_layout, TEMP_DIRECTORY)

        # the created contents file path
        contents_file_path = TEMP_DIRECTORY + "/" + contents_file

        # the created contents file
        contents_file = open(contents_file_path, "r")

        # returns teh contents file
        return contents_file

    def download_contents_file(self, repository_addresses, plugin_name, plugin_version, contents_file, repository_layout = SIMPLE_REPOSITORY_LAYOUT_VALUE, target_directory = TEMP_DIRECTORY):
        """
        Downloads the plugin contents file for the given repository name, plugin name, plugin version and contents file name

        @type repository_name: String
        @param repository_name: The name of the repository to use in the plugin contents file download
        @type plugin_name: String
        @param plugin_name: The name of the plugin to use in the plugin contents file download
        @type plugin_version: String
        @param plugin_version: The version of the plugin to use in the plugin contents file download
        @type contents_file: String
        @param contents_file: The name of the plugin contents file to download
        @type repository_layout: String
        @param repository_layout: The layout of the repository.
        @type target_directory: String
        @param target_directory: The target directory of the download
        @rtype: bool
        @return: The result of the download (if successful or not)
        """

        downloader_plugin = self.system_updater_plugin.downloader_plugin

        # iterates over all the repository addresses
        for repository_address in repository_addresses:
            # prints an info message
            self.system_updater_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))
            repository_address_value = repository_address.value

            # in case the layout of the repository is simple
            # (eg: plugins/plugin_id_version.ext)
            if SIMPLE_REPOSITORY_LAYOUT_VALUE:
                file_address = repository_address_value + "/plugins/" + contents_file
            # in case the layout of the repository is extended
            # (eg: plugins/plugin_name/plugin_version/plugin_id_version.ext)
            elif EXTENDED_REPOSITORY_LAYOUT_VALUE:
                file_address = repository_address_value + "/plugins" + plugin_name + "/" + plugin_version + "/" + contents_file

            result = downloader_plugin.download_package(file_address, target_directory)

            # in case the download was successful
            if result:
                return True
        return False

    def delete_contents_file(self, contents_file):
        # closes the contents file
        contents_file.close()

        # retrieves the contents file path
        contents_file_path = contents_file.name

        # removes the contents file
        os.remove(contents_file_path)
