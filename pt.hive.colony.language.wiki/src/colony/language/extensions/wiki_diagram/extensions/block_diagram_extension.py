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

BLOCK_REGEX_VALUE = "\[([\w, ]*)(\[.*\])? *(\{[\w,\:,\; ]*\})*\]+"
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

HEIGHT_SCALE_FACTOR = 0.5
""" The vertical scale factor, used to compensate the effect of additional rows """

INNER_ROW_SPLITTER_VALUE = "\\"
""" The splitter for inner rows, to be replaced by the regular splitter """

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

    def get_graphics_elements(self, block_language_string):
        # parses the block language string and creates the block structure
        block_structure = self.parse(block_language_string)

        # generates the graphics elements for the parsed block structure
        graphics_elements, viewport_size = self.generate_graphics_elements(0, 0, block_structure, ROW_WIDTH)

        # returns the graphics elements and the viewport size
        return graphics_elements, viewport_size

    def parse(self, block_language_data_string):
        # initializes the block structure
        block_structure = BlockStructure()

        # the highest number of columns in a row
        maximum_number_columns = None

        # the number of rows in the overall structure
        number_rows = 0

        # retrieves the rows by splitting by comma
        rows = block_language_data_string.split(ROW_SPLITTER_VALUE)

        # for each row
        for row in rows:
            # initializes the block row structure
            block_row_structure = BlockRowStructure()

            # initializes the list of row blocks
            row_blocks = []

            # initializes the number of columns in the row
            row_number_columns = 0

            # initializes the maximum number of inner rows in the current row
            row_maximum_number_rows = None

            # finds the matches for the regular expression for detecting blocks
            block_regular_expression_matches = BLOCK_REGEX.finditer(row)

            for block_regular_expression_match in block_regular_expression_matches:
                # creates the block from the regular expression match
                block = self.parse_block(block_regular_expression_match)

                # appends the new block to the blocks list
                row_blocks.append(block)

                # retrieves the number of columns in the block
                block_columns = block.get_number_columns()

                # retrieve the number of rows in the block
                block_rows = block.get_number_rows()

                # increments the row's number of columns
                row_number_columns += block_columns

                if block_rows > row_maximum_number_rows:
                    row_maximum_number_rows = block_rows

            # sets the block contents in the row structure
            block_row_structure.set_blocks(row_blocks)

            # sets the number of rows in the row structure
            block_row_structure.set_number_columns(len(row_blocks))

            # sets the number of rows in the row structure
            block_row_structure.set_number_rows(row_maximum_number_rows)

            # appends the row of blocks to the overall block structure
            block_structure.add_row(block_row_structure)

            # update the maximum column number
            if row_number_columns > maximum_number_columns:
                maximum_number_columns = row_number_columns

            number_rows += row_maximum_number_rows

        # sets the number of columns in the block structure
        block_structure.set_number_columns(maximum_number_columns)

        # sets the number of rows in the block structure
        block_structure.set_number_rows(number_rows)

        # returns the parsed block structure
        return block_structure

    def parse_block(self, block_regular_expression_match):
        # initializes the block
        block = Block()

        block_name =  block_regular_expression_match.group(1)
        child_blocks_string = block_regular_expression_match.group(2)
        block_options_string = block_regular_expression_match.group(3)

        # the number of columns inside the block
        number_columns = 1

        # the number of rows inside the block
        number_rows = 1

        # creates the options map
        options = {}

        # initializes the style class with the default value
        style_class = None

        # initializes the colspan as not defined
        colspan = None

        # initializes the child blocks list
        child_block_structure = None

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

        # retrieves the child blocks
        if child_blocks_string:
            child_blocks_string = child_blocks_string.replace(INNER_ROW_SPLITTER_VALUE, ROW_SPLITTER_VALUE)
            child_block_structure = self.parse(child_blocks_string)

            child_blocks_columns = child_block_structure.get_number_columns()
            child_blocks_rows = child_block_structure.get_number_rows()

            # updates the max columns with the number of columns of the child blocks
            number_columns = child_blocks_columns
            number_rows = child_blocks_rows

        # sets the retrieved name in the block
        block.set_title(block_name)

        # sets the retrieved options in the block
        block.set_options(options)

        # sets the parsed children in the block
        block.set_children(child_block_structure)
        block.set_number_columns(number_columns)
        block.set_number_rows(number_rows)

        # returns the created block
        return block

    def generate_graphics_elements(self, x, y, block_structure, parent_width):
        # initializes the graphics element
        graphics_elements = []

        # retrieves the number of columns in the block structure
        number_columns = block_structure.get_number_columns()

        # initializes the baseline x
        baseline_x = x + HORIZONTAL_SPACING

        # initializes the baseline y
        baseline_y = y + VERTICAL_SPACING

        if parent_width == ROW_WIDTH:
            # calculates the baseline width
            baseline_width = (number_columns / WIDTH_SCALE_FACTOR) * parent_width
        else:
            baseline_width = number_columns * parent_width

        for block_row_structure in block_structure.get_rows():
            # retrieves the number of rows in the block structure
            number_rows = block_row_structure.get_number_rows()

            # computes the baseline height
            if number_rows == 1:
                baseline_height = ROW_HEIGHT
            else:
                baseline_height = (number_rows / HEIGHT_SCALE_FACTOR) * ROW_HEIGHT

            # retrieves the graphics elements for the row
            row_graphics_elements = self.generate_row_graphics_elements(block_row_structure, number_columns, baseline_x, baseline_y, baseline_width, baseline_height)

            # appends the row graphics element to the graphics element
            graphics_elements.extend(row_graphics_elements)

            # updates the baseline for the next rows
            baseline_y += baseline_height + VERTICAL_SPACING

        # creates the view port size
        viewport_size = (baseline_width, baseline_y)

        return graphics_elements, viewport_size

    def generate_row_graphics_elements(self, block_row_structure, max_columns, baseline_x, baseline_y, baseline_width, baseline_height):
        # initializes the row graphics elements
        row_graphics_elements = []

        # determines the number of columns in the current row
        number_columns = block_row_structure.get_number_columns()

        # determines the available width (total width minus spacing)
        available_width = baseline_width - (HORIZONTAL_SPACING * (number_columns + 1))

        # determines the width of each block (assuming equal size)
        column_block_width = available_width / number_columns

        # for each block columns
        for row_block in block_row_structure.get_blocks():
            # retrieves the row block title
            row_block_title = row_block.get_title()

            # retrieves the row block children
            row_block_children = row_block.get_children()

            # retrieves the row block options
            row_block_options = row_block.get_options()

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
                block_height = baseline_height
            else:
                # determines the width for the current block
                block_width = column_block_width

                # determines the height for the current block
                block_height = baseline_height

            if row_block_title and not row_block_title == "":
                # generates the block
                block_graphics_elements = self.generate_block_graphics_elements(baseline_x, baseline_y, block_width, block_height, row_block_title, row_block_children, {"class" : style_class})

                # appends the generated block graphics elements to the row graphics elements
                row_graphics_elements.extend(block_graphics_elements)

            # updates the horizontal baseline
            baseline_x = baseline_x + block_width + HORIZONTAL_SPACING

        # returns the row graphics elements
        return row_graphics_elements

    def generate_block_graphics_elements(self, x, y, width, height, title, child_blocks, options):
        # initializes the block graphics elements
        block_graphics_elements = []

        # calculates the text x
        text_x = x + (width / 2)

        if child_blocks:
            rect_x = 0
            rect_y = 0
            # calculates the text y for a block with childs
            text_y = 0 + 2 * TEXT_PADDING
        else:
            rect_x = x
            rect_y = y
            # calculates the text y for an empty block
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
        rect = self.create_rectangle(rect_x, rect_y, width, height, {"class" : style_class})

        # draws the block text
        text = self.create_text(text_x, text_y, title, {"class" : style_class})

        # initializes the child blocks graphics elements
        child_blocks_graphics_elements = None

        if child_blocks:
            # creates the graphics elements for the child blocks
            child_blocks_graphics_elements, _viewport_size = self.generate_graphics_elements(0, 5, child_blocks, width)

        # adds the shadow rectangle to the block graphics elements
        block_graphics_elements.append(shadow_rect)

        # adds the rectangle to the block graphics elements
        block_graphics_elements.append(rect)

        # adds the text to the block graphics elements
        block_graphics_elements.append(text)

        if child_blocks_graphics_elements:
            # adds the graphics elements for the child block
            block_graphics_elements.extend(child_blocks_graphics_elements)

        if child_blocks:
            viewport = self.create_viewport(x, y, width, height, block_graphics_elements, {"class" : style_class})

            return [viewport]

        # returns the string value
        return block_graphics_elements

    def create_viewport(self, x, y, width, height, childs, options):
        viewport = ("viewport", {"x" : x, "y" : y, "width" : width, "height" : height, "childs" : childs, "options" : options})

        return viewport

    def create_rectangle(self, x, y, width, height, options):
        rectangle = ("rectangle", {"x" : x, "y" : y, "width" : width, "height" : height, "options" : options})

        return rectangle

    def create_text(self, x, y, text, options):
        text = ("text", {"x" : x, "y" : y, "text" : text, "options" : options})

        return text

