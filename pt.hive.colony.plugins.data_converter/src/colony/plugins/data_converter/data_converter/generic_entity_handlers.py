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

EXCLUSION_LIST_VALUE = "exclusion_list"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ATTRIBUTE_NAMES_VALUE = "output_attribute_names"

SEPARATOR_VALUE = "separator"

SPACE_VALUE = " "

def entity_handler_merge_input_attributes(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, arguments):
    # retrieves the mandatory options
    input_attribute_names = arguments[INPUT_ATTRIBUTE_NAMES_VALUE]
    separator = arguments[SEPARATOR_VALUE]
    output_attribute_name = arguments[OUTPUT_ATTRIBUTE_NAME_VALUE]

    # joins all non null field values into one string separated by the specified separator
    values = [input_entity.get_attribute(attribute_name) for attribute_name in input_attribute_names if input_entity.get_attribute(attribute_name)]
    non_null_values = [value for value in values if value]
    values_string = "".join([(unicode(value) + separator) for value in non_null_values])[:-1 * len(separator)]

    # converts the merged string to none in case its empty
    if values_string == "":
        values_string = None

    # sets the merged values in the specified attribute
    output_entity.set_attribute(output_attribute_name, values_string)

    return output_entity

def entity_handler_capitalize_tokens(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, arguments):
    # retrieves the mandatory options
    output_attribute_names = arguments[OUTPUT_ATTRIBUTE_NAMES_VALUE]
    exclusion_list = arguments.get(EXCLUSION_LIST_VALUE, [])

    # capitalizes all tokens in each attribute in case the value is not null
    for output_attribute_name in output_attribute_names:
        output_attribute_value = output_entity.get_attribute(output_attribute_name)

        # skips this attribute in case its value is none
        if not output_attribute_value:
            continue

        # capitalizes the string's tokens and sets the result in the entity's attribute
        capitalized_string = capitalize_tokens(output_attribute_value, exclusion_list)
        output_entity.set_attribute(output_attribute_name, capitalized_string)

    return output_entity

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
