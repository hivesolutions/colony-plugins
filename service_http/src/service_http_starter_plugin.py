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


class ServiceHTTPStarterPlugin(colony.Plugin):
    """
    The main class for the HTTP Service Starter plugin.
    """

    id = "pt.hive.colony.plugins.service.http.starter"
    name = "HTTP Service Starter"
    description = "The plugin that starts the HTTP service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT,
    ]
    capabilities = ["main"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.service.http")]
    main_modules = ["service_http_starter"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.release_ready_semaphore()

        # defines the parameters and starts the service with
        # this map as the configuration
        parameters = dict(socket_provider="normal", port=8080)
        self.service_http_plugin.start_service(parameters)

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.service_http_plugin.stop_service({})
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.Plugin.end_unload_plugin(self)
        self.release_ready_semaphore()
