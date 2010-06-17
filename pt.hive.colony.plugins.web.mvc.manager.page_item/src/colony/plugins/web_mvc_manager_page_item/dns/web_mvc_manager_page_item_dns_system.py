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

import colony.libs.map_util

import web_mvc_manager_page_item_dns_controllers

WEB_MVC_MANAGER_PAGE_ITEM_DNS_RESOURCES_PATH = "web_mvc_manager_page_item/dns/resources"
""" The web mvc manager page item dns resources path """

EXTRAS_PATH = WEB_MVC_MANAGER_PAGE_ITEM_DNS_RESOURCES_PATH + "/extras"
""" The extras path """

DNS_LIST_PAGE_ITEM_ATTRIBUTES = {"menu" : "services/Dns",
                                 "side_panel" : "lists/Dns",
                                 "base_address" : "dns",
                                 "pattern" : (r"^web_mvc_manager/dns$", 1)}
""" The dns list page item attributes """

DNS_SHOW_PAGE_ITEM_ATTRIBUTES = {"pattern" : (r"^web_mvc_manager/dns/[a-zA-Z0-9.]+$", 2)}
""" The dns show page item attributes """

DNS_PARTIAL_LIST_PAGE_ITEM_ATTRIBUTES = {"pattern" : (r"^web_mvc_manager/dns/partial$", 3)}
""" The dns partial list page item attributes """

DNS_RECORDS_PARTIAL_ITEM_ATTRIBUTES = {"pattern" : (r"^web_mvc_manager/dns/[a-zA-Z0-9.]+/records_partial$", 5)}
""" The dns plugins partial page item attributes """

class WebMvcManagerPageItemDns:
    """
    The web mvc manager page item dns class.
    """

    web_mvc_manager_page_item_dns_plugin = None
    """ The web mvc manager page item dns plugin """

    web_mvc_manager_page_item_dns_controller = None
    """ The web mvc manager page item dns controller """

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

        # creates the web mvc manager page item dns controller
        self.web_mvc_manager_page_item_dns_controller = web_mvc_utils_plugin.create_controller(web_mvc_manager_page_item_dns_controllers.WebMvcManagerPageItemDnsController, [self.web_mvc_manager_page_item_dns_plugin, self], {})

    def get_resource_patterns(self):
        """
        Retrieves the map of regular expressions to be used as resource patters,
        to the web mvc service. The map should relate the route with the base
        file system path to be used.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_page_item_dns_plugin.manager

        # retrieves the web mvc manager page item dns plugin path
        web_mvc_manager_page_item_dns_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_page_item_dns_plugin.id)

        return {r"^web_mvc_manager/resources_page_item_dns/.+$" : (web_mvc_manager_page_item_dns_plugin_path + "/" + EXTRAS_PATH, "web_mvc_manager/resources_page_item_dns")}

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

        # creates the dns page item maps
        dns_list_page_item_map = colony.libs.map_util.map_extend(DNS_LIST_PAGE_ITEM_ATTRIBUTES, {"action" : self.web_mvc_manager_page_item_dns_controller.handle_list})
        dns_show_page_item_map = colony.libs.map_util.map_extend(DNS_SHOW_PAGE_ITEM_ATTRIBUTES, {"action" : self.web_mvc_manager_page_item_dns_controller.handle_show})
        dns_partial_list_page_item_map = colony.libs.map_util.map_extend(DNS_PARTIAL_LIST_PAGE_ITEM_ATTRIBUTES, {"action" : self.web_mvc_manager_page_item_dns_controller.handle_partial_list})
        dns_records_partial_page_item_map = colony.libs.map_util.map_extend(DNS_RECORDS_PARTIAL_ITEM_ATTRIBUTES, {"action" : self.web_mvc_manager_page_item_dns_controller.handle_install_plugin})

        return [dns_list_page_item_map, dns_show_page_item_map,
                dns_partial_list_page_item_map, dns_records_partial_page_item_map]
