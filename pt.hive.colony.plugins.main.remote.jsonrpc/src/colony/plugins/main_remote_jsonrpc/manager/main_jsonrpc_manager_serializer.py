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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

__credits__ = "Jan-Klaas Kollhof <keyjaque@yahoo.com>"
""" The credits for the module """

import re
import types

import main_jsonrpc_manager_exceptions

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
    c = match.group(0)
    try:
        replacement = char_replacements[c]
        return replacement
    except KeyError:
        d = ord(c)
        if d < 32:
            return "\\u%04x" % d
        else:
            return c

def dumps(obj):
    return unicode("".join([part for part in dump_parts(obj)]))

def dump_parts(obj):
    obj_type = type(obj)
    if obj == None:
        yield u"null"
    elif obj_type is types.FunctionType:
        yield u"\"function\""
    elif obj_type is types.ModuleType:
        yield u"\"module\""
    elif obj_type is types.MethodType:
        yield u"\"method\""
    elif obj_type is types.InstanceType:
        yield u"{"
        is_first = True
        obj_items = dir(obj)
        for obj_item in obj_items:
            if is_first:
                is_first = False
            else:
                yield u","
            obj_value = getattr(obj, obj_item)
            yield "\"" + obj_item + "\"" + ":"
            for part in dump_parts(obj_value):
                yield part
        yield u"}"
    elif obj_type is types.BooleanType:
        if obj:
            yield u"true"
        else:
            yield u"false"
    elif obj_type is types.DictionaryType:
        yield u"{"
        is_first = True
        for (key, value) in obj.items():
            if is_first:
                is_first = False
            else:
                yield u","
            yield u"\"" + string_escape_re.sub(escape_char, key) + u"\":"
            for part in dump_parts(value):
                yield part
        yield u"}"
    elif obj_type in types.StringTypes:
        yield u"\"" + string_escape_re.sub(escape_char, obj) + u"\""
    elif obj_type in [types.TupleType, types.ListType, types.GeneratorType]:
        yield u"["
        is_first = True
        for item in obj:
            if is_first:
                is_first = False
            else:
                yield u","
            for part in dump_parts(item):
                yield part
        yield u"]"
    elif obj_type in [types.IntType, types.LongType, types.FloatType]:
        yield unicode(obj)
    else:
        raise main_jsonrpc_manager_exceptions.JsonEncodeException(obj)

def loads(s):
    stack = []
    chars = iter(s)
    value = None
    curr_char_is_next = False

    try:
        while(1):
            skip = False
            if not curr_char_is_next:
                c = chars.next()
            while(c in [" ", "\t", "\r", "\n"]):
                c = chars.next()
            curr_char_is_next = False
            if c == "\"":
                value = ""
                try:
                    c = chars.next()
                    while c != "\"":
                        if c == "\\":
                            c = chars.next()
                            try:
                                value += escape_char_to_char[c]
                            except KeyError:
                                if c == "u":
                                    hex_code = chars.next() + chars.next() + chars.next() + chars.next()
                                    value += unichr(int(hex_code, 16))
                                else:
                                    raise main_jsonrpc_manager_exceptions.JsonDecodeException("Bad Escape Sequence Found")
                        else:
                            value += c
                        c = chars.next()
                except StopIteration:
                    raise main_jsonrpc_manager_exceptions.JsonDecodeException("Expected end of String")
            elif c == "{":
                stack.append({})
                skip = True
            elif c == "}":
                value = stack.pop()
            elif c == "[":
                stack.append([])
                skip = True
            elif c == "]":
                value = stack.pop()
            elif c in [",", ":"]:
                skip = True
            elif c in digits_list or c == "-":
                digits = [c]
                c = chars.next()
                num_conv = int
                try:
                    while c in digits_list:
                        digits.append(c)
                        c = chars.next()
                    if c == ".":
                        num_conv = float
                        digits.append(c)
                        c = chars.next()
                        while c in digits_list:
                            digits.append(c)
                            c = chars.next()
                        if c.upper() == "E":
                            digits.append(c)
                            c = chars.next()
                            if c in ["+", "-"]:
                                digits.append(c)
                                c = chars.next()
                                while c in digits_list:
                                    digits.append(c)
                                    c = chars.next()
                            else:
                                raise main_jsonrpc_manager_exceptions.JsonDecodeException("Expected + or -")
                except StopIteration:
                    pass
                value = num_conv("".join(digits))
                curr_char_is_next = True

            elif c in ["t", "f", "n"]:
                kw = c + chars.next() + chars.next() + chars.next()
                if kw == "null":
                    value = None
                elif kw == "true":
                    value = True
                elif kw == "fals" and chars.next() == "e":
                    value = False
                else:
                    raise main_jsonrpc_manager_exceptions.JsonDecodeException("Expected Null, False or True")
            else:
                raise main_jsonrpc_manager_exceptions.JsonDecodeException("Expected []{},\" or Number, Null, False or True")

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
                        raise main_jsonrpc_manager_exceptions.JsonDecodeException("Expected dictionary key, or start of a value")
                else:
                    return value
    except StopIteration:
         raise main_jsonrpc_manager_exceptions.JsonDecodeException("Unexpected end of Json source")
