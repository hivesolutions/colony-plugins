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

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import datetime

CONSOLE_EXTENSION_NAME = "automation_scheduler"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

INVALID_DATE_TIME_MESSAGE = "invalid date time value"
""" The invalid date time message """

INVALID_RECURSION_MESSAGE = "invalid recursion value"
""" The invalid recursion message """

HELP_TEXT = "### BUILD AUTOMATION SCHEDULER HELP ###\n\
schedule_automation <plugin-id> <date-time> <recursion> [plugin-version] - schedules the given automation\n\
show_all_automation_scheduler                                            - shows all the scheduled build automations"
""" The help text """

TABLE_TOP_TEXT = "ID      DATE_TIME      RECURSION      BUILD AUTOMATION ID"
""" The table top text """

COLUMN_SPACING = 8
""" The column spacing """

DATE_FORMAT = "%d-%m-%Y"
""" The date format """

DATE_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"
""" The date time format """

class ConsoleBuildAutomationScheduler:
    """
    The console build automation scheduler class.
    """

    build_automation_scheduler_plugin = None
    """ The build automation scheduler plugin """

    commands = ["schedule_automation", "show_all_automation_scheduler"]
    """ The commands list """

    def __init__(self, build_automation_scheduler_plugin):
        """
        Constructor of the class.

        @type build_automation_scheduler_plugin: BuildAutomationSchedulerPlugin
        @param build_automation_scheduler_plugin: The build automation scheduler plugin.
        """

        self.build_automation_scheduler_plugin = build_automation_scheduler_plugin

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

    def process_schedule_automation(self, args, output_method):
        if len(args) < 3:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the build  automation scheduler
        build_automation_scheduler = self.build_automation_scheduler_plugin.build_automation_scheduler

        # retrieves the plugin id
        plugin_id = args[0]

        # retrieves the date time
        date_time = args[1]

        # retrieves the recursionj list
        recursion = args[2]

        if len(args) > 3:
            plugin_version = args[3]

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

        build_automation_scheduler.register_build_automation_plugin_id(plugin_id, date_time_value, recursion_list)

    def process_show_all_automation_scheduler(self, args, output_method):
        # prints the table top text
        output_method(TABLE_TOP_TEXT)

        # retrieves the build automation scheduler instance
        build_automation_scheduler = self.build_automation_scheduler_plugin.build_automation_scheduler

        # retrieves all the available build automation scheduling items
        build_automation_scheduling_items = build_automation_scheduler.get_all_build_automation_scheduling_items()

        # iterates over all the build automation scheduling items
        for build_automation_scheduling_item in build_automation_scheduling_items:
            output_method(build_automation_scheduling_item.item_id, True)
