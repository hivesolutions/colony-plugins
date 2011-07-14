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

import xmlrpclib

SERVICE_NAME = "xmlrpc"
""" The service name """

class MainXmlrpcClient:
    """
    The main xmlrpc client class.
    """

    main_xmlrpc_client_plugin = None
    """ The main xmlrpc client plugin """

    def __init__(self, main_xmlrpc_client_plugin):
        """
        Constructor of the class.

        @type main_xmlrpc_client_plugin: MainXmlrpcClientPlugin
        @param main_xmlrpc_client_plugin: The main xmlrpc client plugin.
        """

        self.main_xmlrpc_client_plugin = main_xmlrpc_client_plugin

    def get_service_name(self):
        return SERVICE_NAME

    def create_remote_client(self, service_attributes):
        # creates a new xmlrpc client instance
        xmlrpc_client = XmlrpcClient()

        # retrieves the xmlrpc server address
        xmlrpc_server_address = service_attributes["xmlrpc_server_address"]

        # sets the xmlrpc server address
        xmlrpc_client.xmlrpc_server_address = xmlrpc_server_address

        return xmlrpc_client

class XmlrpcClient:
    """
    The xmlrpc client class.
    """

    xmlrpc_server_address = "none"
    """ The xmlrpc server address """

    xmlrpc_server_proxy = None
    """ The xmlrpc server proxy """

    def __init__(self, xmlrpc_server_address = "none", xmlrpc_server_proxy = None):
        """
        Constructor of the class.

        @type xmlrpc_server_address: String
        @param xmlrpc_server_address: The xmlrpc server address.
        @type xmlrpc_server_proxy: ServerProxy
        @param xmlrpc_server_proxy: The xmlrpc server proxy.
        """

        self.xmlrpc_server_address = xmlrpc_server_address
        self.xmlrpc_server_proxy = xmlrpc_server_proxy

    def get_xmlrpc_server_proxy(self):
        """
        Retrieves the server proxy.

        @rtype: ServerProxy
        @return: The xmlrpc server proxy.
        """

        if not self.xmlrpc_server_proxy:
            self.xmlrpc_server_proxy = xmlrpclib.ServerProxy(self.xmlrpc_server_address)

        return self.xmlrpc_server_proxy

    def __nonzero__(self):
        return True

    def __getattr__(self, name):
        # retrieves the xmlrpc server proxy
        xmlrpc_server_proxy = self.get_xmlrpc_server_proxy()

        # retrieves the xmlrpc name proxy
        xmlrpc_name_proxy = getattr(xmlrpc_server_proxy, name)

        # sets the attribute
        setattr(self, name, xmlrpc_name_proxy)

        return xmlrpc_name_proxy
