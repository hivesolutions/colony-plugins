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

class MainClientUtilsPlugin(colony.base.system.Plugin):
    """
    The main class for the Client Main Utils plugin.
    """

    id = "pt.hive.colony.plugins.main.client.utils"
    name = "Client Main Utils"
    description = "The plugin that offers a utils for clients"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_client_utils/utils/resources/baf.xml"
    }
    capabilities = [
        "build_automation_item"
    ]
    capabilities_allowed = [
        "socket_provider",
        "socket_upgrader"
    ]
    main_modules = [
        "main_client_utils.utils.main_client_utils_exceptions",
        "main_client_utils.utils.main_client_utils_system"
    ]

    main_client_utils = None
    """ The main client utils """

    socket_provider_plugins = []
    """ The socket provider plugins """

    socket_upgrader_plugins = []
    """ The socket upgrader plugins """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import main_client_utils.utils.main_client_utils_system
        self.main_client_utils = main_client_utils.utils.main_client_utils_system.MainClientUtils(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

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
