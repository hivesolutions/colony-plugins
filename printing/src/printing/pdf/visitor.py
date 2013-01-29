#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import struct
import base64

import PIL.Image

import colony.libs.string_buffer_util

import exceptions
import printing.manager.ast

FONT_SCALE_FACTOR = 20
""" The font scale factor """

IMAGE_SCALE_FACTOR = 10
""" The image scale factor """

EXCLUSION_LIST = [
    "__class__", "__delattr__", "__dict__", "__doc__", "__getattribute__",
    "__hash__", "__init__", "__module__", "__new__", "__reduce__", "__reduce_ex__",
    "__repr__", "__setattr__", "__str__", "__weakref__", "__format__", "__sizeof__",
    "__subclasshook__", "accept", "accept_double", "accept_post_order", "add_child_node",
    "remove_child_node", "set_indent", "set_value", "indent", "value", "child_nodes"
]
""" The exclusion list """

DEFAULT_ENCODER = "utf-8"
""" The default encoder """

LEFT_TEXT_ALIGN_VALUE = "left"
""" The left text align value """

RIGHT_TEXT_ALIGN_VALUE = "right"
""" The right text align value """

CENTER_TEXT_ALIGN_VALUE = "center"
""" The center text align value """







# -------------- REMOVE -----

import reportlab.pdfgen.canvas
import reportlab.pdfbase.ttfonts
import reportlab.pdfbase.pdfmetrics
import reportlab.lib.units

SCALE = reportlab.lib.units.cm
ROLL_PAPER = (8 * SCALE, 29.7 * SCALE)
PAPER_SIZE = ROLL_PAPER

# ------------------------------




def _visit(ast_node_class):
    """
    Decorator for the visit of an ast node.

    @type ast_node_class: String
    @param ast_node_class: The target class for the visit.
    @rtype: Function
    @return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the visit decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @return: The decorator interceptor function.
        """

        function.ast_node_class = ast_node_class

        return function

    # returns the created decorator
    return decorator

