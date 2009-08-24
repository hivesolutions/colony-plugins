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

ATTRIBUTE_NAMES_VALUE = "attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

JOINS_VALUE = "joins"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "related_entity_non_null_attribute_names"

CREATOR = "%creator%"
""" Value used to identify a creator input entity """

DIAMANTE_MONEY_SALE_SLIP_DOCUMENT_TYPE = "V/D"
""" The money sale slip document type in diamante """

DIAMANTE_INVOICE_DOCUMENT_TYPE = "FAC"
""" The invoice document type in diamante """

DIAMANTE_CREDIT_NOTE_DOCUMENT_TYPE = "NCR"
""" The credit note document type in diamante """

class CustomerReturnConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni CustomerReturn entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to index the loaded input intermediate structure entities
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["vendas"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"vendas" : ["DOCUMENTO", "TIPODOC"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "TIPODOC"]}},
                                      {ENTITY_NAMES_VALUE : ["extrdoc"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"extrdoc" : ["DOCUMENTO", "DOCVINDODE", "TIPODOC"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "DOCVINDODE", "TIPODOC"]}}]

        # defines how to extract customer return entities from vendas entities
        vendas_input_entities = {NAME_VALUE : "vendas",
                                 OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                INPUT_DEPENDENCIES_VALUE : {"vendas" : ["TIPODOC"]},
                                                                                ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : DIAMANTE_CREDIT_NOTE_DOCUMENT_TYPE}}}],
                                                           OUTPUT_ATTRIBUTES_VALUE : []}]}

        # defines how to extract customer return entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "CustomerReturn",
                                                   INPUT_ENTITIES_VALUE : [vendas_input_entities]}]

        # connector used to populate the credit note relation attribute
        credit_note_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                 OUTPUT_DEPENDENCIES_VALUE : {"CreditNote" : []},
                                 ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["CreditNote"]}}

        # defines how to populate the customer return entities' credit note relation
        customer_return_credit_note_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["credit_note"],
                                                RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["customer_return"],
                                                CONNECTORS_VALUE : [credit_note_connector]}

        # connector used to populate the customer relation attribute
        customer_person_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                     INPUT_DEPENDENCIES_VALUE : {"clientes" : ["CODIGO"],
                                                                 "vendas" : ["CLIENTE"]},
                                     OUTPUT_DEPENDENCIES_VALUE : {"CustomerPerson" : []},
                                     ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "clientes",
                                                        JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "CLIENTE"},
                                                        RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE : ["customer_code"],
                                                        OUTPUT_ENTITY_NAMES_VALUE : ["CustomerPerson"]}}

        # defines how to populate the customer return entities' customer relation attribute
        customer_return_customer_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["customer"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["returns_customer"],
                                             CONNECTORS_VALUE : [customer_person_connector]}

        # connector used to populate the return sites relation attribute
        return_sites_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                  INPUT_DEPENDENCIES_VALUE : {"lojas" : ["CODIGO"],
                                                              "vendas" : ["LOJA"]},
                                  OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                                  ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "lojas",
                                                     JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "LOJA"},
                                                     OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # defines how to populate the customer return entities' return sites relation attribute
        customer_return_return_sites_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["return_sites"],
                                                 RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["customer_returns"],
                                                 CONNECTORS_VALUE : [return_sites_connector]}

        # connector used to populate the original sale relation attribute
        original_sale_invoice_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_input_entity",
                                           INPUT_DEPENDENCIES_VALUE : {"extrdoc" : ["DOCUMENTO", "DOCVINDODE", "TIPODOC", "NUMVINDODE"],
                                                                       "vendas" : ["DOCUMENTO", "TIPODOC"]},
                                           ARGUMENTS_VALUE : {JOINS_VALUE : [["extrdoc", {"DOCUMENTO" : ["DOCUMENTO", CREATOR],
                                                                                          "DOCVINDODE" : DIAMANTE_INVOICE_DOCUMENT_TYPE,
                                                                                          "TIPODOC" : DIAMANTE_CREDIT_NOTE_DOCUMENT_TYPE}],
                                                                             ["vendas", {"DOCUMENTO" : ["NUMVINDODE", "extrdoc"],
                                                                                         "TIPODOC" : DIAMANTE_INVOICE_DOCUMENT_TYPE}]],
                                                              OUTPUT_ENTITY_NAMES_VALUE : ["SaleTransaction"]}}

        # connector used to populate the original sale relation attribute
        original_sale_money_sale_slip_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_input_entity",
                                                   INPUT_DEPENDENCIES_VALUE : {"extrdoc" : ["DOCUMENTO", "DOCVINDODE", "TIPODOC", "NUMVINDODE"],
                                                                               "vendas" : ["DOCUMENTO", "TIPODOC"]},
                                                   ARGUMENTS_VALUE : {JOINS_VALUE : [["extrdoc", {"DOCUMENTO" : ["DOCUMENTO", CREATOR],
                                                                                                  "DOCVINDODE" : DIAMANTE_MONEY_SALE_SLIP_DOCUMENT_TYPE,
                                                                                                  "TIPODOC" : DIAMANTE_CREDIT_NOTE_DOCUMENT_TYPE}],
                                                                                     ["vendas", {"DOCUMENTO" : ["NUMVINDODE", "extrdoc"],
                                                                                                 "TIPODOC" : DIAMANTE_MONEY_SALE_SLIP_DOCUMENT_TYPE}]],
                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["SaleTransaction"]}}

        # defines how to populate the customer return's original sale relation attribute
        customer_return_original_sale_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["original_sale"],
                                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["customer_returns"],
                                                  CONNECTORS_VALUE : [original_sale_invoice_connector,
                                                                      original_sale_money_sale_slip_connector]}

        # defines how to connect customer return to other entities
        self.relation_mapping_entities = [{NAME_VALUE : "CustomerReturn",
                                           RELATIONS_VALUE : [customer_return_credit_note_relation,
                                                              customer_return_customer_relation,
                                                              customer_return_return_sites_relation,
                                                              customer_return_original_sale_relation]}]
