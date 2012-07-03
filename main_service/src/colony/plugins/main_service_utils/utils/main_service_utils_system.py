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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import threading

import main_service_utils_sync
import main_service_utils_async
import main_service_utils_exceptions

PORT_RANGES = (
    (38001, 39999),
    (40001, 42999)
)
""" The ranges of port available for services """

SERVICE_CLASSES_MAP = {
    "sync" : main_service_utils_sync.AbstractService,
    "async" : main_service_utils_async.AbstractService
}
""" The map containing the various abstract service types """

class MainServiceUtils:
    """
    The main service utils class.
    """

    main_service_utils_plugin = None
    """ The main service utils plugin """

    socket_provider_plugins_map = {}
    """ The socket provider plugins map """

    socket_upgrader_plugins_map = {}
    """ The socket upgrader plugins map """

    port_generation_lock = None
    """ The lock to protect port generation """

    current_port_range_index = 0
    """ The current port range index being used """

    current_port = None
    """ The current port """

    def __init__(self, main_service_utils_plugin):
        """
        Constructor of the class.

        @type main_service_utils_plugin: MainServiceUtilsPlugin
        @param main_service_utils_plugin: The main service utils plugin.
        """

        self.main_service_utils_plugin = main_service_utils_plugin

        self.socket_provider_plugins_map = {}
        self.socket_upgrader_plugins_map = {}
        self.port_generation_lock = threading.Lock()

        # resets the port value
        self._reset_port()

    def generate_service(self, parameters):
        """
        Generates a new service for the given parameters.
        The generated service includes the creation of a new pool.

        @type parameters: Dictionary
        @param parameters: The parameters for service generation.
        @rtype: AbstractService
        @return: The generated service.
        """

        # retrieves the service type from the parameters in order
        # to retrieve the proper (abstract) service class
        service_type = parameters.get("service_type", "sync")
        service_class = SERVICE_CLASSES_MAP.get(service_type, main_service_utils_sync.AbstractService)

        # creates the service "instance" using the abstract service class
        service_instance = service_class(self, self.main_service_utils_plugin, parameters)

        # returns the service instance
        return service_instance

    def generate_service_port(self, parameters):
        """
        Generates a new service port for the current
        host, avoiding collisions.

        @type parameters: Dictionary
        @param parameters: The parameters for service port generation.
        @rtype: int
        @return: The newly generated port.
        """

        # acquires the port generation lock
        self.port_generation_lock.acquire()

        # increments the current port number
        self.current_port += 1

        # retrieves the initial and final port of the current
        # port range
        _initial_port, final_port = PORT_RANGES[self.current_port_range_index]

        # in case the current port is bigger than the final port
        if self.current_port > final_port:
            # increments the current port range index
            self.current_port_range_index += 1

            # in case the limit of port ranges has been reached
            if self.current_port_range_index == len(PORT_RANGES):
                # raises the port starvation reached exception
                raise main_service_utils_exceptions.PortStarvationReached("no more ports available")
            else:
                # resets the current port value
                self._reset_port()

                # increments the current port value
                self.current_port += 1

        # releases the port generation lock
        self.port_generation_lock.release()

        # returns the current port
        return self.current_port

    def socket_provider_load(self, socket_provider_plugin):
        """
        Loads a socket provider plugin.

        @type socket_provider_plugin: Plugin
        @param socket_provider_plugin: The socket provider plugin
        to be loaded.
        """

        # retrieves the plugin provider name
        provider_name = socket_provider_plugin.get_provider_name()

        # sets the socket provider plugin in the socket provider plugins map
        self.socket_provider_plugins_map[provider_name] = socket_provider_plugin

    def socket_provider_unload(self, socket_provider_plugin):
        """
        Unloads a socket provider plugin.

        @type socket_provider_plugin: Plugin
        @param socket_provider_plugin: The socket provider plugin
        to be unloaded.
        """

        # retrieves the plugin provider name
        provider_name = socket_provider_plugin.get_provider_name()

        # removes the socket provider plugin from the socket provider plugins map
        del self.socket_provider_plugins_map[provider_name]

    def socket_upgrader_load(self, socket_upgrader_plugin):
        """
        Loads a socket upgrader plugin.

        @type socket_upgrader_plugin: Plugin
        @param socket_upgrader_plugin: The socket upgrader plugin
        to be loaded.
        """

        # retrieves the plugin upgrader name
        upgrader_name = socket_upgrader_plugin.get_upgrader_name()

        # sets the socket upgrader plugin in the socket upgrader plugins map
        self.socket_upgrader_plugins_map[upgrader_name] = socket_upgrader_plugin

    def socket_upgrader_unload(self, socket_upgrader_plugin):
        """
        Unloads a socket upgrader plugin.

        @type socket_upgrader_plugin: Plugin
        @param socket_upgrader_plugin: The socket upgrader plugin
        to be unloaded.
        """

        # retrieves the plugin upgrader name
        upgrader_name = socket_upgrader_plugin.get_upgrader_name()

        # removes the socket upgrader plugin from the socket upgrader plugins map
        del self.socket_upgrader_plugins_map[upgrader_name]

    def _reset_port(self):
        """
        Resets the current port value to the initial
        value of the current port range.
        """

        # retrieves the initial and final port of the current
        # port range
        initial_port, _final_port = PORT_RANGES[self.current_port_range_index]

        # sets the current port as the initial port of
        # the port range (minus one)
        self.current_port = initial_port - 1
