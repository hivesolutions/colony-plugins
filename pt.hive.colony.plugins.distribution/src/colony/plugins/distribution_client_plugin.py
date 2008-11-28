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

import colony.plugins.plugin_system

class DistributionClientPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Distribution Client plugin.
    """

    id = "pt.hive.colony.plugins.distribution.client"
    name = "Distribution Client Plugin"
    short_name = "Distribution Client"
    description = "Distribution Client Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["distribution_client"]
    capabilities_allowed = ["distribution_client_adapter", "remote_client_adapter"]
    dependencies = []
    events_handled = []
    events_registrable = []

    distribution_client = None

    distribution_client_adapter_plugins = []
    remote_client_adapter_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global distribution
        import distribution.client.distribution_client_system
        self.distribution_client = distribution.client.distribution_client_system.DistributionClient(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.distribution.client", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.distribution.client", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_remote_instance_references(self):
        return self.distribution_client.get_remote_instance_references()

    def get_remote_plugin_reference(self):
        return self.distribution_client.get_remote_plugin_reference()

    @colony.plugins.decorators.load_allowed_capability("distribution_client_adapter")
    def distribution_client_adapter_load_allowed(self, plugin, capability):
        self.distribution_client_adapter_plugins.append(plugin)

    @colony.plugins.decorators.load_allowed_capability("remote_client_adapter")
    def remote_client_adapter_load_allowed(self, plugin, capability):
        self.remote_client_adapter_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("distribution_client_adapter")
    def distribution_client_adapter_unload_allowed(self, plugin, capability):
        self.distribution_client_adapter_plugins.remove(plugin)

    @colony.plugins.decorators.unload_allowed_capability("remote_client_adapter")
    def remote_client_adapterr_unload_allowed(self, plugin, capability):
        self.remote_client_adapter_plugins.remove(plugin)
