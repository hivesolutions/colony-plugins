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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 9010 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-06-22 09:28:09 +0100 (ter, 22 Jun 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import threading

import work_pool_manager_algorithms

DEFAULT_NUMBER_THREADS = 5
""" The default number of threads to be created """

DEFAULT_MAXIMUM_NUMBER_THREADS = 15
""" The default maximum number of threads to be created """

DEFAULT_MAXIMUM_NUMBER_WORKS_THREAD = 3
""" The default maximum number of works per thread """

CONSTANT_SCHEDULING_ALGORITHM = 1
""" The constant size scheduling algorithm value """

DYNAMIC_SCHEDULING_ALGORITHM = 2
""" The dynamic size scheduling algorithm value """

class WorkPoolManager:
    """
    The work pool manager class.
    """

    work_pool_manager_plugin = None
    """ The work pool manager plugin """

    work_pools_list = []
    """ The list of currently enabled work pools """

    def __init__(self, work_pool_manager_plugin):
        """
        Constructor of the class.

        @type work_pool_manager_plugin: Plugin
        @param work_pool_manager_plugin: The work pool manager plugin.
        """

        self.work_pool_manager_plugin = work_pool_manager_plugin

        self.work_pools_list = []

    def unload(self):
        """
        Unloads the work pool manager, stopping all the available work pools.
        """

        # iterates over all the work pools
        for work_pool in self.work_pools_list:
            # stops the work pool
            work_pool.stop_pool()

    def create_new_work_pool(self, name, description, work_processing_task_class = None, number_threads = DEFAULT_NUMBER_THREADS, scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM, maximum_number_threads = DEFAULT_MAXIMUM_NUMBER_THREADS, maximum_number_works_thread = DEFAULT_MAXIMUM_NUMBER_WORKS_THREAD):
        """
        Creates a new work pool with the given name, description and number of works.

        @type name: String
        @param name: The work pool name.
        @type description: String
        @param description: The work pool description.
        @type work_processing_task_class: Class
        @param work_processing_task_class: The work pool reference to the class to be used for work processing.
        @type number_threads: int
        @param number_threads: The thread pool number of threads.
        @type scheduling_algorithm: int
        @param scheduling_algorithm: The thread pool scheduling algorithm.
        @type maximum_number_threads: int
        @param maximum_number_threads: The thread pool maximum number of threads.
        @type maximum_number_works_thread: int
        @param maximum_number_works_thread: The maximum number of works per thread.
        @rtype: WorkPoolImplementation
        @return: The created thread pool.
        """

        # retrieves the work pool manager plugin
        thread_pool_manager_plugin = self.work_pool_manager_plugin.thread_pool_manager_plugin

        # retrieves the logger
        logger = self.work_pool_manager_plugin.logger

        # retrieves the task descriptor class from the thread pool manager plugin
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates a new work pool
        work_pool = WorkPoolImplementation(thread_pool_manager_plugin, name, description, work_processing_task_class, task_descriptor_class, number_threads, scheduling_algorithm, maximum_number_threads, maximum_number_works_thread, logger)

        # adds the new thread pool to the list of work pools
        self.work_pools_list.append(work_pool)

        # returns the new work pool
        return work_pool

class WorkPoolImplementation:
    """
    The work pool implementation class.
    """

    name = "none"
    """ The work pool name """

    description = "none"
    """ The work pool description """

    work_processing_task_class = None
    """ The work pool reference to the class to be used for work processing """

    task_descriptor_class = None
    """ The work pool task descriptor class """

    number_threads = DEFAULT_NUMBER_THREADS
    """ The work pool number of threads """

    scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM
    """ The work pool scheduling algorithm """

    maximum_number_threads = DEFAULT_MAXIMUM_NUMBER_THREADS
    """ The work pool maximum number of threads """

    maximum_number_works_thread = DEFAULT_MAXIMUM_NUMBER_WORKS_THREAD
    """ The work pool maximum number works thread """

    logger = None
    """ The logger used """

    thread_pool = None
    """ The thread pool to be used for task execution """

    work_tasks_list = []
    """ The list of active wprk tasks """

    algorithm_manager = None
    """ The algorithm manager object reference """

    def __init__(self, thread_pool_manager, name = "none", description = "none", work_processing_task_class = None, task_descriptor_class = None, number_threads = DEFAULT_NUMBER_THREADS, scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM, maximum_number_threads = DEFAULT_MAXIMUM_NUMBER_THREADS, maximum_number_works_thread = DEFAULT_MAXIMUM_NUMBER_WORKS_THREAD, logger = None):
        """
        Constructor of the class

        @type thread_pool_manager: Object
        @param thread_pool_manager: The thread pool manager object to be used to create the thread pool
        @type name: String
        @param name: The work pool name.
        @type description: String
        @param description: The work pool description.
        @type work_processing_task_class: Class
        @param work_processing_task_class: The work pool reference to the class to be used for work processing.
        @type task_descriptor_class: Class
        @param task_descriptor_class: The work pool task descriptor class.
        @type number_threads: int
        @param number_threads: The work pool number of threads.
        @type scheduling_algorithm: int
        @param scheduling_algorithm: The work pool scheduling algorithm.
        @type maximum_number_threads: int
        @param maximum_number_threads: The work pool maximum number of threads.
        @type maximum_number_works_thread: int
        @param maximum_number_works_thread: The maximum number of works per thread.
        @type logger: Log
        @param logger: The logger used.
        """

        self.name = name
        self.description = description
        self.work_processing_task_class = work_processing_task_class
        self.task_descriptor_class = task_descriptor_class
        self.number_threads = number_threads
        self.scheduling_algorithm = scheduling_algorithm
        self.maximum_number_threads = maximum_number_threads
        self.maximum_number_works_thread = maximum_number_works_thread
        self.logger = logger

        # creates the thread pool to be used for in the work pool
        self.thread_pool = thread_pool_manager.create_new_thread_pool(name, description, number_threads, scheduling_algorithm, maximum_number_threads)

        self.work_tasks_list = []

        # sets the remove work method in the work processing task class
        self.work_processing_task_class.remove_work = remove_work

    def start_pool(self):
        """
        Starts the work pool launching and starting all the works.
        """

        # starts the thread pool
        self.thread_pool.start_pool()

        # inserts the same amount of tasks
        # as the number of base threads to be used
        # in order to fulfill the work pool demands
        for _index in range(self.number_threads):
            # inserts the task into the thread pool
            self._insert_task()

        # creates the algorithm manager for the current work pool
        self.algorithm_manager = work_pool_manager_algorithms.RoundRobinAlgorithm(self)

    def stop_pool(self):
        """
        Stops the work pool exiting all the works.
        """

        # stops the thread pool
        self.thread_pool.stop_pool()

    def stop_pool_tasks(self):
        """
        Stops the work tasks pool removing all the tasks.
        """

        # stops the thread pool tasks
        self.thread_pool.stop_pool_tasks()

    def insert_work(self, work_reference):
        """
        Inserts new work into the work pool.

        @type work_reference: Object
        @param work_reference: The object used as reference for the work.
        """

        # retrieves the new work task
        work_task = self.algorithm_manager.get_next()

        # in case there is no space for new work tasks
        if not work_task:
            pass

        # adds the work to the work task
        work_task._add_work(work_reference)

    def get_thread_pool(self):
        """
        Retrieves the thread pool.

        @rtype: ThreadPool
        @return: The thread pool.
        """

        return self.thread_pool

    def _insert_task(self):
        """
        Inserts the currently defined task descriptor
        into  the thread pool.
        """

        # creates an instance of the work processing task class
        work_processing_task = self.work_processing_task_class()

        # creates a new work task with for work processing task
        work_task = WorkTask(work_processing_task)

        # sets the work task in the work processing task
        work_processing_task.work_task = work_task

        # creates a new work task descriptor
        work_task_descriptor = self.task_descriptor_class(start_method = work_task.start,
                                                          stop_method = work_task.stop,
                                                          pause_method = work_task.pause,
                                                          resume_method = work_task.resume)

        # inserts the new work task descriptor into the thread pool
        self.thread_pool.insert_task(work_task_descriptor)

        # adds the work task to the work tasks list
        self.work_tasks_list.append(work_task)

class WorkTask:
    """
    The generic task to process the work.
    """

    work_processing_task = None
    """ The work processing task """

    stop_flag = False
    """ Flag to control stop """

    work_counter = 0
    """ The number of work items available"""

    work_access_condition = None
    """ The condition to control the access to work """

    def __init__(self, work_processing_task):
        """
        Constructor of the class.

        @type work_processing_task: Object
        @param work_processing_task: The work processing task object.
        """

        self.work_processing_task = work_processing_task

        self.work_access_condition = threading.Condition()

    def start(self):
        while not self.stop_flag:
            # acquires the work access condition
            self.work_access_condition.acquire()

            # iterates while there is no work to be done
            while self.work_counter < 1:
                # in case the stop flag is active
                if self.stop_flag:
                    # release the work access condition
                    self.work_access_condition.release()

                    return

                # waits for the work access condition
                self.work_access_condition.wait()

            # calls the process method in the work
            # processing task
            self.work_processing_task.process()

            # release the work access condition
            self.work_access_condition.release()

    def stop(self):
        # acquires the work access condition
        self.work_access_condition.acquire()

        # sets the stop flag
        self.stop_flag = True

        # notifies the work access condition
        self.work_access_condition.notify()

        # releases the work access condition
        self.work_access_condition.release()

    def pause(self):
        pass

    def resume(self):
        pass

    def get_work_processing_task(self):
        """
        Retrieves the work processing task.

        @rtype: Object
        @return: The work processing task.
        """

        return self.work_processing_task

    def _add_work(self, work_reference):
        # acquires the work access condition
        self.work_access_condition.acquire()

        # notifies the work processing task about the new work
        self.work_processing_task.work_added(work_reference)

        # increments the work counter
        self.work_counter += 1

        # notifies the work access condition
        self.work_access_condition.notify()

        # releases the work access condition
        self.work_access_condition.release()

    def _remove_work(self, work_reference):
        # acquires the work access condition
        self.work_access_condition.acquire()

        # decrements the work counter
        self.work_counter -= 1

        # notifies the work processing task about the removed work
        self.work_processing_task.work_removed(work_reference)

        # notifies the work access condition
        self.work_access_condition.notify()

        # releases the work access condition
        self.work_access_condition.release()

def remove_work(self, work_reference):
    """
    Remove work method to be included
    in the work processing task.

    @type work_reference: Object
    @param work_reference: The object used as reference for the work.
    """

    # calls the remove work in the work task
    self.work_task._remove_work(work_reference)
