# SQLite Support in Colony Telemetry Plugin

The Colony Telemetry Plugin now provides **full SQLite support** for file-based database monitoring, diagnostics, and optimization.

## ✅ What Works with SQLite

### **1. Automatic Instrumentation** ✓

All entity manager operations are automatically instrumented:

```python
telemetry_plugin.instrument_entity_manager(entity_manager)
```

Works identically for SQLite, PostgreSQL, and MySQL.

### **2. SQLite BUSY Error Detection** ✓

**OperationalError Detection:**
```python
# Automatically detects SQLite database locked errors
try:
    service.process_order(order_id=1)
except sqlite3.OperationalError as e:
    # "database is locked" automatically detected
    # Span attributes set:
    # - db.lock.contention = True
    # - db.contention.type = "database_locked"
```

**What Gets Tracked:**
- ✅ SQLITE_BUSY errors automatically detected
- ✅ "database is locked" errors caught
- ✅ Span marked with `db.lock.contention = True`
- ✅ Contention type categorized as "database_locked"
- ✅ Metric counter incremented: `db.contention.events`
- ✅ Trace event added: "lock_contention_detected"

### **3. Database Information Monitoring** ✓

**Comprehensive Database Diagnostics:**

```python
detector = telemetry_plugin.get_contention_detector("sqlite")
info = detector.get_database_info(entity_manager)
```

**Returns:**
```python
{
    "file_path": "/path/to/database.db",
    "file_size_bytes": 10485760,
    "file_size_mb": 10.0,
    "page_count": 2560,
    "page_size": 4096,
    "cache_size": 200000,
    "journal_mode": "wal",
    "synchronous": "FULL",
    "busy_timeout_ms": 5000,
    "locking_mode": "NORMAL"
}
```

**PRAGMACommands Used:**
- ✅ `PRAGMA page_count` - Total pages in database
- ✅ `PRAGMA page_size` - Page size in bytes
- ✅ `PRAGMA cache_size` - Cache size in pages
- ✅ `PRAGMA journal_mode` - Journal mode (DELETE, WAL, etc.)
- ✅ `PRAGMA synchronous` - Synchronous mode (OFF, NORMAL, FULL, EXTRA)
- ✅ `PRAGMA busy_timeout` - Lock timeout in milliseconds
- ✅ `PRAGMA locking_mode` - Locking mode (NORMAL, EXCLUSIVE)

### **4. Transaction Statistics** ✓

**Database Statistics:**

```python
stats = detector.get_transaction_stats(entity_manager)
```

**Returns:**
```python
{
    "database_size_bytes": 10485760,
    "database_size_mb": 10.0,
    "page_count": 2560,
    "freelist_count": 128,
    "cache_size": 200000,
    "transaction_level": 0,
    "active_transaction": False
}
```

**Sources:**
- ✅ File system for database size
- ✅ `PRAGMA page_count` for total pages
- ✅ `PRAGMA freelist_count` for free pages (fragmentation indicator)
- ✅ `PRAGMA cache_size` for cache configuration
- ✅ Connection object for transaction state

### **5. Lock Configuration** ✓

**Lock Settings:**

```python
lock_info = detector.get_lock_waits(entity_manager)
```

**Returns:**
```python
[
    {
        "busy_timeout_ms": 5000,
        "locking_mode": "NORMAL"
    }
]
```

### **6. Database Integrity Check** ✓

**PRAGMA integrity_check:**

```python
integrity = detector.get_integrity_check(entity_manager)
```

**Returns:**
```python
{
    "is_ok": True,
    "results": ["ok"],
    "message": "Database integrity OK"
}
```

**Or if issues found:**
```python
{
    "is_ok": False,
    "results": [
        "row 123 missing from index idx_users",
        "btree page 456 has corrupted content"
    ],
    "message": "Database integrity issues found"
}
```

### **7. Database Optimization** ✓

**VACUUM and ANALYZE:**

```python
results = detector.optimize_database(entity_manager)
```

**Returns:**
```python
{
    "size_before_bytes": 10485760,
    "analyze": "completed",
    "vacuum": "completed",
    "size_after_bytes": 8388608,
    "space_saved_bytes": 2097152,
    "space_saved_mb": 2.0
}
```

