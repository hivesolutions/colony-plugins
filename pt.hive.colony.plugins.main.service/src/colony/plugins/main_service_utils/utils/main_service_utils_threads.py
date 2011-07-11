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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import threading

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
            # in case the stop flag is set
            if self.stop_flag:
                # breaks the loop
                break;

            # acquires the service tuple queue condition
            self.service_tuple_queue_condition.acquire()

            try:
                # iterates while the service tuple queue is empty
                # and the stop flag is not set
                while not self.service_tuple_queue and not self.stop_flag:
                    # waits for the service tuple queue condition
                    self.service_tuple_queue_condition.wait()

                # in case the stop flag is set
                if self.stop_flag:
                    # breaks the loop
                    break;

                # pops the top service tuple
                service_tuple = self.service_tuple_queue.pop()
            except Exception, exception:
                # prints an error message about the problem accepting the socket
                self.abstract_service.main_service_utils_plugin.error("Error accepting socket: " + unicode(exception))
            finally:
                # releases the service tuple queue condition
                self.service_tuple_queue_condition.release()

            # unpacks the service tuple retrieving the service connection,
            # the service address and the port
            service_connection, service_address, port = service_tuple

            # inserts the connection and address into the pool
            self.abstract_service._insert_connection_pool(service_connection, service_address, port)

    def stop(self):
        # acquires the service tuple queue condition
        self.service_tuple_queue_condition.acquire()

        try:
            # sets the stop flag
            self.stop_flag = True

            # notifies the service tuple queue condition
            self.service_tuple_queue_condition.notify()
        finally:
            # releases the service tuple queue condition
            self.service_tuple_queue_condition.release()

    def add_service_tuple(self, service_tuple):
        # acquires the service tuple queue condition
        self.service_tuple_queue_condition.acquire()

        try:
            # adds the service tuple to the service tuple queue
            self.service_tuple_queue.append(service_tuple)

            # notifies the service tuple queue condition
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
                # iterates while the service socket queue is empty
                # and the stop flag is not set
                while not self.callable_queue and not self.stop_flag:
                    # waits for the callable queue condition
                    self.callable_queue_condition.wait()

                # in case the stop flag is set
                if self.stop_flag:
                    # breaks the loop
                    break;

                # pops the top callable
                callable = self.callable_queue.pop()
            except Exception, exception:
                # prints an error message about the problem executing callable
                self.abstract_service.main_service_utils_plugin.error("Error executing callable: " + unicode(exception))
            finally:
                # releases the callable queue condition
                self.callable_queue_condition.release()

            # calls the callable
            callable()

    def stop(self):
        # acquires the callable queue condition
        self.callable_queue_condition.acquire()

        try:
            # sets the stop flag
            self.stop_flag = True

            # notifies the callable queue condition
            self.callable_queue_condition.notify()
        finally:
            # releases the callable queue condition
            self.callable_queue_condition.release()

    def add_callable(self, callable):
        # acquires the callable queue condition
        self.callable_queue_condition.acquire()

        try:
            # adds the callable to the callable queue
            self.callable_queue.append(callable)

            # notifies the callable queue condition
            self.callable_queue_condition.notify()
        finally:
            # releases the callable queue condition
            self.callable_queue_condition.release()
