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

    def generate_repository_descriptor_file(self, file_path, repository_name = "none", repository_description = "none", repository_layout = DEFAULT_REPOSITORY_LAYOUT, bundles = [], plugins = [], containers = []):
        # retrieves the repository descriptor string from the repository descriptor generator
        repository_descriptor_string = self.generate_repository_descriptor(repository_name, repository_description, repository_layout, bundles, plugins, containers)

        # opens the file (to write the repository descriptor)
        file = open(file_path, "wb")

        try:
            # writes the repository descriptor to string
            # to the file
            file.write(repository_descriptor_string)
        finally:
            # closes the file
            file.close()

    def generate_repository_descriptor(self, repository_name = "none", repository_description = "none", repository_layout = DEFAULT_REPOSITORY_LAYOUT, bundles = [], plugins = [], containers = []):
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
        @type containers: List
        @param containers: The list of container descriptors to generate the containers.
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

        # iterates over all the bundles
        for bundle in bundles:
            # retrieves the bundle id, version and dependencies
            bundle_id = bundle["id"]
            bundle_version = bundle["version"]
            bundle_dependencies = bundle["dependencies"]
            bundle_hash_digest = bundle["hash_digest"]

            # retrieves the bundle hash digest items
            bundle_hash_digest_items = bundle_hash_digest.items()

            # creates the bundle contents file
            bundle_contents_file = bundle_id + "_" + bundle_version + ".cbx"

            repository_bundle_node = xml_document.createElement("bundle")
            repository_bundles_node.appendChild(repository_bundle_node)

            repository_bundle_name_node = xml_document.createElement("name")
            repository_bundle_node.appendChild(repository_bundle_name_node)

            repository_bundle_name_value_node = xml_document.createTextNode(bundle_id)
            repository_bundle_name_node.appendChild(repository_bundle_name_value_node)

            repository_bundle_type_node = xml_document.createElement("type")
            repository_bundle_node.appendChild(repository_bundle_type_node)

            repository_bundle_type_value_node = xml_document.createTextNode(COLONY_PACKING_TYPE)
            repository_bundle_type_node.appendChild(repository_bundle_type_value_node)

            repository_bundle_id_node = xml_document.createElement("id")
            repository_bundle_node.appendChild(repository_bundle_id_node)

            repository_bundle_id_value_node = xml_document.createTextNode(bundle_id)
            repository_bundle_id_node.appendChild(repository_bundle_id_value_node)

            repository_bundle_version_node = xml_document.createElement("version")
            repository_bundle_node.appendChild(repository_bundle_version_node)

            repository_bundle_version_value_node = xml_document.createTextNode(bundle_version)
            repository_bundle_version_node.appendChild(repository_bundle_version_value_node)

            repository_bundle_contents_file_node = xml_document.createElement("contents_file")
            repository_bundle_node.appendChild(repository_bundle_contents_file_node)

            repository_bundle_contents_file_value_node = xml_document.createTextNode(bundle_contents_file)
            repository_bundle_contents_file_node.appendChild(repository_bundle_contents_file_value_node)

            repository_bundle_dependencies_node = xml_document.createElement("dependencies")
            repository_bundle_node.appendChild(repository_bundle_dependencies_node)

            # iterates over all the bundle dependencies to
            # write the dependencies values
            for bundle_dependency in bundle_dependencies:
                # retrieves the bundle dependency id and version
                bundle_dependency_id = bundle_dependency["id"]
                bundle_dependency_version = bundle_dependency["version"]

                repository_bundle_bundle_dependency_node = xml_document.createElement("bundle_dependency")
                repository_bundle_dependencies_node.appendChild(repository_bundle_bundle_dependency_node)

                repository_bundle_bundle_id_node = xml_document.createElement("id")
                repository_bundle_bundle_dependency_node.appendChild(repository_bundle_bundle_id_node)

                repository_bundle_bundle_id_value_node = xml_document.createTextNode(bundle_dependency_id)
                repository_bundle_bundle_id_node.appendChild(repository_bundle_bundle_id_value_node)

                repository_bundle_bundle_version_node = xml_document.createElement("version")
                repository_bundle_bundle_dependency_node.appendChild(repository_bundle_bundle_version_node)

                repository_bundle_bundle_version_value_node = xml_document.createTextNode(bundle_dependency_version)
                repository_bundle_bundle_version_node.appendChild(repository_bundle_bundle_version_value_node)

            repository_bundle_hash_digest_node = xml_document.createElement("hash_digest_items")
            repository_bundle_node.appendChild(repository_bundle_hash_digest_node)

            # iterates over all the bundle hash digest items to
            # write the hash digest item values
            for bundle_hash_digest_key, bundle_hash_digest_value in bundle_hash_digest_items:
                repository_bundle_bundle_hash_digest_item_node = xml_document.createElement("hash_digest")
                repository_bundle_hash_digest_node.appendChild(repository_bundle_bundle_hash_digest_item_node)

                repository_bundle_bundle_hash_digest_key_node = xml_document.createElement("key")
                repository_bundle_bundle_hash_digest_item_node.appendChild(repository_bundle_bundle_hash_digest_key_node)

                repository_bundle_bundle_hash_digest_key_value_node = xml_document.createTextNode(bundle_hash_digest_key)
                repository_bundle_bundle_hash_digest_key_node.appendChild(repository_bundle_bundle_hash_digest_key_value_node)

                repository_bundle_bundle_hash_digest_value_node = xml_document.createElement("value")
                repository_bundle_bundle_hash_digest_item_node.appendChild(repository_bundle_bundle_hash_digest_value_node)

                repository_bundle_bundle_hash_digest_value_value_node = xml_document.createTextNode(bundle_hash_digest_value)
                repository_bundle_bundle_hash_digest_value_node.appendChild(repository_bundle_bundle_hash_digest_value_value_node)

        # creates the repository plugins element
        repository_plugins_node = xml_document.createElement("plugins")
        repository_node.appendChild(repository_plugins_node)

        # iterates over all the plugins
        for plugin in plugins:
            # retrieves the plugin id, version, dependencies
            # and hash digest
            plugin_id = plugin["id"]
            plugin_version = plugin["version"]
            plugin_dependencies = plugin["dependencies"]
            plugin_hash_digest = plugin["hash_digest"]

            # retrieves the plugin hash digest items
            plugin_hash_digest_items = plugin_hash_digest.items()

            # creates the plugin contents file
            plugin_contents_file = plugin_id + "_" + plugin_version + ".cpx"

            repository_plugin_node = xml_document.createElement("plugin")
            repository_plugins_node.appendChild(repository_plugin_node)

            repository_plugin_name_node = xml_document.createElement("name")
            repository_plugin_node.appendChild(repository_plugin_name_node)

            repository_plugin_name_value_node = xml_document.createTextNode(plugin_id)
            repository_plugin_name_node.appendChild(repository_plugin_name_value_node)

            repository_plugin_type_node = xml_document.createElement("type")
            repository_plugin_node.appendChild(repository_plugin_type_node)

            repository_plugin_type_value_node = xml_document.createTextNode(COLONY_PACKING_TYPE)
            repository_plugin_type_node.appendChild(repository_plugin_type_value_node)

            repository_plugin_id_node = xml_document.createElement("id")
            repository_plugin_node.appendChild(repository_plugin_id_node)

            repository_plugin_id_value_node = xml_document.createTextNode(plugin_id)
            repository_plugin_id_node.appendChild(repository_plugin_id_value_node)

            repository_plugin_version_node = xml_document.createElement("version")
            repository_plugin_node.appendChild(repository_plugin_version_node)

            repository_plugin_version_value_node = xml_document.createTextNode(plugin_version)
            repository_plugin_version_node.appendChild(repository_plugin_version_value_node)

            repository_plugin_contents_file_node = xml_document.createElement("contents_file")
            repository_plugin_node.appendChild(repository_plugin_contents_file_node)

            repository_plugin_contents_file_value_node = xml_document.createTextNode(plugin_contents_file)
            repository_plugin_contents_file_node.appendChild(repository_plugin_contents_file_value_node)

            repository_plugin_dependencies_node = xml_document.createElement("dependencies")
            repository_plugin_node.appendChild(repository_plugin_dependencies_node)

            # iterates over all the plugin dependencies to
            # write the dependencies values
            for plugin_dependency in plugin_dependencies:
                # retrieves the plugin dependency id and version
                plugin_dependency_id = plugin_dependency["id"]
                plugin_dependency_version = plugin_dependency["version"]

                repository_plugin_plugin_dependency_node = xml_document.createElement("plugin_dependency")
                repository_plugin_dependencies_node.appendChild(repository_plugin_plugin_dependency_node)

                repository_plugin_plugin_id_node = xml_document.createElement("id")
                repository_plugin_plugin_dependency_node.appendChild(repository_plugin_plugin_id_node)

                repository_plugin_plugin_id_value_node = xml_document.createTextNode(plugin_dependency_id)
                repository_plugin_plugin_id_node.appendChild(repository_plugin_plugin_id_value_node)

                repository_plugin_plugin_version_node = xml_document.createElement("version")
                repository_plugin_plugin_dependency_node.appendChild(repository_plugin_plugin_version_node)

                repository_plugin_plugin_version_value_node = xml_document.createTextNode(plugin_dependency_version)
                repository_plugin_plugin_version_node.appendChild(repository_plugin_plugin_version_value_node)

            repository_plugin_hash_digest_node = xml_document.createElement("hash_digest_items")
            repository_plugin_node.appendChild(repository_plugin_hash_digest_node)

            # iterates over all the plugin hash digest items to
            # write the hash digest item values
            for plugin_hash_digest_key, plugin_hash_digest_value in plugin_hash_digest_items:
                repository_plugin_plugin_hash_digest_item_node = xml_document.createElement("hash_digest")
                repository_plugin_hash_digest_node.appendChild(repository_plugin_plugin_hash_digest_item_node)

                repository_plugin_plugin_hash_digest_key_node = xml_document.createElement("key")
                repository_plugin_plugin_hash_digest_item_node.appendChild(repository_plugin_plugin_hash_digest_key_node)

                repository_plugin_plugin_hash_digest_key_value_node = xml_document.createTextNode(plugin_hash_digest_key)
                repository_plugin_plugin_hash_digest_key_node.appendChild(repository_plugin_plugin_hash_digest_key_value_node)

                repository_plugin_plugin_hash_digest_value_node = xml_document.createElement("value")
                repository_plugin_plugin_hash_digest_item_node.appendChild(repository_plugin_plugin_hash_digest_value_node)

                repository_plugin_plugin_hash_digest_value_value_node = xml_document.createTextNode(plugin_hash_digest_value)
                repository_plugin_plugin_hash_digest_value_node.appendChild(repository_plugin_plugin_hash_digest_value_value_node)

        # creates the repository containers element
        repository_containers_node = xml_document.createElement("containers")
        repository_node.appendChild(repository_containers_node)

        # iterates over all the containers
        for container in containers:
            # retrieves the container id, version, dependencies
            # and hash digest
            container_id = container["id"]
            container_version = container["version"]
            container_dependencies = plugin["dependencies"]
            container_hash_digest = container["hash_digest"]

            # retrieves the container hash digest items
            container_hash_digest_items = container_hash_digest.items()

            # creates the container contents file
            container_contents_file = container_id + "_" + container_version + ".ccx"

            repository_container_node = xml_document.createElement("container")
            repository_containers_node.appendChild(repository_container_node)

            repository_container_name_node = xml_document.createElement("name")
            repository_container_node.appendChild(repository_container_name_node)

            repository_container_name_value_node = xml_document.createTextNode(container_id)
            repository_container_name_node.appendChild(repository_container_name_value_node)

            repository_container_type_node = xml_document.createElement("type")
            repository_container_node.appendChild(repository_container_type_node)

            repository_container_type_value_node = xml_document.createTextNode(COLONY_PACKING_TYPE)
            repository_container_type_node.appendChild(repository_container_type_value_node)

            repository_container_id_node = xml_document.createElement("id")
            repository_container_node.appendChild(repository_container_id_node)

            repository_container_id_value_node = xml_document.createTextNode(container_id)
            repository_container_id_node.appendChild(repository_container_id_value_node)

            repository_container_version_node = xml_document.createElement("version")
            repository_container_node.appendChild(repository_container_version_node)

            repository_container_version_value_node = xml_document.createTextNode(container_version)
            repository_container_version_node.appendChild(repository_container_version_value_node)

            repository_container_contents_file_node = xml_document.createElement("contents_file")
            repository_container_node.appendChild(repository_container_contents_file_node)

            repository_container_contents_file_value_node = xml_document.createTextNode(container_contents_file)
            repository_container_contents_file_node.appendChild(repository_container_contents_file_value_node)

            repository_container_contents_file_value_node = xml_document.createTextNode(container_contents_file)
            repository_container_contents_file_node.appendChild(repository_container_contents_file_value_node)

            repository_container_dependencies_node = xml_document.createElement("dependencies")
            repository_container_node.appendChild(repository_container_dependencies_node)

            # iterates over all the container dependencies to
            # write the dependencies values
            for container_dependency in container_dependencies:
                # retrieves the container dependency id and version
                container_dependency_id = container_dependency["id"]
                container_dependency_version = container_dependency["version"]

                repository_container_container_dependency_node = xml_document.createElement("container_dependency")
                repository_container_dependencies_node.appendChild(repository_container_container_dependency_node)

                repository_container_container_id_node = xml_document.createElement("id")
                repository_container_container_dependency_node.appendChild(repository_container_container_id_node)

                repository_container_container_id_value_node = xml_document.createTextNode(container_dependency_id)
                repository_container_container_id_node.appendChild(repository_container_container_id_value_node)

                repository_container_container_version_node = xml_document.createElement("version")
                repository_container_container_dependency_node.appendChild(repository_container_container_version_node)

                repository_container_container_version_value_node = xml_document.createTextNode(container_dependency_version)
                repository_container_container_version_node.appendChild(repository_container_container_version_value_node)

            repository_container_hash_digest_node = xml_document.createElement("hash_digest_items")
            repository_container_node.appendChild(repository_container_hash_digest_node)

            # iterates over all the container hash digest items to
            # write the hash digest item values
            for container_hash_digest_key, container_hash_digest_value in container_hash_digest_items:
                repository_container_container_hash_digest_item_node = xml_document.createElement("hash_digest")
                repository_container_hash_digest_node.appendChild(repository_container_container_hash_digest_item_node)

                repository_container_container_hash_digest_key_node = xml_document.createElement("key")
                repository_container_container_hash_digest_item_node.appendChild(repository_container_container_hash_digest_key_node)

                repository_container_container_hash_digest_key_value_node = xml_document.createTextNode(container_hash_digest_key)
                repository_container_container_hash_digest_key_node.appendChild(repository_container_container_hash_digest_key_value_node)

                repository_container_container_hash_digest_value_node = xml_document.createElement("value")
                repository_container_container_hash_digest_item_node.appendChild(repository_container_container_hash_digest_value_node)

                repository_container_container_hash_digest_value_value_node = xml_document.createTextNode(container_hash_digest_value)
                repository_container_container_hash_digest_value_node.appendChild(repository_container_container_hash_digest_value_value_node)

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
