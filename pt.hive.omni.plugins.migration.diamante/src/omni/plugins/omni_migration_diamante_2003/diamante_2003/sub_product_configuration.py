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

OMNI_SELLABLE_TRANSACTIONAL_MERCHANDISE = 1
""" The sellable transactional merchandise indicator in omni """

class SubProductConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni SubProduct entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract sub product entities from sbprodut entities
        sbprodut_input_entities = {NAME_VALUE : "sbprodut",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "company_product_code",
                                                                                         ATTRIBUTE_NAME_VALUE : "SUBCODIGO",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_concatenate_parent_product_code,
                                                                                                            INPUT_DEPENDENCIES_VALUE : {"sbprodut" : ["PRODUTO"],
                                                                                                                                        "produtos" : ["CODIGO"]}}]},
                                                                                        {NAME_VALUE : "weight",
                                                                                         ATTRIBUTE_NAME_VALUE : "PESO"},
                                                                                        {NAME_VALUE : "sellable",
                                                                                         DEFAULT_VALUE_VALUE : OMNI_SELLABLE_TRANSACTIONAL_MERCHANDISE}]}]}

        # defines how to extract product entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "SubProduct",
                                                   INPUT_ENTITIES_VALUE : [sbprodut_input_entities]}]

        # connector used to populate the parent nodes relation attribute
        sub_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                      INPUT_DEPENDENCIES_VALUE : {"produtos" : ["CODIGO"],
                                                                  "sbprodut" : ["PRODUTO"]},
                                      OUTPUT_DEPENDENCIES_VALUE : ["Product"],
                                      ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "produtos",
                                                         JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "PRODUTO"},
                                                         OUTPUT_ENTITY_NAMES_VALUE : ["Product"]}}

        # defines how to populate the product entities' parent nodes relation attribute
        sub_product_parent_nodes_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["parent_nodes"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["child_nodes"],
                                             CONNECTORS_VALUE : [sub_parent_nodes_connector]}

        # defines how to connect the extracted product entities to other entities
        self.relation_mapping_entities = [{NAME_VALUE : "SubProduct",
                                           RELATIONS_VALUE : [sub_product_parent_nodes_relation]}]

    def attribute_handler_concatenate_parent_product_code(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the products associated with this subproduct
        produto = input_entity.get_attribute("PRODUTO")
        produtos_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "produtos", AND_VALUE, "CODIGO", EQUALS_VALUE, produto)
        produtos_entities = input_intermediate_structure.get_entities_by_index(produtos_index)

        # raises an exception in case none or more than one product is found
        if not len(produtos_entities) == 1:
            raise "Unexpected number of parent nodes for sub product"

        # concatenates the parent product code with the sub-product code
        produtos_entity = produtos_entities[0]
        codigo = produtos_entity.get_attribute("CODIGO")
        output_attribute_value = "%s-%s" % (codigo, output_attribute_value)

        return output_attribute_value
