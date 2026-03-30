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

ITERATIONS = 1000
""" The number of iterations to use for bulk operations,
higher values produce more stable results """

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
""" The default SQL types map for column type resolution """


def create_cti_schema(connection):
    """
    Creates the class table inheritance schema with three
    levels: root_entity -> person -> employee. Each class
    stores only its own columns, child tables reference the
    parent via the object_id foreign key.
    """

    cursor = connection.cursor()

    cursor.execute(
        "create table _root_entity("
        "object_id integer primary key, "
        "status integer, "
        "_class text, "
        "_mtime double precision)"
    )

    cursor.execute(
        "create table _person("
        "name text, "
        "age integer, "
        "weight double precision, "
        "_mtime double precision, "
        "object_id integer primary key)"
    )

    cursor.execute(
        "create table _employee("
        "salary integer, "
        "_mtime double precision, "
        "object_id integer primary key)"
    )

    connection.commit()
    cursor.close()


def create_concrete_schema(connection):
    """
    Creates the concrete table inheritance schema with three
    levels. Each concrete class stores all columns (own +
    inherited) in a single flat table.
    """

    cursor = connection.cursor()

    cursor.execute(
        "create table _concrete_root_entity("
        "object_id integer primary key, "
        "status integer, "
        "_class text, "
        "_mtime double precision)"
    )

    cursor.execute(
        "create table _concrete_person("
        "object_id integer primary key, "
        "status integer, "
        "name text, "
        "age integer, "
        "weight double precision, "
        "_class text, "
        "_mtime double precision)"
    )

    cursor.execute(
        "create table _concrete_employee("
        "object_id integer primary key, "
        "status integer, "
        "name text, "
        "age integer, "
        "weight double precision, "
        "salary integer, "
        "_class text, "
        "_mtime double precision)"
    )

    connection.commit()
    cursor.close()


def insert_cti(connection, object_id, name, age, salary):
    """
    Inserts a single employee row across the three CTI tables,
    simulating the entity manager's multi-table insert behavior.
    """

    mtime = time.time()
    cursor = connection.cursor()
    cursor.execute(
        "insert into _root_entity(object_id, status, _class, _mtime) "
        "values(?, 1, 'Employee', ?)",
        (object_id, mtime),
    )
    cursor.execute(
        "insert into _person(object_id, name, age, weight, _mtime) "
        "values(?, ?, ?, 70.5, ?)",
        (object_id, name, age, mtime),
    )
    cursor.execute(
        "insert into _employee(object_id, salary, _mtime) " "values(?, ?, ?)",
        (object_id, salary, mtime),
    )
    cursor.close()


def insert_concrete(connection, object_id, name, age, salary):
    """
    Inserts a single employee row into the concrete flat table,
    simulating the entity manager's single-table insert behavior.
    """

    mtime = time.time()
    cursor = connection.cursor()
    cursor.execute(
        "insert into _concrete_employee("
        "object_id, status, name, age, weight, salary, _class, _mtime"
        ") values(?, 1, ?, ?, 70.5, ?, 'ConcreteEmployee', ?)",
        (object_id, name, age, salary, mtime),
    )
    cursor.close()


