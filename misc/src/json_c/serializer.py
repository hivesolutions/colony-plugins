#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

__credits__ = "Jan-Klaas Kollhof <keyjaque@yahoo.com>"
""" The credits for the module """

import re
import sys
import types
import decimal
import calendar
import datetime
import itertools

import colony

from . import exceptions

EXCLUSION_MAP = {
    "__class__": True,
    "__delattr__": True,
    "__dict__": True,
    "__doc__": True,
    "__getattribute__": True,
    "__hash__": True,
    "__init__": True,
    "__module__": True,
    "__new__": True,
    "__reduce__": True,
    "__reduce_ex__": True,
    "__repr__": True,
    "__setattr__": True,
    "__str__": True,
    "__weakref__": True,
    "__format__": True,
    "__sizeof__": True,
    "__subclasshook__": True,
}
""" The map used to exclude invalid values from an object """

EXCLUSION_TYPES = {types.MethodType: True, types.FunctionType: True}
""" The map used to exclude invalid types from an object """

NUMBER_TYPES = {
    int: True,
    colony.legacy.LONG: True,
    float: True,
    colony.Decimal: True,
    decimal.Decimal: True,
}
""" The map used to check number types """

SEQUENCE_TYPES = {
    tuple: True,
    list: True,
    types.GeneratorType: True,
    itertools.chain: True,
}
""" The map used to check sequence types """

SEQUENCE_BASES = (tuple, list)
""" The base sequence types, used so that the sub-classes of them
are also handled as sequences (and not as generic instances) """

PARTIAL_TYPES = {tuple: True, list: True}
""" The map used to check the types for which a partial (lazy)
dumping operation may be performed, one item at a time """

FAST_VERSION = (3, 7)
""" The minimum interpreter version from which the embedded encoder
generates a result that is exactly equivalent to the "normal" one,
before it both the float representation and the map ordering differ """

NATIVE_TYPES = {
    type(None): True,
    bool: True,
    int: True,
    colony.legacy.LONG: True,
    float: True,
    str: True,
    colony.legacy.UNICODE: True,
    dict: True,
    list: True,
    tuple: True,
}
""" The map used to check the types that are serialized by the
embedded encoder without any kind of external resolution """

INDENTATION_VALUE = "    "
""" The indentation value """

character_replacements = {
    "\t": "\\t",
    "\b": "\\b",
    "\f": "\\f",
    "\n": "\\n",
    "\r": "\\r",
    "\\": "\\\\",
    "/": "\\/",
    '"': '\\"',
}

escape_char_to_char = {
    "t": "\t",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "\\": "\\",
    "/": "/",
    '"': '"',
}

string_escape_re = re.compile(r"[\x00-\x19\\\"/\b\f\n\r\t]")

coerced_key_re = re.compile(r'"(?:true|false|null)":')

digits_list = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")


def escape_character(match):
    """
    Escapes the character based in the given
    match object.

    :type match: MatchObject
    :param match: The math object to retrieve the character.
    :rtype: String
    :return: The escaped character.
    """

    # retrieves the first group from the match
    character = match.group(0)

    try:
        # retrieves the replacement from the char replacement
        replacement = character_replacements[character]

        # returns the replacement character
        return replacement
    except KeyError:
        # retrieves the ordinal (number)
        # of the character
        digit = ord(character)

        # in case the digit is less than thirty
        # two (special characters)
        if digit < 32:
            return "\\u%04x" % digit
        # otherwise
        else:
            # returns the character
            return character


def dumps(object):
    """
    Dumps (converts to JSON) the given object using the "normal"
    approach. The return value of this operation should always
    be a plain buffer/string and so special attention to memory
    usage should be considered a concern.

    :type object: Object
    :param object: The object to be dumped.
    :rtype: String
    :return: The dumped/serialized JSON string.
    """

    parts = dump_parts(object)
    return "".join([part for part in parts])


