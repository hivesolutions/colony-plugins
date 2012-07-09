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

class ServiceUtilsPlugin(colony.base.system.Plugin):
    """
    The main class for the Service Utils plugin.
    """

    id = "pt.hive.colony.plugins.service.utils"
    name = "Service Utils"
    description = "The plugin that offers a utils for services"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities_allowed = [
        "threads",
        "socket_provider",
        "socket_upgrader"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.work.pool", "1.x.x")
    ]
    main_modules = [
        "service.utils.async",
        "service.utils.exceptions",
        "service.utils.sync",
        "service.utils.system",
        "service.utils.threads"
    ]

    service_utils = None
    """ The service utils """

    socket_provider_plugins = []
    """ The socket provider plugins """

    socket_upgrader_plugins = []
    """ The socket upgrader plugins """

    work_pool_plugin = None
    """ The work pool plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import service.utils.system
        self.service_utils = service.utils.system.ServiceUtils(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def generate_service(self, parameters):
        """
        Generates a new service for the given parameters.
        The generated service includes the creation of a new pool.

        @type parameters: Dictionary
        @param parameters: The parameters for service generation.
        @rtype: AbstractService
        @return: The generated service.
        """

        return self.service_utils.generate_service(parameters)

    def generate_service_port(self, parameters):
        """
        Generates a new service port for the current
        host, avoiding collisions.

        @type parameters: Dictionary
        @param parameters: The parameters for service port generation.
        @rtype: int
        @return: The newly generated port.
        """

        return self.service_utils.generate_service_port(parameters)

    @colony.base.decorators.load_allowed_capability("socket_provider")
    def socket_provider_load_allowed(self, plugin, capability):
        self.socket_provider_plugins.append(plugin)
        self.service_utils.socket_provider_load(plugin)

    @colony.base.decorators.load_allowed_capability("socket_upgrader")
    def socket_upgrader_load_allowed(self, plugin, capability):
        self.socket_upgrader_plugins.append(plugin)
        self.service_utils.socket_upgrader_load(plugin)

    @colony.base.decorators.unload_allowed_capability("socket_provider")
    def socket_provider_unload_allowed(self, plugin, capability):
        self.socket_provider_plugins.remove(plugin)
        self.service_utils.socket_provider_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("socket_upgrader")
    def socket_upgrader_unload_allowed(self, plugin, capability):
        self.socket_upgrader_plugins.remove(plugin)
        self.service_utils.socket_upgrader_unload(plugin)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.work.pool")
    def set_work_pool_plugin(self, work_pool_plugin):
        self.work_pool_plugin = work_pool_plugin
