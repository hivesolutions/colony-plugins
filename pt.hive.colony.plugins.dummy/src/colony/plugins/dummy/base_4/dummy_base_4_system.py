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

STATUS_TASK_CREATED = 1
""" The status task created value """

STATUS_TASK_RUNNING = 2
""" The status task running value """

STATUS_TASK_PAUSED = 3
""" The status task paused value """

STATUS_TASK_STOPPED = 4
""" The status task stopped value """

TIMEOUT = 0.5
""" The timeout for thread pool """

class DummyBase4:
    """
    The dummy base 4.
    """

    dummy_base_4_plugin = None
    """ The dummy base 4 plugin """

    test_task = None
    """ The test task """

    def __init__(self, dummy_base_4_plugin):
        """
        Constructor of the class.

        @type dummy_base_4_plugin: DummyBase4Plugin
        @param dummy_base_4_plugin: The dummy base 4 plugin.
        """

        self.dummy_base_4_plugin = dummy_base_4_plugin

    def create_test_task(self):
        # generates the test task
        self.test_task = self._generate_test_task()

        # starts the test task
        self.test_task.start([])

    def pause_test_task(self):
        # pauses the test task
        self.test_task.pause([])

    def resume_test_task(self):
        # resumes the test task
        self.test_task.resume([])

    def stop_test_task(self):
        # stops the test task
        self.test_task.stop([])

    def generate_test_event(self):
        # creates the test (dummy) task
        test_dummy_task = DummyTask(-1, "test_dummy_task", "test_dummy_task_description")

        # generates the event to start the test task
        self.dummy_base_4_plugin.generate_event("task_information_changed.new_task", [test_dummy_task])

    def task_handler(self, task, args):
        # starts the counter value
        counter = 0

        # iterates while the status is not stopped and the
        # counter limit is not reached
        while not task.status == STATUS_TASK_STOPPED and counter <= 100:
            # prints a debug message
            self.dummy_base_4_plugin.debug("Hello World")

            # in case the current task status is paused
            if task.status == STATUS_TASK_PAUSED:
                # confirms the pause
                task.confirm_pause()

                # while the task is paused
                while task.status == STATUS_TASK_PAUSED:
                    # sleeps for the timeout
                    time.sleep(TIMEOUT)

                # confirms the resume
                task.confirm_resume()

            # sleeps for the given timeout
            time.sleep(TIMEOUT)

            # sets the task percentage complete
            task.set_percentage_complete(counter)

            # increments the counter value
            counter += 1

        # confirms the stop
        task.confirm_stop(True)

    def pause_task_handler(self, args):
        self.dummy_base_4_plugin.debug("Task paused")

    def resume_task_handler(self, args):
        self.dummy_base_4_plugin.debug("Task resumed")

    def stop_task_handler(self, args):
        self.dummy_base_4_plugin.debug("Task stopped")

    def _generate_test_task(self):
        # retrieves the task manager plugin
        task_manager_plugin = self.dummy_base_4_plugin.task_manager_plugin

        # creates the test task
        test_task = task_manager_plugin.create_new_task("test_task", "test_task_description", self.task_handler)

        # sets the task operation handlers
        test_task.set_task_pause_handler(self.pause_task_handler)
        test_task.set_task_resume_handler(self.resume_task_handler)
        test_task.set_task_stop_handler(self.stop_task_handler)

        # returns the test task
        return test_task

class DummyTask:
    """
    The dummy task class.
    """

    id = None
    """ The id of the task """

    name = None
    """ The name of the task """

    description = None
    """ The description of the task """

    def __init__(self, id, name, description):
        """
        Constructor of the class.

        @type id: int
        @param id: The id of the task.
        @type name: String
        @param name: The name of the task.
        @type name: description
        @param name: The description of the task.
        """

        self.id = id
        self.name = name
        self.description = description
