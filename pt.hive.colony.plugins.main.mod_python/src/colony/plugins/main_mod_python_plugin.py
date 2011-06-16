#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class MainModPythonPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Mod Python Main plugin
    """

    id = "pt.hive.colony.plugins.main.mod_python"
    name = "Mod Python Main Plugin"
    short_name = "Mod Python Main"
    description = "Mod Python Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_mod_python/mod_python/resources/baf.xml"
    }
    capabilities = [
        "mod_python",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "http_python_handler"
    ]
    main_modules = [
        "main_mod_python.mod_python.main_mod_python_system"
    ]

    main_mod_python = None
    """ The main mod python """

    http_python_handler_plugins = []
    """ The http python handler plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_mod_python.mod_python.main_mod_python_system
        self.main_mod_python = main_mod_python.mod_python.main_mod_python_system.MainModPython(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def handle_request(self, request, plugin_handler_id):
        return self.main_mod_python.handle_request(request, plugin_handler_id)

    @colony.base.decorators.load_allowed_capability("http_python_handler")
    def http_python_handler_capability_load_allowed(self, plugin, capability):
        self.http_python_handler_plugins.append(plugin)
        self.main_mod_python.http_python_handler_load(plugin)

    @colony.base.decorators.unload_allowed_capability("http_python_handler")
    def http_python_handler_capability_unload_allowed(self, plugin, capability):
        self.http_python_handler_plugins.remove(plugin)
        self.main_mod_python.http_python_handler_unload(plugin)
