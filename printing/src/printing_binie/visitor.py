#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import struct
import base64

import PIL.Image

import colony

import printing_manager

from . import exceptions

FONT_SCALE_FACTOR = 20
""" The font scale factor """

IMAGE_SCALE_FACTOR = 10
""" The image scale factor """

EXCLUSION_LIST = [
    "__class__",
    "__delattr__",
    "__dict__",
    "__doc__",
    "__getattribute__",
    "__hash__",
    "__init__",
    "__module__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__str__",
    "__weakref__",
    "__format__",
    "__sizeof__",
    "__subclasshook__",
    "accept",
    "accept_double",
    "accept_post_order",
    "add_child_node",
    "remove_child_node",
    "set_indent",
    "set_value",
    "indent",
    "value",
    "child_nodes"
]
""" The exclusion list """

DEFAULT_ENCODER = "utf-8"
""" The default encoder """

class Visitor:
    """
    The visitor class.
    """

    node_method_map = {}
    """ The node method map """

    visit_childs = True
    """ The visit childs flag """

    visit_next = True
    """ The visit next flag """

    visit_index = 0
    """ The visit index, for multiple visits """

    printing_options = {}
    """ The printing options """

    elements_list = []
    """ The list containing the various elements """

    current_position = None
    """ The current position """

    context_map = {}
    """ The context information map """

    def __init__(self):
        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True
        self.visit_index = 0
        self.printing_options = {}
        self.elements_list = []
        self.current_position = None
        self.context_map = {}

        self.update_node_method_map()

    def update_node_method_map(self):
        # retrieves the class of the current instance
        self_class = self.__class__

        # retrieves the names of the elements for the current class
        self_class_elements = dir(self_class)

        # iterates over all the name of the elements
        for self_class_element in self_class_elements:
            # retrieves the real element value
            self_class_real_element = getattr(self_class, self_class_element)

            # in case the current class real element does not contain
            # an ast node class reference must continue the loop
            if not hasattr(self_class_real_element, "ast_node_class"): continue

            # retrieves the ast node class from the current class real element
            # and sets it in the node method map
            ast_node_class = getattr(self_class_real_element, "ast_node_class")
            self.node_method_map[ast_node_class] = self_class_real_element

    def get_printing_options(self):
        """
        Retrieves the printing options.

        @rtype: Dictionary
        @return: The printing options.
        """

        return self.printing_options

    def set_printing_options(self, printing_options):
        """
        Sets the printing options.

        @type printing_options: Dictionary.
        @param printing_options: The printing options.
        """

        self.printing_options = printing_options

    @colony.dispatch_visit()
    def visit(self, node):
        print("unrecognized element node of type " + node.__class__.__name__)

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @colony.visit(printing_manager.AstNode)
    def visit_ast_node(self, node):
        pass

    @colony.visit(printing_manager.GenericElement)
    def visit_generic_element(self, node):
        pass

    @colony.visit(printing_manager.PrintingDocument)
    def visit_printing_document(self, node):
        # in case it's the first visit
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context(node)

            # retrieves the printing document name
            printing_document_name = node.name

            # resets the list of elements in the document
            self.elements_list = []

            # sets the initial position
            self.current_position = (
                0, 0
            )
        # in case it's the second visit
        elif self.visit_index == 1:
            # retrieves the printing document name and dimensions
            # to be able to update the structure
            printing_document_name = node.name
            printing_document_width = hasattr(node, "width") and int(node.width) or 0
            printing_document_height = hasattr(node, "height") and int(node.height) or 0

            # makes sure that the format of the document name
            # is appropriate for the packing to be performed
            printing_document_name = str(printing_document_name)
            printing_document_name = colony.legacy.bytes(printing_document_name)

            # packs the header value as a binary string
            header = struct.pack(
                "<256sIII",
                printing_document_name,
                printing_document_width,
                printing_document_height,
                len(self.elements_list)
            )
            self.printing_options["file"].write(header)

            # iterates over all the elements list to create their header
            # and then add the element data
            for element in self.elements_list:
                # unpacks the element into the type and its
                # data (contents)
                element_type, element_data = element
                element_length = len(element_data)

                # creates the element header using the type and the length
                # of the element and then writes it and the data into the
                # the current file
                element_header = struct.pack("<II", element_type, element_length)
                self.printing_options["file"].write(element_header)
                self.printing_options["file"].write(element_data)

            # removes the context information
            self.remove_context(node)

    @colony.visit(printing_manager.Block)
    def visit_block(self, node):
        if self.visit_index == 0:
            # adds the node as the context information, this way
            # the complete set of symbols for the block are exposed
            # to the underlying nodes (block opening)
            self.add_context(node)
            self.push_context("biggest_height", 0)

        # in case it's the second visit
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context(node)

    @colony.visit(printing_manager.Paragraph)
    def visit_paragraph(self, node):
        if self.visit_index == 0: self.add_context(node)
        elif self.visit_index == 1: self.remove_context(node)

    @colony.visit(printing_manager.Line)
    def visit_line(self, node):
        if self.visit_index == 0:
            self.add_context(node)
            self.push_context("biggest_height", 0)

            # retrieves the margin top value defined
            # for the current context
            margin_top = int(self.get_context("margin_top", "0"))

            # retrieves the current position in x and y
            # and then updates the current position
            current_position_x, current_position_y = self.current_position
            self.current_position = (
                current_position_x,
                current_position_y - margin_top * FONT_SCALE_FACTOR
            )

        elif self.visit_index == 1:
            biggest_height = self.get_context("biggest_height")
            self.pop_context("biggest_height")

            # retrieves the margin bottom value defined
            # for the current context
            margin_bottom = int(self.get_context("margin_bottom", "0"))

            # retrieves the current position in x and y
            # and then updates the current position
            current_position_x, current_position_y = self.current_position
            self.current_position = (
                0, current_position_y - biggest_height - margin_bottom * FONT_SCALE_FACTOR
            )

            # removes the context information
            self.remove_context(node)

    @colony.visit(printing_manager.Text)
    def visit_text(self, node):
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context(node)

            # retrieves the text and encodes it using
            # the default encoder and ignoring possible errors
            text_encoded = node.text.encode(DEFAULT_ENCODER, "ignore")

            # retrieves the complete set of attributes for the current
            # context to be used for the processing of the node
            font_name = str(self.get_context("font"))
            font_size = int(self.get_context("font_size"))
            text_align = self.get_context("text_align")
            font_style = self.get_context("font_style", "regular")
            margin_left = int(self.get_context("margin_left", "0"))
            margin_right = int(self.get_context("margin_right", "0"))
            position_x = int(self.get_context("x", "0"))
            position_y = int(self.get_context("y", "0"))
            block_width = int(self.get_context("width", "0"))
            block_height = int(self.get_context("height", "0"))

            # endures that the font name is properly encoded
            # as a byte string to avoid packing problems
            font_name = colony.legacy.bytes(font_name)

            # sets the default values for the text weight and for
            # the italic enumeration
            text_weight_int = 0
            text_italic_int = 0

            if font_style == "bold" or font_style == "bold_italic":
                text_weight_int = 1

            if font_style == "italic" or font_style == "bold_italic":
                text_italic_int = 1

            # retrieves the current position in x and y
            _current_position_x, _current_position_y = self.current_position

            # converts the provided text align value into the
            # appropriate integer value representing it
            if text_align == "left": text_align_int = 1
            elif text_align == "right": text_align_int = 2
            elif text_align == "center": text_align_int = 3

            # calculates the text height from the font scale factor
            text_height = font_size * FONT_SCALE_FACTOR

            # packs the element text element structure containing all the meta
            # information that makes part of it then adds the "just" created
            # element to the elements list
            element = struct.pack(
                "<ii256sIIIIIIIIIII",
                0,
                _current_position_y,
                font_name,
                font_size,
                text_align_int,
                text_weight_int,
                text_italic_int,
                margin_left,
                margin_right,
                position_x,
                position_y,
                block_width,
                block_height,
                len(text_encoded) + 1
            )
            element += text_encoded
            element += b"\0"
            self.elements_list.append((1, element))

            # in case the current text height is bigger than the current
            # context biggest height, updates the information
            biggest_height = self.get_context("biggest_height")
            if biggest_height < text_height:
                self.put_context("biggest_height", text_height)

        # in case it's the second visit
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context(node)

    @colony.visit(printing_manager.Image)
    def visit_image(self, node):
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context(node)

            # sets the default values for both the image path
            # and source, both values are unset by default
            image_path = None
            image_source = None

            # retrieves the path or source value to be used
            # in the retrieval (only one value is set)
            if self.has_context("path"): image_path = self.get_context("path")
            elif self.has_context("source"): image_source = self.get_context("source")

            # retrieves the complete set of attributes for the current
            # context to be used for the processing of the node
            text_align = self.get_context("text_align")
            position_x = int(self.get_context("x", "0"))
            position_y = int(self.get_context("y", "0"))
            block_width = int(self.get_context("width", "0"))
            block_height = int(self.get_context("height", "0"))

            # in case the image path is defined must load the
            # image data from the file system
            if image_path:
                # opens the bitmap image directly from the current
                # file system, no dynamically loaded image
                bitmap_image = PIL.Image.open(image_path)

            # in case the image source is defined must load the
            # base 64 image data from the attribute
            elif image_source:
                # decodes the image source from the default base 64
                # encoding to be used for the loading
                image_source_decoded = base64.b64decode(image_source)

                # creates the image buffer then writes the decoded
                # image into it and opens the file object with the
                # created buffer (image loading into structure)
                image_source_buffer = colony.StringBuffer(False)
                image_source_buffer.write(image_source_decoded)
                image_source_buffer.seek(0)
                bitmap_image = PIL.Image.open(image_source_buffer)

            # retrieves the bitmap image width and height
            bitmap_image_width, bitmap_image_height = bitmap_image.size

            # creates a new image without transparency settings, so that
            # no extra color is used ands copies the bitmap image into it
            other_image = PIL.Image.new(
                "RGB",
                (bitmap_image_width, bitmap_image_height),
                color = "white"
            )
            other_image.paste(bitmap_image, bitmap_image)

            # retrieves the current position in x and y
            _current_position_x, current_position_y = self.current_position

            # converts the provided text align value into the
            # appropriate integer value representing it
            if text_align == "left": text_align_int = 1
            elif text_align == "right": text_align_int = 2
            elif text_align == "center": text_align_int = 3

            # sets the real bitmap image height as the bitmap
            # image height (value copy)
            real_bitmap_image_height = bitmap_image_height

            # creates a new string buffer for the image
            string_buffer = colony.StringBuffer(False)

            # saves the new image into the string buffer and then
            # retrieve the buffer data
            other_image.save(string_buffer, "bmp")
            buffer = string_buffer.get_value()

            # packs the element image element structure containing all the meta
            # information that makes part of it then adds the "just" created
            # element to the elements list
            element = struct.pack(
                "<iiIIIIII",
                0,
                current_position_y,
                text_align_int,
                position_x,
                position_y,
                block_width,
                block_height,
                len(buffer)
            )
            element += buffer
            self.elements_list.append((2, element))

            biggest_height = self.get_context("biggest_height")
            if biggest_height < real_bitmap_image_height * IMAGE_SCALE_FACTOR:
                self.put_context("biggest_height", real_bitmap_image_height * IMAGE_SCALE_FACTOR)

        elif self.visit_index == 1:
            self.remove_context(node)

    def get_current_position_context(self):
        """
        Retrieves the current position based on the current
        context information.

        @rtype: Tuple
        @return: The current position base on the current context information
        and applied with the font scale factor.
        """

        # retrieves the current position in x and y
        current_position_x, current_position_y = self.current_position

        # converts the current position to context
        current_position_context = (
            FONT_SCALE_FACTOR * current_position_x,
            -1 * FONT_SCALE_FACTOR * current_position_y
        )

        # returns the current position context
        return current_position_context

    def get_context(self, context_name, default = None):
        if not self.has_context(context_name):
            if not default == None: return default
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_name + " is invalid"
            )

        return self.peek_context(context_name)

    def add_context(self, node):
        valid_attributes = [(value, getattr(node, value)) for value in dir(node) if value not in EXCLUSION_LIST]

        for valid_attribute_name, valid_attribute_value in valid_attributes:
            self.push_context(valid_attribute_name, valid_attribute_value)

    def remove_context(self, node):
        valid_attribute_names = [value for value in dir(node) if value not in EXCLUSION_LIST]

        for valid_attribute_name in valid_attribute_names:
            self.pop_context(valid_attribute_name)

    def push_context(self, context_name, context_value):
        if not context_name in self.context_map:
            self.context_map[context_name] = []

        self.context_map[context_name].append(context_value)

    def pop_context(self, context_name):
        if not context_name in self.context_map:
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_name + " is invalid"
            )

        self.context_map[context_name].pop()

    def peek_context(self, context_name):
        if not context_name in self.context_map:
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_name + " is invalid"
            )

        return self.context_map[context_name][-1]

    def put_context(self, context_name, context_value):
        """
        Puts the given context information in the context
        information map.

        @type context_name: String
        @param context_name: The name of the context information
        to be put in the context information map.
        @type context_value: Object
        @param context_value: The value of the context information to be put
        in the context information map.
        """

        if not context_name in self.context_map:
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_name + " is invalid"
            )

        self.context_map[context_name][-1] = context_value

    def has_context(self, context_name):
        """
        Tests if the given context information name exists
        in the current context information map.

        @type context_name: String
        @param context_name: The context information name
        to be tested against the current context information map.
        @rtype: bool
        @return: If the context information name exists in the
        current context information map (and is valid).
        """

        # in case the context information name exists in the
        # context information map and is not invalid
        if context_name in self.context_map and\
            self.context_map[context_name]: return True
        else: return False
