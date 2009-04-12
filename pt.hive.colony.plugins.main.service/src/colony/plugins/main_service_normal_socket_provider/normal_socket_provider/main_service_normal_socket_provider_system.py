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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import socket

PROVIDER_NAME = "normal"
""" The provider name """

class MainServiceNormalSocketProvider:
    """
    The main service normal socket provider class.
    """

    main_service_normal_socket_provider_plugin = None
    """ The main service normal socket provider plugin """

    def __init__(self, main_service_normal_socket_provider_plugin):
        """
        Constructor of the class.

        @type main_service_normal_socket_provider_plugin: MainServiceNormalSocketProviderPlugin
        @param main_service_normal_socket_provider_plugin: The main service normal socket provider plugin.
        """

        self.main_service_normal_socket_provider_plugin = main_service_normal_socket_provider_plugin

    def get_provider_name(self):
        return PROVIDER_NAME

    def provide_socket(self):
        # creates the normal socket
        normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # returns the normal socket
        return normal_socket
