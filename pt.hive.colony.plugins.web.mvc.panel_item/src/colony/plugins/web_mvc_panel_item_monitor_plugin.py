#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import colony.base.plugin_system
import colony.base.decorators

class WebMvcPanelItemMonitorPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Web Mvc Panel Item Monitor plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.panel_item.monitor"
    name = "Web Mvc Panel Item Monitor Plugin"
    short_name = "Web Mvc Panel Item Monitor"
    description = "The plugin that offers the web mvc panel item monitor"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/web_mvc_panel_item/monitor/resources/baf.xml"
    }
    capabilities = [
        "web.mvc.panel_item",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "web.mvc.monitor_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.web.mvc.utils", "1.0.0")
    ]
    events_fired = [
        "web.mvc.side_panel_reload"
    ]
    main_modules = [
        "web_mvc_panel_item.monitor.web_mvc_panel_item_monitor_controllers",
        "web_mvc_panel_item.monitor.web_mvc_panel_item_monitor_system"
    ]

    web_mvc_panel_item_monitor = None
    """ The web mvc panel item monitor """

    web_mvc_monitor_item_plugins = []
    """ The web mvc monitor item plugins """

    web_mvc_utils_plugin = None
    """ The web mvc utils plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import web_mvc_panel_item.monitor.web_mvc_panel_item_monitor_system
        self.web_mvc_panel_item_monitor = web_mvc_panel_item.monitor.web_mvc_panel_item_monitor_system.WebMvcPanelItemMonitor(self)

        # initializes the structures
        self.web_mvc_monitor_item_plugins = []

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.web_mvc_panel_item_monitor.load_components()

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_panel_item(self, parameters):
        """
        Retrieves the code for the panel item for
        the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to retrieve the code for
        the panel item.
        @rtype: String
        @return: The code for the monitor item.
        """

        return self.web_mvc_panel_item_monitor.get_panel_item(parameters)

    @colony.base.decorators.load_allowed_capability("web.mvc.monitor_item")
    def web_mvc_monitor_item_load_allowed(self, plugin, capability):
        self.web_mvc_monitor_item_plugins.append(plugin)
        self.web_mvc_panel_item_monitor.load_web_mvc_monitor_item_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("web.mvc.monitor_item")
    def web_mvc_monitor_item_unload_allowed(self, plugin, capability):
        self.web_mvc_monitor_item_plugins.remove(plugin)
        self.web_mvc_panel_item_monitor.unload_web_mvc_monitor_item_plugin(plugin)

    def get_web_mvc_utils_plugin(self):
        return self.web_mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.utils")
    def set_web_mvc_utils_plugin(self, web_mvc_utils_plugin):
        self.web_mvc_utils_plugin = web_mvc_utils_plugin
