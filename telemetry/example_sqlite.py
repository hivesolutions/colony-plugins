#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
SQLite-specific example usage of the Colony Telemetry Plugin.
Demonstrates SQLite database monitoring, PRAGMA diagnostics, and optimization.
"""

import colony
from telemetry import decorators


def setup_sqlite_telemetry(plugin_manager):
    """
    Sets up the telemetry plugin for SQLite entity manager.

    :type plugin_manager: PluginManager
    :param plugin_manager: The Colony plugin manager instance.
    :rtype: tuple
    :return: Tuple of (entity_manager, telemetry_plugin).
    """

    # Load the telemetry plugin
    telemetry_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.telemetry")

    # Load the entity manager plugin
    entity_manager_plugin = plugin_manager.get_plugin(
        "pt.hive.colony.plugins.data.entity.manager"
    )

    # Create SQLite entity manager
    entity_manager = entity_manager_plugin.load_entity_manager_properties("sqlite", {
        "id": "sqlite_database",
        "file_path": "/tmp/example.db",
        "cache_size": 200000,
        "synchronous": 2  # FULL mode
    })

    # Instrument the entity manager for telemetry
    telemetry_plugin.instrument_entity_manager(entity_manager)

    print("SQLite entity manager instrumented successfully")

    return entity_manager, telemetry_plugin


def example_sqlite_lock_handling(entity_manager):
    """
    Example demonstrating SQLite lock detection and handling.
    """

    class OrderService:
        def __init__(self, entity_manager):
            self.entity_manager = entity_manager

        @decorators.transaction()
        def process_order(self, order_id):
            """
            Processes an order.
            If the database is locked, OpenTelemetry will detect it.
            """

            # Simulate some database work
            order = self.entity_manager.get(Order, order_id)
            order.status = "processed"
            self.entity_manager.update(order)

            print(f"Processed order {order_id}")

    service = OrderService(entity_manager)

    try:
        # This will be traced, and if a SQLITE_BUSY error occurs,
        # it will be automatically detected and logged
        service.process_order(order_id=1)
    except Exception as e:
        print(f"Error during order processing: {e}")
        # The telemetry system has already logged this with:
        # - db.lock.contention = True
        # - db.contention.type = "database_locked"
        # - Span event: "lock_contention_detected"


def example_sqlite_monitoring(entity_manager, telemetry_plugin):
    """
    Example of SQLite-specific monitoring.
    """

    # Get the SQLite contention detector
    detector = telemetry_plugin.get_contention_detector("sqlite")

    print("\n" + "=" * 60)
    print("SQLite Database Monitoring")
    print("=" * 60)

    # 1. Get database information
    print("\n=== Database Information ===")
    info = detector.get_database_info(entity_manager)

    print(f"File path: {info.get('file_path', 'N/A')}")
    print(f"File size: {info.get('file_size_mb', 0)} MB")
    print(f"Page count: {info.get('page_count', 0)}")
    print(f"Page size: {info.get('page_size', 0)} bytes")
    print(f"Cache size: {info.get('cache_size', 0)} pages")
    print(f"Journal mode: {info.get('journal_mode', 'N/A')}")
    print(f"Synchronous mode: {info.get('synchronous', 'N/A')}")
    print(f"Busy timeout: {info.get('busy_timeout_ms', 0)} ms")
    print(f"Locking mode: {info.get('locking_mode', 'N/A')}")

    # 2. Get lock configuration
    print("\n=== Lock Configuration ===")
    lock_info = detector.get_lock_waits(entity_manager)

    if lock_info:
        for info in lock_info:
            print(f"Busy timeout: {info.get('busy_timeout_ms', 0)} ms")
            print(f"Locking mode: {info.get('locking_mode', 'N/A')}")
    else:
        print("No lock configuration available")

    # 3. Get transaction statistics
    print("\n=== Transaction Statistics ===")
    stats = detector.get_transaction_stats(entity_manager)

    print(f"Database size: {stats.get('database_size_mb', 0)} MB")
    print(f"Page count: {stats.get('page_count', 0)}")
    print(f"Freelist count: {stats.get('freelist_count', 0)}")
    print(f"Cache size: {stats.get('cache_size', 0)}")
    print(f"Transaction level: {stats.get('transaction_level', 0)}")
    print(f"Active transaction: {stats.get('active_transaction', False)}")

    # 4. Run integrity check
    print("\n=== Integrity Check ===")
    integrity = detector.get_integrity_check(entity_manager)

    if integrity.get('is_ok'):
        print("✓ Database integrity OK")
    else:
        print("⚠️  Database integrity issues detected:")
        for result in integrity.get('results', []):
            print(f"  - {result}")

    # 5. Note about slow queries
    print("\n=== Slow Query Detection ===")
    print("SQLite doesn't have a processlist.")
    print("Use OpenTelemetry traces to detect slow queries:")
    print("- Check spans with db.slow_query = true")
    print("- Monitor db.query.duration metric")


def example_sqlite_optimization(entity_manager, telemetry_plugin):
    """
    Example of SQLite database optimization.
    """

    detector = telemetry_plugin.get_contention_detector("sqlite")

    print("\n" + "=" * 60)
    print("SQLite Database Optimization")
    print("=" * 60)

    # Run VACUUM and ANALYZE
    print("\nRunning VACUUM and ANALYZE...")
    results = detector.optimize_database(entity_manager)

    print(f"\nOptimization Results:")
    print(f"  ANALYZE: {results.get('analyze', 'N/A')}")
    print(f"  VACUUM: {results.get('vacuum', 'N/A')}")

    if 'size_before_bytes' in results:
        print(f"  Size before: {round(results['size_before_bytes'] / (1024 * 1024), 2)} MB")

    if 'size_after_bytes' in results:
        print(f"  Size after: {round(results['size_after_bytes'] / (1024 * 1024), 2)} MB")

    if 'space_saved_mb' in results:
        print(f"  Space saved: {results['space_saved_mb']} MB")


def example_sqlite_best_practices():
    """
    Example of SQLite-specific best practices for avoiding contention.
    """

    print("\n" + "=" * 60)
    print("SQLite Best Practices for Avoiding Contention")
    print("=" * 60)

    print("""
