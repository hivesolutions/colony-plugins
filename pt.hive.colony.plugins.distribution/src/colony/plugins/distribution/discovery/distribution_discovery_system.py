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

import time

METHOD_VALUE = "method"
""" The method value """

METHOD_ARGUMENTS_VALUE = "method_arguments"
""" The method arguments value """

METHOD_CALL_VALUE = "method_call"
""" The method call value """

DEFAULT_RECURSION_LIST = [
    0, 0, 0, 10, 0
]
""" The default recursion list to be used for the task """

class DistributionDiscovery:
    """
    The distribution discovery class.
    """

    distribution_discovery_plugin = None
    """ The distribution discovery plugin """

    distribution_discovery_task = None
    """ The distribution discovery task """

    distribution_discovery_adapter_plugins_map = {}
    """ The distribution discovery adapter plugins map """

    def __init__(self, distribution_discovery_plugin):
        """
        Constructor of the class.

        @type distribution_discovery_plugin: DistributionDiscoveryPlugin
        @param distribution_discovery_plugin: The distribution discovery plugin.
        """

        self.distribution_discovery_plugin = distribution_discovery_plugin

        self.distribution_discovery_task = None
        self.distribution_discovery_adapter_plugins_map = {}

    def load_discovery(self, properties):
        """
        Loads the discovery with the given properties.

        @type properties: List
        @param properties: The list of properties for the load of the discovery.
        """

        # retrieves the scheduler plugin
        scheduler_plugin = self.distribution_discovery_plugin.scheduler_plugin

        # retrieves the current time
        current_time = time.time()

        # retrieves the task class
        task_class = scheduler_plugin.get_task_class()

        # creates the task arguments map
        task_arguments = {
            METHOD_VALUE : self._update_discovery,
            METHOD_ARGUMENTS_VALUE : []
        }

        # creates the distribution discovery task
        self.distribution_discovery_task = task_class(METHOD_CALL_VALUE, task_arguments)

        # registers (schedules) the distribution discovery task as absolute and recursive
        scheduler_plugin.register_task_absolute_recursive(self.distribution_discovery_task, current_time, DEFAULT_RECURSION_LIST)

    def unload_discovery(self, properties):
        """
        Unloads the discovery with the given properties.

        @type properties: List
        @param properties: The list of properties for the unload of the discovery.
        """

        # retrieves the scheduler plugin
        scheduler_plugin = self.distribution_discovery_plugin.scheduler_plugin

        # unregisters the distribution discovery task
        scheduler_plugin.unregister_task(self.distribution_discovery_task)

    def distribution_discovery_adapter_load(self, distribution_discovery_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = distribution_discovery_adapter_plugin.get_adapter_name()

        self.distribution_discovery_adapter_plugins_map[adapter_name] = distribution_discovery_adapter_plugin

    def distribution_discovery_adapter_unload(self, distribution_discovery_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = distribution_discovery_adapter_plugin.get_adapter_name()

        del self.distribution_discovery_adapter_plugins_map[adapter_name]

    def _update_discovery(self):
        # iterates over all the distribution discovery adapter plugins
        for _adapter_name, distribution_discovery_adapter_plugin in self.distribution_discovery_adapter_plugins_map.items():
            # handles a new discover in the distribution discovery adapter plugin
            # this update shall change the current status of the distribution registry
            distribution_discovery_adapter_plugin.handle_discover({})
