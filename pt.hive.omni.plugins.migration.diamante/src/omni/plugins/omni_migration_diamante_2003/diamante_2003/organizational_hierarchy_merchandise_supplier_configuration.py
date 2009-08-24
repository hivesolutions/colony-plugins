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

OMNI_NON_CONSIGNABLE_STATUS = 0
""" The non consignable status indicator in omni """

class OrganizationalHierarchyMerchandiseSupplierConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni OrganizationalHierarchyMerchandiseSupplier entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_create_organizational_hierarchy_merchandise_supplier_entities,
                                          OUTPUT_DEPENDENCIES_VALUE : {"PurchaseTransaction" : [],
                                                                       "PurchaseMerchandiseHierarchyTreeNode" : []}}]

    def post_conversion_handler_create_organizational_hierarchy_merchandise_supplier_entities(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_plugin.info("Creating organizational hierarchy merchandise supplier entities")

        # creates organizational hierarchy merchandise supplier entities from purchase line entities
        supplier_line_tuples = []
        purchase_line_entities = output_intermediate_structure.get_entities_by_name("PurchaseMerchandiseHierarchyTreeNode")
        purchase_line_entities = [purchase_line_entity for purchase_line_entity in purchase_line_entities if purchase_line_entity.get_attribute("merchandise") and purchase_line_entity.get_attribute("purchase")]
        for purchase_line_entity in purchase_line_entities:

            # retrieves the merchandise purchased in the purchase line
            merchandise_entity = purchase_line_entity.get_attribute("merchandise")
            merchandise_entity_name = merchandise_entity.get_name()

            # retrieves the necessary attributes for the supplier line from the purchase line and purchase entities
            purchase_entity = purchase_line_entity.get_attribute("purchase")
            billing_site_entity = purchase_entity.get_attribute("billing_site")
            supplier_entity = purchase_entity.get_attribute("supplier")
            unit_cost = purchase_line_entity.get_attribute("unit_cost")

            # skips this line in case no billing site or supplier is found
            if not billing_site_entity or not supplier_entity:
                continue

            # creates a tuple identifying the supplier - merchandise - receiver combination
            supplier_entity_object_id = supplier_entity.get_object_id()
            merchandise_entity_object_id = merchandise_entity.get_object_id()
            billing_site_entity_object_id = billing_site_entity.get_object_id()
            supplier_line_tuple = (supplier_entity_object_id, merchandise_entity_object_id, billing_site_entity_object_id)

            # ignores this purchase line in case it points to supplier line that was already created
            if supplier_line_tuple in supplier_line_tuples:
                continue

            # adds the supplier tuple to the list of created supplier tuples
            supplier_line_tuples.append(supplier_line_tuple)

            # creates a organizational hierarchy merchandise supplier entity
            organizational_hierarchy_merchandise_supplier_entity = output_intermediate_structure.create_entity("OrganizationalHierarchyMerchandiseSupplier")
            organizational_hierarchy_merchandise_supplier_entity.set_attribute("unit_cost", unit_cost)
            organizational_hierarchy_merchandise_supplier_entity.set_attribute("consignable", OMNI_NON_CONSIGNABLE_STATUS)
            organizational_hierarchy_merchandise_supplier_entity.set_attribute("supplier", supplier_entity)
            organizational_hierarchy_merchandise_supplier_entity.set_attribute("supplied_merchandise", merchandise_entity)
            organizational_hierarchy_merchandise_supplier_entity.set_attribute("supplied_organizational_hierarchy", billing_site_entity)

            # sets the other side of the relations created with the merchandise entity
            data_converter.connect_entities(merchandise_entity, "organizational_hierarchy_merchandise_suppliers", organizational_hierarchy_merchandise_supplier_entity)

            # sets the other side of the relations created with the billing site entity
            data_converter.connect_entities(billing_site_entity, "organizational_hierarchy_merchandise_suppliers", organizational_hierarchy_merchandise_supplier_entity)

            # sets the other side of the relations created with the supplier entity
            data_converter.connect_entities(supplier_entity, "supplied_organizational_hierarchies", organizational_hierarchy_merchandise_supplier_entity)

            # adds the merchandise to the list of merchandise commercialized by the supplier
            data_converter.connect_entities(supplier_entity, "commercialized_merchandise", merchandise_entity)

            # adds the supplier to the list of merchandise suppliers
            data_converter.connect_entities(merchandise_entity, "commercialization_suppliers", supplier_entity)

        return output_intermediate_structure
