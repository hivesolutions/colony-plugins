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

import xml.dom.minidom

class Parser:
    """
    The abstract parser class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def parse(self):
        """
        Parses the defined file.
        """

        pass

    def get_value(self):
        """
        Retrieves the result of the parse.

        @rtype: Object
        @return: The result of the parse.
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
        elif node_name == "layout":
            repository.layout = self.parse_layout(repository_element)
        elif node_name == "addresses":
            repository.addresses = self.parse_addresses(repository_element)

    def parse_name(self, name):
        repository_name = name.firstChild.data.strip()
        return repository_name

    def parse_description(self, description):
        repository_description = description.firstChild.data.strip()
        return repository_description

    def parse_layout(self, layout):
        repository_layout = layout.firstChild.data.strip()
        return repository_layout

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

    def get_repository_descriptor(self):
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
        elif node_name == "layout":
            repository_descriptor.layout = self.parse_repository_descriptor_layout(repository_descriptor_element)
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

    def parse_repository_descriptor_layout(self, descriptor_layout):
        repository_descriptor_layout = descriptor_layout.firstChild.data.strip()
        return repository_descriptor_layout

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
        elif node_name == "type":
            package_descriptor.package_type = self.parse_repository_descriptor_package_type(repository_descriptor_package_element)
        elif node_name == "id":
            package_descriptor.id = self.parse_repository_descriptor_package_id(repository_descriptor_package_element)
        elif node_name == "version":
            package_descriptor.version = self.parse_repository_descriptor_package_version(repository_descriptor_package_element)
        elif node_name == "plugins":
            package_descriptor.plugins = self.parse_repository_descriptor_package_plugins(repository_descriptor_package_element)

    def parse_repository_descriptor_package_name(self, descriptor_package_name):
        repository_descriptor_package_name = descriptor_package_name.firstChild.data.strip()
        return repository_descriptor_package_name

    def parse_repository_descriptor_package_type(self, descriptor_package_type):
        repository_descriptor_package_type = descriptor_package_type.firstChild.data.strip()
        return repository_descriptor_package_type

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
        elif node_name == "type":
            plugin_descriptor.plugin_type = self.parse_repository_descriptor_plugin_type(repository_descriptor_plugin_element)
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
        elif node_name == "contents_file":
            plugin_descriptor.contents_file = self.parse_repository_descriptor_plugin_contents_file(repository_descriptor_plugin_element)
        elif node_name == "dependencies":
            plugin_descriptor.dependencies = self.parse_repository_descriptor_plugin_dependencies(repository_descriptor_plugin_element)

    def parse_repository_descriptor_plugin_name(self, descriptor_plugin_name):
        repository_descriptor_plugin_name = descriptor_plugin_name.firstChild.data.strip()
        return repository_descriptor_plugin_name

    def parse_repository_descriptor_plugin_type(self, descriptor_plugin_type):
        repository_descriptor_plugin_type = descriptor_plugin_type.firstChild.data.strip()
        return repository_descriptor_plugin_type

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

    def parse_repository_descriptor_plugin_contents_file(self, descriptor_plugin_contents_file):
        repository_descriptor_plugin_contents_file = descriptor_plugin_contents_file.firstChild.data.strip()
        return repository_descriptor_plugin_contents_file

    def parse_repository_descriptor_plugin_dependencies(self, descriptor_plugin_dependencies):
        repository_descriptor_plugin_dependencies_list = []
        child_nodes = descriptor_plugin_dependencies.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                repository_descriptor_plugin_dependency = self.parse_repository_descriptor_plugin_dependency(child_node)
                repository_descriptor_plugin_dependencies_list.append(repository_descriptor_plugin_dependency)

        return repository_descriptor_plugin_dependencies_list

    def parse_repository_descriptor_plugin_dependency(self, dependency_plugin):
        plugin_dependency = PluginDependency()
        child_nodes = dependency_plugin.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_descriptor_plugin_dependency_element(child_node, plugin_dependency)

        return plugin_dependency

    def parse_repository_descriptor_plugin_dependency_element(self, repository_descriptor_plugin_dependency_element, plugin_dependency):
        node_name = repository_descriptor_plugin_dependency_element.nodeName

        if node_name == "id":
            plugin_dependency.id = self.parse_repository_descriptor_plugin_dependency_id(repository_descriptor_plugin_dependency_element)
        elif node_name == "version":
            plugin_dependency.version = self.parse_repository_descriptor_plugin_dependency_version(repository_descriptor_plugin_dependency_element)

    def parse_repository_descriptor_plugin_dependency_id(self, plugin_dependency_id):
        repository_descriptor_plugin_dependency_id = plugin_dependency_id.firstChild.data.strip()
        return repository_descriptor_plugin_dependency_id

    def parse_repository_descriptor_plugin_dependency_version(self, plugin_dependency_version):
        repository_descriptor_plugin_dependency_version = plugin_dependency_version.firstChild.data.strip()
        return repository_descriptor_plugin_dependency_version

