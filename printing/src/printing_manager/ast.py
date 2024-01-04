#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """


class AstNode(object):
    """
    The AST node class.
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

        :rtype: String
        :return: The default representation of the class.
        """

        return "<ast_node indent:%s child_nodes:%s>" % (
            self.indent,
            len(self.child_nodes),
        )

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.

        :type visitor: Visitor
        :param visitor: The visitor object.
        """

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.

        :type visitor: Visitor
        :param visitor: The visitor object.
        """

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

    def accept_double(self, visitor):
        """
        Accepts the visitor running the iteration logic, using double visiting.

        :type visitor: Visitor
        :param visitor: The visitor object.
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

        :type value: Object
        @para value: The value value.
        """

        self.value = value

    def set_indent(self, indent):
        """
        Sets the indent value.

        :type indent: int
        :param indent: The indent value.
        """

        self.indent = indent

    def add_child_node(self, child_node):
        """
        Adds a child node to the node.

        :type child_node: AstNode
        :param child_node: The child node to be added.
        """

        self.child_nodes.append(child_node)

    def remove_child_node(self, child_node):
        """
        Removes a child node from the node.

        :type child_node: AstNode
        :param child_node: The child node to be removed.
        """

        self.child_nodes.remove(child_node)


class GenericElement(AstNode):
    """
    The generic element class.
    """

    element_name = "none"

    def __init__(self, element_name="none"):
        AstNode.__init__(self)
        self.element_name = element_name


class PrintingDocument(AstNode):
    """
    The printing document class.
    """

    def __init__(self):
        AstNode.__init__(self)


class Block(AstNode):
    """
    The block class.
    """

    def __init__(self):
        AstNode.__init__(self)


class Paragraph(AstNode):
    """
    The paragraph class.
    """

    def __init__(self):
        AstNode.__init__(self)


class Line(AstNode):
    """
    The line class.
    """

    def __init__(self):
        AstNode.__init__(self)


class Text(AstNode):
    """
    The text class.
    """

    def __init__(self):
        AstNode.__init__(self)


class Image(AstNode):
    """
    The image class.
    """

    def __init__(self):
        AstNode.__init__(self)
