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

import os
import sys
import subprocess
import copy
import Ice
import IceGrid

class IceHelper:

    ice_helper_plugin = None

    created_registry_descriptors_list = []
    created_registry_name_created_registry_descriptor_map = {}
    created_node_descriptors_list = []
    created_registry_name_created_node_descriptors_list_map = {}
    created_registry_name_created_node_name_created_node_descriptors_list_map = {}

    def __init__(self, ice_helper_plugin):
        self.ice_helper_plugin = ice_helper_plugin

        self.created_registry_descriptors_list = []
        self.created_registry_name_created_registry_descriptor_map = {}
        self.created_node_descriptors_list = []
        self.created_registry_name_created_node_descriptors_list_map = {}
        self.created_registry_name_created_node_name_created_node_descriptors_list_map = {}

    def unload(self):
        """
        Unloads the ice subsystem "killing" all the ice grid nodes and registries
        """

        # in case there are no available registry
        if not len(self.created_registry_descriptors_list):
            # returns immediately (there's nothing to do)
            return

        # clones the registry descriptors list
        created_registry_descriptors_list_clone = copy.copy(self.created_registry_descriptors_list)

        # iterates over all the registry descriptors
        for created_registry_descriptor in created_registry_descriptors_list_clone:
            # retrieves the created registry name
            created_registry_name = created_registry_descriptor.ice_grid_instance_name

            # retrieves the created registry replica names
            created_registry_replica_names_list = created_registry_descriptor.ice_grid_registry_replica_names_list

            # clones the created registry replica names
            created_registry_replica_names_list_clone = copy.copy(created_registry_replica_names_list)

            # create an admin access object
            admin_access = self.create_admin_access_complete(created_registry_name)

            # in case there are nodes for the current registry
            if created_registry_name in self.created_registry_name_created_node_descriptors_list_map:
                # retrieves the created nodes list
                created_node_descriptors_list = self.created_registry_name_created_node_descriptors_list_map[created_registry_name]

                # clones the created nodes list
                created_node_descriptors_list_clone = copy.copy(created_node_descriptors_list)

                # iterates over all the created nodes
                for created_node_descriptor in created_node_descriptors_list_clone:
                    # retrieves the created ice grid node name
                    created_node_name = created_node_descriptor.ice_grid_node_name

                    # kills the created ice grid node
                    self.kill_node(admin_access, created_registry_name, created_node_name)

            # start the exist master flag
            exists_master = False

            # iterates over all the replica names to kill all the registry replicas
            for created_registry_replica_name in created_registry_replica_names_list_clone:
                # in case the replica is of type Master
                if created_registry_replica_name == "Master":
                    exists_master = True
                # in case the replica is just a "normal" replica
                else:
                    # kill the registry replica
                    self.kill_registry(admin_access, created_registry_name, created_registry_replica_name)

            # in case there is a master replica
            if exists_master:
                # kills the master replica
                self.kill_registry(admin_access, created_registry_name, "Master")

    def load_ice_file(self, file_path):
        Ice.loadSlice(file_path)

    def create_registry(self, start_options):
        """
        Creates an ice grid registry with the given start options

        @type start_options: Dictionary
        @param start_options: The start options for the ice grid registry creation
        """

        ice_grid_registry_path = "C:/Programs/Ice-3.2.1/bin/icegridregistry.exe"
        ice_grid_instance_name = "default.grid"
        ice_grid_default_locator = "default.grid/Locator:default -p 12000"
        ice_grid_registry_client_endpoints = "default -p 12000"
        ice_grid_registry_server_endpoints = "default"
        ice_grid_registry_internal_endpoints = "default"
        ice_grid_registry_data = "db/registry/default.grid/Master"
        ice_grid_registry_replica_name = "Master"
        ice_grid_registry_permissions_verifier = "default.grid/NullPermissionsVerifier"
        ice_grid_registry_admin_permissions_verifier = "default.grid/NullPermissionsVerifier"
        ice_grid_registry_ssl_permissions_verifier = "default.grid/NullSSLPermissionsVerifier"
        ice_grid_registry_admin_ssl_permissions_verifier = "default.grid/NullSSLPermissionsVerifier"
        ice_grid_admin_username = "foo"
        ice_grid_admin_password = "bar"
        ice_grid_registry_log_file = "logs/default.grid/Master/ice_grid_log.log"
        ice_grid_registry_log_file_mode = "a"

        # iterates over all the start options to retrieve their values
        for key in start_options:
            if key == "ice_grid_registry_path":
                ice_grid_registry_path = start_options["ice_grid_registry_path"]
            elif key == "ice_grid_instance_name":
                ice_grid_instance_name = start_options["ice_grid_instance_name"]
            elif key == "ice_grid_default_locator":
                ice_grid_default_locator = start_options["ice_grid_default_locator"]
            elif key == "ice_grid_registry_client_endpoints":
                ice_grid_registry_client_endpoints = start_options["ice_grid_registry_client_endpoints"]
            elif key == "ice_grid_registry_server_endpoints":
                ice_grid_registry_server_endpoints = start_options["ice_grid_registry_server_endpoints"]
            elif key == "ice_grid_registry_internal_endpoints":
                ice_grid_registry_internal_endpoints = start_options["ice_grid_registry_internal_endpoints"]
            elif key == "ice_grid_registry_data":
                ice_grid_registry_data = start_options["ice_grid_registry_data"]
            elif key == "ice_grid_registry_replica_name":
                ice_grid_registry_replica_name = start_options["ice_grid_registry_replica_name"]
            elif key == "ice_grid_registry_permissions_verifier":
                ice_grid_registry_permissions_verifier = start_options["ice_grid_registry_permissions_verifier"]
            elif key == "ice_grid_registry_admin_permissions_verifier":
                ice_grid_registry_admin_permissions_verifier = start_options["ice_grid_registry_admin_permissions_verifier"]
            elif key == "ice_grid_registry_ssl_permissions_verifier":
                ice_grid_registry_ssl_permissions_verifier = start_options["ice_grid_registry_ssl_permissions_verifier"]
            elif key == "ice_grid_registry_admin_ssl_permissions_verifier":
                ice_grid_registry_admin_ssl_permissions_verifier = start_options["ice_grid_registry_admin_ssl_permissions_verifier"]
            elif key == "ice_grid_admin_username":
                ice_grid_admin_username = start_options["ice_grid_admin_username"]
            elif key == "ice_grid_admin_password":
                ice_grid_admin_password = start_options["ice_grid_admin_password"]
            elif key == "ice_grid_registry_log_file":
                ice_grid_registry_log_file = start_options["ice_grid_registry_log_file"]
            elif key == "ice_grid_registry_log_file_mode":
                ice_grid_registry_log_file_mode = start_options["ice_grid_registry_log_file_mode"]

        # in case the current os is windows
        if os.name == "nt":
            import win32con
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = win32con.SW_HIDE
        else:
            startup_info = None

        # in case the directory for the data files is not created
        if not os.path.isdir(ice_grid_registry_data):
            os.makedirs(ice_grid_registry_data)

        # retrieves the directory for the log file
        ice_grid_registry_log_file_directory = os.path.dirname(ice_grid_registry_log_file)

        # in case the directory for the log file is not created
        if not os.path.isdir(ice_grid_registry_log_file_directory):
            os.makedirs(ice_grid_registry_log_file_directory)

        # opens the log file
        ice_registry_log_file = open(ice_grid_registry_log_file, ice_grid_registry_log_file_mode)

        # seeks the file to the end
        ice_registry_log_file.seek(0, os.SEEK_END)

        # creates the list of parameters for the call
        params = [ice_grid_registry_path, "--IceGrid.InstanceName=" + ice_grid_instance_name, "--Ice.Default.Locator=" + ice_grid_default_locator, "--IceGrid.Registry.Client.Endpoints=" + ice_grid_registry_client_endpoints,
                  "--IceGrid.Registry.Server.Endpoints=" + ice_grid_registry_server_endpoints, "--IceGrid.Registry.Internal.Endpoints=" + ice_grid_registry_internal_endpoints, "--IceGrid.Registry.Data=" + ice_grid_registry_data,
                  "--IceGrid.Registry.ReplicaName=" + ice_grid_registry_replica_name, "--IceGrid.Registry.PermissionsVerifier=" + ice_grid_registry_permissions_verifier, "--IceGrid.Registry.AdminPermissionsVerifier=" + ice_grid_registry_admin_permissions_verifier,
                  "--IceGrid.Registry.SSLPermissionsVerifier=" + ice_grid_registry_ssl_permissions_verifier, "--IceGrid.Registry.AdminSSLPermissionsVerifier=" + ice_grid_registry_admin_ssl_permissions_verifier,
                  "--IceGridAdmin.Username=" + ice_grid_admin_username, "--IceGridAdmin.Password=" + ice_grid_admin_password]

        # calls the icegridregistry executable
        subprocess.Popen(params, stdin = ice_registry_log_file, stdout = ice_registry_log_file, stderr = ice_registry_log_file, env = os.environ, startupinfo = startup_info)

        # in case the ice grid instance is already created
        if ice_grid_instance_name in self.created_registry_name_created_registry_descriptor_map:
            # retrieves the existing ice grid registry descriptor object
            ice_grid_registry_descriptor = self.created_registry_name_created_registry_descriptor_map[ice_grid_instance_name]

            # adds the replica name to the list of replica names of the existing ice grid registry descriptor
            ice_grid_registry_descriptor.ice_grid_registry_replica_names_list.append(ice_grid_registry_replica_name)
        # in case there is no ice grid descriptor instance created
        else:
            # creates the ice grid registry descriptor object
            ice_grid_registry_descriptor = IceGridRegistryDescriptor(ice_grid_instance_name, [ice_grid_registry_replica_name])

            # sets the map to point to the correct ice grid descriptor
            self.created_registry_name_created_registry_descriptor_map[ice_grid_instance_name] = ice_grid_registry_descriptor

            # appends the created ice grid registry descriptor to the list of created ice grid registry descriptors
            self.created_registry_descriptors_list.append(ice_grid_registry_descriptor)

    def kill_registry(self, admin_access_object, registry_name, registry_replica_name = "Master"):
        # in case the registry exists and is loaded
        if registry_name in self.created_registry_name_created_registry_descriptor_map:

            # retrieves the registry descriptor
            registry_descriptor = self.created_registry_name_created_registry_descriptor_map[registry_name]

            # retrieves the list of registry replica names
            registry_replica_names_list = registry_descriptor.ice_grid_registry_replica_names_list

            # in case the replica exists in the list of registry replicas
            if registry_replica_name in registry_replica_names_list:
                # removes the replica from the list of registry replicas
                registry_replica_names_list.remove(registry_replica_name)

            # in case there are no more replicas let in the current ice grid registry
            if not len(registry_replica_names_list):
                self.created_registry_descriptors_list.remove(registry_descriptor)
                del self.created_registry_name_created_registry_descriptor_map[registry_name]

                # in case the registry has associated node descriptors list
                if registry_name in self.created_registry_name_created_node_descriptors_list_map:
                    del self.created_registry_name_created_node_descriptors_list_map[registry_name]

            # retrieves all the registry names
            registry_names_list = admin_access_object.getAllRegistryNames()

            # in case the node exists in the registry
            if registry_replica_name in registry_names_list:
                # kills the registry object
                admin_access_object.shutdownRegistry(registry_replica_name)

    def create_node(self, start_options):
        """
        Creates an ice grid node with the given start options

        @type start_options: Dictionary
        @param start_options: The start options for the ice grid node creation
        """

        ice_grid_node_path = "C:/Programs/Ice-3.2.1/bin/icegridnode.exe"
        ice_grid_instance_name = "default.grid"
        ice_default_locator = "default.grid/Locator:default -p 12000"
        ice_grid_node_data = "db/node/default.grid/node1"
        ice_grid_node_endpoints = "default"
        ice_grid_node_name = "node1"
        ice_grid_node_trace_activator = 1
        ice_grid_node_trace_patch = 1
        ice_grid_node_log_file = "logs/default.grid/node1/ice_node_log.log"
        ice_grid_node_log_file_mode = "a"

        # iterates over all the start options to retrieve their values
        for key in start_options:
            if key == "ice_grid_node_path":
                ice_grid_node_path = start_options["ice_grid_node_path"]
            elif key == "ice_grid_instance_name":
                ice_grid_instance_name = start_options["ice_grid_instance_name"]
            elif key == "ice_default_locator":
                ice_default_locator = start_options["ice_default_locator"]
            elif key == "ice_grid_node_data":
                ice_grid_node_data = start_options["ice_grid_node_data"]
            elif key == "ice_grid_node_endpoints":
                ice_grid_node_endpoints = start_options["ice_grid_node_endpoints"]
            elif key == "ice_grid_node_name":
                ice_grid_node_name = start_options["ice_grid_node_name"]
            elif key == "ice_grid_node_trace_activator":
                ice_grid_node_trace_activator = start_options["ice_grid_node_trace_activator"]
            elif key == "ice_grid_node_trace_patch":
                ice_grid_node_trace_patch = start_options["ice_grid_node_trace_patch"]
            elif key == "ice_grid_node_log_file":
                ice_grid_node_log_file = start_options["ice_grid_node_log_file"]
            elif key == "ice_grid_node_log_file_mode":
                ice_grid_node_log_file_mode = start_options["ice_grid_node_log_file_mode"]

        # in case the current os is windows
        if os.name == "nt":
            import win32con
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = win32con.SW_HIDE
        else:
            startup_info = None

        # in case the directory for the data files is not created
        if not os.path.isdir(ice_grid_node_data):
            os.makedirs(ice_grid_node_data)

        # retrieves the directory for the log file
        ice_grid_node_log_file_directory = os.path.dirname(ice_grid_node_log_file)

        # in case the directory for the log file is not created
        if not os.path.isdir(ice_grid_node_log_file_directory):
            os.makedirs(ice_grid_node_log_file_directory)

        # opens the log file
        ice_node_log_file = open(ice_grid_node_log_file, ice_grid_node_log_file_mode)

        # seeks the file to the end
        ice_node_log_file.seek(0, os.SEEK_END)

        # creates the list of parameters for the call
        params = [ice_grid_node_path, "--Ice.Default.Locator=" + ice_default_locator, "--IceGrid.Node.Data=" + ice_grid_node_data, "--IceGrid.Node.Endpoints=" + ice_grid_node_endpoints,
                  "--IceGrid.Node.Name=" + ice_grid_node_name, "--IceGrid.Node.Trace.Activator=" + str(ice_grid_node_trace_activator), "--IceGrid.Node.Trace.Patch=" + str(ice_grid_node_trace_patch)]

        # calls the icegridnode executable
        subprocess.Popen(params, stdin = ice_node_log_file, stdout = ice_node_log_file, stderr = ice_node_log_file, env = os.environ, startupinfo = startup_info)

        # creates the ice grid node descriptor object
        ice_grid_node_descriptor = IceGridNodeDescriptor(ice_grid_node_name, ice_grid_instance_name)

        # adds the ice grid node descriptor to the list of created ice grid node descriptors
        self.created_node_descriptors_list.append(ice_grid_node_descriptor)

        # in case there is no list of node descriptors for the current ice grid instance
        if not ice_grid_instance_name in self.created_registry_name_created_node_descriptors_list_map:
            self.created_registry_name_created_node_descriptors_list_map[ice_grid_instance_name] = []

        # adds the ice grid node descriptor to the list of ice grid node descriptors for the current ice grid instance
        self.created_registry_name_created_node_descriptors_list_map[ice_grid_instance_name].append(ice_grid_node_descriptor)

        # adds the ice grid node to the registry name node name node descriptors list map
        self.created_registry_name_created_node_name_created_node_descriptors_list_map[(ice_grid_instance_name, ice_grid_node_name)] = ice_grid_node_descriptor

    def kill_node(self, admin_access_object, registry_name, node_name):
        # creates the complete node tuple using the registry name and the node name
        complete_node_name_tuple = (registry_name, node_name)

        # in case the node exists and is loaded
        if complete_node_name_tuple in self.created_registry_name_created_node_name_created_node_descriptors_list_map:
            # retrieves the node descriptor
            node_descriptor = self.created_registry_name_created_node_name_created_node_descriptors_list_map[complete_node_name_tuple]

            # removes the node descriptor from the list of node descriptors
            self.created_node_descriptors_list.remove(node_descriptor)

            # removes the node descriptor from the list of node descriptor of the current registry
            self.created_registry_name_created_node_descriptors_list_map[registry_name].remove(node_descriptor)

            # removes the key to the current node
            del self.created_registry_name_created_node_name_created_node_descriptors_list_map[complete_node_name_tuple]

            # retrieves all the node names
            node_names_list = admin_access_object.getAllNodeNames()

            # in case the node exists in the registry
            if node_name in node_names_list:
                # kills the node object
                admin_access_object.shutdownNode(node_name)

    def create_update_application(self, admin_access_object, application_name, application_options):
        application_names = admin_access_object.getAllApplicationNames()

        if application_name in application_names:
            update = True
        else:
            update = False

        # creates the ice application parser
        ice_application_parser = IceApplicationParser(application_options)

        # parses the application options
        ice_application_parser.parse()

        # retrieves the application descriptor
        application_descriptor = ice_application_parser.application_descriptor

        # in case the application should be updated
        if update:
            # syncs the application and sets it for update
            admin_access_object.syncApplication(application_descriptor)
        else:
            # adds the application to the registry
            admin_access_object.addApplication(application_descriptor)

    def get_application(self, admin_access_object, application_name):
        application_names = admin_access_object.getAllApplicationNames()

        # in case the application is not available
        if not application_name in application_names:
            return

        # retrieves the application information from the ice grid registry
        application_information = admin_access_object.getApplicationInfo(application_name)

        # retrieves the application descriptor from the application information
        application_descriptor = application_information.descriptor

        # creates the ice application descriptor parser
        ice_application_descriptor_parser = IceApplicationDescriptorParser(application_descriptor)

        # parses the application descriptor
        ice_application_descriptor_parser.parse()

        # retrieves the application options
        application_options = ice_application_descriptor_parser.application_options

        return application_options

    def create_communicator(self, locator_name, locator_endpoint = "default -p 12000"):
        locator_info = locator_name + "/Locator:" + locator_endpoint
        init_data = Ice.InitializationData()
        init_data.properties = Ice.createProperties()
        init_data.properties.setProperty("Ice.Default.Locator", locator_info)
        communicator = Ice.initialize(init_data)
        return communicator

    def close_communicator(self, communicator):
        communicator.destroy()

    def shutdown_communicator(self, communicator):
        communicator.shutdown()

    def create_access(self, communicator, access_class, access_name):
        access_object = access_class.checkedCast(communicator.stringToProxy(access_name))
        return access_object

    def create_access_access_type(self, communicator, locator_name, access_class, access_type):
        query_path = locator_name + "/Query"
        query_access_object = IceGrid.QueryPrx.checkedCast(communicator.stringToProxy(query_path))
        access_object = access_class.checkedCast(query_access_object.findObjectByType(access_type))
        return access_object

    def create_registry_access(self, communicator, locator_name):
        registry_path = locator_name + "/Registry"
        registry_access_object = IceGrid.RegistryPrx.checkedCast(communicator.stringToProxy(registry_path))
        return registry_access_object

    def create_admin_access(self, communicator, registry_access_object, username = "none", password = "none"):
        admin_session = registry_access_object.createAdminSession(username, password)
        admin_access_object = admin_session.getAdmin()
        return admin_access_object

    def create_admin_access_complete(self, locator_name, locator_endpoint = "default -p 12000", username = "none", password = "none"):
        communicator = self.create_communicator(locator_name, locator_endpoint)
        registry_access_object = self.create_registry_access(communicator, locator_name)
        admin_access_object = self.create_admin_access(communicator, registry_access_object, username, password)
        return admin_access_object

    def close_access(self, access_object):
        access_object.ice_getConnection().close(False)

    def close_access_communicator(self, access_object):
        access_object.ice_getConnection().close(False)
        access_communicator = access_object.ice_getCommunicator()
        self.close_communicator(access_communicator)

    def call_access(self, access_method, access_method_arguments):
        return access_method(*access_method_arguments)

    def get_default_application(self):
        default_nodes = self.get_default_nodes()
        default_server_templates = self.get_default_server_templates()
        default_replica_groups = self.get_default_replica_groups()

        default_application = {"name" : "default_application",
                               "description" : "description",
                               "nodes" : default_nodes,
                               "server_templates" : default_server_templates,
                               "replica_groups" : default_replica_groups}

        return default_application

    def get_default_nodes(self):
        default_node = self.get_default_node()
        default_nodes = [default_node]

        return default_nodes

    def get_default_node(self):
        default_node = {"name" : "node1",
                        "server_instances" : [{"template" : "default.template",
                                               "parameter_values" : [{"name" : "index", "value" : "1"}],
                                               "property_set" : {"properties" : [],
                                                                 "references" : []}}]}

        return default_node

    def get_default_server_templates(self):
        default_server_template = self.get_default_server_template()
        default_server_templates = [default_server_template]

        return default_server_templates

    def get_default_server_template(self):
        default_server_template_descriptor = self.get_default_server_template_descriptor()
        default_server_template = {"name" : "default.template",
                                   "parameters" : [{"value" : "index"}],
                                   "descriptor" : default_server_template_descriptor}

        return default_server_template

    def get_default_server_template_descriptor(self):
        default_server_template_descriptor = {"id" : "default.template.${index}",
                                              "execution_type" : "python",
                                              "activation" : "on-demand",
                                              "application_distribution" : True,
                                              "property_set" : {"properties" : [{"name" : "LogicAdapter.Endpoints",
                                                                                 "value" : "default"},
                                                                                {"name" : "Identity",
                                                                                 "value" : "logic_adapter"}]},
                                              "options" : [{"value" : "default.py"}],
                                              "adapters" : [{"name" : "LogicAdapter",
                                                             "id" : "${server}.LogicAdapter",
                                                             "replica_group_id" : "default.replica.group",
                                                             "register_process" : True,
                                                             "server_lifetime" : True}]}

        return default_server_template_descriptor

    def get_default_replica_groups(self):
        default_replica_group = self.get_default_replica_group()
        default_replica_groups = [default_replica_group]

        return default_replica_groups

    def get_default_replica_group(self):
        default_replica_group = {"id" : "default.replica.group",
                                 "load_balancing" : {"type" : "round_robin",
                                                     "number_replicas" : "1"},
                                 "objects" : [{"name" : "default_op_access",
                                               "category" : None,
                                               "type" : "::default::DefaultOp"}]}

        return default_replica_group

