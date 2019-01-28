#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class RestPlugin(colony.Plugin):
    """
    The main class for the Rest plugin.
    """

    id = "pt.hive.colony.plugins.rest"
    name = "Rest"
    description = "Rest Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "rest",
        "http_handler",
        "rpc_handler"
    ]
    capabilities_allowed = [
        "rest_encoder",
        "rest_service",
        "rpc_service"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.resources.manager"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.random")
    ]
    main_modules = [
        "rest"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import rest
        self.system = rest.Rest(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def is_request_handler(self, request):
        return self.system.is_request_handler(request)

    def handle_request(self, request):
        return self.system.handle_request(request)

    def is_active(self):
        """
        Tests if the service is active.

        :rtype: bool
        :return: If the service is active.
        """

        return self.system.is_active()

    def get_handler_name(self):
        """
        Retrieves the handler name.

        :rtype: String
        :return: The handler name.
        """

        return self.system.get_handler_name()

    def get_handler_port(self):
        """
        Retrieves the handler port.

        :rtype: int
        :return: The handler port.
        """

        return self.system.get_handler_port()

    def get_handler_properties(self):
        """
        Retrieves the handler properties.

        :rtype: Dictionary
        :return: The handler properties.
        """

        return self.system.get_handler_properties()

    @colony.load_allowed_capability("rest_service")
    def rest_service_load_allowed(self, plugin, capability):
        self.system.load_rest_service_plugin(plugin)

    @colony.load_allowed_capability("rpc_service")
    def rpc_service_load_allowed(self, plugin, capability):
        self.system.update_service_methods(plugin)

    @colony.unload_allowed_capability("rest_service")
    def rest_service_unload_allowed(self, plugin, capability):
        self.system.unload_rest_service_plugin(plugin)

    @colony.unload_allowed_capability("rpc_service")
    def rpc_servicer_unload_allowed(self, plugin, capability):
        self.system.update_service_methods()
