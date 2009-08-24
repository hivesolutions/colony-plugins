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

CREATOR_ENTITY_NAMES_VALUE = "creator_entity_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE = "G/C"
""" The consignment slip document type indicator in diamante """

class ConsignmentConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Consignment entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract consignment entities from compras entities
        compras_input_entities = {NAME_VALUE : "compras",
                                  OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                 INPUT_DEPENDENCIES_VALUE : {"compras" : ["TIPODOC"]},
                                                                                 ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE}}}],
                                                            OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "identifier",
                                                                                        ATTRIBUTE_NAME_VALUE : "DOCUMENTO"}]}]}

        # defines how to extract consignment entities from vendas entities
        vendas_input_entities = {NAME_VALUE : "vendas",
                                 OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                INPUT_DEPENDENCIES_VALUE : {"vendas" : ["TIPODOC"]},
                                                                                ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE}}}],
                                                           OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "identifier",
                                                                                       ATTRIBUTE_NAME_VALUE : "DOCUMENTO"}]}]}

        # defines how to extract consignment entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Consignment",
                                                   INPUT_ENTITIES_VALUE : [compras_input_entities,
                                                                           vendas_input_entities]}]

        # connector used to populate the consignment slip relation attribute
        consignment_slip_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                      OUTPUT_DEPENDENCIES_VALUE : ["ConsignmentSlip"],
                                      ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["ConsignmentSlip"]}}

        # defines how to connect consignment entities to consignment slip entities
        consignment_consignment_slip_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["consignment_slip"],
                                                 RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["consignment"],
                                                 CONNECTORS_VALUE :  [consignment_slip_connector]}

        # connector used to populate the consignments supplier relation attribute
        compras_consignments_supplier_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                   INPUT_DEPENDENCIES_VALUE : {"forneced" : ["CODIGO"],
                                                                               "compras" : ["FORNECEDOR"]},
                                                   OUTPUT_DEPENDENCIES_VALUE : ["SupplierCompany"],
                                                   ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "forneced",
                                                                      CREATOR_ENTITY_NAMES_VALUE : ["compras"],
                                                                      JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "FORNECEDOR"},
                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["SupplierCompany"]}}

        # connector used to populate the consignments supplier relation attribute
        vendas_consignments_supplier_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                  INPUT_DEPENDENCIES_VALUE : {"lojas" : ["CODIGO"],
                                                                              "vendas" : ["LOJA"]},
                                                  OUTPUT_DEPENDENCIES_VALUE : ["SupplierCompany"],
                                                  ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "lojas",
                                                                     CREATOR_ENTITY_NAMES_VALUE : ["vendas"],
                                                                     JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "LOJA"},
                                                                     OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # defines how to connect the consignment entities to supplier company entities
        consignment_consignments_supplier_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplier"],
                                                      RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["consignments_supplier"],
                                                      CONNECTORS_VALUE :  [compras_consignments_supplier_connector,
                                                                           vendas_consignments_supplier_connector]}

        # connector used to populate the purchase transactions relation attribute
        purchase_transactions_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                           ARGUMENTS_VALUE : {CREATOR_ENTITY_NAMES_VALUE : ["compras"],
                                                              OUTPUT_ENTITY_NAMES_VALUE : ["PurchaseTransaction"]}}

        # defines how to connect the consignment entities to purchase transaction entities
        consignment_purchase_transactions_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["purchase_transactions"],
                                                      RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["consignment"],
                                                      CONNECTORS_VALUE :  [purchase_transactions_connector]}

        # connector used to populate the sale transactions relation attribute
        sale_transactions_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                       ARGUMENTS_VALUE : {CREATOR_ENTITY_NAMES_VALUE : ["vendas"],
                                                          OUTPUT_ENTITY_NAMES_VALUE : ["SaleTransaction"]}}

        # defines how to connect the consignment entities to sale transaction entities
        consignment_sale_transactions_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sale_transactions"],
                                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["consignment"],
                                                  CONNECTORS_VALUE : [sale_transactions_connector]}

        # defines how to connect the extracted consignment entities to other entities
        self.relation_mapping_entities = [{NAME_VALUE : "Consignment",
                                           RELATIONS_VALUE : [consignment_consignment_slip_relation,
                                                              consignment_consignments_supplier_relation,
                                                              consignment_sale_transactions_relation,
                                                              consignment_purchase_transactions_relation]}]
