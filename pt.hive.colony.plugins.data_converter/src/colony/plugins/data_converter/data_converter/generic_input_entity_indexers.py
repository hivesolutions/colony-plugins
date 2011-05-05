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

ATTRIBUTE_NAMES_VALUE = "attribute_names"

AND_VALUE = "and"

ENTITY_NAME_VALUE = "entity_name"

EQUALS_VALUE = "="

HANDLERS_VALUE = "handlers"

def input_indexer_primary_key(data_converter, configuration, input_intermediate_structure, input_entity, arguments):
    # retrieves the mandatory options
    attribute_names = arguments[ATTRIBUTE_NAMES_VALUE]

    # retrieves the non-mandatory options
    handlers = arguments.get(HANDLERS_VALUE, [])

    # sorts the attribute names so indexes are always created in the same order
    attribute_names = sorted(attribute_names, lambda x,y : cmp(x.lower(), y.lower()))

    # retrieves the attribute values that correspond to the specified attribute names
    attribute_values = [input_entity.get_attribute(attribute_name) for attribute_name in attribute_names if input_entity.has_attribute(attribute_name)]

    # passes the attribute values through the defined handlers
    for handler in handlers:
        attribute_values = [handler(attribute_value) for attribute_value in attribute_values]

    # returns in case not all attributes exist
    if not len(attribute_names) == len(attribute_values):
        return

    input_entity_name = input_entity.get_name()

    index = [
        ENTITY_NAME_VALUE, EQUALS_VALUE, input_entity_name, AND_VALUE
    ]

    # creates the index for the input entity
    attribute_name_value_pairs = zip(attribute_names, attribute_values)
    for attribute_name, attribute_value in attribute_name_value_pairs:
        index.extend([attribute_name, EQUALS_VALUE, attribute_value, AND_VALUE])
    index = index[:-1]
    index = tuple(index)

    # indexes the input entity in case it was not indexed this way before
    if not input_intermediate_structure.get_entities_by_index(index):
        input_intermediate_structure.index_entity(input_entity, index)
