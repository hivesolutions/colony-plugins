#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class EntityMysqlPlugin(colony.base.system.Plugin):
    """
    The main class for the Entity Mysql plugin.
    """

    id = "pt.hive.colony.plugins.data.entity_mysql"
    name = "Entity Mysql"
    description = "The plugin that manages the mysql adaptation structures for the entity manager"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "plugin_test_case_bundle"
    ]
    capabilities_allowed = [
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.x.x")
    ]
    main_modules = [
        "data.entity_manager.decorators",
        "data.entity_manager.exceptions",
        "data.entity_manager.mysql_system",
        "data.entity_manager.pgsql_system",
        "data.entity_manager.sqlite_system"
        "data.entity_manager.structures",
        "data.entity_manager.system",
        "data.entity_manager.test_mocks",
        "data.entity_manager.test"
    ]

    entity_mysql = None
    """ The entity mysql """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import data.entity_manager.system
        self.entity_manager = data.entity_manager.system.DataEntityManager(self)

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

    def get_entity_class(self):
        """
        Retrieves the top level entity class, responsible for the base
        methods to be used along all the entity classes.

        All the entities to be used in the context of the entity manager
        should inherit from this class in order to provide the appropriate
        interface for entity manager handling.

        @rtype: EntityClass
        @return: The top level entity class, responsible for the base
        methods to be used along all the entity classes.
        """

        return self.entity_manager.get_entity_class()

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

    def get_plugin_test_case_bundle(self):
        return self.entity_manager_test.get_plugin_test_case_bundle()

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
