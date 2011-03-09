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

import main_service_http_colony_handler_exceptions

HANDLER_NAME = "colony"
""" The handler name """

PLUGIN_HANDLER_VALUE = "plugin_handler"
""" The plugin handler value """

class MainServiceHttpColonyHandler:
    """
    The main service http colony handler class.
    """

    main_service_http_colony_handler_plugin = None
    """ The main service http colony handler plugin """

    def __init__(self, main_service_http_colony_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_colony_handler_plugin: MainServiceHttpColonyHandlerPlugin
        @param main_service_http_colony_handler_plugin: The main service http colony handler plugin.
        """

        self.main_service_http_colony_handler_plugin = main_service_http_colony_handler_plugin

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        # in case the plugin handler value is defined in
        # the properties
        if PLUGIN_HANDLER_VALUE in request.properties:
            # retrieves the plugin handler id for the plugin handler value
            plugin_handler_id = request.properties[PLUGIN_HANDLER_VALUE]

            # iterates over all the http python handler plugins
            for http_python_handler_plugin in self.main_service_http_colony_handler_plugin.http_python_handler_plugins:
                if http_python_handler_plugin.id == plugin_handler_id:
                    # handles the request by the http python handler plugin and
                    # retrieves the return value
                    return_value = http_python_handler_plugin.handle_request(request)

                    # in case no status code is defined
                    if not request.status_code:
                        if return_value:
                            # sets the default request status code
                            request.status_code = 200
                        else:
                            # sets the default error request status code
                            request.status_code = 500

                    return
        else:
            # iterates over all the http python handler plugins
            for http_python_handler_plugin in self.main_service_http_colony_handler_plugin.http_python_handler_plugins:
                if http_python_handler_plugin.is_request_handler(request):
                    # handles the request by the http python handler plugin and
                    # retrieves the return value
                    return_value = http_python_handler_plugin.handle_request(request)

                    # in case no status code is defined
                    if not request.status_code:
                        if return_value:
                            # sets the default request status code
                            request.status_code = 200
                        else:
                            # sets the default error request status code
                            request.status_code = 500

                    return

        # raises the request not handled exception
        raise main_service_http_colony_handler_exceptions.RequestNotHandled("no python handler plugin could handle the request")
