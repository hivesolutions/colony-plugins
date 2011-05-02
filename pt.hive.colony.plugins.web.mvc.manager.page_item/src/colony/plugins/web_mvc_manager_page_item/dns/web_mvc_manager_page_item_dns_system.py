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

WEB_MVC_MANAGER_PAGE_ITEM_DNS_RESOURCES_PATH = "web_mvc_manager_page_item/dns/resources"
""" The web mvc manager page item dns resources path """

EXTRAS_PATH = WEB_MVC_MANAGER_PAGE_ITEM_DNS_RESOURCES_PATH + "/extras"
""" The extras path """

class WebMvcManagerPageItemDns:
    """
    The web mvc manager page item dns class.
    """

    web_mvc_manager_page_item_dns_plugin = None
    """ The web mvc manager page item dns plugin """

    web_mvc_manager_page_item_dns_controller = None
    """ The web mvc manager page item dns controller """

    web_mvc_manager_page_item_dns_controllers = None
    """ The web mvc manager page item dns controllers """

    def __init__(self, web_mvc_manager_page_item_dns_plugin):
        """
        Constructor of the class.

        @type web_mvc_manager_page_item_dns_plugin: WebMvcManagerPageItemDnsPlugin
        @param web_mvc_manager_page_item_dns_plugin: The web mvc manager page item dns plugin.
        """

        self.web_mvc_manager_page_item_dns_plugin = web_mvc_manager_page_item_dns_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_manager_page_item_dns_plugin.web_mvc_utils_plugin

        # retrieves the current directory path
        current_directory_path = os.path.dirname(__file__)

        # loads the mvc utils in the web mvc manager page item dns controllers module
        web_mvc_manager_page_item_dns_controllers = web_mvc_utils_plugin.import_module_mvc_utils("web_mvc_manager_page_item_dns_controllers", "web_mvc_manager_page_item.dns", current_directory_path)

        # creates the web mvc manager page item dns controller
        self.web_mvc_manager_page_item_dns_controller = web_mvc_utils_plugin.create_controller(web_mvc_manager_page_item_dns_controllers.WebMvcManagerPageItemDnsController, [self.web_mvc_manager_page_item_dns_plugin, self], {})

        # creates the web mvc manager page item dns controllers
        self.web_mvc_manager_page_item_dns_controllers = {
            "main" : self.web_mvc_manager_page_item_dns_controller
        }

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_page_item_dns_plugin.manager

        # retrieves the web mvc manager page item dns plugin path
        web_mvc_manager_page_item_dns_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_page_item_dns_plugin.id)

        return (
            (r"^web_mvc_manager/resources_page_item_dns/.+$", (web_mvc_manager_page_item_dns_plugin_path + "/" + EXTRAS_PATH, "web_mvc_manager/resources_page_item_dns")),
        )

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
                "pattern" : (r"^web_mvc_manager/dns$", self.web_mvc_manager_page_item_dns_controller.handle_list_ajx, "get", "ajx")
            },
            (r"^web_mvc_manager/dns$", self.web_mvc_manager_page_item_dns_controller.handle_list, "get"),
            (r"^web_mvc_manager/dns/partial$", self.web_mvc_manager_page_item_dns_controller.handle_partial_list, "get"),
            (r"^web_mvc_manager/dns/(?P<dns_index>[0-9]+)$", self.web_mvc_manager_page_item_dns_controller.handle_show_ajx, "get", "ajx"),
            (r"^web_mvc_manager/dns/(?P<dns_index>[0-9]+)$", self.web_mvc_manager_page_item_dns_controller.handle_show, "get")
        )