def dumps_f(object):
    """
    Dumps (converts to JSON) the given object using the "embedded"
    approach, meaning that the encoder provided by the language is
    used instead of the "local" one (faster operation).

    The result of this operation is meant to be exactly the same as
    the one of the "normal" approach, whenever such equivalence may
    not be guaranteed the "normal" approach is used instead.

    :type object: Object
    :param object: The object to be dumped.
    :rtype: String
    :return: The dumped/serialized JSON string.
    """

    # verifies that the current interpreter is recent enough for the
    # embedded encoder to generate an equivalent result, otherwise runs
    # the "normal" approach (the only one considered safe)
    if sys.version_info < FAST_VERSION:
        return dumps(object)

    try:
        import json
    except ImportError:
        return dumps(object)

    # runs the embedded dumping operation delegating the resolution of
    # the "unknown" types into the default (callback) function, note that
    # the non finite float values are not allowed so that the "normal"
    # approach is used for them (the representation is a different one)
    try:
        data = json.dumps(
            object,
            default=default_f,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (ValueError, TypeError, exceptions.JSONEncodeException):
        # falls back into the "normal" approach, as the embedded encoder
        # is either unable to encode the object or would encode it in a
        # different way, note that in case the object is really not
        # encodable the "normal" approach raises the proper exception
        return dumps(object)

    # verifies that no key has been coerced by the embedded encoder, as
    # the boolean and none values are converted by it into their JSON
    # counterparts instead of the string ones used by the "normal"
    # approach, note that a string key with such a value also triggers
    # the fallback (equivalent result, just a slower one)
    if coerced_key_re.search(data):
        return dumps(object)

    # escapes the forward slash character as expected by the "normal"
    # approach, note that in a valid JSON string this character may only
    # appear inside a string literal (making the replacement a safe one)
    return data.replace("/", "\\/")


def dumps_lazy_f(object):
    """
    Lazy version of the "embedded" dumps operation, the sequence based
    objects have their items dumped one at a time so that a partial
    result may be generated, for any other object a single (complete)
    part is yielded instead.

    :type object: Object
    :param object: The object to be dumped.
    :rtype: Generator
    :return: The resulting generator that may be used to lazy
    evaluated the various components of the JSON data.
    """

    # in case the object is not a "partial" sequence the complete dumped
    # value is yielded as a single part (no partial result possible)
    if not type(object) in PARTIAL_TYPES:
        yield dumps_f(object)
        return

    # yields the sequence initial value
    yield "["

    # sets the is first flag
    is_first = True

    # iterates over all the items in the object, dumping each one of
    # them separately, note that the concatenation of the various parts
    # is equivalent to the dumping of the complete sequence
    for item in object:
        # in case the is first flag is set
        if is_first:
            # unsets the is first flag
            is_first = False
        # otherwise
        else:
            # yields the comma value
            yield ","

        # yields the dumped item value
        yield dumps_f(item)

    # yields the sequence final value
    yield "]"


def default_f(object):
    """
    Resolves the provided object into a value that the embedded
    encoder is able to serialize, following the same type based
    strategy of the "normal" approach (see dump_parts).

    :type object: Object
    :param object: The object to be resolved into a natively
    serializable value.
    :rtype: Object
    :return: The natively serializable version of the object.
    """

    # in case the current object contains the JSON value
    # method the object to be serialized should be the
    # one retrieved by this method
    has_json_v = hasattr(object, "json_v")
    if has_json_v:
        object = object.json_v()

    # in case the object is none, note that the equality based
    # comparison is used so that the objects that consider
    # themselves none are also handled as such
    if object == None:
        return None

    # retrieves the object type, to be used in the
    # type based resolution of the object
    object_type = type(object)

    # in case the object is already serializable by the embedded
    # encoder it's returned as is (no resolution required)
    if object_type in NATIVE_TYPES:
        return object

    # in case the object is a function
    if object_type is types.FunctionType:
        return "function"

    # in case the object is a module
    if object_type is types.ModuleType:
        return "module"

    # in case the object is a method
    if object_type is types.MethodType:
        return "method"

    # in case the object is a sequence, note that only the single pass
    # ones are able to reach this point (the native ones are handled by
    # the embedded encoder) and so the fallback is always raised, as
    # consuming them would make the "normal" approach lose the contents
    if object_type in SEQUENCE_TYPES:
        raise exceptions.JSONEncodeException(object)

    # in case the object is a number, the float representation is
    # only used in case it's the exact same one that the "normal"
    # approach would have generated (otherwise fallback is raised)
    if object_type in NUMBER_TYPES:
        value = float(object)
        if colony.legacy.UNICODE(object) == repr(value):
            return value
        raise exceptions.JSONEncodeException(object)

    # in case the object is a date time
    if object_type == datetime.datetime:
        object_time_tuple = object.utctimetuple()
        return calendar.timegm(object_time_tuple)

    # in case the object is a date
    if object_type == datetime.date:
        object_time_tuple = object.timetuple()
        return calendar.timegm(object_time_tuple)

    # in case the object is an instance
    if hasattr(object, "__class__"):
        return dict(
            (name, getattr(object, name))
            for name in dir(object)
            if not name.startswith("_")
            and not name in EXCLUSION_MAP
            and not type(getattr(object, name)) in EXCLUSION_TYPES
        )

    # raises the JSON encode exception, as there's no
    # valid strategy to serialize the object
    raise exceptions.JSONEncodeException(object)


def dumps_lazy(object):
    """
    Lazy version of the dumps operation meaning that a lazy
    evaluation generator is returned so that proper evaluation
    of large serialization objects may be used.

    This method must be considered the primary way of archiving
    low memory usage for large data set serialization.

    :type object: Object
    :param object: The object to be dumped.
    :rtype: Generator
    :return: The resulting generator that may be used to lazy
    evaluated the various components of the JSON data.
    """

    return dump_parts(object)


def dumps_pretty(object):
    """
    Dumps (converts to JSON) the given object using the "normal"
    approach.
    This dumps method prints the JSON in "pretty" mode

    :type object: Object
    :param object: The object to be dumped.
    :rtype: String
    :return: The dumped JSON string (pretty).
    """

    return "".join([part for part in dump_parts_pretty(object)])


def dumps_buffer(object):
    """
    Dumps (converts to JSON) the given object using the "buffered"
    approach.

    :type object: Object
    :param object: The object to be dumped.
    :rtype: String
    :return: The dumped JSON string.
    """

    # creates the string buffer
    string_buffer = colony.StringBuffer()

    # dumps the object parts to the string buffer
    dump_parts_buffer(object, string_buffer)

    # retrieves the string value
    string_value = string_buffer.get_value()

    # returns the string value
    return string_value


def dump_parts(object, objects=None, cycles=False):
    """
    Dumps (converts to JSON) the given object parts using the "normal"
    approach, note that the construction of the final string must be
    performed using a generator based strategy.

    :type object: Object
    :param object: The object to have the parts dumped.
    :type objects: Dictionary
    :param objects: The set of object identifiers that have
    already been serialized (avoids circular references).
    :type cycles: bool
    :param cycles: Flag that controls if cycles should be detected
    and avoided (gracefully handled).
    :rtype: Generator
    :return: The generator from which a proper JSON string
    may be constructed using a lazy approach.
    """

    # in case the current object contains the JSON value
    # method the object to be serialized should be the
    # one retrieved by this method
    has_json_v = hasattr(object, "json_v")
    if has_json_v:
        object = object.json_v()

    # in case the objects reference is not initializes
    # starts a new map to hold the contents
    if objects == None:
        objects = {}

    # retrieves the object type and the
    # identifier of the object
    object_id = id(object)
    object_type = type(object)

    # in case the object identifier exists in
    # the list of objects serialized
    if object_id in objects:
        # yields the null value and returns
        # immediately to the calling method
        yield "null"
        return

    # sets the object identifier reference in the
    # map of "already" parsed elements
    if cycles:
        objects[object_id] = True

    # in case the object is none
    if object == None:
        # yields the null value
        yield "null"
    # in case the object is a function
    elif object_type is types.FunctionType:
        # yields the function value
        yield '"function"'
    # in case the object is a module
    elif object_type is types.ModuleType:
        # yields the module value
        yield '"module"'
    # in case the object is a method
    elif object_type is types.MethodType:
        # yields the method value
        yield '"method"'
    # in case the object is a boolean
    elif object_type is bool:
        # in case the object is valid (true)
        if object:
            # yields the true value
            yield "true"
        # otherwise
        else:
            # yields the false value
            yield "false"
    # in case the object is a dictionary
    elif isinstance(object, dict):
        # yields the dictionary initial value
        yield "{"

        # sets the is first flag
        is_first = True

        # iterates over all the object items
        for key, value in colony.legacy.items(object):
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # yields the comma separator
                yield ","

            # converts the key into the string representation
            # to conform with the current JSON specification
            key_s = str(key)

            # iterates over all the parts of the key
            for part in dump_parts(key_s, objects, cycles):
                # yields the part
                yield part

            # yields the separator
            yield ":"

            # iterates over all the parts of the value
            for part in dump_parts(value, objects, cycles):
                # yields the part
                yield part

        # yields the dictionary final value
        yield "}"
    # in case the object is a string
    elif isinstance(object, colony.legacy.STRINGS):
        # yields the string value
        yield '"' + string_escape_re.sub(escape_character, object) + '"'
    # in case the object is a sequence
    elif object_type in SEQUENCE_TYPES or isinstance(object, SEQUENCE_BASES):
        # yields the list initial value
        yield "["

        # sets the is first flag
        is_first = True

        # iterates over all the item in the object
        for item in object:
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise
            else:
                # yields the comma value
                yield ","

            # iterates over all the parts of the item
            for part in dump_parts(item, objects, cycles):
                # yields the part
                yield part

        # yields the list final value
        yield "]"
    # in case the object is a number
    elif object_type in NUMBER_TYPES:
        # yields the number unicode value
        yield colony.legacy.UNICODE(object)
    # in case the object is a date time
    elif object_type == datetime.datetime:
        # converts the object (date time) to a time tuple
        object_time_tuple = object.utctimetuple()

        # converts the object time tuple into a timestamp
        date_time_timestamp = calendar.timegm(object_time_tuple)

        # yields the timestamp unicode value
        yield colony.legacy.UNICODE(date_time_timestamp)
    # in case the object is a date
    elif object_type == datetime.date:
        # converts the object (date) to a time tuple
        object_time_tuple = object.timetuple()

        # converts the object time tuple into a timestamp
        date_timestamp = calendar.timegm(object_time_tuple)

        # yields the timestamp unicode value
        yield colony.legacy.UNICODE(date_timestamp)
    # in case the object is an instance
    elif hasattr(object, "__class__"):
        # yields the dictionary initial value
        yield "{"

        # sets the is first value
        is_first = True

        # retrieves the object items from the object, taking into
        # account the exclusion map and the value type
        object_items = [
            value
            for value in dir(object)
            if not value.startswith("_")
            and not value in EXCLUSION_MAP
            and not type(getattr(object, value)) in EXCLUSION_TYPES
        ]

        # iterates over all the object items
        for object_item in object_items:
            # retrieves the object value from the object
            object_value = getattr(object, object_item)

            # in case the is first value is set
            if is_first:
                # unsets the is first value
                is_first = False
            else:
                # yields the comma value
                yield ","

            # yields the object item
            yield '"' + object_item + '"' + ":"

            # iterates over the object value parts
            for part in dump_parts(object_value, objects, cycles):
                # yields the part
                yield part

        # yields the dictionary final value
        yield "}"
    # in case a different type is set
    else:
        # raises the JSON encode exception
        raise exceptions.JSONEncodeException(object)

    # removes the current object identifier from
    # the map of object already serialized
    if cycles:
        del objects[object_id]


def dump_parts_pretty(object, objects=None, indentation=0, cycles=False):
    """
    Dumps (converts to JSON) the given object parts using the "normal"
    approach.

    :type object: Object
    :param object: The object to have the parts dumped.
    :type objects: Dictionary
    :param objects: The set of object identifiers that have
    already been serialized (avoids circular references).
    :type indentation: int
    :param indentation: The current indentation value.
    :type cycles: bool
    :param cycles: Flag that controls if cycles should be detected
    and avoided (gracefully handled).
    :rtype: String
    :return: The dumped JSON string.
    """

    # in case the current object contains the JSON value
    # method the object to be serialized should be the
    # one retrieved by this method
    has_json_v = hasattr(object, "json_v")
    if has_json_v:
        object = object.json_v()

    # in case the objects reference is not initializes
    # starts a new map to hold the contents
    if objects == None:
        objects = {}

    # retrieves the object type and the
    # identifier of the object
    object_id = id(object)
    object_type = type(object)

    # in case the object identifier exists in
    # the list of objects serialized
    if object_id in objects:
        # yields the null value and returns
        # immediately to the calling method
        yield "null"
        return

    # sets the object identifier reference in the
    # map of "already" parsed elements
    if cycles:
        objects[object_id] = True

    # in case the object is none
    if object == None:
        # yields the null value
        yield "null"
    # in case the object is a function
    elif object_type is types.FunctionType:
        # yields the function value
        yield '"function"'
    # in case the object is a module
    elif object_type is types.ModuleType:
        # yields the module value
        yield '"module"'
    # in case the object is a method
    elif object_type is types.MethodType:
        # yields the method value
        yield '"method"'
    # in case the object is a boolean
    elif object_type is bool:
        # in case the object is valid (true)
        if object:
            # yields the true value
            yield "true"
        # otherwise
        else:
            # yields the false value
            yield "false"
    # in case the object is a dictionary
    elif isinstance(object, dict):
        # yields the dictionary initial value
        yield "{"

        # sets the is first flag
        is_first = True

        # iterates over all the object items
        for key, value in colony.legacy.items(object):
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # yields the comma separator
                yield ","

            # yields the newline value
            yield "\n"

            # iterates over the indentation range (plus one)
            for _index in colony.legacy.xrange(indentation + 1):
                # yields the indentation value
                yield INDENTATION_VALUE

            # converts the key into the string representation
            # to conform with the current JSON specification
            key_s = str(key)

            # iterates over all the parts of the key
            for part in dump_parts_pretty(key_s, objects, indentation, cycles):
                # yields the part
                yield part

            # yields the separator
            yield " : "

            # iterates over all the parts of the value
            for part in dump_parts_pretty(value, objects, indentation + 1, cycles):
                # yields the part
                yield part

        # yields the newline value
        yield "\n"

        # iterates over the indentation range
        for _index in colony.legacy.xrange(indentation):
            # yields the indentation value
            yield INDENTATION_VALUE

        # yields the dictionary final value
        yield "}"
    # in case the object is a string
    elif isinstance(object, colony.legacy.STRINGS):
        # yields the string value
        yield '"' + string_escape_re.sub(escape_character, object) + '"'
    # in case the object is a sequence
    elif object_type in SEQUENCE_TYPES or isinstance(object, SEQUENCE_BASES):
        # yields the list initial value
        yield "["

        # sets the is first flag
        is_first = True

        # iterates over all the item in the object
        for item in object:
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise
            else:
                # yields the comma value
                yield ", "

            # iterates over all the parts of the item
            for part in dump_parts_pretty(item, object, indentation, cycles):
                # yields the part
                yield part

        # yields the list final value
        yield "]"
    # in case the object is a number
    elif object_type in NUMBER_TYPES:
        # yields the number unicode value
        yield colony.legacy.UNICODE(object)
    # in case the object is a date time
    elif object_type == datetime.datetime:
        # converts the object (date time) to a time tuple
        object_time_tuple = object.utctimetuple()

        # converts the object time tuple into a timestamp
        date_time_timestamp = calendar.timegm(object_time_tuple)

        # yields the timestamp unicode value
        yield colony.legacy.UNICODE(date_time_timestamp)
    # in case the object is a date
    elif object_type == datetime.date:
        # converts the object (date) to a time tuple
        object_time_tuple = object.timetuple()

        # converts the object time tuple into a timestamp
        date_timestamp = calendar.timegm(object_time_tuple)

        # yields the timestamp unicode value
        yield colony.legacy.UNICODE(date_timestamp)
    # in case the object is an instance
    elif hasattr(object, "__class__"):
        # yields the dictionary initial value
        yield "{"

        # sets the is first value
        is_first = True

        # retrieves the object items from the object, taking into
        # account the exclusion map and the value type
        object_items = [
            value
            for value in dir(object)
            if not value.startswith("_")
            and not value in EXCLUSION_MAP
            and not type(getattr(object, value)) in EXCLUSION_TYPES
        ]

        # iterates over all the object items
        for object_item in object_items:
            # retrieves the object value from the object
            object_value = getattr(object, object_item)

            # in case the is first value is set
            if is_first:
                # unsets the is first value
                is_first = False
            else:
                # yields the comma value
                yield ","

            # yields the newline value
            yield "\n"

            # iterates over the indentation range (plus one)
            for _index in colony.legacy.xrange(indentation + 1):
                # yields the indentation value
                yield INDENTATION_VALUE

            # yields the object item
            yield '"' + object_item + '"' + " : "

            # iterates over the object value parts
            for part in dump_parts_pretty(
                object_value, objects, indentation + 1, cycles
            ):
                # yields the part
                yield part

        # yields the newline value
        yield "\n"

        # iterates over the indentation range
        for _index in colony.legacy.xrange(indentation):
            # yields the indentation value
            yield INDENTATION_VALUE

        # yields the dictionary final value
        yield "}"
    # in case a different type is set
    else:
        # raises the JSON encode exception
        raise exceptions.JSONEncodeException(object)

    # removes the current object identifier from
    # the map of object already serialized
    if cycles:
        del objects[object_id]


def dump_parts_buffer(object, string_buffer, objects=None, cycles=False):
    """
    Dumps (converts to JSON) the given object parts using the "buffered"
    approach.

    :type object: Object
    :param object: The object to have the parts dumped.
    :type string_buffer: StringBuffer
    :param string_buffer: The string buffer that is going to be
    used to store the partial dump results.
    :type objects: Dictionary
    :param objects: The set of object identifiers that have
    already been serialized (avoids circular references).
    :type cycles: bool
    :param cycles: Flag that controls if cycles should be detected
    and avoided (gracefully handled).
    :rtype: String
    :return: The dumped JSON string.
    """

    # in case the current object contains the JSON value
    # method the object to be serialized should be the
    # one retrieved by this method
    has_json_v = hasattr(object, "json_v")
    if has_json_v:
        object = object.json_v()

    # in case the objects reference is not initializes
    # starts a new map to hold the contents
    if objects == None:
        objects = {}

    # retrieves the object type and the
    # identifier of the object
    object_id = id(object)
    object_type = type(object)

    # in case the object identifier exists in
    # the list of objects serialized
    if object_id in objects:
        # writes the null value and returns
        # immediately to the calling method
        string_buffer.write("null")
        return

    # sets the object identifier reference in the
    # map of "already" parsed elements
    if cycles:
        objects[object_id] = True

    # in case the object is none
    if object == None:
        # writes the null value
        string_buffer.write("null")
    # in case the object is a function
    elif object_type is types.FunctionType:
        # writes the function value
        string_buffer.write('"function"')
    # in case the object is a module
    elif object_type is types.ModuleType:
        # writes the module value
        string_buffer.write('"module"')
    # in case the object is a method
    elif object_type is types.MethodType:
        # writes the method value
        string_buffer.write('"method"')
    # in case the object is a boolean
    elif object_type is bool:
        # in case the object is valid (true)
        if object:
            # writes the true value
            string_buffer.write("true")
        # otherwise
        else:
            # writes the false value
            string_buffer.write("false")
    # in case the object is a dictionary
    elif isinstance(object, dict):
        # writes the dictionary initial value
        string_buffer.write("{")

        # sets the is first flag
        is_first = True

        # iterates over the object items, retrieving the
        # key and the value
        for key, value in colony.legacy.items(object):
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # writes the comma separator
                string_buffer.write(",")

            # converts the key into the string representation
            # to conform with the current JSON specification
            key_s = str(key)

            # dumps the key parts
            dump_parts_buffer(key_s, string_buffer, objects, cycles)

            # writes the separator
            string_buffer.write(":")

            # dumps the value parts
            dump_parts_buffer(value, string_buffer, objects, cycles)

        # writes the dictionary final value
        string_buffer.write("}")
    # in case the object is a string
    elif isinstance(object, colony.legacy.STRINGS):
        # writes the escaped string value
        string_buffer.write('"' + string_escape_re.sub(escape_character, object) + '"')
    # in case the object is a sequence
    elif object_type in SEQUENCE_TYPES or isinstance(object, SEQUENCE_BASES):
        # writes the list initial value
        string_buffer.write("[")

        # sets the is first flag
        is_first = True

        # iterates over all the items in the object
        for item in object:
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # writes the comma separator
                string_buffer.write(",")

            # dumps the item parts
            dump_parts_buffer(item, string_buffer, objects, cycles)

        # writes the list final value
        string_buffer.write("]")
    # in case the object is a number
    elif object_type in NUMBER_TYPES:
        # writes the number string value
        string_buffer.write(str(object))
    # in case the object is a date time
    elif object_type == datetime.datetime:
        # converts the object (date time) to a time tuple
        object_time_tuple = object.utctimetuple()

        # converts the object time tuple into a timestamp
        date_time_timestamp = calendar.timegm(object_time_tuple)

        # writes the timestamp string value
        string_buffer.write(str(date_time_timestamp))
    # in case the object is a date
    elif object_type == datetime.date:
        # converts the object (date) to a time tuple
        object_time_tuple = object.timetuple()

        # converts the object time tuple into a timestamp
        date_timestamp = calendar.timegm(object_time_tuple)

        # writes the timestamp string value
        string_buffer.write(str(date_timestamp))
    # in case the object is an instance
    elif hasattr(object, "__class__"):
        # writes the dictionary initial value
        string_buffer.write("{")

        # sets the is first flag
        is_first = True

        # retrieves the object items from the object, taking into
        # account the exclusion map and the value type
        object_items = [
            value
            for value in dir(object)
            if not value.startswith("_")
            and not value in EXCLUSION_MAP
            and not type(getattr(object, value)) in EXCLUSION_TYPES
        ]

        # iterates over all the object items
        for object_item in object_items:
            # retrieves the object value from the object
            object_value = getattr(object, object_item)

            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise
            else:
                # writes the comma separator
                string_buffer.write(",")

            # writes the object item
            string_buffer.write('"' + object_item + '"' + ":")

            # dumps the object value parts
            dump_parts_buffer(object_value, string_buffer, objects, cycles)

        # writes the dictionary final value
        string_buffer.write("}")
    # in case a different type is set
    else:
        # raises a JSON encode exception
        raise exceptions.JSONEncodeException(object)

    # removes the current object identifier from
    # the map of object already serialized
    if cycles:
        del objects[object_id]


def loads(data):
    # initializes the stack
    stack = []

    # creates the map for structure validation
    valid_map = {}

    # retrieves the characters from the data
    characters = iter(data)

    # starts the value
    value = None

    # unsets the current character is next flag
    current_character_is_next = False

    try:
        # iterates continuously
        while True:
            # unsets the skip flag
            skip = False

            # in case the current character is not
            # the next one
            if not current_character_is_next:
                # retrieves the next character
                character = next(characters)

            # iterates while the character is a space character
            while character in (" ", "\t", "\r", "\n"):
                # retrieves the next character
                character = next(characters)

            # unsets the current character is next flag
            current_character_is_next = False

            # in case it's the beginning of a string
            if character == '"':
                value = ""
                try:
                    # retrieves the next character
                    character = next(characters)

                    # iterates while the string is not finished
                    while not character == '"':
                        if character == "\\":
                            # retrieves the next character
                            character = next(characters)

                            try:
                                value += escape_char_to_char[character]
                            except KeyError:
                                if character == "u":
                                    hex_code = (
                                        next(characters)
                                        + next(characters)
                                        + next(characters)
                                        + next(characters)
                                    )
                                    value += colony.legacy.unichr(int(hex_code, 16))
                                else:
                                    # raises the JSON decode exception
                                    raise exceptions.JSONDecodeException(
                                        "Bad Escape Sequence Found"
                                    )
                        else:
                            value += character

                        # retrieves the next character
                        character = next(characters)
                except StopIteration:
                    # raises the JSON decode exception
                    raise exceptions.JSONDecodeException("Expected end of String")
            elif character == "{":
                # creates a new map
                _map = {}

                # retrieves the map id
                _map_id = id(_map)

                # sets the map to the
                # initial valid state
                valid_map[_map_id] = True

                # adds the map to the stack
                stack.append(_map)

                # sets the skip flag
                skip = True
            elif character == "}":
                # pops the value from the stack
                value = stack.pop()
            elif character == "[":
                # creates a new list
                _list = []

                # retrieves the list id
                _list_id = id(_list)

                # sets the list to the
                # initial valid state
                valid_map[_list_id] = True

                # adds the list to the stack
                stack.append(_list)

                # sets the skip flag
                skip = True
            elif character == "]":
                value = stack.pop()
            elif character in (",", ":"):
                # retrieves the stack top
                top = stack[-1]

                # retrieves the top id
                top_id = id(top)

                # sets the top as valid
                valid_map[top_id] = True

                # sets the skip flag
                skip = True
            elif character in digits_list or character == "-":
                digits = [character]

                character = next(characters)
                num_conv = int
                try:
                    while character in digits_list:
                        digits.append(character)
                        character = next(characters)
                    if character == ".":
                        num_conv = float
                        digits.append(character)
                        character = next(characters)
                        while character in digits_list:
                            digits.append(character)
                            character = next(characters)
                        if character.upper() == "E":
                            digits.append(character)
                            character = next(characters)
                            if character in ["+", "-"]:
                                digits.append(character)
                                character = next(characters)
                                while character in digits_list:
                                    digits.append(character)
                                    character = next(characters)
                            else:
                                raise exceptions.JSONDecodeException("Expected + or -")
                except StopIteration:
                    pass

                value = num_conv("".join(digits))

                # sets the current character is next value
                current_character_is_next = True

            elif character in ("t", "f", "n"):
                kw = character + next(characters) + next(characters) + next(characters)
                if kw == "null":
                    value = None
                elif kw == "true":
                    value = True
                elif kw == "fals" and next(characters) == "e":
                    value = False
                else:
                    # raises the JSON decode exception
                    raise exceptions.JSONDecodeException("Expected Null, False or True")
            else:
                # raises the JSON decode exception
                raise exceptions.JSONDecodeException(
                    'Expected []{}," or Number, Null, False or True'
                )

            if not skip:
                if len(stack):
                    # retrieves the top of the stack
                    top = stack[-1]

                    if type(top) is list:
                        # retrieves the top id
                        top_id = id(top)

                        # in case the top id is not present
                        # in the valid map
                        if not top_id in valid_map:
                            # raises the JSON decode exception
                            raise exceptions.JSONDecodeException(
                                "Expected list structure"
                            )

                        # in case the top is valid
                        if valid_map[top_id]:
                            # appends the value to the top (list)
                            top.append(value)

                            # sets the top as invalid
                            valid_map[top_id] = False
                        else:
                            # raises the JSON decode exception
                            raise exceptions.JSONDecodeException(
                                "Expected list separator ','"
                            )
                    elif type(top) is dict:
                        # appends the value to the stack
                        stack.append(value)
                    elif type(top) in colony.legacy.STRINGS:
                        # retrieves the top id
                        top_id = id(top)

                        # in case the top id is not present
                        # in the valid map
                        if not top_id in valid_map:
                            # raises the JSON decode exception
                            raise exceptions.JSONDecodeException(
                                "Expected dictionary structure"
                            )

                        # in case the top is valid
                        if valid_map[top_id]:
                            # retrieves the top of the stack as
                            # the key
                            key = stack.pop()

                            # retrieves the top of the stack
                            top = stack[-1]

                            # retrieves the top id
                            top_id = id(top)

                            # sets the value in the stack
                            # top value
                            top[key] = value

                            # sets the top as invalid
                            valid_map[top_id] = False
                        else:
                            # raises the JSON decode exception
                            raise exceptions.JSONDecodeException(
                                "Expected dictionary separator ':'"
                            )
                    # otherwise
                    else:
                        # raises the JSON decode exception
                        raise exceptions.JSONDecodeException(
                            "Expected dictionary key, or start of a value"
                        )
                # otherwise
                else:
                    # returns the value
                    return value
    except StopIteration:
        # raises the JSON decode exception
        raise exceptions.JSONDecodeException("Unexpected end of JSON source")


def loads_f(data):
    try:
        import json
    except ImportError:
        return loads(data)
    return json.loads(data)
