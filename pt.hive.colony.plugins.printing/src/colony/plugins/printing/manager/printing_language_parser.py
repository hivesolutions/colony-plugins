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

__revision__ = "$LastChangedRevision: 1089 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-22 23:19:39 +0000 (qui, 22 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import xml.dom.minidom

import printing_language_ast

class Parser:
    """
    The abstract parser class
    """

    def __init__(self):
        """
        Constructor of the class
        """

        pass

    def parse(self):
        """
        Parses the defined file
        """

        pass

    def get_value(self):
        """
        Retrieves the result of the parse

        @rtype: Object
        @return: The result of the parse
        """

        pass

    def parse_element_attributes(self, node, element):
        attributes = node.attributes

        for index in range(attributes.length):
            attribute_node = attributes.item(index)
            attribute_node_name = attribute_node.name
            attribute_node_value = attribute_node.value
            setattr(element, attribute_node_name, attribute_node_value)

class PrintingLanguageParser(Parser):
    """
    The printing language parser class.
    """

    file = None
    """ The file path """

    string = None
    """ The string contents """

    printing_document = None
    """ The printing document """

    def __init__(self, file = None, string = "none"):
        Parser.__init__(self)
        self.file = file
        self.string = string

    def parse(self):
        self.load_printing_language_file(self.file)

    def parse_string(self):
        self.load_printing_language_string(self.string)

    def get_value(self):
        return self.printing_document

    def get_build_automation(self):
        return self.printing_document

    def load_printing_language_file(self, file):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file)

        self.load_printing_language(xml_document)

    def load_printing_language_string(self, string):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parseString(string)

        self.load_printing_language(xml_document)

    def load_printing_language(self, xml_document):
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.printing_document = self.parse_printing_document(child_node)

    def parse_printing_document(self, printing_document):
        printing_document_structure = printing_language_ast.PrintingDocument()
        child_nodes = printing_document.childNodes

        # parses the element attributes
        self.parse_element_attributes(printing_document, printing_document_structure)

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_printing_document_element(child_node, printing_document_structure)

        return printing_document_structure

    def parse_printing_document_element(self, printing_document_element, printing_document):
        node_name = printing_document_element.nodeName
        printing_document_child_nodes = printing_document.child_nodes

        if node_name == "paragraph":
            printing_document_child_nodes.append(self.parse_paragraph(printing_document_element))
        elif node_name == "line":
            printing_document_child_nodes.append(self.parse_line(printing_document_element))
        elif node_name == "text":
            printing_document_child_nodes.append(self.parse_text(printing_document_element))
        elif node_name == "image":
            printing_document_child_nodes.append(self.parse_image(printing_document_element))

    def parse_paragraph(self, paragraph):
        paragraph_structure = printing_language_ast.Paragraph()
        child_nodes = paragraph.childNodes

        # parses the element attributes
        self.parse_element_attributes(paragraph, paragraph_structure)

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_paragraph_element(child_node, paragraph_structure)

        return paragraph_structure

    def parse_paragraph_element(self, paragraph_element, paragraph):
        node_name = paragraph_element.nodeName
        paragraph_child_nodes = paragraph.child_nodes

        if node_name == "line":
            paragraph_child_nodes.append(self.parse_line(paragraph_element))
        elif node_name == "text":
            paragraph_child_nodes.append(self.parse_text(paragraph_element))
        elif node_name == "image":
            paragraph_child_nodes.append(self.parse_image(paragraph_element))

    def parse_line(self, line):
        line_structure = printing_language_ast.Line()
        child_nodes = line.childNodes

        # parses the element attributes
        self.parse_element_attributes(line, line_structure)

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_line_elements(child_node, line_structure)

        return line_structure

    def parse_line_elements(self, line_element, line):
        node_name = line_element.nodeName
        line_child_nodes = line.child_nodes

        if node_name == "text":
            line_child_nodes.append(self.parse_text(line_element))
        elif node_name == "image":
            line_child_nodes.append(self.parse_image(line_element))

    def parse_text(self, text):
        text_structure = printing_language_ast.Text()

        # parses the element attributes
        self.parse_element_attributes(text, text_structure)

        if text.firstChild:
            text_structure.text = text.firstChild.data.strip()
        else:
            text_structure.text = str()

        return text_structure

    def parse_image(self, image):
        image_structure = printing_language_ast.Image()

        # parses the element attributes
        self.parse_element_attributes(image, image_structure)

        return image_structure

def valid_node(node):
    """
    Gets if a node is valid or not for parsing.

    @type node: Node
    @param node: The Xml node to be validated.
    @rtype: bool
    @return: The valid or not valid value.
    """

    # in case the node is of type element
    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        # returns true (valid)
        return True
    # otherwise
    else:
        # returns false (invalid)
        return False
