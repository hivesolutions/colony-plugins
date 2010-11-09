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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

CONSOLE_EXTENSION_NAME = "test"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

INVALID_TEST_ID_MESSAGE = "invalid test id"
""" The invalid test id message """

HELP_TEXT = "### UNIT TESTING HELP ###\n\
start_test <unit-testid> - starts a unit test\n\
start_all_test           - starts all the unit tests\n\
show_all_test            - shows all the unit tests"
""" The help text """

TABLE_TOP_TEXT = "ID      TEST CASE NAME                PLUGIN ID"
""" The table top text """

FIRST_COLUMN_SPACING = 8
""" The first column spacing """

SECOND_COLUMN_SPACING = 30
""" The second column spacing """

ID_REGEX = "[0-9]+"
""" The regular expression to retrieve the id of the test case """

class ConsoleTest:
    """
    The console test class.
    """

    main_test_plugin = None
    """ The main test plugin """

    commands = ["start_test", "start_all_test", "show_all_test"]
    """ The commands list """

    def __init__(self, main_test_plugin):
        """
        Constructor of the class.

        @type main_test_plugin: MainTestPlugin
        @param main_test_plugin: The main test plugin.
        """

        self.main_test_plugin = main_test_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_start_test(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the test case id
        test_case_id = args[0]

        # retrieves the test cases for the given test case id
        test_cases = self.get_test_cases(test_case_id)

        if test_cases:
            output_method("starting test case " + test_case_id)
            self.main_test_plugin.main_test.start_test(test_cases)
        else:
            output_method("invalid test case id")

    def process_start_all_test(self, args, output_method):
        output_method("starting all test cases")
        self.main_test_plugin.main_test.start_all_test()

    def process_show_all_test(self, args, output_method):
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
