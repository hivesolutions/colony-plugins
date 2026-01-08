# MySQL Support in Colony Telemetry Plugin

The Colony Telemetry Plugin now provides **full MySQL support** for database transaction contention detection and performance monitoring.

## ✅ What Works with MySQL

### 1. **Automatic Instrumentation** ✓

All entity manager operations are automatically instrumented when you call:

```python
telemetry_plugin.instrument_entity_manager(entity_manager)
```

This works identically for MySQL as it does for PostgreSQL.

### 2. **MySQL Deadlock Detection** ✓

**Error Code 1213 Detection:**
```python
# Automatically detects MySQL deadlock errors
try:
    service.transfer_inventory(from_warehouse=1, to_warehouse=2)
except MySQLdb.OperationalError as e:
    # Error code 1213 is automatically detected
    # Span attributes set:
    # - db.lock.contention = True
    # - db.contention.type = "deadlock"
```

**What Gets Tracked:**
- ✅ Deadlock error code (1213) automatically detected
- ✅ Span marked with `db.lock.contention = True`
- ✅ Contention type categorized as "deadlock"
- ✅ Metric counter incremented: `db.contention.events`
- ✅ Trace event added: "lock_contention_detected"

### 3. **InnoDB Lock Wait Monitoring** ✓

**Works with MySQL 5.7 and MySQL 8.0+:**

```python
detector = telemetry_plugin.get_contention_detector("mysql")

# Automatically tries MySQL 8.0+ first, falls back to 5.7
blocking_queries = detector.get_blocking_queries(entity_manager)
```

**Returns:**
```python
[
    {
        "waiting_trx_id": "421405999101856",
        "waiting_thread": 12345,
        "waiting_query": "UPDATE products SET stock = stock - 1 WHERE id = 100",
        "blocking_trx_id": "421405999101632",
        "blocking_thread": 12346,
        "blocking_query": "UPDATE products SET stock = stock + 1 WHERE id = 100",
        "wait_started": "2025-12-22 10:30:15",
        "wait_duration_seconds": 5
    }
]
```

**Implementation:**
- ✅ Tries `sys.innodb_lock_waits` (MySQL 8.0+)
- ✅ Falls back to `information_schema.innodb_lock_waits` (MySQL 5.7)
- ✅ Returns unified data structure for both versions

### 4. **Transaction Statistics** ✓

**InnoDB Transaction Monitoring:**

```python
stats = detector.get_transaction_stats(entity_manager)
```

**Returns:**
```python
{
    "total_transactions": 15,
    "running_transactions": 12,
    "lock_wait_transactions": 3,
    "longest_transaction_seconds": 45,
    "avg_transaction_seconds": 2.5,
    "deadlocks": 7  # Lifetime deadlock count
}
```

**Sources:**
- ✅ `information_schema.innodb_trx` for transaction stats
- ✅ `information_schema.GLOBAL_STATUS` for deadlock count
- ✅ Compatible with MySQL 5.7 and 8.0+

### 5. **Lock Wait Statistics** ✓

**InnoDB Lock Wait Metrics:**

```python
lock_waits = detector.get_lock_waits(entity_manager)
```

**Returns:**
```python
[
    {
        "lock_wait_count": 5,
        "total_wait_seconds": 25,
        "max_wait_seconds": 10
    }
]
```

### 6. **Slow Query Detection** ✓

**From PROCESSLIST:**

```python
slow_queries = detector.get_slow_queries(
    entity_manager,
    duration_threshold_seconds=5
)
```

**Returns:**
```python
[
    {
        "pid": 12345,
        "user": "app_user",
        "host": "192.168.1.100:54321",
        "database": "production_db",
        "command": "Query",
        "duration_seconds": 15,
        "state": "Sending data",
        "query": "SELECT * FROM orders WHERE created_at > ..."
    }
]
```

**Features:**
- ✅ Queries from `information_schema.PROCESSLIST`
- ✅ Excludes Sleep commands
- ✅ Configurable threshold
- ✅ Includes query state and command type

### 7. **Deadlock Information** ✓

**From InnoDB Status:**

```python
deadlock_info = detector.get_deadlock_info(entity_manager)
```

**Returns:**
```python
{
    "has_recent_deadlock": True,
    "deadlock_text": "*** (1) TRANSACTION:\n..."
}
```

**Features:**
- ✅ Parses `SHOW ENGINE INNODB STATUS`
- ✅ Extracts LATEST DETECTED DEADLOCK section
- ✅ Returns first 500 characters of deadlock details

## 🎯 OpenTelemetry Metrics for MySQL

All these metrics work automatically with MySQL:

### Histograms
- `db.transaction.duration` - Transaction time (ms)
- `db.query.duration` - Query execution time (ms)
- `db.lock.wait_duration` - Lock acquisition time (ms)

### Counters
- `db.transaction.retries` - Retry count (incremented on deadlocks)
- `db.contention.events` - Contention events (deadlocks, timeouts, etc.)

