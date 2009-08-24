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

ATTRIBUTES_VALUE = "attributes"

CREATOR_ENTITY_NAMES_VALUE = "creator_entity_names"

CREATOR_ENTITY_NULL_ATTRIBUTE_VALUES_VALUE = "creator_entity_null_attribute_values"

CREATOR_ENTITY_NON_NULL_ATTRIBUTE_VALUES_VALUE = "creator_entity_non_null_attribute_values"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE = "G/C"
""" The consignment slip document indicator in diamante """

class ConsignmentMerchandiseHierarchyTreeNodeConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni ConsignmentMerchandiseHierarchyTreeNode entities from diamante.
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
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["sbprodut"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"sbprodut" : ["PRODUTO", "SUBCODIGO"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["PRODUTO", "SUBCODIGO"]}},
                                      {ENTITY_NAMES_VALUE : ["vendas"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"vendas" : ["DOCUMENTO", "TIPODOC"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "TIPODOC"]}},
                                      {ENTITY_NAMES_VALUE : ["compras"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"compras" : ["DOCUMENTO", "FORNECEDOR", "TIPODOC"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "FORNECEDOR", "TIPODOC"]}}]

        # defines how to extract consignment merchandise hierarchy tree node entities from anavenda entities
        anavenda_input_entities = {NAME_VALUE : "anavenda",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"anavenda" : ["TIPODOC"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE}}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "consigned_quantity",
                                                                                         ATTRIBUTE_NAME_VALUE : "QUANTIDADE"}]}]}

        # defines how to extract consignment merchandise hierarchy tree node entities from anacompr entities
        anacompr_input_entities = {NAME_VALUE : "anacompr",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"anacompr" : ["TIPODOC"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE}}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "consigned_quantity",
                                                                                         ATTRIBUTE_NAME_VALUE : "QUANTIDADE"}]}]}

        # defines how to extract consignment merchandise hierarchy tree node entities from sbcompra entities
        sbcompra_input_entities = {NAME_VALUE : "sbcompra",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"sbcompra" : ["TIPODOC"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"TIPODOC" : DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE}}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "consigned_quantity",
                                                                                         ATTRIBUTE_NAME_VALUE : "STOCK"}]}]}

        # defines how to extract consignment merchandise hierarchy tree node entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "ConsignmentMerchandiseHierarchyTreeNode",
                                                   INPUT_ENTITIES_VALUE : [anavenda_input_entities,
                                                                           anacompr_input_entities,
                                                                           sbcompra_input_entities]}]

        # connector used to populate the merchandise relation attribute with product entities created from produtos entities
        anavenda_produtos_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                   INPUT_DEPENDENCIES_VALUE : {"anavenda" : ["PRODUTO"],
                                                                               "produtos" : ["CODIGO"]},
                                                   ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "produtos",
                                                                      CREATOR_ENTITY_NAMES_VALUE : ["anavenda"],
                                                                      CREATOR_ENTITY_NULL_ATTRIBUTE_VALUES_VALUE : ["SUBCODIGO"],
                                                                      JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "PRODUTO"},
                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["Product"]}}

        # connector used to populate the merchandise relation attribute with product entities created from sbprodut entities
        anavenda_sbprodut_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                   INPUT_DEPENDENCIES_VALUE : {"anavenda" : ["PRODUTO", "SUBCODIGO"],
                                                                               "sbprodut" : ["PRODUTO", "SUBCODIGO"]},
                                                   ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "sbprodut",
                                                                      CREATOR_ENTITY_NAMES_VALUE : ["anavenda"],
                                                                      CREATOR_ENTITY_NON_NULL_ATTRIBUTE_VALUES_VALUE : ["SUBCODIGO"],
                                                                      JOIN_ATTRIBUTES_VALUE : {"PRODUTO" : "PRODUTO",
                                                                                               "SUBCODIGO" : "SUBCODIGO"},
                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["SubProduct"]}}

        # connector used to populate the merchandise relation attribute with product entities created from produtos entities
        anacompr_produtos_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                   INPUT_DEPENDENCIES_VALUE : {"anacompr" : ["PRODUTO"],
                                                                               "produtos" : ["CODIGO"]},
                                                   ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "produtos",
                                                                      CREATOR_ENTITY_NAMES_VALUE : ["anacompr"],
                                                                      JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "PRODUTO"},
                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["Product"]}}

        # connector used to populate the merchandise relation attribute with product entities created from sbprodut entities
        anacompr_sbprodut_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                   INPUT_DEPENDENCIES_VALUE : {"sbcompra" : ["PRODUTO", "SUBCODIGO"],
                                                                               "sbprodut" : ["PRODUTO", "SUBCODIGO"]},
                                                   ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "sbprodut",
                                                                      CREATOR_ENTITY_NAMES_VALUE : ["sbcompra"],
                                                                      JOIN_ATTRIBUTES_VALUE : {"PRODUTO" : "PRODUTO",
                                                                                               "SUBCODIGO" : "SUBCODIGO"},
                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["SubProduct"]}}

        # defines how to connect consignment merchandise hierarchy tree node relation entities with merchandise entities
        consignment_merchandise_hierarchy_tree_node_merchandise_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["merchandise"],
                                                                            RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["consignments"],
                                                                            CONNECTORS_VALUE : [anavenda_produtos_merchandise_connector,
                                                                                                anavenda_sbprodut_merchandise_connector,
                                                                                                anacompr_produtos_merchandise_connector,
                                                                                                anacompr_sbprodut_merchandise_connector]}

        # connector used to populate the consignment relation attribute with consignment entities
        anacompr_sbcompra_consignment_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                   INPUT_DEPENDENCIES_VALUE : {"compras" : ["TIPODOC", "DOCUMENTO", "FORNECEDOR"],
                                                                               "anacompr" : ["TIPODOC", "DOCUMENTO", "FORNECEDOR"],
                                                                               "sbcompra" : ["TIPODOC", "DOCUMENTO", "FORNECEDOR"]},
                                                   ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "compras",
                                                                      CREATOR_ENTITY_NAMES_VALUE : ["anacompr", "sbcompra"],
                                                                      JOIN_ATTRIBUTES_VALUE : {"TIPODOC" : "TIPODOC",
                                                                                               "DOCUMENTO" : "DOCUMENTO",
                                                                                               "FORNECEDOR" : "FORNECEDOR"},
                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["Consignment"]}}

        # connector used to populate the consignment relation attribute with consignment entities
        anavenda_consignment_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                          INPUT_DEPENDENCIES_VALUE : {"vendas" : ["TIPODOC", "DOCUMENTO"],
                                                                      "anavenda" : ["TIPODOC", "DOCUMENTO"]},
                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "vendas",
                                                             CREATOR_ENTITY_NAMES_VALUE : ["anavenda"],
                                                             JOIN_ATTRIBUTES_VALUE : {"TIPODOC" : "TIPODOC",
                                                                                      "DOCUMENTO" : "DOCUMENTO"},
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["Consignment"]}}

        # defines how to connect the consignment entities to consignment merchandise hierarchy tree node entities
        consignment_merchandise_hierarchy_tree_node_consignment_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["consignment"],
                                                                            RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["merchandise"],
                                                                            CONNECTORS_VALUE :  [anacompr_sbcompra_consignment_connector,
                                                                                                 anavenda_consignment_connector]}

        # defines how to connect the extracted consignment merchandise hierarchy tree node entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "ConsignmentMerchandiseHierarchyTreeNode",
                                           RELATIONS_VALUE : [consignment_merchandise_hierarchy_tree_node_merchandise_relation,
                                                              consignment_merchandise_hierarchy_tree_node_consignment_relation]}]
