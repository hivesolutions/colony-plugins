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

import data_converter_exceptions

AND_VALUE = "and"

CREATED_VALUE = "created"

CREATOR_ENTITY_NAMES_VALUE = "creator_entity_names"

CREATOR_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "creator_entity_non_null_attribute_names"

CREATOR_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE = "creator_entity_null_attribute_names"

ENTITY_NAME_VALUE = "entity_name"

EQUALS_VALUE = "="

INPUT_OUTPUT_ENTITY_NAMES_VALUE = "input_output_entity_names"

INPUT_ENTITY_VALUE = "input_entity"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

INPUT_ENTITY_OBJECT_ID_VALUE = "input_entity_object_id"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

JOINS_VALUE = "joins"

OUTPUT_ENTITY_NAME_VALUE = "output_entity_name"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

OUTPUT_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "output_entity_non_null_attribute_names"

OUTPUT_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE = "output_entity_null_attribute_names"

OUTPUT_ENTITY_OBJECT_ID_VALUE = "output_entity_object_id"

OUTPUT_ENTITY_VALUE = "output_entity"

RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "related_entity_non_null_attribute_names"

RELATED_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE = "related_entity_null_attribute_names"

WHERE_VALUE = "where"

CREATOR = "%creator%"

def connector_output_entities_created_by_input_entity(data_converter, configuration, input_intermediate_structure, output_intermediate_structure, output_entity, arguments):
    # extracts the mandatory options
    joins = arguments[JOINS_VALUE]
    output_entity_names = arguments[OUTPUT_ENTITY_NAMES_VALUE]

    # returns no indexes in case the output entity is not valid
    if not is_valid_output_entity(output_entity, arguments):
        return []

    entity_name_entity_map = {}

    # retrieves the creator input entity
    output_entity_object_id = output_entity.get_object_id()
    creator_input_entity = get_creator_input_entity(input_intermediate_structure, output_entity_object_id)

    # raises an exception in case the creator input entity was not found
    if not creator_input_entity:
        raise data_converter_exceptions.DataConverterCreatorInputEntityNotFound(str(output_entity_object_id))

    # returns no indexes in case this creator entity is not valid
    if not is_valid_creator_entity(creator_input_entity, arguments):
        return []

    # indexes the creator input entity for later retrieval
    entity_name_entity_map[CREATOR] = creator_input_entity

    # jumps from input entity to input entity with the specified joins, until the final input entity is found
    for input_entity_name, join_attributes_map in joins:

        # collects tuples with the attribute name value pairs with which to perform the join
        attribute_name_value_tuples = []
        for input_attribute_name, join_attribute_value in join_attributes_map.iteritems():

            # retrieves the join attribute value from the specified input entity
            if type(join_attribute_value) == types.ListType:
                join_attribute_name, join_entity_name = join_attribute_value
                join_entity = entity_name_entity_map[join_entity_name]
                join_attribute_value = join_entity.get_attribute(join_attribute_name)

            # defines the attribute name value tuple
            attribute_name_value_tuple = (
                input_attribute_name,
                join_attribute_value
            )

            # adds the attribute name and value pair to the list of tuples
            attribute_name_value_tuples.append(attribute_name_value_tuple)

        # retrieves the input entity targeted by the join
        input_entity = get_input_entity(input_intermediate_structure, input_entity_name, attribute_name_value_tuples)
        entity_name_entity_map[input_entity_name] = input_entity

        # raises an exception in case the input entity was not found
        if not input_entity:
            # @todo: log warning
            return []

    # retrieves the output entities created by final retrieved input entity
    input_entity_object_id = input_entity.get_object_id()
    related_entities = []
    for output_entity_name in output_entity_names:
        related_entities.extend(get_created_output_entities(output_intermediate_structure, input_entity_object_id, output_entity_name))

    # removes the invalid related entities
    related_entities = [related_entity for related_entity in related_entities if related_entity]

    return related_entities

