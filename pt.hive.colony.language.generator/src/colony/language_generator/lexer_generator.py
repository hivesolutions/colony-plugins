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
import logging

import logging_configuration
import lexer_generator_exceptions

DEFAULT_COMPILE_FLAGS = re.UNICODE
""" The default compile flags """

# setups the logger
logging_configuration.setup_logging()

class Token:
    """
    The token class.
    """

    type = None
    """ The type of the token"""

    value = None
    """ The value of the token """

    line_number = None
    """ The current line number """

    lineno = None
    """ The current line number (deprecated) """

    start_index = None
    """ The start index of the token """

    end_index = None
    """ The end index of the token """

    lexpos = None
    """ The current lexer position (deprecated) """

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

        return "<%s, '%s', %i, %i>" % (
            self.type,
            self.value,
            self.start_index,
            self.end_index
        )

class LexerGenerator:
    """
    The lexer class.
    """

    GROUPING_REGEX = r"(?<!\\)\((?!\?\:)"
    """ The grouping regular expression """

    GROUPING_SUBSTITUTION_VALUE = "(?:"
    """ The grouping substitution value """

    LEXER_PREFIX = "t_"
    """ The lexer prefix value """

    ERROR_TOKEN_VALUE = "t_error"
    """ The error token value """

    IGNORE_TOKEN_VALUE = "t_ignore"
    """ The ignore token value """

    TOKENS_LIST_VALUE = "tokens"
    """ The tokens list value """

    BASE_TOKENS_LIST = [
        "comment",
        "ignore",
        "error"
    ]
    """ The base tokens list """

    ADVANCE_TOKENS_LIST = [
        "comment"
    ]
    """ The advance tokens list """

    strings_regex = None
    """ The strings regular expression """

    functions_regex = None
    """ The functions regular expression """

    tokens_list = []
    """ The tokens list """

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

    current_index = 0
    """ The current index of the lexer """

    line_number = 0
    """ The current line number """

    lineno = 0
    """ The current line number (deprecated) """

    lexer_position = 0
    """ The current lexer position """

    lexpos = 0
    """ The current lexer position (deprecated) """

    error_function = None
    """ The error function """

    ignore_value = ""
    """ The ignore value """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.tokens_list = []
        self.strings_list = []
        self.string_regex_list = []
        self.string_name_list = []
        self.functions_list = []
        self.function_regex_list = []
        self.function_name_list = []

    def construct(self, scope):
        """
        Constructs the lexer for the given scope.

        @type scope: Dictionary
        @param scope: The scope to be used in the lexer construction.
        """

        # creates the grouping regex
        grouping_regex = re.compile(LexerGenerator.GROUPING_REGEX, DEFAULT_COMPILE_FLAGS)

        # retrieves the local values copy
        locals = copy.copy(scope)

        # in case the tokens list value is defined in locals
        if LexerGenerator.TOKENS_LIST_VALUE in locals:
            # retrieves the local tokens list
            local_tokens_list = locals[LexerGenerator.TOKENS_LIST_VALUE]

            # extends the tokens list with the local tokens list
            self.tokens_list.extend(local_tokens_list)
        else:
            # raises an exception
            raise Exception("Tokens list is not defined")

        # extends the tokens list with the base tokens
        self.tokens_list.extend(LexerGenerator.BASE_TOKENS_LIST)

        # iterates over all the tokens in the tokens list
        for token in self.tokens_list:
            # creates the local value
            local = LexerGenerator.LEXER_PREFIX + token

            # in case the local value is not defined in locals
            if not local in locals:
                # prints the debug message
                logging.debug("Token %s is not defined in locals" % token)

                continue

            # retrieves the local value
            local_value = locals[local]

            # retrieves the local type
            local_type = type(local_value)

            # retrieves the local prefix
            local_prefix = local[0:2]

            # in case the type of the local is string
            if local_type is types.StringType and local_prefix == LexerGenerator.LEXER_PREFIX:
                # in case the local has the ignore string value
                if local == LexerGenerator.IGNORE_TOKEN_VALUE:
                    # sets the ignore value
                    self.ignore_value = local_value
                else:
                    # adds the local value to the strings list
                    self.strings_list.append(local_value)

                    # retrieves the string name
                    string_name = "_".join(local.split("_")[1:])

                    # adds the string name to the string name list
                    self.string_name_list.append(string_name)

            # in case the type of the local is function
            elif local_type is types.FunctionType and local_prefix == LexerGenerator.LEXER_PREFIX:
                # in case the local has the error function value
                if local == LexerGenerator.ERROR_TOKEN_VALUE:
                    # sets the error function
                    self.error_function = local_value
                else:
                    # adds the local value to the functions list
                    self.functions_list.append(local_value)

                    # retrieves the function name
                    function_name = "_".join(local.split("_")[1:])

                    # adds the function name to the function name list
                    self.function_name_list.append(function_name)

        # iterates over all the string in the string list
        for string in self.strings_list:
            # compiles the string doc to retrieve the regex
            string_regex = re.compile(string, DEFAULT_COMPILE_FLAGS)

            # appends the string regex to the string regex list
            self.string_regex_list.append(string_regex)

        # creates the strings regex list
        strings_regex_list = [grouping_regex.sub(LexerGenerator.GROUPING_SUBSTITUTION_VALUE, string) for string in self.strings_list]

        # creates the groups in the strings regex list
        strings_regex_list = ["(" + string_regex + ")" for string_regex in strings_regex_list]

        # creates the strings regex
        self.strings_regex = re.compile("|".join(strings_regex_list), DEFAULT_COMPILE_FLAGS)

        # iterates over all the functions in the function list
        for function in self.functions_list:
            # retrieves the function doc
            function_doc = function.__doc__

            # compiles the function doc to retrieve the regex
            function_regex = re.compile(function_doc, DEFAULT_COMPILE_FLAGS)

            # appends the function regex to the function regex list
            self.function_regex_list.append(function_regex)

        # creates the functions regex list
        functions_regex_list = [grouping_regex.sub(LexerGenerator.GROUPING_SUBSTITUTION_VALUE, function.__doc__) for function in self.functions_list]

        # creates the groups in the functions regex list
        functions_regex_list = ["(" + function_regex + ")" for function_regex in functions_regex_list]

        # creates the function regex
        self.functions_regex = re.compile("|".join(functions_regex_list), DEFAULT_COMPILE_FLAGS)

    def get_token(self):
        """
        Retrieves a token from the lexer.

        @rtype: Token
        @return: The token that has been retrieved.
        """

        # creates a new token
        token = Token()

        # retrieves the buffer length
        buffer_length = len(self.buffer)

        # loop while the index is valid
        while self.current_index < buffer_length:
            # retrieves the current character
            current_character = self.buffer[self.current_index]

            # in case the current character is invalid
            if current_character == "":
                continue

            # in case the current character is to be ignored
            if current_character in self.ignore_value:
                # increments the current index
                self.current_index += 1

                continue

            # tries to match the buffer with the functions regex
            buffer_match = self.functions_regex.match(self.buffer, self.current_index)

            # in case there was a buffer match
            if buffer_match:
                # retrieves the buffer match last index
                buffer_match_last_index = buffer_match.lastindex - 1

                # retrieves the function name
                function_name = self.function_name_list[buffer_match_last_index]

                # retrieves the function
                function = self.functions_list[buffer_match_last_index]

                # sets the token value
                token.value =  buffer_match.group()

                # sets the token type
                token.type = function_name

                # sets the token start index
                token.start_index = self.current_index

                # sets the token end index
                token.end_index = buffer_match.end() - 1

                # sets the lexer position
                token.lexpos = token.start_index

                # sets the lexer line number
                token.lineno = self.line_number

                # sets the token lexer
                token.lexer = self

                # calls the function with the token
                function(token)

                # sets the new current index
                self.current_index = token.end_index + 1

                # updates the line number
                self.line_number = self.lineno

                # updates the lexer position
                self.lexpos = self.current_index

                # in case the token is to be advanced
                if function_name in LexerGenerator.ADVANCE_TOKENS_LIST:
                    continue
                # in case it's a valid token
                else:
                    # returns the token
                    return token

            # tries to match the buffer with the strings regex
            buffer_match = self.strings_regex.match(self.buffer, self.current_index)

            # in case there was a buffer match
            if buffer_match:
                # retrieves the buffer match last index
                buffer_match_last_index = buffer_match.lastindex - 1

                # retrieves the string name
                string_name = self.string_name_list[buffer_match_last_index]

                # sets the token value
                token.value = buffer_match.group()

                # sets the token type
                token.type = string_name

                # sets the token start index
                token.start_index = self.current_index

                # sets the token end index
                token.end_index = buffer_match.end() - 1

                # sets the lexer position
                token.lexpos = token.start_index

                # sets the lexer line number
                token.lineno = self.line_number

                # sets the token lexer
                token.lexer = self

                # sets the new current index
                self.current_index = token.end_index + 1

                # updates the lexer position
                self.lexpos = self.current_index

                # updates the line number
                self.line_number = self.lineno

                # in case the token is to be advanced
                if string_name in LexerGenerator.ADVANCE_TOKENS_LIST:
                    continue
                # in case it's a valid token
                else:
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

            # sets the lexer position
            token.lexpos = self.current_index

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

        # resets the current index
        self._reset_current_index()

    def get_line_number(self):
        """
        Retrieves the current line number.

        @rtype: int
        @return: The current line number.
        """

        return self.line_number

    def set_line_number(self, line_number):
        """
        Sets the current line number.

        @type line_number: String
        @param line_number: The current line number.
        """

        self.line_number = line_number

    def get_error_function(self):
        """
        Retrieves the error function.

        @rtype: Function
        @return: The error function.
        """

        return self.error_function

    def set_error_function(self, error_function):
        """
        Sets the error function.

        @type error_function: Function
        @param error_function: The error function.
        """

        self.error_function = error_function

    def token(self):
        """
        Retrieves a token from the lexer (deprecated).

        @rtype: Token
        @return: The token that has been retrieved.
        """

        return self.get_token()

    def input(self, buffer):
        """
        Sets the buffer (deprecated).

        @type buffer: String
        @param buffer: The buffer.
        """

        self.set_buffer(buffer)

    def _reset_current_index(self):
        """
        Resets the current index.
        """

        self.current_index = 0
