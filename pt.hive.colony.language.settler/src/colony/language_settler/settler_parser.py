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

import settler_ast

from settler_lexer import * #@UnusedWildImport

COLONY_PARSER_VALUE = "colony"
""" The colony parser value """

PLY_PARSER_VALUE = "ply"
""" The ply parser value """

PARSER_TYPE = COLONY_PARSER_VALUE
""" The parser type """

COLONY_GENERATOR_PATH = "../../../../pt.hive.colony.language.generator/src/colony"
""" The colony generator path """

# parsing rules
# precedence of operators
precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "GREATER", "GREATEREQUAL", "LESS", "LESSEQUAL", "EQUALEQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "POWER"),
    ("right", "NOT"),
    ("right", "UMINUS")
)

def p_program(t):
    "program : statements"

    # retrieves the statements node
    statements_node = t[1]

    # creates the program node
    program_node = settler_ast.ProgramNode()

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
    statements_node = settler_ast.StatementsNode()

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
    statements_node = settler_ast.StatementsNode()

    # sets the statement node in the statements node
    statements_node.set_statement_node(statement_node)

    # sets the next node in the statements node
    statements_node.set_next_node(None)

    t[0] = statements_node

def p_statement_pass(t):
    "statement : PASS"

    # creates the pass node
    pass_node = settler_ast.PassNode()

    t[0] = pass_node

def p_statement_assign(t):
    "statement : name_reference EQUALS expression"

    # retrieves the name reference node
    name_reference_node = t[1]

    # retrieves the expression node
    expression_node = t[3]

    # creates the assign node
    assign_node = settler_ast.AssignNode()

    # sets the expression node in the assign node
    assign_node.set_expression_node(expression_node)

    # sets the name reference node in the assign node
    assign_node.set_name_reference_node(name_reference_node)

    t[0] = assign_node

def p_statement_if_condition(t):
    "statement : IF expression COLON NEWLINE statements else_condition END"

    # retrieves the expression node
    expression_node = t[2]

    # retrieves the statements node
    statements_node = t[5]

    # retrieves the else condition node
    else_condition_node = t[6]

    # creates the if condition node
    if_condition_node = settler_ast.IfConditionNode()

    # sets the expression node in the if condition node
    if_condition_node.set_expression_node(expression_node)

    # sets the statements node in the if condition node
    if_condition_node.set_statements_node(statements_node)

    # sets the else condition node in the if condition node
    if_condition_node.set_else_condition_node(else_condition_node)

    t[0] = if_condition_node

def p_else_condition(t):
    "else_condition : ELSE COLON NEWLINE statements else_condition"

    # retrieves the statements node
    statements_node = t[4]

    # retrieves the next else condition node
    next_else_condition_node = t[5]

    # creates the else condition node
    else_condition_node = settler_ast.ElseConditionNode()

    # sets the statements node in the else condition node
    else_condition_node.set_statements_node(statements_node)

    # sets the next node in the else condition node
    else_condition_node.set_next_node(next_else_condition_node)

    t[0] = else_condition_node

def p_else_if_condition(t):
    "else_condition : ELIF expression COLON NEWLINE statements else_condition"

    # retrieves the expression node
    expression_node = t[2]

    # retrieves the statements node
    statements_node = t[5]

    # retrieves the next else condition node
    next_else_condition_node = t[6]

    # creates the else if condition node
    else_if_condition_node = settler_ast.ElseIfConditionNode()

    # sets the expression node in the else if condition node
    else_if_condition_node.set_expression_node(expression_node)

    # sets the statements node in the else if condition node
    else_if_condition_node.set_statements_node(statements_node)

    # sets the next node in the else if condition node
    else_if_condition_node.set_next_node(next_else_condition_node)

    t[0] = else_if_condition_node

def p_else_condition_null(t):
    "else_condition : "

    # creates the ast sequence end node
    ast_sequence_end_node = settler_ast.AstSequenceEndNode()

    t[0] = ast_sequence_end_node

def p_statement_while(t):
    "statement : WHILE expression COLON NEWLINE statements END"

    # retrieves the expression node
    expression_node = t[2]

    # retrieves the statements node
    statements_node = t[5]

    # creates the while node
    while_node = settler_ast.WhileNode()

    # sets the expression node in the while node
    while_node.set_expression_node(expression_node)

    # sets the statements node in the while node
    while_node.set_statements_node(statements_node)

    t[0] = while_node

