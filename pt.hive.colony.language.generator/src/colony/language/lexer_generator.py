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

import re
import types
import copy

import lexer_generator_exceptions

class Token:
    """
    The token class.
    """

    type = None
    """ The type of the token"""

    value = None
    """ The value of the token """

    start_index = None
    """ The start index of the token """

    end_index = None
    """ The end index of the token """

    lexer = None
    """ The token lexer """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def __repr__(self):
        """
        Returns the default representation of the class.

        @rtype: String
        @return: The default representation of the class.
        """

        return "<%s, %s, %i, %i>" % (
            self.type,
            self.value,
            self.start_index,
            self.end_index
        )

class LexerGenerator:
    """
    The lexer class.
    """

    LEXER_PREFIX = "t_"
    """ The lexer prefix value """

    ERROR_TOKEN_VALUE = "t_error"
    """ The error token value """

    strings_list = []
    """ The strings list """

    string_regex_list = []
    """ The string regex list """

    string_name_list = []
    """ The string name list """

    functions_list = []
    """ The functions list """

    function_regex_list = []
    """ The function regex list """

    function_name_list = []
    """ The function name list """

    buffer = "none"
    """ The buffer value """

    words = []
    """ The words to be used """

    current_index = 0;
    """ The current index of the lexer """

    error_function = None
    """ The error function """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.strings_list = []
        self.string_regex_list = []
        self.string_name_list = []
        self.functions_list = []
        self.function_regex_list = []
        self.function_name_list = []

    def construct(self, scope):
        """
        Constructs the lexer for the given scope.

        @type scope: Map
        @param scope: The scope to be used in the lexer construction.
        """

        # retrieves the local values copy
        locals = copy.copy(scope)

        # iterates over all the locals
        for local in locals:
            # retrieves the local value
            local_value = locals[local]

            # retrieves the local type
            local_type = type(local_value)

            # retrieves the local prefix
            local_prefix = local[0:2]

            # in case the type of the local is string
            if local_type is types.StringType and local_prefix == LexerGenerator.LEXER_PREFIX:
                # adds the local value to the strings list
                self.strings_list.append(local_value)

                self.string_name_list.append(local.split("_")[1])

            # in case the type of the local is function
            elif local_type is types.FunctionType and local_prefix == LexerGenerator.LEXER_PREFIX:
                # in case the local has the error function value
                if local == LexerGenerator.ERROR_TOKEN_VALUE:
                    # sets the error function
                    self.error_function = local_value
                else:
                    # adds the local value to the functions list
                    self.functions_list.append(local_value)

                    # adds the function name to the function name list
                    self.function_name_list.append(local.split("_")[1])

        # iterates over all the string in the string list
        for string in self.strings_list:
            # compiles the string doc to retrieve the regex
            string_regex = re.compile(string)

            # appends the string regex to the string regex list
            self.string_regex_list.append(string_regex)

        # iterates over all the functions in the function list
        for function in self.functions_list:
            # retrieves the function doc
            function_doc = function.__doc__

            # compiles the function doc to retrieve the regex
            function_regex = re.compile(function_doc)

            # appends the function regex to the function regex list
            self.function_regex_list.append(function_regex)

    def get_token(self):
        """
        Retrieves a token from the lexer.

        @rtype: Token
        @return: The token that has been retrieved.
        """

        # creates a new token
        token = Token()

        # loop while the index is valid
        while self.current_index < len(self.buffer):
            if self.buffer[self.current_index] == "":
                continue

            for string_regex, string_name in zip(self.string_regex_list, self.string_name_list):
                # tries to match the buffer with the string regex
                buffer_match = string_regex.match(self.buffer, self.current_index)

                # in case there was a buffer match
                if buffer_match:
                    # sets the token value
                    token.value = buffer_match.group()

                    # sets the token type
                    token.type = string_name

                    # sets the token start index
                    token.start_index = self.current_index

                    # sets the token end index
                    token.end_index = buffer_match.end() - 1

                    # sets the token lexer
                    token.lexer = self

                    # sets the new current index
                    self.current_index = token.end_index + 1

                    # returns the token
                    return token

            for function_regex, function_name, function in zip(self.function_regex_list, self.function_name_list, self.functions_list):
                # tries to match the buffer with the function regex
                buffer_match = function_regex.match(self.buffer, self.current_index)

                # in case there was a buffer match
                if buffer_match:
                    # sets the token value
                    token.value =  buffer_match.group()

                    # sets the token type
                    token.type = function_name

                    # sets the token start index
                    token.start_index = self.current_index

                    # sets the token end index
                    token.end_index = buffer_match.end() - 1

                    # sets the token lexer
                    token.lexer = self

                    # calls the function with the token
                    function(token)

                    # sets the new current index
                    self.current_index = token.end_index + 1

                    # returns the token
                    return token

            # sets the token value
            token.value = self.buffer[self.current_index:]

            # sets the token type
            token.type = "error"

            # sets the token start index
            token.start_index = self.current_index

            # sets the token end index
            token.end_index = self.current_index

            # sets the token lexer
            token.lexer = self

            # in case an error function is defined
            if self.error_function:
                # calls the error function
                self.error_function(token)
            else:
                # raises the invalid token exception
                raise lexer_generator_exceptions.InvalidToken("not scanned %s" % str(token))

        # in case no valid token was found
        return None

    def skip(self, skip_size = 1):
        """
        Skips the given size in the buffer.

        @type skip_size: int
        @param skip_size: The size of the skip.
        """

        # sets the new current index
        self.current_index += skip_size

    def split_all(self):
        """
        Splits the current buffer into words.
        """

        self.words = self.buffer.split()

    def get_buffer(self):
        """
        Retrieves the buffer.

        @rtype: String
        @return: The buffer.
        """

        return self.buffer

    def set_buffer(self, buffer):
        """
        Sets the buffer.

        @type buffer: String
        @param buffer: The buffer.
        """

        self.buffer = buffer