def connector_output_entities_created_by_creator_input_entity(data_converter, configuration, input_intermediate_structure, output_intermediate_structure, output_entity, arguments):
    # extracts the mandatory options
    output_entity_names = arguments[OUTPUT_ENTITY_NAMES_VALUE]

    # returns no indexes in case the output entity is not valid
    if not is_valid_output_entity(output_entity, arguments):
        return []

    # retrieves the creator input entity
    output_entity_object_id = output_entity.get_object_id()
    creator_input_entity = get_creator_input_entity(input_intermediate_structure, output_entity_object_id)

    # raises an exception in case the creator input entity was not found
    if not creator_input_entity:
        raise data_converter_exceptions.DataConverterCreatorInputEntityNotFound(str(output_entity_object_id))

    # returns no indexes in case this creator entity is not valid
    if not is_valid_creator_entity(creator_input_entity, arguments):
        return []

    # retrieves the entities created by the creator input entity
    creator_input_entity_object_id = creator_input_entity.get_object_id()
    related_entities = []
    for output_entity_name in output_entity_names:
        related_entities.extend(get_created_output_entities(output_intermediate_structure, creator_input_entity_object_id, output_entity_name))

    # removes the invalid related entities
    related_entities = [related_entity for related_entity in related_entities if related_entity and is_valid_related_entity(related_entity, arguments)]

    return related_entities

def connector_output_entities_different_creator_input_entity(data_converter, configuration, input_intermediate_structure, output_intermediate_structure, output_entity, arguments):
    # extracts the mandatory options
    input_entity_name = arguments[INPUT_ENTITY_NAME_VALUE]
    join_attributes = arguments[JOIN_ATTRIBUTES_VALUE]
    output_entity_names = arguments[OUTPUT_ENTITY_NAMES_VALUE]

    # returns no indexes in case the output entity is not valid
    if not is_valid_output_entity(output_entity, arguments):
        return []

    # retrieves the the entity that originated this output entity
    output_entity_object_id = output_entity.get_object_id()
    creator_input_entity = get_creator_input_entity(input_intermediate_structure, output_entity_object_id)

    # raises an exception in case the creator input entity was not found
    if not creator_input_entity:
        raise data_converter_exceptions.DataConverterCreatorInputEntityNotFound(str(output_entity_object_id))

    # returns no indexes in case this creator entity is not valid
    if not is_valid_creator_entity(creator_input_entity, arguments):
        return []

    # retrieves the input entity targeted by the join
    attribute_name_value_tuples = [(input_entity_attribute, creator_input_entity.get_attribute(creator_input_entity_attribute)) for input_entity_attribute, creator_input_entity_attribute in join_attributes.items()]
    input_entity = get_input_entity(input_intermediate_structure, input_entity_name, attribute_name_value_tuples)

    # raises an exception in case the input entity was not found
    if not input_entity:
        # @todo: log a warning
        return []

    # retrieves the output entities created by the input entity
    input_entity_object_id = input_entity.get_object_id()
    related_entities = []
    for output_entity_name in output_entity_names:
        related_entities.extend(get_created_output_entities(output_intermediate_structure, input_entity_object_id, output_entity_name))

    # removes the invalid output entities
    related_entities = [related_entity for related_entity in related_entities if related_entity and is_valid_related_entity(related_entity, arguments)]

    return related_entities

def connector_output_entities_created_by_input_entities(data_converter, configuration, input_intermediate_structure, output_intermediate_structure, output_entity, arguments):
    # extracts the mandatory options
    input_entity_name_output_entity_names_map = arguments[INPUT_OUTPUT_ENTITY_NAMES_VALUE]

    # returns no indexes in case the output entity is not valid
    if not is_valid_output_entity(output_entity, arguments):
        return []

    # retrieves the creator input entity
    output_entity_object_id = output_entity.get_object_id()
    creator_input_entity = get_creator_input_entity(input_intermediate_structure, output_entity_object_id)

    # raises an exception in case the creator input entity was not found
    if not creator_input_entity:
        raise data_converter_exceptions.DataConverterCreatorInputEntityNotFound(str(output_entity_object_id))

    # returns no indexes in case this creator entity is not valid
    if not is_valid_creator_entity(creator_input_entity, arguments):
        return []

    # retrieves the created output entities for each creator input entity
    related_entities = []
    for input_entity_name, output_entity_names in input_entity_name_output_entity_names_map.iteritems():
        creator_input_entities = input_intermediate_structure.get_entities_by_name(input_entity_name)

        # collects the output entities of the specified names created by each creator input entity
        for creator_input_entity in creator_input_entities:
            creator_input_entity_object_id = creator_input_entity.get_object_id()
            for output_entity_name in output_entity_names:
                related_entities.extend(get_created_output_entities(output_intermediate_structure, creator_input_entity_object_id, output_entity_name))

    # removes the invalid related entities
    related_entities = [related_entity for related_entity in related_entities if related_entity]
    related_entities = [related_entity for related_entity in related_entities if related_entity and is_valid_related_entity(related_entity, arguments)]

    return related_entities

