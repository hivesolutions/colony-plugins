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

import colony.plugins.plugin_system

class IceHelperPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Ice Helper plugin
    """

    id = "pt.hive.colony.plugins.misc.ice_helper"
    name = "Ice Helper Plugin"
    short_name = "Ice Helper"
    description = "Ice Helper Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["ice_helper", "console_command_extension"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "ZeroC Ice", "Ice", "3.x.x", "http://www.zeroc.com")]
    events_handled = []
    events_registrable = []

    ice_helper = None
    console_ice_helper = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.ice_helper.ice_helping_system
        import misc.ice_helper.console_ice_helper
        self.ice_helper = misc.ice_helper.ice_helping_system.IceHelper(self)
        self.console_ice_helper = misc.ice_helper.console_ice_helper.ConsoleIceHelper(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.ice_helper.unload()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_ice_file(self, file_path):
        self.ice_helper.load_ice_file(file_path)

    def create_registry(self, start_options):
        self.ice_helper.create_registry(start_options)

    def kill_registry(self, registry_name):
        self.ice_helper.kill_registry(registry_name)

    def create_node(self, start_options):
        self.ice_helper.create_node(start_options)

    def kill_node(self, admin_object, node_name):
        self.ice_helper.kill_node(admin_object, node_name)

    def create_update_application(self, admin_access_object, application_name, application_options):
        self.ice_helper.create_update_application(admin_access_object, application_name, application_options)

    def get_application(self, admin_access_object, application_name):
        return self.ice_helper.get_application(admin_access_object, application_name)

    def create_communicator(self, locator_name, locator_endpoint):
        return self.ice_helper.create_communicator(locator_name, locator_endpoint)

    def close_communicator(self, communicator):
        self.ice_helper.close_communicator(communicator)

    def shutdown_communicator(self, communicator):
        self.ice_helper.shutdown_communicator(communicator)

    def create_access(self, communicator, access_class, access_name):
        return self.ice_helper.create_access(communicator, access_class, access_name)

    def create_access_access_type(self, communicator, locator_name, access_class, access_type):
        return self.ice_helper.create_access_type_name(communicator, locator_name, access_class, access_type)

    def create_registry_access(self, communicator, locator_name):
        return self.ice_helper.create_registry_access(communicator, locator_name)

    def create_admin_access(self, communicator, registry_access_object, username, password):
        return self.ice_helper.create_admin_access(communicator, registry_access_object, username, password)

    def create_admin_access_complete(self, locator_name, locator_endpoint, username, password):
        return self.ice_helper.create_admin_access_complete(locator_name, locator_endpoint, username, password)

    def close_access(self, access_object):
        self.ice_helper.close_access(access_object)

    def close_access_communicator(self, access_object):
        self.ice_helper.close_access_communicator(access_object)

    def call_access(self, access_method, access_method_arguments):
        return self.ice_helper.call_access(access_method, access_method_arguments)

    def get_default_application(self):
        return self.ice_helper.get_default_application()

    def get_default_nodes(self):
        return self.ice_helper.get_default_nodes()

    def get_default_node(self):
        return self.ice_helper.get_default_node()

    def get_default_server_templates(self):
        return self.ice_helper.get_default_server_templates() 

    def get_default_server_template(self):
        return self.ice_helper.get_default_server_template()

    def get_default_server_template_descriptor(self):
        return self.ice_helper.get_default_server_template_descriptor()

    def get_default_replica_groups(self):
        return self.ice_helper.get_default_replica_groups()

    def get_default_replica_group(self):
        return self.ice_helper.get_default_replica_group()

    def get_all_commands(self):
        return self.console_ice_helper.get_all_commands()

    def get_handler_command(self, command):
        return self.console_ice_helper.get_handler_command(command)

    def get_help(self):
        return self.console_ice_helper.get_help()
