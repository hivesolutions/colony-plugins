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

import colony


class TelemetryTest(colony.Test):
    """
    The telemetry test class, responsible for testing
    the OpenTelemetry instrumentation functionality.
    """

    def get_bundle(self):
        """
        Retrieves the test bundle, a list with the various
        test case classes.

        :rtype: List
        :return: The list of test case classes.
        """

        return [TelemetryTestCase]


class TelemetryTestCase(colony.ColonyTestCase):
    """
    Test case for the telemetry system.
    """

    def test_plugin_load(self):
        """
        Tests that the telemetry plugin can be loaded.
        """

        # This test would require the full Colony environment
        # For now, we test the basic imports
        try:
            from . import system
            from . import decorators
            from . import contention

            self.assertTrue(hasattr(system, "Telemetry"))
            self.assertTrue(hasattr(decorators, "transaction"))
            self.assertTrue(hasattr(contention, "ContentionDetector"))

        except ImportError as e:
            self.fail("Failed to import telemetry modules: %s" % str(e))

    def test_decorator_without_otel(self):
        """
        Tests that decorators work even when OpenTelemetry is not available.
        """

        from . import decorators

        # Create a mock object with entity_manager
        class MockEntityManager:
            def __init__(self):
                self.begin_called = False
                self.commit_called = False
                self.rollback_called = False

            def begin(self):
                self.begin_called = True

            def commit(self):
                self.commit_called = True

            def rollback(self):
                self.rollback_called = True

        class MockService:
            def __init__(self):
                self.entity_manager = MockEntityManager()

            @decorators.transaction()
            def test_method(self):
                return "success"

        # Test successful transaction
        service = MockService()
        result = service.test_method()

        self.assertEqual(result, "success")
        self.assertTrue(service.entity_manager.begin_called)
        self.assertTrue(service.entity_manager.commit_called)
        self.assertFalse(service.entity_manager.rollback_called)

    def test_decorator_with_exception(self):
        """
        Tests that decorators properly rollback on exception.
        """

        from . import decorators

        class MockEntityManager:
            def __init__(self):
                self.rollback_called = False

            def begin(self):
                pass

            def commit(self):
                pass

            def rollback(self):
                self.rollback_called = True

        class MockService:
            def __init__(self):
                self.entity_manager = MockEntityManager()

            @decorators.transaction()
            def failing_method(self):
                raise ValueError("Test error")

        service = MockService()

        with self.assertRaises(ValueError):
            service.failing_method()

        self.assertTrue(service.entity_manager.rollback_called)

    def test_contention_detector_base(self):
        """
        Tests the base contention detector.
        """

        from . import contention
        from . import system

        # Create a mock telemetry system
        class MockPlugin:
            def warning(self, msg):
                pass

        class MockTelemetrySystem:
            def __init__(self):
                self.plugin = MockPlugin()

        telemetry_sys = MockTelemetrySystem()
        detector = contention.ContentionDetector(telemetry_sys)

        # Test base methods return empty results
        self.assertEqual(detector.get_blocking_queries(None), [])
        self.assertEqual(detector.get_lock_waits(None), [])
        self.assertEqual(detector.get_transaction_stats(None), {})
