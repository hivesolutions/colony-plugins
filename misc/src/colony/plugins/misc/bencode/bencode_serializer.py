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

import re
import types
import datetime
import calendar

import colony.libs.string_buffer_util

import bencode_exceptions

EXCLUSION_MAP = {
    "__class__" : True,
    "__delattr__" : True,
    "__dict__" : True,
    "__doc__" : True,
    "__getattribute__" : True,
    "__hash__" : True,
    "__init__" : True,
    "__module__" : True,
    "__new__" : True,
    "__reduce__" : True,
    "__reduce_ex__" : True,
    "__repr__" : True,
    "__setattr__" : True,
    "__str__" : True,
    "__weakref__" : True,
    "__format__" : True,
    "__sizeof__" : True,
    "__subclasshook__" : True
}
""" The map of items to be excluded from object serialization """

EXCLUSION_TYPES = {
    types.MethodType : True,
    types.FunctionType : True
}
""" The map of types to be excluded from object serialization """

INT_TYPES = {
    types.IntType : True,
    types.LongType : True
}
""" The map of int types """

LIST_TYPES = {
    types.ListType : True,
    types.TupleType : True
}
""" The map of list types """

DECIMAL_REGEX_VALUE = "\d"
""" The decimal regular expression value """

DECIMAL_REGEX = re.compile(DECIMAL_REGEX_VALUE)
""" The decimal regular expression """

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

def _chunk(chunk, string_buffer):
    # retrieves the chunk type
    chunk_type = type(chunk)

    if chunk_type in INT_TYPES:
        # writes the integer chunk into the string buffer
        string_buffer.write("i" + str(chunk) + "e")
    elif chunk_type in types.StringTypes:
        # retrieves the chunk length
        chunk_length = len(chunk)

        # writes the string chunk into the string buffer
        string_buffer.write(str(chunk_length) + ":" + chunk)
    elif chunk_type in LIST_TYPES:
        # writes the start token in the
        # string buffer
        string_buffer.write("l")

        # iterates over all the chunk item
        # in the chunk
        for chunk_item in chunk:
            _chunk(chunk_item, string_buffer)

        # writes the end token in the
        # string buffer
        string_buffer.write("e")
    elif chunk_type == types.DictType:
        # writes the start token in the
        # string buffer
        string_buffer.write("d")

        # retrieves the chunk items
        chunk_items = chunk.items()

        # sorts the chunk items
        chunk_items.sort()

        # iterates over all the chunk items
        # to encode them
        for chunk_key, chunk_value in chunk_items:
            # retrieves the chunk key length
            chunk_key_length = len(chunk_key)

            # writes the chunk item in the string buffer
            string_buffer.write(str(chunk_key_length) + ":" + chunk_key)

            # "chunks" the chunk value
            _chunk(chunk_value, string_buffer)

        # writes the end token in the
        # string buffer
        string_buffer.write("e")
    elif chunk_type == datetime.datetime:
        # retrieves the chunk time tuple
        chunk_time_tuple = chunk.utctimetuple()

        # converts the chunk time tuple to timestamp
        chunk_timestamp = calendar.timegm(chunk_time_tuple)

        # writes the chunk timestamp into the string buffer
        string_buffer.write("i" + str(chunk_timestamp) + "e")
    elif chunk_type == types.InstanceType or hasattr(object, "__class__"):
        # writes the start token in the
        # string buffer
        string_buffer.write("d")

        # retrieves all the chunk keys
        chunk_keys = [value for value in dir(chunk) if not value.startswith("_") and not value in EXCLUSION_MAP and not type(getattr(chunk, value)) in EXCLUSION_TYPES]

        # sorts the chunk keys
        chunk_keys.sort()

        # iterates over all the chunk keys
        for chunk_key in chunk_keys:
            # retrieves the chunk key length
            chunk_key_length = len(chunk_key)

            # retrieves the chunk value from the chunk
            chunk_value = getattr(chunk, chunk_key)

            # writes the chunk item in the string buffer
            string_buffer.write(str(chunk_key_length) + ":" + chunk_key)

            # "chunks" the chunk value
            _chunk(chunk_value, string_buffer)

        # writes the end token in the
        # string buffer
        string_buffer.write("e")
    else:
        # raises the bencode encode exception
        raise bencode_exceptions.BencodeEncodeException("data type not defined: " + str(chunk))

def loads(data):
    # creates a list from the data
    # (the chunks list)
    chunks = list(data)

    # reverses the list
    chunks.reverse()

    # "dechunks" the data (retrieving the root element)
    root_element = _dechunk(chunks)

    # returns the root element
    return root_element

def _dechunk(chunks):
    # retrieves an item from
    # the chunks list
    item = chunks.pop()

    # in case the current item is a dictionary
    if item == "d":
        # retrieves an item from the
        # chunks list
        item = chunks.pop()

        # creates the (empty) map
        map = {}

        # iterates while the map end
        # is not reached
        while not item == "e":
            # adds the item to the chunks list
            # to be able to parse it bellow
            chunks.append(item)

            # retrieves the map key
            key = _dechunk(chunks)

            # retrieves the map value
            map[key] = _dechunk(chunks)

            # removes the item from the chunks list
            item = chunks.pop()

        # returns the map
        return map
    # in case the current item is a list
    elif item == "l":
        # retrieves an item from the
        # chunks list
        item = chunks.pop()

        # creates the empty list
        list = []

        # iterates while the list end
        # is not reached
        while not item == "e":
            # adds the item to the chunks list
            # to be able to parse it bellow
            chunks.append(item)

            # adds the "dechunked" chunk to the list
            list.append(_dechunk(chunks))

            # removes the item from the chunks list
            item = chunks.pop()

        # returns the list
        return list
    # in case the current item is an integer
    elif item == "i":
        # retrieves an item from the
        # chunks list
        item = chunks.pop()

        # sets the initial number value
        number = ""

        # iterates while the integer end
        # is not reached
        while not item == "e":
            # adds the item character to
            # the number value
            number += item

            # removes the item from the chunks list
            item = chunks.pop()

        # returns the integer converted value
        return int(number)
    # in case the current item is a string (starts with
    # the string size integer)
    elif DECIMAL_REGEX.findall(item):
        # sets the initial number value
        number = ""

        # iterates throughout the string size integer
        while DECIMAL_REGEX.findall(item):
            # adds the item character to
            # the number value
            number += item

            # removes the item from the chunks list
            item = chunks.pop()

        # starts the string value
        string_value = ""

        # iterates over the string value size
        for _index in range(1, int(number) + 1):
            # adds the character to the string value
            # and removes it from the chunks list
            string_value += chunks.pop()

        # returns the string value
        return string_value

    # raises the bencode decode exception
    raise bencode_exceptions.BencodeDecodeException("data type not defined: " + str(item))
