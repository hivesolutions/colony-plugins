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

import threading

import colony

from . import algorithms
from . import exceptions

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

RANDOM_WORK_SCHEDULING_ALGORITHM = 1
""" The random work scheduling algorithm value """

ROUND_ROBIN_WORK_SCHEDULING_ALGORITHM = 2
""" The round robin work scheduling algorithm value """

SMART_BUSY_WORK_SCHEDULING_ALGORITHM = 3
""" The smart busy work scheduling algorithm value """

WORK_SCHEDULING_ALGORITHM_NAME_MAP = {
    RANDOM_WORK_SCHEDULING_ALGORITHM: "random",
    ROUND_ROBIN_WORK_SCHEDULING_ALGORITHM: "round_robin",
    SMART_BUSY_WORK_SCHEDULING_ALGORITHM: "smart_busy",
}
""" The work scheduling algorithm name map """

WORK_SCHEDULING_ALGORITHM_CLASS_MAP = {
    RANDOM_WORK_SCHEDULING_ALGORITHM: algorithms.RandomAlgorithm,
    ROUND_ROBIN_WORK_SCHEDULING_ALGORITHM: algorithms.RoundRobinAlgorithm,
    SMART_BUSY_WORK_SCHEDULING_ALGORITHM: algorithms.SmartBusyAlgorithm,
}
""" The work scheduling algorithm class map """


