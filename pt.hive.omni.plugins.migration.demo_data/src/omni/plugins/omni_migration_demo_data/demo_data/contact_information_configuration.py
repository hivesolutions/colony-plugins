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

DD_COMPANY_CONTACT_INFORMATION_ATTRIBUTES = ["Telephone", "Cellphone", "Emails"]
""" The contact information attributes in dd_company entities """

DD_CUSTOMER_CONTACT_INFORMATION_ATTRIBUTES = ["Telephone", "Cellphone", "Emails"]
""" The contact information attributes in dd_customer entities """

DD_SUPPLIER_CONTACT_INFORMATION_ATTRIBUTES = ["Contacts", "Contacts", "Emails"]
""" The contact information attributes in dd_supplier entities """

NEWLINE_CHARACTER = "\n"
""" The newline character in python """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class ContactInformationConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni ContactInformation entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract contact information entities from dd_company entities
        dd_company_input_entities = {NAME_VALUE : "DD_Company",
                                     OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                                    INPUT_DEPENDENCIES_VALUE : {"DD_Company" : DD_COMPANY_CONTACT_INFORMATION_ATTRIBUTES},
                                                                                    ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : DD_COMPANY_CONTACT_INFORMATION_ATTRIBUTES}}],
                                                               OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                                           ATTRIBUTE_NAME_VALUE : "Telephone",
                                                                                           HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                          {NAME_VALUE : "mobile_phone_number",
                                                                                           ATTRIBUTE_NAME_VALUE : "Cellphone",
                                                                                           HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                          {NAME_VALUE : "email",
                                                                                           ATTRIBUTE_NAME_VALUE : "Emails"},
                                                                                          {NAME_VALUE : "status",
                                                                                           DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract contact information entities from dd_customer entities
        dd_customer_input_entities = {NAME_VALUE : "DD_Customer",
                                      OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                                     INPUT_DEPENDENCIES_VALUE : {"DD_Customer" : DD_CUSTOMER_CONTACT_INFORMATION_ATTRIBUTES},
                                                                                     ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : DD_CUSTOMER_CONTACT_INFORMATION_ATTRIBUTES}}],
                                                                OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                                            ATTRIBUTE_NAME_VALUE : "Telephone",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "mobile_phone_number",
                                                                                            ATTRIBUTE_NAME_VALUE : "Cellphone",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "email",
                                                                                            ATTRIBUTE_NAME_VALUE : "Emails"},
                                                                                           {NAME_VALUE : "status",
                                                                                            DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract contact information entities from dd_supplier entities
        dd_supplier_input_entities = {NAME_VALUE : "DD_Supplier",
                                      OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_any_attribute",
                                                                                     INPUT_DEPENDENCIES_VALUE : {"DD_Supplier" : DD_SUPPLIER_CONTACT_INFORMATION_ATTRIBUTES},
                                                                                     ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : DD_SUPPLIER_CONTACT_INFORMATION_ATTRIBUTES}}],
                                                                OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "phone_number",
                                                                                            ATTRIBUTE_NAME_VALUE : "Contacts",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "mobile_phone_number",
                                                                                            ATTRIBUTE_NAME_VALUE : "Contacts",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "email",
                                                                                            ATTRIBUTE_NAME_VALUE : "Emails"},
                                                                                           {NAME_VALUE : "status",
                                                                                            DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract contact information entities
        self.attribute_mapping_output_entities =  [{NAME_VALUE : "ContactInformation",
                                                    INPUT_ENTITIES_VALUE : [dd_company_input_entities,
                                                                            dd_customer_input_entities,
                                                                            dd_supplier_input_entities]}]
