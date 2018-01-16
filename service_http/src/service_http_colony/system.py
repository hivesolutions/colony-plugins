#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import exceptions

HANDLER_NAME = "colony"
""" The handler name """

PLUGIN_HANDLER_VALUE = "plugin_handler"
""" The plugin handler value """

DEFAULT_ERROR_STATUS_CODE = 500
""" The default error status code, this value
is going to be set in the request in case no
valid status code is set in it """

class ServiceHttpColony(colony.System):
    """
    The service http colony (handler) class.
    """

    http_handler_plugin_map = {}
    """ The http handler plugin map """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.http_handler_plugin_map = {}

    def get_handler_name(self):
        """
        Retrieves the handler name.

        :rtype: String
        :return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        :type request: HttpRequest
        :param request: The http request to be handled.
        """

        # in case the plugin handler value is defined in
        # the properties
        if PLUGIN_HANDLER_VALUE in request.properties:
            # retrieves the plugin handler id for the plugin handler value
            plugin_handler_id = request.properties[PLUGIN_HANDLER_VALUE]

            # retrieves the http handler plugin
            http_handler_plugin = self.http_handler_plugin_map.get(plugin_handler_id, None)

            # handles the request by the http handler plugin and
            # retrieves the return value
            http_handler_plugin.handle_request(request)

            # sets the request status code in case it has
            # not been already set
            request.status_code = request.status_code or DEFAULT_ERROR_STATUS_CODE

            # returns immediately
            return
        else:
            # iterates over all the http handler plugins
            for http_handler_plugin in self.plugin.http_handler_plugins:
                # checks if the current http handler plugin
                # is request handler for the current request
                is_request_handler = http_handler_plugin.is_request_handler(request)

                # in case it's not the request handler, must continue
                # the current loop, nothing to handler
                if not is_request_handler: continue

                # handles the request by the http handler plugin and
                # retrieves the return value then sets the status code in
                # the request in case it's defined or default to the error
                # status in case the handler did not set any status code
                http_handler_plugin.handle_request(request)
                request.status_code = request.status_code or DEFAULT_ERROR_STATUS_CODE

                # returns immediately as the request has been correctly
                # handled by the current handler in iteration
                return

        # raises the request not handled exception
        raise exceptions.RequestNotHandled("no python handler plugin could handle the request")

    def http_handler_load(self, http_handler_plugin):
        # retrieves the plugin id
        plugin_id = http_handler_plugin.id

        self.http_handler_plugin_map[plugin_id] = http_handler_plugin

    def http_handler_unload(self, http_handler_plugin):
        # retrieves the plugin id
        plugin_id = http_handler_plugin.id

        del self.http_handler_plugin_map[plugin_id]