class WorkPool(colony.System):
    """
    The work pool class.
    """

    work_pools_list = []
    """ The list of currently enabled work pools """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.work_pools_list = []

    def unload(self):
        """
        Unloads the work pool, stopping all the available work pools.
        """

        # iterates over all the work pools
        for work_pool in self.work_pools_list:
            # stops the work pool
            work_pool.stop_pool()

    def create_new_work_pool(
        self,
        name,
        description,
        work_processing_task_class=None,
        work_processing_task_arguments=[],
        number_threads=DEFAULT_NUMBER_THREADS,
        scheduling_algorithm=CONSTANT_SCHEDULING_ALGORITHM,
        maximum_number_threads=DEFAULT_MAXIMUM_NUMBER_THREADS,
        maximum_number_works_thread=DEFAULT_MAXIMUM_NUMBER_WORKS_THREAD,
        work_scheduling_algorithm=ROUND_ROBIN_WORK_SCHEDULING_ALGORITHM,
    ):
        """
        Creates a new work pool with the given name, description and number of works.

        :type name: String
        :param name: The work pool name.
        :type description: String
        :param description: The work pool description.
        :type work_processing_task_class: Class
        :param work_processing_task_class: The work pool reference to the class to be used for work processing.
        :type work_processing_task_arguments: List
        :param work_processing_task_arguments: The list of arguments to be used to instantiate the work processing task class.
        :type number_threads: int
        :param number_threads: The thread pool number of threads.
        :type scheduling_algorithm: int
        :param scheduling_algorithm: The thread pool scheduling algorithm.
        :type maximum_number_threads: int
        :param maximum_number_threads: The thread pool maximum number of threads.
        :type maximum_number_works_thread: int
        :param maximum_number_works_thread: The maximum number of works per thread.
        :type work_scheduling_algorithm: int
        :param work_scheduling_algorithm: The work pool scheduling algorithm.
        :rtype: WorkPoolImplementation
        :return: The created thread pool.
        """

        # retrieves the work pool plugin
        thread_pool_plugin = self.plugin.thread_pool_plugin

        # retrieves the logger
        logger = self.plugin.logger

        # retrieves the task descriptor class from the thread pool plugin
        task_descriptor_class = thread_pool_plugin.get_thread_task_descriptor_class()

        # creates a new work pool
        work_pool = WorkPoolImplementation(
            thread_pool_plugin,
            name=name,
            description=description,
            work_processing_task_class=work_processing_task_class,
            work_processing_task_arguments=work_processing_task_arguments,
            task_descriptor_class=task_descriptor_class,
            number_threads=number_threads,
            scheduling_algorithm=scheduling_algorithm,
            maximum_number_threads=maximum_number_threads,
            maximum_number_works_thread=maximum_number_works_thread,
            work_scheduling_algorithm=work_scheduling_algorithm,
            logger=logger,
        )

        # adds the new thread pool to the list of work pools
        self.work_pools_list.append(work_pool)

        # returns the new work pool
        return work_pool

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        :rtype: Dictionary
        :return: The system information map.
        """

        # creates the map to hold the system information (ordered  map)
        work_pool_information = colony.OrderedMap()

        # iterates over all the work pools
        for work_pool in self.work_pools_list:
            # retrieves the work pool values
            work_pool_name = work_pool.name
            work_pool_work_scheduling_algorithm = work_pool.work_scheduling_algorithm
            maximum_number_works_thread = work_pool.maximum_number_works_thread
            work_pool_thread_pool = work_pool.thread_pool
            work_pool_work_tasks_list = work_pool.work_tasks_list

            # starts the work pool work counter
            work_pool_work_counter = 0

            # iterates over all the work pool task in the work pool tasks list
            for work_pool_work_task in work_pool_work_tasks_list:
                # increments the work pool work counter with the
                # work pool work task work counter
                work_pool_work_counter += work_pool_work_task.work_counter

            # retrieves the work pool thread pool name
            work_pool_thread_pool_name = work_pool_thread_pool.name

            # retrieves the work pool scheduling algorithm name
            work_pool_scheduling_algorithm_name = WORK_SCHEDULING_ALGORITHM_NAME_MAP[
                work_pool_work_scheduling_algorithm
            ]

            # retrieves the work pool work tasks list length
            work_pool_work_tasks_list_length = len(work_pool_work_tasks_list)

            # creates the work pool work string
            work_pool_work_string = "%d / %d" % (
                work_pool_work_counter,
                maximum_number_works_thread * work_pool_work_tasks_list_length,
            )

            # sets the instance value for the work pool information
            work_pool_information[work_pool_name] = (
                work_pool_work_string,
                work_pool_scheduling_algorithm_name,
                work_pool_thread_pool_name,
            )

        # defines the work pool item columns
        work_pool_item_columns = [
            {"type": "name", "value": "Pool Name"},
            {"type": "value", "value": "CUR / MAX"},
            {"type": "value", "value": "Algorithm"},
            {"type": "value", "value": "Thread Pool"},
        ]

        # creates the work pool item
        work_pool_item = {}

        # sets the work pool item values
        work_pool_item["type"] = "map"
        work_pool_item["columns"] = work_pool_item_columns
        work_pool_item["values"] = work_pool_information

        # creates the system information (item)
        system_information = {}

        # sets the system information (item) values
        system_information["name"] = "Work Pool"
        system_information["items"] = [work_pool_item]

        # returns the system information
        return system_information


class WorkPoolImplementation(object):
    """
    The work pool implementation class.
    """

    name = "none"
    """ The work pool name """

    description = "none"
    """ The work pool description """

    work_processing_task_class = None
    """ The work pool reference to the class to be used for work processing """

    work_processing_task_arguments = None
    """ The list of arguments to be used to instantiate the work processing task class """

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

    work_scheduling_algorithm = ROUND_ROBIN_WORK_SCHEDULING_ALGORITHM
    """ The work pool work scheduling algorithm """

    logger = None
    """ The logger used """

    thread_pool = None
    """ The thread pool to be used for task execution """

    work_tasks_list = []
    """ The list of active work tasks """

    work_tasks_access_lock = None
    """ The work task access lock """

    algorithm_manager = None
    """ The algorithm manager object reference """

    def __init__(
        self,
        thread_pool,
        name="none",
        description="none",
        work_processing_task_class=None,
        work_processing_task_arguments=[],
        task_descriptor_class=None,
        number_threads=DEFAULT_NUMBER_THREADS,
        scheduling_algorithm=CONSTANT_SCHEDULING_ALGORITHM,
        maximum_number_threads=DEFAULT_MAXIMUM_NUMBER_THREADS,
        maximum_number_works_thread=DEFAULT_MAXIMUM_NUMBER_WORKS_THREAD,
        work_scheduling_algorithm=ROUND_ROBIN_WORK_SCHEDULING_ALGORITHM,
        logger=None,
    ):
        """
        Constructor of the class

        :type thread_pool: Object
        :param thread_pool: The thread pool object to be used to create the thread pool
        :type name: String
        :param name: The work pool name.
        :type description: String
        :param description: The work pool description.
        :type work_processing_task_class: Class
        :param work_processing_task_class: The work pool reference to the class to be used for work processing.
        :type work_processing_task_arguments: List
        :param work_processing_task_arguments: The list of arguments to be used to instantiate the work processing task class.
        :type task_descriptor_class: Class
        :param task_descriptor_class: The work pool task descriptor class.
        :type number_threads: int
        :param number_threads: The work pool number of threads.
        :type scheduling_algorithm: int
        :param scheduling_algorithm: The work pool scheduling algorithm.
        :type maximum_number_threads: int
        :param maximum_number_threads: The work pool maximum number of threads.
        :type maximum_number_works_thread: int
        :param maximum_number_works_thread: The maximum number of works per thread.
        :type work_scheduling_algorithm: int
        :param work_scheduling_algorithm: The work pool work scheduling algorithm.
        :type logger: Log
        :param logger: The logger used.
        """

        self.name = name
        self.description = description
        self.work_processing_task_class = work_processing_task_class
        self.work_processing_task_arguments = work_processing_task_arguments
        self.task_descriptor_class = task_descriptor_class
        self.number_threads = number_threads
        self.scheduling_algorithm = scheduling_algorithm
        self.maximum_number_threads = maximum_number_threads
        self.maximum_number_works_thread = maximum_number_works_thread
        self.work_scheduling_algorithm = work_scheduling_algorithm
        self.logger = logger

        # creates the thread pool to be used for in the work pool
        self.thread_pool = thread_pool.create_new_thread_pool(
            name,
            description,
            number_threads,
            scheduling_algorithm,
            maximum_number_threads,
        )

        self.work_tasks_list = []
        self.work_tasks_access_lock = threading.RLock()

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
        for _index in colony.legacy.xrange(self.number_threads):
            # inserts the task into the thread pool
            self._insert_task()

        # retrieves the work scheduling algorithm class
        work_scheduling_algorithm_class = WORK_SCHEDULING_ALGORITHM_CLASS_MAP[
            self.work_scheduling_algorithm
        ]

        # creates the algorithm manager for the current work pool
        self.algorithm_manager = work_scheduling_algorithm_class(self)

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

        # iterates over all the work tasks
        for work_task in self.work_tasks_list:
            # removes all the current work from
            # the work task
            work_task.remove_all_work()

        # stops the thread pool tasks
        self.thread_pool.stop_pool_tasks()

    def insert_work(self, work_reference):
        """
        Inserts new work into the work pool.
        This method is thread safe and may be called
        from different threads.

        :type work_reference: Object
        :param work_reference: The object used as reference for the work.
        """

        # acquires the work tasks access lock
        self.work_tasks_access_lock.acquire()

        try:
            # retrieves the new work task
            work_task = self.algorithm_manager.get_next()

            # in case there is no space for new work tasks
            if not work_task:
                # raises the work pool operation exception
                raise exceptions.WorkPoolOperationException("no work task available")

            # adds the work to the work task
            work_task.add_work(work_reference)
        finally:
            # releases the work tasks access lock
            self.work_tasks_access_lock.release()

    def get_thread_pool(self):
        """
        Retrieves the thread pool.

        :rtype: ThreadPool
        :return: The thread pool.
        """

        return self.thread_pool

    def _insert_task(self):
        """
        Inserts the currently defined task descriptor
        into  the thread pool.
        """

        # creates an instance of the work processing task class,
        # using the work processing task arguments
        work_processing_task = self.work_processing_task_class(
            *self.work_processing_task_arguments
        )

        # creates a new work task with for work processing task
        work_task = WorkTask(self, work_processing_task)

        # sets the work task in the work processing task
        work_processing_task.work_task = work_task

        # creates a new work task descriptor
        work_task_descriptor = self.task_descriptor_class(
            start_method=work_task.start,
            stop_method=work_task.stop,
            pause_method=work_task.pause,
            resume_method=work_task.resume,
        )

        # inserts the new work task descriptor into the thread pool
        self.thread_pool.insert_task(work_task_descriptor)

        # adds the work task to the work tasks list
        self.work_tasks_list.append(work_task)

    def _check_conditions(self, work_task):
        """
        Verifies that the work conditions are met.

        :type work_task: WorkTask
        :param work_task: The work task to be verified.
        :rtype: bool
        :return: The result of the verification.
        """

        # in case the current number of works is equal or greater
        # than the maximum number of works per thread
        if work_task.work_counter >= self.maximum_number_works_thread:
            # returns false (invalid)
            return False

        # returns true (valid)
        return True

    def _work_added(self, work_task, work_reference):
        self.algorithm_manager.work_added(work_task, work_reference)

    def _work_removed(self, work_task, work_reference):
        self.algorithm_manager.work_removed(work_task, work_reference)


class WorkTask(object):
    """
    The generic task to process the work.
    """

    work_pool = None
    """ The work pool for the work task """

    work_processing_task = None
    """ The work processing task """

    stop_flag = False
    """ Flag to control stop """

    work_list = []
    """ The list that containing the work items """

    work_counter = 0
    """ The number of work items available"""

    work_access_condition = None
    """ The condition to control the access to work """

    def __init__(self, work_pool, work_processing_task):
        """
        Constructor of the class.

        :type work_pool: WorkPool
        :param work_pool: The work pool for the work task.
        :type work_processing_task: Object
        :param work_processing_task: The work processing task object.
        """

        self.work_pool = work_pool
        self.work_processing_task = work_processing_task

        self.work_list = []
        self.work_access_condition = threading.Condition()

    def start(self):
        """
        Starts the current task.
        """

        # calls the start method in the work
        # processing task
        self.work_processing_task.start()

        # iterates while the stop flag is not set
        while not self.stop_flag:
            # acquires the work access condition
            self.work_access_condition.acquire()

            # iterates while there is no work to be done
            while self.work_counter < 1:
                # in case the stop flag is active
                if self.stop_flag:
                    # release the work access condition
                    self.work_access_condition.release()

                    # returns immediately
                    return

                # waits for the work access condition
                self.work_access_condition.wait()

            try:
                # calls the process method in the work
                # processing task
                self.work_processing_task.process()
            finally:
                # release the work access condition
                self.work_access_condition.release()

        # calls the stop method in the work
        # processing task
        self.work_processing_task.stop()

    def stop(self):
        """
        Stops the current task.
        """

        # wakes the work processing task
        self.wake()

        # acquires the work access condition
        self.work_access_condition.acquire()

        try:
            # sets the stop flag
            self.stop_flag = True

            # notifies the work access condition
            self.work_access_condition.notify()
        finally:
            # releases the work access condition
            self.work_access_condition.release()

    def pause(self):
        """
        Pauses the current task.
        """

        pass

    def resume(self):
        """
        Resumes the current task.
        """

        pass

    def wake(self):
        """
        Wakes the current task.
        """

        # in case there is no work to
        # be processed
        if not self.work_counter:
            # returns immediately
            return

        # wakes the work processing task
        self.work_processing_task.wake()

    def busy(self):
        """
        Retrieves the current busy status.

        :rtype: bool
        :return: The current busy status.
        """

        # in case there is no work to
        # be processed
        if not self.work_counter:
            # returns false (not busy)
            return False

        # returns the current busy status
        return self.work_processing_task.busy()

    def get_work_processing_task(self):
        """
        Retrieves the work processing task.

        :rtype: Object
        :return: The work processing task.
        """

        return self.work_processing_task

    def remove_all_work(self):
        # wakes the work processing task
        self.wake()

        # acquires the work access condition
        self.work_access_condition.acquire()

        try:
            # iterates over all the work reference
            # in the work list
            for work_reference in self.work_list:
                # removes the work
                self._remove_work(work_reference)
        finally:
            # releases the work access condition
            self.work_access_condition.release()

    def add_work(self, work_reference):
        # wakes the work processing task
        self.wake()

        # acquires the work access condition
        self.work_access_condition.acquire()

        try:
            # calls the inner add work method
            self._add_work(work_reference)
        finally:
            # releases the work access condition
            self.work_access_condition.release()

    def remove_work(self, work_reference):
        # wakes the work processing task
        self.wake()

        # acquires the work access condition
        self.work_access_condition.acquire()

        try:
            # calls the inner remove work method
            self._remove_work(work_reference)
        finally:
            # releases the work access condition
            self.work_access_condition.release()

    def _add_work(self, work_reference):
        """
        Inner method to add work to the work task.
        This method assumes that the work access condition is locked
        and in possession of the current executing thread.

        :type work_reference: Object
        :param work_reference: The object used as reference for the work.
        """

        # notifies the work processing task about the new work
        self.work_processing_task.work_added(work_reference)

        # adds the work reference to the work list
        self.work_list.append(work_reference)

        # increments the work counter
        self.work_counter += 1

        # notifies the work access condition
        self.work_access_condition.notify()

        # notifies the work pool about work added
        self.work_pool._work_added(self, work_reference)

    def _remove_work(self, work_reference):
        """
        Inner method to remove work from the work task.
        This method assumes that the work access condition is locked
        and in possession of the current executing thread.

        :type work_reference: Object
        :param work_reference: The object used as reference for the work.
        """

        # removes the work reference from the work list
        self.work_list.remove(work_reference)

        # decrements the work counter
        self.work_counter -= 1

        # notifies the work processing task about the removed work
        self.work_processing_task.work_removed(work_reference)

        # notifies the work access condition
        self.work_access_condition.notify()

        # notifies the work pool about work removed
        self.work_pool._work_removed(self, work_reference)


def remove_work(self, work_reference):
    """
    Remove work method to be included
    in the work processing task.

    :type work_reference: Object
    :param work_reference: The object used as reference for the work.
    """

    # calls the remove work in the work task
    self.work_task._remove_work(work_reference)
