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

BASE_PROTOCOL_SUFIX = "_tcp"
""" The base protocol sufix """

PROTOCOL_SUFIX = "_colony"
""" The protocol sufix """

LOCAL_DOMAIN = "local"
""" The local domain """

class DistributionBonjourClient:
    """
    The distribution bonjour client class.
    """

    distribution_bonjour_client_plugin = None
    """ The distribution bonjour client plugin """

    def __init__(self, distribution_bonjour_client_plugin):
        """
        Constructor of the class.

        @type distribution_bonjour_client_plugin: DistributionBonjourClientPlugin
        @param distribution_bonjour_client_plugin: The distribution bonjour client plugin.
        """

        self.distribution_bonjour_client_plugin = distribution_bonjour_client_plugin

    def start_distribution_bonjour_client(self):
        # retrieves the bonjour plugin
        bonjour_plugin = self.distribution_bonjour_client_plugin.bonjour_plugin

        # creates the complete protocol name
        complete_protocol_name = PROTOCOL_SUFIX + "." + BASE_PROTOCOL_SUFIX

        # creates the domain
        domain = LOCAL_DOMAIN + "."

        # adds the service for browsing
        bonjour_plugin.add_service_for_browsing(complete_protocol_name, domain)

    def stop_distribution_bonjour_client(self):
        # retrieves the bonjour plugin
        bonjour_plugin = self.distribution_bonjour_client_plugin.bonjour_plugin

        # creates the complete protocol name
        complete_protocol_name = PROTOCOL_SUFIX + "." + BASE_PROTOCOL_SUFIX

        # creates the domain
        domain = LOCAL_DOMAIN + "."

        # adds the service for browsing
        bonjour_plugin.remove_service_for_browsing(complete_protocol_name, domain)

    def get_remote_instance_references(self, properties):
        # retrieves the bonjour plugin
        bonjour_plugin = self.distribution_bonjour_client_plugin.bonjour_plugin

        # creates the list of bonjour remote references
        bonjour_remote_references = []

        # creates the complete protocol name
        complete_protocol_name = PROTOCOL_SUFIX + "." + BASE_PROTOCOL_SUFIX

        # creates the domain
        domain = LOCAL_DOMAIN + "."

        # retrieves the available bonjour services
        bonjour_services = bonjour_plugin.browse_bonjour_services_fast(complete_protocol_name, domain)

        # iterates over all the bonjour services
        for bonjour_service in bonjour_services:
            # unpacks the bonjour service tuple
            bonjour_service_reference_string, bonjour_service_hostname, bonjour_service_port = bonjour_service

            # creates a new bonjour remote reference
            bonjour_remote_reference = BonjourRemoteReference()

            # retrieves the parsed bonjour service reference
            parsed_bonjour_service_reference = self.parse_bonjour_service_reference(bonjour_service_reference_string)

            # in case the parse was successful
            if parsed_bonjour_service_reference:
                # parses the bonjour service reference string retrieving the plugin manager unique id and the service type
                bonjour_service_properties_list, bonjour_service_plugin_manager_uid, bonjour_service_service_type = parsed_bonjour_service_reference

                # sets the plugin manager unique id in the bonjour remote reference
                bonjour_remote_reference.plugin_manager_uid = bonjour_service_plugin_manager_uid

                # sets the service type in the bonjour remote reference
                bonjour_remote_reference.service_type = bonjour_service_service_type

                # sets the hostname in the bonjour remote reference
                bonjour_remote_reference.hostname = bonjour_service_hostname

                # sets the port in the bonjour remote reference
                bonjour_remote_reference.port = bonjour_service_port

                # sets the properties list in the bonjour remote reference
                bonjour_remote_reference.properties_list = bonjour_service_properties_list

                # sets the bonjour service in the bonjour remote reference
                bonjour_remote_reference.bonjour_service = bonjour_service

                # adds the created bonjour remote reference to the list of bonjour remote references
                bonjour_remote_references.append(bonjour_remote_reference)

        return bonjour_remote_references

    def parse_bonjour_service_reference(self, bonjour_service_reference_string):
        """
        Parses the bonjour service reference, retrieving a tuple with the
        plugin manager unique id and the service type.

        @type bonjour_service_reference_string: String
        @param bonjour_service_reference_string: The service reference string.
        @rtype: tuple
        @return: A tuple containing the plugin manager unique id and the service type.
        """

        # retrieves the first and second references from the service reference string
        first_reference, _second_reference = bonjour_service_reference_string.split("._colony._tcp.local.")

        # splits the first reference
        first_reference_splitted = first_reference.split(".")

        # in case the length of the first reference is not three
        if not len(first_reference_splitted) == 3:
            return

        # retrieves the base bonjour service properties, the base plugin manager unique id and the base service type
        bonjour_service_properties, bonjour_service_plugin_manager_uid, bonjour_service_service_type = first_reference.split(".")

        # creates the bonjour service properties list
        bonjour_service_properties_list = []

        # retrieves the bonjour service properties from the base bonjour service properties
        bonjour_service_properties = bonjour_service_properties[2:-1]

        # in case there are bonjour service properties defined
        if bonjour_service_properties:
            # splits the bonjour service properties
            bonjour_service_properties_splitted = bonjour_service_properties.split(":")

            # iterates over all the splitted bonjour service properties
            for bonjour_service_property_splitted in bonjour_service_properties_splitted:
                bonjour_service_properties_list.append(bonjour_service_property_splitted)

        # retrieves the plugin manager unique id from the base plugin manager unique id
        bonjour_service_plugin_manager_uid = bonjour_service_plugin_manager_uid[1:-1]

        # retrieves the service type from the base service type
        bonjour_service_service_type = bonjour_service_service_type[1:]

        # returns a tuple containing the plugin manager unique id and the service type
        return (
            bonjour_service_properties_list,
            bonjour_service_plugin_manager_uid,
            bonjour_service_service_type
        )

class BonjourRemoteReference:
    """
    The bonjour remote reference class.
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

    bonjour_service = None
    """ The bonjour service tuple """

    def __init__(self, plugin_manager_uid = "none", service_type = "none", hostname = "none", port = None, bonjour_service = None):
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
        @type bonjour_service: Tuple
        @param bonjour_service: The bonjour service tuple.
        """

        self.plugin_manager_uid = plugin_manager_uid
        self.service_type = service_type
        self.hostname = hostname
        self.port = port
        self.properties_list = []
        self.bonjour_service = bonjour_service

    def __repr__(self):
        return "<%s, %s, %s, %s, %i>" % (
            self.__class__.__name__,
            self.plugin_manager_uid,
            self.service_type,
            self.hostname,
            self.port
        )
