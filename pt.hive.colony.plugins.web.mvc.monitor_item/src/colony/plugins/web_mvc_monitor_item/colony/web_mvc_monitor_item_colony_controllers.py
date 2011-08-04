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

WEB_MVC_MONITOR_ITEM_COLONY_RESOURCES_PATH = "web_mvc_monitor_item/colony/resources"
""" The web monitor item colony resources path """

class MainController:
    """
    The web mvc monitor item colony main controller.
    """

    web_mvc_monitor_item_colony_plugin = None
    """ The web mvc monitor item colony plugin """

    web_mvc_monitor_item_colony = None
    """ The web mvc monitor item colony """

    def __init__(self, web_mvc_monitor_item_colony_plugin, web_mvc_monitor_item_colony):
        """
        Constructor of the class.

        @type web_mvc_monitor_item_colony_plugin: WebMvcMonitorItemColonyPlugin
        @param web_mvc_monitor_item_colony_plugin: The web mvc monitor item colony plugin.
        @type web_mvc_monitor_item_colony: WebMvcMonitorItemColony
        @param web_mvc_monitor_item_colony: The web mvc monitor item colony.
        """

        self.web_mvc_monitor_item_colony_plugin = web_mvc_monitor_item_colony_plugin
        self.web_mvc_monitor_item_colony = web_mvc_monitor_item_colony

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MONITOR_ITEM_COLONY_RESOURCES_PATH)

    def get_monitor_item(self, rest_request):
        # retrieves the template file
        template_file = self.retrieve_template_file("monitor_item_colony.html.tpl")

        # assigns the colony variables
        self.__assign_colony_variables(template_file)

        # processes the template file
        processed_template_file = self.process_template_file(rest_request, template_file)

        # returns the processed template file
        return processed_template_file

    def __assign_colony_variables(self, template_file):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_monitor_item_colony_plugin.manager

        # assigns the plugin count to the template
        template_file.assign("plugin_count", len(plugin_manager.get_all_plugins()))

        # assigns the plugin loaded count to the template
        template_file.assign("plugin_loaded_count", len(plugin_manager.get_all_loaded_plugins()))

        # assigns the capabilities count to the template
        template_file.assign("capabilities_count", len(plugin_manager.capabilities_plugins_map))
