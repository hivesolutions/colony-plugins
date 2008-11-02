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

import string
import getopt

import colony.plugins.util

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
HELP_TEXT = "### ICE HELPER HELP ###\n\
loadice <file-path>                                                   - starts the loading of the file\n\
createregistry <registry-name> [registry-replica-name] [properties..] - creates a new ice grid registry with the given name, replica name and properties\n\
killregistry <registry-name> [registry-replica-name]                  - kills the registry with the given name and replica name\n\
createnode <registry-name> <node-name> [properties..]                 - creates a new ice grid node in the registry with the given name and with the given name and properties\n\
killnode <registry-name> <node-name>                                  - kills the node in the registry with the given name with the given name\n\
createupdateapplication <application-name>                            - creates or updates an application with the given name\n\
createcommunicator <locator-name> [locator-endpoint]                  - creates a communicator with the given name and endpoint\n\
createaccess <access-class-name> <access-name>                        - creates an access object for the given class and access name\n\
createaccesstype <access-class-name> <access-type>                    - creates an access object for the given class and access type\n\
createregistryaccess                                                  - creates a registry access object to control the ice grid\n\
createadminaccess <username> <password>                               - creates an admin access object to administrate the ice grid\n\
callaccess <method-name> [arguments..]                                - calls a method with the given name with the given arguments\n\
showapplicationinfo <application-name>                                - shows information about the the application with the given name"

ICE_REGISTRY_PARSING_VALUES = ["ice_grid_registry_path=", "ice_grid_instance_name=", "ice_grid_default_locator=",
                               "ice_grid_registry_client_endpoints=", "ice_grid_registry_server_endpoints=",
                               "ice_grid_registry_internal_endpoints=", "ice_grid_registry_data=", "ice_grid_registry_replica_name=",
                               "ice_grid_registry_permissions_verifier=", "ice_grid_registry_admin_permissions_verifier=",
                               "ice_grid_registry_ssl_permissions_verifier=", "ice_grid_registry_admin_ssl_permissions_verifier=",
                               "ice_grid_admin_username=", "ice_grid_admin_password=", "ice_grid_registry_log_file=", "ice_grid_registry_log_file_mode="]

ICE_NODE_PARSING_VALUES = ["ice_grid_node_path=", "ice_grid_instance_name=", "ice_default_locator=", "ice_grid_node_data=",
                           "ice_grid_node_endpoints=", "ice_grid_node_name=", "ice_grid_node_trace_activator=",
                           "ice_grid_node_trace_patch=", "ice_grid_node_log_file=", "ice_grid_node_log_file_mode="]

