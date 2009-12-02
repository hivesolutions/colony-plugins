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

__revision__ = "$LastChangedRevision: 6466 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-11-23 11:20:49 +0000 (seg, 23 Nov 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

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

    def generate_expectation(self):
        """
        Generates a new expectation to be used.

        @rtype: Expectation
        @return: The generated expectation.
        """

        pass

class Expectations:
    """
    The expectations class used to control mock expectations.
    """

    expectations_list = []
    """ The expectation list """

    def __init__(self):
        self.expectations_list = []

    def add_expectation(self, expectation):
        self.expectations_list.append(expectation)

    def remove_exception(self, exception):
        self.expectations_list.remove(expectation)

class Expectation:
    """
    The expectation class used to control mock expectation.
    """

    def __init__(self):
        pass

    def verify_expectation(self, mock):
        """
        Verifies the given expectation for the given mock.

        @type mock: Mock
        @param mock: The mock object to verify the expectation.
        @rtype: bool
        @return: The result of the verification.
        """

        return True

class ParametersExpectation(Expectation):
    """
    The parameters expectation class.
    """

    def __init__(self):
        Expectation.__init__(self)

    def verify_expectation(self, mock):
        # calls the super object retrieving the result
        result = Expectation.verify_expectation(self, mock)

        # in case the result id false
        if not result:
            # returns false immediately
            return False

        pass

class ParametersExpectation(Expectation):
    """
    The parameters expectation class.
    """

    methodNamesList = []
    """ The method names list """

    def __init__(self, methodNamesList):
        Expectation.__init__(self)
        self.methodNamesList = methodNamesList

class ParameterExpectation(Expectation):
    """
    The parameter expectation class.
    """

    def __init__(self):
        Expectation.__init__(self)

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

    def __init__(self, mock_name = "anonymous", mock_return = None, mock_returns_iterator = None, mock_returns_method = None, mock_raises = None):
        self.mock_name = mock_name
        self.mock_return = mock_return
        self.mock_returns_iterator = mock_returns_iterator
        self.mock_returns_method = mock_returns_method
        self.mock_raises = mock_raises
        self.mock_attrs = {}
        self.mock_calls_list = []

    def __repr__(self):
        return "<Mock '%s' '%s'>" % (hex(id(self)), self.mock_name)

    def __call__(self, *args, **kwargs):
        # retrieves the mock return
        mock_return = self._mock_return(*args, **kwargs)

        # creates a new mock call
        mock_call = MockCall(self.mock_name, args, kwargs, mock_return)

        # adds the mock call to the mock calls list
        self.mock_calls_list.append(mock_call)

        # prints the message
        print mock_call

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

    method_return = {}
    """ The method return """

    def __init__(self, method_name, method_arguments, method_key_arguments, method_return):
        self.method_name = method_name
        self.method_arguments = method_arguments
        self.method_key_arguments = method_key_arguments
        self.method_return = method_return

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
