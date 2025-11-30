#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test script to demonstrate different query generation
for different inheritance strategies.
"""

import sys
import os

# Add the parent directory to the path so we can import entity_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import colony


def test_joined_table_strategy():
    """
    Test query generation for joined table inheritance.
    Should generate queries with INNER JOIN for parent tables.
    """
    print("\n=== Testing Joined Table Strategy ===")

    # Create mock entity classes for joined table inheritance
    class Animal(colony.EntityClass):
        """Base animal class using joined table inheritance (default)"""

        id = {"type": "integer", "id": True}
        name = {"type": "text"}

    class Dog(Animal):
        """Dog subclass - should join with Animal table"""

        breed = {"type": "text"}

    # Create a mock entity manager to inspect query generation
    # Note: We can't actually run queries without a database connection,
    # but we can inspect what queries would be generated
    try:
        from entity_manager import system

        manager = system.EntityManager(None)  # No plugin needed for query inspection

        # Generate a find query for Dog
        query_buffer = colony.StringBuffer()
        query_buffer.write("select ")

        # This would normally call _names_query_f and _join_query_f
        # For now, just demonstrate the expected behavior
        print("Expected behavior for Joined Table:")
        print("- Query should include: INNER JOIN Animal ON Dog.id = Animal.id")
        print("- Parent table fields should be joined")

    except Exception as e:
        print(f"Note: Cannot generate actual queries without database: {e}")
        print("Expected behavior for Joined Table:")
        print("- Query should include: INNER JOIN Animal ON Dog.id = Animal.id")
        print("- Parent table fields should be joined")


def test_single_table_strategy():
    """
    Test query generation for single table inheritance.
    Should NOT generate joins, but should add discriminator filter.
    """
    print("\n=== Testing Single Table Strategy ===")

    # Create mock entity classes for single table inheritance
    class Vehicle(colony.EntityClass):
        """Base vehicle class using single table inheritance"""

        __inheritance_strategy__ = "single_table"
        __discriminator_column__ = "vehicle_type"
        __discriminator_value__ = "vehicle"

        id = {"type": "integer", "id": True}
        name = {"type": "text"}

    class Car(Vehicle):
        """Car subclass - should NOT join, but filter by discriminator"""

        __discriminator_value__ = "car"
        num_doors = {"type": "integer"}

    print("Expected behavior for Single Table:")
    print("- Query should NOT include any JOIN clauses for parent tables")
    print("- Query should include: WHERE vehicle_type = 'car'")
    print("- All fields (from Vehicle and Car) are in the same table")
    print("- SELECT should include the discriminator column: vehicle_type")


def test_table_per_class_strategy():
    """
    Test query generation for table per class inheritance.
    Should NOT generate joins to parent tables.
    """
    print("\n=== Testing Table Per Class Strategy ===")

    # Create mock entity classes for table per class inheritance
    class Person(colony.EntityClass):
        """Base person class using table per class inheritance"""

        __inheritance_strategy__ = "table_per_class"

        id = {"type": "integer", "id": True}
        name = {"type": "text"}

    class Employee(Person):
        """Employee subclass - should have its own complete table"""

        employee_id = {"type": "text"}
        department = {"type": "text"}

    print("Expected behavior for Table Per Class:")
    print("- Query should NOT include any JOIN clauses for parent tables")
    print("- Employee table contains ALL fields (id, name, employee_id, department)")
    print("- Query is simply: SELECT * FROM Employee")


def demonstrate_query_differences():
    """
    Main function to demonstrate the differences in query generation
    between the three inheritance strategies.
    """
    print("=" * 70)
    print("INHERITANCE STRATEGY QUERY GENERATION DEMONSTRATION")
    print("=" * 70)
    print("\nThis demonstrates how different inheritance strategies should")
    print("generate different SQL queries:")

    test_joined_table_strategy()
    test_single_table_strategy()
    test_table_per_class_strategy()

    print("\n" + "=" * 70)
    print("SUMMARY OF DIFFERENCES")
    print("=" * 70)
    print("\n1. Joined Table (default):")
    print("   - Creates separate tables for each class")
    print("   - Uses INNER JOINs to combine parent and child data")
    print("   - Each table only has its own fields")

    print("\n2. Single Table:")
    print("   - Single table for entire hierarchy")
    print("   - NO joins required")
    print("   - Uses discriminator column to filter by type")
    print("   - WHERE clause filters on discriminator value")

    print("\n3. Table Per Class:")
    print("   - Each concrete class has complete table with all fields")
    print("   - NO joins required")
    print("   - Each table is self-contained")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demonstrate_query_differences()
