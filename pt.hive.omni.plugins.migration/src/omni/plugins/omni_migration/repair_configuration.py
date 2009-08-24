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

class RepairConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Repair entities from diamante.
    """

    omni_migration_plugin = None
    """ The omni migration plugin """

    def __init__(self, omni_migration_plugin):
        self.omni_migration_plugin = omni_migration_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines the schemas of the intermediate entities populated by this configuration
        self.intermediate_entity_schemas = [{NAME_VALUE : "Repair",
                                             ATTRIBUTES_VALUE : {"company_product_code" : {TYPES_VALUE : STRING_TYPE},
                                                                 "name" : {TYPES_VALUE : STRING_TYPE},
                                                                 "observations" : {TYPES_VALUE : STRING_TYPE},
                                                                 "sellable" : {TYPES_VALUE : INTEGER_TYPE},
                                                                 "parent_nodes" : {LIST_TYPE_VALUE : True,
                                                                                   TYPES_VALUE : ["MerchandiseHierarchyTreeNode"]},
                                                                 "sale_lines" : {LIST_TYPE_VALUE : True,
                                                                                 TYPES_VALUE : ["SaleMerchandiseHierarchyTreeNode"]},
                                                                 "purchase_lines" : {LIST_TYPE_VALUE : True,
                                                                                     TYPES_VALUE : ["PurchaseMerchandiseHierarchyTreeNode"]},
                                                                 "contactable_organizational_units" : {LIST_TYPE_VALUE : True,
                                                                                                       TYPES_VALUE : ["MerchandiseContactableOrganizationalHierarchyTreeNode"]},
                                                                 "organizational_merchandise_hierarchy_tree_node_vat_classes" : {LIST_TYPE_VALUE : True,
                                                                                                                                 TYPES_VALUE : ["OrganizationalMerchandiseHierarchyTreeNodeVatClass"]},
                                                                 "status" : {TYPES_VALUE : INTEGER_TYPE}}}]
