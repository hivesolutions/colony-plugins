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
              ("left", "TIMES", "DIVIDE", "POWER"),
              ("right", "NOT"),)

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
    "statement : SELECT optional_all_distinct selection entity_expression"

    # retrieves the optional all distinct node
    optional_all_distinct_node = t[1]

    # retrieves the selection node
    selection_node = t[2]

    # retrieves the entity expression node
    entity_expression_node = t[3]

    # creates the select node
    select_node = settler_query_ast.SelectNode()

    # sets the optional all distinct node in the select node
    select_node.set_optional_all_distinct_node(optional_all_distinct_node)

    # sets the selection node in the select node
    select_node.set_selection_node(selection_node)

    # sets the entity expression node in the select node
    select_node.set_entity_expression_node(entity_expression_node)

    t[0] = select_node

def p_optional_all_distinct(t):
    """optional_all_distinct :
                             | ALL
                             | DISTINCT"""

    if len(t) > 1:
        # retrieves the enumeration value
        enumeration_value = t[1]
    else:
        # sets the enumeration value as none
        enumeration_value = None

    # creates the optional all distinct node
    optional_all_distinct_node = settler_query_ast.OptionalAllDistinctNode()

    # sets the enumeration value in the optional all distinct node
    optional_all_distinct_node.set_enumeration_value(enumeration_value)

    t[0] = optional_all_distinct_node

def p_selection(t):
    "selection : scalar_expression_commalist"

    # retrieves the scalar expression commalist node
    scalar_expression_commalist_node = t[1]

    # creates the selection node
    selection_node = settler_query_ast.SelectionNode()

    # sets the scalar expression commalist node in the selection node
    selection_node.set_scalar_expression_commalist_node(scalar_expression_commalist_node)

    t[0] = selection_node

def p_scalar_expression_commalist(t):
    """scalar_expression_commalist : scalar_expression
                                   | scalar_expression_commalist COMA scalar_expression"""

    if len(t) > 3:
        # retrieves the scalar expression node
        scalar_expression_node = t[3]

        # retrieves the next scalar expression commalist node
        next_scalar_expression_commalist_node = t[1]
    else:
        # retrieves the scalar expression node
        scalar_expression_node = t[1]

        # sets the next scalar expression commalist as none
        next_scalar_expression_commalist_node = None

    # creates the scalar expression commalist node
    scalar_expression_commalist_node = settler_query_ast.ScalarExpressionCommalistNode()

    # sets the scalar expression node in the scalar expression commalist node
    scalar_expression_commalist_node.set_scalar_expression_node(scalar_expression_node)

    # sets the next node in the scalar expression commalist node
    scalar_expression_commalist_node.set_next_node(next_scalar_expression_commalist_node)

    t[0] = scalar_expression_commalist_node

def p_scalar_expression(t):
    """scalar_expression : scalar_expression PLUS scalar_expression
                         | scalar_expression MINUS scalar_expression
                         | atom"""

def p_atom(t):
    "atom : literal"

    t[0] = "none"

def p_literal(t):
    "literal : NAME"

    t[0] = "none"

def p_table_expression(t):
    "entity_expression : from_clause optional_where_clause"

    t[0] = "none"

def p_from_clause(t):
    "from_clause : FROM entity_reference_commalist"

    t[0] = "none"

def p_entity_reference_commalist(t):
    """entity_reference_commalist : entity_reference
                                  | entity_reference_commalist COMA entity_reference"""

    t[0] = "none"

def p_entity_reference(t):
    "entity_reference : entity"

    t[0] = "none"

def p_entity(t):
    """entity : qualified_entity_name
              | qualified_entity_name AS NAME"""

    t[0] = "none"

def p_qualified_entity_name(t):
    "qualified_entity_name : NAME"

    t[0] = "none"

def p_optional_where_clause(t):
    """optional_where_clause : 
                           | where_clause"""

    t[0] = "none"

def p_where_clause(t):
    "where_clause : WHERE search_condition"

    t[0] = "none"

def p_search_condition(t):
    """search_condition :
                        | search_condition OR search_condition
                        | search_condition AND search_condition
                        | NOT search_condition
                        | LPAREN search_condition RPAREN
                        | predicate"""

    t[0] = "none"

def p_predicate(t):
    """predicate : comparison_predicate
                 | between_predicate
                 | like_predicate
                 | test_for_null
                 | in_predicate
                 | all_or_any_predicate
                 | existence_test
                 | scalar_expression_predicate"""

    t[0] = "none"

def p_comparison_predicate(t):
    "comparison_predicate : scalar_expression EQUALS scalar_expression"

    t[0] = "none"

def p_between_predicate(t):
    """between_predicate : scalar_expression BETWEEN scalar_expression
                         | scalar_expression NOT BETWEEN scalar_expression """

    t[0] = "none"

def p_like_predicate(t):
    """like_predicate : scalar_expression LIKE scalar_expression
                      | scalar_expression NOT LIKE scalar_expression"""

    t[0] = "none"

def p_test_for_null(t):
    """test_for_null : scalar_expression IS NULL
                     | scalar_expression IS NOT NULL"""

    t[0] = "none"

def p_in_predicate(t):
    """in_predicate : scalar_expression IN subquery
                    | scalar_expression NOT IN subquery
                    | scalar_expression IN LPAREN scalar_expression_commalist RPAREN
                    | scalar_expression NOT IN LPAREN scalar_expression_commalist RPAREN"""

    t[0] = "none"

def p_all_or_any_predicate(t):
    "all_or_any_predicate : scalar_expression EQUALS any_all_some subquery"

    t[0] = "none"

def p_any_all_some(t):
    """any_all_some : ANY
                     | ALL
                     | SOME"""

    t[0] = "none"

def p_existence_test(t):
    "existence_test : EXISTS subquery"

    t[0] = "none"

def p_scalar_expression_predicate(t):
    "scalar_expression_predicate : scalar_expression"

    t[0] = "none"

def p_subquery(t):
    "subquery : LPAREN SELECT optional_all_distinct selection entity_expression RPAREN"

    t[0] = "none"

# creates the parser
ply.yacc.yacc()

# sets the settler parser
parser = ply.yacc
