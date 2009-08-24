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

ATTRIBUTE_NAMES_VALUE = "attribute_names"

CREATOR_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE = "creator_entity_non_null_attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

DIAMANTE_CREDIT_NOTE_PAYMENT_TYPE = "NCR"
""" The credit note payment indicator in diamante """

OMNI_USED_CREDIT_NOTE_STATUS = 1
""" The used credit note status in omni """

class CreditNotePaymentConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni CreditNotePayment entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract credit note entities from fpvendas entities
        fpvendas_input_entities = {NAME_VALUE : "fpvendas",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attributes",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"fpvendas" : ["DOCUMENTO"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : ["DOCUMENTO"]}},
                                                                                 {FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"fpvendas" : ["FORMA"]},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"FORMA" : DIAMANTE_CREDIT_NOTE_PAYMENT_TYPE}}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : []}]}

        # defines how to extract credit note payment entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "CreditNotePayment",
                                                   INPUT_ENTITIES_VALUE : [fpvendas_input_entities]}]

        # connector used to populate the credit notes relation attribute
        credit_notes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                  INPUT_DEPENDENCIES_VALUE : {"vendas" : ["TIPODOC", "DOCUMENTO"],
                                                              "fpvendas" : ["FORMA", "DOCUMENTO"]},
                                  ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "vendas",
                                                     CREATOR_ENTITY_NON_NULL_ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO"],
                                                     JOIN_ATTRIBUTES_VALUE : {"TIPODOC" : "FORMA",
                                                                              "DOCUMENTO" : "DOCUMENTO"},
                                                     OUTPUT_ENTITY_NAMES_VALUE : ["CreditNote"]}}

        # defines how to connect sale merchandise hierarchy tree node entities with merchandise entities
        credit_note_payment_credit_notes_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["credit_notes"],
                                                     RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["credit_note_payment"],
                                                     CONNECTORS_VALUE : [credit_notes_connector]}

        # defines how to connect the extracted sale merchandise hierarchy tree node entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "CreditNotePayment",
                                           RELATIONS_VALUE : [credit_note_payment_credit_notes_relation]}]

        # defines how to index the loaded input intermediate structure entities
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["vendas"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"vendas" : ["DOCUMENTO", "TIPODOC"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["DOCUMENTO", "TIPODOC"]}}]

        # defines the handlers that should be executed when the conversion process is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_mark_used_credit_notes,
                                          OUTPUT_DEPENDENCIES_VALUE : {"CreditNote" : []}}]

    def post_conversion_handler_mark_used_credit_notes(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_plugin.info("Marking used credit notes")

        # marks all credit notes associated with credit note payments as used
        credit_note_payment_entities = output_intermediate_structure.get_entities_by_name("CreditNotePayment")
        for credit_note_payment_entity in credit_note_payment_entities:

            # marks this credit note payment's credit notes as used
            credit_note_entities = credit_note_payment_entity.get_attribute("credit_notes")
            for credit_note_entity in credit_note_entities:
                credit_note_entity.set_attribute("credit_note_status", OMNI_USED_CREDIT_NOTE_STATUS)

        return output_intermediate_structure