### Gauges
- `db.transaction.active` - Active transaction count

## 🔍 Trace Attributes for MySQL

### Transaction Spans
```
db.system = "mysql"
db.transaction.type = "required"
db.transaction.duration_ms = 125
db.transaction.contention = true  # If deadlock occurred
db.contention.type = "deadlock"   # MySQL-specific
```

### Query Spans
```
db.system = "mysql"
db.statement = "UPDATE products SET..."
db.slow_query = true
db.lock.contention = true
db.contention.type = "deadlock"
```

## 📊 MySQL Version Compatibility

| Feature | MySQL 5.7 | MySQL 8.0+ |
|---------|-----------|------------|
| InnoDB Lock Waits | ✅ (`information_schema`) | ✅ (`sys.innodb_lock_waits`) |
| Transaction Stats | ✅ | ✅ |
| Deadlock Count | ✅ | ✅ |
| Slow Queries | ✅ | ✅ |
| Deadlock Info | ✅ | ✅ |
| Error Code Detection | ✅ | ✅ |

## 🚀 Quick Start (MySQL)

```python
# 1. Load plugins
telemetry_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.telemetry")
entity_manager_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.data.entity.manager")

# 2. Create MySQL entity manager
entity_manager = entity_manager_plugin.load_entity_manager_properties("mysql", {
    "id": "my_db",
    "host": "localhost",
    "database": "myapp",
})

# 3. Instrument it
telemetry_plugin.instrument_entity_manager(entity_manager)

# 4. Done! Everything is now monitored
```

## 🔬 MySQL-Specific Error Detection

The instrumentation now detects MySQL-specific errors:

```python
# Error Code 1213 (Deadlock)
except MySQLdb.OperationalError as e:
    if e.args[0] == 1213:
        # Automatically detected and logged
        # - Span: db.contention.type = "deadlock"
        # - Metric: db.contention.events +1
```

**Other MySQL Error Codes Detected:**
- ✅ **1213** - Deadlock found when trying to get lock
- ✅ **1205** - Lock wait timeout exceeded
- ✅ **Generic** - String matching for "lock", "timeout", "deadlock"

## 📈 Example Output (MySQL)

### Console Output
```
=== MySQL Contention Monitoring ===

=== Blocking Queries (InnoDB Lock Waits) ===
Deadlock/Block detected:
  Waiting Transaction: 421405999101856 (Thread: 12345)
  Blocking Transaction: 421405999101632 (Thread: 12346)
  Wait Duration: 5 seconds
  Waiting Query: UPDATE products SET stock = stock - 1 WHERE id = 100...
  Blocking Query: UPDATE products SET stock = stock + 1 WHERE id = 100...

=== InnoDB Transaction Statistics ===
Total transactions: 15
Running transactions: 12
Lock waiting transactions: 3
Longest transaction: 45 seconds
Average transaction duration: 2.50 seconds
Total deadlocks (lifetime): 7

⚠️  ALERT: 7 deadlocks have occurred!
```

### Jaeger Traces
```
Span: db.transaction.transfer_inventory
  ├─ db.lock (Warehouse:1) - 2ms
  ├─ db.lock (Warehouse:2) - 5023ms ⚠️
  │  └─ Event: lock_contention_detected
  │      • error.type: OperationalError
  │      • contention_type: deadlock
  └─ Event: transaction.rolled_back

Attributes:
  db.system: mysql
  db.lock.contention: true
  db.contention.type: deadlock
  db.transaction.duration_ms: 5125
```

## 🎨 Colony-Aligned Implementation

The MySQL support follows the Colony framework patterns:

✅ **Non-Intrusive**: Works with existing MySQL entity managers
✅ **Version Agnostic**: Automatic fallback for MySQL 5.7/8.0+
✅ **Error Handling**: Graceful degradation if queries fail
✅ **Logging**: Uses Colony plugin logging methods
✅ **Configuration**: Uses `colony.conf()` for settings

## 📚 Additional Resources

- [example_mysql.py](example_mysql.py) - Complete MySQL examples
- [README.md](README.md) - Full documentation
- [QUICK_START.md](QUICK_START.md) - 5-minute setup guide

## ✅ Summary

**Everything that works with PostgreSQL now works with MySQL:**

| Feature | PostgreSQL | MySQL |
|---------|------------|-------|
| Automatic Instrumentation | ✅ | ✅ |
| Transaction Tracing | ✅ | ✅ |
| Query Monitoring | ✅ | ✅ |
| Lock Wait Detection | ✅ | ✅ |
| Deadlock Detection | ✅ | ✅ |
| Transaction Stats | ✅ | ✅ |
| Slow Query Detection | ✅ | ✅ |
| Contention Events | ✅ | ✅ |
| OpenTelemetry Metrics | ✅ | ✅ |
| OpenTelemetry Traces | ✅ | ✅ |

**MySQL now fully supported! 🎉**
