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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
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

import language_wiki.libs.extension_system
import language_wiki.libs.string_buffer_util

class WikiDiagramExtension(language_wiki.libs.extension_system.Extension):
    """
    The wiki diagram extension class.
    """

    pass

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

        # initializes the string buffer
        string_buffer = language_wiki.libs.string_buffer_util.StringBuffer()

        # retrieves the view box width
        view_box_width = graphics_attributes["view_box_width"]

        # retrieves the view box height
        view_box_height = graphics_attributes["view_box_height"]

        # retrieves the width attribute
        width = graphics_attributes["width"]

        # retrieves the height attribute
        height = graphics_attributes["height"]

        # retrieves the class attribute
        style_class = graphics_attributes["class"]

        if self.graphics_open:
            return

        # starts the svg open tag
        string_buffer.write("<svg:svg version=\"1.1\" baseProfile=\"full\"")

        # adds the style class
        string_buffer.write(" class=\"%s\"" % style_class)

        # adds the view box specification
        string_buffer.write(" viewBox=\"0 0 %f %f\"" % (view_box_width, view_box_height))

        # adds the width specification
        if not width == None:
            string_buffer.write(" width=\"%s\"" % width)

        # adds the height specification
        if not height == None:
            string_buffer.write(" height=\"%s\"" % height)

        # finishes the svn open tag
        string_buffer.write(">")

        # retrieves the string value from the string buffer
        string_value = string_buffer.get_value()

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

    def generate_elements(self, graphics_elements):
        # initializes the string buffer
        string_buffer = language_wiki.libs.string_buffer_util.StringBuffer()

        # for each graphics element
        for graphics_element in graphics_elements:
            # retrieves the graphics element type and attributes
            graphics_element_type, graphics_element_attributes = graphics_element

            # creates the graphics for the graphics element
            graphics_element_string = self.generate_element(graphics_element_type, graphics_element_attributes)

            # adds the graphics element string to the string buffer
            string_buffer.write(graphics_element_string)

        # retrieves the string value
        string_value = string_buffer.get_value()

        return string_value

    def generate_element(self, graphics_element_type, graphics_element_attributes):
        if graphics_element_type == "viewport":
            return self.generate_viewport(graphics_element_attributes)
        elif graphics_element_type == "rectangle":
            return self.generate_rectangle(graphics_element_attributes)
        elif graphics_element_type == "text":
            return self.generate_text(graphics_element_attributes)

    def generate_viewport(self, graphics_attributes):
        x = graphics_attributes["x"]
        y = graphics_attributes["y"]
        width = graphics_attributes["width"]
        height = graphics_attributes["height"]
        child_graphic_elements = graphics_attributes["childs"]

        # create the viewport element
        open_viewport_element_string = "<svg:svg x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"%.1f\">" % (x, y, width, height)

        child_elements_string = self.generate_elements(child_graphic_elements)

        close_viewport_element_string = "</svg:svg>"

        return open_viewport_element_string + child_elements_string + close_viewport_element_string

    def generate_rectangle(self, graphics_attributes):
        x = graphics_attributes["x"]
        y = graphics_attributes["y"]
        width = graphics_attributes["width"]
        height = graphics_attributes["height"]
        options = graphics_attributes["options"]

        # retrieves the style class
        style_class = options.get("class", "")

        # create the rectangle element
        rectangle_element_string = "<svg:rect class=\"%s\" x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"%.1f\"/>" % (style_class, x, y, width, height)

        return rectangle_element_string

    def generate_text(self, graphics_attributes):
        # initializes the string buffer
        string_buffer = language_wiki.libs.string_buffer_util.StringBuffer()

        # retrieves the x
        x = graphics_attributes["x"]

        # retrieves the y
        y = graphics_attributes["y"]

        # retrieves the text
        text = graphics_attributes["text"]

        # escapes the retrieved text
        escaped_text = self.visitor.escape_string_value(text)

        # retrieves the graphic element options
        options = graphics_attributes["options"]

        # opens the text tag
        string_buffer.write("<svg:text")

        # writes the options
        for options_name, option_value in options.items():
            string_buffer.write(" %s=\"%s\"" % (options_name, option_value))

        # opens the text element
        string_buffer.write(" x=\"%.1f\" y=\"%.1f\"" % (x, y))

        string_buffer.write(">")

        # writes the escaped text
        string_buffer.write(escaped_text)

        # closes the text element
        string_buffer.write("</svg:text>")

        # retrieves the string value
        string_value = string_buffer.get_value()

        return string_value

    def get_visitor(self):
        return self.visitor

    def set_visitor(self, visitor):
        self.visitor = visitor
