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


class DiagnosticsSentryPlugin(colony.Plugin):
    """
    The main class for plugin responsible for the reporting of
    the errors raised in the various layers of the infra-structure
    to a Sentry compatible endpoint.
    """

    id = "pt.hive.colony.plugins.diagnostics.sentry"
    name = "Diagnostics Sentry"
    description = "Diagnostics Sentry Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["error_reporter", "test"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.api.sentry")]
    main_modules = ["diagnostics_sentry"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import diagnostics_sentry

        self.system = diagnostics_sentry.DiagnosticsSentry(self)
        self.test = diagnostics_sentry.DiagnosticsSentryTest(self)
        self.system.start()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.stop()

    def capture(self, exception=None, message=None, level=None):
        """
        Captures the provided exception or message, submitting it to
        the Sentry endpoint whenever the reporting is enabled.

        :type exception: Exception
        :param exception: The exception to be reported.
        :type message: String
        :param message: The message to be reported.
        :type level: String
        :param level: The severity level to be associated with the event.
        :rtype: bool
        :return: If the event has been accepted for submission.
        """

        return self.system.capture_safe(
            exception=exception, message=message, level=level
        )
