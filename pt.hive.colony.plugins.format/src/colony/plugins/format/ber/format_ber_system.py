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

import colony.libs.string_buffer_util

EOC_TYPE = 0x00
""" The eoc (end of content) type """

BOOLEAN_TYPE = 0x01
""" The boolean type """

INTEGER_TYPE = 0x02
""" The integer type """

BIT_STRING_TYPE = 0x03
""" The bit string type """

OCTET_STRING_TYPE = 0x04
""" The octet string type """

SEQUENCE_TYPE = 0x30
""" The sequence type """

APPLICATION_TYPE = 0x60
""" The application (base) type """

class FormatBer:
    """
    The format ber class.
    """

    format_ber_plugin = None
    """ The format ber plugin """

    def __init__(self, format_ber_plugin):
        """
        Constructor of the class.

        @type format_ber_plugin: FormatBerPlugin
        @param format_ber_plugin: The format ber plugin.
        """

        self.format_ber_plugin = format_ber_plugin

    def create_structure(self, parameters):
        return BerStructure()

class BerStructure:
    """
    Class representing a ber structure.
    """

    buffer = None
    """ The buffer to be used """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.buffer = colony.libs.string_buffer_util.StringBuffer()

    def to_hex(self, string_value):
        for i in string_value:
            print "0x%02x" % ord(i),

    def pack_integer(self, integer):
        # packs the integer value
        packed_integer = self._pack_integer(integer)

        # packs the integer as a base value
        packed_integer = self.pack_basic_value(packed_integer, INTEGER_TYPE)

        # returns the packed integer
        return packed_integer

    def pack_sequence(self, sequence):
        # packs the sequence value
        packed_sequence = self._pack_sequence(sequence)

        # packs the sequence as a base value
        packed_sequence = self.pack_basic_value(packed_sequence, SEQUENCE_TYPE)

        # returns the packed sequence
        return packed_sequence

    def pack_choice(self, choice):
        # packs the choice value
        packed_choice = self._pack_choice(choice)

        # retrieves the choice type
        choice_type = self._get_type(choice)

        # packs the choice as a base value
        packed_choice = self.pack_basic_value(packed_choice, choice_type)

        # returns the packed choice
        return packed_choice

    def pack_basic_value(self, packed_base_value, type = EOC_TYPE):
        # calculates the packed base value length
        packed_base_value_length = len(packed_base_value)

        # packs the packed base value length
        packed_base_value_length_packed = self._pack_length(packed_base_value_length)

        # creates the packed basic value concatenating the type the length
        # and the value of the basic value
        packed_basic_value = chr(type) + packed_base_value_length_packed + packed_base_value

        # returns the packed basic value
        return packed_basic_value

    def _pack_length(self, length):
        #if not defMode and self.supportIndefLenMode:
        #    return "\x80"

        if length < 0x80:
            return chr(length)
        else:
            substrate = str()

            # iterates while there is length available
            while length:
                # calculates the substrate from the previous
                # substrate
                substrate = chr(length & 0xff) + substrate

                # shifts the length eight bits
                # to the right
                length = length >> 8

            if len(substrate) > 126:
                raise Exception("Length octets overflow (%d)" % len(substrate))

            return chr(0x80 | len(substrate)) + substrate

    def _pack_integer(self, value):
        # creates the list to hold the octets
        octets = []

        # converts the value to long, to save on operations
        value = long(value)

        # iterates continuously
        while True:
            # insets the value in the octets list
            # with an and on the bit value
            octets.insert(0, value & 0xff)

            # in case the value is zero or minus
            # one (end of value)
            if value == 0 or value == -1:
                # breaks the loop
                break

            # shifts the value eight bits
            # to the right
            value = value >> 8

        # in case the
        if value == 0 and octets[0] & 0x80:
            octets.insert(0, 0)

        while len(octets) > 1 and (octets[0] == 0 and octets[1] & 0x80 == 0 or octets[0] == 0xff and octets[1] & 0x80 != 0):
            del octets[0]

        # creates the octets list from the list of values
        chracter_octets = [chr(value) for value in octets]

        # creates the octets string joining the octet characters
        octets_string = "".join(chracter_octets)

        # returns the octets string
        return octets_string

    def _pack_sequence(self, value):
        # saves the value as values list
        values_list = value

        # creates a list to hold the packed sequence values
        sequence_list = []

        # iterates over all the values in
        # the values list
        for value in values_list:
            # retrieves the type for the value
            type = self._get_type(value)

            # retrieves the real for the value
            real_value = self._get_type(value)

            # retrieves the pack method for the type
            pack_method = self.get_pack_method(type)

            # packs the value
            packed_value = pack_method(real_value)

            # writes the packed value in the sequence buffer
            sequence_list.append(packed_value)

        # joins the sequence list to retrieve the octets string
        octets_string = "".join(sequence_list)

        # returns the octets string
        return octets_string

    def _get_type(self, value):
        return value[0]

    def _get_value(self, value):
        return value[1]

    def get_pack_method(self, type):
        a = {0x02 : self.pack_integer,
             0x30 : self.pack_sequence}

        return a[type]
