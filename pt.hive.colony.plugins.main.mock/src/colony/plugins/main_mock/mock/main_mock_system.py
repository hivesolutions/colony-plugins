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

    def generate_mockery(self):
        """
        Generates a new mockery.

        @rtype: Mockery
        @return: The generated mockery.
        """

        return None

    def generate_mock(self, class_reference):
        pass

    def generate_expectation(self):
        pass

class Mockery:
    """
    The mockery class used to manage mocks.
    """

    def __init__(self):
        pass

    def checking(self):
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

    mock_name = None
    """ The mock name """

    def __init__(self, name, returns = None, returns_iter = None, returns_func = None, raises = None):
        self.mock_name = name
        self.mock_returns = returns
        if returns_iter is not None:
            returns_iter = iter(returns_iter)
        self.mock_returns_iter = returns_iter
        self.mock_returns_func = returns_func
        self.mock_raises = raises
        self.mock_attrs = {}

    def __repr__(self):
        return "<Mock '%s' '%s'>" % (hex(id(self)), self.mock_name)

    def __call__(self, *args, **kw):
        MockCall()
        # @todo
        # tenho de manter aki o registo de tudo o que se passa em termos de chamada
        # tenho de poder fazer try catch se necessario

        # retrieves the various parts of the
        parts = [repr(a) for a in args]

        # extends the parts fot the given kword items
        parts.extend("%s=%r" % (items) for items in sorted(kw.items()))

        # creates the message
        message = "Called %s(%s)" % (self.mock_name, ', '.join(parts))

        # prints the message
        print message

        # returns the mock return
        return self._mock_return(*args, **kw)

    def _mock_return(self, *args, **kw):
        if self.mock_raises is not None:
            raise self.mock_raises
        elif self.mock_returns is not None:
            return self.mock_returns
        elif self.mock_returns_iter is not None:
            try:
                return self.mock_returns_iter.next()
            except StopIteration:
                raise Exception("No more mock return values are present.")
        elif self.mock_returns_func is not None:
            return self.mock_returns_func(*args, **kw)
        else:
            return None

    def __getattr__(self, attr):
        if attr not in self.mock_attrs:
            if self.mock_name:
                new_name = self.mock_name + '.' + attr
            else:
                new_name = attr
            self.mock_attrs[attr] = Mock(new_name)
        return self.mock_attrs[attr]

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

    def __init__(self, method_name, method_arguments, method_key_arguments):
        self.method_name = method_name
        self.method_arguments = method_arguments
        self.methid_key_arguments = method_key_arguments

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
