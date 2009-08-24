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

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

EXCLUSION_LIST_VALUE = "exclusion_list"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ATTRIBUTE_NAMES_VALUE = "output_attribute_names"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

OUTPUT_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "output_entity_non_null_attribute_names"

SEPARATOR_VALUE = "separator"

SPACE_VALUE = " "

VALUES_MAP_VALUE = "values_map"

NEWLINE_CHARACTER = "\n"
""" The newline character in python """

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

CLIENTES_ENTITY_OBSERVATION_ATTRIBUTE_NAMES = ["DENOMINA", "OBSERV", "APONTAMENT"]
""" List with the name of the attributes where to extract observations from a clientes entity """

DIAMANTE_INACTIVE_ENTITY_STATUS = 1
""" The inactive entity status indicator in diamante """

DIAMANTE_MALE_GENDER = "1"
""" The male gender indicator in diamante """

DIAMANTE_FEMALE_GENDER = "2"
""" The female gender indicator in diamante """

DIAMANTE_GENDERLESS_GENDER = "3"
""" The genderless gender indicator in diamante """

DIAMANTE_INACTIVE_ENTITY_STATUS = 1
""" The inactive entity status indicator in diamante """

OMNI_GENDERLESS_GENDER = 0
""" The genderless gender indicator in omni """

OMNI_MALE_GENDER = 1
""" The male gender indicator in omni """

OMNI_FEMALE_GENDER = 2
""" The female gender indicator in omni """

class CustomerPersonConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni CustomerPerson entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract customer person entities from clientes entities
        customer_person_input_entities = {NAME_VALUE : "clientes",
                                          OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attributes",
                                                                                         INPUT_DEPENDENCIES_VALUE : {"clientes" : ["NOME"]},
                                                                                         ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : ["NOME"]}},
                                                                                        {FUNCTION_VALUE : "entity_validator_has_all_different_attribute_values",
                                                                                         INPUT_DEPENDENCIES_VALUE : {"clientes" : ["SEXO"]},
                                                                                         ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"SEXO" : DIAMANTE_GENDERLESS_GENDER}}}],
                                                                    HANDLERS_VALUE : [ # merges observations from various fields into one
                                                                                      {FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                       INPUT_DEPENDENCIES_VALUE : {"clientes" : CLIENTES_ENTITY_OBSERVATION_ATTRIBUTE_NAMES},
                                                                                       ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : CLIENTES_ENTITY_OBSERVATION_ATTRIBUTE_NAMES,
                                                                                                          SEPARATOR_VALUE : NEWLINE_CHARACTER,
                                                                                                          OUTPUT_ATTRIBUTE_NAME_VALUE : "observations"}},
                                                                                       # creates the name by joining the name and surname fields
                                                                                      {FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                       INPUT_DEPENDENCIES_VALUE : {"clientes" : ["NOME", "SOBRENOME"]},
                                                                                       ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : ["NOME", "SOBRENOME"],
                                                                                                          SEPARATOR_VALUE : SPACE_VALUE,
                                                                                                          OUTPUT_ATTRIBUTE_NAME_VALUE : "name"}},
                                                                                       # capitalizes each letter in the merged name and observations
                                                                                      {FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                                       ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["name", "observations"],
                                                                                                          EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                                    OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "customer_code",
                                                                                                ATTRIBUTE_NAME_VALUE : "CODIGO"},
                                                                                               {NAME_VALUE : "tax_number",
                                                                                                ATTRIBUTE_NAME_VALUE : "CONTRI"},
                                                                                               {NAME_VALUE : "customer_since",
                                                                                                ATTRIBUTE_NAME_VALUE : "CRIACAO"},
                                                                                               {NAME_VALUE : "national_id_number",
                                                                                                ATTRIBUTE_NAME_VALUE : "BIPROP"},
                                                                                               {NAME_VALUE : "birth_date",
                                                                                                ATTRIBUTE_NAME_VALUE : "ANOS"},
                                                                                               {NAME_VALUE : "gender",
                                                                                                ATTRIBUTE_NAME_VALUE : "SEXO",
                                                                                                HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_map_value",
                                                                                                                   ARGUMENTS_VALUE : {VALUES_MAP_VALUE : {DIAMANTE_GENDERLESS_GENDER : OMNI_GENDERLESS_GENDER,
                                                                                                                                                          DIAMANTE_MALE_GENDER : OMNI_MALE_GENDER,
                                                                                                                                                          DIAMANTE_FEMALE_GENDER : OMNI_FEMALE_GENDER}}}]},
                                                                                               {NAME_VALUE : "occupation",
                                                                                                ATTRIBUTE_NAME_VALUE : "CONTACTO",
                                                                                                HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                                   ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract customer person entities from clientes entities (customers that are married to the
        # customer that was registered)
        relation_customer_person_input_entities = {NAME_VALUE : "clientes",
                                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attributes",
                                                                                                  INPUT_DEPENDENCIES_VALUE : {"clientes" : ["NOME", "CONJUGUE"]},
                                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : ["NOME", "CONJUGUE"]}}],
                                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                                         ATTRIBUTE_NAME_VALUE : "CONJUGUE",
                                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                                            EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}]},
                                                                                                        {NAME_VALUE : "national_id_number",
                                                                                                         ATTRIBUTE_NAME_VALUE : "BICONJ"},
                                                                                                        {NAME_VALUE : "birth_date",
                                                                                                         ATTRIBUTE_NAME_VALUE : "ANICONJ"},
                                                                                                        {NAME_VALUE : "customer_since",
                                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_get_current_date"}]}]}]}

        # defines how to extract customer person entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "CustomerPerson",
                                                   INPUT_ENTITIES_VALUE : [customer_person_input_entities,
                                                                           relation_customer_person_input_entities]}]

        # connector used to populate the addresses relation attribute
        addresses_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                               OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                               ARGUMENTS_VALUE : {OUTPUT_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE : ["customer_code"],
                                                  OUTPUT_ENTITY_NAMES_VALUE : ["Address"]}}

        # defines how to populate the customer company entities' addresses relation attribute
        customer_person_addresses_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["addresses"],
                                              RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                              CONNECTORS_VALUE : [addresses_connector]}

        # connector used to populate the contacts relation attribute
        contacts_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                              OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                              ARGUMENTS_VALUE : {OUTPUT_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE : ["customer_code"],
                                                 OUTPUT_ENTITY_NAMES_VALUE : ["ContactInformation"]}}

        # defines how to populate the customer company entities' contacts relation attribute
        customer_person_contacts_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contacts"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                             CONNECTORS_VALUE : [contacts_connector]}

        # defines how to connect the extracted customer person entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "CustomerPerson",
                                           RELATIONS_VALUE : [customer_person_addresses_relation,
                                                              customer_person_contacts_relation]}]

        # defines the handlers that should be executed when the conversion process is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"CustomerPerson" : {"addresses[0]" : ["primary_address", "primary_address_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"CustomerPerson" : {"contacts[0]" : ["primary_contact_information", "primary_contact_information_contactable_organizational_hierarchy_tree_nodes"]}}}}]
