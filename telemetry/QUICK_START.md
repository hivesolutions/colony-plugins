# Quick Start Guide - OpenTelemetry for Colony Entity Manager

This guide will help you quickly set up OpenTelemetry instrumentation for your Colony application to detect database transaction contention and performance issues.

## Installation

### 1. Install OpenTelemetry Packages

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

### 2. Set Up a Collector (Optional but Recommended)

For production use, run an OpenTelemetry Collector with Jaeger or Tempo:

```bash
# Using Docker
docker run -d --name jaeger \
  -p 4317:4317 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

Access Jaeger UI at: http://localhost:16686

## Basic Configuration

### Environment Variables

```bash
# Configure the OTLP endpoint (Jaeger, Tempo, etc.)
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"

# Set service name for identification
export OTEL_SERVICE_NAME="my-colony-app"

# Optional: Enable console output for debugging
export OTEL_USE_CONSOLE=true

# Optional: Set slow query threshold (default: 25ms)
export SLOW_QUERY_TIME=50
```

## Minimal Code Example

```python
import colony

# Initialize Colony and load plugins
plugin_manager = colony.PluginManager()

# Load the telemetry plugin
telemetry_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.telemetry")

# Load your entity manager
entity_manager_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.data.entity.manager")
entity_manager = entity_manager_plugin.load_entity_manager_properties("pgsql", {
    "id": "my_db",
    "host": "localhost",
    "database": "myapp",
})

# Instrument the entity manager (THIS IS THE KEY STEP!)
telemetry_plugin.instrument_entity_manager(entity_manager)

# That's it! All operations are now instrumented
```

## What Gets Monitored Automatically

Once instrumented, the following are automatically tracked:

1. **All Transactions** - Duration, commits, rollbacks
2. **All Database Queries** - Execution time, SQL statements
3. **All Lock Operations** - Lock acquisition time
4. **Contention Events** - Deadlocks, timeouts, serialization failures
5. **Slow Queries** - Queries exceeding the threshold

## Viewing Traces and Metrics

### Jaeger UI

1. Open http://localhost:16686
2. Select service: `my-colony-app` (or your OTEL_SERVICE_NAME)
3. Click "Find Traces"
4. Look for spans like:
   - `db.transaction.*` - Transaction operations
   - `db.query` - Query executions
   - `db.lock` - Lock operations

### What to Look For

**High Contention:**
- Long `db.lock.wait_duration` spans
- Spans with `db.lock.contention=true` attribute
- Multiple `db.transaction.rollback` events

**Performance Issues:**
- Spans with `db.slow_query=true` attribute
- High P95/P99 transaction durations
- Long query execution times in `db.query` spans

## Detecting Contention Programmatically

```python
# Get a contention detector
detector = telemetry_plugin.get_contention_detector("pgsql")

# Check for blocking queries
blocking = detector.get_blocking_queries(entity_manager)
if blocking:
    print(f"⚠️  {len(blocking)} blocking queries detected!")
    for block in blocking:
        print(f"  PID {block['blocking_pid']} blocking PID {block['blocked_pid']}")

# Check transaction stats
stats = detector.get_transaction_stats(entity_manager)
print(f"Active transactions: {stats['active_transactions']}")
print(f"Deadlocks: {stats.get('deadlocks', 0)}")
```

## Common Issues and Solutions

### Issue: No telemetry data appearing

**Solutions:**
1. Verify OpenTelemetry packages are installed: `pip list | grep opentelemetry`
2. Check OTLP endpoint is accessible: `telnet localhost 4317`
3. Enable console export for debugging: `export OTEL_USE_CONSOLE=true`
4. Check Colony logs for telemetry plugin messages

### Issue: Too much overhead

**Solutions:**
1. Increase metric export interval (default: 30s)
2. Use sampling for traces (configure in TracerProvider)
3. Disable instrumentation for specific operations

### Issue: Missing transaction context

**Solutions:**
1. Ensure entity manager is instrumented BEFORE use
2. Verify the entity manager reference is the instrumented instance
3. Check that decorators are applied correctly

## Production Recommendations

1. **Use OTLP Exporter** - Console exporter is for debugging only
2. **Enable Sampling** - Sample traces in high-traffic scenarios
3. **Monitor Overhead** - Track instrumentation impact with benchmarks
4. **Set Alerts** - Configure alerts for high contention and slow queries
5. **Regular Reviews** - Periodically review traces to identify bottlenecks

## Example Alert Rules (Prometheus)

```yaml
groups:
  - name: database_alerts
    rules:
      - alert: HighDatabaseContention
        expr: rate(db_contention_events_total[5m]) > 10
        annotations:
          summary: "High database contention detected"

      - alert: SlowDatabaseQueries
        expr: histogram_quantile(0.99, rate(db_query_duration_bucket[5m])) > 1000
        annotations:
          summary: "Database queries are slow (P99 > 1s)"
```

## Next Steps

- Read the [full README](README.md) for advanced features
- Review [example_usage.py](example_usage.py) for more examples
- Configure custom metrics and spans for your use case
- Set up dashboards in Grafana for visualization

## Getting Help

- Check Colony plugin logs for errors
- Verify OpenTelemetry configuration with console exporter
- Review Jaeger UI for trace details
- Consult OpenTelemetry documentation: https://opentelemetry.io/docs/
