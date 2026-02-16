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


class LazyCollection(object):
    """
    Lazy-loading collection wrapper that loads all items in a single query
    on first access, preventing N+1 query problems.

    Usage:
        # Instead of:
        for dog in person.dogs:  # Each iteration triggers a query
            print(dog.name)

        # LazyCollection loads all dogs in one query on first iteration:
        dogs = LazyCollection(person, "dogs", entity_manager)
        for dog in dogs:  # Single query for all dogs
            print(dog.name)

    The collection behaves like a list but only queries the database
    when needed (lazy loading) and caches the results.
    """

    def __init__(self, owner, relation_name, entity_manager):
        """
        Constructor for lazy collection.

        :type owner: EntityClass
        :param owner: The entity that owns this relation
        :type relation_name: String
        :param relation_name: The name of the relation attribute
        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to use for queries
        """
        self._owner = owner
        self._relation_name = relation_name
        self._entity_manager = entity_manager
        self._loaded = False
        self._items = []

    def _ensure_loaded(self):
        """
        Loads all items from the database if not already loaded.
        This is called automatically on first access.
        """
        if self._loaded:
            return

        # Get the relation metadata
        owner_class = self._owner.__class__
        relation = owner_class.get_relation(self._relation_name)
        target_class = owner_class.get_target(self._relation_name)

        # Build the filter to get related items
        options = self._build_options(owner_class, relation, target_class)

        # Execute the query to load all items
        self._items = self._entity_manager.find(target_class, options)
        self._loaded = True

    def _build_options(self, owner_class, relation, target_class):
        """
        Builds the query options to load related items.

        :type owner_class: Class
        :param owner_class: The owner's entity class
        :type relation: dict
        :param relation: The relation metadata
        :type target_class: Class
        :param target_class: The target entity class
        :rtype: dict
        :return: Query options for finding related items
        """
        options = {}

        # Determine if this is a mapped relation (FK on this side)
        # or a reverse relation (FK on other side)
        mapper = owner_class.get_mapper(self._relation_name)

        if mapper == owner_class:
            # This side has the FK - shouldn't happen for to-many,
            # but handle it anyway
            # This would be used for finding the target of a to-one relation
            reverse_name = owner_class.get_reverse(self._relation_name)
            fk_value = getattr(self._owner, self._relation_name + "_id", None)
            if fk_value:
                options["filters"] = {"object_id": fk_value}
        else:
            # Other side has the FK (typical for to-many)
            # Need to find items where their FK points to us
            reverse_name = owner_class.get_reverse(self._relation_name)

            # Get our ID
            owner_id = owner_class.get_id_value(self._owner)

            # Build filter: target.reverse_fk = owner_id
            if reverse_name:
                options["filters"] = {reverse_name + "_id": owner_id}

        return options

    def __len__(self):
        """
        Returns the number of items in the collection.
        Triggers loading if not already loaded.
        """
        self._ensure_loaded()
        return len(self._items)

    def __iter__(self):
        """
        Iterates over the collection.
        Triggers loading if not already loaded.
        """
        self._ensure_loaded()
        return iter(self._items)

    def __getitem__(self, index):
        """
        Gets an item by index.
        Triggers loading if not already loaded.
        """
        self._ensure_loaded()
        return self._items[index]

    def __contains__(self, item):
        """
        Checks if an item is in the collection.
        Triggers loading if not already loaded.
        """
        self._ensure_loaded()
        return item in self._items

    def __bool__(self):
        """
        Returns True if the collection is not empty.
        Triggers loading if not already loaded.
        """
        self._ensure_loaded()
        return bool(self._items)

    # Python 2 compatibility
    __nonzero__ = __bool__

    def append(self, item):
        """
        Adds an item to the collection.
        Note: This only adds to the in-memory collection,
        doesn't persist to database.
        """
        self._ensure_loaded()
        if item not in self._items:
            self._items.append(item)

    def remove(self, item):
        """
        Removes an item from the collection.
        Note: This only removes from the in-memory collection,
        doesn't persist to database.
        """
        self._ensure_loaded()
        self._items.remove(item)

    def all(self):
        """
        Returns all items as a list.
        Triggers loading if not already loaded.
        """
        self._ensure_loaded()
        return list(self._items)

    def first(self):
        """
        Returns the first item or None if empty.
        Triggers loading if not already loaded.
        """
        self._ensure_loaded()
        return self._items[0] if self._items else None

    def count(self):
        """
        Returns the count of items.
        Triggers loading if not already loaded.
        """
        return len(self)

    def filter(self, **kwargs):
        """
        Filters the collection by attribute values.
        This operates on the already-loaded items.

        :rtype: list
        :return: Filtered list of items
        """
        self._ensure_loaded()
        result = []
        for item in self._items:
            match = True
            for key, value in kwargs.items():
                if getattr(item, key, None) != value:
                    match = False
                    break
            if match:
                result.append(item)
        return result

    def is_loaded(self):
        """
        Returns whether the collection has been loaded.

        :rtype: bool
        :return: True if loaded, False otherwise
        """
        return self._loaded

    def reload(self):
        """
        Forces a reload of the collection from the database.
        """
        self._loaded = False
        self._items = []
        self._ensure_loaded()


