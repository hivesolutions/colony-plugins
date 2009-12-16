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

import libs.extension_system

class WikiDiagramExtension(libs.extension_system.Extension):
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

        # retrieves the width attribute
        width = graphics_attributes["width"]

        # retrieves the height attribute
        height = graphics_attributes["height"]

        # retrieves the class attribute
        style_class = graphics_attributes["class"]

        if self.graphics_open:
            return

        # creates the string value for the open graphics
        string_value = "<svg:svg class=\"%s\" version=\"1.1\" baseProfile=\"full\" width=\"%fpx\" height=\"%fpx\">" % (style_class, width, height)

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

        # create the rectangle element
        rectangle_element_string = "<svg:rect class=\"%s\" x=\"%.1f%%\" y=\"%.1f%%\" width=\"%.1f%%\" height=\"%.1f%%\"/>" % (style_class, x, y, width, height)

        return rectangle_element_string

    def generate_text(self, graphics_attributes):
        x = graphics_attributes["x"]
        y = graphics_attributes["y"]
        text = graphics_attributes["text"]
        escaped_text = self.visitor.escape_string_value(text)
        options = graphics_attributes["options"]

        # retrieves the style class
        style_class = options.get("class", "")

        # create the text element
        text_element_string = "<svg:text class=\"%s\" x=\"%.1f%%\" y=\"%.1f%%\">%s</svg:text>" % (style_class, x, y, escaped_text)

        return text_element_string

    def get_visitor(self):
        return self.visitor

    def set_visitor(self, visitor):
        self.visitor = visitor
