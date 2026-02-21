#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
MySQL-specific example usage of the Colony Telemetry Plugin.
Demonstrates MySQL deadlock detection, InnoDB monitoring, and contention analysis.
"""

import colony
from telemetry import decorators


def setup_mysql_telemetry(plugin_manager):
    """
    Sets up the telemetry plugin for MySQL entity manager.

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

    # Create MySQL entity manager
    entity_manager = entity_manager_plugin.load_entity_manager_properties("mysql", {
        "id": "mysql_database",
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "example_db",
        "isolation": "read committed",
    })

    # Instrument the entity manager for telemetry
    telemetry_plugin.instrument_entity_manager(entity_manager)

    print("MySQL entity manager instrumented successfully")

    return entity_manager, telemetry_plugin


def example_mysql_deadlock_handling(entity_manager):
    """
    Example demonstrating MySQL deadlock detection and handling.
    """

    class OrderService:
        def __init__(self, entity_manager):
            self.entity_manager = entity_manager

        @decorators.transaction()
        def transfer_inventory(self, from_warehouse, to_warehouse, product_id, quantity):
            """
            Transfers inventory between warehouses.
            This operation can cause deadlocks if multiple transfers happen concurrently.
            OpenTelemetry will automatically detect and track these deadlocks.
            """

            # Lock source warehouse (this order of locking can cause deadlocks)
            self.entity_manager.lock(Warehouse, from_warehouse)

            # Simulate some processing
            import time
            time.sleep(0.1)

            # Lock destination warehouse
            self.entity_manager.lock(Warehouse, to_warehouse)

            # Perform the transfer
            # ... transfer logic here ...

            print(f"Transferred {quantity} of product {product_id} from {from_warehouse} to {to_warehouse}")

    service = OrderService(entity_manager)

    try:
        # This will be traced, and if a deadlock occurs (error 1213),
        # it will be automatically detected and logged
        service.transfer_inventory(
            from_warehouse=1,
            to_warehouse=2,
            product_id=100,
            quantity=50
        )
    except Exception as e:
        print(f"Error during transfer (may be deadlock): {e}")
        # The telemetry system has already logged this with:
        # - db.lock.contention = True
        # - db.contention.type = "deadlock"
        # - Span event: "lock_contention_detected"


def example_mysql_contention_monitoring(entity_manager, telemetry_plugin):
    """
    Example of MySQL-specific contention monitoring.
    """

    # Get the MySQL contention detector
    detector = telemetry_plugin.get_contention_detector("mysql")

    print("\n" + "=" * 60)
    print("MySQL Contention Monitoring")
    print("=" * 60)

    # 1. Check for blocking queries (works with MySQL 5.7 and 8.0+)
    print("\n=== Blocking Queries (InnoDB Lock Waits) ===")
    blocking_queries = detector.get_blocking_queries(entity_manager)

    if blocking_queries:
        for block in blocking_queries:
            print(f"\nDeadlock/Block detected:")
            print(f"  Waiting Transaction: {block['waiting_trx_id']} (Thread: {block['waiting_thread']})")
            print(f"  Blocking Transaction: {block['blocking_trx_id']} (Thread: {block['blocking_thread']})")
            print(f"  Wait Duration: {block['wait_duration_seconds']} seconds")
            print(f"  Waiting Query: {block['waiting_query'][:100] if block['waiting_query'] else 'N/A'}...")
            print(f"  Blocking Query: {block['blocking_query'][:100] if block['blocking_query'] else 'N/A'}...")
    else:
        print("✓ No blocking queries detected")

    # 2. Check InnoDB lock waits
    print("\n=== InnoDB Lock Waits ===")
    lock_waits = detector.get_lock_waits(entity_manager)

    if lock_waits:
        for wait in lock_waits:
            print(f"Lock wait count: {wait['lock_wait_count']}")
            print(f"Total wait time: {wait['total_wait_seconds']} seconds")
            print(f"Max wait time: {wait['max_wait_seconds']} seconds")
    else:
        print("✓ No lock waits detected")

    # 3. Get transaction statistics
    print("\n=== InnoDB Transaction Statistics ===")
    stats = detector.get_transaction_stats(entity_manager)

    print(f"Total transactions: {stats.get('total_transactions', 0)}")
    print(f"Running transactions: {stats.get('running_transactions', 0)}")
    print(f"Lock waiting transactions: {stats.get('lock_wait_transactions', 0)}")
    print(f"Longest transaction: {stats.get('longest_transaction_seconds', 0)} seconds")
    print(f"Average transaction duration: {stats.get('avg_transaction_seconds', 0):.2f} seconds")
    print(f"Total deadlocks (lifetime): {stats.get('deadlocks', 0)}")

    # Alert on concerning metrics
    if stats.get('lock_wait_transactions', 0) > 5:
        print("\n⚠️  WARNING: High number of transactions waiting for locks!")

    if stats.get('deadlocks', 0) > 0:
        print(f"\n⚠️  ALERT: {stats.get('deadlocks')} deadlocks have occurred!")

    # 4. Check for slow queries in processlist
    print("\n=== Slow Queries (from PROCESSLIST) ===")
    slow_queries = detector.get_slow_queries(entity_manager, duration_threshold_seconds=2)

    if slow_queries:
        for query in slow_queries:
            print(f"\nSlow query detected:")
            print(f"  Thread ID: {query['pid']}")
            print(f"  User: {query['user']}@{query['host']}")
            print(f"  Database: {query['database']}")
            print(f"  Duration: {query['duration_seconds']} seconds")
            print(f"  State: {query['state']}")
            print(f"  Query: {query['query'][:100] if query['query'] else 'N/A'}...")
    else:
        print("✓ No slow queries detected (threshold: 2 seconds)")

    # 5. Check for recent deadlocks from InnoDB status
    print("\n=== Recent Deadlock Information ===")
    deadlock_info = detector.get_deadlock_info(entity_manager)

    if deadlock_info.get('has_recent_deadlock'):
        print("⚠️  Recent deadlock detected!")
        print("\nDeadlock details (from SHOW ENGINE INNODB STATUS):")
        print(deadlock_info.get('deadlock_text', 'No details available'))
    else:
        print("✓ No recent deadlocks in InnoDB status")


