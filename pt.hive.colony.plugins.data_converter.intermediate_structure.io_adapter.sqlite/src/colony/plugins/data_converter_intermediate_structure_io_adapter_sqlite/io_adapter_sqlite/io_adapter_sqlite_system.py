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

import sqlite3
import types
import os.path

import io_adapter_sqlite_exceptions

CREATE_TABLE_SQL_QUERY = "CREATE TABLE %s(%s);"
""" Query used to create a new table """

INSERT_ROW_SQL_QUERY = "INSERT INTO %s(%s) VALUES(%s);"
""" Query used to insert a new row """

TABLE_EXISTS_SQL_QUERY = "PRAGMA table_info(%s);"
""" Query used to determine if a table exists in the database """

class IoAdapterSqlite:
    """
    Provides a means to load and save the intermediate structure by using the colony business sqlite.
    """

    def __init__(self, io_adapter_sqlite_plugin):
        """
        Class constructor.

        @type io_adapter_sqlite_plugin: IoAdapterSqlite
        @param io_adapter_sqlite_plugin: Input output adapter sqlite plugin.
        """

        self.io_adapter_sqlite_plugin = io_adapter_sqlite_plugin

    def execute_query(self, connection, query):
        """
        Executes an sqlite query.

        @type connection: Connection
        @param connection: Database connection.
        @type query: str
        @param query: Query one wants to perform.
        @rtype: Dictionary
        @return results: Dictionary with the queries' results.
        """

        cursor = connection.cursor()
        results = cursor.execute(query)
        cursor.close()

        return results

    def table_exists(self, connection, table_name):
        """
        Indicates if the specified table exists.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: str
        @param table_name: Name of the table.
        @rtype: bool
        @return: Boolean indicating if the table exists in the specified database.
        """

        table_exists_sql_query = TABLE_EXISTS_SQL_QUERY % (table_name)
        results = self.execute_query(connection, table_exists_sql_query)

        return bool(results.description)

    def create_table(self, connection, table_name, column_names):
        """
        Creates a database table.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: str
        @param table_name: Name of the table one wants to create.
        @type column_names: List
        @param column_names: Name of the columns the new table will have.
        """

        if not self.table_exists(connection, table_name):
            column_names_sql_query = "".join([column_name + " varchar(255)," for column_name in column_names])[:-1]
            create_table_sql_query = CREATE_TABLE_SQL_QUERY % (table_name, column_names_sql_query)
            self.execute_query(connection, create_table_sql_query)

    def insert_row(self, connection, table_name, column_names, field_values):
        """
        Inserts a row in the database table.

        @type connection: Connection
        @param connection: Database connection.
        @type table_name: str
        @param table_name: Name of the table where one wants to insert a row.
        @type column_names: List
        @param column_names: Name of the fields of the values one will insert.
        @type field_values: List
        @param field_values: List with the values that will be inserted in the new row, in the same order as the column names list.
        """

        column_names_sql_query = "".join([column_name + "," for column_name in column_names])[:-1]
        field_values_sql_query = "".join(["'" + str(field_value).replace("'", "''") + "'," for field_value in field_values])[:-1]
        field_values_sql_query.replace("'None'", "NULL")
        insert_row_sql_query = INSERT_ROW_SQL_QUERY % (table_name, column_names_sql_query, field_values_sql_query)
        self.execute_query(connection, insert_row_sql_query)

    def load(self, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the sqlite with the specified options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        self.io_adapter_sqlite_plugin.logger.info("[%s] Loading intermediate structure with sqlite io adapter" % self.io_adapter_sqlite_plugin.id)

        raise io_adapter_dbase_exceptions.IoAdapterSqliteOperationNotSupported("IoAdapterDbase.save - The intermediate structure sqlite io adapter currently does not support the load operation")

    def save(self, intermediate_structure, options):
        """
        Saves the intermediate structure with the sqlite at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure with the sqlite.
        """

        self.io_adapter_sqlite_plugin.info("Saving intermediate structure with sqlite io adapter")

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_sqlite_exceptions.IoAdapterSqliteOptionNotFound("IoAdapterSqlite.save - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]

        # creates the sqlite connection
        connection = sqlite3.connect(file_path)

        # saves the intermediate structure entities' attributes
        self.save_attributes(intermediate_structure, connection)

        # saves the intermediate structure entities' relations
        self.save_relations(intermediate_structure, connection)

        # commits and closes the sqlite connection
        connection.commit()
        connection.close()

    def save_attributes(self, intermediate_structure, connection):
        """
        Saves the intermediate structure's entities' attributes with the sqlite.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type connection: Connection
        @param connection: Connection to the database.
        """

        self.io_adapter_sqlite_plugin.logger.info("[%s] Saving intermediate structure entities' attributes with sqlite io adapter" % self.io_adapter_sqlite_plugin.id)

        # dictionary used to index the entities created in the save attributes step by their object id
        entity_object_id_entity_map = {}

        # dictionary used to associate intermediate entity object ids with entity object ids
        intermediate_entity_object_id_entity_object_id_map = {}

        # creates a map where to store the computation of intermediate entity non-relation attribute names
        intermediate_entity_name_non_relation_attribute_names_map = {}

        # retrieves the column names for each table by inspecting every intermediate entity
        table_name_column_names_map = {}
        intermediate_entities = intermediate_structure.get_entities()
        for intermediate_entity in intermediate_entities:
            intermediate_entity_name = intermediate_entity.get_name()
            attribute_names = intermediate_entity.get_attributes().keys()
            if not intermediate_entity_name in table_name_column_names_map:
                table_name_column_names_map[intermediate_entity_name] = ["object_id"]
            table_name_column_names_map[intermediate_entity_name].extend(attribute_names)

        # creates the tables where to store the intermediate entities
        for table_name in table_name_column_names_map:
            attribute_names = list(set(table_name_column_names_map[table_name]))
            self.create_table(connection, table_name, attribute_names)

        # inserts a row with which intermediate entity's contents
        for intermediate_entity in intermediate_entities:
            intermediate_entity_name = intermediate_entity.get_name()

            # computes which intermediate entity attributes are not relation attributes and stores the results so that they don't have to be calculated again
            if intermediate_entity_name in intermediate_entity_name_non_relation_attribute_names_map:
                non_relation_attribute_names = intermediate_entity_name_non_relation_attribute_names_map[intermediate_entity_name]
            else:
                non_relation_attribute_names = [attribute_name for attribute_name in intermediate_entity.get_attributes().keys() if type(intermediate_entity.get_attribute(attribute_name)) not in (types.ListType, types.InstanceType)]
                intermediate_entity_name_non_relation_attribute_names_map[intermediate_entity_name] = non_relation_attribute_names

            # inserts a row with the entity
            non_relation_attribute_values = [intermediate_entity.get_object_id()]
            non_relation_attribute_values.extend([intermediate_entity.get_attribute(attribute_name) for attribute_name in non_relation_attribute_names])
            non_relation_attribute_names_with_object_id = ["object_id"]
            non_relation_attribute_names_with_object_id.extend(non_relation_attribute_names)
            self.insert_row(connection, intermediate_entity_name, non_relation_attribute_names_with_object_id, non_relation_attribute_values)

    def save_relations(self, intermediate_structure, connection):
        """
        Saves the intermediate structure's entities' attributes with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type connection: Connection
        @param connection: Connection to the database.
        """

        self.io_adapter_sqlite_plugin.logger.info("[%s] Saving intermediate structure entities' relations with entity manager io adapter" % self.io_adapter_sqlite_plugin.id)

        # creates a map where to store the computation of intermediate entity non-relation attribute names
        intermediate_entity_name_relation_attribute_names_map = {}

        # creates an entity for each intermediate entity in the internal structure and populates it with its attributes
        intermediate_entities = intermediate_structure.get_entities()
        for intermediate_entity in intermediate_entities:

            # retrieves the respective entity which was created in the save attributes step
            intermediate_entity_name = intermediate_entity.get_name()
            intermediate_entity_object_id = intermediate_entity.get_object_id()

            # computes which intermediate entity attributes are relation attributes and stores the results so that they don't have to be calculated again
            if intermediate_entity_name in intermediate_entity_name_relation_attribute_names_map:
                relation_attribute_names = intermediate_entity_name_relation_attribute_names_map[intermediate_entity_name]
            else:
                relation_attribute_names = [attribute_name for attribute_name in intermediate_entity.get_attributes().keys() if type(intermediate_entity.get_attribute(attribute_name)) in (types.ListType, types.InstanceType)]
                intermediate_entity_name_relation_attribute_names_map[intermediate_entity_name] = relation_attribute_names

            # populates the entity with its related entities
            for attribute_name in relation_attribute_names:
                intermediate_related_entity_or_entities = intermediate_entity.get_attribute(attribute_name)

                # encapsulates the relation attribute's value in a list in case its a "to one" relation in order to reuse the following code
                if type(intermediate_related_entity_or_entities) == types.ListType:
                    intermediate_related_entities = intermediate_related_entity_or_entities
                elif intermediate_related_entity_or_entities:
                    intermediate_related_entities = [intermediate_related_entity_or_entities]
                else:
                    intermediate_related_entities = []

                # retrieves entity that corresponds to the intermediate entity that is in the relation attribute adds it to the entity's relation attribute
                for intermediate_related_entity in intermediate_related_entities:
                    intermediate_related_entity_object_id = intermediate_related_entity.get_object_id()

                    # raises an exception in case the related entity is not found
                    if not related_entity:
                        intermediate_related_entity_name = intermediate_related_entity.get_name()
                        raise io_adapter_entity_manager_exceptions.IoAdapterEntityManagerEntityClassNotFound("IoAdapterEntityManager.save - Entity class not found (entity_class_name = %s)" % entity_name)

                    # creates a relation table in case it doesn't exist yet and adds a row with the related intermediate entities' object ids
                    relation_table_name = intermediate_entity_name + intermediate_related_entity_name
                    relation_column_names = [intermediate_entity_name + "_object_id", intermediate_related_entity_name + "_object_id"]
                    self.create_table(connection, relation_table_name, relation_column_names)
                    self.insert_row(connection, relation_table_name, relation_column_names, [intermediate_entity_object_id, intermediate_related_entity_object_id])
