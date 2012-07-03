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

import random
import threading

class WorkPoolManagerAlgorithm:
    """
    The generic work pool manager algorithm.
    """

    work_pool = None
    """ The associated work pool """

    def __init__(self, work_pool):
        """
        Constructor of the class.

        @type work_pool: WorkPool
        @param work_pool: The work pool associated with the algorithm.
        """

        self.work_pool = work_pool

    def work_added(self, work_task, work_reference):
        """
        Called upon new work added to a work task.

        @type work_task: WorkTask
        @param work_task: The work task that added a new
        work reference.
        @type work_reference: Object
        @param work_reference: The added work reference.
        """

        pass

    def work_removed(self, work_task, work_reference):
        """
        Called upon new work removed from a work task.

        @type work_task: WorkTask
        @param work_task: The work task that removed a new
        work reference.
        @type work_reference: Object
        @param work_reference: The removed work reference.
        """

        pass

    def get_next(self):
        """
        Retrieves the next element of the work
        pool to be retrieved, according to the algorithm.

        @rtype: Object
        @return: The next element to be retrieved,
        according to the algorithm.
        """

        return None

class RandomAlgorithm(WorkPoolManagerAlgorithm):
    """
    The random algorithm for work
    pool manager.
    """

    work_tasks_list_lock = None
    """ The lock to control the access to the work tasks list """

    def __init__(self, work_pool):
        """
        Constructor of the class.

        @type work_pool: WorkPool
        @param work_pool: The work pool associated with the algorithm.
        """

        WorkPoolManagerAlgorithm.__init__(self, work_pool)

        self.work_tasks_list_lock = threading.Lock()

    def get_next(self):
        """
        Retrieves the next element of the work
        pool to be retrieved, according to the algorithm.

        @rtype: Object
        @return: The next element to be retrieved,
        according to the algorithm.
        """

        # acquires the lock
        self.work_tasks_list_lock.acquire()

        # retrieves the work tasks list
        work_tasks_list = self.work_pool.work_tasks_list

        # retrieves the work tasks list length
        work_tasks_list_length = len(work_tasks_list)

        # iterates continuously
        while True:
            # generates a random index
            random_index = random.randint(0, work_tasks_list_length - 1)

            # retrieves the worker task from the worker threads list
            work_task = self.work_pool.work_tasks_list[random_index]

            # in case the work task conditions are met
            if self.work_pool._check_conditions(work_task):
                # breaks the cycle
                break

        # releases the lock
        self.work_tasks_list_lock.release()

        # returns the work task
        return work_task

class RoundRobinAlgorithm(WorkPoolManagerAlgorithm):
    """
    The round robin algorithm for work
    pool manager.
    """

    current_index = 0
    """ The current index """

    work_tasks_list_lock = None
    """ The lock to control the access to the work tasks list """

    def __init__(self, work_pool):
        """
        Constructor of the class.

        @type work_pool: WorkPool
        @param work_pool: The work pool associated with the algorithm.
        """

        WorkPoolManagerAlgorithm.__init__(self, work_pool)

        self.work_tasks_list_lock = threading.Lock()

    def get_next(self):
        """
        Retrieves the next element of the work
        pool to be retrieved, according to the algorithm.

        @rtype: Object
        @return: The next element to be retrieved,
        according to the algorithm.
        """

        # acquires the lock
        self.work_tasks_list_lock.acquire()

        # retrieves the work tasks list
        work_tasks_list = self.work_pool.work_tasks_list

        # retrieves the work tasks list length
        work_tasks_list_length = len(work_tasks_list)

        # retrieves the initial current index
        initial_current_index = self.current_index

        # iterates continuously
        while True:
            # in case the current index contains the same
            # value as the work tasks list length
            if self.current_index == work_tasks_list_length:
                # resets the value of the current index
                self.current_index = 0

            # retrieves the worker task from the worker threads list
            work_task = self.work_pool.work_tasks_list[self.current_index]

            # increments the current index
            self.current_index += 1

            # in case the work task conditions are met
            if self.work_pool._check_conditions(work_task):
                # breaks the cycle
                break

            # in case all the task have been checked (and invalidated)
            if self.current_index == initial_current_index:
                # invalidates the work task (no work task available)
                work_task = None

                # breaks the cycle
                break

        # releases the lock
        self.work_tasks_list_lock.release()

        # returns the work task
        return work_task

