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

AND_VALUE = "and"

ATTRIBUTE_NAMES_VALUE = "attribute_names"

CREATOR_ENTITY_NAMES_VALUE = "creator_entity_names"

ENTITY_NAME_VALUE = "entity_name"

EQUALS_VALUE = "equals"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

DIAMANTE_VAT_RATE_21 = 1
""" The diamante indicator used to represent a 21% vat rate """

class MerchandiseContactableOrganizationalHierarchyTreeNodeConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni MerchandiseContactableOrganizationalHierarchyTreeNode entities from diamante.
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
                                       INPUT_DEPENDENCIES_VALUE : {"sbprodut" : ["PRODUTO"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["PRODUTO"]}}]

        # defines how to extract merchandise contactable organizational hierarchy tree node entities from prodloja entities
        prodloja_input_entities = {NAME_VALUE : "prodloja",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : self.entity_validator_is_sellable_product,
                                                                                  INPUT_DEPENDENCIES_VALUE : {"prodloja" : ["CODIGO"]}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "min_stock",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "stock_on_hand",
                                                                                         ATTRIBUTE_NAME_VALUE : "STOCK",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "discount",
                                                                                         DEFAULT_VALUE_VALUE : 0.0},
                                                                                        {NAME_VALUE : "stock_in_transit",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "stock_reserved",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "price",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_copy_price,
                                                                                                            INPUT_DEPENDENCIES_VALUE : {"produtos" : ["CODIGO",
                                                                                                                                                      "VENDASIVA",
                                                                                                                                                      "IVA",
                                                                                                                                                      "PVP"]}}]}]}]}

        # defines how to extract merchandise contactable organizational hierarchy tree node entities from sbprodut entities
        sbprodut_input_entities = {NAME_VALUE : "sbprodut",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "min_stock",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "stock_on_hand",
                                                                                         ATTRIBUTE_NAME_VALUE : "STOCK",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "discount",
                                                                                         DEFAULT_VALUE_VALUE : 0.0},
                                                                                        {NAME_VALUE : "stock_in_transit",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "stock_reserved",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "cost",
                                                                                         ATTRIBUTE_NAME_VALUE : "CUSTO"},
                                                                                        {NAME_VALUE : "price",
                                                                                         ATTRIBUTE_NAME_VALUE : "VALOR"}]}]}

        # defines how to extract merchandise contactable organizational hierarchy tree node entities from servicos entities
        servicos_input_entities = {NAME_VALUE : "servicos",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "min_stock",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "stock_on_hand",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "discount",
                                                                                         DEFAULT_VALUE_VALUE : 0.0},
                                                                                        {NAME_VALUE : "stock_in_transit",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "stock_reserved",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "cost",
                                                                                         ATTRIBUTE_NAME_VALUE : "PRCUSTO"},
                                                                                        {NAME_VALUE : "price",
                                                                                         ATTRIBUTE_NAME_VALUE : "ILIQUIDO"}]}]}

        # defines how to extract merchandise contactable organizational hierarchy tree node entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "MerchandiseContactableOrganizationalHierarchyTreeNode",
                                                   INPUT_ENTITIES_VALUE : [prodloja_input_entities,
                                                                           sbprodut_input_entities,
                                                                           servicos_input_entities]}]

        # connector used to populate the merchandise relation attribute with product entities created from produtos entities
        produtos_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                          INPUT_DEPENDENCIES_VALUE : {"produtos" : ["CODIGO"],
                                                                      "prodloja" : ["CODIGO"]},
                                          OUTPUT_DEPENDENCIES_VALUE : {"Product" : []},
                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "produtos",
                                                             CREATOR_ENTITY_NAMES_VALUE : ["prodloja"],
                                                             JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "CODIGO"},
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["Product"]}}

        # connector used to populate the merchandise relation attribute with repair entities created from servicos entities
        servicos_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Repair" : []},
                                          ARGUMENTS_VALUE : {CREATOR_ENTITY_NAMES_VALUE : ["servicos"],
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["Repair"]}}

        # connector used to populate the merchandise relation attribute with sub product entities created from sbprodut entities
        sbprodut_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                          OUTPUT_DEPENDENCIES_VALUE : {"SubProduct" : []},
                                          ARGUMENTS_VALUE : {CREATOR_ENTITY_NAMES_VALUE : ["sbprodut"],
                                                             OUTPUT_ENTITY_NAMES_VALUE : ["SubProduct"]}}

        # defines how to populate the merchandise contactable organizational hierarchy tree node entities's merchandise relation attribute
        merchandise_contactable_organizational_hierarchy_tree_node_merchandise_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["merchandise"],
                                                                                           RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_units"],
                                                                                           CONNECTORS_VALUE :  [produtos_merchandise_connector,
                                                                                                                servicos_merchandise_connector,
                                                                                                                sbprodut_merchandise_connector]}

        # connector used to populate the contactable organizational hierarchy tree node relation attribute with store entities
        contactable_organizational_hierarchy_tree_node_store_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                                          INPUT_DEPENDENCIES_VALUE : {"lojas" : ["CODIGO"],
                                                                                                      "prodloja" : ["LOJAS"]},
                                                                          OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                                                                          ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "lojas",
                                                                                             CREATOR_ENTITY_NAMES_VALUE : ["prodloja"],
                                                                                             JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "LOJAS"},
                                                                                             OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # connector used to populate the contactable organizational hierarchy tree node relation attribute with system company entities
        contactable_organizational_hierarchy_tree_node_system_company_connector = {FUNCTION_VALUE : "connector_all_output_entities",
                                                                                   OUTPUT_DEPENDENCIES_VALUE : {"SystemCompany" : []},
                                                                                   ARGUMENTS_VALUE : {CREATOR_ENTITY_NAMES_VALUE : ["sbprodut", "servicos"],
                                                                                                      OUTPUT_ENTITY_NAMES_VALUE : ["SystemCompany"]}}

        # defines how to populate the merchandise contactable organizational hierarchy tree node entities' inventory relation
        merchandise_contactable_organizational_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                                                                                                              RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["inventory"],
                                                                                                                              CONNECTORS_VALUE : [contactable_organizational_hierarchy_tree_node_store_connector,
                                                                                                                                                  contactable_organizational_hierarchy_tree_node_system_company_connector]}

        # defines how to connect the extracted merchandise hierarchy contactable organizational hierarchy tree node entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "MerchandiseContactableOrganizationalHierarchyTreeNode",
                                           RELATIONS_VALUE : [merchandise_contactable_organizational_hierarchy_tree_node_merchandise_relation,
                                                              merchandise_contactable_organizational_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node_relation]}]

    def entity_validator_is_sellable_product(self, data_converter, input_intermediate_structure, input_entity, arguments):
        # retrieves the subproducts associated with this product and marks the entity as valid in case
        # it has no subproducts
        codigo = input_entity.get_attribute("CODIGO")
        sbprodut_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "sbprodut", AND_VALUE, "PRODUTO", EQUALS_VALUE, codigo)
        sbprodut_entities = input_intermediate_structure.get_entities_by_index(sbprodut_index)

        return bool(len(sbprodut_entities) == 0)

    def attribute_handler_copy_price(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the entity where the prices product price is stored
        codigo = input_entity.get_attribute("CODIGO")
        produtos_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "produtos", AND_VALUE, "CODIGO", EQUALS_VALUE, codigo)
        produtos = input_intermediate_structure.get_entities_by_index(produtos_index)

        # @todo: this is a hack
        if not len(produtos) == 1:
            return

        produto = produtos[0]

        # recalculate the price for products with a 21% vat rate because that data is corrupt
        vendasiva = produto.get_attribute("VENDASIVA")
        iva = produto.get_attribute("IVA")
        if iva == DIAMANTE_VAT_RATE_21:
            pvp = produto.get_attribute("PVP")
            output_attribute_value = ((pvp - vendasiva) / vendasiva)
        else:
            output_attribute_value = vendasiva

        return output_attribute_value
