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


class MappingStrategy(object):
    """
    Base class for relationship mapping strategies.

    A mapping strategy determines how relationships between entities
    are stored in the database. This includes:
    - Which table owns the foreign key
    - How association tables are named
    - How foreign key columns are named

    Subclasses should implement the get_mapper() method to define
    custom mapping logic.
    """

    def get_mapper(self, cls, relation_name, get_mapper_name=False):
        """
        Determines which class owns the foreign key for a relation.

        :type cls: Class
        :param cls: The entity class containing the relation.
        :type relation_name: String
        :param relation_name: The name of the relation attribute.
        :type get_mapper_name: bool
        :param get_mapper_name: If True, returns (mapper_class, mapper_relation_name) tuple.
        :rtype: Class or tuple
        :return: The class that owns the foreign key, or tuple if get_mapper_name=True.
        """
        raise NotImplementedError("Subclasses must implement get_mapper()")

    def get_foreign_key_column(self, cls, relation_name):
        """
        Determines the foreign key column name for a relation.

        :type cls: Class
        :param cls: The entity class containing the relation.
        :type relation_name: String
        :param relation_name: The name of the relation attribute.
        :rtype: String
        :return: The foreign key column name.
        """
        # Default behavior: relation_name + "_id"
        return "%s_id" % relation_name

    def get_association_table_name(self, cls1, relation_name1, cls2, relation_name2):
        """
        Determines the association table name for many-to-many relations.

        :type cls1: Class
        :param cls1: The first entity class.
        :type relation_name1: String
        :param relation_name1: The relation name in the first class.
        :type cls2: Class
        :param cls2: The second entity class.
        :type relation_name2: String
        :param relation_name2: The relation name in the second class.
        :rtype: String
        :return: The association table name.
        """
        # Default behavior: sorted names with underscore prefix
        table1 = cls1.get_name()
        table2 = cls2.get_name()
        names = [table1, table2]
        names.sort()
        return "_%s_%s" % tuple(names)


class DefaultMappingStrategy(MappingStrategy):
    """
    Default mapping strategy that preserves the original Colony behavior.

    Uses the is_mapper flag and mapped_by attribute to determine
    relationship ownership. This is the strategy used in the original
    implementation.

    Rules:
    1. Check mapped_by attribute in relation definition
    2. Check is_mapper=True flag in relation definition
    3. If neither exists, relation is indirect (many-to-many)
    """

    def get_mapper(self, cls, relation_name, get_mapper_name=False):
        """
        Implements the original Colony mapping logic using is_mapper flags.

        This method replicates the logic from structures.py:2652
        """
        # Initialize mapper_name as None
        mapper_name = None

        # Get relation attributes and reverse relation name
        relation = cls.get_relation(relation_name)
        reverse = cls.get_reverse(relation_name)

        # Get target class and target relation
        target_class = cls.get_target(relation_name)
        target_relation = target_class.get_relation(reverse)

        # Try to retrieve mapper from both target and current class
        target_mapper = target_relation.get("mapped_by", None)
        mapper = relation.get("mapped_by", target_mapper)

        # If mapper was found, determine the mapper name
        if mapper:
            mapper_name = relation_name if mapper == cls else reverse

        # Check target relation for is_mapper attribute
        target_is_mapper = target_relation.get("is_mapper", False)
        mapper = target_class if target_is_mapper else mapper
        mapper_name = reverse if target_is_mapper else mapper_name

        # Check current relation for is_mapper attribute
        is_mapper = relation.get("is_mapper", False)
        mapper = cls if is_mapper else mapper
        mapper_name = relation_name if is_mapper else mapper_name

        # Create return value based on get_mapper_name flag
        return_value = (mapper, mapper_name) if get_mapper_name else mapper
        return return_value


