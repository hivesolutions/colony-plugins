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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class MainServiceNormalSocketProviderPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Service Main Normal Socket Provider plugin.
    """

    id = "pt.hive.colony.plugins.main.service.normal_socket_provider"
    name = "Service Main Normal Socket Provider Plugin"
    short_name = "Service Main Normal Socket Provider"
    description = "The plugin that offers the normal socket provider"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_service_normal_socket_provider/normal_socket_provider/resources/baf.xml"}
    capabilities = ["socket_provider", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_service_normal_socket_provider.normal_socket_provider.main_service_normal_socket_provider_system"]

    main_service_normal_socket_provider = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_service_normal_socket_provider
        import main_service_normal_socket_provider.normal_socket_provider.main_service_normal_socket_provider_system
        self.main_service_normal_socket_provider = main_service_normal_socket_provider.normal_socket_provider.main_service_normal_socket_provider_system.MainServiceNormalSocketProvider(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_provider_name(self):
        """
        Retrieves the socket provider name.

        @rtype: String
        @return: The socket provider name.
        """

        return self.main_service_normal_socket_provider.get_provider_name()

    def provide_socket(self):
        """
        Provides a new socket, configured with
        the default parameters.

        @rtype: Socket
        @return: The provided socket.
        """

        return self.main_service_normal_socket_provider.provide_socket()

    def provide_socket_parameters(self, parameters):
        """
        Provides a new socket, configured with
        the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for socket configuration.
        @rtype: Socket
        @return: The provided socket.
        """

        return self.main_service_normal_socket_provider.provide_socket_parameters(parameters)
