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


class ServiceHTTPTemplateErrorPlugin(colony.Plugin):
    """
    The main class for the HTTP Service Template Error plugin.
    """

    id = "pt.hive.colony.plugins.service.http.template_error"
    name = "HTTP Service Template Error"
    description = "The plugin that offers the HTTP service template error"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT,
    ]
    capabilities = ["http_service_error_handler"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.template_engine")]
    main_modules = ["service_http_template_error"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import service_http_template_error

        self.system = service_http_template_error.ServiceHTTPTemplateError(self)

    def get_error_handler_name(self):
        return self.system.get_error_handler_name()

    def handle_error(self, request, error):
        return self.system.handle_error(request, error)
