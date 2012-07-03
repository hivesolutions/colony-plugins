#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 516 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-28 14:30:47 +0000 (Sex, 28 Nov 2008) $"
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

class RootNode(AstNode):
    """
    The root node class.
    """

    def __init__(self):
        AstNode.__init__(self)

class LiteralNode(AstNode):
    """
    The literal node class.
    """

    def __init__(self, value = None):
        AstNode.__init__(self)

        self.value = value

class MatchNode(AstNode):
    """
    The match node class.
    """

    value_type = None
    """ The value type """

    attributes_map = {}
    """ The attributes map """

    attribute_regex = None
    """ The attribute regular expression """

    attribute_literal_regex = None
    """ The attribute literal regular expression """

    def __init__(self, value = None, attribute_regex = None, attribute_literal_regex = None):
        AstNode.__init__(self)

        self.value = value
        self.attribute_regex = attribute_regex
        self.attribute_literal_regex = attribute_literal_regex

        self.attributes_map = {}

        self.process_value_type()
        self.process_attributes_map()

    def process_value_type(self):
        # retrieve the start match value
        start_match_value = self.get_start_match_value()

        # retrieves the start match value match value
        start_match_value_match_value = start_match_value.get_match_value()

        # splits the start match value match value
        start_match_value_match_value_splitted = start_match_value_match_value.split()

        # retrieves the value type from the start match value match value splitted
        self.value_type = start_match_value_match_value_splitted[0][2:]

    def process_attributes_map(self):
        # retrieve the start match value
        start_match_value = self.get_start_match_value()

        # retrieves the start match value match value
        start_match_value_match_value = start_match_value.get_match_value()

        # finds all the attributes matches
        attributes_matches = self.attribute_regex.finditer(start_match_value_match_value)

        # finds all the attributes literal matches
        attributes_literal_matches = self.attribute_literal_regex.finditer(start_match_value_match_value)

        # iterates over all the attributes matches
        for attribute_match in attributes_matches:
            # retrieves the attribute value
            attribute = attribute_match.group()

            # splits the attribute around the equals sign
            attribute_splitted = attribute.split("=")

            # retrieves the attribute name and value
            attribute_name, attribute_value = attribute_splitted

            # sets the attribute in the attributes map
            self.attributes_map[attribute_name] = {
                "value" : attribute_value,
                "type" : "variable"
            }

        # iterates over all the attributes literal matches
        for attribute_literal_match in attributes_literal_matches:
            # retrieves the attribute literal value
            attribute_literal = attribute_literal_match.group()

            # splits the attribute literal around the equals sign
            attribute_literal_splitted = attribute_literal.split("=")

            # retrieves the attribute literal name and value
            attribute_literal_name, attribute_literal_value = attribute_literal_splitted

            # retrieves the attribute matching group index
            attribute_group_index = attribute_literal_match.lastindex

            # in case it's quoted
            if attribute_group_index == 1:
                attribute_literal_value = attribute_literal_value.strip("'")
            if attribute_group_index == 2:
                attribute_literal_value = attribute_literal_value.strip("\"")
            # in case it's float
            elif attribute_group_index == 3:
                attribute_literal_value = float(attribute_literal_value)
            # in case it's integer
            elif attribute_group_index == 4:
                attribute_literal_value = int(attribute_literal_value)
            # in case it's boolean and true
            elif attribute_group_index == 5:
                attribute_literal_value = True
            # in case it's boolean and false
            elif attribute_group_index == 6:
                attribute_literal_value = False
            # in case it's none
            elif attribute_group_index == 7:
                attribute_literal_value = None

            # sets the attribute literal in the attributes map
            self.attributes_map[attribute_literal_name] = {
                "value" : attribute_literal_value,
                "type" : "literal"
            }

    def get_value_type(self):
        return self.value_type

    def set_value_type(self, value_type):
        self.value_type = value_type

    def get_attributes_map(self):
        return self.attributes_map

    def set_attributes_map(self, attributes_map):
        self.attributes_map = attributes_map

class SingleNode(MatchNode):
    """
    The single node class.
    """

    def __init__(self, value = None, attribute_regex = None, attribute_literal_regex = None):
        MatchNode.__init__(self, value, attribute_regex, attribute_literal_regex)

    def get_start_match_value(self):
        return self.value

    def accept(self, visitor):
        # retrieves the value type
        value_type = self.get_value_type()

        # calls the process accept method with the value type
        visitor.process_accept(self, value_type)

class CompositeNode(MatchNode):
    """
    The composite node class.
    """

    def __init__(self, value = None, attribute_regex = None, attribute_literal_regex = None):
        MatchNode.__init__(self, value, attribute_regex, attribute_literal_regex)

    def get_start_match_value(self):
        return self.value[0]

    def accept(self, visitor):
        # retrieves the value type
        value_type = self.get_value_type()

        # calls the process accept method with the value type
        visitor.process_accept(self, value_type)
