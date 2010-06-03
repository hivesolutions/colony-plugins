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
import colony.plugins.decorators

class WebMvcManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Web Mvc Manager plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.manager"
    name = "Web Mvc Manager Plugin"
    short_name = "Web Mvc Manager"
    description = "The plugin that offers the web mvc manager base infrastructure"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["web.mvc_service"]
    capabilities_allowed = ["web.mvc_service.panel_item"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.web.mvc.utils", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.web.mvc.resources.base", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.web.mvc.resources.ui", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.json", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.packing.manager", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.system.updater", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["web_mvc_manager.manager.web_mvc_manager_controllers", "web_mvc_manager.manager.web_mvc_manager_helpers",
                    "web_mvc_manager.manager.web_mvc_manager_system"]

    web_mvc_manager = None

    web_mvc_service_panel_item_plugins = []

    web_mvc_utils_plugin = None
    web_mvc_resources_base_plugin = None
    web_mvc_resources_ui_plugin = None
    json_plugin = None
    packing_manager_plugin = None
    system_updater_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global web_mvc_manager
        import web_mvc_manager.manager.web_mvc_manager_system
        self.web_mvc_manager = web_mvc_manager.manager.web_mvc_manager_system.WebMvcManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.web_mvc_manager.load_components()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.web.mvc.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.web.mvc.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.web.mvc.manager", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_patterns(self):
        """
        Retrieves the map of regular expressions to be used as patters,
        to the web mvc service. The map should relate the route with the handler
        method/function.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return self.web_mvc_manager.get_patterns()

    def get_communication_patterns(self):
        """
        Retrieves the map of regular expressions to be used as communication patters,
        to the web mvc service. The map should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return self.web_mvc_manager.get_communication_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the map of regular expressions to be used as resource patters,
        to the web mvc service. The map should relate the route with the base
        file system path to be used.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return self.web_mvc_manager.get_resource_patterns()

    @colony.plugins.decorators.load_allowed_capability("web.mvc_service.panel_item")
    def web_mvc_service_panel_item_load_allowed(self, plugin, capability):
        self.web_mvc_service_panel_item_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("web.mvc_service.panel_item")
    def web_mvc_service_panel_item_unload_allowed(self, plugin, capability):
        self.web_mvc_service_panel_item_plugins.remove(plugin)

    def get_web_mvc_utils_plugin(self):
        return self.web_mvc_utils_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.utils")
    def set_web_mvc_utils_plugin(self, web_mvc_utils_plugin):
        self.web_mvc_utils_plugin = web_mvc_utils_plugin

    def get_web_mvc_resources_base_plugin(self):
        return self.web_mvc_resources_base_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.resources.base")
    def set_web_mvc_resources_base_plugin(self, web_mvc_resources_base_plugin):
        self.web_mvc_resources_base_plugin = web_mvc_resources_base_plugin

    def get_web_mvc_resources_ui_plugin(self):
        return self.web_mvc_resources_ui_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.resources.ui")
    def set_web_mvc_resources_ui_plugin(self, web_mvc_resources_ui_plugin):
        self.web_mvc_resources_ui_plugin = web_mvc_resources_ui_plugin

    def get_json_plugin(self):
        return self.json_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin

    def get_packing_manager_plugin(self):
        return self.packing_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.packing.manager")
    def set_packing_manager_plugin(self, packing_manager_plugin):
        self.packing_manager_plugin = packing_manager_plugin

    def get_system_updater_plugin(self):
        return self.system_updater_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.system.updater")
    def set_system_updater_plugin(self, system_updater_plugin):
        self.system_updater_plugin = system_updater_plugin
