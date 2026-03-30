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

SAFE_CHARACTER = "_"
""" The character to be used in table names as the prefix that
provides safety to the creation of them (no reserved names) """

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


def get_table_name(entity_class):
    """
    Retrieves the safe table name for the given entity class,
    using the same convention as the entity manager.

    :type entity_class: EntityClass
    :param entity_class: The entity class to retrieve the name for.
    :rtype: String
    :return: The safe table name.
    """

    name = entity_class.__name__
    # converts CamelCase to snake_case
    result = ""
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            result += "_"
        result += char.lower()
    return SAFE_CHARACTER + result


def get_concrete_descendants(entity_class):
    """
    Retrieves all concrete (non-abstract) descendant classes
    of the given entity class, traversing the full hierarchy
    downward.

    :type entity_class: EntityClass
    :param entity_class: The root entity class.
    :rtype: list
    :return: The list of concrete descendant classes.
    """

    descendants = []
    for subclass in entity_class.__subclasses__():
        if not getattr(subclass, "abstract", False):
            descendants.append(subclass)
        descendants.extend(get_concrete_descendants(subclass))
    return descendants


def get_all_items(entity_class):
    """
    Retrieves all items (own + inherited) for the given entity
    class, flattened into a single dictionary.

    :type entity_class: EntityClass
    :param entity_class: The entity class.
    :rtype: dict
    :return: The map of all items.
    """

    if hasattr(entity_class, "get_all_items"):
        return entity_class.get_all_items()
    return entity_class.get_items()


def get_items(entity_class):
    """
    Retrieves the items for the given entity class at the
    current depth level only.

    :type entity_class: EntityClass
    :param entity_class: The entity class.
    :rtype: dict
    :return: The map of items.
    """

    return entity_class.get_items()


def get_all_parents(entity_class):
    """
    Retrieves all parent classes for the given entity class.

    :type entity_class: EntityClass
    :param entity_class: The entity class.
    :rtype: list
    :return: The list of parent classes.
    """

    return entity_class.get_all_parents()


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

    # retrieves all concrete descendants
    descendants = get_concrete_descendants(entity_class)

    # verifies that there are concrete classes to migrate
    if not descendants and getattr(entity_class, "abstract", False):
        messages.append("no concrete descendants found for migration")
        is_valid = False

    # verifies that the entity class has an id field
    table_id = entity_class.get_id()
    if table_id == None:
        messages.append("entity class has no id field defined")
        is_valid = False

    # verifies that all descendants use the same strategy
    for descendant in descendants:
        desc_strategy = descendant.get_inheritance_strategy()
        if not desc_strategy == current_strategy:
            messages.append(
                "descendant '%s' uses '%s' strategy, expected '%s'"
                % (descendant.__name__, desc_strategy, current_strategy)
            )
            is_valid = False

    if is_valid:
        messages.append("validation passed, hierarchy can be migrated")

    return is_valid, messages


def generate_cti_to_concrete_queries(entity_class, types_map=None):
    """
    Generates the SQL queries to migrate an entity hierarchy
    from class table inheritance to concrete table inheritance.

    This involves joining parent tables into flat tables, copying
    data, and rebuilding indexes.

    :type entity_class: EntityClass
    :param entity_class: The root entity class of the hierarchy.
    :type types_map: dict
    :param types_map: The SQL types map to use for column types.
    :rtype: list
    :return: The list of SQL queries to execute.
    """

    types_map = types_map or SQL_TYPES_MAP
    queries = []
    table_id = entity_class.get_id()
    table_id_value = getattr(entity_class, table_id)
    table_id_type = types_map.get(table_id_value.get("type", "integer"), "integer")

    # collects all concrete classes in the hierarchy including the
    # root entity class itself (if it's not abstract)
    concrete_classes = []
    if not getattr(entity_class, "abstract", False):
        concrete_classes.append(entity_class)
    concrete_classes.extend(get_concrete_descendants(entity_class))

    for concrete_class in concrete_classes:
        table_name = get_table_name(concrete_class)
        new_table_name = table_name + "_concrete"
        all_items = get_all_items(concrete_class)
        all_parents = get_all_parents(concrete_class)

        # builds the column definitions for the new flat table
        columns = []
        select_columns = []
        for item_name, item_value in all_items.items():
            if concrete_class.is_relation(item_name):
                if not concrete_class.is_mapped(item_name):
                    continue
                target_class = concrete_class.get_target(item_name)
                target_id = target_class.get_id()
                target_id_value = getattr(target_class, target_id)
                sql_type = types_map.get(
                    target_id_value.get("type", "integer"), "integer"
                )
            else:
                sql_type = types_map.get(item_value.get("type", "integer"), "integer")

            pk = " primary key" if item_value.get("id", False) else ""
            columns.append("%s %s%s" % (item_name, sql_type, pk))

            # determines which table this column comes from
            # for the data migration SELECT query
            source_table = table_name
            for parent in all_parents:
                if not getattr(parent, "abstract", False):
                    parent_items = get_items(parent)
                    if item_name in parent_items:
                        source_table = get_table_name(parent)
                        break
            select_columns.append("%s.%s" % (source_table, item_name))

        # adds the discriminator and mtime columns
        columns.append("_class text")
        columns.append("_mtime double precision")

        # creates the new flat table
        queries.append("create table %s(%s)" % (new_table_name, ", ".join(columns)))

        # builds the join query to copy data from the old tables
        join_parts = ["select %s" % ", ".join(select_columns)]
        join_parts.append(", %s._class" % get_table_name(entity_class))
        join_parts.append(", %s._mtime" % table_name)
        join_parts.append(" from %s" % table_name)

        for parent in all_parents:
            if getattr(parent, "abstract", False):
                continue
            parent_name = get_table_name(parent)
            join_parts.append(
                " inner join %s on %s.%s = %s.%s"
                % (parent_name, table_name, table_id, parent_name, table_id)
            )

        # filters by the discriminator to only get rows belonging
        # to this concrete class
        if concrete_class != entity_class:
            join_parts.append(
                " where %s._class = '%s'"
                % (get_table_name(entity_class), concrete_class.__name__)
            )

        insert_query = "insert into %s %s" % (
            new_table_name,
            "".join(join_parts),
        )
        queries.append(insert_query)

        # drops the old table and renames the new one
        queries.append("drop table %s" % table_name)
        queries.append("alter table %s rename to %s" % (new_table_name, table_name))

    # drops the parent tables that are no longer needed
    # (only if they are not used by other hierarchies)
    root_table_name = get_table_name(entity_class)
    for concrete_class in concrete_classes:
        if concrete_class == entity_class:
            continue
        for parent in get_all_parents(concrete_class):
            if getattr(parent, "abstract", False):
                continue
            parent_table = get_table_name(parent)
            if parent_table == root_table_name:
                continue
            queries.append("drop table if exists %s" % parent_table)

    # drops the root table if it has been handled
    if not getattr(entity_class, "abstract", False):
        # root table was already renamed above
        pass

    return queries


