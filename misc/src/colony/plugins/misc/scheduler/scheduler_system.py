#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time
import sched
import calendar
import datetime
import threading

import colony.libs.map_util

import scheduler_exceptions

METHOD_CALL_TYPE = "method_call"
""" The method call type """

CONSOLE_COMMAND_TYPE = "console_command"
""" The console command type """

PLUGIN_ID_VALUE = "plugin_id"
""" The plugin id value """

PLUGIN_VERSION_VALUE = "plugin_version"
""" The plugin version value """

METHOD_VALUE = "method"
""" The method value """

METHOD_ARGUMENTS_VALUE = "method_arguments"
""" The method arguments value """

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

RECURSION_LIST_VALUE = "recursion_list"
""" The recursion list value """

CONSOLE_COMMAND_VALUE = "console_command"
""" The console command value """

TASKS_VALUE = "tasks"
""" The tasks value """

SLEEP_STEP_VALUE = "sleep_step"
""" The sleep step value """

DEFAULT_SLEEP_STEP = 1.0
""" The default sleep step value used in sleep function """

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

    sleep_step = DEFAULT_SLEEP_STEP
    """ The sleep step to be used in custom sleep function """

    scheduler = None
    """ The scheduler object """

    scheduler_items = []
    """ The list of scheduler items """

    startup_configuration = {}
    """ The startup configuration """

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
        # the scheduling is creating with the custom sleep function
        # to avoid extra waiting times
        self.scheduler = sched.scheduler(time.time, self._sleep)

        # starts the scheduler items list
        self.scheduler_items = []

        # starts the startup configuration
        self.startup_configuration = {}

    def load_scheduler(self):
        """
        Loads the scheduler, loading the configuration and the
        startup tasks.
        The continuous execution of the scheduler assures the correct
        execution of the tasks.
        """

        # notifies the ready semaphore
        self.scheduler_plugin.release_ready_semaphore()

        # acquires the lock object
        self.scheduler_lock.acquire()

        # loads the (base) configuration
        self._load_configuration()

        # loads the startup tasks
        self._load_startup_tasks()

        # iterates continuously
        while True:
            # acquires the lock object
            self.scheduler_lock.acquire()

            # in case the continue flag is disabled
            # breaks the cycle
            if not self.continue_flag: break

            # runs the scheduler, a cancel operation
            # is triggered in the scheduler the cycle
            # is broken (breaks the loop)
            try: self.scheduler.run()
            except scheduler_exceptions.SchedulerCancel: break

    def unload_scheduler(self):
        """
        Unloads the scheduler, removes all the
        active scheduler items.
        Releases all the active structures.
        """

        # removes all the active scheduler items
        self.remove_all_active_scheduler_items()

        # sets the continue flag to false
        self.continue_flag = False

        # in case the scheduler lock is locked
        # releases the lock (avoids dead lock)
        if self.scheduler_lock.locked(): self.scheduler_lock.release()

    def register_task(self, task, time):
        """
        Registers the given task for the given time.
        The given time is a delta value from the current time.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type time: float
        @param time: The delta time to register the task.
        """

        # calculates the absolute time
        absolute_time = self.timestamp_to_absolute_timestamp(time)

        # registers the task with absolute time
        self.register_task_absolute(task, absolute_time)

    def register_task_absolute(self, task, absolute_time):
        """
        Registers the given task for the given absolute time.
        The given time is an absolute time value.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type absolute_time: float
        @param absolute_time: The absolute time to register the task.
        """

        self.register_task_absolute_recursive(task, absolute_time, None)

    def register_task_date_time(self, task, date_time):
        """
        Registers the given task for the given date time structure.
        The given date time is a delta value from the current time.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type time: datetime
        @param time: The delta date time to register the task.
        """

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # calculates the new date time
        new_date_time = current_date_time + date_time

        # converts the new date time to timestamp
        new_timestamp = self.date_time_to_timestamp(new_date_time)

        # registers the task
        self.register_task_absolute(task, new_timestamp)

    def register_task_date_time_absolute(self, task, absolute_date_time):
        """
        Registers the given task for the given absolute date time.
        The given date time is an absolute time value.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type absolute_date_time: datetime
        @param absolute_date_time: The absolute date time to register the task.
        """

        # converts the absolute date time to timestamp
        absolute_timestamp = self.date_time_to_timestamp(absolute_date_time)

        # registers the task
        self.register_task_absolute(task, absolute_timestamp)

    def register_task_recursive(self, task, time, recursion_list):
        """
        Registers the given task for a recursive usage starting from
        the given time value.
        The given time is a delta value from the current time.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type time: float
        @param time: The delta time to register the task.
        @type recursion_list: List
        @param recursion_list: The recursion list to be used.
        """

        # calculates the absolute time
        absolute_time = self.timestamp_to_absolute_timestamp(time)

        # registers the task
        self.register_task_absolute_recursive(task, absolute_time, recursion_list)

    def register_task_absolute_recursive(self, task, absolute_time, recursion_list):
        """
        Registers the given task for a recursive usage starting from
        the given absolute time value.
        The given time is an absolute time value.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type absolute_time: float
        @param absolute_time: The absolute time to register the task.
        @type recursion_list: List
        @param recursion_list: The recursion list to be used.
        """

        # retrieves the task_type
        task_type = task.task_type

        # retrieves the task arguments
        task_arguments = task.task_arguments

        # in case the task type is of type method_call
        if task_type == METHOD_CALL_TYPE:
            # retrieves the method
            method = task_arguments[METHOD_VALUE]

            # retrieve the method arguments
            method_arguments = task_arguments[METHOD_ARGUMENTS_VALUE]

            # creates a new scheduler item
            scheduler_item = self.create_scheduler_item(method, method_arguments, absolute_time, recursion_list, task)
        # in case the task is of type console_command
        elif task_type == CONSOLE_COMMAND_TYPE:
            # retrieves the console command
            console_command = task_arguments[CONSOLE_COMMAND_VALUE]

            # retrieves the main console plugin
            main_console_plugin = self.scheduler_plugin.main_console_plugin

            # retrieves the default console output method
            default_console_output_method = main_console_plugin.get_default_output_method()

            # creates a new scheduler item
            scheduler_item = self.create_scheduler_item(main_console_plugin.process_command_line, [console_command, default_console_output_method], absolute_time, recursion_list, task)
        # otherwise it's an invalid task type
        else:
            # raises an exception
            raise Exception("Invalid task type: %s" % str(task_type))

        # adds the scheduler item
        self.add_scheduler_item(scheduler_item)

    def register_task_date_time_recursive(self, task, date_time, recursion_list):
        """
        Registers the given task for a recursive usage starting from
        the given date time value.
        The given date time is a delta value from the current date time.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type date_time: float
        @param date_time: The delta date time to register the task.
        @type recursion_list: List
        @param recursion_list: The recursion list to be used.
        """

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # calculates the new date time
        new_date_time = current_date_time + date_time

        # converts the new date time to timestamp
        new_timestamp = self.date_time_to_timestamp(new_date_time)

        # registers the task
        self.register_task_absolute_recursive(task, new_timestamp, recursion_list)

    def register_task_date_time_absolute_recursive(self, task, absolute_date_time, recursion_list):
        """
        Registers the given task for a recursive usage starting from
        the given absolute date time value.
        The given date time is an absolute date time value.

        @type task: SchedulerTask
        @param task: The task to be registered.
        @type absolute_date_time: float
        @param absolute_date_time: The absolute date time to register the task.
        @type recursion_list: List
        @param recursion_list: The recursion list to be used.
        """

        # converts the absolute date time to timestamp
        absolute_timestamp = self.date_time_to_timestamp(absolute_date_time)

        # registers the task
        self.register_task_absolute_recursive(task, absolute_timestamp, recursion_list)

    def unregister_task(self, task):
        """
        Unregisters the given task from the scheduler.
        The task execution is suspended and then canceled.

        @type task: SchedulerTask
        @param task: The task to be unregistered.
        """

        # retrieves the scheduler item from the task
        scheduler_item = task.scheduler_item

        # removes the (active) scheduler item
        self.remove_active_scheduler_item(scheduler_item)

    def get_task_class(self):
        """
        Retrieves the class that represents
        a task in the current scope.

        @rtype: Class
        @return: The task class for the current scope.
        """

        return SchedulerTask

    def set_startup_configuration_property(self, startup_configuration_property):
        # retrieves the startup configuration
        startup_configuration = startup_configuration_property.get_data()

        # cleans the startup configuration
        colony.libs.map_util.map_clean(self.startup_configuration)

        # copies the startup configuration to the startup configuration
        colony.libs.map_util.map_copy(startup_configuration, self.startup_configuration)

    def unset_startup_configuration_property(self):
        # cleans the startup configuration
        colony.libs.map_util.map_clean(self.startup_configuration)

    def create_scheduler_item(self, task_method, task_method_arguments, absolute_time, recursion_list, task):
        # retrieves the guid plugin
        guid_plugin = self.scheduler_plugin.guid_plugin

        # generates a new item id
        item_id = guid_plugin.generate_guid()

        # creates the new scheduler item instance
        scheduler_item = SchedulerItem(item_id, task_method, task_method_arguments, absolute_time, recursion_list, task)

        # sets the scheduler item in the task
        task.scheduler_item = scheduler_item

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
        # must release it (releases the lock)
        if self.scheduler_lock.locked(): self.scheduler_lock.release()

    def remove_scheduler_item(self, scheduler_item):
        # in case the scheduler item is not currently
        # present in the scheduler items, returns immediately
        if not scheduler_item in self.scheduler_items: return

        # removes the scheduler item from the list of scheduler items
        self.scheduler_items.remove(scheduler_item)

    def remove_active_scheduler_item(self, scheduler_item):
        # in case the scheduler item is active
        if scheduler_item.is_active():
            # retrieves the current event
            current_event = scheduler_item.current_event

            # cancels the current event, and in case a value
            # error occurs prints a warning message
            try: self.scheduler.cancel(current_event)
            except ValueError, exception: self.scheduler_plugin.warning("Problem canceling the current event: %s" % unicode(exception))

        # cancels the scheduler item
        scheduler_item.canceled = True

        # removes the scheduler item
        self.remove_scheduler_item(scheduler_item)

    def remove_all_active_scheduler_items(self):
        # iterates over all the scheduler items
        for scheduler_item in self.scheduler_items:
            # removes the scheduler item
            self.remove_active_scheduler_item(scheduler_item)

    def get_all_scheduler_items(self):
        return self.scheduler_items

    def task_hander(self, scheduler_item):
        # retrieves the scheduler item attributes
        item_id = scheduler_item.item_id
        item_task_method = scheduler_item.task_method
        task_method_arguments = scheduler_item.task_method_arguments

        # converts the item id to string
        item_id_string = str(item_id)

        # converts the task method arguments to string
        item_task_method_name = item_task_method.__name__

        # converts the task method arguments to string
        task_method_arguments_string = str(task_method_arguments)

        # print an info message
        self.scheduler_plugin.info("Starting execution of task: " + item_id_string)

        # prints a debug message
        self.scheduler_plugin.debug("Calling task method: " + item_task_method_name + " with arguments: " + task_method_arguments_string)

        try:
            # calls the task method with the task method arguments, this
            # os the execution of the schedule task itself
            item_task_method(*task_method_arguments)
        except BaseException, exception:
            # prints an error message
            self.scheduler_plugin.error("Problem executing scheduler task: " + item_id_string + " (" + item_task_method_name + ") with error: " + unicode(exception))

        # in case the continue flag is not set
        if not self.continue_flag:
            # raises the scheduler cancel exception
            raise scheduler_exceptions.SchedulerCancel("continue flag is not set")

        # retrieves the is recursive value
        is_recursive = scheduler_item.is_recursive()

        # in case it's recursive
        if is_recursive:
            # prints a debug message
            self.scheduler_plugin.debug("Re-scheduling task for recursion: " + item_id_string)

            # retrieves the recursion list
            recursion_list = scheduler_item.recursion_list

            # retrieves the current date time
            current_date_time = datetime.datetime.utcnow()

            # create the delta date time object
            delta_date_time = datetime.timedelta(days = recursion_list[0], hours = recursion_list[1], minutes = recursion_list[2], seconds = recursion_list[3],  microseconds = recursion_list[4])

            # creates the new date time object
            new_date_time = current_date_time + delta_date_time

            # converts the new date time object to a timestamp
            new_timestamp = self.date_time_to_timestamp(new_date_time)

            # sets the timestamp as the new scheduler item time
            scheduler_item.absolute_time = new_timestamp

            # ads the new scheduler item to the scheduler
            self.add_scheduler_item(scheduler_item)

        # otherwise it's not recursive and there is no
        # need to re-schedule the task
        else:
            # removes the scheduler item from the scheduler
            self.remove_scheduler_item(scheduler_item)

        # print an info message
        self.scheduler_plugin.info("Ending execution of task: " + item_id_string)

    def date_time_to_timestamp(self, date_time):
        # creates the date time time tuple
        date_time_time_tuple = date_time.utctimetuple()

        # creates the date time timestamp
        date_time_timestamp = calendar.timegm(date_time_time_tuple)

        # returns the date time timestamp
        return date_time_timestamp

    def timestamp_to_absolute_timestamp(self, timestamp):
        # retrieves the current timestamp
        current_timestamp = time.time()

        # calculates the absolute timestamp
        absolute_timestamp = current_timestamp + timestamp

        # returns the absolute timestamp
        return absolute_timestamp

    def _load_configuration(self):
        """
        Loads the base configuration.
        """

        # retrieves the sleep step from the startup configuration map
        self.sleep_step = self.startup_configuration.get(SLEEP_STEP_VALUE, DEFAULT_SLEEP_STEP)

    def _load_startup_tasks(self):
        """
        Loads the startup tasks.
        These items are registered in the plugin's configuration.
        """

        # retrieves the startup tasks from the startup configuration map
        startup_tasks = self.startup_configuration.get(TASKS_VALUE, [])

        # retrieves the current time
        current_time = time.time()

        # iterates over all the startup tasks
        # to register them
        for startup_task in startup_tasks:
            # retrieves the plugin manager
            plugin_manager = self.scheduler_plugin.manager

            # retrieves the various startup task attributes
            plugin_id = startup_task[PLUGIN_ID_VALUE]
            plugin_version = startup_task.get(PLUGIN_VERSION_VALUE, None)
            method = startup_task[METHOD_VALUE]
            arguments = startup_task[ARGUMENTS_VALUE]
            recursion_list = startup_task[RECURSION_LIST_VALUE]

            # retrieves the plugin
            plugin = plugin_manager.get_plugin_by_id_and_version(plugin_id, plugin_version)

            # retrieves the plugin method
            plugin_method = getattr(plugin, method)

            # creates the "empty" startup task reference
            startup_task_reference = SchedulerTask(METHOD_CALL_TYPE)

            # creates the scheduler item from the plugin method and the arguments
            scheduler_item = self.create_scheduler_item(plugin_method, arguments, current_time, recursion_list, startup_task_reference)

            # adds the scheduler item
            self.add_scheduler_item(scheduler_item)

    def _sleep(self, sleep_time):
        """
        Custom sleep function used to be able to cancel
        the scheduler.

        @type sleep_time: int
        @param sleep_time: The amount of time to sleep.
        """

        # calculates the number of iterations to be used
        # from the sleep step
        iterations = int(sleep_time / self.sleep_step)

        # calculates the extra sleep time from the sleep
        # step modulus
        extra_sleep_time = sleep_time % self.sleep_step

        # iterates over the range of iterations
        for _index in range(iterations):
            # sleep the sleep step
            time.sleep(self.sleep_step)

            # in case the continue flag is not set must
            # return immediately raising a scheduler
            # cancel exception (will stop the scheduler)
            if not self.continue_flag: scheduler_exceptions.SchedulerCancel("continue flag is not set")

        # sleeps the extra sleep time
        time.sleep(extra_sleep_time)

