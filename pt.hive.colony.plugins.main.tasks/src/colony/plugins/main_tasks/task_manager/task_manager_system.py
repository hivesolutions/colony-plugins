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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import threading

DEFAULT_TASK_TYPE = 1
""" The default task type """

SUPER_TASK_TYPE = 2
""" The super task type """

THREAD_PER_TASK_SCHEDULING_ALGORITHM = 1
""" The thread per task scheduling algorithm value """

THREAD_POOL_CONSTANT_SCHEDULING_ALGORITHM = 2
""" The thread pool constant size scheduling algorithm value """

THREAD_POOL_DYNAMIC_SCHEDULING_ALGORITHM = 3
""" The thread pool dynamic size scheduling algorithm value """

DEFAULT_NUMBER_THREADS_THREAD_POOL = 5
""" The default number of threads to be created in the thread pool """

DEFAULT_MAXIMUM_NUMBER_THREADS_THREAD_POOL = 15
""" The default maximum number of threads to be created in the thread pool """

class TaskManager:
    """
    The task manager class
    """

    task_manager_plugin = None
    """ The task manager plugin """

    current_task_id = 0
    """ The current task id """

    task_scheduling_algorithm = THREAD_POOL_CONSTANT_SCHEDULING_ALGORITHM
    """ The task scheduling algorithm """

    task_id_task_map = {}
    """ The map associating the task id's with the tasks """

    thread_pool = None
    """ The thread pool used to manage threads, only used in the thread pool dynamic and constant schedulings """

    task_descriptor_class = None
    """ The task descriptor class for the thread pool """

    def __init__(self, task_manager_plugin, task_scheduling_algorithm = THREAD_POOL_CONSTANT_SCHEDULING_ALGORITHM):
        """
        Constructor of the class

        @type task_manager_plugin: Plugin
        @param task_manager_plugin: The task manager plugin
        @type task_scheduling_algorithm: int
        @param task_scheduling_algorithm: The task scheduling algorithm to be used in the thread processing
        """

        self.task_manager_plugin = task_manager_plugin
        self.task_scheduling_algorithm = task_scheduling_algorithm

        self.task_id_task_map = {}

    def start(self):
        """
        Starts the task manager, creating the necessary resources
        """

        # in case the scheduling algorithm is the thread pool constant one
        if self.task_scheduling_algorithm == THREAD_POOL_CONSTANT_SCHEDULING_ALGORITHM or self.task_scheduling_algorithm == THREAD_POOL_DYNAMIC_SCHEDULING_ALGORITHM:
            if self.task_scheduling_algorithm == THREAD_POOL_CONSTANT_SCHEDULING_ALGORITHM:
                # creates a constant size thread pool
                self.thread_pool = self.task_manager_plugin.thread_pool_manager_plugin.create_new_thread_pool("task_manager", "task manager thread pool", DEFAULT_NUMBER_THREADS_THREAD_POOL, 1, DEFAULT_MAXIMUM_NUMBER_THREADS_THREAD_POOL)
            elif self.task_scheduling_algorithm == THREAD_POOL_DYNAMIC_SCHEDULING_ALGORITHM:
                # creates a dynamic size thread pool
                self.thread_pool = self.task_manager_plugin.thread_pool_manager_plugin.create_new_thread_pool("task_manager", "task manager thread pool", DEFAULT_NUMBER_THREADS_THREAD_POOL, 2, DEFAULT_MAXIMUM_NUMBER_THREADS_THREAD_POOL)

            # starts the thread pool
            self.thread_pool.start_pool()

            # retrieves the task descriptor class for the thread pool
            self.task_descriptor_class = self.task_manager_plugin.thread_pool_manager_plugin.get_thread_task_descriptor_class()

    def create_new_task(self, name, description, task_creation_handler):
        """
        Create a new task with the given name, description and task creation handler

        @type name: String
        @param name: The name for the new task
        @type description: String
        @param description: The description for the new task
        @type task_creation_handler: Method
        @param task_creation_handler: The method to be called upon task creation
        @rtype: Task
        @return: The created task for the give name, description and task creation handler
        """

        task = Task(self, self.current_task_id, name, description, task_creation_handler)
        self.task_id_task_map[task.id] = task
        self.current_task_id += 1

        return task

    def get_task_by_id(self, task_id):
        """
        Retrieves the task with the given task id

        @type task_id: String
        @param task_id: The task id of the task to retrieve
        @rtype: Task
        @return: The task with the given task id
        """

        if task_id in self.task_id_task_map:
            return self.task_id_task_map[task_id]

    def start_task(self, task, args):
        """
        Starts at task according to the current scheduling algorithm

        @type task: Task
        @param task: The task to be started
        @type args: List
        @param args: The arguments to the task creation handler method
        """

        # in case the scheduling algorithm is of type thread per task
        if self.task_scheduling_algorithm == THREAD_PER_TASK_SCHEDULING_ALGORITHM:
            # creates a new thread to run the task plugin
            task.task_thread = TaskThread(task, task.task_creation_handler, args)

            # starts the thread
            task.task_thread.start()
        else:
            # creates a task descriptor to the task
            task_descriptor = self.task_descriptor_class(start_method = task.task_creation_handler)

            # creates the list of arguments to the task creation handler method
            task_creation_handler_arguments_list = [
                task,
                args
            ]

            # insets the task descriptor into the thread pool
            self.thread_pool.insert_task(task_descriptor, task_creation_handler_arguments_list)