class BatchLoader(object):
    """
    Batch loader for efficiently loading related entities across multiple
    parent entities in a single query.

    This solves the N+1 problem when iterating over a collection:

        # Without batch loading (N+1 queries):
        for person in people:  # 1 query
            for dog in person.dogs:  # N queries
                print(dog.name)

        # With batch loading (2 queries):
        BatchLoader.load_relation(entity_manager, people, "dogs")
        for person in people:  # Already loaded
            for dog in person.dogs:  # No query - already loaded
                print(dog.name)
    """

    @staticmethod
    def load_relation(entity_manager, entities, relation_name):
        """
        Batch loads a relation for multiple entities in a single query.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager
        :type entities: list
        :param entities: List of entities to load relations for
        :type relation_name: String
        :param relation_name: The relation to load
        """
        if not entities:
            return

        # Get the entity class and relation metadata
        entity_class = entities[0].__class__
        relation = entity_class.get_relation(relation_name)
        target_class = entity_class.get_target(relation_name)
        reverse_name = entity_class.get_reverse(relation_name)

        # Collect all entity IDs
        entity_ids = [entity_class.get_id_value(entity) for entity in entities]

        # Query for all related items in one go
        options = {"filters": {reverse_name + "_id": {"$in": entity_ids}}}

        related_items = entity_manager.find(target_class, options)

        # Group related items by parent ID
        grouped = {}
        for item in related_items:
            parent_id = getattr(item, reverse_name + "_id", None)
            if parent_id not in grouped:
                grouped[parent_id] = []
            grouped[parent_id].append(item)

        # Assign to parent entities
        for entity in entities:
            entity_id = entity_class.get_id_value(entity)
            items = grouped.get(entity_id, [])

            # Create a pre-loaded lazy collection
            collection = LazyCollection(entity, relation_name, entity_manager)
            collection._items = items
            collection._loaded = True

            # Set it on the entity
            entity.__dict__[relation_name] = collection


class LazyProxy(object):
    """
    Lazy proxy for to-one relations that loads the related entity
    only when accessed.

    Usage:
        # person.parent is a LazyProxy
        parent = person.parent  # Triggers query only when accessed
        print(parent.name)
    """

    def __init__(self, owner, relation_name, entity_manager):
        """
        Constructor for lazy proxy.

        :type owner: EntityClass
        :param owner: The entity that owns this relation
        :type relation_name: String
        :param relation_name: The name of the relation attribute
        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to use for queries
        """
        self._owner = owner
        self._relation_name = relation_name
        self._entity_manager = entity_manager
        self._loaded = False
        self._target = None

    def _ensure_loaded(self):
        """
        Loads the target entity if not already loaded.
        """
        if self._loaded:
            return

        # Get the relation metadata
        owner_class = self._owner.__class__
        target_class = owner_class.get_target(self._relation_name)

        # Get the foreign key value
        fk_column = self._relation_name + "_id"
        fk_value = getattr(self._owner, fk_column, None)

        if fk_value:
            # Load the target entity
            self._target = self._entity_manager.get(target_class, fk_value)

        self._loaded = True

    def __getattr__(self, name):
        """
        Delegates attribute access to the target entity.
        """
        self._ensure_loaded()
        if self._target:
            return getattr(self._target, name)
        raise AttributeError("Relation '%s' is None" % self._relation_name)

    def __bool__(self):
        """
        Returns True if the target exists.
        """
        self._ensure_loaded()
        return self._target is not None

    # Python 2 compatibility
    __nonzero__ = __bool__

    def get(self):
        """
        Returns the actual target entity.
        """
        self._ensure_loaded()
        return self._target
