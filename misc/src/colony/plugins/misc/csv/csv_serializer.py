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

__revision__ = "$LastChangedRevision: 5720 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-21 17:36:22 +0100 (qua, 21 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types

import colony.libs.list_util
import colony.libs.object_util
import colony.libs.string_buffer_util

import csv_exceptions

DEFAULT_ENCODING = "Cp1252"
""" The default encoding for csv files """

NEWLINE_CHARACTER = "\n"
""" The newline character """

SEPARATOR_CHARACTER = ";"
""" The separator character """

LIST_TYPES = (types.ListType, types.TupleType)
""" A tuple with the various list types """

def dumps(object):
    # creates a new string buffer
    string_buffer = colony.libs.string_buffer_util.StringBuffer()

    # "chunks" the object into the string buffer
    _chunk(object, string_buffer)

    # retrieves the string value from the
    # string buffer
    string_value = string_buffer.get_value()

    # returns the string value
    return string_value

def _chunk(object, string_buffer):
    # retrieves the object type
    object_type = type(object)

    # in case the object type is an instance
    # or a map (dictionary)
    if object_type in (types.InstanceType, types.DictionaryType):
        # converts the object into a list
        object = [object]
    # in case the object type is neither an
    # instance nor a list
    elif not object_type in LIST_TYPES:
        # raises the csv encoder exception
        raise csv_exceptions.CsvEncodeException("invalid object type")

    # in case the object is not set, is invalid
    # or is empty there is no need to codify it
    if not object: return

    # retrieves the first object item to try to detect the kind
    # of mode for serialization that must be used
    _object_item = object[0]
    _object_item_type = type(_object_item)

    # in case the type of the first object item is a list or a tuple
    # the mode to be used is the simple one not the map mode, otherwise
    # the map mode is used (usable for both object and maps)
    if _object_item_type in LIST_TYPES: map_mode = False
    else: map_mode = True

    # in case the map mode is enabled the header value must
    # be encoded by retrieving the names of the first object
    # element (considered to be the header element representation)
    if map_mode:
        # retrieves the (header) attribute names in order to
        # create the header value
        attribute_names = _attribute_names(object)
        header_value = SEPARATOR_CHARACTER.join(attribute_names) + NEWLINE_CHARACTER

        # writes the header value to the string buffer
        string_buffer.write(header_value)

    # iterates over all the object (items)
    # in the object list for serialization
    for object_item in object:
        # retrieves the various object items attribute values
        # (from the previously calculated attribute names) in
        # case the simple mode is used there is no need to retrieve
        # them using the header name
        attribute_values = map_mode and colony.libs.object_util.object_attribute_values(object_item, attribute_names) or object_item

        # retrieves the attribute values length
        attribute_values_length = len(attribute_values)

        # starts the index value
        index = 0

        # iterates over all the attribute values
        # to write them to the string buffer
        for attribute_value in attribute_values:
            # retrieves the attribute value type
            attribute_value_type = type(attribute_value)

            # in case the attribute value is not of string types uses the default
            # system conversion to convert then if the attribute value is of type
            # unicode encodes the attribute value using the default encoding
            if not attribute_value_type in (types.StringType, types.UnicodeType): attribute_value = str(attribute_value)
            attribute_value_encoded = attribute_value_type == types.UnicodeType and attribute_value.encode(DEFAULT_ENCODING) or (attribute_value and str(attribute_value))

            # writes the encoded attribute value (in case
            # the value is valid)
            attribute_value_encoded and string_buffer.write(attribute_value_encoded)

            # in case the current index represents
            # the last attribute
            if index == attribute_values_length - 1:
                # continue the loop skipping the separator
                # character writing
                continue

            # writes the separator character
            string_buffer.write(SEPARATOR_CHARACTER)

            # increments the index
            index += 1

        # writes the new line in the string buffer
        string_buffer.write(NEWLINE_CHARACTER)

def _attribute_names(object):
    # retrieves the first element (for initial
    # set reference)
    object_item = object[0]

    # creates the first and initial set of attribute names
    # from the first object item
    attribute_names = colony.libs.object_util.object_attribute_names(object_item)

    # iterates over all the other object items in the set
    # in order to intersect the attributes name list with the
    # previous
    for object_item in object:
        # retrieves the object attribute names for the current
        # object item value
        object_attribute_names = colony.libs.object_util.object_attribute_names(object_item)

        # intersects the attribute names list with the object attribute names
        # list to calculate the current attribute names
        attribute_names = colony.libs.list_util.list_intersect(attribute_names, object_attribute_names)

    # returns the attribute names
    return attribute_names

def loads(data, header = True):
    # strips the data from extra lines
    # (avoids possible problems)
    data = data.strip()

    # splits the data around the new line character
    chunks = [value.strip() for value in data.split(NEWLINE_CHARACTER)]

    # "dechunks" the data (retrieving the object list)
    object = _dechunk(chunks, header)

    # returns the object (list)
    return object

def _dechunk(chunks, header):
    # creates the object list
    object_list = []

    # retrieves the header value
    header_value = chunks[0]

    # retrieves the header value
    header_names = [value.strip() for value in header_value.split(SEPARATOR_CHARACTER)]

    # calculates the number of header names
    number_header_names = len(header_names)

    # retrieves the header names, using the
    # token indexes in case no header is defined
    header_names = header and header_names or range(number_header_names)

    # retrieves the "various" content values
    content_values = header and chunks[1:] or chunks

    # iterates over all the content
    # in the content values
    for content in content_values:
        # creates a new (csv) object (map)
        object = {}

        # retrieves the various object attributes
        object_attributes = [value.strip() for value in content.split(SEPARATOR_CHARACTER)]

        # starts the index value
        index = 0

        # iterates over all the object attributes
        # to set them in the object
        for attribute in object_attributes:
            # retrieves the (current) attribute name
            # from the header names
            attribute_name = header_names[index]

            # set the attribute in the object
            object[attribute_name] = attribute

            # increments the index value
            index += 1

        # adds the object to the object list
        object_list.append(object)

    # returns the object list
    return object_list
