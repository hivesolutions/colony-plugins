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

ATTRIBUTE_EXCLUSION_LIST = ["__class__", "__delattr__", "__dict__", "__doc__", "__getattribute__", "__hash__", "__module__", "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__str__", "__weakref__", "__format__", "__sizeof__", "__subclasshook__", "mapping_options", "id_attribute_name"]
""" The attribute exclusion list """

TYPE_EXCLUSION_LIST = [types.MethodType, types.FunctionType, types.ClassType, types.InstanceType]
""" The type exclusion list """

RELATION_DATA_TYPE = "relation"
""" The relation data type """

ID_FIELD = "id"
""" The id field """

DATA_TYPE_FIELD = "data_type"
""" The data type field """

ID_ATTRIBUTE_NAME_VALUE = "id_attribute_name"
""" The id attribute name value """

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

    entity_manager_engine_plugins_list = []
    """ The list of entity manager engine plugins """

    loaded_entity_classes_list = []
    """ The list of loaded entity classes """

    loaded_entity_classes_map = {}
    """ The map associating the loaded entity classes with their names """

    def __init__(self, entity_manager_plugin):
        """
        Constructor of the class.

        @type entity_manager_plugin: EntityManagerPlugin
        @param entity_manager_plugin: The entity manager plugin.
        """

        self.entity_manager_plugin = entity_manager_plugin

        self.entity_manager_engine_plugins_list = []
        self.loaded_entities_list = []
        self.loaded_entity_classes_map = {}

    def register_entity_manager_engine_plugin(self, entity_manager_engine_plugin):
        if not entity_manager_engine_plugin in self.entity_manager_engine_plugins_list:
            self.entity_manager_engine_plugins_list.append(entity_manager_engine_plugin)

    def unregister_entity_manager_engine_plugin(self, entity_manager_engine_plugin):
        if entity_manager_engine_plugin in self.entity_manager_engine_plugins_list:
            self.entity_manager_engine_plugins_list.remove(entity_manager_engine_plugin)

    def load_entity_class(self, entity_class):
        # retrieves the entity class name
        entity_class_name = entity_class.__name__

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
        for entity_class in entity_bundle:
            self.load_entity_class(entity_class)

    def unload_entity_bundle(self, entity_bundle):
        for entity_class in entity_bundle:
            self.unload_entity_class(entity_class)

    def load_entity_manager(self, engine_name, properties = {}):
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

        # tries to retrieve the entity classes list, falling back to all
        # the currently loaded entity classes list
        entity_classes_list = properties.get(ENTITY_CLASSES_LIST_VALUE, self.loaded_entity_classes_list)

        # tries to retrieve the entity classes map, falling back to all
        # the currently loaded entity classes map
        entity_classes_map = properties.get(ENTITY_CLASSES_MAP_VALUE, self.loaded_entity_classes_map)

        # iterates over all the entity manager engine plugins
        for entity_manager_engine_plugin in self.entity_manager_engine_plugins_list:
            # retrieves the entity manager engine name
            entity_manager_engine_name = entity_manager_engine_plugin.get_engine_name()

            # in case the entity manager engine name is the requested
            # engine name
            if entity_manager_engine_name == engine_name:
                # creates a new entity manager with the entity manager engine plugin, entity classes list
                # and the entity classes map
                entity_manager = EntityManager(entity_manager_engine_plugin, entity_classes_list, entity_classes_map)

                # returns the entity manager
                return entity_manager

        # raises the entity manager engine not found exception
        raise entity_manager_exceptions.EntityManagerEngineNotFound("engine " + engine_name + " not available")

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

        self.connection_thread_id_map = {}
        self.database_connection_thread_id_map = {}
        self.database_system_connection_thread_id_map = {}
        self.transaction_stack_thread_id_map = {}

        self.connection_parameters = {}

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

    def load_entity_manager(self):
        """
        Loads the entity manager, registering the classes
        and creating the table generator (generates the tables).
        """

        self.register_classes()
        self.create_table_generator()

    def unload_entity_manager(self):
        """
        Unloads the entity manager, disabling all the necessary
        structures.
        """

        pass

    def register_classes(self):
        """
        Registers all the available classes in the entity manager,
        the registration includes updating or creating the table definition
        in the target data source.
        """

        # retrieves the connection object
        connection = self.get_connection()

        # iterates over all the entity classes
        # in the entity classes list
        for entity_class in self.entity_classes_list:
            if self.entity_manager_engine_plugin.exists_entity_definition(connection, entity_class):
                if not self.entity_manager_engine_plugin.synced_entity_definition(connection, entity_class):
                    # updates the entity definition (because the model is not synced)
                    self.entity_manager_engine_plugin.update_entity_definition(connection, entity_class)
            else:
                self.entity_manager_engine_plugin.create_entity_definition(connection, entity_class)

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
        if entity_class_name in self.entity_classes_map:
            return self.entity_classes_map[entity_class_name]

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

        # in case the creation of the transaction is successfull
        if self.entity_manager_engine_plugin.create_transaction(connection, transaction_name):
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

        # in case the commit transaction is successful
        if self.entity_manager_engine_plugin.commit_transaction(connection, transaction_name):
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

        # in case the rollback is successful
        if self.entity_manager_engine_plugin.rollback_transaction(connection, transaction_name):
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

    def find_all(self, entity_class, value, search_field_name):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
        return self.entity_manager_engine_plugin.find_all_entities(connection, entity_class, value, search_field_name)

    def _find_all(self, entity_class):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
        return self.entity_manager_engine_plugin.find_all_entities(connection, entity_class, None, None)

    def find_all_options(self, entity_class, value, search_field_name, options):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
        return self.entity_manager_engine_plugin.find_all_entities_options(connection, entity_class, value, search_field_name, options)

    def _find_all_options(self, entity_class, options):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
        return self.entity_manager_engine_plugin.find_all_entities_options(connection, entity_class, None, None, options)

    def lock(self, entity_class, id_value):
        # retrieves the connection object
        connection = self.get_connection()

        # finds all the entities
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

        for entity_class_valid_attribute_value in entity_class_valid_attribute_values:
            if ID_FIELD in entity_class_valid_attribute_value:
                if entity_class_valid_attribute_value[ID_FIELD]:
                    setattr(entity_class, ID_ATTRIBUTE_NAME_VALUE, entity_class_valid_attribute_names[index])
                    return entity_class_valid_attribute_names[index]

            # increments the index value
            index += 1

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

    connection_parameters = []
    """ The connection parameters for the connection """

    transaction_stack = []
    """ The transaction stack for the connection """

    def __init__(self, database_connection, database_system_connection, connection_parameters, transaction_stack):
        self.database_connection = database_connection
        self.database_system_connection = database_system_connection
        self.connection_parameters = connection_parameters
        self.transaction_stack = transaction_stack

    def add_conection_parameter(self, key, value):
        self.connection_parameters[key] = value

    def remove_connection_parameter(self, key):
        del self.connection_parameters[key]

    def get_connection_parameter(self, key):
        if key in self.connection_parameters:
            return self.connection_parameters[key]
