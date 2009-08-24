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

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

class StoreConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Store entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract store entities from lojas entities
        lojas_input_entities = {NAME_VALUE : "lojas",
                                OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                      ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                      HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                         ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract store entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Store",
                                                   INPUT_ENTITIES_VALUE : [lojas_input_entities]}]

        # connector used to populate the addresses relation attribute
        addresses_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                               OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                               ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Address"]}}

        # defines how to populate the store entities' addresses relation attribute
        store_addresses_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["addresses"],
                                    RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                    CONNECTORS_VALUE : [addresses_connector]}

        # connector used to populate the contacts relation attribute
        contacts_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                              OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                              ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["ContactInformation"]}}

        # defines how to populate the store entities' contacts relation attribute
        store_contacts_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contacts"],
                                   RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                   CONNECTORS_VALUE : [contacts_connector]}

        # defines how to connect store entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "Store",
                                           RELATIONS_VALUE : [store_addresses_relation,
                                                              store_contacts_relation]}]

        # defines the handlers that should be executed when the conversion process is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Store" : ["addresses"],
                                                                       "Address" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"Store" : {"addresses[0]" : ["primary_address", "primary_address_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Store" : ["contacts"],
                                                                       "ContactInformation" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"Store" : {"contacts[0]" : ["primary_contact_information", "primary_contact_information_contactable_organizational_hierarchy_tree_nodes"]}}}}]
