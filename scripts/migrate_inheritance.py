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
import shutil
import sqlite3
import argparse
import subprocess

SQL_TYPES_MAP = dict(
    text="text",
    string="varchar(255)",
    integer="integer",
    long="bigint",
    float="double precision",
    decimal="double precision",
    date="double precision",
    data="text",
    metadata="text",
)
""" The default SQL types map, used for column type resolution
when generating migration queries """

INDEX_NAME_LIMITS = dict(sqlite=None, mysql=64, pgsql=63)
""" The maximum length for index names per engine, None means
no limit (SQLite has no practical limit) """


def has_table(connection, table_name, engine="sqlite"):
    """
    Checks if a table exists in the data source using the
    appropriate engine-specific catalog query.

    :type connection: Connection
    :param connection: The database connection.
    :type table_name: String
    :param table_name: The name of the table to check.
    :type engine: String
    :param engine: The database engine name.
    :rtype: bool
    :return: If the table exists in the data source.
    """

    cursor = connection.cursor()
    try:
        if engine == "sqlite":
            cursor.execute(
                "select count(*) from sqlite_master " "where type='table' and name=?",
                (table_name,),
            )
        elif engine == "mysql":
            cursor.execute(
                "select count(*) from information_schema.tables "
                "where table_name = %s",
                (table_name,),
            )
        elif engine == "pgsql":
            cursor.execute(
                "select count(*) from pg_tables " "where tablename = %s",
                (table_name,),
            )
        else:
            return True
        return cursor.fetchone()[0] > 0
    finally:
        cursor.close()


def index_query(table_name, attribute_name, index_type, engine="sqlite"):
    """
    Generates a CREATE INDEX query using the appropriate syntax
    for the given database engine, matching the naming convention
    used by the entity manager's engine implementations.

    :type table_name: String
    :param table_name: The name of the table.
    :type attribute_name: String
    :param attribute_name: The name of the column to index.
    :type index_type: String
    :param index_type: The type of index ("hash" or "btree").
    :type engine: String
    :param engine: The database engine name.
    :rtype: String
    :return: The CREATE INDEX query.
    """

    index_name = "%s_%s_%s" % (table_name, attribute_name, index_type)

    # truncates the index name to the engine-specific limit
    limit = INDEX_NAME_LIMITS.get(engine, None)
    if limit:
        index_name = index_name[-limit:]

    if engine == "mysql":
        return "create index %s on %s(%s) using %s" % (
            index_name,
            table_name,
            attribute_name,
            index_type,
        )
    elif engine == "pgsql":
        return "create index %s on %s using %s (%s)" % (
            index_name,
            table_name,
            index_type,
            attribute_name,
        )
    else:
        return "create index %s on %s(%s)" % (
            index_name,
            table_name,
            attribute_name,
        )


def insert_ignore_query(table_name, columns, select_sql, engine="sqlite"):
    """
    Generates an INSERT query that ignores duplicate key conflicts
    using the appropriate engine-specific syntax.

    :type table_name: String
    :param table_name: The target table name.
    :type columns: String
    :param columns: The comma-separated column list.
    :type select_sql: String
    :param select_sql: The SELECT statement to use as data source.
    :type engine: String
    :param engine: The database engine name.
    :rtype: String
    :return: The INSERT IGNORE query.
    """

    if engine == "mysql":
        return "insert ignore into %s(%s) %s" % (table_name, columns, select_sql)
    elif engine == "pgsql":
        return "insert into %s(%s) %s on conflict do nothing" % (
            table_name,
            columns,
            select_sql,
        )
    else:
        return "insert or ignore into %s(%s) %s" % (table_name, columns, select_sql)


def get_hierarchy_classes(entity_class):
    """
    Retrieves the complete list of concrete (non-abstract) classes
    in the hierarchy, ordered from root to leaf. Includes the root
    class itself if it is not abstract.

    :type entity_class: EntityClass
    :param entity_class: The root entity class.
    :rtype: list
    :return: The ordered list of concrete classes in the hierarchy.
    """

    classes = []
    if not entity_class.is_abstract():
        classes.append(entity_class)

    def _collect(cls):
        for subclass in cls.__subclasses__():
            # avoids duplicates from multiple inheritance paths
            # (e.g. Employee inherits from both Person and Taxable)
            if subclass in classes:
                continue
            if not subclass.is_abstract():
                classes.append(subclass)
            _collect(subclass)

    _collect(entity_class)
    return classes


