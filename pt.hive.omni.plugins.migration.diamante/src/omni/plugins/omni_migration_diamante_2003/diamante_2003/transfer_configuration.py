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

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

LOWERCASE_NAME_TOKENS = ["de", "do", "dos", "da", "das", "em", "e", "a", "o", "as", "os", "com", "para"]
""" List of name tokens that shouldn't be capitalized when a name is normalized """

class TransferConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Transfer entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract transfer entities from trfdocs entities
        trfdocs_input_entities = {NAME_VALUE : "trfdocs",
                                  OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "identifier",
                                                                                        ATTRIBUTE_NAME_VALUE : "NUMERO"},
                                                                                       {NAME_VALUE : "description",
                                                                                        ATTRIBUTE_NAME_VALUE : "APONTAMENT",
                                                                                        HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_capitalize_tokens",
                                                                                                           EXCLUSION_LIST_VALUE : LOWERCASE_NAME_TOKENS}]}]}]}

        # defines how to extract transfer entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Transfer",
                                                   INPUT_ENTITIES_VALUE : [trfdocs_input_entities]}]

        # connector used to populate the transfer's sender relation attribute
        sender_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                            INPUT_DEPENDENCIES_VALUE : {"lojas" : ["CODIGO"],
                                                        "trfdocs" : ["LOJA1"]},
                            OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                            ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "lojas",
                                               JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "LOJA1"},
                                               OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # defines how to populate the transfer entities' sender relation attribute
        transfer_sender_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sender"],
                                    RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sent_transfers"],
                                    CONNECTORS_VALUE : [sender_connector]}

        # connector used to populate the transfer's receiver relation attribute
        receiver_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                              INPUT_DEPENDENCIES_VALUE : {"lojas" : ["CODIGO"],
                                                          "trfdocs" : ["LOJA2"]},
                              OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                              ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "lojas",
                                                 JOIN_ATTRIBUTES_VALUE : {"CODIGO" : "LOJA2"},
                                                 OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # defines how to populate the transfer entities'receiver relation attribute
        transfer_receiver_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["receiver"],
                                      RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["received_transfers"],
                                      CONNECTORS_VALUE : [receiver_connector]}

        # defines how to connect the extracted transfer entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "Transfer",
                                           RELATIONS_VALUE : [transfer_sender_relation,
                                                              transfer_receiver_relation]}]
