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

# the token definitions
tokens = ("NAME", "NUMBER", "STRING", "BOOL", "PLUS",
          "MINUS", "TIMES", "DIVIDE", "POWER",
          "EQUALS", "EQUALEQUAL", "GREATER",
          "GREATEREQUAL", "LESS", "LESSEQUAL",
          "NOT", "AND", "OR", "LPAREN", "RPAREN",
          "LBRACK", "RBRACK", "FUNCTION", "RETURN",
          "COLON", "COMA", "DOT", "IF", "ELSE", "ELIF",
          "END", "NEWLINE", "WHILE", "FOR", "IN", "IMPORT",
          "CLASS", "EXTENDS", "IMPLEMENTS", "INTERFACE",
          "PLUGIN", "CAPABILITY", "ALLOWS", "PASS", "STATIC",
          "GLOBAL")

# the reserved keywords
reserved = {
    "not" : "NOT",
    "and" : "AND",
    "or" : "OR",
    "True" : "BOOL",
    "False" : "BOOL",
    "function" : "FUNCTION",
    "return" : "RETURN",
    "if" : "IF",
    "else" : "ELSE",
    "elif" : "ELIF",
    "end" : "END",
    "while" : "WHILE",
    "for" : "FOR",
    "in" : "IN",
    "import" : "IMPORT",
    "class" : "CLASS",
    "interface" : "INTERFACE",
    "extends" : "EXTENDS",
    "implements" : "IMPLEMENTS",
    "plugin" : "PLUGIN",
    "capability": "CAPABILITY",
    "allows" : "ALLOWS",
    "pass" : "PASS",
    "static" : "STATIC",
    "global" : "GLOBAL"
}

reserved_values = {
    "True" : True,
    "False" : False
}

# token definition
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_POWER = r"\^"
t_EQUALS = r"="

t_EQUALEQUAL = r"=="
t_GREATER = r">"
t_GREATEREQUAL = r">="
t_LESS = r"<"
t_LESSEQUAL = r"<="

t_LPAREN = r"\("
t_RPAREN = r"\)"

t_LBRACK = r"\["
t_RBRACK = r"\]"

t_COLON = r":"
t_COMA = r","
t_DOT = r"\."

def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "NAME")
    t.value = reserved_values.get(t.value, t.value)
    return t

# number definition
def t_NUMBER(t):
    r"\d+"

    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0

    return t

# string definition
def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\""

    t.value = t.value[1:-1]

    return t

# the new line character
def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")
    return t

# single line comments
def t_comment(t):
    r"\#[^\n]*\n+"
    pass

# ignored characters
t_ignore = " "

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# parsing rules
# precedence of operators
precedence = (("left", "OR"),
              ("left", "AND"),
              ("left", "GREATER", "GREATEREQUAL", "LESS", "LESSEQUAL", "EQUALEQUAL"),
              ("left", "PLUS", "MINUS"),
              ("left", "TIMES", "DIVIDE", "POWER"),
              ("right", "NOT"),
              ("right", "UMINUS"),)

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
    "else_condition : ELSE COLON NEWLINE statements"


    t[0] = "asdasd"

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

#def p_statement_expression(t):
    "statement : expression"

    # retrieves the expression node
#    expression_node = t[1]

#    t[0] = expression_node

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



example = locals()
