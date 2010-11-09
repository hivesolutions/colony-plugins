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

__revision__ = "$LastChangedRevision: 1089 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-22 23:19:39 +0000 (qui, 22 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

TEST_IMAGE_PATH = "printing/manager/resources/test_logo.png"
""" The test image relative path """

CONSOLE_EXTENSION_NAME = "printing"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### PRINTING HELP ###\n\
print_test                          - prints a test page\n\
print_test_image                    - prints a test page with an image\n\
print_printing_language <file-path> - prints the page described in the file of the given file path"
""" The help text """

class ConsolePrintingManager:
    """
    The console printing manager class.
    """

    printing_manager_plugin = None
    """ The printing manager plugin """

    commands = ["print_test", "print_test_image", "print_printing_language"]
    """ The commands list """

    def __init__(self, printing_manager_plugin):
        """
        Constructor of the class.

        @type printing_manager_plugin: PrintingManagerPlugin
        @param printing_manager_plugin: The printing manager plugin.
        """

        self.printing_manager_plugin = printing_manager_plugin

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

    def process_print_test(self, args, output_method):
        # retrieves the printing manager instance
        printing_manager = self.printing_manager_plugin.printing_manager

        # prints the test page
        printing_manager.print_test()

    def process_print_test_image(self, args, output_method):
        # retrieves the printing manager instance
        printing_manager = self.printing_manager_plugin.printing_manager

        # prints the test page with an image
        printing_manager.print_test_image()

    def process_print_printing_language(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the printing language file path
        printing_language_file_path = args[0]

        # opens the printing language file
        printing_language_file = open(printing_language_file_path, "r")

        # reads the printing language file contents
        printing_language_file_contents = printing_language_file.read()

        # closes the printing language file
        printing_language_file.close()

        # retrieves the printing manager instance
        printing_manager = self.printing_manager_plugin.printing_manager

        # prints the printing language file
        printing_manager.print_printing_language(printing_language_file_contents)
