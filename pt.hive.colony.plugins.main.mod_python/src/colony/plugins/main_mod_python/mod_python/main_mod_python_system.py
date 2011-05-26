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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class MainModPython:
    """
    The main mod python class.
    """

    main_mod_python_plugin = None
    """ The main mod python plugin """

    http_python_handler_plugin_map = {}
    """ The http python handler plugin map """

    def __init__(self, main_mod_python_plugin):
        """
        Constructor of the class.

        @type main_mod_python_plugin: MainModPythonPlugin
        @param main_mod_python_plugin: The main mod python plugin.
        """

        self.main_mod_python_plugin = main_mod_python_plugin

        self.http_python_handler_plugin_map = {}

    def handle_request(self, request, plugin_handler_id):
        """
        Handles the http request sent.

        @type request: HttpRequest
        @param request: The http request sent by the mod_python.
        @type plugin_handler_id: String
        @param plugin_handler_id: The id of the plugin that handles the request.
        """

        # in case the plugin handler id is already defined
        if plugin_handler_id:
            # retrieves the http python handler plugin
            http_python_handler_plugin = self.http_python_handler_plugin_map.get(plugin_handler_id, None)

            # handles the request using the http python handler plugin
            http_python_handler_plugin.handle_request(request)

            # returns immediately
            return
        # otherwise the plugin is not defined and it
        # must be found first
        else:
            # iterates over all the http python handler plugins
            for http_python_handler_plugin in self.main_mod_python_plugin.http_python_handler_plugins:
                # checks if the current http python handler plugin
                # is request handler for the current request
                is_request_handler = http_python_handler_plugin.is_request_handler(request)

                # in case it's not the request handler
                if not is_request_handler:
                    # continues the loop
                    continue

                # handles the request using the http python handler plugin
                http_python_handler_plugin.handle_request(request)

                # returns immediately
                return

    def http_python_handler_load(self, http_python_handler_plugin):
        # retrieves the plugin id
        plugin_id = http_python_handler_plugin.id

        self.http_python_handler_plugin_map[plugin_id] = http_python_handler_plugin

    def http_python_handler_unload(self, http_python_handler_plugin):
        # retrieves the plugin id
        plugin_id = http_python_handler_plugin.id

        del self.http_python_handler_plugin_map[plugin_id]
