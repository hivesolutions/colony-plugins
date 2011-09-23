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

__revision__ = "$LastChangedRevision: 7683 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 18:34:55 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import thread

import entity_manager_exceptions

ATTRIBUTE_EXCLUSION_LIST = (
    "__class__",
    "__delattr__",
    "__dict__",
    "__doc__",
    "__getattribute__",
    "__hash__",
    "__module__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__str__",
    "__weakref__",
    "__format__",
    "__sizeof__",
    "__subclasshook__",
    "data_state",
    "mapping_options",
    "id_attribute_name"
)
""" The attribute exclusion list """

TYPE_EXCLUSION_LIST = (
    types.MethodType,
    types.FunctionType,
    types.ClassType,
    types.InstanceType
)
""" The type exclusion list """

RELATION_ATTRIBUTES_METHOD_PREFIX = "get_relation_attributes_"
""" The relation attributes method prefix """

RELATION_DATA_TYPE = "relation"
""" The relation data type """

ID_FIELD = "id"
""" The id field """

DATA_TYPE_FIELD = "data_type"
""" The data type field """

TARGET_ENTITY_FIELD = "target_entity"
""" The target entity field """

JOIN_ATTRIBUTE_NAME_FIELD = "join_attribute_name"
""" The join attribute name field """

ID_ATTRIBUTE_NAME_VALUE = "id_attribute_name"
""" The id attribute name value """

ID_VALUE = "id"
""" The id value """

ENTITY_CLASSES_LIST_VALUE = "entity_classes_list"
""" The entity classes list value """

ENTITY_CLASSES_MAP_VALUE = "entity_classes_map"
""" The entity classes map value """

