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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HELPER_NAME = "pyro"
""" The helper name """

PYRO_PROTOCOL_PREFIX = "PYRO://"
""" The pyro protocol prefix """

class DistributionPyroHelper:
    """
    The distribution pyro helper class.
    """

    distribution_pyro_helper_plugin = None
    """ The distribution pyro helper plugin """

    def __init__(self, distribution_pyro_helper_plugin):
        """
        Constructor of the class.
        
        @type distribution_pyro_helper_plugin: DistributionPyroHelperPlugin
        @param distribution_pyro_helper_plugin: The distribution pyro helper plugin.
        """

        self.distribution_pyro_helper_plugin = distribution_pyro_helper_plugin

    def get_helper_name(self):
        return HELPER_NAME

    def create_client(self, remote_reference):
        """
        Creates a pyro remote client from a remote reference.
        
        @type remote_reference: RemoteReference
        @param remote_reference: The remote reference to retrieve the pyro remote client.
        @rtype: PyroRemoteClient
        @return: The pyro remote client retrieved from a remote reference.
        """

        # retrieves the main pyro client plugin
        main_pyro_client_plugin = self.distribution_pyro_helper_plugin.main_pyro_client_plugin

        # retrieves the remote reference hostname
        hostname = remote_reference.hostname

        # retrieves the remote reference port
        port = remote_reference.port

        # retrieves the remote reference properties list
        properties_list = remote_reference.properties_list

        # retrieves the pyro main unique id
        pyro_main_uid = properties_list[0]

        # creates the pyro main uri
        pyro_main_uri = PYRO_PROTOCOL_PREFIX + hostname + ":" + str(port) + "/" + pyro_main_uid

        # creates the pyro remote client
        pyro_remote_client = main_pyro_client_plugin.create_remote_client({"pyro_main_uri" : pyro_main_uri})

        # creates the pyro remote client proxy
        pyro_remote_client_proxy = PyroClientProxy(pyro_remote_client, remote_reference)

        # returns the pyro remote client proxy
        return pyro_remote_client_proxy

class PyroClientProxy:
    """
    The pyro client proxy class.
    """

    pyro_client = None
    """ The pyro client """

    remote_reference = None
    """ The remote reference """

    def __init__(self, pyro_client = None, remote_reference = None):
        """
        Constructor of the class.
        
        @type pyro_client: PyroClient
        @param pyro_client: The pyro client.
        @type remote_reference: RemoteReference
        @param remote_reference: The pyro remote reference.
        """

        self.pyro_client = pyro_client
        self.remote_reference = remote_reference

    def __getattr__(self, name):
        if hasattr(self.pyro_client, name):
            return getattr(self.pyro_client, name)
