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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class BusinessSessionManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Business Entity Manager plugin
    """

    id = "pt.hive.colony.plugins.business.session_manager"
    name = "Business Session Manager Plugin"
    short_name = "Business Session Manager"
    description = "Business Session Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["business_session_manager"]
    capabilities_allowed = ["business_session_serializer", "business_logic", "business_logic_bundle"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.business.entity_manager", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.pool.simple_pool_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    business_session_manager = None

    business_session_serializer_plugins = []

    business_entity_manager_plugin = None
    simple_pool_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global business
        import business.session_manager.business_session_manager_system
        self.business_session_manager = business.session_manager.business_session_manager_system.BusinessSessionManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.business.session_manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.business.session_manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.business.session_manager", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_session_manager(self, session_name, entity_manager):
        return self.business_session_manager.load_session_manager(session_name, entity_manager)

    def load_session_manager_master(self, session_name, entity_manager):
        return self.business_session_manager.load_session_manager_master(session_name, entity_manager)

    def load_session_manager_entity_manager(self, session_name, engine_name):
        return self.business_session_manager.load_session_manager_entity_manager(session_name, engine_name)

    def load_session_manager_master_entity_manager(self, session_name, engine_name):
        return self.business_session_manager.load_session_manager_master_entity_manager(session_name, engine_name)

    def get_transaction_decorator(self):
        return self.business_entity_manager_plugin.get_transaction_decorator()

    @colony.plugins.decorators.load_allowed_capability("business_session_serializer")
    def business_session_serializer_load_allowed(self, plugin, capability):
        self.business_session_serializer_plugins.append(plugin)

    @colony.plugins.decorators.load_allowed_capability("business_logic")
    def business_logic_load_allowed(self, plugin, capability):
        business_logic_class = plugin.get_business_logic_class()
        self.business_session_manager.load_business_logic_class(business_logic_class)

    @colony.plugins.decorators.load_allowed_capability("business_logic_bundle")
    def business_logic_bundle_load_allowed(self, plugin, capability):
        business_logic_bundle = plugin.get_business_logic_bundle()
        self.business_session_manager.load_business_logic_bundle(business_logic_bundle)

    @colony.plugins.decorators.unload_allowed_capability("business_session_serializer")
    def business_session_serializer_unload_allowed(self, plugin, capability):
        if plugin in self.business_session_serializer_plugins:
            self.business_session_serializer_plugins.remove(plugin)

    @colony.plugins.decorators.unload_allowed_capability("business_logic")
    def business_logic_unload_allowed(self, plugin, capability):
        business_logic_class = plugin.get_business_logic_class()
        self.business_session_manager.unload_business_logic_class(business_logic_class)

    @colony.plugins.decorators.unload_allowed_capability("business_logic_bundle")
    def business_logic_bundle_unload_allowed(self, plugin, capability):
        business_logic_bundle = plugin.get_business_logic_bundle()
        self.business_session_manager.unload_business_logic_bundle(business_logic_bundle)

    def get_business_entity_manager_plugin(self):
        return self.business_entity_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.business.entity_manager")
    def set_business_entity_manager_plugin(self, business_entity_manager_plugin):
        self.business_entity_manager_plugin = business_entity_manager_plugin

    def get_simple_pool_manager_plugin(self):
        return self.simple_pool_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.pool.simple_pool_manager")
    def set_simple_pool_manager_plugin(self, simple_pool_manager_plugin):
        self.simple_pool_manager_plugin = simple_pool_manager_plugin
