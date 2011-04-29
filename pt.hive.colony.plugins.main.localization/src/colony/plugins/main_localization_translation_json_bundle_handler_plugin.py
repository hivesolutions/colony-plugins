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

class MainLocalizationTranslationJsonBundleHandlerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Localization Translation Json Bundle Handler Main plugin
    """

    id = "pt.hive.colony.plugins.main.localization.localization_translation_json_bundle_handler"
    name = "Localization Translation Json Bundle Handler Main Plugin"
    short_name = "Localization Translation Json Bundle Handler Main"
    description = "Localization Translation Json Bundle Handler Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_localization_translation_json_bundle_handler/translation_json_bundle_handler/resources/baf.xml"
    }
    capabilities = [
        "localization_translation_bundle_handler",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.0.0")
    ]
    main_modules = [
        "main_localization_translation_json_bundle_handler.translation_json_bundle_handler.main_localization_translation_json_bundle_handler_system"
    ]

    main_localization_translation_json_bundle_handler = None
    """ The main localization translation json bundle handler """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_localization_translation_json_bundle_handler
        import main_localization_translation_json_bundle_handler.translation_json_bundle_handler.main_localization_translation_json_bundle_handler_system
        self.main_localization_translation_json_bundle_handler = main_localization_translation_json_bundle_handler.translation_json_bundle_handler.main_localization_translation_json_bundle_handler_system.MainLocalizationTranslationJsonBundleHandler(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.main.localization.localization_translation_json_bundle_handler", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        return self.main_localization_translation_json_bundle_handler.get_handler_name()

    def handle_bundle(self, bundle):
        return self.main_localization_translation_json_bundle_handler.handle_bundle(bundle)

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
