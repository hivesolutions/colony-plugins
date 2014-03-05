#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class WsgiPlugin(colony.base.system.Plugin):
    """
    The main class for the Wsgi plugin.
    """

    id = "pt.hive.colony.plugins.wsgi"
    name = "Wsgi"
    description = "Provides the basic mechanism to integrate\
    colony into an wsgi based infra-structure"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "wsgi"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.rest")
    ]
    main_modules = [
        "wsgi.exceptions",
        "wsgi.sytem"
    ]

    wsgi = None
    """ The wsgi """

    rest_plugin = None
    """ The reference to the rest plugin to be used to
    route (and handle) the request to be received """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import wsgi.system
        self.wsgi = wsgi.system.Wsgi(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def handle(self, environ, start_response, prefix, alias):
        return self.wsgi.handle(environ, start_response, prefix, alias)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.rest")
    def set_rest_plugin(self, rest_plugin):
        self.rest_plugin = rest_plugin
