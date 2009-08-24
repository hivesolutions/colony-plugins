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

import string

ATTRIBUTES_VALUE = "attributes"

COMMA_VALUE = ","

MINUS_VALUE = "-"

PORTUGAL_VALUE = "Portugal"

OMNI_OFFICE_ADDRESS_TYPE = "Office"
""" The omni office address type """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class AddressConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Address entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract address entities from the dd_company entities
        dd_company_input_entities = {NAME_VALUE : "DD_Company",
                                     OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attributes",
                                                                                    INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Addresses"]},
                                                                                    ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : ["Addresses"]}}],
                                                               HANDLERS_VALUE : [{FUNCTION_VALUE : self.entity_handler_parse_address}],
                                                               OUTPUT_ATTRIBUTES_VALUE : []}]}


        # defines how to extract address entities from the dd_customer entities
        dd_customer_input_entities = {NAME_VALUE : "DD_Customer",
                                      OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attributes",
                                                                                     INPUT_DEPENDENCIES_VALUE : {"DD_Customer" : ["Addresses"]},
                                                                                     ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : ["Addresses"]}}],
                                                                HANDLERS_VALUE : [{FUNCTION_VALUE : self.entity_handler_parse_address}],
                                                                OUTPUT_ATTRIBUTES_VALUE : []}]}

        # defines how to extract address entities from the dd_supplier entities
        dd_supplier_input_entities = {NAME_VALUE : "DD_Supplier",
                                      OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attributes",
                                                                                     INPUT_DEPENDENCIES_VALUE : {"DD_Supplier" : ["Addresses"]},
                                                                                     ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : ["Addresses"]}}],
                                                                HANDLERS_VALUE : [{FUNCTION_VALUE : self.entity_handler_parse_address}],
                                                                OUTPUT_ATTRIBUTES_VALUE : []}]}

        # defines how to extract address entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Address",
                                                   INPUT_ENTITIES_VALUE : [dd_company_input_entities,
                                                                           dd_customer_input_entities,
                                                                           dd_supplier_input_entities]}]

    def entity_handler_parse_address(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, arguments):
        # splits the address into tokens
        addresses = input_entity.get_attribute("Addresses")
        address_tokens = addresses.split(COMMA_VALUE)

        # parses the first token
        street_name = address_tokens[0].strip().capitalize()

        # parses the second token in case it exists
        number_floor = None
        door_number = None
        floor = None
        if len(address_tokens) > 1:
            number_floor = address_tokens[1].strip()
            door_number = address_tokens[1].strip()

        # parses the third token in case it exists
        zip_code = None
        zip_code_name = None
        if len(address_tokens) > 2:
            zip_code = address_tokens[2].strip()

        # parses the building number floor number token
        if number_floor:
            if MINUS_VALUE in number_floor:
                number_floor_tokens = number_floor.split(MINUS_VALUE)
                door_number = number_floor_tokens[0].strip()
                floor = number_floor_tokens[1].strip()

        # parses the zip code token
        if zip_code:

            # iterates through the zip code from back to front until
            zip_code_number = None
            zip_code_indexes = range(len(zip_code))
            zip_code_indexes.reverse()
            zip_code_name = ""
            for zip_code_index in zip_code_indexes:
                zip_code_character = zip_code[zip_code_index]

                # escapes the loop in case a digit is found, splitting
                # the zip code into a number and name
                if zip_code_character in string.digits:
                    zip_code_number = zip_code[:zip_code_index + 1]
                    break

                zip_code_name += zip_code_character

            # sets the retrieved zip code number
            zip_code = zip_code_number

            # inverts the extracted zip code name
            zip_code_name = list(zip_code_name)
            zip_code_name.reverse()
            zip_code_name = "".join(zip_code_name).strip().capitalize()

        # sets the address's attributes
        output_entity.set_attribute("address_type", OMNI_OFFICE_ADDRESS_TYPE)
        output_entity.set_attribute("street_name", street_name)
        output_entity.set_attribute("door_number", door_number)
        output_entity.set_attribute("floor", floor)
        output_entity.set_attribute("city", zip_code_name)
        output_entity.set_attribute("zip_code", zip_code)
        output_entity.set_attribute("zip_code_name", zip_code_name)
        output_entity.set_attribute("country", PORTUGAL_VALUE)

        return output_entity
