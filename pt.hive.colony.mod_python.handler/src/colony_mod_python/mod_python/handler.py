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

import sys
import mod_python

import mod_python.apache

CONTAINER_NAME = "apache"
""" The container name """

MOD_PYTHON_PLUGIN_ID = "pt.hive.colony.plugins.main.mod_python"
""" The mod python plugin id """

plugin_manager = None
""" The plugin manager """

class PluginManagerHandler:
    """
    The plugin manager handler class for the mod_python.
    """

    req = None
    """ The http request sent by the mod_python """

    local_address = None
    """ The local address for the request """

    local_port = None
    """ The local port for the request """

    def __init__(self, req):
        """
        Constructor of the class.
        
        @type req: HttpRequest
        @param req: The http request sent by the mod_python.
        """

        self.req = req
        self.local_address, self.local_port = req.connection.local_addr

    def handle_request(self, data):
        """
        Handles the requested data.
        
        @type data: String
        @param data: The data to handle.
        """

        # creates the plugin handler id object
        plugin_handler_id = None

        # retrieves the mod python options
        python_options = self.req.get_options()

        # retrieves the plugin manager
        manager = self.get_plugin_manager(python_options)

        # retrieves the mod_python plugin
        mod_python_plugin = manager.get_plugin_by_id(MOD_PYTHON_PLUGIN_ID)

        # retrieves the plugin handler id for the current request
        if "PluginHandlerEnv" in python_options:
            plugin_handler_id = python_options["PluginHandlerEnv"]

        # sends the request to the mod_python to handle it
        mod_python_plugin.handle_request(self.req, plugin_handler_id)

        return True

    def get_plugin_manager(self, python_options = {}):
        """
        Retrieves the plugin manager with the given python options.
        
        @type python_options: List
        @param python_options: The list of python options to the (possible) startup of the plugin manager.
        """

        # in case the plugin manager is not loaded
        if not plugin_manager:
            # loads the plugin manager
            self.load_plugin_manager(python_options)

        return plugin_manager

    def load_plugin_manager(self, python_options):
        """
        Loads the plugin manager with the given python options.
        
        @type python_options: List
        @param python_options: The list of python options to the startup of the plugin manager.
        """

        # sets the plugin_manager as a global variable
        global plugin_manager

        # tests the python options to retrieve the plugin manager path
        if not "PluginManagerEnv" in python_options:
            return True

        # retrieves the plugin manager path from the python options
        plugin_manager_path = python_options["PluginManagerEnv"]

        # inserts the plugin path into the default python path
        sys.path.insert(0, plugin_manager_path)

        # imports the main module
        import main

        # sets the command line arguments
        sys.argv.append("--debug")
        sys.argv.append("--noloop")
        sys.argv.append("--container=" + CONTAINER_NAME)
        sys.argv.append("--attributes=apache_address:" + self.local_address + ",apache_port:" + str(self.local_port))
        sys.argv.append("--manager_dir=" + plugin_manager_path)

        # starts the plugin manager
        main.main()

        # retrieves the plugin manager, setting the variable
        plugin_manager = main.plugin_manager

def handler(req):
    """
    The initial handler function for the mod_python.
    
    @type req: HttpRequest
    @param req: The http request sent by the mod_python.
    @rtype: int
    @return: The status for the request.
    """

    # in case the handling was successful
    if PluginManagerHandler(req).handle_request(req):
        return mod_python.apache.OK
    # in case the handling was unsuccessful
    else:
        return mod_python.apache.DECLINED