def p_statement_for(t):
    "statement : FOR NAME IN expression COLON NEWLINE statements END"

    # retrieves the item name
    item_name = t[1]

    # retrieves the expression node
    expression_node = t[4]

    # retrieves the statements node
    statements_node = t[7]

    # creates the for node
    for_node = settler_ast.ForNode()

    # sets the item name in the for node
    for_node.set_item_name(item_name)

    # sets the expression node in the for node
    for_node.set_expression_node(expression_node)

    # sets the statements node in the for node
    for_node.set_statements_node(statements_node)

    t[0] = for_node

def p_statement_return(t):
    "statement : RETURN expression"

    # retrieves the expression node
    expression_node = t[2]

    # creates the return node
    return_node = settler_ast.ReturnNode()

    # sets the expression node in the return node
    return_node.set_expression_node(expression_node)

    t[0] = return_node

def p_statement_global(t):
    "statement : GLOBAL NAME"

    # retrieves the name
    name = t[2]

    # creates the global node
    global_node = settler_ast.GlobalNode()

    # sets the name in the global node
    global_node.set_name(name)

    t[0] = global_node

def p_statement_expression(t):
    "statement : expression"

    # retrieves the expression node
    expression_node = t[1]

    t[0] = expression_node

def p_statement_import(t):
    "statement : import"

    # retrieves the import node
    import_node = t[1]

    t[0] = import_node

def p_statement_function(t):
    "statement : function"

    # retrieves the function node
    function_node = t[1]

    t[0] = function_node

def p_statement_class(t):
    "statement : class"

    # retrieves the class node
    class_node = t[1]

    t[0] = class_node

def p_statement_interface(t):
    "statement : interface"

    # retrieves the interface node
    interface_node = t[1]

    t[0] = interface_node

def p_statement_plugin(t):
    "statement : plugin"

    # retrieves the plugin node
    plugin_node = t[1]

    t[0] = plugin_node

def p_statement_capability(t):
    "statement : capability"

    # retrieves the plugin node
    capability_node = t[1]

    t[0] = capability_node

def p_expression_plus(t):
    "expression : expression PLUS expression"

    # validates the expression
    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the summation expression node
    summation_expression_node = settler_ast.SummationExpressionNode()

    # sets the first expression node in the summation expression node
    summation_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the summation expression node
    summation_expression_node.set_second_expression_node(second_expression_node)

    t[0] = summation_expression_node

def p_expression_minus(t):
    "expression : expression MINUS expression"

    # validates the expression
    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the subtraction expression node
    subtraction_expression_node = settler_ast.SubtractionExpressionNode()

    # sets the first expression node in the subtraction expression node
    subtraction_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the subtraction expression node
    subtraction_expression_node.set_second_expression_node(second_expression_node)

    t[0] = subtraction_expression_node

def p_expression_times(t):
    "expression : expression TIMES expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the multiplication expression node
    multiplication_expression_node = settler_ast.MultiplicationExpressionNode()

    # sets the first expression node in the multiplication expression node
    multiplication_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the multiplication expression node
    multiplication_expression_node.set_second_expression_node(second_expression_node)

    t[0] = multiplication_expression_node

def p_expression_divide(t):
    "expression : expression DIVIDE expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the division expression node
    division_expression_node = settler_ast.DivisionExpressionNode()

    # sets the first expression node in the division expression node
    division_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the division expression node
    division_expression_node.set_second_expression_node(second_expression_node)

    t[0] = division_expression_node

def p_expression_power(t):
    "expression : expression POWER expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the power expression node
    power_expression_node = settler_ast.PowerExpressionNode()

    # sets the first expression node in the power expression node
    power_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the power expression node
    power_expression_node.set_second_expression_node(second_expression_node)

    t[0] = power_expression_node

def p_expression_equal(t):
    "expression : expression EQUALEQUAL expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the equal expression node
    equal_expression_node = settler_ast.EqualExpressionNode()

    # sets the first expression node in the equal expression node
    equal_expression_node.set_first_expression_node(second_expression_node)

    # sets the second expression node in the equal expression node
    equal_expression_node.set_second_expression_node(first_expression_node)

    t[0] = equal_expression_node

