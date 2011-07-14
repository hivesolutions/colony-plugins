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

SERVICE_NAME = "jsonrpc"

class MainJsonrpcClient:
    """
    The main jsonrpc client class.
    """

    main_jsonrpc_client_plugin = None
    """ The main jsonrpc client plugin """

    def __init__(self, main_jsonrpc_client_plugin):
        """
        Constructor of the class.

        @type main_jsonrpc_client_plugin: MainJsonrpcClientPlugin
        @param main_jsonrpc_client_plugin: The main jsonrpc client plugin.
        """

        self.main_jsonrpc_client_plugin = main_jsonrpc_client_plugin

    def get_service_name(self):
        """
        Retrieves the service name.

        @rtype: String
        @return: The service name.
        """

        return SERVICE_NAME

    def create_remote_client(self, service_attributes):
        pass

class JsonrpcClient:
    """
    The jsonrpc client class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass
