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

CONSOLE_EXTENSION_NAME = "ice_service_manager"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### ICE SERVICE MANAGER HELP ###\n\
list_ice_services                - lists all the available ice services\n\
start_ice_service <service-name> - starts an ice service with the given service name\n\
stop_ice_service <service-name>  - stops an ice service with the given service name"
""" The help text """

class ConsoleIceServiceManager:
    """
    The console ice service manager class.
    """

    ice_service_manager_plugin = None
    """ The ice service manager plugin """

    commands = ["list_ice_services", "start_ice_service", "stop_ice_service"]
    """ The commands list """

    def __init__(self, ice_service_manager_plugin):
        """
        Constructor of the class.

        @type ice_service_manager_plugin: IceServiceManagerPlugin
        @param ice_service_manager_plugin: The ice service manager plugin.
        """

        self.ice_service_manager_plugin = ice_service_manager_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_list_ice_services(self, args, output_method):
        ice_service_descriptors = self.ice_service_manager_plugin.ice_service_manager.get_registered_ice_service_descriptors()

        for ice_service_descriptor in ice_service_descriptors:
            self.print_ice_service_descriptor(ice_service_descriptor, output_method)

    def process_start_ice_service(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        ice_service_name = args[0]

        self.ice_service_manager_plugin.ice_service_manager.start_service(ice_service_name)

    def process_stop_ice_service(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        ice_service_name = args[0]

        self.ice_service_manager_plugin.ice_service_manager.stop_service(ice_service_name)

    def print_ice_service_descriptor(self, ice_service_descriptor, output_method):
        output_method("name:             " + ice_service_descriptor.name)
        output_method("description:      " + ice_service_descriptor.description)
        output_method("server_file_path: " + ice_service_descriptor.server_file_path)
