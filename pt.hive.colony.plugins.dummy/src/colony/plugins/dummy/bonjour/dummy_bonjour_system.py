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

import socket

class DummyBonjour:
    """
    The dummy bonjour class
    """

    dummy_bonjour_plugin = None
    """ The dummy bonjour plugin """

    def __init__(self, dummy_bonjour_plugin):
        """
        Constructor of the class
        
        @type dummy_bonjour_plugin: DummyBonjourPlugin
        @param dummy_bonjour_plugin: The dummy bonjour plugin
        """

        self.dummy_bonjour_plugin = dummy_bonjour_plugin
    
    def register_bonjour_service(self):
        """
        Registers the dummy bonjour service.
        """

        # retrieves the bonjour plugin
        bonjour_plugin = self.dummy_bonjour_plugin.bonjour_plugin

        # register the dummy bonjour service
        bonjour_plugin.register_bonjour_service(socket.gethostname() + "_dummy_colony", "_dummy_colony._tcp.", "local.", socket.gethostname(), 25)
