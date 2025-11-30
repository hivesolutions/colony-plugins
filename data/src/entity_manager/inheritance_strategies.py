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


class InheritanceStrategy(object):
    """
    Base class for entity inheritance mapping strategies.

    Different strategies determine how class hierarchies are mapped
    to database tables. Common strategies include:
    - Single Table Inheritance: All classes in hierarchy share one table
    - Joined Table Inheritance: Each class gets its own table (current Colony default)
    - Table Per Class: Each concrete class gets a table with all fields
    """

    def get_strategy_name(self):
        """
        Returns the name of this strategy.

        :rtype: String
        :return: Strategy name
        """
        raise NotImplementedError()

    def should_create_table(self, entity_class):
        """
        Determines if a table should be created for the given entity class.

        :type entity_class: Class
        :param entity_class: The entity class to check
        :rtype: bool
        :return: True if a table should be created
        """
        raise NotImplementedError()

    def get_discriminator_column(self, entity_class):
        """
        Returns the discriminator column name for polymorphic queries.

        :type entity_class: Class
        :param entity_class: The entity class
        :rtype: String or None
        :return: Discriminator column name or None
        """
        return None

    def get_discriminator_value(self, entity_class):
        """
        Returns the discriminator value for this entity class.

        :type entity_class: Class
        :param entity_class: The entity class
        :rtype: String or None
        :return: Discriminator value or None
        """
        return None

    def get_fields_for_table(self, entity_class):
        """
        Returns the fields that should be stored in this class's table.

        :type entity_class: Class
        :param entity_class: The entity class
        :rtype: dict
        :return: Dictionary of field_name -> field_definition
        """
        raise NotImplementedError()

    def requires_joins(self, entity_class):
        """
        Determines if queries need to join parent tables.

        :type entity_class: Class
        :param entity_class: The entity class
        :rtype: bool
        :return: True if joins are needed
        """
        raise NotImplementedError()


class JoinedTableStrategy(InheritanceStrategy):
    """
    Joined Table Inheritance (aka Class Table Inheritance).

    Each class in the hierarchy gets its own table containing only
    the fields defined in that class. Subclass tables have a foreign
    key to the parent table.

    This is the current default behavior in Colony.

    Pros:
    - Normalized schema
    - Easy to add new subclasses
    - No null columns for unused fields

    Cons:
    - Queries require joins
    - Slower performance for deep hierarchies
    """

    def get_strategy_name(self):
        return "joined"

    def should_create_table(self, entity_class):
        """
        Creates a table for every non-abstract class.
        """
        # Check if class is abstract
        return not getattr(entity_class, "abstract", False)

    def get_fields_for_table(self, entity_class):
        """
        Returns only the fields defined directly on this class,
        not inherited fields.
        """
        # Get all fields from this class
        all_fields = entity_class.get_items_map()

        # Get fields from all parent classes
        parent_fields = set()
        for base in entity_class.__bases__:
            if hasattr(base, "get_items_map"):
                parent_fields.update(base.get_items_map().keys())

        # Return only fields defined on this specific class
        this_class_fields = {}
        for name, definition in all_fields.items():
            if name not in parent_fields:
                this_class_fields[name] = definition

        return this_class_fields

    def requires_joins(self, entity_class):
        """
        Joined table strategy always requires joins for subclasses.
        """
        # Check if there are any parent entity classes
        for base in entity_class.__bases__:
            if hasattr(base, "get_items_map") and not getattr(base, "abstract", False):
                return True
        return False


