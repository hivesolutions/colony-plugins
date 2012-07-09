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

class RestPlugin(colony.base.system.Plugin):
    """
    The main class for the Rest plugin.
    """

    id = "pt.hive.colony.plugins.remote.rest"
    name = "Rest"
    description = "Rest Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
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
        colony.base.system.PluginDependency("pt.hive.colony.plugins.resources.resource_manager", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.random", "1.x.x")
    ]
    main_modules = [
        "remote_rest.exceptions",
        "remote_rest.system"
    ]

    rest = None
    """ The rest (manager) object reference """

    resource_manager_plugin = None
    """ The resource manager plugin """

    rest_encoder_plugins = []
    """ The rest encoder plugins """

    rest_service_plugins = []
    """ The rest service plugins """

    rpc_service_plugins = []
    """ The rpc service plugins """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import remote_rest.system
        self.rest = remote_rest.system.Rest(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def is_request_handler(self, request):
        return self.rest.is_request_handler(request)

    def handle_request(self, request):
        return self.rest.handle_request(request)

    def is_active(self):
        """
        Tests if the service is active.

        @rtype: bool
        @return: If the service is active.
        """

        return self.rest.is_active()

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.rest.get_handler_name()

    def get_handler_port(self):
        """
        Retrieves the handler port.

        @rtype: int
        @return: The handler port.
        """

        return self.rest.get_handler_port()

    def get_handler_properties(self):
        """
        Retrieves the handler properties.

        @rtype: Dictionary
        @return: The handler properties.
        """

        return self.rest.get_handler_properties()

    @colony.base.decorators.load_allowed_capability("rest_encoder")
    def rest_encoder_load_allowed(self, plugin, capability):
        self.rest_encoder_plugins.append(plugin)

    @colony.base.decorators.load_allowed_capability("rest_service")
    def rest_service_load_allowed(self, plugin, capability):
        self.rest_service_plugins.append(plugin)
        self.rest.load_rest_service_plugin(plugin)

    @colony.base.decorators.load_allowed_capability("rpc_service")
    def rpc_service_load_allowed(self, plugin, capability):
        self.rpc_service_plugins.append(plugin)
        self.rest.update_service_methods(plugin)

    @colony.base.decorators.unload_allowed_capability("rest_encoder")
    def rest_encoder_unload_allowed(self, plugin, capability):
        self.rest_encoder_plugins.remove(plugin)

    @colony.base.decorators.unload_allowed_capability("rest_service")
    def rest_service_unload_allowed(self, plugin, capability):
        self.rest_service_plugins.remove(plugin)
        self.rest.unload_rest_service_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("rpc_service")
    def rpc_servicer_unload_allowed(self, plugin, capability):
        self.rpc_service_plugins.remove(plugin)
        self.rest.update_service_methods()

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.random")
    def set_random_plugin(self, random_plugin):
        self.random_plugin = random_plugin
