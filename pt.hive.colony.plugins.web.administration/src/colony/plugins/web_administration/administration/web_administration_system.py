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
""" The default encoding """

DEFAULT_TEMPLATE_ENCODING = "Cp1252"
""" The default template encoding """

VALID_STATUS_CODE = 200
""" The valid status code """

XHTML_MIME_TYPE = "application/xhtml+xml"
""" The xhtml mime type """

WEB_ADMINISTRATION_RESOURCES_PATH = "web_administration/administration/resources"
""" The web administration resources path """

class WebAdministration:
    """
    The web administration class.
    """

    web_administration_plugin = None
    """ The web administration plugin """

    def __init__(self, web_administration_plugin):
        """
        Constructor of the class.

        @type web_administration_plugin: WebAdministrationPlugin
        @param web_administration_plugin: The web administration plugin.
        """

        self.web_administration_plugin = web_administration_plugin

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the rest service.

        @rtype: List
        @return: The list of regular expressions to be used as route,
        to the rest service.
        """

        return [
            r"^administrator/.*$"
        ]

    def handle_rest_request(self, rest_request):
        """
        Handles the given rest request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_administration_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.web_administration_plugin.template_engine_manager_plugin

        # retrieves the web administration plugin path
        web_administration_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_administration_plugin.id)

        # creates the template file path
        template_file_path = web_administration_plugin_path + "/" + WEB_ADMINISTRATION_RESOURCES_PATH + "/" + "web_administrator_login.xhtml"

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path_encoding(template_file_path, DEFAULT_TEMPLATE_ENCODING)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.encode(DEFAULT_ENCODING)

        # sets the status code for the rest request
        rest_request.set_status_code(VALID_STATUS_CODE)

        # sets the content type for the rest request
        rest_request.set_content_type(XHTML_MIME_TYPE)

        # sets the result for the rest request
        rest_request.set_result_translated(processed_template_file_encoded)

        # flushes the rest request
        rest_request.flush()