class IceGridRegistryDescriptor:

    ice_grid_instance_name = "none"
    ice_grid_registry_replica_names_list = []

    def __init__(self, ice_grid_instance_name = "none", ice_grid_registry_replica_names_list = []):
        self.ice_grid_instance_name = ice_grid_instance_name
        self.ice_grid_registry_replica_names_list = ice_grid_registry_replica_names_list

class IceGridNodeDescriptor:

    ice_grid_node_name = "none"
    ice_grid_instance_name = "none"

    def __init__(self, ice_grid_node_name = "none", ice_grid_instance_name = "none"):
        self.ice_grid_node_name = ice_grid_node_name
        self.ice_grid_instance_name = ice_grid_instance_name

class IceApplicationParser:

    application_options = None
    application_descriptor = None

    def __init__(self, application_options = None):
        self.application_options = application_options

    def parse(self):
        application_options = self.application_options

        application_descriptor = IceGrid.ApplicationDescriptor()
        application_descriptor.name = application_options["name"]
        application_descriptor.description = application_options["description"]
        application_descriptor.nodes = {}
        application_descriptor.serverTemplates = {}
        application_descriptor.replicaGroups = []

        application_nodes = application_options["nodes"]

        for node in application_nodes:
            node_descriptor = IceGrid.NodeDescriptor()
            node_descriptor.serverInstances = []

            node_server_instances = node["server_instances"]

            for server_instance in node_server_instances:
                server_instance_descriptor = IceGrid.ServerInstanceDescriptor()
                server_instance_descriptor.template = server_instance["template"]
                server_instance_descriptor.parameterValues = {}

                server_instance_parameter_values = server_instance["parameter_values"]

                for parameter_value in server_instance_parameter_values:
                    server_instance_descriptor.parameterValues[parameter_value["name"]] = parameter_value["value"]

                property_set_descriptor = IceGrid.PropertySetDescriptor()
                property_set_descriptor.properties = []
                property_set_descriptor.references = []

                server_instance_property_set = server_instance["property_set"]

                property_set_properties = server_instance_property_set["properties"]
                property_set_references = server_instance_property_set["references"]

                for property in property_set_properties:
                    property_descriptor = IceGrid.PropertyDescriptor()
                    property_descriptor.name = property["name"]
                    property_descriptor.value = property["value"]
                    property_set_descriptor.properties.append(property_descriptor)

                for reference in property_set_references:
                    property_set_descriptor.properties.append(reference)

                # sets the server instance descriptor property set
                server_instance_descriptor.propertySet = property_set_descriptor

                node_descriptor.serverInstances.append(server_instance_descriptor)

            application_descriptor.nodes[node["name"]] = node_descriptor

        application_server_templates = application_options["server_templates"]

        for server_template in application_server_templates:
            template_descriptor = IceGrid.TemplateDescriptor()
            template_descriptor.parameters = []
            template_descriptor.parameters = []

            server_template_parameters = server_template["parameters"]

            for parameter in server_template_parameters:
                template_descriptor.parameters.append(parameter["value"])

            server_template_descriptor = server_template["descriptor"]

            server_descriptor = IceGrid.ServerDescriptor()
            server_descriptor.id = server_template_descriptor["id"]
            server_descriptor.exe = server_template_descriptor["execution_type"]
            server_descriptor.activation = server_template_descriptor["activation"]
            server_descriptor.applicationDistrib = server_template_descriptor["application_distribution"]
            server_descriptor.options = []
            server_descriptor.adapters = []

            property_set_descriptor = IceGrid.PropertySetDescriptor()
            property_set_descriptor.properties = []

            server_descriptor_property_set = server_template_descriptor["property_set"]

            property_set_properties = server_descriptor_property_set["properties"]

            for property in property_set_properties:
                property_descriptor = IceGrid.PropertyDescriptor()
                property_descriptor.name = property["name"]
                property_descriptor.value = property["value"]
                property_set_descriptor.properties.append(property_descriptor)

            # sets the server descriptor property set
            server_descriptor.propertySet = property_set_descriptor

            server_descriptor_options = server_template_descriptor["options"]

            for option in server_descriptor_options:
                server_descriptor.options.append(option["value"])

            server_descriptor_adapters = server_template_descriptor["adapters"]

            for adapter in server_descriptor_adapters:
                adapter_descriptor = IceGrid.AdapterDescriptor()
                adapter_descriptor.name = adapter["name"]
                adapter_descriptor.id = adapter["id"]
                adapter_descriptor.replicaGroupId = adapter["replica_group_id"]
                adapter_descriptor.registerProcess = adapter["register_process"]
                adapter_descriptor.serverLifetime = adapter["server_lifetime"]

                server_descriptor.adapters.append(adapter_descriptor)

            template_descriptor.descriptor = server_descriptor

            application_descriptor.serverTemplates[server_template["name"]] = template_descriptor

        application_replica_groups = application_options["replica_groups"]

        for replica_group in application_replica_groups:
            replica_goup_descriptor = IceGrid.ReplicaGroupDescriptor()
            replica_goup_descriptor.id = replica_group["id"]
            replica_goup_descriptor.objects = []

            replica_group_load_balancing = replica_group["load_balancing"]

            if replica_group_load_balancing["type"] == "adaptive":
                load_blancing_policy = IceGrid.AdaptiveLoadBalancingPolicy()
            elif replica_group_load_balancing["type"] == "ordered":
                load_blancing_policy = IceGrid.OrderedLoadBalancingPolicy()
            elif replica_group_load_balancing["type"] == "random":
                load_blancing_policy = IceGrid.RandomLoadBalancingPolicy()
            elif replica_group_load_balancing["type"] == "round_robin":
                load_blancing_policy = IceGrid.RoundRobinLoadBalancingPolicy()

            load_blancing_policy.nReplicas = replica_group_load_balancing["number_replicas"]

            replica_goup_descriptor.loadBalancing = load_blancing_policy

            replica_group_objects = replica_group["objects"]

            for object in replica_group_objects:
                object_descriptor = IceGrid.ObjectDescriptor()
                object_descriptor.id = Ice.Identity()
                object_descriptor.id.name = object["name"]
                object_descriptor.id.category = None
                object_descriptor.type = object["type"]

                replica_goup_descriptor.objects.append(object_descriptor)

            application_descriptor.replicaGroups.append(replica_goup_descriptor)

        self.application_descriptor = application_descriptor

