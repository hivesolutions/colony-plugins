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

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

class StockAdjustmentConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni StockAdjustment entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract stock adjustment entities from stkprore entities
        stkprore_input_entities = {NAME_VALUE : "stkprore",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "date",
                                                                                         ATTRIBUTE_NAME_VALUE : "DATA"},
                                                                                        {NAME_VALUE : "identifier",
                                                                                         ATTRIBUTE_NAME_VALUE : "DOCUMENTO"},
                                                                                        {NAME_VALUE : "observations",
                                                                                         ATTRIBUTE_NAME_VALUE : "APONTAMENT",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens"}]}]}]}
        # defines how to extract stock adjustment entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "StockAdjustment",
                                                   INPUT_ENTITIES_VALUE : [stkprore_input_entities]}]

        # connector used to populate the stock adjustment reason relation attribute
        stock_adjustment_reason_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                             OUTPUT_DEPENDENCIES_VALUE : {"StockAdjustmentReason" : []},
                                             ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["StockAdjustmentReason"]}}

        # defines how to connect stock adjustment entities to stock adjustment reason entities
        stock_adjustment_stock_adjustment_reason_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["stock_adjustment_reason"],
                                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["stock_adjustments"],
                                                             CONNECTORS_VALUE : [stock_adjustment_reason_connector]}

        # connector used to populate the adjustment owners relation attribute
        adjustment_owners_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                       INPUT_DEPENDENCIES_VALUE : {"vendedor" : ["CODIGO"],
                                                                   "stkprore" : ["RESPONSA"]},
                                       OUTPUT_DEPENDENCIES_VALUE : {"Employee" : []},
                                       ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "vendedor",
                                                          JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "RESPONSA"},
                                                          OUTPUT_ENTITY_NAMES_VALUE : ["Employee"]}}

        # defines how to populate the stock adjustment entities' adjustment owners relation attribute
        stock_adjustment_adjustment_owners_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["adjustment_owners"],
                                                       RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["owned_adjustments"],
                                                       CONNECTORS_VALUE :  [adjustment_owners_connector]}

        # defines how to connect stock adjustment entities to other entities
        self.relation_mapping_entities = [{NAME_VALUE : "StockAdjustment",
                                           RELATIONS_VALUE : [stock_adjustment_stock_adjustment_reason_relation,
                                                              stock_adjustment_adjustment_owners_relation]}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_set_adjustment_target,
                                          INPUT_DEPENDENCIES_VALUE : {"stkproan" : ["LOJAENTRA", "LOJASAI"],
                                                                      "lojas" : ["CODIGO"]}}]

    def post_conversion_handler_set_adjustment_target(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_plugin.info("Setting the stock adjustments' adjustment target")

        # sets the adjustment target for each stock adjustment
        stock_adjustment_entities = output_intermediate_structure.get_entities_by_name("StockAdjustment")
        for stock_adjustment_entity in stock_adjustment_entities:

            # retrieves the adjustment target from one of the stock adjustment lines
            stock_adjustment_merchandise_hierarchy_tree_node_entities = stock_adjustment_entity.get_attribute("stock_adjustment_lines")
            for stock_adjustment_merchandise_hierarchy_tree_node_entity in stock_adjustment_merchandise_hierarchy_tree_node_entities:
                quantity = stock_adjustment_merchandise_hierarchy_tree_node_entity.get_attribute("quantity")

                # retrieves the stock adjustment line's creator input entity
                stock_adjustment_merchandise_hierarchy_tree_node_entity_object_id = stock_adjustment_merchandise_hierarchy_tree_node_entity.get_object_id()
                stkproan_entity_index = (INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, stock_adjustment_merchandise_hierarchy_tree_node_entity_object_id)
                stkproan_entity = input_intermediate_structure.get_entities_by_index(stkproan_entity_index)[0]

                # retrieves the adjustment target from the lojaentra and lojasai field depending on whether the
                # stock adjustment line describes a stock entry or removal
                if quantity > 0:
                    codigo = stkproan_entity.get_attribute("LOJAENTRA")
                else:
                    codigo = stkproan_entity.get_attribute("LOJASAI")

                # retrieves the loja input entity
                loja_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "lojas", AND_VALUE, "CODIGO", EQUALS_VALUE, codigo)
                loja_entity = input_intermediate_structure.get_entities_by_index(loja_entity_index)[0]
                loja_entity_object_id = loja_entity.get_object_id()

                # retrieves the store output entity created from the loja input entity
                store_entity_index = (OUTPUT_ENTITY_VALUE, WHERE_VALUE, INPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, loja_entity_object_id, CREATED_VALUE, OUTPUT_ENTITY_NAME_VALUE, EQUALS_VALUE, "Store")
                store_entity = output_intermediate_structure.get_entities_by_index(store_entity_index)[0]

                # sets the stock adjustment entity's adjustment target attribute
                stock_adjustment_entity.set_attribute("adjustment_target", store_entity)

                # adds the stock adjustment to the store's list of stock adjustments
                data_converter.connect_entities(store_entity, "stock_adjustments", stock_adjustment_entity)

                break

        return output_intermediate_structure