def select_by_id_cti(connection, object_id):
    """
    Retrieves a single employee by ID using the CTI three-table
    join, simulating the entity manager's joined select behavior.
    """

    cursor = connection.cursor()
    cursor.execute(
        "select _employee.object_id, _root_entity.status, "
        "_person.name, _person.age, _person.weight, "
        "_employee.salary, _root_entity._class, _employee._mtime "
        "from _employee "
        "inner join _person on _employee.object_id = _person.object_id "
        "inner join _root_entity on _employee.object_id = _root_entity.object_id "
        "where _employee.object_id = ?",
        (object_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    return row


def select_by_id_concrete(connection, object_id):
    """
    Retrieves a single employee by ID from the concrete flat
    table, simulating the entity manager's single-table select.
    """

    cursor = connection.cursor()
    cursor.execute(
        "select object_id, status, name, age, weight, salary, "
        "_class, _mtime "
        "from _concrete_employee "
        "where object_id = ?",
        (object_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    return row


def select_all_cti(connection):
    """
    Retrieves all employees using the CTI three-table join.
    """

    cursor = connection.cursor()
    cursor.execute(
        "select _employee.object_id, _root_entity.status, "
        "_person.name, _person.age, _person.weight, "
        "_employee.salary, _root_entity._class, _employee._mtime "
        "from _employee "
        "inner join _person on _employee.object_id = _person.object_id "
        "inner join _root_entity on _employee.object_id = _root_entity.object_id"
    )
    rows = cursor.fetchall()
    cursor.close()
    return rows


def select_all_concrete(connection):
    """
    Retrieves all employees from the concrete flat table.
    """

    cursor = connection.cursor()
    cursor.execute(
        "select object_id, status, name, age, weight, salary, "
        "_class, _mtime "
        "from _concrete_employee"
    )
    rows = cursor.fetchall()
    cursor.close()
    return rows


def update_cti(connection, object_id, name, salary):
    """
    Updates an employee across the CTI tables, simulating the
    entity manager's multi-table update behavior.
    """

    mtime = time.time()
    cursor = connection.cursor()
    cursor.execute(
        "update _root_entity set _mtime = ? where object_id = ?",
        (mtime, object_id),
    )
    cursor.execute(
        "update _person set name = ?, _mtime = ? where object_id = ?",
        (name, mtime, object_id),
    )
    cursor.execute(
        "update _employee set salary = ?, _mtime = ? where object_id = ?",
        (salary, mtime, object_id),
    )
    cursor.close()


def update_concrete(connection, object_id, name, salary):
    """
    Updates an employee in the concrete flat table, simulating
    the entity manager's single-table update behavior.
    """

    mtime = time.time()
    cursor = connection.cursor()
    cursor.execute(
        "update _concrete_employee set name = ?, salary = ?, "
        "_mtime = ? where object_id = ?",
        (name, salary, mtime, object_id),
    )
    cursor.close()


def delete_cti(connection, object_id):
    """
    Deletes an employee across the CTI tables, simulating the
    entity manager's multi-table delete behavior.
    """

    cursor = connection.cursor()
    cursor.execute("delete from _employee where object_id = ?", (object_id,))
    cursor.execute("delete from _person where object_id = ?", (object_id,))
    cursor.execute("delete from _root_entity where object_id = ?", (object_id,))
    cursor.close()


def delete_concrete(connection, object_id):
    """
    Deletes an employee from the concrete flat table, simulating
    the entity manager's single-table delete behavior.
    """

    cursor = connection.cursor()
    cursor.execute("delete from _concrete_employee where object_id = ?", (object_id,))
    cursor.close()


def count_cti(connection):
    """
    Counts all employees using the CTI join.
    """

    cursor = connection.cursor()
    cursor.execute(
        "select count(*) from _employee "
        "inner join _person on _employee.object_id = _person.object_id "
        "inner join _root_entity on _employee.object_id = _root_entity.object_id"
    )
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def count_concrete(connection):
    """
    Counts all employees from the concrete flat table.
    """

    cursor = connection.cursor()
    cursor.execute("select count(*) from _concrete_employee")
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def benchmark(label, func, *args):
    """
    Runs the given function with timing and returns the elapsed
    time in milliseconds.

    :type label: String
    :param label: A descriptive label for the benchmark.
    :type func: Function
    :param func: The function to benchmark.
    :rtype: float
    :return: The elapsed time in milliseconds.
    """

    start = time.time()
    result = func(*args)
    elapsed = (time.time() - start) * 1000.0
    return elapsed, result


def run_benchmarks(iterations=None):
    """
    Runs the complete set of benchmarks comparing class table
    inheritance and concrete table inheritance strategies.

    :type iterations: int
    :param iterations: The number of iterations for bulk operations.
    :rtype: list
    :return: A list of result tuples (operation, cti_ms, concrete_ms, speedup).
    """

    iterations = iterations or ITERATIONS
    results = []

    # creates the temporary database files for each strategy
    cti_fd, cti_path = tempfile.mkstemp(suffix=".db")
    concrete_fd, concrete_path = tempfile.mkstemp(suffix=".db")
    os.close(cti_fd)
    os.close(concrete_fd)

    try:
        cti_conn = sqlite3.connect(cti_path)
        concrete_conn = sqlite3.connect(concrete_path)

        # benchmarks the schema creation
        cti_ms, _ = benchmark("create_schema", create_cti_schema, cti_conn)
        concrete_ms, _ = benchmark(
            "create_schema", create_concrete_schema, concrete_conn
        )
        results.append(("Schema Creation", cti_ms, concrete_ms))

        # benchmarks the bulk insert operation
        def bulk_insert_cti():
            for i in range(1, iterations + 1):
                insert_cti(cti_conn, i, "person_%d" % i, 20 + (i % 50), 1000 + i)
            cti_conn.commit()

        def bulk_insert_concrete():
            for i in range(1, iterations + 1):
                insert_concrete(
                    concrete_conn, i, "person_%d" % i, 20 + (i % 50), 1000 + i
                )
            concrete_conn.commit()

        cti_ms, _ = benchmark("bulk_insert", bulk_insert_cti)
        concrete_ms, _ = benchmark("bulk_insert", bulk_insert_concrete)
        results.append(("Bulk INSERT (%d rows)" % iterations, cti_ms, concrete_ms))

        # benchmarks the single select by ID (warm cache, middle of range)
        target_id = iterations // 2

        def repeat_select_cti():
            for _i in range(iterations):
                select_by_id_cti(cti_conn, target_id)

        def repeat_select_concrete():
            for _i in range(iterations):
                select_by_id_concrete(concrete_conn, target_id)

        cti_ms, _ = benchmark("select_by_id", repeat_select_cti)
        concrete_ms, _ = benchmark("select_by_id", repeat_select_concrete)
        results.append(("SELECT by ID (%d lookups)" % iterations, cti_ms, concrete_ms))

        # benchmarks the find all (full table scan)
        def repeat_find_all_cti():
            for _i in range(100):
                select_all_cti(cti_conn)

        def repeat_find_all_concrete():
            for _i in range(100):
                select_all_concrete(concrete_conn)

        cti_ms, _ = benchmark("find_all", repeat_find_all_cti)
        concrete_ms, _ = benchmark("find_all", repeat_find_all_concrete)
        results.append(("SELECT all (100 scans)", cti_ms, concrete_ms))

        # benchmarks the count operation
        def repeat_count_cti():
            for _i in range(iterations):
                count_cti(cti_conn)

        def repeat_count_concrete():
            for _i in range(iterations):
                count_concrete(concrete_conn)

        cti_ms, _ = benchmark("count", repeat_count_cti)
        concrete_ms, _ = benchmark("count", repeat_count_concrete)
        results.append(("COUNT (%d counts)" % iterations, cti_ms, concrete_ms))

        # benchmarks the bulk update operation
        def bulk_update_cti():
            for i in range(1, iterations + 1):
                update_cti(cti_conn, i, "updated_%d" % i, 2000 + i)
            cti_conn.commit()

        def bulk_update_concrete():
            for i in range(1, iterations + 1):
                update_concrete(concrete_conn, i, "updated_%d" % i, 2000 + i)
            concrete_conn.commit()

        cti_ms, _ = benchmark("bulk_update", bulk_update_cti)
        concrete_ms, _ = benchmark("bulk_update", bulk_update_concrete)
        results.append(("Bulk UPDATE (%d rows)" % iterations, cti_ms, concrete_ms))

        # benchmarks the bulk delete operation
        def bulk_delete_cti():
            for i in range(1, iterations + 1):
                delete_cti(cti_conn, i)
            cti_conn.commit()

        def bulk_delete_concrete():
            for i in range(1, iterations + 1):
                delete_concrete(concrete_conn, i)
            concrete_conn.commit()

        cti_ms, _ = benchmark("bulk_delete", bulk_delete_cti)
        concrete_ms, _ = benchmark("bulk_delete", bulk_delete_concrete)
        results.append(("Bulk DELETE (%d rows)" % iterations, cti_ms, concrete_ms))

        # closes the connections
        cti_conn.close()
        concrete_conn.close()

    finally:
        # removes the temporary database files
        if os.path.exists(cti_path):
            os.remove(cti_path)
        if os.path.exists(concrete_path):
            os.remove(concrete_path)

    return results


def print_report(results, iterations=None):
    """
    Prints a formatted benchmark report comparing the two
    inheritance strategies.

    :type results: list
    :param results: The list of result tuples from run_benchmarks.
    :type iterations: int
    :param iterations: The number of iterations used.
    """

    iterations = iterations or ITERATIONS

    print("")
    print("=" * 78)
    print("  Inheritance Strategy Benchmark Report")
    print(
        "  SQLite | %d iterations | 3-level hierarchy (root -> person -> employee)"
        % iterations
    )
    print("=" * 78)
    print("")
    print(
        "  %-35s %12s %12s %10s" % ("Operation", "Class Table", "Concrete", "Speedup")
    )
    print("  " + "-" * 73)

    for operation, cti_ms, concrete_ms in results:
        if cti_ms > 0:
            speedup = cti_ms / concrete_ms if concrete_ms > 0 else float("inf")
        else:
            speedup = 1.0

        # formats the speedup indicator, values above 1.0 mean
        # concrete table is faster, below 1.0 means CTI is faster
        if speedup >= 1.05:
            indicator = "%.2fx faster" % speedup
        elif speedup <= 0.95:
            indicator = "%.2fx slower" % (1.0 / speedup)
        else:
            indicator = "~same"

        print(
            "  %-35s %10.2f ms %10.2f ms %10s"
            % (operation, cti_ms, concrete_ms, indicator)
        )

    print("")
    print("  " + "-" * 73)
    print("  Speedup > 1.0x means Concrete Table is faster than Class Table")
    print("=" * 78)
    print("")


def main():
    """
    Main entry point for the benchmark script, runs the benchmarks
    and prints the report.
    """

    iterations = ITERATIONS
    if len(sys.argv) > 1:
        try:
            iterations = int(sys.argv[1])
        except ValueError:
            print("usage: %s [iterations]" % sys.argv[0])
            sys.exit(1)

    print("Running benchmarks with %d iterations..." % iterations)
    results = run_benchmarks(iterations)
    print_report(results, iterations)


if __name__ == "__main__":
    main()