def get_column_definitions(entity_class, types_map):
    """
    Builds the column definitions for a concrete table at the
    given hierarchy level. Returns a list of (name, sql_type, is_pk)
    tuples for all items including inherited ones.

    Uses the entity class's own get_all_items() to retrieve the
    flattened set of fields, and resolves SQL types using the
    entity class's own type metadata.

    :type entity_class: EntityClass
    :param entity_class: The entity class.
    :type types_map: dict
    :param types_map: The SQL types map.
    :rtype: list
    :return: List of (name, sql_type, is_pk) tuples.
    """

    columns = []
    all_items = entity_class.get_all_items()

    for item_name, item_value in all_items.items():
        # skips unmapped relations (they use indirect/junction tables
        # which are independent of the inheritance strategy)
        if entity_class.is_relation(item_name):
            if not entity_class.is_mapped(item_name):
                continue
            target_class = entity_class.get_target(item_name)
            target_id = target_class.get_id()
            target_id_value = getattr(target_class, target_id)
            sql_type = types_map.get(target_id_value.get("type", "integer"), "integer")
        else:
            sql_type = types_map.get(item_value.get("type", "integer"), "integer")

        is_pk = item_value.get("id", False)
        columns.append((item_name, sql_type, is_pk))

    return columns


def get_source_table_for_column(entity_class, item_name):
    """
    Determines which CTI table a column originates from, by
    walking the names_map to find the declaring class.

    :type entity_class: EntityClass
    :param entity_class: The entity class.
    :type item_name: String
    :param item_name: The column name.
    :rtype: String
    :return: The table name where the column is defined.
    """

    names_map = entity_class.get_names_map()
    declaring_class = names_map.get(item_name, entity_class)
    return declaring_class.get_name()


def backup_database(connection_params, engine):
    """
    Creates a backup of the database before migration.

    For SQLite databases the file is copied, for PostgreSQL
    and MySQL the appropriate dump utilities are used.

    :type connection_params: dict
    :param connection_params: The connection parameters.
    :type engine: String
    :param engine: The database engine name.
    :rtype: String
    :return: The path to the backup file.
    """

    timestamp = int(time.time())

    if engine == "sqlite":
        file_path = connection_params.get("file_path", "")
        backup_path = "%s.backup.%d" % (file_path, timestamp)
        shutil.copy2(file_path, backup_path)
        return backup_path

    elif engine == "pgsql":
        host = connection_params.get("host", "localhost")
        database = connection_params.get("database", "")
        backup_path = "%s.backup.%d.sql" % (database, timestamp)
        subprocess.check_call(["pg_dump", "-h", host, "-f", backup_path, database])
        return backup_path

    elif engine == "mysql":
        host = connection_params.get("host", "localhost")
        database = connection_params.get("database", "")
        user = connection_params.get("user", "root")
        backup_path = "%s.backup.%d.sql" % (database, timestamp)
        with open(backup_path, "w") as f:
            subprocess.check_call(
                ["mysqldump", "-h", host, "-u", user, database], stdout=f
            )
        return backup_path

    raise ValueError("unsupported engine for backup: %s" % engine)


def validate_hierarchy(entity_class, target_strategy):
    """
    Validates that a hierarchy can be migrated to the target
    strategy without issues.

    Checks for unsupported mixed configurations, orphaned
    references, and other potential problems.

    :type entity_class: EntityClass
    :param entity_class: The root entity class.
    :type target_strategy: String
    :param target_strategy: The target inheritance strategy.
    :rtype: tuple
    :return: A tuple of (is_valid, messages) where messages is a
    list of validation messages.
    """

    messages = []
    is_valid = True

    # retrieves the current strategy
    current_strategy = entity_class.get_inheritance_strategy()

    # verifies that the target strategy is different from current
    if current_strategy == target_strategy:
        messages.append(
            "hierarchy already uses '%s' strategy, no migration needed"
            % target_strategy
        )
        return False, messages

    # retrieves all concrete classes in the hierarchy
    hierarchy = get_hierarchy_classes(entity_class)

    # verifies that there are concrete classes to migrate
    if not hierarchy:
        messages.append("no concrete classes found for migration")
        is_valid = False

    # verifies that the entity class has an id field
    table_id = entity_class.get_id()
    if table_id == None:
        messages.append("entity class has no id field defined")
        is_valid = False

    # verifies that all classes use the same strategy
    for cls in hierarchy:
        cls_strategy = cls.get_inheritance_strategy()
        if not cls_strategy == current_strategy:
            messages.append(
                "class '%s' uses '%s' strategy, expected '%s'"
                % (cls.__name__, cls_strategy, current_strategy)
            )
            is_valid = False

    if is_valid:
        messages.append("validation passed, hierarchy can be migrated")

    return is_valid, messages


