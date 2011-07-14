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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

SERVICE_ID = "main_distribution_service"
""" The service id """

CURRENT_TIME_VALUE = "current_time"
""" The current time value """

class MainDistributionService:
    """
    The main distribution service class.
    """

    main_distribution_service_plugin = None
    """ The main distribution service plugin """

    def __init__(self, main_distribution_service_plugin):
        """
        Constructor of the class.

        @type main_distribution_service_plugin: MainDistributionServicePlugin
        @param main_distribution_service_plugin: The main distribution service plugin.
        """

        self.main_distribution_service_plugin = main_distribution_service_plugin

    def get_service_id(self):
        return SERVICE_ID

    def get_service_alias(self):
        return []

    def get_available_rpc_methods(self):
        return []

    def get_rpc_methods_alias(self):
        return {}

    def get_all_registry_entries(self):
        return []

    def ping(self):
        # retrieves the current time
        current_time = time.time()

        # creates the information ping map
        ping_map = {
            CURRENT_TIME_VALUE : current_time
        }

        # returns the ping map (structure)
        return ping_map

    def unload_plugin_manager(self):
        # retrieves the plugin manager
        manager = self.main_distribution_service_plugin.manager

        # unloads the plugin manager system
        manager.unload_system()

    def unload_plugin_by_id(self, plugin_id):
        # retrieves the plugin manager
        manager = self.main_distribution_service_plugin.manager

        # unloads the plugin
        manager.unload_plugin(plugin_id)

    def get_plugin_proxy_by_id(self, plugin_id):
        # retrieves the main distribution plugin system plugin
        main_distribution_plugin_system_plugin = self.main_distribution_service_plugin.main_distribution_plugin_system_plugin

        # creates the plugin proxy using the plugin id
        plugin_proxy = main_distribution_plugin_system_plugin.create_plugin_proxy_by_id(plugin_id)

        # returns the plugin proxy
        return plugin_proxy

    def call_plugin_proxy_method(self, plugin_id, plugin_version, method_name, arguments):
        # retrieves the plugin manager
        manager = self.main_distribution_service_plugin.manager

        # retrieves the plugin for the given id and version
        plugin = manager.get_plugin_by_id_and_version(plugin_id, plugin_version)

        # retrieves the method
        method = getattr(plugin, method_name)

        # calls the method retrieving the return value
        return_value = method(*arguments)

        # returns the return value
        return return_value