1. WAL Mode (Write-Ahead Logging):
   - Use WAL mode for better concurrency
   - PRAGMA journal_mode=WAL
   - Allows readers and writers simultaneously

2. Busy Timeout:
   - Set a reasonable busy timeout
   - PRAGMA busy_timeout=5000 (5 seconds)
   - Reduces SQLITE_BUSY errors

3. Keep Transactions Short:
   - Minimize time between BEGIN and COMMIT
   - SQLite locks the entire database file
   - Long transactions block other writers

4. Batch Writes:
   - Group multiple writes in single transaction
   - Reduces lock/unlock overhead
   - Improves write throughput

5. Appropriate Synchronous Mode:
   - NORMAL for most cases (balance speed/safety)
   - FULL for critical data (slower, safer)
   - OFF only for temporary/cache databases

6. Cache Size:
   - Larger cache reduces I/O
   - PRAGMA cache_size=-64000 (64MB)
   - Negative value means kilobytes

7. Regular VACUUM:
   - Reclaims space from deleted records
   - Run periodically on maintenance window
   - Cannot run inside transaction

8. Use Indexes:
   - Proper indexes reduce query time
   - Shorter queries = less lock time
   - Run ANALYZE after schema changes

Example Monitored Code:
    """)

    print("""
from telemetry import decorators

