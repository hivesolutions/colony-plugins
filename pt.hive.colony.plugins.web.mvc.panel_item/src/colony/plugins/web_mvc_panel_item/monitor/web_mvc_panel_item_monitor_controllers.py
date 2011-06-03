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

WEB_MVC_PANEL_ITEM_MONITOR_RESOURCES_PATH = "web_mvc_panel_item/monitor/resources"
""" The web panel item monitor resources path """

class MainController:
    """
    The web mvc panel item monitor main controller.
    """

    web_mvc_panel_item_monitor_plugin = None
    """ The web mvc panel item monitor plugin """

    web_mvc_panel_item_monitor = None
    """ The web mvc panel item monitor """

    def __init__(self, web_mvc_panel_item_monitor_plugin, web_mvc_panel_item_monitor):
        """
        Constructor of the class.

        @type web_mvc_panel_item_monitor_plugin: WebMvcPanelItemMonitorPlugin
        @param web_mvc_panel_item_monitor_plugin: The web mvc panel item monitor plugin.
        @type web_mvc_panel_item_monitor: WebMvcPanelItemDidYouMonitor
        @param web_mvc_panel_item_monitor: The web mvc panel item monitor.
        """

        self.web_mvc_panel_item_monitor_plugin = web_mvc_panel_item_monitor_plugin
        self.web_mvc_panel_item_monitor = web_mvc_panel_item_monitor

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_PANEL_ITEM_MONITOR_RESOURCES_PATH)

    def get_panel_item(self):
        # retrieves the template file
        template_file = self.retrieve_template_file("panel_item_monitor.html.tpl")

        # assigns the monitor variables
        self.__assign_monitor_item_variables(template_file)

        # processes the template file
        processed_template_file = self.process_template_file(template_file)

        # returns the processed template file
        return processed_template_file

    def __assign_monitor_item_variables(self, template_file):
        # retrieves the web mvc monitor item plugins
        web_mvc_monitor_item_plugins = self.web_mvc_panel_item_monitor_plugin.web_mvc_monitor_item_plugins

        # starts the monitor items list
        monitor_items_list = []

        # iterates over all the web mvc monitor item plugins
        for web_mvc_monitor_item_plugin in web_mvc_monitor_item_plugins:
            monitor_item = web_mvc_monitor_item_plugin.get_monitor_item({})
            monitor_items_list.append(monitor_item)

        # assigns the monitor items to the template
        template_file.assign("monitor_items", monitor_items_list)
