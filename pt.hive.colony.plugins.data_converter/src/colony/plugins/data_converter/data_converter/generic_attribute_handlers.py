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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import datetime

EXCLUSION_LIST_VALUE = "exclusion_list"

MERGE_SEPARATOR_VALUE = "merge_separator"

SPACE_VALUE = " "

TOKEN_SEPARATOR_VALUE = "token_separator"

TOKEN_OFFSETS_VALUE = "token_offsets"

VALUES_MAP_VALUE = "values_map"

def attribute_handler_extract_tokens(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
    # extracts the mandatory options
    token_separator = arguments[TOKEN_SEPARATOR_VALUE]
    token_offsets = arguments[TOKEN_OFFSETS_VALUE]

    # extracts the non-mandatory options
    merge_separator = arguments.get(MERGE_SEPARATOR_VALUE, ",")

    # extracts the specified tokens and merges them into a single string
    tokens = output_attribute_value.split(token_separator)
    output_attribute_value = "".join(unicode(tokens[token_index]) + merge_separator for token_index in range(len(tokens)) if token_index in token_offsets)[:-1]

    return output_attribute_value

def attribute_handler_convert_string_to_lowercase(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
    # converts the string to lowercase
    if output_attribute_value and type(output_attribute_value) in types.StringTypes:
        output_attribute_value = output_attribute_value.lower()

    return output_attribute_value

def attribute_handler_get_current_date(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
    # retrieves the current date and time
    current_datetime = datetime.datetime.utcnow()

    return current_datetime

def attribute_handler_capitalize_string(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
    # capitalizes the string
    if output_attribute_value and type(output_attribute_value) in types.StringTypes:
        output_attribute_value = output_attribute_value.capitalize()

    return output_attribute_value

def attribute_handler_map_value(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
    # retrieves the mandatory options
    values_map = arguments[VALUES_MAP_VALUE]

    # retrieves the value that is associated with the output attribute value
    # by using the provided map
    output_attribute_value = values_map[output_attribute_value]

    return output_attribute_value

def attribute_handler_convert_to_string(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
    # converts the value to a string
    if not output_attribute_value == None:
        output_attribute_value = str(output_attribute_value)

    return output_attribute_value

def attribute_handler_capitalize_tokens(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
    # retrieves the non-mandatory options
    exclusion_list = arguments.get(EXCLUSION_LIST_VALUE, [])

    # capitalizes all tokens in case the value is not null
    if output_attribute_value:
        output_attribute_value = capitalize_tokens(output_attribute_value, exclusion_list)

    return output_attribute_value

def capitalize_tokens(string_value, exclusion_list):
    # splits the string by the space character
    string_value = string_value.lower()
    tokens = string_value.split(SPACE_VALUE)

    # capitalizes all capitalizable tokens
    capitalized_string = str()
    for token in tokens:
        if not token in exclusion_list:
            token = token.capitalize()
        capitalized_string += token + SPACE_VALUE
    capitalized_string = capitalized_string[:-1]
    capitalized_string = capitalized_string[0].upper() + capitalized_string[1:]

    return capitalized_string
