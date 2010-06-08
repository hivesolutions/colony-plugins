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

import psutil
import os

WEB_MVC_MONITOR_ITEM_RESOURCES_RESOURCES_PATH = "web_mvc_monitor_item/resources/resources"
""" The web monitor item resources resources path """

TEMPLATES_PATH = WEB_MVC_MONITOR_ITEM_RESOURCES_RESOURCES_PATH + "/templates"
""" The templates path """

class WebMvcMonitorItemResources:
    """
    The web mvc monitor item resources class.
    """

    web_mvc_monitor_item_resources_plugin = None
    """ The web mvc monitor item resources plugin """

    web_mvc_monitor_item_resources_main_controller = None
    """ The web mvc monitor item resources main controller """

    def __init__(self, web_mvc_monitor_item_resources_plugin):
        """
        Constructor of the class.

        @type web_mvc_monitor_item_resources_plugin: WebMvcMonitorItemResourcesPlugin
        @param web_mvc_monitor_item_resources_plugin: The web mvc monitor item resources plugin.
        """

        self.web_mvc_monitor_item_resources_plugin = web_mvc_monitor_item_resources_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_monitor_item_resources_plugin.web_mvc_utils_plugin

        # creates the web mvc monitor item resources main controller
        self.web_mvc_monitor_item_resources_main_controller = web_mvc_utils_plugin.create_controller(WebMvcMonitorItemResourcesMainController, [self.web_mvc_monitor_item_resources_plugin, self], {})

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

        return self.web_mvc_monitor_item_resources_main_controller.get_monitor_item()

class WebMvcMonitorItemResourcesMainController:
    """
    The web mvc monitor item resources main controller.
    """

    web_mvc_monitor_item_resources_plugin = None
    """ The web mvc monitor item resources plugin """

    web_mvc_monitor_item_resources = None
    """ The web mvc monitor item resources """

    def __init__(self, web_mvc_monitor_item_resources_plugin, web_mvc_monitor_item_resources):
        """
        Constructor of the class.

        @type web_mvc_monitor_item_resources_plugin: WebMvcMonitorItemResourcesPlugin
        @param web_mvc_monitor_item_resources_plugin: The web mvc monitor item resources plugin.
        @type web_mvc_monitor_item_resources: WebMvcMonitorItemResources
        @param web_mvc_monitor_item_resources: The web mvc monitor item resources.
        """

        self.web_mvc_monitor_item_resources_plugin = web_mvc_monitor_item_resources_plugin
        self.web_mvc_monitor_item_resources = web_mvc_monitor_item_resources

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_monitor_item_resources_plugin.manager

        # retrieves the web mvc monitor item resources plugin path
        web_mvc_monitor_item_resources_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_monitor_item_resources_plugin.id)

        # creates the templates path
        templates_path = web_mvc_monitor_item_resources_plugin_path + "/" + TEMPLATES_PATH

        # sets the templates path
        self.set_templates_path(templates_path)

    def get_monitor_item(self):
        # retrieves the template file
        template_file = self.retrieve_template_file("monitor_item_resources.html.tpl")

        # assigns the resources variables
        self.__assign_resources_variables(template_file)

        # processes the template file
        processed_template_file = self.process_template_file(template_file)

        # returns the processed template file
        return processed_template_file

    def __assign_resources_variables(self, template_file):
        # retrieves the current process id
        pid = os.getpid()

        # creates the process representation
        process = psutil.Process(pid)

        # calculates the memory usage in mega bytes
        memory_usage = process.get_memory_info()[0] / 1048576

        # retrieves the cpu usage in percentage
        cpu_usage = process.get_cpu_percent()

        # assigns the memory usage to the template
        template_file.assign("memory_usage", memory_usage)

        # assigns the cpu usage to the template
        template_file.assign("cpu_usage", cpu_usage)
