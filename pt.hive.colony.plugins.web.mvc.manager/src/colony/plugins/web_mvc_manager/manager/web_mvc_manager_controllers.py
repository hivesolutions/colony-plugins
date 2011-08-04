#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import time
import base64

import colony.libs.importer_util

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

WEB_MVC_MANAGER_RESOURCES_PATH = "web_mvc_manager/manager/resources"
""" The web mvc manager resources path """

COLONY_BUNDLE_FILE_EXTENSION = "cbx"
""" The colony bundle file extension """

COLONY_PLUGIN_FILE_EXTENSION = "cpx"
""" The colony plugin file extension """

UPGRADE_VALUE = "upgrade"
""" The upgrade value """

COLONY_PACKING_VALUE = "colony_packing"
""" The colony packing value """

SERIALIZER_VALUE = "serializer"
""" The serializer value """

NORMAL_ENCODER_NAME = None
""" The normal encoder name """

PATTERN_NAMES_VALUE = "pattern_names"
""" The pattern names value """

EXCEPTION_VALUE = "exception"
""" The exception value """

MESSAGE_VALUE = "message"
""" The message value """

EXCEPTION_HANDLER_VALUE = "exception_handler"
""" The exception handler value """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class MainController:
    """
    The web mvc manager main controller.
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

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_RESOURCES_PATH)

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return self.web_mvc_manager.require_permissions(self, rest_request, validation_parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_web_mvc_manager_index(self, rest_request, parameters = {}):
        """
        Handles the given web mvc manager index rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc manager index rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the exception handler
        exception_handler = self.web_mvc_manager.web_mvc_manager_exception_controller

        # sets the exception handler in the parameters
        parameters[EXCEPTION_HANDLER_VALUE] = exception_handler

        # retrieves the template file
        template_file = self.retrieve_template_file("general.html.tpl")

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def generate_handle_handle_web_mvc_manager_page_item(self, original_handler):
        """
        Generates a composite handler from the original page item handler.

        @type original_handler: Method
        @param original_handler: The original page item handler.
        @rtype: Method
        @return: The generated handler method.
        """

        def handle_web_mvc_manager_page_item(rest_request, parameters = {}):
            # retrieves the web mvc manager exception controller
            web_mvc_manager_exception_controller = self.web_mvc_manager.web_mvc_manager_exception_controller

            # retrieves the web mvc manager search helper controller
            web_mvc_manager_search_helper_controller = self.web_mvc_manager.web_mvc_manager_search_helper_controller

            # retrieves the web mvc manager communication helper controller
            web_mvc_manager_communication_helper_controller = self.web_mvc_manager.web_mvc_manager_communication_helper_controller

            # in case the encoder name is normal
            if rest_request.encoder_name == NORMAL_ENCODER_NAME:
                # retrieves the template file
                template_file = self.retrieve_template_file("general.html.tpl")

                # assigns the configuration (side panel) variables to the template
                self.web_mvc_manager.web_mvc_manager_side_panel_controller._assign_configuration_variables(rest_request, template_file)

                # assigns the header variables to the template
                self.web_mvc_manager.web_mvc_manager_header_controller._assign_header_variables(template_file)
            # otherwise it's a different encoding
            else:
                # sets the template file to invalid
                template_file = None

            # defines the default parameters
            default_parameters = {
                "template_file" : template_file,
                "exception_handler" : web_mvc_manager_exception_controller,
                "search_helper" : web_mvc_manager_search_helper_controller,
                "communication_helper" : web_mvc_manager_communication_helper_controller
            }

            # extends the parameters map with the template file reference
            handler_parameters = colony.libs.map_util.map_extend(parameters, default_parameters)

            # sends the request to the original handler and returns the result
            return original_handler(rest_request, handler_parameters)

        return handle_web_mvc_manager_page_item

