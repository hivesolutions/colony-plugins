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

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

def post_conversion_handler_calculate_totals(data_converter, configuration, input_intermediate_structure, output_intermediate_structure, arguments):
    # extracts the mandatory options
    entity_attributes_map = arguments[ENTITY_ATTRIBUTES_MAP_VALUE]

    # sums the attribute values of entities in a entity's relation attribute and sets the
    # total in another entity attribute
    for entity_name_relation_name, attributes_map in entity_attributes_map.items():
        entity_name, relation_name = entity_name_relation_name

        # sums the attributes of each defined relation attribute's contents
        for attribute_name, related_attribute_name in attributes_map.items():

            # sums the attributes for every output entity of the specified name
            output_entities = output_intermediate_structure.get_entities_by_name(entity_name)
            for output_entity in output_entities:

                # retrieves the defined relation attribute and sums the specified attribute
                # for all the entities it contains
                total = 0
                related_entities = output_entity.get_attribute(relation_name)
                for related_entity in related_entities:
                    related_attribute_value = related_entity.get_attribute(related_attribute_name)
                    total += related_attribute_value

                # sets the total in the output entity
                output_entity.set_attribute(attribute_name, total)

    return output_intermediate_structure

def post_conversion_handler_copy_entity_attributes(data_converter, configuration, input_intermediate_structure, output_intermediate_structure, arguments):
    # extracts the mandatory options
    entity_attributes_map = arguments[ENTITY_ATTRIBUTES_MAP_VALUE]

    # copies the attributes from each defined entity into other entity attributes
    for entity_name, attributes_map in entity_attributes_map.iteritems():

        # retrieves the entities with the specified name
        entities = output_intermediate_structure.get_entities_by_name(entity_name)

        # copies the defined attributes from each entity into the other attributes
        for entity in entities:

            # copies each source attribute into the specified destination attribute
            for source_attribute_names, destination_attribute_names in attributes_map.iteritems():

                # retrieves destination attribute names for the source entity and
                # the copied entity
                destination_destination_attribute_name = None
                if type(destination_attribute_names) in types.StringTypes:
                    source_destination_attribute_name = destination_attribute_names
                else:
                    source_destination_attribute_name = destination_attribute_names[0]
                    destination_destination_attribute_name = destination_attribute_names[1]

                if type(source_attribute_names) in types.StringTypes:
                    source_attribute_names = [
                        source_attribute_names
                    ]

                for source_attribute_name in source_attribute_names:

                    # retrieves the specified source attribute index in case one is specified
                    source_attribute_index = None
                    if source_attribute_name[-1] == "]":
                        integer_index = source_attribute_name.index("[")
                        source_attribute_index = source_attribute_name[integer_index + 1 :-1]
                        source_attribute_index = int(source_attribute_index)
                        source_attribute_name = source_attribute_name[:integer_index]

                    # copies the source attribute into the destination attribute in case the source
                    # attribute exists
                    if entity.has_attribute(source_attribute_name):
                        source_attribute = entity.get_attribute(source_attribute_name)

                        # skips this source attribute in case its value is none
                        # or an empty list
                        if not source_attribute:
                            continue

                        # retrieves the source attribute from the specified list position in case the
                        # source attribute is a list and an index was specified
                        if not source_attribute_index == None:
                            source_attribute = source_attribute[source_attribute_index]

                        # copies the source attribute to the entitie's destination attribute
                        entity.set_attribute(source_destination_attribute_name, source_attribute)

                        # copies the source entity into the destination attribute's specified attribute
                        # in case one was specified
                        if destination_destination_attribute_name:
                            destination_destination_attribute_value = source_attribute.get_attribute(destination_destination_attribute_name)

                            # @todo: comment this
                            if type(destination_destination_attribute_value) == types.ListType:
                                destination_destination_attribute_value.append(entity)
                            else:
                                destination_destination_attribute_value = entity

                            source_attribute.set_attribute(destination_destination_attribute_name, destination_destination_attribute_value)

                        # skips to the next attribute copy configuration in case this one was already
                        # performed successfully
                        break

    return output_intermediate_structure
