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

        # creates the controllers for the web mvc monitor item uptime controllers module
        web_mvc_utils_plugin.create_controllers("web_mvc_monitor_item.uptime.web_mvc_monitor_item_uptime_controllers", self, self.web_mvc_monitor_item_uptime_plugin, "web_mvc_monitor_item_uptime")

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
