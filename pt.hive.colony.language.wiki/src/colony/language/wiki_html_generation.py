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

import sys
import cStringIO

import wiki_ast
import wiki_visitor

class HtmlGenerationVisitor(wiki_visitor.Visitor):
    """
    The html generation visitor class.
    """

    string_buffer = None
    """ The string buffer """

    def __init__(self):
        wiki_visitor.Visitor.__init__(self)

        # starts the current element node stack
        self.current_element_node_stack = []

        # creates the string buffer
        self.string_buffer = cStringIO.StringIO()

    def get_string_buffer(self):
        """
        Retrieves the string buffer.

        @rtype: File
        @return: The string buffer.
        """

        return self.string_buffer

    def set_string_buffer(self, string_buffer):
        """
        Sets the string buffer.

        @type string_buffer: File
        @param string_buffer: The string buffer.
        """

        self.string_buffer = string_buffer

    @wiki_visitor._visit(wiki_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.RootNode)
    def visit_root_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.ProgramNode)
    def visit_program_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.StatementsNode)
    def visit_statements_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.StatementNode)
    def visit_statement_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.BoldNode)
    def visit_bold_node(self, node):
        if self.visit_index == 0:
            self.string_buffer.write("<b>")
        elif self.visit_index == 1:
            self.string_buffer.write("</b>")

    @wiki_visitor._visit(wiki_ast.ItalicNode)
    def visit_italic_node(self, node):
        if self.visit_index == 0:
            self.string_buffer.write("<i>")
        elif self.visit_index == 1:
            self.string_buffer.write("</i>")

    @wiki_visitor._visit(wiki_ast.UnderlineNode)
    def visit_underline_node(self, node):
        if self.visit_index == 0:
            self.string_buffer.write("<u>")
        elif self.visit_index == 1:
            self.string_buffer.write("</u>")

    @wiki_visitor._visit(wiki_ast.MonospaceNode)
    def visit_monospace_node(self, node):
        if self.visit_index == 0:
            self.string_buffer.write("<span class=\"monospace\">")
        elif self.visit_index == 1:
            self.string_buffer.write("</span>")

    @wiki_visitor._visit(wiki_ast.NameNode)
    def visit_name_node(self, node):
        if self.visit_index == 0:
            self.string_buffer.write(node.name_value + " ")

    @wiki_visitor._visit(wiki_ast.NewLineNode)
    def visit_new_line_node(self, node):
        if self.visit_index == 0:
            self.string_buffer.write("</br>")
