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

CLIENTES_FIRST_CONTACT_INFORMATION_ATTRIBUTES = ["TEL1", "MOVEL", "FAX", "EMAIL", "URL"]
""" List with the names of the input attributes used to create the first contact information from a clientes entity """

CLIENTES_SECOND_CONTACT_INFORMATION_ATTRIBUTES = ["TEL2"]
""" List with the names of the input attributes used to create the second contact information from a clientes entity """

CLIENTES_THIRD_CONTACT_INFORMATION_ATTRIBUTES = ["TEL3"]
""" List with the names of the input attributes used to create the third contact information from a clientes entity """

EMPRESAS_CONTACT_INFORMATION_ATTRIBUTES = ["TELEFONE", "FAX"]
""" List with the names of the input attributes used to create a contact information from a empresas entity """

FORNECED_FIRST_CONTACT_INFORMATION_ATTRIBUTES = ["TEL1", "MOVEL", "FAX", "EMAIL", "URL"]
""" List with the names of the input attributes used to create the first contact information from a forneced entity """

FORNECED_SECOND_CONTACT_INFORMATION_ATTRIBUTES = ["TEL2"]
""" List with the names of the input attributes used to create the second contact information from a forneced entity """

FORNECED_THIRD_CONTACT_INFORMATION_ATTRIBUTES = ["TEL3"]
""" List with the names of the input attributes used to create the third contact information from a forneced entity """

LOJAS_CONTACT_INFORMATION_ATTRIBUTES = ["TELEFONE", "FAX", "EMAIL"]
""" List with the names of the input attributes used to create a contact information from a lojas entity """

class ContactInformationConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni ContactInformation entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract the first contact information entity from each clientes entity
        clientes_first_input_entities = {VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                              INPUT_DEPENDENCIES_VALUE : {"clientes" : CLIENTES_FIRST_CONTACT_INFORMATION_ATTRIBUTES},
                                                              ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : CLIENTES_FIRST_CONTACT_INFORMATION_ATTRIBUTES}}],
                                         OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                     ATTRIBUTE_NAME_VALUE : "TEL1"},
                                                                    {NAME_VALUE : "mobile_phone_number",
                                                                     ATTRIBUTE_NAME_VALUE : "MOVEL"},
                                                                    {NAME_VALUE : "fax_number",
                                                                     ATTRIBUTE_NAME_VALUE : "FAX"},
                                                                    {NAME_VALUE : "email",
                                                                     ATTRIBUTE_NAME_VALUE : "EMAIL",
                                                                     HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_string_to_lowercase"}]},
                                                                    {NAME_VALUE : "web_page",
                                                                     ATTRIBUTE_NAME_VALUE : "URL",
                                                                     HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_string_to_lowercase"}]}]}

        # defines how to extract the second contact information entity from each clientes entity
        clientes_second_input_entities = {VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                               INPUT_DEPENDENCIES_VALUE : {"clientes" : CLIENTES_SECOND_CONTACT_INFORMATION_ATTRIBUTES},
                                                               ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : CLIENTES_SECOND_CONTACT_INFORMATION_ATTRIBUTES}}],
                                          OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                      ATTRIBUTE_NAME_VALUE : "TEL2"}]}

        # defines how to extract the third contact information entity from each clientes entity
        clientes_third_input_entities = {VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                              INPUT_DEPENDENCIES_VALUE : {"clientes" : CLIENTES_THIRD_CONTACT_INFORMATION_ATTRIBUTES},
                                                              ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : CLIENTES_THIRD_CONTACT_INFORMATION_ATTRIBUTES}}],
                                         OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                     ATTRIBUTE_NAME_VALUE : "TEL3"}]}

        # defines how to extract contact information entities from clientes entities
        clientes_input_entities = {NAME_VALUE : "clientes",
                                   OUTPUT_ENTITIES_VALUE : [clientes_first_input_entities,
                                                            clientes_second_input_entities,
                                                            clientes_third_input_entities]}

        # defines how to extract contact information entities from empresas entities
        empresas_input_entities = {NAME_VALUE : "empresas",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"empresas" : EMPRESAS_CONTACT_INFORMATION_ATTRIBUTES},
                                                                                  ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : EMPRESAS_CONTACT_INFORMATION_ATTRIBUTES}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                                         ATTRIBUTE_NAME_VALUE : "TELEFONE"},
                                                                                        {NAME_VALUE : "fax_number",
                                                                                         ATTRIBUTE_NAME_VALUE : "FAX"}]}]}

        # defines how to extract the first contact information entity from each forneced entity
        forneced_first_input_entities = {VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                              INPUT_DEPENDENCIES_VALUE : {"forneced" : FORNECED_FIRST_CONTACT_INFORMATION_ATTRIBUTES},
                                                              ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : FORNECED_FIRST_CONTACT_INFORMATION_ATTRIBUTES}}],
                                         OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                     ATTRIBUTE_NAME_VALUE : "TEL1"},
                                                                    {NAME_VALUE : "mobile_phone_number",
                                                                     ATTRIBUTE_NAME_VALUE : "MOVEL"},
                                                                    {NAME_VALUE : "fax_number",
                                                                     ATTRIBUTE_NAME_VALUE : "FAX"},
                                                                    {NAME_VALUE : "email",
                                                                     ATTRIBUTE_NAME_VALUE : "EMAIL",
                                                                     HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_string_to_lowercase"}]},
                                                                    {NAME_VALUE : "web_page",
                                                                     ATTRIBUTE_NAME_VALUE : "URL",
                                                                     HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_string_to_lowercase"}]}]}

        # defines how to extract the second contact information entity from each forneced entity
        forneced_second_input_entities = {VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                               INPUT_DEPENDENCIES_VALUE : {"forneced" : FORNECED_SECOND_CONTACT_INFORMATION_ATTRIBUTES},
                                                               ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : FORNECED_SECOND_CONTACT_INFORMATION_ATTRIBUTES}}],
                                          OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                      ATTRIBUTE_NAME_VALUE : "TEL2"}]}

        # defines how to extract the third contact information entity from each forneced entity
        forneced_third_input_entities = {VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                              INPUT_DEPENDENCIES_VALUE : {"forneced" : FORNECED_THIRD_CONTACT_INFORMATION_ATTRIBUTES},
                                                              ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : FORNECED_THIRD_CONTACT_INFORMATION_ATTRIBUTES}}],
                                         OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                     ATTRIBUTE_NAME_VALUE : "TEL3"}]}

        # defines how to extract contact information entities from forneced entities
        forneced_input_entities = {NAME_VALUE : "forneced",
                                   OUTPUT_ENTITIES_VALUE : [forneced_first_input_entities,
                                                            forneced_second_input_entities,
                                                            forneced_third_input_entities]}

        # defines how to extract contact information entities from lojas entities
        lojas_input_entities = {NAME_VALUE : "lojas",
                                OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                               INPUT_DEPENDENCIES_VALUE : {"lojas" : LOJAS_CONTACT_INFORMATION_ATTRIBUTES},
                                                                               ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : LOJAS_CONTACT_INFORMATION_ATTRIBUTES}}],
                                                          OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                                      ATTRIBUTE_NAME_VALUE : "TELEFONE"},
                                                                                     {NAME_VALUE : "fax_number",
                                                                                      ATTRIBUTE_NAME_VALUE : "FAX"},
                                                                                     {NAME_VALUE : "email",
                                                                                      ATTRIBUTE_NAME_VALUE : "EMAIL",
                                                                                      HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_string_to_lowercase"}]}]}]}

        # defines how to extract contact information entities
        self.attribute_mapping_output_entities =  [{NAME_VALUE : "ContactInformation",
                                                    INPUT_ENTITIES_VALUE : [clientes_input_entities,
                                                                            empresas_input_entities,
                                                                            forneced_input_entities,
                                                                            lojas_input_entities]}]