**Operations:**
- ✅ `ANALYZE` - Updates query planner statistics
- ✅ `VACUUM` - Reclaims space and defragments
- ✅ Before/after size comparison
- ✅ Space savings calculation

**Note:** VACUUM cannot be run inside a transaction.

### **8. No Blocking Queries or Slow Queries** ℹ️

Unlike PostgreSQL and MySQL, SQLite has no:
- ❌ System tables for monitoring connections
- ❌ Processlist to query active queries
- ❌ Built-in slow query log

**Alternative:**
- ✅ Use OpenTelemetry traces for slow query detection
- ✅ Monitor `db.query.duration` metric
- ✅ Check spans with `db.slow_query = true`

## 🎯 OpenTelemetry Metrics for SQLite

All these metrics work automatically with SQLite:

### Histograms
- `db.transaction.duration` - Transaction time (ms)
- `db.query.duration` - Query execution time (ms)
- `db.lock.wait_duration` - Lock acquisition time (ms)

### Counters
- `db.transaction.retries` - Retry count
- `db.contention.events` - Contention events (SQLITE_BUSY, etc.)

### Gauges
- `db.transaction.active` - Active transaction count

## 🔍 Trace Attributes for SQLite

### Transaction Spans
```
db.system = "sqlite"
db.transaction.type = "required"
db.transaction.duration_ms = 125
db.transaction.contention = true  # If SQLITE_BUSY occurred
db.contention.type = "database_locked"  # SQLite-specific
```

### Query Spans
```
db.system = "sqlite"
db.statement = "UPDATE products SET..."
db.slow_query = true
db.lock.contention = true
db.contention.type = "database_locked"
```

## 📊 SQLite Characteristics

### Key Differences from PostgreSQL/MySQL

| Feature | PostgreSQL | MySQL | SQLite |
|---------|-----------|-------|--------|
| Architecture | Client-Server | Client-Server | File-based |
| Locking Granularity | Row-level | Row-level | Database-level |
| Concurrency | High | High | Limited (writers block) |
| System Tables | ✅ pg_stat_activity | ✅ information_schema | ❌ None |
| Monitoring | ✅ Rich | ✅ Rich | ⚠️ Limited |
| Lock Types | Many | Many | Few |
| Blocking Query Detection | ✅ Yes | ✅ Yes | ❌ No |
| Optimization | VACUUM ANALYZE | OPTIMIZE TABLE | VACUUM ANALYZE |

### What This Means for Monitoring

**Contention Detection:**
- PostgreSQL/MySQL: Query system tables for blocking queries
- SQLite: Detect SQLITE_BUSY errors via exception handling

**Slow Queries:**
- PostgreSQL/MySQL: Query processlist/pg_stat_activity
- SQLite: Use OpenTelemetry traces (no system tables)

**Lock Monitoring:**
- PostgreSQL/MySQL: Real-time lock wait information
- SQLite: Lock configuration only (no active lock info)

## 🚀 Quick Start (SQLite)

```python
# 1. Load plugins
telemetry_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.telemetry")
entity_manager_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.data.entity.manager")

# 2. Create SQLite entity manager
entity_manager = entity_manager_plugin.load_entity_manager_properties("sqlite", {
    "id": "my_db",
    "file_path": "/path/to/database.db",
    "cache_size": 200000,
    "synchronous": 2
})

# 3. Instrument it
telemetry_plugin.instrument_entity_manager(entity_manager)

# 4. Get SQLite detector
detector = telemetry_plugin.get_contention_detector("sqlite")

# 5. Monitor database
info = detector.get_database_info(entity_manager)
print(f"Database: {info['file_path']}")
print(f"Size: {info['file_size_mb']} MB")
print(f"Journal mode: {info['journal_mode']}")
```

## 🔧 SQLite-Specific Configuration

### Recommended Settings for Better Concurrency

