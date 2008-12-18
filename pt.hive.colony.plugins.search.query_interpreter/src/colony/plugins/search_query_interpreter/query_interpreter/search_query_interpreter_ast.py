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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class AstNode:
    """
    The ast node class.
    """

    value = None
    """ The value """

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

        return "<ast_node value:%s child_nodes:%s>" % (self.value, len(self.child_nodes))

    def set_value(self, value):
        """
        Sets the value value.
        
        @type value: Object
        @para value: The value value.
        """

        self.value = value

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

class QueryNode(AstNode):
    """
    The query node.
    """

    term_node = None
    """ The term node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_term_node(self, term_node):
        """
        Sets the term node.
        
        @type term_node: TermNode
        @param term_node: The term node.
        """

        self.term_node = term_node
        self.add_child_node(term_node)

class BooleanQueryNode(QueryNode):

    query_node = None
    """ The query node """

    def __init__(self):
        """
        Constructor of the class.
        """

        QueryNode.__init__(self)

    def set_query_node(self, term_node):
        """
        Sets the query node.
        
        @type query_node: QueryNode
        @param query_node: The query node.
        """

        self.query_node = query_node
        self.add_child_node(query_node)

class AndBooleanQueryNode(BooleanQueryNode):
    """
    The and boolean query node.
    """

    def __init__(self):
        BooleanQueryNode.__init__(self)

class OrBooleanQueryNode(BooleanQueryNode):

    def __init__(self):
        BooleanQueryNode.__init__(self)

class TermNode(AstNode):

    term_value = None

    def __init__(self):
        AstNode.__init__(self)

    def set_term_value(self, term_value):
        self.term_value = term_value
        self.set_value(term_value)

class QuotedNode(TermNode):

    term_value_list = []

    def __init__(self):
        TermNode.__init__(self)
        self.term_value_list = []

    def set_term_value(self, term_value):
        TermNode.set_term_value(self, term_value)
        self.term_value_list = self.term_value.split()
