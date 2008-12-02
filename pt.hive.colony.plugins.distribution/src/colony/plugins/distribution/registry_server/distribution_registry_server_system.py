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

DISTRIBUTION_SERVER_TYPE = "registry"
""" The distribution server type """

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
            elif registry_type == client:
                self.activate_server_client(properties)

    def activate_server_master(self, properties):
        # retrieves the plugin manager
        manager = self.distribution_registry_server_plugin.manager

        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_registry_server_plugin.distribution_registry_plugin

        # loads the registry with the given properties
        distribution_registry_plugin.load_registry({})

        self.distribution_bonjour_server_plugin.logger.info("Loading the distributed registry")

        # retrieves the main remote plugin
        main_remote_manager_plugin = self.distribution_bonjour_server_plugin.main_remote_manager_plugin

        # retrieves the available rpc handlers
        available_rpc_handlers = main_remote_manager_plugin.get_available_rpc_handlers()

        # retrieves the plugin manager uid
        manager_uid = manager.uid

        import socket

        hostname = socket.gethostname()

        distribution_registry_plugin.register_entry(hostname, "tobias", "default", [], {})

        self.distribution_bonjour_server_plugin.logger.info("Local entry registered")

    def activate_server_slave(self, properties):
        # retrieves the registry hostname
        registry_hostname = properties["registry_hostname"]

        # retrieves the registry port
        registry_hostname = properties["registry_port"]

    def activate_server_client(self, properties):
        # retrieves the registry hostname
        registry_hostname = properties["registry_hostname"]

        # retrieves the registry port
        registry_hostname = properties["registry_port"]
