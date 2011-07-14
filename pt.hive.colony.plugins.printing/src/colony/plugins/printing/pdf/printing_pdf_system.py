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

import printing_pdf_visitor

PRINTING_NAME = "pdf"
""" The printing name """

TEST_TEXT = "Hello world from Hive Colony"
""" The test text """

class PrintingPdf:
    """
    The printing pdf class.
    """

    printing_pdf_plugin = None
    """ The printing pdf plugin """

    def __init__(self, printing_pdf_plugin):
        """
        Constructor of the class.

        @type printing_pdf_plugin: PrintingPdfPlugin
        @param printing_pdf_plugin: The printing pdf plugin.
        """

        self.printing_pdf_plugin = printing_pdf_plugin

    def get_printing_name(self):
        """
        Retrieves the printing name.

        @rtype: String
        @return: The printing name.
        """

        return PRINTING_NAME

    def print_test(self, printing_options = {}):
        # retrieves the document pdf plugin
        document_pdf_plugin = self.printing_pdf_plugin.document_pdf_plugin

        # creates a document controller
        pdf_document_controller = document_pdf_plugin.create_document_controller()

        # retrieves the pdf document page size
        pdf_document_page_width, _pdf_document_page_height = pdf_document_controller.get_page_size()

        # retrieves the inch size
        inch_size = pdf_document_controller.get_inch_size()

        # draws a string centered in the pdf document
        pdf_document_controller.draw_string_centered(pdf_document_page_width / 2, inch_size * 1, TEST_TEXT)

        # saves the pdf document
        pdf_document_controller.save()

    def print_test_image(self, image_path, printing_options = {}):
        print "printing test image in pdf"

    def print_printing_language(self, printing_document, printing_options = {}):
        # creates the pdf printing visitor
        visitor = printing_pdf_visitor.Visitor()

        # retrieves the pdf document controller
        pdf_document_controller = self.get_pdf_document_controller(printing_options)

        # sets the pdf document controller in the visitor
        visitor.set_pdf_document_controller(pdf_document_controller)

        # sets the printing options in the visitor
        visitor.set_printing_options(printing_options)

        # accepts the visitor in the printing document,
        # using double visiting mode
        printing_document.accept_double(visitor)

        # closes the pdf document controller
        self.close_pdf_document_controller(pdf_document_controller)

    def get_pdf_document_controller(self, printing_options):
        """
        Retrieves a new pdf document controller for the
        given printing options.

        @type printing_options: Dictionary
        @param printing_options: The printing options to be used
        to create the pdf document controller.
        @rtype: PdfDocumentController
        @return: The created pdf document controller.
        """

        # retrieves the document pdf plugin
        document_pdf_plugin = self.printing_pdf_plugin.document_pdf_plugin

        # creates a document controller
        pdf_document_controller = document_pdf_plugin.create_document_controller(printing_options)

        # returns the pdf document controller
        return pdf_document_controller

    def close_pdf_document_controller(self, pdf_document_controller):
        """
        Closes the given pdf document controller.

        @type pdf_document_controller: PdfDocumentController
        @param pdf_document_controller: The pdf document controller to be closed.
        """

        # saves the pdf document
        pdf_document_controller.save()
