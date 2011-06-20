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

SERIALIZER_VALUE = "serializer"
""" The serializer value """

TEMPLATE_FILE_VALUE = "template_file"
""" The template file value """

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_DNS_RESOURCES_PATH = "web_mvc_manager/dns/resources"
""" The web mvc manager dns resources path """

PATTERN_NAMES_VALUE = "pattern_names"
""" The pattern names value """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class DnsController:
    """
    The web mvc manager dns controller.
    """

    web_mvc_manager_dns_plugin = None
    """ The web mvc manager dns plugin """

    web_mvc_manager_dns = None
    """ The web mvc manager dns """

    def __init__(self, web_mvc_manager_dns_plugin, web_mvc_manager_dns):
        """
        Constructor of the class.

        @type web_mvc_manager_dns_plugin: WebMvcManagerDnsPlugin
        @param web_mvc_manager_dns_plugin: The web mvc manager dns plugin.
        @type web_mvc_manager_dns: WebMvcManagerDns
        @param web_mvc_manager_dns: The web mvc manager dns.
        """

        self.web_mvc_manager_dns_plugin = web_mvc_manager_dns_plugin
        self.web_mvc_manager_dns = web_mvc_manager_dns

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_DNS_RESOURCES_PATH, extra_templates_path = "dns")

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return []

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("dns.show")
    def handle_show_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_dns_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the pattern names
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the dns index patterns
        dns_index = pattern_names["dns_index"]

        # converts the dns index to integer
        dns_index = int(dns_index)

        # retrieves the specified capability
        dns = self._get_dns(rest_request, dns_index)

        # retrieves the template file
        template_file = self.retrieve_template_file("dns_edit_contents.html.tpl")

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

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("dns.show")
    def handle_show(self, rest_request, parameters = {}):
        # retrieves the pattern names
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the dns index patterns
        dns_index = pattern_names["dns_index"]

        # converts the dns index to integer
        dns_index = int(dns_index)

        # retrieves the specified capability
        dns = self._get_dns(rest_request, dns_index)

        # retrieves the template file from the parameters
        template_file = parameters[TEMPLATE_FILE_VALUE]

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_DNS_RESOURCES_PATH, "templates/dns/dns_edit_contents.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)

        # assigns the include to the template
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_update.html.tpl")

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

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("dns.list")
    def handle_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_dns_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the template file
        template_file = self.retrieve_template_file("dns_list_contents.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("dns.list")
    def handle_list(self, rest_request, parameters = {}):
        # retrieves the template file from the parameters
        template_file = parameters[TEMPLATE_FILE_VALUE]

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_DNS_RESOURCES_PATH, "templates/dns/dns_list_contents.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("dns.list")
    def handle_partial_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_dns_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the start record
        start_record = form_data_map["start_record"]

        # retrieves the number records
        number_records = form_data_map["number_records"]

        # converts the start record to integer
        start_record = int(start_record)

        # converts the number records to integer
        number_records = int(number_records)

        # retrieves the filtered dns zones
        filtered_dns_zones = self._get_filtered_dns_zones(rest_request)

        # retrieves the partial filter from the filtered dns zones
        partial_filtered_dns_zones, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_dns_zones, start_record, number_records)

        # retrieves the template file
        template_file = self.retrieve_template_file("dns_partial_list_contents.html.tpl")

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

    def _get_dns(self, rest_request, dns_index):
        # returns the dns information
        return DnsZone()

    def _get_filtered_dns_zones(self, rest_request):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the search query
        search_query = form_data_map["search_query"]

        # retrieves the dns zones
        dns_zones = self._get_dns_zones()

        # creates the filtered dns zones list
        filtered_dns_zones = [dns_zone for dns_zone in dns_zones if not dns_zone.name.find(search_query) == -1]

        # returns the filtered dns zones
        return filtered_dns_zones

    def _get_dns_zones(self):
        return [
            DnsZone()
        ]

class DnsZone:
    """
    The dns zone class.
    """

    name = "name"
    """ The name of the zone """

    description = "description"
    """ The description of the zone """

    layout = "layout"
    """ The layout of the zone """