def validate_data(connection, entity_class, messages):
    """
    Validates the existing data in the data source before
    migration, checking for orphaned rows and referential
    consistency across the CTI table hierarchy.

    :type connection: Connection
    :param connection: The database connection.
    :type entity_class: EntityClass
    :param entity_class: The root entity class.
    :type messages: list
    :param messages: The list to append validation messages to.
    :rtype: bool
    :return: True if the data is valid for migration.
    """

    is_valid = True
    hierarchy = get_hierarchy_classes(entity_class)
    table_id = entity_class.get_id()
    root_table = entity_class.get_name()

    for cls in hierarchy:
        if cls == entity_class:
            continue

        table_name = cls.get_name()
        all_parents = cls.get_all_parents()

        # checks that every row in a child table has a matching
        # row in each parent table (referential integrity)
        for parent in all_parents:
            if parent.is_abstract():
                continue
            parent_table = parent.get_name()

            cursor = connection.cursor()
            try:
                cursor.execute(
                    "select count(*) from %s where %s not in "
                    "(select %s from %s)"
                    % (table_name, table_id, table_id, parent_table)
                )
                orphan_count = cursor.fetchone()[0]
            finally:
                cursor.close()

            if orphan_count > 0:
                messages.append(
                    "found %d orphaned rows in '%s' with no match in '%s'"
                    % (orphan_count, table_name, parent_table)
                )
                is_valid = False

    return is_valid


