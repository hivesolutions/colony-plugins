# Entity Manager ORM Improvements

This document describes the new features and improvements added to Colony's Entity Manager ORM.

## Table of Contents

1. [Overview](#overview)
2. [New Features](#new-features)
3. [Mapping Strategies](#mapping-strategies)
4. [Descriptor-Based Fields](#descriptor-based-fields)
5. [Inheritance Strategies](#inheritance-strategies)
6. [Lazy Collections](#lazy-collections)
7. [Query Builder API](#query-builder-api)
8. [Migration Guide](#migration-guide)
9. [Integration Roadmap](#integration-roadmap)

## Overview

These improvements address several limitations in the original Entity Manager implementation:

- **Hardcoded mapping strategy** → Pluggable mapping strategies
- **Dict-based field definitions** → Descriptor-based fields with validation
- **Only vertical inheritance** → Multiple inheritance strategies
- **N+1 query problems** → Lazy collection loading
- **Nested dict queries** → Fluent query builder API

All improvements maintain **backward compatibility** with existing code.

## New Features

### 1. Mapping Strategies

**Location**: `mapping_strategies.py`

Provides pluggable strategies for determining relationship ownership and foreign key placement.

#### Available Strategies

**DefaultMappingStrategy** (preserves original behavior)
```python
# Uses is_mapper flags
class Person(EntityClass):
    @staticmethod
    def _relation_dogs():
        return dict(type="to-many", target=Dog, reverse="owner")

class Dog(EntityClass):
    @staticmethod
    def _relation_owner():
        return dict(type="to-one", target=Person, reverse="dogs", is_mapper=True)
```

**ConventionOverConfigurationStrategy** (Rails/Django-style)
```python
# Infers ownership from relation types - no flags needed!
class Person(EntityClass):
    parent = RelationField("to-one", "Person", reverse="children")  # Owns FK
    children = RelationField("to-many", "Person", reverse="parent")  # Doesn't own FK
```

**AnnotationBasedStrategy** (JPA/Hibernate-style)
```python
# Explicit annotations
class Person(EntityClass):
    boss = RelationField(
        "to-one",
        "Person",
        reverse="employees",
        join_column="boss_object_id"  # Explicit FK name
    )
```

#### Usage

```python
# Configure via entity manager options
entity_manager = plugin.load_entity_manager("mysql", {
    "id": "my_em",
    "entities_list": [Person, Dog],
    "options": {
        "mapping_strategy": ConventionOverConfigurationStrategy()
    }
})
```

### 2. Descriptor-Based Fields

**Location**: `fields.py`

Modern Python descriptors replace dict-based field definitions.

#### Benefits

- ✅ Better IDE autocomplete
- ✅ Type hints support
- ✅ Field-level validation
- ✅ Cleaner syntax
- ✅ More Pythonic

#### Available Field Types

```python
from entity_manager import fields

class Person(EntityClass):
    # ID field with auto-generation
    object_id = fields.IdField(generated=True)

    # Text fields
    name = fields.TextField(nullable=False, max_length=255)
    email = fields.TextField(unique=True)

    # Numeric fields with validation
    age = fields.IntegerField(min_value=0, max_value=150, indexed=True)
    weight = fields.FloatField(min_value=0.0)

    # Date field
    birth_date = fields.DateField()

    # Metadata (JSON storage)
    metadata = fields.MetadataField()

    # Relations
    parent = fields.RelationField("to-one", "Person", reverse="children", is_mapper=True)
    dogs = fields.RelationField("to-many", "Dog", reverse="owner")
```

#### Embedded Components

```python
class Address(object):
    street = fields.TextField()
    city = fields.TextField()
    country = fields.TextField()

class Person(EntityClass):
    # Flattens to: home_street, home_city, home_country columns
    home_address = fields.EmbeddedField(Address, prefix="home_")
    work_address = fields.EmbeddedField(Address, prefix="work_")

# Usage
person.home_address.street = "123 Main St"
person.home_address.city = "New York"
```

#### Field Validation

```python
person = Person()
person.age = 25  # OK
person.age = 200  # Raises ValueError (exceeds max_value)
person.name = None  # Raises ValueError (nullable=False)
```

#### Backward Compatibility

Field descriptors are converted to dicts internally:

```python
class Person(EntityClass):
    # New style
    name = fields.TextField(nullable=False)

    # Converted internally to:
    # name = dict(type="text", mandatory=True)
```

### 3. Inheritance Strategies

**Location**: `inheritance_strategies.py`

Supports multiple strategies for mapping class hierarchies to tables.

#### JoinedTableStrategy (default, current behavior)

Each class gets its own table with FK to parent.

```python
class Animal(EntityClass):
    name = fields.TextField()

class Dog(Animal):
    breed = fields.TextField()

# Creates tables:
# - _animal: object_id, name
# - _dog: object_id (FK to _animal), breed
```

**Pros**: Normalized, easy to extend
**Cons**: Requires joins, slower for deep hierarchies

#### SingleTableStrategy (new!)

All classes share one table with discriminator column.

```python
class Animal(EntityClass):
    __inheritance_strategy__ = "single_table"
    __discriminator_column__ = "animal_type"
    __discriminator_value__ = "animal"

    name = fields.TextField()

class Dog(Animal):
    __discriminator_value__ = "dog"
    breed = fields.TextField()

class Cat(Animal):
    __discriminator_value__ = "cat"
    indoor = fields.IntegerField()

# Creates ONE table:
# - _animal: object_id, animal_type, name, breed, indoor
```

**Pros**: No joins, fast queries, simple schema
**Cons**: Many nullable columns, wide table

#### TablePerClassStrategy (new!)

Each concrete class gets a complete table.

```python
class Animal(EntityClass):
    __inheritance_strategy__ = "table_per_class"
    name = fields.TextField()

class Dog(Animal):
    breed = fields.TextField()

# Creates tables:
# - _dog: object_id, name, breed (includes inherited fields)
```

**Pros**: No joins, self-contained tables
**Cons**: Duplicate columns, polymorphic queries difficult

#### Usage

```python
# Set on base class
class Animal(EntityClass):
    __inheritance_strategy__ = "single_table"
    __discriminator_column__ = "type"

# Query polymorphically
all_animals = entity_manager.find(Animal, {})  # Returns Dog, Cat, etc.

# Query specific subclass
only_dogs = entity_manager.find(Dog, {})  # Automatically filters by discriminator
```

### 4. Lazy Collections

**Location**: `lazy_collections.py`

Prevents N+1 query problems when loading related entities.

#### The N+1 Problem

```python
# BAD: N+1 queries
people = entity_manager.find(Person, {})  # 1 query
for person in people:  # N queries follow
    for dog in person.dogs:  # Each iteration queries DB!
        print(dog.name)
```

#### Solution 1: LazyCollection

Loads all items in one query on first access.

```python
# GOOD: 2 queries total
people = entity_manager.find(Person, {})  # 1 query
for person in people:
    # First access to person.dogs triggers ONE query for all dogs
    for dog in person.dogs:  # No additional queries
        print(dog.name)
```

#### Solution 2: BatchLoader

Pre-loads relations for multiple entities at once.

```python
from entity_manager import BatchLoader

# Load all people
people = entity_manager.find(Person, {})  # 1 query

# Batch load all their dogs in one query
BatchLoader.load_relation(entity_manager, people, "dogs")  # 1 query

# Now iterate without queries
for person in people:
    for dog in person.dogs:  # Already loaded!
        print(dog.name)
```

#### Solution 3: Eager Loading (via Query Builder)

```python
# One query with joins
people = entity_manager.query(Person).eager("dogs").all()
```

#### LazyProxy for to-one Relations

```python
from entity_manager import LazyProxy

# Delays loading until accessed
person.parent  # Returns LazyProxy
person.parent.name  # Now triggers query
```

### 5. Query Builder API

**Location**: `query_builder.py`

Fluent interface for building queries instead of nested dictionaries.

#### Basic Usage

```python
from entity_manager import QueryBuilder

# Old way
results = entity_manager.find(Person, {
    "filters": {"age": {"$gt": 18}},
    "order_by": [("name", "asc")],
    "start_record": 0,
    "number_records": 10
})

# New way
results = (
    entity_manager.query(Person)
    .filter(age__gt=18)
    .order_by("name")
    .limit(10)
    .all()
)
```

#### Filter Operators

```python
# Django-style double-underscore lookups
query = entity_manager.query(Person)

query.filter(age=25)              # Exact match
query.filter(age__gt=18)          # Greater than
query.filter(age__gte=18)         # Greater than or equal
query.filter(age__lt=65)          # Less than
query.filter(age__lte=65)         # Less than or equal
query.filter(name__like="John%")  # SQL LIKE
query.filter(status__in=[1,2,3])  # IN clause
query.filter(age__ne=0)           # Not equal
```

#### Chaining

```python
adults = (
    entity_manager.query(Person)
    .filter(age__gte=18, age__lte=65)
    .filter(status=1)
    .order_by("name", "-age")  # name ASC, age DESC
    .limit(20)
    .offset(10)
    .all()
)
```

#### Query Methods

```python
# Get all results
people = query.all()

# Get first result
person = query.first()

# Get single result (raises if 0 or multiple)
john = entity_manager.query(Person).get(name="John Doe")

# Count
count = query.count()

# Check existence
exists = query.exists()

# Eager load relations
people = query.eager("dogs", "cars").all()

# Select specific fields
people = query.only("name", "age").all()

# Locking (FOR UPDATE)
person = query.filter(object_id=123).lock().first()
```

#### Bulk Operations

```python
# Update all matching
entity_manager.query(Person).filter(age__lt=18).update(status=2)

# Delete all matching
entity_manager.query(Person).filter(status=0).delete()
```

#### Clone Queries

```python
base_query = entity_manager.query(Person).filter(status=1)

# Clone and extend
adults = base_query.clone().filter(age__gte=18).all()
children = base_query.clone().filter(age__lt=18).all()
```

## Migration Guide

### Gradual Migration

All new features are **opt-in** and backward compatible.

#### Step 1: Start Using Query Builder

```python
# Replace this:
people = entity_manager.find(Person, {"filters": {"age": {"$gt": 18}}})

# With this:
people = entity_manager.query(Person).filter(age__gt=18).all()
```

#### Step 2: Add Descriptor Fields to New Entities

```python
# New entities can use descriptors
class NewEntity(EntityClass):
    name = fields.TextField(nullable=False)
    age = fields.IntegerField(min_value=0)

# Old entities continue working
class OldEntity(EntityClass):
    name = dict(type="text", mandatory=True)
    age = dict(type="integer")
```

#### Step 3: Use Batch Loading for Performance

```python
# Add BatchLoader where N+1 problems exist
people = entity_manager.find(Person, {})
BatchLoader.load_relation(entity_manager, people, "dogs")
```

#### Step 4: Try Alternative Strategies

```python
# Create new entity manager with convention-based mapping
em = plugin.load_entity_manager("mysql", {
    "options": {
        "mapping_strategy": ConventionOverConfigurationStrategy()
    }
})
```

## Integration Roadmap

To fully integrate these features into the existing codebase, the following changes are needed:

### Phase 1: Core Integration

#### 1.1 EntityManager Updates (system.py)

```python
class EntityManager(object):
    def __init__(self, ..., options={}):
        # Add mapping strategy support
        self.mapping_strategy = options.get(
            'mapping_strategy',
            DefaultMappingStrategy()
        )

    def query(self, entity_class):
        """Add query builder method"""
        return QueryBuilder(self, entity_class)
```

#### 1.2 EntityClass Updates (structures.py)

```python
class EntityClass(object):
    @classmethod
    def get_items_map(cls):
        """Support Field descriptors"""
        items = {}
        for name in dir(cls):
            value = getattr(cls, name)
            if isinstance(value, Field):
                items[name] = value.to_dict()
            elif isinstance(value, dict) and 'type' in value:
                items[name] = value
        return items

    @classmethod
    def get_mapper(cls, relation_name, get_mapper_name=False):
        """Delegate to mapping strategy"""
        strategy = cls._get_mapping_strategy()
        return strategy.get_mapper(cls, relation_name, get_mapper_name)
```

### Phase 2: Advanced Features

#### 2.1 Inheritance Strategy Support

```python
def create_tables(self, entity_classes):
    """Use inheritance strategies"""
    for entity_class in entity_classes:
        strategy = get_inheritance_strategy(entity_class)
        if strategy.should_create_table(entity_class):
            fields = strategy.get_fields_for_table(entity_class)
            self._create_table(entity_class, fields)
```

#### 2.2 Lazy Collection Integration

```python
def _load_lazy_relation(self, relation_name):
    """Return LazyCollection instead of list"""
    return LazyCollection(self, relation_name, self._entity_manager)
```

### Phase 3: Testing & Documentation

- Unit tests for all new features
- Integration tests with existing code
- Performance benchmarks
- Update documentation
- Migration guide for existing projects

## Performance Improvements

### Before

```python
# N+1 queries
people = entity_manager.find(Person, {})  # 1 query
for person in people:  # 100 people
    for dog in person.dogs:  # 100 queries
        print(dog.name)
# Total: 101 queries
```

### After

```python
# 2 queries
people = entity_manager.find(Person, {})
BatchLoader.load_relation(entity_manager, people, "dogs")
for person in people:
    for dog in person.dogs:
        print(dog.name)
# Total: 2 queries (50x improvement!)
```

## Best Practices

### 1. Use Query Builder for Readability

```python
# ✅ Good
entity_manager.query(Person).filter(age__gt=18).order_by("name").all()

# ❌ Harder to read
entity_manager.find(Person, {"filters": {"age": {"$gt": 18}}, "order_by": [("name", "asc")]})
```

### 2. Batch Load Relations

```python
# ✅ Good - 2 queries
people = entity_manager.find(Person, {})
BatchLoader.load_relation(entity_manager, people, "dogs")

# ❌ Bad - N+1 queries
people = entity_manager.find(Person, {})
for person in people:
    for dog in person.dogs:
        pass
```

### 3. Use Appropriate Inheritance Strategy

- **Few subclasses, different fields** → SingleTableStrategy
- **Many subclasses, shared queries** → JoinedTableStrategy
- **Independent subclasses** → TablePerClassStrategy

### 4. Validate at the Field Level

```python
# ✅ Good - validation happens on assignment
class Person(EntityClass):
    age = fields.IntegerField(min_value=0, max_value=150)

# ❌ Less robust - validation only at save time
class Person(EntityClass):
    age = dict(type="integer")
```

## Examples

See `examples_new_features.py` for complete working examples of all features.

## Contributing

When adding new mapping or inheritance strategies:

1. Extend the appropriate base class (`MappingStrategy` or `InheritanceStrategy`)
2. Implement all required methods
3. Add tests
4. Update documentation
5. Add example usage

## Questions?

For questions or issues with these improvements, please file an issue on the Colony repository.
