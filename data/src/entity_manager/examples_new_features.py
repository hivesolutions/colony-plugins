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

"""
Comprehensive examples demonstrating the new Entity Manager features:

1. Mapping Strategies (DefaultMappingStrategy, ConventionOverConfigurationStrategy, AnnotationBasedStrategy)
2. Descriptor-based Fields (Field, TextField, IntegerField, RelationField, etc.)
3. Inheritance Strategies (SingleTableStrategy, JoinedTableStrategy, TablePerClassStrategy)
4. Lazy Collections (preventing N+1 queries)
5. Query Builder API (fluent interface for building queries)
"""

from . import structures
from . import fields
from . import mapping_strategies
from . import inheritance_strategies
from . import query_builder
from . import lazy_collections


# ==============================================================================
# Example 1: Descriptor-Based Field Definitions
# ==============================================================================


class ModernPerson(structures.EntityClass):
    """
    Example entity using descriptor-based field definitions instead of dicts.

    Benefits:
    - Better IDE autocomplete and type hints
    - Validation at assignment time
    - Cleaner syntax
    - More Pythonic
    """

    # ID field with auto-generation
    object_id = fields.IdField(generated=True)

    # Text fields with validation
    name = fields.TextField(nullable=False, max_length=255)
    email = fields.TextField(nullable=False, unique=True)

    # Numeric fields with range validation
    age = fields.IntegerField(min_value=0, max_value=150, indexed=True)
    weight = fields.FloatField(min_value=0.0)

    # Date field
    birth_date = fields.DateField()

    # Metadata field for JSON data
    metadata = fields.MetadataField()

    # Relations using RelationField descriptors
    parent = fields.RelationField("to-one", "ModernPerson", reverse="children", is_mapper=True)
    children = fields.RelationField("to-many", "ModernPerson", reverse="parent")
    dogs = fields.RelationField("to-many", "ModernDog", reverse="owner")

    def __init__(self):
        self.name = "Anonymous"
        self.age = 18


class ModernDog(structures.EntityClass):
    """Example related entity."""

    object_id = fields.IdField(generated=True)
    name = fields.TextField(nullable=False)
    breed = fields.TextField()
    owner = fields.RelationField("to-one", "ModernPerson", reverse="dogs", is_mapper=True)


# ==============================================================================
# Example 2: Single-Table Inheritance
# ==============================================================================


class Animal(structures.EntityClass):
    """
    Base class using single-table inheritance.

    All Animal subclasses share the same table with a discriminator column.
    """

    # Configure single-table inheritance
    __inheritance_strategy__ = "single_table"
    __discriminator_column__ = "animal_type"
    __discriminator_value__ = "animal"

    object_id = fields.IdField(generated=True)
    name = fields.TextField()
    age = fields.IntegerField()


class Dog(Animal):
    """Dog subclass - stored in same table as Animal."""

    __discriminator_value__ = "dog"

    breed = fields.TextField()
    bark_volume = fields.IntegerField()  # Dog-specific field


class Cat(Animal):
    """Cat subclass - stored in same table as Animal."""

    __discriminator_value__ = "cat"

    indoor = fields.IntegerField()  # 1=indoor, 0=outdoor
    meow_frequency = fields.IntegerField()  # Cat-specific field


# ==============================================================================
# Example 3: Embedded Components
# ==============================================================================


class Address(object):
    """
    Component class (not a full entity) that can be embedded.
    """

    street = fields.TextField()
    city = fields.TextField()
    postal_code = fields.TextField()
    country = fields.TextField()


class PersonWithAddress(structures.EntityClass):
    """
    Entity with embedded address components.

    The home_address and work_address fields are flattened into columns:
    - home_street, home_city, home_postal_code, home_country
    - work_street, work_city, work_postal_code, work_country
    """

    object_id = fields.IdField(generated=True)
    name = fields.TextField()

    # Embedded components with prefix
    home_address = fields.EmbeddedField(Address, prefix="home_")
    work_address = fields.EmbeddedField(Address, prefix="work_")


# ==============================================================================
# Example 4: Convention-Based Mapping Strategy
# ==============================================================================


