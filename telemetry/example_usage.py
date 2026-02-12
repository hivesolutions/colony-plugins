#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Example usage of the Colony Telemetry Plugin for detecting
database transaction contention and performance issues.
"""

import colony
from telemetry import decorators


def setup_telemetry(plugin_manager):
    """
    Sets up the telemetry plugin and instruments an entity manager.

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

    # Create entity manager with your configuration
    entity_manager = entity_manager_plugin.load_entity_manager_properties("pgsql", {
        "id": "example_database",
        "host": "localhost",
        "user": "postgres",
        "password": "postgres",
        "database": "example_db",
        "isolation": "serializable",
    })

    # Instrument the entity manager for telemetry
    telemetry_plugin.instrument_entity_manager(entity_manager)

    print("Entity manager instrumented successfully")

    return entity_manager, telemetry_plugin


def example_transaction_tracing(entity_manager):
    """
    Example of transaction tracing with OpenTelemetry.
    """

    # Define a service class that uses instrumented transactions
    class UserService:
        def __init__(self, entity_manager):
            self.entity_manager = entity_manager

        @decorators.transaction()
        def create_user_with_address(self, user_data, address_data):
            """
            Creates a user and address in a single transaction.
            This will be automatically traced.
            """

            # Create user entity
            user = Person()
            user.name = user_data["name"]
            user.email = user_data["email"]
            self.entity_manager.save(user)

            # Create address entity
            address = Address()
            address.street = address_data["street"]
            address.city = address_data["city"]
            address.person = user
            self.entity_manager.save(address)

            return user

        @decorators.transaction()
        def update_user_email(self, user_id, new_email):
            """
            Updates a user's email.
            Demonstrates lock acquisition tracking.
            """

            # Lock the user record
            self.entity_manager.lock(Person, user_id)

            # Find and update
            user = self.entity_manager.get(Person, user_id)
            user.email = new_email
            self.entity_manager.update(user)

            return user

    # Use the service
    service = UserService(entity_manager)

    try:
        user = service.create_user_with_address(
            {"name": "John Doe", "email": "john@example.com"},
            {"street": "123 Main St", "city": "New York"}
        )
        print(f"Created user: {user.name}")

        # Update the user (will show lock acquisition in traces)
        updated_user = service.update_user_email(user.object_id, "newemail@example.com")
        print(f"Updated user email: {updated_user.email}")

    except Exception as e:
        print(f"Error in transaction: {e}")


def example_contention_detection(entity_manager, telemetry_plugin):
    """
    Example of using contention detection utilities.
    """

    # Get the appropriate contention detector
    detector = telemetry_plugin.get_contention_detector("pgsql")

    print("\n=== Checking for Blocking Queries ===")
    blocking_queries = detector.get_blocking_queries(entity_manager)

    if blocking_queries:
        for block in blocking_queries:
            print(f"\nBlocking situation detected:")
            print(f"  Blocking PID: {block['blocking_pid']} ({block['blocking_user']})")
            print(f"  Blocked PID: {block['blocked_pid']} ({block['blocked_user']})")
            print(f"  Blocking query: {block['blocking_statement'][:100]}...")
            print(f"  Duration: {block['blocked_duration']}")
    else:
        print("No blocking queries detected")

    print("\n=== Checking Lock Waits ===")
    lock_waits = detector.get_lock_waits(entity_manager)

    if lock_waits:
        for wait in lock_waits:
            print(f"\nLock wait detected:")
            print(f"  Wait event: {wait['wait_event_type']}.{wait['wait_event']}")
            print(f"  Waiting count: {wait['waiting_count']}")
            print(f"  Max wait duration: {wait['max_wait_duration']}")
    else:
        print("No lock waits detected")

    print("\n=== Transaction Statistics ===")
    stats = detector.get_transaction_stats(entity_manager)

    print(f"Total transactions: {stats.get('total_transactions', 0)}")
    print(f"Active transactions: {stats.get('active_transactions', 0)}")
    print(f"Idle in transaction: {stats.get('idle_in_transaction', 0)}")
    print(f"Longest transaction: {stats.get('longest_transaction', 'N/A')}")
    print(f"Average transaction duration: {stats.get('avg_transaction_duration', 'N/A')}")
    print(f"Deadlocks (lifetime): {stats.get('deadlocks', 0)}")

    print("\n=== Checking Slow Queries ===")
    slow_queries = detector.get_slow_queries(entity_manager, duration_threshold="1 second")

    if slow_queries:
        for query in slow_queries:
            print(f"\nSlow query detected:")
            print(f"  PID: {query['pid']} ({query['user']})")
            print(f"  Duration: {query['duration']}")
            print(f"  State: {query['state']}")
            print(f"  Query: {query['query'][:100]}...")
            if query['wait_event']:
                print(f"  Waiting on: {query['wait_event_type']}.{query['wait_event']}")
    else:
        print("No slow queries detected")


