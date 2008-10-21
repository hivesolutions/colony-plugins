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

# only loads the jabber service if it is being called from the ice registry (main)
if __name__ == "__main__":
    import sys
    import Ice

    Ice.loadSlice(os.path.dirname(__file__) + "/resources/jabber_ice_service_ice_server.ice")
    import pt.hive.colony.plugins.misc.jabbericeservice

    class JabberOp(pt.hive.colony.plugins.misc.jabbericeservice.JabberOp):

        def __init__(self, name):
            self.name = name

        def connect(self, username, password, current = None):
            test_file = open("c:/testtest.txt", "w")
            test_file.write("o valor e " + username)
            return 0

    class JabberIceServiceIceServer(Ice.Application):

        def __init__(self):
            pass

        def run(self, args):
            # retrieves the properties from the communicator
            properties = self.communicator().getProperties()

            # retrieves the object adapter
            adapter = self.communicator().createObjectAdapter("LogicAdapter")

            # creates a new identity for the server
            jabber_op_access_id = Ice.Identity("jabber_op_access", "");

            # adds the service object to the adapter
            adapter.add(JabberOp(properties.getProperty("Ice.ServerId")), jabber_op_access_id)

            # activates the adapter
            adapter.activate()

            # waits for the adapter shutdown
            self.communicator().waitForShutdown()

            return 0

    ice_server = JabberIceServiceIceServer()
    ice_server.main(sys.argv)

def get_server_path():
    """
    Retrieves the path to the ice server file
    
    @rtype: String
    @return: The path to the ice server file
    """

    return os.path.abspath(__file__)
