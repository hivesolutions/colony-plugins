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

COMMA_VALUE = ","

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

VAT_RATE_21 = 0.21
""" The 21% vat rate """

VAT_RATE_20 = 0.20
""" The 20% vat rate """

VAT_RATE_20_START_DATE = (2008, 07, 01)
""" Date when the 20% vat rate started being used """

OMNI_TRANSACTIONAL_MERCHANDISE_TYPES = ["Product", "SubProduct", "Service"]
""" The omni transactional merchandise types """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class SaleTransactionConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni SaleTransaction entities from diamante.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract sale transaction entities from dd_sales entities
        dd_sales_input_entities = {NAME_VALUE : "DD_Sales",
                                   OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "date",
                                                                                         ATTRIBUTE_NAME_VALUE : "Day"},
                                                                                        {NAME_VALUE : "discount",
                                                                                         ATTRIBUTE_NAME_VALUE : "Discount",
                                                                                         HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_calculate_discount,
                                                                                                            INPUT_DEPENDENCIES_VALUE : {"DD_Sales" : ["Day"]}}]},
                                                                                        {NAME_VALUE : "discount_vat",
                                                                                         ATTRIBUTE_NAME_VALUE : "Discount"},
                                                                                        {NAME_VALUE : "price",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "vat",
                                                                                         DEFAULT_VALUE_VALUE : 0},
                                                                                        {NAME_VALUE : "status",
                                                                                         DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract sale transaction entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "SaleTransaction",
                                                   INPUT_ENTITIES_VALUE : [dd_sales_input_entities]}]

        # connector used to populate the person buyer relation attribute
        person_buyer_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                  INPUT_DEPENDENCIES_VALUE : {"DD_Customer" : ["Id"],
                                                              "DD_Sales" : ["Customer"]},
                                  OUTPUT_DEPENDENCIES_VALUE : {"CustomerPerson" : []},
                                  ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Customer",
                                                     JOIN_ATTRIBUTES_VALUE : {"Id" : "Customer"},
                                                     OUTPUT_ENTITY_NAMES_VALUE : ["CustomerPerson"]}}

        # defines how to populate the sale transaction entities' person buyer relation attribute
        sale_transaction_person_buyer_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["person_buyer"],
                                                  RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sales"],
                                                  CONNECTORS_VALUE : [person_buyer_connector]}

        # connector used to populate the seller stockholder relation attribute
        seller_stockholder_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                        INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Name"],
                                                                    "DD_Sales" : ["Store"]},
                                        OUTPUT_DEPENDENCIES_VALUE : {"Store" : []},
                                        ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Company",
                                                           JOIN_ATTRIBUTES_VALUE : {"Name" : "Store"},
                                                           OUTPUT_ENTITY_NAMES_VALUE : ["Store"]}}

        # defines how to populate the sale transaction entities' store relation attribute
        sale_transaction_seller_stockholder_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["seller_stockholder"],
                                                        RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["sales_stockholder"],
                                                        CONNECTORS_VALUE : [seller_stockholder_connector]}

        # defines how to connect the extracted customer person entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "SaleTransaction",
                                           RELATIONS_VALUE : [sale_transaction_person_buyer_relation,
                                                              sale_transaction_seller_stockholder_relation]}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_create_sale_lines,
                                          INPUT_DEPENDENCIES_VALUE : {"DD_Sales" : ["Products"],
                                                                      "DD_Merchandise" : ["Id"]}}]

    def attribute_handler_calculate_discount(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the sale transaction's date
        day = input_entity.get_attribute("Day")

        # calculates the sale transaction's vat rate
        vat_rate = VAT_RATE_21
        if day >= apply(datetime.datetime, VAT_RATE_20_START_DATE):
            vat_rate = VAT_RATE_20

        # calculates the discount without vat
        output_attribute_value = float(output_attribute_value) / float((1 + vat_rate))

        return output_attribute_value

    def post_conversion_create_sale_lines(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_demo_data_plugin.info("Creating sale lines")

        # sums the attributes for every output entity of the specified name
        sale_transaction_entities = output_intermediate_structure.get_entities_by_name("SaleTransaction")
        for sale_transaction_entity in sale_transaction_entities:
            total_vat = 0
            total_price = 0
            total_discount = 0
            total_vat_rate = 0

            # retrieves the entity that originated the sale transaction entity
            output_entity_object_id = sale_transaction_entity.get_object_id()
            creator_input_entity_index = (INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, output_entity_object_id)
            creator_input_entity = input_intermediate_structure.get_entities_by_index(creator_input_entity_index)[0]

            # retrieves the unique identifiers for the merchandise sold in the sale transaction
            products = creator_input_entity.get_attribute("Products")
            product_string_ids = products[1:-1].split(COMMA_VALUE)
            product_ids = [int(product_string_id) for product_string_id in product_string_ids]

            vat = 0
            price = 0

            # retrieves the merchandise output entity associated with each specified merchandise, and
            # creates a sale line for it
            sale_line_entities = []
            for product_id in product_ids:

                # defines the index used to retrieve the creator input entity for the specified merchandise
                creator_input_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "DD_Merchandise",
                                              AND_VALUE, "Id", EQUALS_VALUE, product_id)

                # retrieves the merchandise creator input entity
                creator_input_entity = input_intermediate_structure.get_entities_by_index(creator_input_entity_index)[0]
                creator_input_entity_object_id = creator_input_entity.get_object_id()

                # retrieves the created merchandise output entity
                merchandise_entity = None
                for output_entity_name in OMNI_TRANSACTIONAL_MERCHANDISE_TYPES:
                    merchandise_entity_index = (OUTPUT_ENTITY_VALUE, WHERE_VALUE, INPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, creator_input_entity_object_id,
                                                CREATED_VALUE, OUTPUT_ENTITY_NAME_VALUE, EQUALS_VALUE, output_entity_name)

                    # tries to retrieve an output entity of the current type and breaks the loop in case it is found
                    merchandise_entities = output_intermediate_structure.get_entities_by_index(merchandise_entity_index)
                    if merchandise_entities:
                        merchandise_entity = merchandise_entities[0]
                        break

                unit_price = 0
                vat_rate = VAT_RATE_20
                unit_vat = 0

                # retrieves the price used in the sale and calculates the sale line value
                inventory_lines = merchandise_entity.get_attribute("contactable_organizational_units")
                inventory_line = inventory_lines[0]
                unit_price = inventory_line.get_attribute("price")
                vat_rate = VAT_RATE_20
                unit_vat = unit_price * vat_rate

                # adds the unit vat and unit price to the sale transaction totals
                vat += unit_vat
                price += unit_price

                # creates a sale line entity
                sale_line_entity = output_intermediate_structure.create_entity("SaleMerchandiseHierarchyTreeNode")
                sale_line_entity.set_attribute("status", OMNI_ACTIVE_ENTITY_STATUS)
                sale_line_entity.set_attribute("unit_discount", 0)
                sale_line_entity.set_attribute("quantity", 1)
                sale_line_entity.set_attribute("unit_price", unit_price)
                sale_line_entity.set_attribute("unit_vat", unit_vat)
                sale_line_entity.set_attribute("vat_rate", vat_rate)
                sale_line_entity.set_attribute("sale", sale_transaction_entity)
                sale_line_entity.set_attribute("merchandise", merchandise_entity)
                sale_line_entities.append(sale_line_entity)

                # adds the sale lines to the merchandise's relation attribute
                data_converter.connect_entities(merchandise_entity, "sale_lines", sale_line_entity)

            # sets the sale lines and their totals in the sale transaction
            sale_transaction_entity.set_attribute("price", price)
            sale_transaction_entity.set_attribute("vat", vat)
            sale_transaction_entity.set_attribute("sale_lines", sale_line_entities)

        return output_intermediate_structure
