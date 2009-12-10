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

    def accept_double(self, visitor):
        """
        Accepts the visitor running the iteration logic, using double visiting.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit_index = 0
        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_double(visitor)

        visitor.visit_index = 1
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

    def accept_double(self, visitor):
        """
        Accepts the visitor running the iteration logic, using double visiting.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_double(visitor)

        if self.next_node:
            if visitor.visit_next:
                self.next_node.accept_double(visitor)

        visitor.visit(self)

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

class DecorationNode(StatementNode):
    """
    The decoration node class.
    """

    statements_node = None
    """ The statements node """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class BoldNode(DecorationNode):
    """
    The bold node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        DecorationNode.__init__(self)

class ItalicNode(DecorationNode):
    """
    The italic node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        DecorationNode.__init__(self)

class UnderlineNode(DecorationNode):
    """
    The underline node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        DecorationNode.__init__(self)

class MonospaceNode(DecorationNode):
    """
    The monospace node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        DecorationNode.__init__(self)

class SectionNode(DecorationNode):
    """
    The section node class.
    """

    section_size = None
    """ The section size """

    def __init__(self):
        """
        Constructor of the class.
        """

        DecorationNode.__init__(self)

    def set_section_size(self, section_size):
        """
        Sets the section size.

        @type section_size: int
        @param section_size: The section size.
        """

        self.section_size = section_size

class NameNode(StatementNode):
    """
    The name node class.
    """

    name_value = "none"
    """ The name value """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_name_value(self, name_value):
        """
        Sets the name value.

        @type name_value: String
        @param name_value: The name value.
        """

        self.name_value = name_value

class SpaceNode(StatementNode):
    """
    The space node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

class NewLineNode(StatementNode):
    """
    The new line node class.
    """

    forced = False
    """ The forced flag """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_forced(self, forced):
        """
        Sets the forced flag.

        @type forced: bool
        @param forced: The forced flag.
        """

        self.forced = forced

class ImageNode(StatementNode):
    """
    The image node class.
    """

    image_source = "none"
    """ The image source """

    image_size = None
    """ The image size """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_image_source(self, image_source):
        """
        Sets the image source.

        @type image_source: String
        @param image_source: The image source.
        """

        self.image_source = image_source

    def set_image_size(self, image_size):
        """
        Sets the image size.

        @type image_size: List
        @param image_size: The image size.
        """

        self.image_size = image_size

class LinkNode(StatementNode):
    """
    The link node class.
    """

    link_value = "none"
    """ The link value """

    statements_node = None
    """ The statements node """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_link_value(self, link_value):
        """
        Sets the link value.

        @type link_value: String
        @param link_value: The link value.
        """

        self.link_value = link_value

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class ExternalLinkNode(LinkNode):
    """
    The external link node.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        LinkNode.__init__(self)

class InternalLinkNode(LinkNode):
    """
    The internal link node.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        LinkNode.__init__(self)

class ListNode(StatementNode):
    """
    The list node.
    """

    indentation_value = None
    """ The indentation value """

    statements_node = None
    """ The statements node """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_indentation_value(self, indentation_value):
        """
        Sets the indentation value.

        @type indentation_value: int
        @param indentation_value: The indentation value
        """

        self.indentation_value = indentation_value

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class BulletListNode(ListNode):
    """
    The bullet list node.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ListNode.__init__(self)

class OrderedListNode(ListNode):
    """
    The ordered list node.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ListNode.__init__(self)

class TagNode(StatementNode):
    """
    The tag node.
    """

    tag_name = None
    """ The tag name """

    contents = None
    """ The contents """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_tag_name(self, tag_name):
        """
        Sets the statements node.

        @type tag_name: String
        @param tag_name: The tag name.
        """

        self.tag_name = tag_name

    def set_contents(self, contents):
        """
        Sets the contents.

        @type contents: String
        @param contents: The contents.
        """

        self.contents = contents

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
