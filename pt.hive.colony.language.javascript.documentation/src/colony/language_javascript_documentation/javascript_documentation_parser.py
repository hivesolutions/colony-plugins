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

import javascript_documentation_ast

from javascript_documentation_lexer import *

COLONY_PARSER_VALUE = "colony"
""" The colony parser value """

PLY_PARSER_VALUE = "ply"
""" The ply parser value """

PARSER_TYPE = PLY_PARSER_VALUE
""" The parser type """

COLONY_GENERATOR_PATH = "../../../../pt.hive.colony.language.generator/src/colony"
""" The colony generator path """

def p_program(t):
    "program : statements"

    # retrieves the statements node
    statements_node = t[1]

    # creates the program node
    program_node = javascript_documentation_ast.ProgramNode()

    # sets the statements node in the program node
    program_node.set_statements_node(statements_node)

    t[0] = program_node

def p_statements_multiple(t):
    "statements : statement SEMICOLON statements"

    # retrieves the statement node
    statement_node = t[1]

    # retrieves the next statements node
    next_statements_node = t[3]

    # creates the statements node
    statements_node = javascript_documentation_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(next_statements_node)

    t[0] = statements_node

def p_statements_multiple_newline(t):
    "statements : statement NEWLINE statements"

    # retrieves the statement node
    statement_node = t[1]

    # retrieves the next statements node
    next_statements_node = t[3]

    # creates the statements node
    statements_node = javascript_documentation_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(next_statements_node)

    t[0] = statements_node

def p_statements_single(t):
    "statements : statement SEMICOLON"

    # retrieves the statement node
    statement_node = t[1]

    # creates the statements node
    statements_node = javascript_documentation_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(None)

    t[0] = statements_node

def p_statements_single_newline(t):
    "statements : statement NEWLINE"

    # retrieves the statement node
    statement_node = t[1]

    # creates the statements node
    statements_node = javascript_documentation_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(None)

    t[0] = statements_node

def p_statement_comment(t):
    "statement : COMMENT NEWLINE statement"

    # retrieves the comment value
    comment_value = t[1]

    # retrieves the statement node
    statement_node = t[3]

    # creates the comment node
    comment_node = javascript_documentation_ast.CommentNode()

    # sets the comment value in the comment node
    comment_node.set_comment_value(comment_value)

    # sets the statement node in the comment node
    comment_node.set_statement_node(statement_node)

    t[0] = comment_node

def p_statement_space(t):
    "statement : space"

    # retrieves the space node
    space_node = t[1]

    t[0] = space_node

def p_statement_function(t):
    "statement : function"

    # retrieves the function node
    function_node = t[1]

    t[0] = function_node

def p_statement_assign(t):
    "statement : name_reference EQUALS expression"

    # retrieves the name reference node
    name_reference_node = t[1]

    # retrieves the expression node
    expression_node = t[3]

    # creates the assign node
    assign_node = javascript_documentation_ast.AssignNode()

    # sets the expression node in the assign node
    assign_node.set_expression_node(expression_node)

    # sets the name reference node in the assign node
    assign_node.set_name_reference_node(name_reference_node)

    t[0] = assign_node

def p_expression_number(t):
    "expression : NUMBER"

    # retrieves the number value
    number_value = t[1]

    # creates the integer number value
    integer_number_value = int(number_value)

    # creates the integer expression node
    integer_expression_node = javascript_documentation_ast.IntegerExpressionNode()

    # sets the integer expression node integer value
    integer_expression_node.set_integer_value(integer_number_value)

    t[0] = integer_expression_node

def p_name_reference_multiple(t):
    "name_reference : NAME DOT name_reference"

    # retrieves the name reference value
    name_reference_value = t[1]

    # retrieves the next name reference node
    next_name_reference_node = t[3]

    # creates the name reference node
    name_reference_node = javascript_documentation_ast.NameReferenceNode()

    # sets the name reference in the name reference node
    name_reference_node.set_name_reference(name_reference_value)

    # sets the next node in the name reference node
    name_reference_node.set_next_node(next_name_reference_node)

    t[0] = name_reference_node

def p_name_reference_single(t):
    "name_reference : NAME"

    # retrieves the name reference value
    name_reference_value = t[1]

    # creates the name reference node
    name_reference_node = javascript_documentation_ast.NameReferenceNode()

    # sets the name reference in the name reference node
    name_reference_node.set_name_reference(name_reference_value)

    # sets the next node in the name reference node
    name_reference_node.set_next_node(None)

    t[0] = name_reference_node

def p_expression_function(t):
    "function : FUNCTION NAME LPAREN arguments RPAREN LBRACE statements RBRACE"

    # retrieves the function operators node
    function_operators_node = javascript_documentation_ast.AstSequenceEndNode()

    # retrieves the function name value
    function_name_value = t[2]

    # retrieves the function arguments node
    function_arguments_node = t[4]

    # retrieves the statements node
    statements_node = t[7]

    # creates the function node
    function_node = javascript_documentation_ast.FunctionNode()

    # sets the function operators node in the function node
    function_node.set_function_operators_node(function_operators_node)

    # sets the function name in the function node
    function_node.set_function_name(function_name_value)

    # sets the arguments node in the function node
    function_node.set_function_arguments_node(function_arguments_node)

    # sets the statements node in the function node
    function_node.set_statements_node(statements_node)

    t[0] = function_node

def p_arguments_multiple(t):
    "arguments : argument COMA arguments"

    # retrieves the argument node
    argument_node = t[1]

    # retrieves the next arguments node
    next_arguments_node = t[3]

    # creates the arguments node
    arguments_node = javascript_documentation_ast.ArgumentsNode()

    # sets the argument node in the arguments node
    arguments_node.set_argument_node(argument_node)

    # sets the next node in the arguments node
    arguments_node.set_next_node(next_arguments_node)

    t[0] = arguments_node

def p_arguments_single(t):
    "arguments : argument"

    # retrieves the argument node
    argument_node = t[1]

    # creates the arguments node
    arguments_node = javascript_documentation_ast.ArgumentsNode()

    # sets the argument node in the arguments node
    arguments_node.set_argument_node(argument_node)

    # sets the next node in the arguments node
    arguments_node.set_next_node(None)

    t[0] = arguments_node

def p_arguments_null(t):
    "arguments : "

    # creates the ast sequence end node
    ast_sequence_end_node = javascript_documentation_ast.AstSequenceEndNode()

    t[0] = ast_sequence_end_node

def p_argument_simple(t):
    "argument : NAME"

    # retrieves the name value
    name_value = t[1]

    # creates the argument node
    argument_node = javascript_documentation_ast.ArgumentNode()

    # sets the name in the argument node
    argument_node.set_name(name_value)

    t[0] = argument_node

def p_space(t):
    "space : "

    # creates the space node
    space_node = javascript_documentation_ast.SpaceNode()

    t[0] = space_node

def p_error(t):
    print "Syntax error at '%s'" % t

class DummyParser:
    """
    The dummy parser class.
    """

    def parse(self, value):
        """
        The dummy parser method.

        @type value: String
        @param value: The value to be parsed.
        """

        pass

# creates the dummy parser
parser = DummyParser()

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
