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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys
import stat

import os.path

import colony.libs.string_buffer_util

SPACE_TAB = "    "
""" The space tab string """

WIN32_SYSTEM = "win32"
""" The win32 system value """

class StringNormalization:
    """
    The string normalization class.
    """

    string_normalization_plugin = None
    """ The string normalization plugin """

    def __init__(self, string_normalization_plugin):
        """
        Constructor of the class.

        @type string_normalization_plugin: StringNormalizationPlugin
        @param string_normalization_plugin: The string normalization plugin.
        """

        self.string_normalization_plugin = string_normalization_plugin

def remove_trailing_newlines(file_path, windows_newline):
    # opens the file for reading
    file = open(file_path, "r")

    # creates a string buffer for buffering
    string_buffer = colony.libs.string_buffer_util.StringBuffer()

    # reads the file lines
    file_lines = file.readlines()

    # reverses the file lines
    file_lines.reverse()

    # start the index
    index = 0

    # iterates over all the lines in the file
    # in order to count the final newlines
    for line in file_lines:
        # in case the line is not just a newline character
        if not line == "\n" and not line == "\r\n":
            break

        # decrements the index value
        index -= 1

    # reverses the file lines
    file_lines.reverse()

    if index == 0:
        # retrieves the valid file lines
        valid_file_lines = file_lines
    else:
        # retrieves the valid file lines
        valid_file_lines = file_lines[:index]

    # iterates over all the file lines
    for valid_file_line in valid_file_lines:
        # writes the valid file line to the string buffer
        string_buffer.write(valid_file_line)

    # closes the file for reading
    file.close()

    # retrieves the string value from the string buffer
    string_value = string_buffer.get_value()

    # opens the file for writing
    file = open(file_path, "w")

    # writes the string value to the file
    file.write(string_value)

    # closes the file for writing
    file.close()

def remove_trailing_spaces(file_path, tab_to_spaces, windows_newline):
    # opens the file for reading
    file = open(file_path, "r")

    # creates a string buffer for buffering
    string_buffer = colony.libs.string_buffer_util.StringBuffer()

    # iterates over all the lines in the file
    for line in file:
        # strips the line
        line_stripped = line.rstrip()

        # in case the tab must be replaced with spaces
        if tab_to_spaces:
            # replaces the tab characters with spaces
            line_stripped = line_stripped.replace("\t", SPACE_TAB)

        # writes the stripped line to the string buffer
        string_buffer.write(line_stripped)

        # in case the newline is of type windows
        # and the current platform is not windows
        if windows_newline and not sys.platform == WIN32_SYSTEM:
            # writes the carriage return character and the new line character
            string_buffer.write("\r\n")
        else:
            # writes the new line character
            string_buffer.write("\n")

    # closes the file for reading
    file.close()

    # retrieves the string value from the string buffer
    string_value = string_buffer.get_value()

    # opens the file for writing
    file = open(file_path, "w")

    # writes the string value to the file
    file.write(string_value)

    # closes the file for writing
    file.close()

def remove_trailing_spaces_walker(arguments, directory_name, names):
    """
    Walker function for the removal of trailing spaces
    from files.

    @type arguments: List
    @param arguments: The list of arguments for the removal.
    @type directory_name: String
    @param directory_name: The name of the current directory being walked.
    @type names: List
    @param names: The symbol names of the current directory.
    """

    # unpacks the arguments, retrieving the tab to spaces, trailing newlines, windows newline
    # and file extensions value
    tab_to_spaces, trailing_newlines, windows_newline, file_extensions = arguments

    # retrieves all the names of files that are not directories
    valid_complete_names = [directory_name + "/" + name for name in names if not stat.S_ISDIR(os.stat(directory_name + "/" + name)[stat.ST_MODE])]

    # filters the files with valid file extensions
    valid_complete_names_extensions = [name for name in valid_complete_names if file_extensions == None or name.split(".")[-1] in file_extensions]

    # iterates over all the valid file names
    for valid_complete_names_extension in valid_complete_names_extensions:
        # prints a logging message
        print "Removing trail in file: %s" % valid_complete_names_extension

        # removes the trailing spaces from the file
        remove_trailing_spaces(valid_complete_names_extension, tab_to_spaces, windows_newline)

        # in case the removal of extra newlines is active
        if trailing_newlines:
            # prints a logging message
            print "Removing trail newlines in file: %s" % valid_complete_names_extension

            # removes the extra newlines from the file
            remove_trailing_newlines(valid_complete_names_extension, windows_newline)

def remove_trailing_spaces_recursive(directory_path, tab_to_spaces, trailing_newlines, windows_newline, file_extensions = None, ):
    os.path.walk(directory_path, remove_trailing_spaces_walker, (tab_to_spaces, trailing_newlines, windows_newline, file_extensions))

#if __name__ == "__main__":
#    if len(sys.argv) < 2:
#        print "Invalid number of arguments"
#        print "Usage: " + USAGE_MESSAGE
#        sys.exit(2)
#
#    path = sys.argv[1]
#    recursive = False
#    tab_to_spaces = False
#    trailing_newlines = False
#    windows_newline = True
#    file_extensions = None
#
#    if len(sys.argv) > 2:
#        try:
#            opts, args = getopt.getopt(sys.argv[2:], "rtnue:", [])
#        except getopt.GetoptError, error:
#            print "Invalid number of arguments"
#            print "Usage: " + USAGE_MESSAGE
#            sys.exit(2)
#
#        for option, value in opts:
#            if option == "-r":
#                recursive = True
#            elif option == "-t":
#                tab_to_spaces = True
#            elif option == "-n":
#                trailing_newlines = True
#            elif option == "-u":
#                windows_newline = False
#            elif option == "-e":
#                file_extensions = [value.strip() for value in value.split(",")]
#
#    if recursive:
#        remove_trailing_spaces_recursive(path, tab_to_spaces, trailing_newlines, windows_newline, file_extensions)
#    else:
#        remove_trailing_spaces(path, tab_to_spaces, windows_newline)
#        if trailing_newlines:
#            remove_trailing_newlines(path, windows_newline)