def connector_all_output_entities(data_converter, configuration, input_intermediate_structure, output_intermediate_structure, output_entity, arguments):
    # extracts the mandatory options
    output_entity_names = arguments[OUTPUT_ENTITY_NAMES_VALUE]

    # returns no indexes in case the output entity is not valid
    if not is_valid_output_entity(output_entity, arguments):
        return []

    # retrieves the creator input entity
    output_entity_object_id = output_entity.get_object_id()
    creator_input_entity = get_creator_input_entity(input_intermediate_structure, output_entity_object_id)

    # raises an exception in case the creator input entity was not found
    if not creator_input_entity:
        raise data_converter_exceptions.DataConverterCreatorInputEntityNotFound(str(output_entity_object_id))

    # returns no indexes in case this creator entity is not valid
    if not is_valid_creator_entity(creator_input_entity, arguments):
        return []

    # collects all output entities with the specified names
    related_entities = []
    for output_entity_name in output_entity_names:
        related_entities.extend(output_intermediate_structure.get_entities_by_name(output_entity_name))

    # removes the invalid related entities
    related_entities = [related_entity for related_entity in related_entities if related_entity and is_valid_related_entity(related_entity, arguments)]

    return related_entities

def is_valid_creator_entity(creator_input_entity, arguments):
    # retrieves the specified validators
    creator_entity_names = arguments.get(CREATOR_ENTITY_NAMES_VALUE, None)
    creator_entity_null_attribute_names = arguments.get(CREATOR_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE, [])
    creator_entity_non_null_attribute_names = arguments.get(CREATOR_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE, [])

    # declares the connector as invalid in case the creator input entity doesn't have
    # one of the specified names
    if creator_input_entity:
        creator_input_entity_name = creator_input_entity.get_name()
        if creator_entity_names and not creator_input_entity_name in creator_entity_names:
            return False

    # declares the connector as invalid in case the creator input entity doesn't have
    # the specified attribute value as null
    creator_entity_null_attribute_values = [None for creator_entity_null_attribute_name in creator_entity_null_attribute_names if not creator_input_entity.has_attribute(creator_entity_null_attribute_name) or creator_input_entity.get_attribute(creator_entity_null_attribute_name) == None]
    if not len(creator_entity_null_attribute_names) == len(creator_entity_null_attribute_values):
        return False

    # declares the connector as invalid in case the creator input entity doesn't have
    # the specified attribute value as not null
    creator_entity_non_null_attribute_values = [creator_input_entity.get_attribute(creator_entity_non_null_attribute_name) for creator_entity_non_null_attribute_name in creator_entity_non_null_attribute_names if creator_input_entity.has_attribute(creator_entity_non_null_attribute_name) and not creator_input_entity.get_attribute(creator_entity_non_null_attribute_name) == None]
    if not len(creator_entity_non_null_attribute_names) == len(creator_entity_non_null_attribute_values):
        return False

    return True

