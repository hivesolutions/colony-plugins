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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import ssl
import socket

PROVIDER_NAME = "ssl"
""" The provider name """

RESOURCES_PATH = "main_service_ssl_socket_provider/ssl_socket_provider/resources"
""" The resources path """

class MainServiceSslSocketProvider:
    """
    The main service ssl socket provider class.
    """

    main_service_ssl_socket_provider_plugin = None
    """ The main service ssl socket provider plugin """

    def __init__(self, main_service_ssl_socket_provider_plugin):
        """
        Constructor of the class.

        @type main_service_ssl_socket_provider_plugin: MainServiceSslSocketProviderPlugin
        @param main_service_ssl_socket_provider_plugin: The main service ssl socket provider plugin.
        """

        self.main_service_ssl_socket_provider_plugin = main_service_ssl_socket_provider_plugin

    def get_provider_name(self):
        return PROVIDER_NAME

    def provide_socket(self):
        # retrieves the plugin manager
        manager = self.main_service_ssl_socket_provider_plugin.manager

        # retrieves the main service ssl socket provicer plugin base path
        main_service_ssl_socket_provicer_plugin_path = manager.get_plugin_path_by_id(self.main_service_ssl_socket_provider_plugin.id)

        # sets the main service ssl socket provicer plugin resources path
        main_service_ssl_socket_provicer_plugin_resources_path = main_service_ssl_socket_provicer_plugin_path + "/main_service_ssl_socket_provider/ssl_socket_provider/resources"

        # creates the normal socket
        normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # retrieves the dummy ssl key path
        dummy_ssl_key_path = main_service_ssl_socket_provicer_plugin_resources_path + "/dummy.key"

        # retrieves the dummy ssl certificate path
        dummy_ssl_certificate_path = main_service_ssl_socket_provicer_plugin_resources_path + "/dummy.crt"

        # warps the normal socket into an ssl socket
        ssl_socket = ssl.wrap_socket(normal_socket, dummy_ssl_key_path, dummy_ssl_certificate_path)

        # returns the ssl socket
        return ssl_socket
