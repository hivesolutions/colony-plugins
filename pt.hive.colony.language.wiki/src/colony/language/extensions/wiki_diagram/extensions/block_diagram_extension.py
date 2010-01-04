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

import re

import wiki_diagram.wiki_diagram_extension_system

DIAGRAM_TYPE = "block"
""" The diagram type """

ROW_SPLITTER_VALUE = "/"
""" The value for the row splitter string """

BLOCK_REGEX_VALUE = "\[([\w, ]*)(\{[\w,\:,\; ]*\})*\]+"
""" The block regex value """

OPTIONS_REGEX_VALUE = "\{(.*)\}"
""" The options regex value """

CLASS_REGEX_VALUE = "class *: *(\w*);?"
""" The class regex value """

COLSPAN_REGEX_VALUE = ".*colspan *: *(.*);?"
""" The colspan regex value """

BLOCK_REGEX = re.compile(BLOCK_REGEX_VALUE, re.UNICODE)
""" The block regex """

OPTIONS_REGEX = re.compile(OPTIONS_REGEX_VALUE, re.UNICODE)
""" The options regex """

CLASS_REGEX = re.compile(CLASS_REGEX_VALUE, re.UNICODE)
""" The class regex """

COLSPAN_REGEX = re.compile(COLSPAN_REGEX_VALUE, re.UNICODE)
""" The colspan regex """

ROW_WIDTH = 100
""" The percent value of the width taken up by each row """

ROW_HEIGHT = 7.0
""" The percent value of the height taken up by each row """

PERCENTAGE_FACTOR = 100
""" The percentage factor """

HORIZONTAL_SPACING  = 1.0
""" The horizontal spacing between blocks """

VERTICAL_SPACING = 1.0
""" The vertical spacing between blocks """

SHADOW_DELTA_X = 0.5
""" The x delta to apply to the drop shadow """

SHADOW_DELTA_Y = 0.5
""" The y delta to apply to the drop shadow """

TEXT_PADDING = 2
""" The padding in percentage to apply to the text """

DEFAULT_STYLE_CLASS = "dark"
""" The default style class to apply to the blocks """

WIDTH_SCALE_FACTOR = 1.6
""" The horizontal scale factor, used to compensate the effect of additional columns """

