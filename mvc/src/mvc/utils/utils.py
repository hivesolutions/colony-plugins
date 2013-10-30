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

import inspect

import exceptions

ERROR_STATUS_CODE = 500
""" The error status code """

VALIDATE_VALUE = "validate"
""" The validate value """

VALIDATION_FAILED_VALUE = "validation_failed"
""" The validation failed value """

SERIALIZER_VALUE = "serializer"
""" The serializer value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

EXCEPTION_HANDLER_VALUE = "exception_handler"
""" The exception handler value """

PATTERN_NAMES_VALUE = "pattern_names"
""" The pattern names value """

TO_ONE_RELATION_VALUE = 1
""" The to one relation value """

TO_MANY_RELATION_VALUE = 2
""" The to many relation value """

VALIDATION_METHOD_ENABLED_VALUE = "validation_method_enabled"
""" The validation method enabled value """

PERSIST_UPDATE_TYPE = 0x01
""" The persist only on update (or save) persist type """

PERSIST_SAVE_TYPE = 0x02
""" The persist only on save persist type """

PERSIST_ASSOCIATE_TYPE = 0x04
""" The persist associate persist type """

PERSIST_NONE_TYPE = 0x00
""" The persist none persist type """

PERSIST_ALL_TYPE = PERSIST_UPDATE_TYPE | PERSIST_SAVE_TYPE | PERSIST_ASSOCIATE_TYPE
""" The persist all persist type """

def validated_method(validation_parameters = None, validation_method = None, call_validation_failed = False):
    """
    Decorator for the validated method.

    @type validation_parameters: Object
    @param validation_parameters: The parameters to be used when calling
    the validate method.
    @type validation_method: Method
    @param validation_method: The validation method to be used for extra
    validation (in case it's necessary).
    @type call_validation_failed: bool
    @param call_validation_failed: If the validation failed method should be
    called in case the validation fails.
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

            # retrieves the arguments length
            args_length = len(args)

            # retrieves the self reference
            self = args[0]

            # retrieves the rest request reference
            rest_request = args[1]

            # retrieves the parameters reference
            parameters = args_length > 2 and args[2] or {}

            # in case the controller instance does not have the validate method
            # an exception should be raised indicating the problem
            if not hasattr(self, VALIDATE_VALUE):
                raise exceptions.ControllerValidationError("validation method not found", self)

            # tests if the controller instance contains the validate method and
            # then tries to retrieve the current state of validation for the request
            # workflow, if the current request is already validated or if the current
            # controller does not contain a validate method the validation should
            # not be ran
            contains_validate = hasattr(self, "validate")
            validated = parameters.get("validated", False)
            run_validate = contains_validate and not validated

            # calls the validate method with the rest request
            # the parameters and the validation parameters and retrieves
            # the list with the validation failure reasons, in case no validate
            # method is present ignores the call
            reasons_list = run_validate and\
                self.validate(rest_request, parameters, validation_parameters) or []

            # updates the validated flag for the current request workflow so that
            # no second validation occurs, this is the default (top to down) expected
            # behavior as only the front-end method gets validated
            parameters["validated"] = True

            # tries to retrieves the validation failed method from the current controller
            # instance, this is going to be used in case the validation method is enabled
            validation_failed_method = hasattr(self, VALIDATION_FAILED_VALUE) and\
                self.validation_failed or None

            # retrieves validation method enabled value from the parameters, if this value
            # is set the validation method will be run
            validation_method_enabled = parameters.get(VALIDATION_METHOD_ENABLED_VALUE, True)

            # retrieves the patterns
            patterns = parameters.get(PATTERN_NAMES_VALUE, {})

            # retrieves the session attributes map
            session_attributes = rest_request.get_session_attributes_map()

            # in case the validation method is set and the validation method
            # enabled flag is set in the parameters
            if validation_method and validation_method_enabled:
                try:
                    # calls the validation method with the patterns and the session attributes
                    validation_method_result = validation_method(patterns, session_attributes)

                    # in case the validation method running failed
                    not validation_method_result and reasons_list.append(
                        exceptions.ValidationMethodError("validation method failed in running")
                    )
                except BaseException, exception:
                    # adds the exception to the reasons list
                    reasons_list.append(exception)

            # in case the reasons list is not empty, there was a validation that failed
            # and so either the validation failed method must be called or an exception
            # should be immediately raised indicating the problem
            if reasons_list:

                # in case a validation failed method is defined and
                # the call validation failed flag is set
                if validation_failed_method and call_validation_failed:
                    # calls the validation failed method with the rest request the parameters the
                    # validation parameters and the reasons list and sets the return value
                    return_value = validation_failed_method(
                        rest_request,
                        parameters,
                        validation_parameters,
                        reasons_list
                    )

                # otherwise there is no validation method defined and the exception
                # must be raised (default fallback strategy)
                else:
                    # raises the controller validation failed exception to indicate that
                    # there was a problem validating the controller's action method
                    raise exceptions.ControllerValidationReasonFailed(
                        "validation failed for a series of reasons: " + str(reasons_list),
                        self,
                        reasons_list
                    )

            # otherwise the reason list is empty (no errors have occurred) and so the
            # "normal" function call workflow must be used
            else: return_value = function(*args, **kwargs)

            # returns the return value, retrieved from either the
            # validation method or form the decorated function
            return return_value

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
        @return: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def transaction_method(entity_manager_reference, raise_exception = True):
    """
    Decorator for the "transactional" data logic.
    This decorator should provide the "best" way to create
    a new transaction environment in a target function.

    @type entity_manager: EntityManager
    @param entity_manager: The entity manager to be used for transaction
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

        # retrieves the function specification and uses
        # it to verify if the yield argument is part of
        # it and sets the flag that controls such existence
        # in accordance with the existence of it
        function_spec = inspect.getargspec(function)
        function_args = function_spec.args
        if "_yield" in function_args: is_yield = True
        else: is_yield = False

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

            # in case the yield mode is set tries to retrieve
            # the value of such variable, as it will control
            # the behavior of the function call
            if is_yield: _yield = kwargs.get("_yield", False)
            else: _yield = None

            # in case the current object contains the entity
            # manager reference, no need to try to find it
            # with the entity manager string reference strategy
            if hasattr(self, entity_manager_reference):
                # sets the entity manager as the current reference
                entity_manager = getattr(self, entity_manager_reference)

            # otherwise a new entity manager object must be
            # "retrieved" and set in the environment, this strategy
            # implies the string resolution of the entity manger
            else:
                # splits the entity manager reference
                entity_manager_reference_splitted = entity_manager_reference.split(".")

                # sets the object reference as the current value
                # this is the initial value for the percolation
                # iteration (percolates over the string value)
                current = self

                # iterates over all the entity manager reference values
                # split in parts, this will percolate all the partial
                # values to find the "final" entity manager reference
                for entity_manager_reference_value in entity_manager_reference_splitted:
                    # retrieves the current value using the entity
                    # manager reference value
                    current = getattr(current, entity_manager_reference_value)

                # sets the entity manager as the current value (final
                # iteration) and then sets it in the current entity
                entity_manager = current
                setattr(self, entity_manager_reference, entity_manager)

            # initializes the transaction, calling the begin operation
            # in the entity manager, this should create a new transaction
            # context for the execution of the function code
            entity_manager.begin()

            try:
                # calls the callback function and gets the return value
                # this code should be executed code inside the transaction
                # all the operation will be pending until commit or "rollback"
                # is performed in the current transaction context, note that
                # in case the operation is of type yield and the yield flag
                # is not the complete set of iterations are performed on the
                # function (simulating the normal function behavior)
                return_value = function(*args, **kwargs)
                if is_yield and not _yield: return_value = all(return_value)
            except:
                # "rollsback" the transaction, something wrong
                # has happened and the transaction actions must
                # be correctly reverted
                entity_manager.rollback()

                # in case the raise exception flag is set the
                # exception must be re-raise to the top layers
                if raise_exception:
                    # re-raises the exception to be handled
                    # by the top layers
                    raise
            else:
                # commits the transaction, no problems occurred and
                # so all the pending operations may be persisted
                entity_manager.commit()

            # returns the return value, this is the value returned
            # by the called function (can assume any type)
            return return_value

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
        @return: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

def serialize_exceptions(serialization_parameters = None, default_success = True):
    """
    Decorator for the serialize exceptions.

    @type serialization_parameters: Object
    @param serialization_parameters: The parameters to be used when serializing
    the exception, should condition the serialization process.
    @type default_success: bool
    @param default_success: If an empty success operation should be serialized
    as a simple map containing the result as success (default behavior).
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

            # retrieves the arguments length
            args_length = len(args)

            # retrieves the self reference
            self = args[0]

            # retrieves the rest request reference
            rest_request = args[1]

            # retrieves the parameters reference
            parameters = args_length > 2 and args[2] or {}

            try:
                # calls the callback function,
                # retrieving the return value
                return_value = function(*args, **kwargs)
            except BaseException, exception:
                # logs a warning message because if an exception reached
                # this area it must be considered not handled gracefully
                # and must be considered an anomaly
                self.warning(
                    "There was an exception in controller: " + unicode(exception)
                )

                # retrieves the serializer and the exception
                # values from the parameters
                serializer = parameters.get(SERIALIZER_VALUE, None)
                exception_handler = parameters.get(EXCEPTION_HANDLER_VALUE, None)

                # in case the serializer and the exception
                # handler are not set must raise the exception
                # to the top levels, nothing to be done here
                if not serializer and not exception_handler: raise

                # verifies if the current exception contains a status
                # code attribute and in case it does uses it instead
                # of the default (fallback) error status code
                has_status_code = hasattr(exception, "status_code")
                status_code = exception.status_code if\
                    has_status_code else ERROR_STATUS_CODE

                # sets the error status code in the current request indicating
                # that a problem has occurred (default behavior)
                self.set_status_code(rest_request, status_code)

                # retrieves the exception map for the exception, this map should
                # include extra information on the request together with the "base"
                # information about the exception to be handled
                exception_map = self.get_exception_map(exception, rest_request)

                # in case the serializer is set (uses it as it
                # is has priority)
                if serializer:
                    # dumps the exception map to the serialized form ant then
                    # sets the serialized map as the rest request contents with
                    # the appropriate mime type
                    exception_map_serialized = serializer.dumps(exception_map)
                    mime_type = serializer.get_mime_type()
                    self.set_contents(
                        rest_request,
                        exception_map_serialized,
                        content_type = mime_type
                    )

                    # sets the return value as invalid (error)
                    return_value = False
                # in case the exception handler is set
                elif exception_handler:
                    # handles the exception map with the exception handler
                    return_value = exception_handler.handle_exception(
                        rest_request,
                        exception_map
                    )
            else:
                # checks if the current message is already flushed (data sent to
                # the output) and in case it's not and there should be a default
                # success message sent the default success message is create, then
                # serialized and written to the output stream in the rest request
                is_flushed = rest_request.is_flushed()
                serializer = parameters.get(SERIALIZER_VALUE, None)
                should_default = not is_flushed and default_success and serializer
                if should_default:
                    success_serialized = serializer.dumps(dict(result = "success"))
                    mime_type = serializer.get_mime_type()
                    self.set_contents(
                        rest_request,
                        success_serialized,
                        content_type = mime_type
                    )

            # returns the return value, resulting from the decorated method
            # this should be an already serialized value
            return return_value

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
        @return: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

class Controller(object):
    """
    The base controller class from which all the
    controllers should inherit.

    This controller contains a series of utility
    methods that may be used to complement the
    functionality of the proper implementation.
    """

    plugin = None
    """ The reference to the "owning" plugin, this value
    may be used to retrieve dependencies, allowed plugins
    or the reference to the current context manager """

    system = None
    """ The reference to the "owning" system object, that
    may be used to access inner functionality of the plugin
    use this object carefully because it refers inner
    behavior of the plugin  """

    def __init__(self, plugin, system):
        """
        Constructor of the class.

        @type plugin: Plugin
        @param plugin: The owner plugin of the controller class
        to be used to obtain external references.
        @type system: System
        @param system: The system object used to call inner
        behavior in the current context.
        """

        self.plugin = plugin
        self.system = system
