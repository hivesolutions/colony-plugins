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

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

EXCLUSION_LIST_VALUE = "exclusion_list"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

SEPARATOR_VALUE = "separator"

SPACE_VALUE = " "

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ATTRIBUTE_NAMES_VALUE = "output_attribute_names"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

NEWLINE_CHARACTER = "\n"
""" The newline character in python """

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

FORNECED_ENTITY_OBSERVATION_ATTRIBUTE_NAMES = ["DENOMINA", "CONTACTO", "OBSERV", "APONTAMENT"]
""" List with the attribute names in a forneced input entity that contain observations """

class SupplierCompanyConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni SupplierCompany entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract supplier entities from forneced entities
        forneced_input_entities = {NAME_VALUE : "forneced",
                                   OUTPUT_ENTITIES_VALUE : [{HANDLERS_VALUE : [ # merges observations from various fields into one
                                                                                {FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                 INPUT_DEPENDENCIES_VALUE : {"forneced" : FORNECED_ENTITY_OBSERVATION_ATTRIBUTE_NAMES},
                                                                                 ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : FORNECED_ENTITY_OBSERVATION_ATTRIBUTE_NAMES,
                                                                                                    SEPARATOR_VALUE : NEWLINE_CHARACTER,
                                                                                                    OUTPUT_ATTRIBUTE_NAME_VALUE : "observations"}},
                                                                                # creates the name by joining the name and surname fields
                                                                                {FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                 INPUT_DEPENDENCIES_VALUE : {"forneced" : ["NOME", "SOBRENOME"]},
                                                                                 ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : ["NOME", "SOBRENOME"],
                                                                                                    SEPARATOR_VALUE : SPACE_VALUE,
                                                                                                    OUTPUT_ATTRIBUTE_NAME_VALUE : "name"}},
                                                                                # capitalizes each letter in the merged name and observations
                                                                                {FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                                 ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["name", "observations"],
                                                                                                    EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "corporate_tax_number",
                                                                                         ATTRIBUTE_NAME_VALUE : "CONTRI"}]}]}

        # defines how to extract supplier entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "SupplierCompany",
                                                   INPUT_ENTITIES_VALUE : [forneced_input_entities]}]

        # connector used to populate the addresses relation attribute
        addresses_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                               OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                               ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Address"]}}

        # defines how to populate the supplier company entities' addresses relation attribute
        supplier_company_addresses_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["addresses"],
                                               RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                               CONNECTORS_VALUE : [addresses_connector]}

        # connector used to populate the contacts relation attribute
        contacts_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                              OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                              ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["ContactInformation"]}}

        # defines how to populate the supplier company entities' contacts relation attribute
        supplier_company_contacts_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contacts"],
                                              RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                              CONNECTORS_VALUE : [contacts_connector]}

        # defines how to connect the extracted supplier company entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "SupplierCompany",
                                           RELATIONS_VALUE : [supplier_company_addresses_relation,
                                                              supplier_company_contacts_relation]}]

        # defines the handlers that should be executed when the conversion process is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"SupplierCompany" : ["addresses"],
                                                                       "Address" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"SupplierCompany" : {"addresses[0]" : ["primary_address", "primary_address_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"SupplierCompany" : ["contacts"],
                                                                       "ContactInformation" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"SupplierCompany" : {"contacts[0]" : ["primary_contact_information", "primary_contact_information_contactable_organizational_hierarchy_tree_nodes"]}}}}]
