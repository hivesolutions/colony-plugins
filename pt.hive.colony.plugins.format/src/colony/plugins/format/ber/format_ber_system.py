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

import types

import format_ber_exceptions

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

ENUMERATED_TYPE = 0x0a
""" The enumerated type """

SEQUENCE_TYPE = 0x10
""" The sequence type """

PRIMITIVE_MODE = 0x00
""" The primitive mode """

CONSTRUCTED_MODE = 0x01
""" The constructed mode """

UNIVERSAL_CLASS = 0x00
""" The universal class """

APPLICATION_CLASS = 0x01
""" The application class """

CONTEXT_SPECIFIC_CLASS = 0x02
""" The context specific class """

PRIVATE_CLASS = 0x03
""" The private class """

TYPE_VALUE = "type"
""" The type value """

VALUE_VALUE = "value"
""" The value value """

EXTRA_TYPE_VALUE = "extra_type"
""" The extra type value """

TYPE_NUMBER_VALUE = "type_number"
""" The type number value """

TYPE_CONSTRUCTED_VALUE = "type_constructed"
""" The type constructed value """

TYPE_CLASS_VALUE = "type_class"
""" The type class value """

DEFAULT_TYPE_CONSTRUCTED = {EOC_TYPE : 0x00,
                            BOOLEAN_TYPE : 0x00,
                            INTEGER_TYPE : 0x00,
                            BIT_STRING_TYPE : 0x00,
                            OCTET_STRING_TYPE : 0x00,
                            ENUMERATED_TYPE : 0x00,
                            SEQUENCE_TYPE : 0x01}
""" The map containing the default constructed values for the types """

