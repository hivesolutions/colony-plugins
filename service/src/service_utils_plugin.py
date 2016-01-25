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
""" The author(s) of the module """

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

class ServiceUtilsPlugin(colony.Plugin):
    """
    The main class for the Service Utils plugin.
    """

    id = "pt.hive.colony.plugins.service.utils"
    name = "Service Utils"
    description = "The plugin that offers a utils for services"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities_allowed = [
        "threads",
        "socket_provider",
        "socket_upgrader"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.work.pool")
    ]
    main_modules = [
        "service_utils"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import service_utils
        self.system = service_utils.ServiceUtils(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def generate_service(self, parameters):
        """
        Generates a new service for the given parameters.
        The generated service includes the creation of a new pool.

        @type parameters: Dictionary
        @param parameters: The parameters for service generation.
        @rtype: AbstractService
        @return: The generated service.
        """

        return self.system.generate_service(parameters)

    def generate_service_port(self, parameters):
        """
        Generates a new service port for the current
        host, avoiding collisions.

        @type parameters: Dictionary
        @param parameters: The parameters for service port generation.
        @rtype: int
        @return: The newly generated port.
        """

        return self.system.generate_service_port(parameters)

    @colony.load_allowed_capability("socket_provider")
    def socket_provider_load_allowed(self, plugin, capability):
        self.system.socket_provider_load(plugin)

    @colony.load_allowed_capability("socket_upgrader")
    def socket_upgrader_load_allowed(self, plugin, capability):
        self.system.socket_upgrader_load(plugin)

    @colony.unload_allowed_capability("socket_provider")
    def socket_provider_unload_allowed(self, plugin, capability):
        self.system.socket_provider_unload(plugin)

    @colony.unload_allowed_capability("socket_upgrader")
    def socket_upgrader_unload_allowed(self, plugin, capability):
        self.system.socket_upgrader_unload(plugin)
