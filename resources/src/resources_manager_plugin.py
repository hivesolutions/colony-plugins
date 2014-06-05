#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class ResourcesManagerPlugin(colony.Plugin):
    """
    The main class for the Resources Manager plugin.
    """

    id = "pt.hive.colony.plugins.resources.manager"
    name = "Resources Manager"
    description = "A plugin to manage the resources contained in the plugins"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "startup",
        "resources_manager",
        "test_case",
        "system_information"
    ]
    capabilities_allowed = [
        "resources_parser"
    ]
    events_handled = [
        "plugin_manager.plugin.end_load_plugin",
        "plugin_manager.plugin.unload_plugin"
    ]
    main_modules = [
        "resources_manager.exceptions",
        "resources_manager.parser",
        "resources_manager.system",
        "resources_manager.tests"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import resources_manager
        self.system = resources_manager.ResourcesManager(self)
        self.test = resources_manager.ResourcesManagerTestCase
        self.system.load_system()

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload_system()

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    @colony.event_handler
    def event_handler(self, event_name, *event_args):
        colony.Plugin.event_handler(self, event_name, *event_args)

    def parse_file(self, file_path, full_resources_path):
        """
        Parses the file in the given file path, using the full
        resources path as the base for the parsing.
        The parsing of the file also implies the registering
        of the resources in the internal data structures.

        @type file_path: String
        @param file_path: The path to the file to be parsed.
        @type full_resources_path: String
        @param full_resources_path: The full path to the
        resources path (directory).
        """

        return self.system.parse_file(file_path, full_resources_path)

    def register_resources(self, resources_list, file_path, full_resources_path):
        return self.system.register_resources(resources_list, file_path, full_resources_path)

    def unregister_resources(self, resources_list, file_path, full_resources_path):
        return self.system.unregister_resources(resources_list, file_path, full_resources_path)

    def register_resource(self, resource_namespace, resource_name, resource_type, resource_data):
        return self.system.register_resource(resource_namespace, resource_name, resource_type, resource_data)

    def unregister_resource(self, resource_id):
        return self.system.unregister_resource(resource_id)

    def is_resource_registered(self, resource_id):
        return self.system.is_resource_registered(resource_id)

    def is_resource_name(self, resource_name):
        return self.system.is_resource_name(resource_name)

    def get_resource(self, resource_id):
        return self.system.get_resource(resource_id)

    def get_resources(self, resource_namespace = None, resource_name = None, resource_type = None):
        return self.system.get_resources(resource_namespace, resource_name, resource_type)

    def load_resource_file(self, file_path):
        return self.system.load_resource_file(file_path)

    def get_real_string_value(self, string_value):
        return self.system.get_real_string_value(string_value)

    def get_base_resources_path(self):
        return self.system.get_base_resources_path()

    def get_file_path_resources_list_map(self):
        return self.system.file_path_resources_list_map

    def get_file_path_file_information_map(self):
        return self.system.file_path_file_information_map

    def get_test_case(self):
        return self.test

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        @rtype: Dictionary
        @return: The system information map.
        """

        return self.system.get_system_information()

    @colony.load_allowed_capability("resources_parser")
    def resources_parser_load_allowed(self, plugin, capability):
        self.system.load_resources_parser_plugin(plugin)

    @colony.unload_allowed_capability("resources_parser")
    def resources_parser_unload_allowed(self, plugin, capability):
        self.system.unload_resources_parser_plugin(plugin)

    @colony.event_handler_method("plugin_manager.plugin.end_load_plugin")
    def end_load_plugin_handler(self, event_name, plugin_id, plugin_version, plugin, *event_args):
        self.system.register_plugin_resources(plugin)

    @colony.event_handler_method("plugin_manager.plugin.unload_plugin")
    def unload_plugin_handler(self, event_name, plugin_id, plugin_version, plugin, *event_args):
        self.system.unregister_plugin_resources(plugin)
