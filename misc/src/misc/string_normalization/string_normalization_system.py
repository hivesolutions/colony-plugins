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

import os
import sys
import stat

import colony.libs.string_buffer_util

SPACE_TAB = "    "
""" The space tab string """

NEWLINE = "\n"
""" The newline string """

NEWLINE_WINDOWS = "\r\n"
""" The windows newline string """

TAB = "\t"
""" The tab string """

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

    def remove_trailing_newlines_file(self, file_path, windows_newline):
        """
        Removes the trailing newlines from the contents given.
        This method uses a file and the given file replaces with the
        new contents.

        @type file_path: String
        @param file_path: The path to the file to have the trailing
        newlines removed.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        """

        # reads the file retrieving the file contents
        file_contents = self._read_file(file_path)

        # retrieves the valid contents by removing the
        # trailing newlines from the file contents
        valid_contents = self.remove_trailing_newlines(file_contents, windows_newline)

        # writes the (valid) file contents to the file
        self._write_file(file_path, valid_contents)

    def remove_trailing_newlines(self, contents, windows_newline):
        """
        Removes the trailing newlines from the contents given.

        @type contents: String
        @param contents: The contents to have the trailing newlines removed.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        @rtype: String
        @return: The contents with the trailing newlines removed.
        """

        # prepares the contents lines, retrieving
        # the lines list
        lines_list = self._prepare_lines(contents)

        # filters the lines list, retrieving the valid ones
        valid_lines_list = self._filter_valid_lines(lines_list)

        # creates a string buffer for buffering
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates over all the valid lines
        for valid_line in valid_lines_list:
            # strips the valid line
            valid_line_stripped = valid_line.rstrip()

            # writes the valid line to the string buffer
            string_buffer.write(valid_line_stripped)

            # in case the newline is of type windows
            # and the current platform is not windows
            if windows_newline and not sys.platform == WIN32_SYSTEM:
                # writes the carriage return character and the new line character
                string_buffer.write(NEWLINE_WINDOWS)
            else:
                # writes the new line character
                string_buffer.write(NEWLINE)

        # retrieves the string value from the string buffer
        string_value = string_buffer.get_value()

        # returns the valid string value
        return string_value

    def remove_trailing_spaces_file(self, file_path, tab_to_spaces, windows_newline):
        """
        Removes the trailing spaces from the contents given.
        This method uses a file and the given file replaces with the
        new contents.

        @type file_path: String
        @param file_path: The path to the file to have the trailing
        newlines removed.
        @type tab_to_spaces: bool
        @param tab_to_spaces: If the tab characters should be converted to spaces.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        """

        # reads the file retrieving the file contents
        file_contents = self._read_file(file_path)

        # retrieves the valid contents by removing the
        # trailing spaces from the file contents
        valid_contents = self.remove_trailing_spaces(file_contents, tab_to_spaces, windows_newline)

        # writes the (valid) file contents to the file
        self._write_file(file_path, valid_contents)

    def remove_trailing_spaces(self, contents, tab_to_spaces, windows_newline):
        """
        Removes the trailing spaces from the contents given.

        @type contents: String
        @param contents: The contents to have the trailing spaces removed.
        @type tab_to_spaces: bool
        @param tab_to_spaces: If the tab characters should be converted to spaces.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        @rtype: String
        @return: The contents with the trailing spaces removed.
        """

        # prepares the contents lines, retrieving
        # the lines list
        lines_list = self._prepare_lines(contents)

        # creates a string buffer for buffering
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates over all the lines in the lines list
        for line in lines_list:
            # strips the line
            line_stripped = line.rstrip()

            # in case the tab must be replaced with spaces
            if tab_to_spaces:
                # replaces the tab characters with spaces
                line_stripped = line_stripped.replace(TAB, SPACE_TAB)

            # writes the stripped line to the string buffer
            string_buffer.write(line_stripped)

            # in case the newline is of type windows
            # and the current platform is not windows
            if windows_newline and not sys.platform == WIN32_SYSTEM:
                # writes the carriage return character and the new line character
                string_buffer.write(NEWLINE_WINDOWS)
            else:
                # writes the new line character
                string_buffer.write(NEWLINE)

        # retrieves the string value from the string buffer
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

    def remove_trailing_spaces_recursive(self, directory_path, tab_to_spaces, trailing_newlines, windows_newline, file_extensions):
        """
        Removes the trailing spaces recursively from the given directory path.
        The control parameters include tab to spaces, removal of trailing newlines
        use of the windows line and file extensions filter.

        @type directory_path: String
        @param directory_path: The path to the directory to be used.
        @type tab_to_spaces: bool
        @param tab_to_spaces: If the tab characters should be converted to spaces.
        @type trailing_newlines: bool
        @param trailing_newlines: If the trailing newlines should be removed.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        @type file_extensions: List
        @param file_extensions: The list of file extensions to be filtered.
        """

        os.path.walk(directory_path, self._remove_trailing_spaces_walker, (tab_to_spaces, trailing_newlines, windows_newline, file_extensions))

    def _prepare_lines(self, string_value):
        """
        Prepares the given string value lines, creating a list of
        normalized line values.

        @type string_value: String
        @param string_value: The string value to be converted to list.
        @rtype: List
        @return: The list of prepared line values.
        """

        # splits the string value in the newline and then for each
        # line appends the newline string value
        lines_list = [value + NEWLINE for value in string_value.split("\n")]

        # returns the lines list
        return lines_list

    def _filter_valid_lines(self, lines_list):
        # counts the number of valid lines
        valid_lines_count = self._count_valid_lines(lines_list)

        # retrieves the list of valid lines
        valid_lines_list = lines_list[:valid_lines_count]

        # returns the valid lines list
        return valid_lines_list

    def _count_valid_lines(self, lines_list):
        # starts the index value with the length
        # of the lines list
        index = len(lines_list)

        # inverts the lines list order to count
        # the valid lines
        lines_list.reverse()

        # iterates over all the lines in the lines list
        # in order to count the number of valid lines
        for line in lines_list:
            # in case the line is not just a newline character
            if not line in (NEWLINE, NEWLINE_WINDOWS):
                break

            # decrements the index value
            index -= 1

        # inverts the lines list order (to get back
        # to the original order)
        lines_list.reverse()

        # returns the index value as the number of valid
        # lines in the lines list
        return index

    def _read_file(self, file_path):
        # opens the file for reading
        file = open(file_path, "r")

        try:
            # reads the file contents
            file_contents = file.read()
        finally:
            # closes the file
            file.close()

        # returns the file contents
        return file_contents

    def _write_file(self, file_path, file_contents):
        # opens the file for writing
        file = open(file_path, "w")

        try:
            # writes the file contents
            file_contents = file.write(file_contents)

            # flushes the file contents
            file.flush()
        finally:
            # closes the file
            file.close()

    def _remove_trailing_spaces_walker(self, arguments, directory_name, names):
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
            # prints a debug message
            self.string_normalization_plugin.debug("Removing trail in file: %s" % valid_complete_names_extension)

            # removes the trailing spaces from the file
            self.remove_trailing_spaces_file(valid_complete_names_extension, tab_to_spaces, windows_newline)

            # in case the removal of extra newlines is active
            if trailing_newlines:
                # prints a debug message
                self.string_normalization_plugin.debug("Removing trail newlines in file: %s" % valid_complete_names_extension)

                # removes the extra newlines from the file
                self.remove_trailing_newlines_file(valid_complete_names_extension, windows_newline)
