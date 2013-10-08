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

import os
import thread
import sqlite3
import tempfile

import colony.libs.string_buffer_util

import colony.base.system

ENGINE_NAME = "sqlite"
""" The name of the engine currently in execution """

INTERNAL_VERSION = "1.0.1"
""" The version number that represents the internal
implementation details """

class EntitySqlite(colony.base.system.System):
    """
    The entity sqlite class.
    """

    def get_engine_name(self):
        return ENGINE_NAME

    def get_internal_version(self):
        return INTERNAL_VERSION

    def create_engine(self, entity_manager):
        return SqliteEngine(self, entity_manager)

class SqliteEngine:

    sqlite_system = None
    """ The reference to the "owning" system entity """

    entity_manager = None
    """ The reference to the "owning" entity manager """

    def __init__(self, sqlite_system, entity_manager):
        self.sqlite_system = sqlite_system
        self.entity_manager = entity_manager

    def get_engine_name(self):
        return ENGINE_NAME

    def get_internal_version(self):
        return sqlite3.sqlite_version

    def get_host(self):
        return None

    def get_database_size(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection

        # retrieves the file path of the database file and
        # then uses it to check the size of the database
        file_path = _connection.get_file_path()
        file_size = os.path.getsize(file_path)

        # returns the "calculated" database file size as the
        # size of the database "view"
        return file_size

    def get_database_encoding(self):
        return "utf-8"

    def connect(self, connection, parameters = {}):
        file_path = parameters.get("file_path", None)
        cache_size = parameters.get("cache_size", 200000)
        synchronous = parameters.get("synchronous", 2)
        file_path = file_path or self._get_temporary()
        connection._connection = SqliteConnection(
            file_path,
            cache_size = cache_size,
            synchronous = synchronous
        )
        connection.open()

    def disconnect(self, connection):
        _connection = connection._connection
        _connection.close()
        connection.close()

    def reconnect(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection
        _connection.reopen()

    def destroy(self):
        # retrieves the current connection as disconnects
        # it, disabling any future accesses
        connection = self.entity_manager.get_connection()
        self.disconnect(connection)

        # retrieves the underlying connection and destroys
        # it, it should remove the remaining database files
        _connection = connection._connection
        _connection.destroy()

    def begin(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection
        _connection.push_transaction()

    def commit(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection

        # in case the current transaction level is zero it's
        # not a valid situation as not transaction is open, must
        # raise an exception alerting for the situation
        is_empty_transaction = _connection.is_empty_transaction()
        if is_empty_transaction: raise RuntimeError("invalid transaction level, commit without begin")

        # pops the current transaction, decrementing the current
        # transaction level by one, this will release a transaction
        # level from the stack
        _connection.pop_transaction()

        is_empty_transaction = _connection.is_empty_transaction()
        if not is_empty_transaction: return
        self._commit()

    def rollback(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection

        # in case the current transaction level is zero it's
        # not a valid situation as not transaction is open, must
        # raise an exception alerting for the situation
        is_empty_transaction = _connection.is_empty_transaction()
        if is_empty_transaction: raise RuntimeError("invalid transaction level, rollback without begin")

        # pops the current transaction, decrementing the current
        # transaction level by one, this will release a transaction
        # level from the stack
        _connection.pop_transaction()

        # checks the current transaction for empty state in case
        # it's not empty there is no need to rollback the transaction
        # because it's an inner level and no effect should be made
        is_empty_transaction = _connection.is_empty_transaction()
        if not is_empty_transaction: return

        # runs the "rollback" command in the underlying data base
        # layer, executes the "rollback" operation
        self._rollback()

    def lock(self, entity_class, id_value = None, lock_parents = True):
        table_name = entity_class.get_name()
        table_id = entity_class.get_id()
        self.lock_table(table_name, {
            "field_name" : table_id
        })

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
            #print "<sqlite> %s" % query # ! REMOVE THIS !

            import time
            initial = time.time()
            # executes the query in the current cursor
            # context for the engine
            cursor.execute(query)
            final = time.time()

            if final - initial > 0.025: print "[WARNING] <sqlite - %f> %s" % (final - initial, query) # ! REMOVE THIS !
        except:
            # closes the cursor (safe closing)
            # and re-raises the exception
            cursor.close()
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

    def _rollback(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection
        _connection.rollback()

        # calls the rollback handlers and then
        # resets all the handlers to the original state
        connection.call_rollback_handlers()
        connection.reset_handlers()

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

    def _index_query(self, entity_class, attribute_name, index_type = "hash"):
        # retrieves the associated table name
        # as the "name" of the entity class
        table_name = entity_class.get_name()

        # creates the table index query for the table
        # name associated with the entity class
        query = self._table_index_query(table_name, attribute_name, index_type)

        # returns the generated "dropping" query
        return query

    def _table_index_query(self, table_name, attribute_name, index_type = "hash"):
        # creates the buffer to hold the query and populates it with the
        # base values of the query (base index of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("create index %s_%s_%s_idx on %s(%s)" % (table_name, attribute_name, index_type, table_name, attribute_name))

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "index" query
        return query

    def _lock_table_query(self, table_name, parameters):
        # retrieves the field name from the parameters
        # this is going to be used in the locking query
        # for locking the provided table
        field_name = parameters["field_name"]

        # creates the buffer to hold the query and populates it with the
        # base values of the query (updating of the table in invalid
        # value should be able to lock the sqlite database)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("update %s set %s = %s where 0 = 1" % (table_name, field_name, field_name))

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "locking" query
        return query

    def _has_definition_query(self, entity_class):
        # creates the buffer to hold the query and populates it with the
        # base values of the query (base definition of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("select name from SQLite_Master")

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "dropping" query
        return query

    def _has_definition_result(self, entity_class, cursor):
        # retrieves the associated table name
        # as the "name" of the entity class
        table_name = entity_class.get_name()

        # selects the table names from the cursor
        # by fetching all the items from it, then
        # closes the cursor
        try: table_names = [value[0] for value in cursor]
        finally: cursor.close()

        # checks if there is a definition for the current entity
        # class in the table names list
        has_table_definition = table_name in table_names

        # returns the result of the test for the table
        # definition in the current context
        return has_table_definition

    def _has_table_definition_query(self, table_name):
        # creates the buffer to hold the query and populates it with the
        # base values of the query (base definition of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("select name from SQLite_Master")

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "dropping" query
        return query

    def _has_table_definition_result(self, table_name, cursor):
        # selects the table names from the cursor
        # by fetching all the items from it, then
        # closes the cursor
        try: table_names = [value[0] for value in cursor]
        finally: cursor.close()

        # checks if there is a definition for the current entity
        # class in the table names list
        has_table_definition = table_name in table_names

        # returns the result of the test for the table
        # definition in the current context
        return has_table_definition

    def _get_temporary(self):
        # creates a new temporary file, in the most
        # secure manner and returns the file descriptor
        # and the file path to it, the file descriptor
        # is immediately closed to avoid pending file handles
        file, file_path = tempfile.mkstemp()
        os.close(file)

        # returns the path to the temporary file
        # for external usage
        return file_path

    def _resolve_operator(self, operator):
        return operator

    def _escape_slash(self):
        return False

    def _allow_cascade(self):
        return False

    def _allow_alter_drop(self):
        return False

    def _allow_for_update(self):
        return False

class SqliteConnection:
    """
    Class representing an abstraction on top of
    the sqlite connection, to provide necessary
    abstraction features.
    This features include: thread connection abstraction
    transaction stack retrieval, etc.
    """

    file_path = None
    """ The path to the file containing the sqlite
    database """

    cache_size = None
    """ The size (in pages) of the cache memory to be used
    by the sqlite session """

    synchronous = None
    """ If the current session should use the synchronous mode
    of operation (if asynchronous write is faster) """

    transaction_level_map = {}
    """ The map associating the sqlite connection with the
    transaction depth (nesting) level """

    connections_map = {}
    """ The map associating the thread identifier with the
    connection """

    def __init__(self, file_path, cache_size = 200000, synchronous = 2):
        self.file_path = file_path
        self.cache_size = cache_size
        self.synchronous = synchronous

        self.transaction_level_map = {}
        self.connections_map = {}

    def get_connection(self):
        # retrieves the thread identifier for the
        # current executing thread, then uses it
        # to retrieve the corresponding connection
        thread_id = thread.get_ident()
        connection = self.connections_map.get(thread_id, None)

        # in case a connection is not available for the
        # current thread, one must be create it
        if not connection:
            # creates a new connection and sets it in the
            # connections map for the current thread
            connection = sqlite3.connect(
                self.file_path,
                timeout = 30,
                isolation_level = "DEFERRED"
            )
            self.connections_map[thread_id] = connection

            # creates a new transaction level for the connection
            # in the current thread
            self.transaction_level_map[connection] = 0

            # executes queries for the updating of the cache
            # size for the current session and sets the current
            # query execution to synchronous operating mode
            self._execute_query("pragma cache_size = %d" % self.cache_size).close()
            self._execute_query("pragma synchronous = %d" % self.synchronous).close()

        # returns the correct connection
        # for the current thread
        return connection

    def close(self):
        # iterates over all the connection in the connections
        # map to closes them (will close all the connections)
        for _thread_id, connection in self.connections_map.items():
            # closes the current connection, disables
            # all the pending connections
            connection.close()

            # deletes the transaction level reference
            # for the connection in the transaction
            # level map
            del self.transaction_level_map[connection]

        # clears the connections map, eliminating
        # any pending connection reference
        self.connections_map.clear()

    def reopen(self):
        pass

    def destroy(self):
        os.remove(self.file_path)

    def cursor(self):
        connection = self.get_connection()
        return connection.cursor()

    def commit(self):
        connection = self.get_connection()
        connection.commit()

    def rollback(self):
        connection = self.get_connection()
        connection.rollback()

    def push_transaction(self):
        connection = self.get_connection()
        self.transaction_level_map[connection] += 1

    def pop_transaction(self):
        connection = self.get_connection()
        self.transaction_level_map[connection] -= 1

    def reset_transaction(self):
        connection = self.get_connection()
        self.transaction_level_map[connection] = 0

    def is_empty_transaction(self):
        connection = self.get_connection()
        level = self.transaction_level_map[connection]
        is_empty_transaction = level == 0

        return is_empty_transaction

    def is_valid_transaction(self):
        connection = self.get_connection()
        is_valid_transaction = self.transaction_level_map[connection] >= 0

        return is_valid_transaction

    def get_file_path(self):
        return self.file_path

    def _execute_query(self, query, connection = None):
        # retrieves the current connection and creates
        # a new cursor object for query execution
        connection = connection or self.get_connection()
        cursor = connection.cursor()

        # executes the query using the current cursor
        # then closes the cursor avoid the leak of
        # cursor objects (memory reference leaking)
        try: cursor.execute(query)
        except: cursor.close()

        # returns the cursor that has just been created for
        # the execution of the requested query
        return cursor
