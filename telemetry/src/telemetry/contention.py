#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """


class ContentionDetector(object):
    """
    Base class for database contention detection.
    Provides methods to query and analyze database locking and contention issues.
    """

    telemetry_system = None
    """ Reference to the telemetry system """

    def __init__(self, telemetry_system):
        """
        Constructor of the class.

        :type telemetry_system: Telemetry
        :param telemetry_system: The telemetry system instance.
        """

        self.telemetry_system = telemetry_system

    def get_blocking_queries(self, entity_manager):
        """
        Returns queries that are blocking other queries.
        Base implementation returns empty list.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List of blocking query information dictionaries.
        """

        return []

    def get_lock_waits(self, entity_manager):
        """
        Returns information about current lock waits.
        Base implementation returns empty list.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List of lock wait information dictionaries.
        """

        return []

    def get_transaction_stats(self, entity_manager):
        """
        Returns statistics about active transactions.
        Base implementation returns empty dict.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Transaction statistics dictionary.
        """

        return {}


class PgSQLContentionDetector(ContentionDetector):
    """
    PostgreSQL-specific contention detection.
    Provides detailed lock and transaction analysis for PostgreSQL databases.
    """

    def get_blocking_queries(self, entity_manager):
        """
        Returns PostgreSQL queries that are blocking other queries.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List of blocking query information.
        """

        query = """
        SELECT
            blocked_locks.pid AS blocked_pid,
            blocked_activity.usename AS blocked_user,
            blocking_locks.pid AS blocking_pid,
            blocking_activity.usename AS blocking_user,
            blocked_activity.query AS blocked_statement,
            blocking_activity.query AS blocking_statement,
            blocked_activity.application_name AS blocked_application,
            blocking_activity.application_name AS blocking_application,
            blocked_activity.state AS blocked_state,
            blocking_activity.state AS blocking_state,
            NOW() - blocked_activity.xact_start AS blocked_duration,
            NOW() - blocking_activity.xact_start AS blocking_duration
        FROM pg_catalog.pg_locks blocked_locks
        JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
        JOIN pg_catalog.pg_locks blocking_locks
            ON blocking_locks.locktype = blocked_locks.locktype
            AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
            AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
            AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
            AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
            AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
            AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
            AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
            AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
            AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
            AND blocking_locks.pid != blocked_locks.pid
        JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
        WHERE NOT blocked_locks.granted;
        """

        try:
            cursor = entity_manager.execute_query(query)
            results = []

            for row in cursor:
                results.append({
                    "blocked_pid": row[0],
                    "blocked_user": row[1],
                    "blocking_pid": row[2],
                    "blocking_user": row[3],
                    "blocked_statement": row[4],
                    "blocking_statement": row[5],
                    "blocked_application": row[6],
                    "blocking_application": row[7],
                    "blocked_state": row[8],
                    "blocking_state": row[9],
                    "blocked_duration": str(row[10]) if row[10] else None,
                    "blocking_duration": str(row[11]) if row[11] else None,
                })

            cursor.close()
            return results

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get blocking queries: %s" % str(e)
            )
            return []

    def get_lock_waits(self, entity_manager):
        """
        Returns PostgreSQL lock wait information.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List of lock wait information.
        """

        query = """
        SELECT
            wait_event_type,
            wait_event,
            state,
            COUNT(*) as waiting_count,
            MAX(NOW() - xact_start) as max_wait_duration
        FROM pg_stat_activity
        WHERE wait_event IS NOT NULL
          AND state != 'idle'
        GROUP BY wait_event_type, wait_event, state
        ORDER BY waiting_count DESC;
        """

        try:
            cursor = entity_manager.execute_query(query)
            results = []

            for row in cursor:
                results.append({
                    "wait_event_type": row[0],
                    "wait_event": row[1],
                    "state": row[2],
                    "waiting_count": row[3],
                    "max_wait_duration": str(row[4]) if row[4] else None,
                })

            cursor.close()
            return results

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get lock waits: %s" % str(e)
            )
            return []

    def get_transaction_stats(self, entity_manager):
        """
        Returns PostgreSQL transaction statistics.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Transaction statistics.
        """

        # Get transaction count and durations
        query = """
        SELECT
            COUNT(*) as total_transactions,
            COUNT(*) FILTER (WHERE state = 'active') as active_transactions,
            COUNT(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction,
            COUNT(*) FILTER (WHERE state = 'idle in transaction (aborted)') as aborted_transactions,
            MAX(NOW() - xact_start) as longest_transaction,
            AVG(NOW() - xact_start) as avg_transaction_duration
        FROM pg_stat_activity
        WHERE xact_start IS NOT NULL;
        """

        try:
            cursor = entity_manager.execute_query(query)
            row = cursor.fetchone()

            stats = {
                "total_transactions": row[0] if row[0] else 0,
                "active_transactions": row[1] if row[1] else 0,
                "idle_in_transaction": row[2] if row[2] else 0,
                "aborted_transactions": row[3] if row[3] else 0,
                "longest_transaction": str(row[4]) if row[4] else None,
                "avg_transaction_duration": str(row[5]) if row[5] else None,
            }

            cursor.close()

            # Get deadlock information from pg_stat_database
            deadlock_query = """
            SELECT deadlocks
            FROM pg_stat_database
            WHERE datname = current_database();
            """

            cursor = entity_manager.execute_query(deadlock_query)
            row = cursor.fetchone()

            if row:
                stats["deadlocks"] = row[0] if row[0] else 0

            cursor.close()

            return stats

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get transaction stats: %s" % str(e)
            )
            return {}

    def get_slow_queries(self, entity_manager, duration_threshold="5 seconds"):
        """
        Returns currently executing slow queries.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :type duration_threshold: String
        :param duration_threshold: PostgreSQL interval for slow query threshold.
        :rtype: list
        :return: List of slow query information.
        """

        query = """
        SELECT
            pid,
            usename,
            application_name,
            client_addr,
            state,
            query,
            NOW() - query_start AS duration,
            wait_event_type,
            wait_event
        FROM pg_stat_activity
        WHERE state != 'idle'
          AND query_start IS NOT NULL
          AND NOW() - query_start > interval '%s'
        ORDER BY duration DESC;
        """ % duration_threshold

        try:
            cursor = entity_manager.execute_query(query)
            results = []

            for row in cursor:
                results.append({
                    "pid": row[0],
                    "user": row[1],
                    "application": row[2],
                    "client_addr": str(row[3]) if row[3] else None,
                    "state": row[4],
                    "query": row[5],
                    "duration": str(row[6]) if row[6] else None,
                    "wait_event_type": row[7],
                    "wait_event": row[8],
                })

            cursor.close()
            return results

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get slow queries: %s" % str(e)
            )
            return []


