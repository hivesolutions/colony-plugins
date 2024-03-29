#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "scheduler"
""" The console extension name """

TABLE_TOP_TEXT = "ID      TASK            TIME      RECURSIVITY"
""" The table top text """


class ConsoleScheduler(object):
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

        :type scheduler_plugin: SchedulerPlugin
        :param scheduler_plugin: The scheduler plugin.
        """

        self.scheduler_plugin = scheduler_plugin
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_show_all_scheduler(
        self, arguments, arguments_map, output_method, console_context
    ):
        """
        Processes the show all scheduler command, with the given
        arguments and output method.

        :type arguments: List
        :param arguments: The arguments for the processing.
        :type arguments_map: Dictionary
        :param arguments_map: The map of arguments for the processing.
        :type output_method: Method
        :param output_method: The output method to be used in the processing.
        :type console_context: ConsoleContext
        :param console_context: The console context for the processing.
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
        return {
            "show_all_scheduler": {
                "handler": self.process_show_all_scheduler,
                "description": "shows all the scheduled tasks",
            }
        }