def p_expression_greater(t):
    "expression : expression GREATER expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the greater expression node
    greater_expression_node = settler_ast.GreaterExpressionNode()

    # sets the first expression node in the greater expression node
    greater_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the greater expression node
    greater_expression_node.set_second_expression_node(second_expression_node)

    t[0] = greater_expression_node

def p_expression_greater_equal(t):
    "expression : expression GREATEREQUAL expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the greater equal expression node
    greater_equal_expression_node = settler_ast.GreaterEqualExpressionNode()

    # sets the first expression node in the greater equal expression node
    greater_equal_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the greater equal expression node
    greater_equal_expression_node.set_second_expression_node(second_expression_node)

    t[0] = greater_equal_expression_node

def p_expression_less(t):
    "expression : expression LESS expression"

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the greater expression node
    greater_expression_node = settler_ast.GreaterExpressionNode()

    # sets the first expression node in the greater expression node
    greater_expression_node.set_first_expression_node(second_expression_node)

    # sets the second expression node in the greater expression node
    greater_expression_node.set_second_expression_node(first_expression_node)

    t[0] = greater_expression_node

def p_expression_less_equal(t):
    "expression : expression LESSEQUAL expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the greater equal expression node
    greater_equal_expression_node = settler_ast.GreaterEqualExpressionNode()

    # sets the first expression node in the greater equal expression node
    greater_equal_expression_node.set_first_expression_node(second_expression_node)

    # sets the second expression node in the greater equal expression node
    greater_equal_expression_node.set_second_expression_node(first_expression_node)

    t[0] = greater_equal_expression_node

def p_expression_and(t):
    "expression : expression AND expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the and expression node
    and_expression_node = settler_ast.AndExpressionNode()

    # sets the first expression node in the and expression node
    and_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the and expression node
    and_expression_node.set_second_expression_node(second_expression_node)

    t[0] = and_expression_node

def p_expression_or(t):
    "expression : expression OR expression"

    if not validate_expression_binary(t):
        return False

    # retrieves the first expression node
    first_expression_node = t[1]

    # retrieves the second expression node
    second_expression_node = t[3]

    # creates the or expression node
    or_expression_node = settler_ast.OrExpressionNode()

    # sets the first expression node in the or expression node
    or_expression_node.set_first_expression_node(first_expression_node)

    # sets the second expression node in the or expression node
    or_expression_node.set_second_expression_node(second_expression_node)

    t[0] = or_expression_node

def p_expression_not(t):
    "expression : NOT expression"

    if not validate_expression_unary(t):
        return False

    # retrieves the expression node
    expression_node = t[2]

    # creates the not expression node
    not_expression_node = settler_ast.NotExpressionNode()

    # sets the expression node in the not expression node
    not_expression_node.set_expression_node(expression_node)

    t[0] = not_expression_node

def p_expression_uminus(t):
    "expression : MINUS expression %prec UMINUS"

    if not validate_expression_unary(t):
        return False

    # retrieves the expression node
    expression_node = t[2]

    # creates the negative expression node
    negative_expression_node = settler_ast.NegativeExpressionNode()

    # sets the expression node in the negative expression node
    negative_expression_node.set_expression_node(expression_node)

    t[0] = negative_expression_node

def p_expression_parenthesis(t):
    "expression : LPAREN expression RPAREN"

    if not validate_expression_unary(t):
        return False

    # retrieves the expression node
    expression_node = t[2]

    # creates the parenthesis expression node
    parenthesis_expression_node = settler_ast.ParenthesisExpressionNode()

    # sets the expression node in the parenthesis expression node
    parenthesis_expression_node.set_expression_node(expression_node)

    t[0] = parenthesis_expression_node

def p_expression_number(t):
    "expression : NUMBER"

    # retrieves the number value
    number_value = t[1]

    # creates the integer number value
    integer_number_value = int(number_value)

    # creates the integer expression node
    integer_expression_node = settler_ast.IntegerExpressionNode()

    # sets the integer expression node integer value
    integer_expression_node.set_integer_value(integer_number_value)

    t[0] = integer_expression_node

def p_expression_string(t):
    "expression : STRING"

    # retrieves the string value
    string_value = t[1]

    # creates the string expression node
    string_expression_node = settler_ast.StringExpressionNode()

    # sets the string expression node name
    string_expression_node.set_string_value(string_value)

    t[0] = string_expression_node

