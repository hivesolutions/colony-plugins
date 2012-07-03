#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainServiceHttpTemplateDirectoryListHandlerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Http Service Main Template Directory List Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.http.template_directory_list_handler"
    name = "Http Service Main Template Directory List Handler Plugin"
    short_name = "Http Service Main Template Directory List Handler"
    description = "The plugin that offers the http service template directory list handler"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_service_http_template_directory_list_handler/template_directory_list_handler/resources/baf.xml"
    }
    capabilities = [
        "http_service_directory_list_handler",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.template_engine.manager", "1.x.x")
    ]
    main_modules = [
        "main_service_http_template_directory_list_handler.template_directory_list_handler.main_service_http_template_directory_list_handler_system"
    ]

    main_service_http_template_directory_list_handler = None
    """ The main service http template directory list handler """

    template_engine_manager_plugin = None
    """ The template engine manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_service_http_template_directory_list_handler.template_directory_list_handler.main_service_http_template_directory_list_handler_system
        self.main_service_http_template_directory_list_handler = main_service_http_template_directory_list_handler.template_directory_list_handler.main_service_http_template_directory_list_handler_system.MainServiceHttpTemplateDirectoryListHandler(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_directory_list_handler_name(self):
        return self.main_service_http_template_directory_list_handler.get_directory_list_handler_name()

    def handle_directory_list(self, request, directory_list):
        return self.main_service_http_template_directory_list_handler.handle_directory_list(request, directory_list)

    def get_template_engine_manager_plugin(self):
        return self.template_engine_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.template_engine.manager")
    def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
        self.template_engine_manager_plugin = template_engine_manager_plugin