def is_valid_output_entity(output_entity, arguments):
    # retrieves the specified validators
    output_entity_null_attribute_names = arguments.get(OUTPUT_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE, [])
    output_entity_non_null_attribute_names = arguments.get(OUTPUT_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE, [])

    # declares the connector as invalid in case the output input entity doesn't have
    # the specified attribute value as null
    output_entity_null_attribute_values = [None for output_entity_null_attribute_name in output_entity_null_attribute_names if not output_entity.has_attribute(output_entity_null_attribute_name) or output_entity.get_attribute(output_entity_null_attribute_name) == None]
    if not len(output_entity_null_attribute_names) == len(output_entity_null_attribute_values):
        return False

    # declares the connector as invalid in case the output input entity doesn't have
    # the specified attribute value as not null
    output_entity_non_null_attribute_values = [output_entity.get_attribute(output_entity_non_null_attribute_name) for output_entity_non_null_attribute_name in output_entity_non_null_attribute_names if output_entity.has_attribute(output_entity_non_null_attribute_name) and not output_entity.get_attribute(output_entity_non_null_attribute_name) == None]
    if not len(output_entity_non_null_attribute_names) == len(output_entity_non_null_attribute_values):
        return False

    return True

def is_valid_related_entity(related_entity, arguments):
    # retrieves the specified validators
    related_entity_null_attribute_names = arguments.get(RELATED_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE, [])
    related_entity_non_null_attribute_names = arguments.get(RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE, [])

    # declares the connector as invalid in case the related input entity doesn't have
    # the specified attribute value as null
    related_entity_null_attribute_values = [None for related_entity_null_attribute_name in related_entity_null_attribute_names if not related_entity.has_attribute(related_entity_null_attribute_name) or related_entity.get_attribute(related_entity_null_attribute_name) == None]
    if not len(related_entity_null_attribute_names) == len(related_entity_null_attribute_values):
        return False

    # declares the connector as invalid in case the related input entity doesn't have
    # the specified attribute value as not null
    related_entity_non_null_attribute_values = [None for related_entity_non_null_attribute_name in related_entity_non_null_attribute_names if related_entity.has_attribute(related_entity_non_null_attribute_name) and not related_entity.get_attribute(related_entity_non_null_attribute_name) == None]
    if not len(related_entity_non_null_attribute_names) == len(related_entity_non_null_attribute_values):
        return False

    return True

def get_input_entity(input_intermediate_structure, input_entity_name, attribute_name_value_tuples):
    # sorts the join attributes so the index is always built in the same order
    sorted_join_attributes = sorted(attribute_name_value_tuples, lambda x,y : cmp(x[0].lower(), y[0].lower()))

    # creates the input entity index
    input_entity_index = [ENTITY_NAME_VALUE, EQUALS_VALUE, input_entity_name]
    for attribute_name, attribute_value in sorted_join_attributes:
        input_entity_index.extend([AND_VALUE, attribute_name, EQUALS_VALUE, attribute_value])
    input_entity_index = tuple(input_entity_index)

    # returns in case a null value is in the index
    if None in input_entity_index:
        return None

    # retrieves the input entities that are indexed with this index
    input_entities = input_intermediate_structure.get_entities_by_index(input_entity_index)

    # raises an exception in case more than one input entity is found when only one was expected
    if len(input_entities) > 1:
        raise data_converter_exceptions.DataConverterUnexpectedNumberInputEntitiesException(str(len(input_entities)))

    # returns None in case no entity was found
    if not input_entities:
        # @todo: log warning
        return None

    input_entity = input_entities[0]

    return input_entity

def get_creator_input_entity(input_intermediate_structure, output_entity_object_id):
    input_entity_index = (
        INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, output_entity_object_id
    )

    input_entities = input_intermediate_structure.get_entities_by_index(input_entity_index)

    # raises an exception in case more than one input entity is found when only one was expected
    if len(input_entities) > 1:
        raise data_converter_exceptions.DataConverterUnexpectedNumberInputEntitiesException(str(len(input_entities)))

    # returns None in case no entity was found
    if not input_entities:
        # @todo: log warning
        return None

    input_entity = input_entities[0]

    return input_entity

def get_created_output_entities(output_intermediate_structure, input_entity_object_id, output_entity_name):
    output_entity_index = (
        OUTPUT_ENTITY_VALUE, WHERE_VALUE, INPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, input_entity_object_id,
        CREATED_VALUE, OUTPUT_ENTITY_NAME_VALUE, EQUALS_VALUE, output_entity_name
    )

    output_entities = output_intermediate_structure.get_entities_by_index(output_entity_index)

    return output_entities
