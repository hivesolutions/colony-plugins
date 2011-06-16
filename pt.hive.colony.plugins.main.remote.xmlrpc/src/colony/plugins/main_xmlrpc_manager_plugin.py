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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainXmlrpcManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Xmlrpc Manager Main plugin.
    """

    id = "pt.hive.colony.plugins.main.remote.xmlrpc.manager"
    name = "Xmlrpc Manager Main Plugin"
    short_name = "Xmlrpc Manager Main"
    description = "Xmlrpc Manager Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_remote_xmlrpc/manager/resources/baf.xml"
    }
    capabilities = [
        "xmlrpc_manager",
        "http_python_handler",
        "rpc_handler",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "rpc_service"
    ]
    main_modules = [
        "main_remote_xmlrpc.manager.main_xmlrpc_manager_exceptions",
        "main_remote_xmlrpc.manager.main_xmlrpc_manager_system"
    ]

    main_xmlrpc_manager = None
    """ The main xmlrpc manager """

    rpc_service_plugins = []
    """ The rpc service plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_remote_xmlrpc.manager.main_xmlrpc_manager_system
        self.main_xmlrpc_manager = main_remote_xmlrpc.manager.main_xmlrpc_manager_system.MainXmlrpcManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_handler_filename(self):
        return self.main_xmlrpc_manager.get_handler_filename()

    def is_request_handler(self, request):
        return self.main_xmlrpc_manager.is_request_handler(request)

    def handle_request(self, request):
        return self.main_xmlrpc_manager.handle_request(request)

    def is_active(self):
        """
        Tests if the service is active.

        @rtype: bool
        @return: If the service is active.
        """

        return self.main_xmlrpc_manager.is_active()

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_xmlrpc_manager.get_handler_name()

    def get_handler_port(self):
        """
        Retrieves the handler port.

        @rtype: int
        @return: The handler port.
        """

        return self.main_xmlrpc_manager.get_handler_port()

    def get_handler_properties(self):
        """
        Retrieves the handler properties.

        @rtype: Dictionary
        @return: The handler properties.
        """

        return self.main_xmlrpc_manager.get_handler_properties()

    @colony.base.decorators.load_allowed_capability("rpc_service")
    def rpc_service_capability_load_allowed(self, plugin, capability):
        self.rpc_service_plugins.append(plugin)
        self.main_xmlrpc_manager.update_service_methods(plugin)

    @colony.base.decorators.unload_allowed_capability("rpc_service")
    def rpc_servicer_capability_unload_allowed(self, plugin, capability):
        self.rpc_service_plugins.remove(plugin)
        self.main_xmlrpc_manager.update_service_methods()
