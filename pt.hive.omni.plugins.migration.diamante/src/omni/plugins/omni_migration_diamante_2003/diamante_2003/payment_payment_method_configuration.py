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

import types

ATTRIBUTES_VALUE = "attributes"

ATTRIBUTE_NAMES_VALUE = "attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

PAYMENT_DOCUMENT_TYPES = ["V/D", "FAC"]
""" List with the types of documents that correspond to the payments in diamante """

class PaymentPaymentMethodConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni PaymentPaymentMethod entities from diamante.
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
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "TIPODOC"]}}]

        # defines how to extract payment payment method entities from fpvendas entities
        fpvendas_input_entities = {NAME_VALUE : "fpvendas",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values_in_list",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"fpvendas" : ["TIPODOC"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : PAYMENT_DOCUMENT_TYPES}}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "amount",
                                                                                         ATTRIBUTE_NAME_VALUE : "VALOR"}]}]}

        # defines how to extract payment payment method entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "PaymentPaymentMethod",
                                                   INPUT_ENTITIES_VALUE : [fpvendas_input_entities]}]

        # connector used to populate the payment method relation attribute
        payment_method_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                    OUTPUT_DEPENDENCIES_VALUE : {"CashPayment" : [],
                                                                 "CheckPayment" : [],
                                                                 "CardPayment" : [],
                                                                 "CreditNotePayment" : [],
                                                                 "PostDatedCheckPayment" : [],
                                                                 "GiftCertificatePayment" : [],
                                                                 "InvalidPayment" : []},
                                    ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["CashPayment",
                                                                                    "CheckPayment",
                                                                                    "CardPayment",
                                                                                    "CreditNotePayment",
                                                                                    "PostDatedCheckPayment",
                                                                                    "GiftCertificatePayment",
                                                                                    "InvalidPayment"]}}

        # defines how to populate the payment payment method entities' payment method relation attribute
        payment_payment_method_payment_method_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payment_method"],
                                                          RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payment_lines"],
                                                          CONNECTORS_VALUE : [payment_method_connector]}

        # connector used to populate the payment relation attribute
        payment_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                             INPUT_DEPENDENCIES_VALUE : {"vendas" : ["TIPODOC", "DOCUMENTO"],
                                                         "fpvendas" : ["TIPODOC", "VENDA"]},
                             OUTPUT_DEPENDENCIES_VALUE : {"Payment" : []},
                             ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "vendas",
                                                JOIN_ATTRIBUTES_VALUE : {"TIPODOC" : "TIPODOC",
                                                                         "DOCUMENTO" : "VENDA"},
                                                OUTPUT_ENTITY_NAMES_VALUE : ["Payment"]}}

        # defines how to populate the payment payment method entities' relation attribute
        payment_payment_method_payment_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payment"],
                                                   RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payment_lines"],
                                                   CONNECTORS_VALUE : [payment_connector]}

        # defines how to connect the extracted payment payment method entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "PaymentPaymentMethod",
                                           RELATIONS_VALUE : [payment_payment_method_payment_method_relation,
                                                              payment_payment_method_payment_relation]}]
