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

import socket

DISTRIBUTION_SERVER_TYPE = "registry"
""" The distribution server type """

RESERVED_NAMES = [
    "registry_type",
    "registry_hostname",
    "registry_port",
    "registry_type",
    "endpoint_type"
]
""" The reserved names list """

class DistributionRegistryServer:
    """
    The distribution registry server class.
    """

    distribution_registry_server_plugin = None
    """ The distribution registry server plugin """

    def __init__(self, distribution_registry_server_plugin):
        """
        Constructor of the class.

        @type distribution_registry_server_plugin: DistributionRegistryServerPlugin
        @param distribution_registry_server_plugin: The distribution registry server plugin.
        """

        self.distribution_registry_server_plugin = distribution_registry_server_plugin

    def get_distribution_server_type(self):
        """
        Retrieves the distribution server type.

        @rtype: String
        @return: The distribution server type.
        """

        return DISTRIBUTION_SERVER_TYPE

    def activate_server(self, properties):
        """
        Activates the distribution registry server.

        @type properties: Dictionary
        @param properties: The properties for the registry server activation.
        """

        if "registry_type" in properties:
            # retrieves the registry type
            registry_type = properties["registry_type"]

            # in case the registry type is master
            if registry_type == "master":
                self.activate_server_master(properties)
            # in case the registry type is slave
            elif registry_type == "slave":
                self.activate_server_slave(properties)
            # in case the registry type is client
            elif registry_type == "client":
                self.activate_server_client(properties)

    def deactivate_server(self, properties):
        """
        Deactivates the distribution registry server.

        @type properties: Dictionary
        @param properties: The properties for the registry server deactivation.
        """

        if "registry_type" in properties:
            # retrieves the registry type
            registry_type = properties["registry_type"]

            # in case the registry type is master
            if registry_type == "master":
                self.deactivate_server_master(properties)
            # in case the registry type is slave
            elif registry_type == "slave":
                self.deactivate_server_slave(properties)
            # in case the registry type is client
            elif registry_type == "client":
                self.deactivate_server_client(properties)

    def activate_server_master(self, properties):
        # retrieves the plugin manager
        manager = self.distribution_registry_server_plugin.manager

        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_registry_server_plugin.distribution_registry_plugin

        # loads the registry with the given properties
        distribution_registry_plugin.load_registry({})

        self.distribution_registry_server_plugin.info("Loading the distributed registry")

        # retrieves the main remote plugin
        main_remote_manager_plugin = self.distribution_registry_server_plugin.main_remote_manager_plugin

        # retrieves the available rpc handlers
        available_rpc_handlers = main_remote_manager_plugin.get_available_rpc_handlers()

        # retrieves the plugin manager uid
        manager_uid = manager.uid

        # retrieves the hostname
        hostname = socket.gethostname()

        # retrieves the ip address
        ip_address = socket.gethostbyname(hostname)

        # retrieves the list of available endpoints
        endpoints = self.get_available_endpoints()

        # registers the entry
        distribution_registry_plugin.register_entry(ip_address, manager_uid, "default", endpoints, {})

        self.distribution_registry_server_plugin.info("Local entry registered")

    def activate_server_slave(self, properties):
        # retrieves the registry client
        registry_client = self.get_registry_client(properties)

        if not registry_client:
            return

    def activate_server_client(self, properties):
        # retrieves the registry client
        registry_client = self.get_registry_client(properties)

        if not registry_client:
            return

        # retrieves the plugin manager
        manager = self.distribution_registry_server_plugin.manager

        # retrieves the plugin manager uid
        manager_uid = manager.uid

        # retrieves the hostname
        hostname = socket.gethostname()

        # retrieves the ip address
        ip_address = socket.gethostbyname(hostname)

        # retrieves the list of available endpoints
        endpoints = self.get_available_endpoints()

        registry_client.distribution_registry.register_entry(ip_address, manager_uid, "default", endpoints, {})

    def deactivate_server_master(self, properties):
        pass

    def deactivate_server_slave(self, properties):
        pass

    def deactivate_server_client(self, properties):
        # retrieves the registry client
        registry_client = self.get_registry_client(properties)

        if not registry_client:
            return

        # retrieves the plugin manager
        manager = self.distribution_registry_server_plugin.manager

        # retrieves the plugin manager uid
        manager_uid = manager.uid

        # retrieves the hostname
        hostname = socket.gethostname()

        # retrieves the ip address
        ip_address = socket.gethostbyname(hostname)

        registry_client.distribution_registry.unregister_entry(ip_address, manager_uid)

    def get_registry_client(self, properties):
        """
        Retrieves the registry client for the given properties.

        @type properties: Dictionary
        @param properties: The properties to retrieve the registry client.
        @rtype:
        """

        # retrieves the distribution helper plugins list
        distribution_helper_plugins = self.distribution_registry_server_plugin.distribution_helper_plugins

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

    def get_available_endpoints(self):
        """
        Retrieves the list of available endpoints.

        @rtype: List
        @return: The list of available endpoints.
        """

        # creates the available endpoints list
        available_endpoints = []

        # retrieves the main remote plugin
        main_remote_manager_plugin = self.distribution_registry_server_plugin.main_remote_manager_plugin

        # retrieves the available rpc handlers
        available_rpc_handlers = main_remote_manager_plugin.get_available_rpc_handlers()

        # iterates over all the available rpc handlers
        for available_rpc_handler in available_rpc_handlers:
            # retrieves the available rpc handler name
            available_rpc_handler_name = available_rpc_handler.get_handler_name()

            # retrieves the available rpc handler port
            available_rpc_handler_port = available_rpc_handler.get_handler_port()

            # retrieves the available rpc handler properties
            available_rpc_handler_properties = available_rpc_handler.get_handler_properties()

            # creates the enpoint tuple
            endpoint = (
                available_rpc_handler_name,
                available_rpc_handler_port,
                available_rpc_handler_properties
            )

            # adds the endpoint tuple to the list of available endpoints
            available_endpoints.append(endpoint)

        # returns the available endpoints
        return available_endpoints