class DataEntityManager:
    """
    The data entity manager class.
    """

    entity_manager_plugin = None
    """ The entity manager plugin """

    entity_manager_engine_plugins_map = {}
    """ The map of entity manager engine plugins """

    loaded_entity_classes_list = []
    """ The list of loaded entity classes """

    loaded_entity_classes_map = {}
    """ The map associating the loaded entity classes with their names """

    loaded_entity_manager_map = {}
    """ The map associating the id with the (loaded) entity manager """

    def __init__(self, entity_manager_plugin):
        """
        Constructor of the class.

        @type entity_manager_plugin: EntityManagerPlugin
        @param entity_manager_plugin: The entity manager plugin.
        """

        self.entity_manager_plugin = entity_manager_plugin

        self.entity_manager_engine_plugins_map = {}
        self.loaded_entities_list = []
        self.loaded_entity_classes_map = {}
        self.loaded_entity_manager_map = {}

    def register_entity_manager_engine_plugin(self, entity_manager_engine_plugin):
        # retrieves the plugin engine name
        engine_name = entity_manager_engine_plugin.get_engine_name()

        # sets the entity manager engine plugin in the entity manager
        # engine plugins map
        self.entity_manager_engine_plugins_map[engine_name] = entity_manager_engine_plugin

    def unregister_entity_manager_engine_plugin(self, entity_manager_engine_plugin):
        # retrieves the plugin engine name
        engine_name = entity_manager_engine_plugin.get_engine_name()

        # removes the entity manager engine plugin from the entity manager
        # engine plugins map
        del self.entity_manager_engine_plugins_map[engine_name]

    def load_entity_class(self, entity_class):
        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # adds the entity class to the loaded entity classes structures
        self.loaded_entity_classes_list.append(entity_class)
        self.loaded_entity_classes_map[entity_class_name] = entity_class

    def unload_entity_class(self, entity_class):
        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        if entity_class in self.loaded_entity_classes_list:
            self.loaded_entity_classes_list.remove(entity_class)

        if entity_class_name in self.loaded_entity_classes_map:
            del self.loaded_entity_classes_map[entity_class_name]

    def load_entity_bundle(self, entity_bundle):
        """
        Loads (registers) the given entity bundle
        in the entity manager.

        @type entity_bundle: List
        @param entity_bundle: The entity bundle (list) to be
        loaded in the entity manager.
        """

        # iterates over all the entity classes in the
        # entity bundle (list) to load them
        for entity_class in entity_bundle:
            # loads the entity class
            self.load_entity_class(entity_class)

    def unload_entity_bundle(self, entity_bundle):
        """
        Unloads (unregisters) the given entity bundle
        from the entity manager.

        @type entity_bundle: List
        @param entity_bundle: The entity bundle (list) to be
        unloaded from the entity manager.
        """

        # iterates over all the entity classes in the
        # entity bundle (list) to unload them
        for entity_class in entity_bundle:
            # unloads the entity class
            self.unload_entity_class(entity_class)

    def load_entity_manager(self, engine_name, properties = {}):
        """
        Loads an entity manager for the given engine name.
        The loading of an entity manager may return an existing
        instance in case an entity manager with the same id is
        already loaded.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @type properties: Dictionary
        @param properties: The properties to be used in the
        loading of the entity manager.
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        # tries to retrieve the id of the "target" entity manager, falling back to
        # an undefined value for the id
        id = properties.get(ID_VALUE, None)

        # tries to retrieve the entity classes list, falling back to all
        # the currently loaded entity classes list
        entity_classes_list = properties.get(ENTITY_CLASSES_LIST_VALUE, self.loaded_entity_classes_list)

        # tries to retrieve the entity classes map, falling back to all
        # the currently loaded entity classes map
        entity_classes_map = properties.get(ENTITY_CLASSES_MAP_VALUE, self.loaded_entity_classes_map)

        # in case the engine name does not exist in the entity manager
        # engine plugins map
        if not engine_name in self.entity_manager_engine_plugins_map:
            # raises the entity manager engine not found exception
            raise entity_manager_exceptions.EntityManagerEngineNotFound("engine " + engine_name + " not available")

        # in case the id is already defined in the loaded
        # entity manager map (no need to load the entity manager)
        if id in self.loaded_entity_manager_map:
            # prints a debug message
            self.entity_manager_plugin.debug("Re-loading existent entity manager with id: %s" % id)

            # retrieves the entity manager from the loaded entity
            # manager map
            entity_manager = self.loaded_entity_manager_map[id]

            # extends the entity manager with the current entity classes list
            # and the entity classes map
            entity_manager.extend_entity_manager(entity_classes_list, entity_classes_map)

            # returns the entity manager (immediately)
            return entity_manager

        # prints a debug message
        self.entity_manager_plugin.debug("Loading new entity manager with engine: %s" % engine_name)

        # retrieves the entity mager engine plugin
        entity_manager_engine_plugin = self.entity_manager_engine_plugins_map[engine_name]

        # creates a new entity manager with the entity manager engine plugin, entity classes list
        # and the entity classes map
        entity_manager = EntityManager(entity_manager_engine_plugin, entity_classes_list, entity_classes_map)

        # in case the id of the entity manager is defined
        # (need to set the entity manager in the map)
        if id:
            # sets the entity manager in the loaded entity manager(s) map
            self.loaded_entity_manager_map[id] = entity_manager

        # returns the entity manager
        return entity_manager

class EntityManager:
    """
    The entity manager class.
    """

    entity_manager_engine_plugin = None
    """ The entity manager engine plugin """

    entity_classes_list = []
    """ The list of entity classes """

    entity_classes_map = {}
    """ The map associating the entity classes with their names """

    registered_entity_classes_list = []
    """ The list of entity classes that are already registered """

    connection_thread_id_map = {}
    """ The map containing the connection object (representing the database connection and the connection parameters) for the thread id """

    database_connection_thread_id_map = {}
    """ The map containing the database connection object for the thread id """

    database_system_connection_thread_id_map = {}
    """ The map containing the system database connection object for the thread id """

    transaction_stack_thread_id_map = {}
    """ The map containing the stack containing the pending transactions for the thread id """

    connection_parameters = {}
    """ The map containing the connection parameters """

    def __init__(self, entity_manager_engine_plugin, entity_classes_list, entity_classes_map = None):
        """
        Constructor of the class.

        @type entity_manager_engine_plugin: EntityManagerEnginePlugin
        @param entity_manager_engine_plugin: The engine entity manager plugin to be used.
        @type entity_classes_list: List
        @param entity_classes_list: The list of entity classes to be used.
        @type entity_classes_map: Dictionary
        @param entity_classes_map: The map entity classes to be used.
        """

        self.entity_manager_engine_plugin = entity_manager_engine_plugin
        self.entity_classes_list = entity_classes_list
        self.entity_classes_map = entity_classes_map

        self.registered_entity_classes_list = []
        self.connection_thread_id_map = {}
        self.database_connection_thread_id_map = {}
        self.database_system_connection_thread_id_map = {}
        self.transaction_stack_thread_id_map = {}
        self.connection_parameters = {}

    def get_engine_name(self):
        """
        Retrieves the engine name for the current
        connection.

        @rtype: String
        @return: The engine name for the current
        connection.
        """

        return self.entity_manager_engine_plugin.get_engine_name()

    def get_internal_version(self):
        """
        Retrieves the internal version for the current
        connection.

        @rtype: String
        @return: The internal version for the current
        connection.
        """

        return self.entity_manager_engine_plugin.get_internal_version()

    def get_connection(self):
        """
        Retrieves the current available connection.

        @rtype: Connection
        @return: The current available database connection.
        """

        # gets the id of the current thread
        current_thread_id = thread.get_ident()

        # in case there is no connection available for the current thread
        if not current_thread_id in self.connection_thread_id_map:
            # retrieves the database connection
            database_connection = self.get_database_connection()

            # retrieves the database system connection
            database_system_connection = self.get_database_system_connection()

            # retrieves the transaction stack
            transaction_stack = self.get_transaction_stack()

            # creates the connection object with the specified database connection, database system connection
            # the specified connection parameters and the specified transaction stack
            connection = Connection(database_connection, database_system_connection, self.connection_parameters, transaction_stack)

            # sets the current thread connection
            self.connection_thread_id_map[current_thread_id] = connection

        # returns the current thread connection
        return self.connection_thread_id_map[current_thread_id]

    def close_connection(self):
        """
        Closes the current available connection.
        """

        # closes the database connection and the
        # database system connection
        self.close_database_connection()
        self.close_database_system_connection()

    def get_database_connection(self):
        """
        Retrieves the current available database connection.

        @rtype: Connection
        @return: The current available database connection.
        """

        # gets the id of the current thread
        current_thread_id = thread.get_ident()

        # in case there is no database connection available for the current thread
        if not current_thread_id in self.database_connection_thread_id_map:
            # creates the database connection to the specified engine with the specified connection parameters
            database_connection = self.entity_manager_engine_plugin.create_connection(self.connection_parameters)

            # sets the current thread database connection
            self.database_connection_thread_id_map[current_thread_id] = database_connection

        # returns the current thread database connection
        return self.database_connection_thread_id_map[current_thread_id]

    def get_database_system_connection(self):
        """
        Retrieves the current available database system connection.

        @rtype: Connection
        @return: The current available database system connection.
        """

        # gets the id of the current thread
        current_thread_id = thread.get_ident()

        # in case there is no database connection available for the current thread
        if not current_thread_id in self.database_system_connection_thread_id_map:
            # creates the database system connection to the specified engine with the specified connection parameters
            database_system_connection = self.entity_manager_engine_plugin.create_connection(self.connection_parameters)

            # sets the current thread database system connection
            self.database_system_connection_thread_id_map[current_thread_id] = database_system_connection

        # returns the current thread database system connection
        return self.database_system_connection_thread_id_map[current_thread_id]

    def close_database_connection(self):
        """
        Closes the current available database connection.
        """

        # retrieves the database connection
        database_connection = self.get_database_connection()

        # closes the database connection to the specified engine
        self.entity_manager_engine_plugin.close_connection(database_connection)

    def close_database_system_connection(self):
        """
        Closes the current available database system connection.
        """

        # retrieves the database system connection
        database_system_connection = self.get_database_system_connection()

        # closes the database system connection to the specified engine
        self.entity_manager_engine_plugin.close_connection(database_system_connection)

    def get_database_size(self):
        """
        Retrieves the database size for the current
        connection.

        @rtype: int
        @return: The database size for the current connection.
        """

        # retrieves the connection object
        connection = self.get_connection()

        return self.entity_manager_engine_plugin.get_database_size(connection)

    def get_transaction_stack(self):
        """
        Retrieves the current available transaction stack.

        @rtype: List
        @return: The current available transaction stack.
        """

        # gets the id of the current thread
        current_thread_id = thread.get_ident()

        # in case there is no transaction stack available for the current thread
        if not current_thread_id in self.transaction_stack_thread_id_map:
            # creates a new transaction stack
            transaction_stack = []

            # sets the current thread database transaction stack
            self.transaction_stack_thread_id_map[current_thread_id] = transaction_stack

        # returns the current thread transaction stack
        return self.transaction_stack_thread_id_map[current_thread_id]

    def set_connection_parameters(self, connection_parameters):
        """
        Sets the connection parameters of the entity manager.
        The connection parameters are used to established the connection
        with the database endpoint.

        @type connection_parameters: Dictionary
        @param connection_parameters: The map containing the connection parameters.
        """

        self.connection_parameters = connection_parameters

    def load_entity_manager(self, flush = False):
        """
        Loads the entity manager, registering the classes
        and creating the table generator (generates the tables).
        This method may be used for reloading the classes
        structures in the data source (without any side effect).
        Using the flush method all the internal data structures are
        updated at the cost of some performance impact.

        @type flush: bool
        @param flush: If the the internal data structures should be
        forced for update (more resources used).
        """

        self.register_classes(flush)
        self.create_table_generator()

    def unload_entity_manager(self):
        """
        Unloads the entity manager, disabling all the necessary
        structures.
        """

        pass

    def extend_entity_manager(self, entity_classes_list, entity_classes_map):
        """
        Extends the current entity manager instance with the given
        list of entity classes and the map of (the same) entity classes.

        @type entity_classes_list: List
        @param entity_classes_list: The entity classes list to be
        used in the extension of the entity manager instance.
        @type entity_classes_map: Dictionary
        @param entity_classes_map: The entity classes map to be
        used in the extension of the entity manager instance.
        """

        # iterates over all the entity classes to be registered to add
        # them to the current internal structures (taking into account
        # a possible garbage collection)
        for entity_class_name, entity_class in entity_classes_map.items():
            # checks if the entity class already exists (registered) in the
            # entity manager (garbage collection required)
            entity_class_exists = entity_class_name in self.entity_classes_map

            # in case the entity classes exists (runs garbage collection)
            if entity_class_exists:
                # retrieves the current entity class (reference)
                current_entity_class = self.entity_classes_map[entity_class_name]

                # removes the current entity class from the entity classes
                # list and in case it exists in the registered entity classes
                # list removes it from there also
                self.entity_classes_list.remove(current_entity_class)
                if current_entity_class in self.registered_entity_classes_list:
                    self.registered_entity_classes_list.remove(current_entity_class)

            # adds the entity class to the entity classes list
            # and registers it in the entity classes map (internal
            # structures update)
            self.entity_classes_list.append(entity_class)
            self.entity_classes_map[entity_class_name] = entity_class

    def register_classes(self, flush = False):
        """
        Registers all the available classes in the entity manager,
        the registration includes updating or creating the table definition
        in the target data source.

        @type flush: bool
        @param flush: If the entity classes should be registered even
        if they've already been registered.
        """

        # retrieves the connection object
        connection = self.get_connection()

        # iterates over all the entity classes in the entity
        # classes list (to update or create the entity definition)
        for entity_class in self.entity_classes_list:
            # in case the registration of classes does not require flushing
            # and the entity class is already registered (no need to use
            # data source resources)
            if not flush and entity_class in self.registered_entity_classes_list:
                # continues the loop (no need to lock data source resources)
                continue

            # in case the entity class is already defined in the data
            # source "schema"
            if self.entity_manager_engine_plugin.exists_entity_definition(connection, entity_class):
                # in case the entity definition is not synced with the data source
                if not self.entity_manager_engine_plugin.synced_entity_definition(connection, entity_class):
                    # updates the entity definition (because the model is not synced)
                    self.entity_manager_engine_plugin.update_entity_definition(connection, entity_class)
            # otherwise the entity class is not defined and should be created
            else:
                # creates the entity definition in the data source
                self.entity_manager_engine_plugin.create_entity_definition(connection, entity_class)

            # in case the entity class does not already exists in the registered
            # entity classes list (first time registration)
            if not entity_class in self.registered_entity_classes_list:
                # adds the entity class to the list of registered entity classes
                self.registered_entity_classes_list.append(entity_class)

    def create_table_generator(self):
        # retrieves the connection object
        connection = self.get_connection()

        if not self.entity_manager_engine_plugin.exists_table_generator(connection):
            self.entity_manager_engine_plugin.create_table_generator(connection)

    def lock_table(self, table_name, parameters):
        # retrieves the connection object
        connection = self.get_connection()

        return self.entity_manager_engine_plugin.lock_table(connection, table_name, parameters)

    def retrieve_next_name_id(self, name):
        # retrieves the connection object
        connection = self.get_connection()

        return self.entity_manager_engine_plugin.retrieve_next_name_id(connection, name)

    def set_next_name_id(self, name, next_id):
        # retrieves the connection object
        connection = self.get_connection()

        return self.entity_manager_engine_plugin.set_next_name_id(connection, name, next_id)

    def increment_next_name_id(self, name, id_increment = 1):
        # retrieves the connection object
        connection = self.get_connection()

        return self.entity_manager_engine_plugin.increment_next_name_id(connection, name, id_increment)

    def get_entity_class(self, entity_class_name):
        return self.entity_classes_map.get(entity_class_name, None)

    def create_transaction(self, transaction_name = None):
        """
        Creates a new transaction in the entity manager
        with the given transaction name.

        @type transaction_name: String
        @param transaction_name: The name of the transaction.
        @rtype: bool
        @return: The result of transaction creation.
        """

        # retrieves the connection object
        connection = self.get_connection()

        # creates the transaction in the engine plugin
        self.entity_manager_engine_plugin.create_transaction(connection, transaction_name)

        # retrieves the transaction stack
        transaction_stack = self.get_transaction_stack()

        # adds the transaction name to the transaction stack
        transaction_stack.append(transaction_name)

        # returns true
        return True

    def commit_transaction(self, transaction_name = None):
        """
        Commits the transaction with the given transaction name,
        or the current available transaction if no name is specified.

        @type transaction_name: String
        @param transaction_name: The name of the transaction to the "commited".
        @rtype: bool
        @return: The result of transaction commit.
        """

        # retrieves the transaction stack
        transaction_stack = self.get_transaction_stack()

        # in case the transaction stack is empty
        if not transaction_stack:
            # returns false
            return False

        # retrieves the connection object
        connection = self.get_connection()

        # commits the transaction in the engine plugin
        self.entity_manager_engine_plugin.commit_transaction(connection, transaction_name)

        # pops the current element from the transaction stack
        transaction_stack.pop()

        # returns true
        return True

    def rollback_transaction(self, transaction_name = None):
        """
        "Rollsback" the transaction with the given transaction name,
        or the current available transaction if no name is specified.

        @type transaction_name: String
        @param transaction_name: The name of the transaction to the "rolledback".
        @rtype: bool
        @return: The result of transaction rollback.
        """

        # retrieves the transaction stack
        transaction_stack = self.get_transaction_stack()

        # in case the transaction stack is empty
        if not transaction_stack:
            # returns false
            return False

        # retrieves the connection object
        connection = self.get_connection()

        # "rollsback" the transaction in the engine plugin
        self.entity_manager_engine_plugin.rollback_transaction(connection, transaction_name)

        # pops the current element from the transaction stack
        transaction_stack.pop()

        # returns true
        return True

    def commit(self):
        # retrieves the connection object
        connection = self.get_connection()

        # commits the current cached data
        self.entity_manager_engine_plugin.commit_connection(connection)

    def rollback(self):
        # retrieves the connection object
        connection = self.get_connection()

        # "rollsback" the current cached data
        self.entity_manager_engine_plugin.rollback_connection(connection)

    def validate_relation(self, entity, relation_entity_id, relation_attribute_name):
        # retrieves the connection object
        connection = self.get_connection()

        # validates the relation
        return self.entity_manager_engine_plugin.validate_relation(connection, entity, relation_entity_id, relation_attribute_name)

    def save(self, entity):
        # retrieves the connection object
        connection = self.get_connection()

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case the entity id attribute is defined
        if not entity_id_attribute_value == None:
            # in case there is already an entry with the same key value
            if self.entity_manager_engine_plugin.find_entity(connection, entity_class, entity_id_attribute_value):
                raise entity_manager_exceptions.EntityManagerEngineDuplicateEntry("the key value " + str(entity_id_attribute_value) + " already exists in the database")

        # persists the entity
        return self.entity_manager_engine_plugin.save_entity(connection, entity)

    def _save(self, entity):
        # retrieves the connection object
        connection = self.get_connection()

        # persists the entity
        return self.entity_manager_engine_plugin.save_entity(connection, entity)

    def save_many(self, entities):
        # retrieves the connection object
        connection = self.get_connection()

        # persists the entities
        return self.entity_manager_engine_plugin.save_entities(connection, entities)

    def update(self, entity):
        # retrieves the connection object
        connection = self.get_connection()

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case there is no entry with the same key value
        if not self.entity_manager_engine_plugin.find_entity(connection, entity_class, entity_id_attribute_value):
            # raises the entity manager engine entry not found exception
            raise entity_manager_exceptions.EntityManagerEngineEntryNotFound("the key value " + str(entity_id_attribute_value) + " was not found in the database")

        # persists the entity
        return self.entity_manager_engine_plugin.update_entity(connection, entity)

    def _update(self, entity):
        # retrieves the connection object
        connection = self.get_connection()

        # persists the entity
        return self.entity_manager_engine_plugin.update_entity(connection, entity)

    def remove(self, entity):
        """
        Removes an entity from the database.

        @type entity: Object
        @param entity: The entity to be removed from the database.
        @rtype: bool
        @return: The result of the removal.
        """

        # retrieves the connection object
        connection = self.get_connection()

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case there is no entry with the same key value
        if not self.entity_manager_engine_plugin.find_entity(connection, entity_class, entity_id_attribute_value):
            # raises the entity manager engine entry not found exception
            raise entity_manager_exceptions.EntityManagerEngineEntryNotFound("the key value " + str(entity_id_attribute_value) + " was not found in the database")

        # removes the entity
        return self.entity_manager_engine_plugin.remove_entity(connection, entity)

    def _remove(self, entity):
        # retrieves the connection object
        connection = self.get_connection()

        # removes the entity
        return self.entity_manager_engine_plugin.remove_entity(connection, entity)

    def save_update(self, entity):
        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case the entity id attribute valid
        # is not set
        if entity_id_attribute_value == None:
            # saves the entity
            self.save(entity)
        # otherwise
        else:
            # updates the entity
            self.update(entity)

    def _save_update(self, entity):
        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case the entity id attribute valid
        # is not set
        if entity_id_attribute_value == None:
            # saves the entity
            self._save(entity)
        # otherwise
        else:
            # updates the entity
            self._update(entity)

    def get(self, entity_class, id_value, options = {}):
        # retrieves the connection object
        connection = self.get_connection()

        # finds the entity
        return self.entity_manager_engine_plugin.find_entity_options(connection, entity_class, id_value, options)

    def find_a(self, entity_class, options = {}):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
        return self.entity_manager_engine_plugin.find_all_entities_options(connection, entity_class, options)

    def find(self, entity_class, id_value):
        # retrieves the connection object
        connection = self.get_connection()

        # finds the entity
        return self.entity_manager_engine_plugin.find_entity(connection, entity_class, id_value)

    def find_options(self, entity_class, id_value, options):
        # retrieves the connection object
        connection = self.get_connection()

        # finds the entity
        return self.entity_manager_engine_plugin.find_entity_options(connection, entity_class, id_value, options)

    def _find_all(self, entity_class):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
        return self.entity_manager_engine_plugin.find_all_entities(connection, entity_class)

    def _find_all_options(self, entity_class, options):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
        return self.entity_manager_engine_plugin.find_all_entities_options(connection, entity_class, options)

    def lock(self, entity_class, id_value):
        # retrieves the connection object
        connection = self.get_connection()

        # locks the connection for the given entity class
        # and id value
        return self.entity_manager_engine_plugin.lock(connection, entity_class, id_value)

    def get_entity_class_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all attributes from the given entity class.

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the names of all attributes from the given entity class.
        """

        # retrieves all the class attribute names
        entity_class_attribute_names = dir(entity_class)

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = [attribute_name for attribute_name in entity_class_attribute_names if not attribute_name in ATTRIBUTE_EXCLUSION_LIST and not type(getattr(entity_class, attribute_name)) in TYPE_EXCLUSION_LIST]

        return entity_class_valid_attribute_names

    def get_entity_class_relation_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all the relational attributes from the given entity class.

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the names of all the relational attributes from the given entity class.
        """

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the relation attribute names
        entity_class_relation_attribute_names = [attribute_name for attribute_name in entity_class_valid_attribute_names if getattr(entity_class, attribute_name)[DATA_TYPE_FIELD] == RELATION_DATA_TYPE]

        return entity_class_relation_attribute_names

    def get_entity_class_non_relation_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all the non relational attributes from the given entity class.

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the names of all the non relational attributes from the given entity class.
        """

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the non relation attribute names
        entity_class_non_relation_attribute_names = [attribute_name for attribute_name in entity_class_valid_attribute_names if not getattr(entity_class, attribute_name)[DATA_TYPE_FIELD] == RELATION_DATA_TYPE]

        return entity_class_non_relation_attribute_names

    def get_entity_class_attribute_values(self, entity_class):
        """
        Retrieves a list with the values of all attributes from the given entity class.

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the values of all attributes from the given entity class.
        """

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = [getattr(entity_class, attribute_name) for attribute_name in entity_class_valid_attribute_names]

        return entity_class_valid_attribute_values

    def get_entity_id_attribute_value(self, entity):
        """
        Retrieves the value of the entity id attribute.

        @type entity: Entity
        @param entity: The entity to retrieve the id attribute value.
        @rtype: Object
        @return: The value of the entity id attribute.
        """

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

        # retrieves the entity id attribute value
        entity_id_attribute_value = getattr(entity, entity_class_id_attribute_name)

        return entity_id_attribute_value

    def get_entity_class_id_attribute_value(self, entity_class):
        """
        Retrieves the value of the entity class id attribute.

        @type entity: Class
        @param entity: The entity class to retrieve the id attribute value.
        @rtype: Object
        @return: The value of the entity class id attribute.
        """

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

        # retrieves the entity class id attribute value
        entity_class_id_attribute_value = getattr(entity_class, entity_class_id_attribute_name)

        return entity_class_id_attribute_value

    def get_entity_class_id_attribute_name(self, entity_class):
        """
        Retrieves the name of the entity class id attribute.

        @type entity: Class
        @param entity: The entity class to retrieve the id attribute name.
        @rtype: String
        @return: The name of the entity class id attribute.
        """

        # in case the entity class contains the id attribute name value
        # (cached value)
        if hasattr(entity_class, ID_ATTRIBUTE_NAME_VALUE):
            # retrieves the id attribute directly from the entity class (cached)
            return getattr(entity_class, ID_ATTRIBUTE_NAME_VALUE)

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # creates the initial index value
        index = 0

        # iterates over all the entity class valid attribute values
        # in order to find the correct id value
        for entity_class_valid_attribute_value in entity_class_valid_attribute_values:
            # retrieve the id field value
            id_field_value = entity_class_valid_attribute_value.get(ID_FIELD, False)

            # in case the current attribute value is not an id
            if not id_field_value:
                # increments the index value
                index += 1

                # continues the loop
                continue

            # retrieves the id attribute name
            id_attribute_name = entity_class_valid_attribute_names[index]

            # sets the id attribute name value in the entity class to the id attribute name
            # this strategy allow the caching of the id value (improving speed)
            setattr(entity_class, ID_ATTRIBUTE_NAME_VALUE, id_attribute_name)

            # returns the id attribute name
            return id_attribute_name

    def get_relation_attributes(self, entity_class, relation_attribute_name):
        # creates the method name with the relation attributes prefix and the relation attribute name
        method_name = RELATION_ATTRIBUTES_METHOD_PREFIX + relation_attribute_name

        # in case the entity class does not contain the method
        # for the relation attributes retrieval method
        if not hasattr(entity_class, method_name):
            # raises the entity manager missing relation method exception
            raise entity_manager_exceptions.EntityManagerMissingRelationMethod(method_name)

        # retrieves the relation attributes retrieval method
        relation_attributes_method = getattr(entity_class, method_name)

        # retrieves the relation attributes
        relation_attributes = relation_attributes_method()

        # returns the relation attributes
        return relation_attributes

    def get_attribute_data_type(self, attribute_value, entity_class, relation_attribute_name):
        """
        Retrieves the data type of the give attribute value.

        @type attribute_value: Dictionary
        @param attribute_value: The attribute value, containing the entity attribute metadata.
        @type entity_class: Class
        @param entity_class: The entity class containing the relation.
        @type relation_attribute_name: String
        @param relation_attribute_name: The name of the relation attribute.
        @rtype: String
        @return: The attribute data type.
        """

        # retrieves the attribute value data type
        attribute_value_data_type = attribute_value[DATA_TYPE_FIELD]

        # in case the attribute value data type is of type relation
        if attribute_value_data_type == RELATION_DATA_TYPE:
            # retrieves the relation attributes
            relation_attributes = self.get_relation_attributes(entity_class, relation_attribute_name)

            # retrieves the entity class target entity
            entity_class_target_entity = relation_attributes[TARGET_ENTITY_FIELD]

            # retrieves the entity class join attribute name
            entity_class_join_attribute_name = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

            # retrieves the entity class join attribute
            entity_class_join_attribute = getattr(entity_class_target_entity, entity_class_join_attribute_name)

            # retrieves the data type for the entity class join attribute
            entity_class_join_attribute_data_type = entity_class_join_attribute[DATA_TYPE_FIELD]

            return entity_class_join_attribute_data_type
        # otherwise it must be a "simple" attribute
        else:
            return attribute_value_data_type

    def get_entity_classes_list(self):
        """
        Retrieves the entity classes list.

        @rtype: List
        @return: The entity classes list.
        """

        return self.entity_classes_list

    def set_entity_classes_list(self, entity_classes_list):
        """
        Sets the entity classes list.

        @type entity_classes_list: List
        @param entity_classes_list: The entity classes list.
        """

        self.entity_classes_list = entity_classes_list

    def get_entity_classes_map(self):
        """
        Retrieves the entity classes map.

        @rtype: Dictionary
        @return: The entity classes map.
        """

        return self.entity_classes_map

    def set_entity_classes_map(self, entity_classes_map):
        """
        Sets the entity classes map.

        @type entity_classes_map: Dictionary
        @param entity_classes_map: The entity classes map.
        """

        self.entity_classes_map = entity_classes_map

