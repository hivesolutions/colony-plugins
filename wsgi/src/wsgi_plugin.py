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


class WSGIPlugin(colony.Plugin):
    """
    The main class for the WSGI plugin, providing a bridge between
    WSGI-compliant web servers and the Colony Framework.

    This plugin enables Colony applications to run behind standard
    WSGI servers (e.g., Gunicorn, uWSGI, mod_wsgi) by translating
    the WSGI environ dictionary into Colony request objects and
    forwarding them to the REST plugin for handling.

    The plugin delegates the core logic to the WSGI system class,
    which manages request/response translation, CORS headers, and
    error handling according to PEP 333/3333 specifications.
    """

    id = "pt.hive.colony.plugins.wsgi"
    name = "WSGI"
    description = "Provides the basic mechanism to integrate\
    colony into an WSGI based infra-structure"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT,
    ]
    capabilities = ["wsgi", "test"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.rest")]
    main_modules = ["wsgi"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import wsgi

        self.system = wsgi.WSGI(self)
        self.test = wsgi.WSGITest(self)

    def handle(self, environ, start_response, prefix, alias, rewrite):
        return self.system.handle(environ, start_response, prefix, alias, rewrite)
