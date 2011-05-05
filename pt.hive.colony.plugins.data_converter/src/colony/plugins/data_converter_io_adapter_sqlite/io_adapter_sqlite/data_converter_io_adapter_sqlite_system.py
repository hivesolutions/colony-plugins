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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import types
import sqlite3

import data_converter_io_adapter_sqlite_exceptions

ENTITY_OBJECT_ID_VALUE = "entity_object_id"

EQUALS_VALUE = "="

INPUT_ATTRIBUTE_HANDLERS_VALUE = "input_attribute_handlers"

INPUT_ENTITY_HANDLERS_VALUE = "input_entity_handlers"

INPUT_FILE_PATH_VALUE = "input_file_path"

NAME_VALUE = "name"

OBJECT_ID_VALUE = "object_id"

OUTPUT_ATTRIBUTE_HANDLERS_VALUE = "output_attribute_handlers"

OUTPUT_ENTITY_HANDLERS_VALUE = "output_entity_handlers"

OUTPUT_FILE_PATH_VALUE = "output_file_path"

QUOTE_DOUBLE_VALUE = "''"

RELATION_VALUE = "Relation"

RELATED_ENTITY_OBJECT_ID_VALUE = "related_entity_object_id"

VARCHAR_VALUE = "varchar(255)"

RELATION_COLUMN_NAMES = (
    ENTITY_OBJECT_ID_VALUE,
    RELATED_ENTITY_OBJECT_ID_VALUE
)
""" List with the names of the columns used to map relations in relation tables """

RELATION_TABLE_NAME_SEPARATOR = "__"
""" Separator character used in the relation table name to separate the tokens """

CREATE_TABLE_SQL_QUERY_TEMPLATE = "create table %s(%s);"
""" Query used to create a new table """

INSERT_ROW_SQL_QUERY_TEMPLATE = "insert into %s(%s) values(%s);"
""" Query used to insert a new row """

SELECT_TABLE_SQL_QUERY_TEMPLATE = "select %s from %s;"
""" Query used to retrieve a table's rows """

SELECT_TABLE_INFO_SQL_QUERY_TEMPLATE = "pragma table_info(%s);"
""" Query used to retrieve information about a database table """

SELECT_TABLE_NAMES_SQL_QUERY = "select name from sqlite_master;"
""" Query used to retrieve the names of the tables that exist in the sqlite database """

