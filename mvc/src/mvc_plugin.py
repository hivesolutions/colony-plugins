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

import colony.base.system

class MvcPlugin(colony.base.system.Plugin):
    """
    The main class for the Mvc plugin.
    """

    id = "pt.hive.colony.plugins.mvc"
    name = "Mvc"
    description = "The plugin that offers a strategy abstraction for mvc management"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "mvc",
        "rest_service"
    ]
    capabilities_allowed = [
        "mvc_service"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.format.mime", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.random", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.x.x")
    ]
    events_handled = [
        "mvc.patterns_reload",
        "mvc.patterns_load",
        "mvc.patterns_unload",
        "mvc.communication"
    ]
    main_modules = [
        "mvc.mvc.communication_handler",
        "mvc.mvc.exceptions",
        "mvc.mvc.file_handler",
        "mvc.mvc.system"
    ]

    mvc = None
    """ The mvc object reference to the entry point
    of execution for the plugin calls """

    mvc_service_plugins = []
    """ The mvc service plugins """

    mime_plugin = None
    """ The mime plugin """

    random_plugin = None
    """ The random plugin """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import mvc.mvc.system
        self.mvc = mvc.mvc.system.Mvc(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)
        self.mvc.start_system()

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)
        self.mvc.stop_system()

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.event_handler
    def event_handler(self, event_name, *event_args):
        colony.base.system.Plugin.event_handler(self, event_name, *event_args)

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the rest service.

        @rtype: List
        @return: The list of regular expressions to be used as route,
        to the rest service.
        """

        return self.mvc.get_routes()

    def handle_rest_request(self, rest_request):
        """
        Handles the given rest request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        return self.mvc.handle_rest_request(rest_request)

    @colony.base.decorators.load_allowed_capability("mvc_service")
    def mvc_service_extension_load_allowed(self, plugin, capability):
        self.mvc_service_plugins.append(plugin)
        self.mvc.load_mvc_service_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("mvc_service")
    def mvc_service_extension_unload_allowed(self, plugin, capability):
        self.mvc_service_plugins.remove(plugin)
        self.mvc.unload_mvc_service_plugin(plugin)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime")
    def set_mime_plugin(self, mime_plugin):
        self.mime_plugin = mime_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.random")
    def set_random_plugin(self, random_plugin):
        self.random_plugin = random_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin

    @colony.base.decorators.event_handler_method("mvc.patterns_reload")
    def mvc_patterns_reload_handler(self, event_name, *event_args):
        self.mvc.process_mvc_patterns_reload_event(event_name, *event_args)

    @colony.base.decorators.event_handler_method("mvc.patterns_load")
    def mvc_patterns_load_handler(self, event_name, *event_args):
        self.mvc.process_mvc_patterns_load_event(event_name, *event_args)

    @colony.base.decorators.event_handler_method("mvc.patterns_unload")
    def mvc_patterns_unload_handler(self, event_name, *event_args):
        self.mvc.process_mvc_patterns_unload_event(event_name, *event_args)

    @colony.base.decorators.event_handler_method("mvc.communication")
    def mvc_communication_handler(self, event_name, *event_args):
        self.mvc.process_mvc_communication_event(event_name, *event_args)
