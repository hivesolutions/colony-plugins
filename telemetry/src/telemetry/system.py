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

import time
import functools

import colony

from . import contention

try:
    from opentelemetry import trace, metrics
    from opentelemetry.trace import Status, StatusCode, SpanKind
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
    from opentelemetry.sdk.resources import Resource

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


class Telemetry(colony.System):
    """
    The telemetry system class, responsible for providing
    OpenTelemetry instrumentation for the entity manager.
    """

    tracer = None
    """ The OpenTelemetry tracer instance """

    meter = None
    """ The OpenTelemetry meter instance """

    configured = False
    """ Flag indicating if telemetry has been configured """

    # Metrics
    transaction_duration = None
    transaction_retries = None
    active_transactions = None
    lock_wait_duration = None
    query_duration = None
    contention_events = None

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)

        self.tracer = None
        self.meter = None
        self.configured = False

        # Initialize with default configuration if OpenTelemetry is available
        if OTEL_AVAILABLE:
            self._init_default_config()

    def _init_default_config(self):
        """
        Initializes OpenTelemetry with default console exporters.
        This can be overridden by calling configure() with custom settings.
        """

        # Check if already configured externally
        if trace.get_tracer_provider() != trace.NoOpTracerProvider():
            self.plugin.info("OpenTelemetry already configured externally, using existing configuration")
            self.tracer = trace.get_tracer("colony.entity_manager", "1.0.0")
            self.meter = metrics.get_meter("colony.entity_manager", "1.0.0")
            self.configured = True
            self._init_metrics()
            return

        # Get configuration from environment or use defaults
        otlp_endpoint = colony.conf("OTEL_EXPORTER_OTLP_ENDPOINT", None)
        use_console = colony.conf("OTEL_USE_CONSOLE", False, cast=bool)
        service_name = colony.conf("OTEL_SERVICE_NAME", "colony-entity-manager")

        # Create resource with service name
        resource = Resource.create({"service.name": service_name})

        # Set up tracing
        tracer_provider = TracerProvider(resource=resource)

        if otlp_endpoint:
            try:
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
                span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
                tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
                self.plugin.info("OpenTelemetry tracing configured with OTLP endpoint: %s" % otlp_endpoint)
            except ImportError:
                self.plugin.warning("OTLP exporter not available, install opentelemetry-exporter-otlp")
                use_console = True

        if use_console or not otlp_endpoint:
            span_exporter = ConsoleSpanExporter()
            tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
            self.plugin.info("OpenTelemetry tracing configured with console exporter")

        trace.set_tracer_provider(tracer_provider)
        self.tracer = trace.get_tracer("colony.entity_manager", "1.0.0")

        # Set up metrics
        if otlp_endpoint:
            try:
                from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
                metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
                metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=30000)
                meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
                self.plugin.info("OpenTelemetry metrics configured with OTLP endpoint: %s" % otlp_endpoint)
            except ImportError:
                metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=60000)
                meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
                self.plugin.info("OpenTelemetry metrics configured with console exporter")
        else:
            metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=60000)
            meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
            self.plugin.info("OpenTelemetry metrics configured with console exporter")

        metrics.set_meter_provider(meter_provider)
        self.meter = metrics.get_meter("colony.entity_manager", "1.0.0")

        self.configured = True
        self._init_metrics()

    def _init_metrics(self):
        """Initialize all metric instruments."""

        if not self.meter:
            return

        # Transaction duration histogram
        self.transaction_duration = self.meter.create_histogram(
            name="db.transaction.duration",
            description="Time spent in database transactions",
            unit="ms"
        )

        # Transaction retries counter
        self.transaction_retries = self.meter.create_counter(
            name="db.transaction.retries",
            description="Number of transaction retries due to contention"
        )

        # Active transactions gauge (up-down counter)
        self.active_transactions = self.meter.create_up_down_counter(
            name="db.transaction.active",
            description="Number of active database transactions"
        )

        # Lock wait duration histogram
        self.lock_wait_duration = self.meter.create_histogram(
            name="db.lock.wait_duration",
            description="Time spent waiting for locks",
            unit="ms"
        )

        # Query execution duration histogram
        self.query_duration = self.meter.create_histogram(
            name="db.query.duration",
            description="Database query execution time",
            unit="ms"
        )

        # Contention events counter
        self.contention_events = self.meter.create_counter(
            name="db.contention.events",
            description="Number of contention events detected"
        )

    def configure(self, **kwargs):
        """
        Configures the telemetry system with custom settings.

        :type kwargs: Dictionary
        :param kwargs: Configuration parameters.
        :rtype: bool
        :return: True if configuration was successful.
        """

        if not OTEL_AVAILABLE:
            self.plugin.warning("OpenTelemetry not available, please install required packages")
            return False

        # If tracer/meter providers are provided, use them
        if "tracer_provider" in kwargs:
            trace.set_tracer_provider(kwargs["tracer_provider"])
            self.tracer = trace.get_tracer("colony.entity_manager", "1.0.0")

        if "meter_provider" in kwargs:
            metrics.set_meter_provider(kwargs["meter_provider"])
            self.meter = metrics.get_meter("colony.entity_manager", "1.0.0")

        self.configured = True
        self._init_metrics()

        return True

    def instrument_entity_manager(self, entity_manager):
        """
        Instruments the given entity manager with OpenTelemetry.
        This wraps key methods to add tracing and metrics.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to instrument.
        :rtype: EntityManager
        :return: The instrumented entity manager.
        """

        if not OTEL_AVAILABLE or not self.configured:
            self.plugin.warning("Cannot instrument entity manager: OpenTelemetry not configured")
            return entity_manager

        # Store original methods
        original_begin = entity_manager.begin
        original_commit = entity_manager.commit
        original_rollback = entity_manager.rollback
        original_execute_query = entity_manager.execute_query
        original_lock = entity_manager.lock
        original_lock_table = entity_manager.lock_table

        # Track transaction start times per connection
        transaction_start_times = {}

        # Wrap begin method
        @functools.wraps(original_begin)
        def instrumented_begin():
            connection = entity_manager.get_connection()
            transaction_start_times[id(connection)] = time.time()

            if self.active_transactions:
                self.active_transactions.add(1, {"db.system": entity_manager.engine.get_engine_name()})

            return original_begin()

        # Wrap commit method
        @functools.wraps(original_commit)
        def instrumented_commit():
            connection = entity_manager.get_connection()
            start_time = transaction_start_times.pop(id(connection), None)

            try:
                result = original_commit()

                if start_time and self.transaction_duration:
                    duration = (time.time() - start_time) * 1000
                    self.transaction_duration.record(
                        duration,
                        {"db.system": entity_manager.engine.get_engine_name(), "db.operation": "commit"}
                    )

                return result
            finally:
                if self.active_transactions:
                    self.active_transactions.add(-1, {"db.system": entity_manager.engine.get_engine_name()})

        # Wrap rollback method
        @functools.wraps(original_rollback)
        def instrumented_rollback():
            connection = entity_manager.get_connection()
            start_time = transaction_start_times.pop(id(connection), None)

            try:
                result = original_rollback()

                if start_time and self.transaction_duration:
                    duration = (time.time() - start_time) * 1000
                    self.transaction_duration.record(
                        duration,
                        {"db.system": entity_manager.engine.get_engine_name(), "db.operation": "rollback"}
                    )

                return result
            finally:
                if self.active_transactions:
                    self.active_transactions.add(-1, {"db.system": entity_manager.engine.get_engine_name()})

        # Wrap execute_query method
        @functools.wraps(original_execute_query)
        def instrumented_execute_query(query, close_cursor=True):
            if not self.tracer:
                return original_execute_query(query, close_cursor)

            with self.tracer.start_as_current_span(
                "db.query",
                kind=SpanKind.CLIENT,
                attributes={
                    "db.system": entity_manager.engine.get_engine_name(),
                    "db.statement": query[:500] if len(query) > 500 else query,
                }
            ) as span:
                start_time = time.time()

                try:
                    result = original_execute_query(query, close_cursor)
                    span.set_status(Status(StatusCode.OK))
                    return result

                except Exception as e:
                    # Detect contention-related errors
                    error_str = str(e).lower()
                    error_type = type(e).__name__

                    # Check for database-specific error codes
                    is_lock_error = False
                    contention_type = "unknown"

                    # MySQL deadlock detection (error code 1213)
                    if hasattr(e, 'args') and len(e.args) > 0:
                        error_code = e.args[0] if isinstance(e.args[0], int) else None
                        if error_code == 1213:  # MySQL deadlock
                            is_lock_error = True
                            contention_type = "deadlock"

                    # Generic error string detection
                    if not is_lock_error:
                        lock_keywords = ["lock", "timeout", "deadlock", "serialization", "could not serialize"]
                        is_lock_error = any(keyword in error_str for keyword in lock_keywords)

                        if "deadlock" in error_str:
                            contention_type = "deadlock"
                        elif "timeout" in error_str or "lock timeout" in error_str:
                            contention_type = "lock_timeout"
                        elif "serialization" in error_str or "could not serialize" in error_str:
                            contention_type = "serialization_failure"
                        else:
                            contention_type = "lock_wait"

                    if is_lock_error:
                        span.set_attribute("db.lock.contention", True)
                        span.set_attribute("db.contention.type", contention_type)
                        span.add_event("lock_contention_detected", {
                            "error": str(e),
                            "error_type": error_type,
                            "contention_type": contention_type
                        })

                        if self.contention_events:
                            self.contention_events.add(1, {
                                "db.system": entity_manager.engine.get_engine_name(),
                                "error.type": contention_type
                            })

                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise

                finally:
                    duration = (time.time() - start_time) * 1000

                    if self.query_duration:
                        self.query_duration.record(
                            duration,
                            {"db.system": entity_manager.engine.get_engine_name()}
                        )

                    # Flag slow queries
                    slow_threshold = colony.conf("SLOW_QUERY_TIME", 25, cast=int)
                    if duration > slow_threshold:
                        span.set_attribute("db.slow_query", True)
                        span.add_event("slow_query_detected", {
                            "duration_ms": duration,
                            "threshold_ms": slow_threshold
                        })

        # Wrap lock methods
        @functools.wraps(original_lock)
        def instrumented_lock(entity_class, id_value=None, lock_parents=True):
            if not self.tracer:
                return original_lock(entity_class, id_value, lock_parents)

            with self.tracer.start_as_current_span(
                "db.lock",
                kind=SpanKind.CLIENT,
                attributes={
                    "db.system": entity_manager.engine.get_engine_name(),
                    "db.entity": entity_class.get_name(),
                    "db.lock.type": "row" if id_value else "table"
                }
            ) as span:
                start_time = time.time()

                try:
                    result = original_lock(entity_class, id_value, lock_parents)
                    span.set_status(Status(StatusCode.OK))
                    return result
                finally:
                    duration = (time.time() - start_time) * 1000

                    if self.lock_wait_duration:
                        self.lock_wait_duration.record(
                            duration,
                            {"db.system": entity_manager.engine.get_engine_name()}
                        )

        @functools.wraps(original_lock_table)
        def instrumented_lock_table(table_name, parameters):
            if not self.tracer:
                return original_lock_table(table_name, parameters)

            with self.tracer.start_as_current_span(
                "db.lock_table",
                kind=SpanKind.CLIENT,
                attributes={
                    "db.system": entity_manager.engine.get_engine_name(),
                    "db.table": table_name
                }
            ) as span:
                start_time = time.time()

                try:
                    result = original_lock_table(table_name, parameters)
                    span.set_status(Status(StatusCode.OK))
                    return result
                finally:
                    duration = (time.time() - start_time) * 1000

                    if self.lock_wait_duration:
                        self.lock_wait_duration.record(
                            duration,
                            {"db.system": entity_manager.engine.get_engine_name()}
                        )

        # Replace methods with instrumented versions
        entity_manager.begin = instrumented_begin
        entity_manager.commit = instrumented_commit
        entity_manager.rollback = instrumented_rollback
        entity_manager.execute_query = instrumented_execute_query
        entity_manager.lock = instrumented_lock
        entity_manager.lock_table = instrumented_lock_table

        self.plugin.info("Entity manager instrumented successfully: %s" % entity_manager.id)

        return entity_manager

    def get_contention_detector(self, engine_name):
        """
        Creates a contention detector for the specified database engine.

        :type engine_name: String
        :param engine_name: The database engine name.
        :rtype: ContentionDetector
        :return: The contention detector instance.
        """

        if engine_name == "pgsql":
            return contention.PgSQLContentionDetector(self)
        elif engine_name == "mysql":
            return contention.MySQLContentionDetector(self)
        else:
            return contention.ContentionDetector(self)