def generate_cti_to_concrete_queries(
    entity_class, types_map=None, connection=None, engine="sqlite"
):
    """
    Generates the SQL queries to migrate an entity hierarchy
    from class table inheritance to concrete table inheritance.

    For each class in the hierarchy (root to leaf), creates a
    new flat table with all columns at that level, copies data
    from the joined CTI tables, drops the old tables, and
    renames the new ones. Recreates all indexes.

    The indirect relation (junction) tables are NOT modified
    because their column names reference entity table names
    which remain unchanged between strategies.

    When a connection is provided, only classes whose tables
    exist in the data source are included in the migration.

    :type entity_class: EntityClass
    :param entity_class: The root entity class of the hierarchy.
    :type types_map: dict
    :param types_map: The SQL types map to use for column types.
    :type connection: Connection
    :param connection: Optional connection for table existence checks.
    :rtype: list
    :return: The list of SQL queries to execute.
    """

    types_map = types_map or SQL_TYPES_MAP
    queries = []
    hierarchy = get_hierarchy_classes(entity_class)
    table_id = entity_class.get_id()
    root_table = entity_class.get_name()

    # when a connection is available, filters the hierarchy to only
    # include classes whose tables actually exist in the data source
    if connection:
        _hierarchy = []
        for cls in hierarchy:
            if has_table(connection, cls.get_name(), engine):
                _hierarchy.append(cls)
        hierarchy = _hierarchy

    # phase 1: create new flat tables and copy data
    for cls in hierarchy:
        table_name = cls.get_name()
        new_table_name = table_name + "__concrete_tmp"
        columns = get_column_definitions(cls, types_map)
        all_parents = cls.get_all_parents()

        # builds the CREATE TABLE statement with all flattened
        # columns plus the _class discriminator and _mtime
        col_defs = []
        for col_name, sql_type, is_pk in columns:
            pk = " primary key" if is_pk else ""
            col_defs.append("%s %s%s" % (col_name, sql_type, pk))
        col_defs.append("_class text")
        col_defs.append("_mtime double precision")
        queries.append("create table %s(%s)" % (new_table_name, ", ".join(col_defs)))

        # builds the SELECT to copy data from the old CTI tables,
        # each column is qualified with the table it originates from
        select_cols = []
        for col_name, sql_type, is_pk in columns:
            source_table = get_source_table_for_column(cls, col_name)
            select_cols.append("%s.%s" % (source_table, col_name))

        # adds the discriminator and mtime from the appropriate tables,
        # _class always lives in the root table, _mtime in the leaf
        select_cols.append("%s._class" % root_table)
        select_cols.append("%s._mtime" % table_name)

        # builds the FROM clause with the leaf table and INNER JOINs
        # to all non-abstract parent tables
        from_clause = table_name
        for parent in all_parents:
            if parent.is_abstract():
                continue
            parent_table = parent.get_name()
            from_clause += " inner join %s on %s.%s = %s.%s" % (
                parent_table,
                table_name,
                table_id,
                parent_table,
                table_id,
            )

        # for non-root classes, filters by _class to only get rows
        # belonging to this class and its descendants
        where_clause = ""
        if not cls == entity_class:
            # collects the class names that should be included at
            # this hierarchy level (this class + all descendants)
            class_names = [cls.__name__]
            for desc in get_hierarchy_classes(cls):
                if not desc == cls and desc.__name__ not in class_names:
                    class_names.append(desc.__name__)
            quoted_names = ", ".join(["'%s'" % n for n in class_names])
            where_clause = " where %s._class in (%s)" % (root_table, quoted_names)

        insert_query = "insert into %s select %s from %s%s" % (
            new_table_name,
            ", ".join(select_cols),
            from_clause,
            where_clause,
        )
        queries.append(insert_query)

    # phase 2: drop old CTI tables (leaf first, then parents)
    # collects all unique tables that need to be dropped
    tables_to_drop = []
    for cls in reversed(hierarchy):
        table_name = cls.get_name()
        if table_name not in tables_to_drop:
            tables_to_drop.append(table_name)
        for parent in cls.get_all_parents():
            if parent.is_abstract():
                continue
            parent_table = parent.get_name()
            if parent_table not in tables_to_drop:
                tables_to_drop.append(parent_table)

    for table_name in tables_to_drop:
        queries.append("drop table if exists %s" % table_name)

    # phase 3: rename new tables to the original names
    for cls in hierarchy:
        table_name = cls.get_name()
        new_table_name = table_name + "__concrete_tmp"
        queries.append("alter table %s rename to %s" % (new_table_name, table_name))

    # phase 4: recreate indexes on all new tables
    for cls in hierarchy:
        table_name = cls.get_name()

        # creates indexes on the primary key field (hash + btree)
        pk_name = cls.get_id()
        queries.append(index_query(table_name, pk_name, "hash", engine))
        queries.append(index_query(table_name, pk_name, "btree", engine))

        # creates indexes on the _mtime field (hash + btree)
        queries.append(index_query(table_name, "_mtime", "hash", engine))
        queries.append(index_query(table_name, "_mtime", "btree", engine))

        # creates indexes on mapped relation (foreign key) fields
        all_items = cls.get_all_items()
        for item_name in all_items:
            if cls.is_relation(item_name) and cls.is_mapped(item_name):
                queries.append(index_query(table_name, item_name, "hash", engine))

    return queries


