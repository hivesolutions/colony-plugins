#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class ServiceHttpPlugin(colony.Plugin):
    """
    The main class for the Http Service plugin.
    """

    id = "pt.hive.colony.plugins.service.http"
    name = "Http Service"
    description = "The plugin that offers the http service"
    version = "1.0.1"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "service.http"
    ]
    capabilities_allowed = [
        "http_service_handler",
        "http_service_encoding",
        "http_service_authentication_handler",
        "http_service_error_handler"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.service.utils")
    ]
    main_modules = [
        "service_http"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import service_http
        self.system = service_http.ServiceHttp(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    @colony.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.Plugin.set_configuration_property(self, property_name, property)

    @colony.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.Plugin.unset_configuration_property(self, property_name)

    def start_service(self, parameters):
        return self.system.start_service(parameters)

    def stop_service(self, parameters):
        return self.system.stop_service(parameters)

    @colony.load_allowed_capability("http_service_handler")
    def http_service_handler_load_allowed(self, plugin, capability):
        self.system.http_service_handler_load(plugin)

    @colony.load_allowed_capability("http_service_encoding")
    def http_service_encoding_load_allowed(self, plugin, capability):
        self.system.http_service_encoding_load(plugin)

    @colony.load_allowed_capability("http_service_authentication_handler")
    def http_service_authentication_handler_load_allowed(self, plugin, capability):
        self.system.http_service_authentication_handler_load(plugin)

    @colony.load_allowed_capability("http_service_error_handler")
    def http_service_error_handler_load_allowed(self, plugin, capability):
        self.system.http_service_error_handler_load(plugin)

    @colony.unload_allowed_capability("http_service_handler")
    def http_service_handler_unload_allowed(self, plugin, capability):
        self.system.http_service_handler_unload(plugin)

    @colony.unload_allowed_capability("http_service_encoding")
    def http_service_encoding_unload_allowed(self, plugin, capability):
        self.system.http_service_encoding_unload(plugin)

    @colony.unload_allowed_capability("http_service_authentication_handler")
    def http_service_authentication_handler_unload_allowed(self, plugin, capability):
        self.system.http_service_authentication_handler_unload(plugin)

    @colony.unload_allowed_capability("http_service_error_handler")
    def http_service_error_handler_unload_allowed(self, plugin, capability):
        self.system.http_service_error_handler_unload(plugin)

    @colony.set_configuration_property_method("service_configuration")
    def service_configuration_set_configuration_property(self, property_name, property):
        self.system.set_service_configuration_property(property)

    @colony.unset_configuration_property_method("service_configuration")
    def service_configuration_unset_configuration_property(self, property_name):
        self.system.unset_service_configuration_property()
