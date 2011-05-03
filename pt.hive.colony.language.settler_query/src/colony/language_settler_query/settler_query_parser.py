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

import ply.yacc

import settler_query_ast

from settler_query_lexer import * #@UnusedWildImport

# parsing rules
# precedence of operators
precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "GREATER", "GREATEREQUAL", "LESS", "LESSEQUAL", "EQUALEQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "POWER"),
    ("right", "NOT")
)

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
    optional_all_distinct_node = t[2]

    # retrieves the selection node
    selection_node = t[3]

    # retrieves the entity expression node
    entity_expression_node = t[4]

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

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 1:
        # sets the enumeration value as none
        enumeration_value = None
    elif arguments_length == 2:
        # retrieves the enumeration value
        enumeration_value = t[1]

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

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 2:
        # retrieves the scalar expression node
        scalar_expression_node = t[1]

        # sets the next scalar expression commalist node as none
        next_scalar_expression_commalist_node = None
    elif arguments_length == 4:
        # retrieves the scalar expression node
        scalar_expression_node = t[3]

        # retrieves the next scalar expression commalist node
        next_scalar_expression_commalist_node = t[1]

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
                         | atom
                         | field_reference"""

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 2:
        # retrieves the first node
        first_node = t[1]

        if first_node.__class__ == settler_query_ast.AtomNode:
            # creates the atom scalar expression node
            scalar_expression_node = settler_query_ast.AtomScalarExpressionNode()

            # sets the atom node in the atom scalar expression node
            scalar_expression_node.set_atom_node(first_node)

        elif first_node.__class__ == settler_query_ast.FieldRefereceNode:
            # creates the field reference scalar expression node
            scalar_expression_node = settler_query_ast.FieldReferenceScalarExpressionNode()

            # sets the field reference node in the field reference scalar expression node
            scalar_expression_node.set_field_reference_node(first_node)

    elif arguments_length == 4:
        pass

    t[0] = scalar_expression_node

def p_atom(t):
    "atom : literal"

    # retrieves the literal node
    literal_node = t[1]

    # creates the atom node
    atom_node = settler_query_ast.AtomNode()

    # sets the literal node in the atom node
    atom_node.set_literal_node(literal_node)

    t[0] = atom_node

def p_literal(t):
    """literal : STRING
               | NUMBER"""

    # retrieves the literal value
    literal_value = t[1]

    if type(literal_value) == types.StringType:
        # creates the string literal node
        literal_node = settler_query_ast.StringLiteralNode()

        # sets the string value in the string literal node
        literal_node.set_string_value(literal_value)
    elif type(literal_value) == types.IntType:
        # creates the integer literal node
        literal_node = settler_query_ast.IntegerLiteralNode()

        # sets the integer value in the integer literal node
        literal_node.set_integer_value(literal_value)

    t[0] = literal_node

def p_field_reference(t):
    """field_reference : NAME
                       | NAME DOT field_reference"""

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 2:
        # retrieves the field reference name
        field_reference_name = t[1]

        # sets the next filed reference node as none
        next_field_reference_node = None
    elif arguments_length == 4:
        # retrieves the field reference name
        field_reference_name = t[3]

        # retrieves the next field reference node
        next_field_reference_node = t[1]

    # creates the field reference node
    field_reference_node = settler_query_ast.FieldRefereceNode()

    # sets the field reference name in the field reference node
    field_reference_node.set_field_reference_name(field_reference_name)

    # sets the next node in the field reference node
    field_reference_node.set_next_node(next_field_reference_node)

    t[0] = field_reference_node

def p_entity_expression(t):
    "entity_expression : from_clause optional_where_clause"

    # retrieves the from clause node
    from_clause_node = t[1]

    # retrieves the optional where clause node
    optional_where_clause_node = t[2]

    # creates the entity expression node
    entity_expression_node = settler_query_ast.EntityExpressionNode()

    # sets the from clause node in the entity expression node
    entity_expression_node.set_from_clause_node(from_clause_node)

    # sets the optional where clause node in the entity expression node
    entity_expression_node.set_optional_where_clause_node(optional_where_clause_node)

    t[0] = entity_expression_node

def p_from_clause(t):
    "from_clause : FROM entity_reference_commalist"

    # retrieves the entity reference commalist node
    entity_reference_commalist_node = t[2]

    # creates the from clause node
    from_clause_node = settler_query_ast.FromClauseNode()

    # sets the entity reference commalist node in the from clause node
    from_clause_node.set_entity_reference_commalist_node(entity_reference_commalist_node)

    t[0] = from_clause_node

def p_entity_reference_commalist(t):
    """entity_reference_commalist : entity_reference
                                  | entity_reference_commalist COMA entity_reference"""

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 2:
        # retrieves the entity reference node
        entity_reference_node = t[1]

        # sets the next entity reference commalist node as none
        next_entity_reference_commalist_node = None
    elif arguments_length == 4:
        # retrieves the entity reference node
        entity_reference_node = t[3]

        # retrieves the next entity reference commalist node
        next_entity_reference_commalist_node = t[1]

    # creates the entity reference commalist node
    entity_reference_commalist_node = settler_query_ast.EntityReferenceCommalistNode()

    # sets the entity reference node in the entity reference commalist node
    entity_reference_commalist_node.set_entity_reference_node(entity_reference_node)

    # sets the next node in the entity reference commalist node
    entity_reference_commalist_node.set_next_node(next_entity_reference_commalist_node)

    t[0] = entity_reference_commalist_node

def p_entity_reference(t):
    "entity_reference : entity"

    # retrieves the entity node
    entity_node = t[1]

    # creates the entity reference node
    entity_reference_node = settler_query_ast.EntityReferenceNode()

    # sets the entity node in the entity reference node
    entity_reference_node.set_entity_node(entity_node)

    t[0] = entity_reference_node

def p_entity(t):
    """entity : qualified_entity_name
              | qualified_entity_name AS NAME"""

    # retrieves the qualified entity name node
    qualified_entity_name_node = t[1]

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 2:
        # creates the entity node
        entity_node = settler_query_ast.EntityNode()
    elif arguments_length == 4:
        # retrieves the entity as name value
        entity_as_name_value = t[3]

        # creates the entity node
        entity_node = settler_query_ast.EntityAsNameNode()

        # sets the entity as name value in the entity as name node
        entity_node.set_entity_as_name_value(entity_as_name_value)

    # sets the qualified entity name node in the entity node
    entity_node.set_qualified_entity_name_node(qualified_entity_name_node)

    t[0] = entity_node

def p_qualified_entity_name(t):
    "qualified_entity_name : NAME"

    # retrieves the qualified entity name value
    qualified_entity_name_value = t[1]

    # creates the qualified entity name node
    qualified_entity_name_node = settler_query_ast.QualifiedEntityNameNode()

    # sets the qualified entity name value in the qualified entity name node
    qualified_entity_name_node.set_qualified_entity_name_value(qualified_entity_name_value)

    t[0] = qualified_entity_name_node

def p_optional_where_clause(t):
    """optional_where_clause :
                             | where_clause"""

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 1:
        # sets the where clause node as none
        where_clause_node = None
    elif arguments_length == 2:
        # retrieves the where clause node
        where_clause_node = t[1]

    # creates the optional where clause node
    optional_where_clause_node = settler_query_ast.OptionalWhereClauseNode()

    # sets the where clause node in the optional where clause node
    optional_where_clause_node.set_where_clause_node(where_clause_node)

    t[0] = optional_where_clause_node

def p_where_clause(t):
    "where_clause : WHERE search_condition"

    # retrieves the search condition node
    search_condition_node = t[2]

    # creates the where clause node
    where_clause_node = settler_query_ast.WhereClauseNode()

    # sets the search condition node in the where clause node
    where_clause_node.set_search_condition_node(search_condition_node)

    t[0] = where_clause_node

def p_search_condition(t):
    """search_condition :
                        | predicate
                        | NOT search_condition
                        | search_condition AND search_condition
                        | search_condition OR search_condition
                        | LPAREN search_condition RPAREN"""

    # retrieves the arguments length
    arguments_length = len(t)

    if arguments_length == 1:
        # creates the search condition node
        search_condition_node = settler_query_ast.SearchConditionNode()
    elif arguments_length == 2:
        # retrieves the predicate node
        predicate_node = t[1]

        # creates the predicate search condition node
        search_condition_node = settler_query_ast.PredicateSearchConditionNode()

        # sets the predicate node in the predicate search condition node
        search_condition_node.set_predicate_node(predicate_node)
    elif arguments_length == 3:
        # retrieves the not expression search condition node
        not_expression_search_condition_node = t[2]

        # creates the not expression search condition node
        search_condition_node = settler_query_ast.NotExpressionSearchConditionNode()

        # sets the expression search condition node in the not expression search condition node
        search_condition_node.set_expression_search_condition_node(not_expression_search_condition_node)
    elif arguments_length == 4:
        if t[2] == "and" or t[2] == "or":
            # retrieves the first expression search condition node
            first_expression_search_condition_node = t[1]

            # retrieves the second expression search condition node
            second_expression_search_condition_node = t[3]

            if t[2] == "and":
                # creates the and expression search condition node
                search_condition_node = settler_query_ast.AndExpressionSearchConditionNode()
            elif t[2] == "or":
                # creates the or expression search condition node
                search_condition_node = settler_query_ast.OrExpressionSearchConditionNode()

            # sets the first expression search condition node in the search condition node
            search_condition_node.set_first_expression_search_condition_node(first_expression_search_condition_node)

            # sets the second expression search condition node in the search condition node
            search_condition_node.set_second_expression_search_condition_node(second_expression_search_condition_node)
        elif t[1] == "(" and t[3] == ")":
            # retrieves the parenthesis expression search condition node
            parenthesis_expression_search_condition_node = t[2]

            # creates the parenthesis expression search condition node
            search_condition_node = settler_query_ast.ParenthesisExpressionSearchConditionNode()

            # sets the expression search condition node in the parenthesis expression search condition node
            search_condition_node.set_expression_search_condition_node(parenthesis_expression_search_condition_node)

    t[0] = search_condition_node

def p_predicate(t):
    """predicate : comparison_predicate
                 | between_predicate
                 | like_predicate
                 | test_for_null
                 | in_predicate
                 | in_subquery_predicate
                 | all_or_any_predicate
                 | existence_test
                 | scalar_expression_predicate"""

    t[0] = t[1]

def p_comparison_predicate(t):
    """comparison_predicate : scalar_expression EQUALS scalar_expression
                            | scalar_expression GREATER scalar_expression
                            | scalar_expression GREATEREQUAL scalar_expression
                            | scalar_expression LESS scalar_expression
                            | scalar_expression LESSEQUAL scalar_expression"""

    if t[2] == "<" or t[2] == "<=":
        # retrieves the first scalar expression node
        first_scalar_expression_node = t[3]

        # retrieves the second scalar expression node
        second_scalar_expression_node = t[1]
    else:
        # retrieves the first scalar expression node
        first_scalar_expression_node = t[1]

        # retrieves the second scalar expression node
        second_scalar_expression_node = t[3]

    if t[2] == "=":
        # creates the equals comparison predicate node
        comparison_predicate_node = settler_query_ast.EqualComparisonPredicateNode()
    elif t[2] == ">" or t[2] == "<":
        # creates the greater comparison predicate node
        comparison_predicate_node = settler_query_ast.GreaterComparisonPredicateNode()
    elif t[2] == ">=" or t[2] == "<=":
        # creates the greater equals comparison predicate node
        comparison_predicate_node = settler_query_ast.GreaterEqualComparisonPredicateNode()

    # sets the first scalar expression node in the comparison predicate node
    comparison_predicate_node.set_first_scalar_expression_node(first_scalar_expression_node)

    # sets the second scalar expression node in the comparison predicate node
    comparison_predicate_node.set_second_scalar_expression_node(second_scalar_expression_node)

    t[0] = comparison_predicate_node

def p_between_predicate(t):
    """between_predicate : scalar_expression BETWEEN scalar_expression
                         | scalar_expression NOT BETWEEN scalar_expression """

    # retrieves the first scalar expression node
    first_scalar_expression_node = t[1]

    if t[2] == "between":
        # retrieves the second scalar expression node
        second_scalar_expression_node = t[3]

        # creates the between predicate node
        between_predicate_node = settler_query_ast.BetweenPredicateNode()
    elif t[2] == "not":
        # retrieves the second scalar expression node
        second_scalar_expression_node = t[4]

        # creates the not between predicate node
        between_predicate_node = settler_query_ast.NotBetweenPredicateNode()

    # sets the first scalar expression node in the between predicate node
    between_predicate_node.set_first_scalar_expression_node(first_scalar_expression_node)

    # sets the second scalar expression node in the between predicate node
    between_predicate_node.set_second_scalar_expression_node(second_scalar_expression_node)

    t[0] = between_predicate_node

def p_like_predicate(t):
    """like_predicate : scalar_expression LIKE scalar_expression
                      | scalar_expression NOT LIKE scalar_expression"""

    # retrieves the first scalar expression node
    first_scalar_expression_node = t[1]

    if t[2] == "like":
        # retrieves the second scalar expression node
        second_scalar_expression_node = t[3]

        # creates the like predicate node
        like_predicate_node = settler_query_ast.LikePredicateNode()
    elif t[2] == "not":
        # retrieves the second scalar expression node
        second_scalar_expression_node = t[4]

        # creates the not like predicate node
        like_predicate_node = settler_query_ast.NotLikePredicateNode()

    # sets the first scalar expression node in the like predicate node
    like_predicate_node.set_first_scalar_expression_node(first_scalar_expression_node)

    # sets the second scalar expression node in the like predicate node
    like_predicate_node.set_second_scalar_expression_node(second_scalar_expression_node)

    t[0] = like_predicate_node

def p_test_for_null(t):
    """test_for_null : scalar_expression IS NULL
                     | scalar_expression IS NOT NULL"""

    # retrieves the scalar expression node
    scalar_expression_node = t[1]

    if t[3] == "null":
        # creates the is null predicate node
        test_for_null_node = settler_query_ast.IsNullPredicateNode()
    elif t[3] == "not":
        # creates the is not null predicate node
        test_for_null_node = settler_query_ast.IsNotNullPredicateNode()

    # sets the scalar expression node in the test for null node
    test_for_null_node.set_scalar_expression_node(scalar_expression_node)

    t[0] = test_for_null_node

def p_in_predicate(t):
    """in_predicate : scalar_expression IN LPAREN scalar_expression_commalist RPAREN
                    | scalar_expression NOT IN LPAREN scalar_expression_commalist RPAREN"""

    # retrieves the scalar expression node
    scalar_expression_node = t[1]

    if t[2] == "in":
        # retrieves the scalar expression commalist node
        scalar_expression_commalist_node = t[4]

        # creates the in predicate node
        in_predicate_node = settler_query_ast.InPredicateNode()
    elif t[2] == "not":
        # retrieves the scalar expression commalist node
        scalar_expression_commalist_node = t[5]

        # creates the not in predicate node
        in_predicate_node = settler_query_ast.NotInPredicateNode()

    # sets the scalar expression node in the in predicate node
    in_predicate_node.set_scalar_expression_node(scalar_expression_node)

    t[0] = in_predicate_node

def p_in_subquery_predicate(t):
    """in_subquery_predicate : scalar_expression IN subquery
                             | scalar_expression NOT IN subquery"""

    # retrieves the scalar expression node
    scalar_expression_node = t[1]

    if t[2] == "in":
        # retrieves the subquery node
        scalar_expression_commalist_node = t[3]

        # creates the in subquery predicate node
        in_subquery_predicate_node = settler_query_ast.InSubqueryPredicateNode()
    elif t[2] == "not":
        # retrieves the subquery node
        scalar_expression_commalist_node = t[4]

        # creates the not in subquery predicate node
        in_subquery_predicate_node = settler_query_ast.NotInSubqueryPredicateNode()

    # sets the scalar expression node in the in predicate node
    in_subquery_predicate_node.set_scalar_expression_node(scalar_expression_node)

    t[0] = in_subquery_predicate_node

def p_all_or_any_predicate(t):
    "all_or_any_predicate : scalar_expression EQUALS any_all_some subquery"

    # retrieves the scalar expression node
    scalar_expression_node = t[1]

    # retrieves the any all some node
    any_all_some_node = t[3]

    # retrieves the subquery node
    subquery_node = t[4]

    # creates the all or any predicate node
    all_or_any_predicate_node = settler_query_ast.AllOrAnyPredicateNode()

    # sets the scalar expression node in the all or any predicate node
    all_or_any_predicate_node.set_scalar_expression_node(scalar_expression_node)

    # sets the any all some node in the all or any predicate node
    all_or_any_predicate_node.set_any_all_some_node(any_all_some_node)

    # sets the subquery node in the all or any predicate node
    all_or_any_predicate_node.set_subquery_node(subquery_node)

    t[0] = all_or_any_predicate_node

def p_any_all_some(t):
    """any_all_some : ANY
                    | ALL
                    | SOME"""

    # retrieves the any all some value
    any_all_some_value = t[1]

    # creates the any all some node
    any_all_some_node = settler_query_ast.AnyAllSomeNode()

    # sets the any all some value in the any all some node
    any_all_some_node.set_any_all_some_value(any_all_some_value)

    t[0] = any_all_some_node

def p_existence_test(t):
    "existence_test : EXISTS subquery"

    # retrieves the subquery node
    subquery_node = t[2]

    # creates the existence test node
    existence_test_node = settler_query_ast.ExistenceTestNode()

    # sets the subquery node in the existence test node
    existence_test_node.set_subquery_node(subquery_node)

    t[0] = existence_test_node

def p_scalar_expression_predicate(t):
    "scalar_expression_predicate : scalar_expression"

    # retrieves the scalar expression node
    scalar_expression_node = t[1]

    # creates the scalar expression predicate node
    scalar_expression_predicate_node = settler_query_ast.ScalarExpressionPredicateNode()

    # sets the scalar expression node in the scalar expression predicate node
    scalar_expression_predicate_node.set_scalar_expression_node(scalar_expression_node)

    t[0] = scalar_expression_predicate_node

def p_subquery(t):
    "subquery : LPAREN SELECT optional_all_distinct selection entity_expression RPAREN"

    # retrieves the optional all distinct node
    optional_all_distinct_node = t[3]

    # retrieves the selection node
    selection_node = t[4]

    # retrieves the entity expression node
    entity_expression_node = t[5]

    # creates the subquery node
    subquery_node = settler_query_ast.SubqueryNode()

    # sets the optional all distinct node in the subquery node
    subquery_node.set_optional_all_distinct_node(optional_all_distinct_node)

    # sets the selection node in the subquery node
    subquery_node.set_selection_node(selection_node)

    # sets the entity expression node in the subquery node
    subquery_node.set_entity_expression_node(entity_expression_node)

    t[0] = subquery_node

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

# creates the parser
ply.yacc.yacc()

# sets the settler parser
parser = ply.yacc
