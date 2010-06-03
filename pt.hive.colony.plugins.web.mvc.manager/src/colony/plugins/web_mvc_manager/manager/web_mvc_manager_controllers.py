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

import copy
import random

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_RESOURCES_PATH = "web_mvc_manager/manager/resources"
""" The web mvc manager resources path """

TEMPLATES_PATH = WEB_MVC_MANAGER_RESOURCES_PATH + "/templates"
""" The templates path """

AJAX_ENCODER_NAME = "ajx"
""" The ajax encoder name """

JSON_ENCODER_NAME = "json"
""" The json encoder name """

PLUGINS_DIRECTORY = "colony/plugins"
""" The plugins directory value """

LOAD_VALUE = "load"
""" The load value """

UNLOAD_VALUE = "unload"
""" The unload value """

LOADED_VALUE = "loaded"
""" The loaded value """

UNLOADED_VALUE = "unloaded"
""" The unloaded value """

PROVIDING_VALUE = "providing"
""" The providing value """

ALLOWING_VALUE = "allowing"
""" The allowing value """

DID_YOU_KNOW_LIST = ("Chuck Norris once shot down a German fighter plane with his finger, by yelling, \"Bang!\"",
                     "A Handicapped parking sign does not signify that this spot is for handicapped people. It is actually in fact a warning, that the spot belongs to Chuck Norris and that you will be handicapped if you park there.",
                     "Everybody loves Raymond. Except Chuck Norris.",
                     "Chuck Norris once round-house kicked a salesman. Over the phone.")
""" The list of did you know sentences """

