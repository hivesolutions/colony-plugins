#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import types

import formcode_exceptions

NAME_TYPE_VALUE = "name"
""" The name type value """

SEQUENCE_TYPE_VALUE = "sequence"
""" The sequence type value """

MAP_TYPE_VALUE = "map"
""" The map type value """

ATTRIBUTE_PARSING_REGEX_VALUE = "(?P<name>[\w]+)|(?P<sequence>\[\])|(?P<map>\[\w+\])"
""" The attribute parsing regular expression value """

ATTRIBUTE_PARSING_REGEX = re.compile(ATTRIBUTE_PARSING_REGEX_VALUE)
""" The attribute parsing regex """

NUMBER_TYPES = {
    types.IntType : True,
    types.LongType: True,
    types.FloatType : True
}
""" The map used to check number types """

SEQUENCE_TYPES = {
    types.TupleType : True,
    types.ListType : True,
    types.GeneratorType : True
}
""" The map used to check sequence types """

def dumps(object, base_path = ""):
    return "".join([part for part in dump_parts(object, base_path)]).rstrip("&")

def dump_parts(object, current_path):
    """
    Dumps (converts to formcode) the given object parts using the "normal"
    approach.

    @type object: Object
    @param object: The object to have the parts dumped.
    @type String: String
    @param String: The current path value.
    @rtype: String
    @return: The dumped formcode string.
    """

    # retrieves the object type
    object_type = type(object)

    # in case the object is none
    if object == None:
        # yields the null (empty) value
        yield _create_value("", current_path)
    # in case the object is a sequence
    elif object_type in SEQUENCE_TYPES:
        # creates the new current path
        current_path = current_path + "[]"

        # iterates over all the item in the object
        for item in object:
            # iterates over all the parts of the item
            for part in dump_parts(item, current_path):
                # yields the part
                yield part
    # in case the object is a dictionary
    elif object_type is types.DictionaryType:
        # iterates over all the object items
        for key, value in object.items():
            # creates the new current path
            new_current_path = current_path + "[" + unicode(key) + "]"

            # iterates over all the parts of the value
            for part in dump_parts(value, new_current_path):
                # yields the part
                yield part
    # in case the object is a boolean
    elif object_type is types.BooleanType:
        # in case the object is valid (true)
        if object:
            # yields the true value
            yield _create_value("true", current_path)
        # otherwise
        else:
            # yields the false value
            yield _create_value("false", current_path)
    # in case the object is a number
    elif object_type in NUMBER_TYPES:
        # yields the number unicode value
        yield _create_value(unicode(object), current_path)
    # in case the object is a string
    elif object_type in types.StringTypes:
        # yields the string value
        yield _create_value(object, current_path)
    # in case a different type is set
    else:
        # raises the formcode encode exception
        raise formcode_exceptions.FormcodeEncodeException(object)

def loads(data):
    # creates the base attributes map
    base_attributes_map = {}

    # splits the data on the and value
    # retrieving the form attribute pairs
    form_attribute_pairs = data.split("&")

    # iterates over all the form attribute pairs
    for form_attribute_pair in form_attribute_pairs:
        # splits the form attribute pair retrieving the form
        # attribute name and value
        form_attribute_name, form_attribute_value = form_attribute_pair.split("=")

        # parses the given form attribute using the base attributes map and the
        # current form attribute name and value
        _process_form_attribute(base_attributes_map, form_attribute_name, form_attribute_value)

    # returns the base attributes map
    return base_attributes_map

def _create_value(value, current_path):
    """
    Creates the value base on the given value (string)
    and for the given current path.

    @type value: String
    @param value: The string value to be used in the
    creation of the value.
    @type current_path: String
    @param current_path: The current path to be used.
    @rtype: String
    @return: The created value.
    """

    return current_path + "=" + value + "&"

