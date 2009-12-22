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

import time
import logging

import lexer_generator
import parser_generator

import examples.simple_example

# creates the initial time
initial_time = time.time()

# sets the current valid example
valid_example = examples.simple_example.example

# creates a new lexer generator
lexer_generator = lexer_generator.LexerGenerator()

# creates a new parser generator
parser_generator = parser_generator.ParserGenerator(parser_generator.ParserGenerator.LR0_PARSER_TYPE)

# sets the lexer in the parser
parser_generator.set_lexer(lexer_generator)

# constructs the parser
parser_generator.construct(valid_example)

# parses the current buffer and retrieves the result
parse_result = parser_generator.parse("1+1")

# creates the final time
final_time = time.time()

# calculates the difference time
difference_time = final_time - initial_time

# print the info message
logging.info("Took: %ss" % str(difference_time))
