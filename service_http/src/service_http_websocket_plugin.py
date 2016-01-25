#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class ServiceHttpWebsocketPlugin(colony.Plugin):
    """
    The main class for the Http Service Websocket plugin.
    """

    id = "pt.hive.colony.plugins.service.http.websocket"
    name = "Http Service Websocket"
    description = "The plugin that offers the http service websocket"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "http_service_handler"
    ]
    capabilities_allowed = [
        "websocket_handler"
    ]
    main_modules = [
        "service_http_websocket"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import service_http_websocket
        self.system = service_http_websocket.ServiceHttpWebsocket(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.system.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        return self.system.handle_request(request)

    @colony.load_allowed_capability("websocket_handler")
    def websocket_handler_load_allowed(self, plugin, capability):
        self.system_handler.websocket_handler_load(plugin)

    @colony.unload_allowed_capability("websocket_handler")
    def websocket_handler_unload_allowed(self, plugin, capability):
        self.system_handler.websocket_handler_unload(plugin)
