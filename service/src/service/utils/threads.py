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
import heapq
import threading

CONDITION_TIMEOUT = 1.0
""" The timeout value for the condition object,
this value should not be to small otherwise system
resources may be used in excess """

class ServiceAcceptingThread(threading.Thread):
    """
    Class that handles the accepting of the service
    socket.
    """

    abstract_service = None
    """ The abstract service reference """

    stop_flag = False
    """ The flag that controls the execution of the thread """

    service_tuple_queue = []
    """ The service tuple queue """

    service_tuple_queue_condition = None
    """ The condition that controls the service tuple queue """

    def __init__(self, abstract_service):
        """
        Constructor of the class.
        """
        threading.Thread.__init__(self)

        self.abstract_service = abstract_service

        self.service_tuple_queue = []

        self.service_tuple_queue_condition = threading.Condition()

    def run(self):
        # unsets the stop flag
        self.stop_flag = False

        # iterates continuously
        while True:
            # in case the stop flag is set must break
            # the loop immediately
            if self.stop_flag: break;

            # acquires the service tuple queue condition
            self.service_tuple_queue_condition.acquire()

            try:
                # iterates while the service tuple queue is empty
                # and the stop flag is not set, waiting for the
                # callable tuple queue condition
                while not self.service_tuple_queue and not self.stop_flag:
                    self.service_tuple_queue_condition.wait(CONDITION_TIMEOUT)

                # in case the stop flag is set must break
                # the loop immediately
                if self.stop_flag: break;

                # pops the top service tuple to be used in the accepting
                # process inserting it into the connection pool
                service_tuple = self.service_tuple_queue.pop()
            except BaseException, exception:
                # prints an error message about the problem accessing the service tuple queue
                self.abstract_service.service_utils_plugin.error("Error accessing service tuple queue: " + unicode(exception))
            finally:
                # releases the service tuple queue condition
                self.service_tuple_queue_condition.release()

            try:
                # unpacks the service tuple retrieving the service connection,
                # the service address and the port
                service_connection, service_address, port = service_tuple

                # inserts the connection and address into the pool
                self.abstract_service._insert_connection_pool(service_connection, service_address, port)
            except BaseException, exception:
                # prints a warning message about the problem accepting the socket
                self.abstract_service.service_utils_plugin.warning("Error accepting socket: " + unicode(exception))

    def stop(self):
        # acquires the service tuple queue condition
        self.service_tuple_queue_condition.acquire()

        try:
            # sets the stop flag and notifies the callable
            # queue condition so that the event loop is
            # stopped immediately
            self.stop_flag = True
            self.service_tuple_queue_condition.notify()
        finally:
            # releases the service tuple queue condition
            self.service_tuple_queue_condition.release()

    def add_service_tuple(self, service_tuple):
        # acquires the service tuple queue condition
        self.service_tuple_queue_condition.acquire()

        try:
            # adds the service tuple to the service tuple queue and
            # notifies the service tuple queue condition so that
            # the event loop is waked and the service tuple processed
            self.service_tuple_queue.append(service_tuple)
            self.service_tuple_queue_condition.notify()
        finally:
            # releases the service tuple queue condition
            self.service_tuple_queue_condition.release()

class ServiceExecutionThread(threading.Thread):
    """
    Class that handles the execution of background
    callable elements.
    """

    abstract_service = None
    """ The abstract service reference """

    stop_flag = False
    """ The flag that controls the execution of the thread """

    callable_queue = []
    """ The callable queue """

    callable_queue_condition = None
    """ The condition that controls the callable queue """

    def __init__(self, abstract_service):
        """
        Constructor of the class.
        """
        threading.Thread.__init__(self)

        self.abstract_service = abstract_service

        self.callable_queue = []

        self.callable_queue_condition = threading.Condition()

    def run(self):
        # unsets the stop flag
        self.stop_flag = False

        # iterates continuously
        while True:
            # acquires the callable queue condition
            self.callable_queue_condition.acquire()

            try:
                # iterates while the callable queue is empty
                # and the stop flag is not set, waiting for the
                # callable queue condition
                while not self.callable_queue and not self.stop_flag:
                    self.callable_queue_condition.wait(CONDITION_TIMEOUT)

                # in case the stop flag is set must break
                # the loop immediately
                if self.stop_flag: break;

                # retrieves the current timestamp value so that it's
                # possible to compare the target callable timestamp and
                # the current time (for validation)
                _timestamp = time.time()

                # retrieves the current top callable value from the callable
                # queue (peek value)  and checks if the timestamp is valid
                # for execution at the current time
                timestamp, callable, retries, timeout = self.callable_queue[0]
                if timestamp > _timestamp: self.callable_queue_condition.wait(CONDITION_TIMEOUT); continue

                # pops the top callable to be used in the calling process
                # the callable queue should not be empty
                heapq.heappop(self.callable_queue)
            except BaseException, exception:
                # prints an error message about the problem accessing the callable queue
                self.abstract_service.service_utils_plugin.error("Error accessing callable queue: " + unicode(exception))
            finally:
                # releases the callable queue condition
                self.callable_queue_condition.release()

            try:
                # calls the callable object
                callable()
            except BaseException, exception:
                # prints a warning message about the problem executing callable
                self.abstract_service.service_utils_plugin.warning("Error executing callable: " + unicode(exception))

                # in case there are still retries remaining to be used for the
                # callable the callable is inserted back to the list with one
                # less retry and with the timeout value as the delta time
                if retries: self.add_callable(callable, retries - 1, timeout, time.time() + timeout)

    def stop(self):
        # acquires the callable queue condition
        self.callable_queue_condition.acquire()

        try:
            # sets the stop flag and notifies the callable
            # queue condition so that the event loop is
            # stopped immediately
            self.stop_flag = True
            self.callable_queue_condition.notify()
        finally:
            # releases the callable queue condition
            self.callable_queue_condition.release()

    def add_callable(self, callable, retries = 0, timeout = 0.0, timestamp = None):
        # acquires the callable queue condition
        self.callable_queue_condition.acquire()

        try:
            # retrieves the current timestamp value and creates
            # the callable tuple with it and the other values
            timestamp = timestamp or time.time()
            callable_tuple = (timestamp, callable, retries, timeout)

            # adds the callable (tuple) to the callable queue and
            # notifies the callable queue condition so that
            # the event loop is waked and the callable processed
            heapq.heappush(self.callable_queue, callable_tuple)
            self.callable_queue_condition.notify()
        finally:
            # releases the callable queue condition
            self.callable_queue_condition.release()
