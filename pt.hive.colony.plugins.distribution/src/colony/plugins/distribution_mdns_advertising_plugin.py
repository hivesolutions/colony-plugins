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

class DistributionMdnsAdvertisingPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Mdns Advertising plugin.
    """

    id = "pt.hive.colony.plugins.distribution.mdns.advertising"
    name = "Distribution Mdns Advertising Plugin"
    short_name = "Distribution Mdns Advertising"
    description = "Distribution Mdns Advertising Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/distribution/mdns_advertising/resources/baf.xml"
    }
    capabilities = [
        "distribution_advertising_adapter",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.distribution.registry", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.client.mdns", "1.0.0")
    ]
    main_modules = [
        "distribution.mdns_advertising.distribution_mdns_advertising_system"
    ]

    distribution_mdns_advertising = None
    """ The distribution mdns advertising """

    distribution_registry_plugin = None
    """ The distribution registry plugin """

    main_client_mdns_plugin = None
    """ The main client mdns plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import distribution.mdns_advertising.distribution_mdns_advertising_system
        self.distribution_mdns_advertising = distribution.mdns_advertising.distribution_mdns_advertising_system.DistributionMdnsAdvertising(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return self.distribution_mdns_advertising.get_adapter_name()

    def handle_advertise(self, arguments):
        """
        Handles a (distribution) advertising.

        @type arguments: Dictionary
        @param arguments: The arguments to the
        (distribution) advertising.
        """

        return self.distribution_mdns_advertising.handle_advertise(arguments)

    def get_distribution_registry_plugin(self):
        return self.distribution_registry_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.distribution.registry")
    def set_distribution_registry_plugin(self, distribution_registry_plugin):
        self.distribution_registry_plugin = distribution_registry_plugin

    def get_main_client_mdns_plugin(self):
        return self.main_client_mdns_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.mdns")
    def set_main_client_mdns_plugin(self, main_client_mdns_plugin):
        self.main_client_mdns_plugin = main_client_mdns_plugin
