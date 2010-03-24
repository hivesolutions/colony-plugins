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

class BusinessEntityManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Business Entity Manager plugin
    """

    id = "pt.hive.colony.plugins.business.entity_manager"
    name = "Business Entity Manager Plugin"
    short_name = "Business Entity Manager"
    description = "Business Entity Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["entity_manager"]
    capabilities_allowed = ["entity_manager_engine", "entity", "entity_bundle"]
    dependencies = []
    events_handled = []
    events_registrable = []

    business_entity_manager = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global business
        import business.entity_manager.business_entity_manager_system
        import business.entity_manager.business_entity_manager_decorators
        self.business_entity_manager = business.entity_manager.business_entity_manager_system.BusinessEntityManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.business.entity_manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.business.entity_manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_entity_manager(self, engine_name):
        """
        Loads an entity manager for the given engine name.

        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        return self.business_entity_manager.load_entity_manager(engine_name)

    def get_transaction_decorator(self):
        """
        Retrieves the transaction decorator used to decorate
        a method in order to force transaction existence.

        @rtype: Function
        @return: The transaction decorator function.
        """

        return business.entity_manager.business_entity_manager_decorators.transaction

    @colony.plugins.decorators.load_allowed_capability("entity_manager_engine")
    def entity_manager_engine_load_allowed(self, plugin, capability):
        self.business_entity_manager.register_entity_manager_engine_plugin(plugin)

    @colony.plugins.decorators.load_allowed_capability("entity")
    def entity_capability_load_allowed(self, plugin, capability):
        entity_class = plugin.get_entity_class()
        self.business_entity_manager.load_entity_class(entity_class)

    @colony.plugins.decorators.load_allowed_capability("entity_bundle")
    def entity_bundle_capability_load_allowed(self, plugin, capability):
        entity_bundle = plugin.get_entity_bundle()
        self.business_entity_manager.load_entity_bundle(entity_bundle)

    @colony.plugins.decorators.unload_allowed_capability("entity_manager_engine")
    def entity_manager_engine_unload_allowed(self, plugin, capability):
        self.business_entity_manager.unregister_entity_manager_engine_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("entity")
    def entity_capability_unload_allowed(self, plugin, capability):
        entity_class = plugin.get_entity_class()
        self.business_entity_manager.unload_entity_class(entity_class)

    @colony.plugins.decorators.unload_allowed_capability("entity_bundle")
    def entity_bundle_capability_unload_allowed(self, plugin, capability):
        entity_bundle = plugin.get_entity_bundle()
        self.business_entity_manager.unload_entity_bundle(entity_bundle)
