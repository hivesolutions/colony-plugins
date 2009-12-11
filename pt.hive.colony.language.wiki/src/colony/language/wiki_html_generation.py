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
import time
import copy
import cStringIO

import libs.string_buffer_util

import wiki_ast
import wiki_visitor
import wiki_exceptions

DOCTYPE_HEADER_VALUE = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
""" The doctype header value """

META_HEADER_VALUE = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">"
""" The meta header value """

CSS_HEADER_VALUE = "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/main.css\" />"
""" The css header value """

RECURSION_LIMIT = 1000000
""" The recursion limit """

SIMPLE_PARSE_VALUE = "simple_parse"
""" The simple parse value """

GENERATE_FOOTER_VALUE = "generate_footer"
""" The generate footer value """

AUTO_NUMBERED_SECTIONS_VALUE = "auto_numbered_sections"
""" The auto numbered sections value """

AVAILABLE_TAG_NAMES = ("del",)
""" The available tag names """

class HtmlGenerationVisitor(wiki_visitor.Visitor):
    """
    The html generation visitor class.
    """

    start_time = None
    """ The start time value """

    end_time = None
    """ The end time value """

    string_buffer = None
    """ The string buffer """

    extension_manager = None
    """ The extension manager """

    paragraph_open = False
    """ The paragraph open flag """

    current_section_string = "none"
    """ The current section string """

    section_values_map = {}
    """ The sections values map """

    configuration_map = {}
    """ The configuration map """

    previous_recursion_limit = None
    """ The previous recursion limit value """

    def __init__(self):
        wiki_visitor.Visitor.__init__(self)

        # creates the string buffer
        self.string_buffer = libs.string_buffer_util.StringBuffer()

        # starts the section values map
        self.section_values_map = {}

        # starts the configuration map
        self.configuration_map = {}

    def new_parse(self, contents, configuration_map, string_buffer = None):
        # in case the string buffer is not defined
        if not string_buffer:
            # sets the string buffer
            string_buffer = self.string_buffer

        # parses the contents retrieving the parse result
        parse_result = self.parser.parse(contents)

        # clones the visitor
        cloned_visitor = self.clone()

        # sets the string buffer in the cloned visitor
        cloned_visitor.set_string_buffer(string_buffer)

        # retrieves the configuration map
        cloned_configuration_map = cloned_visitor.get_configuration_map()

        # iterates over all the configuration keys in the configuration map
        for configuration_key in configuration_map:
            # retrieves the configuration value for the configuration key
            configuration_value = configuration_map[configuration_key]

            # sets the configuration property in the cloned configuration map
            cloned_configuration_map[configuration_key] = configuration_value

        # accepts the double visit
        parse_result.accept_double(cloned_visitor)

    def clone(self):
        """
        Clones the visitor.

        @rtype: Visitor
        @return: The cloned visitor.
        """

        # clones the current visitor
        cloned_visitor = wiki_visitor.Visitor.clone(self)

        # cones the configuration map
        clone_configuration_map = copy.copy(self.configuration_map)

        # sets the visitor attributes in the cloned visitor
        cloned_visitor.set_string_buffer(self.string_buffer)
        cloned_visitor.set_extension_manager(self.extension_manager)
        cloned_visitor.set_configuration_map(clone_configuration_map)

        # returns the cloned visitor
        return cloned_visitor

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

    def get_extension_manager(self):
        """
        Retrieves the extension manager.

        @rtype: ExtensionManager
        @return: The extension manager.
        """

        return self.extension_manager

    def set_extension_manager(self, extension_manager):
        """
        Sets the string buffer.

        @type extension_manager: ExtensionManager
        @param extension_manager: The extension manager.
        """

        self.extension_manager = extension_manager

    def get_configuration_map(self):
        """
        Retrieves the configuration map.

        @rtype: Dictionary
        @return: The configuration map.
        """

        return self.configuration_map

    def set_configuration_map(self, configuration_map):
        """
        Sets the configuration map.

        @type configuration_map: Dictionary
        @param configuration_map: The configuration map.
        """

        self.configuration_map = configuration_map

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
            # retrieves the current recursion limit and saves it
            self.previous_recursion_limit = sys.getrecursionlimit()

            # sets the new recursion limit
            sys.setrecursionlimit(RECURSION_LIMIT)

            # in case the simple parse is not valid
            if not self.configuration_map.get(SIMPLE_PARSE_VALUE, False):
                # writes the doc type header
                self._write(DOCTYPE_HEADER_VALUE)

                # writes the head
                self._write("<head>")

                # writes the meta header value
                self._write(META_HEADER_VALUE)

                # writes the css header value
                self._write(CSS_HEADER_VALUE)

                # writes the head end
                self._write("</head>")

                # writes the body
                self._write("<body>")

                # opens a paragraph
                self.open_paragraph()

            # in case the start time is not defined
            if not self.start_time:
                # sets the start time
                self.start_time = time.time()
        elif self.visit_index == 1:
            # sets the end time
            self.end_time = time.time()

            # calculates the delta time
            delta_time = self.end_time - self.start_time

            # rounds the delta time
            delta_time_rounded = round(delta_time, 2)

            # sets the previous recursion limit
            sys.setrecursionlimit(self.previous_recursion_limit)

            # in case the generate footer is valid
            if self.configuration_map.get(GENERATE_FOOTER_VALUE, False):
                self._write("<div class=\"footer\">")
                self._write("Document generated be colony framework in %s seconds" % str(delta_time_rounded))
                self._write("<div class=\"logo_image\">")
                self._write("<img src=\"images/logo_omni.gif\"/>")
                self._write("</div>")
                self._write("</div>")
            # in case the simple parse is not valid
            if not self.configuration_map.get(SIMPLE_PARSE_VALUE, False):
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
            self._write("<code class=\"monospace\">")
        elif self.visit_index == 1:
            self._write("</code>")

    @wiki_visitor._visit(wiki_ast.SectionNode)
    def visit_section_node(self, node):
        if self.visit_index == 0:
            # retrieves the node section size
            node_section_size = node.section_size

            # in case the section size is not available in
            # the section values map
            if not node.section_size in self.section_values_map:
                # creates the section size in the section values map
                self.section_values_map[node_section_size] = 0

            # increments the section values map
            self.section_values_map[node_section_size] += 1

            # creates the value
            string_value = str()

            # iterates over all the index in the section size range
            for index in range(node_section_size):
                # calculates the next index
                next_index = index + 1

                # in case the next index does not exists
                # in the section values map
                if not next_index in self.section_values_map:
                    # creates the section size in the section values map
                    self.section_values_map[next_index] = 0

                # retrieves the next value from the section values map
                next_value = self.section_values_map[next_index]

                # adds the next value to the string value
                string_value += str(next_value) + "."

            # sets the current section string
            self.current_section_string = string_value

            # closes the current paragraph
            self.close_paragraph()

            self._write("<h" + str(node.section_size) + " id=\"" + self.current_section_string + "\">")

            # in case the auto numbered sections is valid
            if self.configuration_map.get(AUTO_NUMBERED_SECTIONS_VALUE, False):
                self._write(self.current_section_string)
        elif self.visit_index == 1:
            self._write("<a class=\"headerlink\" title=\"Permalink to this headline\" href=\"#" + self.current_section_string + "\">¶</a>")
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
            self._write("<a class=\"external\" href=\"" + node.link_value + "\">")

            # in case the statements node is not defined
            if not node.statements_node:
                self._write(node.link_value)
        elif self.visit_index == 1:
            self._write("</a>")

    @wiki_visitor._visit(wiki_ast.InternalLinkNode)
    def visit_internal_link_node(self, node):
        if self.visit_index == 0:
            self._write("<a class=\"internal\" href=\"" + node.link_value + ".html\">")

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
            self._write("<div>")
        elif self.visit_index == 1:
            self._write("</div>")
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
            self._write("<div>")
        elif self.visit_index == 1:
            self._write("</div>")
            self._write("</li>")
            self._write("</ol>")

    @wiki_visitor._visit(wiki_ast.TagNode)
    def visit_tag_node(self, node):
        if self.visit_index == 0:
            # retrieves the tag name
            node_tag_name = node.tag_name

            # retrieves the tag contents
            node_tag_contents = node.contents

            # in case the node tag name is in
            # the available tag names
            if node_tag_name in AVAILABLE_TAG_NAMES:
                self._write("<" + node_tag_name + ">")
                self._write(node_tag_contents)
                self._write("</" + node_tag_name + ">")
            else:
                # retrieves the generator extensions
                generator_extensions = self.extension_manager.get_extensions_by_capability("generator")

                # splits the node tag name
                node_tag_name_splitted = node_tag_name.split()

                # retrieves the node tag name splitted length
                node_tag_name_splitted_length = len(node_tag_name_splitted)

                # in case the length of the node tag name
                # splitted is less than one
                if node_tag_name_splitted_length < 1:
                    # raisers the invalid tag name exception
                    raise wiki_exceptions.InvalidTagName("tag name is not valid: " + node_tag_name)

                # retrieves the node tag value
                node_tag_value = node_tag_name_splitted[0]

                # retrieves the generator extensions for the given tag
                tag_generator_extensions = [extension for extension in generator_extensions if extension.get_generator_type() == node_tag_value]

                # iterates over all the tag generator extensions
                for tag_generator_extension in tag_generator_extensions:
                    # generates the html for the given tag node
                    html = tag_generator_extension.generate_html(node, self)

                    # writes the html to the buffer
                    self._write(html)

    def _write(self, string_value):
        """
        Writes the given string value to the string buffer.

        @type string_value: String
        @param string_value: The string value to be written
        to the string buffer.
        """

        self.string_buffer.write(string_value)

    def open_paragraph(self):
        """
        Opens the paragraph.
        """

        if self.paragraph_open:
            return

        self._write("<p>")
        self.paragraph_open = True

    def close_paragraph(self):
        """
        Closes the paragraph.
        """

        if not self.paragraph_open:
            return

        self._write("</p>")
        self.paragraph_open = False

    def escape_string_value(self, string_value):
        """
        Escapes the given string value.

        @type string_value: String
        @param string_value: The string value to be escaped.
        @rtype: String
        @return: The escaped string value.
        """

        # strips the string value
        string_value = string_value.strip()

        # replaces the less than characters in the string value
        string_value = string_value.replace("<", "&lt;")

        # replaces the greater than characters in the string value
        string_value = string_value.replace(">", "&gt;")

        # replaces the newlines in the string value
        string_value = string_value.replace("\n", "<br/>")

        # replaces the spaces in the string value
        string_value = string_value.replace(" ", "&nbsp;")

        # returns the string value
        return string_value
