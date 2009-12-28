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

import wiki_exceptions
import wiki_extension_system

import wiki_diagram.wiki_diagram_extension_system

GENERATOR_TYPE = "diagram"
""" The generator type """

DEFAULT_WIDTH_VALUE = "500px"
""" The default width value """

DEFAULT_HEIGHT_VALUE = None
""" The default height value """

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

    def __init__(self, manager = None, logger = None):
        """
        Constructor of the class.

        @type manager: ExtensionManager
        @param manager: The parent extension manager.
        @type logger: Logger
        @param logger: The extension manager logger.
        """

        wiki_extension_system.WikiExtension.__init__(self, manager, logger)

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

        # retrieves the width
        node_tag_width = node_attributes_map.get("width", DEFAULT_WIDTH_VALUE)

        # retrieves the height
        node_tag_height = node_attributes_map.get("height", DEFAULT_HEIGHT_VALUE)

        # retrieves the diagram extensions for the given tag
        node_tag_diagram_extensions = [extension for extension in diagram_extensions if extension.get_diagram_type() == diagram_type]

        # writes the start div diagram tag
        string_buffer.write("<div class=\"diagram\">")

        # generates the diagrams using the available extensions
        for node_tag_diagram_extension in node_tag_diagram_extensions:
            # retrieves the tokens list
            graphics_elements, viewport_size = node_tag_diagram_extension.get_graphics_elements(contents)

            # unpacks the view box dimensions
            view_box_width, view_box_height = viewport_size

            # creates the vector graphics support
            vector_graphics = wiki_diagram.wiki_diagram_extension_system.ScalableVectorGraphics()

            # sets the visitor in the vector graphics
            vector_graphics.set_visitor(visitor)

            # diagram type style class
            diagram_type_style_class = diagram_type + "-diagram"

            # starts the graphics
            open_graphics_string = vector_graphics.open_graphics({"class" : diagram_type_style_class, "width" : node_tag_width, "height" : node_tag_height, "view_box_width" : view_box_width, "view_box_height" : view_box_height})

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
