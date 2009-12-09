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

CONSOLE_EXTENSION_NAME = "scheduler"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### SCHEDULER HELP ###\n\
show_all_scheduler - shows all the scheduled tasks"
""" The help text """

TABLE_TOP_TEXT = "ID      TASK            TIME      RECURSIVITY"
""" The table top text """

class ConsoleScheduler:
    """
    The console scheduler class.
    """

    scheduler_plugin = None
    """ The scheduler plugin """

    commands = ["show_all_scheduler"]
    """ The commands list """

    def __init__(self, scheduler_plugin):
        """
        Constructor of the class.

        @type scheduler_plugin: SchedulerPlugin
        @param scheduler_plugin: The scheduler plugin.
        """

        self.scheduler_plugin = scheduler_plugin

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

    def process_show_all_scheduler(self, args, output_method):
        # prints the table top text
        output_method(TABLE_TOP_TEXT)

        # retrieves the scheduler instance
        scheduler = self.scheduler_plugin.scheduler

        # retrieves all the available scheduler items
        scheduler_items = scheduler.get_all_scheduler_items()

        # iterates over all the scheduler items
        for scheduler_item in scheduler_items:
            output_method(scheduler_item.item_id, True)
