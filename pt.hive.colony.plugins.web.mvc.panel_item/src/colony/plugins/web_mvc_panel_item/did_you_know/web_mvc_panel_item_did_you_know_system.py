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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

class WebMvcPanelItemDidYouKnow:
    """
    The web mvc panel item did you know class.
    """

    web_mvc_panel_item_did_you_know_plugin = None
    """ The web mvc panel item did you know plugin """

    web_mvc_panel_item_did_you_know_main_controller = None
    """ The web mvc panel item did you know main controller """

    def __init__(self, web_mvc_panel_item_did_you_know_plugin):
        """
        Constructor of the class.

        @type web_mvc_panel_item_did_you_know_plugin: WebMvcPanelItemDidYouKnowPlugin
        @param web_mvc_panel_item_did_you_know_plugin: The web mvc panel item did you know plugin
        """

        self.web_mvc_panel_item_did_you_know_plugin = web_mvc_panel_item_did_you_know_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_panel_item_did_you_know_plugin.web_mvc_utils_plugin

        # creates the web mvc panel item did you know main controller
        #self.web_mvc_panel_item_did_you_know_main_controller = web_mvc_utils_plugin.create_controller(WebMvcManagerMainController, [self.web_mvc_manager_plugin, self], {})

    def get_patterns(self):
        """
        Retrieves the map of regular expressions to be used as patters,
        to the web mvc service. The map should relate the route with the handler
        method/function.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return {}

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

        return {}

    def get_resource_patterns(self):
        """
        Retrieves the map of regular expressions to be used as resource patters,
        to the web mvc service. The map should relate the route with the base
        file system path to be used.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return {}

    def get_panel_item(self, parameters):
        return "<div id=\"tobias\"></div>"
