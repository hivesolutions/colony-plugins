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

import os

class WebMvcCommunicationPushApple:
    """
    The web mvc communication push apple class.
    """

    web_mvc_communication_push_apple_plugin = None
    """ The web mvc communication push apple plugin """

    web_mvc_communication_push_apple_controller = None
    """ The web mvc communication push apple controller """

    web_mvc_communication_push_apple_controllers = None
    """ The web mvc communication push apple controllers """

    notification_handler_apple_push_plugins_map = {}
    """ The notification handler apple push plugins map """

    apple_push_configuration_map = {}
    """ The apple push configuration map """

    def __init__(self, web_mvc_communication_push_apple_plugin):
        """
        Constructor of the class.

        @type web_mvc_communication_push_apple_plugin: WebMvcCommunicationPushApplePlugin
        @param web_mvc_communication_push_apple_plugin: The web mvc communication push apple plugin.
        """

        self.web_mvc_communication_push_apple_plugin = web_mvc_communication_push_apple_plugin

        self.notification_handler_apple_push_plugins_map = {}
        self.apple_push_configuration_map = {}

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_communication_push_apple_plugin.web_mvc_utils_plugin

        # retrieves the current directory path
        current_directory_path = os.path.dirname(__file__)

        # loads the mvc utils in the web mvc communication push apple controllers module
        web_mvc_communication_push_apple_controllers = web_mvc_utils_plugin.import_module_mvc_utils("web_mvc_communication_push_apple_controllers", "web_mvc_communication_push_apple.communication_push_apple", current_directory_path)

        # creates the web mvc manager communication push apple controller
        self.web_mvc_communication_push_apple_controller = web_mvc_utils_plugin.create_controller(web_mvc_communication_push_apple_controllers.WebMvcCommunicationPushAppleController, [self.web_mvc_communication_push_apple_plugin, self], {})

        # creates the web mvc communication push apple controllers
        self.web_mvc_communication_push_apple_controllers = {
            "main" : self.web_mvc_communication_push_apple_controller
        }

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return ((r"^web_mvc_communication_push_apple/?$", self.web_mvc_communication_push_apple_controller.handle_show, "get"),
                (r"^web_mvc_communication_push_apple/register$", self.web_mvc_communication_push_apple_controller.handle_register, "post"),
                (r"^web_mvc_communication_push_apple/unregister$", self.web_mvc_communication_push_apple_controller.handle_unregister, "post"),
                (r"^web_mvc_communication_push_apple/load_profile$", self.web_mvc_communication_push_apple_controller.handle_load_profile, "post"),
                (r"^web_mvc_communication_push_apple/unload_profile$", self.web_mvc_communication_push_apple_controller.handle_unload_profile, "post"))

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the web mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return ()

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

    def notification_handler_apple_push_load(self, notification_handler_apple_push_plugin):
        # retrieves the plugin handler name
        handler_name = notification_handler_apple_push_plugin.get_handler_name()

        self.notification_handler_apple_push_plugins_map[handler_name] = notification_handler_apple_push_plugin

    def notification_handler_apple_push_unload(self, notification_handler_apple_push_plugin):
        # retrieves the plugin handler name
        handler_name = notification_handler_apple_push_plugin.get_handler_name()

        del self.notification_handler_apple_push_plugins_map[handler_name]

    def set_configuration_property(self, configuration_propery):
        # retrieves the configuration
        configuration = configuration_propery.get_data()

        # retrieves the apple push configuration map
        apple_push_configuration_map = configuration["apple_push_configuration"]

        # sets the apple push configuration map
        self.apple_push_configuration_map = apple_push_configuration_map

    def unset_configuration_property(self):
        # sets the apple push configuration map
        self.apple_push_configuration_map = {}
