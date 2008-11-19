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

class AstNode(object):
    """
    The ast node class.
    """

    value = None
    """ The value """

    ident = False
    """ The identation level """

    child_nodes = []
    """ The list of child nodes """

    def __init__(self):
        self.child_nodes = []

    def __repr__(self):
        return "<ast_node ident:%s child_nodes:%s>" % (self.ident, len(self.child_nodes))

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

    def set_value(self, value):
        self.value = value

    def set_ident(self, ident):
        self.ident = ident

    def add_child_node(self, child_node):
        self.child_nodes.append(child_node)

    def remove_child_node(self, child_node):
        self.child_nodes.remove(child_node)

class AstSequenceNode(AstNode):
    """
    The ast sequence node class.
    """

    next_node = None
    """ The next node """

    valid = True
    """ The valid flag """

    def __init__(self):
        AstNode.__init__(self)

    def __iter__(self):
        # creates the ast sequence node iterator
        ast_sequence_node_iterator = AstSequenceNodeIterator(self)

        # returns the ast sequence node iterator
        return ast_sequence_node_iterator

    def set_next_node(self, next_node):
        self.next_node = next_node

    def get_last_node(self):
        # sets the current sequence node
        sequence_node = self

        # retrieves the next sequence node
        next_sequence_node = self.next_node

        while not next_sequence_node == None:
            sequence_node = next_sequence_node
            next_sequence_node = sequence_node.next_node

        return sequence_node

    def get_all_nodes(self):
        # constructs the nodes list
        nodes_list = [value for value in self]

        # returns the nodes list
        return nodes_list

    def count(self):
        # retrieve all nodes
        all_nodes = self.get_all_nodes()

        # calculates the length of all nodes
        length_all_nodes = len(all_nodes)

        # returns the length of all nodes
        return length_all_nodes

    def is_valid(self):
        return self.valid

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        if self.next_node:
            if visitor.visit_next:
                self.next_node.accept(visitor)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        if self.next_node:
            if visitor.visit_next:
                self.next_node.accept_post_order(visitor)

class AstSequenceEndNode(AstSequenceNode):
    """
    The ast sequence end node class.
    """

    def __init__(self):
        AstSequenceNode.__init__(self)
        self.valid = False

class RootNode(AstNode):
    """
    The root node class.
    """

    def __init__(self):
        AstNode.__init__(self)

class ProgramNode(RootNode):
    """
    The program node class.
    """

    statements_node = None
    """ The statements node """

    def __init__(self):
        RootNode.__init__(self)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

class StatementsNode(AstSequenceNode):
    """
    The statements node class.
    """

    statement_node = None
    """ The statement node """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_statement_node(self, statement_node):
        self.statement_node = statement_node
        self.add_child_node(statement_node)

class StatementNode(AstNode):
    """
    The statement node class.
    """

    def __init__(self):
        AstNode.__init__(self)

class PassNode(StatementNode):
    """
    The pass node class.
    """

    def __init__(self):
        StatementNode.__init__(self)

