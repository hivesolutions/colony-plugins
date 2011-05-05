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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class DistributionServer:
    """
    The distribution server class.
    """

    distribution_server_plugin = None
    """ The distribution server plugin """

    def __init__(self, distribution_server_plugin):
        """
        Constructor of the class.

        @type distribution_server_plugin: DistributionServerPlugin
        @param distribution_server_plugin: The distribution server plugin.
        """

        self.distribution_server_plugin = distribution_server_plugin

    def activate_server(self, plugin = None, properties = {}):
        """
        Activates the distribution server.

        @type plugin: Plugin
        @param plugin: The plugin containing the distribution server to be activated.
        @type properties: Dictionary
        @param properties: The properties for the server activation.
        """

        if plugin:
            # sets the distribution server adapter plugins as a list containing the defined plugin
            distribution_server_adapter_plugins = [
                plugin
            ]
        else:
            # retrieves the distribution server adapter plugins
            distribution_server_adapter_plugins = self.distribution_server_plugin.distribution_server_adapter_plugins

        # retrieves the resource manager plugin
        resource_manager_plugin = self.distribution_server_plugin.resource_manager_plugin

        # iterates over all the distribution server adapter plugins
        for distribution_server_adapter_plugin in distribution_server_adapter_plugins:
            # retrieves the distribution server adapter plugin resources
            distribution_server_adapter_plugin_resources = resource_manager_plugin.get_resources(distribution_server_adapter_plugin.id)

            # merges the available properties and the gathered resources
            self.merge_properties_resources(properties, distribution_server_adapter_plugin_resources)

            # activates the distribution server adapter server
            distribution_server_adapter_plugin.activate_server(properties)

    def deactivate_server(self, plugin = None, properties = {}):
        """
        Deactivates the distribution server.

        @type plugin: Plugin
        @param plugin: The plugin containing the distribution server to be deactivated.
        @type properties: Dictionary
        @param properties: The properties for the server deactivation.
        """

        if plugin:
            # sets the distribution server adapter plugins as a list containing the defined plugin
            distribution_server_adapter_plugins = [
                plugin
            ]
        else:
            # retrieves the distribution server adapter plugins
            distribution_server_adapter_plugins = self.distribution_server_plugin.distribution_server_adapter_plugins

        # retrieves the resource manager plugin
        resource_manager_plugin = self.distribution_server_plugin.resource_manager_plugin

        # iterates over all the distribution server adapter plugins
        for distribution_server_adapter_plugin in distribution_server_adapter_plugins:
            # retrieves the distribution server adapter plugin resources
            distribution_server_adapter_plugin_resources = resource_manager_plugin.get_resources(distribution_server_adapter_plugin.id)

            # merges the available properties and the gathered resources
            self.merge_properties_resources(properties, distribution_server_adapter_plugin_resources)

            # deactivates the distribution server adapter server
            distribution_server_adapter_plugin.deactivate_server(properties)

    def merge_properties_resources(self, properties, resources):
        """
        Merges the map containing properties and the given list of resources.

        @type properties: Dictionary
        @param properties: The properties map to be merged with the given resources.
        @type resources: List
        @param resources: The list of resources to be merged with the properties map.
        """

        # iterates over all the resources
        for resource in resources:
            # retrieves the resource name
            resource_name = resource.name

            # retrieves the resource data
            resource_data = resource.data

            # sets the property
            properties[resource_name] = resource_data
