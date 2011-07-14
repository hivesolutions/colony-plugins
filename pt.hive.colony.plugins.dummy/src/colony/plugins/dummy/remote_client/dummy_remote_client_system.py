#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class DummyRemoteClient:
    """
    The dummy remote client class.
    """

    dummy_remote_client_plugin = None
    """ The dummy remote client plugin """

    def __init__(self, dummy_remote_client_plugin):
        """
        Constructor of the class.

        @type dummy_remote_client_plugin: DummyRemoteClientPlugin
        @param dummy_remote_client_plugin: he dummy remote client plugin.
        """

        self.dummy_remote_client_plugin = dummy_remote_client_plugin

    def create_remote_call(self):
        # retrieves the remote client manager plugin
        remote_client_manager_plugin = self.dummy_remote_client_plugin.remote_client_manager_plugin

        # defines the parameters
        parameters = {
            "pyro_main_uri" : "PYRO://192.168.1.21:7766/c0a80115239814b98c09807c8217e571"
        }

        # creates the pyro remote client
        remote_client = remote_client_manager_plugin.create_remote_client("pyro", parameters)

        # in case no remote client is set
        if not remote_client:
            # prints a warning message
            self.dummy_remote_client_plugin.warning("Could not load remote client")

            # returns immediately
            return

        # calls the remote hello method
        remote_client.object2.hello()
