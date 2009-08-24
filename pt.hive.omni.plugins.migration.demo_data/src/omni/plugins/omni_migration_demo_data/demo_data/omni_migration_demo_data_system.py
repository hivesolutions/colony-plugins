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

import os
import types
import time
import datetime

AND_VALUE = "and"

ARGUMENTS_VALUE = "arguments"

ATTRIBUTE_NAME_VALUE = "attribute_name"

ATTRIBUTE_MAPPING_VALUE = "attribute_mapping"

CREATED_VALUE = "created"

CONNECTORS_VALUE = "connectors"

DEFAULT_VALUE_VALUE = "default_value"

ENTITIES_VALUE = "entities"

ENTITY_NAME_VALUE = "entity_name"

ENTITY_NAMES_VALUE = "entity_names"

ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE = "entity_relation_attribute_names"

EQUALS_VALUE = "="

FUNCTION_VALUE = "function"

HANDLERS_VALUE = "handlers"

INPUT_ATTRIBUTE_HANDLERS_VALUE = "input_attribute_handlers"

INPUT_DEPENDENCIES_VALUE = "input_dependencies"

INPUT_ENTITY_OBJECT_ID_VALUE = "input_entity_object_id"

INPUT_ENTITY_VALUE = "input_entity"

INPUT_ENTITIES_VALUE = "input_entities"

IO_ADAPTER_PLUGIN_ID_VALUE = "io_adapter_plugin_id"

LIST_TYPE_VALUE = "list_type"

TYPES_VALUE = "types"

NAME_VALUE = "name"

OUTPUT_ATTRIBUTES_VALUE = "output_attributes"

OUTPUT_ATTRIBUTE_HANDLERS_VALUE = "output_attribute_handlers"

OUTPUT_DEPENDENCIES_VALUE = "output_dependencies"

OUTPUT_ENTITIES_VALUE = "output_entities"

OUTPUT_ENTITY_VALUE = "output_entity"

OUTPUT_ENTITY_NAME_VALUE = "output_entity_name"

OUTPUT_ENTITY_OBJECT_ID_VALUE = "output_entity_object_id"

POST_CONVERSION_HANDLERS_VALUE = "post_conversion_handlers"

RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE = "related_entity_relation_attribute_names"

RELATION_MAPPING_VALUE = "relation_mapping"

RELATIONS_VALUE = "relations"

VALIDATORS_VALUE = "validators"

WHERE_VALUE = "where"

IMPORT_MODULE_NAMES = ["address_configuration",
                       "category_configuration",
                       "collection_configuration",
                       "company_configuration",
                       "contact_information_configuration",
                       "customer_hierarchy_tree_configuration",
                       "customer_person_configuration",
                       "department_configuration",
                       "employee_configuration",
                       "media_configuration",
                       "merchandise_contactable_organizational_hierarchy_tree_node_configuration",
                       "merchandise_hierarchy_tree_configuration",
                       "organizational_hierarchy_merchandise_supplier_configuration",
                       "organizational_hierarchy_tree_configuration",
                       "organizational_merchandise_hierarchy_tree_node_vat_class_configuration",
                       "product_configuration",
                       "sale_transaction_configuration",
                       "service_configuration",
                       "store_configuration",
                       "sub_product_configuration",
                       "supplier_company_configuration",
                       "supplier_hierarchy_tree_configuration",
                       "system_company_configuration",
                       "warehouse_configuration",
                       "user_configuration",
                       "vat_class_configuration"]

ATTRIBUTE_NAMES_VALUE = "attribute_names"

FILE_PATH_VALUE = "file_path"

ENTITY_MANAGER_ENGINE_VALUE = "entity_manager_engine"

ENTITY_MANAGER_SQLITE_ENGINE_VALUE = "sqlite"

DIRECTORY_PATHS_VALUE = "directory_paths"

TOKEN_SEPARATOR_VALUE = "token_separator"

FILE_NAME_REGEX_VALUE = "file_name_regex"

SEMI_COLON_VALUE = ";"