class SmartBusyAlgorithm(WorkPoolManagerAlgorithm):
    """
    The smart busy algorithm for work
    pool manager.
    """

    work_tasks_list = []
    """ The work tasks list """

    work_tasks_map = {}
    """ The work tasks map """

    work_tasks_list_lock = None
    """ The lock to control the access to the work tasks list """

    def __init__(self, work_pool):
        """
        Constructor of the class.

        @type work_pool: WorkPool
        @param work_pool: The work pool associated with the algorithm.
        """

        WorkPoolManagerAlgorithm.__init__(self, work_pool)

        self.work_tasks_list = []
        self.work_tasks_map = {}
        self.work_tasks_list_lock = threading.RLock()

        # starts the data structures
        self._start_structures()

    def work_added(self, work_task, work_reference):
        """
        Called upon new work added to a work task.

        @type work_task: WorkTask
        @param work_task: The work task that added a new
        work reference.
        @type work_reference: Object
        @param work_reference: The added work reference.
        """

        # acquires the lock
        self.work_tasks_list_lock.acquire()

        # retrieves the work task tuple from the work tasks map
        work_task_tuple = self.work_tasks_map[work_task]

        # increments the work task tuple work count value
        work_task_tuple[1] += 1

        # sorts the work tasks list
        self.work_tasks_list.sort(self._sort_work_task_tuple)

        # releases the lock
        self.work_tasks_list_lock.release()

    def work_removed(self, work_task, work_reference):
        """
        Called upon new work removed from a work task.

        @type work_task: WorkTask
        @param work_task: The work task that removed a new
        work reference.
        @type work_reference: Object
        @param work_reference: The removed work reference.
        """

        # acquires the lock
        self.work_tasks_list_lock.acquire()

        # retrieves the work task tuple from the work tasks map
        work_task_tuple = self.work_tasks_map[work_task]

        # decrements the work task tuple work count value
        work_task_tuple[1] -= 1

        # sorts the work tasks list
        self.work_tasks_list.sort(self._sort_work_task_tuple)

        # releases the lock
        self.work_tasks_list_lock.release()

    def get_next(self):
        """
        Retrieves the next element of the work
        pool to be retrieved, according to the algorithm.

        @rtype: Object
        @return: The next element to be retrieved,
        according to the algorithm.
        """

        # acquires the lock
        self.work_tasks_list_lock.acquire()

        # iterates continuously
        while True:
            # retrieves the worker task from the work tasks list (ordered)
            work_task_tuple = self.work_tasks_list[0]

            # unpacks the work task tuple
            work_task, _work_task_work_count = work_task_tuple

            # in case the work task conditions are met
            if self.work_pool._check_conditions(work_task):
                # breaks the cycle
                break
            # otherwise there are no work tasks available
            else:
                # invalidates the work task (no work task available)
                work_task = None

                # breaks the cycle
                break

        # releases the lock
        self.work_tasks_list_lock.release()

        # returns the work task
        return work_task

    def _start_structures(self):
        # iterates over all the work task in the
        # work tasks list
        for work_task in self.work_pool.work_tasks_list:
            # creates the work task tuple
            work_task_tuple = [
                work_task,
                0
            ]

            # adds the work task tuple to the work tasks list
            self.work_tasks_list.append(work_task_tuple)

            # sets the work task tuple in the work tasks map
            self.work_tasks_map[work_task] = work_task_tuple

    def _sort_work_task_tuple(self, first_value, second_value):
        # retrieves the first value work count
        first_value_work_count = first_value[1]

        # retrieves the second value work count
        second_value_work_count = second_value[1]

        # returns the difference between the first value work count
        # and the second value work count
        return first_value_work_count - second_value_work_count
