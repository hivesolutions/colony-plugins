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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

__credits__ = "Jan-Klaas Kollhof <keyjaque@yahoo.com>"
""" The credits for the module """

import re
import types
import datetime
import calendar

import colony.libs.string_buffer_util

import json_exceptions

EXCLUSION_MAP = {"__class__" : True, "__delattr__" : True, "__dict__" : True, "__doc__" : True, "__getattribute__" : True, "__hash__" : True,
                 "__init__" : True, "__module__" : True, "__new__" : True, "__reduce__" : True, "__reduce_ex__" : True, "__repr__" : True,
                 "__setattr__" : True, "__str__" : True, "__weakref__" : True, "__format__" : True, "__sizeof__" : True, "__subclasshook__" : True}
""" The map used to exclude invalid values from an object """

EXCLUSION_TYPES = {types.MethodType : True, types.FunctionType : True}
""" The map used to exclude invalid types from an object """

NUMBER_TYPES = {types.IntType : True, types.LongType: True, types.FloatType : True}
""" The map used to check number types """

SEQUENCE_TYPES = {types.TupleType : True, types.ListType : True, types.GeneratorType : True}
""" The map used to check sequence types """

char_replacements = {
        "\t" : "\\t",
        "\b" : "\\b",
        "\f" : "\\f",
        "\n" : "\\n",
        "\r" : "\\r",
        "\\" : "\\\\",
        "/" : "\\/",
        "\"" : "\\\""}

escape_char_to_char = {
        "t": "\t",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "\\": "\\",
        "/": "/",
        "\"" : "\""}

string_escape_re = re.compile(r"[\x00-\x19\\\"/\b\f\n\r\t]")
digits_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def escape_char(match):
    character = match.group(0)
    try:
        replacement = char_replacements[character]
        return replacement
    except KeyError:
        d = ord(character)
        if d < 32:
            return "\\u%04x" % d
        else:
            return character

def dumps_buffer(object):
    # creates the string buffer
    string_buffer = colony.libs.string_buffer_util.StringBuffer()

    # dumps the object parts to the string buffer
    dump_parts_buffer(object, string_buffer)

    # retrieves the string value
    string_value = string_buffer.get_value()

    # returns the string value
    return string_value

def dumps(object):
    return "".join([part for part in dump_parts(object)])

def dump_parts_buffer(object, string_buffer):
    # retrieves the object type
    object_type = type(object)

    # in case the object is none
    if object == None:
        # writes the null value
        string_buffer.write("null")
    # in case the object is a function
    elif object_type is types.FunctionType:
        # writes the function value
        string_buffer.write("\"function\"")
    # in case the object is module
    elif object_type is types.ModuleType:
        # writes the module value
        string_buffer.write("\"module\"")
    # in case the object is a method
    elif object_type is types.MethodType:
        # writes the method value
        string_buffer.write("\"method\"")
    # in case the object is a boolean
    elif object_type is types.BooleanType:
        # in case the object is valid (true)
        if object:
            # writes the true value
            string_buffer.write("true")
        # otherwise
        else:
            # writes the false value
            string_buffer.write("false")
    # in case the object is a dictionary
    elif object_type is types.DictionaryType:
        # writes the dictionary initial value
        string_buffer.write("{")

        # sets the is first flag
        is_first = True

        # iterates over the object items, retrieving the
        # key and the value
        for key, value in object.items():
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # writes the comma separator
                string_buffer.write(",")

            # dumps the key parts
            dump_parts_buffer(key, string_buffer)

            # writes the separator
            string_buffer.write(":")

            # dumps the value parts
            dump_parts_buffer(value, string_buffer)

        # writes the dictionary final value
        string_buffer.write("}")
    # in case the object is a string
    elif object_type in types.StringTypes:
        # writes the escaped string value
        string_buffer.write("\"" + string_escape_re.sub(escape_char, object) + "\"")
    # in case the object is a sequence
    elif object_type in SEQUENCE_TYPES:
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
            dump_parts_buffer(item, string_buffer)

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
    # in case the object is an instance
    elif object_type is types.InstanceType or hasattr(object, "__class__"):
        # writes the dictionary initial value
        string_buffer.write("{")

        # sets the is first flag
        is_first = True

        # retrieves the object items from the object, taking into
        # account the exclusion map and the value type
        object_items = [value for value in dir(object) if not value.startswith("_") and not value in EXCLUSION_MAP and not type(getattr(object, value)) in EXCLUSION_TYPES]

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
            string_buffer.write("\"" + object_item + "\"" + ":")

            # dumps the object value parts
            dump_parts_buffer(object_value, string_buffer)

        # writes the dictionary final value
        string_buffer.write("}")
    # in case a different type is set
    else:
        # raises a json encode exception
        raise json_exceptions.JsonEncodeException(object)

def dump_parts(object, indentation = 0):
    object_type = type(object)

    if object == None:
        yield "null"
    elif object_type is types.FunctionType:
        yield "\"function\""
    elif object_type is types.ModuleType:
        yield "\"module\""
    elif object_type is types.MethodType:
        yield "\"method\""
    elif object_type is types.BooleanType:
        if object:
            yield "true"
        else:
            yield "false"
    elif object_type is types.DictionaryType:
        yield "{"
        is_first = True
        for key, value in object.items():
            if is_first:
                is_first = False
            else:
                yield ","

            yield "\n"
            for _index in range(indentation + 1):
                yield "    "

            for part in dump_parts(key):
                yield part + " : "

            for part in dump_parts(value, indentation + 1):
                yield part
        yield "\n"
        for _index in range(indentation):
            yield "    "
        yield "}"
    elif object_type in types.StringTypes:
        yield "\"" + string_escape_re.sub(escape_char, object) + "\""
    elif object_type in SEQUENCE_TYPES:
        yield "["
        is_first = True
        for item in object:
            if is_first:
                is_first = False
            else:
                yield ", "
            for part in dump_parts(item, indentation):
                yield part
        yield "]"
    elif object_type in NUMBER_TYPES:
        yield unicode(object)
    elif object_type == datetime.datetime:
        object_time_tuple = object.utctimetuple()
        date_time_timestamp = calendar.timegm(object_time_tuple)
        yield unicode(date_time_timestamp)
    elif object_type is types.InstanceType or hasattr(object, "__class__"):
        yield "{"
        is_first = True
        object_items = [value for value in dir(object) if not value.startswith("_") and not value in EXCLUSION_MAP and not type(getattr(object, value)) in EXCLUSION_TYPES]
        for object_item in object_items:
            object_value = getattr(object, object_item)
            if is_first:
                is_first = False
                yield "\"" + object_item + "\"" + ":"
            else:
                yield ",\"" + object_item + "\"" + ":"
            for part in dump_parts(object_value):
                yield part
        yield "}"
    else:
        raise json_exceptions.JsonEncodeException(object)

def loads(string):
    stack = []
    chars = iter(string)
    value = None
    curr_char_is_next = False

    try:
        while(1):
            skip = False
            if not curr_char_is_next:
                character = chars.next()
            while(character in [" ", "\t", "\r", "\n"]):
                character = chars.next()
            curr_char_is_next = False

            # in case it's the beginning of a string
            if character == "\"":
                value = ""
                try:
                    character = chars.next()

                    # iterates while the string is not finished
                    while character != "\"":
                        if character == "\\":
                            character = chars.next()
                            try:
                                value += escape_char_to_char[character]
                            except KeyError:
                                if character == "u":
                                    hex_code = chars.next() + chars.next() + chars.next() + chars.next()
                                    value += unichr(int(hex_code, 16))
                                else:
                                    raise json_exceptions.JsonDecodeException("Bad Escape Sequence Found")
                        else:
                            value += character
                        character = chars.next()
                except StopIteration:
                    raise json_exceptions.JsonDecodeException("Expected end of String")
            elif character == "{":
                stack.append({})
                skip = True
            elif character == "}":
                value = stack.pop()
            elif character == "[":
                stack.append([])
                skip = True
            elif character == "]":
                value = stack.pop()
            elif character in [",", ":"]:
                skip = True
            elif character in digits_list or character == "-":
                digits = [character]
                character = chars.next()
                num_conv = int
                try:
                    while character in digits_list:
                        digits.append(character)
                        character = chars.next()
                    if character == ".":
                        num_conv = float
                        digits.append(character)
                        character = chars.next()
                        while character in digits_list:
                            digits.append(character)
                            character = chars.next()
                        if character.upper() == "E":
                            digits.append(character)
                            character = chars.next()
                            if character in ["+", "-"]:
                                digits.append(character)
                                character = chars.next()
                                while character in digits_list:
                                    digits.append(character)
                                    character = chars.next()
                            else:
                                raise json_exceptions.JsonDecodeException("Expected + or -")
                except StopIteration:
                    pass
                value = num_conv("".join(digits))
                curr_char_is_next = True

            elif character in ["t", "f", "n"]:
                kw = character + chars.next() + chars.next() + chars.next()
                if kw == "null":
                    value = None
                elif kw == "true":
                    value = True
                elif kw == "fals" and chars.next() == "e":
                    value = False
                else:
                    raise json_exceptions.JsonDecodeException("Expected Null, False or True")
            else:
                raise json_exceptions.JsonDecodeException("Expected []{},\" or Number, Null, False or True")

            if not skip:
                if len(stack):
                    top = stack[-1]
                    if type(top) is types.ListType:
                        top.append(value)
                    elif type(top) is types.DictionaryType:
                        stack.append(value)
                    elif type(top) in types.StringTypes:
                        key = stack.pop()
                        stack[-1][key] = value
                    else:
                        raise json_exceptions.JsonDecodeException("Expected dictionary key, or start of a value")
                else:
                    return value
    except StopIteration:
        raise json_exceptions.JsonDecodeException("Unexpected end of Json source")
