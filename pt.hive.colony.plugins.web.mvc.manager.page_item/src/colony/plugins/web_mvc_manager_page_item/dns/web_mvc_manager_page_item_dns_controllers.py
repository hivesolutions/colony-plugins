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

import colony.libs.importer_util

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_PAGE_ITEM_DNS_RESOURCES_PATH = "web_mvc_manager_page_item/dns/resources"
""" The web mvc manager page item dns resources path """

TEMPLATES_PATH = WEB_MVC_MANAGER_PAGE_ITEM_DNS_RESOURCES_PATH + "/templates"
""" The templates path """

AJAX_ENCODER_NAME = "ajx"
""" The ajax encoder name """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class WebMvcManagerPageItemDnsController:
    """
    The web mvc manager page item dns controller.
    """

    web_mvc_manager_page_item_dns_plugin = None
    """ The web mvc manager page item dns plugin """

    web_mvc_manager_page_item_dns = None
    """ The web mvc manager page item dns """

    def __init__(self, web_mvc_manager_page_item_dns_plugin, web_mvc_manager_page_item_dns):
        """
        Constructor of the class.

        @type web_mvc_manager_page_item_dns_plugin: WebMvcManagerPageItemDnsPlugin
        @param web_mvc_manager_page_item_dns_plugin: The web mvc manager page item dns plugin.
        @type web_mvc_manager_page_item_dns: WebMvcManagerPageItemDns
        @param web_mvc_manager_page_item_dns: The web mvc manager page item dns.
        """

        self.web_mvc_manager_page_item_dns_plugin = web_mvc_manager_page_item_dns_plugin
        self.web_mvc_manager_page_item_dns = web_mvc_manager_page_item_dns

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_page_item_dns_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_page_item_dns_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_page_item_dns_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_page_item_dns_plugin_path + "/" + TEMPLATES_PATH + "/dns"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_show(self, rest_request, parameters = {}):
        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("dns_edit_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # assigns the include to the template
            self.assign_include_template_file(template_file, "page_include", "capability/dns_edit_contents.html.tpl")

            # assigns the include to the template
            self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_update.html.tpl")

        # retrieves the specified capability
        dns = self._get_dns(rest_request)

        # retrieves the respository index
        dns_index = int(rest_request.path_list[-1])

        # assigns the dns to the template
        template_file.assign("dns", dns)

        # assigns the dns index to the template
        template_file.assign("dns_index", dns_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_list(self, rest_request, parameters = {}):
        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("dns_list_contents.html.tpl")
        else:
            # retrieves the template file from the parameters
            template_file = parameters["template_file"]

            # assigns the include to the template
            self.assign_include_template_file(template_file, "page_include", "dns/dns_list_contents.html.tpl")

            # assigns the include to the template
            self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_partial_list(self, rest_request, parameters = {}):
        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the template file
        template_file = self.retrieve_template_file("dns_partial_list_contents.html.tpl")

        # retrieves the filtered dns zones
        filtered_dns_zones = self._get_fitered_dns_zones(rest_request)

        # retrieves the partial filter from the filtered dns zones
        partial_filtered_dns_zones, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_dns_zones)

        # assigns the dns zones to the template
        template_file.assign("dns_zones", partial_filtered_dns_zones)

        # assigns the start record to the template
        template_file.assign("start_record", start_record)

        # assigns the number records to the template
        template_file.assign("number_records", number_records)

        # assigns the total number records to the template
        template_file.assign("total_number_records", total_number_records)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def _get_dns(self, rest_request, index = -1):
        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_page_item_dns_plugin.system_updater_plugin

        # retrieves the dns index from the rest request's path list
        dns_index = int(rest_request.path_list[index])

        # retrieves all the dns zones
        dns_zones = system_updater_plugin.get_dns_zones()

        # retrieves the dns from the dns zones list
        dns = dns_zones[dns_index - 1]

        # retrieves the dns name
        dns_name = dns.name

        # retrieves the dns for the dns with the given name
        dns_information = system_updater_plugin.get_dns_information_by_dns_name(dns_name)

        return dns_information

    def _get_fitered_dns_zones(self, rest_request):
        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        search_query = form_data_map["search_query"]

        # retrieves the dns zones
        dns_zones = self._get_dns_zones()

        # creates the filtered dns zones list
        filtered_dns_zones = []

        # iterates over all the dns zones
        for dns_zone in dns_zones:
            # in case the search query is found in the dns name
            if not dns_zone.name.find(search_query) == -1:
                # adds the dns to the filtered dns zones
                filtered_dns_zones.append(dns_zone)

        # returns the filtered dns zones
        return filtered_dns_zones

    def _get_dns_zones(self):
        return [DnsZone(), DnsZone()]

class DnsZone:
    name = "tobias"

    description = "asdas"

    layout = "nada"