def generate_concrete_to_cti_queries(
    entity_class, types_map=None, connection=None, engine="sqlite"
):
    """
    Generates the SQL queries to migrate an entity hierarchy
    from concrete table inheritance to class table inheritance.

    Splits the flat concrete tables into per-class-level tables
    where each table contains only its own columns plus a foreign
    key reference to the parent table.

    When a connection is provided, only classes whose tables
    exist in the data source are included in the migration.

    :type entity_class: EntityClass
    :param entity_class: The root entity class of the hierarchy.
    :type types_map: dict
    :param types_map: The SQL types map to use for column types.
    :type connection: Connection
    :param connection: Optional connection for table existence checks.
    :rtype: list
    :return: The list of SQL queries to execute.
    """

    types_map = types_map or SQL_TYPES_MAP
    queries = []
    hierarchy = get_hierarchy_classes(entity_class)

    # when a connection is available, filters the hierarchy to only
    # include classes whose tables actually exist in the data source
    if connection:
        _hierarchy = []
        for cls in hierarchy:
            if has_table(connection, cls.get_name(), engine):
                _hierarchy.append(cls)
        hierarchy = _hierarchy
    table_id = entity_class.get_id()
    table_id_value = getattr(entity_class, table_id)
    table_id_type = types_map.get(table_id_value.get("type", "integer"), "integer")

    # collects all unique class levels that need their own CTI table,
    # ordered from root to leaf
    class_levels = []
    for cls in hierarchy:
        for parent in cls.get_all_parents():
            if parent.is_abstract():
                continue
            if parent not in class_levels:
                class_levels.append(parent)
        if cls not in class_levels:
            class_levels.append(cls)

    # phase 1: create new per-level CTI tables
    for cls in class_levels:
        table_name = cls.get_name()
        new_table_name = table_name + "__cti_tmp"
        own_items = cls.get_items()

        col_defs = []
        id_set = False
        for item_name, item_value in own_items.items():
            if cls.is_relation(item_name):
                if not cls.is_mapped(item_name):
                    continue
                target_class = cls.get_target(item_name)
                target_id = target_class.get_id()
                target_id_value = getattr(target_class, target_id)
                sql_type = types_map.get(
                    target_id_value.get("type", "integer"), "integer"
                )
            else:
                sql_type = types_map.get(item_value.get("type", "integer"), "integer")

            pk = ""
            if item_value.get("id", False):
                pk = " primary key"
                id_set = True
            col_defs.append("%s %s%s" % (item_name, sql_type, pk))

        # adds _class discriminator for the root level
        if not cls.has_parents():
            col_defs.append("_class text")

        # adds _mtime
        col_defs.append("_mtime double precision")

        # adds upper reference for non-root classes (FK to parent)
        if not id_set:
            col_defs.append("%s %s primary key" % (table_id, table_id_type))

        queries.append("create table %s(%s)" % (new_table_name, ", ".join(col_defs)))

    # phase 2: copy data from the concrete tables into the CTI tables,
    # uses the leaf-most concrete table that contains each entity
    for cls in hierarchy:
        concrete_table = cls.get_name()

        for level in class_levels:
            # checks if this level is an ancestor (or self) of cls
            all_parents = cls.get_all_parents()
            if not level == cls and level not in all_parents:
                continue

            level_table = level.get_name()
            new_table_name = level_table + "__cti_tmp"
            own_items = level.get_items()

            select_cols = []
            for item_name in own_items:
                if level.is_relation(item_name):
                    if not level.is_mapped(item_name):
                        continue
                select_cols.append(item_name)

            # adds the id field if not already included
            if table_id not in select_cols:
                select_cols.append(table_id)

            # adds _class for root level
            if not level.has_parents():
                select_cols.append("_class")

            # adds _mtime
            select_cols.append("_mtime")

            # filters to only get rows for this specific class to
            # avoid duplicates when multiple concrete classes map
            # to the same CTI level
            select_sql = "select %s from %s where _class = '%s'" % (
                ", ".join(select_cols),
                concrete_table,
                cls.__name__,
            )
            insert_query = insert_ignore_query(
                new_table_name, ", ".join(select_cols), select_sql, engine
            )
            queries.append(insert_query)

    # phase 3: drop old concrete tables
    for cls in reversed(hierarchy):
        table_name = cls.get_name()
        queries.append("drop table if exists %s" % table_name)

    # phase 4: rename new tables
    for level in class_levels:
        level_table = level.get_name()
        new_table_name = level_table + "__cti_tmp"
        queries.append("alter table %s rename to %s" % (new_table_name, level_table))

    # phase 5: recreate indexes on all CTI tables
    for level in class_levels:
        table_name = level.get_name()
        pk_name = level.get_id() or table_id

        queries.append(index_query(table_name, pk_name, "hash", engine))
        queries.append(index_query(table_name, pk_name, "btree", engine))
        queries.append(index_query(table_name, "_mtime", "hash", engine))
        queries.append(index_query(table_name, "_mtime", "btree", engine))

        own_items = level.get_items()
        for item_name in own_items:
            if level.is_relation(item_name) and level.is_mapped(item_name):
                queries.append(index_query(table_name, item_name, "hash", engine))

    return queries


