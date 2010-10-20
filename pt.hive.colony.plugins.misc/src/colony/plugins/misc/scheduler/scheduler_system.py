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

import time
import sched
import datetime
import threading

import colony.libs.map_util

METHOD_CALL_TYPE = "method_call"
""" The method call type """

CONSOLE_COMMAND_TYPE = "console_command"
""" The console command type """

class Scheduler:
    """
    The scheduler class.
    """

    scheduler_plugin = None
    """ The build automation plugin """

    scheduler_lock = None
    """ The scheduler lock """

    continue_flag = True
    """ The scheduler continue flag """

    scheduler = None
    """ The scheduler object """

    scheduler_items = []
    """ The list of scheduler items """

    startup_items = {}
    """ The startup items """

    def __init__(self, scheduler_plugin):
        """
        Constructor of the class.

        @type scheduler_plugin: SchedulerPlugin
        @param scheduler_plugin: The scheduler plugin.
        """

        self.scheduler_plugin = scheduler_plugin

        # creates a new lock object
        self.scheduler_lock = threading.Lock()

        # sets the continue flag value
        self.continue_flag = True

        # creates the new scheduler object to control the scheduling
        self.scheduler = sched.scheduler(time.time, time.sleep)

        # starts the scheduler items list
        self.scheduler_items = []

        # starts the startup items
        self.startup_items = {}

    def load_scheduler(self):
        # notifies the ready semaphore
        self.scheduler_plugin.release_ready_semaphore()

        # acquires the lock object
        self.scheduler_lock.acquire()

        # loads the startup items
        self._load_startup_items()

        self._load_dummy_item()

        # iterates continuously
        while True:
            # acquires the lock object
            self.scheduler_lock.acquire()

            # in case the continue flag is disabled
            if not self.continue_flag:
                print "VAI PARAR POR CAUSA DA CONTINUE FLAG"

                # breaks the cycle
                break

            # runs the scheduler
            self.scheduler.run()

    def load_dummy_item(self):
        dummy = lambda: True

        current_time = time.time()

        recursion_list = [0, 0, 0, 1, 0]

        # creates the scheduler item from the plugin method and the arguments
        scheduler_item = self.create_scheduler_item(dummy, [], current_time, recursion_list)

        # adds the scheduler item
        self.add_scheduler_item(scheduler_item)

    def unload_scheduler(self):
        print "VAI COMECAR O UNLOADING do scheduler"

        # removes all the active scheduler items
        self.remove_all_active_scheduler_items()

        # sets the continue flag to false
        self.continue_flag = False

        print "VAI TESTAR O LOCK"

        # in case the scheduler lock is locked
        if self.scheduler_lock.locked():
            # releases the lock
            self.scheduler_lock.release()

        print "VAI ACABAR O UNLOADING do scheduler"

    def register_task(self, task, time):
        # calculates the absolute time
        absolute_time = self.timestamp_to_absolute_timestamp(time)

        # registers the task
        return self.register_task_absolute(task, absolute_time)

    def register_task_absolute(self, task, absolute_time):
        return self.register_task_absolute_recursive(task, absolute_time, None)

    def register_task_date_time(self, task, date_time):
        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # calculates the new date time
        new_date_time = current_date_time + date_time

        # converts the new date time to timestamp
        new_timestamp = self.date_time_to_timestamp(new_date_time)

        # registers the task
        return self.register_task_absolute(task, new_timestamp)

    def register_task_date_time_absolute(self, task, absolute_date_time):
        # converts the absolute date time to timestamp
        absolute_timestamp = self.date_time_to_timestamp(absolute_date_time)

        # registers the task
        return self.register_task_absolute(task, absolute_timestamp)

    def register_task_recursive(self, task, time, recursion_list):
        # calculates the absolute time
        absolute_time = self.timestamp_to_absolute_timestamp(time)

        # registers the task
        return self.register_task_absolute_recursive(task, absolute_time, recursion_list)

    def register_task_absolute_recursive(self, task, absolute_time, recursion_list):
        # retrieves the task_type
        task_type = task.task_type

        # retrieves the task arguments
        task_arguments = task.task_arguments

        # in case the task type is of type method_call
        if task_type == METHOD_CALL_TYPE:
            # retrieves the method
            method = task_arguments["method"]

            # retrieve the method arguments
            method_arguments = task_arguments["method_arguments"]

            # creates a new scheduler item
            scheduler_item = self.create_scheduler_item(method, method_arguments, absolute_time, recursion_list)
        # in case the task is of type console_command
        elif task_type == CONSOLE_COMMAND_TYPE:
            # retrieves the console command
            console_command = task_arguments["console_command"]

            # retrieves the main console plugin
            main_console_plugin = self.scheduler_plugin.main_console_plugin

            # retrieves the default console output method
            default_console_output_method = main_console_plugin.get_default_output_method()

            # creates a new scheduler item
            scheduler_item = self.create_scheduler_item(main_console_plugin.process_command_line, [console_command, default_console_output_method], absolute_time, recursion_list)

        # adds the scheduler item
        self.add_scheduler_item(scheduler_item)

    def register_task_date_time_recursive(self, task, date_time, recursion_list):
        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # calculates the new date time
        new_date_time = current_date_time + date_time

        # converts the new date time to timestamp
        new_timestamp = self.date_time_to_timestamp(new_date_time)

        # registers the task
        return self.register_task_absolute_recursive(task, new_timestamp, recursion_list)

    def register_task_date_time_absolute_recursive(self, task, absolute_date_time, recursion_list):
        # converts the absolute date time to timestamp
        absolute_timestamp = self.date_time_to_timestamp(absolute_date_time)

        # registers the task
        return self.register_task_absolute_recursive(task, absolute_timestamp, recursion_list)

    def get_task_class(self):
        return SchedulerTask

    def set_startup_items_property(self, startup_items_property):
        # retrieves the startup items
        startup_items = startup_items_property.get_data()

        # cleans the startup items
        colony.libs.map_util.map_clean(self.startup_items)

        # copies the startup items to the startup items
        colony.libs.map_util.map_copy(startup_items, self.startup_items)

    def unset_startup_items_property(self):
        # cleans the startup items
        colony.libs.map_util.map_clean(self.startup_items)

    def create_scheduler_item(self, task_method, task_method_arguments, absolute_time, recursion_list):
        # retrieves the guid plugin
        guid_plugin = self.scheduler_plugin.guid_plugin

        # generates a new item id
        item_id = guid_plugin.generate_guid()

        # creates the new scheduler item instance
        scheduler_item = SchedulerItem(item_id, task_method, task_method_arguments, absolute_time, recursion_list)

        # returns the scheduler item instance
        return scheduler_item

    def add_scheduler_item(self, scheduler_item):
        # in case the scheduler item does not exist in the list of scheduler items
        if not scheduler_item in self.scheduler_items:
            # adds the scheduler item to the list of scheduler items
            self.scheduler_items.append(scheduler_item)

        # creates the new scheduler task
        current_event = self.scheduler.enterabs(scheduler_item.absolute_time, 1, self.task_hander, [scheduler_item])

        # sets the current event for the scheduler item
        scheduler_item.current_event = current_event

        # in case the scheduler lock is locked
        if self.scheduler_lock.locked():
            # releases the lock
            self.scheduler_lock.release()

    def remove_scheduler_item(self, scheduler_item):
        if scheduler_item in self.scheduler_items:
            # removes the scheduler item from the list of scheduler items
            self.scheduler_items.remove(scheduler_item)

    def remove_active_scheduler_item(self, scheduler_item):
        # in case the scheduler item is active
        if scheduler_item.is_active():
            # retrieves the current event
            current_event = scheduler_item.current_event

            print "VAI CANCELAR O ELEMENTO"

            # cancels the current event
            self.scheduler.cancel(current_event)

        # cancels the scheduler item
        scheduler_item.canceled = True

        # removes the scheduler item
        self.remove_scheduler_item(scheduler_item)

    def remove_all_active_scheduler_items(self):
        print "VAI remover OS scheduler items"

        # iterates over all the scheduler items
        for scheduler_item in self.scheduler_items:
            # removes the scheduler item
            self.remove_active_scheduler_item(scheduler_item)

        print "Acabou de remover os scheduler items"

    def get_all_scheduler_items(self):
        return self.scheduler_items

    def task_hander(self, scheduler_item):
        # retrieves the scheduler item attributes
        item_task_method = scheduler_item.task_method
        task_method_arguments = scheduler_item.task_method_arguments

        # calls the task method with the task method arguments
        item_task_method(*task_method_arguments)

        # retrieves the is recursive value
        is_recursive = scheduler_item.is_recursive()

        if is_recursive:
            # retrieves the recursion list
            recursion_list = scheduler_item.recursion_list

            # retrieves the current date time
            current_date_time = datetime.datetime.now()

            # create the delta date time object
            delta_date_time = datetime.timedelta(days = recursion_list[0], hours = recursion_list[1], minutes = recursion_list[2], seconds = recursion_list[3],  microseconds = recursion_list[4])

            # creates the new date time object
            new_date_time = current_date_time +  delta_date_time

            # converts the new date time object to a timestamp
            new_timestamp = self.date_time_to_timestamp(new_date_time)

            # sets the timestamp as the new scheduler item time
            scheduler_item.absolute_time = new_timestamp

            # ads the new scheduler item to the scheduler
            self.add_scheduler_item(scheduler_item)
        else:
            self.remove_scheduler_item(scheduler_item)

    def date_time_to_timestamp(self, date_time):
        # creates the date time time tuple
        date_time_time_tuple = date_time.timetuple()

        # creates the date time timestamp
        date_time_timestamp = time.mktime(date_time_time_tuple)

        # returns the date time timestamp
        return date_time_timestamp

    def timestamp_to_absolute_timestamp(self, timestamp):
        # retrieves the current timestamp
        current_timestamp = time.time()

        # calculates the absolute timestamp
        absolute_timestamp = current_timestamp + timestamp

        # returns the absolute timestamp
        return absolute_timestamp

    def _load_startup_items(self):
        """
        Loads the startup items.
        These items are registered in the plugin's configuration.
        """

        # retrieves the startup tasks from the startup items map
        startup_tasks = self.startup_items.get("tasks", [])

        # retrieves the current time
        current_time = time.time()

        # iterates over all the startup tasks
        # to register them
        for startup_task in startup_tasks:
            # retrieves the plugin manager
            plugin_manager = self.scheduler_plugin.manager

            # retrieves the various startup task attributes
            plugin_id = startup_task["plugin_id"]
            plugin_version = startup_task.get("plugin_version", None)
            method = startup_task["method"]
            arguments = startup_task["arguments"]
            recursion_list = startup_task["recursion_list"]

            # retrieves the plugin
            plugin = plugin_manager.get_plugin_by_id_and_version(plugin_id, plugin_version)

            # retrieves the plugin method
            plugin_method = getattr(plugin, method)

            # creates the scheduler item from the plugin method and the arguments
            scheduler_item = self.create_scheduler_item(plugin_method, arguments, current_time, recursion_list)

            # adds the scheduler item
            self.add_scheduler_item(scheduler_item)

class SchedulerTask:
    """
    The scheduler task class.
    """

    task_type = "none"
    """ The task type """

    task_arguments = {}
    """ The task arguments map """

    def __init__(self, task_type, task_arguments = {}):
        self.task_type = task_type
        self.task_arguments = task_arguments

class SchedulerItem:
    """
    The scheduler item class.
    """

    item_id = "none"
    """ The item id """

    task_method = None
    """ The task method """

    task_method_arguments = None
    """ The task method arguments """

    absolute_time = None
    """ The absolute time """

    recursion_list = None
    """ The recursion list """

    current_event = None
    """ The current event """

    canceled = False
    """ The canceled flag """

    def __init__(self, item_id, task_method, task_method_arguments, absolute_time, recursion_list = None, current_event = None, canceled = False):
        self.item_id = item_id
        self.task_method = task_method
        self.task_method_arguments = task_method_arguments
        self.absolute_time = absolute_time
        self.recursion_list = recursion_list
        self.current_event = current_event
        self.canceled = canceled

    def is_recursive(self):
        if self.recursion_list and not self.canceled:
            return True
        else:
            return False

    def is_active(self):
        if self.current_event and not self.canceled:
            return True
        else:
            return False
