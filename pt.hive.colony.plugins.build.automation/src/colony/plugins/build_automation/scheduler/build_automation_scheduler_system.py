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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class BuildAutomationScheduler:
    """
    The build automation scheduler class.
    """

    build_automation_scheduler_plugin = None
    """ The build automation scheduler plugin """

    build_automation_scheduling_item_list = []
    """ The build automation scheduling item list """

    def __init__(self, build_automation_scheduler_plugin):
        """
        Constructor of the class.

        @type build_automation_scheduler_plugin: BuildAutomationSchedulerPlugin
        @param build_automation_scheduler_plugin: The build automation scheduler plugin.
        """

        self.build_automation_scheduler_plugin = build_automation_scheduler_plugin

        self.build_automation_scheduling_item_list = []

    def register_build_automation_plugin_id(self, plugin_id, date_time, recursion_list):
        # retrieves the build automation plugin
        build_automation_plugin = self.build_automation_scheduler_plugin.build_automation_plugin

        # retrieves the scheduler plugin
        scheduler_plugin = self.build_automation_scheduler_plugin.scheduler_plugin

        # retrieves the guid plugin
        guid_plugin = self.build_automation_scheduler_plugin.guid_plugin

        # generates a guid for the item id
        item_id = guid_plugin.generate_guid()

        # retrieves the method call
        method_call = build_automation_plugin.run_automation_plugin_id

        # creates the list of method arguments
        method_arguments = [plugin_id]

        # creates a new build automation scheduling item
        build_automation_scheduling_item = BuildAutomationSchedulingItem(item_id, method_call, method_arguments)

        # creates the task arguments map
        task_arguments = {}

        # sets the method in the task arguments
        task_arguments["method"] = self.scheduling_handler

        # sets the method arguments in the task arguments
        task_arguments["method_arguments"] = [build_automation_scheduling_item]

        # retrieves the task class
        task_class = scheduler_plugin.get_task_class()

        # creates the build automation task class
        build_automation_task = task_class("method_call", task_arguments)

        # schedules the task as absolute and recursive
        scheduler_plugin.register_task_date_time_absolute_recursive(build_automation_task, date_time, recursion_list)

        # adds the build automation scheduling item to the build automation scheduling item list
        self.build_automation_scheduling_item_list.append(build_automation_scheduling_item)

    def scheduling_handler(self, build_automation_scheduling_item):
        # retrieves the callback method
        callback_method = build_automation_scheduling_item.callback_method

        # retrieves the callback method arguments
        callback_method_arguments = build_automation_scheduling_item.callback_method_arguments

        # calls the callback method with the given arguments
        callback_method(*callback_method_arguments)

    def get_all_build_automation_scheduling_items(self):
        return self.build_automation_scheduling_item_list

class BuildAutomationSchedulingItem:

    item_id = "none"
    """ The item id """

    callback_method = None
    """ The callback method """

    callback_method_arguments = []
    """ The callback method arguments """

    def __init__(self, item_id = "none", callback_method = None, callback_method_arguments = []):
        self.item_id =  item_id
        self.callback_method = callback_method
        self.callback_method_arguments = callback_method_arguments
