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

ATTRIBUTES_VALUE = "attributes"

def entity_validator_has_all_attributes(data_converter, configuration, input_intermediate_structure, input_entity, arguments):
    """
    Validator used to verify if the input entity has all of the
    specified attributes.

    @type data_converter: DataConverter
    @param data_converter: The data converter.
    @type configuration: DataConverterConfiguration
    @param configuration: The data converter configuration being used.
    @type input_intermediate_structure: IntermediateStructure
    @param input_intermediate_structure: Intermediate structure
    where data is converted from.
    @type input_entity: Entity
    @param input_entity: Entity one wants to validate.
    @type arguments: Dictionary
    @param arguments: Options used to configure the validator's
    behaviour.
    @rtype: bool
    @return: Boolean indicating if the entity passes the validator
    test.
    """

    # retrieves the mandatory options
    attribute_names = arguments[ATTRIBUTES_VALUE]

    # returns false in case one of the attributes is null
    for attribute_name in attribute_names:
        input_entity_attribute_value = input_entity.get_attribute(attribute_name)
        if input_entity_attribute_value == None:
            return False

    return True

def entity_validator_has_any_attribute(data_converter, configuration, input_intermediate_structure, input_entity, arguments):
    """
    Validator used to verify if the input entity has any of the
    specified attributes.

    @type data_converter: DataConverter
    @param data_converter: The data converter.
    @type configuration: DataConverterConfiguration
    @param configuration: The data converter configuration being used.
    @type input_intermediate_structure: IntermediateStructure
    @param input_intermediate_structure: Intermediate structure
    where data is converted from.
    @type input_entity: Entity
    @param input_entity: Entity one wants to validate.
    @type arguments: Dictionary
    @param arguments: Options used to configure the validator's
    behaviour.
    @rtype: bool
    @return: Boolean indicating if the entity passes the validator
    test.
    """

    # retrieves the mandatory options
    attribute_names = arguments[ATTRIBUTES_VALUE]

    attribute_values = [input_entity.get_attribute(attribute_name) for attribute_name in attribute_names if not input_entity.get_attribute(attribute_name) == None]

    return bool(attribute_values)

def entity_validator_has_all_attribute_values(data_converter, configuration, input_intermediate_structure, input_entity, arguments):
    """
    Validator used to verify if the input entity has all of the
    specified attribute values.

    @type data_converter: DataConverter
    @param data_converter: The data converter.
    @type input_intermediate_structure: IntermediateStructure
    @param input_intermediate_structure: Intermediate structure
    where data is converted from.
    @type input_entity: Entity
    @param input_entity: Entity one wants to validate.
    @type arguments: Dictionary
    @param arguments: Options used to configure the validator's
    behaviour.
    @rtype: bool
    @return: Boolean indicating if the entity passes the validator
    test.
    """

    # retrieves the mandatory options
    attribute_name_value_map = arguments[ATTRIBUTES_VALUE]

    # returns false in case the entity doesn't have one of the specified attribute values
    for attribute_name, attribute_value in attribute_name_value_map.iteritems():
        input_entity_attribute_value = input_entity.get_attribute(attribute_name)
        if not input_entity_attribute_value == attribute_value:
            return False

    return True

def entity_validator_has_all_different_attribute_values(data_converter, configuration, input_intermediate_structure, input_entity, arguments):
    """
    Validator used to verify if the input entity has none of the
    specified attribute values.

    @type data_converter: DataConverter
    @param data_converter: The data converter.
    @type input_intermediate_structure: IntermediateStructure
    @param input_intermediate_structure: Intermediate structure
    where data is converted from.
    @type input_entity: Entity
    @param input_entity: Entity one wants to validate.
    @type arguments: Dictionary
    @param arguments: Options used to configure the validator's
    behaviour.
    @rtype: bool
    @return: Boolean indicating if the entity passes the validator
    test.
    """

    # retrieves the mandatory options
    attribute_name_value_map = arguments[ATTRIBUTES_VALUE]

    # returns false in case the entity has one of the specified attribute values
    for attribute_name, attribute_value in attribute_name_value_map.iteritems():
        input_entity_attribute_value = input_entity.get_attribute(attribute_name)
        if input_entity_attribute_value == attribute_value:
            return False

    return True

def entity_validator_has_all_attribute_values_in_list(data_converter, configuration, input_intermediate_structure, input_entity, arguments):
    """
    Validator used to verify if the input entity has all of the
    specified attribute values.

    @type data_converter: DataConverter
    @param data_converter: The data converter.
    @type configuration: DataConverterConfiguration
    @param configuration: The data converter configuration being used.
    @type input_intermediate_structure: IntermediateStructure
    @param input_intermediate_structure: Intermediate structure
    where data is converted from.
    @type input_entity: Entity
    @param input_entity: Entity one wants to validate.
    @type arguments: Dictionary
    @param arguments: Options used to configure the validator's
    behaviour.
    @rtype: bool
    @return: Boolean indicating if the entity passes the validator
    test.
    """

    # retrieves the mandatory options
    attribute_name_list_pairs_map = arguments[ATTRIBUTES_VALUE]

    # returns false in case one of the attribute values is not on the correspondent list
    for attribute_name, value_list in attribute_name_list_pairs_map.iteritems():
        input_entity_attribute_value = input_entity.get_attribute(attribute_name)
        if not input_entity_attribute_value in value_list:
            return False

    return True
