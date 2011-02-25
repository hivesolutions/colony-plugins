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

import types
import unittest

import colony.libs.test_util

import lexer_generator
import parser_generator
import parser_generator_exceptions

import examples.bug_example
import examples.extra_example
import examples.look_ahead_example
import examples.reduce_reduce_example
import examples.shift_reduce_example
import examples.simple_example
import examples.ultra_simple_example

class TestParser(colony.libs.test_util.ColonyTestCase):
    """
    The test parser class.
    """

    def testLR0(self):
        """
        Tests using the LR0 parser generator.
        """

        # retrieves the example
        example = self.get_example()

        # in case no example is defined
        if not example:
            # returns immediately
            return

        # creates a new lexer generator
        self.lexer_generator = lexer_generator.LexerGenerator()

        # creates a new parser generator
        self.parser_generator = parser_generator.ParserGenerator(parser_generator.ParserGenerator.LR0_PARSER_TYPE)

        # sets the lexer in the parser
        self.parser_generator.set_lexer(self.lexer_generator)

        # constructs the parser
        self.parser_generator.construct(example)

        # calls the parser methods
        self.call_parser_methods()

    def testLR1(self):
        """
        Tests using the LR1 parser generator.
        """

        # retrieves the example
        example = self.get_example()

        # in case no example is defined
        if not example:
            # returns immediately
            return

        # creates a new lexer generator
        self.lexer_generator = lexer_generator.LexerGenerator()

        # creates a new parser generator
        self.parser_generator = parser_generator.ParserGenerator(parser_generator.ParserGenerator.LR1_PARSER_TYPE)

        # sets the lexer in the parser
        self.parser_generator.set_lexer(self.lexer_generator)

        # constructs the parser
        self.parser_generator.construct(example)

        # calls the parser methods
        self.call_parser_methods()

    def call_parser_methods(self):
        """
        Calls the parser methods.
        """

        # retrieves the instance values
        values = dir(self)

        # iterates over all the values
        for value in values:
            if value[:7] == "parser_":
                # retrieves the instance attribute
                instance_attribute = getattr(self, value)

                # retrieves the instance attribute type
                instance_attribute_type = type(instance_attribute)

                # in case the type of the instance attribute is method
                if instance_attribute_type == types.MethodType:
                    # calls the instance attribute
                    instance_attribute()

    def get_example(self):
        """
        Retrieves the examples module for the current test.

        @rtype: Module
        @return: The examples module for the current test.
        """

        return None

class TestBugExample(TestParser):
    """
    The test bug example class.
    """

    def parser_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("ab")

        # parses the current buffer
        self.parser_generator._parse()

    def get_example(self):
        return examples.bug_example.example

class TestExtraExample(TestParser):
    """
    The test extra example class.
    """

    def parser_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("ab")

        # parses the current buffer
        self.parser_generator._parse()

    def get_example(self):
        return examples.extra_example.example

class TestLookAheadExample(TestParser):
    """
    The test look ahead example class.
    """

    def parser_base_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("aabaab")

        # parses the current buffer
        self.parser_generator._parse()

    def parser_extra_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("abb")

        # parses the current buffer
        self.parser_generator._parse()

    def get_example(self):
        return examples.look_ahead_example.example

class TestReduceReduceExample(TestParser):
    """
    The test reduce reduce example class.
    """

    def testLR0(self):
        self.assertRaises(parser_generator_exceptions.ReduceReduceConflict, TestParser.testLR0, self)

    def testLR1(self):
        self.assertRaises(parser_generator_exceptions.ReduceReduceConflict, TestParser.testLR0, self)

    def get_example(self):
        return examples.reduce_reduce_example.example

class TestShiftReduceExample(TestParser):
    """
    The test shift reduce example class.
    """

    def testLR0(self):
        self.assertRaises(parser_generator_exceptions.ShiftReduceConflict, TestParser.testLR0, self)

    def testLR1(self):
        self.assertRaises(parser_generator_exceptions.ShiftReduceConflict, TestParser.testLR0, self)

    def get_example(self):
        return examples.shift_reduce_example.example

class TestSimpleExample(TestParser):
    """
    The test simple example class.
    """

    def parser_sum_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("1 + 1 + 1")

        # parses the current buffer
        self.parser_generator._parse()

    def parser_subtraction_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("1 - 1 - 1")

        # parses the current buffer
        self.parser_generator._parse()

    def parser_multiplication_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("1 * 1 * 1")

        # parses the current buffer
        self.parser_generator._parse()

    def parser_division_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("1 / 1 / 1")

        # parses the current buffer
        self.parser_generator._parse()

    def parser_mixed_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("1 + 1 - 1 * 1")

        # parses the current buffer
        self.parser_generator._parse()

    def get_example(self):
        return examples.simple_example.example

class TestUltraSimpleExample(TestParser):
    """
    The test ultra simple example class.
    """

    def parser_sum_test(self):
        # sets the buffer in the parser generator
        self.parser_generator.set_buffer("1 + 1 + 1")

        # parses the current buffer
        self.parser_generator._parse()

    def get_example(self):
        return examples.ultra_simple_example.example

if __name__ == "__main__":
    unittest.main()
