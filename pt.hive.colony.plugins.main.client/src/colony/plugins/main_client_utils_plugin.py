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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class MainClientUtilsPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Client Main Utils plugin.
    """

    id = "pt.hive.colony.plugins.main.client.utils"
    name = "Client Main Utils Plugin"
    short_name = "Client Main Utils"
    description = "The plugin that offers a utils for clients"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_client_utils/utils/resources/baf.xml"}
    capabilities = ["build_automation_item"]
    capabilities_allowed = ["socket_provider", "socket_upgrader"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_client_utils.utils.main_client_utils_exceptions",
                    "main_client_utils.utils.main_client_utils_system"]

    main_client_utils = None

    socket_provider_plugins = []
    socket_upgrader_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_client_utils
        import main_client_utils.utils.main_client_utils_system
        self.main_client_utils = main_client_utils.utils.main_client_utils_system.MainClientUtils(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.main.client.utils", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.main.client.utils", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def generate_client(self, parameters):
        """
        Generates a new client for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for client generation.
        @rtype: AbstractClient
        @return: The generated client.
        """

        return self.main_client_utils.generate_client(parameters)

    @colony.base.decorators.load_allowed_capability("socket_provider")
    def socket_provider_load_allowed(self, plugin, capability):
        self.socket_provider_plugins.append(plugin)
        self.main_client_utils.socket_provider_load(plugin)

    @colony.base.decorators.load_allowed_capability("socket_upgrader")
    def socket_upgrader_load_allowed(self, plugin, capability):
        self.socket_upgrader_plugins.append(plugin)
        self.main_client_utils.socket_upgrader_load(plugin)

    @colony.base.decorators.unload_allowed_capability("socket_provider")
    def socket_provider_unload_allowed(self, plugin, capability):
        self.socket_provider_plugins.remove(plugin)
        self.main_client_utils.socket_provider_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("socket_upgrader")
    def socket_upgrader_unload_allowed(self, plugin, capability):
        self.socket_upgrader_plugins.remove(plugin)
        self.main_client_utils.socket_upgrader_unload(plugin)