def _process_form_attribute(parent_structure, current_attribute_name, attribute_value, index = 0):
    """
    Processes a form attribute using the sent parent structure and for
    the given index as a reference.
    At the end the parent structure is changed and contains the form
    attribute in the correct structure place.

    @type parent_structure: List/Dictionary
    @param parent_structure: The parent structure to be used to set the
    attribute.
    @type current_attribute_name: String
    @param current_attribute_name: The current attribute name, current
    because it's parsed
    recursively using this process method.
    @type attribute_value: Object
    @param attribute_value: The attribute value.
    @type index: int
    @param index: The index of the current attribute reference.
    """

    # retrieves the current match result
    match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name)

    # in case there is no match result
    if not match_result:
        # raises the formcode decode exception
        raise formcode_exceptions.FormcodeEncodeException("invalid match value: " + current_attribute_name)

    # retrieves the match result end position
    match_result_end = match_result.end()

    # checks if it's the last attribute name
    is_last_attribute_name = match_result_end == len(current_attribute_name)

    # retrieves the match result name
    match_result_name = match_result.lastgroup

    # retrieves the match result value
    match_result_value = match_result.group()

    # in case the match result value is of type map
    # the parentheses need to be removed
    if match_result_name == MAP_TYPE_VALUE:
        # retrieves the match result value without the parentheses
        match_result_value = match_result_value[1:-1]

    # in case it's the only (last) match available
    if is_last_attribute_name:
        # in case the match result is of type name
        if match_result_name == NAME_TYPE_VALUE:
            # sets the attribute value in the parent structure
            parent_structure[match_result_value] = attribute_value
        # in case the match result is of type sequence
        elif match_result_name == SEQUENCE_TYPE_VALUE:
            # adds the attribute value to the
            # parent structure
            parent_structure.append(attribute_value)
        # in case the match result is of type map
        elif match_result_name == MAP_TYPE_VALUE:
            # sets the attribute value in the parent structure
            parent_structure[match_result_value] = attribute_value

    # there is more parsing to be made
    else:
        # retrieves the next match value in order to make
        next_match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name, match_result_end)

        # in case there is no next match result
        if not next_match_result:
            # raises the formcode decode exception
            raise formcode_exceptions.FormcodeEncodeException("invalid next match value: " + current_attribute_name)

        # retrieves the next match result name
        next_match_result_name = next_match_result.lastgroup

        # retrieves the next match result value
        next_match_result_value = next_match_result.group()

        # in case the next match result value is of type map
        # the parentheses need to be removed
        if next_match_result_name == MAP_TYPE_VALUE:
            # retrieves the next match result value without the parentheses
            next_match_result_value = next_match_result_value[1:-1]

        # in case the next match is of type name
        if next_match_result_name == NAME_TYPE_VALUE:
            # raises the formcode decode exception
            raise formcode_exceptions.FormcodeEncodeException("invalid next match value (it's a name): " + current_attribute_name)

        # in case the next match is of type list, a list needs to
        # be created in order to support the sequence, in case a list
        # already exists it is used instead
        elif next_match_result_name == SEQUENCE_TYPE_VALUE:
            # in case the match result value exists in the
            # parent structure there is no need to create a new structure
            # the previous one should be used
            if match_result_value in parent_structure:
                # sets the current attribute value as the value that
                # exists in the parent structure
                current_attribute_value = parent_structure[match_result_value]
            else:
                # creates a new list structure
                current_attribute_value = []
        # in case the next match is of type map, a map needs to
        # be created in order to support the mapping structure, in case a map
        # already exists it is used instead
        elif next_match_result_name == MAP_TYPE_VALUE:
            # in case the current match result is a sequence
            # it's required to check for the valid structure
            # it may be set or it may be a new structure depending
            # on the current "selected" index
            if match_result_name == SEQUENCE_TYPE_VALUE:
                # retrieves the parent structure length
                parent_structure_length = len(parent_structure)

                # in case the parent structure length is
                # not sufficient to hold the the elements
                if parent_structure_length <= index:
                    # creates a new map structure
                    current_attribute_value = {}
                else:
                    # sets the current attribute value as the structure
                    # in the current "selected" index
                    current_attribute_value = parent_structure[index]
            # in case the match result value exists in the
            # parent structure there is no need to create a new structure
            # the previous one should be used
            elif match_result_value in parent_structure:
                # sets the current attribute value as the value that
                # exists in the parent structure
                current_attribute_value = parent_structure[match_result_value]
            else:
                # creates a new map structure
                current_attribute_value = {}

        # in case the match result is of type name (first match)
        if match_result_name == NAME_TYPE_VALUE:
            # sets the current attribute value in the parent structure
            parent_structure[match_result_value] = current_attribute_value
        # in case the match result is of type sequence
        elif match_result_name == SEQUENCE_TYPE_VALUE:
            # retrieves the parent structure length
            parent_structure_length = len(parent_structure)

            # in case the current attribute value is meant
            # to be added to the parent structure
            if parent_structure_length <= index:
                # adds the current attribute value to the
                # parent structure
                parent_structure.append(current_attribute_value)
        # in case the match result is of type map
        elif match_result_name == MAP_TYPE_VALUE:
            # sets the current attribute value in the parent structure
            parent_structure[match_result_value] = current_attribute_value

        # retrieves the remaining attribute name
        remaining_attribute_name = current_attribute_name[match_result_end:]

        # processes the next form attribute with the current attribute value as the new parent structure
        # the remaining attribute name as the new current attribute name and the attribute value
        # continues with the same value
        _process_form_attribute(current_attribute_value, remaining_attribute_name, attribute_value, index)