def dispatch_visit():
    """
    Decorator for the dispatch visit of an ast node.

    @rtype: Function
    @return: The created decorator.
    """

    def create_decorator_interceptor(function):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type function: Function
        @param function: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the dispatch visit decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # retrieves the self values
            self_value = args[0]

            # retrieves the node value
            node_value = args[1]

            # retrieves the node value class
            node_value_class = node_value.__class__

            # retrieves the mro list from the node value class
            node_value_class_mro = node_value_class.mro()

            # iterates over all the node value class mro elements
            for node_value_class_mro_element in node_value_class_mro:
                # in case the node method map does not exists in
                # the current instance must continue the loop
                if not hasattr(self_value, "node_method_map"): continue
                
                # retrieves the node method map from the current instance
                # and verifies that the node value class exists in the
                # node method map, otherwise continues the loop
                node_method_map = getattr(self_value, "node_method_map")
                if not node_value_class_mro_element in node_method_map: continue
                    
                # retrieves the correct visit method for the element and
                # then calls it "enclosed" by calls to the before and after
                # visit handler methods
                visit_method = node_method_map[node_value_class_mro_element]
                self_value.before_visit(*args[1:], **kwargs)
                visit_method(*args, **kwargs)
                self_value.after_visit(*args[1:], **kwargs)

                return

            # in case of failure to find the proper callback
            function(*args, **kwargs)

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the dispatch visit decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @return: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

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

    context_information_map = {}
    """ The context information map """

    def __init__(self):
        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True
        self.visit_index = 0
        self.printing_options = {}
        self.elements_list = []
        self.current_position = None
        self.context_information_map = {}

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

            # in case the current class real element contains an ast node class reference
            if hasattr(self_class_real_element, "ast_node_class"):
                # retrieves the ast node class from the current class real element
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

    @dispatch_visit()
    def visit(self, node):
        print "unrecognized element node of type " + node.__class__.__name__

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @_visit(printing.manager.ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @_visit(printing.manager.ast.GenericElement)
    def visit_generic_element(self, node):
        pass

    @_visit(printing.manager.ast.PrintingDocument)
    def visit_printing_document(self, node):
        # in case it's the first visit
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context_information(node)

            # retrieves the printing document name
            printing_document_name = node.name

            # resets the list of elements in the document
            self.elements_list = []

            # sets the initial position
            self.current_position = (
                0, 0
            )
            
            # ------------------------- REMOVE ----------------------
            
            canvas = reportlab.pdfgen.canvas.Canvas(
                "c:/out.pdf",
                pagesize = PAPER_SIZE
            )
            width, height = PAPER_SIZE
            
            self.printing_options["canvas"] = canvas
            self.printing_options["width"] = width
            self.printing_options["height"] = height
            
            #  ------------------------------------------------------------
            
        # in case it's the second visit
        elif self.visit_index == 1:
            
            #  ------------------------------------------------------------
            
            canvas = self.printing_options["canvas"]
            canvas.save()
            
            #  ------------------------------------------------------------
            
            
            # retrieves the printing document name
            printing_document_name = node.name
            printing_document_width = hasattr(node, "width") and int(node.width) or 0
            printing_document_height = hasattr(node, "height") and int(node.height) or 0

            # packs the header value as a binary string
            header = struct.pack(
                "<256sIII",
                str(printing_document_name),
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
            self.remove_context_information(node)

    @_visit(printing.manager.ast.Block)
    def visit_block(self, node):
        if self.visit_index == 0:
            # adds the node as the context information, this way
            # the complete set of symbols for the block are exposed
            # to the underlying nodes (block opening)
            self.add_context_information(node)
            self.push_context_information("biggest_height", 0)

        # in case it's the second visit
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context_information(node)

    @_visit(printing.manager.ast.Paragraph)
    def visit_paragraph(self, node):
        if self.visit_index == 0:
            self.add_context_information(node)
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context_information(node)

    @_visit(printing.manager.ast.Line)
    def visit_line(self, node):
        if self.visit_index == 0:
            self.add_context_information(node)

            self.push_context_information("biggest_height", 0)

            if self.has_context_information("margin_top"):
                # retrieves the margin top
                margin_top = int(self.get_context_information("margin_top"))
            else:
                # sets the default margin top
                margin_top = 0

            # retrieves the current position in x and y
            current_position_x, current_position_y = self.current_position

            # updates the current position values
            self.current_position = (
                current_position_x,
                current_position_y - margin_top * FONT_SCALE_FACTOR
            )
        elif self.visit_index == 1:
            biggest_height = self.get_context_information("biggest_height")

            self.pop_context_information("biggest_height")

            if self.has_context_information("margin_bottom"):
                # retrieves the margin bottom
                margin_bottom = int(self.get_context_information("margin_bottom"))
            else:
                # sets the default margin bottom
                margin_bottom = 0

            # retrieves the current position in x and y
            current_position_x, current_position_y = self.current_position

            # sets the new current position
            self.current_position = (
                0, current_position_y - biggest_height - margin_bottom * FONT_SCALE_FACTOR
            )

            # removes the context information
            self.remove_context_information(node)

    @_visit(printing.manager.ast.Text)
    def visit_text(self, node):
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context_information(node)

            # retrieves the text and encodes it using
            # the default encoder and ignoring possible errors
            text_encoded = node.text.encode(DEFAULT_ENCODER, "ignore")

            # retrieves the font name
            font_name = str(self.get_context_information("font"))

            # retrieves the font size
            font_size = int(self.get_context_information("font_size"))

            # retrieves the text align
            text_align = self.get_context_information("text_align")

            if self.has_context_information("font_style"):
                # retrieves the font style
                font_style = self.get_context_information("font_style")
            else:
                # sets the font style
                font_style = "regular"

            if self.has_context_information("margin_left"):
                # retrieves the margin left
                margin_left = int(self.get_context_information("margin_left"))
            else:
                # sets the default margin left
                margin_left = 0

            if self.has_context_information("margin_right"):
                # retrieves the margin right
                margin_right = int(self.get_context_information("margin_right"))
            else:
                # sets the default margin right
                margin_right = 0

            if self.has_context_information("x"):
                # retrieves the x position (block position)
                position_x = int(self.get_context_information("x"))
            else:
                # retrieves the x position (default and global position)
                position_x = 0

            if self.has_context_information("y"):
                # retrieves the y position (block position)
                position_y = int(self.get_context_information("y"))
            else:
                # retrieves the y position (default and global position)
                position_y = 0

            if self.has_context_information("width"):
                # retrieves the width (block width)
                block_width = int(self.get_context_information("width"))
            else:
                # retrieves the width (default and global width)
                block_width = 0

            if self.has_context_information("height"):
                # retrieves the height (block height)
                block_height = int(self.get_context_information("height"))
            else:
                # retrieves the height (default and global height)
                block_height = 0

            # sets the default values for the text weight and for
            # the italic enumeration
            text_weight_int = 0
            text_italic_int = 0

            if font_style == "bold" or font_style == "bold_italic":
                text_weight_int = 1

            if font_style == "italic" or font_style == "bold_italic":
                text_italic_int = 1

            # retrieves the current position in x and y
            _current_position_context_x, current_position_context_y = self.current_position

            # in case the text align is left
            if text_align == LEFT_TEXT_ALIGN_VALUE:
                text_align_int = 1

            # in case the text align is right
            elif text_align == RIGHT_TEXT_ALIGN_VALUE:
                text_align_int = 2

            # in case the text align is left
            elif text_align == CENTER_TEXT_ALIGN_VALUE:
                text_align_int = 3

            # calculates the text height from the font scale factor
            text_height = font_size * FONT_SCALE_FACTOR;

            # packs the element text element structure containing all the meta
            # information that makes part of it then adds the "just" created
            # element to the elements list
            element = struct.pack(
                "<ii256sIIIIIIIIIII",
                0,
                current_position_context_y,
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
            element += "\0"
            self.elements_list.append((1, element))
            
            # ------------------------- REMOVE ----------------------
            
            canvas = self.printing_options["canvas"]
            height = self.printing_options["height"]
            canvas.drawString(position_x, current_position_context_y + height, text_encoded)
            
            # ----------------------------------------
            
            

            # in case the current text height is bigger than the current
            # context biggest height, updates the information
            if self.get_context_information("biggest_height") < text_height:
                # substitutes the new biggest height with the text height
                self.put_context_information("biggest_height", text_height)

        # in case it's the second visit
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context_information(node)

    @_visit(printing.manager.ast.Image)
    def visit_image(self, node):
        if self.visit_index == 0:
            self.add_context_information(node)

        elif self.visit_index == 1:
            self.remove_context_information(node)

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

    def get_context_information(self, context_information_name):
        if not self.has_context_information(context_information_name):
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_information_name + " is invalid"
            )

        return self.peek_context_information(context_information_name)

    def add_context_information(self, node):
        valid_attributes = [(value, getattr(node, value)) for value in dir(node) if value not in EXCLUSION_LIST]

        for valid_attribute_name, valid_attribute_value in valid_attributes:
            self.push_context_information(valid_attribute_name, valid_attribute_value)

    def remove_context_information(self, node):
        valid_attribute_names = [value for value in dir(node) if value not in EXCLUSION_LIST]

        for valid_attribute_name in valid_attribute_names:
            self.pop_context_information(valid_attribute_name)

    def push_context_information(self, context_information_name, context_information_value):
        if not context_information_name in self.context_information_map:
            self.context_information_map[context_information_name] = []

        self.context_information_map[context_information_name].append(context_information_value)

    def pop_context_information(self, context_information_name):
        if not context_information_name in self.context_information_map:
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_information_name + " is invalid"
            )

        self.context_information_map[context_information_name].pop()

    def peek_context_information(self, context_information_name):
        if not context_information_name in self.context_information_map:
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_information_name + " is invalid"
            )

        return self.context_information_map[context_information_name][-1]

    def put_context_information(self, context_information_name, context_information_value):
        """
        Puts the given context information in the context
        information map.

        @type context_information_name: String
        @param context_information_name: The name of the context information
        to be put in the context information map.
        @type context_information_value: Object
        @param context_information_value: The value of the context information to be put
        in the context information map.
        """

        if not context_information_name in self.context_information_map:
            raise exceptions.InvalidContextInformationName(
                "the context information name: " + context_information_name + " is invalid"
            )

        self.context_information_map[context_information_name][-1] = context_information_value

    def has_context_information(self, context_information_name):
        """
        Tests if the given context information name exists
        in the current context information map.

        @type context_information_name: String
        @param context_information_name: The context information name
        to be tested against the current context information map.
        @rtype: bool
        @return: If the context information name exists in the
        current context information map (and is valid).
        """

        # in case the context information name exists in the
        # context information map and is not invalid
        if context_information_name in self.context_information_map and\
            self.context_information_map[context_information_name]:
            # returns true
            return True
        # otherwise
        else:
            # returns false
            return False