class MySQLContentionDetector(ContentionDetector):
    """
    MySQL-specific contention detection.
    Provides lock and transaction analysis for MySQL databases.
    Works with MySQL 5.7+ and MySQL 8.0+ (using performance_schema).
    """

    def get_blocking_queries(self, entity_manager):
        """
        Returns MySQL queries that are blocking other queries.
        Uses performance_schema for MySQL 8.0+ compatibility.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List of blocking query information.
        """

        # Try MySQL 8.0+ performance_schema approach first
        query_perf = """
        SELECT
            waiting_trx_id,
            waiting_pid,
            waiting_query,
            blocking_trx_id,
            blocking_pid,
            blocking_query,
            wait_started,
            TIMESTAMPDIFF(SECOND, wait_started, NOW()) as wait_duration_seconds
        FROM sys.innodb_lock_waits;
        """

        try:
            cursor = entity_manager.execute_query(query_perf)
            results = []

            for row in cursor:
                results.append({
                    "waiting_trx_id": row[0],
                    "waiting_thread": row[1],
                    "waiting_query": row[2],
                    "blocking_trx_id": row[3],
                    "blocking_thread": row[4],
                    "blocking_query": row[5],
                    "wait_started": str(row[6]) if row[6] else None,
                    "wait_duration_seconds": row[7] if row[7] else 0,
                })

            cursor.close()
            return results

        except Exception:
            # Fallback to information_schema for older MySQL versions
            pass

        # Fallback query for MySQL 5.7
        query_legacy = """
        SELECT
            r.trx_id as waiting_trx_id,
            r.trx_mysql_thread_id as waiting_thread,
            r.trx_query as waiting_query,
            b.trx_id as blocking_trx_id,
            b.trx_mysql_thread_id as blocking_thread,
            b.trx_query as blocking_query,
            r.trx_wait_started as wait_started,
            TIMESTAMPDIFF(SECOND, r.trx_wait_started, NOW()) as wait_duration_seconds
        FROM information_schema.innodb_lock_waits w
        INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
        INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;
        """

        try:
            cursor = entity_manager.execute_query(query_legacy)
            results = []

            for row in cursor:
                results.append({
                    "waiting_trx_id": row[0],
                    "waiting_thread": row[1],
                    "waiting_query": row[2],
                    "blocking_trx_id": row[3],
                    "blocking_thread": row[4],
                    "blocking_query": row[5],
                    "wait_started": str(row[6]) if row[6] else None,
                    "wait_duration_seconds": row[7] if row[7] else 0,
                })

            cursor.close()
            return results

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get blocking queries: %s" % str(e)
            )
            return []

    def get_lock_waits(self, entity_manager):
        """
        Returns MySQL lock wait information.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List of lock wait information.
        """

        query = """
        SELECT
            COUNT(*) as lock_wait_count,
            SUM(TIMESTAMPDIFF(SECOND, trx_wait_started, NOW())) as total_wait_seconds,
            MAX(TIMESTAMPDIFF(SECOND, trx_wait_started, NOW())) as max_wait_seconds
        FROM information_schema.innodb_trx
        WHERE trx_state = 'LOCK WAIT';
        """

        try:
            cursor = entity_manager.execute_query(query)
            row = cursor.fetchone()

            results = []
            if row:
                results.append({
                    "lock_wait_count": row[0] if row[0] else 0,
                    "total_wait_seconds": row[1] if row[1] else 0,
                    "max_wait_seconds": row[2] if row[2] else 0,
                })

            cursor.close()
            return results

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get lock waits: %s" % str(e)
            )
            return []

    def get_transaction_stats(self, entity_manager):
        """
        Returns MySQL transaction statistics.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Transaction statistics.
        """

        # Use conditional aggregation instead of FILTER for MySQL compatibility
        query = """
        SELECT
            COUNT(*) as total_transactions,
            SUM(CASE WHEN trx_state = 'RUNNING' THEN 1 ELSE 0 END) as running_transactions,
            SUM(CASE WHEN trx_state = 'LOCK WAIT' THEN 1 ELSE 0 END) as lock_wait_transactions,
            MAX(TIMESTAMPDIFF(SECOND, trx_started, NOW())) as longest_transaction_seconds,
            AVG(TIMESTAMPDIFF(SECOND, trx_started, NOW())) as avg_transaction_seconds
        FROM information_schema.innodb_trx;
        """

        try:
            cursor = entity_manager.execute_query(query)
            row = cursor.fetchone()

            stats = {}
            if row:
                stats = {
                    "total_transactions": row[0] if row[0] else 0,
                    "running_transactions": row[1] if row[1] else 0,
                    "lock_wait_transactions": row[2] if row[2] else 0,
                    "longest_transaction_seconds": row[3] if row[3] else 0,
                    "avg_transaction_seconds": float(row[4]) if row[4] else 0.0,
                }

            cursor.close()

            # Get deadlock information
            deadlock_query = """
            SELECT VARIABLE_VALUE
            FROM information_schema.GLOBAL_STATUS
            WHERE VARIABLE_NAME = 'Innodb_deadlocks';
            """

            try:
                cursor = entity_manager.execute_query(deadlock_query)
                row = cursor.fetchone()
                if row:
                    stats["deadlocks"] = int(row[0]) if row[0] else 0
                cursor.close()
            except Exception:
                pass

            return stats

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get transaction stats: %s" % str(e)
            )
            return {}

    def get_slow_queries(self, entity_manager, duration_threshold_seconds=5):
        """
        Returns currently executing slow queries from processlist.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :type duration_threshold_seconds: int
        :param duration_threshold_seconds: Minimum query duration in seconds.
        :rtype: list
        :return: List of slow query information.
        """

        query = """
        SELECT
            ID as pid,
            USER as user,
            HOST as host,
            DB as db,
            COMMAND as command,
            TIME as duration_seconds,
            STATE as state,
            INFO as query
        FROM information_schema.PROCESSLIST
        WHERE COMMAND != 'Sleep'
          AND TIME > %d
          AND INFO IS NOT NULL
        ORDER BY TIME DESC;
        """ % duration_threshold_seconds

        try:
            cursor = entity_manager.execute_query(query)
            results = []

            for row in cursor:
                results.append({
                    "pid": row[0],
                    "user": row[1],
                    "host": row[2],
                    "database": row[3],
                    "command": row[4],
                    "duration_seconds": row[5],
                    "state": row[6],
                    "query": row[7],
                })

            cursor.close()
            return results

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get slow queries: %s" % str(e)
            )
            return []

    def get_deadlock_info(self, entity_manager):
        """
        Returns recent deadlock information from InnoDB status.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Deadlock information.
        """

        query = "SHOW ENGINE INNODB STATUS"

        try:
            cursor = entity_manager.execute_query(query)
            row = cursor.fetchone()

            if row and len(row) > 2:
                status_text = row[2]

                # Parse the latest deadlock information
                deadlock_info = {}
                if "LATEST DETECTED DEADLOCK" in status_text:
                    # Extract deadlock section
                    start = status_text.find("LATEST DETECTED DEADLOCK")
                    end = status_text.find("------------", start + 1)
                    if end > start:
                        deadlock_section = status_text[start:end]
                        deadlock_info["has_recent_deadlock"] = True
                        deadlock_info["deadlock_text"] = deadlock_section[:500]  # First 500 chars
                else:
                    deadlock_info["has_recent_deadlock"] = False

                cursor.close()
                return deadlock_info

            cursor.close()
            return {}

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get deadlock info: %s" % str(e)
            )
            return {}