```python
# Enable WAL mode (Write-Ahead Logging)
cursor = entity_manager.execute_query("PRAGMA journal_mode=WAL")

# Benefits:
# - Readers don't block writers
# - Writers don't block readers
# - Better concurrency for multi-threaded apps

# Set busy timeout (wait for locks)
cursor = entity_manager.execute_query("PRAGMA busy_timeout=5000")

# Benefits:
# - Waits up to 5 seconds instead of failing immediately
# - Reduces SQLITE_BUSY errors
# - Better for concurrent access

# Increase cache size
cursor = entity_manager.execute_query("PRAGMA cache_size=-64000")

# Benefits:
# - 64 MB cache (negative = kilobytes)
# - Reduces disk I/O
# - Faster query execution
```

### Synchronous Modes

```python
# PRAGMA synchronous settings:
# 0 = OFF    - Fastest, data loss risk
# 1 = NORMAL - Good balance (recommended)
# 2 = FULL   - Safest, slower
# 3 = EXTRA  - Paranoid mode

# For development/testing:
PRAGMA synchronous=NORMAL

# For production (critical data):
PRAGMA synchronous=FULL
```

## 📈 Example Output (SQLite)

### Console Output
```
=== SQLite Database Monitoring ===

=== Database Information ===
File path: /path/to/database.db
File size: 10.5 MB
Page count: 2560
Page size: 4096 bytes
Cache size: 200000 pages
Journal mode: wal
Synchronous mode: FULL
Busy timeout: 5000 ms
Locking mode: NORMAL

=== Lock Configuration ===
Busy timeout: 5000 ms
Locking mode: NORMAL

=== Transaction Statistics ===
Database size: 10.5 MB
Page count: 2560
Freelist count: 128
Cache size: 200000
Transaction level: 0
Active transaction: False

=== Integrity Check ===
✓ Database integrity OK
```

### Jaeger Traces
```
Span: db.transaction.process_order
  Attributes:
    db.system: sqlite
    db.lock.contention: true
    db.contention.type: database_locked
    db.transaction.duration_ms: 125
  Events:
    - lock_contention_detected
    - transaction.rolled_back
```

## 🎨 Best Practices

### 1. Enable WAL Mode
```python
# Do this once when creating/initializing database
PRAGMA journal_mode=WAL
```

### 2. Set Reasonable Busy Timeout
```python
# Wait 5 seconds before returning SQLITE_BUSY
PRAGMA busy_timeout=5000
```

### 3. Keep Transactions Short
```python
# Bad: Long-running transaction
@decorators.transaction()
def slow_operation():
    # ... lots of work ...
    # Holds database lock for long time

# Good: Short transaction
@decorators.transaction()
def quick_operation():
    # ... minimal work ...
    # Release lock quickly
```

### 4. Batch Writes
```python
# Bad: Many small transactions
for item in items:
    @transaction
    def update_one():
        item.update()

# Good: One transaction for all
@transaction
def update_all():
    for item in items:
        item.update()
```

### 5. Regular Maintenance
```python
# Run periodically (e.g., weekly)
results = detector.optimize_database(entity_manager)

# Benefits:
# - Reclaims space from deleted records
# - Updates query planner statistics
# - Reduces fragmentation
```

## 📚 Additional Resources

- [example_sqlite.py](example_sqlite.py) - Complete SQLite examples
- [README.md](README.md) - Full documentation
- [QUICK_START.md](QUICK_START.md) - 5-minute setup guide

## ✅ Summary

**SQLite support is complete!**

| Feature | PostgreSQL | MySQL | SQLite |
|---------|-----------|-------|--------|
| Automatic Instrumentation | ✅ | ✅ | ✅ |
| Transaction Tracing | ✅ | ✅ | ✅ |
| Query Monitoring | ✅ | ✅ | ✅ |
| Lock Detection | ✅ | ✅ | ✅ |
| Error Detection | ✅ | ✅ | ✅ |
| Database Info | ✅ | ✅ | ✅ |
| Transaction Stats | ✅ | ✅ | ✅ |
| Integrity Check | ✅ | ✅ | ✅ |
| Optimization | ✅ | ✅ | ✅ |
| OpenTelemetry Metrics | ✅ | ✅ | ✅ |
| OpenTelemetry Traces | ✅ | ✅ | ✅ |

**All three major databases fully supported! 🎉**
