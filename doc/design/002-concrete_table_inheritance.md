# COP-002: Concrete Table Inheritance Strategy

## Document Information

| Field               | Value                                                                |
| ------------------- | -------------------------------------------------------------------- |
| **Document Number** | COP-002                                                              |
| **Date**            | 2026-03-30                                                           |
| **Author**          | João Magalhães <joamag@hive.pt>                                      |
| **Subject**         | Concrete Table Inheritance as Alternative to Class Table Inheritance |
| **Status**          | Draft                                                                |
| **Version**         | 1.0                                                                  |

## Description

### Problem

The entity manager supports only Class Table Inheritance (CTI), where each class in a hierarchy stores only its own attributes and queries require joins across all parent tables to reconstruct a full entity. For read-heavy workloads with deep hierarchies this introduces significant query complexity and performance overhead, as every retrieval must join multiple tables. There is no alternative strategy that trades storage for query simplicity.

### Solution

Introduce a **Concrete Table Inheritance** strategy that coexists alongside the existing Class Table Inheritance. When an entity hierarchy opts in via `inheritance = "concrete_table"`, every concrete (non-abstract) class in the hierarchy produces a table containing **all attributes from the root down to that class level**. This eliminates joins on read at any hierarchy level and enables polymorphic queries natively — querying a parent class returns all descendant entities since they all have rows in the parent's table.

The key design principle: **each table in the hierarchy is a complete, self-contained view of that class level**. Writing an entity inserts/updates/deletes rows in every ancestor table, duplicating inherited field values. Reading an entity selects from a single table with no joins.

### Schema Design

Given a hierarchy `ConcreteRootEntity -> ConcretePerson -> ConcreteEmployee`:

```text
_concrete_root_entity table:
  object_id (PK), status, metadata, _class, _mtime
  Contains: ALL entities (root, person, employee rows)

_concrete_person table:
  object_id (PK), status, metadata, name, age, weight, _class, _mtime
  Contains: person + employee rows (all fields from root + person)

_concrete_employee table:
  object_id (PK), status, metadata, name, age, weight, salary, _class, _mtime
  Contains: employee rows only (all fields from root + person + employee)
```

The `_class` discriminator is present in every table and stores the actual concrete class name (e.g. `"ConcreteEmployee"`), enabling ad-hoc filtering when needed.

### Query Behavior

**CREATE TABLE**: Each concrete class creates its own table with `get_all_items()` (all inherited + own fields). Parent classes also create their own tables with their own `get_all_items()`. Every table includes `_class` and `_mtime`.

**INSERT** (save): Writing a `ConcreteEmployee` with `object_id=1` produces three inserts:

```sql
INSERT INTO _concrete_root_entity(object_id, status, _class, _mtime) VALUES(1, 1, 'ConcreteEmployee', ...)
INSERT INTO _concrete_person(object_id, status, name, age, _class, _mtime) VALUES(1, 1, 'John', 30, 'ConcreteEmployee', ...)
INSERT INTO _concrete_employee(object_id, status, name, age, salary, _class, _mtime) VALUES(1, 1, 'John', 30, 500, 'ConcreteEmployee', ...)
```

**SELECT** (find/get): Reading from any level is a single-table query with no joins:

```sql
-- Get employee by ID (all fields available, no joins)
SELECT * FROM _concrete_employee WHERE object_id = 1

-- Polymorphic: get all entities at root level
SELECT * FROM _concrete_root_entity

-- Polymorphic: get all persons (includes employees)
SELECT * FROM _concrete_person
```

**UPDATE**: Modifying a `ConcreteEmployee` produces three updates, one per ancestor table:

```sql
UPDATE _concrete_root_entity SET status = 2, _mtime = ... WHERE object_id = 1
UPDATE _concrete_person SET name = 'Jane', _mtime = ... WHERE object_id = 1
UPDATE _concrete_employee SET salary = 600, _mtime = ... WHERE object_id = 1
```

**DELETE**: Removing a `ConcreteEmployee` produces three deletes:

```sql
DELETE FROM _concrete_employee WHERE object_id = 1
DELETE FROM _concrete_person WHERE object_id = 1
DELETE FROM _concrete_root_entity WHERE object_id = 1
```

### Implementation Details

**Strategy Selector**: The `EntityClass` base class gains an `inheritance` class attribute (default `"class_table"`). Setting `inheritance = "concrete_table"` on a root class propagates to all descendants via `get_inheritance_strategy()`.

**Flattened Items**: The `get_all_items()` classmethod on `EntityClass` returns all items (own + inherited from all parents, including abstract parents) flattened into a single dictionary. This is used by `_create_definition_query` and `_save_query` for concrete table entities.

**Table Creation (`create()`)**: For concrete table hierarchies, parent classes are created recursively (not skipped). Each class creates its own table using `get_all_items()` to include all inherited columns.

**Save/Update/Delete Queries**: For concrete table entities, the `items_map` used for query generation iterates over each ancestor class but uses `get_all_items()` at each level (not just that level's own items). This produces one query per ancestor table, each containing all fields relevant to that hierarchy level.

**Find Queries**: For concrete table entities, `_names_query_f` and `_join_query_f` use a single-entry items map with all fields attributed to the queried class. No parent table joins are generated. The `_class` discriminator column references the entity's own table.

### Trade-offs

| Aspect               | Class Table                              | Concrete Table                                       |
| -------------------- | ---------------------------------------- | ---------------------------------------------------- |
| Storage              | Normalized, no duplication               | Duplicated across hierarchy tables                   |
| Read (single entity) | Joins across N parent tables             | Single table, no joins                               |
| Read (polymorphic)   | Joins + lazy loading for child fields    | Single table with all fields at that level           |
| Write                | One INSERT per class level (narrow rows) | One INSERT per ancestor (wide rows, duplicated data) |
| Count/Aggregation    | Joins required                           | Single table scan                                    |
| Schema changes       | Add column to one table                  | Add column to that table + all descendant tables     |

### Usage

```python
class ConcreteRootEntity(structures.EntityClass):
    inheritance = "concrete_table"

    object_id = dict(id=True, type="integer", generated=True)
    status = dict(type="integer")

class ConcretePerson(ConcreteRootEntity):
    name = dict(type="text")
    age = dict(type="integer")

class ConcreteEmployee(ConcretePerson):
    salary = dict(type="integer")
```

No changes are needed to the entity manager API — `save()`, `update()`, `remove()`, `find()`, `get()`, and `count()` work transparently.

---

**Document Classification**: Internal Technical Documentation
