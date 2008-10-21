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

import os

import main_remote_plugin_manager_access_ice_server

DEFAULT_ICE_GRID_REGISTRY_LOCATOR_NAME = "default.grid"
DEFAULT_ICE_GRID_REGISTRY_LOCATOR_ENDPOINT = "default -p 12000"

class MainRemotePluginManagerAccess:

    main_remote_plugin_manager_access_plugin = None

    main_remote_plugin_manager_access_ice_server = None

    def __init__(self, main_remote_plugin_manager_access_plugin):
        """
        Constructor of the class
        
        @type main_remote_plugin_manager_access_plugin: Plugin
        @param main_remote_plugin_manager_access_plugin: The remote plugin manager access plugin
        """

        self.main_remote_plugin_manager_access_plugin = main_remote_plugin_manager_access_plugin

    def start_registry(self):
        """
        Starts the registry in the plugin manager ice service
        """

        # retrieves the ice helper plugin to help in the creation of ice functionalities
        ice_helper_plugin = self.main_remote_plugin_manager_access_plugin.ice_helper_plugin

        # loads the ice file
        ice_helper_plugin.load_ice_file(os.path.dirname(__file__) + "/resources/main_remote_plugin_manager_service_ice_server.ice")

        # import the generated ice stubs
        import pt.hive.colony.plugins.main.remote.pluginmanagericeservice

        # creates the communicator with the default ice grid registry
        communicator = ice_helper_plugin.create_communicator(DEFAULT_ICE_GRID_REGISTRY_LOCATOR_NAME, DEFAULT_ICE_GRID_REGISTRY_LOCATOR_ENDPOINT)

        # creates the access object to the plugin manager op proxy
        access_object = ice_helper_plugin.create_access(communicator, pt.hive.colony.plugins.main.remote.pluginmanagericeservice.PluginManagerOpPrx, "plugin_manager_op_access")

        # registers this plugin manager
        access_object.registerPluginManager("tobias")

        # closes the communicator
        ice_helper_plugin.close_access_communicator(access_object)

        self.main_remote_plugin_manager_access_ice_server = main_remote_plugin_manager_access_ice_server.MainRemotePluginManagerAccessIceServer()
        self.main_remote_plugin_manager_access_ice_server.start_server(self.main_remote_plugin_manager_access_plugin.manager)

    def stop_registry(self):
        self.main_remote_plugin_manager_access_ice_server.stop_server()
