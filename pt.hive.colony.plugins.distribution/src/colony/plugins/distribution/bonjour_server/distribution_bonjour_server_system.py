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

DISTRIBUTION_SERVER_TYPE = "bonjour"
""" The distribution server type """

PROPERTIES_SUFIX = "_pp"
""" The properties sufix """

BASE_PROTOCOL_SUFIX = "_tcp"
""" The base protocol sufix """

PROTOCOL_SUFIX = "_colony"
""" The protocol sufix """

LOCAL_DOMAIN = "local"
""" The local domain """

DEFAULT_PORT = 25
""" The default port """

class DistributionBonjourServer:
    """
    The distribution bonjour server class.
    """

    distribution_bonjour_server_plugin = None
    """ The distribution bonjour server plugin """

    def __init__(self, distribution_bonjour_server_plugin):
        """
        Constructor of the class.
        
        @type distribution_bonjour_server_plugin: DistributionBonjourServerPlugin
        @param distribution_bonjour_server_plugin: The distribution bonjour server plugin.
        """

        self.distribution_bonjour_server_plugin = distribution_bonjour_server_plugin

    def get_distribution_server_type(self):
        """
        Retrieves the distribution server type.
        
        @rtype: String
        @return: The distribution server type.
        """

        return DISTRIBUTION_SERVER_TYPE

    def activate_server(self, properties):
        """
        Activates the distribution bonjour server.
        
        @type properties: Dictionary
        @param properties: The properties for the bonjour server activation.
        """

        # retrieves the plugin manager
        manager = self.distribution_bonjour_server_plugin.manager

        # retrieves the bonjour plugin
        bonjour_plugin = self.distribution_bonjour_server_plugin.bonjour_plugin

        # retrieves the main remote plugin
        main_remote_manager_plugin = self.distribution_bonjour_server_plugin.main_remote_manager_plugin

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

            # starts the service id
            service_id = PROPERTIES_SUFIX + "_"

            # creates the is first flag
            is_first = True

            # iterates over the available rpc handler properties
            for available_rpc_handler_property in available_rpc_handler_properties:
                # retrieves the available rpc handler value
                available_rpc_handler_value = available_rpc_handler_properties[available_rpc_handler_property]

                # in case it is the first value
                if is_first:
                    is_first = False
                else:
                    # adds the property separator token
                    service_id += ":"

                # adds the property value
                service_id += str(available_rpc_handler_value)

            # adds the service id separator
            service_id += "."

            # creates the service id
            service_id += "_" + manager.uid + "._" + available_rpc_handler_name

            # creates the complete protocol name
            complete_protocol_name = PROTOCOL_SUFIX + "." + BASE_PROTOCOL_SUFIX

            # creates the domain
            domain = LOCAL_DOMAIN + "."

            # creates the hostname
            hostname = socket.gethostname()

            # creates the ip address
            ip_address = socket.gethostbyname(hostname)

            # register the dummy bonjour service
            bonjour_plugin.register_bonjour_service(service_id, complete_protocol_name, domain, ip_address, available_rpc_handler_port)

            self.distribution_bonjour_server_plugin.logger.info("Registering bonjour service '%s'", (service_id))