def example_mysql_best_practices():
    """
    Example of MySQL-specific best practices for contention avoidance.
    """

    print("\n" + "=" * 60)
    print("MySQL Best Practices for Avoiding Contention")
    print("=" * 60)

    print("""
1. Lock Ordering:
   - Always acquire locks in the same order across transactions
   - Example: Lock table A before table B consistently

2. Keep Transactions Short:
   - Minimize time between BEGIN and COMMIT
   - Avoid long-running queries inside transactions

3. Use Appropriate Isolation Levels:
   - READ COMMITTED for most cases (less locking)
   - REPEATABLE READ only when necessary
   - SERIALIZABLE for strict consistency (highest contention)

4. InnoDB Row-Level Locking:
   - Use WHERE clauses to lock specific rows
   - Avoid full table scans in transactions

5. Monitor InnoDB Status:
   - Regularly check for deadlocks
   - Monitor lock wait timeouts
   - Review transaction history length

6. Index Optimization:
   - Ensure queries use indexes to reduce lock scope
   - Covering indexes reduce lock duration

7. Batch Operations:
   - Process large updates in smaller batches
   - Reduces lock contention and duration

Example Monitored Code:
    """)

    print("""
from telemetry import decorators

class InventoryService:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager

    @decorators.transaction()
    def update_stock_levels(self, product_ids):
        '''
        Updates stock levels for multiple products.
        Telemetry will track:
        - Transaction duration
        - Lock wait times
        - Deadlock occurrences (if any)
        '''

        # Process in batches to reduce lock contention
        batch_size = 100

        for i in range(0, len(product_ids), batch_size):
            batch = product_ids[i:i + batch_size]

            # Lock only the specific products needed
            for product_id in batch:
                self.entity_manager.lock(Product, product_id)

                # Update product
                product = self.entity_manager.get(Product, product_id)
                product.stock_level = calculate_new_stock(product)
                self.entity_manager.update(product)
    """)


def monitor_mysql_periodically(entity_manager, telemetry_plugin, interval=30):
    """
    Sets up periodic MySQL monitoring for production environments.

    :type entity_manager: EntityManager
    :param entity_manager: The MySQL entity manager.
    :type telemetry_plugin: TelemetryPlugin
    :param telemetry_plugin: The telemetry plugin instance.
    :type interval: int
    :param interval: Check interval in seconds.
    """

    import time
    import threading

    detector = telemetry_plugin.get_contention_detector("mysql")

    def monitor():
        print(f"\nStarted MySQL monitoring (checking every {interval}s)")

        while True:
            try:
                # Check for blocking situations
                blocking = detector.get_blocking_queries(entity_manager)
                if blocking:
                    print(f"\n[ALERT] {len(blocking)} InnoDB lock waits detected!")
                    for block in blocking:
                        print(f"  Thread {block['blocking_thread']} blocking thread {block['waiting_thread']}")
                        print(f"  Wait duration: {block['wait_duration_seconds']}s")

                # Check transaction stats
                stats = detector.get_transaction_stats(entity_manager)

                # Alert on concerning metrics
                if stats.get('lock_wait_transactions', 0) > 3:
                    print(f"\n[WARNING] {stats['lock_wait_transactions']} transactions waiting for locks")

                if stats.get('longest_transaction_seconds', 0) > 60:
                    print(f"\n[WARNING] Long-running transaction: {stats['longest_transaction_seconds']}s")

                # Check for new deadlocks
                if stats.get('deadlocks', 0) > 0:
                    deadlock_info = detector.get_deadlock_info(entity_manager)
                    if deadlock_info.get('has_recent_deadlock'):
                        print(f"\n[ALERT] Recent deadlock detected! Total: {stats['deadlocks']}")

                time.sleep(interval)

            except Exception as e:
                print(f"Error in monitoring thread: {e}")
                time.sleep(interval)

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()


def main():
    """
    Main example function for MySQL telemetry.
    """

    print("Colony Telemetry Plugin - MySQL Examples")
    print("=" * 60)

    print("\nMySQL-Specific Features:")
    print("- InnoDB lock wait detection (MySQL 5.7 and 8.0+)")
    print("- Deadlock monitoring (error code 1213 detection)")
    print("- Transaction statistics from information_schema")
    print("- SHOW ENGINE INNODB STATUS parsing")
    print("- Processlist-based slow query detection")

    print("\n" + "=" * 60)
    print("\nTo use with your MySQL application:")
    print("1. Ensure MySQLdb or pymysql is installed")
    print("2. Configure OTEL_EXPORTER_OTLP_ENDPOINT")
    print("3. Load and instrument your entity manager")
    print("4. Use @decorators.transaction() on your methods")
    print("5. Monitor contention with the MySQL detector")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
