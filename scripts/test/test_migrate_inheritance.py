#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys
import time
import sqlite3
import tempfile
import unittest

# adds the scripts directory to the path to allow importing
# the migration script directly
_script_dir = os.path.dirname(os.path.abspath(__file__))
_scripts_dir = os.path.dirname(_script_dir)
sys.path.insert(0, _scripts_dir)

import migrate_inheritance

# -- Mock entity classes -----------------------------------------------------
# These provide the minimal interface required by the migration script
# for hierarchy traversal and column resolution, without depending on
# the Colony entity manager infrastructure.


class MockEntityBase(object):
    """
    Base mock entity class providing the minimal interface
    required by the migration script for hierarchy traversal
    and column resolution.
    """

    inheritance = "class_table"
    abstract = False

    @classmethod
    def get_name(cls):
        result = ""
        for i, char in enumerate(cls.__name__):
            if char.isupper() and i > 0:
                result += "_"
            result += char.lower()
        return "_" + result

    @classmethod
    def get_id(cls):
        items = cls._own_items()
        for name, value in items.items():
            if value.get("id", False):
                return name
        parents = cls._get_entity_parents()
        for parent in parents:
            parent_id = parent.get_id()
            if parent_id:
                return parent_id
        return None

    @classmethod
    def is_abstract(cls):
        return cls.abstract

    @classmethod
    def get_inheritance_strategy(cls):
        if "inheritance" in cls.__dict__:
            return cls.inheritance
        parents = cls._get_entity_parents()
        for parent in parents:
            strategy = parent.get_inheritance_strategy()
            if strategy != "class_table":
                return strategy
        return "class_table"

    @classmethod
    def _get_entity_parents(cls):
        parents = []
        for base in cls.__bases__:
            if base == MockEntityBase or base == object:
                continue
            parents.append(base)
        return parents

    @classmethod
    def get_parents(cls):
        return cls._get_entity_parents()

    @classmethod
    def get_all_parents(cls):
        all_parents = []
        for parent in cls.get_parents():
            for grandparent in parent.get_all_parents():
                if grandparent not in all_parents:
                    all_parents.append(grandparent)
            if parent not in all_parents:
                all_parents.append(parent)
        return all_parents

    @classmethod
    def has_parents(cls):
        parents = cls._get_entity_parents()
        if not parents:
            return False
        if len(parents) == 1 and parents[0] == MockEntityBase:
            return False
        return True

    @classmethod
    def _own_items(cls):
        items = {}
        for key, value in cls.__dict__.items():
            if key.startswith("_"):
                continue
            if key[0].isupper():
                continue
            if not isinstance(value, dict):
                continue
            if "type" not in value:
                continue
            items[key] = value
        return items

    @classmethod
    def get_items(cls):
        return cls._own_items()

    @classmethod
    def get_all_items(cls):
        all_items = {}
        for parent in cls.get_all_parents():
            all_items.update(parent._own_items())
        all_items.update(cls._own_items())
        return all_items

    @classmethod
    def get_names_map(cls):
        names_map = {}
        for parent in cls.get_all_parents():
            for name in parent._own_items():
                names_map[name] = parent
        for name in cls._own_items():
            names_map[name] = cls
        return names_map

    @classmethod
    def is_relation(cls, name):
        all_items = cls.get_all_items()
        item = all_items.get(name, None)
        if item == None:
            return False
        return item.get("type") == "relation"

    @classmethod
    def is_mapped(cls, name):
        return False

    @classmethod
    def get_target(cls, name):
        return cls


# CTI hierarchy mocks (class_table strategy)


class MockRootEntity(MockEntityBase):
    object_id = dict(id=True, type="integer", generated=True)
    status = dict(type="integer")


class MockPerson(MockRootEntity):
    name = dict(type="text")
    age = dict(type="integer")


class MockEmployee(MockPerson):
    salary = dict(type="integer")


# Concrete table hierarchy mocks (concrete_table strategy)


class MockConcreteRoot(MockEntityBase):
    inheritance = "concrete_table"
    object_id = dict(id=True, type="integer", generated=True)
    status = dict(type="integer")


