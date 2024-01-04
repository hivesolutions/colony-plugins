#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class MVCPlugin(colony.Plugin):
    """
    The main class for the MVC plugin.
    """

    id = "pt.hive.colony.plugins.mvc"
    name = "MVC"
    description = "The plugin that offers a strategy abstraction for MVC management"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "mvc",
        "rest_service"
    ]
    capabilities_allowed = [
        "mvc_service"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.format.mime"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.random"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.csv"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.json")
    ]
    events_handled = [
        "mvc.patterns_reload",
        "mvc.patterns_load",
        "mvc.patterns_unload",
        "mvc.communication"
    ]
    main_modules = [
        "mvc"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import mvc
        self.system = mvc.MVC(self)

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.system.start_system()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.stop_system()

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    @colony.event_handler
    def event_handler(self, event_name, *event_args):
        colony.Plugin.event_handler(self, event_name, *event_args)

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the REST service.

        :rtype: List
        :return: The list of regular expressions to be used as route,
        to the REST service.
        """

        return self.system.get_routes()

    def handle_rest_request(self, rest_request):
        """
        Handles the given REST request.

        :type rest_request: RESTRequest
        :param rest_request: The REST request to be handled.
        :rtype: bool
        :return: The result of the handling.
        """

        return self.system.handle_rest_request(rest_request)

    @colony.load_allowed_capability("mvc_service")
    def mvc_service_extension_load_allowed(self, plugin, capability):
        self.system.load_mvc_service_plugin(plugin)

    @colony.unload_allowed_capability("mvc_service")
    def mvc_service_extension_unload_allowed(self, plugin, capability):
        self.system.unload_mvc_service_plugin(plugin)

    @colony.event_handler_method("mvc.patterns_reload")
    def mvc_patterns_reload_handler(self, event_name, *event_args):
        self.system.process_mvc_patterns_reload_event(event_name, *event_args)

    @colony.event_handler_method("mvc.patterns_load")
    def mvc_patterns_load_handler(self, event_name, *event_args):
        self.system.process_mvc_patterns_load_event(event_name, *event_args)

    @colony.event_handler_method("mvc.patterns_unload")
    def mvc_patterns_unload_handler(self, event_name, *event_args):
        self.system.process_mvc_patterns_unload_event(event_name, *event_args)

    @colony.event_handler_method("mvc.communication")
    def mvc_communication_handler(self, event_name, *event_args):
        self.system.process_mvc_communication_event(event_name, *event_args)
