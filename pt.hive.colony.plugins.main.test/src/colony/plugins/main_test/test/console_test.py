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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

TABLE_TOP_TEXT = "ID      TEST CASE NAME                PLUGIN ID"
""" The table top text """

FIRST_COLUMN_SPACING = 8
""" The first column spacing """

SECOND_COLUMN_SPACING = 30
""" The second column spacing """

ID_REGEX = "[0-9]+"
""" The regular expression to retrieve the id of the test case """

CONSOLE_EXTENSION_NAME = "main_test"
""" The console extension name """

class ConsoleTest:
    """
    The console main test class.
    """

    main_test_plugin = None
    """ The main test plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, main_test_plugin):
        """
        Constructor of the class.

        @type main_test_plugin: MainTestPlugin
        @param main_test_plugin: The main test plugin.
        """

        self.main_test_plugin = main_test_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_start_test(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the start test command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the main test instance
        main_test = self.main_test_plugin.main_test

        # retrieves the test case id from the arguments
        test_case_id = arguments_map["test_case_id"]

        # retrieves the test cases for the given test case id
        test_cases = self.get_test_cases(test_case_id)

        if test_cases:
            output_method("starting test case " + test_case_id)
            result = main_test.start_test(test_cases)

            # processes the result
            self._process_result(result, output_method)
        else:
            output_method("invalid test case id")

    def process_start_all_test(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the start all test command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the main test instance
        main_test = self.main_test_plugin.main_test

        # outputs a message stating that testing has started
        output_method("starting all test cases")

        # runs the all tests
        result = main_test.start_all_test()

        # processes the result
        self._process_result(result, output_method)

    def process_show_all_test(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the show all test command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # prints the table top text
        output_method(TABLE_TOP_TEXT)

        # retrieves the main test instance
        main_test = self.main_test_plugin.main_test

        # retrieves all the available test cases
        test_cases = main_test.get_all_test_cases()

        # iterates over all the test cases
        for test_case in test_cases:
            # retrieves the internal id of the test case
            test_case_id = main_test.loaded_test_cases_id_map[test_case]

            # converts the internal id of the test case to string
            test_case_id_str = str(test_case_id)

            # retrieves the test case name
            test_case_name = main_test.test_case_test_case_name_map[test_case]

            # retrieves the test case plugin associated with the test case
            test_case_plugin = main_test.test_case_test_case_plugin_map[test_case]

            # retrieves the id of the test case plugin
            test_case_plugin_id = test_case_plugin.id

            output_method(test_case_id_str, False)

            for _index in range(FIRST_COLUMN_SPACING - len(test_case_id_str)):
                output_method(" ", False)

            output_method(test_case_name, False)

            for _index in range(SECOND_COLUMN_SPACING - len(test_case_name)):
                output_method(" ", False)

            output_method(test_case_plugin_id, True)

    def get_test_cases(self, id):
        test_cases = None
        valid = False

        # retrieves the main test instance
        main_test = self.main_test_plugin.main_test

        # compiles the regular expression
        compilation = re.compile(ID_REGEX)
        result = compilation.match(id)

        # if there is at least one match
        if result:
            valid = result.group() == id

        # if it matches the regular expression
        if valid:
            int_value = int(id)
            if int_value in main_test.id_loaded_test_cases_map:
                test_case = main_test.id_loaded_test_cases_map[int_value]
                test_cases = [test_case]
        else:
            test_case_name = id

            if test_case_name in main_test.test_case_name_test_cases_map:
                # retrieves the test cases associated with the given test case name
                test_cases = main_test.test_case_name_test_cases_map[test_case_name]

        return test_cases

    def _process_result(self, result, output_method):
        # retrieves the tests run
        result_tests_run = result.testsRun

        # retrieves the failures and errors
        result_failures = result.failures
        result_errors = result.errors

        # retrieves the length of failures and errors
        failures_length = len(result_failures)
        errors_length = len(result_errors)

        # outputs a message
        output_method("[%d] tests executed..." % result_tests_run)

        # outputs a message
        output_method("[%d] failures found..." % failures_length)

        # iterates over all the result failures
        for failure, failure_traceback in result_failures:
            # retrieves the failure id
            failure_id = failure.id()

            # outputs the failure description
            output_method("name: " + failure_id)
            output_method("traceback: " + failure_traceback)

        # outputs a message
        output_method("[%d] errors found..." % errors_length)

        # iterates over all the result errors
        for error, error_traceback in result_errors:
            # retrieves the error id
            error_id = error.id()

            # prints the error description
            output_method("name: " + error_id)
            output_method("traceback: " + error_traceback)

    def get_test_case_id_list(self, argument, console_context):
        # retrieves the main test instance
        main_test = self.main_test_plugin.main_test

        # retrieves all the available test cases
        test_cases = main_test.get_all_test_cases()

        # initializes the test case ids list
        test_case_ids = []

        # collects the test case ids
        for test_case in test_cases:
            # retrieves the test case ids
            test_case_id = main_test.loaded_test_cases_id_map[test_case]

            # creates the string representation of the test case id
            test_case_id_string = str(test_case_id)

            # adds the test case id to the list
            test_case_ids.append(test_case_id_string)

        # returns the test case ids
        return test_case_ids

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "start_test" : {
                "handler" : self.process_start_test,
                "description" : "starts a unit test",
                "arguments" : [
                    {
                        "name" : "test_case_id",
                        "description" : "the unique identifier for the test case",
                        "values" : self.get_test_case_id_list,
                        "mandatory" : True
                    }
                ]
            },
            "start_all_test" : {
                "handler" : self.process_start_all_test,
                "description" : "starts all the unit tests"
            },
            "show_all_test" : {
                "handler" : self.process_show_all_test,
                "description" : "shows all the unit tests"
            }
        }

        # returns the commands map
        return commands_map
