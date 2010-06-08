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

WEB_MVC_MONITOR_ITEM_COLONY_RESOURCES_PATH = "web_mvc_monitor_item/colony/resources"
""" The web monitor item colony resources path """

TEMPLATES_PATH = WEB_MVC_MONITOR_ITEM_COLONY_RESOURCES_PATH + "/templates"
""" The templates path """

class WebMvcMonitorItemColony:
    """
    The web mvc monitor item colony class.
    """

    web_mvc_monitor_item_colony_plugin = None
    """ The web mvc monitor item colony plugin """

    web_mvc_monitor_item_colony_main_controller = None
    """ The web mvc monitor item colony main controller """

    def __init__(self, web_mvc_monitor_item_colony_plugin):
        """
        Constructor of the class.

        @type web_mvc_monitor_item_colony_plugin: WebMvcMonitorItemColonyPlugin
        @param web_mvc_monitor_item_colony_plugin: The web mvc monitor item colony plugin.
        """

        self.web_mvc_monitor_item_colony_plugin = web_mvc_monitor_item_colony_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_monitor_item_colony_plugin.web_mvc_utils_plugin

        # creates the web mvc monitor item colony main controller
        self.web_mvc_monitor_item_colony_main_controller = web_mvc_utils_plugin.create_controller(WebMvcMonitorItemColonyMainController, [self.web_mvc_monitor_item_colony_plugin, self], {})

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

        return self.web_mvc_monitor_item_colony_main_controller.get_monitor_item()

class WebMvcMonitorItemColonyMainController:
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

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_monitor_item_colony_plugin.manager

        # retrieves the web mvc monitor item colony plugin path
        web_mvc_monitor_item_colony_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_monitor_item_colony_plugin.id)

        # creates the templates path
        templates_path = web_mvc_monitor_item_colony_plugin_path + "/" + TEMPLATES_PATH

        # sets the templates path
        self.set_templates_path(templates_path)

    def get_monitor_item(self):
        # retrieves the template file
        template_file = self.retrieve_template_file("monitor_item_colony.html.tpl")

        # assigns the colony variables
        self.__assign_colony_variables(template_file)

        # processes the template file
        processed_template_file = self.process_template_file(template_file)

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
