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

EXCLUSION_LIST_VALUE = "exclusion_list"

OUTPUT_ATTRIBUTE_NAMES_VALUE = "output_attribute_names"

CLIENTES_FIRST_ADDRESS_INPUT_ATTRIBUTES = ["MORADA1", "LOCALIDAD1", "CODPOS1", "PAIS1"]
""" List with the names of the input attributes used to create the first address from a clientes entity """

CLIENTES_SECOND_ADDRESS_INPUT_ATTRIBUTES = ["MORADA2", "LOCALIDAD2", "CODPOS2", "PAIS2"]
""" List with the names of the input attributes used to create the first address from a clientes entity """

EMPRESAS_ADDRESS_INPUT_ATTRIBUTES = ["MORADA", "LOCALIDADE", "CODIPOS"]
""" List with the names of the input attributes used to create an address from a empresas entity """

FORNECED_ADDRESS_INPUT_ATTRIBUTES = ["MORADA", "LOCALIDAD", "CODPOS", "PAIS"]
""" List with the names of the input attributes used to create an address from a forneced entity """

LOJAS_ADDRESS_INPUT_ATTRIBUTES = ["MORADA", "LOCAL"]
""" List with the names of the input attributes used to create an address from a lojas entity """

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

class AddressConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Address entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract address entities from the clientes entities
        clientes_input_entities = {NAME_VALUE : "clientes",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"clientes" : CLIENTES_FIRST_ADDRESS_INPUT_ATTRIBUTES},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : CLIENTES_FIRST_ADDRESS_INPUT_ATTRIBUTES}}],
                                                             HANDLERS_VALUE : [{FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                                ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["street_name", "zip_code_name"],
                                                                                                   EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "street_name",
                                                                                         ATTRIBUTE_NAME_VALUE : "MORADA1"},
                                                                                        {NAME_VALUE : "zip_code_name",
                                                                                         ATTRIBUTE_NAME_VALUE : "LOCALIDAD1"},
                                                                                        {NAME_VALUE : "zip_code",
                                                                                         ATTRIBUTE_NAME_VALUE : "CODPOS1"},
                                                                                         # @todo: this is a lugar da joia customization
                                                                                        {NAME_VALUE : "description",
                                                                                         ATTRIBUTE_NAME_VALUE : "MORADA2",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                            ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]},
                                                                                        {NAME_VALUE : "country",
                                                                                         ATTRIBUTE_NAME_VALUE : "PAIS1",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_get_country_name,
                                                                                                            INPUT_DEPENDENCIES_VALUE : {"paises" : ["CODIGO", "DESCRICAO"]}}]}]}]}

        # defines how to extract address entities from empresas entities
        empresas_input_entities = {NAME_VALUE : "empresas",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"empresas" : EMPRESAS_ADDRESS_INPUT_ATTRIBUTES},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : EMPRESAS_ADDRESS_INPUT_ATTRIBUTES}}],
                                                             HANDLERS_VALUE : [{FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                                ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["street_name", "zip_code_name"],
                                                                                                   EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "street_name",
                                                                                         ATTRIBUTE_NAME_VALUE : "MORADA"},
                                                                                        {NAME_VALUE : "zip_code_name",
                                                                                         ATTRIBUTE_NAME_VALUE : "LOCALIDADE"},
                                                                                        {NAME_VALUE : "zip_code",
                                                                                         ATTRIBUTE_NAME_VALUE : "CODIPOS"}]}]}

        # defines how to extract address entities from forneced entities
        forneced_input_entities = {NAME_VALUE : "forneced",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"forneced" : FORNECED_ADDRESS_INPUT_ATTRIBUTES},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : FORNECED_ADDRESS_INPUT_ATTRIBUTES}}],
                                                             HANDLERS_VALUE : [{FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                                ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["street_name", "zip_code_name"],
                                                                                                   EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "street_name",
                                                                                         ATTRIBUTE_NAME_VALUE : "MORADA"},
                                                                                        {NAME_VALUE : "zip_code_name",
                                                                                         ATTRIBUTE_NAME_VALUE : "LOCALIDAD"},
                                                                                        {NAME_VALUE : "zip_code",
                                                                                         ATTRIBUTE_NAME_VALUE : "CODPOS"},
                                                                                        {NAME_VALUE : "country",
                                                                                         ATTRIBUTE_NAME_VALUE : "PAIS",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_get_country_name,
                                                                                                            INPUT_DEPENDENCIES_VALUE : {"paises" : ["CODIGO", "DESCRICAO"]}}]}]}]}

        # defines how to extract address entities from lojas entities
        lojas_input_entities = {NAME_VALUE : "lojas",
                                OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                               INPUT_DEPENDENCIES_VALUE : {"lojas" : LOJAS_ADDRESS_INPUT_ATTRIBUTES},
                                                                               ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : LOJAS_ADDRESS_INPUT_ATTRIBUTES}}],
                                                          HANDLERS_VALUE : [{FUNCTION_VALUE : "entity_handler_capitalize_tokens",
                                                                             ARGUMENTS_VALUE : {OUTPUT_ATTRIBUTE_NAMES_VALUE : ["street_name", "zip_code_name"],
                                                                                                EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}],
                                                          OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "street_name",
                                                                                      ATTRIBUTE_NAME_VALUE : "MORADA"},
                                                                                     {NAME_VALUE : "zip_code_name",
                                                                                      ATTRIBUTE_NAME_VALUE : "LOCAL"}]}]}

        # defines how to extract address entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Address",
                                                   INPUT_ENTITIES_VALUE : [clientes_input_entities,
                                                                           empresas_input_entities,
                                                                           forneced_input_entities,
                                                                           lojas_input_entities]}]

    def attribute_handler_get_country_name(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the name of the country specified by the diamante country identifier
        if output_attribute_value:
            paises_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "paises", AND_VALUE, "CODIGO", EQUALS_VALUE, output_attribute_value)
            paises_entity = input_intermediate_structure.get_entities_by_index(paises_entity_index)[0]
            output_attribute_value = paises_entity.get_attribute("DESCRICAO")

        return output_attribute_value
