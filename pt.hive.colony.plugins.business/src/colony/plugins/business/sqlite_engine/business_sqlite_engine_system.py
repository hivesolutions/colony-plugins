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

import time
import types
import sqlite3

import business_sqlite_engine_exceptions

ENGINE_NAME = "sqlite"
""" The engine name """

DATA_TYPE_MAP = {"text" : "text",
                 "numeric" : "numeric",
                 "relation" : "relation"}
""" The data type map """

FILE_PATH_VALUE = "file_path"
""" The file path value """

AUTOCOMMIT_VALUE = "autocommit"
""" The autocommit value """

ISOLATION_LEVEL_VALUE = "isolation_level"
""" The isolation level value """

ATTRIBUTE_EXCLUSION_LIST = ["__class__", "__delattr__", "__dict__", "__doc__", "__getattribute__", "__hash__", "__module__", "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__str__", "__weakref__", "mapping_options"]
""" The attribute exclusion list """

TYPE_EXCLUSION_LIST = [types.MethodType, types.FunctionType, types.ClassType]
""" The type exclusion list """

RELATION_DATA_TYPE = "relation"
""" The relation data type """

ID_FIELD = "id"
""" The id field """

DATA_TYPE_FIELD = "data_type"
""" The data type field """

GENERATED_FIELD = "generated"
""" The generated field """

GENERATOR_TYPE_FIELD = "generator_type"
""" The generator type field """

RELATION_ATTRIBUTES_METHOD_FIELD = "relation_attributes_method"
""" The relation attributes method field """

RELATION_TYPE_FIELD = "relation_type"
""" The relation type field """

TARGET_ENTITY_FIELD = "target_entity"
""" The target entity field """

TARGET_ENTITY_NAME_FIELD = "target_entity_name"
""" The target entity name field """

JOIN_ATTRIBUTE_FIELD = "join_attribute"
""" The join attribute field """

JOIN_ATTRIBUTE_NAME_FIELD = "join_attribute_name"
""" The join attribute name field """

ATTRIBUTE_COLUMN_NAME_FIELD = "attribute_column_name"
""" The attribute column name field """

JOIN_ATTRIBUTE_COLUMN_NAME_FIELD = "join_attribute_column_name"
""" The join attribute column name field """

MAPPED_BY_FIELD = "mapped_by"
""" The mapped by field """

JOIN_TABLE_FIELD = "join_table"
""" The join table field """

OPTIONAL_FIELD = "optional"
""" The optional field """

DEFAULT_OPTIONAL_FIELD_VALUE = True
""" The default optional field value """

RELATION_ATTRIBUTES_METHOD_PREFIX = "get_relation_attributes_"
""" The relation attributes method prefix """

ONE_TO_ONE_RELATION = "one-to-one"
""" The one to one relation """

ONE_TO_MANY_RELATION = "one-to-many"
""" The one to many relation """

MANY_TO_ONE_RELATION = "many-to-one"
""" The many to one relation """

MANY_TO_MANY_RELATION = "many-to-many"
""" The many to many relation """

