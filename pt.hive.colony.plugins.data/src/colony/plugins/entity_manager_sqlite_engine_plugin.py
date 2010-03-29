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

__revision__ = "$LastChangedRevision: 7650 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 12:16:51 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class EntityManagerSqliteEnginePlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Entity Manager Sqlite Engine plugin.
    """

    id = "pt.hive.colony.plugins.data.entity_manager.sqlite_engine"
    name = "Entity Manager Sqlite Engine Plugin"
    short_name = "Entity Manager Sqlite Engine"
    description = "Entity Manager Sqlite Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["entity_manager_engine"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.business.helper", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["data.entity_manager_sqlite_engine.entity_manager_sqlite_engine_exceptions", "data.entity_manager_sqlite_engine.entity_manager_sqlite_engine_system"]

    entity_manager_sqlite_engine = None

    business_helper_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data
        import data.entity_manager_sqlite_engine.entity_manager_sqlite_engine_system
        self.entity_manager_sqlite_engine = data.entity_manager_sqlite_engine.entity_manager_sqlite_engine_system.EntityManagerSqliteEngine(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.data.entity_manager.sqlite_engine", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_engine_name(self):
        return self.entity_manager_sqlite_engine.get_engine_name()

    def create_connection(self, connection_parameters):
        return self.entity_manager_sqlite_engine.create_connection(connection_parameters)

    def close_connection(self, connection):
        return self.entity_manager_sqlite_engine.close_connection(connection)

    def commit_connection(self, connection):
        return self.entity_manager_sqlite_engine.commit_connection(connection)

    def rollback_connection(self, connection):
        return self.entity_manager_sqlite_engine.rollback_connection(connection)

    def create_transaction(self, connection, transaction_name):
        return self.entity_manager_sqlite_engine.create_transaction(connection, transaction_name)

    def commit_transaction(self, connection, transaction_name):
        return self.entity_manager_sqlite_engine.commit_transaction(connection, transaction_name)

    def rollback_transaction(self, connection, transaction_name):
        return self.entity_manager_sqlite_engine.rollback_transaction(connection, transaction_name)

    def exists_entity_definition(self, connection, entity_class):
        return self.entity_manager_sqlite_engine.exists_entity_definition(connection, entity_class)

    def synced_entity_definition(self, connection, entity_class):
        return self.entity_manager_sqlite_engine.synced_entity_definition(connection, entity_class)

    def create_entity_definition(self, connection, entity_class):
        return self.entity_manager_sqlite_engine.create_entity_definition(connection, entity_class)

    def remove_entity_definition(self, connection, entity_class):
        return self.entity_manager_sqlite_engine.remove_entity_definition(connection, entity_class)

    def update_entity_definition(self, connection, entity_class):
        return self.entity_manager_sqlite_engine.update_entity_definition(connection, entity_class)

    def create_table_generator(self, connection):
        return self.entity_manager_sqlite_engine.create_table_generator(connection)

    def exists_table_generator(self, connection):
        return self.entity_manager_sqlite_engine.exists_table_generator(connection)

    def retrieve_next_name_id(self, connection, name):
        return self.entity_manager_sqlite_engine.retrieve_next_name_id(connection, name)

    def set_next_name_id(self, connection, name, next_id):
        return self.entity_manager_sqlite_engine.set_next_name_id(connection, name, next_id)

    def increment_next_name_id(self, connection, name, id_increment = 1):
        return self.entity_manager_sqlite_engine.increment_next_name_id(connection, name, id_increment)

    def save_entity(self, connection, entity):
        return self.entity_manager_sqlite_engine.save_entity(connection, entity)

    def save_entities(self, connection, entities):
        return self.entity_manager_sqlite_engine.save_entities(connection, entities)

    def update_entity(self, connection, entity):
        return self.entity_manager_sqlite_engine.update_entity(connection, entity)

    def remove_entity(self, connection, entity):
        return self.entity_manager_sqlite_engine.remove_entity(connection, entity)

    def find_entity(self, connection, entity_class, id_value):
        return self.entity_manager_sqlite_engine.find_entity(connection, entity_class, id_value)

    def find_entity_options(self, connection, entity_class, id_value, options):
        return self.entity_manager_sqlite_engine.find_entity_options(connection, entity_class, id_value, options = options)

    def find_all_entities(self, connection, entity_class, value, search_field_name):
        return self.entity_manager_sqlite_engine.find_all_entities(connection, entity_class, value, search_field_name)

    def find_all_entities_options(self, connection, entity_class, value, search_field_name, options):
        return self.entity_manager_sqlite_engine.find_all_entities_options(connection, entity_class, value, search_field_name, options = options)

    def get_business_helper_plugin(self):
        return self.business_helper_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.business.helper")
    def set_business_helper_plugin(self, business_helper_plugin):
        self.business_helper_plugin = business_helper_plugin
