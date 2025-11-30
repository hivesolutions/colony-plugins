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


class QueryBuilder(object):
    """
    Fluent query builder API for constructing entity queries.

    Provides a chainable interface for building queries instead of
    nested dictionaries:

    Usage:
        # Old way:
        entity_manager.find(Person, {
            "filters": {"age": {"$gt": 18}, "name": {"$like": "John%"}},
            "order_by": [("name", "asc")],
            "start_record": 0,
            "number_records": 10
        })

        # New way:
        entity_manager.query(Person)
            .filter(age__gt=18)
            .filter(name__like="John%")
            .order_by("name")
            .limit(10)
            .all()
    """

    def __init__(self, entity_manager, entity_class):
        """
        Constructor for query builder.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to execute queries
        :type entity_class: Class
        :param entity_class: The entity class to query
        """
        self._entity_manager = entity_manager
        self._entity_class = entity_class
        self._filters = {}
        self._order_by = []
        self._start_record = None
        self._number_records = None
        self._eager_relations = {}
        self._lock = False
        self._fields = None

    def filter(self, **kwargs):
        """
        Adds filter conditions to the query.

        Supports Django-style lookups with double underscore:
        - field__gt: greater than
        - field__gte: greater than or equal
        - field__lt: less than
        - field__lte: less than or equal
        - field__like: SQL LIKE
        - field__in: IN clause
        - field: exact match

        Usage:
            .filter(age__gt=18, name="John")
            .filter(status__in=[1, 2, 3])

        :rtype: QueryBuilder
        :return: self for chaining
        """
        for key, value in kwargs.items():
            # Parse field__operator syntax
            if "__" in key:
                field, operator = key.rsplit("__", 1)
                self._add_filter(field, operator, value)
            else:
                # Exact match
                self._add_filter(key, "eq", value)

        return self

    def _add_filter(self, field, operator, value):
        """
        Internal method to add a filter condition.

        :type field: String
        :param field: The field name
        :type operator: String
        :param operator: The operator (gt, lt, like, etc.)
        :type value: object
        :param value: The value to compare
        """
        # Map operator to Colony filter syntax
        operator_map = {
            "eq": None,  # Direct value
            "gt": "$gt",
            "gte": "$gte",
            "lt": "$lt",
            "lte": "$lte",
            "like": "$like",
            "in": "$in",
            "ne": "$ne",
            "not": "$not",
        }

        colony_op = operator_map.get(operator)

        if colony_op is None:
            # Direct value (exact match)
            self._filters[field] = value
        else:
            # Operator-based filter
            if field not in self._filters:
                self._filters[field] = {}
            elif not isinstance(self._filters[field], dict):
                # Convert to dict if it was a direct value
                old_value = self._filters[field]
                self._filters[field] = {"$eq": old_value}

            self._filters[field][colony_op] = value

    def order_by(self, *fields):
        """
        Adds ordering to the query.

        Usage:
            .order_by("name")           # Ascending
            .order_by("-age")           # Descending (prefix with -)
            .order_by("name", "-age")   # Multiple fields

        :type fields: tuple
        :param fields: Field names to order by
        :rtype: QueryBuilder
        :return: self for chaining
        """
        for field in fields:
            if field.startswith("-"):
                # Descending order
                self._order_by.append((field[1:], "desc"))
            else:
                # Ascending order
                self._order_by.append((field, "asc"))

        return self

    def limit(self, count):
        """
        Limits the number of results.

        Usage:
            .limit(10)

        :type count: int
        :param count: Maximum number of results
        :rtype: QueryBuilder
        :return: self for chaining
        """
        self._number_records = count
        return self

    def offset(self, count):
        """
        Skips the first N results.

        Usage:
            .offset(20).limit(10)  # Get results 20-30

        :type count: int
        :param count: Number of results to skip
        :rtype: QueryBuilder
        :return: self for chaining
        """
        self._start_record = count
        return self

    def eager(self, *relations):
        """
        Eagerly loads related entities.

        Usage:
            .eager("dogs", "cars")  # Load dogs and cars relations

        :type relations: tuple
        :param relations: Relation names to eagerly load
        :rtype: QueryBuilder
        :return: self for chaining
        """
        for relation in relations:
            self._eager_relations[relation] = {}
        return self

    def lock(self):
        """
        Adds a FOR UPDATE lock to the query.

        Usage:
            .lock()  # Locks selected rows

        :rtype: QueryBuilder
        :return: self for chaining
        """
        self._lock = True
        return self

    def only(self, *fields):
        """
        Selects only specific fields.

        Usage:
            .only("name", "age")  # Only load name and age

        :type fields: tuple
        :param fields: Field names to load
        :rtype: QueryBuilder
        :return: self for chaining
        """
        self._fields = list(fields)
        return self

    def _build_options(self):
        """
        Builds the options dictionary for entity_manager.find().

        :rtype: dict
        :return: Options dictionary
        """
        options = {}

        if self._filters:
            options["filters"] = self._filters

        if self._order_by:
            options["order_by"] = self._order_by

        if self._start_record is not None:
            options["start_record"] = self._start_record

        if self._number_records is not None:
            options["number_records"] = self._number_records

        if self._eager_relations:
            options["eager"] = self._eager_relations

        if self._lock:
            options["lock"] = True

        if self._fields:
            options["fields"] = self._fields

        return options

    def all(self):
        """
        Executes the query and returns all results.

        :rtype: list
        :return: List of entity instances
        """
        options = self._build_options()
        return self._entity_manager.find(self._entity_class, options)

    def first(self):
        """
        Executes the query and returns the first result.

        :rtype: EntityClass or None
        :return: First entity or None if no results
        """
        options = self._build_options()
        options["number_records"] = 1
        results = self._entity_manager.find(self._entity_class, options)
        return results[0] if results else None

    def count(self):
        """
        Returns the count of matching records.

        :rtype: int
        :return: Count of matching entities
        """
        options = self._build_options()
        options["count"] = True
        return self._entity_manager.count(self._entity_class, options)

    def exists(self):
        """
        Returns whether any matching records exist.

        :rtype: bool
        :return: True if at least one match exists
        """
        return self.count() > 0

    def get(self, **kwargs):
        """
        Gets a single entity matching the criteria.
        Raises exception if not found or multiple found.

        Usage:
            .get(object_id=123)

        :rtype: EntityClass
        :return: The matching entity
        """
        self.filter(**kwargs)
        options = self._build_options()
        results = self._entity_manager.find(self._entity_class, options)

        if len(results) == 0:
            raise Exception("No %s found matching criteria" % self._entity_class.__name__)
        elif len(results) > 1:
            raise Exception(
                "Multiple %s found matching criteria" % self._entity_class.__name__
            )

        return results[0]

    def delete(self):
        """
        Deletes all entities matching the query.

        :rtype: int
        :return: Number of entities deleted
        """
        entities = self.all()
        for entity in entities:
            self._entity_manager.remove(entity)
        return len(entities)

    def update(self, **kwargs):
        """
        Updates all entities matching the query.

        Usage:
            .filter(status=1).update(status=2)

        :type kwargs: dict
        :param kwargs: Fields to update
        :rtype: int
        :return: Number of entities updated
        """
        entities = self.all()
        for entity in entities:
            for key, value in kwargs.items():
                setattr(entity, key, value)
            self._entity_manager.update(entity)
        return len(entities)

    def clone(self):
        """
        Creates a copy of this query builder.

        :rtype: QueryBuilder
        :return: Cloned query builder
        """
        import copy

        new_qb = QueryBuilder(self._entity_manager, self._entity_class)
        new_qb._filters = copy.deepcopy(self._filters)
        new_qb._order_by = list(self._order_by)
        new_qb._start_record = self._start_record
        new_qb._number_records = self._number_records
        new_qb._eager_relations = dict(self._eager_relations)
        new_qb._lock = self._lock
        new_qb._fields = list(self._fields) if self._fields else None

        return new_qb


