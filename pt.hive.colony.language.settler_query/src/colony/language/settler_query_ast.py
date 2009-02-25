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

class EnumerationNode(AstNode):
    """
    The enumeration node class.
    """

    enumeration_value = "none"
    """ The enumeration value """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_enumeration_value(self, enumeration_value):
        """
        Sets the enumeration value.
        
        @type enumeration_value: String
        @param enumeration_value: The enumeration value.
        """

        self.enumeration_value = enumeration_value

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

class PassNode(StatementNode):
    """
    The pass node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

class SelectNode(StatementNode):
    """
    The select node class.
    """
    
    optional_all_distinct_node = None
    """ The optional all distinct node """

    selection_node = None
    """ The selection node """

    entity_expression = None
    """ The entity expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_optional_all_distinct_node(self, optional_all_distinct_node):
        """
        Sets the optional all distinct node.
        
        @type optional_all_distinct_node: OptionalAllDistinctNode
        @param optional_all_distinct_node: The optional all distinct node.
        """

        self.optional_all_distinct_node = optional_all_distinct_node
        self.add_child_node(optional_all_distinct_node)

    def set_selection_node(self, selection_node):
        """
        Sets the selection node.
        
        @type selection_node: SelectionNode
        @param selection_node: The selection node.
        """

        self.selection_node = selection_node
        self.add_child_node(selection_node)

    def set_entity_expression_node(self, entity_expression_node):
        """
        Sets the entity expression node.
        
        @type entity_expression_node: EntityExpressionNode
        @param entity_expression_node: The entity expression node.
        """

        self.entity_expression_node = entity_expression_node
        self.add_child_node(entity_expression_node)

class OptionalAllDistinctNode(EnumerationNode):
    """
    The optional all distinct node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        EnumerationNode.__init__(self)

class SelectionNode(AstNode):
    """
    The selection node class.
    """

    scalar_expression_commalist_node = None
    """ The scalar expression commalist node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)