def p_expression_bool(t):
    "expression : BOOL"

    # retrieves the boolean value
    boolean_value = t[1]

    # creates the bool expression node
    bool_expression_node = settler_ast.BoolExpressionNode()

    # sets the bool expression node bool value
    bool_expression_node.set_bool_value(boolean_value)

    t[0] = bool_expression_node

def p_expression_name(t):
    "expression : name_reference"

    # retrieves the name reference node
    name_reference_node = t[1]

    # creates the name expression node
    name_expression_node = settler_ast.NameExpressionNode()

    # sets the name expression node name reference node
    name_expression_node.set_name_reference_node(name_reference_node)

    t[0] = name_expression_node

def p_expression_list(t):
    "expression : LBRACK list_contents RBRACK"

    # retrieves the list contents node
    list_contents_node = t[2]

    # creates the list expression node
    list_expression_node = settler_ast.ListExpressionNode()

    # sets the list contents node in the list expression node
    list_expression_node.set_list_contents_node(list_contents_node)

    t[0] = list_expression_node

def p_list_contents_multiple(t):
    "list_contents : expression COMA list_contents"

    # retrieves the expression node
    expression_node = t[1]

    # retrieves the next list contents node
    next_list_contents_node = t[3]

    # creates the list contents node
    list_contents_node = settler_ast.ListContentsNode()

    # sets the expression node in the list contents node
    list_contents_node.set_expression_node(expression_node)

    # sets the next node in the list contents node
    list_contents_node.set_next_node(next_list_contents_node)

    t[0] = list_contents_node

def p_list_contents_single(t):
    "list_contents : expression"

    # retrieves the expression node
    expression_node = t[1]

    # creates the list contents node
    list_contents_node = settler_ast.ListContentsNode()

    # sets the expression node in the list contents node
    list_contents_node.set_expression_node(expression_node)

    # sets the next node in the list contents node
    list_contents_node.set_next_node(None)

    t[0] = list_contents_node

def p_list_contents_null(t):
    "list_contents : "

    # creates the ast sequence end node
    ast_sequence_end_node = settler_ast.AstSequenceEndNode()

    t[0] = ast_sequence_end_node

def p_name_reference_multiple(t):
    "name_reference : NAME DOT name_reference"

    # retrieves the name reference value
    name_reference_value = t[1]

    # retrieves the next name reference node
    next_name_reference_node = t[3]

    # creates the name reference node
    name_reference_node = settler_ast.NameReferenceNode()

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
    name_reference_node = settler_ast.NameReferenceNode()

    # sets the name reference in the name reference node
    name_reference_node.set_name_reference(name_reference_value)

    # sets the next node in the name reference node
    name_reference_node.set_next_node(None)

    t[0] = name_reference_node

def p_expression_import_multiple(t):
    "import : IMPORT name_reference COMA import"

    # retrieves the import name reference node
    import_name_reference_node = t[2]

    # retrieves the next import node
    next_import_node = t[4]

    # creates the import node
    import_node = settler_ast.ImportNode()

    # sets the import name reference node in the import node
    import_node.set_import_name_reference_node(import_name_reference_node)

    # sets the next node in the import node
    import_node.set_next_node(next_import_node)

    t[0] = import_node

def p_expression_import_single(t):
    "import : IMPORT name_reference"

    # retrieves the import name reference node
    import_name_reference_node = t[2]

    # creates the import node
    import_node = settler_ast.ImportNode()

    # sets the import name reference node in the import node
    import_node.set_import_name_reference_node(import_name_reference_node)

    # sets the next node in the import node
    import_node.set_next_node(None)

    t[0] = import_node

def p_expression_function(t):
    "function : FUNCTION NAME LPAREN arguments RPAREN COLON NEWLINE statements END"

    # retrieves the function operators node
    function_operators_node = settler_ast.AstSequenceEndNode()

    # retrieves the function name value
    function_name_value = t[2]

    # retrieves the function arguments node
    function_arguments_node = t[4]

    # retrieves the statements node
    statements_node = t[8]

    # creates the function node
    function_node = settler_ast.FunctionNode()

    # sets the function operators node in the function node
    function_node.set_function_operators_node(function_operators_node)

    # sets the function name in the function node
    function_node.set_function_name(function_name_value)

    # sets the arguments node in the function node
    function_node.set_function_arguments_node(function_arguments_node)

    # sets the statements node in the function node
    function_node.set_statements_node(statements_node)

    t[0] = function_node

