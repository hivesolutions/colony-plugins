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

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainRemoteClientManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Remote Client Manager Main plugin
    """

    id = "pt.hive.colony.plugins.main.remote.client.manager"
    name = "Remote Client Manager Main Plugin"
    short_name = "Remote Client Manager Main"
    description = "Remote Client Manager Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_remote_client/manager/resources/baf.xml"
    }
    capabilities = [
        "remote_client_manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "remote_client_adapter"
    ]
    main_modules = [
        "main_remote_client.manager.main_remote_client_manager_system"
    ]

    main_remote_client_manager = None
    """ The main remote client manager """

    remote_client_adapter_plugins = []
    """ The remote client adapter plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_remote_client.manager.main_remote_client_manager_system
        self.main_remote_client_manager = main_remote_client.manager.main_remote_client_manager_system.MainRemoteClientManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.main.remote.client.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.main.remote.client.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_remote_client(self, service_name, service_attributes):
        return self.main_remote_client_manager.create_remote_client(service_name, service_attributes)

    @colony.base.decorators.load_allowed_capability("remote_client_adapter")
    def remote_client_adapter_load_allowed(self, plugin, capability):
        self.main_remote_client_manager.register_remote_client_adapter_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("remote_client_adapter")
    def remote_client_adapter_unload_allowed(self, plugin, capability):
        self.main_remote_client_manager.unregister_remote_client_adapter_plugin(plugin)
