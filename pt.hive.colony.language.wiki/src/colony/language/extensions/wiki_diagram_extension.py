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

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import libs.string_buffer_util

import wiki_extension_system

import wiki_diagram.wiki_diagram_extension_system

GENERATOR_TYPE = "diagram"
""" The generator type """

class WikiDiagramExtension(wiki_extension_system.WikiExtension):
    """
    The wiki diagram extension class.
    """

    id = "pt.hive.colony.language.wiki.extensions.diagram"
    """ The extension id """

    name = "Diagram Generation Plugin"
    """ The name of the extension """

    short_name = "Diagram Generation"
    """ The short name of the extension """

    description = "Extension for diagram generation"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = ["generator"]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    extension_manager = None
    """ The extension manager """

    def __init__(self, manager = None):
        """
        Constructor of the class.

        @type manager: ExtensionManager
        @param manager: The parent extension manager.
        """

        wiki_extension_system.WikiExtension.__init__(self, manager)

        # creates a new extension manager
        self.extension_manager = libs.extension_system.ExtensionManager(["./extensions/wiki_diagram/extensions"])
        self.extension_manager.set_extension_class(wiki_diagram.wiki_diagram_extension_system.WikiDiagramExtension)
        self.extension_manager.start_logger()
        self.extension_manager.load_system()

    def get_generator_type(self):
        """
        Retrieves the generator type.

        @rtype: String
        @return: The generator type.
        """

        return GENERATOR_TYPE

    def generate_html(self, tag_node, visitor):
        """
        Generates the html code for the given tag node.

        @type tag_node: TagNode
        @param tag_node: The tag node to be processed.
        @type visitor: Visitor
        @param visitor: The requester visitor.
        @rtype: String
        @return: The generated html code.
        """

        # retrieves the tag contents
        contents = tag_node.contents

        # creates the string buffer
        string_buffer = libs.string_buffer_util.StringBuffer()

        # retrieves the code highlighting extensions
        diagram_extensions = self.extension_manager.get_extensions_by_capability("diagram")

        # retrieves the tag name
        node_tag_name = tag_node.tag_name

        # retrieves the tag attributes map
        node_attributes_map = tag_node.attributes_map

        # retrieves the tag attributes map keys
        node_attributes_map_keys = node_attributes_map.keys()

        # retrieves the type
        diagram_type = node_attributes_map.get("type", "none")

        # in case the diagram type is not specified
        if not diagram_type:
            # raisers the invalid tag name exception
            raise wiki_exceptions.InvalidTagName("tag name is not valid: " + node_tag_name)

        # retrieves the title
        node_tag_title = node_attributes_map.get("title", "none")

        # retrieves the diagram extensions for the given tag
        node_tag_diagram_extensions = [extension for extension in diagram_extensions if extension.get_diagram_type() == diagram_type]

        # writes the start div diagram tag
        string_buffer.write("<div class=\"diagram\" style=\"display: block;\">")

        # writes the title
        string_buffer.write("<h1>" + node_tag_title + "</h1>")

        # generates the diagrams using the available extensions
        for node_tag_diagram_extension in node_tag_diagram_extensions:
            # retrieves the tokens list
            graphics_elements = node_tag_diagram_extension.get_graphics_elements(contents)

            # creates the vector graphics support
            vector_graphics = ScalableVectorGraphics()

            # sets the visitor in the vector graphics
            vector_graphics.set_visitor(visitor)

            # diagram type style class
            diagram_type_style_class = diagram_type + "-diagram"

            # starts the graphics
            open_graphics_string = vector_graphics.open_graphics({"class" : diagram_type_style_class, "width" : 600, "height" : 300})

            # writes the open graphics tag
            string_buffer.write(open_graphics_string)

            # for each graphics element
            for graphics_element in graphics_elements:
                # retrieves the graphics element type and attributes
                graphics_element_type, graphics_element_attributes = graphics_element

                # creates the graphics for the graphics element
                graphics_element_string = vector_graphics.generate_element(graphics_element_type, graphics_element_attributes)

                # adds the graphics element string to the string buffer
                string_buffer.write(graphics_element_string)

            # stops the graphics
            close_graphics_string = vector_graphics.close_graphics()

            # writes the close graphics tag
            string_buffer.write(close_graphics_string)

        # writes the end div diagram tag
        string_buffer.write("</div>")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

class AbstractVectorGraphics:
    def __init__(self):
        pass

    def open_graphics(self):
        """
        Opens the graphics.
        """

        pass

    def close_graphics(self):
        """
        Closes the graphics.
        """

        pass

    def get_visitor(self):
        pass

    def set_visitor(self, visitor):
        pass

class ScalableVectorGraphics(AbstractVectorGraphics):
    def __init__(self):
        self.graphics_open = False
        self.visitor = None

    def open_graphics(self, graphics_attributes):
        """
        Opens the graphics.
        """

        # retrieves the width attribute
        width = graphics_attributes["width"]

        # retrieves the height attribute
        height = graphics_attributes["height"]

        # retrieves the class attribute
        style_class = graphics_attributes["class"]

        if self.graphics_open:
            return

        # creates the string value for the open graphics
        string_value = "<svg:svg class=\"%s\" version=\"1.1\" baseProfile=\"full\" width=\"%f px\" height=\"%f px\">" % (style_class, width, height)

        # signals the graphics tag is open
        self.graphics_open = True

        return string_value

    def close_graphics(self):
        """
        Closes the graphics.
        """

        if not self.graphics_open:
            return

        # creates the string value for the close graphics
        string_value = "</svg:svg>"

        # signals the graphics tag is closed
        self.graphics_open = False

        return string_value

    def generate_element(self, graphics_element_type, graphics_element_attributes):
        if graphics_element_type == "rectangle":
            return self.generate_rectangle(graphics_element_attributes)
        elif graphics_element_type == "text":
            return self.generate_text(graphics_element_attributes)

    def generate_rectangle(self, graphics_attributes):
        x = graphics_attributes["x"]
        y = graphics_attributes["y"]
        width = graphics_attributes["width"]
        height = graphics_attributes["height"]
        options = graphics_attributes["options"]

        # retrieves the style class
        style_class = options.get("class", "")

        # @todo: build the element string gradually
        rectangle_element_string = "<svg:rect class=\"%s\" x=\"%f\" y=\"%f\" width=\"%f\" height=\"%f\"/>" % (style_class, x, y, width, height)

        return rectangle_element_string

    def generate_text(self, graphics_attributes):
        x = graphics_attributes["x"]
        y = graphics_attributes["y"]
        text = graphics_attributes["text"]
        escaped_text = self.visitor.escape_string_value(text)
        options = graphics_attributes["options"]

        # retrieves the style class
        style_class = options.get("class", "")

        # @todo: build the element string gradually
        text_element_string = "<svg:text class=\"{%s}\" x=\"{%f} \" y=\"{%f}\">{%s}</svg:text>" % (style_class, x, y, escaped_text)

        return text_element_string

    def get_visitor(self):
        return self.visitor

    def set_visitor(self, visitor):
        self.visitor = visitor
