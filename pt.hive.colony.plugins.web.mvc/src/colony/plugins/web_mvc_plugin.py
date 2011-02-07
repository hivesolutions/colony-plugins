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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class WebMvcPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Web Mvc plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc"
    name = "Web Mvc Plugin"
    short_name = "Web Mvc"
    description = "The plugin that offers a web strategy abstraction for mvc management"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/web_mvc/mvc/resources/baf.xml"}
    capabilities = ["web.mvc", "rest_service", "build_automation_item"]
    capabilities_allowed = ["web.mvc_service"]
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.format.mime", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.random", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.json", "1.0.0")]
    events_handled = []
    events_registrable = ["web.mvc.patterns_reload", "web.mvc.patterns_load", "web.mvc.patterns_unload", "web.mvc.communication"]
    main_modules = ["web_mvc.mvc.web_mvc_communication_handler",
                    "web_mvc.mvc.web_mvc_exceptions",
                    "web_mvc.mvc.web_mvc_file_handler",
                    "web_mvc.mvc.web_mvc_system"]

    web_mvc = None

    web_mvc_service_plugins = []

    format_mime_plugin = None
    random_plugin = None
    json_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global web_mvc
        import web_mvc.mvc.web_mvc_system
        self.web_mvc = web_mvc.mvc.web_mvc_system.WebMvc(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.web.mvc", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.web.mvc", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.web.mvc", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.event_handler("pt.hive.colony.plugins.web.mvc", "1.0.0")
    def event_handler(self, event_name, *event_args):
        colony.base.plugin_system.Plugin.event_handler(self, event_name, *event_args)

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the rest service.

        @rtype: List
        @return: The list of regular expressions to be used as route,
        to the rest service.
        """

        return self.web_mvc.get_routes()

    def handle_rest_request(self, rest_request):
        """
        Handles the given rest request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        return self.web_mvc.handle_rest_request(rest_request)

    @colony.base.decorators.load_allowed_capability("web.mvc_service")
    def web_mvc_service_extension_load_allowed(self, plugin, capability):
        self.web_mvc_service_plugins.append(plugin)
        self.web_mvc.load_web_mvc_service_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("web.mvc_service")
    def web_mvc_service_extension_unload_allowed(self, plugin, capability):
        self.web_mvc_service_plugins.remove(plugin)
        self.web_mvc.unload_web_mvc_service_plugin(plugin)

    def get_format_mime_plugin(self):
        return self.format_mime_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime")
    def set_format_mime_plugin(self, format_mime_plugin):
        self.format_mime_plugin = format_mime_plugin

    def get_random_plugin(self):
        return self.random_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.random")
    def set_random_plugin(self, random_plugin):
        self.random_plugin = random_plugin

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin

    @colony.base.decorators.event_handler_method("web.mvc.patterns_reload")
    def web_mvc_patterns_reload_handler(self, event_name, *event_args):
        self.web_mvc.process_web_mvc_patterns_reload_event(event_name, *event_args)

    @colony.base.decorators.event_handler_method("web.mvc.patterns_load")
    def web_mvc_patterns_load_handler(self, event_name, *event_args):
        self.web_mvc.process_web_mvc_patterns_load_event(event_name, *event_args)

    @colony.base.decorators.event_handler_method("web.mvc.patterns_unload")
    def web_mvc_patterns_unload_handler(self, event_name, *event_args):
        self.web_mvc.process_web_mvc_patterns_unload_event(event_name, *event_args)

    @colony.base.decorators.event_handler_method("web.mvc.communication")
    def web_mvc_communication_handler(self, event_name, *event_args):
        self.web_mvc.process_web_mvc_communication_event(event_name, *event_args)
