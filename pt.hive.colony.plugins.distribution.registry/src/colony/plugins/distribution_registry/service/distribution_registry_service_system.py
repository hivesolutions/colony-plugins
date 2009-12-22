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

SERVICE_ID = "distribution_registry"
""" The service id """

class DistributionRegistryService:
    """
    The distribution registry service class.
    """

    distribution_registry_service_plugin = None
    """ The distribution registry service plugin """

    def __init__(self, distribution_registry_service_plugin):
        """
        Constructor of the class.

        @type distribution_registry_service_plugin: DistributionRegistryServicePlugin
        @param distribution_registry_service_plugin: The distribution registry service plugin.
        """

        self.distribution_registry_service_plugin = distribution_registry_service_plugin

    def get_service_id(self):
        return SERVICE_ID

    def get_service_alias(self):
        return []

    def get_available_rpc_methods(self):
        return []

    def get_rpc_methods_alias(self):
        return {}

    def register_entry(self, hostname, name, type, endpoints, metadata):
        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_registry_service_plugin.distribution_registry_plugin

        distribution_registry_plugin.register_entry(hostname, name, type, endpoints, metadata)

    def unregister_entry(self, hostname, name):
        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_registry_service_plugin.distribution_registry_plugin

        distribution_registry_plugin.unregister_entry(hostname, name)

    def get_all_registry_entries(self):
        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_registry_service_plugin.distribution_registry_plugin

        return distribution_registry_plugin.get_all_registry_entries()