def example_custom_monitoring():
    """
    Example of custom query monitoring.
    """

    class ReportService:
        def __init__(self, entity_manager):
            self.entity_manager = entity_manager

        @decorators.monitored_query
        def generate_user_report(self, start_date, end_date):
            """
            Custom query method that will be monitored.
            """

            # Complex query that might be slow
            query = """
            SELECT u.name, u.email, COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON o.user_id = u.id
            WHERE o.created_at BETWEEN %s AND %s
            GROUP BY u.id, u.name, u.email
            ORDER BY order_count DESC
            LIMIT 100
            """

            cursor = self.entity_manager.execute_query(query % (start_date, end_date))
            results = cursor.fetchall()
            cursor.close()

            return results

    print("\n=== Custom Query Monitoring ===")
    print("The @monitored_query decorator will create spans for custom queries")
    print("This helps track performance of complex analytical queries")


def monitor_contention_periodically(entity_manager, telemetry_plugin, interval=30):
    """
    Example of periodic contention monitoring.

    :type entity_manager: EntityManager
    :param entity_manager: The entity manager instance.
    :type telemetry_plugin: TelemetryPlugin
    :param telemetry_plugin: The telemetry plugin instance.
    :type interval: int
    :param interval: Check interval in seconds.
    """

    import time
    import threading

    detector = telemetry_plugin.get_contention_detector("pgsql")

    def monitor():
        while True:
            try:
                # Check for contention issues
                blocking = detector.get_blocking_queries(entity_manager)

                if blocking:
                    print(f"\n[ALERT] {len(blocking)} blocking queries detected!")
                    for block in blocking:
                        print(f"  Blocking PID {block['blocking_pid']} -> Blocked PID {block['blocked_pid']}")

                # Check transaction stats
                stats = detector.get_transaction_stats(entity_manager)

                if stats.get('idle_in_transaction', 0) > 5:
                    print(f"\n[WARNING] High idle-in-transaction count: {stats['idle_in_transaction']}")

                time.sleep(interval)

            except Exception as e:
                print(f"Error in monitoring thread: {e}")
                time.sleep(interval)

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()

    print(f"Started contention monitoring (checking every {interval}s)")


def main():
    """
    Main example function demonstrating all features.
    """

    print("Colony Telemetry Plugin - Example Usage")
    print("=" * 50)

    # Note: In a real application, you would get the plugin_manager
    # from your Colony environment. This is just for demonstration.
    print("\nTo use this example in your application:")
    print("1. Ensure OpenTelemetry packages are installed")
    print("2. Configure OTEL_EXPORTER_OTLP_ENDPOINT or use console exporter")
    print("3. Load the telemetry plugin via Colony plugin manager")
    print("4. Instrument your entity manager")
    print("5. Use the instrumented decorators in your code")

    print("\n" + "=" * 50)
    print("\nSee README.md for detailed configuration and usage instructions")


if __name__ == "__main__":
    main()
