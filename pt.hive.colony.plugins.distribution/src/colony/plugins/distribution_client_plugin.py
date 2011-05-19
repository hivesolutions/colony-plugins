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

class DistributionClientPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Client plugin.
    """

    id = "pt.hive.colony.plugins.distribution.client"
    name = "Distribution Client Plugin"
    short_name = "Distribution Client"
    description = "Distribution Client Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/distribution/client/resources/baf.xml"
    }
    capabilities = [
        "distribution_client",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "distribution_client_adapter",
        "distribution_helper"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.resources.resource_manager", "1.0.0")
    ]
    main_modules = [
        "distribution.client.distribution_client_system"
    ]

    distribution_client = None
    """ The distribution client """

    distribution_client_adapter_plugins = []
    """ The distribution client adapter plugins """

    distribution_helper_plugins = []
    """ The distribution helper plugins """

    resource_manager_plugin = None
    """ The resource manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import distribution.client.distribution_client_system
        self.distribution_client = distribution.client.distribution_client_system.DistributionClient(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.distribution.client", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.distribution.client", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.distribution.client", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_remote_instance_references(self):
        return self.distribution_client.get_remote_instance_references()

    def get_remote_client_references(self):
        return self.distribution_client.get_remote_client_references()

    def get_remote_client_references_by_host(self):
        return self.distribution_client.get_remote_client_references_by_host()

    def get_remote_plugin_reference(self):
        return self.distribution_client.get_remote_plugin_reference()

    @colony.base.decorators.load_allowed_capability("distribution_client_adapter")
    def distribution_client_adapter_load_allowed(self, plugin, capability):
        self.distribution_client_adapter_plugins.append(plugin)

    @colony.base.decorators.load_allowed_capability("distribution_helper")
    def distribution_helper_load_allowed(self, plugin, capability):
        self.distribution_helper_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("distribution_client_adapter")
    def distribution_client_adapter_unload_allowed(self, plugin, capability):
        self.distribution_client_adapter_plugins.remove(plugin)

    @colony.base.decorators.unload_allowed_capability("distribution_helper")
    def distribution_helper_unload_allowed(self, plugin, capability):
        self.distribution_helper_plugins.remove(plugin)

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin
