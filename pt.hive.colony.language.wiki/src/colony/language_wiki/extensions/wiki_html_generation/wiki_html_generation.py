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

import language_wiki.libs.string_buffer_util

import language_wiki.wiki_ast
import language_wiki.wiki_visitor
import language_wiki.wiki_exceptions

DEFAULT_RESOURCES_PATH = "resources"
""" The default resources path """

DOCTYPE_HEADER_VALUE = "<!DOCTYPE html>"
""" The doctype header value """

META_HEADER_VALUE = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\" />"
""" The meta header value """

CSS_HEADER_VALUE = "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/main.css\" />"
""" The css header value """

JS_HEADER_VALUE = "<script type=\"text/javascript\" src=\"js/main.js\"></script>"
""" The js header value """

RECURSION_LIMIT = 1000000
""" The recursion limit """

SIMPLE_PARSE_VALUE = "simple_parse"
""" The simple parse value """

GENERATE_FOOTER_VALUE = "generate_footer"
""" The generate footer value """

AUTO_NUMBERED_SECTIONS_VALUE = "auto_numbered_sections"
""" The auto numbered sections value """

MAXIMUM_SECTIONS_VALUE = 5
""" The maximum sections value """

ESCAPE_NAME_VALUE = "escape_name"
""" The escape name value """

AVAILABLE_TAG_NAMES = ("del",)
""" The available tag names """

INDEX_KEYS_LIST = ("Introduction", "Tutorials", "Standards &amp; Practices", "Design documents", "How-tos", "Demos")
""" The index keys list """

INDEX_MAP = {
    "Introduction" : {
        "order" : [
            "What is Colony?",
            "What Can I Build With Colony?",
            "How Can I Get Started?",
            "How Can I Help?",
            "Frequently Asked Questions"
        ],
        "items" : {
            "What is Colony?" : "documentation_what_is_colony.html",
            "What Can I Build With Colony?" : "documentation_what_can_i_build_with_colony.html",
            "How Can I Get Started?" : "documentation_how_can_i_get_started.html",
            "How Can I Help?" : "documentation_how_can_i_help.html",
            "Frequently Asked Questions" : "documentation_frequently_asked_questions.html"
        }
    },
    "Tutorials" : {
        "order" : [
            "Colony Hello World Tutorial",
            "Colony Web Hello World Tutorial",
            "Colony Web MVC Hello World Tutorial"
        ],
        "items" : {
            "Colony Hello World Tutorial" : "documentation_tutorial_colony_hello_world.html",
            "Colony Web Hello World Tutorial" : "documentation_tutorial_colony_web_hello_world.html",
            "Colony Web MVC Hello World Tutorial" : "documentation_tutorial_colony_web_mvc_hello_world.html"
        }
    },
    "Standards &amp; Practices" : {
        "order" : [
            "Colony Style Guide"
        ],
        "items" :  {
            "Colony Style Guide" : "documentation_colony_style_guide.html"
        }
    },
    "Design documents" : {
        "order" : [
            "Colony Plugin Framework",
            "Colony Web Plugin Framework",
            "Colony Web MVC Framework"
        ],
        "items" : {
            "Colony Plugin Framework" : "documentation_colony_plugin_framework.html",
            "Colony Web Plugin Framework" : "documentation_colony_web_plugin_framework.html",
            "Colony Web MVC Framework" : "documentation_colony_web_mvc_framework.html"
        }
    },
    "How-tos" : {
        "order" : [],
        "items" : {}
    },
    "Demos" : {
        "order" : [],
        "items" : {}
    }
}
""" The index map """

INDEX_PAGE = "index.html"
""" The index page """

BASE_LEVEL_VALUE = 0
""" The base level value """

class HtmlGenerationVisitor(language_wiki.wiki_visitor.Visitor):
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

    resources_paths_list = []
    """ The resources paths list """

    section_values_map = {}
    """ The sections values map """

    image_values_map = {}
    """ The image values map """

    configuration_map = {}
    """ The configuration map """

    previous_recursion_limit = None
    """ The previous recursion limit value """

    def __init__(self):
        language_wiki.wiki_visitor.Visitor.__init__(self)

        # creates the string buffer
        self.string_buffer = language_wiki.libs.string_buffer_util.StringBuffer()

        # start the resources paths list
        self.resources_paths_list = []

        # starts the section values map
        self.section_values_map = {}

        # start the image values map
        self.image_values_map = {}

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
        cloned_visitor = language_wiki.wiki_visitor.Visitor.clone(self)

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

    def get_resources_paths_list(self):
        """
        Retrieves the configuration map.

        @rtype: List
        @return: The resources paths list.
        """

        return self.resources_paths_list

    def set_resources_paths_list(self, resources_paths_list):
        """
        Sets the resources paths list.

        @type resources_paths_list: List
        @param resources_paths_list: The resources paths list.
        """

        self.resources_paths_list = resources_paths_list

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

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        pass

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.RootNode)
    def visit_root_node(self, node):
        pass

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.ProgramNode)
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

                # writes the html
                self._write("<html>")

                # writes the head
                self._write("<head>")

                # writes the meta header value
                self._write(META_HEADER_VALUE)

                # writes the css header value
                self._write(CSS_HEADER_VALUE)

                # writes the js header value
                self._write(JS_HEADER_VALUE)

                # writes the head end
                self._write("</head>")

                # writes the body
                self._write("<body>")

                # writes the wiki header
                self._write("<div id=\"wiki-header\">")
                self._write("<div class=\"wiki-header-contents\">")
                self._write("<div class=\"logo-image\">")
                self._write("<a href=\"" + INDEX_PAGE + "\">")
                self._write("<img src=\"images/colony_logo.png\"/>")
                self._write("</a>")
                self._write("</div>")
                self._write("<div class=\"menu-contents\">")
                self._write("<ul>")
                self._write("<li class=\"menu\"><a href=\"" + INDEX_PAGE + "\">Home</a></li>")
                self._write("<li class=\"menu menu-index\"><a id=\"index-opener\" href=\"#\" onclick=\"switchMenu(); return false;\">Index</a>")

                # generates the menu index
                self._generate_menu_index()

                self._write("</li>")
                self._write("<li class=\"menu\"><a href=\"documentation_how_can_i_help.html\">Contribute</a></li>")
                self._write("<li class=\"menu\"><a href=\"documentation_credits.html\">Credits</a></li>")
                self._write("</ul>")
                self._write("</div>")
                self._write("</div>")
                self._write("</div>")

                # writes the wiki contents
                self._write("<div id=\"wiki-contents\">")

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

            # closes the paragraph
            self.close_paragraph()

            # in case the generate footer is valid
            if self.configuration_map.get(GENERATE_FOOTER_VALUE, False):
                self._write("</div>")
                self._write("<div id=\"wiki-footer\">")
                self._write("<div class=\"wiki-footer-contents\">")
                self._write("<div class=\"logo-image\">")
                self._write("<a href=\"http://getcolony.com\"><img src=\"images/powered_by_colony.png\"/></a>")
                self._write("</div>")
                self._write("<div class=\"separator\">")
                self._write("<img src=\"images/separator.png\"/>")
                self._write("</div>")
                self._write("<div class=\"text-contents\">")
                self._write("Document generated by colony framework in %s seconds<br />" % str(delta_time_rounded))
                self._write("Copyright <a href=\"http://www.hive.pt\">Hive Solutions Lda.</a> distributed under <a href=\"http://creativecommons.org/licenses/by-sa/3.0\"> Creative Commons License</a>")
                self._write("</div>")
                self._write("</div>")
                self._write("</div>")

            # in case the simple parse is not valid
            if not self.configuration_map.get(SIMPLE_PARSE_VALUE, False):
                # closes the body
                self._write("</body>")

                # closes the html
                self._write("</html>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.StatementsNode)
    def visit_statements_node(self, node):
        pass

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.StatementNode)
    def visit_statement_node(self, node):
        pass

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.BoldNode)
    def visit_bold_node(self, node):
        if self.visit_index == 0:
            self._write("<b>")
        elif self.visit_index == 1:
            self._write("</b>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.ItalicNode)
    def visit_italic_node(self, node):
        if self.visit_index == 0:
            self._write("<i>")
        elif self.visit_index == 1:
            self._write("</i>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.UnderlineNode)
    def visit_underline_node(self, node):
        if self.visit_index == 0:
            self._write("<u>")
        elif self.visit_index == 1:
            self._write("</u>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.MonospaceNode)
    def visit_monospace_node(self, node):
        if self.visit_index == 0:
            self._write("<code class=\"monospace\">")
        elif self.visit_index == 1:
            self._write("</code>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.SectionNode)
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

            # iterates over all the next section values
            for index in range(node_section_size + 1, MAXIMUM_SECTIONS_VALUE):
                # resets the section size in the section values map
                self.section_values_map[index] = 0

            # sets the current section string
            self.current_section_string = string_value

            # closes the current paragraph
            self.close_paragraph()

            # writes the header value no the string value
            self._write("<h" + str(node.section_size) + " id=\"section-" + self.current_section_string + "\">")

            # in case the auto numbered sections is valid
            if self.configuration_map.get(AUTO_NUMBERED_SECTIONS_VALUE, False):
                self._write(self.current_section_string)
        elif self.visit_index == 1:
            self._write("<a class=\"headerlink\" title=\"Permalink to this headline\" href=\"#section-" + self.current_section_string + "\">¶</a>")
            self._write("</h" + str(node.section_size) + ">")

            # opens a new paragraph
            self.open_paragraph()

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.NameNode)
    def visit_name_node(self, node):
        if self.visit_index == 0:
            # retrieves the name value
            name_value = node.name_value

            # in case the name value is to be escaped
            if self.configuration_map.get(ESCAPE_NAME_VALUE, True):
                # escapes the name value
                name_value = self.escape_string_value(node.name_value)

            self._write(name_value)

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.NewLineNode)
    def visit_new_line_node(self, node):
        if self.visit_index == 0:
            self.close_paragraph()
            self.open_paragraph()

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.SpaceNode)
    def visit_space_node(self, node):
        if self.visit_index == 0:
            self._write(" ")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.ImageNode)
    def visit_image_node(self, node):
        if self.visit_index == 0:
            # in case the base vale is not available in
            # the image values map
            if not BASE_LEVEL_VALUE in self.image_values_map:
                # creates the base value in the image values map
                self.image_values_map[BASE_LEVEL_VALUE] = 0

            # increments the image values map
            self.image_values_map[BASE_LEVEL_VALUE] += 1

            # retrieves the current image value
            current_image_value = self.image_values_map[BASE_LEVEL_VALUE]

            # converts the current image value to string
            current_image_string = str(current_image_value)

            self._write("<div id=\"image-" + current_image_string + "\" class=\"image\">")
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

            self._write("/>")

            self._write("<p>")

            self._write("<span class=\"image-id\">Figure " + current_image_string + "</span>")

            # in case the statements node is defined
            if node.statements_node:
                self._write(" - ")

            # creates the resource path
            resource_path = DEFAULT_RESOURCES_PATH + "/" + node.image_source

            # adds the image resource to the resources paths list
            self.resources_paths_list.append(resource_path)
        elif self.visit_index == 1:
            self._write("</p>")
            self._write("</div>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.LinkNode)
    def visit_link_node(self, node):
        pass

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.ExternalLinkNode)
    def visit_external_link_node(self, node):
        if self.visit_index == 0:
            # retrieves the special names
            special_names = node.get_special_names()

            self._write("<a class=\"external")

            # iterates over all the special names
            for special_name in special_names:
                self._write(" " + special_name)

            self._write("\" href=\"" + node.link_value + "\">")

            # in case the statements node is not defined
            if not node.statements_node:
                self._write(node.link_value)
        elif self.visit_index == 1:
            self._write("</a>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.InternalLinkNode)
    def visit_internal_link_node(self, node):
        if self.visit_index == 0:
            self._write("<a class=\"internal\" href=\"" + node.link_value + ".html\">")

            # in case the statements node is not defined
            if not node.statements_node:
                self._write(node.link_value)
        elif self.visit_index == 1:
            self._write("</a>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.ListNode)
    def visit_list_node(self, node):
        pass

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.BulletListNode)
    def visit_bullet_list_node(self, node):
        if self.visit_index == 0:
            if self.string_buffer.get_last() == "</ul>":
                self.string_buffer.rollback_last()
            else:
                self._write("<ul>")

            self._write("<li class=\"indentation-" + str(node.indentation_value) + "\">")
            self._write("<div>")
        elif self.visit_index == 1:
            self._write("</div>")
            self._write("</li>")
            self._write("</ul>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.OrderedListNode)
    def visit_ordered_list_node(self, node):
        if self.visit_index == 0:
            if self.string_buffer.get_last() == "</ol>":
                self.string_buffer.rollback_last()
            else:
                self._write("<ol>")

            self._write("<li class=\"indentation-" + str(node.indentation_value) + "\">")
            self._write("<div>")
        elif self.visit_index == 1:
            self._write("</div>")
            self._write("</li>")
            self._write("</ol>")

    @language_wiki.wiki_visitor._visit(language_wiki.wiki_ast.TagNode)
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
                    raise language_wiki.wiki_exceptions.InvalidTagName("tag name is not valid: " + node_tag_name)

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

        # replaces the ands in the string value
        string_value = string_value.replace("&", "&amp;")

        # replaces the less than characters in the string value
        string_value = string_value.replace("<", "&lt;")

        # replaces the greater than characters in the string value
        string_value = string_value.replace(">", "&gt;")

        # replaces the newlines in the string value
        string_value = string_value.replace("\n", "<br />")

        # replaces the spaces in the string value
        string_value = string_value.replace(" ", "&nbsp;")

        # returns the string value
        return string_value

    def _generate_menu_index(self):
        """
        Generates the menu index.
        """

        self._write("<div id=\"index\" style=\"opacity: 0.0;visibility: hidden;\">")
        self._write("<hr/>")
        self._write("<dl>")

        # iterates over all the index keys in the index keys list
        for index_key in INDEX_KEYS_LIST:
            self._write("<dt>" + index_key + "</dt>")
            index_value = INDEX_MAP[index_key]

            # retrieves the index value order list
            index_value_order_list = index_value.get("order", [])

            # retrieves the index valu items map
            index_value_items_map = index_value.get("items", {})

            for index_value_key in index_value_order_list:
                index_value_value = index_value_items_map[index_value_key]

                self._write("<dd><a href=\"" + index_value_value + "\">" + index_value_key + "</a></dd>")

        self._write("</dl>")
        self._write("</div>")
