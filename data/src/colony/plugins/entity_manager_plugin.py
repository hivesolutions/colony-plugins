#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import colony.base.plugin_system
import colony.base.decorators

class EntityManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Entity Manager plugin.
    """

    id = "pt.hive.colony.plugins.data.entity_manager"
    name = "Entity Manager Plugin"
    short_name = "Data Entity Manager"
    description = "The plugin that manages the entity manager orm system"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/data/entity_manager/resources/baf.xml"
    }
    capabilities = [
        "entity_manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "entity_manager_engine",
        "entity",
        "entity_bundle"
    ]
    main_modules = [
        "data.entity_manager.entity_manager_decorators",
        "data.entity_manager.entity_manager_exceptions",
        "data.entity_manager.entity_manager_system"
    ]

    entity_manager = None
    """ The entity manager """

    entity_manager_decorators_module = None
    """ The entity manager decorators module """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import data.entity_manager.entity_manager_system
        import data.entity_manager.entity_manager_decorators
        self.entity_manager = data.entity_manager.entity_manager_system.DataEntityManager(self)
        self.entity_manager_decorators_module = data.entity_manager.entity_manager_decorators

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_entity_manager(self, engine_name):
        """
        Loads an entity manager for the given engine name.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        return self.entity_manager.load_entity_manager(engine_name)

    def load_entity_manager_properties(self, engine_name, properties):
        """
        Loads an entity manager for the given engine name.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @type properties: Dictionary
        @param properties: The properties to be used in the
        loading of the entity manager
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        return self.entity_manager.load_entity_manager(engine_name, properties)

    def get_entity_manager(self, id):
        """
        Retrieves the appropriate entity manager instance for the
        given (entity manager) identifier.
        In case no entity manager instance is found none is retrieved.

        @type id: String
        @param id: The identifier of the entity manager to be retrieved.
        @rtype: EntityManager
        @return: The retrieved entity manager.
        """

        return self.entity_manager.get_entity_manager(id)

    def get_transaction_decorator(self):
        """
        Retrieves the transaction decorator used to decorate
        a method in order to force transaction existence.

        @rtype: Function
        @return: The transaction decorator function.
        """

        return self.entity_manager_decorators_module.transaction

    def get_lock_table_decorator(self):
        """
        Retrieves the lock table decorator used to decorate
        a method in order to force locking in table.

        @rtype: Function
        @return: The lock table decorator function.
        """

        return self.entity_manager_decorators_module.lock_table

    @colony.base.decorators.load_allowed_capability("entity_manager_engine")
    def entity_manager_engine_load_allowed(self, plugin, capability):
        self.entity_manager.register_entity_manager_engine_plugin(plugin)

    @colony.base.decorators.load_allowed_capability("entity")
    def entity_capability_load_allowed(self, plugin, capability):
        entity_class = plugin.get_entity_class()
        self.entity_manager.load_entity_class(entity_class)

    @colony.base.decorators.load_allowed_capability("entity_bundle")
    def entity_bundle_capability_load_allowed(self, plugin, capability):
        entity_bundle = plugin.get_entity_bundle()
        self.entity_manager.load_entity_bundle(entity_bundle)

    @colony.base.decorators.unload_allowed_capability("entity_manager_engine")
    def entity_manager_engine_unload_allowed(self, plugin, capability):
        self.entity_manager.unregister_entity_manager_engine_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("entity")
    def entity_capability_unload_allowed(self, plugin, capability):
        entity_class = plugin.get_entity_class()
        self.entity_manager.unload_entity_class(entity_class)

    @colony.base.decorators.unload_allowed_capability("entity_bundle")
    def entity_bundle_capability_unload_allowed(self, plugin, capability):
        entity_bundle = plugin.get_entity_bundle()
        self.entity_manager.unload_entity_bundle(entity_bundle)
