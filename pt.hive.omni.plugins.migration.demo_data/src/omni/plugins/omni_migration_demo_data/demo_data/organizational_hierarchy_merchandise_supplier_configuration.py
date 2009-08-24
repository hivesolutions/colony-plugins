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

import types

ATTRIBUTES_VALUE = "attributes"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

INPUT_OUTPUT_ENTITY_NAMES_VALUE = "input_output_entity_names"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

DEMO_DATA_TRANSACTIONAL_MERCHANDISE_TYPES = ["product", "subproduct", "service"]
""" The transactional merchandise types in the demo data """

OMNI_NON_CONSIGNABLE_STATUS = 0
""" The non consignable status indicator in omni """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class OrganizationalHierarchyMerchandiseSupplierConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni OrganizationalHierarchyMerchandiseSupplier entities from the demo data.
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
        dd_merchandise_input_entities = {NAME_VALUE : "DD_Merchandise",
                                         OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values_in_list",
                                                                                        INPUT_DEPENDENCIES_VALUE : {"DD_Merchandise" : ["Type"]},
                                                                                        ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"Type" : DEMO_DATA_TRANSACTIONAL_MERCHANDISE_TYPES}}}],
                                                                   OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "consignable",
                                                                                               DEFAULT_VALUE_VALUE : OMNI_NON_CONSIGNABLE_STATUS},
                                                                                              {NAME_VALUE : "unit_cost",
                                                                                               ATTRIBUTE_NAME_VALUE : "Price"},
                                                                                              {NAME_VALUE : "status",
                                                                                               DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract organizational hierarchy merchandise supplier entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "OrganizationalHierarchyMerchandiseSupplier",
                                                   INPUT_ENTITIES_VALUE : [dd_merchandise_input_entities]}]

        # connector used to populate the supplied merchandise relation attribute
        supplied_merchandise_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Product" : [],
                                                                       "SubProduct" : [],
                                                                       "Service" : []},
                                          ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Product", "SubProduct", "Service"]}}

        # defines how to populate the organizational hierarchy merchandise supplier entities' supplied merchandise relation
        organizational_hierarchy_merchandise_supplier_supplied_merchandise_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplied_merchandise"],
                                                                                       RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["organizational_hierarchy_merchandise_suppliers"],
                                                                                       CONNECTORS_VALUE : [supplied_merchandise_connector]}

        # connector used to populate the supplier relation attribute
        supplier_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                              INPUT_DEPENDENCIES_VALUE : {"DD_Supplier" : ["Id"],
                                                          "DD_Merchandise" : ["Supplier"]},
                              OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                              ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Supplier",
                                                 JOIN_ATTRIBUTES_VALUE : {"Id" : "Supplier"},
                                                 OUTPUT_ENTITY_NAMES_VALUE : ["SupplierCompany"]}}

        # defines how to populate the organizational hierarchy merchandise supplier entities' supplier relation
        organizational_hierarchy_merchandise_supplier_supplier_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplier"],
                                                                           RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["organizational_hierarchy_merchandise_suppliers"],
                                                                           CONNECTORS_VALUE : [supplier_connector]}

        # connector used to populate the supplied organizational hierarchy relation attribute
        supplied_organizational_hierarchy_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_input_entities",
                                                       OUTPUT_DEPENDENCIES_VALUE : {"SystemCompany" : []},
                                                       ARGUMENTS_VALUE : {INPUT_OUTPUT_ENTITY_NAMES_VALUE : {"DD_Company" : ["SystemCompany"]}}}

        # defines how to populate the organizational hierarchy merchandise supplier entities' supplier organizational hierarchy relation
        organizational_hierarchy_merchandise_supplier_supplied_organizational_hierarchy_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["supplied_organizational_hierarchy"],
                                                                                                    RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["organizational_hierarchy_merchandise_suppliers"],
                                                                                                    CONNECTORS_VALUE : [supplied_organizational_hierarchy_connector]}

        # defines how to connect the extracted organizational hierarchy merchandise supplier entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "OrganizationalHierarchyMerchandiseSupplier",
                                           RELATIONS_VALUE : [organizational_hierarchy_merchandise_supplier_supplied_merchandise_relation,
                                                              organizational_hierarchy_merchandise_supplier_supplier_relation,
                                                              organizational_hierarchy_merchandise_supplier_supplied_organizational_hierarchy_relation]}]
