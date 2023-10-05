#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import types
import itertools

import colony

from . import exceptions

DEFAULT_ENCODING = "Cp1252"
""" The default encoding for CSV files, this
is defined according to the mostly used version
of the CSV in the computer industry """

NEWLINE_CHARACTER = "\n"
""" The newline character, that should
be present at the end of each CSV row """

SEPARATOR_CHARACTER = ";"
""" The separator character separating
each of the item columns in a CSV file """

SPECIAL_SEQUENCE = ("\n", "\r", ";")
""" The sequence string that defines the various
characters that should be replaced (sanitization) """

SPECIAL_MAP = dict([ord(key), ord(" ")] for key in SPECIAL_SEQUENCE)
""" The map version of the special sequence that map each
of the special items in the sequence into an invalid value """

LIST_TYPES = (list, tuple, types.GeneratorType, itertools.chain)
""" A tuple with the various list types considered
as proper sequences for the current serializer """

def dumps(object, encoding = DEFAULT_ENCODING):
    # "chunks" the object into a resulting generator
    # object that is going to be used for string
    chunks = _chunk(object)

    # joins the various chunks as a single string value
    # and then in case there's an encoding defined
    # encodes the data into the target encoding
    string_value = "".join([chunk for chunk in chunks])
    if encoding: string_value = string_value.encode(encoding, "ignore")

    # returns the string value as an unicode
    # or a raw/bytes string in case it was
    # properly decoded (using provided encoding)
    return string_value

def dumps_lazy(object, encoding = DEFAULT_ENCODING):
    # iterates over the complete set of chunk in the
    # generator encoding the chunk (if required) and
    # the re-yield the value to the upper layers
    for chunk in _chunk(object):
        if encoding: chunk = chunk.encode(encoding, "ignore")
        yield chunk

def _chunk(object, flatten = True, empty = True):
    # retrieves the object type
    object_type = type(object)

    # in case the object type is key to value
    # based (map or dictionary) must convert the
    # object into a list for processing
    if object_type == dict: object = [object]

    # in case the object type is neither an
    # instance nor a list it's considered not
    # valid and an exception should be raised
    elif not object_type in LIST_TYPES and not isinstance(object, LIST_TYPES):
        raise exceptions.CSVEncodeException("invalid object type")

    # in case the object is not set, is invalid
    # or is empty there is no need to codify it
    if not object: return

    # sets the "original" and default value for the attribute names
    # so that no local variable is referenced before assignment
    attribute_names = None

    # verifies if the type of the object provided for serialization
    # is generator, if that's the case special handling is required
    # as these objects defer in interface from tuples and lists
    is_generator = colony.legacy.is_generator(object)

    # retrieves the first object item to try to detect the kind
    # of mode for serialization that must be used
    _object_item = next(object) if is_generator else object[0]
    _object_item_type = type(_object_item)

    # in case the type of the first object item is a list or a tuple
    # the mode to be used is the simple one not the map mode, otherwise
    # the map mode is used (usable for both object and maps)
    if _object_item_type in LIST_TYPES: map_mode = False
    else: map_mode = True

    # in case the flatten mode is set and the current object item is a
    # map it must be first "flattened" so that it can be used with the
    # complete set of relations properly set for it
    flatten = flatten and map_mode
    if flatten: _object_item = colony.map_flatten(_object_item)

    # in case the map mode is enabled the header value must
    # be encoded by retrieving the names of the first object
    # element (considered to be the header element representation)
    if map_mode:
        # retrieves the (header) attribute names in order to create
        # the header value from its names, note that the flatten value
        # is provided so that it may be used in the proper attribute
        # names retrieval as new names may become available for flat
        attribute_names = _attribute_names(
            _object_item,
            object = [] if is_generator else object,
            flatten = flatten
        )
        header_value = SEPARATOR_CHARACTER.join(attribute_names) + NEWLINE_CHARACTER

        # verifies if the header is encoded as an unicode string
        # if that's not the case it must be converted into an
        # unicode string using the default encoding for writing
        is_unicode = type(header_value) == colony.legacy.UNICODE
        if not is_unicode: header_value = header_value.decode("utf-8")

        # yields the header value into current generator, note that
        # this value is defined as an unicode based string
        yield header_value

    # in case the generator mode is defined we must run the proper
    # chunk line operation for the first line as we're never going
    # to have a chance to iterate over that line again
    if is_generator:
        chunks = _chunk_line(
            _object_item,
            attribute_names = attribute_names,
            empty = empty,
            map_mode = map_mode
        )
        for chunk in chunks: yield chunk

    # iterates over all the object (items) in the object list for
    # serialization so that it's able to chunk (serialize) each item
    for object_item in object:
        if flatten: object_item = colony.map_flatten(object_item)
        chunks = _chunk_line(
            object_item,
            attribute_names = attribute_names,
            empty = empty,
            map_mode = map_mode
        )
        for chunk in chunks: yield chunk

