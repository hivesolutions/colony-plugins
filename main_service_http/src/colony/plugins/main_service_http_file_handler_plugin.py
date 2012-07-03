#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainServiceHttpFileHandlerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Http Service Main File Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.http.file_handler"
    name = "Http Service Main File Handler Plugin"
    short_name = "Http Service Main File Handler"
    description = "The plugin that offers the http service file handler"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_service_http_file_handler/file_handler/resources/baf.xml"
    }
    capabilities = [
        "http_service_handler",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "http_service_directory_list_handler"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.format.mime", "1.x.x"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.resources.resource_manager", "1.x.x")
    ]
    main_modules = [
        "main_service_http_file_handler.file_handler.main_service_http_file_handler_exceptions",
        "main_service_http_file_handler.file_handler.main_service_http_file_handler_system"
    ]

    main_service_http_file_handler = None
    """ The main service http file handler """

    http_service_directory_list_handler_plugins = []
    """ The http service directory list handler plugins """

    format_mime_plugin = None
    """ The format mime plugin """

    resource_manager_plugin = None
    """ The resource manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_service_http_file_handler.file_handler.main_service_http_file_handler_system
        self.main_service_http_file_handler = main_service_http_file_handler.file_handler.main_service_http_file_handler_system.MainServiceHttpFileHandler(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_service_http_file_handler.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        return self.main_service_http_file_handler.handle_request(request)

    @colony.base.decorators.load_allowed_capability("http_service_directory_list_handler")
    def http_service_directory_list_handler_load_allowed(self, plugin, capability):
        self.http_service_directory_list_handler_plugins.append(plugin)
        self.main_service_http_file_handler.http_service_directory_list_handler_load(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_directory_list_handler")
    def http_service_directory_list_handler_unload_allowed(self, plugin, capability):
        self.http_service_directory_list_handler_plugins.remove(plugin)
        self.main_service_http_file_handler.http_service_directory_list_handler_unload(plugin)

    def get_format_mime_plugin(self):
        return self.format_mime_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime")
    def set_format_mime_plugin(self, format_mime_plugin):
        self.format_mime_plugin = format_mime_plugin

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    @colony.base.decorators.set_configuration_property_method("handler_configuration")
    def handler_configuration_set_configuration_property(self, property_name, property):
        self.main_service_http_file_handler.set_handler_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("handler_configuration")
    def handler_configuration_unset_configuration_property(self, property_name):
        self.main_service_http_file_handler.unset_handler_configuration_property()
