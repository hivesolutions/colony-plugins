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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 12939 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-02-01 17:54:16 +0000 (Tue, 01 Feb 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import datetime

CONSOLE_EXTENSION_NAME = "automation_scheduler"
""" The console extension name """

TABLE_TOP_TEXT = "ID      DATE_TIME      RECURSION      BUILD AUTOMATION ID"
""" The table top text """

COLUMN_SPACING = 8
""" The column spacing """

DATE_FORMAT = "%d-%m-%Y"
""" The date format """

DATE_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"
""" The date time format """

INVALID_DATE_TIME_MESSAGE = "invalid date time value"
""" The invalid date time message """

INVALID_RECURSION_MESSAGE = "invalid recursion value"
""" The invalid recursion message """

class ConsoleBuildAutomationScheduler:
    """
    The console build automation scheduler class.
    """

    build_automation_scheduler_plugin = None
    """ The build automation scheduler plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, build_automation_scheduler_plugin):
        """
        Constructor of the class.

        @type build_automation_scheduler_plugin: BuildAutomationSchedulerPlugin
        @param build_automation_scheduler_plugin: The build automation scheduler plugin.
        """

        self.build_automation_scheduler_plugin = build_automation_scheduler_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_schedule_automation(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the run automation command, with the given
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

        # retrieves the mandatory arguments
        plugin_id = arguments_map["plugin_id"]
        date_time = arguments_map["date_time"]
        recursion = arguments_map["recursion"]

        # retrieves the build automation scheduler
        build_automation_scheduler = self.build_automation_scheduler_plugin.build_automation_scheduler

        # retrieves the date time length
        date_time_len = len(date_time)

        if date_time_len == 10:
            date_time_value = datetime.datetime.strptime(date_time, DATE_FORMAT)
        elif date_time_len == 19:
            date_time_value = datetime.datetime.strptime(date_time, DATE_TIME_FORMAT)
        else:
            output_method(INVALID_DATE_TIME_MESSAGE)
            return

        recursion_strip = recursion.strip()
        recursion_split = recursion_strip.split(",")

        if not len(recursion_split) == 5:
            output_method(INVALID_RECURSION_MESSAGE)
            return

        recursion_list = []

        for recursion_split_item in recursion_split:
            recursion_split_item_int = int(recursion_split_item)
            recursion_list.append(recursion_split_item_int)

        build_automation_scheduler.register_build_automation_scheduler_plugin_id(plugin_id, date_time_value, recursion_list)

    def process_show_all_automation_scheduler(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the show all automation scheduler command, with the given
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

        # prints the table top text
        output_method(TABLE_TOP_TEXT)

        # retrieves the build automation scheduler instance
        build_automation_scheduler = self.build_automation_scheduler_plugin.build_automation_scheduler

        # retrieves all the available build automation scheduling items
        build_automation_scheduling_items = build_automation_scheduler.get_all_build_automation_scheduling_items()

        # iterates over all the build automation scheduling items
        for build_automation_scheduling_item in build_automation_scheduling_items:
            output_method(build_automation_scheduling_item.item_id, True)

    def get_plugin_id_list(self, argument, console_context):
        # retrieves the plugin manager
        plugin_manager = self.build_automation_scheduler_plugin.manager

        # retrieves the plugin id list
        plugin_id_list = plugin_manager.plugin_instances_map.keys()

        # returns the plugin id list
        return plugin_id_list

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "schedule_automation" : {
                "handler" : self.process_schedule_automation,
                "description" : "schedules the given automation",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to perform the build automation in",
                        "values" : self.get_plugin_id_list,
                        "mandatory" : True
                    },
                    {
                        "name" : "date_time",
                        "description" : "the date when to run the build automation",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "recursion",
                        "description" : "the build automation recursion",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "plugin_version",
                        "description" : "the version of the plugin to perform the build automation in",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            },
            "show_all_automation_scheduler" : {
                "handler" : self.process_show_all_automation_scheduler,
                "description" : "shows all the scheduled build automations"
            }
        }

        # returns the commands map
        return commands_map