class IceApplicationDescriptorParser:

    application_descriptor = None
    application_options = None

    def __init__(self, application_descriptor = None):
        self.application_descriptor = application_descriptor

    def parse(self):
        application_descriptor = self.application_descriptor

        application_options = {}

        application_options["name"] = application_descriptor.name
        application_options["description"] = application_descriptor.description
        application_options["nodes"] = []
        application_options["server_templates"] = []
        application_options["replica_groups"] = []

        application_descriptor_nodes_map = application_descriptor.nodes

        for node_name in application_descriptor_nodes_map:
            node = application_descriptor_nodes_map[node_name]

            node_structure = {}

            node_structure["name"] = node_name
            node_structure["server_instances"] = []

            node_server_instances = node.serverInstances

            for server_instance in node_server_instances:
                server_instance_structure = {}
                server_instance_structure["template"] = server_instance.template
                server_instance_structure["parameter_values"] = []
                server_instance_structure["property_set"] = {}

                server_instance_parameter_values_map = server_instance.parameterValues

                for parameter_name in server_instance_parameter_values_map:
                    parameter_value = server_instance_parameter_values_map[parameter_name]

                    parameter_value_structure = {}

                    parameter_value_structure["name"] = parameter_name
                    parameter_value_structure["value"] = parameter_value

                    server_instance_structure["parameter_values"].append(parameter_value_structure)

                property_set_options_structure = []
                property_set_references_structure = []

                server_instance_property_set = server_instance.propertySet
                property_set_properties = server_instance_property_set.properties

                for property in property_set_properties:
                    property_structure = {}

                    property_structure["name"] = property.name
                    property_structure["value"] = property.value

                    property_set_options_structure.append(property_structure)

                property_set_references = server_instance_property_set.references

                for reference in property_set_references:
                    property_set_references_structure.append(reference)

                server_instance_structure["property_set"]["properties"] = property_set_options_structure
                server_instance_structure["property_set"]["references"] = property_set_references_structure

                node_structure["server_instances"].append(server_instance_structure)

            application_options["nodes"].append(node_structure)

        application_descriptor_server_templates_map = application_descriptor.serverTemplates

        for server_template_name in application_descriptor_server_templates_map:
            server_template = application_descriptor_server_templates_map[server_template_name]

            server_template_structure = {}

            server_template_structure["name"] = server_template_name
            server_template_structure["parameters"] = []

            server_template_parameters = server_template.parameters

            for parameter in server_template_parameters:
                parameter_structure = {}

                parameter_structure["value"] = parameter

                server_template_structure["parameters"].append(parameter_structure)

            server_template_descriptor_structure = {}

            server_template_descriptor = server_template.descriptor

            server_template_descriptor_structure["id"] = server_template_descriptor.id
            server_template_descriptor_structure["execution_type"] = server_template_descriptor.exe
            server_template_descriptor_structure["activation"] = server_template_descriptor.activation
            server_template_descriptor_structure["application_distribution"] = server_template_descriptor.applicationDistrib
            server_template_descriptor_structure["property_set"] = {}
            server_template_descriptor_structure["options"] = []
            server_template_descriptor_structure["adapters"] = []

            property_set_options_structure = []
            property_set_references_structure = []

            server_template_descriptor_property_set = server_template_descriptor.propertySet
            property_set_properties = server_template_descriptor_property_set.properties

            for property in property_set_properties:
                property_structure = {}

                property_structure["name"] = property.name
                property_structure["value"] = property.value

                property_set_options_structure.append(property_structure)

            property_set_references = server_template_descriptor_property_set.references

            for reference in property_set_references:
                property_set_references_structure.append(reference)

            server_template_descriptor_structure["property_set"]["properties"] = property_set_options_structure
            server_template_descriptor_structure["property_set"]["references"] = property_set_references_structure

            server_template_descriptor_options = server_template_descriptor.options

            for option in server_template_descriptor_options:
                option_structure = {}

                option_structure["value"] = option

                server_template_descriptor_structure["options"].append(option_structure)

            server_template_descriptor_adapters = server_template_descriptor.adapters

            for adapter in server_template_descriptor_adapters:
                adapter_structure = {}

                adapter_structure["name"] = adapter.name
                adapter_structure["id"] = adapter.id
                adapter_structure["replica_group_id"] = adapter.replicaGroupId
                adapter_structure["register_process"] = adapter.registerProcess
                adapter_structure["server_lifetime"] = adapter.serverLifetime

                server_template_descriptor_structure["adapters"].append(adapter_structure)

            server_template_structure["descriptor"] = server_template_descriptor_structure

            application_options["server_templates"].append(server_template_structure)

        application_descriptor_replica_groups = application_descriptor.replicaGroups

        for replica_group in application_descriptor_replica_groups:
            replica_group_structure = {}

            replica_group_structure["id"] = replica_group.id
            replica_group_structure["objects"] = []

            replica_group_load_balancing_structure = {}

            replica_group_load_balancing = replica_group.loadBalancing
            replica_group_load_balancing_type = replica_group_load_balancing.__class__.__name__

            if replica_group_load_balancing_type == "AdaptiveLoadBalancingPolicy":
                replica_group_load_balancing_structure["type"] = "adaptive"
            elif replica_group_load_balancing_type == "OrderedLoadBalancingPolicy":
                replica_group_load_balancing_structure["type"] = "ordered"
            elif replica_group_load_balancing_type == "RandomLoadBalancingPolicy":
                replica_group_load_balancing_structure["type"] = "random"
            elif replica_group_load_balancing_type == "RoundRobinLoadBalancingPolicy":
                replica_group_load_balancing_structure["type"] = "round_robin"

            replica_group_load_balancing_structure["number_replicas"] = replica_group_load_balancing.nReplicas

            replica_group_structure["load_balancing"] = replica_group_load_balancing_structure

            replica_group_objects = replica_group.objects

            for object in replica_group_objects:
                object_structure = {}

                object_structure["name"] = object.id.name
                object_structure["category"] = object.id.category
                object_structure["type"] = object.type

                replica_group_structure["objects"].append(object_structure)

            application_options["replica_groups"].append(replica_group_structure)

        self.application_options = application_options
