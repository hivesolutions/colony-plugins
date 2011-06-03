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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class WebMvcPanelItemMonitor:
    """
    The web mvc panel item monitor class.
    """

    web_mvc_panel_item_monitor_plugin = None
    """ The web mvc panel item monitor plugin """

    web_mvc_panel_item_monitor_main_controller = None
    """ The web mvc panel item monitor main controller """

    def __init__(self, web_mvc_panel_item_monitor_plugin):
        """
        Constructor of the class.

        @type web_mvc_panel_item_monitor_plugin: WebMvcPanelItemMonitorPlugin
        @param web_mvc_panel_item_monitor_plugin: The web mvc panel item monitor plugin.
        """

        self.web_mvc_panel_item_monitor_plugin = web_mvc_panel_item_monitor_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_panel_item_monitor_plugin.web_mvc_utils_plugin

        # creates the controllers for the web mvc panel item monitor controllers module
        web_mvc_utils_plugin.create_controllers("web_mvc_panel_item.monitor.web_mvc_panel_item_monitor_controllers", self, self.web_mvc_panel_item_monitor_plugin, "web_mvc_panel_item_monitor")

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return ()

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

        return self.web_mvc_panel_item_monitor_main_controller.get_panel_item()

    def load_web_mvc_monitor_item_plugin(self, web_mvc_monitor_item_plugin):
        """
        Loads the given web mvc monitor item plugin.

        @type web_mvc_monitor_item_plugin: Plugin
        @param web_mvc_monitor_item_plugin: The web mvc monitor item plugin to be loaded.
        """

        self.web_mvc_panel_item_monitor_plugin.generate_event("web.mvc.side_panel_reload", [])

    def unload_web_mvc_monitor_item_plugin(self, web_mvc_monitor_item_plugin):
        """
        Unloads the given web mvc monitor item plugin.

        @type web_mvc_monitor_item_plugin: Plugin
        @param web_mvc_monitor_item_plugin: The web mvc monitor item plugin to be loaded.
        """

        self.web_mvc_panel_item_monitor_plugin.generate_event("web.mvc.side_panel_reload", [])
