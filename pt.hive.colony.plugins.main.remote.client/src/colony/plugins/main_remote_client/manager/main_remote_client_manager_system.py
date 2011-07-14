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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class MainRemoteClientManager:
    """
    The main remote client manager class.
    """

    main_remote_client_manager_plugin = None
    """ The main remote client manager plugin """

    remote_client_adapter_plugins_list = []
    """ The list of remote client adapter plugins """

    service_name_remote_client_adapter_plugin_map = {}
    """ The map relating the service name  with the remote client adapter plugin """

    def __init__(self, main_remote_client_manager_plugin):
        """
        Constructor of the class.

        @type main_remote_client_manager_plugin: MainRemoteClientManagerPlugin
        @param main_remote_client_manager_plugin: The main remote client manager plugin.
        """

        self.main_remote_client_manager_plugin = main_remote_client_manager_plugin

        self.remote_client_adapter_plugins_list = []
        self.service_name_remote_client_adapter_plugin_map = {}

    def register_remote_client_adapter_plugin(self, remote_client_adapter_plugin):
        # retrieves the service name
        service_name = remote_client_adapter_plugin.get_service_name()

        if not remote_client_adapter_plugin in self.remote_client_adapter_plugins_list:
            self.remote_client_adapter_plugins_list.append(remote_client_adapter_plugin)

        if not service_name in self.service_name_remote_client_adapter_plugin_map:
            self.service_name_remote_client_adapter_plugin_map[service_name] = remote_client_adapter_plugin

    def unregister_remote_client_adapter_plugin(self, remote_client_adapter_plugin):
        # retrieves the service name
        service_name = remote_client_adapter_plugin.get_service_name()

        if remote_client_adapter_plugin in self.remote_client_adapter_plugins_list:
            self.remote_client_adapter_plugins_list.remove(remote_client_adapter_plugin)

        if service_name in self.service_name_remote_client_adapter_plugin_map:
            del self.service_name_remote_client_adapter_plugin_map[service_name]

    def create_remote_client(self, service_name, service_attributes):
        """
        Creates a remote client for the given service name,
        with the given service attributes.

        @type service_name: String
        @param service_name: The name of the client service to be used.
        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: RemoteClient
        @return: The created remote client.
        """

        if not service_name in self.service_name_remote_client_adapter_plugin_map:
            return

        # retrieves the remote client adapter plugin
        remote_client_adapter_plugin = self.service_name_remote_client_adapter_plugin_map[service_name]

        # creates the remote client instance
        remote_client = remote_client_adapter_plugin.create_remote_client(service_attributes)

        return remote_client

class RemoteClient:
    """
    The remote client class.
    """

    def __init__(self):
        pass
