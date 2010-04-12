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

import reportlab.lib.units
import reportlab.pdfgen.canvas
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts

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
        # retrieves the y position (considering the page height)
        y_position = self._get_y_position(y_position)

        # draws the string into the canvas
        self.canvas.drawString(x_position, y_position, string_value)

    def draw_string_centered(self, x_position, y_position, string_value):
        # retrieves the y position (considering the page height)
        y_position = self._get_y_position(y_position)

        # draws the string into the canvas (centered)
        self.canvas.drawCentredString(x_position, y_position, string_value)

    def get_page_size(self):
        return self.canvas._pagesize

    def get_current_font(self):
        return (self.canvas._fontname, self.canvas._fontsize)

    def set_font(self, font_name, font_size):
        # retrieves the list of available fonts
        available_fonts_list = self.canvas.getAvailableFonts()

        # in case the font name is not present in the
        # list of available fonts, tries to register the font
        if not font_name in available_fonts_list:
            # creates the true type font
            true_type_font = reportlab.pdfbase.ttfonts.TTFont(font_name, font_name + ".ttf")

            # registers the true type font
            reportlab.pdfbase.pdfmetrics.registerFont(true_type_font)

        # sets the font in the current canvas
        self.canvas.setFont(font_name, font_size)

    def save(self):
        self.canvas.save()

    def get_inch_size(self):
        return reportlab.lib.units.inch

    def _get_y_position(self, y_position):
        """
        Retrieves the y coordinate taking into account the
        page height and the current font height.

        @type y_position: int
        @param y_position: The base y position.
        @rtype: int
        @return: The calculated y position.
        """

        # retrieves the current font height
        current_font_height = self._get_current_font_height()

        return self.canvas._pagesize[1] - y_position - current_font_height

    def _get_current_font_height(self):
        """
        Retrieves the current font height.

        @rtype: int
        @return: The current font height.
        """

        # retrieves the current font name and size
        current_font_name, current_font_size = self.get_current_font()

        # retrieves the current font height
        current_font_height = self._get_font_height(current_font_name, current_font_size)

        # returns the current font height
        return current_font_height

    def _get_font_height(self, font_name, font_size):
        """
        Retrieves the font height for the given font name
        and size.

        @type font_name: String
        @param font_name: The name of the font to retrieve the height.
        """

        # retrieves the font descriptor
        font = reportlab.pdfbase.pdfmetrics.getFont(font_name)

        # retrieves the font face
        font_face = font.face

        # retrieves the font ascent
        font_ascent = font_face.ascent

        # retrieves the font descent
        font_descent = font_face.descent

        # converts both the font ascent and descent to decimal
        font_ascent_decimal = font_ascent / 1000.0
        font_descent_decimal = font_descent / 1000.0

        # calculates the font height by adding both the descent and the ascent value
        font_height = (font_ascent_decimal * self.canvas._fontsize) + (font_descent_decimal * self.canvas._fontsize * -1)

        # returns the font height
        return font_height
