#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class ServiceHttpColonyPlugin(colony.Plugin):
    """
    The main class for the Http Service Colony plugin.
    """

    id = "pt.hive.colony.plugins.service.http.colony"
    name = "Http Service Colony"
    description = "The plugin that offers the http service colony"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "http_service_handler"
    ]
    capabilities_allowed = [
        "http_handler"
    ]
    main_modules = [
        "service_http_colony"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import service_http_colony
        self.system = service_http_colony.ServiceHttpColony(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        :rtype: String
        :return: The handler name.
        """

        return self.system.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given http request.

        :type request: HttpRequest
        :param request: The http request to be handled.
        """

        return self.system.handle_request(request)

    @colony.load_allowed_capability("http_handler")
    def http_handler_load_allowed(self, plugin, capability):
        self.system.http_handler_load(plugin)

    @colony.unload_allowed_capability("http_handler")
    def http_handler_unload_allowed(self, plugin, capability):
        self.system.http_handler_unload(plugin)
