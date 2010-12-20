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

import unittest

import main_console_system

class MainConsoleTestCase(unittest.TestCase):
    """
    The main console test case class.
    """

    last_output = None
    """ The last output value """

    def setUp(self):
        self.main_console = main_console_system.MainConsole(MainConsoleTestCase.plugin)

    def test_process_command_line(self):
        """
        Tests the process command line using one of the commands.
        """

        # process the status command line
        return_value = self.main_console.process_command_line("status", self.output_method)

        # assets the return value
        self.assertEqual(return_value, True)

    def test_echo_command(self):
        """
        Tests the echo command of the console.
        """

        # process the echo command line
        return_value = self.main_console.process_command_line("echo colony", self.output_method)

        # asserts the echo value
        self.assertEqual(self.last_output, "colony")

        # assets the return value
        self.assertEqual(return_value, True)

    def test_echo_command_invalid_arguments(self):
        """
        Tests and invalid command of the console.
        """

        # process the invalid command line
        return_value = self.main_console.process_command_line("echo", self.output_method)

        # asserts the echo value
        self.assertEqual(self.last_output, main_console_system.INVALID_NUMBER_ARGUMENTS_MESSAGE)

        # assets the return value
        self.assertEqual(return_value, True)

    def test_invalid_command(self):
        """
        Tests and invalid command of the console.
        """

        # process the invalid command line
        return_value = self.main_console.process_command_line("invalid_command", self.output_method)

        # asserts the echo value
        self.assertEqual(self.last_output, main_console_system.INVALID_COMMAND_MESSAGE)

        # assets the return value
        self.assertEqual(return_value, False)

    def output_method(self, text, new_line = True):
        self.last_output = text
