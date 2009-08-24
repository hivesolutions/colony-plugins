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

CREATOR_ENTITY_NAMES_VALUE = "creator_entity_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

PURCHASE_MERCHANDISE_HIERARCHY_TREE_NODE_DOCUMENT_TYPES = ["V/D", "FAC", "G/C"]
""" List with the types of documents that correspond to the purchase merchandise hierarchy tree nodes in diamante """

class PurchaseMerchandiseHierarchyTreeNodeConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni PurchaseMerchandiseHierarchyTreeNodeConfiguration entities from diamante.
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
                                      {ENTITY_NAMES_VALUE : ["sbprodut"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"sbprodut" : ["PRODUTO", "SUBCODIGO"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["PRODUTO", "SUBCODIGO"]}}]

        # defines how to extract purchase merchandise hierarchy tree node entities from anacompr entities
        anacompr_input_entities = {NAME_VALUE : "anacompr",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values_in_list",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"anacompr" : ["TIPODOC"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : PURCHASE_MERCHANDISE_HIERARCHY_TREE_NODE_DOCUMENT_TYPES}}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "quantity",
                                                                                         ATTRIBUTE_NAME_VALUE : "QUANTIDADE"},
                                                                                        {NAME_VALUE : "financial_discount",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "financial_discount_vat",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "unit_discount",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "unit_discount_vat",
                                                                                         DEFAULT_VALUE_VALUE : 0}]}]}

        # defines how to extract purchase merchandise hierarchy tree node entities from sbcompra entities
        sbcompra_input_entities = {NAME_VALUE : "sbcompra",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values_in_list",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"sbcompra" : ["TIPODOC"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : PURCHASE_MERCHANDISE_HIERARCHY_TREE_NODE_DOCUMENT_TYPES}}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "quantity",
                                                                                         ATTRIBUTE_NAME_VALUE : "STOCK"},
                                                                                        {NAME_VALUE : "financial_discount",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "financial_discount_vat",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "unit_discount",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "unit_discount_vat",
                                                                                         DEFAULT_VALUE_VALUE : 0}]}]}

        # defines how to extract purchase merchandise hierarchy tree node entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "PurchaseMerchandiseHierarchyTreeNode",
                                                   INPUT_ENTITIES_VALUE : [anacompr_input_entities,
                                                                           sbcompra_input_entities]}]

        # connector used to populate the merchandise relation attribute with product entities created from produtos entities
        produtos_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                          INPUT_DEPENDENCIES_VALUE : {"anacompr" : ["PRODUTO"],
                                                                      "produtos" : ["CODIGO"]},
                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "produtos",
                                                             CREATOR_ENTITY_NAMES_VALUE : ["anacompr"],
                                                             JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "PRODUTO"},
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["Product"]}}

        # connector used to populate the merchandise relation attribute with repair entities created from servicos entities
        servicos_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                          INPUT_DEPENDENCIES_VALUE : {"anacompr" : ["PRODUTO"],
                                                                      "servicos" : ["CODIGO"]},
                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "servicos",
                                                             CREATOR_ENTITY_NAMES_VALUE : ["anacompr"],
                                                             JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "PRODUTO"},
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["Repair"]}}

        # connector used to populate the merchandise relation attribute with sub product entities created from sbprodut entities
        sbprodut_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                          INPUT_DEPENDENCIES_VALUE : {"sbcompra" : ["PRODUTO", "SUBCODIGO"],
                                                                      "sbprodut" : ["PRODUTO", "SUBCODIGO"]},
                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "sbprodut",
                                                             CREATOR_ENTITY_NAMES_VALUE : ["sbcompra"],
                                                             JOIN_ATTRIBUTES_VALUE : {"PRODUTO" : "PRODUTO",
                                                                                      "SUBCODIGO" : "SUBCODIGO"},
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["SubProduct"]}}

        # defines how to populate the purchase merchandise hierarchy tree node entities' merchandise relation attribute
        purchase_merchandise_hierarchy_tree_node_merchandise_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["merchandise"],
                                                                         RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["purchase_lines"],
                                                                         CONNECTORS_VALUE :  [produtos_merchandise_connector,
                                                                                              servicos_merchandise_connector,
                                                                                              sbprodut_merchandise_connector]}

        # connector used to populate the purchase relation attribute
        purchase_relation = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                             INPUT_DEPENDENCIES_VALUE : {"compras" : ["TIPODOC", "DOCUMENTO", "FORNECEDOR"],
                                                         "sbcompra" : ["TIPODOC", "DOCUMENTO", "FORNECEDOR"],
                                                         "anacompr" : ["TIPODOC", "DOCUMENTO", "FORNECEDOR"]},
                             ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "compras",
                                                JOIN_ATTRIBUTES_VALUE : {"TIPODOC" : "TIPODOC",
                                                                         "DOCUMENTO" : "DOCUMENTO",
                                                                         "FORNECEDOR" : "FORNECEDOR"},
                                                OUTPUT_ENTITY_NAMES_VALUE : ["PurchaseTransaction"]}}

        # define how to populate the purchase merchandise hierarchy tree node entities' purchase relation attribute
        purchase_merchandise_hierarchy_tree_node_purchase_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["purchase"],
                                                                      RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["purchase_lines"],
                                                                      CONNECTORS_VALUE : [purchase_relation]}

        # defines how to connect the extracted purchase merchandise hierarchy tree node entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "PurchaseMerchandiseHierarchyTreeNode",
                                           RELATIONS_VALUE : [purchase_merchandise_hierarchy_tree_node_merchandise_relation,
                                                              purchase_merchandise_hierarchy_tree_node_purchase_relation]}]