class Connection:
    """
    The class representing a database connection
    with the associated attributes.
    """

    database_connection = None
    """ The database connection object """

    database_system_connection = None
    """ The database system connection object """

    connection_parameters = {}
    """ The connection parameters for the connection """

    transaction_stack = []
    """ The transaction stack for the connection """

    def __init__(self, database_connection, database_system_connection, connection_parameters, transaction_stack):
        """
        Constructor of the class.

        @type database_connection: DatabaseConnection
        @param database_connection: The database connection object.
        @type database_system_connection: DatabaseConnection
        @param database_system_connection: The database system connection object.
        @type connection_parameters: Dictionary
        @param connection_parameters: The connection parameters for the connection.
        @type transaction_stack: List
        @param transaction_stack: The transaction stack for the connection.
        """

        self.database_connection = database_connection
        self.database_system_connection = database_system_connection
        self.connection_parameters = connection_parameters
        self.transaction_stack = transaction_stack

    def add_conection_parameter(self, key, value):
        """
        Adds a parameter to the connection.

        @type key: String
        @param key: The name of the parameter to be added.
        @type value: Object
        @param value: The parameter value to be added.
        """

        self.connection_parameters[key] = value

    def remove_connection_parameter(self, key):
        """
        Removes the parameter with the given name
        from the connection parameters.

        @type key: String
        @param key: The name of the parameter to be removed.
        """

        del self.connection_parameters[key]

    def get_connection_parameter(self, key):
        """
        Retrieves the parameter with the given name
        from the connection.

        @type key: String
        @param key: The name of the parameter to be
        retrieved.
        @rtype: Object
        @return: The retrieved parameter.
        """

        return self.connection_parameters.get(key, None)
