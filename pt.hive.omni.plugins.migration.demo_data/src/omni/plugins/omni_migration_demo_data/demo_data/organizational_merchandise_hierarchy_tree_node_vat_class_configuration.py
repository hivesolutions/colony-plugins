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

DIAMANTE_INACTIVE_ENTITY_STATUS = 1
""" The inactive entity status indicator in diamante """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

OMNI_VAT_RATE_20 = 0.20
""" The omni 20% vat rate """

class OrganizationalMerchandiseHierarchyTreeNodeVatClassConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni OrganizationalMerchandiseHierarchyTreeNodeVatClassConfiguration entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_create_organizational_merchandise_hierarchy_tree_node_vat_class_entities,
                                          OUTPUT_DEPENDENCIES_VALUE : {"MerchandiseContactableOrganizationalHierarchyTreeNode" : [],
                                                                       "VatClass" : []}}]

    def post_conversion_handler_create_organizational_merchandise_hierarchy_tree_node_vat_class_entities(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_demo_data_plugin.info("Creating vat lines")

        # retrieves the 20% vat class entity
        vat_class_entities = output_intermediate_structure.get_entities_by_name("VatClass")
        vat_20_entity = None
        for vat_class_entity in vat_class_entities:
            vat_class_vat_rate = vat_class_entity.get_attribute("vat_rate")
            if round(vat_class_vat_rate, 2) == OMNI_VAT_RATE_20:
                vat_20_entity = vat_class_entity

        # creates organizational hierarchy merchandise vat entities from inventory line entities
        inventory_line_entities = output_intermediate_structure.get_entities_by_name("MerchandiseContactableOrganizationalHierarchyTreeNode")
        for inventory_line_entity in inventory_line_entities:

            # retrieves the necessary attributes for the vat line from the inventory line entities
            merchandise_entity = inventory_line_entity.get_attribute("merchandise")
            contactable_organizational_hierarchy_tree_node_entity = inventory_line_entity.get_attribute("contactable_organizational_hierarchy_tree_node")

            # creates an organizational hierarchy merchandise vat class entity
            organizational_merchandise_hierarchy_tree_node_vat_class_entity = output_intermediate_structure.create_entity("OrganizationalMerchandiseHierarchyTreeNodeVatClass")
            organizational_merchandise_hierarchy_tree_node_vat_class_entity.set_attribute("status", OMNI_ACTIVE_ENTITY_STATUS)
            organizational_merchandise_hierarchy_tree_node_vat_class_entity.set_attribute("vat_class", vat_20_entity)
            organizational_merchandise_hierarchy_tree_node_vat_class_entity.set_attribute("merchandise", merchandise_entity)
            organizational_merchandise_hierarchy_tree_node_vat_class_entity.set_attribute("organizational_hierarchy_tree_node", contactable_organizational_hierarchy_tree_node_entity)

            # sets the other side of the relations created in the organizational merchandise hierarchy tree node vat class entity
            for entity in (merchandise_entity, contactable_organizational_hierarchy_tree_node_entity, vat_20_entity):
                # @todo: this is a hack
                if None in (merchandise_entity, contactable_organizational_hierarchy_tree_node_entity, vat_20_entity):
                    continue

                data_converter.connect_entities(entity, "organizational_merchandise_hierarchy_tree_node_vat_classes", organizational_merchandise_hierarchy_tree_node_vat_class_entity)

        return output_intermediate_structure
