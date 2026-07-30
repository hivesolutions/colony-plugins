# COP-002: Hi-Lo ID Generation Strategy

## Document Information

| Field               | Value                                          |
| ------------------- | ---------------------------------------------- |
| **Document Number** | COP-002                                        |
| **Date**            | 2026-07-15                                     |
| **Author**          | João Magalhães <joamag@hive.pt>                |
| **Subject**         | Hi-Lo ID Generation Strategy for Entity Fields |
| **Status**          | Implemented                                    |
| **Version**         | 1.0                                            |

## Description

### Problem

The entity manager generates identifier values for `generated` fields using the `table` strategy by default. Every single ID generation performs a full round trip to the data source: the generator table row is locked, the current `next_id` value is selected and an update (or insert) is executed. This means that saving N entities implies N generator lock/select/update cycles, which becomes a significant bottleneck for insert-heavy workloads and a source of row lock contention when multiple processes or threads generate IDs for the same field concurrently.

### Solution

A new Hi-Lo generator strategy (`generator_type="hilo"`) pre-allocates pools (ranges) of IDs from the generator table and serves individual IDs from process memory. The data source is only accessed when a pool is exhausted, reducing the number of generator queries by a factor of the pool size.

| Component               | Role                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| `_generate_hilo()`      | Generator strategy entry point, resolves field name and pool size and sets the entity value |
| `_hilo_grab_id()`       | Serves the next ID from the in-memory pool, allocating a new pool when exhausted            |
| `_hilo_allocate_pool()` | Reserves a new range in the generator table using a single atomic increment                 |
| `_hilo_discard_pool()`  | Invalidates the pool of a field (used on transaction rollback)                              |
| `_reset_hilo()`         | Clears all pools (used when the data source is destroyed)                                   |

The pool allocation reuses the exact same generator table infrastructure as the `table` strategy: `increment_id()` was generalized with an `increment` parameter (default `1`) so that a pool of size P is reserved with a single locked select plus update, incrementing `next_id` by P instead of 1. The allocated range becomes `[next_id - P, next_id - 1]`.

### Compatibility with the Table Strategy

The generator table stores `next_id` as "the next value to be handed out" for both strategies. Because the Hi-Lo allocation preserves this invariant, a field may be migrated between `table` and `hilo` strategies (in either direction) without ID collisions, and multiple processes using different strategies for the same field remain consistent.

### Concurrency and Transactions

Pool state is kept per entity manager instance in `_hilo_pools` and guarded by a local `threading.Lock` (`_hilo_lock`), so ID consumption is thread-safe and does not involve any database locking. Database locking only occurs during pool allocation, using the same generator table row lock as the `table` strategy.

Because the pool reservation (generator update) runs inside the caller's transaction, a rollback would undo the reservation while the in-memory pool remained valid, allowing a future allocation to hand out the same range twice. To prevent duplicated identifiers, the allocation registers an `after_rollback` callback that discards the field's pool when the allocating transaction is rolled back. Discarded ranges are simply re-allocated on the next generation request.

Pools are also discarded when the data source is destroyed (`destroy()`), keeping the in-memory state consistent with the (removed) generator table.

### Trade-offs

- **Gaps in the sequence**: IDs remaining in a pool are lost when the process terminates, the pool is discarded on rollback or the data source is re-created. Hi-Lo guarantees uniqueness, not density, and should not be used when a gapless sequence is required (eg: legal document numbering).
- **Ordering across instances**: two entity manager instances hold disjoint pools, so IDs are not globally monotonic with respect to creation time.
- **Pool size tuning**: larger pools mean fewer database accesses but larger potential gaps. The default (`HILO_POOL_SIZE = 100`) is a balanced choice for most workloads.

## Usage

The strategy is enabled per field via the `generator_type` attribute, with optional per-field pool size and generator field name customization:

```python
class Ticket(RootEntity):

    ticket_id = dict(
        type="integer",
        generated=True,
        generator_type="hilo",
        generator_field_name="ticket_ticket_id",
        generator_pool_size=10,
    )
```

| Attribute              | Default                      | Purpose                                          |
| ---------------------- | ---------------------------- | ------------------------------------------------ |
| `generator_type`       | `"table"`                    | Set to `"hilo"` to enable the Hi-Lo strategy     |
| `generator_pool_size`  | `HILO_POOL_SIZE` (100)       | Number of IDs reserved per database access       |
| `generator_field_name` | `<table name>_<field name>`  | Name of the counter row in the generator table   |

## Performance

Benchmarks were run against the real `EntityManager` + `SQLiteEngine` stack (Python 3.9, macOS, file-based SQLite, 5 runs per scenario, median values). Note that SQLite is an in-process engine where a query is at its cheapest, so the wall-clock gains represent a lower bound: on networked engines (MySQL, PostgreSQL) every generator query saved is a full network round trip plus row lock window.

### Raw ID Generation (20000 IDs, single transaction)

| Strategy          | Throughput (IDs/s) | Generator Queries | Speedup |
| ----------------- | ------------------ | ----------------- | ------- |
| Table             | ~86000             | 40000             | 1x      |
| Hi-Lo (pool 100)  | ~2758000           | 400               | ~32x    |

### Pool Size Sensitivity (10000 IDs)

| Strategy           | Throughput (IDs/s) | Generator Queries | Speedup |
| ------------------ | ------------------ | ----------------- | ------- |
| Table              | ~82000             | 20000             | 1x      |
| Hi-Lo (pool 10)    | ~599000            | 2000              | ~7x     |
| Hi-Lo (pool 100)   | ~2790000           | 200               | ~34x    |
| Hi-Lo (pool 1000)  | ~4256000           | 20                | ~52x    |

### End-to-End Entity Saves

| Scenario                            | Table (saves/s) | Hi-Lo pool 100 (saves/s) | Total Queries (table vs hilo) | Gain  |
| ----------------------------------- | --------------- | ------------------------ | ----------------------------- | ----- |
| 5000 saves, single transaction      | ~19300          | ~26400                   | 20000 vs 10100                | +37%  |
| 1000 saves, transaction per save    | ~2700           | ~3200                    | 4000 vs 2020                  | +20%  |

The end-to-end save scenarios show that the Hi-Lo strategy roughly halves the total number of queries per save (the entity insert dominates the remainder), with the raw generation scenarios demonstrating the isolated generator improvement that scales with pool size.

## References

- Implementation: `data/src/entity_manager/system.py` (`_generate_hilo`, `_hilo_grab_id`, `_hilo_allocate_pool`, `_hilo_discard_pool`, `_reset_hilo`)
- Tests: `data/src/entity_manager/test.py` and the `Ticket` mock entity in `data/src/entity_manager/mocks.py`
- Pattern: [Hi/Lo algorithm](https://en.wikipedia.org/wiki/Hi/Lo_algorithm), as popularized by Hibernate's `hilo` generator

---

**Document Classification**: Internal Technical Documentation
