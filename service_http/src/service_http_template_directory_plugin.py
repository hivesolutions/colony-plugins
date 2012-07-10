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

class ServiceHttpTemplateDirectoryPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Service Template Directory plugin.
    """

    id = "pt.hive.colony.plugins.service.http.template_directory"
    name = "Http Service Template Directory"
    description = "The plugin that offers the http service template directory"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "directory_handler"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.template_engine", "1.x.x")
    ]
    main_modules = [
        "service_http.template_directory.system"
    ]

    service_http_template_directory = None
    """ The service http template directory (handler) """

    template_engine_plugin = None
    """ The template engine plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import service_http.template_directory.system
        self.service_http_template_directory = service_http.template_directory.system.ServiceHttpTemplateDirectory(self) 

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_directory_handler_name(self):
        return self.service_http_template_directory.get_directory_handler_name()

    def handle_directory_list(self, request, directory_list):
        return self.service_http_template_directory.handle_directory_list(request, directory_list)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.template_engine")
    def set_template_engine_plugin(self, template_engine_plugin):
        self.template_engine_plugin = template_engine_plugin
