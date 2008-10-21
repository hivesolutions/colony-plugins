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

__revision__ = "$LastChangedRevision: 2119 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:55:58 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import threading
import Ice

import colony.plugins.util

DEFAULT_ADAPTER_NAME = "LogicAdapter"
DEFAULT_ADAPTER_ENDPOINTS = "tcp -p 10012:udp -p 10013"
DEFAULT_SERVER_ID = "dummy"

class MainRemotePluginManagerAccessIceServer:

    ice_server = None

    def __init__(self):
        pass

    def start_server(self, plugin_manager):
        init_data = Ice.InitializationData()
        init_data.properties = Ice.createProperties()
        init_data.properties.setProperty(DEFAULT_ADAPTER_NAME + ".Endpoints", DEFAULT_ADAPTER_ENDPOINTS)
        init_data.properties.setProperty("Ice.ServerId", DEFAULT_SERVER_ID)
        communicator = Ice.initialize(init_data)

        # creates the ice server object
        self.ice_server = MainRemotePluginManagerAccessIceServerImplementation(communicator)

        # starts the server
        self.ice_server.run(None)

    def stop_server(self):
        if self.ice_server:
            self.ice_server.communicator.destroy()

    def get_server_path(self):
        """
        Retrieves the path to the ice server file
        
        @rtype: String
        @return: The path to the ice server file
        """

        return os.path.abspath(__file__)

class MainRemotePluginManagerAccessIceServerImplementation:
    
    communicator = None
    started = False

    def __init__(self, communicator):
        self.communicator = communicator

    def run(self, args):
        Ice.loadSlice(os.path.dirname(__file__) + "/resources/main_remote_plugin_manager_access.ice")
        import pt.hive.colony.plugins.main.remote.pluginmanageraccess

        class PluginManagerAccessOp(pt.hive.colony.plugins.main.remote.pluginmanageraccess.PluginManagerAccessOp):

            def __init__(self, name):
                self.name = name

            def getPluginDescriptorById(self, pluginId, current = None):
                return None

        # retrieves the properties from the communicator
        properties = self.communicator.getProperties()

        # retrieves the object adapter
        adapter = self.communicator.createObjectAdapter(DEFAULT_ADAPTER_NAME)

        # creates a new identity for the server
        plugin_manager_op_access_id = Ice.Identity("plugin_manager_access_op_access", "");

        # adds the service object to the adapter
        adapter.add(PluginManagerAccessOp(properties.getProperty("Ice.ServerId")), plugin_manager_op_access_id)

        # activates the adapter
        adapter.activate()

        # sets the flag started to true to alert the finish of the loading
        self.started = True

        # waits for the communicator shutdown
        self.communicator.waitForShutdown()
