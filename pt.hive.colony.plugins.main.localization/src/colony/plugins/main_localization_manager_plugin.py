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

__revision__ = "$LastChangedRevision: 5412 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-12 08:06:34 +0100 (seg, 12 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainLocalizationManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Localization Manager Main plugin
    """

    id = "pt.hive.colony.plugins.main.localization.localization_manager"
    name = "Localization Manager Main Plugin"
    short_name = "Localization Manager Main"
    description = "Localization Manager Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_localization_manager/manager/resources/baf.xml"
    }
    capabilities = [
        "localization_manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "localization_handler"
    ]
    main_modules = [
        "main_localization_manager.manager.main_localization_manager_system"
    ]

    main_localization_manager = None
    """ The main localization manager """

    localization_handler_plugins = []
    """ The localization handler plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_localization_manager.manager.main_localization_manager_system
        self.main_localization_manager = main_localization_manager.manager.main_localization_manager_system.MainLocalizationManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.main.localization.localization_manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.main.localization.localization_manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_locale(self, locale_identifier, locale_type, locale_properties):
        return self.main_localization_manager.get_locale(locale_identifier, locale_type, locale_properties)

    @colony.base.decorators.load_allowed_capability("localization_handler")
    def localization_handler_load_allowed(self, plugin, capability):
        self.localization_handler_plugins.append(plugin)
        self.main_localization_manager.load_localization_handler_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("localization_handler")
    def localization_handler_unload_allowed(self, plugin, capability):
        self.localization_handler_plugins.remove(plugin)
        self.main_localization_manager.unload_localization_handler_plugin(plugin)
