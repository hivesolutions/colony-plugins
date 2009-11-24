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

    indent = False
    """ The indentation level """

    child_nodes = []
    """ The list of child nodes """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.child_nodes = []

    def __repr__(self):
        """
        Returns the default representation of the class.

        @rtype: String
        @return: The default representation of the class.
        """

        return "<ast_node indent:%s child_nodes:%s>" % (self.indent, len(self.child_nodes))

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
        """
        Sets the value value.

        @type value: Object
        @para value: The value value.
        """

        self.value = value

    def set_indent(self, indent):
        """
        Sets the indent value.

        @type indent: int
        @param indent: The indent value.
        """

        self.indent = indent

    def add_child_node(self, child_node):
        """
        Adds a child node to the node.

        @type child_node: AstNode
        @param child_node: The child node to be added.
        """

        self.child_nodes.append(child_node)

    def remove_child_node(self, child_node):
        """
        Removes a child node from the node.

        @type child_node: AstNode
        @param child_node: The child node to be removed.
        """

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
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def __iter__(self):
        """
        Returns the iterator object for sequence iteration.

        @rtype: AstSequenceNodeIterator
        @return: The iterator object for sequence iteration.
        """

        # creates the ast sequence node iterator
        ast_sequence_node_iterator = AstSequenceNodeIterator(self)

        # returns the ast sequence node iterator
        return ast_sequence_node_iterator

    def set_next_node(self, next_node):
        """
        Sets the next node.

        @type next_node: AstSequenceNode
        @param next_node: The next node.
        """

        self.next_node = next_node

    def get_last_node(self):
        """
        Retrieves the last node.

        @rtype: AstSequenceNode
        @return: The last node.
        """

        # sets the current sequence node
        sequence_node = self

        # retrieves the next sequence node
        next_sequence_node = self.next_node

        while not next_sequence_node == None:
            sequence_node = next_sequence_node
            next_sequence_node = sequence_node.next_node

        return sequence_node

    def get_all_nodes(self):
        """
        Retrieves all the nodes in the sequence.

        @rtype: List
        @return: All the nodes in the sequence.
        """

        # constructs the nodes list
        nodes_list = [value for value in self]

        # returns the nodes list
        return nodes_list

    def count(self):
        """
        Counts the number of nodes in the sequence.

        @rtype: int
        @return: The number of nodes in the sequence.
        """

        # retrieve all nodes
        all_nodes = self.get_all_nodes()

        # calculates the length of all nodes
        length_all_nodes = len(all_nodes)

        # returns the length of all nodes
        return length_all_nodes

    def is_valid(self):
        """
        Retrieves if a node is valid or not.

        @rtype: bool
        @return: The is valid value.
        """

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
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)
        self.valid = False

class RootNode(AstNode):
    """
    The root node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class ProgramNode(RootNode):
    """
    The program node class.
    """

    statements_node = None
    """ The statements node """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootNode.__init__(self)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class StatementsNode(AstSequenceNode):
    """
    The statements node class.
    """

    statement_node = None
    """ The statement node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_statement_node(self, statement_node):
        """
        Sets the statement node.

        @type statement_node: StatementNode
        @param statement_node: The statement node.
        """

        self.statement_node = statement_node
        self.add_child_node(statement_node)

class StatementNode(AstNode):
    """
    The statement node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class CommentNode(StatementNode):
    """
    The comment node class.
    """

    comment_value = "none"
    """ The comment value """

    statement_node = None
    """ The statement node """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_comment_value(self, comment_value):
        """
        Sets the comment value.

        @type comment_value: String
        @param comment_value: The comment value.
        """

        self.comment_value = comment_value

    def set_statement_node(self, statement_node):
        """
        Sets the statement node.

        @type statement_node: StatementNode
        @param statement_node: The statement node.
        """

        self.statement_node = statement_node
        self.add_child_node(statement_node)

class PassNode(StatementNode):
    """
    The pass node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

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
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_name_reference_node(self, name_reference_node):
        """
        Sets the name reference node.

        @type name_reference_node: NameReferenceNode
        @param name_reference_node: The name reference node.
        """

        self.name_reference_node = name_reference_node
        self.add_child_node(name_reference_node)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

        self.expression_node = expression_node
        self.add_child_node(expression_node)

