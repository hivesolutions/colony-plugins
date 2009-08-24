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

EXCLUSION_LIST_VALUE = "exclusion_list"

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

class CategoryConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Category entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract category entities from estilo entities
        estilo_input_entities = {NAME_VALUE : "estilo",
                                 OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                       ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                       HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                          ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract category entities from pureza entities
        pureza_input_entities = {NAME_VALUE : "pureza",
                                 OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                       ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                       HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                          ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract category entities from qualidad entities
        qualidad_input_entities = {NAME_VALUE : "qualidad",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                         ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                            ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract category entities from talhe entities
        talhe_input_entities = {NAME_VALUE : "talhe",
                                OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                      ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                      HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                         ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract category entities from tipopeca entities
        tipopeca_input_entities = {NAME_VALUE : "tipopeca",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                         ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                            ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract category entities from tipoprod entities
        tipoprod_input_entities = {NAME_VALUE : "tipoprod",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                         ATTRIBUTE_NAME_VALUE : "DESCRICAO",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                            ARGUMENTS_VALUE : {EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}}]}]}]}

        # defines how to extract category entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Category",
                                                   INPUT_ENTITIES_VALUE : [estilo_input_entities,
                                                                           pureza_input_entities,
                                                                           qualidad_input_entities,
                                                                           talhe_input_entities,
                                                                           tipopeca_input_entities,
                                                                           tipoprod_input_entities]}]
