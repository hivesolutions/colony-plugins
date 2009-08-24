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

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

EXCLUSION_LIST_VALUE = "exclusion_list"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ATTRIBUTE_NAMES_VALUE = "output_attribute_names"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

SEPARATOR_VALUE = "separator"

NEWLINE_CHARACTER = "\n"
""" The newline character in python """

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

PRODUTOS_ENTITY_OBSERVATION_ATTRIBUTE_NAMES = ["APONTAMENT", "SEGDESCR"]
""" List with the names of the attributes that contains observations in a produtos entity """

OMNI_NON_SELLABLE_TRANSACTIONAL_MERCHANDISE = 0
""" The non sellable transactional merchandise indicator in omni """

OMNI_SELLABLE_TRANSACTIONAL_MERCHANDISE = 1
""" The sellable transactional merchandise indicator in omni """

class ProductConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Product entities from diamante.
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

        # defines how to extract product entities from produtos entities
        produtos_input_entities = {NAME_VALUE : "produtos",
                                   OUTPUT_ENTITIES_VALUE : [{HANDLERS_VALUE : [ # merges observations from various fields into one
                                                                               {FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                INPUT_DEPENDENCIES_VALUE : {"produtos" : PRODUTOS_ENTITY_OBSERVATION_ATTRIBUTE_NAMES},
                                                                                ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : PRODUTOS_ENTITY_OBSERVATION_ATTRIBUTE_NAMES,
                                                                                                   SEPARATOR_VALUE : NEWLINE_CHARACTER,
                                                                                                   OUTPUT_ATTRIBUTE_NAME_VALUE : "description"}},
                                                                                # capitalizes each letter in the merged observations
                                                                               {FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                                ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["description"],
                                                                                                   EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                         ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                            ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]},
                                                                                        {NAME_VALUE : "sellable",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_get_sellable_status,
                                                                                                            INPUT_DEPENDENCIES_VALUE : {"sbprodut" : ["PRODUTO"]}}]},
                                                                                        {NAME_VALUE : "upc",
                                                                                         ATTRIBUTE_NAME_VALUE : "CODBARRAS",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                        {NAME_VALUE : "company_product_code",
                                                                                         ATTRIBUTE_NAME_VALUE : "CODIGO"},
                                                                                        {NAME_VALUE : "weight",
                                                                                         ATTRIBUTE_NAME_VALUE : "PESOUNIT"}]}]}
        # defines how to extract product entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Product",
                                                   INPUT_ENTITIES_VALUE : [produtos_input_entities]}]

        # connector used to populate the parent nodes relation attribute
        coleccao_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                           INPUT_DEPENDENCIES_VALUE : {"produtos" : ["COLECCAO"],
                                                                       "coleccao" : ["CODIGO"]},
                                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "coleccao",
                                                              JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "COLECCAO"},
                                                              OUTPUT_ENTITY_NAMES_VALUE : ["Collection"]}}

        # connector used to populate the parent nodes relation attribute with product entities created from estilo entities
        estilo_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                         INPUT_DEPENDENCIES_VALUE : {"produtos" : ["ESTILO"],
                                                                      "estilo" : ["CODIGO"]},
                                         ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "estilo",
                                                            JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "ESTILO"},
                                                            OUTPUT_ENTITY_NAMES_VALUE : ["Category"]}}

        # connector used to populate the parent nodes relation attribute with product entities created from pureza entities
        pureza_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                         INPUT_DEPENDENCIES_VALUE : {"produtos" : ["PUREZA"],
                                                                     "pureza" : ["CODIGO"]},
                                         ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "pureza",
                                                            JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "PUREZA"},
                                                            OUTPUT_ENTITY_NAMES_VALUE : ["Category"]}}

        # connector used to populate the parent nodes relation attribute with product entities created from qualidad entities
        qualidad_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                           INPUT_DEPENDENCIES_VALUE : {"produtos" : ["QUALIDADE"],
                                                                       "qualidad" : ["CODIGO"]},
                                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "qualidad",
                                                              JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "QUALIDADE"},
                                                              OUTPUT_ENTITY_NAMES_VALUE : ["Category"]}}

        # connector used to populate the parent nodes relation attribute with product entities created from talhe entities
        talhe_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                        INPUT_DEPENDENCIES_VALUE : {"produtos" : ["TALHE"],
                                                                    "talhe" : ["CODIGO"]},
                                        ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "talhe",
                                                           JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "TALHE"},
                                                           OUTPUT_ENTITY_NAMES_VALUE : ["Category"]}}

        # connector used to populate the parent nodes relation attribute with product entities created from tipopeca entities
        tipopeca_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                           INPUT_DEPENDENCIES_VALUE : {"produtos" : ["TIPOPECA"],
                                                                       "tipopeca" : ["CODIGO"]},
                                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "tipopeca",
                                                              JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "TIPOPECA"},
                                                              OUTPUT_ENTITY_NAMES_VALUE : ["Category"]}}

        # connector used to populate the parent nodes relation attribute with product entities created from tipoprod entities
        tipoprod_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                           INPUT_DEPENDENCIES_VALUE : {"produtos" : ["TIPOPRO"],
                                                                       "tipoprod" : ["CODIGO"]},
                                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "tipoprod",
                                                              JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "TIPOPRO"},
                                                              OUTPUT_ENTITY_NAMES_VALUE : ["Category"]}}

        # defines how to populate the product entities' parent nodes relation attribute
        product_parent_nodes_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["parent_nodes"],
                                         RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["child_nodes"],
                                         CONNECTORS_VALUE : [coleccao_parent_nodes_connector,
                                                             estilo_parent_nodes_connector,
                                                             pureza_parent_nodes_connector,
                                                             qualidad_parent_nodes_connector,
                                                             talhe_parent_nodes_connector,
                                                             tipopeca_parent_nodes_connector,
                                                             tipoprod_parent_nodes_connector]}

        # connector used to populate the media relation attribute with media entities
        media_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                           INPUT_DEPENDENCIES_VALUE : {"imagens_definitivo" : ["name_without_extension"],
                                                       "produtos" : ["CODIGO"]},
                           OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "imagens_definitivo",
                                              JOIN_ATTRIBUTES_VALUE : {"name_without_extension" : "CODIGO"},
                                              OUTPUT_ENTITY_NAMES_VALUE : ["Media"]}}

        # defines how to populate the company entities' media relation
        product_media_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["media"],
                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["entities"],
                                  CONNECTORS_VALUE : [media_connector]}

        # defines how to connect the extracted product entities to other entities
        self.relation_mapping_entities = [{NAME_VALUE : "Product",
                                           RELATIONS_VALUE : [product_parent_nodes_relation,
                                                              product_media_relation]}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"Product" : {"media[0]" : ["primary_media", "primary_entities"]}}}}]

    def attribute_handler_get_sellable_status(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the subproducts associated with this product
        codigo = input_entity.get_attribute("CODIGO")
        sbprodut_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "sbprodut", AND_VALUE, "PRODUTO", EQUALS_VALUE, codigo)
        sbprodut_entities = input_intermediate_structure.get_entities_by_index(sbprodut_index)

        # marks the product as sellable in case it has no subproducts
        sellable_status = OMNI_NON_SELLABLE_TRANSACTIONAL_MERCHANDISE
        if not sbprodut_entities:
            sellable_status = OMNI_SELLABLE_TRANSACTIONAL_MERCHANDISE

        return sellable_status