class Q(object):
    """
    Q object for complex query expressions.

    Allows combining filters with AND/OR logic:

    Usage:
        # (age > 18 AND name = "John") OR (age > 65)
        Q(age__gt=18, name="John") | Q(age__gt=65)

        # age > 18 AND (status = 1 OR status = 2)
        Q(age__gt=18) & (Q(status=1) | Q(status=2))

    Note: This is a future enhancement - not fully integrated yet.
    """

    def __init__(self, **kwargs):
        self.filters = kwargs
        self.children = []
        self.connector = "AND"

    def __or__(self, other):
        """
        Combines two Q objects with OR.
        """
        new_q = Q()
        new_q.children = [self, other]
        new_q.connector = "OR"
        return new_q

    def __and__(self, other):
        """
        Combines two Q objects with AND.
        """
        new_q = Q()
        new_q.children = [self, other]
        new_q.connector = "AND"
        return new_q

    def to_filters(self):
        """
        Converts Q object to Colony filter format.

        :rtype: dict
        :return: Filter dictionary
        """
        if not self.children:
            return self.filters

        # For complex expressions, would need to build nested filters
        # This is a simplified implementation
        result = {}
        for child in self.children:
            if isinstance(child, Q):
                result.update(child.to_filters())
            else:
                result.update(child)

        return result