class IoAdapterSqlite:
    """
    Provides a means to load and save the intermediate structure by using
    the colony business sqlite.
    """

    io_adapter_sqlite_plugin = None
    """ Io adapter sqlite plugin """

    connection_table_names_map = {}
    """ Dictionary relating an sqlite connection with the names of the tables exist in this connection """

    def __init__(self, io_adapter_sqlite_plugin):
        """
        Constructor of the class.

        @type io_adapter_sqlite_plugin: IoAdapterSqlite
        @param io_adapter_sqlite_plugin: Input output adapter sqlite plugin.
        """

        self.io_adapter_sqlite_plugin = io_adapter_sqlite_plugin
        self.connection_table_names_map = {}

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the entity
        manager with the specified options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the
        data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # extracts the mandatory options
        file_path = configuration.get_option(INPUT_FILE_PATH_VALUE)

        # raises and exception in case the specified file does not exist
        if not os.path.exists(file_path):
            raise data_converter_io_adapter_sqlite_exceptions.IoAdapterSqliteFileNotFound(file_path)

        # creates the sqlite connection
        connection = sqlite3.connect(file_path)

        try:
            # loads the intermediate structure entities' attributes
            self.load_attributes(intermediate_structure, connection, options)

            # loads the intermediate structure entities' relations
            self.load_relations(intermediate_structure, connection, options)
        finally:
            # closes the sqlite connection
            self.close_connection(connection)

    def load_attributes(self, intermediate_structure, connection, options):
        """
        Loads the intermediate structure's entities' attributes from the sqlite connection.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type connection: Connection
        @param connection: Connection to the database.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # retrieves the name of all tables in the database
        table_names = self.get_table_names(connection)

        # creates an entity for each table row and populates it with the row's field values
        for table_name in table_names:

            # retrieves the table's column names
            column_names = self.get_table_column_names(connection, table_name)

            # retrieves the table's rows with the specified fields
            rows = self.get_rows(connection, table_name, column_names)

            # iterates through the table rows creating an entity for each row with its contents
            self.load_attributes_rows(intermediate_structure, connection, table_name, rows, options)

    def load_attributes_rows(self, intermediate_structure, connection, table_name, rows, options):
        """
        Loads the intermediate structure's entities' attributes from the provided table rows.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type connection: Connection
        @param connection: Connection to the database.
        @type table_name: String
        @param table_name: Name of the table the provided rows belong to.
        @type rows: List
        @param rows: List of table rows where to extract the entity attributes from.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # extracts the non-mandatory options
        input_entity_handlers = options.get(INPUT_ENTITY_HANDLERS_VALUE, [])
        input_attribute_handlers = options.get(INPUT_ATTRIBUTE_HANDLERS_VALUE, [])

        # retrieves the table's column names
        column_names = self.get_table_column_names(connection, table_name)

        # creates an entity for each row and populates it with the row's fields
        for row in rows:

            # creates the intermediate entity and loads the stored object id
            entity = intermediate_structure.create_entity(table_name)

            # copies the row's field values to the entity
            for column_name_index in range(len(column_names)):
                column_name = column_names[column_name_index]
                field_value = row[column_name_index]

                # passes the field value through the configured input attribute handlers
                for input_attribute_handler in input_attribute_handlers:
                    field_value = input_attribute_handler(intermediate_structure, entity, field_value)

                # @todo: this is a temporary hack, do not use the table's object ids to build the intermediate structure
                if column_name == OBJECT_ID_VALUE:
                    entity.object_id = int(field_value)
                else:
                    # sets the field value as an entity attribute
                    entity.set_attribute(column_name, field_value)

                # passes the field value through the configured input entity handlers
                for input_entity_handler in input_entity_handlers:
                    field_value = input_entity_handler(intermediate_structure, entity)

    def load_relations(self, intermediate_structure, connection, options):
        """
        Loads the intermediate structure's entities' relations with the sqlite connection.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type connection: Connection
        @param connection: Connection to the database.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # retrieves the names of all relation tables in the database
        table_names = self.get_table_names(connection)
        relation_table_names = [table_name for table_name in table_names if table_name.endswith(RELATION_VALUE)]

        # associates the intermediate structure entities specified in the relation tables
        for relation_table_name in relation_table_names:

            # retrieves the table's rows with the specified fields
            rows = self.get_rows(connection, table_name, RELATION_COLUMN_NAMES)

            # iterates through the relation rows associating the intermediate structure entities indicated by them
            self.load_relations_rows(intermediate_structure, connection, relation_table_name, rows, options)

    def load_relations_rows(self, intermediate_structure, connection, table_name, rows):
        """
        Loads the intermediate structure's entities' relations from the provided table rows.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type connection: Connection
        @param connection: Connection to the database.
        @type table_name: String
        @param table_name: Name of the table from where the provided rows belong.
        @type rows: List
        @param rows: List of table rows where to extract the table relations from.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # extracts information about the relation table from its name
        _entity_name, relation_attribute_name, _related_entity_name, _relation_value = table_name.split(RELATION_TABLE_NAME_SEPARATOR)

        # creates an intermediate entity for each row and populates it with the row's fields
        for row in rows:
            # retrieves the entities' object ids
            entity_object_id = row[0]
            entity_object_id = int(entity_object_id)
            related_entity_object_id = row[1]
            related_entity_object_id = int(related_entity_object_id)

            # retrieves the entity and the related entity
            entity_index = self.get_intermediate_entity_index(entity_object_id)
            entity = intermediate_structure.get_entity(entity_index)
            related_entity_index = self.get_intermediate_entity_index(related_entity_object_id)
            related_entity = intermediate_structure.get_entity(related_entity_index)

            # updates the entity's relation attribute
            entity_attribute_value = entity.get_attribute(relation_attribute_name)
            if type(entity_attribute_value) == types.ListType:
                entity_attribute_value.append(related_entity)
            else:
                entity_attribute_value = related_entity
            entity.set_attribute(relation_attribute_name, entity_attribute_value)

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure at the location and with the characteristics
        defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure
        with the sqlite.
        """

        # extracts the mandatory options
        file_path = configuration.get_option(OUTPUT_FILE_PATH_VALUE)

        # creates the sqlite connection
        connection = sqlite3.connect(file_path)

        try:
            # saves the intermediate structure entities' attributes
            self.save_attributes(intermediate_structure, connection, options)

            # saves the intermediate structure entities' relations
            self.save_relations(intermediate_structure, connection, options)

            # commits and closes the sqlite connection
            connection.commit()
        finally:
            # closes the sqlite connection
            self.close_connection(connection)

    def save_attributes(self, intermediate_structure, connection, options):
        """
        Saves the intermediate structure's entities' attributes with the sqlite connection.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type connection: Connection
        @param connection: Connection to the database.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure
        with the sqlite.
        """

        # retrieves the column names for each table
        table_name_column_names_map = {}
        entities = intermediate_structure.get_entities()
        for entity in entities:
            entity_name = entity.get_name()
            attribute_names = [attribute_name for attribute_name, attribute_value in entity.get_attributes().iteritems() if not type(attribute_value) in (types.ListType, types.InstanceType)]
            if not entity_name in table_name_column_names_map:
                table_name_column_names_map[entity_name] = [
                    OBJECT_ID_VALUE
                ]
            table_name_column_names_map[entity_name].extend(attribute_names)

        # creates the tables where to store the intermediate entities
        for table_name in table_name_column_names_map:
            attribute_names = list(set(table_name_column_names_map[table_name]))
            self.create_table(connection, table_name, attribute_names)

        # iterates through the entities saving their attributes as rows in the correspondent entity table
        self.save_attributes_entities(intermediate_structure, connection, entities, options)

    def save_attributes_entities(self, intermediate_structure, connection, entities, options):
        """
        Saves the intermediate structure's entities' attributes with the sqlite connection.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type connection: Connection
        @param connection: Connection to the database.
        @type entities: List
        @param entities: List of entities whose attributes one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure
        with the sqlite.
        """

        # extracts the non-mandatory options
        output_entity_handlers = options.get(OUTPUT_ENTITY_HANDLERS_VALUE, [])
        output_attribute_handlers = options.get(OUTPUT_ATTRIBUTE_HANDLERS_VALUE, [])

        # inserts a row with each intermediate entity's contents
        for entity in entities:
            entity_object_id = entity.get_object_id()
            entity_name = entity.get_name()

            # passes the entity through the specified output entity handlers
            for output_entity_handler in output_entity_handlers:
                entity = output_entity_handler(intermediate_structure, entity)

            # creates the list of attributes names and values to insert in the row that represents the entity
            non_relation_attribute_names = self.get_non_relation_attribute_names(entity)
            non_relation_attribute_values = [entity_object_id]
            non_relation_attribute_values.extend([entity.get_attribute(attribute_name) for attribute_name in non_relation_attribute_names])
            non_relation_attribute_names_with_object_id = [OBJECT_ID_VALUE]
            non_relation_attribute_names_with_object_id.extend(non_relation_attribute_names)

            # passes the attributes through the specified output attribute handlers
            for output_attribute_handler in output_attribute_handlers:
                non_relation_attribute_values = [output_attribute_handler(intermediate_structure, entity, non_relation_attribute_value) for non_relation_attribute_value in non_relation_attribute_values]

            # inserts a row in the database representing this entity
            self.insert_row(connection, entity_name, non_relation_attribute_names_with_object_id, non_relation_attribute_values)

    def save_relations(self, intermediate_structure, connection, options):
        """
        Saves the intermediate structure's entities' relations with the sqlite connection.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type connection: Connection
        @param connection: Connection to the database.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure
        with the sqlite.
        """

        # creates an entity for each intermediate entity in the internal structure and populates it with its attributes
        entities = intermediate_structure.get_entities()
        for entity in entities:

            # iterates through the entity's relation attributes saving the relations to the sqlite database
            self.save_relations_relation_attributes(intermediate_structure, connection, entity, options)

    def save_relations_relation_attributes(self, intermediate_structure, connection, entity, options):
        """
        Saves the intermediate structure's entities' relations of the specified entity with the sqlite connection.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type connection: Connection
        @param connection: Connection to the database.
        @type entity: Entity
        @param entity: Entity whose relations one wants to save in the database.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure
        with the sqlite.
        """

        # retrieves the entity's relation attribute values and saves them in the database
        relation_attribute_names = self.get_relation_attribute_names(entity)
        for relation_attribute_name in relation_attribute_names:

            # iterates though the related entities in the relation attribute saving the relation between the entity and that one
            self.save_relations_relation_attributes_related_entities(intermediate_structure, connection, entity, relation_attribute_name, options)

    def save_relations_relation_attributes_related_entities(self, intermediate_structure, connection, entity, relation_attribute_name, options):
        """
        Saves the intermediate structure's entities' relations of the specified entity with
        the sqlite connection.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type connection: Connection
        @param connection: Connection to the database.
        @type entity: Entity
        @param entity: Entity whose relations one wants to save in the database.
        @type relation_attribute_name: String
        @param relation_attribute_name: Name of the entity's relation attribute whose related entities
        association one wants to store in the database.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure
        with the sqlite.
        """

        entity_name = entity.get_name()
        entity_object_id = entity.get_object_id()

        # encapsulates the relation attribute's value in a list in case its a "to one" relation in order to reuse the following code
        related_entity_or_entities = entity.get_attribute(relation_attribute_name)
        if type(related_entity_or_entities) == types.ListType:
            related_entities = related_entity_or_entities
        elif related_entity_or_entities:
            related_entities = [related_entity_or_entities]
        else:
            related_entities = []

        # retrieves entity that corresponds to the intermediate entity that is in the relation attribute adds it to the entity's relation attribute
        for related_entity in related_entities:
            related_entity_name = related_entity.get_name()
            related_entity_object_id = related_entity.get_object_id()

            # raises an exception in case the related entity is not found
            if not related_entity:
                raise data_converter_io_adapter_sqlite_exceptions.IoAdapterSqliteEntityClassNotFound(entity_name)

            # creates a relation table in case it doesn't exist yet
            relation_table_name = entity_name + RELATION_TABLE_NAME_SEPARATOR + relation_attribute_name + RELATION_TABLE_NAME_SEPARATOR + related_entity_name + RELATION_TABLE_NAME_SEPARATOR + RELATION_VALUE
            self.create_table(connection, relation_table_name, RELATION_COLUMN_NAMES)

            # adds a row to the relation table used to indicate that the two entities are related to each other
            relation_column_values = [entity_object_id, related_entity_object_id]
            self.insert_row(connection, relation_table_name, RELATION_COLUMN_NAMES, relation_column_values)

    def get_intermediate_entity_index(self, intermediate_entity_object_id):
        """
        Retrieves the index used to retrieve an entity from the intermediate structure.

        @type intermediate_entity_object_id: int
        @param intermediate_entity_object_id: Intermediate structure object id for the entity one wants to retrieve.
        @rtype: String
        @return: String with the index that can be used to retrieve an entity from the intermediate structure.
        """

        intermediate_entity_index = (
            OBJECT_ID_VALUE, EQUALS_VALUE, intermediate_entity_object_id
        )

        return intermediate_entity_index

    def get_non_relation_attribute_names(self, entity):
        """
        Retrieves the names of the provided intermediate structure entity's non
        relation attributes.

        @type entity: Entity
        @param entity: The entity whose non relation attribute names one wants
        to retrieve.
        @rtype: List
        @return: List with the names of the entity's non relation attributes.
        """

        entity_attributes_map = entity.get_attributes()
        entity_attributes_names = entity_attributes_map.keys()
        non_relation_attribute_names = [attribute_name for attribute_name in entity_attributes_names if type(entity.get_attribute(attribute_name)) not in (types.ListType, types.InstanceType)]

        return non_relation_attribute_names

    def get_relation_attribute_names(self, entity):
        """
        Retrieves the names of the provided intermediate structure entity's
        relation attributes.

        @type entity: Entity
        @param entity: The entity whose relation attribute names one wants
        to retrieve.
        @rtype: List
        @return: List with the names of the entity's relation attributes.
        """

        entity_attributes_map = entity.get_attributes()
        entity_attributes_names = entity_attributes_map.keys()
        relation_attribute_names = [attribute_name for attribute_name in entity_attributes_names if type(entity.get_attribute(attribute_name)) in (types.ListType, types.InstanceType)]

        return relation_attribute_names

    def close_connection(self, connection):
        """
        Closes the sqlite connection and releases all resources
        related with it.

        @type connection: Connection
        @param connection: Database connection.
        """

        # removes the connection from the connection table names map
        if connection in self.connection_table_names_map:
            del self.connection_table_names_map[connection]

        # closes the connection
        connection.close()

    def execute_query(self, connection, query):
        """
        Executes a sqlite query.

        @type connection: Connection
        @param connection: Database connection.
        @type query: String
        @param query: Query one wants to perform.
        @rtype: Dictionary
        @return results: Dictionary with the queries' results.
        """

        cursor = connection.cursor()

        try:
            cursor.execute(query)
            results = cursor.fetchall()
        finally:
            cursor.close()

        return results

    def table_exists(self, connection, table_name):
        """
        Indicates if the specified table exists.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: String
        @param table_name: Name of the table.
        @rtype: bool
        @return: Boolean indicating if the table exists in the specified database.
        """

        # creates an entry where to store the tables that exist in this connection
        # in case the entry doesn't exist yet
        if not connection in self.connection_table_names_map:
            self.connection_table_names_map[connection] = []

        # returns true in case the table is already in the list of existing tables for
        # this connection
        if table_name in self.connection_table_names_map[connection]:
            return True

        # queries the database to figure out if the table exists
        table_info_sql_query = SELECT_TABLE_INFO_SQL_QUERY_TEMPLATE % (table_name)
        results = self.execute_query(connection, table_info_sql_query)
        table_exists = bool(results)

        # adds the table name to the list of existing tables for this connection in
        # case it exists
        if table_exists:
            self.connection_table_names_map[connection].append(table_name)

        return table_exists

    def create_table(self, connection, table_name, column_names):
        """
        Creates a database table.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: String
        @param table_name: Name of the table one wants to create.
        @type column_names: List
        @param column_names: Name of the columns the new table will have.
        """

        # creates the specified table in case it doesn't exist
        if not self.table_exists(connection, table_name):

            # creates the columns part of the sql create table query
            column_names_sql_template = "%s " + VARCHAR_VALUE + ","
            column_names_sql_query = "".join([column_names_sql_template % column_name for column_name in column_names])[:-1]

            # creates the sql create table query
            create_table_sql_query = CREATE_TABLE_SQL_QUERY_TEMPLATE % (table_name, column_names_sql_query)

            # executes the sql create table query
            self.execute_query(connection, create_table_sql_query)

    def get_table_names(self, connection):
        """
        Retrieves the name of the tables that exist in the database.

        @type connection: Connection
        @param connection: Database connection.
        @rtype: List
        @return: List of database table names.
        """

        # retrieves the tables that exist in the database
        results = self.execute_query(connection, SELECT_TABLE_NAMES_SQL_QUERY)
        table_names = [result[0] for result in results]

        return table_names

    def get_table_column_names(self, connection, table_name):
        """
        Returns the names of the columns in the specified table.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: String
        @param table_name Name of the table where one wants to retrieve the
        column names from.
        @rtype: List
        @return: List with the specified table's column names.
        """

        # retrieves the names of the columns in the specified table
        table_info_sql_query = SELECT_TABLE_INFO_SQL_QUERY_TEMPLATE % (table_name)
        results = self.execute_query(connection, table_info_sql_query)
        column_names = [result[1] for result in results]

        return column_names

    def get_rows(self, connection, table_name, column_names = ["*"]):
        """
        Retrieves the specified table's rows.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: String
        @param table_name: Name of the table where one wants to retrieve rows from.
        @type column_names: List
        @param column_names: Optional list of column names that determine which row
        fields should be retrieved.
        @rtype: List
        @return: List with the rows that belong to the specified table.
        """

        # creates the columns list part of the sql select table query
        column_names_sql_template = "%s,"
        column_names_sql_query = "".join([column_names_sql_template % column_name for column_name in column_names])[:-1]

        # creates the select table sql query
        select_table_sql_query_template = SELECT_TABLE_SQL_QUERY_TEMPLATE % (column_names_sql_query, table_name)

        # retrieves the table's rows
        rows = self.execute_query(connection, select_table_sql_query_template)

        return rows

    def insert_row(self, connection, table_name, column_names, field_values):
        """
        Inserts a row in the database table.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: String
        @param table_name: Name of the table where one wants to insert a row.
        @type column_names: List
        @param column_names: Name of the fields of the values one will insert.
        @type field_values: List
        @param field_values: List with the values that will be inserted in the new row,
        in the same order as the column names list.
        """

        # creates the columns list part of the sql insert query
        column_names_sql_template = "%s,"
        column_names_sql_query = "".join([column_names_sql_template % column_name for column_name in column_names])[:-1]

        # replaces the quote character for two quotes in every value to obey to the sqlite query syntax
        escaped_field_values = [str(field_value).replace("'", "''") for field_value in field_values]

        # creates the values part of the sql insert query
        field_values_sql_query_template = "'%s',"
        field_values_sql_query = "".join([field_values_sql_query_template % field_value for field_value in escaped_field_values])[:-1]

        # replaces all none strings with a null constant in the field values part of the sql insert query
        field_values_sql_query = field_values_sql_query.replace("'None'", "null")

        # creates the sql insert query
        insert_row_sql_query = INSERT_ROW_SQL_QUERY_TEMPLATE % (table_name, column_names_sql_query, field_values_sql_query)

        # executes the sql insert query
        self.execute_query(connection, insert_row_sql_query)
