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

__revision__ = "$LastChangedRevision: 6466 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-11-23 11:20:49 +0000 (seg, 23 Nov 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import exceptions

import main_mock_exceptions

class MainMock:
    """
    The main mock class.
    """

    main_mock_plugin = None
    """ The main mock plugin """

    def __init__(self, main_mock_plugin):
        """
        Constructor of the class

        @type main_mock_plugin: MainMockPlugin
        @param main_mock_plugin: The main mock plugin.
        """

        self.main_mock_plugin = main_mock_plugin

    def generate_mockery(self, mockery_name):
        """
        Generates a new mockery with the given name.

        @type mockery_name: MainMockPlugin
        @param mockery_name: The name to be used in the mockery.
        @rtype: Mockery
        @return: The generated mockery.
        """

        # creates a new mock object for the given
        # mockery name
        mockery = Mockery(mockery_name)

        # returns the mockery
        return mockery

class Mockery:
    """
    The mockery class used to manage mocks.
    """

    mockery_name = "none"
    """ The mockery name """

    def __init__(self, mockery_name):
        """
        Constructor of the class

        @type mockery_name: MainMockPlugin
        @param mockery_name: The name to be used in the mockery.
        """

        self.mockery_name = mockery_name

    def checking(self):
        pass

    def generate_mock(self, mock_name = "anonymous", mock_return = None, mock_returns_iterator = None, mock_returns_method = None, mock_raises = None):
        """
        Generates a new mock object with the given
        mock name.

        @type mock_name: String
        @param mock_name: The name to be used in the mock.
        @type mock_return: Object
        @param mock_return: The return to be used in the mock.
        @type mock_returns_iterator: Iterator
        @param mock_returns_iterator: The returns iterator to be used in the mock.
        @type mock_returns_method: Method
        @param mock_returns_method: The returns method to be used in the mock.
        @type mock_raises: Exception
        @param mock_raises: The exception to be used in the mock.
        @rtype: Mock
        @return: The generated mock.
        """

        # creates a new mock object for the given
        # mock name
        mock = Mock(mock_name, mock_return, mock_returns_iterator, mock_returns_method, mock_raises)

        # returns the mock
        return mock

    def generate_expectation(self, expectation_type, expectation_key_arguments):
        """
        Generates a new expectation to be used.

        @type expectation_type: String
        @param expectation_type: The type of the expectation to be generated.
        @type expectation_key_arguments: Dictionary
        @param expectation_key_arguments: The expectation key aguments to be used.
        @rtype: Expectation
        @return: The generated expectation.
        """

        # retrieves the global variables
        global_variables = globals()

        # retrieves the expectation class from the global variables
        expectation_class = global_variables[expectation_type]

        # creates the expectation using the expectation key arguments
        expectation = expectation_class(**expectation_key_arguments)

        # returns the expectation
        return expectation

