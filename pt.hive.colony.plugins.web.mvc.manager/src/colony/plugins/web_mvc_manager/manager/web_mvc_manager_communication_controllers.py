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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
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

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class WebMvcManagerCommunicationController:
    """
    The web mvc manager communication controller.
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

    def handle_data(self, rest_communication_request, parameters = {}):
        """
        Handles the given data communication request.

        @type rest_communication_request: RestRequest
        @param rest_communication_request: The web mvc manager data rest
        communication request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        pass

    def handle_connection_changed(self, rest_communication_request, parameters = {}):
        """
        Handles the given connection changed communication request.

        @type rest_communication_request: RestRequest
        @param rest_communication_request: The web mvc manager connection changed
        rest communication request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        pass
