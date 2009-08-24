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

import datetime
import types

ATTRIBUTES_VALUE = "attributes"

EXCLUSION_LIST_VALUE = "exclusion_list"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ATTRIBUTE_NAMES_VALUE = "output_attribute_names"

RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "related_entity_non_null_attribute_names"

SEPARATOR_VALUE = "separator"

NEWLINE_CHARACTER = "\n"
""" The newline character in python """

VAT_RATE_21 = 0.21
""" The 21% vat rate """

VAT_RATE_20 = 0.20
""" The 20% vat rate """

VAT_RATE_20_START_DATE = (2008, 07, 01)
""" Date when the 20% vat rate started being used """

VENDAS_ENTITY_OBSERVATION_ATTRIBUTE_NAMES = ["APONTAMENT", "CLINOME", "CLIMORADA", "CLICONTRIB", "CLILOCALI"]
""" List with the name of the attributes where to extract observations from a vendas entity """

SALE_TRANSACTION_DOCUMENT_TYPES = ["V/D", "FAC", "G/C"]
""" List with the types of documents that correspond to the sale transactions in diamante """

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

class SaleTransactionConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni SaleTransaction entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract sale transaction entities from vendas entities
        vendas_input_entities = {NAME_VALUE : "vendas",
                                 OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values_in_list",
                                                                                INPUT_DEPENDENCIES_VALUE : {"vendas" : ["TIPODOC"]},
                                                                                ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : SALE_TRANSACTION_DOCUMENT_TYPES}}}],
                                                           HANDLERS_VALUE : [ # merges observations from various fields into one
                                                                              {FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                               INPUT_DEPENDENCIES_VALUE : {"vendas" : VENDAS_ENTITY_OBSERVATION_ATTRIBUTE_NAMES},
                                                                               ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : VENDAS_ENTITY_OBSERVATION_ATTRIBUTE_NAMES,
                                                                                                  SEPARATOR_VALUE : NEWLINE_CHARACTER,
                                                                                                  OUTPUT_ATTRIBUTE_NAME_VALUE : "observations"}},
                                                                               # capitalizes each letter in the merged observations
                                                                              {FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                               ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["observations"],
                                                                                                  EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                           OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "date",
                                                                                       ATTRIBUTE_NAME_VALUE : "DATA",
                                                                                       HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_add_hours,
                                                                                                          INPUT_DEPENDENCIES_VALUE : {"vendas" : ["HORAS"]}}]},
                                                                                      {NAME_VALUE : "discount",
                                                                                       ATTRIBUTE_NAME_VALUE : "TOTDESCVAL",
                                                                                       HANDLERS_VALUE :[{FUNCTION_VALUE : self.attribute_handler_calculate_discount,
                                                                                                         INPUT_DEPENDENCIES_VALUE : {"vendas" : ["DATA"]}}]},
                                                                                      {NAME_VALUE : "discount_vat",
                                                                                       ATTRIBUTE_NAME_VALUE : "TOTDESCVAL"},
                                                                                      {NAME_VALUE : "price",
                                                                                       DEFAULT_VALUE_VALUE : 0},
                                                                                      {NAME_VALUE : "vat",
                                                                                       DEFAULT_VALUE_VALUE : 0}]}]}

        # defines how to extract sale transaction entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "SaleTransaction",
                                                   INPUT_ENTITIES_VALUE : [vendas_input_entities]}]

        # connector used to populate the sellers relation attribute
        sellers_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                             INPUT_DEPENDENCIES_VALUE : {"vendedor" : ["CODIGO"],
                                                         "vendas" : ["VENDEDOR"]},
                             OUTPUT_DEPENDENCIES_VALUE : {"Employee" : []},
                             ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "vendedor",
                                                JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "VENDEDOR"},
                                                OUTPUT_ENTITY_NAMES_VALUE : ["Employee"]}}

        # defines how to populate the sale transaction entities' sellers relation attribute
        sale_transaction_sellers_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sellers"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sales_seller"],
                                             CONNECTORS_VALUE : [sellers_connector]}

        # connector used to populate the person buyer relation attribute
        person_buyer_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                  INPUT_DEPENDENCIES_VALUE : {"clientes" : ["CODIGO"],
                                                              "vendas" : ["CLIENTE"]},
                                  OUTPUT_DEPENDENCIES_VALUE : {"CustomerPerson" : []},
                                  ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "clientes",
                                                     JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "CLIENTE"},
                                                     RELATED_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE : ["customer_code"],
                                                     OUTPUT_ENTITY_NAMES_VALUE : ["CustomerPerson"]}}

        # defines how to populate the sale transaction entities' person buyer relation attribute
        sale_transaction_person_buyer_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["person_buyer"],
                                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sales"],
                                                  CONNECTORS_VALUE : [person_buyer_connector]}

        # connector used to populate the company buyer relation attribute
        company_buyer_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                   INPUT_DEPENDENCIES_VALUE : {"clientes" : ["CODIGO"],
                                                               "vendas" : ["CLIENTE"]},
                                   OUTPUT_DEPENDENCIES_VALUE : {"CustomerCompany" : []},
                                   ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "clientes",
                                                      JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "CLIENTE"},
                                                      OUTPUT_ENTITY_NAMES_VALUE : ["CustomerCompany"]}}

        # defines how to populate the sale transaction entities' company buyer relation attribute
        sale_transaction_company_buyer_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["company_buyer"],
                                                   RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sales"],
                                                   CONNECTORS_VALUE : [company_buyer_connector]}

        # connector used to populate the seller stockholder relation attribute
        seller_stockholder_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                        INPUT_DEPENDENCIES_VALUE : {"lojas" : ["CODIGO"],
                                                                    "vendas" : ["LOJA"]},
                                        OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                                        ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "lojas",
                                                           JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "LOJA"},
                                                           OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # defines how to populate the sale transaction entities' store relation attribute
        sale_transaction_seller_stockholder_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["seller_stockholder"],
                                                        RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sales_stockholder"],
                                                        CONNECTORS_VALUE : [seller_stockholder_connector]}

        # connector used to populate the invoice relation attribute
        invoice_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                             OUTPUT_DEPENDENCIES_VALUE : {"Invoice" : []},
                             ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Invoice"]}}

        # defines how to populate the sale transaction entities' invoice relation attribute
        sale_transaction_invoice_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["invoice"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sale_transaction"],
                                             CONNECTORS_VALUE : [invoice_connector]}

        # connector used to populate the money sale slip relation attribute
        money_sale_slip_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                     OUTPUT_DEPENDENCIES_VALUE : {"MoneySaleSlip" : []},
                                     ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["MoneySaleSlip"]}}

        # defines how to populate the sale transaction entities' money sale slip relation attribute
        sale_transaction_money_sale_slip_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["money_sale_slip"],
                                                     RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sale_transaction"],
                                                     CONNECTORS_VALUE :  [money_sale_slip_connector]}

        # connector used to populate the payment relation attribute
        payment_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                             OUTPUT_DEPENDENCIES_VALUE : {"Payment" : []},
                             ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Payment"]}}

        # defines how to populate the sale transaction entities' payments relation attribute
        sale_transaction_payment_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payments"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sales"],
                                             CONNECTORS_VALUE : [payment_connector]}

        # defines how to connect the extracted customer person entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "SaleTransaction",
                                           RELATIONS_VALUE : [sale_transaction_sellers_relation,
                                                              sale_transaction_person_buyer_relation,
                                                              sale_transaction_company_buyer_relation,
                                                              sale_transaction_seller_stockholder_relation,
                                                              sale_transaction_invoice_relation,
                                                              sale_transaction_money_sale_slip_relation,
                                                              sale_transaction_payment_relation]}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_calculate_prices_vats,
                                          INPUT_DEPENDENCIES_VALUE : {"anavenda" : ["PRCTOTCIVA", "QUANTIDADE"]},
                                          OUTPUT_DEPENDENCIES_VALUE : {"SaleMerchandiseHierarchyTreeNode" : []}}]

    def attribute_handler_add_hours(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # adds the hours to the sale transaction date

        # parses the horas input attribute
        horas = input_entity.get_attribute("HORAS")
        hours_token, minutes_token = horas.split(":")

        # adds the hours and minutes to the current date
        date = output_attribute_value
        output_attribute_value = datetime.datetime(date.year, date.month, date.day, int(hours_token), int(minutes_token), 0, 0)

        return output_attribute_value

    def attribute_handler_calculate_discount(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the discount vat and the date
        totdescval = input_entity.get_attribute("TOTDESCVAL")
        data = input_entity.get_attribute("DATA")

        # calculates the sale transaction's vat rate
        vat_rate = VAT_RATE_21
        if data >= apply(datetime.datetime, VAT_RATE_20_START_DATE):
            vat_rate = VAT_RATE_20

        # calculates the discount without vat
        output_attribute_value = float(totdescval) / float((1 + vat_rate))

        return output_attribute_value

    def post_conversion_handler_calculate_prices_vats(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_plugin.info("Calculating sale prices and vats")

        # calculates each sale transaction's price and vat while calculating its sale line's unit price, vat and vat rate
        sale_transaction_entities = output_intermediate_structure.get_entities_by_name("SaleTransaction")
        for sale_transaction_entity in sale_transaction_entities:
            price = 0
            vat = 0

            # calculates the sale transaction's vat rate
            date = sale_transaction_entity.get_attribute("date")
            vat_rate = VAT_RATE_21
            if date >= apply(datetime.datetime, VAT_RATE_20_START_DATE):
                vat_rate = VAT_RATE_20

            # calculates the unit price and vat for each sale line
            sale_line_entities = sale_transaction_entity.get_attribute("sale_lines")
            for sale_line_entity in sale_line_entities:

                # retrieves the sale line's creator input entity
                sale_line_entity_object_id = sale_line_entity.get_object_id()
                creator_input_entity = self.get_creator_input_entity(input_intermediate_structure, sale_line_entity_object_id)

                # calculates the sale line's unit price and unit vat
                prctotciva = creator_input_entity.get_attribute("PRCTOTCIVA")
                quantidade = creator_input_entity.get_attribute("QUANTIDADE")
                unit_price = float(prctotciva) / float(quantidade) / float((1 + vat_rate))
                unit_vat = unit_price * vat_rate

                # sets the vat rate, unit price and unit vat in the sale line
                sale_line_entity.set_attribute("vat_rate", vat_rate)
                sale_line_entity.set_attribute("unit_price", unit_price)
                sale_line_entity.set_attribute("unit_vat", unit_vat)

                # accumulates the sale line's value to calculate the sale transaction's totals
                price += unit_price * quantidade
                vat += unit_vat * quantidade

            # sets the sale transaction's total price and vat
            sale_transaction_entity.set_attribute("price", price)
            sale_transaction_entity.set_attribute("vat", vat)

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
