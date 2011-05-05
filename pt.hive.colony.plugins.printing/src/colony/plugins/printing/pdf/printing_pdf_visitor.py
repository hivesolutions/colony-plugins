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

import base64

import PIL.Image

import colony.libs.string_buffer_util

import printing_pdf_exceptions
import printing.manager.printing_language_ast

IMAGE_SCALE_FACTOR = 0.5
""" The image scale factor """

EXCLUSION_LIST = [
    "__class__", "__delattr__", "__dict__", "__doc__", "__getattribute__",
    "__hash__", "__init__", "__module__", "__new__", "__reduce__",
    "__reduce_ex__", "__repr__", "__setattr__", "__str__", "__weakref__",
    "__format__", "__sizeof__", "__subclasshook__", "accept", "accept_double",
    "accept_post_order", "add_child_node", "remove_child_node", "set_indent",
    "set_value", "indent", "value", "child_nodes"
]
""" The exclusion list """

DEFAULT_ENCODER = "Cp1252"
""" The default encoder """

LEFT_TEXT_ALIGN_VALUE = "left"
""" The left text align value """

RIGHT_TEXT_ALIGN_VALUE = "right"
""" The right text align value """

CENTER_TEXT_ALIGN_VALUE = "center"
""" The center text align value """

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
                # in case the node method map exist in the current instance
                if hasattr(self_value, "node_method_map"):
                    # retrieves the node method map from the current instance
                    node_method_map = getattr(self_value, "node_method_map")

                    # in case the node value class exists in the node method map
                    if node_value_class_mro_element in node_method_map:
                        # retrieves the visit method for the given node value class
                        visit_method = node_method_map[node_value_class_mro_element]

                        # calls the before visit method
                        self_value.before_visit(*args[1:], **kwargs)

                        # calls the visit method
                        visit_method(*args, **kwargs)

                        # calls the after visit method
                        self_value.after_visit(*args[1:], **kwargs)

                        return

            # in case of failure to find the proper callbak
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

    pdf_document_controller = None
    """ The pdf document controller """

    printing_options = {}
    """ The printing options """

    current_position = None
    """ The current position """

    context_information_map = {}
    """ The context information map """

    def __init__(self):
        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True
        self.visit_index = 0
        self.printer_handler = None
        self.printing_options = {}
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

    def get_pdf_document_controller(self):
        """
        Retrieves the pdf document controller.

        @rtype: PdfDocumentController
        @return: The pdf document controller.
        """

        return self.pdf_document_controller

    def set_pdf_document_controller(self, pdf_document_controller):
        """
        Sets the pdf document controller.

        @type pdf_document_controller: PdfDocumentController
        @param pdf_document_controller: The pdf document controller.
        """

        self.pdf_document_controller = pdf_document_controller

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

    @_visit(printing.manager.printing_language_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @_visit(printing.manager.printing_language_ast.GenericElement)
    def visit_generic_element(self, node):
        pass

    @_visit(printing.manager.printing_language_ast.PrintingDocument)
    def visit_printing_document(self, node):
        # in case it's the first visit
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context_information(node)

            # retrieves the printing document name
            printing_document_name = node.name

            # sets the title in the pdf document controller
            self.pdf_document_controller.set_title(printing_document_name)

            # sets the initial position
            self.current_position = (
                0, 0
            )
        # in case it's the second visit
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context_information(node)

    @_visit(printing.manager.printing_language_ast.Paragraph)
    def visit_paragraph(self, node):
        if self.visit_index == 0:
            self.add_context_information(node)
        elif self.visit_index == 1:
            self.remove_context_information(node)

    @_visit(printing.manager.printing_language_ast.Line)
    def visit_line(self, node):
        # in case it's the first visit
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context_information(node)

            # initializes the biggest height context information
            self.push_context_information("biggest_height", 0)

            # in case margin top exists
            if self.has_context_information("margin_top"):
                # retrieves the margin top
                margin_top = int(self.get_context_information("margin_top"))
            else:
                # sets the default margin top
                margin_top = 0

            # retrieves the current position in x and y
            current_position_x, current_position_y = self.current_position

            self.current_position = (
                current_position_x,
                current_position_y + margin_top
            )
        elif self.visit_index == 1:
            # retrieves the line biggest height
            biggest_height = self.get_context_information("biggest_height")

            # pops the current biggest height context
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
                0,
                current_position_y + biggest_height + margin_bottom
            )

            # removes the context information
            self.remove_context_information(node)

    @_visit(printing.manager.printing_language_ast.Text)
    def visit_text(self, node):
        # in case it's the first visit
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context_information(node)

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

            # sets the font in the pdf document controller
            self.pdf_document_controller.set_font(font_name, font_size, font_style)

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

            # retrieves the current position in x and y
            _current_position_context_x, current_position_context_y = self.current_position

            # retrieves the text width and height
            text_width, text_height = self.pdf_document_controller.get_text_size(node.text)

            # retrieves the current page size
            page_width, _page_height = self.pdf_document_controller.get_page_size()

            # starts the text x coordinate with the margins
            text_x = margin_left - margin_right

            # in case the text align is left
            if text_align == LEFT_TEXT_ALIGN_VALUE:
                text_x += 0
            # in case the text align is right
            elif text_align == RIGHT_TEXT_ALIGN_VALUE:
                text_x += page_width - text_width
            # in case the text align is left
            elif text_align == CENTER_TEXT_ALIGN_VALUE:
                text_x += int(page_width / 2) - int(text_width / 2)

            # starts the text y coordinate with the current y position
            text_y = current_position_context_y

            # draws a string in the pdf document
            self.pdf_document_controller.draw_string(text_x, text_y, node.text)

            # in case the current text height is bigger than the current
            # context biggest height, updates the information
            if self.get_context_information("biggest_height") < text_height:
                # substitutes the new biggest height with the text height
                self.put_context_information("biggest_height", text_height)

        # in case it's the second visit
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context_information(node)

    @_visit(printing.manager.printing_language_ast.Image)
    def visit_image(self, node):
        # in case it's the first visit
        if self.visit_index == 0:
            # adds the node as the context information
            self.add_context_information(node)

            # sets the image path object
            image_path = None

            # starts the image source object
            image_source = None

            if self.has_context_information("path"):
                # retrieves the image path
                image_path = self.get_context_information("path")
            elif self.has_context_information("source"):
                # retrieves the image source
                image_source = self.get_context_information("source")

            # retrieves the text align
            text_align = self.get_context_information("text_align")

            # in case the image path is defined
            if image_path:
                # opens the bitmap image
                bitmap_image = PIL.Image.open(image_path)
            # in case the image source is defined
            elif image_source:
                # decodes the image source
                image_source_decoded = base64.b64decode(image_source)

                # creates the image buffer
                image_source_buffer = colony.libs.string_buffer_util.StringBuffer(False)

                # writes the image source decoded in the image source buffer
                image_source_buffer.write(image_source_decoded)

                # goes to the beginning of the file
                image_source_buffer.seek(0)

                # opens the bitmap image
                bitmap_image = PIL.Image.open(image_source_buffer)

            # retrieves the bitmap image width and height
            bitmap_image_width, bitmap_image_height = bitmap_image.size

            real_bitmap_image_width = bitmap_image_width * IMAGE_SCALE_FACTOR
            real_bitmap_image_height = bitmap_image_height * IMAGE_SCALE_FACTOR

            # retrieves the current position in x and y
            current_position_x, current_position_y = self.current_position

            # retrieves the current page size
            page_width, _page_height = self.pdf_document_controller.get_page_size()

            if text_align == "left":
                real_bitmap_x = 0
            elif text_align == "right":
                real_bitmap_x = page_width - real_bitmap_image_width
            elif text_align == "center":
                real_bitmap_x = int(page_width / 2) - (real_bitmap_image_width / 2)

            real_bitmap_y = current_position_y

            self.pdf_document_controller.draw_image(bitmap_image, real_bitmap_x, real_bitmap_y, real_bitmap_image_width, real_bitmap_image_height)

            # sets the new current position
            self.current_position = (
                current_position_x + real_bitmap_image_height,
                current_position_y
            )

            # in case the bitmap image height is bigger than the current
            # context biggest height, updates the information
            if self.get_context_information("biggest_height") < real_bitmap_image_height:
                # substitutes the new biggest height with the bitmap image height
                self.put_context_information("biggest_height", real_bitmap_image_height)

        # in case it's the second visit
        elif self.visit_index == 1:
            # removes the context information
            self.remove_context_information(node)

    def get_current_position_context(self):
        # retrieves the current position in x and y
        current_position_x, current_position_y = self.current_position

        # converts the current position to context
        current_position_context = (
            current_position_x,
            -1 * current_position_y
        )

        return current_position_context

    def get_context_information(self, context_information_name):
        if not self.has_context_information(context_information_name):
            raise printing_pdf_exceptions.InvalidContextInformationName("the context information name: " + context_information_name + " is invalid")

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
            raise printing_pdf_exceptions.InvalidContextInformationName("the context information name: " + context_information_name + " is invalid")

        self.context_information_map[context_information_name].pop()

    def peek_context_information(self, context_information_name):
        if not context_information_name in self.context_information_map:
            raise printing_pdf_exceptions.InvalidContextInformationName("the context information name: " + context_information_name + " is invalid")

        return self.context_information_map[context_information_name][-1]

    def put_context_information(self, context_information_name, context_information_value):
        if not context_information_name in self.context_information_map:
            raise printing_pdf_exceptions.InvalidContextInformationName("the context information name: " + context_information_name + " is invalid")

        self.context_information_map[context_information_name][-1] = context_information_value

    def has_context_information(self, context_information_name):
        if not context_information_name in self.context_information_map or not self.context_information_map[context_information_name]:
            return False
        else:
            return True
