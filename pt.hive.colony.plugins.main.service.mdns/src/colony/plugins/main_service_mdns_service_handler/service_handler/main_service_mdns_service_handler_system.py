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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HANDLER_NAME = "service"
""" The handler name """

PTR_TYPE = "PTR"
""" The ptr type """

class MainServiceMdnsServiceHandler:
    """
    The main service mdns service handler class.
    """

    main_service_mdns_service_handler_plugin = None
    """ The main service mdns service handler plugin """

    mdns_service_name_handler_plugins_map = {}
    """ The mdns service name handler plugins map """

    def __init__(self, main_service_mdns_service_handler_plugin):
        """
        Constructor of the class.

        @type main_service_mdns_service_handler_plugin: MainServiceMdnsServiceHandlerPlugin
        @param main_service_mdns_service_handler_plugin: The main service mdns service handler plugin.
        """

        self.main_service_mdns_service_handler_plugin = main_service_mdns_service_handler_plugin

        self.mdns_service_name_handler_plugins_map = {}

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request, arguments):
        """
        Handles the given mdns request.

        @type request: MdnsRequest
        @param request: The mdns request to be handled.
        @type arguments: Dictionary
        @param arguments: The arguments to the mdns handling.
        """

        # checks if the request represents a response
        request_is_response = request.is_response()

        # in case the request is in fact a response
        if request_is_response:
            # returns immediately (no response)
            return

        # retrieves the request queries
        request_queries = request.queries

        # iterates over all the request queries to
        # handle them with the proper plugin handler
        for request_query in request_queries:
            # unpacks the request query into name, type and class
            query_name, query_type, _query_class = request_query

            # in case the query type is not a reverse (service resolution)
            if not query_type == PTR_TYPE:
                # continues the loop
                continue

            # tries to retrieve the service handler plugin and handles the
            # request in case one exists
            mdns_service_name_handler_plugin = self.mdns_service_name_handler_plugins_map.get(query_name, None)
            mdns_service_name_handler_plugin and mdns_service_name_handler_plugin.handle_request(request, arguments)

    def mdns_service_name_handler_load(self, mdns_service_name_handler_plugin):
        # retrieves the plugin handler name
        handler_name = mdns_service_name_handler_plugin.get_handler_name()

        self.mdns_service_name_handler_plugins_map[handler_name] = mdns_service_name_handler_plugin

    def mdns_service_name_handler_unload(self, mdns_service_name_handler_plugin):
        # retrieves the plugin handler name
        handler_name = mdns_service_name_handler_plugin.get_handler_name()

        del self.mdns_service_name_handler_plugins_map[handler_name]
