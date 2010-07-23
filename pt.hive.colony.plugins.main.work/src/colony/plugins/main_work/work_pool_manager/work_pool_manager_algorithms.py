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

    def get_next(self):
        """
        Retrieves the next element of the work
        pool to be retrieved, according to the algorithm.

        @rtype: Object
        @return: The next element to be retrieved,
        according to the algorithm.
        """

        return None

class RoundRobinAlgorithm(WorkPoolManagerAlgorithm):
    """
    The round robin algorithm for work
    pool manager.
    """

    current_index = 0
    """ The current index """

    work_tasks_list_lock = None
    """ The lock to control the acces to the work tasks list """

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
