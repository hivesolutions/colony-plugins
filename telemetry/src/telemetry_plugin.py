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


class TelemetryPlugin(colony.Plugin):
    """
    The main class for the Telemetry plugin.
    Provides OpenTelemetry instrumentation for the entity manager
    to detect transaction contention and performance issues.
    """

    id = "pt.hive.colony.plugins.telemetry"
    name = "Telemetry"
    description = "OpenTelemetry instrumentation for entity manager monitoring"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["telemetry"]
    dependencies = [
        colony.PackageDependency(
            "OpenTelemetry API",
            "opentelemetry-api",
        ),
        colony.PackageDependency(
            "OpenTelemetry SDK",
            "opentelemetry-sdk",
        ),
    ]
    main_modules = ["telemetry"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import telemetry

        self.system = telemetry.Telemetry(self)
        self.decorators = telemetry.decorators
        self.test = telemetry.test.TelemetryTest(self)

    def instrument_entity_manager(self, entity_manager):
        """
        Instruments the given entity manager with OpenTelemetry
        tracing and metrics collection.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to instrument.
        :rtype: EntityManager
        :return: The instrumented entity manager.
        """

        return self.system.instrument_entity_manager(entity_manager)

    def get_transaction_decorator(self):
        """
        Retrieves the instrumented transaction decorator that
        provides OpenTelemetry tracing.

        :rtype: Function
        :return: The instrumented transaction decorator.
        """

        return self.decorators.transaction

    def get_contention_detector(self, engine_name):
        """
        Creates a contention detector for the specified database engine.

        :type engine_name: String
        :param engine_name: The database engine name (pgsql, mysql, sqlite).
        :rtype: ContentionDetector
        :return: The contention detector instance.
        """

        return self.system.get_contention_detector(engine_name)

    def configure_telemetry(self, **kwargs):
        """
        Configures the telemetry system with custom settings.

        :rtype: bool
        :return: True if configuration was successful.
        """

        return self.system.configure(**kwargs)
