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

ATTRIBUTE_NAMES_VALUE = "attribute_names"

EXCLUSION_LIST_VALUE = "exclusion_list"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

JOINS_VALUE = "joins"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

CREATOR = "%creator%"
""" Value used to identify a creator input entity """

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

DIAMANTE_MONEY_SALE_SLIP_DOCUMENT_TYPE = "V/D"
""" The money sale slip document type in diamante """

DIAMANTE_INVOICE_DOCUMENT_TYPE = "FAC"
""" The invoice document type in diamante """

DIAMANTE_CREDIT_NOTE_DOCUMENT_TYPE = "NCR"
""" The credit note document type in diamante """

DIAMANTE_RECEIPT_DOCUMENT_TYPE = "REC"
""" The receipt document type in diamante """

DIAMANTE_RETURN_TO_VENDOR_SLIP_DOCUMENT_TYPE = "DEV"
""" The return to vendor slip document type in diamante """

class SupplierReturnConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni SupplierReturn entities from diamante.
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
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["compras"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"compras" : ["DOCUMENTO", "FORNECEDOR", "TIPODOC"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "FORNECEDOR", "TIPODOC"]}},
                                      {ENTITY_NAMES_VALUE : ["extrdocc"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"extrdocc" : ["DOCUMENTO", "DOCVINDODE", "FORNECEDOR", "TIPODOC"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "DOCVINDODE", "FORNECEDOR", "TIPODOC"]}}]

        # defines how to extract supplier return entities from devolver entities
        devolver_input_entities = {NAME_VALUE : "devolver",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : self.entity_validator_is_supplier_return,
                                                                                  INPUT_DEPENDENCIES_VALUE : {"devolver" : ["DOCUMENTO", "FORNECEDOR"]}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "date",
                                                                                         ATTRIBUTE_NAME_VALUE : "DATA"},
                                                                                        {NAME_VALUE : "description",
                                                                                         ATTRIBUTE_NAME_VALUE : "APONTAMENT",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                            EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}]}]}]}

        # defines how to extract supplier return entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "SupplierReturn",
                                                   INPUT_ENTITIES_VALUE : [devolver_input_entities]}]

        # connector used to populate the supplier relation attribute
        supplier_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                              INPUT_DEPENDENCIES_VALUE : {"forneced" : ["CODIGO"],
                                                          "devolver" : ["FORNECEDOR"]},
                              OUTPUT_DEPENDENCIES_VALUE : {"SupplierCompany" : []},
                              ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "forneced",
                                                 JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "FORNECEDOR"},
                                                 OUTPUT_ENTITY_NAMES_VALUE : ["SupplierCompany"]}}

        # defines how to populate the supplier return entities' supplier relation attribute
        supplier_return_supplier_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplier"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplier_returns"],
                                             CONNECTORS_VALUE :  [supplier_connector]}

        # connector used to populate the return to vendor slip relation attribute
        return_to_vendor_slip_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                           OUTPUT_DEPENDENCIES_VALUE : {"ReturnToVendorSlip" : []},
                                           ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["ReturnToVendorSlip"]}}

        # defines how to populate the supplier return entities' return to vendor slip relation attribute
        supplier_return_return_to_vendor_slip_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["return_to_vendor_slip"],
                                                          RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplier_return"],
                                                          CONNECTORS_VALUE :  [return_to_vendor_slip_connector]}

        # connector used to populate the original purchase transaction relation attribute
        original_purchase_transaction_credit_note_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_input_entity",
                                                               INPUT_DEPENDENCIES_VALUE : {"extrdocc" : ["DOCUMENTO", "DOCVINDODE", "TIPODOC", "NUMVINDODE", "FORNECEDOR"],
                                                                                           "compras" : ["DOCUMENTO", "TIPODOC", "FORNECEDOR"]},
                                                               ARGUMENTS_VALUE : {JOINS_VALUE : [["extrdocc", {"DOCUMENTO" : ["DOCUMENTO", CREATOR],
                                                                                                               "DOCVINDODE" : DIAMANTE_INVOICE_DOCUMENT_TYPE,
                                                                                                               "TIPODOC" : DIAMANTE_RETURN_TO_VENDOR_SLIP_DOCUMENT_TYPE,
                                                                                                               "FORNECEDOR" : ["FORNECEDOR", CREATOR]}],
                                                                                                 ["compras", {"DOCUMENTO" : ["NUMVINDODE", "extrdocc"],
                                                                                                              "TIPODOC" : DIAMANTE_INVOICE_DOCUMENT_TYPE,
                                                                                                              "FORNECEDOR" : ["FORNECEDOR", CREATOR]}]],
                                                                                  OUTPUT_ENTITY_NAMES_VALUE : ["PurchaseTransaction"]}}

        # defines how to populate the supplier return's original purchase transaction relation attribute
        supplier_return_original_purchase_transaction_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["original_purchase_transaction"],
                                                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplier_returns"],
                                                                  CONNECTORS_VALUE : [original_purchase_transaction_credit_note_connector]}

        # defines how to connect supplier return to other entities
        self.relation_mapping_entities = [{NAME_VALUE : "SupplierReturn",
                                           RELATIONS_VALUE : [supplier_return_supplier_relation,
                                                              supplier_return_return_to_vendor_slip_relation,
                                                              supplier_return_original_purchase_transaction_relation]}]

    def entity_validator_is_supplier_return(self, data_converter, input_intermediate_structure, input_entity, arguments):
        # indicates if the entity represents a supplier return

        documento = input_entity.get_attribute("DOCUMENTO")
        fornecedor = input_entity.get_attribute("FORNECEDOR")

        extrdocc_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "extrdocc",
                                 AND_VALUE, "DOCUMENTO", EQUALS_VALUE, documento,
                                 AND_VALUE, "DOCVINDODE", EQUALS_VALUE, DIAMANTE_INVOICE_DOCUMENT_TYPE,
                                 AND_VALUE, "FORNECEDOR", EQUALS_VALUE, fornecedor,
                                 AND_VALUE, "TIPODOC", EQUALS_VALUE, DIAMANTE_RETURN_TO_VENDOR_SLIP_DOCUMENT_TYPE)

        entities = input_intermediate_structure.get_entities_by_index(extrdocc_entity_index)

        return len(entities) == 1