def _chunk_line(object_item, attribute_names = None, empty = True, map_mode = False):
    # retrieves the various object items attribute values
    # (from the previously calculated attribute names) in
    # case the simple mode is used there is no need to retrieve
    # them using the header name
    attribute_values = map_mode and colony.object_attribute_values(
        object_item,
        attribute_names,
        strict = False
    ) or object_item

    # retrieves the attribute values length
    attribute_values_length = len(attribute_values)

    # starts the index value, that is going to be used in
    # the write operation of the various attributes in line
    index = 0

    # iterates over all the attribute values
    # to yield them into the current generator
    for attribute_value in attribute_values:
        # retrieves the attribute value type, this is going to
        # be used to determine the proper encoding operation
        attribute_value_type = type(attribute_value)

        # verifies the proper attribute type and according
        # to that creates the proper unicode based string
        # to be yield to the current generator, note that for
        # byte based strings the default encoding for the
        # system is used as a fallback (possible to fail)
        if empty and attribute_value == None:
            attribute_value = colony.legacy.u("")
        elif attribute_value_type == colony.legacy.BYTES:
            attribute_value = attribute_value.decode("utf-8")
        elif not attribute_value_type in colony.legacy.STRINGS:
            attribute_value = colony.legacy.UNICODE(attribute_value)

        # "sanitizes" the attribute value by removed some of the
        # problematic characters from the attribute value
        attribute_value = attribute_value.translate(SPECIAL_MAP)

        # yields the (decoded) attribute value, in case
        # the value is valid (avoiding invalid values)
        if attribute_value: yield attribute_value

        # in case the current index represents the last
        # attribute must continue the loop as the the
        # separator character is not required in this case
        if index == attribute_values_length - 1: continue

        # yields the separator character and then increments
        # the current index so that it's possible to count values
        separator = colony.legacy.u(SEPARATOR_CHARACTER)
        yield separator
        index += 1

    # yields the new line in the current generator, note that the value
    # is first encoded as an unicode string (provides common ground)
    newline = colony.legacy.u(NEWLINE_CHARACTER)
    yield newline

def _attribute_names(object_item, object = [], sort = True, flatten = True):
    # creates the first and initial set of attribute names
    # from the first object item, this is considered to be
    # the default one from which all the other will intersect
    attribute_names = colony.object_attribute_names(object_item)

    # iterates over all the other object items in the set
    # in order to intersect the attributes name list with the
    # previous, this would create the complete names set
    for object_item in object:
        # retrieves the object attribute names for the current
        # object item value and then intersects the current
        # names list with the new one (avoiding duplicates)
        if flatten: object_item = colony.map_flatten(object_item)
        object_attribute_names = colony.object_attribute_names(object_item)
        attribute_names = colony.list_intersect(
            attribute_names,
            object_attribute_names
        )

    # in case the sort flag is set sorts the gathered attribute
    # names and then returns them to the caller method
    if sort: attribute_names.sort()
    return attribute_names

def loads(data, header = True):
    # strips the data from extra lines
    # (avoids possible problems)
    data = data.strip()

    # splits the data around the new line character
    chunks = [value.strip() for value in data.split(NEWLINE_CHARACTER)]

    # "dechunks" the data (retrieving the object list) and then returns
    # the "loaded" object to the caller method (result value)
    object = _dechunk(chunks, header)
    return object

def _dechunk(chunks, header):
    # creates the object list
    object_list = []

    # retrieves the header value and unpacks it retrieving its complete
    # set of names, considering them to be the header of the CSV
    header_value = chunks[0]
    header_names = [value.strip() for value in header_value.split(SEPARATOR_CHARACTER)]

    # calculates the number of header names
    number_header_names = len(header_names)

    # retrieves the header names, using the
    # token indexes in case no header is defined
    header_names = header and header_names or colony.legacy.range(number_header_names)

    # retrieves the "various" content values
    content_values = header and chunks[1:] or chunks

    # iterates over all the content
    # in the content values
    for content in content_values:
        # creates a new (CSV) object (map)
        object = {}

        # retrieves the various object attributes
        object_attributes = [value.strip() for value in content.split(SEPARATOR_CHARACTER)]

        # starts the index value
        index = 0

        # iterates over all the object attributes
        # to set them in the object
        for attribute in object_attributes:
            # retrieves the (current) attribute name
            # from the header names and then sets the
            # the attribute in the object, incrementing
            # then the index value (new iteration)
            attribute_name = header_names[index]
            object[attribute_name] = attribute
            index += 1

        # adds the object to the object list
        object_list.append(object)

    # returns the object list
    return object_list