class BusinessSqliteEngine:
    """
    The business sqlite engine class.
    """

    business_sqlite_engine_plugin = None
    """ The business sqlite engine plugin """

    def __init__(self, business_sqlite_engine_plugin):
        """
        Constructor of the class
        
        @type business_sqlite_engine_plugin: BusinessSqliteEnginePlugin
        @param business_sqlite_engine_plugin: The business sqlite engine plugin.
        """

        self.business_sqlite_engine_plugin = business_sqlite_engine_plugin

    def get_engine_name(self):
        """
        Retrieves the name of the engine.
        
        @rtype: String
        @return: The name of the engine.
        """

        return ENGINE_NAME

    def create_connection(self, connection_parameters):
        """
        Creates the connection using the given connection parameters.
        
        @type connection_parameters: List
        @param connection_parameters: The connection parameters.
        @rtype: Connection
        @return: The created connection.
        """

        # in case the file path is not defined
        if not FILE_PATH_VALUE in connection_parameters:
            raise business_sqlite_engine_exceptions.MissingProperty(FILE_PATH_VALUE)

        # retrieves the file path parameter value
        file_path = connection_parameters[FILE_PATH_VALUE]

        # sets the isolation level value as deferred
        isolation_level_value = "DEFERRED"

        if AUTOCOMMIT_VALUE in connection_parameters:
            # retrieves the autocommit parameter value
            autocommit_value = connection_parameters[AUTOCOMMIT_VALUE]

            if autocommit_value:
                isolation_level_value = None

        if ISOLATION_LEVEL_VALUE in connection_parameters:
            isolation_level_value = connection_parameters[ISOLATION_LEVEL_VALUE]

        # creates the sqlite database connection
        connection = sqlite3.connect(file_path, isolation_level = isolation_level_value)

        return connection

    def commit_connection(self, connection):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # commits the changes to the connection
        database_connection.commit()

        return True

    def rollback_connection(self, connection):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # "rollsback" the changes to the connection
        database_connection.rollback()

        return True

    def create_transaction(self, connection, transaction_name):
        return True

    def commit_transaction(self, connection, transaction_name):
        # retrieves the transaction stack from the connection object
        transaction_stack = connection.transaction_stack

        # in case there is only one element in the transaction stack
        if len(transaction_stack) == 1:
            return self.commit_connection(connection)

        return True

    def rollback_transaction(self, connection, transaction_name):
        # "rollsback" the transaction        
        return self.rollback_connection(connection)

    def exists_entity_definition(self, connection, entity_class):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # selects all the names of existing tables
        self.execute_query(cursor, "select name from SQLite_Master")

        # selects the table names from the cursor
        table_names_list = [value[0] for value in cursor]

        # closes the cursor
        cursor.close()

        # in case the entity class name exists in the tables names list
        if entity_class_name in table_names_list:
            return True
        else:
            return False

    def exists_table_definition(self, connection, table_name):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # selects all the names of existing tables
        self.execute_query(cursor, "select name from SQLite_Master")

        # selects the table names from the cursor
        table_names_list = [value[0] for value in cursor]

        # closes the cursor
        cursor.close()

        # in case the table name exists in the tables names list
        if table_name in table_names_list:
            return True
        else:
            return False

    def exists_table_column_definition(self, connection, table_name, column_name):
        if not self.exists_table_definition(connection, table_name):
            return False

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # creates the initial query string value
        query_string_value = "pragma table_info(" + table_name + ")"

        # executes the query retrieving the values
        self.execute_query(cursor, query_string_value)

        # selects the table information from the cursor
        table_information_list = [value for value in cursor]

        # iterates over all the table information
        for table_information_item in table_information_list:
            # retrieves the attribute name
            attribute_name = table_information_item[1]

            # in case the attribute name is the same
            # as the column name
            if attribute_name == column_name:
                # closes the cursor
                cursor.close()

                return True

        # closes the cursor
        cursor.close()

        return False

    def synced_entity_definition(self, connection, entity_class):
        """
        Checks if an entity definition is synchronized with the correspondent database information.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity_class: Class
        @param entity_class: The entity class to be checked.
        @rtype: bool
        @return: The result of the check.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # retrieves the number of attributes in the entity class
        entity_class_valid_attributes_size = len(entity_class_valid_attribute_names)

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # creates the initial query string value
        query_string_value = "pragma table_info(" + entity_class_name + ")"

        # executes the query retrieving the values
        self.execute_query(cursor, query_string_value)

        # selects the table information from the cursor
        table_information_list = [value for value in cursor]

        # creates the initial index value
        index = 0

        # retrieves the table information list size
        table_information_list_size = len(table_information_list)

        # in case the table information list size is different from the entity class
        # valid attributes size, invalid number of attributes situation
        if not table_information_list_size == entity_class_valid_attributes_size:
            # closes the cursor
            cursor.close()

            # returns false
            return False

        # iterates over all the table information
        for table_information_item in table_information_list:
            # retrieves the attribute name
            attribute_name = table_information_item[1]

            # retrieves the attribute data type
            attribute_data_type = table_information_item[2]

            # retrieves the entity class valid attribute name
            entity_class_valid_attribute_name = entity_class_valid_attribute_names[index]

            # retrieves the entity class valid attribute value
            entity_class_valid_attribute_value = entity_class_valid_attribute_values[index]

            # retrieves the entity class valid attribute data type
            entity_class_valid_attribute_data_type = entity_class_valid_attribute_value[DATA_TYPE_FIELD]

            # retrieves the entity class valid attribute target data type
            entity_class_valid_attribute_target_data_type = DATA_TYPE_MAP[entity_class_valid_attribute_data_type]

            # in case the attribute name is not the same as the entity class valid attribute name,
            # invalid attribute name situation
            if not attribute_name == entity_class_valid_attribute_name:
                # closes the cursor
                cursor.close()

                return False

            # in case the attribute data type is not the same as the entity class valid attribute target data type,
            # invalid attribute data type situation
            if not attribute_data_type == entity_class_valid_attribute_target_data_type:
                # closes the cursor
                cursor.close()

                return False

            # increments the index value
            index += 1

        # closes the cursor
        cursor.close()

        return True

    def create_entity_definition(self, connection, entity_class):
        """
        Creates the entity definition in the database from the entity class.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity_class: Class
        @param entity_class: The entity class to be used in the creation.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # creates the initial query string value
        query_string_value = "create table " + entity_class_name + "("

        # creates the initial index value
        index = 0

        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the entity class valid attribute names
        for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
            # retrieves the entity class valid attribute value
            entity_class_valid_attribute_value = entity_class_valid_attribute_values[index]

            # retrieves the entity class valid attribute data type
            entity_class_valid_attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_class_valid_attribute_name)

            # retrieves the valid sqlite data type from the formal entity data type
            entity_class_valid_attribute_target_data_type = DATA_TYPE_MAP[entity_class_valid_attribute_data_type]

            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ", "

            # extends the query string value
            query_string_value += entity_class_valid_attribute_name + " " + entity_class_valid_attribute_target_data_type

            # increments the index value
            index += 1

        # closes the query string value
        query_string_value += ")"

        # executes the query creating the table
        self.execute_query(cursor, query_string_value)

        # closes the cursor
        cursor.close()

        # creates the entity relations definition
        self.create_entity_relations_definition(connection, entity_class)

    def create_entity_relations_definition(self, connection, entity_class):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves the entity class valid indirect attribute names
        entity_class_valid_indirect_attribute_names = self.get_entity_class_indirect_attribute_names(entity_class)

        # retrieves the entity class valid indirect attribute values
        entity_class_valid_indirect_attribute_values = self.get_entity_class_indirect_attribute_values(entity_class)

        # iterates over all the entity class valid indirect attribute names
        for entity_class_valid_indirect_attribute_name in entity_class_valid_indirect_attribute_names:
            # retrieves the relation attributes for the given attribute name in the given entity class
            relation_attributes = self.get_relation_attributes(entity_class, entity_class_valid_indirect_attribute_name)

            # retrieves the relation type field
            relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

            # in case the relation is of type many-to-many
            if relation_type_field == MANY_TO_MANY_RELATION:
                # retrieves the join table field
                join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                # retrieves the attribute column name field
                attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                # retrieves the id attribute name
                id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

                # retrieves the id attribute value
                id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

                # retrieves the id attribute data type
                id_attribute_data_type = self.get_attribute_data_type(id_attribute_value, entity_class, id_attribute_name)

                # retrieves the valid sqlite data type from the formal id attribute data type
                id_attribute_target_data_type = DATA_TYPE_MAP[id_attribute_data_type]

                if self.exists_table_definition(connection, join_table_field):
                    if not self.exists_table_column_definition(connection, join_table_field, attribute_column_name_field):
                        # creates the query string value
                        query_string_value = "alter table " + join_table_field + " add column " + attribute_column_name_field + " " + id_attribute_target_data_type

                        # executes the query altering the table
                        self.execute_query(cursor, query_string_value)
                else:
                    # creates the query string value
                    query_string_value = "create table " + join_table_field + "(" + attribute_column_name_field + " " + id_attribute_target_data_type + ")"

                    # executes the query creating the table
                    self.execute_query(cursor, query_string_value)

        # closes the cursor
        cursor.close()

    def update_entity_definition(self, connection, entity_class):
        """
        Updates the entity definition in the database from the entity class.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity_class: Class
        @param entity_class: The entity class to be used in the update.
        """

        pass

    def save_entity(self, connection, entity):
        """
        Saves the given entity instance in the database, using the given connection.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity: Object
        @param entity: The entity instance to be saved.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute value
        entity_class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

        # in case the id field is to be generated
        if GENERATED_FIELD in entity_class_id_attribute_value:
            # retrieves the entity class id attribute name
            entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)
            setattr(entity, entity_class_id_attribute_name, int(time.time() % 10 * 100000000))

        # retrieves the entity id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case there is already an entry with the same key value
        if self.find_entity(connection, entity_class, entity_id_attribute_value):
            raise business_sqlite_engine_exceptions.SqliteEngineDuplicateEntry("the key value " + str(entity_id_attribute_value) + " already exists in the database")

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid attribute names, removes method values and the name exceptions
        entity_valid_attribute_names = self.get_entity_attribute_names(entity)

        # retrieves all the valid attribute values
        entity_valid_attribute_values = self.get_entity_attribute_values(entity)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # creates the initial query string value
        query_string_value = "insert into " + entity_class_name + "("

        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the entity valid attribute names
        for entity_valid_attribute_name in entity_valid_attribute_names:
            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ", "

            # extends the query string value
            query_string_value += entity_valid_attribute_name

        # extends the query string value
        query_string_value += ") values("

        # creates the initial index value
        index = 0

        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the valid attribute values
        for entity_valid_attribute_value in entity_valid_attribute_values:
            # retrieves the current entity class valid attribute value
            entity_class_valid_attribute_value = entity_class_valid_attribute_values[index]

            # retrieves the entity valid attribute name
            entity_valid_attribute_name = entity_valid_attribute_names[index]

            # retrieves the entity class valid attribute value data type
            entity_class_valid_attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_valid_attribute_name)

            # in case the attribute is of type relation
            if self.is_attribute_relation(entity_class_valid_attribute_value):
                entity_valid_attribute_value = self.get_relation_attribute_value(entity_valid_attribute_value, entity_class_valid_attribute_value, entity_class, entity_valid_attribute_name)

            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ", "

            # in case the value is None a null is added
            if entity_valid_attribute_value == None:
                query_string_value += "null"
            else:
                if entity_class_valid_attribute_data_type == "text":
                    # extends the query string value
                    query_string_value += "'" + entity_valid_attribute_value + "'"
                else:
                    # extends the query string value
                    query_string_value += str(entity_valid_attribute_value)

            # increments the index value
            index += 1

        # closes the query string value
        query_string_value += ")"

        # executes the query inserting the values
        self.execute_query(cursor, query_string_value)

        # closes the cursor
        cursor.close()

        # saves the entity indirect relations
        self.save_entity_indirect_relations(connection, entity)

    def save_entity_indirect_relations(self, connection, entity):
        """
        Saves the indirect relations for the given entity instance in the database,
        using the given connection.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity: Object
        @param entity: The entity instance with the indirect relations to be saved.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves all the valid indirect attribute names, removes method values and the name exceptions
        entity_valid_indirect_attribute_names = self.get_entity_indirect_attribute_names(entity)

        # retrieves all the valid attribute values
        entity_valid_indirect_attribute_values = self.get_entity_indirect_attribute_values(entity)

        # retrieves all the class valid attribute values
        entity_class_valid_indirect_attribute_values = self.get_entity_class_indirect_attribute_values(entity_class)

        # creates the initial index value
        index = 0

        # iterates over all the entity valid indirect attribute names
        for entity_valid_indirect_attribute_name in entity_valid_indirect_attribute_names:
            # retrieves the entity valid indirect attribute value
            entity_valid_indirect_attribute_value = entity_valid_indirect_attribute_values[index]

            # retrieves the entity class valid indirect attribute value
            entity_class_valid_indirect_attribute_value = entity_class_valid_indirect_attribute_values[index]

            # retrieves the relation attributes for the given attribute name in the given entity class
            relation_attributes = self.get_relation_attributes(entity_class, entity_valid_indirect_attribute_name)

            # retrieves the relation type field
            relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

            # in case the relation is of type one-to-many or one-to-one with an entity valid indirect attribute value
            if relation_type_field == ONE_TO_MANY_RELATION or (relation_type_field == ONE_TO_ONE_RELATION and entity_valid_indirect_attribute_value):
                if relation_type_field == ONE_TO_ONE_RELATION:
                    entity_valid_indirect_attribute_value = [entity_valid_indirect_attribute_value]

                # retrieves the target entity field
                target_entity_field = relation_attributes[TARGET_ENTITY_FIELD]

                # retrieves the target entity name field
                target_entity_name_field = relation_attributes[TARGET_ENTITY_NAME_FIELD]

                # retrieves the join attribute name field
                join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                # retrieves the id attribute value
                id_attribute_value = self.get_entity_id_attribute_value(entity)

                # retrieves the target entity id attribute name
                target_entity_id_attribute_name = self.get_entity_class_id_attribute_name(target_entity_field)

                # iterates over all the objects in the entity valid indirect attribute value (list)
                for object_value in entity_valid_indirect_attribute_value:
                    # retrieves the target entity id attribute value
                    target_entity_id_attribute_value = self.get_entity_id_attribute_value(object_value)

                    # creates the initial query string value
                    query_string_value = "update " + target_entity_name_field + " set " + join_attribute_name_field + " = "

                    if type(id_attribute_value) in types.StringTypes:
                        query_string_value += "'" + id_attribute_value + "'"
                    else:
                        query_string_value += str(id_attribute_value)

                    query_string_value += " where " + target_entity_id_attribute_name + " = "

                    if type(target_entity_id_attribute_value) in types.StringTypes:
                        query_string_value += "'" + target_entity_id_attribute_value + "'"
                    else:
                        query_string_value += str(target_entity_id_attribute_value)

                    # executes the query updating the values
                    self.execute_query(cursor, query_string_value)

            # in case the relation is of type many-to-many
            elif relation_type_field == MANY_TO_MANY_RELATION:
                # retrieves the join table field
                join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                # retrieves the target entity field
                target_entity_field = relation_attributes[TARGET_ENTITY_FIELD]

                # retrieves the target entity name field
                target_entity_name_field = relation_attributes[TARGET_ENTITY_NAME_FIELD]

                # retrieves the join attribute field
                join_attribute_field = relation_attributes[JOIN_ATTRIBUTE_FIELD]

                # retrieves the join attribute name field
                join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                # retrieves the join attribute column name field
                join_attribute_column_name_field = relation_attributes[JOIN_ATTRIBUTE_COLUMN_NAME_FIELD]

                # retrieves the attribute column name field
                attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                # retrieves the target attribute value data type
                target_attribute_value_data_type = self.get_attribute_data_type(join_attribute_field, target_entity_field, join_attribute_name_field)

                # retrieves the id attribute name
                id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

                # retrieves the id attribute value
                id_attribute_value = self.get_entity_id_attribute_value(entity)

                # retrieves the class id attribute value
                class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

                # retrieves the id attribute value data type
                id_attribute_value_data_type = self.get_attribute_data_type(class_id_attribute_value, entity_class, id_attribute_name)

                # iterates over all the objects in the entity valid indirect attribute value (list)
                for object_value in entity_valid_indirect_attribute_value:
                    # retrieves the target attribute value
                    target_attribute_value = getattr(object_value, join_attribute_name_field)

                    # creates the initial query string value
                    query_string_value = "insert into " + join_table_field + "(" + attribute_column_name_field + ", " +\
                                         join_attribute_column_name_field + ") values("

                    if id_attribute_value_data_type == "text":
                        # extends the query string value
                        query_string_value += "'" + id_attribute_value + "', "
                    else:
                        # extends the query string value
                        query_string_value += str(id_attribute_value) + ", "

                    if target_attribute_value_data_type == "text":
                        # extends the query string value
                        query_string_value += "'" + target_attribute_value + "')"
                    else:
                        # extends the query string value
                        query_string_value += str(target_attribute_value) + ")"

                    # executes the query inserting the values
                    self.execute_query(cursor, query_string_value)

            # increments the index value
            index += 1

        # closes the cursor
        cursor.close()

    def remove_entity(self, connection, entity):
        """
        Removes the given entity instance from the database, using the given connection.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity: Object
        @param entity: The entity instance to be removed.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case there is no entry with the same key value
        if not self.find_entity(connection, entity_class, entity_id_attribute_value):
            raise business_sqlite_engine_exceptions.SqliteEngineEntryNotFound("the key value " + str(entity_id_attribute_value) + " was not found in the database")

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

        # creates the initial query string value
        query_string_value = "delete from " + entity_class_name + " where " + entity_class_id_attribute_name + " = "

        if type(entity_id_attribute_value) in types.StringTypes:
            query_string_value += "'" + entity_id_attribute_value + "'"
        else:
            query_string_value += str(entity_id_attribute_value)

        # executes the query removing the values
        self.execute_query(cursor, query_string_value)

        # closes the cursor
        cursor.close()

        # removes entity indirect relations
        self.remove_entity_indirect_relations(connection, entity)

    def remove_entity_indirect_relations(self, connection, entity):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves all the valid indirect attribute names, removes method values and the name exceptions
        entity_valid_indirect_attribute_names = self.get_entity_indirect_attribute_names(entity)

        # iterates over all the entity valid indirect attribute names
        for entity_valid_indirect_attribute_name in entity_valid_indirect_attribute_names:
            # retrieves the relation attributes for the given attribute name in the given entity class
            relation_attributes = self.get_relation_attributes(entity_class, entity_valid_indirect_attribute_name)

            # retrieves the relation type field
            relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

            # in case the relation is of type many-to-many
            if relation_type_field == MANY_TO_MANY_RELATION:
                # retrieves the join table field
                join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                # retrieves the attribute column name field
                attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                # retrieves the id attribute value
                id_attribute_value = self.get_entity_id_attribute_value(entity)

                # creates the initial query string value
                query_string_value = "delete from " + join_table_field + " where " + attribute_column_name_field + " = "

                if type(id_attribute_value) in types.StringTypes:
                    query_string_value += "'" + id_attribute_value + "'"
                else:
                    query_string_value += str(id_attribute_value)

                # executes the query removing the values
                self.execute_query(cursor, query_string_value)

        # closes the cursor
        cursor.close()

    def find_entity(self, connection, entity_class, id_value, search_field_name = None, retrieved_entities_list = None):
        """
        Retrieves an entity instance of the declared class type with the given id, using the given connection.
        The search field name is used to find an entity with a value different than the id field.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity_class: Class
        @param entity_class: The entity class of the entity to retrieve.
        @type id_value: Object
        @param id_value: The id of the entity to retrieve.
        @type search_field_name: String
        @param search_field_name: The name of the field to be used in the search.
        @type retrieved_entities_list: BufferedEntities
        @param retrieved_entities_list: The already retrieved entities.
        @rtype: Object
        @return: The retrieved entity instance.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

        # in case the retrieved entities object is not started
        if not retrieved_entities_list:
            # creates a retrieved entities object
            retrieved_entities_list = BufferedEntities()

        # in case the search field is valid
        if search_field_name:
            # the id attribute name is changed to the search field name
            entity_class_id_attribute_name = search_field_name
        else:
            # retrieves the already buffered entity
            buffered_entity = retrieved_entities_list.get_entity(entity_class, id_value)

            # in case the entity is already buffered
            if buffered_entity:
                # returns the buffered entity
                return buffered_entity

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # creates the initial query string value
        query_string_value = "select "

        # the first flag to control the first field to be processed
        is_first = True

        for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ", "

            query_string_value += entity_class_valid_attribute_name

        query_string_value += " from " + entity_class_name + " where " + entity_class_id_attribute_name + " = "

        if type(id_value) in types.StringTypes:
            query_string_value += "'" + id_value + "'"
        else:
            query_string_value += str(id_value)

        # executes the query retrieving the values
        self.execute_query(cursor, query_string_value)

        # selects the values from the cursor
        values_list = [value for value in cursor]

        # in case there is at least one selection
        if len(values_list):
            # creates a new entity instance
            entity = entity_class()

            # retrieves the first value from the values list
            first_value = values_list[0]

            # creates the initial index value
            index = 0

            # creates the relation attributes list
            # this list is used for relation attributes post-processing
            relation_attributes_list = []

            # iterates over all the attribute values of the first value
            for attribute_value in first_value:
                # retrieves the entity class attribute name
                entity_class_valid_attribute_name = entity_class_valid_attribute_names[index]

                # in case the attribute is a relation
                if self.is_attribute_name_relation(entity_class_valid_attribute_name, entity_class):
                    # creates the relation attribute tuple
                    relation_attribute_tuple = (entity_class_valid_attribute_name, attribute_value)

                    # adds the relation attribute tuple to the list of relation attributes
                    relation_attributes_list.append(relation_attribute_tuple)
                else:
                    # sets the attribute in the instance
                    setattr(entity, entity_class_valid_attribute_name, attribute_value)

                # increments the index value
                index += 1

            # retrieves the id attribute value
            id_attribute_value = self.get_entity_id_attribute_value(entity)

            # retrieves the already buffered entity
            buffered_entity = retrieved_entities_list.get_entity(entity_class, id_attribute_value)

            # in case the entity is already buffered
            if buffered_entity:
                # closes the cursor
                cursor.close()

                # returns the buffered entity
                return buffered_entity
            else:
                # adds the entity to the list of retrieved entities
                retrieved_entities_list.add_entity(id_attribute_value, entity)

                # iterates over all the relation attributes list
                for entity_class_valid_attribute_name, attribute_value in relation_attributes_list:
                    # retrieves the relation attribute value
                    relation_attribute_value = self.get_relation_value(connection, entity_class_valid_attribute_name, entity_class, attribute_value, id_value, retrieved_entities_list)

                    # sets the relation attribute in the instance
                    setattr(entity, entity_class_valid_attribute_name, relation_attribute_value)

                # closes the cursor
                cursor.close()

            # retrieves all the valid indirect attribute names, removes method values and the name exceptions
            entity_valid_indirect_attribute_names = self.get_entity_indirect_attribute_names(entity)

            # iterates over all the entity valid indirect attribute names
            for entity_valid_indirect_attribute_name in entity_valid_indirect_attribute_names:
                # retrieves the relation attributes for the given attribute name in the given entity class
                relation_attributes = self.get_relation_attributes(entity_class, entity_valid_indirect_attribute_name)

                # retrieves the relation type field
                relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

                # in case the relation is of type many-to-many
                if relation_type_field == MANY_TO_MANY_RELATION:
                    # retrieves the join table field
                    join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                    # retrieves the target entity field
                    target_entity_field = relation_attributes[TARGET_ENTITY_FIELD]

                    # retrieves the target entity name field
                    target_entity_name_field = relation_attributes[TARGET_ENTITY_NAME_FIELD]

                    # retrieves the join attribute column name field
                    join_attribute_column_name_field = relation_attributes[JOIN_ATTRIBUTE_COLUMN_NAME_FIELD]

                    # retrieves the attribute column name field
                    attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                    # retrieves the id attribute value
                    id_attribute_value = self.get_entity_id_attribute_value(entity)

                    # creates the initial query string value
                    query_string_value = "select " + join_attribute_column_name_field + " from " + join_table_field + " where " + attribute_column_name_field + " = "

                    if type(id_attribute_value) in types.StringTypes:
                        query_string_value += "'" + id_attribute_value + "'"
                    else:
                        query_string_value += str(id_attribute_value)

                    # executes the query removing the values
                    self.execute_query(cursor, query_string_value)

                    # selects the values from the cursor
                    values_list = [value for value in cursor]

                    # creates the target entities list
                    target_entities_list = []

                    # iterates over the values list
                    for value in values_list:
                        # retrieves the target attribute value
                        target_attribute_value = value[0]

                        # retrieves the target entity
                        target_entity = self.find_entity(connection, target_entity_field, target_attribute_value, retrieved_entities_list = retrieved_entities_list)

                        # appends the target entity to the list of target entities
                        target_entities_list.append(target_entity)

                    # sets the relation attribute in the instance
                    setattr(entity, entity_valid_indirect_attribute_name, target_entities_list)

            # returns the created entity
            return entity

        # closes the cursor
        cursor.close()

    def find_all_entities(self, connection, entity_class, field_value, search_field_name, retrieved_entities_list = None):
        """
        Retrieves all entity instances of the declared class type with the given value, using the given connection.
        The search field name is used to find an entity with a value of the given field.
        
        @type connection: Connection
        @param connection: The database connection to use.
        @type entity_class: Class
        @param entity_class: The entity class of the entity to retrieve.
        @type field_value: Object
        @param field_value: The field value of the entity to retrieve.
        @type search_field_name: String
        @param search_field_name: The name of the field to be used in the search.
        @type retrieved_entities_list: BufferedEntities
        @param retrieved_entities_list: The already retrieved entities.
        @rtype: Object
        @return: The retrieved entity instances.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = search_field_name

        # in case the retrieved entities object is not started
        if not retrieved_entities_list:
            # creates a retrieved entities object
            retrieved_entities_list = BufferedEntities()

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        # creates the initial query string value
        query_string_value = "select "

        # the first flag to control the first field to be processed
        is_first = True

        for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ", "

            query_string_value += entity_class_valid_attribute_name

        if field_value == None:
            query_string_value += " from " + entity_class_name
        else:
            query_string_value += " from " + entity_class_name + " where " + entity_class_id_attribute_name + " = "

            if type(field_value) in types.StringTypes:
                query_string_value += "'" + field_value + "'"
            else:
                query_string_value += str(field_value)

        # executes the query retrieving the values
        self.execute_query(cursor, query_string_value)

        # selects the values from the cursor
        values_list = [value for value in cursor]

        # creates the list of entities
        entities_list = []

        # iterates over all the values in the values list
        for value in values_list:
            # creates a new entity instance
            entity = entity_class()

            # retrieves the id attribute value
            id_attribute_value = self.get_entity_id_attribute_value(entity)

            # adds the entity to the list of retrieved entities
            retrieved_entities_list.add_entity(id_attribute_value, entity)

            # creates the initial index value
            index = 0

            # creates the relation attributes list
            # this list is used for relation attributes post-processing
            relation_attributes_list = []

            # iterates over all the attribute values of the value
            for attribute_value in value:
                # retrieves the entity class attribute name
                entity_class_valid_attribute_name = entity_class_valid_attribute_names[index]

                # in case the attribute is a relation
                if self.is_attribute_name_relation(entity_class_valid_attribute_name, entity_class):
                    # creates the relation attribute tuple
                    relation_attribute_tuple = (entity_class_valid_attribute_name, attribute_value)

                    # adds the relation attribute tuple to the list of relation attributes
                    relation_attributes_list.append(relation_attribute_tuple)
                else:
                    # sets the attribute in the instance
                    setattr(entity, entity_class_valid_attribute_name, attribute_value)

                # increments the index value
                index += 1

            # retrieves the id attribute value
            id_attribute_value = self.get_entity_id_attribute_value(entity)

            # retrieves the already buffered entity
            buffered_entity = retrieved_entities_list.get_entity(entity_class, id_attribute_value)

            # in case the entity is already buffered
            if buffered_entity:
                # closes the cursor
                cursor.close()

                # sets the entity as the buffered entity
                entity = buffered_entity
            else:
                # adds the entity to the list of retrieved entities
                retrieved_entities_list.add_entity(id_attribute_value, entity)

                # iterates over all the relation attributes list
                for entity_class_valid_attribute_name, attribute_value in relation_attributes_list:
                    # retrieves the relation attribute value
                    relation_attribute_value = self.get_relation_value(connection, entity_class_valid_attribute_name, entity_class, attribute_value, id_attribute_value, retrieved_entities_list)

                    # sets the relation attribute in the instance
                    setattr(entity, entity_class_valid_attribute_name, relation_attribute_value)

            # adds the entity to the list of entities
            entities_list.append(entity)

        # closes the cursor
        cursor.close()

        return entities_list

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

        # retrieves all the valid class attribute names, removes method values, the name exceptions and the indirect attributes
        entity_class_valid_attribute_names = [attribute_name for attribute_name in entity_class_attribute_names if not attribute_name in ATTRIBUTE_EXCLUSION_LIST and not type(getattr(entity_class, attribute_name)) in TYPE_EXCLUSION_LIST and not self.is_attribute_name_table_joined_relation(attribute_name, entity_class)]

        return entity_class_valid_attribute_names

    def get_entity_class_indirect_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all indirect attributes from the given entity class.
        
        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the names of all the indirect attributes from the given entity class.
        """

        # retrieves all the class attribute names
        entity_class_attribute_names = dir(entity_class)

        # retrieves all the valid class indirect attribute names, removes method values and the name exceptions and the non indirect attributes
        entity_class_valid_indirect_attribute_names = [attribute_name for attribute_name in entity_class_attribute_names if not attribute_name in ATTRIBUTE_EXCLUSION_LIST and not type(getattr(entity_class, attribute_name)) in TYPE_EXCLUSION_LIST and self.is_attribute_name_indirect_relation(attribute_name, entity_class)]

        return entity_class_valid_indirect_attribute_names

    def get_entity_attribute_names(self, entity):
        """
        Retrieves a list with the names of all attributes from the given entity instance.
        
        @type entity: Object
        @param entity: The entity instance.
        @rtype: List
        @return: The list with the names of all attributes from the given entity instance.
        """

        # retrieves the entity class
        entity_class = entity.__class__

        return self.get_entity_class_attribute_names(entity_class)

    def get_entity_indirect_attribute_names(self, entity):
        """
        Retrieves a list with the names of all indirect attributes from the given entity instance.
        
        @type entity: Object
        @param entity: The entity instance.
        @rtype: List
        @return: The list with the names of all indirect attributes from the given entity instance.
        """

        # retrieves the entity class
        entity_class = entity.__class__

        return self.get_entity_class_indirect_attribute_names(entity_class)

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
        entity_class_non_relation_attribute_names = [attribute_name for attribute_name in entity_class_valid_attribute_names if not attribute_name[DATA_TYPE_FIELD] == RELATION_DATA_TYPE]

        return entity_class_non_relation_attribute_names

    def get_entity_non_relation_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all the non relational attributes from the given entity instance.
        
        @type entity_class: Object
        @param entity_class: The entity instance.
        @rtype: List
        @return: The list with the names of all the non relational attributes from the given entity instance.
        """

        # retrieves the entity class
        entity_class = entity.__class__

        return self.get_entity_class_non_relation_attribute_names(entity_class)

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

    def get_entity_class_indirect_attribute_values(self, entity_class):
        """
        Retrieves a list with the values of all indirect attributes from the given entity class.
        
        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the values of all indirect attributes from the given entity class.
        """

        # retrieves all the valid class indirect attribute names
        entity_class_valid_indirect_attribute_names = self.get_entity_class_indirect_attribute_names(entity_class)

        # retrieves all the valid class indirect attribute values
        entity_class_valid_indirect_attribute_values = [getattr(entity_class, attribute_name) for attribute_name in entity_class_valid_indirect_attribute_names]

        return entity_class_valid_indirect_attribute_values

    def get_entity_attribute_values(self, entity):
        """
        Retrieves a list with the values of all attributes from the given entity instance.
        
        @type entity: Object
        @param entity: The entity instance.
        @rtype: List
        @return: The list with the values of all attributes from the given entity instance.
        """

        # retrieves the entity class
        entity_class = entity.__class__

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid attribute values
        entity_valid_attribute_values = [getattr(entity, attribute_name) for attribute_name in entity_class_valid_attribute_names]

        return entity_valid_attribute_values

    def get_entity_indirect_attribute_values(self, entity):
        """
        Retrieves a list with the values of all indirect attributes from the given entity instance.
        
        @type entity: Object
        @param entity: The entity instance.
        @rtype: List
        @return: The list with the values of all indirect attributes from the given entity instance.
        """

        # retrieves the entity class
        entity_class = entity.__class__

        # retrieves all the valid class indirect attribute names
        entity_class_valid_indirect_attribute_names = self.get_entity_class_indirect_attribute_names(entity_class)

        # retrieves all the valid attribute values
        entity_valid_indirect_attribute_values = [getattr(entity, attribute_name) for attribute_name in entity_class_valid_indirect_attribute_names]

        return entity_valid_indirect_attribute_values

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

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # creates the initial index value
        index = 0

        for entity_class_valid_attribute_value in entity_class_valid_attribute_values:
            if ID_FIELD in entity_class_valid_attribute_value:
                if entity_class_valid_attribute_value[ID_FIELD]:
                    return entity_class_valid_attribute_names[index]

            # increments the index value
            index += 1

    def is_attribute_relation(self, attribute_value):
        """
        Retrieves the result of the attribute relation test.
        
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to test for relation.
        @rtype: bool
        @return: The result of the attribute relation test.
        """

        if attribute_value == None:
            return False

        attribute_value_data_type = attribute_value[DATA_TYPE_FIELD]

        if attribute_value_data_type == RELATION_DATA_TYPE:
            return True
        else:
            return False

    def is_attribute_name_relation(self, attribute_name, entity_class):
        """
        Retrieves the result of the attribute name relation test.
        
        @type attribute_name: Object
        @param attribute_name: The value of the attribute name to test for relation.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for relation.
        @rtype: bool
        @return: The result of the attribute name relation test.
        """

        # retrieves the attribute value
        attribute_value = getattr(entity_class, attribute_name)

        # tests the attribute value for relation
        return self.is_attribute_relation(attribute_value)

    def is_attribute_indirect_relation(self, attribute_value, attribute_name, entity_class):
        """
        Retrieves the result of the attribute indirect relation test.
        
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to test for indirect relation.
        @type attribute_name: String
        @param attribute_name: The value of the attribute name to test for indirect relation.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for indirect relation.
        @rtype: bool
        @return: The result of the attribute indirect relation test.
        """

        # is case the attribute is of type relation
        if self.is_attribute_relation(attribute_value):
            # retrieves the relation attributes
            relation_attributes = self.get_relation_attributes(entity_class, attribute_name)

            # retrieves the relation type
            relation_type = relation_attributes[RELATION_TYPE_FIELD]

            if relation_type == ONE_TO_MANY_RELATION:
                return True
            elif relation_type == MANY_TO_MANY_RELATION:
                return True
            elif relation_type == ONE_TO_ONE_RELATION:
                # in case the mapped by field is defined in the relation attributes
                if MAPPED_BY_FIELD in relation_attributes:
                    return True
                else:
                    return False
        else:
            return False

    def is_attribute_name_indirect_relation(self, attribute_name, entity_class):
        """
        Retrieves the result of the attribute name indirect relation test.
        
        @type attribute_name: Object
        @param attribute_name: The value of the attribute name to test for indirect relation.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for indirect relation.
        @rtype: bool
        @return: The result of the attribute name indirect relation test.
        """

        # retrieves the attribute value
        attribute_value = getattr(entity_class, attribute_name)

        # tests the attribute value for indirect relation
        return self.is_attribute_indirect_relation(attribute_value, attribute_name, entity_class)

    def is_attribute_table_joined_relation(self, attribute_value, attribute_name, entity_class):
        """
        Retrieves the result of the attribute table joined relation test.
        
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to test for table joined relation.
        @type attribute_name: String
        @param attribute_name: The value of the attribute name to test for table joined relation.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for table joined relation.
        @rtype: bool
        @return: The result of the attribute table joined relation test.
        """

        # is case the attribute is of type relation
        if self.is_attribute_relation(attribute_value):
            # retrieves the relation attributes
            relation_attributes = self.get_relation_attributes(entity_class, attribute_name)

            # retrieves the relation type
            relation_type = relation_attributes[RELATION_TYPE_FIELD]

            if relation_type == MANY_TO_MANY_RELATION:
                return True
        else:
            return False

    def is_attribute_name_table_joined_relation(self, attribute_name, entity_class):
        """
        Retrieves the result of the attribute name table joined relation test.
        
        @type attribute_name: Object
        @param attribute_name: The value of the attribute name to test for table joined relation.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for table joined relation.
        @rtype: bool
        @return: The result of the attribute name table joined relation test.
        """

        # retrieves the attribute value
        attribute_value = getattr(entity_class, attribute_name)

        # tests the attribute value for table joined relation
        return self.is_attribute_table_joined_relation(attribute_value, attribute_name, entity_class)

    def get_relation_attribute_value(self, attribute_value, class_attribute_value, entity_class, relation_attribute_name):
        """
        Retrieves the value of a relation attribute value sent for the given class attribute values.
        
        @type attribute_value: Object
        @param attriobute_value: The relation attribute value.
        @type class_attribute_value: Dictionary
        @param class_attribute_value: The class attribute value, containing the entity attribute metadata.
        @type entity_class: Class
        @param entity_class: The entity class containing the relation.
        @type relation_attribute_name: String
        @param relation_attribute_name: The name of the relation attribute.
        @rtype: Object
        @return: The value of the relation attribute.
        """

        # in case the value of the attribute is None returns immediately
        if attribute_value == None:
            return None

        # retrieves the class attribute value data type
        class_attribute_value_data_type = class_attribute_value[DATA_TYPE_FIELD]

        # in case the class attribute value data type is of type relation
        if class_attribute_value_data_type == RELATION_DATA_TYPE:
            # retrieves the relation attributes
            relation_attributes = self.get_relation_attributes(entity_class, relation_attribute_name)

            # retrieves the join attribute name field
            join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

            # retrieves the mapped by field
            mapped_by_field = relation_attributes.get(MAPPED_BY_FIELD, entity_class)

            # retrieves the optional field
            optional_field = relation_attributes.get(OPTIONAL_FIELD, DEFAULT_OPTIONAL_FIELD_VALUE)

            # retrieves the attribute value type
            attribute_value_type = type(attribute_value)

            # in case the relation attribute value type is not of type instance
            if not attribute_value_type == types.InstanceType:
                # in case the value is optional
                if optional_field:
                    # returns None
                    return None
                else:
                    raise business_sqlite_engine_exceptions.SqliteEngineMissingMandatoryValue("the relational value: " + relation_attribute_name + " was not found in entity: " + entity_class.__name__)

            # retrieves the relation attribute value
            relation_attribute_value = getattr(attribute_value, join_attribute_name_field)

            # returns the relation attribute value
            return relation_attribute_value

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

            # retrieves the relation attribute relation type
            relation_attribute_relation_type = relation_attributes[RELATION_TYPE_FIELD]

            # retrieves the relation attribute relation type
            relation_attribute_relation_type = relation_attributes[RELATION_TYPE_FIELD]

            # retrieves the entity class join attribute
            entity_class_join_attribute = relation_attributes[JOIN_ATTRIBUTE_FIELD]

            # retrieves the data type for the entity class join attribute
            entity_class_join_attribute_data_type = entity_class_join_attribute[DATA_TYPE_FIELD]

            return entity_class_join_attribute_data_type
        else:
            return attribute_value_data_type

    def get_relation_value(self, connection, relation_attribute_name, entity_class, relation_attribute_value, id_value, retrieved_entities_list):
        # retrieves the attribute value
        attribute_value = getattr(entity_class, relation_attribute_name)

        # retrieves the data type for the field
        attribute_value_data_type = attribute_value[DATA_TYPE_FIELD]

        # in case the data type of the field is relation
        if attribute_value_data_type == RELATION_DATA_TYPE:
            # retrieves the relation attributes
            relation_attributes = self.get_relation_attributes(entity_class, relation_attribute_name)

            # retrieves the relation attribute relation type
            relation_attribute_relation_type = relation_attributes[RELATION_TYPE_FIELD]

            # in case the relation type if of type one-to-one
            if relation_attribute_relation_type == ONE_TO_ONE_RELATION or relation_attribute_relation_type == MANY_TO_ONE_RELATION:
                # retrieves the target entity class
                target_entity_class = relation_attributes[TARGET_ENTITY_FIELD]

                # retrieves the mapped by field
                mapped_by_field = relation_attributes.get(MAPPED_BY_FIELD, entity_class)

                if mapped_by_field == entity_class:
                    # in case the relation attribute value is null
                    if relation_attribute_value == None:
                        return None

                    return self.find_entity(connection, target_entity_class, relation_attribute_value, retrieved_entities_list = retrieved_entities_list)
                else:
                    # retrieves the join attribute name field
                    join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                    return self.find_entity(connection, target_entity_class, id_value, join_attribute_name_field, retrieved_entities_list = retrieved_entities_list)
            elif relation_attribute_relation_type == ONE_TO_MANY_RELATION:
                # retrieves the target entity class
                target_entity_class = relation_attributes[TARGET_ENTITY_FIELD]

                # retrieves the mapped by field
                mapped_by_field = relation_attributes[MAPPED_BY_FIELD]

                # retrieves the join attribute name field
                join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                return self.find_all_entities(connection, target_entity_class, id_value, join_attribute_name_field, retrieved_entities_list = retrieved_entities_list)

    def get_relation_attributes(self, entity_class, relation_attribute_name):
        # creates the method name with the relation attributes prefix and the relation attribute name
        method_name = RELATION_ATTRIBUTES_METHOD_PREFIX + relation_attribute_name

        if hasattr(entity_class, method_name):
            # retrieves the relation attributes retrieval method
            relation_attributes_method = getattr(entity_class, method_name)

            # retrieves the relation attributes
            relation_attributes = relation_attributes_method()

            return relation_attributes

    def execute_query(self, cursor, query_string_value):
        """
        Executes a query in the give cursor using the query string value provided.
        
        @type cursor: Cursor
        @param cursor: The cursor where the query is going to be executed.
        @type query_string_value: String
        @param query_string_value: The string value of the query to be executed.
        """

        # logs the query string value
        self.log_query(query_string_value)

        # executes the query in the database
        cursor.execute(query_string_value)

    def log_query(self, query_string_value):
        """
        Logs the given query string value into the plugin manager logger.
        
        @type query_string_value: String
        @param query_string_value: The query string value to be logged.
        """

        self.business_sqlite_engine_plugin.debug("sql: " + query_string_value)

class BufferedEntities:
    """
    The buffered entities class.
    """

    buffered_entities_map = {}
    """ The buffered entities map """

    def __init__(self):
        """
        Constructor of the class
        """

        self.buffered_entities_map = {}

    def add_entity(self, id_value, entity):
        """
        Adds an entity to the buffer.
        
        @type id_value: Object
        @param id_value: The id of the entity to add.
        @type entity: Object
        @param entity: The entity to add.
        """

        # retrieves the entity class
        entity_class = entity.__class__

        if not entity_class in self.buffered_entities_map:
            self.buffered_entities_map[entity_class] = {}

        buffered_entities_map_entity_class_map = self.buffered_entities_map[entity_class]

        buffered_entities_map_entity_class_map[id_value] = entity

    def get_entity(self, entity_class, id_value):
        """
        Retrieves an entity from the buffer.
        
        @type entity_class: Class
        @param entity_class: The entity class of the entity to retrieve.
        @type id_value: Object
        @param id_value: The id of the entity to retrieve.
        """

        if not entity_class in self.buffered_entities_map:
            return None

        buffered_entities_map_entity_class_map = self.buffered_entities_map[entity_class]

        if not id_value in buffered_entities_map_entity_class_map:
            return None

        entity = buffered_entities_map_entity_class_map[id_value]

        return entity
