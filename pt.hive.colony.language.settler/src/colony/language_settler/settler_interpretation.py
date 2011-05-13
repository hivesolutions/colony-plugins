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
import settler_visitor

EXECUTION_TYPE = "execution"
CONDITIONAL_TYPE = "conditional"
LOOP_TYPE = "loop"
CALL_TYPE = "call"
DECLARATION_TYPE = "declaration"

CONTEXT_TYPE_TYPE = {
    "global" : EXECUTION_TYPE,
    "execution" : EXECUTION_TYPE,
    "boolean_expression" : EXECUTION_TYPE,
    "if_condition" : CONDITIONAL_TYPE,
    "else_condition" : CONDITIONAL_TYPE,
    "while" : LOOP_TYPE,
    "for" : LOOP_TYPE,
    "function_call" : CALL_TYPE,
    "function" : DECLARATION_TYPE
}

EXECUTION_CONTEXT_TYPES = [
    "global",
    "execution",
    "boolean_expression"
]

CONDITIONAL_CONTEXT_TYPES = [
    "if_condition",
    "else_condition"
]

LOOP_CONTEXT_TYPES = [
    "while",
    "for"
]

CALL_CONTEXT_TYPES = [
    "function_call"
]

DECLARATION_CONTEXT_TYPES = [
    "function"
]

RETURN_CONTEXT_TYPES = [
    "return"
]

context_type_ast_node_map = {
    "boolean_expression" : [
        settler_ast.AndExpressionNode,
        settler_ast.OrExpressionNode
    ],
    "if_condition" : [
        settler_ast.IfConditionNode
    ],
    "else_condition" : [
        settler_ast.ElseConditionNode,
        settler_ast.ElseConditionNode
    ],
    "while" : [
        settler_ast.WhileNode
    ],
    "for" : [
        settler_ast.ForNode
    ],
    "function_call" : [
        settler_ast.FunctionCallNode
    ],
    "function" : [
        settler_ast.FunctionNode
    ]
}

