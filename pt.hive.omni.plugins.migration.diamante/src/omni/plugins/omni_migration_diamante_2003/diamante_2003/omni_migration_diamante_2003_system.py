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
import os.path

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
                       "card_payment_configuration",
                       "cash_payment_configuration",
                       "category_configuration",
                       "check_payment_configuration",
                       "collection_configuration",
                       "consignment_configuration",
                       "consignment_merchandise_hierarchy_tree_node_configuration",
                       "consignment_return_configuration",
                       "consignment_slip_configuration",
                       "contact_information_configuration",
                       "credit_note_configuration",
                       "credit_note_payment_configuration",
                       "customer_company_configuration",
                       "customer_hierarchy_tree_configuration",
                       "customer_person_configuration",
                       "customer_return_configuration",
                       "debit_note_configuration",
                       "employee_configuration",
                       "gift_certificate_configuration",
                       "gift_certificate_payment_configuration",
                       "invalid_payment_configuration",
                       "invoice_configuration",
                       "media_configuration",
                       "merchandise_contactable_organizational_hierarchy_tree_node_configuration",
                       "merchandise_hierarchy_tree_node_return_configuration",
                       "merchandise_hierarchy_tree_configuration",
                       "money_sale_slip_configuration",
                       "organizational_hierarchy_tree_configuration",
                       "organizational_hierarchy_merchandise_supplier_configuration",
                       "organizational_merchandise_hierarchy_tree_node_vat_class_configuration",
                       "payment_configuration",
                       "payment_payment_method_configuration",
                       "person_relation_configuration",
                       "post_dated_check_payment_configuration",
                       "product_configuration",
                       "purchase_merchandise_hierarchy_tree_node_configuration",
                       "purchase_transaction_configuration",
                       "repair_configuration",
                       "return_to_vendor_slip_configuration",
                       "sale_merchandise_hierarchy_tree_node_configuration",
                       "sale_transaction_configuration",
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
                       "vat_class_configuration"]

ATTRIBUTE_NAMES_VALUE = "attribute_names"

FILE_PATH_VALUE = "file_path"

DIRECTORY_PATHS_VALUE = "directory_paths"

ENTITY_MANAGER_ENGINE_VALUE = "entity_manager_engine"

LATIN1_VALUE = "latin1"
""" The latin1 encoding in python """

UTF8_VALUE = "utf-8"
""" The utf8 encoding in python """

OMNI_NON_CONSIGNABLE_STATUS = 0
""" The non consignable status in omni """

DIAMANTE_INACTIVE_ENTITY_STATUS = 1
""" The inactive entity status in diamante """

OMNI_INACTIVE_ENTITY_STATUS = 0
""" The inactive entity status indicator in omni """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

DIAMANTE_DIRECTORY_NAME = "DIA2002"
""" Name of the diamante directory """

OUTPUT_DATABASE_FILE_NAME = "omni_database_diamante.sqlite"
""" Name of the file where to output the migrated date to """

IO_ADAPTER_DBASE_PLUGIN_ID = "pt.hive.colony.plugins.data_converter.io_adapter.dbase"
""" The unique identifier for the dbase io adapter plugin """

IO_ADAPTER_ENTITY_MANAGER_PLUGIN_ID = "pt.hive.colony.plugins.data_converter.io_adapter.entity_manager"
""" The unique identifier for the entity manager io adapter plugin """

ENTITY_MANAGER_SQLITE_ENGINE_VALUE = "sqlite"
""" The identifier for the entity manager sqlite engine """