def p_function_operators_multiple(t):
    "function_operators : function_operator COMA function_operators"

    # retrieves the function operator node
    function_operator_node = t[1]

    # retrieves the next function operators node
    next_function_operators_node = t[3]

    # creates the function operators node
    function_operators_node = settler_ast.FunctionOperatorsNode()

    # sets the function operator node in the function operators node
    function_operators_node.set_function_operator_node(function_operator_node)

    # sets the next node in the function operators node
    function_operators_node.set_next_node(next_function_operators_node)

    t[0] = function_operators_node

def p_function_operators_single(t):
    "function_operators : function_operator"

    # retrieves the function operator node
    function_operator_node = t[1]

    # creates the function operators node
    function_operators_node = settler_ast.FunctionOperatorsNode()

    # sets the function operator node in the function operators node
    function_operators_node.set_function_operator_node(function_operator_node)

    # sets the next node in the function operators node
    function_operators_node.set_next_node(None)

    t[0] = function_operators_node

def p_function_operators_null(t):
    "function_operators : "

    # creates the ast sequence end node
    ast_sequence_end_node = settler_ast.AstSequenceEndNode()

    t[0] = ast_sequence_end_node

def p_function_operator_static(t):
    "function_operator : STATIC"

    # creates the static function operator node
    static_function_operator_node = settler_ast.StaticFunctionOperatorNode()

    t[0] = static_function_operator_node

def p_arguments_multiple(t):
    "arguments : argument COMA arguments"

    # retrieves the argument node
    argument_node = t[1]

    # retrieves the next arguments node
    next_arguments_node = t[3]

    # creates the arguments node
    arguments_node = settler_ast.ArgumentsNode()

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
    arguments_node = settler_ast.ArgumentsNode()

    # sets the argument node in the arguments node
    arguments_node.set_argument_node(argument_node)

    # sets the next node in the arguments node
    arguments_node.set_next_node(None)

    t[0] = arguments_node

def p_arguments_null(t):
    "arguments : "

    # creates the ast sequence end node
    ast_sequence_end_node = settler_ast.AstSequenceEndNode()

    t[0] = ast_sequence_end_node

def p_argument_simple(t):
    "argument : NAME"

    # retrieves the name value
    name_value = t[1]

    # creates the argument node
    argument_node = settler_ast.ArgumentNode()

    # sets the name in the argument node
    argument_node.set_name(name_value)

    t[0] = argument_node

def p_argument_default_value(t):
    "argument : NAME EQUALS expression"

    # retrieves the name value
    name_value = t[1]

    # retrieves the expression node
    expression_node = t[3]

    # creates the default value argument node
    default_value_argument_node = settler_ast.DefaultValueArgumentNode()

    # sets the name in the default value argument node
    default_value_argument_node.set_name(name_value)

    # sets the expression node in the default value argument node
    default_value_argument_node.set_expression_node(expression_node)

    t[0] = default_value_argument_node

def p_expression_function_call(t):
    "expression : name_reference LPAREN argument_values RPAREN"

    # retrieves the function name reference node
    function_name_reference_node = t[1]

    # retrieves the function argument values node
    function_argument_values_node = t[3]

    # creates the function call node
    function_call_node = settler_ast.FunctionCallNode()

    # sets the function name reference node in the function call node
    function_call_node.set_function_name_reference_node(function_name_reference_node)

    # sets the function arguments value node in the function call node
    function_call_node.set_function_argument_values_node(function_argument_values_node)

    t[0] = function_call_node

def p_argument_values_multiple(t):
    "argument_values : argument_value COMA argument_values"

    # retrieves the argument value node
    argument_value_node = t[1]

    # retrieves the next argument values node
    next_argument_values_node = t[3]

    # creates the argument values node
    argument_values_node = settler_ast.ArgumentValuesNode()

    # sets the argument value node in the argument values node
    argument_values_node.set_argument_value_node(argument_value_node)

    # sets the next node in the argument values node
    argument_values_node.set_next_node(next_argument_values_node)

    t[0] = argument_values_node

