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

import ply.yacc

import settler_query_ast

from settler_query_lexer import *

# parsing rules
# precedence of operators
precedence = (("left", "OR"),
              ("left", "AND"),
              ("left", "GREATER", "GREATEREQUAL", "LESS", "LESSEQUAL", "EQUALEQUAL"),
              ("left", "PLUS", "MINUS"),
              ("left", "TIMES", "DIVIDE", "POWER"),)

def p_program(t):
    "program : statements"

    # retrieves the statements node
    statements_node = t[1]

    # creates the program node
    program_node = settler_query_ast.ProgramNode()

    # sets the statements node in the program node
    program_node.set_statements_node(statements_node)

    t[0] = program_node

def p_statements_multiple(t):
    "statements : statement NEWLINE statements"

    # retrieves the statement node
    statement_node = t[1]

    # retrieves the next statements node
    next_statements_node = t[3]

    # creates the statements node
    statements_node = settler_query_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(next_statements_node)

    t[0] = statements_node

def p_statements_single(t):
    "statements : statement NEWLINE"

    # retrieves the statement node
    statement_node = t[1]

    # creates the statements node
    statements_node = settler_query_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(None)

    t[0] = statements_node

def p_statement_pass(t):
    "statement : PASS"

    # creates the pass node
    pass_node = settler_query_ast.PassNode()

    t[0] = pass_node

def p_statement_select(t):
    "statement : SELECT"

    # creates the select node
    select_node = settler_query_ast.SelectNode()

    t[0] = select_node

# creates the parser
ply.yacc.yacc()

# sets the settler parser
parser = ply.yacc
