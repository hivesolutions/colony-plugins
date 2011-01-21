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

import time
import copy

import colony.libs.importer_util

import web_mvc_manager_page_item_dns_exceptions

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

JSON_ENCODER_NAME = "json"
""" The json encoder name """

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

            # sets the page to be included
            template_file.assign("page_include", "capability/dns_edit_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_update.html.tpl")

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

            # sets the page to be included
            template_file.assign("page_include", "dns/dns_list_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

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

        # retrieves the filtered repositories
        filtered_repositories = self._get_fitered_repositories(rest_request)

        # retrieves the partial filter from the filtered repositories
        partial_filtered_repositories, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_repositories)

        # assigns the repositories to the template
        template_file.assign("repositories", partial_filtered_repositories)

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

    def handle_install_plugin(self, rest_request, parameters = {}):
        # in case the encoder name is ajax
        if rest_request.encoder_name == JSON_ENCODER_NAME:
            # retrieves the json plugin
            json_plugin = self.web_mvc_manager_page_item_dns_plugin.json_plugin

            # retrieves the communication helper
            communication_helper = parameters["communication_helper"]

            # install the plugin and retrieves the result
            install_plugin_result = self._install_plugin(rest_request)

            # serializes the install result using the json plugin
            serialized_status = json_plugin.dumps(install_plugin_result)

            # sets the serialized status as the rest request contents
            self.set_contents(rest_request, serialized_status)

            # sends the serialized broadcast message
            communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/install", serialized_status)

            return True

        return True

    def handle_plugins_partial_list(self, rest_request, parameters = {}):
        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the template file
        template_file = self.retrieve_template_file("dns_plugins_partial_list_contents.html.tpl")

        # retrieves the filtered repositories
        filtered_dns_plugins = self._get_fitered_dns_plugins(rest_request)

        # retrieves the partial filter from the filtered dns plugins
        partial_filtered_dns_plugins, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_dns_plugins)

        # assigns the repositories to the template
        template_file.assign("dns_plugins", partial_filtered_dns_plugins)

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

    def handle_packages_partial_list(self, rest_request, parameters = {}):
        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the template file
        template_file = self.retrieve_template_file("dns_partial_list_contents.html.tpl")

        # retrieves the filtered repositories
        filtered_repositories = self._get_fitered_repositories(rest_request)

        # retrieves the partial filter from the filtered repositories
        partial_filtered_repositories, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_repositories)

        # assigns the repositories to the template
        template_file.assign("repositories", partial_filtered_repositories)

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

        # retrieves all the repositories
        repositories = system_updater_plugin.get_repositories()

        # retrieves the dns from the repositories list
        dns = repositories[dns_index - 1]

        # retrieves the dns name
        dns_name = dns.name

        # retrieves the dns for the dns with the given name
        dns_information = system_updater_plugin.get_dns_information_by_dns_name(dns_name)

        return dns_information

    def _get_fitered_repositories(self, rest_request):
        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        search_query = form_data_map["search_query"]

        # retrieves the repositories
        repositories = self._get_repositories()

        # creates the filtered repositories list
        filtered_repositories = []

        # iterates over all the repositories
        for dns in repositories:
            # in case the search query is found in the dns name
            if not dns.name.find(search_query) == -1:
                # adds the dns to the filtered repositories
                filtered_repositories.append(dns)

        # returns the filtered repositories
        return filtered_repositories

    def _get_fitered_dns_plugins(self, rest_request):
        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        search_query = form_data_map["search_query"]

        # retrieves the dns
        dns = self._get_dns(rest_request, -2)

        # creates the filtered dns plugins
        filtered_dns_plugins = []

        # iterates over all the dns plugins
        for dns_plugin in dns.plugins:
            # in case the search query is found in the dns plugin id
            if not dns_plugin.id.find(search_query) == -1:
                # adds the dns plugin to the filtered dns plugins
                filtered_dns_plugins.append(dns_plugin)

        return filtered_dns_plugins

    def _get_repositories(self):
        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_page_item_dns_plugin.system_updater_plugin

        # retrieves all the repositories
        repositories = system_updater_plugin.get_repositories()

        return repositories

    def _install_plugin(self, rest_request):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_page_item_dns_plugin.manager

        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_page_item_dns_plugin.system_updater_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        plugin_id = form_data_map["plugin_id"]
        plugin_version = form_data_map["plugin_version"]

        # creates the delta plugin install map
        delta_plugin_install_map = {"installed" : [], "uninstalled" : []}

        # retrieves the (beginning) list of available plugins
        available_plugins_beginning = copy.copy(plugin_manager.get_all_plugins())

        # tries to install the plugin
        return_value = system_updater_plugin.install_plugin(plugin_id, plugin_version)

        # sleeps for a second to give time for the autoloader to update
        time.sleep(1.0)

        # in case the return value is not valid
        if not return_value:
            # raises a runtime exception
            raise web_mvc_manager_page_item_dns_exceptions.RuntimeException("problem installing plugin")

        # retrieves the (end) list of available plugins
        available_plugins_end = plugin_manager.get_all_plugins()

        # iterates over all the plugins available at the beginning
        # to check if they exist in the current available plugins
        for available_plugin_beginning in available_plugins_beginning:
            if not available_plugin_beginning in available_plugins_end:
                delta_plugin_install_map["uninstalled"].append(available_plugin_beginning.id)

        # iterates over all the plugins available at the end
        # to check if they exist in the previously available plugins
        for available_plugin_end in available_plugins_end:
            if not available_plugin_end in available_plugins_beginning:
                delta_plugin_install_map["installed"].append(available_plugin_end.id)

        # returns the delta plugin install map
        return delta_plugin_install_map