def p_argument_values_single(t):
    "argument_values : argument_value"

    # retrieves the argument value node
    argument_value_node = t[1]

    # creates the argument values node
    argument_values_node = settler_ast.ArgumentValuesNode()

    # sets the argument value node in the argument values node
    argument_values_node.set_argument_value_node(argument_value_node)

    # sets the next node in the argument values node
    argument_values_node.set_next_node(None)

    t[0] = argument_values_node

def p_argument_values_null(t):
    "argument_values : "

    # creates the ast sequence end node
    ast_sequence_end_node = settler_ast.AstSequenceEndNode()

    t[0] = ast_sequence_end_node

def p_argument_value(t):
    "argument_value : expression"

    # retrieves the expression node
    expression_node = t[1]

    # creates the argument value node
    argument_value_node = settler_ast.ArgumentValueNode()

    # sets the expression node in the argument value node
    argument_value_node.set_expression_node(expression_node)

    t[0] = argument_value_node

def p_expression_class(t):
    "class : CLASS NAME extends implements COLON NEWLINE statements END"

    # retrieves the class name value
    class_name_value = t[2]

    # retrieves the extends node
    extends_node = t[3]

    # retrieves the implements node
    implements_node = t[4]

    # retrieves the statements node
    statements_node = t[7]

    # creates the class node
    class_node = settler_ast.ClassNode()

    # sets the class name in the class node
    class_node.set_class_name(class_name_value)

    # sets the extends node in the class node
    class_node.set_extends_node(extends_node)

    # sets the implements node in the class node
    class_node.set_implements_node(implements_node)

    # sets the statements node in the class node
    class_node.set_statements_node(statements_node)

    t[0] = class_node

def p_extends(t):
    "extends : EXTENDS extends_values"

    # retrieves the extends values node
    extends_values_node = t[2]

    # creates the extends node
    extends_node = settler_ast.ExtendsNode()

    # sets the extends values node in the extends node
    extends_node.set_extends_values_node(extends_values_node)

    t[0] = extends_node

def p_extends_null(t):
    "extends : "

    # creates the extends node
    extends_node = settler_ast.ExtendsNode()

    t[0] = extends_node

def p_extends_values_multiple(t):
    "extends_values : NAME COMA extends_values"

    # retrieves the extends values name
    extends_values_name = t[1]

    # retrieves the next extends values node
    next_extends_values_node = t[3]

    # creates the extends values node
    extends_values_node = settler_ast.ExtendsValuesNode()

    # sets the extends values name in the extends values node
    extends_values_node.set_extends_values_name(extends_values_name)

    # sets the next node in the extends values node
    extends_values_node.set_next_node(next_extends_values_node)

    t[0] = extends_values_node

def p_extends_values_single(t):
    "extends_values : NAME"

    # retrieves the extends values name
    extends_values_name = t[1]

    # creates the extends values node
    extends_values_node = settler_ast.ExtendsValuesNode()

    # sets the extends values name in the extends values node
    extends_values_node.set_extends_values_name(extends_values_name)

    # sets the next node in the extends values node
    extends_values_node.set_next_node(None)

    t[0] = extends_values_node

def p_implements(t):
    "implements : IMPLEMENTS implements_values"

    # retrieves the implements values node
    implements_values_node = t[2]

    # creates the implements node
    implements_node = settler_ast.ImplementsNode()

    # sets the implements values node in the implements node
    implements_node.set_implements_values_node(implements_values_node)

    t[0] = implements_node

def p_implements_null(t):
    "implements : "

    # creates the implements node
    implements_node = settler_ast.ImplementsNode()

    t[0] = implements_node

def p_implements_values_multiple(t):
    "implements_values : NAME COMA implements_values"

    # retrieves the implements values name
    implements_values_name = t[1]

    # retrieves the next implements values node
    next_implements_values_node = t[3]

    # creates the implements values node
    implements_values_node = settler_ast.ImplementsValuesNode()

    # sets the implements values name in the implements values node
    implements_values_node.set_implements_values_name(implements_values_name)

    # sets the next node in the implements values node
    implements_values_node.set_next_node(next_implements_values_node)

    t[0] = implements_values_node

