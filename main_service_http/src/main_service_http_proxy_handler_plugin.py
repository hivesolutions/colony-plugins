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

class MainServiceHttpProxyHandlerPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Service Main Proxy Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.http.proxy_handler"
    name = "Http Service Main Proxy Handler"
    description = "The plugin that offers the http service proxy handler"
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
    capabilities_allowed = [
        "http_service_directory_list_handler"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.client.http", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.main.pool.element_pool_manager", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.url_parser", "1.x.x")
    ]
    main_modules = [
        "main_service_http_proxy_handler.proxy_handler.main_service_http_proxy_handler_exceptions",
        "main_service_http_proxy_handler.proxy_handler.main_service_http_proxy_handler_system"
    ]

    main_service_http_proxy_handler = None
    """ The main service http proxy handler """

    client_http_plugin = None
    """ The client http plugin """

    element_pool_manager_plugin = None
    """ The element pool manager plugin """

    url_parser_plugin = None
    """ The url parser plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import main_service_http_proxy_handler.proxy_handler.main_service_http_proxy_handler_system
        self.main_service_http_proxy_handler = main_service_http_proxy_handler.proxy_handler.main_service_http_proxy_handler_system.MainServiceHttpProxyHandler(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)
        self.main_service_http_proxy_handler.load_handler()

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)
        self.main_service_http_proxy_handler.unload_handler()

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_service_http_proxy_handler.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        return self.main_service_http_proxy_handler.handle_request(request)

    def get_client_http_plugin(self):
        return self.client_http_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.client.http")
    def set_client_http_plugin(self, client_http_plugin):
        self.client_http_plugin = client_http_plugin

    def get_element_pool_manager_plugin(self):
        return self.element_pool_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.pool.element_pool_manager")
    def set_element_pool_manager_plugin(self, element_pool_manager_plugin):
        self.element_pool_manager_plugin = element_pool_manager_plugin

    def get_url_parser_plugin(self):
        return self.url_parser_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.url_parser")
    def set_url_parser_plugin(self, url_parser_plugin):
        self.url_parser_plugin = url_parser_plugin