class ConsoleIceHelper:

    commands = ["loadice", "createregistry", "killregistry", "createnode", "killnode", "createupdateapplication", "createcommunicator", "createaccess", "createaccesstype", "createregistryaccess", "createadminaccess", "callaccess", "showapplicationinfo"]

    ice_helper_plugin = None

    communicator = None
    locator_name = None

    def __init__(self, ice_helper_plugin = None):
        self.ice_helper_plugin = ice_helper_plugin

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_loadice(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        file_path = args[0]

        output_method("starting ice load of " + file_path)

        self.ice_helper_plugin.ice_helper.load_ice_file(file_path)

    def process_createregistry(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        registry_name = args[0]
        if len(args) > 1:
            registry_replica_name = args[1]
        else:
            registry_replica_name = "Master"

        output_method("creating new ice grid registry " + registry_name)

        registry_data = "db/registry/" + registry_name + "/" + registry_replica_name

        registry_permissions_verifier = registry_name + "/NullPermissionsVerifier"
        registry_admin_permissions_verifier = registry_name + "/NullPermissionsVerifier"
        registry_ssl_permissions_verifier = registry_name + "/NullSSLPermissionsVerifier"
        registry_admin_ssl_permissions_verifier = registry_name + "/NullSSLPermissionsVerifier"

        registry_log_file = "logs/" + registry_name + "/" + registry_replica_name + "/ice_grid_log.log"

        start_options = {"ice_grid_instance_name" : registry_name,
                         "ice_grid_registry_data" : registry_data,
                         "ice_grid_registry_replica_name" : registry_replica_name,
                         "ice_grid_registry_permissions_verifier" : registry_permissions_verifier,
                         "ice_grid_registry_admin_permissions_verifier" : registry_admin_permissions_verifier,
                         "ice_grid_registry_ssl_permissions_verifier" : registry_ssl_permissions_verifier,
                         "ice_grid_registry_admin_ssl_permissions_verifier" : registry_admin_ssl_permissions_verifier,
                         "ice_grid_registry_log_file" : registry_log_file}

        if len(args) > 2:
            ice_properties = args[2:]
            ice_option_parser = IceOptionParser(ICE_REGISTRY_PARSING_VALUES)
            ice_option_parser.parse(ice_properties, start_options)

        self.ice_helper_plugin.ice_helper.create_registry(start_options)

    def process_killregistry(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        registry_name = args[0]
        if len(args) > 1:
            registry_replica_name = args[1]
        else:
            registry_replica_name = "Master"

        output_method("killing ice grid registry " + registry_name)

        self.ice_helper_plugin.ice_helper.kill_registry(self.access, registry_name)

    def process_createnode(self, args, output_method):
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        registry_name = args[0]
        node_name = args[1]

        output_method("creating new ice grid node " + node_name)

        default_locator = registry_name + "/Locator:default -p 12000"
        node_data = "db/node/" + registry_name + "/" + node_name

        node_log_file = "logs/" + registry_name + "/" + node_name + "/ice_node_log.log"

        start_options = {"ice_grid_instance_name" : registry_name,
                         "ice_default_locator" : default_locator,
                         "ice_grid_node_data" : node_data,
                         "ice_grid_node_name" : node_name,
                         "ice_grid_node_log_file" : node_log_file}

        if len(args) > 2:
            ice_properties = args[2:]
            ice_option_parser = IceOptionParser(ICE_NODE_PARSING_VALUES)
            ice_option_parser.parse(ice_properties, start_options)

        self.ice_helper_plugin.ice_helper.create_node(start_options)

    def process_killnode(self, args, output_method):
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        registry_name = args[0]
        node_name = args[1]

        output_method("killing ice grid node " + node_name)

        self.ice_helper_plugin.ice_helper.kill_node(self.access, registry_name, node_name)

    def process_createupdateapplication(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        application_name = args[0]

        output_method("creating or updating application " + application_name)

        application_options = self.ice_helper_plugin.ice_helper.get_default_application()
        application_options["name"] = application_name

        self.ice_helper_plugin.ice_helper.create_update_application(self.access, application_name, application_options)

    def process_createcommunicator(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        locator_name = args[0]
        if len(args) > 1:
            locator_endpoint = args[1]
        else:
            locator_endpoint = "default -p 12000"

        output_method("creating new communicator " + locator_name)

        self.communicator = self.ice_helper_plugin.ice_helper.create_communicator(locator_name, locator_endpoint)
        self.locator_name = locator_name

    def process_createaccess(self, args, output_method):
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        access_complete_class_name = args[0]
        access_name = args[1]

        # splits the complete class name using the "." character
        split_result = access_complete_class_name.split(".")

        # retrieves the module name 
        access_module_name = string.join(split_result[:-1], ".")
        # retrieves just the class name
        access_class_name = split_result[-1]

        # imports the access module
        access_module = colony.plugins.util.module_import(access_module_name)

        # retrieves the access class
        access_class = getattr(access_module, access_class_name)

        output_method("creating new access object " + access_name)

        self.access = self.ice_helper_plugin.ice_helper.create_access(self.communicator, access_class, access_name)

    def process_createaccesstype(self, args, output_method):
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        access_complete_class_name = args[0]
        access_type = args[1]

        # splits the complete class name using the "." character
        split_result = access_complete_class_name.split(".")

        # retrieves the module name 
        access_module_name = string.join(split_result[:-1], ".")
        # retrieves just the class name
        access_class_name = split_result[-1]

        # imports the access module
        access_module = colony.plugins.util.module_import(access_module_name)

        # retrieves the access class
        access_class = getattr(access_module, access_class_name)

        output_method("creating new access object of type " + access_type)

        self.access = self.ice_helper_plugin.ice_helper.create_access_access_type(self.communicator, self.locator_name, access_class, access_type)

    def process_createregistryaccess(self, args, output_method):
        output_method("creating new registry object")

        self.access = self.ice_helper_plugin.ice_helper.create_registry_access(self.communicator, self.locator_name)

    def process_createadminaccess(self, args, output_method):
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        username = args[0]
        password = args[1]

        output_method("creating new admin object")

        self.access = self.ice_helper_plugin.ice_helper.create_admin_access(self.communicator, self.access, username, password)

    def process_callaccess(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        access_method_name = args[0]
        access_method_arguments = args[1:]

        access_method = getattr(self.access, access_method_name)

        output_method("calling access method " + access_method_name)

        self.ice_helper_plugin.ice_helper.call_access(access_method, access_method_arguments)

    def process_showapplicationinfo(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        application_name = args[0]

        application_options = self.ice_helper_plugin.ice_helper.get_application(self.access, application_name)
        output_method(str(application_options))

class IceOptionParser:

    values = []

    def __init__(self, values = []):
        self.values = values

    def parse(self, properties, options):
        opts, args = getopt.getopt(properties, ":", self.values)

        for option, value in opts:
            treated_option = option[2:] 
            options[treated_option] = value
