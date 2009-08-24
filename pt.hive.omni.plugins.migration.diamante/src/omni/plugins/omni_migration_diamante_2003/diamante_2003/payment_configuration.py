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

ATTRIBUTES_VALUE = "attributes"

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

PAYMENT_DOCUMENT_TYPES = ["V/D", "FAC"]
""" List with the types of documents that correspond to the payments in diamante """

class PaymentConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Payment entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract payment entities from vendas entities
        vendas_input_entities = {NAME_VALUE : "vendas",
                                 OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values_in_list",
                                                                                INPUT_DEPENDENCIES_VALUE : {"vendas" : ["TIPODOC"]},
                                                                                ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : PAYMENT_DOCUMENT_TYPES}}}],
                                                           OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "date",
                                                                                       ATTRIBUTE_NAME_VALUE : "DATA",
                                                                                       HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_add_hours,
                                                                                                          INPUT_DEPENDENCIES_VALUE : {"vendas" : ["HORAS"]}}]}]}]}

        # defines how to extract payment entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Payment",
                                                   INPUT_ENTITIES_VALUE : [vendas_input_entities]}]

        # connector used to populate the money sale slip relation attribute
        money_sale_slip_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                     OUTPUT_DEPENDENCIES_VALUE : {"MoneySaleSlip" : []},
                                     ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["MoneySaleSlip"]}}

        # defines how to populate the payment entities' money sale slip relation attribute
        payment_money_sale_slip_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["money_sale_slip"],
                                            RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payment"],
                                            CONNECTORS_VALUE :  [money_sale_slip_connector]}

        # connector used to populate the payment receiver relation attribute
        payment_receiver_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                      INPUT_DEPENDENCIES_VALUE : {"vendas" : ["VENDEDOR"],
                                                                  "vendedor" : ["CODIGO"]},
                                      OUTPUT_DEPENDENCIES_VALUE : {"Employee" : []},
                                      ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "vendedor",
                                                         JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "VENDEDOR"},
                                                         OUTPUT_ENTITY_NAMES_VALUE : ["Employee"]}}

        # defines how to populate the payment entities' payment receiver relation attribute
        payment_payment_receiver_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payment_receiver"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["payments_received"],
                                             CONNECTORS_VALUE : [payment_receiver_connector]}

        # defines how to connect the extracted payment entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "Payment",
                                           RELATIONS_VALUE : [payment_money_sale_slip_relation,
                                                              payment_payment_receiver_relation]}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_calculate_totals",
                                          OUTPUT_DEPENDENCIES_VALUE : {"PaymentPaymentMethod" : ["amount"]},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {("Payment", "payment_lines") : {"amount" : "amount"}}}}]

    def attribute_handler_add_hours(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # adds the hours to the sale transaction date

        # parses the horas input attribute
        horas = input_entity.get_attribute("HORAS")
        hours_token, minutes_token = horas.split(":")

        # adds the hours and minutes to the current date
        date = output_attribute_value
        output_attribute_value = datetime.datetime(date.year, date.month, date.day, int(hours_token), int(minutes_token), 0, 0)

        return output_attribute_value
