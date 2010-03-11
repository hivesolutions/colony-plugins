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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class WebMvcUtilsPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Web Mvc Utils plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.utils"
    name = "Web Mvc Utils Plugin"
    short_name = "Web Mvc Utils"
    description = "The plugin that offers the top-level abstractions for mvc processing"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["web.mvc.utils"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["web_mvc_utils.mvc_utils.web_mvc_controller", "web_mvc_utils.mvc_utils.web_mvc_model", "web_mvc_utils.mvc_utils.web_mvc_utils_exceptions",
                    "web_mvc_utils.mvc_utils.web_mvc_utils_system"]

    web_mvc_utils = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global web_mvc_utils
        import web_mvc_utils.mvc_utils.web_mvc_utils_system
        self.web_mvc_utils = web_mvc_utils.mvc_utils.web_mvc_utils_system.WebMvcUtils(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_model(self, base_model, base_arguments_list, base_arguments_map):
        return self.web_mvc_utils.create_model(base_model, base_arguments_list, base_arguments_map)

    def create_controller(self, base_controller, base_arguments_list, base_arguments_map):
        return self.web_mvc_utils.create_controller(base_controller, base_arguments_list, base_arguments_map)
