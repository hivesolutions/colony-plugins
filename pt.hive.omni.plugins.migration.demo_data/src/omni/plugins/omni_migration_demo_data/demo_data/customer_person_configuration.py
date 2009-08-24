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

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

DEMO_DATA_CUSTOMER_PERSON_TYPE = "customer_person"
""" The customer person type indicator in the demo data """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class CustomerPersonConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni CustomerPerson entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to index the loaded input intermediate structure entities
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["DD_Media_Customer"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"DD_Media_Customer" : ["name_without_extension"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["name_without_extension"],
                                                          HANDLERS_VALUE : [self.convert_media_id]}}]

        # defines how to extract customer person entities from dd_customer entities
        dd_customer_input_entities = {NAME_VALUE : "DD_Customer",
                                      OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                     INPUT_DEPENDENCIES_VALUE : {"DD_Customer" : ["Type"]},
                                                                                     ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"Type" : DEMO_DATA_CUSTOMER_PERSON_TYPE}}}],
                                                                OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "customer_code",
                                                                                            ATTRIBUTE_NAME_VALUE : "Id",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "national_id_number",
                                                                                            ATTRIBUTE_NAME_VALUE : "Bi",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "tax_number",
                                                                                            ATTRIBUTE_NAME_VALUE : "Nif",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "birth_date",
                                                                                            ATTRIBUTE_NAME_VALUE : "Birthdate"},
                                                                                           {NAME_VALUE : "customer_since",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_get_current_date"}]},
                                                                                           {NAME_VALUE : "name",
                                                                                            ATTRIBUTE_NAME_VALUE : "Name"},
                                                                                           {NAME_VALUE : "status",
                                                                                            DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract customer person entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "CustomerPerson",
                                                   INPUT_ENTITIES_VALUE : [dd_customer_input_entities]}]

        # connector used to populate the addresses relation attribute
        addresses_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                               OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                               ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Address"]}}

        # defines how to populate the customer person entities' addresses relation attribute
        customer_person_addresses_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["addresses"],
                                              RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                              CONNECTORS_VALUE : [addresses_connector]}

        # connector used to populate the contacts relation attribute
        contacts_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                              OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                              ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["ContactInformation"]}}

        # defines how to populate the customer person entities' contacts relation attribute
        customer_person_contacts_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contacts"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                             CONNECTORS_VALUE : [contacts_connector]}

        # connector used to populate the media relation attribute with media entities
        media_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                           INPUT_DEPENDENCIES_VALUE : {"DD_Media_Customer" : ["name_without_extension"],
                                                       "DD_Merchandise" : ["Id"]},
                           OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Media_Customer",
                                              JOIN_ATTRIBUTES_VALUE : {"name_without_extension" : "Id"},
                                              OUTPUT_ENTITY_NAMES_VALUE : ["Media"]}}

        # defines how to populate the customer person entities' parent nodes relation
        customer_person_media_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["media"],
                                          RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["entities"],
                                          CONNECTORS_VALUE : [media_connector]}

        # defines how to connect the extracted customer person entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "CustomerPerson",
                                           RELATIONS_VALUE : [customer_person_addresses_relation,
                                                              customer_person_contacts_relation,
                                                              customer_person_media_relation]}]

        # defines the handlers that should be executed when the conversion process is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"CustomerPerson" : {"addresses[0]" : ["primary_address", "primary_address_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"CustomerPerson" : {"contacts[0]" : ["primary_contact_information", "primary_contact_information_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"CustomerPerson" : {"media[0]" : ["primary_media", "primary_entities"]}}}}]

    def convert_media_id(self, value):
        # retrieves the media's id
        if "_" in value:
            value = value[:value.index("_")]

        # tries to convert the id to
        # an integer
        try:
            value = int(value)
        except:
            pass

        return value
