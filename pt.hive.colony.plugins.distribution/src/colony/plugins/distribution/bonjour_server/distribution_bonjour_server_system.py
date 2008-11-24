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

import socket

BASE_PROTOCOL_SUFIX = "_tcp"

PROTOCOL_SUFIX = "_colony"

LOCAL_DOMAIN = "local"

DEFAULT_PORT = 25

class DistributionBonjourServer:
    """
    The distribution bonjour server class.
    """

    distribution_bonjour_server_plugin = None
    """ The distribution bonjour server plugin """

    def __init__(self, distribution_bonjour_server_plugin):
        """
        Constructor of the class.
        
        @type distribution_bonjour_server_plugin: DistributionBonjourServerPlugin
        @param distribution_bonjour_server_plugin: The distribution bonjour server plugin.
        """

        self.distribution_bonjour_server_plugin = distribution_bonjour_server_plugin

    def activate_server(self, properties):
        # retrieves the bonjour plugin
        bonjour_plugin = self.distribution_bonjour_server_plugin.bonjour_plugin

        # creates the service id
        service_id = socket.gethostname() + PROTOCOL_SUFIX

        # creates the complete protocol name
        complete_protocol_name = PROTOCOL_SUFIX + "." + BASE_PROTOCOL_SUFIX

        # creates the domain
        domain = LOCAL_DOMAIN + "."

        # creates the hostname
        hostname = socket.gethostname()

        # creates the port
        port = DEFAULT_PORT

        # register the dummy bonjour service
        bonjour_plugin.register_bonjour_service(service_id, complete_protocol_name, domain, hostname, port)
