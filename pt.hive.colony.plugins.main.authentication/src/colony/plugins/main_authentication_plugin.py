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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2318 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:29:06 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class MainAuthenticationPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Authentication Main plugin.
    """

    id = "pt.hive.colony.plugins.main.authentication"
    name = "Authentication Main Plugin"
    short_name = "Authentication Main"
    description = "Plugin that provides the authentication front-end mechanisms"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_authentication/authentication/resources/baf.xml"}
    capabilities = ["authentication", "build_automation_item"]
    capabilities_allowed = ["authentication_handler"]
    dependencies = []
    events_handled = []
    events_registrable = []

    main_authentication = None

    authentication_handler_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_authentication
        import main_authentication.authentication.main_authentication_system
        self.main_authentication = main_authentication.authentication.main_authentication_system.MainAuthentication(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.main.authentication", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.main.authentication", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def authenticate_user(self, username, password, authentication_handler, arguments):
        return self.main_authentication.authenticate_user(username, password, authentication_handler, arguments)

    def process_authentication_string(self, authentication_string):
        return self.main_authentication.process_authentication_string(authentication_string)

    @colony.plugins.decorators.load_allowed_capability("authentication_handler")
    def authentication_handler_load_allowed(self, plugin, capability):
        self.authentication_handler_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("authentication_handler")
    def authentication_handler_unload_allowed(self, plugin, capability):
        self.authentication_handler_plugins.remove(plugin)
