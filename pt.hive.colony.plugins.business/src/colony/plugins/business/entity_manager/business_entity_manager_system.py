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

__revision__ = "$LastChangedRevision: 2102 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 14:47:02 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import thread

import business_entity_manager_exceptions

ATTRIBUTE_EXCLUSION_LIST = ["__doc__", "__init__", "__module__", "mapping_options"]

TYPE_EXCLUSION_LIST = [types.MethodType, types.FunctionType, types.ClassType]

RELATION_DATA_TYPE = "relation"

DATA_TYPE_FIELD = "data_type"

class BusinessEntityManager:
    """
    The business entity manager class
    """

    business_entity_manager_plugin = None
    """ The business entity manager plugin """

    entity_manager_engine_plugins_list = []
    """ The list of entity manager engine plugins """

    loaded_entity_classes_list = []
    """ The list of loaded entity classes """

    loaded_entity_classes_map = {}
    """ The map associating the loaded entity classes with their names """

    def __init__(self, business_entity_manager_plugin):
        """
        Constructor of the class
        
        @type business_entity_manager_plugin: BusinessEntityManagerPlugin
        @param business_entity_manager_plugin: The business entity manager plugin
        """

        self.business_entity_manager_plugin = business_entity_manager_plugin

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

    def load_entity_manager(self, engine_name):
        for entity_manager_engine_plugin in self.entity_manager_engine_plugins_list:
            entity_manager_engine_name = entity_manager_engine_plugin.get_engine_name()

            if entity_manager_engine_name == engine_name:
                entity_manager = EntityManager(entity_manager_engine_plugin, self.loaded_entity_classes_list, self.loaded_entity_classes_map)
                return entity_manager

        raise business_entity_manager_exceptions.EntityManagerEngineNotFound("engine " + engine_name + " not available")

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

    transaction_stack_thread_id_map = {}
    """ The map containing the stack containing the pending transactions for the thread id """

    connection_parameters = {}
    """ The map containing the connection parameters """

    def __init__(self, entity_manager_engine_plugin, entity_classes_list, loaded_entity_classes_map = None):
        self.entity_manager_engine_plugin = entity_manager_engine_plugin
        self.entity_classes_list = entity_classes_list
        self.entity_classes_map = loaded_entity_classes_map

        self.connection_thread_id_map = {}
        self.database_connection_thread_id_map = {}
        self.transaction_stack_thread_id_map = {}

        self.connection_parameters = {}

    def get_connection(self):
        """
        Retrieves the current available connection
        
        @rtype: Connection
        @return: The current available database connection
        """

        # gets the id of the current thread
        current_thread_id = thread.get_ident()

        # in case there is no connection available for the current thread
        if not current_thread_id in self.connection_thread_id_map:
            # retrieves the database connection
            database_connection = self.get_database_connection()

            # retrieves the transaction stack
            transaction_stack = self.get_transaction_stack()

            # creates the connection object with the specified database connection, the specified connection parameters and the specified transaction stack
            connection = Connection(database_connection, self.connection_parameters, transaction_stack)

            # sets the current thread connection
            self.connection_thread_id_map[current_thread_id] = connection

        # returns the current thread connection
        return self.connection_thread_id_map[current_thread_id]

    def get_database_connection(self):
        """
        Retrieves the current available database connection
        
        @rtype: Connection
        @return: The current available database connection
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

    def get_transaction_stack(self):
        """
        Retrieves the current available transaction stack
        
        @rtype: List
        @return: The current available transaction stack
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
        self.connection_parameters = connection_parameters

    def load_entity_manager(self):
        self.register_classes()

    def register_classes(self):
        # retrieves the connection object
        connection = self.get_connection()

        for entity_class in self.entity_classes_list:
            if self.entity_manager_engine_plugin.exists_entity_definition(connection, entity_class):
                if not self.entity_manager_engine_plugin.synced_entity_definition(connection, entity_class):
                    pass
                    # @todo not synched needs to be updated
            else:
                self.entity_manager_engine_plugin.create_entity_definition(connection, entity_class)

    def get_entity_class(self, entity_class_name):
        if entity_class_name in self.entity_classes_map:
            return self.entity_classes_map[entity_class_name]

    def create_transaction(self, transaction_name = None):
        """
        Creates a new transaction in the entity manager
        wth the given transaction name
        
        @type transaction_name: String
        @param transaction_name: The name of the transaction
        @rtype: bool
        @return: The result of transaction creation
        """

        # retrieves the connection object
        connection = self.get_connection()

        if self.entity_manager_engine_plugin.create_transaction(connection, transaction_name):
            # retrieves the transaction stack
            transaction_stack = self.get_transaction_stack()

            transaction_stack.append(transaction_name)

            return True

    def commit_transaction(self, transaction_name = None):
        """
        Commits the transaction with the given transaction name,
        or the current available transaction if no name is specified
        
        @type transaction_name: String
        @param transaction_name: The name of the transaction to the "commited"
        @rtype: bool
        @return: The result of transaction commit
        """

        # retrieves the transaction stack
        transaction_stack = self.get_transaction_stack()

        # in case the transaction stack is empty
        if not transaction_stack:
            return False

        # retrieves the connection object
        connection = self.get_connection()

        if self.entity_manager_engine_plugin.commit_transaction(connection, transaction_name):
            transaction_stack.pop()

            return True

    def rollback_transaction(self, transaction_name = None):
        """
        "Rollsback" the transaction with the given transaction name,
        or the current available transaction if no name is specified
        
        @type transaction_name: String
        @param transaction_name: The name of the transaction to the "rolledback"
        @rtype: bool
        @return: The result of transaction rollback
        """

        # retrieves the transaction stack
        transaction_stack = self.get_transaction_stack()

        # in case the transaction stack is empty
        if not transaction_stack:
            return False

        # retrieves the connection object
        connection = self.get_connection()

        if self.entity_manager_engine_plugin.rollback_transaction(connection, transaction_name):
            del transaction_stack[:]

            return True

    def commit(self):
        # retrieves the connection object
        connection = self.get_connection()

        # commits the current cached data
        return self.entity_manager_engine_plugin.commit_connection(connection)

    def rollback(self):
        # retrieves the connection object
        connection = self.get_connection()

        # "rollsback" the current cached data
        return self.entity_manager_engine_plugin.rollback_connection(connection)

    def save(self, entity):
        # retrieves the connection object
        connection = self.get_connection()

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case there is already an entry with the same key value
        if self.entity_manager_engine_plugin.find_entity(connection, entity_class, entity_id_attribute_value):
            raise business_entity_manager_exceptions.EntityManagerEngineDuplicateEntry("the key value " + str(entity_id_attribute_value) + " already exists in the database")

        # persists the entity
        return self.entity_manager_engine_plugin.save_entity(connection, entity)

    def remove(self, entity):
        """
        Removes an entity from the database
        
        @type entity: Object
        @param entity: The entity to be removed from the database
        @rtype: bool
        @return: The result of the removal 
        """
        
        # retrieves the connection object
        connection = self.get_connection()

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case there is no entry with the same key value
        if not self.entity_manager_engine_plugin.find_entity(connection, entity_class, entity_id_attribute_value):
            raise business_entity_manager_exceptions.EntityManagerEngineEntryNotFound("the key value " + str(entity_id_attribute_value) + " was not found in the database")

        # removes the entity
        return self.entity_manager_engine_plugin.remove_entity(connection, entity)

    def find(self, entity_class, id_value):
        # retrieves the connection object
        connection = self.get_connection()

        # finds the entity
        return self.entity_manager_engine_plugin.find_entity(connection, entity_class, id_value)

    def get_entity_class_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all attributes from the given entity class
        
        @type entity_class: Class
        @param entity_class: The entity class
        @rtype: List
        @return: The list with the names of all attributes from the given entity class
        """

        # retrieves all the class attribute names
        entity_class_attribute_names = dir(entity_class)

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = [attribute_name for attribute_name in entity_class_attribute_names if not attribute_name in ATTRIBUTE_EXCLUSION_LIST and not type(getattr(entity_class, attribute_name)) in TYPE_EXCLUSION_LIST]

        return entity_class_valid_attribute_names

    def get_entity_class_non_relation_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all the non relational attributes from the given entity class
        
        @type entity_class: Class
        @param entity_class: The entity class
        @rtype: List
        @return: The list with the names of all the non relational attributes from the given entity class
        """

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the non relation attribute names
        entity_class_non_relation_attribute_names = [attribute_name for attribute_name in entity_class_valid_attribute_names if not attribute_name[DATA_TYPE_FIELD] == RELATION_DATA_TYPE]

        return entity_class_non_relation_attribute_names

    def get_entity_class_attribute_values(self, entity_class):
        """
        Retrieves a list with the values of all attributes from the given entity class
        
        @type entity_class: Class
        @param entity_class: The entity class
        @rtype: List
        @return: The list with the values of all attributes from the given entity class
        """

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = [getattr(entity_class, attribute_name) for attribute_name in entity_class_valid_attribute_names]

        return entity_class_valid_attribute_values

    def get_entity_id_attribute_value(self, entity):
        """
        Retrieves the value of the entity id attribute
        
        @type entity: Entity
        @param entity: The entity to retrieve the id attribute value
        @rtype: Object
        @return: The value of the entity id attribute
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
        Retrieves the value of the entity class id attribute
        
        @type entity: Class
        @param entity: The entity class to retrieve the id attribute value
        @rtype: Object
        @return: The value of the entity class id attribute
        """

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

        # retrieves the entity class id attribute value
        entity_class_id_attribute_value = getattr(entity_class, entity_class_id_attribute_name)

        return entity_class_id_attribute_value

    def get_entity_class_id_attribute_name(self, entity_class):
        """
        Retrieves the name of the entity class id attribute
        
        @type entity: Class
        @param entity: The entity class to retrieve the id attribute name
        @rtype: String
        @return: The name of the entity class id attribute
        """

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # creates the initial index value
        index = 0

        for entity_class_valid_attribute_value in entity_class_valid_attribute_values:
            if "id" in entity_class_valid_attribute_value:
                if entity_class_valid_attribute_value["id"]:
                    return entity_class_valid_attribute_names[index]

            # increments the index value
            index += 1

class Connection:
    """
    The class representing a database connection
    with the associated attributes
    """

    database_connection = None
    """ The database connection object """

    connection_parameters = []
    """ The connection parameters for the connection """

    transaction_stack = []
    """ The transaction stack for the connection """

    def __init__(self, database_connection, connection_parameters, transaction_stack):
        self.database_connection = database_connection
        self.connection_parameters = connection_parameters
        self.transaction_stack = transaction_stack

    def add_conection_parameter(self, key, value):
        self.connection_parameters[key] = value

    def remove_connection_parameter(self, key):
        del self.connection_parameters[key]

    def get_connection_parameter(self, key):
        if key in self.connection_parameters:
            return self.connection_parameters[key]
