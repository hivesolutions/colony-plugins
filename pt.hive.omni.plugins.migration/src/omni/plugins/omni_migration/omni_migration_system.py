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

TYPES_VALUE = "types"

LIST_TYPE_VALUE = "list_type"

ATTRIBUTES_VALUE = "attributes"

NAME_VALUE = "name"

STRING_TYPE = [types.StringType, types.UnicodeType]
""" String type """

INTEGER_TYPE = [types.IntType, types.LongType]
""" Integer type """

FLOAT_TYPE = [types.FloatType]
""" Float type """

NUMERIC_TYPE = [types.IntType, types.LongType, types.FloatType]
""" Numeric type """

DATE_TYPE = [type(datetime.datetime.now())]
""" Date type """

IMPORT_MODULE_NAMES = ["address_configuration",
                       "card_payment_configuration",
                       "cash_payment_configuration",
                       "category_configuration",
                       "check_payment_configuration",
                       "collection_configuration",
                       "company_configuration",
                       "consignment_configuration",
                       "consignment_merchandise_hierarchy_tree_node_configuration",
                       "consignment_return_configuration",
                       "consignment_slip_configuration",
                       "contact_information_configuration",
                       "cost_configuration",
                       "credit_note_configuration",
                       "credit_note_payment_configuration",
                       "customer_company_configuration",
                       "customer_hierarchy_tree_configuration",
                       "customer_person_configuration",
                       "customer_return_configuration",
                       "debit_note_configuration",
                       "department_configuration",
                       "employee_configuration",
                       "gift_certificate_configuration",
                       "gift_certificate_payment_configuration",
                       "invalid_payment_configuration",
                       "invoice_configuration",
                       "margin_configuration",
                       "media_configuration",
                       "merchandise_contactable_organizational_hierarchy_tree_node_configuration",
                       "merchandise_hierarchy_tree_node_return_configuration",
                       "merchandise_hierarchy_tree_configuration",
                       "money_sale_slip_configuration",
                       "organizational_hierarchy_merchandise_supplier_configuration",
                       "organizational_hierarchy_tree_configuration",
                       "organizational_merchandise_hierarchy_tree_node_vat_class_configuration",
                       "payment_configuration",
                       "payment_payment_method_configuration",
                       "person_relation_configuration",
                       "post_dated_check_payment_configuration",
                       "price_configuration",
                       "product_configuration",
                       "purchase_merchandise_hierarchy_tree_node_configuration",
                       "purchase_transaction_configuration",
                       "repair_configuration",
                       "return_to_vendor_slip_configuration",
                       "sale_merchandise_hierarchy_tree_node_configuration",
                       "sale_transaction_configuration",
                       "service_configuration",
                       "stock_adjustment_configuration",
                       "stock_adjustment_merchandise_hierarchy_tree_node_configuration",
                       "stock_adjustment_reason_configuration",
                       "store_configuration",
                       "sub_product_configuration",
                       "supplier_company_configuration",
                       "supplier_hierarchy_tree_configuration",
                       "supplier_return_configuration",
                       "system_company_configuration",
                       "transfer_configuration",
                       "transfer_merchandise_hierarchy_tree_node_configuration",
                       "user_configuration",
                       "vat_class_configuration",
                       "warehouse_configuration"]

class OmniMigration:
    """
    Configuration specifying how to migrate data to omni.
    """

    omni_migration_plugin = None
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

    def __init__(self, omni_migration_plugin):
        """
        Class constructor.

        @type omni_migration_plugin: OmniMigrationDemoDataPlugin
        @param omni_migration_plugin: Demo Data to Omni migration plugin.
        """

        self.omni_migration_plugin = omni_migration_plugin
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

        # collects the configuration instances from the specified imports
        self.configuration_instances = []
        for configuration_module_name, configuration_module in self.configuration_module_name_module_map.iteritems():
            class_name = "".join([module_name_token.capitalize() for module_name_token in configuration_module_name.split("_")])
            class_reference = getattr(configuration_module, class_name)
            configuration_instance = class_reference(self.omni_migration_plugin)
            configuration_instance.load_data_converter_configuration()
            self.configuration_instances.append(configuration_instance)

        # defines the schemas of the intermediate entities populated by this configuration
        self.intermediate_entity_schemas = []

        # defines how the input adapter should read data from the input source
        self.input_io_adapters_options = []

        # defines how the output adapter should write data to the output destination
        self.output_io_adapters_options = []

        # defines how to index the loaded input intermediate structure entities
        self.input_entity_indexers = []

        # defines how to index the converted output entities
        self.output_entity_indexers = []

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = []

    def get_intermediate_entity_schemas(self):
        """
        Returns the intermediate structure schemas
        provided by this configuration.

        @rtype: List
        @return: The intermediate structure schema
        configurations provided by this configuration.
        """

        intermediate_entity_schemas = []
        intermediate_entity_schemas.extend(self.intermediate_entity_schemas)
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "intermediate_entity_schemas"):
                intermediate_entity_schemas.extend(configuration_instance.intermediate_entity_schemas)

        return intermediate_entity_schemas

    def get_attribute_mapping_output_entities(self):
        """
        Returns the attribute mapping output entity configurations
        provided by this configuration.

        @rtype: List
        @return: The attribute mapping output entity
        configurations provided by this configuration.
        """

        attribute_mapping_output_entities = []
        attribute_mapping_output_entities.extend(self.attribute_mapping_output_entities)
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "attribute_mapping_output_entities"):
                attribute_mapping_output_entities.extend(configuration_instance.attribute_mapping_output_entities)

        return attribute_mapping_output_entities

    def get_relation_mapping_entities(self):
        """
        Returns the relation mapping entity configurations
        provided by this configuration.

        @rtype: List
        @return: Relation mapping entity configurations
        provided by this configuration.
        """

        relation_mapping_entities = []
        relation_mapping_entities.extend(self.relation_mapping_entities)
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "relation_mapping_entities"):
                relation_mapping_entities.extend(configuration_instance.relation_mapping_entities)

        return relation_mapping_entities

    def get_post_attribute_mapping_handlers(self):
        """
        Returns the post attribute mapping handlers
        provided by this configuration.

        @rtype: List
        @return: List of post attribute mapping handlers
        provided by this configuration.
        """

        post_attribute_mapping_handlers = []
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

        post_relation_mapping_handlers = []
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

        post_conversion_handlers = []
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

        input_entity_indexers = []
        input_entity_indexers.extend(self.input_entity_indexers)
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "input_entity_indexers"):
                input_entity_indexers.extend(configuration_instance.input_entity_indexers)

        return input_entity_indexers

    def get_output_entity_indexers(self):
        """
        Returns the output entity indexers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        output_entity_indexers = []
        output_entity_indexers.extend(self.output_entity_indexers)
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "output_entity_indexers"):
                output_entity_indexers.extend(configuration_instance.output_entity_indexers)

        return output_entity_indexers

    def get_input_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to load data into the intermediate structure with.

        @rtype: List
        @return: List with maps with the input output adapter configuration.
        """

        input_io_adapters_options = []
        input_io_adapters_options.extend(self.input_io_adapters_options)
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "input_io_adapters_options"):
                input_io_adapters_options.extend(configuration_instance.input_io_adapters_options)

        return input_io_adapters_options

    def get_output_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to save the intermediate structure with.

        @rtype: List
        @return: List with maps with the input output adapter configuration.
        """

        output_io_adapters_options = []
        output_io_adapters_options.extend(self.output_io_adapters_options)
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "output_io_adapters_options"):
                output_io_adapters_options.extend(configuration_instance.output_io_adapters_options)

        return output_io_adapters_options