class Repository:
    """
    The repository class.
    """

    name = "none"
    description = "none"
    layout = "none"
    addresses = []

    def __init__(self, name = "none", description = "none", layout = "none"):
        self.name = name
        self.description = description
        self.addresses = []

    def __repr__(self):
        return "<%s, %s>" % (
            self.__class__.__name__,
            self.name
        )

class Address:
    """
    The address class.
    """

    name = "none"
    description = "none"
    value = "none"

    def __init__(self, name = "none", description = "none", value = "none"):
        self.name = name
        self.description = description
        self.value = value

    def __repr__(self):
        return "<%s, %s>" % (
            self.__class__.__name__,
            self.value
        )

class RepositoryDescriptor:
    """
    The repository descriptor class.
    """

    name = "none"
    description = "none"
    layout = "none"
    packages = []
    plugins = []

    def __init__(self, name = "none", description = "none", layout = "none"):
        self.name = name
        self.description = description
        self.packages = []
        self.plugins = []

    def __repr__(self):
        return "<%s, %s>" % (
            self.__class__.__name__,
            self.name
        )

    def get_package(self, package_id, package_version = None):
        for package in self.packages:
            if package.id == package_id:
                if not package_version:
                    return package
                elif package.version == package_version:
                    return package

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
    """
    The package descriptor class.
    """

    name = "none"
    package_type = "none"
    id = "none"
    version = "none"
    plugins = []

    def __init__(self, name = "none", package_type = "none", id = "none", version = "none"):
        self.name = name
        self.package_type = package_type
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
    """
    The package plugin descriptor class.
    """

    id = "none"
    version = "none"

    def __init__(self, id = "none", version = "none"):
        self.id = id
        self.version = version

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.id,
            self.version
        )

class PluginDescriptor:
    """
    The plugin descriptor class.
    """

    name = "none"
    plugin_type = "none"
    id = "none"
    version = "none"
    main_class = "none"
    file_name = "none"
    contents_file = "none"
    dependencies = []

    def __init__(self, name = "none", plugin_type = "none", id = "none", version = "none", main_class = "none", file_name = "none", contents_file = "none"):
        self.name = name
        self.plugin_type = plugin_type
        self.id = id
        self.version = version
        self.main_class = main_class
        self.file_name = file_name
        self.contents_file = contents_file
        self.dependencies = []

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.version
        )

class PluginDependency:
    """
    The plugin dependency class.
    """

    id = "none"
    """ The id of the plugin dependency """

    version = "none"
    """ The version of the plugin dependency """

    def __init__(self, id = "none", version = "none"):
        self.id = id
        self.version = version

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.id,
            self.version
        )

def valid_node(node):
    """
    Gets if a node is valid or not for parsing.

    @type node: Node
    @param node: The Xml node to be validated.
    @rtype: bool
    @return: The valid or not valid value.
    """

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        return True
    else:
        return False