def migrate(
    entity_class,
    target_strategy,
    connection,
    engine="sqlite",
    connection_params=None,
    types_map=None,
    dry_run=False,
    validate_only=False,
    skip_backup=False,
):
    """
    Migrates an entire entity hierarchy between class_table and
    concrete_table inheritance strategies.

    The migration runs inside a transaction for atomic rollback
    on failure. A backup is automatically created before migrating.

    :type entity_class: EntityClass
    :param entity_class: The root entity class of the hierarchy.
    :type target_strategy: String
    :param target_strategy: The target strategy ("class_table" or
    "concrete_table").
    :type connection: Connection
    :param connection: The database connection to use.
    :type engine: String
    :param engine: The database engine name.
    :type connection_params: dict
    :param connection_params: The connection parameters (for backup).
    :type types_map: dict
    :param types_map: The SQL types map for column type resolution.
    :type dry_run: bool
    :param dry_run: If True, prints the SQL without executing.
    :type validate_only: bool
    :param validate_only: If True, only validates without executing.
    :type skip_backup: bool
    :param skip_backup: If True, skips the backup step.
    :rtype: tuple
    :return: A tuple of (success, messages) indicating the result.
    """

    messages = []
    connection_params = connection_params or {}

    # validates the hierarchy first
    is_valid, validation_messages = validate_hierarchy(entity_class, target_strategy)
    messages.extend(validation_messages)

    if not is_valid:
        return False, messages

    if validate_only:
        return True, messages

    # determines the current strategy and generates the
    # appropriate migration queries
    current_strategy = entity_class.get_inheritance_strategy()

    if current_strategy == "class_table" and target_strategy == "concrete_table":
        queries = generate_cti_to_concrete_queries(
            entity_class, types_map, connection, engine
        )
    elif current_strategy == "concrete_table" and target_strategy == "class_table":
        queries = generate_concrete_to_cti_queries(
            entity_class, types_map, connection, engine
        )
    else:
        messages.append(
            "unsupported migration direction: %s -> %s"
            % (current_strategy, target_strategy)
        )
        return False, messages

    # in dry-run mode, just prints the queries
    if dry_run:
        messages.append("dry-run mode, no changes will be made")
        for query in queries:
            messages.append("  %s;" % query)
        return True, messages

    # creates a backup before migrating
    if not skip_backup:
        try:
            backup_path = backup_database(connection_params, engine)
            messages.append("backup created at: %s" % backup_path)
        except Exception as exception:
            messages.append("failed to create backup: %s" % str(exception))
            return False, messages

    # executes the migration queries inside a transaction
    try:
        cursor = connection.cursor()

        for query in queries:
            messages.append("executing: %s" % query)
            cursor.execute(query)

        connection.commit()
        messages.append("migration completed successfully")
        return True, messages

    except Exception as exception:
        # rolls back the transaction on failure
        try:
            connection.rollback()
        except Exception:
            pass
        messages.append("migration failed: %s" % str(exception))
        messages.append("transaction rolled back")
        return False, messages


def main():
    """
    Main entry point for the migration script, parses command
    line arguments and executes the migration.
    """

    parser = argparse.ArgumentParser(
        description="Migrate entity hierarchies between inheritance strategies"
    )
    parser.add_argument(
        "entity_class",
        help="the fully qualified name of the root entity class",
    )
    parser.add_argument(
        "target_strategy",
        choices=["class_table", "concrete_table"],
        help="the target inheritance strategy",
    )
    parser.add_argument(
        "--engine",
        choices=["sqlite", "mysql", "pgsql"],
        default="sqlite",
        help="the database engine (default: sqlite)",
    )
    parser.add_argument(
        "--database",
        required=True,
        help="the database file path (sqlite) or name (mysql/pgsql)",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="the database host (mysql/pgsql, default: localhost)",
    )
    parser.add_argument(
        "--user",
        default="root",
        help="the database user (mysql/pgsql, default: root)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the SQL without executing",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="validate the hierarchy without executing",
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help="skip the backup step",
    )

    args = parser.parse_args()

    # imports the entity class from the provided module path
    module_path, class_name = args.entity_class.rsplit(".", 1)
    module = __import__(module_path, fromlist=[class_name])
    entity_class = getattr(module, class_name)

    # creates the database connection
    connection_params = dict(
        file_path=args.database,
        database=args.database,
        host=args.host,
        user=args.user,
    )

    if args.engine == "sqlite":
        connection = sqlite3.connect(args.database)
    else:
        print("error: only SQLite connections are supported directly")
        print("for MySQL/PostgreSQL, use the migrate() function from Python")
        sys.exit(1)

    try:
        success, messages = migrate(
            entity_class=entity_class,
            target_strategy=args.target_strategy,
            connection=connection,
            engine=args.engine,
            connection_params=connection_params,
            dry_run=args.dry_run,
            validate_only=args.validate,
            skip_backup=args.skip_backup,
        )

        for message in messages:
            print(message)

        sys.exit(0 if success else 1)

    finally:
        connection.close()


if __name__ == "__main__":
    main()