class SidePanelController:
    """
    The web mvc manager side panel controller.
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

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_RESOURCES_PATH, extra_templates_path = "side_panel")

    def handle_update(self, rest_request, parameters = {}):
        """
        Handles the given update rest request.

        @type rest_request: RestRequest
        @param rest_request: The take the bill update rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("side_panel_update.html.tpl")

        # assigns the update variables
        self._assign_update_variables(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def handle_configuration(self, rest_request, parameters = {}):
        """
        Handles the given configuration rest request.

        @type rest_request: RestRequest
        @param rest_request: The take the bill configuration rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("side_panel_configuration.html.tpl")

        # assigns the configuration variables
        self._assign_configuration_variables(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def _assign_update_variables(self, rest_request, template_file):
        self.__assign_panel_item_variables(rest_request, template_file)

    def _assign_configuration_variables(self, rest_request, template_file):
        self.__assign_panel_item_variables(rest_request, template_file)

    def __assign_panel_item_variables(self, rest_request, template_file):
        # retrieves the web mvc panel item plugins
        web_mvc_panel_item_plugins = self.web_mvc_manager_plugin.web_mvc_panel_item_plugins

        # starts the panel items list
        panel_items_list = []

        # iterates over all the web mvc panel item plugins
        for web_mvc_panel_item_plugin in web_mvc_panel_item_plugins:
            panel_item = web_mvc_panel_item_plugin.get_panel_item(rest_request, {})
            panel_items_list.append(panel_item)

        # assigns the panel items to the template
        template_file.assign("panel_items", panel_items_list)

class HeaderController:
    """
    The web mvc manager header controller.
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

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_RESOURCES_PATH)

    def handle_header(self, rest_request, parameters = {}):
        """
        Handles the given header rest request.

        @type rest_request: RestRequest
        @param rest_request: The take the bill header rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("header.html.tpl")

        # assigns the header variables
        self._assign_header_variables(template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def _assign_header_variables(self, template_file):
        # assigns the menu items to the template
        template_file.assign("menu_items", self.web_mvc_manager.menu_items_map)

class PackageController:
    """
    The web mvc manager package controller.
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

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return self.web_mvc_manager.require_permissions(self, rest_request, validation_parameters)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("packages.create")
    def handle_create_serialized(self, rest_request, parameters = {}):
        # deploys the package
        self._deploy_package(rest_request)

    def handle_create_json(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle create serialized method
        self.handle_create_serialized(rest_request, parameters)

    def _deploy_package(self, rest_request, package_type = COLONY_PLUGIN_FILE_EXTENSION):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the system installer plugin
        system_installer_plugin = self.web_mvc_manager_plugin.system_installer_plugin

        # retrieves the web mvc manager plugin id
        web_mvc_manager_plugin_id = self.web_mvc_manager_plugin.id

        # retrieves a temporary plugin path
        temporary_plugin_path = plugin_manager.get_temporary_plugin_path_by_id(web_mvc_manager_plugin_id)

        # creates the temporary plugin path directories
        not os.path.exists(temporary_plugin_path) and os.makedirs(temporary_plugin_path)

        # retrieves the current time
        current_time = time.time()

        # generates a unique file name base on the
        # current time
        unique_file_name = str(current_time) + "." + package_type

        # creates the unique file path joining the temporary plugin path
        # and the unique file name
        unique_file_path = os.path.join(temporary_plugin_path, unique_file_name)

        # retrieves the request contents
        contents = rest_request.request.read()

        # decodes the contents from base64
        contents_decoded = base64.b64decode(contents)

        # opens the temporary (unique) cpx file
        temp_file = open(unique_file_path, "wb")

        try:
            try:
                # writes the contents (decoded) to the file
                temp_file.write(contents_decoded)
            finally:
                # closes the temporary file
                temp_file.close()

            # installation options
            installation_properties = {
                UPGRADE_VALUE : True
            }

            # installs the package
            system_installer_plugin.install_package(unique_file_path, installation_properties, COLONY_PACKING_VALUE)
        finally:
            # removes the temporary file (with the unique file path)
            os.remove(unique_file_path)

class BundleController:
    """
    The web mvc manager bundle controller.
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

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return self.web_mvc_manager.require_permissions(self, rest_request, validation_parameters)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("bundles.create")
    def handle_create_serialized(self, rest_request, parameters = {}):
        # retrieves the package controller
        web_mvc_manager_package_controller = self.web_mvc_manager.web_mvc_manager_package_controller

        # deploys the package
        web_mvc_manager_package_controller._deploy_package(rest_request, COLONY_BUNDLE_FILE_EXTENSION)

    def handle_create_json(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle create serialized method
        self.handle_create_serialized(rest_request, parameters)

class ExceptionController:
    """
    The web mvc manager exception controller.
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

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_RESOURCES_PATH)

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