class Mock:
    """
    The mock class used to encapsulate mock objects.
    """

    mock_name = "anonymous"
    """ The mock name """

    mock_return = None
    """ The mock return """

    mock_returns_iterator = None
    """ The mock returns iterator """

    mock_returns_method = None
    """ The mock returns method """

    mock_raises = None
    """ The mock raises """

    mock_attrs = {}
    """ The mock attrs """

    mock_calls_list = []
    """ The mock calls list """

    expectations_list = []
    """ The expectations list """

    verification_state_map = {}
    """ The verification state map """

    def __init__(self, mock_name = "anonymous", mock_return = None, mock_returns_iterator = None, mock_returns_method = None, mock_raises = None):
        self.mock_name = mock_name
        self.mock_return = mock_return
        self.mock_returns_iterator = mock_returns_iterator
        self.mock_returns_method = mock_returns_method
        self.mock_raises = mock_raises
        self.mock_attrs = {}
        self.mock_calls_list = []
        self.expectations_list = []
        self.verification_state_map = {}

    def __repr__(self):
        return "<Mock '%s' '%s'>" % (hex(id(self)), self.mock_name)

    def __call__(self, *args, **kwargs):
        # start the mock exception
        mock_exception = None

        try:
            # retrieves the mock return
            mock_return = self._mock_return(*args, **kwargs)
        except Exception, exception:
            # sets the mock exception
            mock_exception = exception

            # sets the return value
            mock_return = None

        # creates a new mock call
        mock_call = MockCall(self.mock_name, args, kwargs, mock_return, mock_exception)

        # adds the mock call to the mock calls list
        self.mock_calls_list.append(mock_call)

        # verifies the expectation for the current mock call
        self._verify_expectations(mock_call)

        # returns the mock return
        return mock_return

    def __getattr__(self, attr):
        # in case the attr in no defined in the mock
        # attrs map
        if attr not in self.mock_attrs:
            # in case there is a mock name defined
            if self.mock_name:
                # sets the new name as the mock name appended
                # with the attr
                new_name = self.mock_name + "." + attr
            # otherwise
            else:
                # sets the new name as the attr
                new_name = attr

            # creates a new mock with the new name
            self.mock_attrs[attr] = Mock(new_name)

        # retrieves the mock attr from the mock attrs map
        mock_attr = self.mock_attrs[attr]

        # returns the mock attr
        return mock_attr

    def add_expectation(self, expectation):
        """
        Adds an expectation to the expectations list.

        @type expectation: Expectatation
        @param expectation: The expectation to be added.
        """

        # adds the expectation to the expectations list
        self.expectations_list.append(expectation)

    def remove_expectation(self, expectation):
        """
        Adds an expectation from the expectations list.

        @type expectation: Expectatation
        @param expectation: The expectation to be removed.
        """

        # removes the expectation from the expectations list
        self.expectations_list.remove(expectation)

    def _reset_verification_state(self):
        """
        Resets the current verification state.
        """

        # clears the verification state map
        self.verification_state_map.clear()

    def _verify_expectations(self, mock_call):
        """
        Verifies expectations for the given mock call.

        @type mock_call: MockCall
        @param mock_call: The mock call to be used in verification.
        """

        # iterates over all the expectations
        # in the expectations list
        for expectation in self.expectations_list:
            # verifies the current expectation
            return_value = expectation.verify_expectation(self, mock_call, self.verification_state_map)

            # in case the return value is false
            if not return_value:
                # raises an expectation failed exception
                raise main_mock_exceptions.ExpectationFailed("problem verifying expectation %s" % expectation)
            elif type(return_value) == types.InstanceType and return_value.__class__ == ExpectationResult:
                # raises an expectation failed exception
                raise main_mock_exceptions.ExpectationFailed("problem verifying expectation %s (%s)" % (expectation, return_value))

    def _mock_return(self, *args, **kwargs):
        """
        Retrieves the mock return value for the given arguments.

        @rtype: Object
        @return: The mock return value for the given arguments.
        """

        # in case a raising is defined
        if self.mock_raises:
            raise self.mock_raises
        # in case a return is defined
        elif self.mock_return:
            return self.mock_return
        # in case a return iterator is defined
        elif self.mock_returns_iterator:
            try:
                # returns the current returns iterator
                return self.mock_returns_iterator.next()
            except StopIteration:
                raise main_mock_exceptions.InvalidReturnIteration("no more mock return values are present")
        # in case return method is defined
        elif self.mock_returns_method:
            # calls the mock returns method
            return self.mock_returns_method(*args, **kwargs)

        # returns none
        return None

class MockCall:
    """
    Class that represents a mock call.
    """

    method_name = None
    """ The method name """

    method_arguments = []
    """ The method arguments """

    methid_key_arguments = {}
    """ The method key arguments """

    method_return = None
    """ The method return """

    method_exception = None
    """ The method exception """

    def __init__(self, method_name, method_arguments, method_key_arguments, method_return, method_exception):
        """
        Constructor of the class.

        @type method_name: String
        @param method_name: The method name.
        @type method_arguments: List
        @param method_arguments: The method arguments.
        @type method_key_arguments: Dictionary
        @param method_key_arguments: The method key arguments.
        @type method_return: Object
        @param method_return:  The method return.
        @type method_exception: Exception
        @param method_exception: The method exception.
        """

        self.method_name = method_name
        self.method_arguments = method_arguments
        self.method_key_arguments = method_key_arguments
        self.method_return = method_return
        self.method_exception = method_exception

    def __repr__(self):
        # retrieves the various parts of the
        parts = [str(method_argument) for method_argument in self.method_arguments]

        # extends the parts fot the given kword items
        parts.extend("%s=%r" % method_key_argument_items for method_key_argument_items in sorted(self.method_key_arguments.items()))

        # creates the message
        message = "%s(%s) -> %s" % (self.method_name, ", ".join(parts), str(self.method_return))

        # returns the message
        return message

    def set_method_name(self, method_name):
        """
        Sets the method name.

        @type method_name: String
        @param method_name: The method name.
        """

        self.method_name = method_name

    def get_method_name(self):
        """
        Retrieves the method name.

        @rtype: String
        @return: The method name.
        """

        return self.method_name

    def set_method_arguments(self, method_arguments):
        """
        Sets the method arguments.

        @type method_arguments: List
        @param method_arguments: The method arguments.
        """

        self.method_arguments = method_arguments

    def get_method_arguments(self):
        """
        Retrieves the method arguments.

        @rtype: List
        @return: The method arguments.
        """

        return self.method_arguments

    def set_method_key_arguments(self, method_key_arguments):
        """
        Sets the method key arguments.

        @type method_key_arguments: Dictionary
        @param method_key_arguments: The method key arguments.
        """

        self.method_key_arguments = method_key_arguments

    def get_method_key_arguments(self):
        """
        Retrieves the method key arguments.

        @rtype: Dictionary
        @return: The method key arguments.
        """

        return self.method_key_arguments

    def set_method_return(self, method_return):
        """
        Sets the method return.

        @type method_return: Object
        @param method_return: The method return.
        """

        self.method_return = method_return

    def get_method_return(self):
        """
        Retrieves the method return.

        @rtype: Object
        @return: The method return.
        """

        return self.method_return

    def set_method_exception(self, method_exception):
        """
        Sets the method exception.

        @type method_exception: Exception
        @param method_exception: The method exception.
        """

        self.method_exception = method_exception

    def get_method_exception(self):
        """
        Retrieves the method exception.

        @rtype: Exception
        @return: The method exception.
        """

        return self.method_exception

