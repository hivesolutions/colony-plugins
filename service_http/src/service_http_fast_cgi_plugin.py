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
import colony.base.decorators

class ServiceHttpFastCgiPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Service Fast Cgi plugin.
    """

    id = "pt.hive.colony.plugins.service.http.fast_cgi"
    name = "Http Service Fast Cgi"
    description = "The plugin that offers the http service fast cgi"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "http_service_handler"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.resources.manager", "1.x.x")
    ]
    main_modules = [
        "service_http.fast_cgi.exceptions",
        "service_http.fast_cgi.system"
    ]

    service_http_fast_cgi = None
    """ The service http fast cgi (handler) """

    resources_manager_plugin = None
    """ The resources manager plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import service_http.fast_cgi.system
        self.service_http_fast_cgi = service_http.fast_cgi.system.ServiceHttpFastCgi(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.service_http_fast_cgi.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        return self.service_http_fast_cgi.handle_request(request)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.manager")
    def set_resources_manager_plugin(self, resources_manager_plugin):
        self.resources_manager_plugin = resources_manager_plugin
