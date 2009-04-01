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

import os
import sys
import gc
import xml.dom.minidom

import colony.plugins.plugin_system

PLUGINS_DIRECTORY = "colony/plugins"
TEMP_DIRECTORY = "colony/plugins/tmp"
REPOSITORIES_FILE_PATH = "resources/repositories.xml"
REPOSITORY_DESCRIPTOR_FILE = "repository_descriptor.xml"
#@todo: review and comment this file
# @todo melhorar o plugin pondo cache no acesso aos servidores
# e pondo mais suporte para gestao de dependecias
# pondo tb suporte para transacoes
class PluginDownloader:
    """
    The plugin downloader system class
    """

    plugin_downloader_plugin = None
    """ The plugin downloader plugin """

    repository_list = []
    """ The list of repositories """

    repository_descriptor_list = []
    """ The list of respository desciptors """

    repository_repository_descriptor_map = {}
    """ The map relating repositories with repository descriptors """

    repository_descriptor_repository_map = {}
    """ The map relating repository descriptors with repositories """

    def __init__(self, plugin_downloader_plugin):
        """
        Constructor of the class

        @type plugin_downloader_plugin: Plugin
        @param plugin_downloader_plugin: The plugin downloader plugin
        """

        self.plugin_downloader_plugin = plugin_downloader_plugin

        self.repository_list = []
        self.repository_descriptor_list = []
        self.repository_repository_descriptor_map = {}
        self.repository_descriptor_repository_map = {}

    def load_plugin_downloader(self):
        """
        Starts the plugin downloader
        """

        repositories_file_path = os.path.join(os.path.dirname(__file__), REPOSITORIES_FILE_PATH)
        repositories_file_parser = RepositoriesFileParser(repositories_file_path)
        repositories_file_parser.parse()
        self.repository_list = repositories_file_parser.get_value()

    def download_plugin(self, plugin_identifier, plugin_version = None):
        """
        Downloads the plugin with the given id and version

        @type plugin_identifier: String
        @param plugin_identifier: The id of the plugin to download
        @type plugin_version: String
        @param plugin_version: The version of the plugin to download
        @rtype: bool
        @return: The result of the download (if successful or not)
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the plugin
        plugin_descriptor = self.get_plugin(plugin_identifier, plugin_version)

        # if there's no results from plugin_identifier being a plugin id tries to match it as a plugin name
        if not plugin_descriptor:
            plugin_descriptor = self.get_plugin_name(plugin_identifier, plugin_version)

        # in case the plugin is available
        if plugin_descriptor:
            self.plugin_downloader_plugin.info("Plugin '%s' v%s found" % (plugin_identifier, plugin_version))
            return self.process_plugin_descriptor(plugin_descriptor)
        else:
            self.plugin_downloader_plugin.info("Plugin '%s' v%s not found" % (plugin_identifier, plugin_version))
            return False

    def process_plugin_descriptor(self, plugin_descriptor):
        """
        Processes a given plugin descriptor retrieving the validity of the plugin
        (if it exists, if the code is valid and if all the dependencies for it are loaded)

        @type plugin_descriptor: PluginDescriptor
        @param plugin_descriptor: The plugin descriptor to verify
        @rtype: bool
        @return: The validity of the plugin descriptor
        """

        repository_descriptor = self.get_repository_descriptor_plugin_descriptor(plugin_descriptor)

        # in case there's no repository descriptor containing that plugin descriptor
        if not repository_descriptor in self.repository_descriptor_repository_map:
            return False

        # retrieves the repository structure for the provided repository descriptor
        repository = self.repository_descriptor_repository_map[repository_descriptor]

        # gets the plugin file from the server in stream format
        plugin_file = self.get_plugin_file(repository.addresses, plugin_descriptor.name, plugin_descriptor.version, plugin_descriptor.file_name)

        # compiles the code in the stream
        plugin_file_object = compile(plugin_file, "<CodeString>", "exec")

        # executes the compiled code
        exec plugin_file_object in globals()

        # gets the name of the class from the plugin descriptor
        class_name = plugin_descriptor.main_class

        # gets the class from local defs
        main_class = globals()[class_name]

        # checks if the dependencies are available
        availability = self.get_dependencies_availability(main_class)

        # in case the dependencies for the plugin were not found
        if not availability:
            self.plugin_downloader_plugin.info("Dependencies for plugin '%s' v%s not found" % (plugin_descriptor.name, plugin_descriptor.version))
            return False

        # deletes the main_class definition
        del main_class
        del globals()[class_name]

        # runs garbage collector to update the __subclasses__() call
        gc.collect()

        # in case the plugin contains payload
        if not plugin_descriptor.zip_file == "none":
            # downloads the plugin payload file
            self.download_plugin_payload(repository.addresses, plugin_descriptor.name, plugin_descriptor.version, plugin_descriptor.zip_file)

        # downloads the plugin file initializing the plugin loading procedures
        self.download_plugin_file(repository.addresses, plugin_descriptor.name, plugin_descriptor.version, plugin_descriptor.file_name)

        return True

    def get_dependencies_availability(self, plugin):
        """
        Tests if all the dependencies for the given plugin are available

        @type plugin: Plugin
        @param plugin: The plugin to test for the availability of the dependencies
        @rtype: bool
        @return: The result of the plugin dependencies availability test
        """

        # retrieves the plugin manager
        manager = self.plugin_downloader_plugin.manager

        plugin_instance = plugin()
        plugin_dependencies = plugin_instance.get_all_plugin_dependencies()

        # iterates over all the plugin dependencies
        for dependency in plugin_dependencies:
            dependency_id = dependency.plugin_id
            dependency_version = dependency.plugin_version

            # in case the plugin is not currently loaded
            if not manager._get_plugin_by_id_and_version(dependency_id, dependency_version):
                # in case the plugin is not available for download
                if not self.download_plugin(dependency_id, dependency_version):
                    return False

        return True

    def get_plugin(self, plugin_id, plugin_version = None):
        """
        Retrieves the plugin descriptor for the given plugin id and version

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the plugin descriptor
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve the plugin descriptor
        @rtype: PluginDescriptor
        @return: The plugin descriptor for the plugin with the given id and version
        """

        # iterates over all the repositories available
        for repository_descriptor in self.repository_descriptor_list:
            plugin = repository_descriptor.get_plugin(plugin_id, plugin_version)

            # in case plugin exists in current repository
            if plugin:
                return plugin

    def get_plugin_name(self, plugin_name, plugin_version = None):
        """
        Retrieves the plugin name for the given plugin id and version

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the plugin name
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve the plugin name
        @rtype: String
        @return: The plugin name for the plugin with the given id and version
        """

        # iterates over all the repositories available
        for repository_descriptor in self.repository_descriptor_list:
            plugin = repository_descriptor.get_plugin_name(plugin_name, plugin_version)

            # in case plugin exists in current repository
            if plugin:
                return plugin

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
            repository_descriptor_file_parser = RepositoryDescriptorFileParser(repository_descriptor_file)
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

        downloader_plugin = self.plugin_downloader_plugin.downloader_plugin

        # iterates over all the repositories
        for repository_address in repository_addresses:
            self.plugin_downloader_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))
            repository_address_value = repository_address.value
            file_address = repository_address_value + "/" + REPOSITORY_DESCRIPTOR_FILE
            file_buffer = downloader_plugin.get_download_package_stream(file_address)
            # in case the download was successful
            if file_buffer:
                return file_buffer

    def get_plugin_file(self, repository_addresses, plugin_name, plugin_version, plugin_file_name):
        """
        Retrieves the plugin file stream for the given repository addresses and plugin name, version and file name

        @type repository_addresses: List
        @param repository_addresses: The repository addresses to search
        @type plugin_name: String
        @param plugin_name: The name of the plugin to retrieve the stream
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve the stream
        @type plugin_file_name: String
        @param plugin_file_name: The file name of the plugin to retrieve the stream
        @rtype: Stream
        @return: The stream containing the plugin for the given repository addresses and plugin name, version and file name
        """

        downloader_plugin = self.plugin_downloader_plugin.downloader_plugin

        # iterates over all the repositories
        for repository_address in repository_addresses:
            self.plugin_downloader_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))
            repository_address_value = repository_address.value
            file_address = repository_address_value + "/" + plugin_name + "/" + plugin_version + "/" + plugin_file_name
            file_buffer = downloader_plugin.get_download_package_stream(file_address)
            # in case the download was successful
            if file_buffer:
                return file_buffer

    def download_plugin_file(self, repository_addresses, plugin_name, plugin_version, plugin_file_name):
        """
        Downloads the plugin file for the given repository addresses and plugin name, version and file name

        @type repository_addresses: List
        @param repository_addresses: The repository addresses to search
        @type plugin_name: String
        @param plugin_name: The name of the plugin to download
        @type plugin_version: String
        @param plugin_version: The version of the plugin to download
        @type plugin_file_name: String
        @param plugin_file_name: The file name of the plugin to download
        @rtype: bool
        @return: The result of the download (if successful or not)
        """

        downloader_plugin = self.plugin_downloader_plugin.downloader_plugin

        # iterates over all the repositories
        for repository_address in repository_addresses:
            self.plugin_downloader_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))
            repository_address_value = repository_address.value
            file_address = repository_address_value + "/" + plugin_name + "/" + plugin_version + "/" + plugin_file_name
            result = downloader_plugin.download_package(file_address, PLUGINS_DIRECTORY)
            # in case the download was successful
            if result:
                return True
        return False

    def download_plugin_payload(self, repository_addresses, plugin_name, plugin_version, plugin_zip_file):
        """
        Downloads the plugin payload file for the given repository addresses and plugin name, version and plugin zip file name

        @type repository_addresses: List
        @param repository_addresses: The repository addresses to search
        @type plugin_name: String
        @param plugin_name: The name of the plugin payload to download
        @type plugin_version: String
        @param plugin_version: The version of the plugin payload to download
        @type plugin_zip_file: String
        @param plugin_zip_file: The plugin zip file name of the plugin payload to download
        @rtype: bool
        @return: The result of the download (if successful or not)
        """

        downloader_plugin = self.plugin_downloader_plugin.downloader_plugin

        # iterates over all the repositories
        for repository_address in repository_addresses:
            self.plugin_downloader_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))
            repository_address_value = repository_address.value
            file_address = repository_address_value + "/" + plugin_name + "/" + plugin_version + "/" + plugin_zip_file
            result = downloader_plugin.download_package(file_address, PLUGINS_DIRECTORY)
            # in case the download was successful
            if result:
                self.uncompress_zip_file(PLUGINS_DIRECTORY + "/" + plugin_zip_file)
                return True
        return False

    def uncompress_zip_file(self, file_path):
        """
        Uncompresses a zip file in the given path

        @type file_path: String
        @param file_path: The file path of the file to unzip
        """

        # retrieves the zip plugin from the plugin downloader plugin
        zip_plugin = self.plugin_downloader_plugin.zip_plugin

        # extracts the zip file
        zip_plugin.unzip(file_path, PLUGINS_DIRECTORY)

        # removes the zip file after the extraction
        os.remove(file_path)

class Parser:
    """
    The abstract parser class
    """

    def __init__(self):
        """
        Constructor of the class
        """

        pass

    def parse(self):
        """
        Parses the defined file
        """

        pass

    def get_value(self):
        """
        Retrieves the result of the parse

        @rtype: Object
        @return: The result of the parse
        """

        pass

class RepositoriesFileParser(Parser):

    file_path = None

    repository_list = []

    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path

    def parse(self):
        self.load_repository_file(self.file_path)

    def get_value(self):
        return self.repository_list

    def get_repository_list(self):
        return self.repository_list

    def load_repository_file(self, file_path):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.repository_list = self.parse_repositories(child_node)

    def parse_repositories(self, repositories):
        repository_list = []
        child_nodes = repositories.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                repository_list.append(self.parse_repository(child_node))

        return repository_list

    def parse_repository(self, repository):
        repository_structure = Repository()
        child_nodes = repository.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_element(child_node, repository_structure)

        return repository_structure

    def parse_repository_element(self, repository_element, repository):
        node_name = repository_element.nodeName

        if node_name == "name":
            repository.name = self.parse_name(repository_element)
        elif node_name == "description":
            repository.description = self.parse_description(repository_element)
        elif node_name == "addresses":
            repository.addresses = self.parse_addresses(repository_element)

    def parse_name(self, name):
        repository_name = name.firstChild.data.strip()
        return repository_name

    def parse_description(self, description):
        repository_description = description.firstChild.data.strip()
        return repository_description

    def parse_addresses(self, addresses):
        addresses_list = []
        child_nodes = addresses.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                address = self.parse_address(child_node)
                addresses_list.append(address)

        return addresses_list

    def parse_address(self, address):
        address_structure = Address()
        address_structure.name = address.getAttribute("name")
        address_structure.value = address.firstChild.data.strip()

        return address_structure

class RepositoryDescriptorFileParser(Parser):

    file = None

    repository_descriptor = None

    def __init__(self, file = None):
        Parser.__init__(self)
        self.file = file

    def parse(self):
        self.load_repository_descriptor_file(self.file)

    def get_value(self):
        return self.repository_descriptor

    def get_repository_list(self):
        return self.repository_descriptor

    def load_repository_descriptor_file(self, file):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parseString(file)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.repository_descriptor = self.parse_repository_descriptor(child_node)

    def parse_repository_descriptor(self, repository_descriptor):
        repository_descriptor_structure = RepositoryDescriptor()
        child_nodes = repository_descriptor.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_descriptor_element(child_node, repository_descriptor_structure)

        return repository_descriptor_structure

    def parse_repository_descriptor_element(self, repository_descriptor_element, repository_descriptor):
        node_name = repository_descriptor_element.nodeName

        if node_name == "name":
            repository_descriptor.name = self.parse_repository_descriptor_name(repository_descriptor_element)
        elif node_name == "description":
            repository_descriptor.description = self.parse_repository_descriptor_description(repository_descriptor_element)
        elif node_name == "packages":
            repository_descriptor.packages = self.parse_repository_descriptor_packages(repository_descriptor_element)
        elif node_name == "plugins":
            repository_descriptor.plugins = self.parse_repository_descriptor_plugins(repository_descriptor_element)

    def parse_repository_descriptor_name(self, descriptor_name):
        repository_descriptor_name = descriptor_name.firstChild.data.strip()
        return repository_descriptor_name

    def parse_repository_descriptor_description(self, descriptor_description):
        repository_descriptor_description = descriptor_description.firstChild.data.strip()
        return repository_descriptor_description

    def parse_repository_descriptor_packages(self, descriptor_packages):
        repository_descriptor_packages_list = []
        child_nodes = descriptor_packages.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                repository_descriptor_package = self.parse_repository_descriptor_package(child_node)
                repository_descriptor_packages_list.append(repository_descriptor_package)

        return repository_descriptor_packages_list

    def parse_repository_descriptor_package(self, descriptor_package):
        package_descriptor = PackageDescriptor()
        child_nodes = descriptor_package.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_descriptor_package_element(child_node, package_descriptor)

        return package_descriptor

    def parse_repository_descriptor_package_element(self, repository_descriptor_package_element, package_descriptor):
        node_name = repository_descriptor_package_element.nodeName

        if node_name == "name":
            package_descriptor.name = self.parse_repository_descriptor_package_name(repository_descriptor_package_element)
        elif node_name == "id":
            package_descriptor.id = self.parse_repository_descriptor_package_id(repository_descriptor_package_element)
        elif node_name == "version":
            package_descriptor.version = self.parse_repository_descriptor_package_version(repository_descriptor_package_element)
        elif node_name == "plugins":
            package_descriptor.plugins = self.parse_repository_descriptor_package_plugins(repository_descriptor_package_element)

    def parse_repository_descriptor_package_name(self, descriptor_package_name):
        repository_descriptor_package_name = descriptor_package_name.firstChild.data.strip()
        return repository_descriptor_package_name

    def parse_repository_descriptor_package_id(self, descriptor_package_id):
        repository_descriptor_package_id = descriptor_package_id.firstChild.data.strip()
        return repository_descriptor_package_id

    def parse_repository_descriptor_package_version(self, descriptor_package_version):
        repository_descriptor_package_version = descriptor_package_version.firstChild.data.strip()
        return repository_descriptor_package_version

    def parse_repository_descriptor_package_plugins(self, descriptor_package_plugins):
        repository_descriptor_package_plugins_list = []
        child_nodes = descriptor_package_plugins.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                repository_descriptor_package_plugin = self.parse_repository_descriptor_package_plugin(child_node)
                repository_descriptor_package_plugins_list.append(repository_descriptor_package_plugin)

        return repository_descriptor_package_plugins_list

    def parse_repository_descriptor_package_plugin(self, descriptor_package_plugin):
        package_plugin_descriptor = PackagePluginDescriptor()
        child_nodes = descriptor_package_plugin.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_descriptor_package_plugin_element(child_node, package_plugin_descriptor)

        return package_plugin_descriptor

    def parse_repository_descriptor_package_plugin_element(self, repository_descriptor_package_plugin_element, package_plugin_descriptor):
        node_name = repository_descriptor_package_plugin_element.nodeName

        if node_name == "id":
            package_plugin_descriptor.id = self.parse_repository_descriptor_package_plugin_id(repository_descriptor_package_plugin_element)
        elif node_name == "version":
            package_plugin_descriptor.version = self.parse_repository_descriptor_package_plugin_version(repository_descriptor_package_plugin_element)

    def parse_repository_descriptor_package_plugin_id(self, descriptor_package_plugin_id):
        repository_descriptor_package_plugin_id = descriptor_package_plugin_id.firstChild.data.strip()
        return repository_descriptor_package_plugin_id

    def parse_repository_descriptor_package_plugin_version(self, descriptor_package_plugin_version):
        repository_descriptor_package_plugin_version = descriptor_package_plugin_version.firstChild.data.strip()
        return repository_descriptor_package_plugin_version

    def parse_repository_descriptor_plugins(self, descriptor_plugins):
        repository_descriptor_plugins_list = []
        child_nodes = descriptor_plugins.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                repository_descriptor_plugin = self.parse_repository_descriptor_plugin(child_node)
                repository_descriptor_plugins_list.append(repository_descriptor_plugin)

        return repository_descriptor_plugins_list

    def parse_repository_descriptor_plugin(self, descriptor_plugin):
        plugin_descriptor = PluginDescriptor()
        child_nodes = descriptor_plugin.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_descriptor_plugin_element(child_node, plugin_descriptor)

        return plugin_descriptor

    def parse_repository_descriptor_plugin_element(self, repository_descriptor_plugin_element, plugin_descriptor):
        node_name = repository_descriptor_plugin_element.nodeName

        if node_name == "name":
            plugin_descriptor.name = self.parse_repository_descriptor_plugin_name(repository_descriptor_plugin_element)
        elif node_name == "id":
            plugin_descriptor.id = self.parse_repository_descriptor_plugin_id(repository_descriptor_plugin_element)
        elif node_name == "version":
            plugin_descriptor.version = self.parse_repository_descriptor_plugin_version(repository_descriptor_plugin_element)
        elif node_name == "main_module":
            plugin_descriptor.main_module = self.parse_repository_descriptor_plugin_main_module(repository_descriptor_plugin_element)
        elif node_name == "main_class":
            plugin_descriptor.main_class = self.parse_repository_descriptor_plugin_main_class(repository_descriptor_plugin_element)
        elif node_name == "file_name":
            plugin_descriptor.file_name = self.parse_repository_descriptor_plugin_file_name(repository_descriptor_plugin_element)
        elif node_name == "zip_file":
            plugin_descriptor.zip_file = self.parse_repository_descriptor_plugin_zip_file(repository_descriptor_plugin_element)

    def parse_repository_descriptor_plugin_name(self, descriptor_plugin_name):
        repository_descriptor_plugin_name = descriptor_plugin_name.firstChild.data.strip()
        return repository_descriptor_plugin_name

    def parse_repository_descriptor_plugin_id(self, descriptor_plugin_id):
        repository_descriptor_plugin_id = descriptor_plugin_id.firstChild.data.strip()
        return repository_descriptor_plugin_id

    def parse_repository_descriptor_plugin_version(self, descriptor_plugin_version):
        repository_descriptor_plugin_version = descriptor_plugin_version.firstChild.data.strip()
        return repository_descriptor_plugin_version

    def parse_repository_descriptor_plugin_main_module(self, descriptor_plugin_main_module):
        repository_descriptor_plugin_main_module = descriptor_plugin_main_module.firstChild.data.strip()
        return repository_descriptor_plugin_main_module

    def parse_repository_descriptor_plugin_main_class(self, descriptor_plugin_main_class):
        repository_descriptor_plugin_main_class = descriptor_plugin_main_class.firstChild.data.strip()
        return repository_descriptor_plugin_main_class

    def parse_repository_descriptor_plugin_file_name(self, descriptor_plugin_file_name):
        repository_descriptor_plugin_file_name = descriptor_plugin_file_name.firstChild.data.strip()
        return repository_descriptor_plugin_file_name

    def parse_repository_descriptor_plugin_zip_file(self, descriptor_plugin_zip_file):
        repository_descriptor_plugin_zip_file = descriptor_plugin_zip_file.firstChild.data.strip()
        return repository_descriptor_plugin_zip_file

class Repository:
    name = "none"
    description = "none"
    addresses = []

    def __init__(self, name = "none", description = "none"):
        self.name = name
        self.description = description
        self.addresses = []

class Address:
    name = "none"
    description = "none"
    value = "none"

    def __init__(self, name = "none", description = "none", value = "none"):
        self.name = name
        self.description = description
        self.value = value

class RepositoryDescriptor:
    name = "none"
    description = "none"
    packages = []
    plugins = []

    def __init__(self, name = "none", description = "none"):
        self.name = name
        self.description = description
        self.packages = []
        self.plugins = []

    def __repr__(self):
        return "<%s, %s>" % (
            self.__class__.__name__,
            self.name
        )

    def get_plugin(self, plugin_id, plugin_version = None):
        for plugin in self.plugins:
            if plugin.id == plugin_id:
                if not plugin_version:
                    return plugin
                elif plugin.version == plugin_version:
                    return plugin

    def get_plugin_name(self, plugin_name, plugin_version = None):
        for plugin in self.plugins:
            if plugin.name == plugin_name:
                if not plugin_version:
                    return plugin
                elif plugin.version == plugin_version:
                    return plugin

class PackageDescriptor:
    name = "none"
    id = "none"
    version = "none"
    plugins = []

    def __init__(self, name = "none", id = "none", version = "none"):
        self.name = name
        self.id = id
        self.version = version
        self.plugins = []

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.version
        )

class PackagePluginDescriptor:
    id = "none"
    version = "none"

    def __init__(self, id = "none", version = "none"):
        self.id = id
        self.version = version

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.version
        )

class PluginDescriptor:
    name = "none"
    id = "none"
    version = "none"
    main_class = "none"
    file_name = "none"
    zip_file = "none"

    def __init__(self, name = "none", id = "none", version = "none", main_class = "none", file_name = "none", zip_file = "none"):
        self.name = name
        self.id = id
        self.version = version
        self.main_class = main_class
        self.file_name = file_name
        self.zip_file = zip_file

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.version
        )

def valid_node(node):
    """
    Gets if a node is valid or not for parsing

    @type node: Node
    @param node: The Xml node to be validated
    @rtype: bool
    @return: The valid or not valid value
    """

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        return True
    else:
        return False
