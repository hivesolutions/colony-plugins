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

class MainDistributionServicePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Main Service plugin.
    """

    id = "pt.hive.colony.plugins.distribution.main.registry.service"
    name = "Distribution Main Service Plugin"
    short_name = "Distribution Main Service"
    description = "Distribution Main Service Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_distribution/service/resources/baf.xml"}
    capabilities = ["rpc_service", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.distribution.main.plugin_system", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["main_distribution.service.main_distribution_service_system"]

    main_distribution_service = None

    @colony.base.decorators.load_plugin("pt.hive.colony.plugins.distribution.main.registry.service", "1.0.0")
    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_distribution
        import main_distribution.service.main_distribution_service_system
        self.main_distribution_service = main_distribution.service.main_distribution_service_system.MainDistributionService(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.distribution.main.registry.service", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.plugin_call(True)
    def get_service_id(self):
        return self.main_distribution_service.get_service_id()

    @colony.base.decorators.plugin_call(True)
    def get_service_alias(self):
        return self.main_distribution_service.get_service_alias()

    @colony.base.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return self.main_distribution_service.get_available_rpc_methods()

    @colony.base.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return self.main_distribution_service.get_rpc_methods_alias()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def unload_plugin_manager(self):
        return self.main_distribution_service.unload_plugin_manager()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def unload_plugin_by_id(self, plugin_id):
        return self.main_distribution_service.unload_plugin_by_id(plugin_id)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_plugin_proxy_by_id(self, plugin_id):
        return self.main_distribution_service.get_plugin_proxy_by_id(plugin_id)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def call_plugin_proxy_method(self, plugin_id, plugin_version, method_name, arguments):
        return self.main_distribution_service.call_plugin_proxy_method(plugin_id, plugin_version, method_name, arguments)

    def get_main_distribution_plugin_system_plugin(self):
        return self.main_distribution_plugin_system_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.distribution.main.plugin_system")
    def set_main_distribution_plugin_system_plugin(self, main_distribution_plugin_system_plugin):
        self.main_distribution_plugin_system_plugin = main_distribution_plugin_system_plugin