class ReturnNode(StatementNode):
    """
    The return node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

        self.expression_node = expression_node
        self.add_child_node(expression_node)

class GlobalNode(StatementNode):
    """
    The global node class.
    """

    name = None
    """ The name """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_name(self, name):
        """
        Sets the name value.

        @type name: String
        @param name: The name value.
        """

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
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

        self.expression_node = expression_node
        self.add_child_node(expression_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

    def set_else_condition_node(self, else_condition_node):
        """
        Sets the else condition node.

        @type else_condition_node: ElseConditionNode
        @param else_condition_node: The else condition node.
        """

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
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class ElseIfConditionNode(ElseConditionNode):
    """
    The else if condition node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ElseConditionNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

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
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

        self.expression_node = expression_node
        self.add_child_node(expression_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

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
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_item_name(self, item_name):
        """
        Sets the item name.

        @type item_name: String
        @param item_name: The item name.
        """

        self.item_name = item_name

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

        self.expression_node = expression_node
        self.add_child_node(expression_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class ExpressionNode(StatementNode):
    """
    The expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

class NumberExpressionNode(ExpressionNode):
    """
    The number expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

class IntegerExpressionNode(NumberExpressionNode):
    """
    The integer expression node class.
    """

    integer_value = None
    """ The integer value """

    def __init__(self):
        """
        Constructor of the class.
        """

        NumberExpressionNode.__init__(self)

    def set_integer_value(self, integer_value):
        """
        Sets the integer value.

        @type integer_value: int
        @param integer_value: The integer value.
        """

        self.integer_value = integer_value

class StringExpressionNode(ExpressionNode):
    """
    The string expression node class.
    """

    string_value = None
    """ The string value """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_string_value(self, string_value):
        """
        Sets the string value.

        @type string_value: String
        @param string_value: The string value.
        """

        self.string_value = string_value

class BoolExpressionNode(ExpressionNode):
    """
    The bool expression node class.
    """

    bool_value = None
    """ The bool value """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_bool_value(self, bool_value):
        """
        Sets the bool value.

        @type bool_value: bool
        @param bool_value: The bool value.
        """

        self.bool_value = bool_value

class NameExpressionNode(ExpressionNode):
    """
    The name expression node class.
    """

    name_reference_node = None
    """ The name reference node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_name_reference_node(self, name_reference_node):
        """
        Sets the name reference node.

        @type name_reference_node: NameReferenceNode
        @param name_reference_node: The name reference node.
        """

        self.name_reference_node = name_reference_node
        self.add_child_node(name_reference_node)

class ListExpressionNode(ExpressionNode):
    """
    The list expression node class.
    """

    list_contents_node = None
    """ The list contents node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_list_contents_node(self, list_contents_node):
        """
        Sets the list contents node.

        @type list_contents_node: ListContentsNode
        @param list_contents_node: The list contents node.
        """

        self.list_contents_node = list_contents_node
        self.add_child_node(list_contents_node)

class ListContentsNode(AstSequenceNode):
    """
    The list contents node.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

        self.expression_node = expression_node
        self.add_child_node(expression_node)

class UnaryExpressionNode(ExpressionNode):
    """
    The unary expression node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

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
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_first_expression_node(self, first_expression_node):
        """
        Sets the first expression node.

        @type first_expression_node: ExpressionNode
        @param first_expression_node: The first expression node.
        """

        self.first_expression_node = first_expression_node
        self.add_child_node(first_expression_node)

    def set_second_expression_node(self, second_expression_node):
        """
        Sets the second expression node.

        @type second_expression_node: ExpressionNode
        @param second_expression_node: The second expression node.
        """

        self.second_expression_node = second_expression_node
        self.add_child_node(second_expression_node)

class ArithmethicExpressionNode(BinaryExpressionNode):
    """
    The arithmetic expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryExpressionNode.__init__(self)

class SummationExpressionNode(ArithmethicExpressionNode):
    """
    The summation expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ArithmethicExpressionNode.__init__(self)

class SubtractionExpressionNode(ArithmethicExpressionNode):
    """
    The subtraction expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ArithmethicExpressionNode.__init__(self)

class MultiplicationExpressionNode(ArithmethicExpressionNode):
    """
    The multiplication expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ArithmethicExpressionNode.__init__(self)

class DivisionExpressionNode(ArithmethicExpressionNode):
    """
    The division expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ArithmethicExpressionNode.__init__(self)

class PowerExpressionNode(ArithmethicExpressionNode):
    """
    The power expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ArithmethicExpressionNode.__init__(self)

class BooleanExpressionNode(BinaryExpressionNode):
    """
    The boolean expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryExpressionNode.__init__(self)

class EqualExpressionNode(BooleanExpressionNode):
    """
    The equal expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BooleanExpressionNode.__init__(self)

class GreaterExpressionNode(BooleanExpressionNode):
    """
    The greater expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BooleanExpressionNode.__init__(self)

class GreaterEqualExpressionNode(BooleanExpressionNode):
    """
    The greater equal expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BooleanExpressionNode.__init__(self)

class AndExpressionNode(BooleanExpressionNode):
    """
    The and expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

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
        """
        Constructor of the class.
        """

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
        """
        Constructor of the class.
        """

        UnaryExpressionNode.__init__(self)

class ParenthesisExpressionNode(UnaryExpressionNode):
    """
    The parenthesis expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

class NegativeExpressionNode(UnaryExpressionNode):
    """
    The negative expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

class NameReferenceNode(AstSequenceNode):
    """
    The name reference node.
    """

    name_reference = None
    """ The name reference """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_name_reference(self, name_reference):
        """
        Sets the name reference.

        @type name_reference: String
        @param name_reference: The name reference.
        """

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
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_import_name_reference_node(self, import_name_reference_node):
        """
        Sets the import name reference node.

        @type import_name_reference_node: NameReferenceNode
        @param import_name_reference_node: The import name reference node.
        """

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
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_function_operators_node(self, function_operators_node):
        """
        Sets the function operators node.

        @type function_operators_node: FunctionOperatorsNode
        @param function_operators_node: The function operators node.
        """

        self.function_operators_node = function_operators_node
        self.add_child_node(function_operators_node)

    def set_function_name(self, function_name):
        """
        Sets the function name.

        @type function_name: String
        @param function_name: The function name.
        """

        self.function_name = function_name

    def set_function_arguments_node(self, function_arguments_node):
        """
        Sets the function arguments node.

        @type function_arguments_node: FunctionArgumentsNode
        @param function_arguments_node: The function arguments node.
        """

        self.function_arguments_node = function_arguments_node
        self.add_child_node(function_arguments_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class FunctionOperatorsNode(AstSequenceNode):
    """
    The function operators node class.
    """

    function_operator_node = None
    """ The function operator node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_function_operator_node(self, function_operator_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.function_operator_node = function_operator_node
        self.add_child_node(function_operator_node)

class FunctionOperatorNode(AstNode):
    """
    The function operator node class.
    """

    function_operator_name = None
    """ The function operator name """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_function_operator_name(self, function_operator_name):
        """
        Sets the function operator name.

        @type function_operator_name: String
        @param function_operator_name: The function operator name.
        """

        self.function_operator_name = function_operator_name

class StaticFunctionOperatorNode(FunctionOperatorNode):
    """
    The static function operator node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        FunctionOperatorNode.__init__(self)
        self.set_function_operator_name("static")

class ArgumentsNode(AstSequenceNode):
    """
    The arguments node class.
    """

    argument_node = None
    """ The argument node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_argument_node(self, argument_node):
        """
        Sets the argument node.

        @type argument_node: ArgumentNode
        @param argument_node: The argument node.
        """

        self.argument_node = argument_node
        self.add_child_node(argument_node)

class ArgumentNode(AstNode):
    """
    The argument node class.
    """

    name = None
    """ The name """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_name(self, name):
        """
        Sets the name value.

        @type name: String
        @param name: The name value.
        """

        self.name = name

class DefaultValueArgumentNode(ArgumentNode):
    """
    The default value argument node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ArgumentNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

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
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_function_name_reference_node(self, function_name_reference_node):
        """
        Sets the function name reference node.

        @type function_name_reference_node: NameReferenceNode
        @param function_name_reference_node: The name reference node.
        """

        self.function_name_reference_node = function_name_reference_node
        self.add_child_node(function_name_reference_node)

    def set_function_argument_values_node(self, function_argument_values_node):
        """
        Sets the function argument values node.

        @type function_argument_values_node: ArgumentValuesNode
        @param function_argument_values_node: The function argument values node.
        """

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
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_argument_value_node(self, argument_value_node):
        """
        Sets the argument value node.

        @type argument_value_node: ArgumentValueNode
        @param argument_value_node: The argument value node.
        """

        self.argument_value_node = argument_value_node
        self.add_child_node(argument_value_node)

class ArgumentValueNode(AstNode):
    """
    The argument value node class.
    """

    expression_node = None
    """ The expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_expression_node(self, expression_node):
        """
        Sets the expression node.

        @type expression_node: ExpressionNode
        @param expression_node: The expression node.
        """

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
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_class_name(self, class_name):
        """
        Sets the class name.

        @type class_name: String
        @param class_name: The class name.
        """

        self.class_name = class_name

    def set_extends_node(self, extends_node):
        """
        Sets the extends node.

        @type extends_node: ExtendsNode
        @param extends_node: The extends node.
        """

        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_implements_node(self, implements_node):
        """
        Sets the implements node.

        @type implements_node: ImplementsNode
        @param implements_node: The implements node.
        """

        self.implements_node = implements_node
        self.add_child_node(implements_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

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
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_extends_values_node(self, extends_values_node):
        """
        Sets the extends values node.

        @type extends_values_node: ExtendsValuesNode
        @param extends_values_node: The extends values node.
        """

        self.extends_values_node = extends_values_node
        self.add_child_node(extends_values_node)

class ExtendsValuesNode(AstSequenceNode):
    """
    The extends values node class.
    """

    extends_values_name = None
    """ The extends values name """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_extends_values_name(self, extends_values_name):
        """
        Sets the extends values name.

        @type extends_values_name: String
        @param extends_values_name: The extends values name.
        """

        self.extends_values_name = extends_values_name

class ImplementsNode(AstNode):
    """
    The implements node class.
    """

    implements_values_node = None
    """The implements values node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_implements_values_node(self, implements_values_node):
        """
        Sets the implements values node.

        @type implements_values_node: ImplementsValuesNode
        @param implements_values_node: The implements values node.
        """

        self.implements_values_node = implements_values_node
        self.add_child_node(implements_values_node)

class ImplementsValuesNode(AstSequenceNode):
    """
    The implements values node class.
    """

    implements_values_name = None
    """ The implements values name """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_implements_values_name(self, implements_values_name):
        """
        Sets the implements values name.

        @type implements_values_name: String
        @param implements_values_name: The implements values name.
        """

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
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_interface_name(self, interface_name):
        """
        Sets the interface name.

        @type interface_name: String
        @param interface_name: The interface name.
        """

        self.interface_name = interface_name

    def set_extends_node(self, extends_node):
        """
        Sets the extends node.

        @type extends_node: ExtendsNode
        @param extends_node: The extends node.
        """

        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

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
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_plugin_name(self, plugin_name):
        """
        Sets the plugin name.

        @type plugin_name: String
        @param plugin_name: The plugin name.
        """

        self.plugin_name = plugin_name

    def set_extends_node(self, extends_node):
        """
        Sets the extends node.

        @type extends_node: ExtendsNode
        @param extends_node: The extends node.
        """

        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_implements_node(self, implements_node):
        """
        Sets the implements node.

        @type implements_node: ImplementsNode
        @param implements_node: The implements node.
        """

        self.implements_node = implements_node
        self.add_child_node(implements_node)

    def set_allows_node(self, allows_node):
        """
        Sets the allows node.

        @type allows_node: AllowsNode
        @param allows_node: The allows node.
        """

        self.allows_node = allows_node
        self.add_child_node(allows_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

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
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_allows_values_node(self, allows_values_node):
        """
        Sets the allows values node.

        @type allows_values_node: AllowsValuesNode
        @param allows_values_node: The allows values node.
        """

        self.allows_values_node = allows_values_node
        self.add_child_node(allows_values_node)

class AllowsValuesNode(AstSequenceNode):
    """
    The allows values node class.
    """

    allows_values_name = None
    """ The allows values name """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_allows_values_name(self, allows_values_name):
        """
        Sets the allows values name.

        @type allows_values_name: String
        @param allows_values_name: The allows values name.
        """

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
        """
        Constructor of the class.
        """

        ExpressionNode.__init__(self)

    def set_capability_name(self, capability_name):
        """
        Sets the capability name.

        @type capability_name: String
        @param capability_name: The capability name.
        """

        self.capability_name = capability_name

    def set_extends_node(self, extends_node):
        """
        Sets the extends node.

        @type extends_node: ExtendsNode
        @param extends_node: The extends node.
        """

        self.extends_node = extends_node
        self.add_child_node(extends_node)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class SpaceNode(AstNode):
    """
    The space node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class AstSequenceNodeIterator:
    """
    The ast sequence node iterator class.
    """

    ast_sequence_node = None
    """ The ast sequence node """

    def __init__(self, ast_sequence_node):
        """
        Constructor of the class.

        @type ast_sequence_node: AstSequenceNode
        @param ast_sequence_node: The ast sequence node for the iterator.
        """

        self.ast_sequence_node = ast_sequence_node

    def __iter__(self):
        """
        Returns the iterator object for sequence iteration.

        @rtype: AstSequenceNodeIterator
        @return: The iterator object for sequence iteration.
        """

        return self

    def next(self):
        """
        Retrieves the next ast sequence node.

        @rtype: AstSequenceNode
        @return: The next ast sequence node.
        """

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
