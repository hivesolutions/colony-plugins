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

class WebMvcManagerDns:
    """
    The web mvc manager dns class.
    """

    web_mvc_manager_dns_plugin = None
    """ The web mvc manager dns plugin """

    def __init__(self, web_mvc_manager_dns_plugin):
        """
        Constructor of the class.

        @type web_mvc_manager_dns_plugin: WebMvcManagerDnsPlugin
        @param web_mvc_manager_dns_plugin: The web mvc manager dns plugin.
        """

        self.web_mvc_manager_dns_plugin = web_mvc_manager_dns_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_manager_dns_plugin.web_mvc_utils_plugin

        # creates the controllers for the web mvc manager dns controller modules
        web_mvc_utils_plugin.create_controllers("web_mvc_manager.dns.web_mvc_manager_dns_controllers", self, self.web_mvc_manager_dns_plugin, "web_mvc_manager_dns")

    def get_page_item_bundle(self, parameters):
        """
        Retrieves a bundle containing all the maps with information
        on all the page items. The maps should contain information
        about the composition of the page item.

        @type parameters: Dictionary
        @param parameters: The parameters to retrieve the page
        item bundle.
        @rtype: List
        @return: A list containing information on all page items.
        """

        return (
            {
                "menu" : "services/Dns",
                "side_panel" : "lists/Dns",
                "base_address" : "dns",
                "pattern" : (r"^web_mvc_manager/dns$", self.web_mvc_manager_dns_dns_controller.handle_list_ajx, "get", "ajx")
            },
            (r"^web_mvc_manager/dns$", self.web_mvc_manager_dns_dns_controller.handle_list, "get"),
            (r"^web_mvc_manager/dns/partial$", self.web_mvc_manager_dns_dns_controller.handle_partial_list_ajx, "get"),
            (r"^web_mvc_manager/dns/(?P<dns_index>[0-9]+)$", self.web_mvc_manager_dns_dns_controller.handle_show_ajx, "get", "ajx"),
            (r"^web_mvc_manager/dns/(?P<dns_index>[0-9]+)$", self.web_mvc_manager_dns_dns_controller.handle_show, "get")
        )