class Expectations:
    """
    The expectations class used to control mock expectations.
    """

    expectations_list = []
    """ The expectation list """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.expectations_list = []

    def add_expectation(self, expectation):
        """
        Adds an expectation to the expectations list.

        @type expectation: Expectatation
        @param expectation: The expectation to be added.
        """

        # adds the expectation to the expectations list
        self.expectations_list.append(expectation)

    def remove_expectation(self, expectation):
        """
        Adds an expectation from the expectations list.

        @type expectation: Expectatation
        @param expectation: The expectation to be removed.
        """

        # removes the expectation from the expectations list
        self.expectations_list.remove(expectation)

    def get_expectations_list(self):
        """
        Retrieves the expectations list.

        @rtype: List
        @return: The expectations list.
        """

        return self.expectations_list

    def set_expectations_list(self, expectations_list):
        """
        Sets the expectations list.

        @type expectations_list: List
        @param expectations_list: The expectations list.
        """

        self.expectations_list = expectations_list

class Expectation:
    """
    The expectation class used to control mock expectation.
    """

    def __init__(self):
        """
        Constructor of the class
        """

        pass

    def __repr__(self):
        return self.__class__.__name__

    def verify_expectation(self, mock, mock_call, verification_state_map):
        """
        Verifies the given expectation for the given mock.

        @type mock: Mock
        @param mock: The mock object to verify the expectation.
        @type mock_call: MockCall
        @param mock_call: The mock call to verify the expectation.
        @type verification_state_map: Dictionary
        @param verification_state_map: The verification state map that contains
        the verification state.
        @rtype: bool
        @return: The result of the verification.
        """

        return True

class ParametersExpectation(Expectation):
    """
    The parameters expectation class.
    """

    method_arguments = []
    """ The method arguments """

    method_key_arguments = {}
    """ The method key arguments """

    def __init__(self, method_arguments = [], method_key_arguments = {}):
        """
        Constructor of the class

        @type method_arguments: List
        @param method_arguments: The list of expected method arguments.
        @type method_key_arguments: Dictionary
        @param method_key_arguments: The map of expected method key arguments.
        """

        Expectation.__init__(self)
        self.method_arguments = method_arguments
        self.method_key_arguments = method_key_arguments

    def verify_expectation(self, mock, mock_call, verification_state_map):
        # calls the super object retrieving the result
        result = Expectation.verify_expectation(self, mock, mock_call, verification_state_map)

        # in case the result id false
        if not result:
            # returns false immediately
            return False

        # retrieves the mock call method arguments
        mock_call_method_arguments = mock_call.get_method_arguments()

        # retrieves the mock call method key arguments
        mock_call_method_key_arguments = mock_call.get_method_key_arguments()

        # in case the method arguments are not the same
        if not self.method_arguments == mock_call_method_arguments:
            # returns expectation result
            return ExpectationResult(self.method_arguments, mock_call_method_arguments)

        # in case the method key arguments are not the same
        if not self.method_key_arguments == mock_call_method_key_arguments:
            # returns expectation result
            return ExpectationResult(self.method_key_arguments, mock_call_method_key_arguments)

        # returns true
        return True