class DataService:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager

    @decorators.transaction()
    def batch_update_users(self, user_ids, new_status):
        '''
        Updates multiple users in a single transaction.
        Telemetry will track:
        - Transaction duration
        - Any SQLITE_BUSY errors
        - Database lock contentions
        '''

        for user_id in user_ids:
            user = self.entity_manager.get(User, user_id)
            user.status = new_status
            self.entity_manager.update(user)

        # All updates committed together
        # Reduces lock/unlock overhead
    """)


def example_sqlite_wal_mode(entity_manager):
    """
    Example of configuring WAL mode for better concurrency.
    """

    print("\n" + "=" * 60)
    print("Configuring SQLite WAL Mode")
    print("=" * 60)

    try:
        # Enable WAL mode
        cursor = entity_manager.execute_query("PRAGMA journal_mode=WAL")
        result = cursor.fetchone()
        cursor.close()

        print(f"\n✓ Journal mode set to: {result[0]}")
        print("  Benefits:")
        print("  - Readers don't block writers")
        print("  - Writers don't block readers")
        print("  - Better concurrency for multi-threaded apps")

        # Set busy timeout
        cursor = entity_manager.execute_query("PRAGMA busy_timeout=5000")
        cursor.close()

        print("\n✓ Busy timeout set to: 5000 ms")
        print("  SQLite will wait up to 5 seconds before returning SQLITE_BUSY")

        # Increase cache size
        cursor = entity_manager.execute_query("PRAGMA cache_size=-64000")
        cursor.close()

        print("\n✓ Cache size set to: 64 MB")
        print("  Larger cache reduces disk I/O")

    except Exception as e:
        print(f"\nError configuring SQLite: {e}")


def monitor_sqlite_periodically(entity_manager, telemetry_plugin, interval=60):
    """
    Sets up periodic SQLite monitoring for production environments.

    :type entity_manager: EntityManager
    :param entity_manager: The SQLite entity manager.
    :type telemetry_plugin: TelemetryPlugin
    :param telemetry_plugin: The telemetry plugin instance.
    :type interval: int
    :param interval: Check interval in seconds.
    """

    import time
    import threading

    detector = telemetry_plugin.get_contention_detector("sqlite")

    def monitor():
        print(f"\nStarted SQLite monitoring (checking every {interval}s)")

        while True:
            try:
                # Check database size and stats
                stats = detector.get_transaction_stats(entity_manager)

                # Alert on large database
                db_size_mb = stats.get('database_size_mb', 0)
                if db_size_mb > 1000:  # 1GB
                    print(f"\n[WARNING] Database size: {db_size_mb} MB")

                # Alert on high freelist (fragmentation)
                freelist = stats.get('freelist_count', 0)
                page_count = stats.get('page_count', 1)
                if freelist > page_count * 0.1:  # >10% free pages
                    print(f"\n[WARNING] High fragmentation: {freelist} free pages")
                    print("  Consider running VACUUM")

                # Check integrity periodically (e.g., daily)
                import datetime
                if datetime.datetime.now().hour == 3:  # 3 AM
                    integrity = detector.get_integrity_check(entity_manager)
                    if not integrity.get('is_ok'):
                        print("\n[ALERT] Database integrity check failed!")

                time.sleep(interval)

            except Exception as e:
                print(f"Error in monitoring thread: {e}")
                time.sleep(interval)

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()


def main():
    """
    Main example function for SQLite telemetry.
    """

    print("Colony Telemetry Plugin - SQLite Examples")
    print("=" * 60)

    print("\nSQLite-Specific Features:")
    print("- Database file monitoring")
    print("- PRAGMA-based diagnostics")
    print("- SQLITE_BUSY error detection")
    print("- Database integrity checks")
    print("- VACUUM and ANALYZE optimization")
    print("- WAL mode configuration")

    print("\n" + "=" * 60)
    print("\nTo use with your SQLite application:")
    print("1. Load and instrument your entity manager")
    print("2. Use @decorators.transaction() on your methods")
    print("3. Monitor with the SQLite detector")
    print("4. Enable WAL mode for better concurrency")
    print("5. Run periodic VACUUM for maintenance")

    print("\n" + "=" * 60)
    print("\nKey Differences from PostgreSQL/MySQL:")
    print("- File-based, not client-server")
    print("- Database-level locks (not row-level)")
    print("- No system tables for monitoring")
    print("- PRAGMA statements for diagnostics")
    print("- VACUUM needed for space reclamation")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