DEFAULT_CLASS = 0x00
""" The default class to be used """

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

    pack_methods_map = {}
    """ The map containing the references to the pack methods """

    unpack_methods_map = {}
    """ The map containing the references to the unpack methods """

    type_alias_map = {}
    """ The type alias map """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.buffer = colony.libs.string_buffer_util.StringBuffer()
        self.type_alias_map = {}

        # creates the pack methods map reference
        self.pack_methods_map = {INTEGER_TYPE : self.pack_integer,
                                 OCTET_STRING_TYPE : self.pack_octet_string,
                                 ENUMERATED_TYPE : self.pack_enumerated,
                                 SEQUENCE_TYPE : self.pack_sequence}

        # creates the unpack methods map reference
        self.unpack_methods_map = {INTEGER_TYPE : self.unpack_integer,
                                   OCTET_STRING_TYPE : self.unpack_octet_string,
                                   ENUMERATED_TYPE : self.unpack_enumerated,
                                   SEQUENCE_TYPE : self.unpack_sequence}

    def to_hex(self, string_value):
        for index in string_value:
            print "0x%02x" % ord(index),

    def pack(self, value):
        # retrieves the type number for the value
        type_number = self._get_type_number(value)

        # retrieves the pack method for the type number
        pack_method = self._get_pack_method(type_number)

        # packs the value
        packed_value = pack_method(value)

        # returns the packed value
        return packed_value

    def unpack(self, packed_value):
        # retrieves the type for the packed number value
        type_number = self._get_packed_type_number(packed_value)

        # retrieves the unpack method for the type number
        unpack_method = self._get_unpack_method(type_number)

        # unpacks the packed value
        value = unpack_method(packed_value)

        # returns the value
        return value

    def pack_integer(self, integer):
        # resolves the integer type
        integer_type = self._get_type(integer)

        # retrieves the integer type
        integer_type = self._get_extra_type(integer, integer_type)

        # retrieves the integer value
        integer_value = self._get_value(integer)

        # packs the integer value
        packed_integer = self._pack_integer(integer_value)

        # packs the integer as a base value
        packed_integer = self.pack_base_value(packed_integer, integer_type)

        # returns the packed integer
        return packed_integer

    def pack_octet_string(self, octet_string):
        # resolves the octet string type
        octet_string_type = self._get_type(octet_string)

        # retrieves the octet string type
        octet_string_type = self._get_extra_type(octet_string, octet_string_type)

        # retrieves the octet string value
        octet_sting_value = self._get_value(octet_string)

        # packs the octet string value
        packed_octet_string = self._pack_octet_string(octet_sting_value)

        # packs the octet string as a base value
        packed_octet_string = self.pack_base_value(packed_octet_string, octet_string_type)

        # returns the packed octet string
        return packed_octet_string

    def pack_enumerated(self, enumerated):
        # resolves the enumerated type
        enumerated_type = self._get_type(enumerated)

        # retrieves the enumerated type
        enumerated_type = self._get_extra_type(enumerated, enumerated_type)

        # retrieves the enumerated value
        enumerated_value = self._get_value(enumerated)

        # packs the enumerated value (as integer)
        packed_enumerated = self._pack_integer(enumerated_value)

        # packs the enumerated as a base value
        packed_enumerated = self.pack_base_value(packed_enumerated, enumerated_type)

        # returns the packed enumerated
        return packed_enumerated

    def pack_sequence(self, sequence):
        # resolves the sequence type
        sequence_type = self._get_type(sequence)

        # retrieves the sequence type
        sequence_type = self._get_extra_type(sequence, sequence_type)

        # retrieves the sequence value
        sequence_value = self._get_value(sequence)

        # packs the sequence value
        packed_sequence = self._pack_sequence(sequence_value)

        # packs the sequence as a base value
        packed_sequence = self.pack_base_value(packed_sequence, sequence_type)

        # returns the packed sequence
        return packed_sequence

    def pack_base_value(self, packed_base_value, type = EOC_TYPE):
        # calculates the packed base value length
        packed_base_value_length = len(packed_base_value)

        # packs the packed base value length
        packed_base_value_length_packed = self._pack_length(packed_base_value_length)

        # creates the packed base value concatenating the type the length
        # and the value of the base value
        packed_base_value = chr(type) + packed_base_value_length_packed + packed_base_value

        # returns the packed base value
        return packed_base_value

    def unpack_integer(self, packed_integer):
        # resolves the integer type
        integer_type = self._resolve_base_type(INTEGER_TYPE)

        # retrieves the packed integer extra type
        packed_integer_extra_type = self._get_packed_extra_type(packed_integer, integer_type)

        # retrieves the packed integer value
        packed_integer_value = self._get_packed_value(packed_integer)

        # unpacks the packed integer value
        upacked_integer_value = self._unpack_integer(packed_integer_value)

        # unpacks the integer as a base value
        integer = self.unpack_base_value(upacked_integer_value, integer_type, packed_integer_extra_type)

        # returns the integer
        return integer

    def unpack_octet_string(self, packed_octet_string):
        # resolves the octet string type
        octet_string_type = self._resolve_base_type(OCTET_STRING_TYPE)

        # retrieves the packed octet string extra type
        packed_octet_string_extra_type = self._get_packed_extra_type(packed_octet_string, octet_string_type)

        # retrieves the packed octet string value
        packed_octet_string_value = self._get_packed_value(packed_octet_string)

        # unpacks the packed octet string value
        upacked_octet_string_value = self._unpack_octet_string(packed_octet_string_value)

        # unpacks the octet string as a base value
        octet_string = self.unpack_base_value(upacked_octet_string_value, octet_string_type, packed_octet_string_extra_type)

        # returns the octet string
        return octet_string

    def unpack_enumerated(self, packed_enumerated):
        # resolves the enumerated type
        enumerated_type = self._resolve_base_type(ENUMERATED_TYPE)

        # retrieves the packed enumerated extra type
        packed_enumerated_extra_type = self._get_packed_extra_type(packed_enumerated, enumerated_type)

        # retrieves the packed enumerated value
        packed_enumerated_value = self._get_packed_value(packed_enumerated)

        # unpacks the packed enumerated value (as integer)
        upacked_enumerated_value = self._unpack_integer(packed_enumerated_value)

        # unpacks the enumerated as a base value
        enumerated = self.unpack_base_value(upacked_enumerated_value, enumerated_type, packed_enumerated_extra_type)

        # returns the enumerated
        return enumerated

    def unpack_sequence(self, packed_sequence):
        # resolves the sequence type
        sequence_type = self._resolve_base_type(SEQUENCE_TYPE)

        # retrieves the packed sequence extra type
        packed_sequence_extra_type = self._get_packed_extra_type(packed_sequence, sequence_type)

        # retrieves the packed sequence value
        packed_sequence_value = self._get_packed_value(packed_sequence)

        # unpacks the packed sequence value
        upacked_sequence_value = self._unpack_sequence(packed_sequence_value)

        # unpacks the sequence as a base value
        sequence = self.unpack_base_value(upacked_sequence_value, sequence_type, packed_sequence_extra_type)

        # returns the sequence
        return sequence

    def unpack_base_value(self, unpacked_base_value, type = EOC_TYPE, extra_type = None):
        # retrieves the type tuple for the given type
        type_number, type_constructed, type_class = self._get_type_tuple(None, type)

        # creates the type map (to set as type value)
        type_map = {TYPE_NUMBER_VALUE : type_number,
                    TYPE_CONSTRUCTED_VALUE : type_constructed,
                    TYPE_CLASS_VALUE : type_class}

        # creates the unpacked base value
        unpaked_base_value = {TYPE_VALUE : type_map, VALUE_VALUE : unpacked_base_value}

        # in case the extra type is defined
        if not extra_type == None:
            # retrieves the extra type tuple for the given extra type
            extra_type_number, extra_type_constructed, extra_type_class = self._get_type_tuple(None, extra_type)

            # creates the extra type map (to set as extra type value)
            extra_type_map = {TYPE_NUMBER_VALUE : extra_type_number,
                              TYPE_CONSTRUCTED_VALUE : extra_type_constructed,
                              TYPE_CLASS_VALUE : extra_type_class}

            # sets the extra type (map) in the unpacked base value
            unpaked_base_value[EXTRA_TYPE_VALUE] = extra_type_map

        # returns the unpacked base value
        return unpaked_base_value

    def get_type_alias_map(self):
        """
        Retrieves the type alias map.

        @rtype: Dictionary
        @return: The type alias map.
        """

        return self.type_alias_map

    def set_type_alias_map(self, type_alias_map):
        """
        Sets the type alias map.

        @type type_alias_map: Dictionary
        @param type_alias_map: The type alias map.
        """

        self.type_alias_map = type_alias_map

    def _pack_length(self, length):
        # in case the length is less than 0x80
        if length < 0x80:
            return chr(length)
        else:
            # creates the substrate string
            substrate = str()

            # iterates while there is length available
            while length:
                # calculates the substrate from the previous
                # substrate
                substrate = chr(length & 0xff) + substrate

                # shifts the length eight bits
                # to the right
                length = length >> 8

            # retrieves the substrate length
            substrate_length = len(substrate)

            # in case the length of the substrate is too big (overflow)
            if substrate_length > 126:
                # raises the packing error
                raise format_ber_exceptions.PackingError("length octets overflow: %d" % substrate_length)

            return chr(0x80 | len(substrate)) + substrate

    def _unpack_length(self, packed_length):
        # sets the packed value as the substrate
        substrate = packed_length

        # retrieves the first octet
        first_octet = ord(substrate[0])

        if first_octet == 0x80:
            size = 1
            length = -1
        elif first_octet < 0x80:
            size = 1
            length = first_octet
        else:
            # retrieves the size of the length string
            size = first_octet & 0x7F

            # retrieves the substrate length
            substrate_length = len(substrate)

            # in case the size is bigger than the
            # substrate length without one value, there is no
            # space for the length value in the substrate
            if size > substrate_length - 1:
                # raises the unpacking error
                raise format_ber_exceptions.UnpackingError("invalid substrate value invalid size: %d" % substrate_length)

            # encoded in length bytes
            length = 0

            # retrieves the length string
            length_string = substrate[1:size + 1]

            # iterates over all the characters in the
            # length string
            for length_character in length_string:
                # increments the length with the current
                # length character value
                length = (length << 8) | ord(length_character)

            # increments the size for the extra value
            size += 1

        # returns the length
        return length, size

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

    def _pack_octet_string(self, value):
        # sets the octets string as the value
        octets_string = value

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
            # packs the value
            packed_value = self.pack(value)

            # writes the packed value in the sequence buffer
            sequence_list.append(packed_value)

        # joins the sequence list to retrieve the octets string
        octets_string = "".join(sequence_list)

        # returns the octets string
        return octets_string

    def _unpack_integer(self, packed_value):
        octets = map(ord, packed_value)

        if octets[0] & 0x80:
            integer = -1
        else:
            integer = 0

        for octet in octets:
            integer = integer << 8 | octet

        # returns the integer
        return integer

    def _unpack_octet_string(self, packed_value):
        # sets the packed string as the octet string
        octet_string = packed_value

        # returns the octet string
        return octet_string

    def _unpack_sequence(self, packed_value):
        # retrieves the packed value length
        packed_value_length = len(packed_value)

        # starts the index counter value
        index = 0

        # creates the values list to hold
        # the sequence values
        values_list = []

        # iterates while the index has not reached
        # the packed value length
        while index < packed_value_length:
            # retrieves the current packed value
            current_packed_value_buffer = packed_value[index:]

            # retrieves the current packed value length and length size
            current_packed_value_length, current_packed_value_length_size = self._get_packed_length(current_packed_value_buffer)

            # calculates the current packed value total length
            current_packed_value_total_length = current_packed_value_length + current_packed_value_length_size + 1

            # retrieves the "real" current packed value
            current_packed_value = packed_value[index:index + current_packed_value_total_length]

            # unpacks the current packed value, retrieving the current value
            current_value = self.unpack(current_packed_value)

            # adds the current value to the values list
            values_list.append(current_value)

            # increments the index
            index += current_packed_value_total_length

        # sets the sequence as the values list
        sequence = values_list

        # returns the sequence
        return sequence

    def _resolve_base_type(self, value):
        type_value = {}

        type_value[TYPE_NUMBER_VALUE] = value

        type = self._resolve_type(type_value)

        return type

    def _resolve_type(self, type_value):
        # retrieves the type of the type value
        type_value_type = type(type_value)

        # in case the type is described
        # as a direct integer value
        if type_value_type == types.IntType:
            # sets the type number as the type value
            type_number = type_value

            # sets the type value as an empty map
            type_value = {}
        # otherwise it must be a dictionary
        else:
            # retrieves the type number from the type value
            type_number = type_value[TYPE_NUMBER_VALUE]

        # retrieves the default type constructed
        default_type_constructed = DEFAULT_TYPE_CONSTRUCTED.get(type_number, PRIMITIVE_MODE)

        # retrieves the type constructed from the type value
        type_constructed = type_value.get(TYPE_CONSTRUCTED_VALUE, default_type_constructed)

        # retrieves the type class from the type value
        type_class = type_value.get(TYPE_CLASS_VALUE, DEFAULT_CLASS)

        # starts the type value from the type number
        _type = type_number

        # adds the type constructed to the type
        _type |= type_constructed << 5

        # adds the type class to the type
        _type |= type_class << 6

        # returns the type
        return _type

    def _get_type(self, value, base_index = TYPE_VALUE):
        # in case the base index does not exist
        # in the value
        if not base_index in value:
            # returns invalid
            return None

        # retrieves the type value from the value
        type_value = value[base_index]

        # resolves the type
        type = self._resolve_type(type_value)

        # returns the type
        return type

    def _get_type_tuple(self, value, type = None):
        # retrieves the type for the value
        type = type or self._get_type(value)

        # retrieves the type number
        type_number = self._get_type_number(value, type)

        # retrieves the type constructed
        type_constructed = self._get_type_constructed(value, type)

        # retrieves the type class
        type_class = self._get_type_class(value, type)

        # creates the type tuple from the
        # number, constructed and class
        type_tuple = (type_number, type_constructed, type_class)

        # returns the type tuple
        return type_tuple

    def _get_type_number(self, value, type = None):
        # retrieves the type for the value
        type = type or self._get_type(value)

        # retrieves the type number from the type
        type_number = type & 0x1f

        # returns the type number
        return type_number

    def _get_type_constructed(self, value, type = None):
        # retrieves the type for the value
        type = type or self._get_type(value)

        # retrieves the type constructed from the type
        type_constructed = (type & 0x20) >> 5

        # returns the type constructed
        return type_constructed

    def _get_type_class(self, value, type = None):
        # retrieves the type for the value
        type = type or self._get_type(value)

        # retrieves the type class from the type
        type_class = (type & 0xc0) >> 6

        # returns the type class
        return type_class

    def _get_value(self, value):
        return value[VALUE_VALUE]

    def _get_extra_type(self, value, base_type = EOC_TYPE):
        return self._get_type(value, EXTRA_TYPE_VALUE) or base_type

    def _get_packed_type_number(self, packed_value):
        # retrieves the extra type for the packed value
        extra_type = self._get_packed_extra_type(packed_value)

        # retrieves the type tuple from the extra type
        type_number, _type_constructed, type_class = self._get_type_tuple(None, extra_type)

        # retrieves the type alias map for the type class
        type_alias_map = self.type_alias_map.get(type_class, {})

        # retrieves the type for the extra type
        type_number = type_alias_map.get(type_number, type_number)

        # returns the type number
        return type_number

    def _get_packed_extra_type(self, packed_value, base_type = EOC_TYPE):
        # retrieves the extra type octet (character)
        extra_type_octet = packed_value[0]

        # converts the extra type octet to ordinal
        extra_type = ord(extra_type_octet)

        # in case the extra type and the base
        # type are the same
        if extra_type == base_type:
            # returns invalid
            return None

        # returns the extra type
        return extra_type

    def _get_packed_length(self, packed_value):
        # retrieves the packed length from the packed
        # value
        packed_length = packed_value[1:]

        # unpacks the length and size from the packed length
        length, size = self._unpack_length(packed_length)

        # returns the length and size
        return length, size

    def _get_packed_value(self, packed_base_value):
        # retrieves the packed base value length and length size
        _packed_base_value_length, packed_base_value_length_size = self._get_packed_length(packed_base_value)

        # calculates the base value for retrieval of the packed value
        base_value = packed_base_value_length_size + 1

        # retrieves the packed value
        packed_value = packed_base_value[base_value:]

        # returns the packed value
        return packed_value

    def _get_pack_method(self, type_number):
        # retrieves the pack method for the type number
        pack_method = self.pack_methods_map[type_number]

        # returns the pack method
        return pack_method

    def _get_unpack_method(self, type_number):
        # retrieves the unpack method for the type number
        unpack_method = self.unpack_methods_map[type_number]

        # returns the unpack method
        return unpack_method
