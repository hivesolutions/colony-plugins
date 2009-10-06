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

import lexer_generator
import parser_generator

import examples.bug_example
import examples.extra_example
import examples.look_ahead_example
import examples.ply_example
import examples.reduce_reduce_example
import examples.shift_reduce_example
import examples.simple_example
import examples.ultra_simple_example

# sets the current valid example
valid_example = examples.extra_example.example

# creates a new lexer generator
lexer_generator = lexer_generator.LexerGenerator()

# creates a new parser generator
parser_generator = parser_generator.ParserGenerator(parser_generator.ParserGenerator.LR1_PARSER_TYPE)

# sets the lexer in the parser
parser_generator.set_lexer(lexer_generator)

# constructs the parser
parser_generator.construct(valid_example)

# prints the rules string
print parser_generator._get_rules_string()

# prints the item sets string
print parser_generator._get_item_sets_string()

# prints the transition table string
print parser_generator._get_transition_table_string()

# prints the action table string
print parser_generator._get_action_table_string()

# prints the goto table string
print parser_generator._get_goto_table_string()

# sets the buffer in the parser generator
parser_generator.set_buffer("ab")

# parses the current buffer
parser_generator.parse()
