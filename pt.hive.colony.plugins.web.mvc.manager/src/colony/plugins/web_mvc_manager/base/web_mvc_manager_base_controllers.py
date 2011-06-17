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

import colony.libs.importer_util

SERIALIZER_VALUE = "serializer"
""" The serializer value """

EXCEPTION_HANDLER_VALUE = "exception_handler"
""" The exception handler value """

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_BASE_RESOURCES_PATH = "web_mvc_manager/base/resources"
""" The web mvc manager base resources path """

COLONY_BUNDLE_FILE_EXTENSION = "cbx"
""" The colony bundle file extension """

COLONY_PLUGIN_FILE_EXTENSION = "cpx"
""" The colony plugin file extension """

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

EXCEPTION_VALUE = "exception"
""" The exception value """

MESSAGE_VALUE = "message"
""" The message value """

PATTERN_NAMES_VALUE = "pattern_names"
""" The pattern names value """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class PluginController:
    """
    The web mvc manager base plugin controller.
    """

    web_mvc_manager_base_plugin = None
    """ The web mvc manager bae plugin """

    web_mvc_manager_base = None
    """ The web mvc manager base """

    def __init__(self, web_mvc_manager_base_plugin, web_mvc_manager_base):
        """
        Constructor of the class.

        @type web_mvc_manager_base_plugin: WebMvcManagerBasePlugin
        @param web_mvc_manager_base_plugin: The web mvc manager base plugin.
        @type web_mvc_manager_base: WebMvcManagerBase
        @param web_mvc_manager_base: The web mvc manager base.
        """

        self.web_mvc_manager_base_plugin = web_mvc_manager_base_plugin
        self.web_mvc_manager_base = web_mvc_manager_base

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_BASE_RESOURCES_PATH, extra_templates_path = "plugin")

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return []

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("plugins.list")
    def handle_list(self, rest_request, parameters = {}):
        # retrieves the exception handler
        exception_handler = self.web_mvc_manager_base.web_mvc_manager_base_exception_controller

        # sets the exception handler in the parameters
        parameters[EXCEPTION_HANDLER_VALUE] = exception_handler

        # retrieves the template file from the parameters
        template_file = parameters["template_file"]

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_BASE_RESOURCES_PATH, "templates/plugin/plugin_list_contents.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)

        # assigns the include to the template
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("plugins.list")
    def handle_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_base_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the template file
        template_file = self.retrieve_template_file("plugin_list_contents.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("plugins.list")
    def handle_partial_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_base_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the form data attributes
        search_query = form_data_map["search_query"]

        # retrieves the start record
        start_record = form_data_map["start_record"]

        # retrieves the number records
        number_records = form_data_map["number_records"]

        # converts the start record to integer
        start_record = int(start_record)

        # converts the number records to integer
        number_records = int(number_records)

        # retrieves the filtered plugins
        filtered_plugins = self._get_filtered_plugins(rest_request, search_query)

        # retrieves the partial filtered plugins and meta data
        partial_filtered_plugins, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_plugins, start_record, number_records)

        # retrieves the template file
        template_file = self.retrieve_template_file("plugin_partial_list_contents.html.tpl")

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

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("plugins.show")
    def handle_show(self, rest_request, parameters = {}):
        # retrieves the exception handler
        exception_handler = self.web_mvc_manager_base.web_mvc_manager_base_exception_controller

        # sets the exception handler in the parameters
        parameters[EXCEPTION_HANDLER_VALUE] = exception_handler

        # retrieves the template file from the parameters
        template_file = parameters["template_file"]

        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the plugin id pattern
        plugin_id = pattern_names["plugin_id"]

        # retrieves the specified plugin
        plugin = self._get_plugin(rest_request, plugin_id)

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", "plugin/plugin_list_contents.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the plugin to the template
        template_file.assign("plugin", plugin)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("plugins.show")
    def handle_show_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_base_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the plugin id pattern
        plugin_id = pattern_names["plugin_id"]

        # retrieves the specified plugin
        plugin = self._get_plugin(rest_request, plugin_id)

        # retrieves the template file
        template_file = self.retrieve_template_file("plugin_edit_contents.html.tpl")

        # assigns the plugin to the template
        template_file.assign("plugin", plugin)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("plugins.change_status")
    def handle_change_status_serialized(self, rest_request, parameters = {}):
        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the communication helper
        communication_helper = parameters["communication_helper"]

        # retrieves the plugin id pattern
        plugin_id = pattern_names["plugin_id"]

        # retrieves the plugin status from the form data map
        plugin_status = form_data_map["plugin_status"]

        # changes the plugin status and retrieves the result
        change_status_plugin_result = self._change_status_plugin(rest_request, plugin_id, plugin_status)

        # serializes the change status result using the json plugin
        serialized_status = serializer.dumps(change_status_plugin_result)

        # sets the serialized status as the rest request contents
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/change_status", serialized_status)

    def handle_change_status_json(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_base_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle create serialized method
        self.handle_change_status_serialized(rest_request, parameters)

    def _get_plugin(self, rest_request, plugin_id):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_base_plugin.manager

        # retrieves the plugin from the given plugin id
        plugin = plugin_manager._get_plugin_by_id(plugin_id)

        # returns the specified plugin
        return plugin

    def _get_filtered_plugins(self, rest_request, search_query):
        # retrieves the plugins
        plugins = self._get_plugins()

        # creates the filtered plugins list
        filtered_plugins = [plugin for plugin in plugins if not plugin.id.find(search_query) == -1]

        # returns the filtered plugins
        return filtered_plugins

    def _get_plugins(self):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_base_plugin.manager

        # retrieves the plugins
        plugins = plugin_manager.get_all_plugins()

        # returns all plugins
        return plugins

    def _change_status_plugin(self, rest_request, plugin_id, plugin_status):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_base_plugin.manager

        # retrieves the (beginning) list of loaded plugins
        loaded_plugins_beginning = copy.copy(plugin_manager.get_all_loaded_plugins())

        # loads the plugin for the given plugin id in case the plugin status is load
        (plugin_status == LOAD_VALUE) and plugin_manager.load_plugin(plugin_id)

        # unloads the plugin for the given plugin id in case the plugin status in unload
        (plugin_status == UNLOAD_VALUE) and plugin_manager.unload_plugin(plugin_id)

        # retrieves the (end) list of loaded plugins
        loaded_plugins_end = plugin_manager.get_all_loaded_plugins()

        # iterates over all the plugins loaded at the end
        # to check if they exist in the previously loaded plugins
        loaded_list = [loaded_plugin_end.id for loaded_plugin_end in loaded_plugins_end if not loaded_plugin_end in loaded_plugins_beginning]

        # iterates over all the plugins loaded at the beginning
        # to check if they exist in the current loaded plugins
        unloaded_list = [loaded_plugin_beginning.id for loaded_plugin_beginning in loaded_plugins_beginning if not loaded_plugin_beginning in loaded_plugins_end]

        # creates the delta plugin status map
        delta_plugin_status_map = {
            LOADED_VALUE : loaded_list,
            UNLOADED_VALUE : unloaded_list
        }

        # returns the delta plugin status map
        return delta_plugin_status_map

class CapabilityController:
    """
    The web mvc manager base capability controller.
    """

    web_mvc_manager_base_plugin = None
    """ The web mvc manager base plugin """

    web_mvc_manager_base = None
    """ The web mvc manager base """

    def __init__(self, web_mvc_manager_base_plugin, web_mvc_manager_base):
        """
        Constructor of the class.

        @type web_mvc_manager_base_plugin: WebMvcManagerBasePlugin
        @param web_mvc_manager_base_plugin: The web mvc manager base plugin.
        @type web_mvc_manager_base: WebMvcManagerBase
        @param web_mvc_manager_base: The web mvc manager base.
        """

        self.web_mvc_manager_base_plugin = web_mvc_manager_base_plugin
        self.web_mvc_manager_base = web_mvc_manager_base

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_BASE_RESOURCES_PATH, extra_templates_path = "capability")

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return []

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("capabilites.list")
    def handle_list(self, rest_request, parameters = {}):
        # retrieves the exception handler
        exception_handler = self.web_mvc_manager_base.web_mvc_manager_base_exception_controller

        # sets the exception handler in the parameters
        parameters[EXCEPTION_HANDLER_VALUE] = exception_handler

        # retrieves the template file
        template_file = self.retrieve_template_file("../general.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", "capability/capability_list_contents.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("capabilites.list")
    def handle_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_base_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the template file
        template_file = self.retrieve_template_file("capability_list_contents.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("capabilites.list")
    def handle_partial_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_base_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the form data attributes
        search_query = form_data_map["search_query"]

        # retrieves the start record
        start_record = form_data_map["start_record"]

        # retrieves the number records
        number_records = form_data_map["number_records"]

        # converts the start record to integer
        start_record = int(start_record)

        # converts the number records to integer
        number_records = int(number_records)

        # retrieves the filtered capabilities
        filtered_capabilities = self._get_filtered_capabilities(rest_request, search_query)

        # retrieves the partial filter from the filtered capabilities
        partial_filtered_capabilities, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_capabilities, start_record, number_records)

        # retrieves the template file
        template_file = self.retrieve_template_file("capability_partial_list_contents.html.tpl")

        # assigns the capabilities to the template
        template_file.assign("capabilities", partial_filtered_capabilities)

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

    @web_mvc_utils.validated_method("capabilites.show")
    def handle_show(self, rest_request, parameters = {}):
        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the capability pattern
        capability = pattern_names["capability"]

        # retrieves the plugins map for the capability
        plugins_capability = self._get_plugins_capability(rest_request, capability)

        # retrieves the sub capabilities for the capability
        sub_capabilities = self._get_sub_capabilities(rest_request, capability)

        # retrieves the template file
        template_file = self.retrieve_template_file("../general.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", "capability/capability_edit_contents.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

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

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("capabilites.show")
    def handle_show_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_base_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the capability pattern
        capability = pattern_names["capability"]

        # retrieves the plugins map for the capability
        plugins_capability = self._get_plugins_capability(rest_request, capability)

        # retrieves the sub capabilities for the capability
        sub_capabilities = self._get_sub_capabilities(rest_request, capability)

        # retrieves the template file
        template_file = self.retrieve_template_file("capability_edit_contents.html.tpl")

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

    def _get_filtered_capabilities(self, rest_request, search_query):
        # retrieves the capabilities
        capabilities = self._get_capabilities()

        # creates the filtered capabilities list
        filtered_capabilities = [capability for capability in capabilities if not capability.find(search_query) == -1]

        # returns the filtered capabilities
        return filtered_capabilities

    def _get_capabilities(self):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_base_plugin.manager

        # retrieves all the capabilities
        capabilities = plugin_manager.capabilities_plugin_instances_map.keys()

        # sorts all the capabilities
        capabilities.sort()

        # returns the capabilities
        return capabilities

    def _get_plugins_capability(self, rest_request, capability):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_base_plugin.manager

        # retrieves the plugins providing the capability
        plugins_offering = list(set(plugin_manager.capabilities_plugin_instances_map.get(capability, [])))

        # retrieves the plugins allowing the capability
        plugins_allowing = list(set(plugin_manager.capabilities_plugins_map.get(capability, [])))

        # creates an unique set of plugins offering the capability
        plugins_offering_unique = set(plugins_offering)

        # creates an unique set of plugins allowing the capability
        plugins_allowing_unique = set(plugins_allowing)

        # defines the plugins map
        plugins_map = {
            PROVIDING_VALUE : plugins_offering_unique,
            ALLOWING_VALUE : plugins_allowing_unique
        }

        # returns the plugins map
        return plugins_map

    def _get_sub_capabilities(self, rest_request, capability):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_base_plugin.manager

        # retrieves the sub capabilities for the capability
        sub_capabilities = plugin_manager.capabilities_sub_capabilities_map.get(capability, [])

        # returns the sub capabilities
        return sub_capabilities

class ExceptionController:
    """
    The web mvc manager base exception controller.
    """

    web_mvc_manager_base_plugin = None
    """ The web mvc manager base plugin """

    web_mvc_manager_base = None
    """ The web mvc manager base """

    def __init__(self, web_mvc_manager_base_plugin, web_mvc_manager_base):
        """
        Constructor of the class.

        @type web_mvc_manager_base_plugin: WebMvcManagerBasePlugin
        @param web_mvc_manager_base_plugin: The web mvc manager base plugin.
        @type web_mvc_manager_base: WebMvcManagerBase
        @param web_mvc_manager_base: The web mvc manager base.
        """

        self.web_mvc_manager_base_plugin = web_mvc_manager_base_plugin
        self.web_mvc_manager_base = web_mvc_manager_base

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_BASE_RESOURCES_PATH)

    def handle_exception(self, rest_request, parameters = {}):
        """
        Handles an exception.

        @type rest_request: RestRequest
        @param rest_request: The rest request for which the exception occurred.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the exception
        exception = parameters.get(EXCEPTION_VALUE)

        # retrieves the exception message
        exception_message = exception.get(MESSAGE_VALUE)

        # creates the exception complete message
        exception_complete_message = "Exception: " + exception_message

        # sets the exception message in the rest request
        self.set_contents(rest_request, exception_complete_message)
