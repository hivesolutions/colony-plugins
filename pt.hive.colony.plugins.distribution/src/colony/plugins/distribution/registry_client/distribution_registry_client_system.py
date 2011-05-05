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

RESERVED_NAMES = [
    "registry_type",
    "registry_hostname",
    "registry_port",
    "registry_type",
    "endpoint_type"
]
""" The reserved names list """

class DistributionRegistryClient:
    """
    The distribution registry client class.
    """

    distribution_registry_client_plugin = None
    """ The distribution registry client plugin """

    def __init__(self, distribution_registry_client_plugin):
        """
        Constructor of the class.

        @type distribution_registry_client_plugin: DistributionRegistryClientPlugin
        @param distribution_registry_client_plugin: The distribution registry client plugin.
        """

        self.distribution_registry_client_plugin = distribution_registry_client_plugin

    def get_remote_instance_references(self, properties):
        # in case there are no properties defined
        if not properties:
            return []

        # creates the list of bonjour remote references
        registry_remote_references = []

        # retrieves the registry client
        registry_client = self.get_registry_client(properties)

        # retrieves the registry entries
        registry_entries = registry_client.get_all_registry_entries()

        # iterates over all the registry entries
        for registry_entry in registry_entries:
            # retrieves the plugin manager unique id
            plugin_manager_uid = registry_entry["name"]

            # retrieves the hostname
            hostname = registry_entry["hostname"]

            # retrieves the endpoints
            endpoints = registry_entry["endpoints"]

            # iterates over all the endpoints
            for endpoint in endpoints:
                # retrieves the service type, port and properties map from the endpoint
                service_type, port, properties_map = endpoint

                # creates the properties list from the properties map
                properties_list = properties_map.values()

                # creates a new registry remote reference
                registry_remote_reference = RegistryRemoteReference()

                # sets the plugin manager unique id in the registry remote reference
                registry_remote_reference.plugin_manager_uid = plugin_manager_uid

                # sets the service type in the registry remote reference
                registry_remote_reference.service_type = service_type

                # sets the hostname in the registry remote reference
                registry_remote_reference.hostname = hostname

                # sets the port in the registry remote reference
                registry_remote_reference.port = port

                # sets the properties list in the registry remote reference
                registry_remote_reference.properties_list = properties_list

                # sets the registry entry list in the registry remote reference
                registry_remote_reference.registry_entry = registry_entry

                # adds the created registry remote reference to the list of registry remote references
                registry_remote_references.append(registry_remote_reference)

        # returns the registry remote references
        return registry_remote_references

    def get_registry_client(self, properties):
        """
        Retrieves the registry client for the given properties.

        @type properties: Dictionary
        @param properties: The properties to retrieve the registry client.
        @rtype:
        """

        # retrieves the distribution helper plugins list
        distribution_helper_plugins = self.distribution_registry_client_plugin.distribution_helper_plugins

        # retrieves the registry hostname
        registry_hostname = properties["registry_hostname"]

        # retrieves the registry port
        registry_port = properties["registry_port"]

        # retrieves the registry end point type
        registry_endpoint_type = properties["endpoint_type"]

        # creates the map of non reserved properties
        non_reserved_properties = {}

        # iterates over all the properties
        for property_key in properties:
            # in case the property key name is not reserved
            if not property_key in RESERVED_NAMES:
                # retrieves the property value
                property_value = properties[property_key]

                # adds the property value to the map of non reserved properties
                non_reserved_properties[property_key] = property_value

        # iterates over all the distribution helper plugins
        for distribution_helper_plugin in distribution_helper_plugins:
            # retrieves the helper name
            helper_name = distribution_helper_plugin.get_helper_name()

            # in case the helper name is the same as the registry endpoint type
            if helper_name == registry_endpoint_type:
                # calls the helper to retrieve the client using the host information
                return distribution_helper_plugin.create_client_host(registry_hostname, registry_port, non_reserved_properties)

class RegistryRemoteReference:
    """
    The registry remote reference class.
    """

    plugin_manager_uid = "none"
    """ The plugin manager unique id """

    service_type = "none"
    """ The service type """

    hostname = "none"
    """ The hostname """

    port = None
    """ The port """

    properties_list = []
    """ The properties list """

    registry_entry = None
    """ The registry entry tuple """

    def __init__(self, plugin_manager_uid = "none", service_type = "none", hostname = "none", port = None, registry_entry = None):
        """
        Constructor of the class.

        @type plugin_manager_uid: String
        @param plugin_manager_uid: The plugin manager unique id.
        @type service_type: String
        @param service_type: The service type.
        @type hostname: String
        @param hostname: The hostname.
        @type port: int
        @param port: The port.
        @type registry_entry: Tuple
        @param registry_entry: The registry entry tuple.
        """

        self.plugin_manager_uid = plugin_manager_uid
        self.service_type = service_type
        self.hostname = hostname
        self.port = port
        self.properties_list = []
        self.registry_entry = registry_entry

    def __repr__(self):
        return "<%s, %s, %s, %s, %i>" % (
            self.__class__.__name__,
            self.plugin_manager_uid,
            self.service_type,
            self.hostname,
            self.port
        )
