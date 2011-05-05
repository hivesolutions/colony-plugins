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

CREATED_VALUE = "created"

EQUALS_VALUE = "="

INPUT_ENTITY_VALUE = "input_entity"

INPUT_ENTITY_OBJECT_ID_VALUE = "input_entity_object_id"

OUTPUT_ENTITY_VALUE = "output_entity"

OUTPUT_ENTITY_NAME_VALUE = "output_entity_name"

OUTPUT_ENTITY_OBJECT_ID_VALUE = "output_entity_object_id"

WHERE_VALUE = "where"

def output_indexer_created_output_entities(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, arguments):
    input_entity_object_id = input_entity.get_object_id()
    output_entity_name = output_entity.get_name()

    # adds the output entity to the list of all output entities with this name that were created by this specific input entity
    output_entity_index = (
        OUTPUT_ENTITY_VALUE, WHERE_VALUE, INPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, input_entity_object_id,
        CREATED_VALUE, OUTPUT_ENTITY_NAME_VALUE, EQUALS_VALUE, output_entity_name
    )

    output_intermediate_structure.index_entity(output_entity, output_entity_index)

def output_indexer_creator_input_entity(data_converter, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, arguments):
    output_entity_object_id = output_entity.get_object_id()

    input_entity_index = (
        INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, output_entity_object_id
    )

    # indexes the input entity by the created output entity
    input_intermediate_structure.index_entity(input_entity, input_entity_index)
