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

import libs.string_buffer_util

import wiki_ast
import wiki_visitor

DOCTYPE_HEADER_VALUE = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
""" The doctype header value """

META_HEADER_VALUE = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">"
""" The meta header value """

CSS_HEADER_VALUE = "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/main.css\" />"
""" The css header value """

class HtmlGenerationVisitor(wiki_visitor.Visitor):
    """
    The html generation visitor class.
    """

    string_buffer = None
    """ The string buffer """

    paragraph_open = False
    """ The paragraph open flag """

    section_values_map = {}
    """ The sections values map """

    def __init__(self):
        wiki_visitor.Visitor.__init__(self)

        # starts the section values map
        self.section_values_map = {}

        # creates the string buffer
        self.string_buffer = libs.string_buffer_util.StringBuffer()

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
        if self.visit_index == 0:
            self._write(DOCTYPE_HEADER_VALUE)
            self._write("<head>")
            self._write(META_HEADER_VALUE)
            self._write(CSS_HEADER_VALUE)
            self._write("</head>")
            self._write("<body>")
            self.open_paragraph()
        elif self.visit_index == 1:
            self._write("</body>")

    @wiki_visitor._visit(wiki_ast.StatementsNode)
    def visit_statements_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.StatementNode)
    def visit_statement_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.BoldNode)
    def visit_bold_node(self, node):
        if self.visit_index == 0:
            self._write("<b>")
        elif self.visit_index == 1:
            self._write("</b>")

    @wiki_visitor._visit(wiki_ast.ItalicNode)
    def visit_italic_node(self, node):
        if self.visit_index == 0:
            self._write("<i>")
        elif self.visit_index == 1:
            self._write("</i>")

    @wiki_visitor._visit(wiki_ast.UnderlineNode)
    def visit_underline_node(self, node):
        if self.visit_index == 0:
            self._write("<u>")
        elif self.visit_index == 1:
            self._write("</u>")

    @wiki_visitor._visit(wiki_ast.MonospaceNode)
    def visit_monospace_node(self, node):
        if self.visit_index == 0:
            self._write("<span class=\"monospace\">")
        elif self.visit_index == 1:
            self._write("</span>")

    @wiki_visitor._visit(wiki_ast.SectionNode)
    def visit_section_node(self, node):
        if self.visit_index == 0:
            if not node.section_size in self.section_values_map:
                self.section_values_map[node.section_size] = 0

            self.section_values_map[node.section_size] += 1

            value = ""

            for index in range(node.section_size):
                if not index + 1 in self.section_values_map:
                    self.section_values_map[index + 1] = 0

                value += str(self.section_values_map[index + 1]) + "."

            # closes the current paragraph
            self.close_paragraph()
            self._write("<h" + str(node.section_size) + ">" + value + " ")
        elif self.visit_index == 1:
            self._write("</h" + str(node.section_size) + ">")

            # opens a new paragraph
            self.open_paragraph()

    @wiki_visitor._visit(wiki_ast.NameNode)
    def visit_name_node(self, node):
        if self.visit_index == 0:
            self._write(node.name_value)

    @wiki_visitor._visit(wiki_ast.NewLineNode)
    def visit_new_line_node(self, node):
        if self.visit_index == 0:
            self.close_paragraph()
            self.open_paragraph()

    @wiki_visitor._visit(wiki_ast.SpaceNode)
    def visit_space_node(self, node):
        if self.visit_index == 0:
            self._write(" ")

    @wiki_visitor._visit(wiki_ast.ImageNode)
    def visit_image_node(self, node):
        if self.visit_index == 0:
            self._write("<img src=\"" + node.image_source + "\"")

            # in case the image size is valid
            if node.image_size:
                # retrieves the image size
                image_size = node.image_size

                # retrieves the image size length
                image_size_length = len(image_size)

                # retrieves the image width
                image_width = node.image_size[0]

                # appends the image width to the string buffer
                self._write(" width=" + image_width)

                # in case the image size length is greater than one
                if image_size_length > 1:
                    # retrieves the image height
                    image_height = image_size[1]

                    # appends the image height to the string buffer
                    self._write(" height=" + image_height)

            self._write(">")

    @wiki_visitor._visit(wiki_ast.LinkNode)
    def visit_link_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.ExternalLinkNode)
    def visit_external_link_node(self, node):
        if self.visit_index == 0:
            self._write("<a href=\"" + node.link_value + "\">")

            # in case the statements node is not defined
            if not node.statements_node:
                self._write(node.link_value)
        elif self.visit_index == 1:
            self._write("</a>")

    @wiki_visitor._visit(wiki_ast.ListNode)
    def visit_list_node(self, node):
        pass

    @wiki_visitor._visit(wiki_ast.BulletListNode)
    def visit_bullet_list_node(self, node):
        if self.visit_index == 0:
            if self.string_buffer.get_last() == "</ul>":
                self.string_buffer.rollback_last()
            else:
                self._write("<ul>")

            self._write("<li>")
        elif self.visit_index == 1:
            self._write("</li>")
            self._write("</ul>")

    @wiki_visitor._visit(wiki_ast.OrderedListNode)
    def visit_ordered_list_node(self, node):
        if self.visit_index == 0:
            if self.string_buffer.get_last() == "</ol>":
                self.string_buffer.rollback_last()
            else:
                self._write("<ol>")

            self._write("<li>")
        elif self.visit_index == 1:
            self._write("</li>")
            self._write("</ol>")

    def _write(self, string_value):
        """
        Writes the given string value to the string buffer.

        @type string_value: String
        @param string_value: The string value to be written
        to the string buffer.
        """

        self.string_buffer.write(string_value)

    def close_paragraph(self):
        if not self.paragraph_open:
            return

        self._write("</p>")
        self.paragraph_open = False

    def open_paragraph(self):
        if self.paragraph_open:
            return

        self._write("<p>")
        self.paragraph_open = True
