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

__revision__ = "$LastChangedRevision: 12670 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-13 13:08:29 +0000 (qui, 13 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

CONSOLE_EXTENSION_NAME = "main_packing_manager"
""" The console extension name """

class ConsoleMainPackingManager:
    """
    The console main packing manager class.
    """

    main_packing_manager_plugin = None
    """ The main packing manager plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, main_packing_manager_plugin):
        """
        Constructor of the class.

        @type main_packing_manager_plugin: MainPackingManagerPlugin
        @param main_packing_manager_plugin: The main packing manager plugin.
        """

        self.main_packing_manager_plugin = main_packing_manager_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_pack(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the pack command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the main packing manager
        main_packing_manager = self.main_packing_manager_plugin.main_packing_manager

        # retrieves the current path
        current_path = console_context.get_path()

        # retrieves the path from the arguments
        path = arguments_map["path"]

        # retrieves the service name from the arguments
        service_name = arguments_map.get("service_name", "colony")

        # retrieves the target path from the arguments
        target_path = arguments_map.get("target_path", current_path)

        # retrieves the full path using the console context
        full_path = console_context.get_full_path(path)

        # creates the properties map for the directory packing
        properties = {
            "target_path" : target_path
        }

        # packs the files using the main packing manager
        main_packing_manager.pack_files([full_path], properties, service_name)

    def process_unpack(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the unpack command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the main packing manager
        main_packing_manager = self.main_packing_manager_plugin.main_packing_manager

        # retrieves the current path
        current_path = console_context.get_path()

        # retrieves the path from the arguments
        path = arguments_map["path"]

        # retrieves the service name from the arguments
        service_name = arguments_map.get("service_name", "colony")

        # retrieves the target path from the arguments
        target_path = arguments_map.get("target_path", current_path)

        # retrieves the full path using the console context
        full_path = console_context.get_full_path(path)

        # creates the properties map for the directory packing
        properties = {
            "target_path" : target_path
        }

        # unpacks the files using the main packing manager
        main_packing_manager.unpack_files([full_path], properties, service_name)

    def get_path_names_list(self, argument, console_context):
        # retrieves the directory name from the argument
        directory_name = os.path.dirname(argument)

        # retrieves the "full" path
        path = console_context.get_full_path(directory_name)

        # retrieves the path exists value
        path_exists = os.path.exists(path)

        # in case the path does
        # not exists
        if not path_exists:
            # returns empty list
            return []

        # retrieves the path names
        path_names = os.listdir(path)

        # in case the directory name is set
        if directory_name:
            # re-creates the path name joining the directory name
            path_names = [os.path.join(directory_name, value) for value in path_names]

        # returns the path names list
        return path_names

    def get_service_names_list(self, argument, console_context):
        # retrieves the main packing manager
        main_packing_manager = self.main_packing_manager_plugin.main_packing_manager

        # retrieves the service name packing service plugin map
        service_name_packing_service_plugin_map = main_packing_manager.service_name_packing_service_plugin_map

        # retrieves the service name packing service plugin map keys
        service_name_packing_service_plugin_map_keys = service_name_packing_service_plugin_map.keys()

        # returns the service name packing service plugin map keys
        return service_name_packing_service_plugin_map_keys

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "pack" : {
                "handler" : self.process_pack,
                "description" : "packs the given file with the given type",
                "arguments" : [
                    {
                        "name" : "path",
                        "description" : "the path to the file to be used in packing",
                        "values" : self.get_path_names_list,
                        "mandatory" : True
                    },
                    {
                        "name" : "service_name",
                        "description" : "the name of the service to be used for packing",
                        "values" : self.get_service_names_list,
                        "mandatory" : False
                    },
                    {
                        "name" : "target_path",
                        "description" : "the path to deploy the created package",
                        "values" : self.get_path_names_list,
                        "mandatory" : False
                    }
                ]
            },
            "unpack" : {
                "handler" : self.process_unpack,
                "description" : "unpacks the given file with the given type",
                "arguments" : [
                    {
                        "name" : "path",
                        "description" : "the path to the file to be used in unpacking",
                        "values" : self.get_path_names_list,
                        "mandatory" : True
                    },
                    {
                        "name" : "service_name",
                        "description" : "the name of the service to be used for unpacking",
                        "values" : self.get_service_names_list,
                        "mandatory" : False
                    },
                    {
                        "name" : "target_path",
                        "description" : "the path to deploy the destroyed package",
                        "values" : self.get_path_names_list,
                        "mandatory" : False
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