class ConventionPerson(structures.EntityClass):
    """
    Example using convention-over-configuration mapping.

    With ConventionOverConfigurationStrategy, you don't need to specify
    is_mapper flags - the ORM infers ownership from relation types:
    - to-one relations own the FK
    - to-many relations don't own the FK
    """

    object_id = fields.IdField(generated=True)
    name = fields.TextField()

    # No is_mapper needed - convention says to-one owns FK
    parent = fields.RelationField("to-one", "ConventionPerson", reverse="children")

    # No need to specify ownership - inferred from reverse to-one
    children = fields.RelationField("to-many", "ConventionPerson", reverse="parent")


# ==============================================================================
# Example 5: Annotation-Based Mapping Strategy
# ==============================================================================


class AnnotatedPerson(structures.EntityClass):
    """
    Example using JPA-style annotation-based mapping.

    Explicit join columns and join tables provide maximum control.
    """

    object_id = fields.IdField(generated=True)
    name = fields.TextField()

    # Explicit join column specification
    boss = fields.RelationField(
        "to-one",
        "AnnotatedPerson",
        reverse="employees",
        join_column="boss_object_id"  # Explicit FK column name
    )

    employees = fields.RelationField("to-many", "AnnotatedPerson", reverse="boss")

    # Many-to-many with explicit join table
    projects = fields.RelationField(
        "to-many",
        "Project",
        reverse="members",
        join_table={
            "name": "person_project",
            "join_columns": ["person_id"],
            "inverse_join_columns": ["project_id"]
        }
    )


class Project(structures.EntityClass):
    """Project entity for many-to-many example."""

    object_id = fields.IdField(generated=True)
    name = fields.TextField()
    members = fields.RelationField("to-many", "AnnotatedPerson", reverse="projects")


# ==============================================================================
# Usage Examples
# ==============================================================================


def example_query_builder(entity_manager):
    """
    Demonstrates the fluent query builder API.
    """
    # Old way (nested dicts)
    old_results = entity_manager.find(ModernPerson, {
        "filters": {
            "age": {"$gt": 18},
            "name": {"$like": "John%"}
        },
        "order_by": [("name", "asc")],
        "start_record": 0,
        "number_records": 10
    })

    # New way (fluent interface)
    new_results = (
        entity_manager.query(ModernPerson)
        .filter(age__gt=18)
        .filter(name__like="John%")
        .order_by("name")
        .limit(10)
        .all()
    )

    # Chaining multiple filters
    adults = (
        entity_manager.query(ModernPerson)
        .filter(age__gte=18, age__lte=65)
        .filter(email__like="%@example.com")
        .order_by("-age")  # Descending
        .all()
    )

    # Get single entity
    john = entity_manager.query(ModernPerson).get(name="John Doe")

    # Count
    count = entity_manager.query(ModernPerson).filter(age__gt=18).count()

    # Exists check
    has_adults = entity_manager.query(ModernPerson).filter(age__gt=18).exists()

    # First result
    youngest = entity_manager.query(ModernPerson).order_by("age").first()

    # Eager loading
    people_with_dogs = (
        entity_manager.query(ModernPerson)
        .eager("dogs")
        .all()
    )

    # Locking
    locked_person = (
        entity_manager.query(ModernPerson)
        .filter(object_id=123)
        .lock()
        .first()
    )

    # Update
    entity_manager.query(ModernPerson).filter(age__lt=18).update(status=2)

    # Delete
    entity_manager.query(ModernPerson).filter(status=0).delete()


def example_lazy_collections(entity_manager):
    """
    Demonstrates lazy collections to prevent N+1 queries.
    """
    # Problem: N+1 queries (old behavior)
    people = entity_manager.find(ModernPerson, {})
    for person in people:  # 1 query
        for dog in person.dogs:  # N queries (one per person)
            print(dog.name)

    # Solution 1: Batch loading
    people = entity_manager.find(ModernPerson, {})
    lazy_collections.BatchLoader.load_relation(entity_manager, people, "dogs")
    for person in people:  # Now all dogs are pre-loaded
        for dog in person.dogs:  # No additional queries
            print(dog.name)

    # Solution 2: Eager loading via query builder
    people = entity_manager.query(ModernPerson).eager("dogs").all()
    for person in people:
        for dog in person.dogs:  # Already loaded
            print(dog.name)