class SidePanelController:
    """
    The side panel controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/side_panel"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_update(self, rest_request, parameters = {}):
        """
        Handles the given update rest request.

        @type rest_request: RestRequest
        @param rest_request: The take the bill index rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("side_panel_update.html.tpl")

        # assigns the update variables
        self._assign_update_variables(template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_configuration(self, rest_request, parameters = {}):
        """
        Handles the given configuration rest request.

        @type rest_request: RestRequest
        @param rest_request: The take the bill index rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("side_panel_configuration.html.tpl")

        # assigns the configuration variables
        self._assign_configuration_variables(template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def _assign_update_variables(self, template_file):
        self.__assign_status_variables(template_file)
        self.__assign_did_you_know_variables(template_file)

    def _assign_configuration_variables(self, template_file):
        self.__assign_status_variables(template_file)
        self.__assign_did_you_know_variables(template_file)

    def __assign_status_variables(self, template_file):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # assigns the plugin count to the template
        template_file.assign("plugin_count", len(plugin_manager.get_all_plugins()))

        # assigns the plugin loaded count to the template
        template_file.assign("plugin_loaded_count", len(plugin_manager.get_all_loaded_plugins()))

        # assigns the capabilities count to the template
        template_file.assign("capabilities_count", len(plugin_manager.capabilities_plugins_map))

        import psutil
        import os
        import time

        pid = os.getpid()

        process = psutil.Process(pid)

        # calculates the memory usage in mega bytes
        memory_usage = process.get_memory_info()[0] / 1048576

        cpu_usage = process.get_cpu_percent()

        # assigns the memory usage to the template
        template_file.assign("memory_usage", memory_usage)

        # assigns the cpu usage to the template
        template_file.assign("cpu_usage", cpu_usage)

        # retrieves the current time
        current_time = time.time()

        uptime = current_time - plugin_manager.plugin_manager_timestamp

        uptime_string = str(int(uptime)) + "s"

        # assigns the uptime to the template
        template_file.assign("uptime", uptime_string)

    def __assign_did_you_know_variables(self, template_file):
        # retrieves the did you know list length
        did_you_know_list_length = len(DID_YOU_KNOW_LIST)

        # generates the random value
        random_value = random.randint(0, did_you_know_list_length - 1)

        # retrieves the random did you know sentence
        did_you_know = DID_YOU_KNOW_LIST[random_value]

        # assigns the did you know to the template
        template_file.assign("did_you_know", did_you_know)

class PluginController:
    """
    The web mvc manager plugin controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/plugin"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_new(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # creates a new company in case this is a post request
        if rest_request.is_post():
            # deploys the package
            self._deploy_package(rest_request)

            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("plugin_new_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "plugin/plugin_new_contents.html.tpl")

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

    def handle_show(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("plugin_edit_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "plugin/plugin_edit_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # retrieves the specified plugin
        plugin = self._get_plugin(rest_request)

        # assigns the plugin to the template
        template_file.assign("plugin", plugin)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_list(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("plugin_list_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "plugin/plugin_list_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

            # assigns the configuration (side panel) variable to the template
            self.web_mvc_manager.web_mvc_manager_side_panel_controller._assign_configuration_variables(template_file)

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # assigns the plugins to the template
        template_file.assign("plugins", plugin_manager.get_all_plugins())

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_partial_list(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # retrieves the template file
        template_file = self.retrieve_template_file("plugin_partial_list_contents.html.tpl")

        # retrieves the filtered plugins
        filtered_plugins = self._get_fitered_plugins(rest_request)

        partial_filtered_plugins, start_record, number_records, total_number_records = self._partial_filter(rest_request, filtered_plugins)

        # assigns the plugins to the template
        template_file.assign("plugins", partial_filtered_plugins)

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

    def handle_change_status(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == JSON_ENCODER_NAME:
            # changes the plugin status and retrieves the result
            change_status_plugin_result = self._change_status_plugin(rest_request)

            # retrieves the json plugin
            json_plugin = self.web_mvc_manager_plugin.json_plugin

            # serializes the change status result using the json plugin
            serialized_status = json_plugin.dumps(change_status_plugin_result)

            # sets the serialized status as the rest request contents
            self.set_contents(rest_request, serialized_status)

            # sends the serialized broadcast message
            self._send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/change_status", serialized_status)

            return True

        # returns true
        return True

    def _send_serialized_broadcast_message(self, parameters, connection_name, message_id, message_contents):
        # serializes the message using, sending the message id and the message contents
        serialized_message = self._get_serialized_message(message_id, message_contents)

        # sends the broadcast communication message
        self.send_broadcast_communication_message(parameters, connection_name, serialized_message)

    def _get_serialized_message(self, message_id, message_contents):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_plugin.json_plugin

        # creates the message map
        message_map = {}

        # sets the message attributes in the message map
        message_map["id"] = message_id
        message_map["contents"] = message_contents

        # serializes the message map using the json plugin
        serialized_message = json_plugin.dumps(message_map)

        # returns the serialized message
        return serialized_message

    def _deploy_package(self, rest_request):
        # retrieves the request contents
        contents = rest_request.request.read()

        # opens the temporary cpx file
        temp_file = open("c:/temp.cpx", "wb")

        # writes the contents to the file
        temp_file.write(contents)

        # closes the temporary file
        temp_file.close()

        # retrieves the packing manager plugin
        packing_manager_plugin = self.web_mvc_manager_plugin.packing_manager_plugin

        # creates the properties map for the file unpacking packing
        properties = {"target_path" : PLUGINS_DIRECTORY}

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files(["c:/temp.cpx"], properties, "colony")

    def _partial_filter(self, rest_request, contents_list):
        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        start_record = int(form_data_map["start_record"])
        number_records = int(form_data_map["number_records"])

        # retrieves the partial contents list
        partial_contents_list = contents_list[start_record:start_record + number_records]

        # retrieves the total number of records from the contents list
        total_number_records = len(contents_list)

        # in case the total number of records is smaller
        # than the request number of records
        if total_number_records < number_records:
            # the number of records is set to the total number of records
            number_records = total_number_records

        # creates the filter contents tuple
        filter_contents = (partial_contents_list, start_record, number_records, total_number_records)

        # returns the filter contents tuple
        return filter_contents

    def _get_plugin(self, rest_request):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the plugin's id from the rest request's path list
        plguin_id = rest_request.path_list[-1]

        # retrieves the plugin from the given plugin id
        plugin = plugin_manager._get_plugin_by_id(plguin_id)

        return plugin

    def _get_fitered_plugins(self, rest_request):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        search_query = form_data_map["search_query"]

        # retrieves the plugins
        plugins = plugin_manager.get_all_plugins()

        # creates the filtered plugins list
        filtered_plugins = []

        # iterates over all the plugins
        for plugin in plugins:
            # in case the search query is found in the plugin id
            if not plugin.id.find(search_query) == -1:
                # adds the plugin to the filtered plugins
                filtered_plugins.append(plugin)

        # returns the filtered plugins
        return filtered_plugins

    def _change_status_plugin(self, rest_request):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        plugin_id = form_data_map["plugin_id"]
        plugin_status = form_data_map["plugin_status"]

        # retrieves the (beginning) list of loaded plugins
        loaded_plugins_beginning = copy.copy(plugin_manager.get_all_loaded_plugins())

        # in case the plugin status is load
        if plugin_status == LOAD_VALUE:
            # loads the plugin for the given plugin id
            plugin_manager.load_plugin(plugin_id)
        # in case the plugin status in unload
        elif plugin_status == UNLOAD_VALUE:
            # unloads the plugin for the given plugin id
            plugin_manager.unload_plugin(plugin_id)

        # retrieves the (end) list of loaded plugins
        loaded_plugins_end = plugin_manager.get_all_loaded_plugins()

        # creates the delta plugin status map
        delta_plugin_status_map = {UNLOADED_VALUE : [], LOADED_VALUE : []}

        # iterates over all the plugins loaded at the beginning
        # to check if they exist in the current loaded plugins
        for loaded_plugin_beginning in loaded_plugins_beginning:
            if not loaded_plugin_beginning in loaded_plugins_end:
                delta_plugin_status_map[UNLOADED_VALUE].append(loaded_plugin_beginning.id)

        # iterates over all the plugins loaded at the end
        # to check if they exist in the previously loaded plugins
        for loaded_plugin_end in loaded_plugins_end:
            if not loaded_plugin_end in loaded_plugins_beginning:
                delta_plugin_status_map[LOADED_VALUE].append(loaded_plugin_end.id)

        # returns the delta plugin status map
        return delta_plugin_status_map

class CapabilityController:
    """
    The web mvc manager capability controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/capability"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_show(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("capability_edit_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "capability/capability_edit_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # retrieves the specified capability
        capability = self._get_capability(rest_request)

        # retrieves the plugins map for the capability
        plugins_capability = self._get_plugins_capability(capability)

        # retrieves the sub capabilities for the capability
        sub_capabilities = self._get_sub_capabilities(capability)

        # assigns the capability to the template
        template_file.assign("capability", capability)

        # assigns the plugins capability to the template
        template_file.assign("plugins_capability", plugins_capability)

        # assigns the sub capabilities to the template
        template_file.assign("sub_capabilities", sub_capabilities)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_list(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("capability_list_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "capability/capability_list_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # retrieves the capabilities
        capabilities = self._get_capabilities()

        # assigns the plugins to the template
        template_file.assign("capabilities", capabilities)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def _get_capabilities(self):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves all the capabilities
        capabilities = plugin_manager.capabilities_plugin_instances_map.keys()

        # sorts all the capabilities
        capabilities.sort()

        return capabilities

    def _get_capability(self, rest_request):
        # retrieves the capability from the rest request's path list
        capability = rest_request.path_list[-1]

        return capability

    def _get_plugins_capability(self, capability):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the plugins providing the capability
        plugins_offering = list(set(plugin_manager.capabilities_plugin_instances_map.get(capability, [])))

        # retrieves the plugins allowing the capability
        plugins_allowing = list(set(plugin_manager.capabilities_plugins_map.get(capability, [])))

        # creates an unique set of plugins offering the capability
        plugins_offering_unique = set(plugins_offering)

        # creates an unique set of plugins allowing the capability
        plugins_allowing_unique = set(plugins_allowing)

        return {PROVIDING_VALUE : plugins_offering_unique, ALLOWING_VALUE : plugins_allowing_unique}

    def _get_sub_capabilities(self, capability):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the sub capabilities for the capability
        sub_capabilities = plugin_manager.capabilities_sub_capabilities_map.get(capability, [])

        return sub_capabilities

class RepositoryController:
    """
    The web mvc manager repository controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/repository"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_show(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("repository_edit_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "capability/repository_edit_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_update.html.tpl")

        # retrieves the specified capability
        repository = self._get_repository(rest_request)

        # assigns the capability to the template
        template_file.assign("repository", repository)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_list(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("repository_list_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "repository/repository_list_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # retrieves the respositories
        repositories = self._get_repositories()

        # assigns the plugins to the template
        template_file.assign("repositories", repositories)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def _get_repository(self, rest_request):
        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_plugin.system_updater_plugin

        # retrieves the repository index from the rest request's path list
        repository_index = int(rest_request.path_list[-1])

        # retrieves all the repositories
        repositories = system_updater_plugin.get_repositories()

        repository = repositories[repository_index - 1]

        repository_name = repository.name

        # retrieves the repository for the repository with the given name
        repository_information = system_updater_plugin.get_repository_information_by_repository_name(repository_name)

        return repository_information

    def _get_repositories(self):
        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_plugin.system_updater_plugin

        # retrieves all the repositories
        repositories = system_updater_plugin.get_repositories()

        return repositories
