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
import sqlite3
import argparse

# adds the entity manager plugin source directory to the path so
# that the migration logic may be imported as a "normal" module
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
""" The base path of the repository, used as the reference
for the resolution of the plugin source directories """

sys.path.insert(0, os.path.join(BASE_PATH, "data", "src"))

from entity_manager import migration


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
        success, messages = migration.migrate(
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
