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

CONSOLE_EXTENSION_NAME = "file_system"
""" The console extension name """

class MainConsoleFileSystem:
    """
    The main console base class.
    """

    main_console_file_system_plugin = None
    """ The main console file system plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, main_console_file_system_plugin):
        """
        Constructor of the class.

        @type main_console_file_system_plugin: MainConsoleFileSystemPlugin
        @param main_console_file_system_plugin: The main console file system plugin.
        """

        self.main_console_file_system_plugin = main_console_file_system_plugin

        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_cd(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the cd command, with the given
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

        # retrieves the path argument
        path = arguments_map["path"]

        # retrieves the full path for the "new" console
        # context path
        console_context_path = console_context.get_full_path(path)

        # retrieves the path exists and is directory
        path_is_directory = os.path.isdir(console_context_path)

        # in case the path is not a directory
        if not path_is_directory:
            # writes the invalid path message
            output_method("invalid path '%s'" % path)

            # returns immediately
            return

        # sets the console context path
        console_context.set_path(console_context_path)

    def process_ls(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the ls command, with the given
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

        # retrieves the path from the arguments
        path = arguments_map.get("path", None)

        # retrieves the path
        console_context_path = console_context.get_path()

        # sets the path value
        path = path or console_context_path

        # retrieves the "full" path
        full_path = console_context.get_full_path(path)

        # retrieves the path exists value
        path_exists = os.path.exists(full_path)

        # in case the path does not exists
        if not path_exists:
            # writes the invalid path message
            output_method("invalid path '%s'" % path)

            # returns immediately
            return

        # retrieves the path is a directory
        path_is_directory = os.path.isdir(full_path)

        # in case the path is a directory
        if path_is_directory:
            # retrieves the path names
            path_names = os.listdir(full_path)

            # sets the path contents as the
            # path names
            path_contents = path_names
        else:
            # retrieves the path base name
            path_base_name = os.path.basename(full_path)

            # sets the path contents as the
            # path base name
            path_contents = [path_base_name]

        # iterates over all the path contents
        for path_item in path_contents:
            # writes the value of the path item
            output_method(path_item)

    def process_pwd(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the pwd command, with the given
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

        # retrieves the console context path
        console_context_path = console_context.get_path()

        # writes the value of the console context path
        output_method(console_context_path)

    def process_cat(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the cat command, with the given
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

        # retrieves the path from the arguments
        path = arguments_map["path"]

        # retrieves the full path using the console context
        full_path = console_context.get_full_path(path)

        # read the file in the path
        file = open(full_path, "rb")

        try:
            # reads the file contents
            file_contents = file.read()

            # writes the file contents
            output_method(file_contents)
        finally:
            # closes the file
            file.close()

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

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
                        "cd" : {
                            "handler" : self.process_cd,
                            "description" : "changes the current directory",
                            "arguments" : [
                                {
                                    "name" : "path",
                                    "description" : "the path to be used for cd",
                                    "values" : self.get_path_names_list,
                                    "mandatory" : True
                                }
                            ]
                        },
                        "ls" : {
                            "handler" : self.process_ls,
                            "description" : "list the contents of the current path",
                            "arguments" : [
                                {
                                    "name" : "path",
                                    "description" : "the path to be used for ls",
                                    "values" : self.get_path_names_list,
                                    "mandatory" : False
                                }
                            ]
                        },
                        "pwd" : {
                            "handler" : self.process_pwd,
                            "description" : "show the present working directory"
                        },
                        "cat" : {
                            "handler" : self.process_cat,
                            "description" : "prints the file in the path to the output",
                            "arguments" : [
                                {
                                    "name" : "path",
                                    "description" : "the path to be used for cat",
                                    "values" : self.get_path_names_list,
                                    "mandatory" : True
                                }
                            ]
                        }
                    }

        # returns the commands map
        return commands_map
