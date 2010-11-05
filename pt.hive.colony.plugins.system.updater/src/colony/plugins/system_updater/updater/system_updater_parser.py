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
    """
    The repositories file parser class.
    """

    file_path = None
    """ The file path """

    repository_list = []
    """ The repository list """

    def __init__(self, file_path = None):
        """
        Constructor of the class.

        @type file_path: String
        @param file_path: The file path.
        """

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
        child_nodes = address.childNodes
        address_structure.name = address.getAttribute("name")
        address_structure.value = address.firstChild.data.strip()

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_address_element(child_node, address_structure)

        return address_structure

    def parse_address_element(self, address_element, address):
        node_name = address_element.nodeName

        if node_name == "authentication":
            address.authentication = self.parse_repository_descriptor_name(address_element)

    def parse_authentication(self, authentication):
        authentication_structure = Authentication()
        child_nodes = authentication.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_authentication_element(child_node, authentication_structure)

        return authentication_structure

    def parse_authentication_element(self, authentication_element, authentication):
        node_name = authentication_element.nodeName

        if node_name == "username":
            authentication.username = self.parse_authentication_username(authentication_element)
        elif node_name == "password":
            authentication.password = self.parse_authentication_password(authentication_element)
        elif node_name == "method":
            authentication.method = self.parse_authentication_method(authentication_element)

    def parse_authentication_username(self, authentication_username):
        authentication_username_value = authentication_username.firstChild.data.strip()
        return authentication_username_value

    def parse_authentication_password(self, authentication_password):
        authentication_password_value = authentication_password.firstChild.data.strip()
        return authentication_password_value

    def parse_authentication_method(self, authentication_method):
        authentication_method_value = authentication_method.firstChild.data.strip()
        return authentication_method_value