class InterpretationVisitor(settler_visitor.Visitor):
    """
    The interpretation visitor class.
    """

    processing_structure = None
    """ The processing structure """

    return_flag = False
    """ The return flag """

    return_type = "none"
    """ The return type """

    values_stack = []
    """ The values stack """

    def __init__(self):
        settler_visitor.Visitor.__init__(self)

        self.values_stack = []

    def set_processing_structure(self, processing_structure):
        self.processing_structure = processing_structure

    def get_current_context(self):
        return self.processing_structure.get_current_context()

    def get_current_context_stack(self):
        return self.processing_structure.get_current_context_stack()

    def pop_current_context(self):
        settler_visitor.Visitor.pop_current_context(self)
        self.processing_structure.pop_current_context()

    def pop_current_context_local(self):
        self.processing_structure.pop_current_context_local()

    def push_current_context(self, context):
        settler_visitor.Visitor.push_current_context(self, context)
        self.processing_structure.push_current_context(context)

    def push_current_context_local(self, context):
        self.processing_structure.push_current_context_local(context)

    def valid_context_type(self, context_type, node):
        if not context_type in CONTEXT_TYPE_TYPE:
            return False

        type = CONTEXT_TYPE_TYPE[context_type]

        # retrieves current context type
        current_context_type = self.get_current_context_type()

        if not current_context_type in CONTEXT_TYPE_TYPE:
            return False

        current_type = CONTEXT_TYPE_TYPE[current_context_type]

        if type == EXECUTION_TYPE:
            if not current_type in [DECLARATION_TYPE] and not self.return_flag:
                return True
        elif type == CONDITIONAL_TYPE:
            if not current_type in [DECLARATION_TYPE, CONDITIONAL_TYPE] and not self.return_flag:
                return True
        elif type == LOOP_TYPE:
            if not current_type in [DECLARATION_TYPE, LOOP_TYPE] and not self.return_flag:
                return True
        elif type == CALL_TYPE:
            if not current_type in [DECLARATION_TYPE, CALL_TYPE, CONDITIONAL_TYPE, LOOP_TYPE] and not self.return_flag:
                return True
        elif type == DECLARATION_TYPE:
            return True

        return False

    def get_value(self):
        return self.values_stack[-1]

    def pop_value(self):
        self.values_stack.pop()

    def push_value(self, value):
        self.values_stack.append(value)

    def is_node_current_execution_context(self, node, context_type):
        # retrieves the node class
        node_class = node.__class__

        if context_type in context_type_ast_node_map:
            context_type_ast_node_list = context_type_ast_node_map[context_type]

            if node_class in context_type_ast_node_list:
                return True

    def test_context_type(self, node, context_type):
        # retrieves current context type
        current_context_type = self.get_current_context_type()

        if current_context_type == context_type:
            return True
        else:
            return False

    def execution_context(self, node):
        if self.return_flag:
            return False

        # retrieves current context type
        context_type = self.get_current_context_type()

        if self.is_node_current_execution_context(node, context_type):
            return True

        if context_type in EXECUTION_CONTEXT_TYPES:
            return True
        else:
            return False

    def conditional_context(self, node):
        if self.return_flag:
            return False

        # retrieves current context type
        context_type = self.get_current_context_type()

        if self.is_node_current_execution_context(node, context_type):
            return True

        if context_type in CONDITIONAL_CONTEXT_TYPES:
            return True
        else:
            return False

    def loop_context(self, node):
        if self.return_flag:
            return False

        # retrieves current context type
        context_type = self.get_current_context_type()

        if self.is_node_current_execution_context(node, context_type):
            return True

        if context_type in LOOP_CONTEXT_TYPES:
            return True
        else:
            return False

    def return_context(self, node):
        # retrieves current context type
        context_type = self.get_current_context_type()

        if self.is_node_current_execution_context(node, context_type):
            return True

        if context_type in RETURN_CONTEXT_TYPES:
            return True
        else:
            return False

    def call_context(self, node):
        # retrieves current context type
        context_type = self.get_current_context_type()

        if self.is_node_current_execution_context(node, context_type):
            return True

        if context_type in CALL_CONTEXT_TYPES:
            return True
        else:
            return False

    def declaration_context(self, node):
        # retrieves current context type
        context_type = self.get_current_context_type()

        if self.is_node_current_execution_context(node, context_type):
            return True

        if context_type in DECLARATION_CONTEXT_TYPES:
            return True
        else:
            return False

    def get_last_sequence_node(self, sequence_node):
        # retrieves the next sequence node
        next_sequence_node = sequence_node.next_node

        while not next_sequence_node == None:
            sequence_node = next_sequence_node
            next_sequence_node = sequence_node.next_node

        return sequence_node

    @settler_visitor._visit(settler_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.RootNode)
    def visit_root_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ProgramNode)
    def visit_program_node(self, node):
        # retrieves the statements node
        statements_node = node.statements_node

        # retrieves the last statements node
        last_statements_node = statements_node.get_last_node()

        # retrieves the last statements value
        last_statements_value = last_statements_node.value

        # sets the node value as last statements value
        node.set_value(last_statements_value)

    @settler_visitor._visit(settler_ast.StatementsNode)
    def visit_statements_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the statement node
        statement_node = node.statement_node

        # retrieves the statement value
        statement_value = statement_node.value

        # sets the node value as statement value
        node.set_value(statement_value)

    @settler_visitor._visit(settler_ast.AssignNode)
    def visit_assign_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the name
        name = node.name

        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the expression value
        expression_value = expression_node.value

        # sets the symbol value in the current context
        self.processing_structure.set_symbol_value_current_context(name, expression_value)

        # sets the node value as None
        node.set_value(None)

    @settler_visitor._visit(settler_ast.ReturnNode)
    def visit_return_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # pushes the context type as execution
        self.push_current_context_type("execution", node)

        # calls the visitor in the if expression
        expression_node.accept_post_order(self)

        # pops the context type
        self.pop_current_context_type(node)

        # retrieves the expression value
        expression_value = expression_node.value

        # sets the node value as the expression value
        node.set_value(expression_value)

        # sets the return flag as true
        self.return_flag = True

        # sets the return type as return
        self.return_type = "return"

        # pushes the return node
        self.push_value(node)

    @settler_visitor._visit(settler_ast.IfConditionNode)
    def visit_if_condition_node(self, node):
        # tests the conditional context
        if not self.conditional_context(node):
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the statements node
        statements_node = node.statements_node

        # retrieves the else condition node
        else_condition_node = node.else_condition_node

        # pushes the context type as execution
        self.push_current_context_type("execution", node)

        # calls the visitor in the if expression
        expression_node.accept_post_order(self)

        # pops the context type
        self.pop_current_context_type(node)

        # retrieves the expression value
        expression_value = expression_node.value

        # in case the value is positive
        if expression_value:
            # pushes the context type as execution
            self.push_current_context_type("execution", node)

            # calls the visitor in the if statements
            statements_node.accept_post_order(self)

            # pops the context type
            self.pop_current_context_type(node)

            # retrieves the last statements node
            last_statements_node = statements_node.get_last_node()

            # retrieves the last statements value
            last_statements_value = last_statements_node.value

            # sets the node value as the statements value
            node.set_value(last_statements_value)
        elif else_condition_node.is_valid():
            # pushes the context type as execution
            self.push_current_context_type("else_condition", node)

            # calls the visitor in the else condition
            else_condition_node.accept(self)

            # pops the context type
            self.pop_current_context_type(node)

            # retrieves the else condition value
            else_condition_value = else_condition_node.value

            # sets the node value as the statements value
            node.set_value(else_condition_value)
        else:
            # sets the node value as the statements value
            node.set_value(None)

    @settler_visitor._visit(settler_ast.ElseConditionNode)
    def visit_else_condition_node(self, node):
        # tests the else_condition context
        if not self.test_context_type(node, "else_condition"):
            return

        # retrieves the statements node
        statements_node = node.statements_node

        # pushes the context type as execution
        self.push_current_context_type("execution", node)

        # calls the visitor in the else statements
        statements_node.accept_post_order(self)

        # pops the context type
        self.pop_current_context_type(node)

        # retrieves the last statements node
        last_statements_node = statements_node.get_last_node()

        # retrieves the last statements value
        last_statements_value = last_statements_node.value

        # sets the node value as the statements value
        node.set_value(last_statements_value)

        # sets the visit childs flag as false, disabling the visit on child nodes
        self.visit_childs = False

        # sets the visit next flag as false, disabling the visit on next nodes
        self.visit_next = False

    @settler_visitor._visit(settler_ast.ElseIfConditionNode)
    def visit_else_if_condition_node(self, node):
        # tests the else_condition context
        if not self.test_context_type(node, "else_condition"):
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the statements node
        statements_node = node.statements_node

        # retrieves the next else condition node
        next_else_condition_node = node.next_node

        # pushes the context type as execution
        self.push_current_context_type("execution", node)

        # calls the visitor in the else if expression
        expression_node.accept_post_order(self)

        # pops the context type
        self.pop_current_context_type(node)

        # retrieves the expression value
        expression_value = expression_node.value

        # in case the value is positive
        if expression_value:
            # pushes the context type as execution
            self.push_current_context_type("execution", node)

            # calls the visitor in the else if statements
            statements_node.accept_post_order(self)

            # pops the context type
            self.pop_current_context_type(node)

            # retrieves the last statements node
            last_statements_node = statements_node.get_last_node()

            # retrieves the last statements value
            last_statements_value = last_statements_node.value

            # sets the node value as the statements value
            node.set_value(last_statements_value)
        elif next_else_condition_node.is_valid():
            # calls the visitor in the next else condition
            next_else_condition_node.accept(self)

            # retrieves the next else condition value
            next_else_condition_value = next_else_condition_node.value

            # sets the node value as the statements value
            node.set_value(next_else_condition_value)
        else:
            # sets the node value as the statements value
            node.set_value(None)

        # sets the visit childs flag as false, disabling the visit on child nodes
        self.visit_childs = False

        # sets the visit next flag as false, disabling the visit on next nodes
        self.visit_next = False

    @settler_visitor._visit(settler_ast.WhileNode)
    def visit_while_node(self, node):
        # tests the loop context
        if not self.loop_context(node):
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the statements node
        statements_node = node.statements_node

        # pushes the context type as execution
        self.push_current_context_type("execution", node)

        # calls the visitor in the else if expression
        expression_node.accept_post_order(self)

        # pops the context type
        self.pop_current_context_type(node)

        # retrieves the expression value
        expression_value = expression_node.value

        while expression_value:
            # pushes the context type as execution
            self.push_current_context_type("execution", node)

            # calls the visitor in the while statements
            statements_node.accept_post_order(self)

            # pops the context type
            self.pop_current_context_type(node)

            # retrieves the last statements node
            last_statements_node = statements_node.get_last_node()

            # retrieves the last statements value
            last_statements_value = last_statements_node.value

            # sets the node value as the statements value
            node.set_value(last_statements_value)

            # pushes the context type as execution
            self.push_current_context_type("execution", node)

            # calls the visitor in the else if expression
            expression_node.accept_post_order(self)

            # pops the context type
            self.pop_current_context_type(node)

            # retrieves the expression value
            expression_value = expression_node.value

    @settler_visitor._visit(settler_ast.ForNode)
    def visit_for_node_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        print "ForNode: " + str(node)

    @settler_visitor._visit(settler_ast.ExpressionNode)
    def visit_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.NumberExpressionNode)
    def visit_number_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.IntegerExpressionNode)
    def visit_integer_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the integer value
        integer_value = node.integer_value

        # sets the node value as the integer value
        node.set_value(integer_value)

    @settler_visitor._visit(settler_ast.StringExpressionNode)
    def visit_string_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the string value
        string_value = node.string_value

        # sets the node value as the string value
        node.set_value(string_value)

    @settler_visitor._visit(settler_ast.BoolExpressionNode)
    def visit_bool_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the bool value
        bool_value = node.bool_value

        # sets the node value as the bool value
        node.set_value(bool_value)

    @settler_visitor._visit(settler_ast.NameExpressionNode)
    def visit_name_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the name
        name = node.name

        # gets the symbol value in the current context
        symbol_value = self.processing_structure.get_symbol_value_current_context(name)

        # sets the node value as the symbol value
        node.set_value(symbol_value)

    @settler_visitor._visit(settler_ast.ListExpressionNode)
    def visit_list_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the list contents node
        list_contents_node = node.list_contents_node

        # creates an empty list of values
        list_values = []

        # iterates over the list contents nodes
        for list_contents_node_item in list_contents_node:
            if not list_contents_node_item.is_valid():
                break

            # retrieves list contents node value
            list_contents_node_value = list_contents_node_item.value

            # appends the value to the list of values
            list_values.append(list_contents_node_value)

        # sets the node value as the list of values
        node.set_value(list_values)

    @settler_visitor._visit(settler_ast.ListContentsNode)
    def visit_list_contents_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # in case the node is not valid
        if not node.is_valid():
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # pushes the context type as execution
        self.push_current_context_type("execution", node)

        # calls the visitor in the expression node
        expression_node.accept_post_order(self)

        # pops the context type
        self.pop_current_context_type(node)

        # retrieves the expression value
        expression_value = expression_node.value

        # sets the node value as the expression value
        node.set_value(expression_value)

    @settler_visitor._visit(settler_ast.UnaryExpressionNode)
    def visit_unary_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.BinaryExpressionNode)
    def visit_binary_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ArithmethicExpressionNode)
    def visit_arithmethic_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.SummationExpressionNode)
    def visit_summation_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the summation expression value
        summation_expression_value = first_expression_value + second_expression_value

        # sets the node value as the summation expression value
        node.set_value(summation_expression_value)

    @settler_visitor._visit(settler_ast.SubtractionExpressionNode)
    def visit_subtraction_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the subtraction expression value
        subtraction_expression_value = first_expression_value - second_expression_value

        # sets the node value as the subtraction expression value
        node.set_value(subtraction_expression_value)

    @settler_visitor._visit(settler_ast.MultiplicationExpressionNode)
    def visit_multiplication_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the multiplication expression value
        multiplication_expression_value = first_expression_value * second_expression_value

        # sets the node value as the multiplication expression value
        node.set_value(multiplication_expression_value)

    @settler_visitor._visit(settler_ast.DivisionExpressionNode)
    def visit_division_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the division expression value
        division_expression_value = first_expression_value / second_expression_value

        # sets the node value as the division expression value
        node.set_value(division_expression_value)

    @settler_visitor._visit(settler_ast.PowerExpressionNode)
    def visit_power_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the power expression value
        power_expression_value = first_expression_value ** second_expression_value

        # sets the node value as the power expression value
        node.set_value(power_expression_value)

    @settler_visitor._visit(settler_ast.BooleanExpressionNode)
    def visit_boolean_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.EqualExpressionNode)
    def visit_equal_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the equal expression value
        equal_expression_value = first_expression_value == second_expression_value

        # sets the node value as the equal expression value
        node.set_value(equal_expression_value)

    @settler_visitor._visit(settler_ast.GreaterExpressionNode)
    def visit_greater_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the greater expression value
        greater_expression_value = first_expression_value > second_expression_value

        # sets the node value as the greater expression value
        node.set_value(greater_expression_value)

    @settler_visitor._visit(settler_ast.GreaterEqualExpressionNode)
    def visit_greater_equal_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the greater equal expression value
        greater_equal_expression_value = first_expression_value >= second_expression_value

        # sets the node value as the greater equal expression value
        node.set_value(greater_equal_expression_value)

    @settler_visitor._visit(settler_ast.AndExpressionNode)
    def visit_and_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the and expression value
        and_expression_value = first_expression_value and second_expression_value

        # sets the node value as the and expression value
        node.set_value(and_expression_value)

    @settler_visitor._visit(settler_ast.OrExpressionNode)
    def visit_or_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # retrieves the first expression value
        first_expression_value = first_expression_node.value

        # retrieves the second expression value
        second_expression_value = second_expression_node.value

        # calculates the or expression value
        or_expression_value = first_expression_value or second_expression_value

        # sets the node value as the or expression value
        node.set_value(or_expression_value)

    @settler_visitor._visit(settler_ast.NotExpressionNode)
    def visit_not_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the expression value
        expression_value = expression_node.value

        # calculates the not expression value
        not_expression_value = not expression_value

        # sets the node value as the not expression value
        node.set_value(not_expression_value)

    @settler_visitor._visit(settler_ast.ParenthesisExpressionNode)
    def visit_parenthesis_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the expression value
        expression_value = expression_node.value

        # calculates the parenthesis expression value
        parenthesis_expression_value = (
            expression_value,
        )

        # sets the node value as the parenthesis expression value
        node.set_value(parenthesis_expression_value)

    @settler_visitor._visit(settler_ast.NegativeExpressionNode)
    def visit_negative_expression_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the expression value
        expression_value = expression_node.value

        # calculates the negative expression value
        negative_expression_value = -expression_value

        # sets the node value as the negative expression value
        node.set_value(negative_expression_value)

    @settler_visitor._visit(settler_ast.FunctionNode)
    def visit_function_node(self, node):
        # tests the declaration context
        if not self.declaration_context(node):
            return

        # retrieves the function name
        function_name = node.function_name

        # sets the function node in the current context
        self.processing_structure.set_symbol_value_current_context(function_name, node)

        # sets the node value as None
        node.set_value(None)

    @settler_visitor._visit(settler_ast.ArgumentsNode)
    def visit_arguments_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ArgumentNode)
    def visit_argument_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.DefaultValueArgumentNode)
    def visit_default_argument_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.FunctionCallNode)
    def visit_function_call_node(self, node):
        # tests the execution context
        if not self.execution_context(node):
            return

        # retrieves the function name
        function_name = node.function_name

        # retrieves the function argument values node
        function_argument_values_node = node.function_argument_values_node

        # retrieves the python builtins module
        python_builtins = globals()["__builtins__"]

        if function_name in python_builtins:
            # retrieves the python builtin function
            builtin_function = python_builtins[function_name]

            # retrieves the argument values
            argument_values = self.get_argument_values(function_argument_values_node)

            # calls the builtin function
            return_value = builtin_function(*argument_values)

            # sets the node value as the return value
            node.set_value(return_value)
        elif function_name == "print":
            # retrieves the argument values
            argument_values = self.get_argument_values(function_argument_values_node)

            # calls the print function
            print argument_values[0]

            # sets the node value as None
            node.set_value(None)
        else:
            # gets the function node in the current context
            function_node = self.processing_structure.get_symbol_value_current_context(function_name)

            # retrieves the function arguments node
            fuction_arguments_node = function_node.function_arguments_node

            # retrieves the function node statements node
            statements_node = function_node.statements_node

            # pushes the current context as a local one
            self.push_current_context_local(function_name)

            # iterates over all the function arguments node and over all the function arguments values node,
            # to set the argument values in the symbols table
            for fuction_arguments_node_item, function_argument_values_node_item in zip(fuction_arguments_node, function_argument_values_node):
                # in case the function argument values node is not valid
                if not function_argument_values_node_item.is_valid():
                    break

                # retrieves the argument name
                name = fuction_arguments_node_item.argument_node.name

                # retrieves the argument value
                argument_value = self.get_argument_value(function_argument_values_node_item)

                # sets the expression value in the current context
                self.processing_structure.set_symbol_value_current_context(name, argument_value)

            # pushes the context type as execution
            self.push_current_context_type("execution", node)

            # calls the visitor in the function statements
            statements_node.accept_post_order(self)

            # pops the context type
            self.pop_current_context_type(node)

            # in case there is a return value
            if self.return_flag and self.return_type == "return":
                # retrieves the return node
                return_node = self.get_value()

                # retrieves the return value
                return_value = return_node.value

                # pop the current values stack value
                self.pop_value()

                # sets the node value as the return value
                node.set_value(return_value)

                # resets the return flag state
                self.return_flag = False
                self.return_type = "none"
            else:
                # sets the node value as None
                node.set_value(None)

            # pops the current context as a local one
            self.pop_current_context_local()

    @settler_visitor._visit(settler_ast.ArgumentValuesNode)
    def visit_argument_values_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ArgumentValueNode)
    def visit_argument_value_node(self, node):
        pass

    def get_argument_values(self, function_argument_values_node):
        argument_values = []

        for function_argument_values_node_item in function_argument_values_node:
            if function_argument_values_node_item.is_valid():
                argument_value = self.get_argument_value(function_argument_values_node_item)
                argument_values.append(argument_value)

        return argument_values

    def get_argument_value(self, function_argument_values_node):
        # retrieves the argument expression
        expression_node = function_argument_values_node.argument_value_node.expression_node

        # pushes the context type as execution
        self.push_current_context_type("execution", function_argument_values_node)

        # calls the visitor in the expression node
        expression_node.accept_post_order(self)

        # pops the context type
        self.pop_current_context_type(function_argument_values_node)

        # retrieves the expression value
        expression_value = expression_node.value

        return expression_value
