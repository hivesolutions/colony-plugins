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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1283 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-02-06 07:09:52 +0000 (sex, 06 Fev 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import threading

DEFAULT_POOL_SIZE = 10
""" The default pool size """

class ElementPoolManager:
    """
    The element pool manager class.
    """

    element_pool_manager_plugin = None
    """ The element pool manager plugin """

    element_pools_list = []
    """ The list of currently enabled element pools """

    def __init__(self, element_pool_manager_plugin):
        """
        Constructor of the class

        @type element_pool_manager_plugin: ElementPoolManagerPlugin
        @param element_pool_manager_plugin: The element pool manager plugin.
        """

        self.element_pool_manager_plugin = element_pool_manager_plugin

        self.element_pools_list = []

    def create_new_element_pool(self, create_method, destroy_method, pool_size = DEFAULT_POOL_SIZE):
        """
        Creates a new element pool with the given create method, destroy method and pool size.

        @type create_method: Method
        @param create_method: The method used to create an element.
        @type destroy_method: Method
        @param destroy_method: The method used to destroy an element.
        @type pool_size: int
        @param pool_size: The element pool size.
        @rtype: ElementPoolImplementation
        @return: The created element pool.
        """

        # creates a new element pool
        element_pool = ElementPoolImplementation(create_method, destroy_method, pool_size)

        # adds the new element pool to the list of element pools
        self.element_pools_list.append(element_pool)

        # returns the new element pool
        return element_pool

class ElementPoolImplementation:
    """
    The element pool implementation class.
    """

    create_method = None
    """ Method used to create an element """

    destroy_method = None
    """ Method used to destroy an element """

    pool_size = None
    """ The size of the pool (number of elements) """

    available_elements = []
    """ The list of available elements """

    element_access_lock = None
    """ The lock that controls the element access """

    element_access_condition = None
    """ The condition that controls the element access """

    def __init__(self, create_method, destroy_method, pool_size = DEFAULT_POOL_SIZE):
        """
        Constructor of the class.

        @type create_method: Method
        @param create_method: The method used to create an element.
        @type destroy_method: Method
        @param destroy_method: The method used to destroy an element.
        @type pool_size: int
        @param pool_size: The size of the pool to be created.
        """

        self.create_method = create_method
        self.destroy_method = destroy_method
        self.pool_size = pool_size

        self.element_access_lock = threading.RLock()
        self.element_access_condition = threading.Condition()

    def start(self, arguments):
        # iterates over the size of the pool
        for _index in range(self.pool_size):
            # creates an element with the given arguments
            element = self.create_method(arguments)

            # adds the element to the list of available
            # elements
            self.available_elements.append(element)

    def stop(self, arguments):
        # iterates over all the available elements
        for element in self.available_elements:
            # destroys an element with the given arguments
            self.destroy_method(element, arguments)

        # empties the available elements
        self.available_elements = []

    def pop(self, immediate = False):
        # acquires the element access lock
        self.element_access_lock.acquire()

        # in case the list of available elements
        # is valid an not empty
        if self.available_elements:
            # pops the element from the list of available elements
            element = self.available_elements.pop()
        else:
            # sets the element as null
            element = None

        # releases the element access lock
        self.element_access_lock.release()

        # in case the retrieval is not valid
        # and the current mode is not immediate
        # the waiting mode is activated
        if element == None and not immediate:
            # acquires the element access condition
            self.element_access_condition.acquire()

            # in case the list of available elements
            # is empty
            while not self.available_elements:
                # waits for the element access condition
                # to be notified
                self.element_access_condition.wait()

            # pops the element from the list of available elements
            element = self.available_elements.pop()

            # releases the element access condition
            self.element_access_condition.release()

        # returns the element
        return element

    def put(self, element):
        # acquires the element access lock
        self.element_access_lock.acquire()

        # acquires the element access condition
        self.element_access_condition.acquire()

        # inserts the element in the list of available elements
        self.available_elements.insert(0, element)

        # notifies the element access condition
        self.element_access_condition.notify()

        # releases the element access condition
        self.element_access_condition.release()

        # releases the element access lock
        self.element_access_lock.release()
