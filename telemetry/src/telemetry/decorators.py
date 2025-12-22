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

try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode, SpanKind

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


def transaction(transaction_type="required", trace_enabled=True):
    """
    Instrumented decorator for transactional data logic with OpenTelemetry tracing.
    This decorator extends the standard transaction decorator with observability.

    The decorator provides:
    - Distributed tracing with OpenTelemetry
    - Automatic span creation for transactions
    - Transaction duration tracking
    - Error and rollback tracking
    - Retry detection for contention scenarios

    :type transaction_type: String
    :param transaction_type: The type of transaction to be created.
    :type trace_enabled: bool
    :param trace_enabled: Whether to enable tracing for this transaction.
    :rtype: Function
    :return: The created decorator function.
    """

    def create_decorator_interceptor(function):
        """
        Creates a decorator interceptor that intercepts the normal function call.

        :type function: Function
        :param function: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the instrumented transaction decorator.
            """

            # Retrieves the instance self to access entity manager
            self_value = args[0]

            # Get tracer if available
            tracer = None
            if OTEL_AVAILABLE and trace_enabled:
                try:
                    tracer = trace.get_tracer("colony.entity_manager")
                except:
                    pass

            # Determine if we should create a span
            should_trace = tracer is not None

            if should_trace:
                # Get engine name for attributes
                try:
                    engine_name = self_value.entity_manager.engine.get_engine_name()
                except:
                    engine_name = "unknown"

                span = tracer.start_span(
                    f"db.transaction.{function.__name__}",
                    kind=SpanKind.CLIENT,
                    attributes={
                        "db.system": engine_name,
                        "db.transaction.type": transaction_type,
                        "code.function": function.__name__,
                        "code.namespace": function.__module__,
                    }
                )
                ctx_token = trace.set_span_in_context(span)
            else:
                span = None

            start_time = time.time()
            retry_count = 0

            try:
                # Begin transaction
                self_value.entity_manager.begin()

                if span:
                    span.add_event("transaction.started")

                # Execute the function
                return_value = function(*args, **kwargs)

                # Commit transaction
                self_value.entity_manager.commit()

                if span:
                    span.add_event("transaction.committed")
                    span.set_status(Status(StatusCode.OK))

            except Exception as e:
                # Rollback on error
                self_value.entity_manager.rollback()

                if span:
                    span.add_event("transaction.rolled_back")

                    # Detect contention-related errors
                    error_str = str(e).lower()
                    is_contention = any(
                        keyword in error_str
                        for keyword in [
                            "lock",
                            "timeout",
                            "deadlock",
                            "serialization",
                            "could not serialize",
                        ]
                    )

                    if is_contention:
                        span.set_attribute("db.transaction.contention", True)
                        span.add_event("contention_detected", {"error.type": type(e).__name__})
                        retry_count += 1

                    span.set_attribute("db.transaction.retry_count", retry_count)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)

                # Re-raise the exception
                raise

            finally:
                # Record duration
                duration = (time.time() - start_time) * 1000

                if span:
                    span.set_attribute("db.transaction.duration_ms", duration)
                    span.end()

            return return_value

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the instrumented transaction decorator.

        :type function: Function
        :param function: The function to be decorated.
        :rtype: Function
        :return: The decorator interceptor function.
        """

        decorator_interceptor_function = create_decorator_interceptor(function)
        return decorator_interceptor_function

    return decorator


def monitored_query(function):
    """
    Decorator to monitor query execution with OpenTelemetry.
    Useful for tracking custom query methods.

    :type function: Function
    :param function: The function to decorate.
    :rtype: Function
    :return: The decorated function.
    """

    def wrapper(*args, **kwargs):
        if not OTEL_AVAILABLE:
            return function(*args, **kwargs)

        tracer = trace.get_tracer("colony.entity_manager")

        with tracer.start_as_current_span(
            f"db.custom_query.{function.__name__}",
            kind=SpanKind.CLIENT,
            attributes={
                "code.function": function.__name__,
                "code.namespace": function.__module__,
            }
        ) as span:
            start_time = time.time()

            try:
                result = function(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

            finally:
                duration = (time.time() - start_time) * 1000
                span.set_attribute("duration_ms", duration)

    return wrapper