class BlockStructure:

    rows = None
    """ The list of row structures in the block structure """

    number_columns = None
    """ The number of columns in the block structure """

    number_rows = None
    """ The number of rows in the block structure """

    def __init__(self):
        self.rows = []

    def get_rows(self):
        return self.rows

    def set_rows(self, rows):
        self.rows = rows

    def add_row(self, row):
        self.rows.append(row)

    def get_number_columns(self):
        return self.number_columns

    def set_number_columns(self, number_columns):
        self.number_columns = number_columns

    def get_number_rows(self):
        return self.number_rows

    def set_number_rows(self, number_rows):
        self.number_rows = number_rows

class BlockRowStructure:

    blocks = None
    """ The list of blocks in the row """

    number_columns = None
    """ The number of rows in the current row structure """

    number_rows = None
    """ The number of inner rows in the current row structure """

    def __init__(self):
        self.blocks = []

    def get_blocks(self):
        return self.blocks

    def set_blocks(self, blocks):
        self.blocks = blocks

    def get_number_columns(self):
        return self.number_columns

    def set_number_columns(self, number_columns):
        self.number_columns = number_columns

    def get_number_rows(self):
        return self.number_rows

    def set_number_rows(self, number_rows):
        self.number_rows = number_rows

class Block:

    title = None
    """ The title of the block """

    children = None
    """ The list of childs in the block """

    options = None
    """ The options controlling the block """

    number_columns = None
    """ The number of columns in the current block """

    number_rows = None
    """ The number of rows in the current block """

    def __init__(self):
        pass

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_children(self):
        return self.children

    def set_children(self, children):
        self.children = children

    def get_options(self):
        return self.options

    def set_options(self, options):
        self.options = options

    def get_number_rows(self):
        return self.number_rows

    def set_number_rows(self, number_rows):
        self.number_rows = number_rows

    def get_number_columns(self):
        return self.number_columns

    def set_number_columns(self, number_columns):
        self.number_columns = number_columns
