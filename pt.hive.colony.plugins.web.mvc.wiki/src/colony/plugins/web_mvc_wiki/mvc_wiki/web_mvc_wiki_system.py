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

class WebMvcWiki:
    """
    The web mvc wiki class.
    """

    web_mvc_wiki_plugin = None
    """ The web mvc wiki plugin """

    def __init__(self, web_mvc_plugin):
        """
        Constructor of the class.

        @type web_mvc_plugin: WebMvcPlugin
        @param web_mvc_plugin: The web mvc plugin.
        """

        self.web_mvc_plugin = web_mvc_plugin

    def get_patterns(self):
        """
        Retrieves the map of regular expressions to be used as patters,
        to the web mvc service. The map should relate the route with the handler
        method/function.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return {r"^wiki/.*$" : self.handle_wiki}

    def handle_wiki(self, rest_request):
        """
        Handles the given wiki rest request.

        @type rest_request: RestRequest
        @param rest_request: The wiki rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # sets the content type for the rest request
        rest_request.set_content_type("text/html")

        # sets the content type for the rest request
        rest_request.set_result_translated("hello wiki")

        # flushes the rest request
        rest_request.flush()

        # returns true
        return True
