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

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class MerchandiseContactableOrganizationalHierarchyTreeNodeConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni MerchandiseContactableOrganizationalHierarchyTreeNode entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract product entities from dd_merchandise entities
        dd_merchandise_input_entities = {NAME_VALUE : "DD_Stock",
                                         OUTPUT_ENTITIES_VALUE : [{HANDLERS_VALUE : [{FUNCTION_VALUE : self.entity_handler_set_cost_margin_price,
                                                                                      INPUT_DEPENDENCIES_VALUE : {"DD_Merchandise" : ["Price", "Margin"]}}],
                                                                   OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "stock_on_hand",
                                                                                               ATTRIBUTE_NAME_VALUE : "Stock on hand"},
                                                                                              {NAME_VALUE : "min_stock",
                                                                                               DEFAULT_VALUE_VALUE : 0},
                                                                                              {NAME_VALUE : "discount",
                                                                                               DEFAULT_VALUE_VALUE : 0},
                                                                                              {NAME_VALUE : "stock_in_transit",
                                                                                               DEFAULT_VALUE_VALUE : 0},
                                                                                              {NAME_VALUE : "stock_reserved",
                                                                                               DEFAULT_VALUE_VALUE : 0},
                                                                                              {NAME_VALUE : "status",
                                                                                               DEFAULT_VALUE_VALUE: OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract merchandise contactable organizational hierarchy tree node entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "MerchandiseContactableOrganizationalHierarchyTreeNode",
                                                   INPUT_ENTITIES_VALUE : [dd_merchandise_input_entities]}]

        # connector used to populate the contactable organizational hierarchy tree node's relation attribute
        contactable_organizational_hierarchy_tree_node_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                                                    INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Name"],
                                                                                                "DD_Stock" : ["Functional Unit"]},
                                                                    OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                                                                    ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Company",
                                                                                       JOIN_ATTRIBUTES_VALUE : {"Name" : "Functional Unit"},
                                                                                       OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # defines how to populate the merchandise contactable organizational hierarchy tree node entities' contactable organizational hierarchy tree node relation
        merchandise_contactable_organizational_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                                                                                                              RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["inventory"],
                                                                                                                              CONNECTORS_VALUE : [contactable_organizational_hierarchy_tree_node_connector]}

        # connector used to populate the merchandise relation attribute
        merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                 INPUT_DEPENDENCIES_VALUE : {"DD_Stock" : ["Merchandise"],
                                                             "DD_Merchandise" : ["Id"]},
                                 OUTPUT_DEPENDENCIES_VALUE : {"Collection" : [],
                                                              "Category" : [],
                                                              "Product" : [],
                                                              "SubProduct" : [],
                                                              "Service" : []},
                                 ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Merchandise",
                                                    JOIN_ATTRIBUTES_VALUE : {"Id" : "Merchandise"},
                                                    OUTPUT_ENTITY_NAMES_VALUE : ["Collection",
                                                                                 "Category",
                                                                                 "Product",
                                                                                 "SubProduct",
                                                                                 "Service"]}}

        # defines how to populate the merchandise contactable organizational hierarchy tree node entities' merchandise relation
        merchandise_contactable_organizational_hierarchy_tree_node_merchandise_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["merchandise"],
                                                                                           RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_units"],
                                                                                           CONNECTORS_VALUE : [merchandise_connector]}

        # defines how to connect the extracted merchandise contactable organizational hierarchy tree node entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "MerchandiseContactableOrganizationalHierarchyTreeNode",
                                           RELATIONS_VALUE : [merchandise_contactable_organizational_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node_relation,
                                                              merchandise_contactable_organizational_hierarchy_tree_node_merchandise_relation]}]

    def entity_handler_set_cost_margin_price(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, arguments):
        # retrieves the merchandise input entity that corresponds to the inventory line
        merchandise_id = input_entity.get_attribute("Merchandise")
        merchandise_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "DD_Merchandise",
                                    AND_VALUE, "Id", EQUALS_VALUE, merchandise_id)
        merchandise_entities = input_intermediate_structure.get_entities_by_index(merchandise_entity_index)

        # raises an exception in case none or more than one merchandise is found
        if not len(merchandise_entities) == 1:
            raise "Unexpected number of merchandise found"

        merchandise_entity = merchandise_entities[0]

        # climbs up the merchandise's hierarchy looking for its price
        while not merchandise_entity.get_attribute("Price"):
            merchandise_entity_parent = merchandise_entity.get_attribute("Parent")
            merchandise_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "DD_Merchandise",
                                        AND_VALUE, "Name", EQUALS_VALUE, merchandise_entity_parent)
            merchandise_entities = input_intermediate_structure.get_entities_by_index(merchandise_entity_index)

            # raises an exception in case none or more than one merchandise is found
            if not len(merchandise_entities) == 1:
                raise "Unexpected number of merchandise found"

            merchandise_entity = merchandise_entities[0]

        # raises an exception in case no price for the merchandise was found
        price = merchandise_entity.get_attribute("Price")
        if not price:
            raise "No price for merchandise was found"

        # calculates the cost, margin and price
        cost = price
        margin = 0

        # applies the input entity margin to calculate the price in case it exists
        if merchandise_entity.has_attribute("Margin") and merchandise_entity.get_attribute("Margin"):
            margin = merchandise_entity.get_attribute("Margin")
            margin = margin / 100
            price = cost + (cost * margin)

        # sets the cost, margin and price in the output entity
        output_entity.set_attribute("cost", cost)
        output_entity.set_attribute("price", price)
        output_entity.set_attribute("margin", margin)

        return output_entity
