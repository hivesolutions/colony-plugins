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

import time

import colony.libs.time_util

WEB_MVC_MONITOR_ITEM_UPTIME_RESOURCES_PATH = "web_mvc_monitor_item/uptime/resources"
""" The web monitor item uptime resources path """

TEMPLATES_PATH = WEB_MVC_MONITOR_ITEM_UPTIME_RESOURCES_PATH + "/templates"
""" The templates path """

class WebMvcMonitorItemUptime:
    """
    The web mvc monitor item uptime class.
    """

    web_mvc_monitor_item_uptime_plugin = None
    """ The web mvc monitor item uptime plugin """

    web_mvc_monitor_item_uptime_main_controller = None
    """ The web mvc monitor item uptime main controller """

    def __init__(self, web_mvc_monitor_item_uptime_plugin):
        """
        Constructor of the class.

        @type web_mvc_monitor_item_uptime_plugin: WebMvcMonitorItemUptimePlugin
        @param web_mvc_monitor_item_uptime_plugin: The web mvc monitor item uptime plugin.
        """

        self.web_mvc_monitor_item_uptime_plugin = web_mvc_monitor_item_uptime_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_monitor_item_uptime_plugin.web_mvc_utils_plugin

        # creates the web mvc monitor item uptime main controller
        self.web_mvc_monitor_item_uptime_main_controller = web_mvc_utils_plugin.create_controller(WebMvcMonitorItemUptimeMainController, [self.web_mvc_monitor_item_uptime_plugin, self], {})

    def get_monitor_item(self, parameters):
        """
        Retrieves the code for the monitor item for
        the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to retrieve the code for
        the monitor item.
        @rtype: String
        @return: The code for the monitor item.
        """

        return self.web_mvc_monitor_item_uptime_main_controller.get_monitor_item()

class WebMvcMonitorItemUptimeMainController:
    """
    The web mvc monitor item uptime main controller.
    """

    web_mvc_monitor_item_uptime_plugin = None
    """ The web mvc monitor item uptime plugin """

    web_mvc_monitor_item_uptime = None
    """ The web mvc monitor item uptime """

    def __init__(self, web_mvc_monitor_item_uptime_plugin, web_mvc_monitor_item_uptime):
        """
        Constructor of the class.

        @type web_mvc_monitor_item_uptime_plugin: WebMvcMonitorItemUptimePlugin
        @param web_mvc_monitor_item_uptime_plugin: The web mvc monitor item uptime plugin.
        @type web_mvc_monitor_item_uptime: WebMvcMonitorItemUptime
        @param web_mvc_monitor_item_uptime: The web mvc monitor item uptime.
        """

        self.web_mvc_monitor_item_uptime_plugin = web_mvc_monitor_item_uptime_plugin
        self.web_mvc_monitor_item_uptime = web_mvc_monitor_item_uptime

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_monitor_item_uptime_plugin.manager

        # retrieves the web mvc monitor item uptime plugin path
        web_mvc_monitor_item_uptime_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_monitor_item_uptime_plugin.id)

        # creates the templates path
        templates_path = web_mvc_monitor_item_uptime_plugin_path + "/" + TEMPLATES_PATH

        # sets the templates path
        self.set_templates_path(templates_path)

    def get_monitor_item(self):
        # retrieves the template file
        template_file = self.retrieve_template_file("monitor_item_uptime.html.tpl")

        # assigns the uptime variables
        self.__assign_uptime_variables(template_file)

        # processes the template file
        processed_template_file = self.process_template_file(template_file)

        # returns the processed template file
        return processed_template_file

    def __assign_uptime_variables(self, template_file):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_monitor_item_uptime_plugin.manager

        # retrieves the current time
        current_time = time.time()

        # calculates the uptime
        uptime = current_time - plugin_manager.plugin_manager_timestamp

        # creates the uptime string
        uptime_string = colony.libs.time_util.format_seconds_smart(uptime, "basic", ("day", "hour", "minute"))

        # assigns the uptime to the template
        template_file.assign("uptime", uptime_string)