def p_implements_values_single(t):
    "implements_values : NAME"

    # retrieves the implements values name
    implements_values_name = t[1]

    # creates the implements values node
    implements_values_node = settler_ast.ImplementsValuesNode()

    # sets the implements values name in the implements values node
    implements_values_node.set_implements_values_name(implements_values_name)

    # sets the next node in the implements values node
    implements_values_node.set_next_node(None)

    t[0] = implements_values_node

def p_expression_interface(t):
    "interface : INTERFACE NAME extends COLON NEWLINE statements END"

    # retrieves the interface name value
    interface_name_value = t[2]

    # retrieves the extends node
    extends_node = t[3]

    # retrieves the statements node
    statements_node = t[6]

    # creates the interface node
    interface_node = settler_ast.InterfaceNode()

    # sets the interface name in the interface node
    interface_node.set_interface_name(interface_name_value)

    # sets the extends node in the interface node
    interface_node.set_extends_node(extends_node)

    # sets the statements node in the interface node
    interface_node.set_statements_node(statements_node)

    t[0] = interface_node

def p_expression_plugin(t):
    "plugin : PLUGIN NAME extends implements allows COLON NEWLINE statements END"

    # retrieves the plugin name value
    plugin_name_value = t[2]

    # retrieves the extends node
    extends_node = t[3]

    # retrieves the implements node
    implements_node = t[4]

    # retrieves the allows node
    allows_node = t[5]

    # retrieves the statements node
    statements_node = t[8]

    # creates the plugin node
    plugin_node = settler_ast.PluginNode()

    # sets the plugin name in the plugin node
    plugin_node.set_plugin_name(plugin_name_value)

    # sets the extends node in the plugin node
    plugin_node.set_extends_node(extends_node)

    # sets the implements node in the plugin node
    plugin_node.set_implements_node(implements_node)

    # sets the allows node in the plugin node
    plugin_node.set_allows_node(allows_node)

    # sets the statements node in the plugin node
    plugin_node.set_statements_node(statements_node)

    t[0] = plugin_node

def p_allows(t):
    "allows : ALLOWS allows_values"

    # retrieves the allows values node
    allows_values_node = t[2]

    # creates the allows node
    allows_node = settler_ast.AllowsNode()

    # sets the allows values node in the allows node
    allows_node.set_allows_values_node(allows_values_node)

    t[0] = allows_node

def p_allows_null(t):
    "allows : "

    # creates the allows node
    allows_node = settler_ast.AllowsNode()

    t[0] = allows_node

def p_allows_values_multiple(t):
    "allows_values : NAME COMA allows_values"

    # retrieves the allows values name
    allows_values_name = t[1]

    # retrieves the next allows values node
    next_allows_values_node = t[3]

    # creates the allows values node
    allows_values_node = settler_ast.AllowsValuesNode()

    # sets the allows values name in the allows values node
    allows_values_node.set_allows_values_name(allows_values_name)

    # sets the next node in the allows values node
    allows_values_node.set_next_node(next_allows_values_node)

    t[0] = allows_values_node

def p_allows_values_single(t):
    "allows_values : NAME"

    # retrieves the allows values name
    allows_values_name = t[1]

    # creates the allows values node
    allows_values_node = settler_ast.AllowsValuesNode()

    # sets the allows values name in the allows values node
    allows_values_node.set_allows_values_name(allows_values_name)

    # sets the next node in the allows values node
    allows_values_node.set_next_node(None)

    t[0] = allows_values_node

def p_expression_capability(t):
    "capability : CAPABILITY NAME extends COLON NEWLINE statements END"

    # retrieves the capability name value
    capability_name_value = t[2]

    # retrieves the extends node
    extends_node = t[3]

    # retrieves the statements node
    statements_node = t[6]

    # creates the capability node
    capability_node = settler_ast.CapabilityNode()

    # sets the capability name in the capability node
    capability_node.set_capability_name(capability_name_value)

    # sets the extends node in the capability node
    capability_node.set_extends_node(extends_node)

    # sets the statements node in the capability node
    capability_node.set_statements_node(statements_node)

    t[0] = capability_node

def p_error(t):
    print "Syntax error at '%s'" % t

def validate_expression_unary(t):
    expression_node = t[2]

    if expression_node == None:
        return False

    return True

def validate_expression_binary(t):
    first_expression_node = t[1]
    second_expression_node = t[3]

    if first_expression_node == None or second_expression_node == None:
        return False

    return True

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
