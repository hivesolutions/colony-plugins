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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

import colony.libs.map_util

CONSOLE_EXTENSION_NAME = "log_analyzer"
""" The console extension name """

class ConsoleHttpLogAnalyzer:
    """
    The console log analyzer class.
    """

    http_log_analyzer_plugin = None
    """ The log analyzer plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, http_log_analyzer_plugin):
        """
        Constructor of the class.

        @type http_log_analyzer_plugin: HttpLogAnalyzerPlugin
        @param http_log_analyzer_plugin: The http log analyzer plugin.
        """

        self.http_log_analyzer_plugin = http_log_analyzer_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_analyze_http_log(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the analyze http log command, with the given
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

        # retrieves the log analyzer
        log_analyzer = self.http_log_analyzer_plugin.log_analyzer

        # retrieves the path from the arguments
        path = arguments_map["path"]

        # retrieves the log type from the arguments
        log_type = arguments_map.get("log_type", "common")

        # retrieves the full path using the console context
        full_path = console_context.get_full_path(path)

        # analyzes the log file
        log_analyzis_map = log_analyzer.analyze_log(full_path, log_type)

        # outputs the log analyzis map
        colony.libs.map_util.map_output(log_analyzis_map, output_method)

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
            "analyze_http_log" : {
                "handler" : self.process_analyze_http_log,
                "description" : "analyzes the specified http log file",
                "arguments" : [
                    {
                        "name" : "path",
                        "description" : "the http log file path",
                        "values" : self.get_path_names_list,
                        "mandatory" : True
                    },
                    {
                        "name" : "log_type",
                        "description" : "the http log type",
                        "values" : ("common",),
                        "mandatory" : False
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
