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

__revision__ = "$LastChangedRevision: 12938 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-02-01 17:43:36 +0000 (Tue, 01 Feb 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "scheduler"
""" The console extension name """

TABLE_TOP_TEXT = "ID      TASK            TIME      RECURSIVITY"
""" The table top text """

class ConsoleScheduler:
    """
    The console scheduler class.
    """

    scheduler_plugin = None
    """ The scheduler plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, scheduler_plugin):
        """
        Constructor of the class.

        @type scheduler_plugin: SchedulerPlugin
        @param scheduler_plugin: The scheduler plugin.
        """

        self.scheduler_plugin = scheduler_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_show_all_scheduler(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the show all scheduler command, with the given
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

        # retrieves the scheduler instance
        scheduler = self.scheduler_plugin.scheduler

        # retrieves all the available scheduler items
        scheduler_items = scheduler.get_all_scheduler_items()

        # iterates over all the scheduler items
        for scheduler_item in scheduler_items:
            output_method(scheduler_item.item_id, True)

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
                        "show_all_scheduler" : {
                            "handler" : self.process_show_all_scheduler,
                            "description" : "shows all the scheduled tasks"
                        }
                    }

        # returns the commands map
        return commands_map
