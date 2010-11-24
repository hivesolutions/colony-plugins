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

__revision__ = "$LastChangedRevision: 9010 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-06-22 09:28:09 +0100 (ter, 22 Jun 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import thread

class WorkPoolDummy:
    """
    The work pool dummy class.
    """

    work_pool_dummy_plugin = None
    """ The work pool dummy plugin """

    work_pool = None
    """ The dummy pool """

    def __init__(self, work_pool_dummy_plugin):
        """
        Constructor of the class.

        @type work_pool_dummy_plugin: Plugin
        @param work_pool_dummy_plugin: The work pool dummy plugin.
        """

        self.work_pool_dummy_plugin = work_pool_dummy_plugin

    def start_pool(self):
        """
        Starts the dummy pool.
        """

        # retrieves the work pool manager plugin
        work_pool_manager_plugin = self.work_pool_dummy_plugin.work_pool_manager_plugin

        # creates the (dummy) work pool for the given parameters
        self.work_pool = work_pool_manager_plugin.create_new_work_pool("dummy work pool", "dummy work pool", ProcessingClass, [self], 3, 1, 5, 10, 1)

        # start the (dummy) work pool
        self.work_pool.start_pool()

        # iterates over the range of pool
        # tasks to be inserted
        for _index in range(10):
            # inserts the dummy work in the work pool
            self.work_pool.insert_work(_index)

    def stop_pool(self):
        """
        Stops the dummy pool.
        """

        # stops the (dummy) work pool tasks
        self.work_pool.stop_pool_tasks()

        # stops the (dummy) work pool
        self.work_pool.stop_pool()

class ProcessingClass:
    """
    The class for the processing of the work.
    This class is used as dummy processor for
    the dummy work pool.
    """

    work_pool_dummy = None
    """ The work poool dummy """

    work_list = []
    """ The list of work """

    def __init__(self, work_pool_dummy):
        self.work_pool_dummy = work_pool_dummy

        self.work_list = []

    def start(self):
        pass

    def stop(self):
        pass

    def process(self):
        # retrieves the work pool dummy plugin
        work_pool_dummy_plugin = self.work_pool_dummy.work_pool_dummy_plugin

        # iterates over the list of work
        for work in self.work_list:
            # retrieves the current thread id
            thread_id = thread.get_ident()

            # prints the current work string
            work_pool_dummy_plugin.debug(str(work) + " " + str(thread_id))

            # removes the work
            self.remove_work(work)

    def wake(self):
        pass

    def busy(self):
        return False

    def work_added(self, work_reference):
        self.work_list.append(work_reference)

    def work_removed(self, work_reference):
        self.work_list.remove(work_reference)
