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

def transaction(transaction_type = "required"):
    """
    Decorator for the "transactional" data logic.
    This decorator should provide the "best" way to create
    a new transaction environment in a target function.

    The type of transaction to be created may be set with
    the optional parameter, but this is considered to be an
    advanced feature and should be used carefully

    @type transaction_type: String
    @param transaction_type: The type of transaction to be created,
    this option is considered to be an advanced feature (use it
    with extreme care).
    @rtype: Function
    @return: The created decorator, that can be used to decorate
    a function to be executed in a new "transactional" environment.
    """

    def create_decorator_interceptor(function):
        """
        Creates a decorator interceptor, that intercepts
        the normal function call.

        @type function: Function
        @param function: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the transaction decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # retrieves the instance self, to be used to
            # retrieve the associated attributes, (eg: entity
            # manager reference)
            self_value = args[0]

            # initializes the transaction, calling the begin operation
            # in the entity manager, this should create a new transaction
            # context for the execution of the function code
            self_value.entity_manager.begin()

            try:
                # calls the callback function and gets the return value
                # this code should be executed code inside the transaction
                # all the operation will be pending until commit or "rollback"
                # is performed in the current transaction context
                return_value = function(*args, **kwargs)
            except:
                # "rollsback" the transaction, something wrong
                # has happened and the transaction actions must
                # be correctly reverted
                self_value.entity_manager.rollback()

                # re-raises the exception, for top level exception
                # catching, someone else must catch this exception
                raise
            else:
                # commits the transaction, no problems occurred and
                # so all the pending operations may be persisted
                self_value.entity_manager.commit()

            # returns the return value, this is the value returned
            # by the called function (can assume any type)
            return return_value

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the transaction decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @return: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def lock_table(table_name, parameters):
    """
    Decorator for the locking table data logic, the "best" way
    to lock table oriented resources.

    This decorator provides an easy way to ensure table locking
    before executing a given task, the lock is only release on
    exiting the current transaction context.

    This method required that a transaction context exist, can
    only lock inside a transaction-

    @type table_name: String
    @param table_name: The name of the table to be locked,
    the requested table must be present int he data source.
    @type parameters: Dictionary
    @param parameters: The parameters for the lock, these
    should be a map with data source specific options.
    @rtype: Function
    @return: The created decorator.
    """

    def create_decorator_interceptor(function):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type function: Function
        @param function: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the lock_table decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # retrieves the instance self, to be used to
            # retrieve the associated attributes, (eg: entity
            # manager reference)
            self_value = args[0]

            # locks the table with the provided name, any additional
            # operation on this table during the current "transactional"
            # context will result in a block of the operation
            self_value.entity_manager.lock_table(table_name, parameters)

            # calls the callback function and gets the return value
            # the calling will occur only after the locking of the
            # table occurs (ensures lock on table)
            return_value = function(*args, **kwargs)

            # returns the return value, this is the value returned
            # by the called function (can assume any type)
            return return_value

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the transaction decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @return: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator
