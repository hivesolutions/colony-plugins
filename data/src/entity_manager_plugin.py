#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class EntityManagerPlugin(colony.Plugin):
    """
    The main class for the Entity Manager plugin.
    """

    id = "pt.hive.colony.plugins.data.entity.manager"
    name = "Entity Manager"
    description = "The plugin that manages the entity manager orm system"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["test"]
    capabilities_allowed = ["entity_engine"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.misc.json")]
    main_modules = ["entity_manager"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import entity_manager

        self.system = entity_manager.DataEntityManager(self)
        self.test = entity_manager.test.EntityManagerTest(self)
        self.decorators = entity_manager.decorators

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def load_entity_manager(self, engine_name):
        """
        Loads an entity manager for the given engine name.

        :type engine_name: String
        :param engine_name: The name of the engine to be used.
        :rtype: EntityManager
        :return: The loaded entity manager.
        """

        return self.system.load_entity_manager(engine_name)

    def load_entity_manager_properties(self, engine_name, properties):
        """
        Loads an entity manager for the given engine name.

        :type engine_name: String
        :param engine_name: The name of the engine to be used.
        :type properties: Dictionary
        :param properties: The properties to be used in the
        loading of the entity manager
        :rtype: EntityManager
        :return: The loaded entity manager.
        """

        return self.system.load_entity_manager(engine_name, properties)

    def get_entity_manager(self, id):
        """
        Retrieves the appropriate entity manager instance for the
        given (entity manager) identifier.
        In case no entity manager instance is found none is retrieved.

        :type id: String
        :param id: The identifier of the entity manager to be retrieved.
        :rtype: EntityManager
        :return: The retrieved entity manager.
        """

        return self.system.get_entity_manager(id)

    def get_entity_class(self):
        """
        Retrieves the top level entity class, responsible for the base
        methods to be used along all the entity classes.

        All the entities to be used in the context of the entity manager
        should inherit from this class in order to provide the appropriate
        interface for entity manager handling.

        :rtype: EntityClass
        :return: The top level entity class, responsible for the base
        methods to be used along all the entity classes.
        """

        return self.system.get_entity_class()

    def get_transaction_decorator(self):
        """
        Retrieves the transaction decorator used to decorate
        a method in order to force transaction existence.

        :rtype: Function
        :return: The transaction decorator function.
        """

        return self.decorators.transaction

    def get_lock_table_decorator(self):
        """
        Retrieves the lock table decorator used to decorate
        a method in order to force locking in table.

        :rtype: Function
        :return: The lock table decorator function.
        """

        return self.decorators.lock_table

    @colony.load_allowed_capability("entity_engine")
    def entity_engine_load_allowed(self, plugin, capability):
        self.system.register_entity_engine_plugin(plugin)

    @colony.unload_allowed_capability("entity_engine")
    def entity_engine_unload_allowed(self, plugin, capability):
        self.system.unregister_entity_engine_plugin(plugin)
