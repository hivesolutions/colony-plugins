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

CREATOR_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "creator_entity_non_null_attribute_names"

CREATOR_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE = "creator_entity_null_attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

class StockAdjustmentMerchandiseHierarchyTreeNodeConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni StockAdjustmentMerchandiseHierarchyTreeNode entities from diamante.
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
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["stkprore"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"stkprore" : ["DOCUMENTO", "TIPO"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "TIPO"]}},
                                      {ENTITY_NAMES_VALUE : ["sbprodut"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"sbprodut" : ["PRODUTO", "SUBCODIGO"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["PRODUTO", "SUBCODIGO"]}}]

        # defines how to extract stock adjustment merchandise hierarchy tree node entities from stkproan entities
        stkproan_input_entities = {NAME_VALUE : "stkproan",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "quantity",
                                                                                         ATTRIBUTE_NAME_VALUE : "QT",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_convert_quantity_sign,
                                                                                                            INPUT_DEPENDENCIES_VALUE : {"stkproan" : ["LOJASAI"]}}]}]}]}

        # defines how to extract stock adjustment merchandise hierarchy tree node entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "StockAdjustmentMerchandiseHierarchyTreeNode",
                                                   INPUT_ENTITIES_VALUE : [stkproan_input_entities]}]

        # connector used to populate the merchandise relation attribute with product entities created from produtos entities
        produtos_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                          INPUT_DEPENDENCIES_VALUE : {"produtos" : ["CODIGO"],
                                                                      "stkproan" : ["PRODUTO"]},
                                          OUTPUT_DEPENDENCIES_VALUE : {"Product" : []},
                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "produtos",
                                                             CREATOR_ENTITY_NULL_ATTRIBUTE_NAMES_VALUE : ["SUBCODIGO"],
                                                             JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "PRODUTO"},
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["Product"]}}

        # connector used to populate the merchandise relation attribute with sub product entities created from sbprodut entities
        sbprodut_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                          INPUT_DEPENDENCIES_VALUE : {"sbprodut" : ["PRODUTO", "SUBCODIGO"],
                                                                      "stkproan" : ["PRODUTO", "SUBCODIGO"]},
                                          OUTPUT_DEPENDENCIES_VALUE : {"SubProduct" : []},
                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "sbprodut",
                                                             CREATOR_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE : ["PRODUTO", "SUBCODIGO"],
                                                             JOIN_ATTRIBUTES_VALUE : {"PRODUTO" : "PRODUTO",
                                                                                      "SUBCODIGO" : "SUBCODIGO"},
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["SubProduct"]}}

        # defines how to populate the stock adjustment merchandise hierarchy tree node entities' merchandise relation attribute
        stock_adjustment_merchandise_hierarchy_tree_node_merchandise_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["merchandise"],
                                                                                 RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["stock_adjustment_lines"],
                                                                                 CONNECTORS_VALUE :  [produtos_merchandise_connector,
                                                                                                      sbprodut_merchandise_connector]}

        # connector used to populate the stock adjustment relation attribute
        stock_adjustment_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                      INPUT_DEPENDENCIES_VALUE : {"stkproan" : ["TIPO", "DOCUMENTO"],
                                                                  "stkprore" : ["TIPO", "DOCUMENTO"]},
                                      ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "stkprore",
                                                         JOIN_ATTRIBUTES_VALUE : {"TIPO" : "TIPO",
                                                                                  "DOCUMENTO" : "DOCUMENTO"},
                                                         OUTPUT_ENTITY_NAMES_VALUE :  ["StockAdjustment"]}}

        # defines how to populate the stock adjustment merchandise hierarchy tree node entities' stock adjustment relation attribute
        stock_adjustment_merchandise_hierarchy_tree_node_stock_adjustment_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["stock_adjustment"],
                                                                                      RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["stock_adjustment_lines"],
                                                                                      CONNECTORS_VALUE :  [stock_adjustment_connector]}

        # defines how to connect the extracted stock adjustment merchandise hierarchy tree node entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "StockAdjustmentMerchandiseHierarchyTreeNode",
                                           RELATIONS_VALUE : [stock_adjustment_merchandise_hierarchy_tree_node_merchandise_relation,
                                                              stock_adjustment_merchandise_hierarchy_tree_node_stock_adjustment_relation]}]

    def attribute_handler_convert_quantity_sign(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # converts the adjusted stock quantity to represent if
        # it's a stock increase (positive) or a decrease (negative)

        lojasai = input_entity.get_attribute("LOJASAI")

        if lojasai:
            output_attribute_value = -1 * output_attribute_value

        return output_attribute_value
