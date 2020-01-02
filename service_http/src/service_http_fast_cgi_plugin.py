#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class ServiceHTTPFastCGIPlugin(colony.Plugin):
    """
    The main class for the HTTP Service FastCGI plugin.
    """

    id = "pt.hive.colony.plugins.service.http.fast_cgi"
    name = "HTTP Service FastCGI"
    description = "The plugin that offers the HTTP service FastCGI"
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
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.resources.manager")
    ]
    main_modules = [
        "service_http_fast_cgi"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import service_http_fast_cgi
        self.system = service_http_fast_cgi.ServiceHTTPFastCGI(self)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        :rtype: String
        :return: The handler name.
        """

        return self.system.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given HTTP request.

        :type request: HTTPRequest
        :param request: The HTTP request to be handled.
        """

        return self.system.handle_request(request)
