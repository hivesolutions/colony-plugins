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

# only loads the plugin manager service if it is being called from the ice registry (main)
if __name__ == "__main__":
    import sys
    import Ice

    Ice.loadSlice(os.path.dirname(__file__) + "/resources/main_remote_plugin_manager_service_ice_server.ice")
    import pt.hive.colony.plugins.main.remote.pluginmanagericeservice

    class PluginManagerOp(pt.hive.colony.plugins.main.remote.pluginmanagericeservice.PluginManagerOp):

        def __init__(self, name):
            self.name = name

        def registerPluginManager(self, id, current = None):
            print "registou: " + id
            return 0

        def getPluginDescriptorById(self, pluginId, current = None):
            return None

    class MainRemotePluginManagerIceServiceIceServer(Ice.Application):

        def __init__(self):
            pass

        def run(self, args):
            # retrieves the properties from the communicator
            properties = self.communicator().getProperties()

            # retrieves the object adapter
            adapter = self.communicator().createObjectAdapter("LogicAdapter")

            # creates a new identity for the server
            plugin_manager_op_access_id = Ice.Identity("plugin_manager_op_access", "");

            # adds the service object to the adapter
            adapter.add(PluginManagerOp(properties.getProperty("Ice.ServerId")), plugin_manager_op_access_id)

            # activates the adapter
            adapter.activate()

            # waits for the adapter shutdown
            self.communicator().waitForShutdown()

            return 0

    ice_server = MainRemotePluginManagerIceServiceIceServer()
    ice_server.main(sys.argv)

def get_server_path():
    """
    Retrieves the path to the ice server file

    @rtype: String
    @return: The path to the ice server file
    """

    return os.path.abspath(__file__)
