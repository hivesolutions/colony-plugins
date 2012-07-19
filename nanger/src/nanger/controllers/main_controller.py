#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.import_util

mvc_utils = colony.libs.import_util.__import__("mvc_utils")
controllers = colony.libs.import_util.__import__("controllers")

class MainController(controllers.Controller):
    """
    The nanger main controller.
    """

    def handle_index(self, rest_request, parameters = {}):
        """
        Handles the given index rest request.

        @type rest_request: RestRequest
        @param rest_request: The index rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "general/index.html.tpl"
        )
        template_file.assign("title", "Colony Framework")
        template_file.assign("area", "home")
        self.process_set_contents(rest_request, template_file)

    def handle_console(self, rest_request, parameters = {}):
        """
        Handles the given console rest request.

        @type rest_request: RestRequest
        @param rest_request: The console rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "general/console.html.tpl"
        )
        template_file.assign("title", "Console")
        template_file.assign("area", "console")
        self.process_set_contents(rest_request, template_file)

    def handle_about(self, rest_request, parameters = {}):
        """
        Handles the given about rest request.

        @type rest_request: RestRequest
        @param rest_request: The console rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "general/about.html.tpl"
        )
        template_file.assign("title", "About")
        template_file.assign("area", "about")
        self.process_set_contents(rest_request, template_file)