class SingleTableStrategy(InheritanceStrategy):
    """
    Single Table Inheritance.

    All classes in the hierarchy share a single table. A discriminator
    column identifies the concrete class for each row.

    Usage:
        class Animal(EntityClass):
            __inheritance_strategy__ = "single_table"
            __discriminator_column__ = "animal_type"
            __discriminator_value__ = "animal"

        class Dog(Animal):
            __discriminator_value__ = "dog"

    Pros:
    - No joins needed
    - Fast queries
    - Simple schema

    Cons:
    - Many null columns
    - All fields must be nullable
    - Single table can become very wide
    """

    def get_strategy_name(self):
        return "single_table"

    def should_create_table(self, entity_class):
        """
        Only creates a table for the root class in the hierarchy.
        """
        # Check if this is the root class (defines the strategy)
        if hasattr(entity_class, "__inheritance_strategy__"):
            return True

        # Check if any parent already created the table
        for base in entity_class.__bases__:
            if hasattr(base, "__inheritance_strategy__"):
                return False

        return True

    def get_discriminator_column(self, entity_class):
        """
        Returns the discriminator column name from the root class.
        """
        # Check this class first
        if hasattr(entity_class, "__discriminator_column__"):
            return entity_class.__discriminator_column__

        # Check parent classes
        for base in entity_class.__bases__:
            if hasattr(base, "get_discriminator_column"):
                col = self.get_discriminator_column(base)
                if col:
                    return col

        return "entity_type"  # Default discriminator column name

    def get_discriminator_value(self, entity_class):
        """
        Returns the discriminator value for this class.
        """
        if hasattr(entity_class, "__discriminator_value__"):
            return entity_class.__discriminator_value__

        # Default to class name
        return entity_class.__name__

    def get_fields_for_table(self, entity_class):
        """
        Returns ALL fields from the entire hierarchy, since they
        all go in the same table.
        """
        # Find the root class
        root_class = self._find_root_class(entity_class)

        # Get all fields from the root class and all subclasses
        all_fields = {}

        # Start with root class fields
        all_fields.update(root_class.get_items_map())

        # Add discriminator column if not already present
        discriminator_col = self.get_discriminator_column(entity_class)
        if discriminator_col not in all_fields:
            all_fields[discriminator_col] = {"type": "text", "indexed": True}

        # Note: In a real implementation, we'd need to scan all
        # subclasses to get their fields too. For now, we just
        # get fields from the current class hierarchy.
        for base in entity_class.__mro__:
            if hasattr(base, "get_items_map") and base != entity_class:
                all_fields.update(base.get_items_map())

        return all_fields

    def requires_joins(self, entity_class):
        """
        Single table inheritance never requires joins.
        """
        return False

    def _find_root_class(self, entity_class):
        """
        Finds the root class in the inheritance hierarchy
        (the one that defines __inheritance_strategy__).
        """
        if hasattr(entity_class, "__inheritance_strategy__"):
            # Check if any parent also has it (go deeper)
            for base in entity_class.__bases__:
                if hasattr(base, "__inheritance_strategy__"):
                    return self._find_root_class(base)
            return entity_class

        # Check parents
        for base in entity_class.__bases__:
            if hasattr(base, "__inheritance_strategy__"):
                return self._find_root_class(base)

        return entity_class


class TablePerClassStrategy(InheritanceStrategy):
    """
    Table Per Concrete Class Inheritance.

    Each concrete (non-abstract) class gets its own table containing
    ALL fields (including inherited ones). No foreign keys between tables.

    Pros:
    - No joins needed
    - Each table is self-contained
    - Good performance for queries on single class

    Cons:
    - Duplicate column definitions
    - Polymorphic queries are difficult
    - Schema changes must be applied to all tables
    """

    def get_strategy_name(self):
        return "table_per_class"

    def should_create_table(self, entity_class):
        """
        Creates a table for every non-abstract class.
        """
        return not getattr(entity_class, "abstract", False)

    def get_fields_for_table(self, entity_class):
        """
        Returns ALL fields including inherited ones.
        """
        # Get complete items map including inherited fields
        return entity_class.get_items_map()

    def requires_joins(self, entity_class):
        """
        Table per class never requires joins.
        """
        return False


def get_inheritance_strategy(entity_class):
    """
    Factory function to get the appropriate inheritance strategy
    for an entity class.

    Checks for __inheritance_strategy__ attribute on the class
    or its parents. Defaults to JoinedTableStrategy.

    :type entity_class: Class
    :param entity_class: The entity class
    :rtype: InheritanceStrategy
    :return: The inheritance strategy instance
    """
    # Check for explicit strategy attribute
    strategy_name = None

    if hasattr(entity_class, "__inheritance_strategy__"):
        strategy_name = entity_class.__inheritance_strategy__
    else:
        # Check parent classes
        for base in entity_class.__mro__:
            if hasattr(base, "__inheritance_strategy__"):
                strategy_name = base.__inheritance_strategy__
                break

    # Map strategy names to classes
    strategies = {
        "single_table": SingleTableStrategy,
        "joined": JoinedTableStrategy,
        "table_per_class": TablePerClassStrategy,
    }

    # Default to joined table (current Colony behavior)
    if not strategy_name or strategy_name not in strategies:
        return JoinedTableStrategy()

    return strategies[strategy_name]()
