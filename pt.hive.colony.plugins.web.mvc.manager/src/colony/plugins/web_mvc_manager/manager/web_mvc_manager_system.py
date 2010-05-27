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

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_RESOURCES_PATH = "web_mvc_manager/manager/resources"
""" The web mvc manager resources path """

TEMPLATES_PATH = WEB_MVC_MANAGER_RESOURCES_PATH + "/templates"
""" The templates path """

class WebMvcManager:
    """
    The web mvc manager class.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager_main_controller = None
    """ The web mvc manager main controller """

    def __init__(self, web_mvc_manager_plugin):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_manager_plugin.web_mvc_utils_plugin

        # creates the web mvc manager main controller
        #self.take_the_bill_main_controller = web_mvc_utils_plugin.create_controller(WebMvcManagerMainController, [self.web_mvc_manager_plugin, self], {})

    def get_patterns(self):
        """
        Retrieves the map of regular expressions to be used as patters,
        to the web mvc service. The map should relate the route with the handler
        method/function.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return {}

        #return {r"^web_mvc_manager/?$" : self.take_the_bill_main_controller.handle_take_the_bill_index,
        #        r"^web_mvc_manager/index$" : self.take_the_bill_main_controller.handle_take_the_bill_index}

    def get_resource_patterns(self):
        # estes sao os patterns para serem enviados para
        # o file handleers

        # rinha de sacar aki o plugin path
        # e tinha de perceber para onde e ke os tinha de enviar

        # tenho de mandar um evento sempre que alguma destas coisas muda

        return {}

        #return {r"^web_mvc_manager/?$" : "c:/tobias",
        #        r"^web_mvc_manager/index$" : self.take_the_bill_main_controller.handle_take_the_bill_index}

class WebMvcManagerMainController:
    """
    The web mvc manager main controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager main plugin """

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
        plugin_manager = self.take_the_bill_main_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/site"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_web_mvc_manager_index(self, rest_request, parameters = {}):
        """
        Handles the given web mvc manager index rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc manager index rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("site_general.html.tpl")

        # sets the page to be included

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True
