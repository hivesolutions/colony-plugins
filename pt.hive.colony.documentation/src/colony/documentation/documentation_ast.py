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

class ProjectNode(AstNode):
    """
    The project node class.
    """

    project_name = "none"
    """ The project name """

    project_author = "none"
    """ The project author """

    project_description = "none"
    """ The project description """

    def __init__(self):
        AstNode.__init__(self)

    def set_project_name(self, project_name):
        """
        Sets the project name.

        @type project_name: String
        @param project_name: The project name.
        """

        self.project_name = project_name

    def set_project_author(self, project_author):
        """
        Sets the project author.

        @type project_author: String
        @param project_author: The project author.
        """

        self.project_author = project_author

    def set_project_description(self, project_description):
        """
        Sets the project description.

        @type project_description: String
        @param project_description: The project description.
        """

        self.project_description = project_description

class DocumentationElementNode(AstNode):
    """
    The documentation element node class.
    """

    name = "none"
    """ The name """

    description = "none"
    """ The description """

    file_reference = "none"
    """ The file reference """

    file_position = None
    """ The file position """

    def __init__(self):
        AstNode.__init__(self)

    def set_name(self, name):
        """
        Sets the name.

        @type name: String
        @param name: The name.
        """

        self.name = name

    def set_description(self, description):
        """
        Sets the description.

        @type description: String
        @param description: The description.
        """

        self.description = description

    def set_file_reference(self, file_reference):
        """
        Sets the file reference.

        @type file_reference: String
        @param file_reference: The file reference.
        """

        self.file_reference = file_reference

    def set_file_position(self, file_position):
        """
        Sets the file position.

        @type file_position: int
        @param file_position: The file position
        """

        self.file_position = file_position

class NamespaceNode(DocumentationElementNode):
    """
    The namespace node class.
    """

    def __init__(self):
        DocumentationElementNode.__init__(self)

class ClassNode(DocumentationElementNode):
    """
    The class node class.
    """

    parent_class_node = None
    """ The parent class node """

    def __init__(self):
        DocumentationElementNode.__init__(self)

    def set_parent_class_node(self, parent_class_node):
        """
        Sets the parent class node.

        @type parent_class_node: ClassNode
        @param parent_class_node: The parent class node.
        """

        self.parent_class_node = parent_class_node
        self.add_child_node(parent_class_node)

class FunctionNode(DocumentationElementNode):
    """
    The function node class.
    """

    def __init__(self):
        DocumentationElementNode.__init__(self)

class VariableNode(DocumentationElementNode):
    """
    The variable node class.
    """

    def __init__(self):
        DocumentationElementNode.__init__(self)

class ConstantNode(DocumentationElementNode):
    """
    The variable node class.
    """

    def __init__(self):
        DocumentationElementNode.__init__(self)