class RepositoryDescriptorFileParser(Parser):
    """
    The repository descriptor file parser class.
    """

    file = None
    """ The file """

    repository_descriptor = None
    """ The repository descriptor """

    def __init__(self, file = None):
        """
        Constructor of the class.

        @type file: File
        @param file: The file.
        """

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
        elif node_name == "bundles":
            repository_descriptor.bundles = self.parse_repository_descriptor_bundles(repository_descriptor_element)
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

    def parse_repository_descriptor_bundles(self, descriptor_bundles):
        repository_descriptor_bundles_list = []
        child_nodes = descriptor_bundles.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                repository_descriptor_bundle = self.parse_repository_descriptor_bundle(child_node)
                repository_descriptor_bundles_list.append(repository_descriptor_bundle)

        return repository_descriptor_bundles_list

    def parse_repository_descriptor_bundle(self, descriptor_bundle):
        bundle_descriptor = BundleDescriptor()
        child_nodes = descriptor_bundle.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_descriptor_bundle_element(child_node, bundle_descriptor)

        return bundle_descriptor

    def parse_repository_descriptor_bundle_element(self, repository_descriptor_bundle_element, bundle_descriptor):
        node_name = repository_descriptor_bundle_element.nodeName

        if node_name == "name":
            bundle_descriptor.name = self.parse_repository_descriptor_bundle_name(repository_descriptor_bundle_element)
        elif node_name == "type":
            bundle_descriptor.bundle_type = self.parse_repository_descriptor_bundle_type(repository_descriptor_bundle_element)
        elif node_name == "id":
            bundle_descriptor.id = self.parse_repository_descriptor_bundle_id(repository_descriptor_bundle_element)
        elif node_name == "version":
            bundle_descriptor.version = self.parse_repository_descriptor_bundle_version(repository_descriptor_bundle_element)
        elif node_name == "contents_file":
            bundle_descriptor.contents_file = self.parse_repository_descriptor_bundle_contents_file(repository_descriptor_bundle_element)
        elif node_name == "dependencies":
            bundle_descriptor.dependencies = self.parse_repository_descriptor_bundle_dependencies(repository_descriptor_bundle_element)

    def parse_repository_descriptor_bundle_name(self, descriptor_bundle_name):
        repository_descriptor_bundle_name = descriptor_bundle_name.firstChild.data.strip()
        return repository_descriptor_bundle_name

    def parse_repository_descriptor_bundle_type(self, descriptor_bundle_type):
        repository_descriptor_bundle_type = descriptor_bundle_type.firstChild.data.strip()
        return repository_descriptor_bundle_type

    def parse_repository_descriptor_bundle_id(self, descriptor_bundle_id):
        repository_descriptor_bundle_id = descriptor_bundle_id.firstChild.data.strip()
        return repository_descriptor_bundle_id

    def parse_repository_descriptor_bundle_version(self, descriptor_bundle_version):
        repository_descriptor_bundle_version = descriptor_bundle_version.firstChild.data.strip()
        return repository_descriptor_bundle_version

    def parse_repository_descriptor_bundle_contents_file(self, descriptor_bundle_contents_file):
        repository_descriptor_bundle_contents_file = descriptor_bundle_contents_file.firstChild.data.strip()
        return repository_descriptor_bundle_contents_file

    def parse_repository_descriptor_bundle_dependencies(self, descriptor_bundle_dependencies):
        repository_descriptor_bundle_dependencies_list = []
        child_nodes = descriptor_bundle_dependencies.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                repository_descriptor_bundle_dependency = self.parse_repository_descriptor_bundle_dependency(child_node)
                repository_descriptor_bundle_dependencies_list.append(repository_descriptor_bundle_dependency)

        return repository_descriptor_bundle_dependencies_list

    def parse_repository_descriptor_bundle_dependency(self, dependency_bundle):
        bundle_dependency = BundleDependency()
        child_nodes = dependency_bundle.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_repository_descriptor_bundle_dependency_element(child_node, bundle_dependency)

        return bundle_dependency

    def parse_repository_descriptor_bundle_dependency_element(self, repository_descriptor_bundle_dependency_element, bundle_dependency):
        node_name = repository_descriptor_bundle_dependency_element.nodeName

        if node_name == "id":
            bundle_dependency.id = self.parse_repository_descriptor_bundle_dependency_id(repository_descriptor_bundle_dependency_element)
        elif node_name == "version":
            bundle_dependency.version = self.parse_repository_descriptor_bundle_dependency_version(repository_descriptor_bundle_dependency_element)

    def parse_repository_descriptor_bundle_dependency_id(self, bundle_dependency_id):
        repository_descriptor_bundle_dependency_id = bundle_dependency_id.firstChild.data.strip()
        return repository_descriptor_bundle_dependency_id

    def parse_repository_descriptor_bundle_dependency_version(self, bundle_dependency_version):
        repository_descriptor_bundle_dependency_version = bundle_dependency_version.firstChild.data.strip()
        return repository_descriptor_bundle_dependency_version

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
    """ The name of the repository """

    description = "none"
    """ The description of the repository """

    layout = "none"
    """ The layout of the repository """

    addresses = []
    """ The addresses of the repository """

    def __init__(self, name = "none", description = "none", layout = "none"):
        """
        Constructor of the class.

        @type name: String
        @param name: The name of the repository.
        @type description: String
        @param description: The description of the repository.
        @type layout: String
        @param layout: The layout of the repository.
        @type addresses: List
        @param addresses: The addresses of the repository.
        """

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
    """ The name of the address """

    description = "none"
    """ The description of the address """

    value = "none"
    """ The value of the address """

    authentication = None
    """ The authentication of the address """

    def __init__(self, name = "none", description = "none", value = "none", authentication = None):
        """
        Constructor of the class.

        @type name: String
        @param name: The name of the address.
        @type description: String
        @param description: The description of the address.
        @type value: String
        @param value: The value of the address.
        @type authentication: Authentication
        @param authentication: The authentication of the address.
        """

        self.name = name
        self.description = description
        self.value = value
        self.authentication = authentication

    def __repr__(self):
        return "<%s, %s>" % (
            self.__class__.__name__,
            self.value
        )

class Authentication:
    """
    The authentication class.
    """

    username = "none"
    """ The username of the authentication """

    password = "none"
    """ The password of the authentication """

    method = "none"
    """ The method of the authentication """

    def __init__(self, username = "none", password = "none", method = "none"):
        """
        Constructor of the class.

        @type username: String
        @param username: The username of the authentication.
        @type password: String
        @param password: The password of the authentication.
        @type method: String
        @param method: The method of the authentication.
        """

        self.username = username
        self.password = password
        self.method = method

    def __repr__(self):
        return "<%s, %s, %s, %s>" % (
            self.__class__.__name__,
            self.username,
            self.password,
            self.method
        )