def generate_concrete_to_cti_queries(entity_class, types_map=None):
    """
    Generates the SQL queries to migrate an entity hierarchy
    from concrete table inheritance to class table inheritance.

    This involves splitting flat tables into per-class-level
    tables, distributing columns and data accordingly.

    :type entity_class: EntityClass
    :param entity_class: The root entity class of the hierarchy.
    :type types_map: dict
    :param types_map: The SQL types map to use for column types.
    :rtype: list
    :return: The list of SQL queries to execute.
    """

    types_map = types_map or SQL_TYPES_MAP
    queries = []
    table_id = entity_class.get_id()
    table_id_value = getattr(entity_class, table_id)
    table_id_type = types_map.get(table_id_value.get("type", "integer"), "integer")

    # collects all concrete classes in the hierarchy
    concrete_classes = []
    if not getattr(entity_class, "abstract", False):
        concrete_classes.append(entity_class)
    concrete_classes.extend(get_concrete_descendants(entity_class))

    # collects all unique class levels that need their own tables
    # in class table inheritance mode
    class_levels = []
    if not getattr(entity_class, "abstract", False):
        class_levels.append(entity_class)
    for concrete_class in concrete_classes:
        for parent in get_all_parents(concrete_class):
            if getattr(parent, "abstract", False):
                continue
            if parent not in class_levels:
                class_levels.append(parent)
        if concrete_class not in class_levels:
            class_levels.append(concrete_class)

    # creates the per-class-level tables
    for class_level in class_levels:
        level_table_name = get_table_name(class_level)
        level_items = get_items(class_level)
        new_table_name = level_table_name + "_cti"

        columns = []
        id_set = False
        for item_name, item_value in level_items.items():
            if class_level.is_relation(item_name):
                if not class_level.is_mapped(item_name):
                    continue
                target_class = class_level.get_target(item_name)
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
            columns.append("%s %s%s" % (item_name, sql_type, pk))

        # adds discriminator for the top-level class
        if not class_level.has_parents():
            columns.append("_class text")

        # adds mtime
        columns.append("_mtime double precision")

        # adds upper reference for child classes
        if not id_set:
            columns.append("%s %s primary key" % (table_id, table_id_type))

        queries.append("create table %s(%s)" % (new_table_name, ", ".join(columns)))

    # populates the per-class-level tables from the flat tables
    for concrete_class in concrete_classes:
        flat_table_name = get_table_name(concrete_class)

        for class_level in class_levels:
            level_table_name = get_table_name(class_level)
            new_table_name = level_table_name + "_cti"
            level_items = get_items(class_level)

            # checks if this class level is relevant to this concrete class
            all_parents = get_all_parents(concrete_class)
            if class_level != concrete_class and class_level not in all_parents:
                continue

            # builds the select columns for this class level
            select_cols = []
            for item_name in level_items:
                if class_level.is_relation(item_name):
                    if not class_level.is_mapped(item_name):
                        continue
                select_cols.append(item_name)

            # adds the id field if not already included
            if table_id not in select_cols:
                select_cols.append(table_id)

            # adds discriminator for top-level class
            if not class_level.has_parents():
                select_cols.append("_class")

            # adds mtime
            select_cols.append("_mtime")

            insert_query = "insert into %s(%s) select %s from %s" % (
                new_table_name,
                ", ".join(select_cols),
                ", ".join(select_cols),
                flat_table_name,
            )
            queries.append(insert_query)

    # drops the old flat tables and renames the new ones
    for concrete_class in concrete_classes:
        flat_table_name = get_table_name(concrete_class)
        queries.append("drop table %s" % flat_table_name)

    for class_level in class_levels:
        level_table_name = get_table_name(class_level)
        new_table_name = level_table_name + "_cti"
        queries.append(
            "alter table %s rename to %s" % (new_table_name, level_table_name)
        )

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
        queries = generate_cti_to_concrete_queries(entity_class, types_map)
    elif current_strategy == "concrete_table" and target_strategy == "class_table":
        queries = generate_concrete_to_cti_queries(entity_class, types_map)
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