class BlockDiagramExtension(wiki_diagram.wiki_diagram_extension_system.WikiDiagramExtension):
    """
    The block diagram extension class.
    """

    id = "pt.hive.colony.language.wiki.diagram.extensions.block_diagram"
    """ The extension id """

    name = "Block Diagram Extension"
    """ The name of the extension """

    short_name = "Block Diagram"
    """ The short name of the extension """

    description = "Extension for generating block diagrams"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = ["diagram"]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    def get_diagram_type(self):
        """
        Retrieves the diagram type.

        @rtype: String
        @return: The diagram type.
        """

        return DIAGRAM_TYPE

    def get_graphics_elements(self, contents):
        # initializes the graphics element
        graphics_elements = []

        # initializes the max columns
        max_columns = None

        # initializes the baseline x
        baseline_x = HORIZONTAL_SPACING

        # initializes the baseline y
        baseline_y = VERTICAL_SPACING

        # the block matrix
        blocks = []

        # retrieves the rows by splitting by comma
        rows = contents.split(ROW_SPLITTER_VALUE)

        # for each row
        for row in rows:
            # initializes the list of row blocks
            row_blocks = []

            block_regular_expression_matches = BLOCK_REGEX.finditer(row)

            for block_regular_expression_match in block_regular_expression_matches:
                block_name =  block_regular_expression_match.group(1)
                block_options_string = block_regular_expression_match.group(2)

                # creates the options map
                options = {}

                # initializes the style class with the default value
                style_class = None

                # initializes the colspan as not defined
                colspan = None

                if block_options_string:
                    # tries to match the regular expression for the block options
                    options_regular_expression_match = OPTIONS_REGEX.match(block_options_string)

                    # in case no match occurs, raises an error
                    if not options_regular_expression_match:
                        # @todo: raise a specific exception
                        raise

                    # retrieves the first capture group, corresponding to the options string itself
                    options_string = options_regular_expression_match.group(1)

                    # in case the options string is found, retrieves the options from it
                    if options_string:
                        class_regular_expression_match = CLASS_REGEX.match(options_string)
                        # in case the the class is defined
                        if class_regular_expression_match:
                            # overrides the default style definition
                            style_class = class_regular_expression_match.group(1)

                            # sets the style class in the options map
                            options["class"] = style_class

                        colspan_regular_expression_match = COLSPAN_REGEX.match(options_string)
                        if colspan_regular_expression_match:
                            # retrieves the colspan from the options match
                            colspan = colspan_regular_expression_match.group(1)

                            # sets the colspan in the options map
                            options["colspan"] = colspan

                # creates the block tuple
                block = (block_name, options)

                # appends the new block to the blocks list
                row_blocks.append(block)

            # update the maximum column number
            if len(row_blocks) > max_columns:
                max_columns = len(row_blocks)

            # appends the row of blocks to the overall blocks matrix
            blocks.append(row_blocks)

        # calculates the baseline width
        baseline_width = (max_columns / WIDTH_SCALE_FACTOR) * ROW_WIDTH

        for row_blocks in blocks:
            # retrieves the graphics elements for the row
            row_graphics_elements = self.get_row_graphics_elements(row_blocks, max_columns, baseline_x, baseline_y, baseline_width)

            # appends the row graphics element to the graphics element
            graphics_elements.extend(row_graphics_elements)

            # updates the baseline for the next rows
            baseline_y += ROW_HEIGHT + VERTICAL_SPACING

        # creates the view port size
        viewport_size = (baseline_width, baseline_y)

        # returns the graphics elements and the viewport size
        return graphics_elements, viewport_size

    def get_row_graphics_elements(self, row_blocks, max_columns, baseline_x, baseline_y, baseline_width):
        # initializes the row graphics elements
        row_graphics_elements = []

        # saves the original baseline x
        original_baseline_x = baseline_x

        # determines the number of columns
        number_columns = len(row_blocks)

        # determines the available width (total width minus spacing)
        available_width = baseline_width - (HORIZONTAL_SPACING * (number_columns + 1))

        # determines the width of each block (assuming equal size)
        column_block_width = available_width / number_columns

        # for each block columns
        for row_block in row_blocks:
            # unpacks the row block
            row_block_title, row_block_options = row_block

            if row_block_options:
                style_class = row_block_options.get("class", DEFAULT_STYLE_CLASS)
                colspan = row_block_options.get("colspan", None)
            else:
                style_class = DEFAULT_STYLE_CLASS
                colspan = None

            if colspan:
                # determines the minimum block width (according to row with more columns)
                min_block_width = available_width / max_columns

                # determines the width for the current block with specified colspan
                block_width = float(colspan) * min_block_width

                # determines the height for the current block
                block_height = ROW_HEIGHT
            else:
                # determines the width for the current block
                block_width = column_block_width

                # determines the height for the current block
                block_height = ROW_HEIGHT

            if row_block_title and not row_block_title == "":
                # generates the block
                block_graphics_elements = self.get_block_graphics_elements(baseline_x, baseline_y, block_width, block_height, row_block_title, {"class" : style_class})

                # appends the generated block graphics elements to the row graphics elements
                row_graphics_elements.extend(block_graphics_elements)

            # updates the horizontal baseline
            baseline_x = baseline_x + block_width + HORIZONTAL_SPACING

        # returns the row graphics elements
        return row_graphics_elements

    def get_block_graphics_elements(self, x, y, width, height, title, options):
        # initializes the block graphics elements
        block_graphics_elements = []

        # calculates the text x
        text_x = x + (width / 2)

        # calculates the text y
        text_y = y + (height / 2) + TEXT_PADDING

        # calculates the shadow x
        shadow_x = x + SHADOW_DELTA_X

        # calculates the shadow y
        shadow_y = y + SHADOW_DELTA_Y

        # retrieves the block style from the options
        style_class = options["class"]

        # draws the block shadow rectangle
        shadow_rect = self.create_rectangle(shadow_x, shadow_y, width, height, {"class" : "shadow"})

        # draws the block rectangle
        rect = self.create_rectangle(x, y, width, height, {"class" : style_class})

        # draws the block text
        text = self.create_text(text_x, text_y, title, {"class" : style_class})

        # adds the shadow rectangle to the block graphics elements
        block_graphics_elements.append(shadow_rect)

        # adds the rectangle to the block graphics elements
        block_graphics_elements.append(rect)

        # adds the text to the block graphics elements
        block_graphics_elements.append(text)

        # returns the string value
        return block_graphics_elements

    def create_rectangle(self, x, y, width, height, options):
        rectangle = ("rectangle", {"x" : x, "y" : y, "width" : width, "height" : height, "options" : options})

        return rectangle

    def create_text(self, x, y, text, options):
        text = ("text", {"x" : x, "y" : y, "text" : text, "options" : options})

        return text