class RepositoryDescriptor:
    """
    The repository descriptor class.
    """

    name = "none"
    """ The name of the repository descriptor """

    description = "none"
    """ The description of the repository descriptor """

    layout = "none"
    """ The layout of the repository descriptor """

    packages = []
    """ The packages of the repository descriptor """

    plugins = []
    """ The plugins of the repository descriptor """

    def __init__(self, name = "none", description = "none", layout = "none"):
        """
        Constructor of the class.

        @type name: String
        @param name: The name of the repository descriptor.
        @type description: String
        @param description: The description of the repository descriptor.
        @type layout: String
        @param layout: The layout of the repository descriptor.
        """

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
    """ The name of the package descriptor """

    package_type = "none"
    """ The package type of the package descriptor """

    id = "none"
    """ The id of the package descriptor """

    version = "none"
    """ The version of the package descriptor """

    plugins = []
    """ The plugins of the package descriptor """

    def __init__(self, name = "none", package_type = "none", id = "none", version = "none"):
        """
        Constructor of the class.

        @type name: String
        @param name: The name of the package descriptor.
        @type package_type: String
        @param package_type: The package type of the package descriptor.
        @type id: String
        @param id: The id of the package descriptor.
        @type version: String
        @param version: The version of the package descriptor.
        """

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
    """ The id of the package plugin descriptor """

    version = "none"
    """ The version of the package plugin descriptor """

    def __init__(self, id = "none", version = "none"):
        """
        Constructor of the class.

        @type id: String
        @param id: The id of the package plugin descriptor.
        @type version: String
        @param version: The version of the package plugin descriptor.
        """

        self.id = id
        self.version = version

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.id,
            self.version
        )

class BundleDescriptor:
    """
    The bundle descriptor class.
    """

    name = "none"
    """ The name of the bundle descriptor """

    bundle_type = "none"
    """ The bundle type of the bundle descriptor """

    id = "none"
    """ The id of the bundle descriptor """

    version = "none"
    """ The version of the bundle descriptor """

    dependencies = []
    """ The dependencies of the bundle descriptor """

    def __init__(self, name = "none", bundle_type = "none", id = "none", version = "none"):
        """
        Constructor of the class.

        @type name: String
        @param name: The name of the bundle descriptor.
        @type bundle_type: String
        @param bundle_type: The bundle type of the bundle descriptor.
        @type id: String
        @param id: The id of the bundle descriptor.
        @type version: String
        @param version: The version of the bundle descriptor.
        """

        self.name = name
        self.bundle_type = bundle_type
        self.id = id
        self.version = version

        self.dependencies = []

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.version
        )

class BundleDependency:
    """
    The bundle dependency class.
    """

    id = "none"
    """ The id of the bundle dependency """

    version = "none"
    """ The version of the bundle dependency """

    def __init__(self, id = "none", version = "none"):
        """
        Constructor of the class.

        @type id: String
        @param id: The id of the bundle dependency.
        @type version: String
        @param version: The version of the bundle dependency.
        """

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
    """ The name of the plugin descriptor """

    plugin_type = "none"
    """ The plugin type of the plugin descriptor """

    id = "none"
    """ The id of the plugin descriptor """

    version = "none"
    """ The version of the plugin descriptor """

    main_class = "none"
    """ The main class of the plugin descriptor """

    file_name = "none"
    """ The file class of the plugin descriptor """

    contents_file = "none"
    """ The contents file of the plugin descriptor """

    dependencies = []
    """ The dependencies of the plugin descriptor """

    def __init__(self, name = "none", plugin_type = "none", id = "none", version = "none", main_class = "none", file_name = "none", contents_file = "none"):
        """
        Constructor of the class.

        @type name: String
        @param name: The name of the plugin descriptor.
        @type plugin_type: String
        @param plugin_type: The plugin type of the plugin descriptor.
        @type id: String
        @param id: The id of the plugin descriptor.
        @type version: String
        @param version: The version of the plugin descriptor.
        @type main_class: String
        @param main_class: The main class of the plugin descriptor.
        @type file_name: String
        @param file_name: The file name of the plugin descriptor.
        @type contents_file: String
        @param contents_file: The contents file of the plugin descriptor.
        """

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
        """
        Constructor of the class.

        @type id: String
        @param id: The id of the plugin dependency.
        @type version: String
        @param version: The version of the plugin dependency.
        """

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

    # in case the node is of type element
    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        # returns true (valid)
        return True
    # otherwise
    else:
        # returns false (invalid)
        return False
