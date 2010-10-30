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

import web_mvc_communication_push_controllers

class WebMvcCommunicationPush:
    """
    The web mvc communication push class.
    """

    web_mvc_communication_push_plugin = None
    """ The web mvc manager plugin """

    web_mvc_communication_push_controller = None
    """ The web mvc communication push controller """

    def __init__(self, web_mvc_communication_push_plugin):
        """
        Constructor of the class.

        @type web_mvc_communication_push_plugin: WebMvcCommunicationPushPlugin
        @param web_mvc_communication_push_plugin: The web mvc communication push plugin.
        """

        self.web_mvc_communication_push_plugin = web_mvc_communication_push_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_communication_push_plugin.web_mvc_utils_plugin

        # creates the web mvc manager communication push controller
        self.web_mvc_communication_push_controller = web_mvc_utils_plugin.create_controller(web_mvc_communication_push_controllers.WebMvcCommunicationPushController, [self.web_mvc_communication_push_plugin, self], {})

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return ((r"^web_mvc_communication_push/?$", self.web_mvc_communication_push_controller.handle_show),
                (r"^web_mvc_communication_push/register$", self.web_mvc_communication_push_controller.handle_register),
                (r"^web_mvc_communication_push/unregister$", self.web_mvc_communication_push_controller.handle_unregister),
                (r"^web_mvc_communication_push/message$", self.web_mvc_communication_push_controller.handle_message),
                (r"^web_mvc_communication_push/set_property$", self.web_mvc_communication_push_controller.handle_set_property),
                (r"^web_mvc_communication_push/stat$", self.web_mvc_communication_push_controller.handle_stat),
                (r"^web_mvc_communication_push/load_profile$", self.web_mvc_communication_push_controller.handle_load_profile),
                (r"^web_mvc_communication_push/unload_profile$", self.web_mvc_communication_push_controller.handle_unload_profile),
                (r"^web_mvc_communication_push/set_profile$", self.web_mvc_communication_push_controller.handle_set_profile),
                (r"^web_mvc_communication_push/unset_profile$", self.web_mvc_communication_push_controller.handle_unset_profile))

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
