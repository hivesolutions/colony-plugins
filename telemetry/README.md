# Telemetry Plugin for Colony

OpenTelemetry instrumentation for the Colony entity manager to detect database transaction contention and performance issues.

## Features

- **Automatic Instrumentation**: Non-intrusive monitoring of entity manager operations
- **Transaction Tracing**: Distributed tracing for database transactions
- **Performance Metrics**: Track query duration, lock waits, and transaction stats
- **Contention Detection**: Identify blocking queries, deadlocks, and serialization failures
- **Database-Specific Monitoring**: Specialized detectors for PostgreSQL and MySQL

## Installation

### Dependencies

```bash
pip install opentelemetry-api opentelemetry-sdk
```

For OTLP export (recommended):

```bash
pip install opentelemetry-exporter-otlp
```

## Configuration

### Environment Variables

```bash
# Enable OpenTelemetry (optional, auto-configured)
export OTEL_SERVICE_NAME="colony-entity-manager"

# Configure OTLP endpoint (Jaeger, Tempo, etc.)
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"

# Use console exporter for testing
export OTEL_USE_CONSOLE=true

# Slow query threshold in milliseconds
export SLOW_QUERY_TIME=25
```

## Usage

### Basic Instrumentation

```python
# Load the telemetry plugin
telemetry_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.telemetry")

# Load and instrument your entity manager
entity_manager_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.data.entity.manager")
entity_manager = entity_manager_plugin.load_entity_manager_properties("pgsql", {
    "id": "my_database",
    "entities_list": [Person, Address, Order]
})

# Instrument the entity manager
telemetry_plugin.instrument_entity_manager(entity_manager)
```

### Using Instrumented Decorators

```python
from telemetry import decorators

class MyService:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager

    @decorators.transaction()
    def create_user(self, name, email):
        """
        This transaction will be automatically traced with OpenTelemetry.
        """
        user = Person()
        user.name = name
        user.email = email
        self.entity_manager.save(user)
        return user

    @decorators.monitored_query
    def find_users_by_age(self, min_age):
        """
        Custom queries can also be monitored.
        """
        return self.entity_manager.find(Person, {"age": {"$gte": min_age}})
```

### Contention Detection

```python
# Get a contention detector for your database
detector = telemetry_plugin.get_contention_detector("pgsql")

# Check for blocking queries
blocking_queries = detector.get_blocking_queries(entity_manager)
for block in blocking_queries:
    print(f"PID {block['blocking_pid']} is blocking PID {block['blocked_pid']}")
    print(f"  Blocking query: {block['blocking_statement']}")
    print(f"  Duration: {block['blocking_duration']}")

# Get lock wait information
lock_waits = detector.get_lock_waits(entity_manager)
for wait in lock_waits:
    print(f"Wait event: {wait['wait_event']} ({wait['waiting_count']} waiting)")

# Get transaction statistics
stats = detector.get_transaction_stats(entity_manager)
print(f"Active transactions: {stats['active_transactions']}")
print(f"Longest transaction: {stats['longest_transaction']}")
print(f"Deadlocks: {stats.get('deadlocks', 0)}")

# Get slow queries (PostgreSQL only)
slow_queries = detector.get_slow_queries(entity_manager, duration_threshold="5 seconds")
for query in slow_queries:
    print(f"Slow query (PID {query['pid']}): {query['query']}")
    print(f"  Duration: {query['duration']}")
    print(f"  Wait event: {query['wait_event']}")
```

### Custom Configuration

```python
# Configure telemetry programmatically
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Set up custom tracer provider
tracer_provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(endpoint="http://your-collector:4317")
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Configure the telemetry plugin
telemetry_plugin.configure_telemetry(tracer_provider=tracer_provider)
```

## Metrics Collected

### Histograms

- `db.transaction.duration` - Transaction execution time (ms)
- `db.query.duration` - Query execution time (ms)
- `db.lock.wait_duration` - Lock acquisition time (ms)

### Counters

- `db.transaction.retries` - Transaction retry count
- `db.contention.events` - Contention event count

### Gauges

- `db.transaction.active` - Active transaction count

## Trace Attributes

### Transaction Spans

- `db.system` - Database engine (pgsql, mysql, sqlite)
- `db.transaction.type` - Transaction type
- `db.transaction.duration_ms` - Duration in milliseconds
- `db.transaction.contention` - Contention detected flag
- `db.transaction.retry_count` - Number of retries

### Query Spans

- `db.system` - Database engine
- `db.statement` - SQL query (truncated to 500 chars)
- `db.slow_query` - Slow query flag
- `db.lock.contention` - Lock contention detected flag

### Lock Spans

- `db.system` - Database engine
- `db.entity` - Entity/table name
- `db.lock.type` - Lock type (row/table)

## Events

Spans include these events:

- `transaction.started` - Transaction begin
- `transaction.committed` - Transaction commit
- `transaction.rolled_back` - Transaction rollback
- `contention_detected` - Contention identified
- `lock_contention_detected` - Lock timeout/deadlock
- `slow_query_detected` - Query exceeded threshold

## Visualization

### Recommended Stack

- **Jaeger** or **Tempo** - Distributed tracing backend
- **Prometheus** - Metrics collection
- **Grafana** - Dashboards and alerting

### Sample Prometheus Queries

```promql
# P95 transaction duration by operation
histogram_quantile(0.95,
  rate(db_transaction_duration_bucket[5m])
)

# Transaction retry rate
rate(db_transaction_retries_total[5m])

# Active transaction count
db_transaction_active

# P99 query duration
histogram_quantile(0.99,
  rate(db_query_duration_bucket[5m])
)

# Contention event rate
rate(db_contention_events_total[5m])
```

## Performance Impact

The instrumentation is designed to be lightweight:

- Tracing uses asynchronous batch export
- Metrics are aggregated locally before export
- Minimal overhead on normal operations
- Can be disabled via configuration

## Troubleshooting

### No telemetry data appearing

1. Check OpenTelemetry packages are installed
2. Verify OTLP endpoint is accessible
3. Enable console exporter: `export OTEL_USE_CONSOLE=true`
4. Check Colony plugin logs

### High overhead

1. Reduce trace sampling rate
2. Increase metric export interval
3. Use OTLP instead of console exporter
4. Disable instrumentation for hot paths

## License

Apache License, Version 2.0
