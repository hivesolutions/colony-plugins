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

import wiki_ast

from wiki_lexer import *

COLONY_PARSER_VALUE = "colony"
""" The colony parser value """

PLY_PARSER_VALUE = "ply"
""" The ply parser value """

PARSER_TYPE = COLONY_PARSER_VALUE
""" The parser type """

COLONY_GENERATOR_PATH = "../../../../pt.hive.colony.language.generator/src/colony"
""" The colony generator path """

def p_program(t):
    "program : statements"

    # retrieves the statements node
    statements_node = t[1]

    # creates the program node
    program_node = wiki_ast.ProgramNode()

    # sets the statements node in the program node
    program_node.set_statements_node(statements_node)

    t[0] = program_node

def p_statements_multiple(t):
    "statements : statement SPACE statements"

    # retrieves the statement node
    statement_node = t[1]

    # retrieves the next statements node
    next_statements_node = t[3]

    # creates the statements node
    statements_node = wiki_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(next_statements_node)

    t[0] = statements_node

def p_statements_multiple_newline(t):
    "statements : statement NEWLINE statements"

    # retrieves the statement node
    statement_node = t[1]

    # retrieves the newline value
    newline_value = t[2]

    # retrieves the next statements node
    next_statements_node = t[3]

    # creates the statements node
    statements_node = wiki_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # in case the newline value is greater than one
    if newline_value > 1:
        # creates the new line node
        new_line_node = wiki_ast.NewLineNode()

        # creates the statements aux node
        statements_aux_node = wiki_ast.StatementsNode()

        # sets the new line node in the statements aux node
        statements_aux_node.set_statement_node(new_line_node)

        # sets the next node in the statements aux node
        statements_aux_node.set_next_node(next_statements_node)

        # sets the statements aux node in the statements node
        statements_node.set_next_node(statements_aux_node)
    else:
        # sets the next node in the statements node
        statements_node.set_next_node(next_statements_node)

    t[0] = statements_node

def p_statements_single(t):
    "statements : statement"

    # retrieves the statement node
    statement_node = t[1]

    # creates the statements node
    statements_node = wiki_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(None)

    t[0] = statements_node

def p_statement_bolt(t):
    "statement : BOLD statements BOLD"

    # retrieves the statements node
    statements_node = t[2]

    # creates the bold node
    bold_node = wiki_ast.BoldNode()

    # sets the statements node in the bold node
    bold_node.set_statements_node(statements_node)

    t[0] = bold_node

def p_statement_italic(t):
    "statement : ITALIC statements ITALIC"

    # retrieves the statements node
    statements_node = t[2]

    # creates the italic node
    italic_node = wiki_ast.ItalicNode()

    # sets the statements node in the italic node
    italic_node.set_statements_node(statements_node)

    t[0] = italic_node

def p_statement_underline(t):
    "statement : UNDERLINE statements UNDERLINE"

    # retrieves the statements node
    statements_node = t[2]

    # creates the underline node
    underline_node = wiki_ast.UnderlineNode()

    # sets the statements node in the underline node
    underline_node.set_statements_node(statements_node)

    t[0] = underline_node

def p_statement_monospace(t):
    "statement : MONOSPACE statements MONOSPACE"

    # retrieves the statements node
    statements_node = t[2]

    # creates the monospace node
    monospace_node = wiki_ast.MonospaceNode()

    # sets the statements node in the monospace node
    monospace_node.set_statements_node(statements_node)

    t[0] = monospace_node

def p_statement_name(t):
    "statement : NAME"

    # retrieves the name value
    name_value = t[1]

    # creates the name node
    name_node = wiki_ast.NameNode()

    # sets the name value in the name node
    name_node.set_name_value(name_value)

    t[0] = name_node

def p_statement_newline_forced(t):
    "statement : FORCED_NEWLINE"

    # creates the new line node
    new_line_node = wiki_ast.NewLineNode()

    # sets the forced in the new line node
    new_line_node.set_forced(True)

    t[0] = new_line_node

# in case it's the colony parser type
if PARSER_TYPE == COLONY_PARSER_VALUE:
    # imports the sys package
    import sys

    # appends the colony language generator path
    sys.path.append(COLONY_GENERATOR_PATH)

    # imports the colony generator package
    import language_generator.parser_generator

    # creates a new parser generator
    parser_generator = language_generator.parser_generator.ParserGenerator(language_generator.parser_generator.ParserGenerator.LR0_PARSER_TYPE, True, globals())

    # sets the colony settler parser
    parser = parser_generator
# in case it's the ply parser type
elif PARSER_TYPE == PLY_PARSER_VALUE:
    # imports the ply packages
    import ply.lex
    import ply.yacc

    # creates the lexer
    ply.lex.lex()

    # creates the parser
    ply.yacc.yacc()

    # sets the settler parser
    parser = ply.yacc
