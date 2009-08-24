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
import datetime

ATTRIBUTES_VALUE = "attributes"

ATTRIBUTE_NAMES_VALUE = "attribute_names"

EXCLUSION_LIST_VALUE = "exclusion_list"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

VAT_RATE_21 = 0.21
""" The 21% vat rate """

VAT_RATE_20 = 0.20
""" The 20% vat rate """

VAT_RATE_20_START_DATE = (2008, 07, 01)
""" Date when the 20% vat rate started being used """

PURCHASE_TRANSACTION_DOCUMENT_TYPES = ["V/D", "FAC", "G/C"]
""" List with the types of documents that correspond to the purchase transactions in diamante """

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

class PurchaseTransactionConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni PurchaseTransaction entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract purchase transaction entities from compras entities
        compras_input_entities = {NAME_VALUE : "compras",
                                  OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values_in_list",
                                                                                 INPUT_DEPENDENCIES_VALUE : {"compras" : ["TIPODOC"]},
                                                                                 ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : PURCHASE_TRANSACTION_DOCUMENT_TYPES}}}],
                                                            OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "date",
                                                                                        ATTRIBUTE_NAME_VALUE : "DATA"},
                                                                                       {NAME_VALUE : "discount",
                                                                                        ATTRIBUTE_NAME_VALUE : "TOTDESCVAL",
                                                                                        HANDLERS_VALUE :[{FUNCTION_VALUE : self.attribute_handler_calculate_discount,
                                                                                                          INPUT_DEPENDENCIES_VALUE : {"compras" : ["DATA"]}}]},
                                                                                       {NAME_VALUE : "discount_vat",
                                                                                        ATTRIBUTE_NAME_VALUE : "TOTDESCVAL"},
                                                                                       {NAME_VALUE : "cost",
                                                                                        DEFAULT_VALUE_VALUE : 0},
                                                                                       {NAME_VALUE : "vat",
                                                                                        DEFAULT_VALUE_VALUE : 0},
                                                                                       {NAME_VALUE : "observations",
                                                                                        ATTRIBUTE_NAME_VALUE : "APONTAMENT",
                                                                                        HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                           EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}]}]}]}

        # defines how to extract purchase transaction entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "PurchaseTransaction",
                                                   INPUT_ENTITIES_VALUE : [compras_input_entities]}]

        # connector used to populate the supplier relation attribute
        supplier_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                              INPUT_DEPENDENCIES_VALUE : {"forneced" : ["CODIGO"],
                                                          "compras" : ["FORNECEDOR"]},
                              OUTPUT_DEPENDENCIES_VALUE : {"SupplierCompany" : []},
                              ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "forneced",
                                                 JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "FORNECEDOR"},
                                                 OUTPUT_ENTITY_NAMES_VALUE : ["SupplierCompany"]}}

        # define how to populate the purchase transaction entities' supplier relation attribute
        purchase_transaction_supplier_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplier"],
                                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["purchases_supplier"],
                                                  CONNECTORS_VALUE : [supplier_connector]}

        # defines how to connect the extracted purchase transaction entities to other entities
        self.relation_mapping_entities = [{NAME_VALUE : "PurchaseTransaction",
                                           RELATIONS_VALUE : [purchase_transaction_supplier_relation]}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_calculate_prices_vats,
                                          INPUT_DEPENDENCIES_VALUE : {"anacompr" : ["PRCTOTCIVA", "QUANTIDADE"],
                                                                      "sbcompra" : ["CUSTO", "STOCK"]},
                                          OUTPUT_DEPENDENCIES_VALUE : {"SaleMerchandiseHierarchyTreeNode" : []}},
                                         {FUNCTION_VALUE : self.post_conversion_handler_set_delivery_billing_site,
                                          INPUT_DEPENDENCIES_VALUE : {"anacompr" : ["LOJA"],
                                                                      "lojas" : ["CODIGO"]}}]

    def attribute_handler_calculate_discount(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the discount vat and the date
        totdescval = input_entity.get_attribute("TOTDESCVAL")
        data = input_entity.get_attribute("DATA")

        # calculates the purchase transaction's vat rate
        vat_rate = VAT_RATE_21
        if data and data >= apply(datetime.datetime, VAT_RATE_20_START_DATE):
            vat_rate = VAT_RATE_20

        # calculates the discount without vat
        output_attribute_value = float(totdescval) / float((1 + vat_rate))

        return output_attribute_value

    def post_conversion_handler_set_delivery_billing_site(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_plugin.info("Associating purchase transactions with billing and delivery site")

        # extracts the billing and delivery sites from the creators of the purchase line entities
        purchase_transaction_entities = output_intermediate_structure.get_entities_by_name("PurchaseTransaction")
        for purchase_transaction_entity in purchase_transaction_entities:

            # retrieves the creator input entity for the purchase transaction's first purchase line
            purchase_line_entities = purchase_transaction_entity.get_attribute("purchase_lines")

            # @todo: this is a hack
            if not purchase_line_entities:
                continue

            # retrieves the first purchase line
            purchase_line_entity = purchase_line_entities[0]

            # retrieves the purchase line's creator input entity
            purchase_line_object_id = purchase_line_entity.get_object_id()
            purchase_line_creator_input_entity_index = (INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, purchase_line_object_id)
            purchase_line_creator_input_entity = input_intermediate_structure.get_entities_by_index(purchase_line_creator_input_entity_index)[0]

            # retrieves the lojas input entity indicated by the purchase line entity's creator input entity
            loja = purchase_line_creator_input_entity.get_attribute("LOJA")
            lojas_input_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "lojas", AND_VALUE, "CODIGO", EQUALS_VALUE, loja)
            lojas_input_entities = input_intermediate_structure.get_entities_by_index(lojas_input_entity_index)
            lojas_input_entity = lojas_input_entities[0]

            # retrieves the store entity created from the previously retrieved lojas input entity
            lojas_input_entity_object_id = lojas_input_entity.get_object_id()
            created_output_entities_index = (OUTPUT_ENTITY_VALUE, WHERE_VALUE, INPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, lojas_input_entity_object_id, CREATED_VALUE, OUTPUT_ENTITY_NAME_VALUE, EQUALS_VALUE, "Store")
            store_entities = output_intermediate_structure.get_entities_by_index(created_output_entities_index)

            # @todo: this is a hack
            if not store_entities:
                continue

            store_entity = store_entities[0]

            # sets the retrieved store entity as the billing and delivery site for this purchase transaction
            purchase_transaction_entity.set_attribute("billing_site", store_entity)
            purchase_transaction_entity.set_attribute("delivery_site", store_entity)

        return output_intermediate_structure

    def post_conversion_handler_calculate_prices_vats(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_plugin.info("Calculating purchase prices and vats")

        # calculates each purchase transaction's price and vat while calculating its purchase line's unit price, vat and vat rate
        purchase_transaction_entities = output_intermediate_structure.get_entities_by_name("PurchaseTransaction")
        for purchase_transaction_entity in purchase_transaction_entities:
            cost = 0
            vat = 0

            # calculates the purchase transaction's vat rate
            vat_rate = VAT_RATE_21
            date = purchase_transaction_entity.get_attribute("date")
            if date and date >= apply(datetime.datetime, VAT_RATE_20_START_DATE):
                vat_rate = VAT_RATE_20

            # calculates the unit cost and vat for each purchase line
            purchase_line_entities = purchase_transaction_entity.get_attribute("purchase_lines")
            for purchase_line_entity in purchase_line_entities:

                # retrieves the purchase line's creator input entity
                purchase_line_entity_object_id = purchase_line_entity.get_object_id()
                creator_input_entity = self.get_creator_input_entity(input_intermediate_structure, purchase_line_entity_object_id)

                # calculates the purchase line's unit cost and unit vat
                if creator_input_entity.get_name() == "anacompr":
                    prctotciva = creator_input_entity.get_attribute("PRCTOTCIVA")
                    quantidade = creator_input_entity.get_attribute("QUANTIDADE")
                    unit_cost = float(prctotciva) / float(quantidade) / float((1 + vat_rate))
                    unit_vat = unit_cost * vat_rate
                elif creator_input_entity.get_name() == "sbcompra":
                    custo = creator_input_entity.get_attribute("CUSTO")
                    stock = creator_input_entity.get_attribute("STOCK")
                    unit_cost = float(custo) / float(stock) / float((1 + vat_rate))
                    unit_vat = unit_cost * vat_rate

                # sets the vat rate, unit cost and unit vat in the purchase line
                purchase_line_entity.set_attribute("vat_rate", vat_rate)
                purchase_line_entity.set_attribute("unit_cost", unit_cost)
                purchase_line_entity.set_attribute("unit_vat", unit_vat)

                # accumulates the purchase line's value to calculate the purchase transaction's totals
                cost += unit_cost * quantidade
                vat += unit_vat * quantidade

            # sets the purchase transaction's total cost and vat
            purchase_transaction_entity.set_attribute("cost", cost)
            purchase_transaction_entity.set_attribute("vat", vat)

        return output_intermediate_structure

    def get_creator_input_entity(self, input_intermediate_structure, output_entity_object_id):
        # retrieves the creator input entity for the output entity with the specified object id
        input_entity_index = (INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, output_entity_object_id)
        input_entities = input_intermediate_structure.get_entities_by_index(input_entity_index)

        # returns in case no input entity or more than one input entity is found
        if not len(input_entities) == 1:
            return None

        input_entity = input_entities[0]

        return input_entity
