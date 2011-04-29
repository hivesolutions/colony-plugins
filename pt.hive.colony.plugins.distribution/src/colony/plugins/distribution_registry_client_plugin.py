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

class DistributionRegistryClientPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Registry Client plugin.
    """

    id = "pt.hive.colony.plugins.distribution.registry_client"
    name = "Distribution Registry Client Plugin"
    short_name = "Distribution Registry Client"
    description = "Distribution Registry Client Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/distribution/registry_client/resources/baf.xml"
    }
    capabilities = [
        "distribution_client_adapter",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "distribution_helper"
    ]
    main_modules = [
        "distribution.registry_client.distribution_registry_client_system"
    ]

    distribution_registry_client = None
    """ The distribution registry client """

    distribution_helper_plugins = []
    """ The distribution helper plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global distribution
        import distribution.registry_client.distribution_registry_client_system
        self.distribution_registry_client = distribution.registry_client.distribution_registry_client_system.DistributionRegistryClient(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.distribution.registry_client", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.distribution.registry_clieny", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_remote_instance_references(self, properties):
        return self.distribution_registry_client.get_remote_instance_references(properties)

    @colony.base.decorators.load_allowed_capability("distribution_helper")
    def distribution_helper_load_allowed(self, plugin, capability):
        self.distribution_helper_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("distribution_helper")
    def distribution_helper_unload_allowed(self, plugin, capability):
        self.distribution_helper_plugins.remove(plugin)
