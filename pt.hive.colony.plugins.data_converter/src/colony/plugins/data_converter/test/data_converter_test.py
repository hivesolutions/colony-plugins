#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1026 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-19 23:05:23 +0000 (seg, 19 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import unittest
import os.path

class DataConverterTest:
    """
    The data converter plugin unit test class.
    """

    data_converter_test_plugin = None
    """ The base data test plugin """

    def __init__(self, data_converter_test_plugin):
        """
        Constructor of the class.

        @type data_converter_test_plugin: DataConverterTestPlugin
        @param data_converter_test_plugin: The data converter test plugin.
        """

        self.data_converter_test_plugin = data_converter_test_plugin

    def get_plugin_test_case_bundle(self):
        return [DataConverterTestPluginTestCase]

class DataConverterTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin.info("Setting up Data Converter Test Case...")

        # retrieves the resource manager plugin
        resource_manager_plugin = self.plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # retrieves the data converter plugin
        self.data_converter_plugin = self.plugin.data_converter_plugin

        # retrieves the intermediate structure plugin
        self.intermediate_structure_plugin = self.plugin.intermediate_structure_plugin

        # creates the path where to store the serialized input intermediate structures used in the test
        self.test_intermediate_structure_file_path = os.path.join(user_home_path, "test_intermediate_structure.pickle")

    def test_convert_data(self):
        # creates the input intermediate structure where to start the conversion from
        intermediate_structure = self.intermediate_structure_plugin.create_intermediate_structure()
        client_entity = intermediate_structure.create_entity("client")
        client_entity.set_attribute("customer_type", "person")
        client_entity.set_attribute("name", "customer person")
        client_entity.set_attribute("telephone", "1234")
        client_entity.set_attribute("fax", "4321")
        client_entity.set_attribute("street", "person street name")
        client_entity = intermediate_structure.create_entity("client")
        client_entity.set_attribute("customer_type", "company")
        client_entity.set_attribute("name", "customer company")
        client_entity.set_attribute("telephone", "5678")
        client_entity.set_attribute("fax", "8765")
        client_entity.set_attribute("street", "company street name")

        # defines the output options
        input_output_options = {"io_adapter_plugin_id" : "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle",
                                "file_path" : self.test_intermediate_structure_file_path}

        # saves the input intermediate structure
        self.intermediate_structure_plugin.save(intermediate_structure, "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle", input_output_options)

        # defines the attribute mapping options
        customer_output_attributes = [{"name" : "name",
                                       "attribute_name" : "name",
                                       "handlers" : [self.capitalize_name]}]
        client_output_entities = [{"name" : "pt.hive.CustomerPerson",
                                   "validators" : [self.is_customer_person_entity],
                                   "output_attributes" : customer_output_attributes},
                                  {"name" : "pt.hive.CustomerCompany",
                                   "validators" : [self.is_customer_company_entity],
                                   "output_attributes" : customer_output_attributes},
                                  {"name" : "pt.hive.ContactInformation",
                                   "output_attributes" : [{"name": "phone_number",
                                                           "attribute_name" : "telephone"}]},
                                  {"name" : "pt.hive.ContactInformation",
                                   "output_attributes" : [{"name": "fax_number",
                                                           "attribute_name" : "fax"}]},
                                  {"name" : "pt.hive.Address",
                                   "output_attributes" : [{"name": "street_name",
                                                           "attribute_name" : "street"}]}]
        attribute_mapping = {"input_entities" : [{"name" : "client",
                                                  "output_entities" : client_output_entities}]}

        # defines the relation mapping options
        customer_person_address_relation = {"name" : "pt.hive.CustomerPerson",
                                            "relations" : [{"entity_relation_attribute_names" : ["addresses"],
                                                            "related_entity_relation_attribute_names" : ["contactable_organizational_hierarchy_tree_node"],
                                                            "index" : self.get_creator_index("client", "pt.hive.Address")}]}
        customer_person_contact_information_relation = {"name" : "pt.hive.CustomerPerson",
                                                        "relations" : [{"entity_relation_attribute_names" : ["contact_informations"],
                                                                        "related_entity_relation_attribute_names" : ["contactable_organizational_hierarchy_tree_node"],
                                                                        "index" : self.get_creator_index("client", "pt.hive.ContactInformation")}]}
        customer_company_address_relation = {"name" : "pt.hive.CustomerCompany",
                                             "relations" : [{"entity_relation_attribute_names" : ["addresses"],
                                                             "related_entity_relation_attribute_names" : ["contactable_organizational_hierarchy_tree_node"],
                                                             "index" : self.get_creator_index("client", "pt.hive.Address")}]}
        customer_company_contact_information_relation = {"name" : "pt.hive.CustomerCompany",
                                                         "relations" : [{"entity_relation_attribute_names" : ["contact_informations"],
                                                                         "related_entity_relation_attribute_names" : ["contactable_organizational_hierarchy_tree_node"],
                                                                         "index" : self.get_creator_index("client", "pt.hive.ContactInformation")}]}
        relation_mapping = {"entities" : [customer_person_address_relation, customer_person_contact_information_relation, customer_company_address_relation, customer_company_contact_information_relation]}

        conversion_options = {"map_data" : True,
                              "attribute_mapping" : attribute_mapping,
                              "relation_mapping" : relation_mapping}

        # converts the data
        self.data_converter_plugin.convert_data(input_output_options, input_output_options, conversion_options)

        # loads the results of the data conversion operation
        self.intermediate_structure_plugin.load(intermediate_structure, "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle", input_output_options)

        # retrieves the entities that were the result of the conversion
        customer_company_entities = intermediate_structure.get_entities("pt.hive.CustomerCompany")
        self.assertEquals(len(customer_company_entities), 1)
        customer_person_entities = intermediate_structure.get_entities("pt.hive.CustomerPerson")
        self.assertEquals(len(customer_person_entities), 1)
        address_entities = intermediate_structure.get_entities("pt.hive.Address")
        self.assertEquals(len(address_entities), 2)
        contact_information_entities = intermediate_structure.get_entities("pt.hive.ContactInformation")
        self.assertEquals(len(contact_information_entities), 4)

        # test the customer person entity
        customer_person_entity = customer_person_entities[0]
        self.assertEquals(len(customer_person_entity.get_attributes()), 3)
        self.assertEquals(customer_person_entity.get_attribute("name"), "Customer Person")
        self.assertEquals(len(customer_person_entity.get_attribute("addresses").get_attributes()), 2)
        self.assertEquals(customer_person_entity.get_attribute("addresses").get_attribute("street_name"), "person street name")
        self.assertEquals(customer_person_entity.get_attribute("addresses").get_attribute("contactable_organizational_hierarchy_tree_node"), customer_person_entity)
        self.assertEquals(len(customer_person_entity.get_attribute("contact_informations")), 2)
        for contact_information_entity in customer_person_entity.get_attribute("contact_informations"):
            if contact_information_entity.has_attribute("phone_number"):
                self.assertEquals(contact_information_entity.get_attribute("phone_number"), "1234")
            else:
                self.assertEquals(contact_information_entity.get_attribute("fax_number"), "4321")
            self.assertEquals(contact_information_entity.get_attribute("contactable_organizational_hierarchy_tree_node"), customer_person_entity)

        # test the customer company entity
        customer_company_entity = customer_company_entities[0]
        self.assertEquals(len(customer_company_entity.get_attributes()), 3)
        self.assertEquals(customer_company_entity.get_attribute("name"), "Customer Company")
        self.assertEquals(len(customer_company_entity.get_attribute("addresses").get_attributes()), 2)
        self.assertEquals(customer_company_entity.get_attribute("addresses").get_attribute("street_name"), "company street name")
        self.assertEquals(customer_company_entity.get_attribute("addresses").get_attribute("contactable_organizational_hierarchy_tree_node"), customer_company_entity)
        self.assertEquals(len(customer_company_entity.get_attribute("contact_informations")), 2)
        for contact_information_entity in customer_company_entity.get_attribute("contact_informations"):
            if contact_information_entity.has_attribute("phone_number"):
                self.assertEquals(contact_information_entity.get_attribute("phone_number"), "5678")
            else:
                self.assertEquals(contact_information_entity.get_attribute("fax_number"), "8765")
            self.assertEquals(contact_information_entity.get_attribute("contactable_organizational_hierarchy_tree_node"), customer_company_entity)

    def tearDown(self):
        self.plugin.info("Tearing down Data Converter Test Case...")

        # removes the test intermediate structure file
        if os.path.exists(self.test_intermediate_structure_file_path):
            os.remove(self.test_intermediate_structure_file_path)

    def is_customer_person_entity(self, entity):
        if entity.get_attribute("customer_type") == "person":
            return True
        return False

    def is_customer_company_entity(self, entity):
        if entity.get_attribute("customer_type") == "company":
            return True
        return False

    def capitalize_name(self, name):
        name_tokens = name.split(" ")
        name = "".join([(name_token.capitalize() + " ") for name_token in name_tokens])[:-1]

        return name

    def get_creator_index(self, input_entity_name, output_entity_name):
        return (("constant", "input_entity_object_id"),
                ("constant", input_entity_name),
                ("constant", "="),
                ("function", self.get_input_entity_object_id),
                ("constant", "created"),
                ("constant", "output_entity_name"),
                ("constant", "="),
                ("constant", output_entity_name))

    def get_input_entity_object_id(self, input_entity, output_entity):
        return input_entity.get_object_id()

class DataConverterTestPluginTestCase:

    @staticmethod
    def get_test_case():
        return DataConverterTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Data Converter Test Plugin test case covering the data converter testing"
