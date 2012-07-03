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

import pgdb

import colony.libs.string_buffer_util

OPERATORS_MAP = {
    "length" : "char_length"
}
""" The map that resolves the various specific operator
for the pgsql implementation from the generic ones """

class PgsqlSystem:

    def get_engine_name(self):
        return "pgsql"

    def get_internal_version(self):
        return pgdb.version

    def create_engine(self, entity_manager):
        return PgsqlEngine(self, entity_manager)

class PgsqlEngine:

    pgsql_system = None
    """ The reference to the "owning" system entity """

    entity_manager = None
    """ The reference to the "owning" entity manager """

    def __init__(self, pgsql_system, entity_manager):
        self.pgsql_system = pgsql_system
        self.entity_manager = entity_manager

    def get_engine_name(self):
        return "pgsql"

    def get_internal_version(self):
        return pgdb.version

    def get_host(self):
        connection = self.entity_manager.get_connection()
        host = connection._host

        if ":" in host:
            hostname, port_string = host.split(":")
            host_tuple = (hostname, int(port_string))
        else:
            host_tuple = (host, 5432)

        return host_tuple

    def get_database_size(self):
        connection = self.entity_manager.get_connection()
        query = self._database_size_query(connection._database)
        cursor = self.execute_query(query)
        try: result = self._database_size_result(cursor)
        finally: cursor.close()
        return result

    def get_database_encoding(self):
        connection = self.entity_manager.get_connection()
        if hasattr(connection, "_encoding"): return connection._encoding

        query = self._database_encoding_query(connection._database)
        cursor = self.execute_query(query)
        try: result = self._database_encoding_result(cursor)
        finally: cursor.close()

        # caches the database encoding into the current
        # connection object (no need to retrieve it again
        # from the data source) then returns it to the caller
        connection._encoding = result
        return result

    def connect(self, connection, parameters = {}):
        host = parameters.get("host", "localhost")
        user = parameters.get("user", "postgres")
        password = parameters.get("password", "postgres")
        database = parameters.get("database", "default")
        connection._connection = pgdb.connect(host = host, user = user, password = password, database = database);
        connection._transaction_level = 0
        connection._user = user
        connection._host = host
        connection._database = database
        connection.open()

    def disconnect(self, connection):
        _connection = connection._connection
        _connection.close()
        connection.close()

    def reconnect(self):
        pass

    def destroy(self):
        # @TODO: put this is the correct way
        self._execute_query_t("drop schema public cascade").close()
        self._execute_query_t("create schema public").close()

        # retrieves the current available connection
        # and "disconnects" it (no latter access will
        # be possible)
        connection = self.entity_manager.get_connection()
        self.disconnect(connection)

    def begin(self):
        connection = self.entity_manager.get_connection()
        connection._transaction_level += 1

    def commit(self):
        connection = self.entity_manager.get_connection()

        # in case the current transaction level is zero it's
        # not a valid situation as not transaction is open, must
        # raise an exception alerting for the situation
        if connection._transaction_level == 0: raise RuntimeError("invalid transaction level, commit without begin")
        connection._transaction_level -= 1
        if connection._transaction_level == 0: self._commit()

    def rollback(self):
        connection = self.entity_manager.get_connection()
        if connection._transaction_level == 0: raise RuntimeError("invalid transaction level, rollback without begin")
        connection._transaction_level -= 1
        if connection._transaction_level == 0: self._rollback()

    def lock(self, entity_class, id_value = None):
        # retrieves the table name and id associated
        # with the entity class to be locked, these
        # values are going to be used to set the appropriate
        # values in the field name and value keys
        table_name = entity_class.get_name()
        table_id = entity_class.get_id()

        # checks if the provided id values is going
        # to be considered into the locking (row locking)
        # or if the locking is going to be table level
        id_value_valid = not id_value == None

        # validates that the id value is valid as an id
        # attribute, type validation (security consideration)
        id_value_valid and entity_class._validate_value(table_id, id_value)

        # converts the table id value into the appropriate
        # sql representation for query usage (casting) this
        # is only done in case the id value is considered valid
        id_sql_value = id_value_valid and entity_class._get_sql_value(table_id, id_value) or None

        # locks the table associated with the current entity class
        # the lock may be row level or table level (depending on
        # the definition or not of the id value)
        self.lock_table(table_name, {"field_name" : entity_class.get_id(), "field_value" : id_sql_value})

    def lock_table(self, table_name, parameters):
        query = self._lock_table_query(table_name, parameters)
        self.execute_query(query).close()

    def has_definition(self, entity_class):
        query = self._has_definition_query(entity_class)
        cursor = self.execute_query(query)
        try: result = self._has_definition_result(entity_class, cursor)
        finally: cursor.close()
        return result

    def has_table_definition(self, table_name):
        query = self._has_table_definition_query(table_name)
        cursor = self.execute_query(query)
        try: result = self._has_table_definition_result(table_name, cursor)
        finally: cursor.close()
        return result

    def execute_query(self, query, cursor = None):
        """
        Executes the given query using the provided cursor
        or "inside" a new cursor context in case none is
        provided.

        @type query: String
        @param query: The query that is going to be executed
        in the current engine.
        @type cursor: Cursor
        @param cursor: The cursor that is going to be execute
        the query in the engine, this cursor must have been
        created for this engine.
        @rtype: Cursor
        @return: The cursor that was used for the query execution
        it must be closed in the outside context.
        """

        # retrieves the current connection from the associated
        # entity manager and then retrieves the internal database
        # connection for data access
        connection = self.entity_manager.get_connection()
        _connection = connection._connection

        # creates a new cursor to be used in case one
        # is required, for usage
        cursor = cursor or _connection.cursor()

        try:
            print "<pgsql> %s" % query # ! REMOVE THIS !

            # executes the query in the current cursor
            # context for the engine
            cursor.execute(query)
        except BaseException, exception:
            # closes the cursor (safe closing)
            # and re-raises the exception
            cursor.close()

            # in case the exception class is included in one of the
            # possible formats of the adapter, it must be converted
            # into the proper "integrity" representation
            if exception.__class__ in (AssertionError, pgdb.DatabaseError):
                # creates the (integrity) exception from the exception
                # message extracted from the exception and raises it
                # to the top level handlers
                exception_message = unicode(exception)
                exception = IntegrityError(exception_message)
                raise exception

            # re-raises the exception to the top level layers
            raise

        # returns the cursor to be used to retrieve
        # the resulting values from the query execution
        return cursor

    def _commit(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection
        _connection.commit()

        # calls the commit handlers and then
        # resets all the handlers to the original state
        connection.call_commit_handlers()
        connection.reset_handlers()

        print "<pgsql> COMMIT"

    def _rollback(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection
        _connection.rollback()

        # calls the rollback handlers and then
        # resets all the handlers to the original state
        connection.call_rollback_handlers()
        connection.reset_handlers()

        print "<pgsql> ROLLBACK"

    def _execute_query_t(self, query, cursor = None):
        """
        Executes the given query using the provided cursor
        or "inside" a new cursor context in case none is
        provided.

        This method executes the query inside an "exclusive"
        transaction context that is created "just" for the
        query execution.

        @type query: String
        @param query: The query that is going to be executed
        in the current engine.
        @type cursor: Cursor
        @param cursor: The cursor that is going to be execute
        the query in the engine, this cursor must have been
        created for this engine.
        @rtype: Cursor
        @return: The cursor that was used for the query execution
        it must be closed in the outside context.
        """

        # begins a new transaction context for the
        # execution of the query
        self.begin()

        try:
            # executes the query in the current context
            # the failure will result in a "rollback" and
            # the success in a commit, the cursor is saved
            # for latter return
            cursor = self.execute_query(query, cursor)
        except:
            # rolls back the current transaction because
            # the query failed to execute, then re-raises
            # the exception to the upper level
            self.rollback()
            raise
        else:
            # commits the current transaction because there
            # was success in execution
            self.commit()

        # returns the cursor to be used to retrieve
        # the resulting values from the query execution
        return cursor

    def _database_size_query(self, database_name):
        # creates the query for the calculation of the database
        # size according to the requested database name
        query = "select pg_database_size('%s')" % database_name

        # returns the generated database size query
        return query

    def _database_size_result(self, cursor):
        # selects all the elements from the cursor the
        # database size should be the first element, then
        # closes the cursor
        try: counts = cursor.fetchall()
        finally: cursor.close()

        # retrieves the database size as the first element
        # of the first retrieved row
        datbase_size = counts[0][0]

        # returns the result of the retrieval of the database
        # size from the data source
        return datbase_size

    def _database_encoding_query(self, database_name):
        # creates the query for the retrieval of the database
        # encoding according to the requested database name
        query = "select pg_encoding_to_char(encoding) from pg_database where datname = '%s';" % database_name

        # returns the generated database encoding query
        return query

    def _database_encoding_result(self, cursor):
        # selects all the elements from the cursor the
        # database encoding should be the first element,
        # then closes the cursor
        try: counts = cursor.fetchall()
        finally: cursor.close()

        # retrieves the database encoding as the first element
        # of the first retrieved row
        datbase_encoding = counts[0][0]

        # returns the result of the retrieval of the database
        # encoding from the data source
        return datbase_encoding

    def _index_query(self, entity_class, attribute_name, index_type = "hash"):
        # retrieves the associated table name
        # as the "name" of the entity class
        table_name = entity_class.get_name()

        # creates the table index query for the table
        # name associated with the entity class
        query = self._table_index_query(table_name, attribute_name, index_type)

        # returns the generated "index" query
        return query

    def _table_index_query(self, table_name, attribute_name, index_type = "hash"):
        # creates the buffer to hold the query and populates it with the
        # base values of the query (base index of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("create index %s_%s_%s_idx on %s using %s (%s)" % (table_name, attribute_name, index_type, table_name, index_type, attribute_name))

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "index" query
        return query

    def _lock_table_query(self, table_name, parameters):
        # retrieves the field name amd value from the
        # parameters these is going to be used in the
        # locking query for locking the provided table
        field_name = parameters["field_name"]
        field_value = parameters.get("field_value", None)

        # creates the buffer to hold the query and populates it with the
        # base values of the query (selecting the table for update in
        # the required field values will lock the appropriate rows)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("select * from %s" % table_name)
        field_value and query_buffer.write(" where %s = %s" % (field_name, field_value))
        query_buffer.write(" for update")

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "locking" query
        return query

    def _has_definition_query(self, entity_class):
        # retrieves the associated table name
        # as the "name" of the entity class
        table_name = entity_class.get_name()

        # creates the buffer to hold the query and populates it with the
        # base values of the query (base definition of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("select count(*) from pg_tables where tablename = '%s'" % table_name)

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "dropping" query
        return query

    def _has_definition_result(self, entity_class, cursor):
        try:
            # selects all the counts for the table in the database
            # this values should be an integer
            counts = cursor.fetchall()
        finally:
            # closes the cursor
            cursor.close()

        # checks if there is at least one count records
        # for the table definition
        has_table_definition = counts and counts[0][0] > 0

        # returns the result of the test for the table
        # definition in the current context
        return has_table_definition

    def _has_table_definition_query(self, table_name):
        # creates the buffer to hold the query and populates it with the
        # base values of the query (base definition of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("select count(*) from pg_tables where tablename = '%s'" % table_name)

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "dropping" query
        return query

    def _has_table_definition_result(self, table_name, cursor):
        # selects all the counts for the table in the database
        # this values should be an integer, then closes the cursor
        try: counts = cursor.fetchall()
        finally: cursor.close()

        # checks if there is at least one count records
        # for the table definition
        has_table_definition = counts and counts[0][0] > 0

        # returns the result of the test for the table
        # definition in the current context
        return has_table_definition

    def _resolve_operator(self, operator):
        return OPERATORS_MAP.get(operator, operator)

    def _escape_slash(self):
        return False

    def _allow_cascade(self):
        return True

    def _allow_alter_drop(self):
        return False

class IntegrityError(RuntimeError):
    pass
