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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import colony.plugins.plugin_system
import colony.plugins.decorators

class MainServiceHttpTemplateErrorHandlerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Http Service Main Template Error Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.http.template_error_handler"
    name = "Http Service Main Template Error Handler Plugin"
    short_name = "Http Service Main Template Error Handler"
    description = "The plugin that offers the http service template error handler"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.IRON_PYTHON_ENVIRONMENT]
    capabilities = ["http_service_error_handler"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.template_engine.manager", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["main_service_http_template_error_handler.template_error_handler.main_service_http_template_error_handler_system"]

    main_service_http_template_error_handler = None

    template_engine_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_service_http_template_error_handler
        import main_service_http_template_error_handler.template_error_handler.main_service_http_template_error_handler_system
        self.main_service_http_template_error_handler = main_service_http_template_error_handler.template_error_handler.main_service_http_template_error_handler_system.MainServiceHttpTemplateErrorHandler(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.main.service.http.template_error_handler", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_error_handler_name(self):
        return self.main_service_http_template_error_handler.get_error_handler_name()

    def handle_error(self, request, error):
        return self.main_service_http_template_error_handler.handle_error(request, error)

    def get_template_engine_manager_plugin(self):
        return self.template_engine_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.template_engine.manager")
    def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
        self.template_engine_manager_plugin = template_engine_manager_plugin
