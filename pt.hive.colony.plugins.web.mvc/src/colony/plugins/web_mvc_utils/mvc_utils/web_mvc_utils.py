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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

def transaction_method(entity_manager_reference, raise_exception = True):
    """
    Decorator for the transaction method.

    @type entity_manager: EntityManager
    @param plugin_id: The entity manager to be used for transaction
    management, this entity manager should be started and running.
    @type raise_exception: bool
    @param raise_exception: If an exception should be raised in case it occurs.
    @rtype: Function
    @return: The created decorator.
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
            The interceptor function for the transaction_method decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # retrieves the self reference
            self = args[0]

            # in case the current object contains
            # the entity manager reference
            if hasattr(self, entity_manager_reference):
                # sets the entity manager as the current reference
                entity_manager = getattr(self, entity_manager_reference)
            else:
                # splits the entity manager reference
                entity_manager_reference_splitted = entity_manager_reference.split(".")

                # sets the object reference as the current value
                current = self

                # iterates over all the entity manager reference values
                # splited in parts
                for entity_manager_reference_value in entity_manager_reference_splitted:
                    # retrieves the current value using the entity
                    # manager reference value
                    current = getattr(current, entity_manager_reference_value)

                # sets the entity manager as the current
                # value
                entity_manager = current

                # sets the entity manager in the object reference
                setattr(self, entity_manager_reference, entity_manager)

            # creates a transaction
            entity_manager.create_transaction()

            try:
                # calls the callback function,
                # returning the value
                return function(*args, **kwargs)
            except:
                # rolls back the transaction
                entity_manager.rollback_transaction()

                # in case the raise exception flag is set
                if raise_exception:
                    # re-raises the exception
                    raise
            else:
                # commits the transaction
                entity_manager.commit_transaction()

        # returns the decorator interceptor
        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the load_allowed decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @param: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator
