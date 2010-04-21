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

EXCLUSION_TYPES = {types.MethodType : True, types.FunctionType : True}

NUMBER_TYPES = {types.IntType : True, types.LongType: True, types.FloatType : True}

SEQUENCE_TYPES = {types.TupleType : True, types.ListType : True, types.GeneratorType : True}

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
    object_type = type(object)
    if object == None:
        string_buffer.write("null")
    elif object_type is types.FunctionType:
        string_buffer.write("\"function\"")
    elif object_type is types.ModuleType:
        string_buffer.write("\"module\"")
    elif object_type is types.MethodType:
        string_buffer.write("\"method\"")
    elif object_type is types.BooleanType:
        if object:
            string_buffer.write("true")
        else:
            string_buffer.write("false")
    elif object_type is types.DictionaryType:
        string_buffer.write("{")
        is_first = True
        for key, value in object.items():
            if is_first:
                is_first = False
            else:
                string_buffer.write(",")
            dump_parts_buffer(key, string_buffer)
            string_buffer.write(":")
            dump_parts_buffer(value, string_buffer)
        string_buffer.write("}")
    elif object_type in types.StringTypes:
        string_buffer.write("\"" + string_escape_re.sub(escape_char, object) + "\"")
    elif object_type in SEQUENCE_TYPES:
        string_buffer.write("[")
        is_first = True
        for item in object:
            if is_first:
                is_first = False
            else:
                string_buffer.write(",")
            dump_parts_buffer(item, string_buffer)
        string_buffer.write("]")
    elif object_type in NUMBER_TYPES:
        string_buffer.write(str(object))
    elif object_type == datetime.datetime:
        obj_time_tuple = object.utctimetuple()
        date_time_timestamp = calendar.timegm(obj_time_tuple)
        string_buffer.write(str(date_time_timestamp))
    elif object_type is types.InstanceType or hasattr(object, "__class__"):
        string_buffer.write("{")
        is_first = True
        obj_items = [value for value in dir(object) if not value.startswith("_") and not value in EXCLUSION_MAP and not type(getattr(object, value)) in EXCLUSION_TYPES]
        for obj_item in obj_items:
            obj_value = getattr(object, obj_item)
            if is_first:
                is_first = False
                string_buffer.write("\"" + obj_item + "\"" + ":")
            else:
                string_buffer.write(",\"" + obj_item + "\"" + ":")
            dump_parts_buffer(obj_value, string_buffer)
        string_buffer.write("}")
    else:
        raise json_exceptions.JsonEncodeException(object)

def dump_parts(object):
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
                for part in dump_parts(key):
                    yield part + ":"
            else:
                for part in dump_parts(key):
                    yield "," + part + ":"
            for part in dump_parts(value):
                yield part
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
                yield ","
            for part in dump_parts(item):
                yield part
        yield "]"
    elif object_type in NUMBER_TYPES:
        yield unicode(object)
    elif object_type == datetime.datetime:
        obj_time_tuple = object.utctimetuple()
        date_time_timestamp = calendar.timegm(obj_time_tuple)
        yield unicode(date_time_timestamp)
    elif object_type is types.InstanceType or hasattr(object, "__class__"):
        yield "{"
        is_first = True
        obj_items = [value for value in dir(object) if not value.startswith("_") and not value in EXCLUSION_MAP and not type(getattr(object, value)) in EXCLUSION_TYPES]
        for obj_item in obj_items:
            obj_value = getattr(object, obj_item)
            if is_first:
                is_first = False
                yield "\"" + obj_item + "\"" + ":"
            else:
                yield ",\"" + obj_item + "\"" + ":"
            for part in dump_parts(obj_value):
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
