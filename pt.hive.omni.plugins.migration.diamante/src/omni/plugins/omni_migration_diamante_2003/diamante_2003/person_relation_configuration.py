#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Omni ERP
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

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

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "related_entity_non_null_attribute_names"

RELATED_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE = "related_entity_null_attribute_names"

OMNI_MARRIED_PERSON_RELATION_TYPE = 1
""" Married person relation indicator in omni """

class PersonRelationConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni PersonRelation entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract person relation entities from clientes entities
        clientes_input_entities = {NAME_VALUE : "clientes",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attributes",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"clientes" : ["NOME", "CONJUGUE"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : ["NOME", "CONJUGUE"]}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "type",
                                                                                         DEFAULT_VALUE_VALUE : OMNI_MARRIED_PERSON_RELATION_TYPE}]}]}

        # defines how to extract person relation entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "PersonRelation",
                                                   INPUT_ENTITIES_VALUE : [clientes_input_entities]}]

        # connector used to populate the first person relation attribute
        first_person_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                  OUTPUT_DEPENDENCIES_VALUE : {"CustomerPerson" : []},
                                  ARGUMENTS_VALUE : {RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE : ["customer_code"],
                                                     OUTPUT_ENTITY_NAMES_VALUE : ["CustomerPerson"]}}

        # defines how to populate the person relation entities' first person relation attribute
        person_relation_first_person_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["first_person"],
                                                 RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["personally_related_with_as_first_person"],
                                                 CONNECTORS_VALUE : [first_person_connector]}

        # connector used to populate the second person relation attribute
        second_person_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                   OUTPUT_DEPENDENCIES_VALUE : {"CustomerPerson" : []},
                                   ARGUMENTS_VALUE : {RELATED_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE : ["customer_code"],
                                                      OUTPUT_ENTITY_NAMES_VALUE : ["CustomerPerson"]}}

        # defines how to populate the person relation entities' second person relation attribute
        person_relation_second_person_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["second_person"],
                                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["personally_related_with_as_second_person"],
                                                  CONNECTORS_VALUE : [second_person_connector]}

        # defines how to connect person relation entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "PersonRelation",
                                           RELATIONS_VALUE : [person_relation_first_person_relation,
                                                              person_relation_second_person_relation]}]
