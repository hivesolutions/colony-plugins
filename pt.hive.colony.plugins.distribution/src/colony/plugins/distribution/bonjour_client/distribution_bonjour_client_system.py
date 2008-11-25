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

class DistributionBonjourClient:
    """
    The distribution bonjour client class.
    """

    distribution_bonjour_client_plugin = None
    """ The distribution bonjour client plugin """

    def __init__(self, distribution_bonjour_client_plugin):
        """
        Constructor of the class.
        
        @type distribution_bonjour_client_plugin: DistributionBonjourClientPlugin
        @param distribution_bonjour_client_plugin: The distribution bonjour client plugin.
        """

        self.distribution_bonjour_client_plugin = distribution_bonjour_client_plugin

    def get_remote_instance_references(self):
        # retrieves the bonjour plugin
        bonjour_plugin = self.distribution_bonjour_client_plugin.bonjour_plugin

        bonjour_services = bonjour_plugin.browse_bonjour_services("_colony._tcp", "local.", 10)

        for bonjour_service in bonjour_services:
            print bonjour_service
