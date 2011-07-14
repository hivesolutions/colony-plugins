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

import simple_pool_manager_exceptions

DEFAULT_POOL_SIZE = 5
""" The default pool size """

DEFAULT_MAXIMUM_POOL_SIZE = 10
""" The default maximum pool size """

CONSTANT_SCHEDULING_ALGORITHM = 1
""" The constant size scheduling algorithm value """

DYNAMIC_SCHEDULING_ALGORITHM = 2
""" The dynamic size scheduling algorithm value """

class SimplePoolManager:
    """
    The simple pool manager class.
    """

    simple_pool_manager_plugin = None
    """ The simple pool manager plugin """

    simple_pools_list = []
    """ The list of currently enabled simple pools """

    def __init__(self, simple_pool_manager_plugin):
        """
        Constructor of the class

        @type simple_pool_manager_plugin: SimplePoolManagerPlugin
        @param simple_pool_manager_plugin: The simple pool manager plugin.
        """

        self.simple_pool_manager_plugin = simple_pool_manager_plugin

        self.simple_pools_list = []

    def create_new_simple_pool(self, name, description, pool_size = DEFAULT_POOL_SIZE, scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM, maximum_pool_size = DEFAULT_MAXIMUM_POOL_SIZE):
        """
        Creates a new simple pool with the given name, description and pool size.

        @type name: String
        @param name: The simple pool name.
        @type description: String
        @param description: The simple pool description.
        @type pool_size: int
        @param pool_size: The simple pool size.
        @type scheduling_algorithm: int
        @param scheduling_algorithm: The simple pool scheduling algorithm.
        @type maximum_pool_size: int
        @param maximum_pool_size: The maximum pool size.
        @rtype: SimplePoolImplementation
        @return: The created simple pool.
        """

        # retrieves the logger
        logger = self.simple_pool_manager_plugin.logger

        # creates a new simple pool
        simple_pool = SimplePoolImplementation(name, description, pool_size, scheduling_algorithm, maximum_pool_size, logger)

        # adds the new simple pool to the list of simple pools
        self.simple_pools_list.append(simple_pool)

        # returns the new simple pool
        return simple_pool

class SimplePoolImplementation:
    """
    The simple pool implementation class.
    """

    name = "none"
    """ The simple pool name """

    description = "none"
    """ The simple pool description """

    pool_size = DEFAULT_POOL_SIZE
    """ The simple pool size """

    scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM
    """ The simple pool scheduling algorithm """

    maximum_pool_size = DEFAULT_MAXIMUM_POOL_SIZE
    """ The simple pool maximum pool size """

    logger = None
    """ The logger used """

    pool_items_list = []
    """ The list of all the items in the pool """

    free_pool_items_list = []
    """ The list of all the free items in the pool """

    busy_pool_items_list = []
    """ The list of all the busy items in the pool """

    item_constructor_method = None
    """ The item constructor method """

    item_destructor_method = None
    """ The item destructor method """

    def __init__(self, name = "none", description = "none", pool_size = DEFAULT_POOL_SIZE, scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM, maximum_pool_size = DEFAULT_MAXIMUM_POOL_SIZE, logger = None):
        """
        Constructor of the class

        @type name: String
        @param name: The simple pool name
        @type description: String
        @param description: The simple pool description
        @type pool_size: int
        @param pool_size: The simple pool size.
        @type scheduling_algorithm: int
        @param scheduling_algorithm: The simple pool scheduling algorithm.
        @type maximum_pool_size: int
        @param maximum_pool_size: The maximum pool size.
        @type logger: Log
        @param logger: The logger used.
        """

        self.name = name
        self.description = description
        self.pool_size = pool_size
        self.scheduling_algorithm = scheduling_algorithm
        self.maximum_pool_size = maximum_pool_size
        self.logger = logger

        self.pool_items_list = []
        self.free_pool_items_list = []
        self.busy_pool_items_list = []

    def construct_pool(self):
        """
        Constructs the pool.
        """

        # iterates over the pool size range
        for _index in range(self.pool_size):
            # creates and adds a pool item
            self._create_add_pool_item()

    def add_pool_item(self, pool_item):
        """
        Adds a pool item to the pool.

        @type pool_item: Object
        @param pool_item: The pool item to be added to the pool.
        """

        # in case the pool is "growable"
        if self._pool_growable():
            # adds the pool item to the pool items list
            self.pool_items_list.append(pool_item)
        else:
            # raises an exception
            raise simple_pool_manager_exceptions.SimplePoolManagerPoolFull("can't grow the pool")

    def get_pool_item(self):
        """
        Retrieves a pool item.
        """

        # in case there are no items
        # in the pool items list
        if not len(self.pool_items_list):
            # grows the pool
            self.grow_pool()

        # retrieves the pool item
        pool_item = self.pool_items_list.pop()

        # returns the pool item
        return pool_item

    def release_pool_item(self, pool_item):
        """
        Releases the pool item, returning it to the pool.

        @type pool_item: Object
        @param pool_item: The pool item to be returned to the pool.
        """

        # adds the pool item to the pool items list
        self.pool_items_list.append(pool_item)

    def set_auto_release(self, pool_item, timeout):
        pass

    def grow_pool(self, size = 1):
        """
        Grows the pool by the given size.

        @type size: int
        @param size: The size to be used in the pool growth.
        """

        # iterates in the size range
        for _index in range(size):
            # creates the pool item and adds
            # it to the pool
            self._create_add_pool_item()

    def get_item_contructor_method(self):
        """
        Retrieves the item constructor method.

        @rtype: Method
        @return: The item constructor method.
        """

        return self.item_constructor_method

    def set_item_constructor_method(self, item_constructor_method):
        """
        Sets the item constructor method.

        @type item_constructor_method: Method
        @param item_constructor_method: The item constructor method.
        """

        self.item_constructor_method = item_constructor_method

    def get_item_destructor_method(self):
        """
        Retrieves the item destructor method.

        @rtype: Method
        @return: The item destructor method.
        """

        return self.item_destructor_method

    def set_item_destructor_method(self, item_destructor_method):
        """
        Sets the item destructor method.

        @type item_destructor_method: Method
        @param item_destructor_method: The item destructor method.
        """

        self.item_destructor_method = item_destructor_method

    def _pool_growable(self):
        """
        Returns if the simple pool can grow or not.

        @rtype: bool
        @return: The result of the is growable test.
        """

        # retrieves the current pool size
        current_pool_size = len(self.pool_items_list)

        if self.scheduling_algorithm == CONSTANT_SCHEDULING_ALGORITHM:
            if current_pool_size < self.pool_size:
                return True
            else:
                return False
        elif self.scheduling_algorithm == DYNAMIC_SCHEDULING_ALGORITHM:
            if current_pool_size < self.maximum_pool_size:
                return True
            else:
                return False

    def _create_add_pool_item(self):
        """
        Creates a pool item and adds it to the pool.
        """

        # in case there is no item constructor method defined
        if not self.item_constructor_method:
            # raises an exception
            raise simple_pool_manager_exceptions.SimplePoolManagerInvalidItemConstructor("no item constructor defined")

        # creates the pool item
        pool_item = self.item_constructor_method()

        # adds the pool item
        self.add_pool_item(pool_item)
