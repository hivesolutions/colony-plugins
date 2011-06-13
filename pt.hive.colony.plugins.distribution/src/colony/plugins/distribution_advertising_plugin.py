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

class DistributionAdvertisingPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Advertising plugin.
    """

    id = "pt.hive.colony.plugins.distribution.advertising"
    name = "Distribution Advertising Plugin"
    short_name = "Distribution Advertising"
    description = "Plugin responsible for the scheduling and management of the advertising plugins"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/distribution/advertising/resources/baf.xml"
    }
    capabilities = [
        "distribution_advertising",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "distribution_advertising_adapter",
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.scheduler", "1.0.0"),
    ]
    main_modules = [
        "distribution.advertising.distribution_advertising_system"
    ]

    distribution_advertising = None
    """ The distribution advertising """

    distribution_advertising_adapter_plugins = []
    """ The distribution adapter plugins """

    scheduler_plugin = None
    """ The scheduler plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import distribution.advertising.distribution_advertising_system
        self.distribution_advertising = distribution.advertising.distribution_advertising_system.DistributionAdvertising(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.distribution_advertising.load_advertising({})

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.distribution_advertising.unload_advertising({})

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.distribution.advertising", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.distribution.advertising", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.distribution.advertising", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_advertising(self, properties):
        return self.distribution_advertising.load_advertising(properties)

    def unload_advertising(self, properties):
        return self.distribution_advertising.unload_advertising(properties)

    @colony.base.decorators.load_allowed_capability("distribution_advertising_adapter")
    def distribution_advertising_adapter_load_allowed(self, plugin, capability):
        self.distribution_advertising_adapter_plugins.append(plugin)
        self.distribution_advertising.distribution_advertising_adapter_load(plugin)

    @colony.base.decorators.unload_allowed_capability("distribution_advertising_adapter")
    def distribution_advertising_adapter_plugins_unload_allowed(self, plugin, capability):
        self.distribution_advertising_adapter_plugins.remove(plugin)
        self.distribution_advertising.distribution_advertising_adapter_unload(plugin)

    def get_scheduler_plugin(self):
        return self.scheduler_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.scheduler")
    def set_scheduler_plugin(self, scheduler_plugin):
        self.scheduler_plugin = scheduler_plugin
