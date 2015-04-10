#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import colony

try: import pgdb
except:
    try: import psycopg2; pgdb = psycopg2
    except: import psycopg2cffi; pgdb = psycopg2cffi

ENGINE_NAME = "pgsql"
""" The name of the engine currently in execution
it's going to be used to identify the system """

ISOLATION_LEVEL = "serializable"
""" The isolation level to be used in the connections
created by the driver, this isolation level is considered
to be very restrictive (most isolated) and ensures that
something that is read on a transaction is not read by
another until the transaction is finished """

SLOW_QUERY_TIME = 25
""" The minimum time in milliseconds before a query is
considered to be slow and a warning message should be logger
into the currently attached logger (for debugging) """

OPERATORS_MAP = dict(
    length = "char_length"
)
""" The map that resolves the various specific operator
for the pgsql implementation from the generic ones """

class EntityPgsql(colony.System):
    """
    The entity pgsql class.
    """

    def get_engine_name(self):
        return ENGINE_NAME

    def get_internal_version(self):
        return pgdb.version

    def create_engine(self, entity_manager):
        return PgsqlEngine(self, entity_manager)

class PgsqlEngine(object):

    pgsql_system = None
    """ The reference to the "owning" system entity """

    entity_manager = None
    """ The reference to the "owning" entity manager """

    def __init__(self, pgsql_system, entity_manager):
        self.pgsql_system = pgsql_system
        self.entity_manager = entity_manager

    def get_engine_name(self):
        return ENGINE_NAME

    def get_internal_version(self):
        if hasattr(pgdb, "version"): return pgdb.version
        if hasattr(pgdb, "__version__"): return pgdb.__version__
        return None

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
        _connection = connection._connection
        encoding = _connection.get_database_encoding()
        return encoding

    def connect(self, connection, parameters = {}):
        db_prefix = parameters.get("db_prefix", "")
        db_default = self.entity_manager.id or db_prefix + "default"
        host = parameters.get("host", "localhost")
        user = parameters.get("user", "postgres")
        password = parameters.get("password", "postgres")
        database = parameters.get("database", db_default)
        isolation = parameters.get("isolation", ISOLATION_LEVEL)
        host = colony.conf("DB_HOST", host)
        user = colony.conf("DB_USER", user)
        password = colony.conf("DB_PASSWORD", password)
        database = colony.conf("DB_NAME", database)
        isolation = colony.conf("DB_ISOLATION", isolation)
        show_sql = colony.conf("SHOW_SQL", False)
        connection._connection = PgsqlConnection(
            host = host,
            user = user,
            password = password,
            database = database,
            isolation = isolation
        )
        connection._transaction_level = 0
        connection._user = user
        connection._host = host
        connection._database = database
        connection._isolation = isolation
        connection._show_sql = show_sql
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
        # runs the proper queries that will drop the complete set of
        # tables in the currently selected schema
        self._execute_query_t("drop schema public cascade").close()
        self._execute_query_t("create schema public").close()

        # retrieves the current available connection
        # and "disconnects" it (no latter access will
        # be possible)
        connection = self.entity_manager.get_connection()
        self.disconnect(connection)

    def begin(self):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection
        _connection.push_transaction()

    def commit(self):
        # retrieves the current connection from the associated
        # entity manager and then retrieves the internal database
        # connection for data access (logic retrieval)
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
        # retrieves the current connection from the associated
        # entity manager and then retrieves the internal database
        # connection for data access (logic retrieval)
        connection = self.entity_manager.get_connection()
        _connection = connection._connection

        # checks if the current connection has been closed in the middle
        # for such situation the current method should return, it's not
        # possible to perform the rollback operation
        is_close = _connection.is_close()
        if is_close: return

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

        # retrieves the complete set of parents from the entity class
        # and default to an empty sequence in case the lock parents flag
        # is not set (no parents to be locked)
        parents = entity_class.get_all_parents() if lock_parents else ()

        # iterates over all the parents from the current entity class
        # to lock their respective table so that the entity is protected
        # in all it's levels oh inheritance
        for parent in parents:
            # locks the table associated with the current parent class
            # the lock may be row level or table level (depending on
            # the definition or not of the id value)
            parent_table_name = parent.get_name()
            self.lock_table(parent_table_name, {
                "field_name" : table_id,
                "field_value" : id_sql_value
            })

        # locks the table associated with the current entity class
        # the lock may be row level or table level (depending on
        # the definition or not of the id value)
        self.lock_table(table_name, {
            "field_name" : table_id,
            "field_value" : id_sql_value
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

        # gathers the name of the data base for which the query
        # is going to be executed (helps with debug operations)
        database = _connection.get_database()

        # creates a new cursor to be used in case one
        # is required, for usage
        cursor = cursor or _connection.cursor()

        try:
            # prints a debug message about the query that is going to be
            # executed under the pgsql engine (for debugging purposes)
            self.pgsql_system.debug("[%s] [%s] %s" % (ENGINE_NAME, database, query))

            # in case the current connections requests that the sql string
            # should be displayed it's printed to the logger properly
            if connection._show_sql: self.pgsql_system.info("[%s] [%s] %s" % (ENGINE_NAME, database, query))

            # takes a snapshot of the initial time for the
            # the query, this is going to be used to detect
            # the queries that are considered slow
            initial = time.time()

            # executes the query in the current cursor context
            # for the engine, in case there's an exception during
            # the execution of the query the query is logged
            try: cursor.execute(query)
            except: self.pgsql_system.info("[%s] [%s] %s" % (ENGINE_NAME, database, query)); raise
            final = time.time()

            # verifies if the timing for the current executing query
            # is too high (slow query) and if it's prints a warning
            # message as this may condition the way the system behaves
            delta = int((final - initial) * 1000)
            is_slow = delta > SLOW_QUERY_TIME
            if is_slow: self.pgsql_system.info("[%s] [%s] [%d ms] %s" % (ENGINE_NAME, database, delta, query))

            # triggers a notification about the sql query execution that
            # has just been performed (should contain also the time in ms)
            colony.notify_g("sql.executed", query, ENGINE_NAME, delta)
        except BaseException as exception:
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
                exception_message = colony.legacy.UNICODE(exception)
                exception = IntegrityError(exception_message)
                raise exception

            # re-raises the exception to the top level layers
            raise

        # returns the cursor to be used to retrieve
        # the resulting values from the query execution
        return cursor

    def serializable(self):
        self.isolation_level("serializable")

    def isolation_level(self, isolation):
        connection = self.entity_manager.get_connection()
        _connection = connection._connection
        _connection.isolation_level(isolation)

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
        # constructs the index name from the various components of it, note
        # that the value is truncated to the maximum length possible, this
        # may create problem with duplicated index naming (requires caution)
        index_name = "%s_%s_%s" % (table_name, attribute_name, index_type)
        index_name = index_name[-63:]

        # creates the buffer to hold the query and populates it with the
        # base values of the query (base index of the table)
        query_buffer = colony.StringBuffer()
        query_buffer.write("create index %s on %s using %s (%s)" % (index_name, table_name, index_type, attribute_name))

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "index" query
        return query

    def _lock_table_query(self, table_name, parameters):
        # retrieves the field name and value from the
        # parameters these is going to be used in the
        # locking query for locking the provided table
        field_name = parameters.get("field_name", None)
        field_value = parameters.get("field_value", None)

        # retrieves the list of fields (names) to be locked
        # in the table (can't be accessed)
        fields = parameters.get("fields", None)

        # constructs the fields part of the query separated
        # by commas, in case no set of fields is provided all
        # the table fields are locked (uses "wildcard")
        fields_string = fields and ", ".join(fields) or "*"

        # creates the buffer to hold the query and populates it with the
        # base values of the query (selecting the table for update in
        # the required field values will lock the appropriate rows)
        query_buffer = colony.StringBuffer()
        query_buffer.write("select %s from %s" % (fields_string, table_name))
        field_name and field_value and query_buffer.write(" where %s = %s" % (field_name, field_value))
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
        query_buffer = colony.StringBuffer()
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
        query_buffer = colony.StringBuffer()
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

    def _is_serializable(self):
        connection = self.entity_manager.get_connection()
        return connection._isolation == "serializable"

    def _escape_slash(self):
        return False

    def _allow_cascade(self):
        return True

    def _allow_alter_drop(self):
        return False

    def _allow_for_update(self):
        # currently pgsql does not support the row level locking
        # for outer joins, meaning that queries that for queries
        # contain relations loading it would be impossible to lock
        # the selected rows, making the for update support not reliable
        # this is considered a major drawback towards pgsql usage
        return False

class PgsqlConnection(object):
    """
    Class that represents a logical connection with a
    pgsql database, it should be used to encapsulate
    the inner details of a connection.
    """

    host = None
    """ The current (remote) host for the connection this
    can be used to control the access to the remote database """

    user = None
    """ The name of the user (username) to be used in the
    authentication process for the connection """

    password = None
    """ The password of the user to be used in the
    authentication process for the connection """

    database = None
    """ The database to be used during the connection, this
    should be a plain string for proper representation """

    isolation = None
    """ The isolation level that is currently in use
    for the connection, may be changed at run-time """

    connection = None
    """ The reference to the underlying connection that handles
    the proper pipelining of the execution """

    transaction_level = 0
    """ The current transaction depth for the connection, this value
    should be increment by opening a transaction and decremented for
    each close of a transaction """

    def __init__(
        self,
        host = "localhost",
        user = "root",
        password = "root",
        database = "default",
        isolation = ISOLATION_LEVEL
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.isolation = isolation

        self.connection = None
        self.transaction_level = 0

    def get_connection(self, create = True):
        # in case there's a connection already defined (and open)
        # for the current logical connection returns it to the
        # proper caller method, otherwise goes for creation
        if self.connection: return self.connection
        if not create: return None

        # creates a new connection and sets it in the current
        # instance so that it may be properly re-used latter
        self.connection = pgdb.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        self.transaction_level = 0

        # sets the isolation level for the connection as the one
        # defined to be the default one by the "driver"
        self._execute_query(
            "set session characteristics as transaction isolation level %s" % self.isolation
        ).close()

        # returns the correct connection that has been created
        # to the caller method, os that it may be used
        return self.connection

    def ensure_connection(self):
        # by default ensure a connection is exactly the same operation
        # as the retrieving a singleton based connection
        self.get_connection()

    def close(self):
        # verifies if there's an open and valid "physical" connection
        # and if taht's the case closes it and unsets the value
        if not self.connection: return
        self.connection.close()
        self.connection = None
        self.transaction_level = 0

    def reopen(self):
        """
        Triggers the "forced" re-opening of the remote database connection
        for that it invalidates the connection closing it an dereferencing
        it in the internal structures.

        This method only invalidates the proper connection for the current
        thread all the other connection in the other threads remain open.

        For this kind of strategy (single thread support) this operations
        is equivalent to the close one.
        """

        self.close()

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
        self.ensure_connection()
        self.transaction_level += 1

    def pop_transaction(self):
        self.ensure_connection()
        self.transaction_level -= 1

    def reset_transaction(self):
        self.transaction_level = 0

    def isolation_level(self, isolation):
        self.isolation = isolation
        self._execute_query("set transaction isolation level %s" % self.isolation)

    def is_close(self):
        connection = self.get_connection(create = False)
        is_close = connection == None
        return is_close

    def is_empty_transaction(self):
        is_empty_transaction = self.transaction_level == 0
        return is_empty_transaction

    def is_valid_transaction(self):
        is_valid_transaction = self.transaction_level >= 0
        return is_valid_transaction

    def get_database(self):
        return self.database

    def get_database_encoding(self):
        # checks if the current object already contains the encoding
        # attribute set for such cases the retrieval is immediate
        if hasattr(self, "_encoding"): return self._encoding

        # retrieves the query to be used in the retrieval of the
        # database encoding and executes it retrieving the encoding
        # used in the current database
        query = self._database_encoding_query(self.database)
        cursor = self._execute_query(query)
        try: result = self._database_encoding_result(cursor)
        finally: cursor.close()

        # caches the database encoding into the current
        # connection object (no need to retrieve it again
        # from the data source) then returns it to the caller
        self._encoding = result
        return result

    def _database_encoding_query(self, database_name):
        query = "select pg_encoding_to_char(encoding) from pg_database where datname = '%s';" % database_name
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

class IntegrityError(RuntimeError):
    pass
