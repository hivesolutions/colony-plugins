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
import colony.plugins.decorators

class JavascriptFileHandlerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Javascript File Handler plugin
    """

    id = "pt.hive.colony.plugins.javascript.file_handler"
    name = "Javascript File Handler Plugin"
    short_name = "Javascript File Handler"
    description = "Javascript File Handler Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT]
    capabilities = ["javascript_file_handler", "http_python_handler"]
    capabilities_allowed = ["javascript_handler"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.javascript.manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    javascript_file_handler = None

    javascript_handler_plugins = []

    javascript_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global javascript_file_handler
        import javascript_file_handler.file_handler.javascript_file_handler_system
        self.javascript_file_handler = javascript_file_handler.file_handler.javascript_file_handler_system.JavascriptFileHandler(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.javascript.file_handler", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.javascript.file_handler", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.javascript.file_handler", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_handler_filename(self):
        return self.javascript_file_handler.get_handler_filename()

    def is_request_handler(self, request):
        return self.javascript_file_handler.is_request_handler(request)

    def handle_request(self, request):
        return self.javascript_file_handler.handle_request(request)

    @colony.plugins.decorators.load_allowed_capability("javascript_handler")
    def javascript_handler_load_allowed(self, plugin, capability):
        self.javascript_handler_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("javascript_handler")
    def javascript_handler_unload_allowed(self, plugin, capability):
        self.javascript_handler_plugins.remove(plugin)

    def get_javascript_manager_plugin(self):
        return self.javascript_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.javascript.manager")
    def set_javascript_manager_plugin(self, javascript_manager_plugin):
        self.javascript_manager_plugin = javascript_manager_plugin