class ReturnExpectation(Expectation):
    """
    The return expectation class.
    """

    return_value = None
    """ The return value """

    returns_iterator_value = None
    """ The returns iterator value """

    returns_method_value = None
    """ The returns method value """

    def __init__(self, return_value = None, returns_iterator_value = None, returns_method_value = None):
        Expectation.__init__(self)
        self.return_value = return_value
        self.returns_iterator_value = returns_iterator_value
        self.returns_method_value = returns_method_value

    def verify_expectation(self, mock, mock_call, verification_state_map):
        # calls the super object retrieving the result
        result = Expectation.verify_expectation(self, mock, mock_call, verification_state_map)

        # in case the result id false
        if not result:
            # returns false immediately
            return False

        # retrieves the mock call method return
        mock_call_method_return = mock_call.get_method_return()

        # in case a return is defined
        if self.return_value:
            expected_return_value = self.mock_return
        # in case a return iterator is defined
        elif self.returns_iterator_value:
            try:
                # returns the current returns iterator
                expected_return_value = self.returns_iterator_value.next()
            except StopIteration:
                raise main_mock_exceptions.InvalidReturnIteration("no more mock return values are present")
        # in case return method is defined
        elif self.returns_method_value:
            # calls the mock returns method
            expected_return_value = self.returns_method_value(*args, **kwargs)

        # in case the call method return value is not the expected
        if not expected_return_value == mock_call_method_return:
            # returns expectation result
            return ExpectationResult(expected_return_value, mock_call_method_return)

        # returns true
        return True

class ExceptionExpectation(Expectation):
    """
    The exception expectation class.
    """

    exception_value = None
    """ The exception value """

    successful_calls = 0
    """ The sucessfull calls count (the number of calls before expecting exception) """

    call_count = 0
    """ The number of calls made """

    def __init__(self, exception_value = None, successful_calls = 0):
        Expectation.__init__(self)
        self.exception_value = exception_value
        self.successful_calls = successful_calls

    def verify_expectation(self, mock, mock_call, verification_state_map):
        # increments the call count
        self.call_count += 1

        # calls the super object retrieving the result
        result = Expectation.verify_expectation(self, mock, mock_call, verification_state_map)

        # in case the result id false
        if not result:
            # returns false immediately
            return False

        # in case the call call is greater than the sucessfull calls
        if self.call_count > self.successful_calls:
            # retrieves the mock call method expection
            mock_call_method_exception = mock_call.get_method_exception()

            # retrieves the call method exception class
            mock_call_method_exception_class = mock_call_method_exception.__class__

            # in case the mock call method exception is not valid
            if not mock_call_method_exception:
                # sets the result as false
                result = False

            # in case the mock call method exception is not an exception
            if not type(mock_call_method_exception) == exceptions.Exception:
                # sets the result as false
                result = False

            # in case the call method exception value is not the expected
            if not self.exception_value == mock_call_method_exception_class:
                # sets the result as false
                result = False

            # in case the result is invalid
            if not result:
                # returns expectation result
                return ExpectationResult(self.exception_value, mock_call_method_exception_class)

        # returns true
        return True

class ExpectationResult:
    """
    The expectation result class used to encapsulate mock expectation resuls.
    """

    expected_value = None
    """ The expected value """

    received_value = None
    """ The received value """

    def __init__(self, expected_value = None, received_value = None):
        """
        Constructor of the class.

        @type expected_value: Object
        @param expected_value: The expected value.
        @type received_value: Object
        @param received_value: The received value.
        """

        self.expected_value = expected_value
        self.received_value = received_value

    def __repr__(self):
        return "Expected '%s' received '%s" % (self.expected_value, self.received_value)

    def get_expected_value(self):
        """
        Retrieves the expected value.

        @rtype: Object
        @return: The expected value.
        """

        return self.expected_value

    def set_expected_value(self, expected_value):
        """
        Sets the expected value.

        @type expected_value: Object
        @param expected_value: The expected value.
        """

        self.expected_value = expected_value


    def get_received_value(self):
        """
        Retrieves the received value.

        @rtype: Object
        @return: The received value.
        """

        return self.received_value

    def set_received_value(self, received_value):
        """
        Sets the received value.

        @type received_value: Object
        @param received_value: The expected value.
        """

        self.received_value = received_value