class SchedulerTask:
    """
    The scheduler task class.
    """

    task_type = "none"
    """ The task type """

    task_arguments = {}
    """ The task arguments map """

    scheduler_item = None
    """ The scheduler item """

    def __init__(self, task_type, task_arguments = {}, scheduler_item = None):
        """
        Constructor of the class.

        @type task_type: String
        @param task_type: The task type.
        @type task_arguments: Dictionary
        @param task_arguments: The task arguments map.
        @type scheduler_item: SchedulerItem
        @param scheduler_item: The scheduler item.
        """

        self.task_type = task_type
        self.task_arguments = task_arguments
        self.scheduler_item = scheduler_item

class SchedulerItem:
    """
    The scheduler item class.
    This is the runtime abstraction used to control the
    execution of the tasks.
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

    scheduler_task = None
    """ The task associated with this item """

    current_event = None
    """ The current event """

    canceled = False
    """ The canceled flag """

    def __init__(self, item_id, task_method, task_method_arguments, absolute_time, recursion_list = None, scheduler_task = None, current_event = None, canceled = False):
        """
        Constructor of the class.

        @type item_id: String
        @param item_id: The item id.
        @type task_method: Method
        @param task_method: The task method.
        @type task_method_arguments: List
        @param task_method_arguments: The task method arguments.
        @type absolute_time: float
        @param absolute_time: The absolute time.
        @type recursion_list: List
        @param recursion_list: The recursion list.
        @type scheduler_task: SchedulerTask
        @param scheduler_task: The scheduler task.
        @type current_event: Event
        @param current_event: The current event.
        @type canceled: bool
        @param canceled: The canceled flag.
        """

        self.item_id = item_id
        self.task_method = task_method
        self.task_method_arguments = task_method_arguments
        self.absolute_time = absolute_time
        self.recursion_list = recursion_list
        self.scheduler_task = scheduler_task
        self.current_event = current_event
        self.canceled = canceled

    def is_recursive(self):
        """
        Retrieves if the current scheduler task
        is recursive or not.

        @rtype: bool
        @return: If the current task is recursive
        or not.
        """

        # in case the recursion list is set and the
        # canceled flag is not
        if self.recursion_list and not self.canceled:
            # returns true (valid)
            return True
        # otherwise it's not recursive
        else:
            # returns false (invalid)
            return False

    def is_active(self):
        """
        Retrieves if the current scheduler task
        is active or not.

        @rtype: bool
        @return: If the current task is active
        or not.
        """

        # in case the current event is set and the
        # canceled flag is not
        if self.current_event and not self.canceled:
            # returns true (valid)
            return True
        # otherwise it's not active
        else:
            # returns false (invalid)
            return False
