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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 7750 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-29 14:32:40 +0100 (seg, 29 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import time
import types
import sqlite3
import datetime
import calendar

import colony.libs.string_buffer_util

import entity_manager_sqlite_engine_exceptions

ENGINE_NAME = "sqlite"
""" The engine name """

DEFAULT_ISOLATION_LEVEL = "DEFERRED"
""" The default isolation level """

DEFAULT_TIMEOUT_VALUE = 30
""" The default timeout value """

DATA_TYPE_MAP = {
    "text" : "text",
    "numeric" : "numeric",
    "integer" : "integer",
    "float" : "real",
    "date" : "numeric",
    "relation" : "relation"
}
""" The data type map """

DATA_TYPE_PYTHON_MAP = {
    "text" : (
        types.StringType,
        types.UnicodeType,
        types.NoneType
    ),
    "numeric" : (
        types.IntType,
        types.LongType,
        types.FloatType,
        types.NoneType
    ),
    "integer" : (
        types.IntType,
        types.LongType,
        types.NoneType
    ),
    "float" : (
        types.IntType,
        types.LongType,
        types.FloatType,
        types.NoneType
    ),
    "date" : (
        datetime.datetime,
        types.IntType,
        types.NoneType
    )
}
""" The data type python map """

FILE_PATH_VALUE = "file_path"
""" The file path value """

AUTOCOMMIT_VALUE = "autocommit"
""" The autocommit value """

ISOLATION_LEVEL_VALUE = "isolation_level"
""" The isolation level value """

DATA_REFERENCE_VALUE = "data_reference"
""" The data reference value """

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
    "__slotnames__",
    "__subclasshook__",
    "data_state",
    "data_reference",
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

RELATION_DATA_TYPE = "relation"
""" The relation data type """

EAGER_FETCH_TYPE = "eager"
""" The eager fetch type """

LAZY_FETCH_TYPE = "lazy"
""" The lazy fetch type """

ID_FIELD = "id"
""" The id field """

DATA_TYPE_FIELD = "data_type"
""" The data type field """

FETCH_TYPE_FIELD = "fetch_type"
""" The fetch type field """

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

ID_ATTRIBUTE_NAME_VALUE = "id_attribute_name"
""" The id attribute name value """

EXISTS_ENTITY_DEFINITION_QUERY = "select name from SQLite_Master"
""" The exists entity definition query """

SAVED_STATE_VALUE = 1
""" The saved state value """

UPDATED_STATE_VALUE = 2
""" The updated state value """

REMOVED_STATE_VALUE = 3
""" The removed state value """

INEXISTING_ATTRIBUTE_REASON_CODE = 1
""" The inexisting attribute reason code """

INEXISTING_RELATION_ATTRIBUTE_REASON_CODE = 2
""" The inexisting relation attribute reason code """

INVALID_ATTRIBUTE_TYPE_REASON_CODE = 3
""" The invalid attribute type reason code """

INEXISTING_ATTRIBUTE_REASON_CODES = (1, 2)
""" The inexisting attribute reason codes """

FORCE_UPDATE_REASON_CODES = (2, 3)
""" The force update reason codes """

class EntityManagerSqliteEngine:
    """
    The entity manager sqlite engine class.
    """

    entity_manager_sqlite_engine_plugin = None
    """ The entity manager sqlite engine plugin """

    _query_counter = None
    """ The counter that control the number of executed queries """

    _query_time = None
    """ The value that control the time spent in query execution """

    _attribute_names_cache_map = {}
    """ The map that holds cache data related with attribute names for the entity classes """

    _mapped_by_other_names_cache_map = {}
    """ The map that holds cache data related with mapped by other names for the entity classes """

    _indirect_attribute_names_cache_map = {}
    """ The map that holds cache data related with indirect attribute names for the entity classes """

    _non_relation_attribute_names_cache_map = {}
    """ The map that holds cache data related with non relation attribute names for the entity classes """

    _class_attribute_values_cache_map = {}
    """ The map that holds cache data related with class attribute values for the entity classes """

    _indirect_attribute_values_cache_map = {}
    """ The map that holds cache data related with indirect attribute values for the entity classes """

    def __init__(self, entity_manager_sqlite_engine_plugin):
        """
        Constructor of the class

        @type entity_manager_sqlite_engine_plugin: EntityManagerSqliteEnginePlugin
        @param entity_manager_sqlite_engine_plugin: The entity manager sqlite engine plugin.
        """

        self.entity_manager_sqlite_engine_plugin = entity_manager_sqlite_engine_plugin

        self._query_counter = 0
        self._query_time = 0.0
        self._attribute_names_cache_map = {}
        self._mapped_by_other_names_cache_map = {}
        self._indirect_attribute_names_cache_map = {}
        self._non_relation_attribute_names_cache_map = {}
        self._class_attribute_values_cache_map = {}
        self._indirect_attribute_values_cache_map = {}

    def get_engine_name(self):
        """
        Retrieves the name of the engine.

        @rtype: String
        @return: The name of the engine.
        """

        return ENGINE_NAME

    def get_internal_version(self):
        """
        Retrieves the internal database manager oriented
        version of the engine.

        @rtype: String
        @return: internal database manager oriented
        version of the engine.
        """

        return sqlite3.sqlite_version

    def create_connection(self, connection_parameters):
        """
        Creates the connection using the given connection parameters.

        @type connection_parameters: List
        @param connection_parameters: The connection parameters.
        @rtype: DatabaseConnection
        @return: The created database connection.
        """

        # in case the file path is not defined
        if not FILE_PATH_VALUE in connection_parameters:
            # raises the missing property exception
            raise entity_manager_sqlite_engine_exceptions.MissingProperty(FILE_PATH_VALUE)

        # retrieves the file path parameter value
        file_path = connection_parameters[FILE_PATH_VALUE]

        # sets the default isolation level value
        isolation_level_value = DEFAULT_ISOLATION_LEVEL

        # retrieves the autocommit parameter value
        autocommit_value = connection_parameters.get(AUTOCOMMIT_VALUE, False)

        # in case the autocommit (flag) is set
        if autocommit_value:
            # unsets the isolation level value
            isolation_level_value = None

        # in case the isolation level is set
        if ISOLATION_LEVEL_VALUE in connection_parameters:
            # retrieves the isolation level value
            isolation_level_value = connection_parameters[ISOLATION_LEVEL_VALUE]

        # creates the sqlite database connection
        # the connection object to be used internally
        database_connection = sqlite3.connect(file_path, timeout = DEFAULT_TIMEOUT_VALUE, isolation_level = isolation_level_value)

        # returns the created database connection
        return database_connection

    def close_connection(self, connection):
        """
        Closes the given connection.

        @type connection: Connection
        @param connection: The connection to be closed.
        """

        # closes the connection (database connection)
        connection.close()

    def commit_connection(self, connection):
        """
        Commits the current transaction in the given connections.

        @type connection: Connection
        @param connection: The connection with the transaction
        to be committed.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # commits the changes to the connection
        database_connection.commit()

        # calls the commit handlers and then
        # resets all the handlers to the original state
        connection.call_commit_handlers()
        connection.reset_handlers()

    def commit_system_connection(self, connection):
        """
        Commits the current connection completely.
        All the transactions in the connections will be committed.

        @type connection: Connection
        @param connection: The connection to be committed.
        """

        # retrieves the database system connection from the connection object
        database_system_connection = connection.database_system_connection

        # commits the changes to the connection
        database_system_connection.commit()

        # calls the commit handlers and then
        # resets all the handlers to the original state
        connection.call_commit_handlers()
        connection.reset_handlers()

    def rollback_connection(self, connection):
        """
        "Rollsback" the current transaction in the given connection.

        @type connection: Connection
        @param connection: The connection with the transaction to
        be "rollbacked".
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # "rollsback" the changes to the connection
        database_connection.rollback()

        # calls the rollback handlers and then
        # resets all the handlers to the original state
        connection.call_rollback_handlers()
        connection.reset_handlers()

    def rollback_system_connection(self, connection):
        """
        "Rollsback" the current transaction completely.
        All the transactions in the connections will be "rollbacked".

        @type connection: Connection
        @param connection: The connection to be "rollbacked".
        """

        # retrieves the database system connection from the connection object
        database_system_connection = connection.database_system_connection

        # "rollsback" the changes to the connection
        database_system_connection.rollback()

        # calls the rollback handlers and then
        # resets all the handlers to the original state
        connection.call_rollback_handlers()
        connection.reset_handlers()

    def get_database_size(self, connection):
        """
        Retrieves the size of the database referred
        in the given connection.
        The returned value is measured in bytes.

        @rtype: int
        @return: The size of the database referred
        in the given connection.
        """

        # retrieves the file path to the database
        file_path = connection.get_connection_parameter(FILE_PATH_VALUE)

        # retrieves the file size for the database
        file_size = os.path.getsize(file_path)

        # returns the file size
        return file_size

    def create_transaction(self, connection, transaction_name):
        """
        Creates a new transaction in the given connection
        with the given name.

        @type connection: Connection
        @param connection: The connection to create the transaction.
        @type transaction_name: String
        @param transaction_name: The name of the transaction to
        be created.
        """

        pass

    def commit_transaction(self, connection, transaction_name):
        """
        Commits the transaction with the given name.

        @type connection: Connection
        @param connection: The connection to commit the transaction.
        @type transaction_name: String
        @param transaction_name: The name of the transaction to be
        committed.
        """

        # retrieves the transaction stack from the connection object
        transaction_stack = connection.transaction_stack

        # retrieves the transaction stack length
        transaction_stack_length = len(transaction_stack)

        # in case the transaction stack length is greater
        # than one (inner transaction)
        if transaction_stack_length > 1:
            # returns immediately (no need to commit
            # an inner transaction)
            return

        # commits the connection
        self.commit_connection(connection)

    def rollback_transaction(self, connection, transaction_name):
        """
        "Rollsback" the transaction with the given name.

        @type connection: Connection
        @param connection: The connection to commit the transaction.
        @type transaction_name: String
        @param transaction_name: The name of the transaction to be
        "rollbacked".
        """

        # retrieves the transaction stack from the connection object
        transaction_stack = connection.transaction_stack

        # retrieves the transaction stack length
        transaction_stack_length = len(transaction_stack)

        # in case the transaction stack length is greater
        # than one (inner transaction)
        if transaction_stack_length > 1:
            # returns immediately (no need to rollback
            # an inner transaction)
            return

        # "rollsback" the transaction
        self.rollback_connection(connection)

    def exists_entity_definition(self, connection, entity_class):
        """
        Checks if there is a definition for the entity in the provided
        class in the database.
        This checking requires a query in the database, so
        this is an expensive operation.

        @type connection: Connection
        @param connection: The connection to be used.
        @type entity_class: Entity
        @param entity_class: The class containing the entity to
        be verified for definition on the database.
        @rtype: bool
        @return: The result of the entity definition existence test.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # selects all the names of existing tables
            self.execute_query(cursor, EXISTS_ENTITY_DEFINITION_QUERY)

            # selects the table names from the cursor
            # by fetching all the items from it
            table_names_list = [value[0] for value in cursor]
        finally:
            # closes the cursor
            cursor.close()

        # tests if the entity class name exists in the table names list
        # retrieving the result into a boolean flag
        entity_definition_exists = entity_class_name in table_names_list

        # returns the result of the entity definition exists test
        return entity_definition_exists

    def exists_table_definition(self, connection, table_name):
        """
        Checks if the table definition for the given table name
        already exits in the database.
        This verification requires a query in the database, so
        this is an expensive operation.

        @type connection: Connection
        @param connection: The connection to be used.
        @type table_name: String
        @param table_name: The name of the table to be checked
        for database definition.
        @rtype: bool
        @return: If the target database already contains the
        definition of the given table.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # selects all the names of existing tables
            self.execute_query(cursor, EXISTS_ENTITY_DEFINITION_QUERY)

            # selects the table names from the cursor
            # by fetching all the items from it
            table_names_list = [value[0] for value in cursor]
        finally:
            # closes the cursor
            cursor.close()

        # tests if the table name exists in the table names list
        # retrieving the result into a boolean flag
        table_definition_exists = table_name in table_names_list

        # returns the result of the table definition exists test
        return table_definition_exists

    def exists_table_column_definition(self, connection, table_name, column_name):
        # tests if the table definition exists for the current table
        exists_table_definition = self.exists_table_definition(connection, table_name)

        # in case the table definition does not exists
        if not exists_table_definition:
            # returns false (invalid)
            return False

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the query string value
            query_string_value = self.create_exists_table_column_definition(table_name)

            # executes the query retrieving the values
            self.execute_query(cursor, query_string_value)

            # selects the table information from the cursor
            # by fetching all the items from it
            table_information_list = cursor.fetchall()

            # iterates over all the table information, to try to find
            # the "target" column name
            for table_information_item in table_information_list:
                # retrieves the attribute name
                attribute_name = table_information_item[1]

                # in case the attribute name is not the same
                # as the column name
                if not attribute_name == column_name:
                    # continues the loop
                    continue

                # returns true (valid)
                return True
        finally:
            # closes the cursor
            cursor.close()

        # returns false (invalid)
        return False

    def create_exists_table_column_definition(self, table_name):
        # creates the initial query string value
        query_string_value = "pragma table_info(" + table_name + ")"

        # returns the query string value
        return query_string_value

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

        # retrieves the unsynced attributes of the entity class
        unsynced_attributes_list = self._get_unsynced_attributes(connection, entity_class)

        # retrieves the unsynced relation attributes of the entity class
        unsynced_relation_attributes_list = self._get_unsynced_relation_attributes(connection, entity_class)

        # in case the unsynced (or relation) attributes list is not
        # empty and valid
        if unsynced_attributes_list or unsynced_relation_attributes_list:
            # returns false (the class is not completely synced)
            return False
        # in case the unsynced attributes list is empty or invalid
        else:
            # returns true (the class is synced)
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

        try:
            # retrieves the entity class name
            entity_class_name = entity_class.__name__

            # retrieves all the valid class attribute names, removes method values and the name exceptions
            entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

            # retrieves all the valid class attribute values
            entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

            # creates the query string buffer
            query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

            # creates the initial query string buffer
            query_string_buffer.write("create table " + entity_class_name + "(")

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
                    # adds a comma to the query string buffer
                    query_string_buffer.write(", ")

                # extends the query string buffer
                query_string_buffer.write(entity_class_valid_attribute_name + " " + entity_class_valid_attribute_target_data_type)

                # increments the index value
                index += 1

            # closes the query string buffer
            query_string_buffer.write(")")

            # retrieves the query string value
            query_string_value = query_string_buffer.get_value()

            # executes the query creating the table
            self.execute_query(cursor, query_string_value)

            # retrieves the entity id attribute name
            entity_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

            # creates the initial query string value
            query_string_value = "create index " + entity_class_name + entity_id_attribute_name + "index on " + entity_class_name + "(" + entity_id_attribute_name + ")"

            # executes the query creating the table
            self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

        # creates the entity relations definition
        self.create_update_entity_relations_definition(connection, entity_class)

    def create_update_entity_relations_definition(self, connection, entity_class):
        """
        Creates or updates the entity relations definition.
        The method starts by retrieving the current relation schema for the
        given entity class, in case the related (association) tables are not
        currently updated it proceeds by updating them.

        @type connection: Connection
        @param connection: The database connection to use.
        @type entity_class: Class
        @param entity_class: The entity class to be used in the creation or updating.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class valid indirect attribute names
            entity_class_valid_indirect_attribute_names = self.get_entity_class_indirect_attribute_names(entity_class)

            # iterates over all the entity class valid indirect attribute names
            for entity_class_valid_indirect_attribute_name in entity_class_valid_indirect_attribute_names:
                # retrieves the relation attributes for the given attribute name in the given entity class
                # in order to be able to retrieve the relation type (field)
                relation_attributes = self.get_relation_attributes(entity_class, entity_class_valid_indirect_attribute_name)
                relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

                # in case the relation is of type many-to-many, association
                # table must be taken into account for schema syncing
                if relation_type_field == MANY_TO_MANY_RELATION:
                    # retrieves the join table and the attribute column name
                    # from the relation attributes
                    join_table_field = relation_attributes[JOIN_TABLE_FIELD]
                    attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                    # retrieves the id attribute name, value and then used them
                    # to retrieve the id attribute data type (for association table foreign keys)
                    id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)
                    id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)
                    id_attribute_data_type = self.get_attribute_data_type(id_attribute_value, entity_class, id_attribute_name)

                    # retrieves the valid sqlite data type from the formal id attribute data type
                    id_attribute_target_data_type = DATA_TYPE_MAP[id_attribute_data_type]

                    # in case the table definition already exists (need to alter the table)
                    if self.exists_table_definition(connection, join_table_field):
                        if not self.exists_table_column_definition(connection, join_table_field, attribute_column_name_field):
                            # creates the query string value fr table alteration
                            # and executes it altering the table
                            query_string_value = "alter table " + join_table_field + " add column " + attribute_column_name_field + " " + id_attribute_target_data_type
                            self.execute_query(cursor, query_string_value)

                    # otherwise no "association" table definition exits (a table must be created)
                    else:
                        # creates the query string value for the association table creation
                        # and executes it
                        query_string_value = "create table " + join_table_field + "(" + attribute_column_name_field + " " + id_attribute_target_data_type + ")"
                        self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

    def remove_entity_definition(self, connection, entity_class):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class name
            entity_class_name = entity_class.__name__

            # creates the query string value and executes the
            # query dropping the table (removal of entity)
            query_string_value = "drop table " + entity_class_name
            self.execute_query(cursor, query_string_value)
        finally:
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

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves the unsynced attributes list from the entity class
        unsynced_attributes_list = self._get_unsynced_attributes(connection, entity_class)

        # retrieves the unsynced relation attributes list from the entity class
        unsynced_relation_attributes_list = self._get_unsynced_relation_attributes(connection, entity_class)

        # in case there are no unsynced attributes an relation attributes
        if not unsynced_attributes_list and not unsynced_relation_attributes_list:
            # returns immediately
            return

        # unsets the requires table recreation flag
        requires_table_recreation = False

        # iterates over all the unsynced attributes, to check if any
        # of the attribute problems is due to a type conflict
        for unsynced_attribute in unsynced_attributes_list:
            # retrieves the unsynced attribute name and reason
            _unsynced_attribute_name, unsynced_attribute_reason = unsynced_attribute

            if unsynced_attribute_reason in FORCE_UPDATE_REASON_CODES:
                # sets the requires table recreation flag
                requires_table_recreation = True

                # breaks the loop
                break

        # in case it requires table recreation
        if requires_table_recreation:
            # saves the entity table data in a list of entities
            entities_list = self._save_entity_table_data(connection, entity_class)

            # removes the entity definition by removing the
            # currently created tables
            self.remove_entity_definition(connection, entity_class)

            # creates the entity definition by creating the necessary tables
            self.create_entity_definition(connection, entity_class)

            # restores the entity table data in the associated tables
            self._restore_entity_table_data(connection, entity_class, entities_list)
        # in case the table just requires an addition of a column
        else:
            # retrieves the database connection from the connection object
            database_connection = connection.database_connection

            # creates the cursor for the given connection
            cursor = database_connection.cursor()

            try:
                # iterates over all the unsynced attributes
                for unsynced_attribute in unsynced_attributes_list:
                    # retrieves the unsynced attribute name and reason
                    unsynced_attribute_name, unsynced_attribute_reason = unsynced_attribute

                    # retrieves the unsynced attribute value
                    unsynced_attribute_value = getattr(entity_class, unsynced_attribute_name)

                    # retrieves the unsynced attribute data type
                    unsynced_attribute_data_type = self.get_attribute_data_type(unsynced_attribute_value, entity_class, unsynced_attribute_name)

                    # retrieves the valid sqlite data type from the formal unsynced attribute data type
                    unsynced_attribute_target_data_type = DATA_TYPE_MAP[unsynced_attribute_data_type]

                    if unsynced_attribute_reason == INEXISTING_ATTRIBUTE_REASON_CODE:
                        # creates the query string value
                        query_string_value = "alter table " + entity_class_name + " add column " + unsynced_attribute_name + " " + unsynced_attribute_target_data_type

                        # executes the query altering the table
                        self.execute_query(cursor, query_string_value)
            finally:
                # closes the cursor
                cursor.close()

        # tries to create (update) the entity relations definition (to update the many to many relations)
        self.create_update_entity_relations_definition(connection, entity_class)

    def create_table_generator(self, connection):
        """
        Creates the table generator, in the current
        database context.

        @type connection: Connection
        @param connection: The database connection to use.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # creates the query for the creation of the generator table
            query_string_value = "create table generator (name numeric, next_id numeric)"

            # executes the query creating the table
            self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

    def exists_table_generator(self, connection):
        """
        Checks if there is already a table generator for the given
        connection.

        @type connection: Connection
        @param connection: The database connection to use.
        @rtype: bool
        @return: If there is already a table generator for the
        connection.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # creates the query for the existence checking in generator table
            query_string_value = "pragma table_info(generator)"

            # executes the query creating the table
            self.execute_query(cursor, query_string_value)

            # selects the values from the cursor
            # by fetching all the items from it
            values_list = cursor.fetchall()
        finally:
            # closes the cursor
            cursor.close()

        # retrieves the exists table generator result
        exists_table_generator = values_list and True or False

        # returns the exists table generator result
        return exists_table_generator

    def lock_table(self, connection, table_name, parameters):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the column name from the parameters
            column_name = parameters["column_name"]

            # creates the query for the database lock
            query_string_value = "update " + table_name + " set " + column_name + " = " + column_name + " where 0 = 1"

            # executes the query creating the table
            self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

    def retrieve_next_name_id(self, connection, name):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # creates the query for the database lock and executes it
            # locking the generator table
            query_string_value = "update generator set next_id = next_id where 0 = 1"
            self.execute_query(cursor, query_string_value)

            # creates the query for the selection of the generator table
            # and executes it selecting the table
            query_string_value = "select name, next_id from generator where name = '" + name + "'"
            self.execute_query(cursor, query_string_value)

            # selects the values from the cursor
            # by fetching all the items from it
            values_list = cursor.fetchall()

            # in case no values were retrieved for the
            # given generator, value found
            if not values_list:
                # returns none, no such value
                return None
        finally:
            # closes the cursor
            cursor.close()

        return values_list[0][1]

    def set_next_name_id(self, connection, name, next_id):
        """
        Sets the next name id for the given name (identifier).

        @type connection: Connection
        @param connection: The connection to be used.
        @type name: String
        @param name: The name (identifier) to set the next id.
        @type next_id: Object
        @param next_id: The next id to be set.
        """

        # retrieves the previous next id (it may not find any
        # next name id)
        previous_next_name_id = self.retrieve_next_name_id(connection, name)

        # uses the internal setter method (safe)
        self._set_next_name_id(connection, name, next_id, previous_next_name_id)

    def _set_next_name_id(self, connection, name, next_id, previous_next_name_id):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # creates the query string buffer
            query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

            # in case there is already a valid next id
            if previous_next_name_id:
                # creates the query for the update of the data
                query_string_buffer.write("update generator set next_id = ")

                # retrieves the next id type
                next_id_type = type(next_id)

                # in case the next id type is string
                if next_id_type == types.StringType:
                    # writes the next
                    query_string_buffer.write("'" + next_id + "'")
                # otherwise it must be a string convertible value
                # and a numeric one
                else:
                    # converts the next id to string
                    next_id_string = str(next_id)

                    # writes the next id in string mode
                    query_string_buffer.write(next_id_string)

                # writes the where clause to the query string buffer
                query_string_buffer.write(" where name = '" + name + "'")
            # otherwise its a new next id value
            else:
                # creates the query for the insertion of the data
                query_string_buffer.write("insert into generator(name, next_id) values('" + name + "', ")

                # retrieves the next id type
                next_id_type = type(next_id)

                # in case the next id type is string
                if next_id_type == types.StringType:
                    # writes the next
                    query_string_buffer.write("'" + next_id + "')")
                # otherwise it must be a string convertible value
                # and a numeric one
                else:
                    # converts the next id to string
                    next_id_string = str(next_id)

                    # writes the next id in string mode
                    query_string_buffer.write(next_id_string + ")")

            # retrieves the query string value
            query_string_value = query_string_buffer.get_value()

            # executes the query creating the table
            self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

    def increment_next_name_id(self, connection, name, id_increment = 1):
        # retrieves the previous next name id
        previous_next_name_id = self.retrieve_next_name_id(connection, name)

        # uses the internal increment method
        self._increment_next_name_id(connection, name, previous_next_name_id, id_increment)

    def _increment_next_name_id(self, connection, name, previous_next_name_id, id_increment = 1):
        # in case there is no previous next name id defined
        if not previous_next_name_id:
            # raises the sqlite invalid next id exception
            raise entity_manager_sqlite_engine_exceptions.SqliteInvalidNextId("no previous next name id found")

        # calculates the next name id based on the previous next name id
        next_name_id = previous_next_name_id + id_increment

        # sets the next name id
        self._set_next_name_id(connection, name, next_name_id, previous_next_name_id)

    def validate_relation(self, connection, entity, relation_entity_id, relation_attribute_name):
        # retrieves the entity class
        entity_class = entity.__class__

        # creates the options map for retrieving
        # the relation in eager mode
        options = {
            "eager" : {
                relation_attribute_name : {}
            }
        }

        # retrieves the entity id attribute value (id value)
        id_value = self.get_entity_id_attribute_value(entity)

        # in case the id value for the base entity
        # is not yet set (not persisted)
        if id_value == None:
            # returns false (validation failed)
            # the base entity for validation is not
            # yet persisted
            return False

        # retrieves the entity (and the relation in eager mode)
        _entity = self.find_entity_options(connection, entity_class, id_value, options = options)

        # retrieves the relation attribute from the entity and then
        # retrieves the type of it
        relation_attribute = getattr(_entity, relation_attribute_name)
        relation_attribute_type = type(relation_attribute)

        # in case the relation attribute is
        # not currently set, or invalid
        if relation_attribute == None:
            # returns false (validation failed)
            # there is no relation in the given
            # relation attribute
            return False

        # in case the relation attribute is of type
        # list (to many relation)
        if relation_attribute_type == types.ListType:
            # iterate over all the items in the relation
            # attribute
            for relation_attribute_item in relation_attribute:
                # retrieves the relation entity id (attribute)
                _relation_entity_id = self.get_entity_id_attribute_value(relation_attribute_item)

                # in case the relation entity id does not matches
                if not _relation_entity_id == relation_entity_id:
                    # continues the loop
                    continue

                # returns true (validation succeeded)
                return True
        # otherwise it must be a to one relation, and there
        # must be a valid value set there
        else:
            # retrieves the relation entity id (attribute)
            _relation_entity_id = self.get_entity_id_attribute_value(relation_attribute)

            # in case the relation entity id does not matches
            if not _relation_entity_id == relation_entity_id:
                # returns false (validation failed)
                return False

            # returns true (validation succeeded)
            return True

        # returns false (validation failed)
        return False

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

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # generates the id for the entity if necessary
            self.generate_id(connection, entity)

            # retrieves the query string value
            query_string_value = self.create_save_entity_query(entity)

            # executes the query inserting the values
            self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

        # saves the entity indirect relations
        self.save_entity_indirect_relations(connection, entity)

        # sets the entity data state as saved
        entity.data_state = SAVED_STATE_VALUE

    def save_entities(self, connection, entities):
        # iterates over all the entities
        # to save them
        for entity in entities:
            # saves the entity
            self.save_entity(connection, entity)

    def create_save_entity_query(self, entity):
        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid attribute names, removes method values and the name exceptions
        entity_valid_attribute_names = self.get_entity_attribute_names(entity)

        # retrieves all the valid attribute values
        entity_valid_attribute_values = self.get_entity_attribute_values(entity)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # creates the query string buffer
        query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # creates the initial query string buffer
        query_string_buffer.write("insert into " + entity_class_name + "(")

        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the entity valid attribute names
        for entity_valid_attribute_name in entity_valid_attribute_names:
            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string buffer
                query_string_buffer.write(", ")

            # extends the query string buffer
            query_string_buffer.write(entity_valid_attribute_name)

        # extends the query string buffer
        query_string_buffer.write(") values(")

        # creates the initial index value
        index = 0

        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the valid attribute values
        for entity_valid_attribute_value in entity_valid_attribute_values:
            # in case the entity valid attribute value is lazy loaded
            if entity_valid_attribute_value == "%lazy-loaded%":
                # increments the index value
                index += 1

                # continues the loop
                continue

            # retrieves the current entity class valid attribute value
            entity_class_valid_attribute_value = entity_class_valid_attribute_values[index]

            # retrieves the entity valid attribute name
            entity_valid_attribute_name = entity_valid_attribute_names[index]

            # retrieves the entity class valid attribute value data type
            entity_class_valid_attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_valid_attribute_name)

            # checks if the attribute is of type relation
            is_attribute_relation = self.is_attribute_relation(entity_class_valid_attribute_value)

            # in case the attribute is of type relation
            if is_attribute_relation:
                # retrieves the relation attribute value using the current entity class, the relation attribute
                # resolution system uses the join attribute to find the correct attribute value
                entity_valid_attribute_value = self.get_relation_attribute_value(entity_valid_attribute_value, entity_class_valid_attribute_value, entity_class, entity_valid_attribute_name)

            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            # otherwise it is not the first field to be processed
            else:
                # adds a comma to the query string buffer
                query_string_buffer.write(", ")

            # retrieves the entity valid attribute sqlite string value
            entity_valid_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(entity_valid_attribute_value, entity_class_valid_attribute_data_type)

            # writes the entity valid attribute sqlite string value into the query string buffer
            query_string_buffer.write(entity_valid_attribute_value_sqlite_string_value)

            # increments the index value
            index += 1

        # closes the query string buffer
        query_string_buffer.write(")")

        # retrieves the query string value
        query_string_value = query_string_buffer.get_value()

        # returns the query string value
        return query_string_value

    def generate_id(self, connection, entity):
        """
        Generates the id value for the given entity.
        In case the given entity id generation is not set
        nothing happens.

        @type connection: Connection
        @param connection: The connection to be used.
        @type entity: Entity
        @param entity: The entity to generate the id.
        """

        # retrieves the entity class for the entity
        entity_class = entity.__class__

        # retrieves the entity class name for the entity
        entity_class_name = entity_class.__name__

        # retrieves the entity class id attribute value
        entity_class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

        # retrieves the entity id attribute value
        entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

        # in case the id attribute is already defined
        # (no need to generate an id)
        if not entity_id_attribute_value == None:
            # returns immediately (no need to generate id)
            return

        # in case the id field is not to be generated
        # (no need to generate an id)
        if not GENERATED_FIELD in entity_class_id_attribute_value:
            # returns immediately (no need to generate id)
            return

        # retrieves the generator type field
        generator_type = entity_class_id_attribute_value[GENERATOR_TYPE_FIELD]

        # in case the generator type is universal unique id
        if generator_type == "uuid":
            # generates a pseudo unique id
            next_id_value = int(time.time() % 10 * 100000000)
        # in case the generator type is table
        elif generator_type == "table":
            # retrieves the table generator field name, in case it is not set
            # the entity class name is used
            table_generator_field_name = entity_class_id_attribute_value.get("table_generator_field_name", entity_class_name)

            # retrieves the next id value
            next_id_value = self.retrieve_next_name_id(connection, table_generator_field_name)

            # in case the next id value is already defined
            if next_id_value:
                # increments the next name id value (involves locking table)
                self._increment_next_name_id(connection, table_generator_field_name, next_id_value)
            # otherwise a new id value must be created
            else:
                # sets the initial next id value
                next_id_value = 1

                # sets the next name id (involves locking table)
                self.set_next_name_id(connection, table_generator_field_name, next_id_value + 1)

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

        # sets the new entity id attribute value
        setattr(entity, entity_class_id_attribute_name, next_id_value)

        # creates a new lambda function to rollback the changes for
        # the generated entity id in the entity and adds it as a
        # rollback handler (called upon rollback)
        revert_generated_entity_id = lambda connection: setattr(entity, entity_class_id_attribute_name, None)
        connection.add_rollback_handler(revert_generated_entity_id)

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

        try:
            # retrieves the entity class for the entity
            entity_class = entity.__class__

            # retrieves all the valid indirect attribute names, removes method values and the name exceptions
            entity_valid_indirect_attribute_names = self.get_entity_indirect_attribute_names(entity)

            # retrieves all the valid attribute values
            entity_valid_indirect_attribute_values = self.get_entity_indirect_attribute_values(entity)

            # creates the initial index value
            index = 0

            # iterates over all the entity valid indirect attribute names
            for entity_valid_indirect_attribute_name in entity_valid_indirect_attribute_names:
                # retrieves the entity valid indirect attribute value
                entity_valid_indirect_attribute_value = entity_valid_indirect_attribute_values[index]

                # in case the entity valid indirect attribute value is not lazy loaded
                if not entity_valid_indirect_attribute_value == "%lazy-loaded%":
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

                        # retrieves the join attribute name field
                        join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                        # retrieves the target entity name
                        target_entity_name_field = target_entity_field.__name__

                        # retrieves the id attribute name
                        id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

                        # retrieves the id attribute value
                        id_attribute_value = self.get_entity_id_attribute_value(entity)

                        # retrieves the class id attribute value
                        class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

                        # retrieves the id attribute value data type
                        id_attribute_value_data_type = self.get_attribute_data_type(class_id_attribute_value, entity_class, id_attribute_name)

                        # retrieves the target entity id attribute name
                        target_entity_id_attribute_name = self.get_entity_class_id_attribute_name(target_entity_field)

                        # retrieves the target entity id attribute value
                        target_entity_id_attribute_value = self.get_entity_class_id_attribute_value(target_entity_field)

                        # retrieves the target entity id attribute value data type
                        target_entity_id_attribute_value_data_type = self.get_attribute_data_type(target_entity_id_attribute_value, target_entity_field, target_entity_id_attribute_name)

                        # iterates over all the objects in the entity valid indirect attribute value (list)
                        for object_value in entity_valid_indirect_attribute_value:
                            # retrieves the target entity id attribute value
                            target_entity_id_attribute_value = self.get_entity_id_attribute_value(object_value)

                            # creates the query string buffer
                            query_string_buffer = colony.libs.string_buffer_util.StringBuffer();

                            # creates the initial query string buffer
                            query_string_buffer.write("update " + target_entity_name_field + " set " + join_attribute_name_field + " = ")

                            # retrieves the id attribute sqlite string value
                            id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(id_attribute_value, id_attribute_value_data_type)

                            # writes the id attribute value sqlite string value
                            query_string_buffer.write(id_attribute_value_sqlite_string_value)

                            # writes the where clause in the query string buffer
                            query_string_buffer.write(" where " + target_entity_id_attribute_name + " = ")

                            # retrieves the id attribute sqlite string value
                            target_entity_id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(target_entity_id_attribute_value, target_entity_id_attribute_value_data_type)

                            # writes the target entity id attribute value sqlite string value
                            query_string_buffer.write(target_entity_id_attribute_value_sqlite_string_value)

                            # retrieves the query string value
                            query_string_value = query_string_buffer.get_value()

                            # executes the query updating the values
                            self.execute_query(cursor, query_string_value)

                    # in case the relation is of type many-to-many
                    elif relation_type_field == MANY_TO_MANY_RELATION:
                        # retrieves the join table field
                        join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                        # retrieves the target entity field
                        target_entity_field = relation_attributes[TARGET_ENTITY_FIELD]

                        # retrieves the join attribute name field
                        join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                        # retrieves the join attribute column name field
                        join_attribute_column_name_field = relation_attributes[JOIN_ATTRIBUTE_COLUMN_NAME_FIELD]

                        # retrieves the attribute column name field
                        attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                        # retrieves the target entity name
                        target_entity_name_field = target_entity_field.__name__

                        # retrieves the join attribute
                        join_attribute_field = getattr(target_entity_field, join_attribute_name_field)

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

                            # creates the query string buffer
                            query_string_buffer = colony.libs.string_buffer_util.StringBuffer();

                            # creates the initial query string value
                            query_string_buffer.write(
                                "insert into " + join_table_field + "(" + attribute_column_name_field + ", " + \
                                join_attribute_column_name_field + ") values("
                            )

                            # retrieves the id attribute sqlite string value
                            id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(id_attribute_value, id_attribute_value_data_type)

                            # writes the id attribute value sqlite string value to the query string buffer
                            query_string_buffer.write(id_attribute_value_sqlite_string_value)

                            # adds a comma to the query string buffer
                            query_string_buffer.write(", ")

                            # retrieves the target attribute sqlite string value
                            target_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(target_attribute_value, target_attribute_value_data_type)

                            # writes the target attribute value sqlite string value
                            query_string_buffer.write(target_attribute_value_sqlite_string_value)

                            # adds the closing brace to the query string buffer
                            query_string_buffer.write(")")

                            # retrieves the query string value
                            query_string_value = query_string_buffer.get_value()

                            # executes the query inserting the values
                            self.execute_query(cursor, query_string_value)

                # increments the index value
                index += 1
        finally:
            # closes the cursor
            cursor.close()

    def update_entity(self, connection, entity):
        """
        Updates the given entity instance in the database, using the given connection.

        @type connection: Connection
        @param connection: The database connection to use.
        @type entity: Object
        @param entity: The entity instance to be saved.
        """

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class for the entity
            entity_class = entity.__class__

            # retrieves the entity class id attribute value
            entity_class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

            # retrieves the entity class id attribute name
            entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

            # retrieves the entity class id attribute value data type
            entity_class_id_attribute_value_data_type = self.get_attribute_data_type(entity_class_id_attribute_value, entity_class, entity_class_id_attribute_name)

            # retrieves the entity id attribute value
            entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

            # retrieves the entity class name
            entity_class_name = entity_class.__name__

            # retrieves all the valid attribute names, removes method values and the name exceptions
            entity_valid_attribute_names = self.get_entity_attribute_names(entity)

            # retrieves all the valid attribute values
            entity_valid_attribute_values = self.get_entity_attribute_values(entity)

            # retrieves all the valid class attribute values
            entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

            # creates the query string buffer
            query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

            # creates the initial query string buffer
            query_string_buffer.write("update " + entity_class_name + " set ")

            # creates the initial index value
            index = 0

            # the first flag to control the first field to be processed
            is_first = True

            # iterates over all the entity valid attribute names and valid attribute values
            for entity_valid_attribute_name, entity_valid_attribute_value in zip(entity_valid_attribute_names, entity_valid_attribute_values):
                # in case the entity valid attribute value is lazy loaded
                if entity_valid_attribute_value == "%lazy-loaded%":
                    # increments the index value
                    index += 1

                    # continues the loop
                    continue

                # retrieves the current entity class valid attribute value
                entity_class_valid_attribute_value = entity_class_valid_attribute_values[index]

                # retrieves the entity class valid attribute value data type
                entity_class_valid_attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_valid_attribute_name)

                # checks if the attribute is of type relation
                is_attribute_relation = self.is_attribute_relation(entity_class_valid_attribute_value)

                # in case the attribute is of type relation
                if is_attribute_relation:
                    # retrieves the relation attribute value using the current entity class, the relation attribute
                    # resolution system uses the join attribute to find the correct attribute value
                    entity_valid_attribute_value = self.get_relation_attribute_value(entity_valid_attribute_value, entity_class_valid_attribute_value, entity_class, entity_valid_attribute_name)

                # in case is the first field to be processed
                if is_first:
                    # sets the is flag to false to start adding commas
                    is_first = False
                else:
                    # adds a comma to the query string buffer
                    query_string_buffer.write(", ")

                # extends the query string buffer
                query_string_buffer.write(entity_valid_attribute_name + " = ")

                # retrieves the entity valid attribute value sqlite string value
                entity_valid_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(entity_valid_attribute_value, entity_class_valid_attribute_data_type)

                # writes the entity valid attribute value sqlite string value
                query_string_buffer.write(entity_valid_attribute_value_sqlite_string_value)

                # increments the index value
                index += 1

            # extends the query string buffer
            query_string_buffer.write(" where " + entity_class_id_attribute_name + " = ")

            # retrieves the entity id attribute value sqlite string value
            entity_id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(entity_id_attribute_value, entity_class_id_attribute_value_data_type)

            # writes the entity id attribute value sqlite string value
            query_string_buffer.write(entity_id_attribute_value_sqlite_string_value)

            # retrieves the query string value
            query_string_value = query_string_buffer.get_value()

            # executes the query updating the values
            self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

        # removes the current entity indirect relations (except the lazy loaded ones)
        self.remove_entity_indirect_relations(connection, entity, False)

        # saves the entity indirect relations
        self.save_entity_indirect_relations(connection, entity)

        # sets the entity data state as updated
        entity.data_state = UPDATED_STATE_VALUE

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

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class for the entity
            entity_class = entity.__class__

            # retrieves the entity class id attribute value
            entity_id_attribute_value = self.get_entity_id_attribute_value(entity)

            # retrieves the entity class name
            entity_class_name = entity_class.__name__

            # retrieves the entity class id attribute name
            entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

            # retrieves the entity class id attribute value
            entity_class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

            # retrieves the entity class id attribute value data type
            entity_class_id_attribute_value_data_type = self.get_attribute_data_type(entity_class_id_attribute_value, entity_class, entity_class_id_attribute_name)

            # creates the initial query string value
            query_string_value = "delete from " + entity_class_name + " where " + entity_class_id_attribute_name + " = "

            # retrieves the entity id attribute value sqlite string value
            entity_id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(entity_id_attribute_value, entity_class_id_attribute_value_data_type)

            query_string_value += entity_id_attribute_value_sqlite_string_value

            # executes the query removing the values
            self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

        # removes entity indirect relations
        self.remove_entity_indirect_relations(connection, entity)

        # sets the entity data state as removed
        entity.data_state = REMOVED_STATE_VALUE

    def remove_entity_indirect_relations(self, connection, entity, remove_lazy = True):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class for the entity
            entity_class = entity.__class__

            # retrieves the entity class id attribute name
            entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

            # retrieves the entity class id attribute value
            entity_class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

            # retrieves the entity class id attribute value data type
            entity_class_id_attribute_value_data_type = self.get_attribute_data_type(entity_class_id_attribute_value, entity_class, entity_class_id_attribute_name)

            # retrieves the id attribute value
            id_attribute_value = self.get_entity_id_attribute_value(entity)

            # retrieves all the valid indirect attribute names, removes method values and the name exceptions
            entity_valid_indirect_attribute_names = self.get_entity_indirect_attribute_names(entity)

            # iterates over all the entity valid indirect attribute names
            for entity_valid_indirect_attribute_name in entity_valid_indirect_attribute_names:
                # retrieves the entity valid indirect attribute
                entity_valid_indirect_attribute = getattr(entity, entity_valid_indirect_attribute_name)

                if remove_lazy or not entity_valid_indirect_attribute == "%lazy-loaded%":
                    # retrieves the relation attributes for the given attribute name in the given entity class
                    relation_attributes = self.get_relation_attributes(entity_class, entity_valid_indirect_attribute_name)

                    # retrieves the relation type field
                    relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

                    if relation_type_field == ONE_TO_ONE_RELATION or relation_type_field == ONE_TO_MANY_RELATION:
                        # retrieves the target entity
                        target_entity_field = relation_attributes[TARGET_ENTITY_FIELD]

                        # retrieves the join attribute name field
                        join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                        # retrieves the target entity name
                        target_entity_name_field = target_entity_field.__name__

                        # creates the initial query string value
                        query_string_value = "update " + target_entity_name_field + " set " + join_attribute_name_field + " = null where " + join_attribute_name_field + " = "

                        # retrieves the entity id attribute value sqlite string value
                        entity_id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(id_attribute_value, entity_class_id_attribute_value_data_type)

                        query_string_value += entity_id_attribute_value_sqlite_string_value

                        # executes the query removing the values
                        self.execute_query(cursor, query_string_value)

                    # in case the relation is of type many-to-many
                    elif relation_type_field == MANY_TO_MANY_RELATION:
                        # retrieves the join table field
                        join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                        # retrieves the attribute column name field
                        attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                        # creates the initial query string value
                        query_string_value = "delete from " + join_table_field + " where " + attribute_column_name_field + " = "

                        # retrieves the entity id attribute value sqlite string value
                        entity_id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(id_attribute_value, entity_class_id_attribute_value_data_type)

                        query_string_value += entity_id_attribute_value_sqlite_string_value

                        # executes the query removing the values
                        self.execute_query(cursor, query_string_value)
        finally:
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

        return self.find_entity_options(connection, entity_class, id_value, search_field_name, retrieved_entities_list)

    def find_entity_options(self, connection, entity_class, id_value, search_field_name = None, retrieved_entities_list = None, options = {}):
        # normalizes the options from a simplistic view
        # to the fully recursive and extend view (if necessary)
        options = connection.normalize_options(options)

        # retrieves the eager (loading) relations option
        eager_relations = options.get("eager", {})

        # retrieves the fields option
        fields = options.get("fields", {})

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves the entity class id attribute name
        entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

        # retrieves the entity class id attribute value
        entity_class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

        # retrieves the entity class id attribute value data type
        entity_class_id_attribute_value_data_type = self.get_attribute_data_type(entity_class_id_attribute_value, entity_class, entity_class_id_attribute_name)

        # in case the retrieved entities object is not started
        if not retrieved_entities_list:
            # creates a retrieved entities object
            retrieved_entities_list = BufferedEntities()

        # in case the search field is valid
        if search_field_name:
            # the id attribute name is changed to the search field name
            entity_class_id_attribute_name = search_field_name

            # the value of the id attribute is changed to the search field attribute value
            entity_class_id_attribute_value = getattr(entity_class, search_field_name)

            # retrieves the entity class id attribute value data type
            entity_class_id_attribute_value_data_type = self.get_attribute_data_type(entity_class_id_attribute_value, entity_class, entity_class_id_attribute_name)
        else:
            # retrieves the already buffered entity
            buffered_entity = retrieved_entities_list.get_entity(entity_class, id_value)

            # in case the entity is already buffered
            if buffered_entity:
                # unsets the flag
                flag = False

                for key in eager_relations:
                    if getattr(buffered_entity, key) == "%lazy-loaded%":
                        flag = True

                if not flag:
                    # returns the buffered entity
                    return buffered_entity

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity sub classes
            entity_sub_classes = self.get_entity_sub_classes(entity_class)

            # appends the entity class to the entity sub classes
            entity_sub_classes.append(entity_class)

            # creates the entity sub classes map
            entity_sub_classes_map = {}

            # creates the entity class valid attribute names list
            entity_class_valid_attribute_names = []

            # iterates over all the entity sub classes
            for entity_sub_class in entity_sub_classes:
                # retrieves the entity sub class name
                entity_sub_class_name = entity_sub_class.__name__

                # adds the entity sub class to the entity sub classes map
                entity_sub_classes_map[entity_sub_class_name] = entity_sub_class

                # retrieves the entity sub class valid attribute names
                entity_sub_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_sub_class)

                # extends the entity class valid attribute names with the new entity sub class valid attribute names
                entity_class_valid_attribute_names.extend([value for value in entity_sub_class_valid_attribute_names if not value in entity_class_valid_attribute_names])

            # the first flag to control the sub class to be processed
            is_first_sub_class = True

            # creates the initial query string buffer
            query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

            # iterates over all the entity sub classes
            for entity_sub_class in entity_sub_classes:
                # retrieves the entity sub class name
                entity_sub_class_name = entity_sub_class.__name__

                # in case is the first sub class to be processed
                if is_first_sub_class:
                    # sets the is flag to false to start adding union all
                    is_first_sub_class = False
                else:
                    # adds a union all to the query string value
                    query_string_buffer.write(" union all ")

                # creates the select query string value
                query_string_buffer.write("select ")

                query_string_buffer.write("'" + entity_sub_class_name + "' as class_data_type")

                # retrieves the entity sub class valid attribute names
                entity_sub_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_sub_class)

                for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
                    # adds a comma to the query string value
                    query_string_buffer.write(", ")

                    if entity_class_valid_attribute_name in entity_sub_class_valid_attribute_names:
                        query_string_buffer.write(entity_class_valid_attribute_name)
                    else:
                        query_string_buffer.write("'' as " + entity_class_valid_attribute_name)

                query_string_buffer.write(" from " + entity_sub_class_name + " where " + entity_class_id_attribute_name + " = ")

                # retrieves the id value sqlite string value
                id_value_sqlite_string_value = self.get_attribute_sqlite_string_value(id_value, entity_class_id_attribute_value_data_type)

                query_string_buffer.write(id_value_sqlite_string_value)

            # retrieves the query string value
            query_string_value = query_string_buffer.get_value()

            # executes the query retrieving the values
            self.execute_query(cursor, query_string_value)

            # selects the values from the cursor
            # by fetching all the items from it
            values_list = cursor.fetchall()

            # in case there is at least one selection
            if len(values_list):
                # retrieves the first value from the values list
                first_value = values_list[0]

                # retrieves the entity class name
                entity_class_name = first_value[0]

                # sets the current entity class
                entity_class = entity_sub_classes_map[entity_class_name]

                # creates a new entity
                entity = entity_class()

                # changes the first value to start one step forward
                first_value = first_value[1:]

                # creates the initial index value
                index = 0

                # creates the relation attributes list
                # this list is used for relation attributes post-processing
                relation_attributes_list = []

                # iterates over all the attribute values of the first value
                for attribute_value in first_value:
                    # retrieves the entity class attribute name
                    entity_class_valid_attribute_name = entity_class_valid_attribute_names[index]

                    # in case the attribute exists for the current entity class
                    if hasattr(entity_class, entity_class_valid_attribute_name):
                        # in case the attribute is a relation
                        if self.is_attribute_name_relation(entity_class_valid_attribute_name, entity_class):
                            # in case the relation attribute is not meant to be eager loaded
                            if self.is_attribute_name_lazy_relation(entity_class_valid_attribute_name, entity_class) and not entity_class_valid_attribute_name in eager_relations:
                                # sets the lazy loaded attribute in the instance
                                setattr(entity, entity_class_valid_attribute_name, "%lazy-loaded%")
                            # otherwise it's not a relation (simple attribute)
                            else:
                                # creates the relation attribute tuple
                                relation_attribute_tuple = (
                                    entity_class_valid_attribute_name,
                                    attribute_value
                                )

                                # adds the relation attribute tuple to the list of relation attributes
                                relation_attributes_list.append(relation_attribute_tuple)
                        else:

                            # retrieves the entity class attribute value
                            entity_class_valid_attribute_value = getattr(entity_class, entity_class_valid_attribute_name)

                            # retrieves the attribute data type
                            attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_class_valid_attribute_name)

                            # retrieves the processed attribute value
                            processed_attribute_value = self.get_processed_sqlite_attribute_value(attribute_value, attribute_data_type)

                            # sets the processed attribute value in the instance
                            setattr(entity, entity_class_valid_attribute_name, processed_attribute_value)

                    # increments the index value
                    index += 1

                # retrieves all the mapped by other names
                mapped_by_other_names = self.get_entity_class_mapped_by_other_names(entity_class)

                # iterates over all the mapped by other names
                for mapped_by_other_name in mapped_by_other_names:
                    # in case the mapped by other name is a lazy relation and is not set in the eager
                    # loading relations
                    if self.is_attribute_name_lazy_relation(mapped_by_other_name, entity_class) and not mapped_by_other_name in eager_relations:
                        # sets the lazy loaded attribute in the instance
                        setattr(entity, mapped_by_other_name, "%lazy-loaded%")
                    # otherwise it's an eager relation and should be loaded
                    else:
                        # creates the mapped by other attribute tuple
                        mapped_by_other_attribute_tuple = (
                            mapped_by_other_name,
                            None
                        )

                        # adds the mapped by other attribute tuple to the list of relation attributes
                        relation_attributes_list.append(mapped_by_other_attribute_tuple)

                # retrieves the id attribute value
                id_attribute_value = self.get_entity_id_attribute_value(entity)

                # retrieves the already buffered entity
                buffered_entity = retrieved_entities_list.get_entity(entity_class, id_attribute_value)

                # in case the entity is already buffered
                if buffered_entity:
                    # unsets the lazy loaded flag
                    lazy_loaded_flag = False

                    # iterates over all the eager (loading) relations
                    # to make sure that they are correctly loaded
                    for key in eager_relations:
                        # retrieves the eager (loading) relation
                        eager_relation = getattr(buffered_entity, key)

                        # in case the eager (loading) relation is lazy loaded
                        if eager_relation == "%lazy-loaded%":
                            # sets the lazy loaded flag
                            # because one of the eager (loading) relations
                            # in the buffered entities is lazy loaded
                            lazy_loaded_flag = True

                    # in case the lazy loaded flag is not set
                    if not lazy_loaded_flag:
                        # returns the buffered entity
                        return buffered_entity
                # otherwise the entity is not buffered
                else:
                    # adds the entity to the list of retrieved entities
                    retrieved_entities_list.add_entity(id_attribute_value, entity)

                    # iterates over all the relation attributes list
                    for entity_class_valid_attribute_name, attribute_value in relation_attributes_list:
                        # retrieves the relation options
                        relation_options = eager_relations.get(entity_class_valid_attribute_name, {})

                        # retrieves the relation attribute value
                        relation_attribute_value = self.get_relation_value(connection, entity_class_valid_attribute_name, entity_class, attribute_value, id_value, retrieved_entities_list, relation_options)

                        # sets the relation attribute in the instance
                        setattr(entity, entity_class_valid_attribute_name, relation_attribute_value)

                # retrieves all the valid indirect attribute names, removes method values and the name exceptions
                entity_valid_indirect_attribute_names = self.get_entity_indirect_attribute_names(entity)

                # iterates over all the entity valid indirect attribute names
                for entity_valid_indirect_attribute_name in entity_valid_indirect_attribute_names:
                    # retrieves the relation options
                    relation_options = eager_relations.get(entity_valid_indirect_attribute_name, {})

                    # retrieves the relation attributes for the given attribute name in the given entity class
                    relation_attributes = self.get_relation_attributes(entity_class, entity_valid_indirect_attribute_name)

                    # retrieves the relation type field
                    relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

                    # in case the relation is of type many-to-many
                    if relation_type_field == MANY_TO_MANY_RELATION:
                        # in case the relation attribute is not meant to be eager loaded
                        if self.is_attribute_name_lazy_relation(entity_valid_indirect_attribute_name, entity_class) and not entity_valid_indirect_attribute_name in eager_relations:
                            # sets the lazy loaded attribute in the instance
                            setattr(entity, entity_valid_indirect_attribute_name, "%lazy-loaded%")
                        else:
                            # retrieves the join table field
                            join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                            # retrieves the target entity field
                            target_entity_field = relation_attributes[TARGET_ENTITY_FIELD]

                            # retrieves the join attribute column name field
                            join_attribute_column_name_field = relation_attributes[JOIN_ATTRIBUTE_COLUMN_NAME_FIELD]

                            # retrieves the attribute column name field
                            attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                            # retrieves the id attribute value
                            id_attribute_value = self.get_entity_id_attribute_value(entity)

                            # retrieves the entity class id attribute name
                            entity_class_id_attribute_name = self.get_entity_class_id_attribute_name(entity_class)

                            # retrieves the entity class id attribute value
                            entity_class_id_attribute_value = self.get_entity_class_id_attribute_value(entity_class)

                            # retrieves the entity class id attribute value data type
                            entity_class_id_attribute_value_data_type = self.get_attribute_data_type(entity_class_id_attribute_value, entity_class, entity_class_id_attribute_name)

                            # retrieves the entity id attribute value sqlite string value
                            entity_id_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(id_attribute_value, entity_class_id_attribute_value_data_type)

                            # creates the query string value
                            query_string_value = "select " + join_attribute_column_name_field + " from " + join_table_field + " where " + attribute_column_name_field + " = " + entity_id_attribute_value_sqlite_string_value

                            # executes the query removing the values
                            self.execute_query(cursor, query_string_value)

                            # selects the values from the cursor
                            # by fetching all the items from it
                            values_list = cursor.fetchall()

                            # creates the target entities list
                            target_entities_list = []

                            # iterates over the values list
                            for value in values_list:
                                # retrieves the target attribute value
                                target_attribute_value = value[0]

                                # retrieves the target entity
                                target_entity = self.find_entity_options(connection, target_entity_field, target_attribute_value, retrieved_entities_list = retrieved_entities_list, options = relation_options)

                                # appends the target entity to the list of target entities
                                target_entities_list.append(target_entity)

                            # sets the relation attribute in the instance
                            setattr(entity, entity_valid_indirect_attribute_name, target_entities_list)

                # sets the entity fields
                entity = self._set_entity_fields(entity, fields)

                # returns the created entity
                return entity
        finally:
            # closes the cursor
            cursor.close()

    def find_all_entities(self, connection, entity_class, field_value = None, search_field_name = None, retrieved_entities_list = None):
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

        return self.find_all_entities_options(connection, entity_class, field_value, search_field_name, retrieved_entities_list)

    def find_all_entities_options(self, connection, entity_class, field_value = None, search_field_name = None, retrieved_entities_list = None, options = {}):
        # normalizes the options from a simplistic view
        # to the fully recursive and extend view (if necessary)
        options = connection.normalize_options(options)

        # retrieves the eager (loading) relations option
        eager_relations = options.get("eager", {})

        # retrieves the fields option
        fields = options.get("fields", {})

        # retrieves the retrieve eager (loading) relations option
        retrieve_eager_relations = options.get("retrieve_eager", len(eager_relations) > 0)

        # retrieves the count
        count = options.get("count", False)

        # retrieves the start record
        start_record = options.get("start_record", 0)

        # retrieves the number of records
        number_records = options.get("number_records", -1)

        # retrieves the order by
        order_by = options.get("order_by", [])

        # retrieves the filters
        filters = options.get("filters", [])

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # in case the search field is defined
        if search_field_name:
            # retrieves the entity class id attribute name
            entity_class_id_attribute_name = search_field_name

            # the value of the id attribute is changed to the search field attribute value
            entity_class_id_attribute_value = getattr(entity_class, search_field_name)

            # retrieves the entity class id attribute value data type
            entity_class_id_attribute_value_data_type = self.get_attribute_data_type(entity_class_id_attribute_value, entity_class, entity_class_id_attribute_name)

        # in case the retrieved entities object is not started
        if not retrieved_entities_list:
            # creates a retrieved entities object
            retrieved_entities_list = BufferedEntities()

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity sub classes
            entity_sub_classes = self.get_entity_sub_classes(entity_class)

            # appends the entity class to the entity sub classes
            entity_sub_classes.append(entity_class)

            # creates the entity sub classes map
            entity_sub_classes_map = {}

            # creates the entity class valid attribute names list
            entity_class_valid_attribute_names = []

            # iterates over all the entity sub classes
            for entity_sub_class in entity_sub_classes:
                # retrieves the entity sub class name
                entity_sub_class_name = entity_sub_class.__name__

                # adds the entity sub class to the entity sub classes map
                entity_sub_classes_map[entity_sub_class_name] = entity_sub_class

                # retrieves the entity sub class valid attribute names
                entity_sub_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_sub_class)

                # extends the entity class valid attribute names with the new entity sub class valid attribute names
                entity_class_valid_attribute_names.extend([value for value in entity_sub_class_valid_attribute_names if not value in entity_class_valid_attribute_names])

            # the first flag to control the sub class to be processed
            is_first_sub_class = True

            # creates the query string buffer
            query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

            # in case it's a count select
            if count:
                query_string_buffer.write(" select sum(counter) from (")

            # iterates over all the entity sub classes
            for entity_sub_class in entity_sub_classes:
                # retrieves the entity sub class name
                entity_sub_class_name = entity_sub_class.__name__

                # in case is the first sub class to be processed
                if is_first_sub_class:
                    # sets the is flag to false to start adding union all
                    is_first_sub_class = False
                else:
                    # adds a union all to the query string value
                    query_string_buffer.write(" union all ")

                # creates the select query string value
                query_string_buffer.write("select ")

                # in case it's a count select
                if count:
                    query_string_buffer.write(" count(1) as counter ")
                # in case it's a normal select
                else:
                    query_string_buffer.write("'" + entity_sub_class_name + "' as class_data_type")

                    # retrieves the entity sub class valid attribute names
                    entity_sub_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_sub_class)

                    for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
                        # adds a comma to the query string value
                        query_string_buffer.write(", ")

                        if entity_class_valid_attribute_name in entity_sub_class_valid_attribute_names:
                            query_string_buffer.write(entity_class_valid_attribute_name)
                        else:
                            query_string_buffer.write("'' as " + entity_class_valid_attribute_name)

                # sets the is first where clause flag
                is_first_where = True

                if field_value == None:
                    query_string_buffer.write(" from " + entity_sub_class_name)
                else:
                    query_string_buffer.write(" from " + entity_sub_class_name + " where " + entity_class_id_attribute_name + " = ")

                    # retrieves the field value value sqlite string value
                    field_value_sqlite_string_value = self.get_attribute_sqlite_string_value(field_value, entity_class_id_attribute_value_data_type)

                    query_string_buffer.write(field_value_sqlite_string_value)

                    # unsets the is first where clause flag
                    is_first_where = False

                # processes the filters part of the query string
                # this function recursively populates the query string
                # buffer with the filter clauses
                self._process_filters(query_string_buffer, entity_class, filters, is_first_where)

            # in case it's a count select
            if count:
                query_string_buffer.write(")")

            # in case there is at least one order by definition
            if len(order_by):
                query_string_buffer.write(" order by ")

                is_first_order_by = True

                # iterates over all the order by values
                for order_by_value in order_by:
                    order_by_name, order_by_order = order_by_value

                    if is_first_order_by:
                        is_first_order_by = False
                    else:
                        # adds a comma to the query string value
                        query_string_buffer.write(", ")
                    query_string_buffer.write(order_by_name)

                    if order_by_order == "ascending":
                        query_string_buffer.write(" asc")
                    elif order_by_order == "descending":
                        query_string_buffer.write(" desc")

            query_string_buffer.write(" limit " + str(start_record) + ", " + str(number_records))

            # retrieves the query string value
            query_string_value = query_string_buffer.get_value()

            # executes the query retrieving the values
            self.execute_query(cursor, query_string_value)

            # selects the values from the cursor
            values_list = cursor.fetchall()

            # in case it's a count select
            if count:
                # starts the count value
                count_value = 0

                for value in values_list[0]:
                    count_value += value

                # returns the count value
                return count_value

            # creates the list of entities
            entities_list = []

            # in case the eager (loading) relations should be retrieved
            if retrieve_eager_relations:
                # iterates over all the values in the values list
                for value in values_list:
                    # retrieves the entity class name
                    entity_class_name = value[0]

                    # sets the current entity class
                    entity_class = entity_sub_classes_map[entity_class_name]

                    # creates a new entity
                    entity = entity_class()

                    # changes the value to start one step forward
                    value = value[1:]

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

                        # in case the attribute exists for the current entity class
                        if hasattr(entity_class, entity_class_valid_attribute_name):
                            # in case the attribute is a relation
                            if self.is_attribute_name_relation(entity_class_valid_attribute_name, entity_class):
                                # in case the attribute is lazy and is not in the eager (loading) relations map
                                if self.is_attribute_name_lazy_relation(entity_class_valid_attribute_name, entity_class) and not entity_class_valid_attribute_name in eager_relations:
                                    # sets the lazy loaded attribute in the instance
                                    setattr(entity, entity_class_valid_attribute_name, "%lazy-loaded%")
                                else:
                                    # creates the relation attribute tuple
                                    relation_attribute_tuple = (
                                        entity_class_valid_attribute_name,
                                        attribute_value
                                    )

                                    # adds the relation attribute tuple to the list of relation attributes
                                    relation_attributes_list.append(relation_attribute_tuple)
                            # otherwise it's not a relation (simple attribute)
                            else:
                                # retrieves the entity class attribute value
                                entity_class_valid_attribute_value = getattr(entity_class, entity_class_valid_attribute_name)

                                # retrieves the attribute data type
                                attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_class_valid_attribute_name)

                                # retrieves the processed attribute value
                                processed_attribute_value = self.get_processed_sqlite_attribute_value(attribute_value, attribute_data_type)

                                # sets the processed attribute value in the instance
                                setattr(entity, entity_class_valid_attribute_name, processed_attribute_value)

                        # increments the index value
                        index += 1

                    # retrieves all the mapped by other names
                    mapped_by_other_names = self.get_entity_class_mapped_by_other_names(entity_class)

                    # iterates over all the mapped by other names
                    for mapped_by_other_name in mapped_by_other_names:
                        # in case the mapped by other name is a lazy relation and is not set in the eager
                        # loading relations
                        if self.is_attribute_name_lazy_relation(mapped_by_other_name, entity_class) and not mapped_by_other_name in eager_relations:
                            # sets the lazy loaded attribute in the instance
                            setattr(entity, mapped_by_other_name, "%lazy-loaded%")
                        # otherwise it's an eager relation and should be loaded
                        else:
                            # creates the mapped by other attribute tuple
                            mapped_by_other_attribute_tuple = (
                                mapped_by_other_name,
                                None
                            )

                            # adds the mapped by other attribute tuple to the list of relation attributes
                            relation_attributes_list.append(mapped_by_other_attribute_tuple)

                    # retrieves the id attribute value
                    id_attribute_value = self.get_entity_id_attribute_value(entity)

                    # retrieves the already buffered entity
                    buffered_entity = retrieved_entities_list.get_entity(entity_class, id_attribute_value)

                    # in case the entity is already buffered
                    if buffered_entity:
                        # sets the entity as the buffered entity
                        entity = buffered_entity
                    else:
                        # adds the entity to the list of retrieved entities
                        retrieved_entities_list.add_entity(id_attribute_value, entity)

                        # iterates over all the relation attributes list
                        for entity_class_valid_attribute_name, attribute_value in relation_attributes_list:
                            # retrieves the relation options
                            relation_options = eager_relations.get(entity_class_valid_attribute_name, {})

                            # retrieves the relation attribute value
                            relation_attribute_value = self.get_relation_value(connection, entity_class_valid_attribute_name, entity_class, attribute_value, id_attribute_value, retrieved_entities_list, options = relation_options)

                            # sets the relation attribute in the instance
                            setattr(entity, entity_class_valid_attribute_name, relation_attribute_value)

                    # sets the entity fields
                    entity = self._set_entity_fields(entity, fields)

                    # adds the entity to the list of entities
                    entities_list.append(entity)
            else:
                # iterates over all the values in the values list
                for value in values_list:
                    # retrieves the entity class name
                    entity_class_name = value[0]

                    # sets the current entity class
                    entity_class = entity_sub_classes_map[entity_class_name]

                    # creates a new entity
                    entity = entity_class()

                    # changes the value to start one step forward
                    value = value[1:]

                    # creates the initial index value
                    index = 0

                    # iterates over all the attribute values of the value
                    for attribute_value in value:
                        # retrieves the entity class attribute name
                        entity_class_valid_attribute_name = entity_class_valid_attribute_names[index]

                        # in case the attribute exists for the current entity class
                        if hasattr(entity_class, entity_class_valid_attribute_name):
                            # retrieves the entity class attribute value
                            entity_class_valid_attribute_value = getattr(entity_class, entity_class_valid_attribute_name)

                            # retrieves the attribute data type
                            attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_class_valid_attribute_name)

                            # retrieves the processed attribute value
                            processed_attribute_value = self.get_processed_sqlite_attribute_value(attribute_value, attribute_data_type)

                            # sets the attribute value in the entity
                            setattr(entity, entity_class_valid_attribute_name, processed_attribute_value)

                        # increments the index value
                        index += 1

                    # sets the entity fields
                    entity = self._set_entity_fields(entity, fields)

                    # adds the entity to the list of entities
                    entities_list.append(entity)
        finally:
            # closes the cursor
            cursor.close()

        # returns the entities list
        return entities_list

    def lock(self, connection, entity_class, id_value):
        """
        Locks the database using the given connection
        for the given entity class and id value.

        @type connection: Connection
        @param connection: The database connection to use.
        @type entity_class: Class
        @param entity_class: The entity class.
        @type id_value: Object
        @param id_value: The value of the id attribute
        of the entity to be used for locking.
        """

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves the entity class valid attribute first name
        entity_class_valid_attribute_first_name = entity_class_valid_attribute_names[0]

        # creates the parameters map
        parameters = {
            "column_name" : entity_class_valid_attribute_first_name
        }

        # locks the table in order to lock the entity
        self.lock_table(connection, entity_class_name, parameters)

    def get_entity_class_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all attributes from the given entity class.
        The valid attributes are the ones that are simple attributes or that
        are relation attributes mapped in the current entity class.

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the names of all attributes from the given entity class.
        """

        # tries to retrieve the entity class valid attribute
        # names from the attribute names cache map
        entity_class_valid_attribute_names = self._attribute_names_cache_map.get(entity_class, None)

        # in case the entity class valid attribute names
        # are found and valid
        if not entity_class_valid_attribute_names == None:
            # returns the entity class valid attribute names
            return entity_class_valid_attribute_names

        # retrieves all the class attribute names
        entity_class_attribute_names = dir(entity_class)

        # retrieves all the valid class attribute names, removes method values, the name exceptions, the indirect attributes and the mapped by other attributes
        entity_class_valid_attribute_names = [attribute_name for attribute_name in entity_class_attribute_names if not attribute_name in ATTRIBUTE_EXCLUSION_LIST and not type(getattr(entity_class, attribute_name)) in TYPE_EXCLUSION_LIST and not self.is_attribute_name_table_joined_relation(attribute_name, entity_class) and not self.is_attribute_name_mapped_by_other(attribute_name, entity_class)]

        # sets the entity class valid attribute names in the
        # attribute names cache map
        self._attribute_names_cache_map[entity_class] = entity_class_valid_attribute_names

        # returns the entity class valid attribute names
        return entity_class_valid_attribute_names

    def get_entity_class_mapped_by_other_names(self, entity_class):
        """
        Retrieves a list with the names of all attributes from the given entity class.
        The mapped by other attributes are the ones that are mapped by the other side
        of the relation, in this case the entity class is a non owner one.

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the names of all attributes from the given entity class.
        """

        # tries to retrieve the entity class mapped by
        # other attribute names from the mapped by other
        # names cache map
        entity_class_mapped_by_other_attribute_names = self._mapped_by_other_names_cache_map.get(entity_class, None)

        # in case the entity class mapped by other attribute names
        # are found and valid
        if not entity_class_mapped_by_other_attribute_names == None:
            # returns the entity class mapped by other
            # attribute names
            return entity_class_mapped_by_other_attribute_names

        # retrieves all the class attribute names
        entity_class_attribute_names = dir(entity_class)

        # retrieves all the mapped by other attribute names, removes method values, the name exceptions, the indirect attributes and filters the mapped by other attributes
        entity_class_mapped_by_other_attribute_names = [attribute_name for attribute_name in entity_class_attribute_names if not attribute_name in ATTRIBUTE_EXCLUSION_LIST and not type(getattr(entity_class, attribute_name)) in TYPE_EXCLUSION_LIST and not self.is_attribute_name_table_joined_relation(attribute_name, entity_class) and self.is_attribute_name_mapped_by_other(attribute_name, entity_class)]

        # sets the entity class mapped by other attribute
        # names in the mapped by other names cache map
        self._mapped_by_other_names_cache_map[entity_class] = entity_class_mapped_by_other_attribute_names

        # returns the entity class mapped by other names
        return entity_class_mapped_by_other_attribute_names

    def get_entity_class_indirect_attribute_names(self, entity_class):
        """
        Retrieves a list with the names of all indirect attributes from the given entity class.
        The indirect attributes are the ones that are mapped by a join table or by the other
        entity (non owner case).

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the names of all the indirect attributes from the given entity class.
        """

        # tries to retrieve the entity class valid indirect
        # attribute names from the indirect attribute names
        # cache map
        entity_class_valid_indirect_attribute_names = self._indirect_attribute_names_cache_map.get(entity_class, None)

        # in case the entity class valid indirect attribute names
        # are found and valid
        if not entity_class_valid_indirect_attribute_names == None:
            # returns the entity class valid indirect attribute
            # names
            return entity_class_valid_indirect_attribute_names

        # retrieves all the class attribute names
        entity_class_attribute_names = dir(entity_class)

        # retrieves all the valid class indirect attribute names, removes method values and the name exceptions and the non indirect attributes
        entity_class_valid_indirect_attribute_names = [attribute_name for attribute_name in entity_class_attribute_names if not attribute_name in ATTRIBUTE_EXCLUSION_LIST and not type(getattr(entity_class, attribute_name)) in TYPE_EXCLUSION_LIST and self.is_attribute_name_indirect_relation(attribute_name, entity_class)]

        # sets the entity class valid indirect attribute names
        # in the indirect attribute names cache map
        self._indirect_attribute_names_cache_map[entity_class] = entity_class_valid_indirect_attribute_names

        # returns the entity class valid indirect attribute names
        return entity_class_valid_indirect_attribute_names

    def get_entity_attribute_names(self, entity):
        """
        Retrieves a list with the names of all attributes from the given entity instance.

        @type entity: Object
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

        # tries to retrieve the entity class non relation
        # attribute names from the non relation attribute
        # names cache map
        entity_class_non_relation_attribute_names = self._non_relation_attribute_names_cache_map.get(entity_class, None)

        # in case the entity class non relation attribute names
        # are found and valid
        if not entity_class_non_relation_attribute_names == None:
            # returns the entity class non relation attribute
            # names
            return entity_class_non_relation_attribute_names

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the non relation attribute names
        entity_class_non_relation_attribute_names = [attribute_name for attribute_name in entity_class_valid_attribute_names if not attribute_name[DATA_TYPE_FIELD] == RELATION_DATA_TYPE]

        # sets the entity class non relation attribute names
        # in the non relation attribute names cache map
        self._non_relation_attribute_names_cache_map[entity_class] = entity_class_non_relation_attribute_names

        # returns the entity class non relation attribute names
        return entity_class_non_relation_attribute_names

    def get_entity_non_relation_attribute_names(self, entity):
        """
        Retrieves a list with the names of all the non relational attributes from the given entity instance.

        @type entity: Object
        @param entity: The entity instance.
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

        # tries to retrieve the entity class valid attribute
        # values from the class attribute values cache map
        entity_class_valid_attribute_values = self._class_attribute_values_cache_map.get(entity_class, None)

        # in case the entity class valid attribute values
        # are found and valid
        if not entity_class_valid_attribute_values == None:
            # returns the entity class valid attribute values
            return entity_class_valid_attribute_values

        # retrieves all the valid class attribute names
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = [getattr(entity_class, attribute_name) for attribute_name in entity_class_valid_attribute_names]

        # sets the entity class valid attribute values in the
        # class attribute values cache map
        self._class_attribute_values_cache_map[entity_class] = entity_class_valid_attribute_values

        # returns the entity class non relation attribute values
        return entity_class_valid_attribute_values

    def get_entity_class_indirect_attribute_values(self, entity_class):
        """
        Retrieves a list with the values of all indirect attributes from the given entity class.

        @type entity_class: Class
        @param entity_class: The entity class.
        @rtype: List
        @return: The list with the values of all indirect attributes from the given entity class.
        """

        # tries to retrieve the entity class valid indirect
        # attribute values from the indirect attribute values
        # cache map
        entity_class_valid_indirect_attribute_values = self._indirect_attribute_values_cache_map.get(entity_class, None)

        # in case the entity class valid indirect attribute values
        # are found and valid
        if not entity_class_valid_indirect_attribute_values == None:
            # returns the entity class valid indirect attribute value
            return entity_class_valid_indirect_attribute_values

        # retrieves all the valid class indirect attribute names
        entity_class_valid_indirect_attribute_names = self.get_entity_class_indirect_attribute_names(entity_class)

        # retrieves all the valid class indirect attribute values
        entity_class_valid_indirect_attribute_values = [getattr(entity_class, attribute_name) for attribute_name in entity_class_valid_indirect_attribute_names]

        # sets the entity class valid indirect attribute values
        # in the indirect attribute values cache map
        self._indirect_attribute_values_cache_map[entity_class] = entity_class_valid_indirect_attribute_values

        # returns the entity class valid indirect attribute values
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

        # starts the valid attribute values (list)
        entity_valid_attribute_values = []

        # iterates over all the entity class valid attribute names
        for attribute_name in entity_class_valid_attribute_names:
            # retrieves the attribute value for the attribute name
            attribute_value = getattr(entity, attribute_name)

            # retrieves the class attribute value for the attribute name
            class_attribute_value = getattr(entity_class, attribute_name)

            # retrieves the attribute value type
            attribute_value_type = type(attribute_value)

            # retrieves the data type value from the class attribute value
            data_type = class_attribute_value.get("data_type", False)

            # retrieves the is mandatory value from the class attribute value
            is_mandatory = class_attribute_value.get("mandatory", False)

            # retrieves the "expected" python data types
            python_data_types = DATA_TYPE_PYTHON_MAP.get(data_type, None)

            # in case the attribute value type is not the "expected" python
            # data types, tests if the python data type is defined (validation ready
            # attribute type)
            if python_data_types and not attribute_value_type in python_data_types:
                # raises the sqlite engine type check failed exception
                raise entity_manager_sqlite_engine_exceptions.SqliteEngineTypeCheckFailed("in attribute value: " + attribute_name + " expected type(s): " + str(python_data_types) + " got: " + str(attribute_value_type))

            # in case the attribute is mandatory and the attribute
            # value is not set
            if is_mandatory and attribute_value == None:
                # raises the sqlite engine missing mandatory value exception
                raise entity_manager_sqlite_engine_exceptions.SqliteEngineMissingMandatoryValue("the mandatory value: " + attribute_name + " was not found in entity: " + entity_class.__name__)

            # adds the attribute value to the entity valid
            # attribute values
            entity_valid_attribute_values.append(attribute_value)

        # returns the entity valid attribute values
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

    def is_attribute_relation(self, attribute_value):
        """
        Retrieves the result of the attribute relation test.

        @type attribute_value: Object
        @param attribute_value: The value of the attribute to test for relation.
        @rtype: bool
        @return: The result of the attribute relation test.
        """

        # in case the attribute value is not set
        if attribute_value == None:
            # returns false (not relation)
            return False

        # retrieves the attribute value data type
        attribute_value_data_type = attribute_value[DATA_TYPE_FIELD]

        # in case the attribute is a relation
        if attribute_value_data_type == RELATION_DATA_TYPE:
            # returns true (relation)
            return True
        # otherwise it is not a relation
        else:
            # returns false (not relation)
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

    def is_attribute_lazy_relation(self, attribute_value):
        """
        Retrieves the result of the attribute lazy relation test.

        @type attribute_value: Object
        @param attribute_value: The value of the attribute to test for lazy relation.
        @rtype: bool
        @return: The result of the attribute lazy relation test.
        """

        if attribute_value == None:
            return False

        if not self.is_attribute_relation(attribute_value):
            return False

        if not FETCH_TYPE_FIELD in attribute_value:
            return False

        attribute_value_fetch_type = attribute_value[FETCH_TYPE_FIELD]

        if attribute_value_fetch_type == LAZY_FETCH_TYPE:
            return True
        else:
            return False

    def is_attribute_name_lazy_relation(self, attribute_name, entity_class):
        """
        Retrieves the result of the attribute name lazy relation test.

        @type attribute_name: Object
        @param attribute_name: The value of the attribute name to test for lazy relation.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for lazy relation.
        @rtype: bool
        @return: The result of the attribute name lazy relation test.
        """

        # retrieves the attribute value
        attribute_value = getattr(entity_class, attribute_name)

        # tests the attribute value for lazy relation
        return self.is_attribute_lazy_relation(attribute_value)

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

            # in case it's a one to many relation
            if relation_type == ONE_TO_MANY_RELATION:
                # returns true (valid)
                return True
            # in case it's a many to many relation
            elif relation_type == MANY_TO_MANY_RELATION:
                # returns true (valid)
                return True
            # in case it's a one to one relation, it will check if
            # the entity is mapped by other relation
            elif relation_type == ONE_TO_ONE_RELATION:
                # retrieves the mapped by value
                mapped_by = relation_attributes.get(MAPPED_BY_FIELD, entity_class)

                # in case the relation is not mapped by the
                # the entity class
                if not mapped_by == entity_class:
                    # returns true (valid)
                    return True
                # otherwise the relation is mapped by the
                # entity class itself
                else:
                    # returns false (invalid)
                    return False
        # otherwise the attribute is not a relation
        else:
            # returns false (invalid)
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

            # in case the relation type is many to many
            if relation_type == MANY_TO_MANY_RELATION:
                # returns true (valid)
                return True
        # otherwise it's not a relation
        else:
            # return false (invalid)
            return False

    def is_attribute_mapped_by_other(self, attribute_value, attribute_name, entity_class):
        """
        Retrieves the result of the attribute mapped by other test.

        @type attribute_value: Object
        @param attribute_value: The value of the attribute to test for mapped by other.
        @type attribute_name: String
        @param attribute_name: The value of the attribute name to test for mapped by other.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for mapped by other.
        @rtype: bool
        @return: The result of the attribute mapped by other test.
        """

        # is case the attribute is of type relation
        if self.is_attribute_relation(attribute_value):
            # retrieves the relation attributes
            relation_attributes = self.get_relation_attributes(entity_class, attribute_name)

            # retrieves the mapped by
            mapped_by = relation_attributes.get(MAPPED_BY_FIELD, entity_class)

            # in case the relation is not mapped
            # by itself it must be mapped by "other"
            if not mapped_by == entity_class:
                # returns true (valid)
                return True
            # otherwise it must be mapped by itself
            else:
                # returns false (invalid)
                return False
        # otherwise it's not a relation
        else:
            # return false (invalid)
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

    def is_attribute_name_mapped_by_other(self, attribute_name, entity_class):
        """
        Retrieves the result of the attribute name mapped by other test.

        @type attribute_name: Object
        @param attribute_name: The value of the attribute name to test for mapped by other.
        @type entity_class: Class
        @param entity_class: The entity class for the attribute name to test for mapped by other.
        @rtype: bool
        @return: The result of the attribute name mapped by other test.
        """

        # retrieves the attribute value
        attribute_value = getattr(entity_class, attribute_name)

        # tests the attribute value for mapped by other
        return self.is_attribute_mapped_by_other(attribute_value, attribute_name, entity_class)

    def get_relation_attribute_value(self, attribute_value, class_attribute_value, entity_class, relation_attribute_name):
        """
        Retrieves the value of a relation attribute value sent for the given class attribute values.
        The relation attribute value must be set prior to retrieval.

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

        # retrieves the business helper plugin
        business_helper_plugin = self.entity_manager_sqlite_engine_plugin.business_helper_plugin

        # retrieves the object entity class
        object_entity_class = business_helper_plugin.get_entity_class()

        # in case the value of the attribute is none returns immediately
        if attribute_value == None:
            # returns immediately none (unset)
            return None

        # retrieves the class attribute value data type
        class_attribute_value_data_type = class_attribute_value[DATA_TYPE_FIELD]

        # in case the class attribute value data type is not of type relation
        if not class_attribute_value_data_type == RELATION_DATA_TYPE:
            # returns immediately none (unset)
            return None

        # retrieves the relation attributes
        relation_attributes = self.get_relation_attributes(entity_class, relation_attribute_name)

        # retrieves the mapped by field
        mapped_by_field = relation_attributes.get(MAPPED_BY_FIELD, entity_class)

        # in case the relation attribute is not mapped by the current entity class
        # there is no need to return any value (because there is no need to persist it)
        if not mapped_by_field == entity_class:
            # returns immediately none (unset)
            return None

        # retrieves the join attribute name field
        join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

        # retrieves the optional field
        optional_field = relation_attributes.get(OPTIONAL_FIELD, DEFAULT_OPTIONAL_FIELD_VALUE)

        # in case the relation attribute value is of type entity class
        if not isinstance(attribute_value, object_entity_class):
            # in case the value is optional
            if optional_field:
                # returns none (unset)
                return None
            # otherwise
            else:
                # raises the sqlite engine missing mandatory value
                raise entity_manager_sqlite_engine_exceptions.SqliteEngineMissingMandatoryValue("the relational value: " + relation_attribute_name + " was not found in entity: " + entity_class.__name__)

        # retrieves the relation attribute value
        relation_attribute_value = getattr(attribute_value, join_attribute_name_field)

        # returns the relation attribute value
        return relation_attribute_value

    def get_attribute_data_type(self, attribute_value, entity_class, relation_attribute_name, resolve_relations = False):
        """
        Retrieves the data type of the give attribute value.

        @type attribute_value: Dictionary
        @param attribute_value: The attribute value, containing the entity attribute metadata.
        @type entity_class: Class
        @param entity_class: The entity class containing the relation.
        @type relation_attribute_name: String
        @param relation_attribute_name: The name of the relation attribute.
        @type resolve_relations: bool
        @param resolve_relations: If the mapped by other relations should be
        resolved. This is important if the final goal is to always retrieve
        the primitive data type of the attribute.
        @rtype: String
        @return: The attribute data type.
        """

        # retrieves the attribute value data type
        attribute_value_data_type = attribute_value[DATA_TYPE_FIELD]

        # in case the attribute value data type is of type relation
        if attribute_value_data_type == RELATION_DATA_TYPE:
            # retrieves the relation attributes from the entity class
            relation_attributes = self.get_relation_attributes(entity_class, relation_attribute_name)

            # retrieves the entity class target entity and
            # join attribute name fields
            entity_class_target_entity = relation_attributes[TARGET_ENTITY_FIELD]
            entity_class_join_attribute_name = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

            # retrieves the entity class join attribute and then uses it
            # to retrieve the entity class join attribute data type
            entity_class_join_attribute = getattr(entity_class_target_entity, entity_class_join_attribute_name)
            entity_class_join_attribute_data_type = entity_class_join_attribute[DATA_TYPE_FIELD]

            # in case the entity class join attribute data type is relation
            # (mapped by other situation)
            if resolve_relations and entity_class_join_attribute_data_type == RELATION_DATA_TYPE:
                # retrieves the relation attributes from the entity class
                # target entity (class mapping the relation)
                relation_attributes = self.get_relation_attributes(entity_class_target_entity, entity_class_join_attribute_name)

                # retrieves the entity class target entity and
                # join attribute name fields
                entity_class_target_entity = relation_attributes[TARGET_ENTITY_FIELD]
                entity_class_join_attribute_name = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                # retrieves the entity class join attribute and then uses it
                # to retrieve the entity class join attribute data type
                entity_class_join_attribute = getattr(entity_class_target_entity, entity_class_join_attribute_name)
                entity_class_join_attribute_data_type = entity_class_join_attribute[DATA_TYPE_FIELD]

            # returns the entity class join attribute data type
            return entity_class_join_attribute_data_type
        # otherwise it must be a "simple" attribute
        else:
            # returns the attribute value data type
            return attribute_value_data_type

    def get_relation_value(self, connection, relation_attribute_name, entity_class, relation_attribute_value, id_value, retrieved_entities_list, options):
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

                    return self.find_entity_options(connection, target_entity_class, relation_attribute_value, retrieved_entities_list = retrieved_entities_list, options = options)
                else:
                    # retrieves the join attribute name field
                    join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                    return self.find_entity_options(connection, target_entity_class, id_value, join_attribute_name_field, retrieved_entities_list = retrieved_entities_list, options = options)
            elif relation_attribute_relation_type == ONE_TO_MANY_RELATION:
                # retrieves the target entity class
                target_entity_class = relation_attributes[TARGET_ENTITY_FIELD]

                # retrieves the join attribute name field
                join_attribute_name_field = relation_attributes[JOIN_ATTRIBUTE_NAME_FIELD]

                # normalizes the options from a simplistic view
                # to the fully recursive and extend view (if necessary)
                # this step is required to avoid possible map collision in the
                # options map
                options = connection.normalize_options(options)

                # sets the retrieve eager (loading) relations option as true or the
                # previously assigned value
                options["retrieve_eager"] = options.get("retrieve_eager", True)

                return self.find_all_entities_options(connection, target_entity_class, id_value, join_attribute_name_field, retrieved_entities_list = retrieved_entities_list, options = options)

    def get_relation_attributes(self, entity_class, relation_attribute_name):
        # creates the method name with the relation attributes prefix and the relation attribute name
        method_name = RELATION_ATTRIBUTES_METHOD_PREFIX + relation_attribute_name

        # in case the entity class does not contain the method
        # for the relation attributes retrieval method
        if not hasattr(entity_class, method_name):
            # raises the sqlite engine missing relation method exception
            raise entity_manager_sqlite_engine_exceptions.SqliteEngineMissingRelationMethod(method_name)

        # retrieves the relation attributes retrieval method
        relation_attributes_method = getattr(entity_class, method_name)

        # retrieves the relation attributes
        relation_attributes = relation_attributes_method()

        # returns the relation attributes
        return relation_attributes

    def execute_query(self, cursor, query_string_value):
        """
        Executes a query in the given cursor using the query string value provided.
        This method provides automatic logging features.

        @type cursor: Cursor
        @param cursor: The cursor where the query is going to be executed.
        @type query_string_value: String
        @param query_string_value: The string value of the query to be executed.
        """

        # retrieves the start time
        # for time measurement
        start_time = time.clock()

        # logs the query string value
        self.log_query(query_string_value)

        # executes the query in the database
        cursor.execute(query_string_value)

        # increments the query counter
        self._query_counter += 1

        # calculates the delta time based on the
        # final time
        end_time = time.clock()
        delta_time = end_time - start_time

        # increments the query time with the
        # current query execution time
        self._query_time += delta_time

    def execute_script(self, cursor, script_string_value):
        """
        Executes a script in the given cursor using the script string value provided.

        @type cursor: Cursor
        @param cursor: The cursor where the script is going to be executed.
        @type script_string_value: String
        @param script_string_value: The string value of the script to be executed.
        """

        # logs the script string value
        self.log_script(script_string_value)

        # executes the script in the database
        cursor.executescript(script_string_value)

    def log_query(self, query_string_value):
        """
        Logs the given query string value into the plugin manager logger.

        @type query_string_value: String
        @param query_string_value: The query string value to be logged.
        """

        self.entity_manager_sqlite_engine_plugin.debug("sql: " + query_string_value)

    def log_script(self, script_string_value):
        """
        Logs the given script string value into the plugin manager logger.

        @type script_string_value: String
        @param script_string_value: The script string value to be logged.
        """

        self.entity_manager_sqlite_engine_plugin.debug("sql script: " + script_string_value)

    def get_attribute_sqlite_string_value(self, attribute_value, attribute_data_type):
        """
        Retrieves the sqlite string representation of the given attribute.
        The conversion into the correct sqlite representation is critical
        for the correct behaviour and security of the data source.

        @type attribute_value: Object
        @param attribute_value: The attribute value.
        @type attribute_data_type: String
        @param attribute_data_type: The attribute data type.
        @rtype: String
        @return: The sqlite string representation of the given attribute.
        """

        # in case the value is none a null
        if attribute_value == None:
            # returns the sql null value
            return "null"

        # in case the attribute data type is text, normal
        # separators must be applied
        if attribute_data_type == "text":
            # retrieves the escaped attribute value
            escaped_attribute_value = self.escape_text_value(attribute_value)

            # returns the escaped attribute value with the
            # string separators
            return "'" + escaped_attribute_value + "'"
        # in case the attribute data type is date, the date time
        # structure must be converted to a float value
        elif attribute_data_type == "date":
            # retrieves teh attribute value type
            attribute_value_type = type(attribute_value)

            # in case the attribute is given in the date time format
            if attribute_value_type == datetime.datetime:
                # retrieves the date time tuple
                date_time_tuple = attribute_value.utctimetuple()

                # creates the date time timestamp and then
                # converts the timestamp to string representation
                date_time_timestamp = calendar.timegm(date_time_tuple)
                date_time_timestamp_string = str(date_time_timestamp)

                # returns the data time timestamp into
                # string representation
                return date_time_timestamp_string
            # in case the attribute value type is an integer
            # (timestamp value)
            elif attribute_value_type == types.IntType:
                # converts the attribute value (integer)
                # into a float value and then converts it
                # into a string representation
                float_attribute_value = float(attribute_value)
                float_attribute_value_string = str(float_attribute_value)

                # returns the float attribute value converted
                # into a string
                return float_attribute_value_string
            # otherwise it's an unknown
            else:
                # converts the attribute value to string
                # (simple conversion)
                attribute_value_string = str(attribute_value)

                # returns the attribute value converted
                # into string
                return attribute_value_string
        # otherwise it must be a default value and it is
        # converted using the default string converter
        else:
            # converts the attribute value to string
            # (simple conversion)
            attribute_value_string = str(attribute_value)

            # returns the attribute value converted
            # into string
            return attribute_value_string

    def escape_text_value(self, text_value, escape_double_quotes = False):
        """
        Escapes the text value in the sqlite context.
        This escaping process is important even for
        security reasons.

        @type text_value: String
        @param text_value: The text value to be escapted.
        @type escape_double_quotes: bool
        @param escape_double_quotes: If the double quotes should be escaped.
        @rtype: String
        @return: The escaped text value.
        """

        # escapes the quote values
        escaped_text_value = text_value.replace("'", "''")

        # in case the escape double quotes is active
        if escape_double_quotes:
            # escapes the double quote values
            escaped_text_value = escaped_text_value.replace("\"", "\"\"")

        # returns the escaped text value
        return escaped_text_value

    def get_processed_sqlite_attribute_value(self, attribute_value, attribute_data_type):
        """
        Retrieves the sqlite string representation of the given attribute.

        @type attribute_value: Object
        @param attribute_value: The attribute value.
        @type attribute_data_type: String
        @param attribute_data_type: The attribute data type.
        @rtype: Object
        @return: The python object representing the given sqlite object.
        """

        # in case the value is none
        if attribute_value == None:
            return None

        # in case the attribute date type is date
        if attribute_data_type == "date":
            # converts the attribute value to float
            attribute_value = float(attribute_value)

            # converts the attribute value to date time value
            date_time_value = datetime.datetime.utcfromtimestamp(attribute_value)

            # returns the date time (converted) value
            return date_time_value

        # returns the attribute value
        return attribute_value

    def get_entity_sub_classes(self, entity_class):
        """
        Retrieves all the sub classes (recursive descent) from the
        the given entity class.
        This method excludes possible data reference classes while
        gathering the sub classes.

        @type entity_class: Class
        @param entity_class: The entity class to gather the various
        sub classes.
        @rtype: List
        @return: The list of sub classes for the given entity class.
        """

        # start the entity sub sub classes list
        entity_sub_sub_classes = []

        # retrieves the entity subclasses that aren't data references
        # excluding data reference is crucial to avoid possible duplicated
        # "behaviour" in query execution
        entity_sub_classes = [entity_sub_class for entity_sub_class in entity_class.__subclasses__() if not hasattr(entity_sub_class, DATA_REFERENCE_VALUE) or entity_sub_class.data_reference == False]

        # iterates over all the entity direct sub classes
        # to gather the sub sub classes values
        for entity_sub_class in entity_sub_classes:
            # retrieves the sub entity sub classes list from the entity sub class
            # and adds it to the entity "sub sub" classes list
            entity_sub_sub_classes_list = self.get_entity_sub_classes(entity_sub_class)
            entity_sub_sub_classes.extend(entity_sub_sub_classes_list)

        # extends the entity sub classes with the entity sub sub classes
        entity_sub_classes.extend(entity_sub_sub_classes)

        # returns the entity sub classes
        return entity_sub_classes

    def _save_entity_table_data(self, connection, entity_class):
        # creates the entities list
        entities_list = []

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class name
            entity_class_name = entity_class.__name__

            # creates the query string buffer
            query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

            # writes the initial select statement
            query_string_buffer.write("select ")

            # retrieves all the valid class attribute names, removes method values and the name exceptions
            entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

            missing_attributes_list = self._get_missing_attributes(connection, entity_class)

            entity_class_valid_attribute_names = [value for value in entity_class_valid_attribute_names if not value in missing_attributes_list]

            # sets the is first flag
            is_first = True

            for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
                if is_first:
                    is_first = False
                else:
                    query_string_buffer.write(", ")

                query_string_buffer.write(entity_class_valid_attribute_name)

            query_string_buffer.write(" from " + entity_class_name)

            # retrieves the query string value
            query_string_value = query_string_buffer.get_value()

            # executes the query selecting the table
            self.execute_query(cursor, query_string_value)

            # selects the values from the cursor
            # by fetching all the items from it
            values_list = cursor.fetchall()

            for value in values_list:
                # creates a new entity
                entity = entity_class()

                # starts the index
                index = 0

                for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
                    entity_class_valid_attribute_value = value[index]

                    setattr(entity, entity_class_valid_attribute_name, entity_class_valid_attribute_value)

                    # increments the index
                    index += 1

                # iterates over all the missing attributes and sets them to invalid
                # none value
                for missing_attribute in missing_attributes_list:
                    # sets the none value in the missing attribute
                    setattr(entity, missing_attribute, None)

                # adds the entity to the entities list
                entities_list.append(entity)
        finally:
            # closes the cursor
            cursor.close()

        # returns the entities list
        return entities_list

    def _restore_entity_table_data(self, connection, entity_class, entities_list):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class name
            entity_class_name = entity_class.__name__

            # iterates over all the entities in the entities list
            for entity in entities_list:
                # creates the query string buffer
                query_string_buffer = colony.libs.string_buffer_util.StringBuffer()

                # writes the insert into statement
                query_string_buffer.write("insert into " + entity_class_name + "(")

                # retrieves all the valid class attribute names, removes method values and the name exceptions
                entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

                # sets the is first flag
                is_first = True

                for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
                    if hasattr(entity, entity_class_valid_attribute_name):
                        if is_first:
                            is_first = False
                        else:
                            query_string_buffer.write(", ")

                        query_string_buffer.write(entity_class_valid_attribute_name)

                query_string_buffer.write(") values (")

                # sets the is first flag
                is_first = True

                for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
                    if hasattr(entity, entity_class_valid_attribute_name):
                        entity_valid_attribute_value = getattr(entity, entity_class_valid_attribute_name)

                        entity_class_valid_attribute_value = getattr(entity_class, entity_class_valid_attribute_name)

                        # retrieves the entity class valid attribute value data type
                        entity_class_valid_attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_class_valid_attribute_name)

                        # retrieves the entity valid attribute sqlite string value
                        entity_valid_attribute_value_sqlite_string_value = self.get_attribute_sqlite_string_value(entity_valid_attribute_value, entity_class_valid_attribute_data_type)

                        # in case the it's the first
                        # attribute
                        if is_first:
                            # unsets the is first flag
                            is_first = False
                        else:
                            # writes a comma to the query string
                            query_string_buffer.write(", ")

                        query_string_buffer.write(entity_valid_attribute_value_sqlite_string_value)

                query_string_buffer.write(")")

                # retrieves the query string value
                query_string_value = query_string_buffer.get_value()

                # executes the query inserting the record into the table
                self.execute_query(cursor, query_string_value)
        finally:
            # closes the cursor
            cursor.close()

    def _get_unsynced_attributes(self, connection, entity_class):
        # creates the unsynced attributes list
        unsynced_attributes_list = []

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # retrieves the entity class name
        entity_class_name = entity_class.__name__

        # retrieves all the valid class attribute names, removes method values and the name exceptions
        entity_class_valid_attribute_names = self.get_entity_class_attribute_names(entity_class)

        # retrieves all the valid class attribute values
        entity_class_valid_attribute_values = self.get_entity_class_attribute_values(entity_class)

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # creates the initial query string value
            query_string_value = "pragma table_info(" + entity_class_name + ")"

            # executes the query retrieving the values
            self.execute_query(cursor, query_string_value)

            # selects the table information from the cursor
            # by fetching all the items from it
            table_information_list = cursor.fetchall()

            # creates the table information map
            table_information_map = {}

            # iterates over all the table information
            for table_information_item in table_information_list:
                # retrieves the attribute name
                attribute_name = table_information_item[1]

                # retrieves the attribute data type
                attribute_data_type = table_information_item[2]

                # sets the attribute data type in the table information map
                table_information_map[attribute_name] = attribute_data_type

            # starts the index value
            index = 0

            # iterates over all the entity class valid attribute names
            for entity_class_valid_attribute_name in entity_class_valid_attribute_names:
                # in case the entity class valid attribute name is not defined
                # in the table information map (attribute does not exists in the data source)
                if not entity_class_valid_attribute_name in table_information_map:
                    # in case the attribute missing is of type relation
                    if self.is_attribute_name_relation(entity_class_valid_attribute_name, entity_class):
                        # adds the attribute to the unsynced attributes with reason
                        # relation attribute inexistent
                        unsynced_attributes_list.append((entity_class_valid_attribute_name, INEXISTING_RELATION_ATTRIBUTE_REASON_CODE))
                    else:
                        # adds the attribute to the unsynced attributes with reason
                        # attribute inexistent
                        unsynced_attributes_list.append((entity_class_valid_attribute_name, INEXISTING_ATTRIBUTE_REASON_CODE))
                # the attribute exists in the data source
                else:
                    # retrieves the attribute data type
                    attribute_data_type = table_information_map[entity_class_valid_attribute_name]

                    # retrieves the entity class valid attribute value
                    entity_class_valid_attribute_value = entity_class_valid_attribute_values[index]

                    # retrieves the entity class valid attribute data type
                    entity_class_valid_attribute_data_type = self.get_attribute_data_type(entity_class_valid_attribute_value, entity_class, entity_class_valid_attribute_name)

                    # retrieves the entity class valid attribute target data type
                    entity_class_valid_attribute_target_data_type = DATA_TYPE_MAP[entity_class_valid_attribute_data_type]

                    # checks if the data type in both the data source and schema are the same
                    if not entity_class_valid_attribute_target_data_type == attribute_data_type:
                        # adds the attribute to the unsynced attributes with reason
                        # attribute type mismatch
                        unsynced_attributes_list.append((entity_class_valid_attribute_name, INVALID_ATTRIBUTE_TYPE_REASON_CODE))

                # increments the index
                index += 1
        finally:
            # closes the cursor
            cursor.close()

        # returns unsynced attributes list
        return unsynced_attributes_list

    def _get_unsynced_relation_attributes(self, connection, entity_class):
        # creates the unsynced attributes list
        unsynced_attributes_list = []

        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # creates the cursor for the given connection
        cursor = database_connection.cursor()

        try:
            # retrieves the entity class valid indirect attribute names
            entity_class_valid_indirect_attribute_names = self.get_entity_class_indirect_attribute_names(entity_class)

            # iterates over all the entity class valid indirect attribute names
            # and checks if any of them is not mapped in a relation table (but only if it is a many-to many relation)
            for entity_class_valid_indirect_attribute_name in entity_class_valid_indirect_attribute_names:
                # retrieves the relation attributes for the given attribute name in the given entity class
                relation_attributes = self.get_relation_attributes(entity_class, entity_class_valid_indirect_attribute_name)

                # retrieves the relation type field
                relation_type_field = relation_attributes[RELATION_TYPE_FIELD]

                # in case the relation is not of type many-to-many
                if not relation_type_field == MANY_TO_MANY_RELATION:
                    # continues the loop
                    continue

                # retrieves the join table field
                join_table_field = relation_attributes[JOIN_TABLE_FIELD]

                # retrieves the attribute column name field
                attribute_column_name_field = relation_attributes[ATTRIBUTE_COLUMN_NAME_FIELD]

                # tests to check if exists a table definition for the join table
                exists_table_definition = self.exists_table_definition(connection, join_table_field)

                # in case there is a table definition for the relation table
                if exists_table_definition:
                    # tests to check if the join field definition exists in the join table
                    exists_join_field_definition = self.exists_table_column_definition(connection, join_table_field, attribute_column_name_field);

                    # in case the join field definition does not exist
                    # in the join table it must be created
                    if not exists_join_field_definition:
                        # adds the attribute to the unsynced attributes with reason
                        # attribute inexistent
                        unsynced_attributes_list.append((entity_class_valid_indirect_attribute_name, INEXISTING_ATTRIBUTE_REASON_CODE))
                # otherwise there is no table definition and it must
                # be created
                else:
                    # adds the attribute to the unsynced attributes with reason
                    # attribute inexistent
                    unsynced_attributes_list.append((entity_class_valid_indirect_attribute_name, INEXISTING_ATTRIBUTE_REASON_CODE))
        finally:
            # closes the cursor
            cursor.close()

        # returns unsynced attributes list
        return unsynced_attributes_list

    def _get_missing_attributes(self, connection, entity_class):
        # retrieves the unsynced attributes list
        unsynced_attributes_list = self._get_unsynced_attributes(connection, entity_class)

        # filters the unsynced attributes list to create the missing attributes list
        missing_attributes_list = [value[0] for value in unsynced_attributes_list if value[1] in INEXISTING_ATTRIBUTE_REASON_CODES]

        # returns the missing attributes list
        return missing_attributes_list

    def _set_entity_fields(self, entity, fields):
        """
        Sets the given fields into the entity.
        In order to avoid problems while setting fields into an
        entity a new entity is created and the fields are set
        into the entity that does not inherit from object
        and so does not protected the field setting.

        @type entity: Entity
        @param entity: The entity to set the fields.
        @type fields: List
        @param fields: The list of fields to be set.
        @rtype: Entity
        @return: The entity with the fields set.
        """

        # in case no field are defined
        if not fields:
            # returns the entity itself
            return entity

        # creates a new (default) entity
        new_entity = DefaultEntity()

        # iterates over all the field to populate
        # the entity
        for field in fields:
            # retrieve the field value
            # and sets it into the new entity
            field_value = getattr(entity, field)
            setattr(new_entity, field, field_value)

        # returns the new entity
        return new_entity

    def _process_filters(self, query_string_buffer, entity_class, filters, is_first = True):
        """
        Processes the given list of filters, populating the query
        string buffer with the appropriate clauses.
        The population of the query string buffer is made using
        a recursive descent over the filters.

        @type query_string_buffer: StringBuffer
        @param query_string_buffer: The query string buffer currently
        in use, for the query creation.
        @type entity_class: EntityClass
        @param entity_class: The entity class to be used as reference
        for the filters.
        @param filters: List
        @param filters: The list of filters to be processed.
        @type is_first: bool
        @param is_first: Flag that indicated if this is the first where clause
        to be present in the buffer.
        """

        # iterates over all the filters
        # to process them
        for filter in filters:
            # in case the is first flag
            # is set
            if is_first:
                # adds the where operator in the query
                # string buffer
                query_string_buffer.write(" where (")

                # unsets the is first flag
                is_first = False
            # otherwise the and operator
            # must be added to the query
            # string buffer
            else:
                # adds the and operator in the query
                # string buffer
                query_string_buffer.write(" and (")

            # retrieves the filter type and then uses
            # it to retrieve the appropriate filter method
            filter_type = filter["type"]
            filter_method = getattr(self, "_process_filter_" + filter_type)

            # calls the filter method, updating the contents of the query
            # string buffer accordingly
            filter_method(query_string_buffer, entity_class, filter)

            # writes the end of the filter
            query_string_buffer.write(")")

    def _process_filter_equals(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the equals filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name and value
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # retrieves the filter field class value
            filter_field_class_value = getattr(entity_class, filter_field_name)

            # retrieves the filter value value data type
            # and then uses it to convert the value to the appropriate
            # representation in the sqlite type system
            filter_value_data_type = self.get_attribute_data_type(filter_field_class_value, entity_class, filter_field_name)
            filter_field_value_sqlite_string_value = self.get_attribute_sqlite_string_value(filter_field_value, filter_value_data_type)

            # writes the equals clause in the query string buffer
            query_string_buffer.write(filter_field_name + " = " + filter_field_value_sqlite_string_value)

    def _process_filter_not_equals(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the not equals filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name and value
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # retrieves the filter field class value
            filter_field_class_value = getattr(entity_class, filter_field_name)

            # retrieves the filter value value data type
            # and then uses it to convert the value to the appropriate
            # representation in the sqlite type system
            filter_value_data_type = self.get_attribute_data_type(filter_field_class_value, entity_class, filter_field_name)
            filter_field_value_sqlite_string_value = self.get_attribute_sqlite_string_value(filter_field_value, filter_value_data_type)

            # writes the not equals clause in the query string buffer
            query_string_buffer.write("not " + filter_field_name + " = " + filter_field_value_sqlite_string_value)

    def _process_filter_in(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the in filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name and value
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # retrieves the filter field class value
            filter_field_class_value = getattr(entity_class, filter_field_name)

            # retrieves the entity class id attribute value data type
            filter_value_data_type = self.get_attribute_data_type(filter_field_class_value, entity_class, filter_field_name)

            # retrieves the filter field value value sqlite string value list to then
            # convert into an sql sequence representation
            filter_field_value_sqlite_string_value_list = [self.get_attribute_sqlite_string_value(value, filter_value_data_type) for value in filter_field_value]
            filter_field_value_sqlite_string_value = "(" + ", ".join(filter_field_value_sqlite_string_value_list) + ")"

            # writes the in clause in the query string buffer
            query_string_buffer.write(filter_field_name + " in " + filter_field_value_sqlite_string_value)

    def _process_filter_not_in(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the not in filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name and value
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # retrieves the filter field class value
            filter_field_class_value = getattr(entity_class, filter_field_name)

            # retrieves the entity class id attribute value data type
            filter_value_data_type = self.get_attribute_data_type(filter_field_class_value, entity_class, filter_field_name)

            # retrieves the filter field value value sqlite string value list to then
            # convert into an sql sequence representation
            filter_field_value_sqlite_string_value_list = [self.get_attribute_sqlite_string_value(value, filter_value_data_type) for value in filter_field_value]
            filter_field_value_sqlite_string_value = "(" + ", ".join(filter_field_value_sqlite_string_value_list) + ")"

            # writes the in clause not in the query string buffer
            query_string_buffer.write("not " + filter_field_name + " in " + filter_field_value_sqlite_string_value)

    def _process_filter_like(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields and
        # like filter type
        filter_fields = filter["fields"]
        like_filter_type = filter.get("like_filter_type", "both")

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the like filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name and value
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # creates a new buffer for the filter field value
            filter_field_value_buffer = colony.libs.string_buffer_util.StringBuffer()

            # sets the is first filter field
            # value flag
            is_first_filter_field_value = True

            # iterates over all the splitted filter
            # field values (separates the words for the like)
            for splitted_filter_value in filter_field_value.split():
                # in case the is first filter field
                # value is set
                if is_first_filter_field_value:
                    # unsets the is first filter field
                    # value
                    is_first_filter_field_value = False
                # otherwise the wildcard operator must
                # be added to the filter field value
                else:
                    # writes the wildcard operator
                    # in the filter field value buffer
                    filter_field_value_buffer.write("%")

                # writes the splitted filter value into
                # the filter field value buffer
                filter_field_value_buffer.write(splitted_filter_value)

            # writes the initial part of the like operand
            # in the query string buffer
            query_string_buffer.write(filter_field_name + " like ")

            # in case the like filter type is left
            # or both, the initial part must be wildcard
            if like_filter_type in ("left", "both"):
                # writes the wildcard to the query
                # string buffer
                query_string_buffer.write("'%")
            # otherwise no wildcard is set at the
            # initial (left) part of the string
            else:
                # writes the initial string to the
                # query string buffer
                query_string_buffer.write("'")

            # retrieves the filter field value string (from buffer) and
            # writes it into the query string buffer
            filter_field_value_string = filter_field_value_buffer.get_value()
            query_string_buffer.write(filter_field_value_string)

            # in case the like filter type is right
            # or both, the final part must be wildcard
            if like_filter_type in ("right", "both"):
                # writes the wildcard to the query
                # string buffer
                query_string_buffer.write("%'")
            # otherwise no wildcard is set at the
            # final (right) part of the string
            else:
                # writes the final string to the
                # query string buffer
                query_string_buffer.write("'")

    def _process_filter_greater(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the greater filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name and value
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # retrieves the filter field class value
            filter_field_class_value = getattr(entity_class, filter_field_name)

            # retrieves the filter value value data type
            # and then uses it to convert the value to the appropriate
            # representation in the sqlite type system
            filter_value_data_type = self.get_attribute_data_type(filter_field_class_value, entity_class, filter_field_name)
            filter_field_value_sqlite_string_value = self.get_attribute_sqlite_string_value(filter_field_value, filter_value_data_type)

            # writes the greater clause not in the query string buffer
            query_string_buffer.write(filter_field_name + " > " + filter_field_value_sqlite_string_value)

    def _process_filter_lesser(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the lesser filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name and value
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # retrieves the filter field class value
            filter_field_class_value = getattr(entity_class, filter_field_name)

            # retrieves the filter value value data type
            # and then uses it to convert the value to the appropriate
            # representation in the sqlite type system
            filter_value_data_type = self.get_attribute_data_type(filter_field_class_value, entity_class, filter_field_name)
            filter_field_value_sqlite_string_value = self.get_attribute_sqlite_string_value(filter_field_value, filter_value_data_type)

            # writes the lesser clause not in the query string buffer
            query_string_buffer.write(filter_field_name + " < " + filter_field_value_sqlite_string_value)

    def _process_filter_is_null(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the is null filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name
            filter_field_name = filter_field["name"]

            # writes the is null clause not in the query string buffer
            query_string_buffer.write(filter_field_name + " is null")

    def _process_filter_is_not_null(self, query_string_buffer, entity_class, filter):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the is not null filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or ")

            # retrieves the filter field name
            filter_field_name = filter_field["name"]

            # writes the is not null clause not in the query string buffer
            query_string_buffer.write(filter_field_name + " is not null")

    def _process_filter_or(self, query_string_buffer, entity_class, filter):
        # retrieves the filters
        filters = filter["filters"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter
        # to set the or filter
        for _filter in filters:
            # in case the is first flag
            # is set
            if is_first:
                # writes the start of the filter
                query_string_buffer.write("(")

                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # string buffer
                query_string_buffer.write(" or (")

            # retrieves the filter type and then uses
            # it to retrieve the appropriate filter method
            filter_type = _filter["type"]
            filter_method = getattr(self, "_process_filter_" + filter_type)

            # calls the filter method, updating the contents of the query
            # string buffer accordingly
            filter_method(query_string_buffer, entity_class, _filter)

            # writes the end of the filter
            query_string_buffer.write(")")

class BufferedEntities:
    """
    The buffered entities class.
    This class controls a buffer of entities for lazy retrieval.
    """

    buffered_entities_map = {}
    """ The buffered entities map """

    def __init__(self):
        """
        Constructor of the class.
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

        # in case the entity class does not exist in the
        # buffered entities map
        if not entity_class in self.buffered_entities_map:
            # sets the entity class in the buffered entities
            # map as a new empty map
            self.buffered_entities_map[entity_class] = {}

        # retrieves the entity class map from the buffered entities map
        buffered_entities_map_entity_class_map = self.buffered_entities_map[entity_class]

        # sets the entity in the entity class map for the id value
        buffered_entities_map_entity_class_map[id_value] = entity

    def get_entity(self, entity_class, id_value):
        """
        Retrieves an entity from the buffer.

        @type entity_class: Class
        @param entity_class: The entity class of the entity to retrieve.
        @type id_value: Object
        @param id_value: The id of the entity to retrieve.
        @rtype: Entity
        @return: The retrieved entity or none in case it's not found.
        """

        # retrieves the entity sub classes
        entity_sub_classes = self.get_entity_sub_classes(entity_class)

        # appends the entity class to the valid entity sub classes list
        entity_sub_classes.append(entity_class)

        # retrieves the valid entity sub classes
        valid_entity_sub_classes = [value for value in entity_sub_classes if value in self.buffered_entities_map]

        # in case no valid entity sub classes are found
        if not valid_entity_sub_classes:
            # returns none (invalid)
            return None

        # iterates over all the valid entity sub classes
        # trying to find the entity for the id value
        for valid_entity_sub_class in valid_entity_sub_classes:
            # retrieves the entity class map for the "current" entity sub class
            buffered_entities_map_entity_class_map = self.buffered_entities_map[valid_entity_sub_class]

            # in case the id value does not exists in the buffered
            # entities map entity class map
            if not id_value in buffered_entities_map_entity_class_map:
                # continues the loop
                continue

            # retrieves the entity from the buffered entities map entity class map
            entity = buffered_entities_map_entity_class_map[id_value]

            # returns the buffered entity
            return entity

        # returns none (invalid)
        return None

    def get_entity_sub_classes(self, entity_class):
        """
        Retrieves the entity sub classes from the given
        entity class.

        @type entity_class: Class
        @param entity_class: The entity class to retrieve
        the sub classes.
        @rtype: List
        @return: The sub classes for the given entity class.
        """

        # retrieves the entity class direct sub classes
        entity_sub_classes = entity_class.__subclasses__()

        # start the entity sub sub classes list
        entity_sub_sub_classes = []

        # iterates over all the entity direct sub classes
        for entity_sub_class in entity_sub_classes:
            # retrieves the sub entity sub classes list
            entity_sub_sub_classses_list = self.get_entity_sub_classes(entity_sub_class)

            # extends the entity sub sub classes list sub entity sub classes list
            entity_sub_sub_classes.extend(entity_sub_sub_classses_list)

        # extends the entity sub classes with the entity sub sub classes
        entity_sub_classes.extend(entity_sub_sub_classes)

        # returns the entity sub classes
        return entity_sub_classes

class DefaultEntity:
    """
    The default entity class.
    This class does not inherit from the object
    class in order to avoid attribute protection.
    """

    pass