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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import os
import psutil

WEB_MVC_MONITOR_ITEM_RESOURCES_RESOURCES_PATH = "web_mvc_monitor_item/resources/resources"
""" The web monitor item resources resources path """

class MainController:
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

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MONITOR_ITEM_RESOURCES_RESOURCES_PATH)

    def get_monitor_item(self, rest_request):
        # retrieves the template file
        template_file = self.retrieve_template_file("monitor_item_resources.html.tpl")

        # assigns the resources variables
        self.__assign_resources_variables(template_file)

        # processes the template file
        processed_template_file = self.process_template_file(rest_request, template_file)

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

        # assigns the template variables
        template_file.assign("memory_usage", memory_usage)
        template_file.assign("cpu_usage", cpu_usage)