class Task:
    """
    The task class, that represents the task unit
    """

    STATUS_TASK_CREATED = 1
    """ The status task created value """

    STATUS_TASK_RUNNING = 2
    """ The status task running value """

    STATUS_TASK_PAUSED = 3
    """ The status task paused value """

    STATUS_TASK_STOPPED = 4
    """ The status task paused value """

    task_manager = None
    """ The task manager """

    id = -1
    """ The task id """

    name = "none"
    """ The task name """

    description = "none"
    """ The task description """

    type = DEFAULT_TASK_TYPE
    """ The task type """

    status = STATUS_TASK_CREATED
    """ The current task status """

    status_confirmed = True
    """ The status confirmed flag """

    percentage_complete = 0
    """ The percentage complete value """

    task_manager_plugin = None
    """ The task manager plugin """

    task_thread = None
    """ The task thread associated """

    task_creation_handler = None
    """ The task creation handler method """

    task_pause_handler = None
    """ The task pause handler method """

    task_resume_handler = None
    """ The task resume handler method """

    task_stop_handler = None
    """ The task stop handler method """

    def __init__(self, task_manager = None, id = -1, name = "none", description = "none", task_creation_handler = None):
        """
        Constructor of the class

        @type task_manager: TaskManager
        @param task_manager: The task manager associated
        @type id: String
        @param id: The task id
        @type name: String
        @param name: The task name
        @type description: String
        @param description: The task description
        @type task_creation_handler: Method
        @param task_creation_handler: The task creation handler method
        """

        self.task_manager = task_manager
        self.id = id
        self.name = name
        self.description = description
        self.task_creation_handler = task_creation_handler

        self.task_manager_plugin = self.task_manager.task_manager_plugin

        # generates the new task created event
        self.task_manager_plugin.generate_event("task_information_changed.new_task", [self])

    def set_task_creation_handler(self, task_creation_handler):
        """
        Sets the task creation handler for the task

        @type task_creation_handler: Method
        @param task_creation_handler: The task creation handler method
        """

        self.task_creation_handler = task_creation_handler

    def set_task_pause_handler(self, task_pause_handler):
        """
        Sets the task pause handler for the task

        @type task_pause_handler: Method
        @param task_pause_handler: The task pause handler method
        """

        self.task_pause_handler = task_pause_handler

    def set_task_resume_handler(self, task_resume_handler):
        """
        Sets the task resume handler for the task

        @type task_resume_handler: Method
        @param task_resume_handler: The task resume handler method
        """

        self.task_resume_handler = task_resume_handler

    def set_task_stop_handler(self, task_stop_handler):
        """
        Sets the task stop handler for the task

        @type task_stop_handler: Method
        @param task_stop_handler: The task stop handler method
        """

        self.task_stop_handler = task_stop_handler

    def set_percentage_complete(self, percentage_complete):
        """
        Sets the percentage complete for the task

        @type percentage_complete: int
        @param percentage_complete: The percentage complete
        """

        self.percentage_complete = percentage_complete

        # defines the event arguments
        event_arguments = [
            self,
            {
                "percentage_complete" : percentage_complete
            }
        ]

        # generates a task updated event
        self.task_manager_plugin.generate_event("task_information_changed.updated_task", event_arguments)

    def start(self, args):
        """
        Starts the task with the given arguments

        @type args: List
        @param args: The arguments to start the task
        """

        if self.status == self.STATUS_TASK_CREATED and self.task_creation_handler:
            # starts the task using the task manager
            self.task_manager.start_task(self, args)

            # sets the new task status (running)
            self.status = self.STATUS_TASK_RUNNING

            # confirms the status
            self.status_confirmed = True

    def pause(self, args):
        """
        Pauses the task with the given arguments

        @type args: List
        @param args: The arguments to pause the task
        """

        if self.status == self.STATUS_TASK_RUNNING and self.task_pause_handler:
            # calls the task pause handler
            self.task_pause_handler(args)

            # sets the new task status (paused)
            self.status = self.STATUS_TASK_PAUSED

            # confirms the status
            self.status_confirmed = False

    def resume(self, args):
        """
        Resumes the task with the given arguments

        @type args: List
        @param args: The arguments to resume the task
        """

        if self.status == self.STATUS_TASK_PAUSED and self.task_resume_handler:
            # calls the task resume handler
            self.task_resume_handler(args)

            # sets the new task status (running)
            self.status = self.STATUS_TASK_RUNNING

            # confirms the status
            self.status_confirmed = False

    def stop(self, args):
        """
        Stops the task with the given arguments

        @type args: List
        @param args: The arguments to stop the task
        """

        if self.status == self.STATUS_TASK_RUNNING or self.status == self.STATUS_TASK_PAUSED and self.task_stop_handler:
            # calls the task stop handler
            self.task_stop_handler(args)

            # sets the new task status (stopped)
            self.status = self.STATUS_TASK_STOPPED

            # confirms the status
            self.status_confirmed = False

    def confirm_pause(self, force = False):
        """
        Confirms the pause, for the current pending pause in the task

        @type force: bool
        @param force: The force value for the confirm (if already confirmed re-confirms)
        """

        if not self.status == self.STATUS_TASK_PAUSED and not force:
            return

        # sets the status of the task as paused
        self.status = self.STATUS_TASK_PAUSED

        # confirms the status
        self.status_confirmed = True

        # defines the event arguments
        event_arguments = [
            self,
            {
                "status" : "paused"
            }
        ]

        # generates a task updated event
        self.task_manager_plugin.generate_event("task_information_changed.updated_task", event_arguments)

    def confirm_resume(self, force = False):
        """
        Confirms the resume, for the current pending resume in the task

        @type force: bool
        @param force: The force value for the confirm (if already confirmed re-confirms)
        """

        if not self.status == self.STATUS_TASK_RUNNING and not force:
            return

        # sets the new task status (running)
        self.status = self.STATUS_TASK_RUNNING

        # confirms the status
        self.status_confirmed = True

        # defines the event arguments
        event_arguments = [
            self,
            {
                "status" : "running"
            }
        ]

        # generates a task updated event
        self.task_manager_plugin.generate_event("task_information_changed.updated_task", event_arguments)

    def confirm_stop(self, force = False):
        """
        Confirms the stop, for the current pending stop in the task

        @type force: bool
        @param force: The force value for the confirm (if already confirmed re-confirms)
        """

        if not self.status == self.STATUS_TASK_STOPPED and not force:
            return

        # sets the new task status (stopped)
        self.status = self.STATUS_TASK_STOPPED

        # confirms the status
        self.status_confirmed = True

        # generates a task updated event for the stop of the task
        self.task_manager_plugin.generate_event("task_information_changed.stopped_task", [self])

class TaskThread(threading.Thread):
    """
    The task thread task
    """

    task = None
    """ The associated task """

    task_creation_handler = None
    """ The task creation handler method """

    args = []
    """ The arguments for the task creation """

    def __init__(self, task, task_creation_handler = None, args = []):
        """
        Constructor of the class

        @type task: Task
        @param task: The associated task
        @type task_creation_handler: Method
        @param task_creation_handler: The task creation handler method
        @type args: List
        @param args: The arguments for the task creation
        """

        threading.Thread.__init__(self)
        self.task = task
        self.task_creation_handler = task_creation_handler
        self.args = args

    def run(self):
        """
        Starts the run of the thread
        """

        if self.task_creation_handler:
            self.task_creation_handler(self.task, self.args)
