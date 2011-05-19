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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class DistributionRegistryServerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Registry Server plugin.
    """

    id = "pt.hive.colony.plugins.distribution.registry_server"
    name = "Distribution Registry Server Plugin"
    short_name = "Distribution Registry Server"
    description = "Distribution Registry Server Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/distribution/registry_server/resources/baf.xml"
    }
    capabilities = [
        "distribution_server_adapter",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "distribution_helper"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.distribution.registry", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.remote.manager", "1.0.0")
    ]
    main_modules = [
        "distribution.registry_server.distribution_registry_server_system"
    ]

    distribution_registry_server = None
    """ The distribution registry server """

    distribution_helper_plugins = []
    """ The distribution helper plugins """

    distribution_registry_plugin = None
    """ The distribution registry plugin """

    main_remote_manager_plugin = None
    """ The main remote manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import distribution.registry_server.distribution_registry_server_system
        self.distribution_registry_server = distribution.registry_server.distribution_registry_server_system.DistributionRegistryServer(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.distribution.registry_server", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.distribution.registry_server", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.distribution.registry_server", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_distribution_server_type(self):
        return self.distribution_registry_server.get_distribution_server_type()

    def activate_server(self, properties):
        return self.distribution_registry_server.activate_server(properties)

    def deactivate_server(self, properties):
        return self.distribution_registry_server.deactivate_server(properties)

    @colony.base.decorators.load_allowed_capability("distribution_helper")
    def distribution_helper_load_allowed(self, plugin, capability):
        self.distribution_helper_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("distribution_helper")
    def distribution_helper_unload_allowed(self, plugin, capability):
        self.distribution_helper_plugins.remove(plugin)

    def get_distribution_registry_plugin(self):
        return self.distribution_registry_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.distribution.registry")
    def set_distribution_registry_plugin(self, distribution_registry_plugin):
        self.distribution_registry_plugin = distribution_registry_plugin

    def get_main_remote_manager_plugin(self):
        return self.main_remote_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.remote.manager")
    def set_main_remote_manager_plugin(self, main_remote_manager_plugin):
        self.main_remote_manager_plugin = main_remote_manager_plugin
