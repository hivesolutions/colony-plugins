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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

import sys
import StringIO

import colony.libs.importer_util

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_PAGE_ITEM_CODE_EXECUTION_RESOURCES_PATH = "web_mvc_manager_page_item/code_execution/resources"
""" The web mvc manager page item code_execution resources path """

TEMPLATES_PATH = WEB_MVC_MANAGER_PAGE_ITEM_CODE_EXECUTION_RESOURCES_PATH + "/templates"
""" The templates path """

AJAX_ENCODER_NAME = "ajx"
""" The ajax encoder name """

JSON_ENCODER_NAME = "json"
""" The json encoder name """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class WebMvcManagerPageItemCodeExecutionController:
    """
    The web mvc manager page item code execution controller.
    """

    web_mvc_manager_page_item_code_execution_plugin = None
    """ The web mvc manager page item code execution plugin """

    web_mvc_manager_page_item_code_execution = None
    """ The web mvc manager page item code execution """

    def __init__(self, web_mvc_manager_page_item_code_execution_plugin, web_mvc_manager_page_item_code_execution):
        """
        Constructor of the class.

        @type web_mvc_manager_page_item_code_execution_plugin: WebMvcManagerPageItemCodeExecutionPlugin
        @param web_mvc_manager_page_item_code_execution_plugin: The web mvc manager page item code execution plugin.
        @type web_mvc_manager_page_item_code_execution: WebMvcManagerPageItemCodeExecution
        @param web_mvc_manager_page_item_code_execution: The web mvc manager page item code execution.
        """

        self.web_mvc_manager_page_item_code_execution_plugin = web_mvc_manager_page_item_code_execution_plugin
        self.web_mvc_manager_page_item_code_execution = web_mvc_manager_page_item_code_execution

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_page_item_code_execution_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_page_item_code_execution_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_page_item_code_execution_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_page_item_code_execution_plugin_path + "/" + TEMPLATES_PATH + "/code_execution"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_new_ajx(self, rest_request, parameters = {}):
        # retrieves the template file
        template_file = self.retrieve_template_file("code_execution_contents.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_new(self, rest_request, parameters = {}):
        # retrieves the template file from the parameters
        template_file = parameters["template_file"]

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", "code_execution/code_execution_contents.html.tpl")

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

    def handle_execute(self, rest_request, parameters = {}):
        # retrieves the template file
        template_file = self.retrieve_template_file("code_execution_contents.html.tpl")

        # executes the command
        output_message = self.execute_command(rest_request)

        # assigns the output to the template
        template_file.assign("output_message", output_message)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def execute_command(self, rest_request):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the command
        command = form_data_map["command"]

        # returns in case no command was specified
        if not command:
            return

        # creates a stream for stdout
        stdout_stream = StringIO.StringIO()

        # temporarily redirects the stdout stream
        sys.stdout = stdout_stream

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_page_item_code_execution_plugin.manager

        try:
            # executes the command
            exec(command, globals(), locals())

            # retrieves the command execution output
            output_message = stdout_stream.getvalue()
        except Exception, exception:
            # sets the exception as the output message
            output_message = unicode(exception)

        # restores stdout
        sys.stdout = sys.__stdout__

        # closes the stdout stream
        stdout_stream.close()

        # converts empty output to none
        if output_message == "":
            output_message = None
        else:
            # replaces new lines with line breaks
            output_message = output_message.replace("\n", "<br />")

        return output_message
