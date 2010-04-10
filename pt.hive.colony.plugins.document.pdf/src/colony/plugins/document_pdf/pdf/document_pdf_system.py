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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import document_pdf_filters
import document_pdf_exceptions

class DocumentPdf:
    """
    The document pdf class.
    """

    document_pdf_plugin = None
    """ The document pdf plugin """

    def __init__(self, document_pdf_plugin):
        """
        Constructor of the class.

        @type document_pdf_plugin: DocumentPdfPlugin
        @param document_pdf_plugin: The document pdf plugin.
        """

        self.document_pdf_plugin = document_pdf_plugin

    def create_document_controller(self, document_attributes):
        # tries to retrieve the file attribute
        file = document_attributes.get("file", None)

        # in case the file attribute is not defined
        if not file:
            # raises the mandatory attribute not found exception
            raise document_pdf_exceptions.MandatoryAttributeNotFound("file")

        reportlab_pdf_document_controller = ReportLabPdfDocumentController(file)

        ascii85_filter = document_pdf_filters.Ascii85Filter()
        flate_filter = document_pdf_filters.FlateFilter()

        data = "Gap@D_$WFm'Lhapro)L<_*!jn@V)B;en?UF)Ti\"Ld]Ki9k6gpRHsAhA9$n#EU)R\"l'fs]UA6pF//(W.u(A/r:44`=1G@5N*\F*j5iY:4rm/%B_#<l*&p]~>"
        data = ascii85_filter.decode(data)
        data = flate_filter.decode(data)

        print data

        return reportlab_pdf_document_controller

class PdfDocumentController:
    """
    The pdf document controller class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

import reportlab.pdfgen.canvas
import reportlab.lib.units

class ReportLabPdfDocumentController:
    """
    The reportlab pdf document controller class.
    """

    canvas = None
    """ The canvas object """

    def __init__(self, file):
        """
        Constructor of the class.

        @type file: String/File
        @param file: The name of the file to describe the pdf
        document, in alternative it may be a file like object.
        """

        # creates the canvas with the given file
        self.canvas = reportlab.pdfgen.canvas.Canvas(file)

    def draw_string(self, x_position, y_position, string_value):
        self.canvas.drawString(x_position, y_position, string_value)

    def draw_string_centered(self, x_position, y_position, string_value):
        self.canvas.drawCentredString(x_position, y_position, string_value)

    def get_page_size(self):
        return self.canvas._pagesize

    def save(self):
        self.canvas.save()

    def get_inch_size(self):
        return reportlab.lib.units.inch
