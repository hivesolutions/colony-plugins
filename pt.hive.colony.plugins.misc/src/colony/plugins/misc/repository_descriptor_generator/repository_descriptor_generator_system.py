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

DEFAULT_REPOSITORY_LAYOUT = "simple"
""" The default repository layout """

COLONY_PACKING_TYPE = "colony_packing"
""" The colony packing type """

class RepositoryDescriptorGenerator:
    """
    The repository descriptor generator class.
    """

    repository_descriptor_generator_plugin = None
    """ The repository descriptor generator plugin """

    def __init__(self, repository_descriptor_generator_plugin):
        """
        Constructor of the class.

        @type repository_descriptor_generator_plugin: RepositoryDescriptorPlugin
        @param repository_descriptor_generator_plugin: The repository descriptor generator plugin
        """

        self.repository_descriptor_generator_plugin = repository_descriptor_generator_plugin

    def generate_repository_descriptor_file(self, file_path, repository_name = "none", repository_description = "none", repository_layout = DEFAULT_REPOSITORY_LAYOUT, bundles = [], plugins = [], libraries = []):
        # retrieves the repository descriptor string from the repository descriptor generator
        repository_descriptor_string = self.generate_repository_descriptor(repository_name, repository_description, repository_layout)

        # opens the file (to write the repository descriptor)
        file = open(file_path, "wb")

        try:
            # writes the repository descriptor to string
            # to the file
            file.write(repository_descriptor_string)
        finally:
            # closes the file
            file.close()

    def generate_repository_descriptor(self, repository_name = "none", repository_description = "none", repository_layout = DEFAULT_REPOSITORY_LAYOUT, bundles = [], plugins = [], libraries = []):
        """
        Generates a repository descriptor file (xml) using the current loaded plugins.
        The generated repository is named after the sent argument and description.
        The generated repository descriptor obeys the defined repository descriptor.

        @type repository_name: String
        @param repository_name: The name to be used to refer the repository.
        @type repository_description: String
        @param repository_description: The description to be used by the repository.
        @type repository_layout: String
        @param repository_layout: The layout to be used by the repository.
        @type bundles: List
        @param bundles: The list of bundle descriptors to generate the bundles.
        @type plugins: List
        @param plugins: The list of plugin descriptors to generate the plugins.
        @type libraries: List
        @param libraries: The list of library descriptors to generate the libraries.
        @rtype: String
        @return: The string containing the repository descriptor.
        """

        xml_document = xml.dom.minidom.Document()

        # creates the repository element
        repository_node = xml_document.createElement("repository")
        xml_document.appendChild(repository_node)

        # creates the repository name element
        repository_name_node = xml_document.createElement("name")
        repository_node.appendChild(repository_name_node)

        # creates the repository name value element
        repository_name_value_node = xml_document.createTextNode(repository_name)
        repository_name_node.appendChild(repository_name_value_node)

        # creates the repository description element
        repository_description_node = xml_document.createElement("description")
        repository_node.appendChild(repository_description_node)

        # creates the repository description value element
        repository_description_value_node = xml_document.createTextNode(repository_description)
        repository_description_node.appendChild(repository_description_value_node)

        # creates the repository layout element
        repository_layout_node = xml_document.createElement("layout")
        repository_node.appendChild(repository_layout_node)

        # creates the repository layout value element
        repository_description_layout_node = xml_document.createTextNode(repository_layout)
        repository_layout_node.appendChild(repository_description_layout_node)

        # creates the repository packages element
        repository_packages_node = xml_document.createElement("packages")
        repository_node.appendChild(repository_packages_node)

        # creates the repository bundles element
        repository_bundles_node = xml_document.createElement("bundles")
        repository_node.appendChild(repository_bundles_node)

        # creates the repository plugins element
        repository_plugins_node = xml_document.createElement("plugins")
        repository_node.appendChild(repository_plugins_node)

        # retrieves the plugin list for the plugin descriptors
        plugins_list = [self._get_plugin(value) for value in plugins]

        # iterates over all the plugins
        for plugin in plugins_list:
            repository_plugin_node = xml_document.createElement("plugin")
            repository_plugins_node.appendChild(repository_plugin_node)

            repository_plugin_name_node = xml_document.createElement("name")
            repository_plugin_node.appendChild(repository_plugin_name_node)

            repository_plugin_name_value_node = xml_document.createTextNode(plugin.id)
            repository_plugin_name_node.appendChild(repository_plugin_name_value_node)

            repository_plugin_type_node = xml_document.createElement("type")
            repository_plugin_node.appendChild(repository_plugin_type_node)

            repository_plugin_type_value_node = xml_document.createTextNode(COLONY_PACKING_TYPE)
            repository_plugin_type_node.appendChild(repository_plugin_type_value_node)

            repository_plugin_id_node = xml_document.createElement("id")
            repository_plugin_node.appendChild(repository_plugin_id_node)

            repository_plugin_id_value_node = xml_document.createTextNode(plugin.id)
            repository_plugin_id_node.appendChild(repository_plugin_id_value_node)

            repository_plugin_version_node = xml_document.createElement("version")
            repository_plugin_node.appendChild(repository_plugin_version_node)

            repository_plugin_version_value_node = xml_document.createTextNode(plugin.version)
            repository_plugin_version_node.appendChild(repository_plugin_version_value_node)

            repository_plugin_main_module_node = xml_document.createElement("main_module")
            repository_plugin_node.appendChild(repository_plugin_main_module_node)

            repository_plugin_main_module_value_node = xml_document.createTextNode("none")
            repository_plugin_main_module_node.appendChild(repository_plugin_main_module_value_node)

            repository_plugin_main_class_node = xml_document.createElement("main_class")
            repository_plugin_node.appendChild(repository_plugin_main_class_node)

            repository_plugin_main_class_value_node = xml_document.createTextNode("none")
            repository_plugin_main_class_node.appendChild(repository_plugin_main_class_value_node)

            repository_plugin_file_name_node = xml_document.createElement("file_name")
            repository_plugin_node.appendChild(repository_plugin_file_name_node)

            repository_plugin_file_name_value_node = xml_document.createTextNode("none")
            repository_plugin_file_name_node.appendChild(repository_plugin_file_name_value_node)

            repository_plugin_contents_file_node = xml_document.createElement("contents_file")
            repository_plugin_node.appendChild(repository_plugin_contents_file_node)

            repository_plugin_contents_file_value_node = xml_document.createTextNode(plugin.id + "_" + plugin.version + ".cpx")
            repository_plugin_contents_file_node.appendChild(repository_plugin_contents_file_value_node)

            repository_plugin_dependencies_node = xml_document.createElement("dependencies")
            repository_plugin_node.appendChild(repository_plugin_dependencies_node)

            plugin_plugin_dependencies = plugin.get_all_plugin_dependencies()

            # iterates over all the plugin dependencies to
            # write the dependencies values
            for plugin_dependency in plugin_plugin_dependencies:
                repository_plugin_plugin_dependency_node = xml_document.createElement("plugin_dependency")
                repository_plugin_dependencies_node.appendChild(repository_plugin_plugin_dependency_node)

                repository_plugin_plugin_id_node = xml_document.createElement("id")
                repository_plugin_plugin_dependency_node.appendChild(repository_plugin_plugin_id_node)

                repository_plugin_plugin_id_value_node = xml_document.createTextNode(plugin_dependency.plugin_id)
                repository_plugin_plugin_id_node.appendChild(repository_plugin_plugin_id_value_node)

                repository_plugin_plugin_version_node = xml_document.createElement("version")
                repository_plugin_plugin_dependency_node.appendChild(repository_plugin_plugin_version_node)

                repository_plugin_plugin_version_value_node = xml_document.createTextNode(plugin_dependency.plugin_version)
                repository_plugin_plugin_version_node.appendChild(repository_plugin_plugin_version_value_node)

        # generates the repository descriptor string from the xml document
        repository_descriptor_string = xml_document.toprettyxml(indent = "    ")

        # returns the repository descriptor string
        return repository_descriptor_string

    def _get_plugin(self, plugin_descriptor):
        # retrieves the plugin manager
        plugin_manager = self.repository_descriptor_generator_plugin.manager

        # retrieves the plugin descriptor id
        plugin_descriptor_id = plugin_descriptor["id"]

        # retrieves the plugin descriptor version
        plugin_descriptor_version = plugin_descriptor["version"]

        # retrieves the plugin for the given id and version
        plugin = plugin_manager._get_plugin_by_id_and_version(plugin_descriptor_id, plugin_descriptor_version)

        # returns the plugin
        return plugin