COMMA_VALUE = ","

DOT_VALUE = "."

UTF8_VALUE = "utf8"

EURO_CURRENCY_SYMBOL = "€"
""" The euro currency symbol """

PERCENTAGE_SYMBOL = "%"
""" The percentage symbol """

ENTITY_MANAGER_SQLITE_ENGINE_VALUE = "sqlite"
""" Engine to use the entity manager with """

DEMO_DATA_DIRECTORY_NAME = "demo_data"
""" Name of the directory where the demo data is located """

OUTPUT_DATABASE_FILE_NAME = "omni_database_demo_data.sqlite"
""" Name of the file where to output the migrated date to """

DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
""" Format used to parse dates with times """

DATE_FORMAT = "%d-%m-%Y"
""" Format used to parse dates """

IO_ADAPTER_CSV_PLUGIN_ID = "pt.hive.colony.plugins.data_converter.io_adapter.csv"
""" Unique identifier for the csv io adapter plugin """

IO_ADAPTER_ENTITY_MANAGER_PLUGIN_ID = "pt.hive.colony.plugins.data_converter.io_adapter.entity_manager"
""" Unique identifier for the entity manager io adapter plugin """

class OmniMigrationDemoData:
    """
    Configuration specifying how to migrate demo data
    to omni.
    """

    omni_migration_demo_data_plugin = None
    """ Demo Data to Omni migration plugin """

    attribute_mapping_output_entities = []
    """ Attribute mapping output entity configurations provided by this configuration """

    attribute_mapping_output_attributes = []
    """ Attribute mapping output attribute configurations provided by this configuration """

    relation_mapping_entities = []
    """ Relation mapping entity configurations provided by this configuration """

    relation_mapping_relations = []
    """ Relation mapping relation configurations provided by this configuration """

    input_entity_indexers = []
    """ Indexers to apply to the input intermediate structure """

    output_entity_indexers = []
    """ Indexers to apply to the output intermediate structure """

    post_attribute_mapping_handlers = []
    """ List of post attribute mapping handlers provided by this configuration """

    post_relation_mapping_handlers = []
    """ List of post relation mapping handlers provided by this configuration """

    post_conversion_handlers = []
    """ List of post conversion handlers provided by this configuration """

    input_io_adapter_options = {}
    """ Dictionary with the options to provide the input io adapter """

    output_io_adapter_options = {}
    """ Dictionary with the options to provide the output io adapter """

    configuration_instances = []
    """ List of configuration instances """

    def __init__(self, omni_migration_demo_data_plugin):
        """
        Class constructor.

        @type omni_migration_demo_data_plugin: OmniMigrationDemoDataPlugin
        @param omni_migration_demo_data_plugin: Demo Data to Omni migration plugin.
        """

        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin
        self.attribute_mapping_output_entities = []
        self.attribute_mapping_output_attributes = []
        self.relation_mapping_entities = []
        self.relation_mapping_relations = []
        self.input_entity_indexers = []
        self.output_entity_indexers = []
        self.post_attribute_mapping_handlers = []
        self.post_relation_mapping_handlers = []
        self.post_conversion_handlers = []
        self.input_io_adapter_options = {}
        self.output_io_adapter_options = {}
        self.configuration_module_name_module_map = {}
        self.configuration_instances = []

        # imports the specified modules
        for module_name in IMPORT_MODULE_NAMES:
            module = __import__(module_name, globals(), locals())
            self.configuration_module_name_module_map[module_name] = module

            # injects the configuration tokens into the configuration module
            for global_name, global_value in globals().iteritems():
                setattr(module, global_name, global_value)

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # retrieves the demo data and output database paths
        resource_manager_plugin = self.omni_migration_demo_data_plugin.resource_manager_plugin
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")
        user_home_path = user_home_path_resource.data
        demo_data_path = os.path.join(user_home_path, DEMO_DATA_DIRECTORY_NAME)
        output_database_path = os.path.join(user_home_path, OUTPUT_DATABASE_FILE_NAME)

        # collects the configuration instances from the specified imports
        self.configuration_instances = []
        for configuration_module_name, configuration_module in self.configuration_module_name_module_map.iteritems():
            class_name = "".join([module_name_token.capitalize() for module_name_token in configuration_module_name.split("_")])
            class_reference = getattr(configuration_module, class_name)
            configuration_instance = class_reference(self.omni_migration_demo_data_plugin)
            configuration_instance.load_data_converter_configuration()
            self.configuration_instances.append(configuration_instance)

        # defines the schemas of the intermediate entities populated by this configuration
        self.intermediate_entity_schemas = []

        # defines how the input adapter should read data from the input source
        self.input_io_adapters_options = [{IO_ADAPTER_PLUGIN_ID_VALUE : IO_ADAPTER_CSV_PLUGIN_ID,
                                           TOKEN_SEPARATOR_VALUE : SEMI_COLON_VALUE,
                                           DIRECTORY_PATHS_VALUE : [demo_data_path],
                                           INPUT_ATTRIBUTE_HANDLERS_VALUE : [self.io_adapter_attribute_handler_convert_utf8_string_to_unicode,
                                                                             self.io_adapter_attribute_handler_convert_strikethrough_to_null,
                                                                             self.io_adapter_attribute_handler_convert_dates,
                                                                             self.io_adapter_attribute_handler_convert_currencies_percentages]}]

        # defines how the output adapter should write data to the output destination
        self.output_io_adapters_options = [{IO_ADAPTER_PLUGIN_ID_VALUE : IO_ADAPTER_ENTITY_MANAGER_PLUGIN_ID,
                                            ENTITY_MANAGER_ENGINE_VALUE : ENTITY_MANAGER_SQLITE_ENGINE_VALUE,
                                            FILE_PATH_VALUE : output_database_path,
                                            OUTPUT_ATTRIBUTE_HANDLERS_VALUE : [self.io_adapter_attribute_handler_convert_unicode_to_utf8]}]

        # defines how to index the loaded input intermediate structure entities
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["DD_Company", "DD_Supplier", "DD_Merchandise"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Name"],
                                                                   "DD_Supplier" : ["Name"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["Name"]}},
                                      {ENTITY_NAMES_VALUE : ["DD_Customer", "DD_Supplier", "DD_Merchandise"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"DD_Customer" : ["Id"],
                                                                   "DD_Supplier" : ["Id"],
                                                                   "DD_Merchandise" : ["Id"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["Id"]}}]

        # defines how to index the converted output entities
        self.output_entity_indexers = [{FUNCTION_VALUE : "output_indexer_created_output_entities"},
                                       {FUNCTION_VALUE : "output_indexer_creator_input_entity"}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_create_prices_costs_margins}]

    def io_adapter_attribute_handler_convert_utf8_string_to_unicode(self, intermediate_structure, entity, attribute_value):
        # decodes the attribute from utf8 to unicode in case it is a string
        if attribute_value and type(attribute_value) in types.StringTypes:
            attribute_value = attribute_value.decode(UTF8_VALUE)

        return attribute_value

    def io_adapter_attribute_handler_convert_unicode_to_utf8(self, intermediate_structure, entity, attribute_value):
        # encodes the attribute from unicode to utf-8 in case it is a unicode
        if attribute_value and type(attribute_value) == types.UnicodeType:
            attribute_value = attribute_value.encode(UTF8_VALUE)

        return attribute_value

    def io_adapter_attribute_handler_convert_strikethrough_to_null(self, intermediate_structure, entity, attribute_value):
        # converts strikethrough values to null
        if attribute_value and type(attribute_value) in types.StringTypes and attribute_value.count("-") == len(attribute_value):
            attribute_value = None

        return attribute_value

    def io_adapter_attribute_handler_convert_currencies_percentages(self, intermediate_structure, entity, attribute_value):
        # converts a string with currency or percentage value to a float
        if attribute_value and type(attribute_value) in types.StringTypes and attribute_value.strip()[-1] in (EURO_CURRENCY_SYMBOL, PERCENTAGE_SYMBOL):
            attribute_value = float(attribute_value.strip()[:-1].replace(COMMA_VALUE, DOT_VALUE).strip())

        return attribute_value

    def io_adapter_attribute_handler_convert_dates(self, intermediate_structure, entity, attribute_value):
        # tries to convert a date in a string to a date object
        if attribute_value and type(attribute_value) in types.StringTypes:

            # converts the string to a date, ignoring the conversion in case it fails
            for date_format in (DATETIME_FORMAT, DATE_FORMAT):
                try:
                    time_tuple = list(time.strptime(attribute_value, date_format))[:-2]
                    attribute_value = apply(datetime.datetime, time_tuple)
                    break
                except ValueError:
                    pass

        return attribute_value

    def post_conversion_handler_create_prices_costs_margins(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        # defines the existing price relations
        price_relations_map = {"SaleMerchandiseHierarchyTreeNode" : {"unit_price" : "sale_merchandise_hierarchy_tree_node_unit_price"},
                               "MerchandiseContactableOrganizationalHierarchyTreeNode" : {"price" : "merchandise_contactable_organizational_hierarchy_tree_node"},
                               "SaleTransaction" : {"price" : "sale"}}

        # defines the existing cost relations
        cost_relations_map = {"MerchandiseContactableOrganizationalHierarchyTreeNode" : {"cost" : "merchandise_contactable_organizational_hierarchy_tree_node"},
                              "PurchaseMerchandiseHierarchyTreeNode" : {"unit_cost" : "purchase_merchandise_hierarchy_tree_node_unit_cost"},
                              "OrganizationalHierarchyMerchandiseSupplier" : {"unit_cost" : "organizational_hierarchy_merchandise_supplier"},
                              "PurchaseTransaction" : {"cost" : "purchase"}}

        # defines the existing margin relations
        margin_relations_map = {"MerchandiseContactableOrganizationalHierarchyTreeNode" : {"margin" : "merchandise_contactable_organizational_hierarchy_tree_node"}}

        # replaces all price, margin and cost values with their respective entities
        entities = output_intermediate_structure.get_entities()
        for entity in entities:
            entity_name = entity.get_name()
            attributes_map = entity.get_attributes()
            for attribute_name, attribute_value in attributes_map.iteritems():

                # retrieves the appropriate relation mapping
                if "price" in attribute_name:
                    value_entity_name = "Price"
                    relations_map = price_relations_map.get(entity_name, {})
                elif "cost" in attribute_name:
                    value_entity_name = "Cost"
                    relations_map = cost_relations_map.get(entity_name, {})
                elif "margin" in attribute_name:
                    value_entity_name = "Margin"
                    relations_map = margin_relations_map.get(entity_name, {})
                else:
                    relations_map = {}

                # replaces the value with the respective entity and connects the two entities
                value_relation_attribute_name = relations_map.get(attribute_name)
                if value_relation_attribute_name:
                    value_entity = output_intermediate_structure.create_entity(value_entity_name)
                    value_entity.set_attribute("value", attribute_value)
                    entity.set_attribute(attribute_name, value_entity)
                    value_entity.set_attribute(value_relation_attribute_name, entity)

        return output_intermediate_structure

    def get_intermediate_entity_schemas(self):
        """
        Returns the intermediate structure schemas
        provided by this configuration.

        @rtype: List
        @return: The intermediate structure schema
        configurations provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        intermediate_entity_schemas = omni_migration_plugin.get_intermediate_entity_schemas()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "intermediate_entity_schemas"):
                intermediate_entity_schemas.extend(configuration_instance.intermediate_entity_schemas)
        intermediate_entity_schemas.extend(self.intermediate_entity_schemas)

        return intermediate_entity_schemas

    def get_attribute_mapping_output_entities(self):
        """
        Returns the attribute mapping output entity configurations
        provided by this configuration.

        @rtype: List
        @return: The attribute mapping output entity
        configurations provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        attribute_mapping_output_entities = omni_migration_plugin.get_attribute_mapping_output_entities()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "attribute_mapping_output_entities"):
                attribute_mapping_output_entities.extend(configuration_instance.attribute_mapping_output_entities)
        attribute_mapping_output_entities.extend(self.attribute_mapping_output_entities)

        return attribute_mapping_output_entities

    def get_relation_mapping_entities(self):
        """
        Returns the relation mapping entity configurations
        provided by this configuration.

        @rtype: List
        @return: Relation mapping entity configurations
        provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        relation_mapping_entities = omni_migration_plugin.get_relation_mapping_entities()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "relation_mapping_entities"):
                relation_mapping_entities.extend(configuration_instance.relation_mapping_entities)
        relation_mapping_entities.extend(self.relation_mapping_entities)

        return relation_mapping_entities

    def get_post_attribute_mapping_handlers(self):
        """
        Returns the post attribute mapping handlers
        provided by this configuration.

        @rtype: List
        @return: List of post attribute mapping handlers
        provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        post_attribute_mapping_handlers = omni_migration_plugin.get_post_attribute_mapping_handlers()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "post_attribute_mapping_handlers"):
                post_attribute_mapping_handlers.extend(configuration_instance.post_attribute_mapping_handlers)
        post_attribute_mapping_handlers.extend(self.post_attribute_mapping_handlers)

        return post_attribute_mapping_handlers

    def get_post_relation_mapping_handlers(self):
        """
        Returns the post relation mapping handlers
        provided by this configuration.

        @rtype: List
        @return: List of post relation mapping handlers
        provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        post_relation_mapping_handlers = omni_migration_plugin.get_post_relation_mapping_handlers()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "post_relation_mapping_handlers"):
                post_relation_mapping_handlers.extend(configuration_instance.post_relation_mapping_handlers)
        post_relation_mapping_handlers.extend(self.post_relation_mapping_handlers)

        return post_relation_mapping_handlers

    def get_post_conversion_handlers(self):
        """
        Returns the post conversion handlers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        post_conversion_handlers = omni_migration_plugin.get_post_conversion_handlers()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "post_conversion_handlers"):
                post_conversion_handlers.extend(configuration_instance.post_conversion_handlers)
        post_conversion_handlers.extend(self.post_conversion_handlers)

        return post_conversion_handlers

    def get_input_entity_indexers(self):
        """
        Returns the input entity indexers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        input_entity_indexers = omni_migration_plugin.get_input_entity_indexers()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "input_entity_indexers"):
                input_entity_indexers.extend(configuration_instance.input_entity_indexers)
        input_entity_indexers.extend(self.input_entity_indexers)

        return input_entity_indexers

    def get_output_entity_indexers(self):
        """
        Returns the output entity indexers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        output_entity_indexers = omni_migration_plugin.get_output_entity_indexers()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "output_entity_indexers"):
                output_entity_indexers.extend(configuration_instance.output_entity_indexers)
        output_entity_indexers.extend(self.output_entity_indexers)

        return output_entity_indexers

    def get_input_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to load data into the intermediate structure with.

        @rtype: List
        @return: List with maps with the input output adapter configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        input_io_adapters_options = omni_migration_plugin.get_input_io_adapters_options()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "input_io_adapters_options"):
                input_io_adapters_options.extend(configuration_instance.input_io_adapters_options)
        input_io_adapters_options.extend(self.input_io_adapters_options)

        return input_io_adapters_options

    def get_output_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to save the intermediate structure with.

        @rtype: List
        @return: List with maps with the input output adapter configuration.
        """

        omni_migration_plugin = self.omni_migration_demo_data_plugin.omni_migration_plugin

        output_io_adapters_options = omni_migration_plugin.get_output_io_adapters_options()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "output_io_adapters_options"):
                output_io_adapters_options.extend(configuration_instance.output_io_adapters_options)
        output_io_adapters_options.extend(self.output_io_adapters_options)

        return output_io_adapters_options
