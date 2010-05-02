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

from xml_lexer import *

COLONY_GENERATOR_PATH = "../../../../../pt.hive.colony.language.generator/src/colony"
""" The colony generator path """

# appends the colony language generator path
sys.path.append(COLONY_GENERATOR_PATH)

# imports the colony generator package
import language_generator.lexer_generator

USAGE_MESSAGE = "xml_beautifier input_file_path [output_file_path]"
""" The usage message """

DEFAULT_OUTPUT_FILE_PATH = "out.xml"
""" The default output file path """

TAG_INIT_VALUE = "TAG_INIT"
""" The tag init value """

TAG_END_VALUE = "TAG_END"
""" The tag end value """

TAG_SIMPLE_VALUE = "TAG_SIMPLE"
""" The tag simple value """

INDENTATION_TOKEN = "    "
""" The indentation token """

class XmlBeautifier:
    """
    The xml beautifier class.
    """

    input_file_buffer = None
    """ The input file buffer """

    output_file_buffer = None
    """ The output file buffer """

    def __init__(self, input_file_buffer = None, output_file_buffer = None):
        self.input_file_buffer = input_file_buffer
        self.output_file_buffer = output_file_buffer

    def beautify(self):
        """
        Beautifies the contents of the current input file buffer.
        Writes the result to the output buffer.
        """

        # reads the file contents
        xml_file_contents = self.input_file_buffer.read()

        # strips the xml file contents
        xml_file_contents = xml_file_contents.strip()

        # creates a new lexer
        lexer = language_generator.lexer_generator.LexerGenerator()

        # constructs the lexer
        lexer.construct(globals())

        # sets the input in the lexer
        lexer.input(xml_file_contents)

        # retrieves the current token from the lexer
        token = lexer.token()

        # start the indentation index
        indentation_index = 0

        # start the initial flag
        initial_flag = True

        # starts the previous tag value
        previous_tag = None

        # while there is a valid token
        while token:
            # retrieves the token type
            token_type = token.type

            # retrieve the token value
            token_value = token.value

            # in case the current token type is tag init
            if token_type == TAG_INIT_VALUE:
                # writes a newline
                self._write_newline(initial_flag, indentation_index)

                # writes the token value
                self.output_file_buffer.write(token_value)

                # sets the previous tag value
                previous_tag = TAG_INIT_VALUE

                # increments the indentation index
                indentation_index += 1
            # in case the current token type is tag end
            elif token_type == TAG_END_VALUE:
                # decrements the indentation index
                indentation_index -= 1

                # in case the previous tag is a tag end
                if previous_tag == TAG_END_VALUE:
                    # writes a newline
                    self._write_newline(initial_flag, indentation_index)

                # writes the token value
                self.output_file_buffer.write(token_value)

                # sets the previous tag value
                previous_tag = TAG_END_VALUE
            # in case the current token type is tag simple
            elif token_type == TAG_SIMPLE_VALUE:
                # writes the token value
                self.output_file_buffer.write(token_value)

                # sets the previous tag value
                previous_tag = TAG_END_VALUE
            else:
                # writes the token value
                self.output_file_buffer.write(token_value)

            # in case the initial flag is set
            if initial_flag:
                # unsets the initial flag
                initial_flag = False

            # retrieves the token
            token = lexer.token()

    def set_input_file_buffer(self, input_file_buffer):
        """
        Sets the input file buffer.

        @type input_file_buffer: File
        @param input_file_buffer: The input file buffer.
        """

        self.input_file_buffer = input_file_buffer

    def get_input_file_buffer(self):
        """
        Retrieves the input file buffer.

        @rtype: File
        @return: The input file buffer.
        """

        return self.input_file_buffer

    def set_output_file_buffer(self, output_file_buffer):
        """
        Sets the output file buffer.

        @type output_file_buffer: File
        @param output_file_buffer: The output file buffer.
        """

        self.output_file_buffer = output_file_buffer

    def get_output_file_buffer(self):
        """
        Retrieves the output file buffer.

        @rtype: File
        @return: The output file buffer.
        """

        return self.output_file_buffer

    def _write_newline(self, initial_flag, indentation_index):
        """
        Writes a newline for the current xml status.

        @type initial_flag: bool
        @param initial_flag: The flag indicating if it's the initial token.
        @type indentation_index: int
        @param indentation_index: The current indentation index to be used.
        """

        # in case the initial flag is not set
        if not initial_flag:
            self.output_file_buffer.write("\n")

        for _index in range(indentation_index):
            self.output_file_buffer.write(INDENTATION_TOKEN)

if __name__ == "__main__":
    # in case the number of arguments is invalid
    if len(sys.argv) < 2:
        print "Invalid number of arguments"
        print "Usage: " + USAGE_MESSAGE
        sys.exit(2)

    # retrieves the input file path
    input_file_path = sys.argv[1]

    # in case the number of arguments is greater than two
    if len(sys.argv) > 2:
        # retrieves the output file path
        output_file_path = sys.argv[2]
    else:
        # sets the default output file path
        output_file_path = DEFAULT_OUTPUT_FILE_PATH

    # opens the input file
    input_file = open(input_file_path)

    # opens the output file
    output_file = open(output_file_path, "wb+")

    # creates the xml beautifier
    xml_beautifier = XmlBeautifier(input_file, output_file)

    # beautifies the xml
    xml_beautifier.beautify()

    # closes the input file
    input_file.close()

    # closes the output file
    output_file.close()