class ConventionOverConfigurationStrategy(MappingStrategy):
    """
    Convention-based mapping strategy inspired by Rails/Django ORMs.

    Uses naming conventions to infer relationship ownership:
    - to-one relations: current class owns the foreign key
    - to-many relations: target class owns the foreign key (via reverse to-one)
    - Explicit many-to-many: creates association table

    This eliminates the need for is_mapper flags in most cases.
    """

    def get_mapper(self, cls, relation_name, get_mapper_name=False):
        """
        Uses conventions to determine relationship ownership.
        """
        relation = cls.get_relation(relation_name)
        relation_type = relation.get("type")
        reverse = cls.get_reverse(relation_name)

        # Convention: to-one relations are always mapped on this side
        if relation_type == "to-one":
            mapper = cls
            mapper_name = relation_name
            return (mapper, mapper_name) if get_mapper_name else mapper

        # For to-many, check if there's a reverse to-one
        target_class = cls.get_target(relation_name)
        target_relation = target_class.get_relation(reverse)
        target_type = target_relation.get("type") if target_relation else None

        # If reverse is to-one, it owns the mapping
        if target_type == "to-one":
            mapper = target_class
            mapper_name = reverse
            return (mapper, mapper_name) if get_mapper_name else mapper

        # Otherwise, it's many-to-many (no mapper)
        mapper = None
        mapper_name = None
        return (mapper, mapper_name) if get_mapper_name else mapper


class AnnotationBasedStrategy(MappingStrategy):
    """
    JPA/Hibernate-style annotation-based mapping strategy.

    Requires explicit annotations in relation definitions:
    - join_column: specifies the foreign key column
    - inverse_join_column: for many-to-many relations
    - join_table: explicit association table configuration

    This provides maximum control but requires more verbose definitions.
    """

    def get_mapper(self, cls, relation_name, get_mapper_name=False):
        """
        Uses explicit annotations to determine relationship ownership.
        """
        relation = cls.get_relation(relation_name)
        reverse = cls.get_reverse(relation_name)
        target_class = cls.get_target(relation_name)

        # Check for explicit join_column annotation
        if "join_column" in relation:
            mapper = cls
            mapper_name = relation_name
            return (mapper, mapper_name) if get_mapper_name else mapper

        # Check for join_table annotation (many-to-many)
        if "join_table" in relation:
            mapper = None
            mapper_name = None
            return (mapper, mapper_name) if get_mapper_name else mapper

        # Check target for join_column
        target_relation = target_class.get_relation(reverse)
        if target_relation and "join_column" in target_relation:
            mapper = target_class
            mapper_name = reverse
            return (mapper, mapper_name) if get_mapper_name else mapper

        # Default to convention-based logic
        relation_type = relation.get("type")
        if relation_type == "to-one":
            mapper = cls
            mapper_name = relation_name
        else:
            mapper = None
            mapper_name = None

        return (mapper, mapper_name) if get_mapper_name else mapper

    def get_foreign_key_column(self, cls, relation_name):
        """
        Uses join_column annotation or falls back to default naming.
        """
        relation = cls.get_relation(relation_name)
        join_column = relation.get("join_column")

        if join_column:
            # Can be a string or a dict with 'name' key
            if isinstance(join_column, dict):
                return join_column.get("name", "%s_id" % relation_name)
            return join_column

        return super(AnnotationBasedStrategy, self).get_foreign_key_column(
            cls, relation_name
        )

    def get_association_table_name(self, cls1, relation_name1, cls2, relation_name2):
        """
        Uses join_table annotation or falls back to default naming.
        """
        relation1 = cls1.get_relation(relation_name1)
        join_table = relation1.get("join_table")

        if join_table:
            if isinstance(join_table, dict):
                return join_table.get("name")
            return join_table

        return super(AnnotationBasedStrategy, self).get_association_table_name(
            cls1, relation_name1, cls2, relation_name2
        )


# Default strategy instance
DEFAULT_STRATEGY = DefaultMappingStrategy()