class MockConcretePerson(MockConcreteRoot):
    name = dict(type="text")
    age = dict(type="integer")


class MockConcreteEmployee(MockConcretePerson):
    salary = dict(type="integer")


# -- Helper functions --------------------------------------------------------


def _create_cti_database():
    """
    Creates a temporary SQLite database with a CTI schema matching
    MockRootEntity -> MockPerson -> MockEmployee, inserts test data,
    and returns the (connection, file_path) tuple.
    """

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute(
        "create table _mock_root_entity("
        "object_id integer primary key, "
        "status integer, "
        "_class text, "
        "_mtime double precision)"
    )
    cursor.execute(
        "create table _mock_person("
        "name text, "
        "age integer, "
        "_mtime double precision, "
        "object_id integer primary key)"
    )
    cursor.execute(
        "create table _mock_employee("
        "salary integer, "
        "_mtime double precision, "
        "object_id integer primary key)"
    )

    mtime = time.time()

    # inserts a person (id=1) and an employee (id=2)
    cursor.execute(
        "insert into _mock_root_entity values(1, 1, 'MockPerson', ?)", (mtime,)
    )
    cursor.execute("insert into _mock_person values('person_one', 25, ?, 1)", (mtime,))
    cursor.execute(
        "insert into _mock_root_entity values(2, 1, 'MockEmployee', ?)", (mtime,)
    )
    cursor.execute(
        "insert into _mock_person values('employee_one', 30, ?, 2)", (mtime,)
    )
    cursor.execute("insert into _mock_employee values(500, ?, 2)", (mtime,))

    conn.commit()
    cursor.close()
    return conn, path


def _create_concrete_database():
    """
    Creates a temporary SQLite database with a concrete table schema
    matching MockConcreteRoot -> MockConcretePerson -> MockConcreteEmployee,
    inserts test data, and returns the (connection, file_path) tuple.
    """

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute(
        "create table _mock_concrete_root("
        "object_id integer primary key, "
        "status integer, "
        "_class text, "
        "_mtime double precision)"
    )
    cursor.execute(
        "create table _mock_concrete_person("
        "object_id integer primary key, "
        "status integer, "
        "name text, "
        "age integer, "
        "_class text, "
        "_mtime double precision)"
    )
    cursor.execute(
        "create table _mock_concrete_employee("
        "object_id integer primary key, "
        "status integer, "
        "name text, "
        "age integer, "
        "salary integer, "
        "_class text, "
        "_mtime double precision)"
    )

    mtime = time.time()

    # inserts a person (id=1) into root + person tables
    cursor.execute(
        "insert into _mock_concrete_root values(1, 1, 'MockConcretePerson', ?)",
        (mtime,),
    )
    cursor.execute(
        "insert into _mock_concrete_person values(1, 1, 'person_one', 25, "
        "'MockConcretePerson', ?)",
        (mtime,),
    )

    # inserts an employee (id=2) into root + person + employee tables
    cursor.execute(
        "insert into _mock_concrete_root values(2, 1, 'MockConcreteEmployee', ?)",
        (mtime,),
    )
    cursor.execute(
        "insert into _mock_concrete_person values(2, 1, 'employee_one', 30, "
        "'MockConcreteEmployee', ?)",
        (mtime,),
    )
    cursor.execute(
        "insert into _mock_concrete_employee values(2, 1, 'employee_one', 30, "
        "500, 'MockConcreteEmployee', ?)",
        (mtime,),
    )

    conn.commit()
    cursor.close()
    return conn, path


