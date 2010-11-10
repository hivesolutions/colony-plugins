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

import zlib

import colony.libs.string_buffer_util

import document_pdf_exceptions

class DocumentPdfFilter:
    """
    Abstract class describing a document
    pdf filter.
    """

    filter_type = None
    """ The type of filter being used """

    def __init__(self, filter_type = None):
        """
        Constructor of the class.

        @type filter_type: String
        @param filter_type: The type of filter being used.
        """

        self.filter_type = filter_type

    def encode(self, data):
        """
        Encodes the given data with the current defined
        filter.

        @type data: String
        @param data: The data to be encoded.
        @rtype: String
        @return: The encoded data.
        """

        pass

    def decode(self, data, decode_parameters):
        """
        Decodes the given
        """

        pass

class FlateFilter(DocumentPdfFilter):
    """
    The flat filter
    """

    def __init__(self, filter_type = "flate"):
        """
        Constructor of the class.

        @type filter_type: String
        @param filter_type: The type of filter being used.
        """

        DocumentPdfFilter.__init__(self, filter_type)

    def encode(self, data):
        DocumentPdfFilter.encode(self, data)

        # encodes the data using the zlib
        # (DEFLATE) algorithm
        encoded_data = zlib.compress(data)

        # returns the encoded data
        return encoded_data

    def decode(self, data, decode_parameters = {}):
        DocumentPdfFilter.decode(self, data, decode_parameters)

        # decodes the data using the zlib
        # (DEFLATE) algorithm
        decoded_data = zlib.decompress(data)

        # tries to retrieve the predictor parameter
        predictor = decode_parameters.get("/Predictor", 1)

        # in case there is a predictor (predictor == 1 no predictor)
        if not predictor == 1:
            columns = decode_parameters["/Columns"]

            # checks if it is a png predictor
            if predictor >= 10 and predictor <= 15:
                # creates the string buffer
                string_buffer = colony.libs.string_buffer_util.StringBuffer()

                # png prediction can vary from row to row
                row_length = columns + 1

                # retrieves the decoded data length
                decoded_data_length = len(decoded_data)

                if not decoded_data_length % row_length == 0:
                    # raises a pdf read error exception
                    raise document_pdf_exceptions.PdfReadError("invalid row length: " + str(row_length))

                previous_rowdata = (0,) * row_length

                for row in xrange(len(decoded_data) / row_length):
                    # retrieves the current row data
                    row_data = [ord(x) for x in decoded_data[(row * row_length):((row + 1) * row_length)]]

                    # retrieves the filter byte
                    filterByte = row_data[0]

                    if filterByte == 0:
                        pass
                    elif filterByte == 1:
                        for i in range(2, row_length):
                            row_data[i] = (row_data[i] + row_data[i - 1]) % 256
                    elif filterByte == 2:
                        for i in range(1, row_length):
                            row_data[i] = (row_data[i] + previous_rowdata[i]) % 256
                    else:
                        # raises a pdf read error exception
                        raise document_pdf_exceptions.PdfReadError("unsupported png filter: " + repr(filterByte))

                    # sets the current row data as the previous row data
                    previous_rowdata = row_data

                    string_buffer.write("".join([chr(x) for x in row_data[1:]]))

                # retrieves the decoded data from the string buffer
                decoded_data = string_buffer.get_value()
            else:
                # raises a pdf read error exception
                raise document_pdf_exceptions.PdfReadError("unsupported flatedecode predictor: " + repr(predictor))

        # returns the decoded data
        return decoded_data

class AsciiHexFitler(DocumentPdfFilter):
    """
    The ascii hex filter class.
    """

    def __init__(self, filter_type = "ascii_hex"):
        """
        Constructor of the class.

        @type filter_type: String
        @param filter_type: The type of filter being used.
        """

        DocumentPdfFilter.__init__(self, filter_type)

    def decode(self, data, decode_parameters = {}):
        DocumentPdfFilter.decode(self, data, decode_parameters)

        # starts the string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        char = str()

        # starts the index
        index = 0

        while True:
            # retrieves the current character
            c = data[index]

            # in case the end of data
            # is found
            if c == ">":
                break
            # in case it's a space
            elif c.isspace():
                # increments the index
                index += 1

                # continues the loop
                continue

            char += c

            if len(char) == 2:
                # converts the character value from base 16
                # to "normal"character value
                string_buffer.write(chr(int(char, base = 16)))

                # resets the character value
                char = str()

            # increments the index
            index += 1

        assert char == ""

        # retrieves the decoded data from the string buffer
        decoded_data = string_buffer.get_value()

        # returns the decoded data
        return decoded_data

class Ascii85Filter(DocumentPdfFilter):
    """
    The ascii 85 filter class.
    """

    def __init__(self, filter_type = "ascii_85"):
        """
        Constructor of the class.

        @type filter_type: String
        @param filter_type: The type of filter being used.
        """

        DocumentPdfFilter.__init__(self, filter_type)

    def decode(self, data, decode_parameters = {}):
        # starts the decoded data
        decoded_data = str()

        group = []

        # starts the index
        index = 0

        hit_eod = False

        # remove all whitespace from data
        data = [value for value in data if not (value in " \n\r\t")]

        while not hit_eod:
            c = data[index]

            if len(decoded_data) == 0 and c == "<" and data[index + 1] == "~":
                index += 2
                continue
            elif c == "z":
                assert len(group) == 0

                decoded_data += "\x00\x00\x00\x00"

                continue
            elif c == "~" and data[index + 1] == ">":
                if len(group) != 0:
                    # cannot have a final group of just 1 char
                    assert len(group) > 1

                    cnt = len(group) - 1

                    group += [85, 85, 85]

                    hit_eod = cnt
                else:
                    break
            else:
                c = ord(c) - 33
                assert c >= 0 and c < 85
                group += [c]
            if len(group) >= 5:
                b = group[0] * (85 ** 4) + \
                    group[1] * (85 ** 3) + \
                    group[2] * (85 ** 2) + \
                    group[3] * 85 + \
                    group[4]

                assert b < (2 ** 32 - 1)

                c4 = chr((b >> 0) % 256)
                c3 = chr((b >> 8) % 256)
                c2 = chr((b >> 16) % 256)
                c1 = chr(b >> 24)

                decoded_data += (c1 + c2 + c3 + c4)

                if hit_eod:
                    decoded_data = decoded_data[:-4 + hit_eod]

                group = []

            # increments the index
            index += 1

        # returns the decoded data
        return decoded_data