def example_mapping_strategies(entity_manager):
    """
    Demonstrates how to use different mapping strategies.
    """
    # Configure entity manager with convention-based mapping
    from . import mapping_strategies

    # Option 1: Set globally via entity manager options
    entity_manager_with_conventions = entity_manager.plugin.load_entity_manager(
        "sqlite",
        {
            "id": "convention_based",
            "entities_list": [ConventionPerson],
            "options": {
                "mapping_strategy": mapping_strategies.ConventionOverConfigurationStrategy()
            }
        }
    )

    # Option 2: Set on specific entity class
    # (This would require modifications to EntityClass to check for a
    # __mapping_strategy__ attribute)

    # Using annotation-based mapping
    entity_manager_annotated = entity_manager.plugin.load_entity_manager(
        "sqlite",
        {
            "id": "annotation_based",
            "entities_list": [AnnotatedPerson, Project],
            "options": {
                "mapping_strategy": mapping_strategies.AnnotationBasedStrategy()
            }
        }
    )


def example_inheritance_strategies(entity_manager):
    """
    Demonstrates different inheritance strategies.
    """
    # Single-table inheritance
    # All Animal, Dog, Cat instances share one table
    entity_manager.create_entities([Animal, Dog, Cat])

    # Create instances
    generic_animal = Animal()
    generic_animal.name = "Unknown"
    entity_manager.save(generic_animal)

    dog = Dog()
    dog.name = "Buddy"
    dog.breed = "Golden Retriever"
    dog.bark_volume = 10
    entity_manager.save(dog)

    cat = Cat()
    cat.name = "Whiskers"
    cat.indoor = 1
    cat.meow_frequency = 5
    entity_manager.save(cat)

    # Query all animals (polymorphic query)
    all_animals = entity_manager.find(Animal, {})  # Returns Animal, Dog, and Cat instances

    # Query only dogs
    all_dogs = entity_manager.find(Dog, {})  # Returns only Dog instances

    # The ORM automatically adds discriminator filters based on the class


def example_field_validation():
    """
    Demonstrates field-level validation.
    """
    person = ModernPerson()

    # This works
    person.age = 25

    # This raises ValueError (age > max_value)
    try:
        person.age = 200
    except ValueError as e:
        print("Validation error:", e)

    # This raises ValueError (nullable=False)
    try:
        person.name = None
    except ValueError as e:
        print("Validation error:", e)


# ==============================================================================
# Integration Notes
# ==============================================================================

"""
INTEGRATION GUIDE:

To fully integrate these features into the existing Entity Manager, the following
changes would be needed in system.py and structures.py:

1. EntityManager.__init__() - Accept mapping_strategy parameter:

   def __init__(self, ..., options={}):
       self.mapping_strategy = options.get('mapping_strategy', DefaultMappingStrategy())

2. EntityManager.query() - Add query builder method:

   def query(self, entity_class):
       return QueryBuilder(self, entity_class)

3. EntityClass.get_mapper() - Delegate to strategy:

   @classmethod
   def get_mapper(cls, relation_name, get_mapper_name=False):
       strategy = cls._get_mapping_strategy()
       return strategy.get_mapper(cls, relation_name, get_mapper_name)

4. EntityManager.create_tables() - Use inheritance strategy:

   def create_tables(self, entity_class):
       strategy = get_inheritance_strategy(entity_class)
       if strategy.should_create_table(entity_class):
           fields = strategy.get_fields_for_table(entity_class)
           # Create table with fields

5. EntityClass metadata handling - Support Field descriptors:

   @classmethod
   def get_items_map(cls):
       # Check for Field descriptors in addition to dict attributes
       items = {}
       for name, value in cls.__dict__.items():
           if isinstance(value, Field):
               items[name] = value.to_dict()
           elif isinstance(value, dict) and 'type' in value:
               items[name] = value
       return items

6. Lazy loading - Use LazyCollection:

   def _load_lazy_relation(self, relation_name):
       # Instead of loading items directly, return LazyCollection
       return LazyCollection(self, relation_name, self._entity_manager)

These changes maintain backward compatibility while enabling the new features.
"""