def _table_exists(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(
        "select count(*) from sqlite_master where type='table' and name=?",
        (table_name,),
    )
    result = cursor.fetchone()[0]
    cursor.close()
    return result > 0


def _count_rows(connection, table_name):
    cursor = connection.cursor()
    cursor.execute("select count(*) from %s" % table_name)
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def _get_columns(connection, table_name):
    cursor = connection.cursor()
    cursor.execute("pragma table_info(%s)" % table_name)
    columns = [row[1] for row in cursor.fetchall()]
    cursor.close()
    return columns


# -- Test cases --------------------------------------------------------------


class MigrateInheritanceValidateTestCase(unittest.TestCase):
    """
    Tests for the validate_hierarchy function, verifying that
    hierarchy validation correctly accepts or rejects migration
    requests based on the current and target strategies.
    """

    def test_validate_same_strategy(self):
        is_valid, messages = migrate_inheritance.validate_hierarchy(
            MockRootEntity, "class_table"
        )
        self.assertFalse(is_valid)
        self.assertTrue(any("already uses" in m for m in messages))

    def test_validate_concrete_same_strategy(self):
        is_valid, messages = migrate_inheritance.validate_hierarchy(
            MockConcreteRoot, "concrete_table"
        )
        self.assertFalse(is_valid)
        self.assertTrue(any("already uses" in m for m in messages))

    def test_validate_cti_to_concrete(self):
        is_valid, messages = migrate_inheritance.validate_hierarchy(
            MockRootEntity, "concrete_table"
        )
        self.assertTrue(is_valid)
        self.assertTrue(any("validation passed" in m for m in messages))

    def test_validate_concrete_to_cti(self):
        is_valid, messages = migrate_inheritance.validate_hierarchy(
            MockConcreteRoot, "class_table"
        )
        self.assertTrue(is_valid)
        self.assertTrue(any("validation passed" in m for m in messages))


class MigrateInheritanceQueryTestCase(unittest.TestCase):
    """
    Tests for the query generation functions, verifying that the
    generated SQL contains the expected statement types for both
    migration directions.
    """

    def test_generate_queries_cti_to_concrete(self):
        queries = migrate_inheritance.generate_cti_to_concrete_queries(MockRootEntity)
        self.assertNotEqual(queries, [])

        create_queries = [q for q in queries if q.startswith("create table")]
        self.assertTrue(len(create_queries) > 0)

        insert_queries = [q for q in queries if q.startswith("insert into")]
        self.assertTrue(len(insert_queries) > 0)

        drop_queries = [q for q in queries if q.startswith("drop table")]
        self.assertTrue(len(drop_queries) > 0)

        alter_queries = [q for q in queries if q.startswith("alter table")]
        self.assertTrue(len(alter_queries) > 0)

    def test_generate_queries_concrete_to_cti(self):
        queries = migrate_inheritance.generate_concrete_to_cti_queries(MockConcreteRoot)
        self.assertNotEqual(queries, [])

        create_queries = [q for q in queries if q.startswith("create table")]
        self.assertTrue(len(create_queries) > 0)

        insert_queries = [q for q in queries if q.startswith("insert")]
        self.assertTrue(len(insert_queries) > 0)

        drop_queries = [q for q in queries if q.startswith("drop table")]
        self.assertTrue(len(drop_queries) > 0)


class MigrateInheritanceEngineTestCase(unittest.TestCase):
    """
    Tests for the engine-specific SQL generation helpers, verifying
    that each database engine produces correct syntax for index
    creation and duplicate-safe inserts.
    """

    def test_index_query_sqlite(self):
        query = migrate_inheritance.index_query(
            "_person", "object_id", "hash", "sqlite"
        )
        self.assertEqual(
            query, "create index _person_object_id_hash on _person(object_id)"
        )

    def test_index_query_mysql(self):
        query = migrate_inheritance.index_query("_person", "object_id", "hash", "mysql")
        self.assertEqual(
            query,
            "create index _person_object_id_hash on _person(object_id) using hash",
        )

    def test_index_query_pgsql(self):
        query = migrate_inheritance.index_query("_person", "object_id", "hash", "pgsql")
        self.assertEqual(
            query,
            "create index _person_object_id_hash on _person using hash (object_id)",
        )

    def test_index_name_truncation_mysql(self):
        long_table = "_very_long_table_name_that_exceeds_limits"
        long_attr = "very_long_attribute_name"
        query = migrate_inheritance.index_query(long_table, long_attr, "hash", "mysql")
        index_name = query.split(" on ")[0].replace("create index ", "")
        self.assertTrue(len(index_name) <= 64)

    def test_index_name_truncation_pgsql(self):
        long_table = "_very_long_table_name_that_exceeds_limits"
        long_attr = "very_long_attribute_name"
        query = migrate_inheritance.index_query(long_table, long_attr, "hash", "pgsql")
        index_name = query.split(" on ")[0].replace("create index ", "")
        self.assertTrue(len(index_name) <= 63)

    def test_insert_ignore_sqlite(self):
        query = migrate_inheritance.insert_ignore_query(
            "_person", "id, name", "select id, name from _tmp", "sqlite"
        )
        self.assertTrue(query.startswith("insert or ignore into"))

    def test_insert_ignore_mysql(self):
        query = migrate_inheritance.insert_ignore_query(
            "_person", "id, name", "select id, name from _tmp", "mysql"
        )
        self.assertTrue(query.startswith("insert ignore into"))

    def test_insert_ignore_pgsql(self):
        query = migrate_inheritance.insert_ignore_query(
            "_person", "id, name", "select id, name from _tmp", "pgsql"
        )
        self.assertTrue(query.endswith("on conflict do nothing"))

    def test_generate_queries_mysql_indexes(self):
        queries = migrate_inheritance.generate_cti_to_concrete_queries(
            MockRootEntity, engine="mysql"
        )
        index_queries = [q for q in queries if q.startswith("create index")]
        self.assertTrue(len(index_queries) > 0)
        self.assertTrue(all("using" in q for q in index_queries))

    def test_generate_queries_pgsql_indexes(self):
        queries = migrate_inheritance.generate_cti_to_concrete_queries(
            MockRootEntity, engine="pgsql"
        )
        index_queries = [q for q in queries if q.startswith("create index")]
        self.assertTrue(len(index_queries) > 0)
        self.assertTrue(all("using" in q for q in index_queries))

    def test_generate_queries_concrete_to_cti_mysql(self):
        queries = migrate_inheritance.generate_concrete_to_cti_queries(
            MockConcreteRoot, engine="mysql"
        )
        insert_queries = [q for q in queries if q.startswith("insert")]
        self.assertTrue(len(insert_queries) > 0)
        self.assertTrue(all("insert ignore" in q for q in insert_queries))

    def test_generate_queries_concrete_to_cti_pgsql(self):
        queries = migrate_inheritance.generate_concrete_to_cti_queries(
            MockConcreteRoot, engine="pgsql"
        )
        insert_queries = [q for q in queries if q.startswith("insert")]
        self.assertTrue(len(insert_queries) > 0)
        self.assertTrue(all("on conflict do nothing" in q for q in insert_queries))


class MigrateInheritanceBackupTestCase(unittest.TestCase):
    """
    Tests for the backup functionality, verifying file creation,
    data integrity, and failure handling.
    """

    def test_backup_sqlite(self):
        conn, path = _create_cti_database()
        try:
            connection_params = dict(file_path=path)
            backup_path = migrate_inheritance.backup_database(
                connection_params, "sqlite"
            )
            try:
                self.assertTrue(os.path.exists(backup_path))
                self.assertTrue(os.path.getsize(backup_path) > 0)
                self.assertTrue(".backup." in backup_path)
            finally:
                if os.path.exists(backup_path):
                    os.remove(backup_path)
        finally:
            conn.close()
            os.remove(path)

    def test_backup_data_integrity(self):
        conn, path = _create_cti_database()
        try:
            connection_params = dict(file_path=path)
            backup_path = migrate_inheritance.backup_database(
                connection_params, "sqlite"
            )
            backup_conn = None
            try:
                backup_conn = sqlite3.connect(backup_path)
                cursor = backup_conn.cursor()

                cursor.execute(
                    "select count(*) from sqlite_master "
                    "where type='table' and name='_mock_root_entity'"
                )
                self.assertEqual(cursor.fetchone()[0], 1)

                cursor.execute(
                    "select count(*) from sqlite_master "
                    "where type='table' and name='_mock_person'"
                )
                self.assertEqual(cursor.fetchone()[0], 1)

                cursor.execute(
                    "select object_id, status from _mock_root_entity "
                    "where object_id = 1"
                )
                row = cursor.fetchone()
                self.assertNotEqual(row, None)
                self.assertEqual(row[0], 1)
                self.assertEqual(row[1], 1)

                cursor.execute("select name, age from _mock_person where object_id = 1")
                row = cursor.fetchone()
                self.assertNotEqual(row, None)
                self.assertEqual(row[0], "person_one")
                self.assertEqual(row[1], 25)
            finally:
                if backup_conn:
                    backup_conn.close()
                if os.path.exists(backup_path):
                    os.remove(backup_path)
        finally:
            conn.close()
            os.remove(path)

    def test_migrate_creates_backup(self):
        conn, path = _create_concrete_database()
        try:
            connection_params = dict(file_path=path)

            # uses a failing connection so the migration fails after
            # the backup is created, isolating the backup step
            class FailAfterBackupCursor(object):
                def execute(self, query, *args):
                    if query.startswith("select count"):
                        return
                    raise Exception("intentional failure after backup")

                def fetchone(self):
                    return (1,)

                def close(self):
                    pass

            class FailAfterBackupConnection(object):
                def cursor(self):
                    return FailAfterBackupCursor()

                def commit(self):
                    pass

                def rollback(self):
                    pass

            failing_conn = FailAfterBackupConnection()

            success, messages = migrate_inheritance.migrate(
                entity_class=MockConcreteRoot,
                target_strategy="class_table",
                connection=failing_conn,
                engine="sqlite",
                connection_params=connection_params,
                skip_backup=False,
            )

            self.assertFalse(success)
            backup_messages = [m for m in messages if "backup created" in m]
            self.assertEqual(len(backup_messages), 1)

            backup_msg = backup_messages[0]
            backup_path = backup_msg.split("backup created at: ")[1]
            try:
                self.assertTrue(os.path.exists(backup_path))
                self.assertTrue(os.path.getsize(backup_path) > 0)
            finally:
                if os.path.exists(backup_path):
                    os.remove(backup_path)
        finally:
            conn.close()
            os.remove(path)

    def test_migrate_aborts_on_backup_failure(self):
        conn, path = _create_concrete_database()
        try:
            connection_params = dict(file_path="/nonexistent/path/database.db")

            success, messages = migrate_inheritance.migrate(
                entity_class=MockConcreteRoot,
                target_strategy="class_table",
                connection=conn,
                engine="sqlite",
                connection_params=connection_params,
                skip_backup=False,
            )

            self.assertFalse(success)
            self.assertTrue(any("failed to create backup" in m for m in messages))
        finally:
            conn.close()
            os.remove(path)


class MigrateInheritanceDryRunTestCase(unittest.TestCase):
    """
    Tests for the dry-run mode, verifying that SQL is generated
    but no changes are made to the data source.
    """

    def test_dry_run_cti_to_concrete(self):
        conn, path = _create_cti_database()
        try:
            success, messages = migrate_inheritance.migrate(
                entity_class=MockRootEntity,
                target_strategy="concrete_table",
                connection=conn,
                engine="sqlite",
                dry_run=True,
                skip_backup=True,
            )

            self.assertTrue(success)
            self.assertTrue(any("dry-run mode" in m for m in messages))
            self.assertTrue(any("create table" in m for m in messages))

            # verifies that the original tables still exist unchanged
            self.assertTrue(_table_exists(conn, "_mock_root_entity"))
            self.assertTrue(_table_exists(conn, "_mock_person"))
        finally:
            conn.close()
            os.remove(path)

    def test_dry_run_concrete_to_cti(self):
        conn, path = _create_concrete_database()
        try:
            success, messages = migrate_inheritance.migrate(
                entity_class=MockConcreteRoot,
                target_strategy="class_table",
                connection=conn,
                engine="sqlite",
                dry_run=True,
                skip_backup=True,
            )

            self.assertTrue(success)
            self.assertTrue(any("dry-run mode" in m for m in messages))
            self.assertTrue(any("create table" in m for m in messages))

            # verifies that the original tables still exist unchanged
            self.assertTrue(_table_exists(conn, "_mock_concrete_person"))
        finally:
            conn.close()
            os.remove(path)


class MigrateInheritanceRollbackTestCase(unittest.TestCase):
    """
    Tests for transaction rollback on migration failure, verifying
    that the database remains unchanged when a query fails.
    """

    def test_migrate_rollback_on_failure(self):
        conn, path = _create_cti_database()
        try:
            # wraps the connection to fail after the first migration
            # query, allowing table existence checks to pass through
            class FailingCursor(object):
                def __init__(self, real_cursor):
                    self._real = real_cursor
                    self._count = 0

                def execute(self, query, *args):
                    is_migration_query = any(
                        query.startswith(k)
                        for k in ("create ", "insert ", "drop ", "alter ")
                    )
                    if is_migration_query:
                        self._count += 1
                        if self._count > 1:
                            raise Exception("simulated failure")
                    return self._real.execute(query, *args)

                def fetchone(self):
                    return self._real.fetchone()

                def close(self):
                    return self._real.close()

            class FailingConnection(object):
                def __init__(self, real_conn):
                    self._real = real_conn
                    self._rolled_back = False

                def cursor(self):
                    return FailingCursor(self._real.cursor())

                def commit(self):
                    return self._real.commit()

                def rollback(self):
                    self._rolled_back = True
                    return self._real.rollback()

            failing_conn = FailingConnection(conn)

            success, messages = migrate_inheritance.migrate(
                entity_class=MockRootEntity,
                target_strategy="concrete_table",
                connection=failing_conn,
                engine="sqlite",
                skip_backup=True,
            )

            self.assertFalse(success)
            self.assertTrue(any("migration failed" in m for m in messages))
            self.assertTrue(any("rolled back" in m for m in messages))
            self.assertTrue(failing_conn._rolled_back)
        finally:
            conn.close()
            os.remove(path)


class MigrateInheritanceEndToEndTestCase(unittest.TestCase):
    """
    End-to-end migration tests that create a real database with
    data, run the migration, and verify the resulting schema and
    data integrity.
    """

    def test_end_to_end_cti_to_concrete(self):
        conn, path = _create_cti_database()
        try:
            # verifies the CTI table structure before migration
            self.assertTrue(_table_exists(conn, "_mock_root_entity"))
            self.assertTrue(_table_exists(conn, "_mock_person"))
            self.assertTrue(_table_exists(conn, "_mock_employee"))
            self.assertEqual(_count_rows(conn, "_mock_root_entity"), 2)
            self.assertEqual(_count_rows(conn, "_mock_person"), 2)
            self.assertEqual(_count_rows(conn, "_mock_employee"), 1)

            # verifies that _mock_person does NOT have the status
            # column (it's in _mock_root_entity in CTI mode)
            person_cols = _get_columns(conn, "_mock_person")
            self.assertFalse("status" in person_cols)

            # runs the migration
            success, messages = migrate_inheritance.migrate(
                entity_class=MockRootEntity,
                target_strategy="concrete_table",
                connection=conn,
                engine="sqlite",
                skip_backup=True,
            )
            self.assertTrue(success, "migration failed: %s" % "; ".join(messages))

            # verifies the new concrete table structure
            self.assertTrue(_table_exists(conn, "_mock_root_entity"))
            self.assertTrue(_table_exists(conn, "_mock_person"))
            self.assertTrue(_table_exists(conn, "_mock_employee"))

            # verifies that _mock_person NOW has the inherited
            # status column
            person_cols = _get_columns(conn, "_mock_person")
            self.assertTrue("status" in person_cols)
            self.assertTrue("name" in person_cols)
            self.assertTrue("object_id" in person_cols)

            # verifies that _mock_employee has ALL columns
            employee_cols = _get_columns(conn, "_mock_employee")
            self.assertTrue("status" in employee_cols)
            self.assertTrue("name" in employee_cols)
            self.assertTrue("salary" in employee_cols)

            # verifies data integrity: row counts at each level
            self.assertEqual(_count_rows(conn, "_mock_root_entity"), 2)
            self.assertEqual(_count_rows(conn, "_mock_person"), 2)
            self.assertEqual(_count_rows(conn, "_mock_employee"), 1)

            # verifies actual values in the migrated tables
            cursor = conn.cursor()

            cursor.execute(
                "select object_id, status, name, age, salary, _class "
                "from _mock_employee where object_id = 2"
            )
            row = cursor.fetchone()
            self.assertNotEqual(row, None)
            self.assertEqual(row[0], 2)
            self.assertEqual(row[1], 1)
            self.assertEqual(row[2], "employee_one")
            self.assertEqual(row[3], 30)
            self.assertEqual(row[4], 500)
            self.assertEqual(row[5], "MockEmployee")

            # verifies the employee row also exists in _mock_person
            cursor.execute(
                "select object_id, status, name, _class "
                "from _mock_person where object_id = 2"
            )
            row = cursor.fetchone()
            self.assertNotEqual(row, None)
            self.assertEqual(row[2], "employee_one")
            self.assertEqual(row[3], "MockEmployee")

            # verifies both entities exist in _mock_root_entity
            cursor.execute("select count(*) from _mock_root_entity")
            self.assertEqual(cursor.fetchone()[0], 2)

            cursor.close()
        finally:
            conn.close()
            os.remove(path)

    def test_end_to_end_concrete_to_cti(self):
        conn, path = _create_concrete_database()
        try:
            # verifies the concrete table structure before migration
            self.assertTrue(_table_exists(conn, "_mock_concrete_root"))
            self.assertTrue(_table_exists(conn, "_mock_concrete_person"))
            self.assertTrue(_table_exists(conn, "_mock_concrete_employee"))

            # verifies that _mock_concrete_person has the inherited
            # status column (concrete table mode)
            person_cols = _get_columns(conn, "_mock_concrete_person")
            self.assertTrue("status" in person_cols)

            # runs the migration
            success, messages = migrate_inheritance.migrate(
                entity_class=MockConcreteRoot,
                target_strategy="class_table",
                connection=conn,
                engine="sqlite",
                skip_backup=True,
            )
            self.assertTrue(success, "migration failed: %s" % "; ".join(messages))

            # verifies the CTI table structure after migration
            self.assertTrue(_table_exists(conn, "_mock_concrete_root"))
            self.assertTrue(_table_exists(conn, "_mock_concrete_person"))
            self.assertTrue(_table_exists(conn, "_mock_concrete_employee"))

            # verifies that _mock_concrete_person in CTI mode does
            # NOT have the status column (belongs to root)
            person_cols = _get_columns(conn, "_mock_concrete_person")
            self.assertTrue("name" in person_cols)
            self.assertFalse("status" in person_cols)

            # verifies data integrity
            cursor = conn.cursor()

            cursor.execute("select count(*) from _mock_concrete_root")
            self.assertEqual(cursor.fetchone()[0], 2)

            cursor.execute(
                "select object_id, salary from _mock_concrete_employee "
                "where object_id = 2"
            )
            row = cursor.fetchone()
            self.assertNotEqual(row, None)
            self.assertEqual(row[0], 2)
            self.assertEqual(row[1], 500)

            cursor.execute(
                "select object_id, name, age from _mock_concrete_person "
                "where object_id = 1"
            )
            row = cursor.fetchone()
            self.assertNotEqual(row, None)
            self.assertEqual(row[1], "person_one")
            self.assertEqual(row[2], 25)

            cursor.execute("select _class from _mock_concrete_root where object_id = 2")
            row = cursor.fetchone()
            self.assertNotEqual(row, None)
            self.assertEqual(row[0], "MockConcreteEmployee")

            cursor.close()
        finally:
            conn.close()
            os.remove(path)

    def test_migration_preserves_indexes(self):
        conn, path = _create_cti_database()
        try:
            success, messages = migrate_inheritance.migrate(
                entity_class=MockRootEntity,
                target_strategy="concrete_table",
                connection=conn,
                engine="sqlite",
                skip_backup=True,
            )
            self.assertTrue(success)

            # verifies that indexes were recreated on the migrated tables
            cursor = conn.cursor()
            cursor.execute(
                "select count(*) from sqlite_master where type='index' "
                "and tbl_name='_mock_person'"
            )
            index_count = cursor.fetchone()[0]
            cursor.close()

            # should have at least: pk_hash, pk_btree, mtime_hash, mtime_btree
            self.assertTrue(index_count >= 4)
        finally:
            conn.close()
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