class AssignNode(StatementNode):
    """
    The assign node class.
    """

    name_reference_node = None
    """ The name reference node """

    expression_node = None
    """ The expression node """

    def __init__(self):
        StatementNode.__init__(self)

    def set_name_reference_node(self, name_reference_node):
        self.name_reference_node = name_reference_node
        self.add_child_node(name_reference_node)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("assign", self):
            return

        visitor.push_current_context_type("assign", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("assign", self):
            return

        visitor.push_current_context_type("assign", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class ReturnNode(StatementNode):
    """
    The return node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        StatementNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

class GlobalNode(StatementNode):
    """
    The global node class.
    """

    name = None
    """ The name """

    def __init__(self):
        StatementNode.__init__(self)

    def set_name(self, name):
        self.name = name

class IfConditionNode(StatementNode):
    """
    The if condition node class.
    """

    expression_node = None
    """ The expression node """

    statements_node = None
    """ The statements node """

    else_condition_node = None
    """ The else condition node """

    def __init__(self):
        StatementNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

    def set_else_condition_node(self, else_condition_node):
        self.else_condition_node = else_condition_node
        self.add_child_node(else_condition_node)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("if_condition", self):
            return

        visitor.push_current_context_type("if_condition", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("if_condition", self):
            return

        visitor.push_current_context_type("if_condition", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class ElseConditionNode(AstSequenceNode):
    """
    The else condition node class.
    """

    statements_node = None
    """ The statements node """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

class ElseIfConditionNode(ElseConditionNode):
    """
    The else if condition node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        ElseConditionNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

class WhileNode(StatementNode):
    """
    The while node class.
    """

    expression_node = None
    """ The expression node """

    statements_node = None
    """ The statements node """

    def __init__(self):
        StatementNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("while", self):
            return

        visitor.push_current_context_type("while", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("while", self):
            return

        visitor.push_current_context_type("while", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class ForNode(StatementNode):
    """
    The for node class.
    """

    item_name = None
    """ The item name """

    expression_node = None
    """ The expression node """

    statements_node = None
    """ The statements node """

    def __init__(self):
        StatementNode.__init__(self)

    def set_item_name(self, item_name):
        self.item_name = item_name

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

class ExpressionNode(StatementNode):
    """
    The expression node class.
    """

    def __init__(self):
        StatementNode.__init__(self)

class NumberExpressionNode(ExpressionNode):
    """
    The number expression node class.
    """

    def __init__(self):
        ExpressionNode.__init__(self)

class IntegerExpressionNode(NumberExpressionNode):
    """
    The integer expression node class.
    """

    integer_value = None
    """ The integer value """

    def __init__(self):
        NumberExpressionNode.__init__(self)

    def set_integer_value(self, integer_value):
        self.integer_value = integer_value

class StringExpressionNode(ExpressionNode):
    """
    The string expression node class.
    """

    string_value = None
    """ The string value """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_string_value(self, string_value):
        self.string_value = string_value

class BoolExpressionNode(ExpressionNode):
    """
    The bool expression node class.
    """

    bool_value = None
    """ The bool value """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_bool_value(self, bool_value):
        self.bool_value = bool_value

class NameExpressionNode(ExpressionNode):
    """
    The name expression node class.
    """

    name_reference_node = None
    """ The name reference node """

    def __init__(self):
        ExpressionNode.__init__(self)    

    def set_name_reference_node(self, name_reference_node):
        self.name_reference_node = name_reference_node
        self.add_child_node(name_reference_node)

class ListExpressionNode(ExpressionNode):
    """
    The list expression node class.
    """

    list_contents_node = None
    """ The list contents node """

    def __init__(self):
        ExpressionNode.__init__(self)    

    def set_list_contents_node(self, list_contents_node):
        self.list_contents_node = list_contents_node
        self.add_child_node(list_contents_node)

class ListContentsNode(AstSequenceNode):
    """
    The list contents node.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

class UnaryExpressionNode(ExpressionNode):
    """
    The unary expression node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

class BinaryExpressionNode(ExpressionNode):
    """
    The binary expression node class.
    """

    first_expression_node = None
    """ The first expression node """

    second_expression_node = None
    """ The second expression node """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_first_expression_node(self, first_expression_node):
        self.first_expression_node = first_expression_node
        self.add_child_node(first_expression_node)

    def set_second_expression_node(self, second_expression_node):
        self.second_expression_node = second_expression_node
        self.add_child_node(second_expression_node)

class ArithmethicExpressionNode(BinaryExpressionNode):
    """
    The arithmetic expression node class.
    """

    def __init__(self):
        BinaryExpressionNode.__init__(self)

class SummationExpressionNode(ArithmethicExpressionNode):
    """
    The summation expression node class.
    """

    def __init__(self):
        ArithmethicExpressionNode.__init__(self)

class SubtractionExpressionNode(ArithmethicExpressionNode):
    """
    The subtraction expression node class.
    """

    def __init__(self):
        ArithmethicExpressionNode.__init__(self)

class MultiplicationExpressionNode(ArithmethicExpressionNode):
    """
    The multiplication expression node class.
    """

    def __init__(self):
        ArithmethicExpressionNode.__init__(self)

class DivisionExpressionNode(ArithmethicExpressionNode):
    """
    The division expression node class.
    """

    def __init__(self):
        ArithmethicExpressionNode.__init__(self)

class PowerExpressionNode(ArithmethicExpressionNode):
    """
    The power expression node class.
    """

    def __init__(self):
        ArithmethicExpressionNode.__init__(self)

class BooleanExpressionNode(BinaryExpressionNode):
    """
    The boolean expression node class.
    """

    def __init__(self):
        BinaryExpressionNode.__init__(self)

class EqualExpressionNode(BooleanExpressionNode):
    """
    The equal expression node class.
    """

    def __init__(self):
        BooleanExpressionNode.__init__(self)

class GreaterExpressionNode(BooleanExpressionNode):
    """
    The greater expression node class.
    """

    def __init__(self):
        BooleanExpressionNode.__init__(self)

class GreaterEqualExpressionNode(BooleanExpressionNode):
    """
    The greater equal expression node class.
    """

    def __init__(self):
        BooleanExpressionNode.__init__(self)

class AndExpressionNode(BooleanExpressionNode):
    """
    The and expression node class.
    """

    def __init__(self):
        BooleanExpressionNode.__init__(self)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("boolean_expression", self):
            return

        visitor.push_current_context_type("boolean_expression", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("boolean_expression", self):
            return

        visitor.push_current_context_type("boolean_expression", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class OrExpressionNode(BooleanExpressionNode):
    """
    The or expression node class.
    """

    def __init__(self):
        BooleanExpressionNode.__init__(self)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("boolean_expression", self):
            return

        visitor.push_current_context_type("boolean_expression", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("boolean_expression", self):
            return

        visitor.push_current_context_type("boolean_expression", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class NotExpressionNode(UnaryExpressionNode):
    """
    The not expression node class.
    """

    def __init__(self):
        UnaryExpressionNode.__init__(self)

class ParenthesisExpressionNode(UnaryExpressionNode):
    """
    The parenthesis expression node class.
    """

    def __init__(self):
        ExpressionNode.__init__(self)

class NegativeExpressionNode(UnaryExpressionNode):
    """
    The negative expression node class.
    """

    def __init__(self):
        ExpressionNode.__init__(self)

class NameReferenceNode(AstSequenceNode):
    """
    The name reference node.
    """

    name_reference = None
    """ The name reference """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_name_reference(self, name_reference):
        self.name_reference = name_reference

    def to_name(self):
        """
        Converts the name reference node to a fully qualified name.
        
        @rtype: String
        @return: The fully qualified name reference.
        """

        # creates a new name variable
        name = ""

        # creates the is first flag
        is_first = True

        for name_reference_node in self:
            if is_first:
                is_first = False
            else:
                name += "."
            name_reference = name_reference_node.name_reference
            name += name_reference

        return name

class ImportNode(AstSequenceNode):
    """
    The import node.
    """

    import_name_reference_node = None
    """ The import name reference node """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_import_name_reference_node(self, import_name_reference_node):
        self.import_name_reference_node = import_name_reference_node

class FunctionNode(ExpressionNode):
    """
    The function node class.
    """

    function_operators_node = None
    """ The function operators node """

    function_name = None
    """ The function name """

    function_arguments_node = None
    """ The function arguments node """

    statements_node = None
    """ The statements node """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_function_operators_node(self, function_operators_node):
        self.function_operators_node = function_operators_node
        self.add_child_node(function_operators_node)

    def set_function_name(self, function_name):
        self.function_name = function_name

    def set_function_arguments_node(self, function_arguments_node):
        self.function_arguments_node = function_arguments_node
        self.add_child_node(function_arguments_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

    def is_static(self):
        """
        Returns if the function is of type static or not.
        
        @rtype: bool
        @return: The result of the static type test.
        """

        if not self.function_operators_node.is_valid():
            return False

        # iterates over all the function operators nodes
        for function_operators_node_item in self.function_operators_node:
            # retrieves the function operator node 
            function_operator_node = function_operators_node_item.function_operator_node

            if function_operator_node.function_operator_name == "static":
                return True

        return False

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("function", self):
            return

        visitor.push_current_context_type("function", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("function", self):
            return

        visitor.push_current_context_type("function", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class FunctionOperatorsNode(AstSequenceNode):
    """
    The function operators node class.
    """

    function_operator_node = None
    """ The function operator node """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_function_operator_node(self, function_operator_node):
        self.function_operator_node = function_operator_node
        self.add_child_node(function_operator_node)

class FunctionOperatorNode(AstNode):
    """
    The function operator node class.
    """

    function_operator_name = None
    """ The function operator name """

    def __init__(self):
        AstNode.__init__(self)

    def set_function_operator_name(self, function_operator_name):
        self.function_operator_name = function_operator_name

class StaticFunctionOperatorNode(FunctionOperatorNode):
    """
    The static function operator node class.
    """

    def __init__(self):
        FunctionOperatorNode.__init__(self)
        self.set_function_operator_name("static")

class ArgumentsNode(AstSequenceNode):
    """
    The arguments node class.
    """

    argument_node = None
    """ The argument node """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_argument_node(self, argument_node):
        self.argument_node = argument_node
        self.add_child_node(argument_node)

class ArgumentNode(AstNode):
    """
    The argument node class.
    """

    name = None
    """ The name """

    def __init__(self):
        AstNode.__init__(self)

    def set_name(self, name):
        self.name = name

class DefaultValueArgumentNode(ArgumentNode):
    """
    The default value argument node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        ArgumentNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

class FunctionCallNode(AstNode):
    """
    The function call node class.
    """

    function_name_reference_node = None
    """ The function name reference node """

    function_argument_values_node = None
    """ The function argument values node """

    def __init__(self):
        AstNode.__init__(self)

    def set_function_name_reference_node(self, function_name_reference_node):
        self.function_name_reference_node = function_name_reference_node
        self.add_child_node(function_name_reference_node)

    def set_function_argument_values_node(self, function_argument_values_node):
        self.function_argument_values_node = function_argument_values_node
        self.add_child_node(function_argument_values_node)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("function_call", self):
            return

        visitor.push_current_context_type("function_call", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("function_call", self):
            return

        visitor.push_current_context_type("function_call", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class ArgumentValuesNode(AstSequenceNode):
    """
    The argument values node class.
    """

    argument_value_node = None
    """ The argument value node """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_argument_value_node(self, argument_value_node):
        self.argument_value_node = argument_value_node
        self.add_child_node(argument_value_node)

class ArgumentValueNode(AstNode):
    """
    The argument value node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        AstNode.__init__(self)

    def set_expression_node(self, expression_node):
        self.expression_node = expression_node
        self.add_child_node(expression_node)

class ClassNode(ExpressionNode):
    """
    The class node class.
    """

    class_name = None
    """ The class name """

    extends_node = None
    """ The extends node """

    implements_node = None
    """ The implements node """

    statements_node = None
    """ The statements node """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_class_name(self, class_name):
        self.class_name = class_name

    def set_extends_node(self, extends_node):
        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_implements_node(self, implements_node):
        self.implements_node = implements_node
        self.add_child_node(implements_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("class", self):
            return

        visitor.push_current_context_type("class", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("class", self):
            return

        visitor.push_current_context_type("class", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class ExtendsNode(AstNode):
    """
    The extends node class.
    """

    extends_values_node = None
    """ The extends values node """

    def __init__(self):
        AstNode.__init__(self)

    def set_extends_values_node(self, extends_values_node):
        self.extends_values_node = extends_values_node
        self.add_child_node(extends_values_node)

class ExtendsValuesNode(AstSequenceNode):
    """
    The extends values node class.
    """

    extends_values_name = None
    """ The extends values name """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_extends_values_name(self, extends_values_name):
        self.extends_values_name = extends_values_name

class ImplementsNode(AstNode):
    """
    The implements node class.
    """

    implements_values_node = None
    """The implements values node """

    def __init__(self):
        AstNode.__init__(self)

    def set_implements_values_node(self, implements_values_node):
        self.implements_values_node = implements_values_node
        self.add_child_node(implements_values_node)

class ImplementsValuesNode(AstSequenceNode):
    """
    The implements values node class.
    """

    implements_values_name = None
    """ The implements values name """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_implements_values_name(self, implements_values_name):
        self.implements_values_name = implements_values_name

class InterfaceNode(ExpressionNode):
    """
    The interface node class.
    """

    interface_name = None
    """ The interface name """

    extends_node = None
    """ The extends node """

    statements_node = None
    """ The statements node """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_interface_name(self, interface_name):
        self.interface_name = interface_name

    def set_extends_node(self, extends_node):
        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

class PluginNode(ExpressionNode):
    """
    The plugin node class.
    """

    plugin_name = None
    """ The plugin name """

    extends_node = None
    """ The extends node """

    implements_node = None
    """ The implements node """

    allows_node = None
    """ The allows node """

    statements_node = None
    """ The statements node """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_plugin_name(self, plugin_name):
        self.plugin_name = plugin_name

    def set_extends_node(self, extends_node):
        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_implements_node(self, implements_node):
        self.implements_node = implements_node
        self.add_child_node(implements_node)

    def set_allows_node(self, allows_node):
        self.allows_node = allows_node
        self.add_child_node(allows_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("plugin", self):
            return

        visitor.push_current_context_type("plugin", self)

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        visitor.pop_current_context_type(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.
        
        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if not visitor.valid_context_type("plugin", self):
            return

        visitor.push_current_context_type("plugin", self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        visitor.pop_current_context_type(self)

class AllowsNode(AstNode):
    """
    The allows node class.
    """

    allows_values_node = None
    """The allows values node """

    def __init__(self):
        AstNode.__init__(self)

    def set_allows_values_node(self, allows_values_node):
        self.allows_values_node = allows_values_node
        self.add_child_node(allows_values_node)

class AllowsValuesNode(AstSequenceNode):
    """
    The allows values node class.
    """

    allows_values_name = None
    """ The allows values name """

    def __init__(self):
        AstSequenceNode.__init__(self)

    def set_allows_values_name(self, allows_values_name):
        self.allows_values_name = allows_values_name

class CapabilityNode(ExpressionNode):
    """
    The capability node class.
    """

    capability_name = None
    """ The capability name """

    extends_node = None
    """ The extends node """

    statements_node = None
    """ The statements node """

    def __init__(self):
        ExpressionNode.__init__(self)

    def set_capability_name(self, capability_name):
        self.capability_name = capability_name

    def set_extends_node(self, extends_node):
        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_statements_node(self, statements_node):
        self.statements_node = statements_node
        self.add_child_node(statements_node)

class AstSequenceNodeIterator:
    """
    The ast sequence node iterator class.
    """

    ast_sequence_node = None
    """ The ast sequence node """

    def __init__(self, ast_sequence_node):
        self.ast_sequence_node = ast_sequence_node

    def __iter__(self):
        return self

    def next(self):
        # retrieves the current ast sequence node
        current_ast_sequence_node = self.ast_sequence_node

        # in case the current ast sequence node is None or an ast sequence end node
        if current_ast_sequence_node == None or current_ast_sequence_node.__class__ == AstSequenceEndNode:
            # breaks the iteration
            raise StopIteration()

        # retrieves the next ast sequence node
        next_ast_sequence_node = self.ast_sequence_node.next_node

        # sets the next ast sequence node as the new ast sequence node
        self.ast_sequence_node = next_ast_sequence_node

        # returns the current ast sequence node
        return current_ast_sequence_node
