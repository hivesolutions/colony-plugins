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

class ServiceHttpGzipPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Service Gzip plugin.
    """

    id = "pt.hive.colony.plugins.service.http.gzip"
    name = "Http Service Gzip"
    description = "The plugin that offers the http service gzip"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "http_service_encoding"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.gzip", "1.x.x")
    ]
    main_modules = [
        "service_http.gzip.system"
    ]

    service_http_gzip = None
    """ The service http gzip (encoding) """

    gzip_plugin = None
    """ The gzip plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import service_http.gzip.system
        self.service_http_gzip = service_http.gzip.system.ServiceHttpGzip(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_encoding_name(self):
        return self.service_http_gzip.get_encoding_name()

    def encode_contents(self, contents_string):
        return self.service_http_gzip.encode_contents(contents_string)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.gzip")
    def set_gzip_plugin(self, gzip_plugin):
        self.gzip_plugin = gzip_plugin