class OmniMigrationDiamante2003:
    """
    Configuration specifying how to migrate diamante 2003
    to omni.
    """

    omni_migration_diamante_2003_plugin = None
    """ Omni to Diamante migration plugin """

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

    post_conversion_handlers = []
    """ List of post conversion handlers provided by this configuration """

    input_io_adapter_options = {}
    """ Dictionary with the options to provide the input io adapter """

    output_io_adapter_options = {}
    """ Dictionary with the options to provide the output io adapter """

    configuration_instances = []
    """ List of configuration instances """

    def __init__(self, omni_migration_diamante_2003_plugin):
        """
        Class constructor.

        @type omni_migration_diamante_2003_plugin: OmniDiamanteMigrationPlugin
        @param omni_migration_diamante_2003_plugin: Omni to Diamante migration plugin.
        """

        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin
        self.attribute_mapping_output_entities = []
        self.attribute_mapping_output_attributes = []
        self.relation_mapping_entities = []
        self.relation_mapping_relations = []
        self.input_entity_indexers = []
        self.output_entity_indexers = []
        self.post_attribute_mapping_handlers = []
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
        resource_manager_plugin = self.omni_migration_diamante_2003_plugin.resource_manager_plugin
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")
        user_home_path = user_home_path_resource.data
        diamante_path = os.path.join(user_home_path, DIAMANTE_DIRECTORY_NAME)
        output_database_path = os.path.join(user_home_path, OUTPUT_DATABASE_FILE_NAME)

        # collects the configuration instances from the specified imports
        self.configuration_instances = []
        for configuration_module_name, configuration_module in self.configuration_module_name_module_map.iteritems():
            class_name = "".join([module_name_token.capitalize() for module_name_token in configuration_module_name.split("_")])
            class_reference = getattr(configuration_module, class_name)
            configuration_instance = class_reference(self.omni_migration_diamante_2003_plugin)
            configuration_instance.load_data_converter_configuration()
            self.configuration_instances.append(configuration_instance)

        # defines the schemas for the used intermediate structure entities
        self.intermediate_entity_schemas = []

        # defines how the input adapter should read data from the input source
        self.input_io_adapters_options = [{IO_ADAPTER_PLUGIN_ID_VALUE : IO_ADAPTER_DBASE_PLUGIN_ID,
                                           DIRECTORY_PATHS_VALUE : [diamante_path],
                                           INPUT_ATTRIBUTE_HANDLERS_VALUE : [self.io_adapter_attribute_handler_convert_latin1_string_to_unicode]}]

        # defines how the output adapter should write data to the output destination
        self.output_io_adapters_options = [{IO_ADAPTER_PLUGIN_ID_VALUE : IO_ADAPTER_ENTITY_MANAGER_PLUGIN_ID,
                                            ENTITY_MANAGER_ENGINE_VALUE : ENTITY_MANAGER_SQLITE_ENGINE_VALUE,
                                            FILE_PATH_VALUE : output_database_path,
                                            OUTPUT_ATTRIBUTE_HANDLERS_VALUE : [self.io_adapter_attribute_handler_convert_unicode_to_utf8]}]

        # defines how to index the loaded input intermediate structure entities
        self.input_entity_indexers = [{FUNCTION_VALUE : "input_indexer_primary_key",
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["CODIGO"]}}]

        # defines how to index the converted output entities
        self.output_entity_indexers = [{FUNCTION_VALUE : "output_indexer_created_output_entities"},
                                       {FUNCTION_VALUE : "output_indexer_creator_input_entity"}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_create_prices_costs_margins},
                                         {FUNCTION_VALUE : self.post_conversion_handler_assign_entity_status}]

    def io_adapter_attribute_handler_convert_latin1_string_to_unicode(self, intermediate_structure, entity, attribute_value):
        # decodes the attribute from latin1 to unicode in case it is a string
        if attribute_value and type(attribute_value) == types.StringType:
            attribute_value = attribute_value.decode(LATIN1_VALUE)

        return attribute_value

    def io_adapter_attribute_handler_convert_unicode_to_utf8(self, intermediate_structure, entity, attribute_value):
        # encodes the attribute from unicode to utf-8 in case it is a unicode
        #if attribute_value and type(attribute_value) == types.UnicodeType:
        #    attribute_value = attribute_value.encode(UTF8_VALUE)

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

    def post_conversion_handler_assign_entity_status(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        # sets the enabled/disabled status in all output entities
        output_entities = output_intermediate_structure.get_entities()
        for output_entity in output_entities:
            status = OMNI_ACTIVE_ENTITY_STATUS

            # retrieves the creator input entity
            output_entity_object_id = output_entity.get_object_id()
            creator_input_entity = self.get_creator_input_entity(input_intermediate_structure, output_entity_object_id)

            # turns the status to disabled in case the creator input entity is disabled
            if creator_input_entity and creator_input_entity.has_attribute("ANULADO") and creator_input_entity.get_attribute("ANULADO") == DIAMANTE_INACTIVE_ENTITY_STATUS:
                status = OMNI_INACTIVE_ENTITY_STATUS

            # sets the output entity's status
            output_entity.set_attribute("status", status)

        return output_intermediate_structure

    def get_creator_input_entity(self, input_intermediate_structure, output_entity_object_id):
        # retrieves the creator input entity for the output entity with the specified object id
        input_entity_index = (INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, output_entity_object_id)
        input_entities = input_intermediate_structure.get_entities_by_index(input_entity_index)

        # returns in case no input entity or more than one input entity is found
        if not len(input_entities) == 1:
            return None

        input_entity = input_entities[0]

        return input_entity

    def get_intermediate_entity_schemas(self):
        """
        Returns the intermediate structure schemas
        provided by this configuration.

        @rtype: List
        @return: The intermediate structure schema
        configurations provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

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

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

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

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

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

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

        post_attribute_mapping_handlers = omni_migration_plugin.get_post_attribute_mapping_handlers()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "post_attribute_mapping_handlers"):
                post_attribute_mapping_handlers.extend(configuration_instance.post_attribute_mapping_handlers)
        post_attribute_mapping_handlers.extend(self.post_attribute_mapping_handlers)

        return post_attribute_mapping_handlers

    def get_post_conversion_handlers(self):
        """
        Returns the post conversion handlers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

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

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

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

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

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

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

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

        omni_migration_plugin = self.omni_migration_diamante_2003_plugin.omni_migration_plugin

        output_io_adapters_options = omni_migration_plugin.get_output_io_adapters_options()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "output_io_adapters_options"):
                output_io_adapters_options.extend(configuration_instance.output_io_adapters_options)
        output_io_adapters_options.extend(self.output_io_adapters_options)

        return output_io_adapters_options