class SQLiteContentionDetector(ContentionDetector):
    """
    SQLite-specific contention detection.
    Provides monitoring for SQLite databases with file-based locking.

    Note: SQLite uses database-level locks rather than row-level locks,
    so contention patterns are different from PostgreSQL and MySQL.
    """

    def get_database_info(self, entity_manager):
        """
        Returns SQLite database information and statistics.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Database information.
        """

        try:
            info = {}

            # Get database file path and size
            connection = entity_manager.get_connection()
            _connection = connection._connection

            try:
                file_path = _connection.get_file_path()
                info["file_path"] = file_path

                import os
                if os.path.exists(file_path):
                    info["file_size_bytes"] = os.path.getsize(file_path)
                    info["file_size_mb"] = round(info["file_size_bytes"] / (1024 * 1024), 2)
            except Exception:
                pass

            # Get page count and page size
            try:
                cursor = entity_manager.execute_query("PRAGMA page_count")
                row = cursor.fetchone()
                if row:
                    info["page_count"] = row[0]
                cursor.close()

                cursor = entity_manager.execute_query("PRAGMA page_size")
                row = cursor.fetchone()
                if row:
                    info["page_size"] = row[0]
                cursor.close()
            except Exception:
                pass

            # Get cache size
            try:
                cursor = entity_manager.execute_query("PRAGMA cache_size")
                row = cursor.fetchone()
                if row:
                    info["cache_size"] = row[0]
                cursor.close()
            except Exception:
                pass

            # Get journal mode
            try:
                cursor = entity_manager.execute_query("PRAGMA journal_mode")
                row = cursor.fetchone()
                if row:
                    info["journal_mode"] = row[0]
                cursor.close()
            except Exception:
                pass

            # Get synchronous mode
            try:
                cursor = entity_manager.execute_query("PRAGMA synchronous")
                row = cursor.fetchone()
                if row:
                    sync_modes = {0: "OFF", 1: "NORMAL", 2: "FULL", 3: "EXTRA"}
                    info["synchronous"] = sync_modes.get(row[0], row[0])
                cursor.close()
            except Exception:
                pass

            # Get busy timeout
            try:
                cursor = entity_manager.execute_query("PRAGMA busy_timeout")
                row = cursor.fetchone()
                if row:
                    info["busy_timeout_ms"] = row[0]
                cursor.close()
            except Exception:
                pass

            # Get locking mode
            try:
                cursor = entity_manager.execute_query("PRAGMA locking_mode")
                row = cursor.fetchone()
                if row:
                    info["locking_mode"] = row[0]
                cursor.close()
            except Exception:
                pass

            return info

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get database info: %s" % str(e)
            )
            return {}

    def get_blocking_queries(self, entity_manager):
        """
        SQLite uses database-level locks, not row-level locks.
        This method returns information about lock contention.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List with lock information (or empty if no contention).
        """

        # SQLite doesn't have a way to query blocked connections like PostgreSQL/MySQL
        # Contention is detected via SQLITE_BUSY errors in execute_query
        return []

    def get_lock_waits(self, entity_manager):
        """
        Returns information about SQLite locking configuration.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: list
        :return: List with lock configuration.
        """

        try:
            info = {}

            # Get busy timeout (how long to wait for locks)
            cursor = entity_manager.execute_query("PRAGMA busy_timeout")
            row = cursor.fetchone()
            if row:
                info["busy_timeout_ms"] = row[0]
            cursor.close()

            # Get locking mode
            cursor = entity_manager.execute_query("PRAGMA locking_mode")
            row = cursor.fetchone()
            if row:
                info["locking_mode"] = row[0]
            cursor.close()

            return [info] if info else []

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get lock info: %s" % str(e)
            )
            return []

    def get_transaction_stats(self, entity_manager):
        """
        Returns SQLite database statistics.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Database statistics.
        """

        try:
            stats = {}

            # Get database file size
            try:
                connection = entity_manager.get_connection()
                _connection = connection._connection
                file_path = _connection.get_file_path()

                import os
                if os.path.exists(file_path):
                    stats["database_size_bytes"] = os.path.getsize(file_path)
                    stats["database_size_mb"] = round(stats["database_size_bytes"] / (1024 * 1024), 2)
            except Exception:
                pass

            # Get page statistics
            try:
                cursor = entity_manager.execute_query("PRAGMA page_count")
                row = cursor.fetchone()
                if row:
                    stats["page_count"] = row[0]
                cursor.close()

                cursor = entity_manager.execute_query("PRAGMA freelist_count")
                row = cursor.fetchone()
                if row:
                    stats["freelist_count"] = row[0]
                cursor.close()
            except Exception:
                pass

            # Get cache statistics (if available)
            try:
                cursor = entity_manager.execute_query("PRAGMA cache_size")
                row = cursor.fetchone()
                if row:
                    stats["cache_size"] = row[0]
                cursor.close()
            except Exception:
                pass

            # Get transaction level from connection
            try:
                connection = entity_manager.get_connection()
                _connection = connection._connection
                if hasattr(_connection, 'transaction_level'):
                    stats["transaction_level"] = _connection.transaction_level
                    stats["active_transaction"] = _connection.transaction_level > 0
            except Exception:
                pass

            return stats

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to get transaction stats: %s" % str(e)
            )
            return {}

    def get_slow_queries(self, entity_manager, duration_threshold_seconds=5):
        """
        SQLite doesn't have a processlist like MySQL or pg_stat_activity like PostgreSQL.
        Slow queries are detected via instrumentation timing, not system tables.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :type duration_threshold_seconds: int
        :param duration_threshold_seconds: Query duration threshold (not used for SQLite).
        :rtype: list
        :return: Empty list (use OpenTelemetry traces for slow query detection).
        """

        # SQLite doesn't expose a query log or processlist
        # Use OpenTelemetry traces to detect slow queries
        return []

    def optimize_database(self, entity_manager):
        """
        Runs VACUUM and ANALYZE to optimize the SQLite database.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Optimization results.
        """

        try:
            results = {}

            # Get size before optimization
            connection = entity_manager.get_connection()
            _connection = connection._connection
            file_path = _connection.get_file_path()

            import os
            if os.path.exists(file_path):
                results["size_before_bytes"] = os.path.getsize(file_path)

            # Run ANALYZE to update statistics
            try:
                cursor = entity_manager.execute_query("ANALYZE")
                cursor.close()
                results["analyze"] = "completed"
            except Exception as e:
                results["analyze"] = f"failed: {str(e)}"

            # Run VACUUM to reclaim space (can't be in a transaction)
            try:
                # Note: VACUUM cannot be run inside a transaction
                cursor = entity_manager.execute_query("VACUUM")
                cursor.close()
                results["vacuum"] = "completed"
            except Exception as e:
                results["vacuum"] = f"failed: {str(e)}"

            # Get size after optimization
            if os.path.exists(file_path):
                results["size_after_bytes"] = os.path.getsize(file_path)
                if "size_before_bytes" in results:
                    saved = results["size_before_bytes"] - results["size_after_bytes"]
                    results["space_saved_bytes"] = saved
                    results["space_saved_mb"] = round(saved / (1024 * 1024), 2)

            return results

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to optimize database: %s" % str(e)
            )
            return {"error": str(e)}

    def get_integrity_check(self, entity_manager):
        """
        Runs PRAGMA integrity_check on the database.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to query.
        :rtype: dict
        :return: Integrity check results.
        """

        try:
            cursor = entity_manager.execute_query("PRAGMA integrity_check")
            rows = cursor.fetchall()
            cursor.close()

            results = []
            for row in rows:
                results.append(row[0])

            is_ok = len(results) == 1 and results[0] == "ok"

            return {
                "is_ok": is_ok,
                "results": results,
                "message": "Database integrity OK" if is_ok else "Database integrity issues found"
            }

        except Exception as e:
            self.telemetry_system.plugin.warning(
                "Failed to check integrity: %s" % str(e)
            )
            return {"error": str(e)}
