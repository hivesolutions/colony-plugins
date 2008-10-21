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

__revision__ = "$LastChangedRevision: 2096 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:02:08 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class IceServiceManager:

    ice_service_manager_plugin = None
    
    ice_service_descriptors_list = []
    service_name_ice_service_descriptor_map = {}

    def __init__(self, ice_service_manager_plugin):
        self.ice_service_manager_plugin = ice_service_manager_plugin

        self.ice_service_descriptors_list = []
        self.service_name_ice_service_descriptor_map = {}
        
    def unload(self):
        pass

    def get_registered_ice_service_descriptors(self):
        return self.ice_service_descriptors_list

    def refresh_services(self):
        # retrieves all the ice service plugins available
        ice_service_plugins = self.ice_service_manager_plugin.ice_service_plugins

        for ice_service_plugin in ice_service_plugins:
            ice_service_descriptor = ice_service_plugin.get_ice_service_descriptor(IceServiceDescriptor)
            self.register_service(ice_service_descriptor)

    def register_service(self, ice_service_descriptor):
        # retrieves the ice service name
        ice_service_name = ice_service_descriptor.name

        # in case the ice service does not exists
        if not ice_service_name in self.service_name_ice_service_descriptor_map:
            self.ice_service_descriptors_list.append(ice_service_descriptor)
            self.service_name_ice_service_descriptor_map[ice_service_name] = ice_service_descriptor

    def start_service(self, ice_service_name):
        """
        Starts an ice service with the given name
        
        @type ice_service_name: String
        @param ice_service_name: The name of the service to be started
        """

        # in case the service is not registered
        if not ice_service_name in self.service_name_ice_service_descriptor_map:
            return

        # retrieves the ice helper plugin to access ice functions
        ice_helper_plugin = self.ice_service_manager_plugin.ice_helper_plugin

        # retrieves the ice service descriptor
        ice_service_descriptor = self.service_name_ice_service_descriptor_map[ice_service_name]

        # creates a new ice registry
        ice_helper_plugin.create_registry({})

        # creates a new ice node
        ice_helper_plugin.create_node({})

        # creates the admin access object
        admin_access_object = ice_helper_plugin.create_admin_access_complete("default.grid", "default -p 12000", "none", "none")

        # creates the application options
        application_options = ice_helper_plugin.get_default_application()

        # sets the service name
        application_options["name"] = ice_service_descriptor.name

        # sets the service description
        application_options["description"] = ice_service_descriptor.description

        application_server_templates = application_options["server_templates"]
        default_server_template = application_server_templates[0]
        default_server_template_templates_descriptor = default_server_template["descriptor"]
        default_server_template_templates_descriptor["execution_type"] = "python"
        templates_descriptor_options = default_server_template_templates_descriptor["options"]
        default_templates_descriptor_option = templates_descriptor_options[0]
        default_templates_descriptor_option["value"] = ice_service_descriptor.server_file_path 

        application_replica_groups = application_options["replica_groups"]

        default_replica_group = application_replica_groups[0]
        default_replica_group_objects = default_replica_group["objects"]

        for access_object in ice_service_descriptor.access_objects_list:
            default_replica_group_objects.append(access_object)

        # creates or updates the application
        ice_helper_plugin.create_update_application(admin_access_object, ice_service_descriptor.name, application_options)

        # closes the admin access object and the associated communicator
        ice_helper_plugin.close_access_communicator(admin_access_object)

    def stop_service(self, ice_service_name):
        pass

class IceServiceDescriptor:

    name = "none"
    description = "none"
    server_file_path = None
    access_objects_list = []

    def __init__(self, name = "none", description = "none", server_file_path = None, access_objects_list = []):
        self.name = name
        self.description = description
        self.server_file_path = server_file_path
        self.access_objects_list = access_objects_list
