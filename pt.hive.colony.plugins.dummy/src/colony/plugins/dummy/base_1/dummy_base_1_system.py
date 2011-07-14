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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

NUMBER_TASKS = 1
""" The number of tasks """

TIMEOUT = 0.5
""" The timeout value to be used """

ITERATIONS_PRINT = 120
""" The number of iterations until printing """

class DummyBase1:
    """
    The dummy base 1.
    """

    dummy_base_1_plugin = None
    """ The dummy base 1 plugin """

    test_pool = None
    """ The test pool """

    def __init__(self, dummy_base_1_plugin):
        """
        Constructor of the class.

        @type dummy_base_1_plugin: DummyBase1Plugin
        @param dummy_base_1_plugin: The dummy base 1 plugin.
        """

        self.dummy_base_1_plugin = dummy_base_1_plugin

    def start_pool(self):
        # retrieves the thread pool manager plugin
        thread_pool_manager_plugin = self.dummy_base_1_plugin.thread_pool_manager_plugin

        # creates the test pool
        self.test_pool = thread_pool_manager_plugin.create_new_thread_pool("test pool", "test pool description", 5, 1, 5)

        # starts the test pool
        self.test_pool.start_pool()

        # the control flags
        self.valid = True
        self.paused = False

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # iterates over the range of task to be created
        for _index in range(NUMBER_TASKS):
            # creates the task descriptor for the task
            self.task_descriptor = task_descriptor_class(start_method = self.start_print_running_thread_pool,
                                                         stop_method = self.stop_print_running_thread_pool,
                                                         pause_method = self.pause_print_running_thread_pool,
                                                         resume_method = self.resume_print_running_thread_pool)

            # insets the task into the test pool
            self.test_pool.insert_task(self.task_descriptor)

    def stop_pool(self):
        # removes the task from the test pool
        self.test_pool.remove_task(self.task_descriptor)

    def start_print_running_thread_pool(self):
        # starts the index value
        index = 0

        # iterates while it's valid
        while self.valid:
            # in case the paused flag is not valid
            if not self.paused:
                # prints a debug message in case the number of iterations
                # required for printing have been reached
                not index % ITERATIONS_PRINT and self.dummy_base_1_plugin.debug("Running in thread pool")

            # sleeps for the given time
            time.sleep(TIMEOUT)

            # increments the index value
            index += 1

    def stop_print_running_thread_pool(self):
        # unsets the valid flag
        self.valid = False

    def pause_print_running_thread_pool(self):
        # sets the paused flag
        self.paused = True

    def resume_print_running_thread_pool(self):
        # unsets the paused flag
        self.paused = False
