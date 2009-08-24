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

IMPORT_MODULE_NAMES = ["user_configuration"]

OMNI_NON_CONSIGNABLE_STATUS = 0

LUGAR_DA_JOIA_MAXIMUM_CUSTOMER_CODE = "99999"

class OmniMigrationDiamante2003LugarDaJoia:
    """
    Configuration specifying how to migrate diamante 2003
    to omni for the lugar da joia deployment.
    """

    omni_migration_diamante_2003_lugar_da_joia_plugin = None
    """ Omni to Diamante migration lugar da joia plugin """

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

    def __init__(self, omni_migration_diamante_2003_lugar_da_joia_plugin):
        """
        Class constructor.

        @type omni_migration_diamante_2003_lugar_da_joia_plugin: OmniDiamanteMigrationPlugin
        @param omni_migration_diamante_2003_lugar_da_joia_plugin: Omni to Diamante migration plugin.
        """

        self.omni_migration_diamante_2003_lugar_da_joia_plugin = omni_migration_diamante_2003_lugar_da_joia_plugin
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

        # collects the configuration instances from the specified imports
        self.configuration_instances = []
        for configuration_module_name, configuration_module in self.configuration_module_name_module_map.iteritems():
            class_name = "".join([module_name_token.capitalize() for module_name_token in configuration_module_name.split("_")])
            class_reference = getattr(configuration_module, class_name)
            configuration_instance = class_reference(self.omni_migration_diamante_2003_lugar_da_joia_plugin)
            configuration_instance.load_data_converter_configuration()
            self.configuration_instances.append(configuration_instance)

        # defines the schemas of the intermediate entities populated by this configuration
        self.intermediate_entity_schemas = []

        # defines how the input adapter should read data from the input source
        self.input_io_adapters_options = []

        # defines how the output adapter should write data to the output destination
        self.output_io_adapters_options = []

        # defines the handlers that must be executed when the attribute mapping part of the conversion has finished
        self.post_attribute_mapping_handlers = [{FUNCTION_VALUE : self.post_attribute_mapping_handler_remove_duplicate_customer_persons,
                                                 OUTPUT_DEPENDENCIES_VALUE : {"CustomerPerson" : []}}]

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_create_customer_codes,
                                          OUTPUT_DEPENDENCIES_VALUE : {"CustomerPerson" : [],
                                                                       "CustomerCompany" : []}}]
                                         #{FUNCTION_VALUE : self.post_conversion_handler_execute_sub_product_transfers,
                                         # OUTPUT_DEPENDENCIES_VALUE : {"SystemCompany" : [],
                                         #                              "SubProduct" : [],
                                         #                              "Transfer" : []}}]

    def post_attribute_mapping_handler_remove_duplicate_customer_persons(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_lugar_da_joia_plugin.info("Removing duplicate customer persons")

        # removes duplicate customer persons (customer persons with the same customer code)

        customer_code_entities_map = {}

        # retrieves every customer person entity and indexes it by its customer code
        customer_person_entities = output_intermediate_structure.get_entities_by_name("CustomerPerson")
        customer_person_entities = [customer_person_entity for customer_person_entity in customer_person_entities if customer_person_entity.get_attribute("customer_code")]
        for customer_person_entity in customer_person_entities:
            customer_code = customer_person_entity.get_attribute("customer_code")

            # allocates a list for customer person entities with this customer code
            # in case it wasn't allocated before
            if not customer_code in customer_code_entities_map:
                customer_code_entities_map[customer_code] = []

            # adds the customer person to the list for customers with this customer code
            customer_code_entities_map[customer_code].append(customer_person_entity)

        # removes every customer person that has the same customer code as an already existing one
        for customer_code, customer_person_entities in customer_code_entities_map.iteritems():
            if len(customer_person_entities) > 1:
                for customer_person_entity in customer_person_entities[1:]:
                    # logs the customer person about to be removed
                    customer_code = customer_person_entity.get_attribute("customer_code")
                    self.omni_migration_diamante_2003_lugar_da_joia_plugin.info("Removing duplicate customer persons with customer code '%s'" % customer_code)

                    # removes all customer person and person relation entities created by this duplicate's creator
                    customer_person_object_id = customer_person_entity.get_object_id()
                    creator_input_entity = self.get_creator_input_entity(input_intermediate_structure, customer_person_object_id)
                    creator_input_entity_object_id = creator_input_entity.get_object_id()
                    removable_entities = self.get_created_output_entities(output_intermediate_structure, creator_input_entity_object_id, "CustomerPerson")
                    removable_entities.extend(self.get_created_output_entities(output_intermediate_structure, creator_input_entity_object_id, "PersonRelation"))
                    removable_entities.extend(self.get_created_output_entities(output_intermediate_structure, creator_input_entity_object_id, "Address"))
                    removable_entities.extend(self.get_created_output_entities(output_intermediate_structure, creator_input_entity_object_id, "ContactInformation"))
                    for removable_entity in removable_entities:
                        output_intermediate_structure.remove_entity(removable_entity)

        return output_intermediate_structure

    def post_conversion_handler_create_customer_codes(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_diamante_2003_lugar_da_joia_plugin.info("Creating missing customer codes")

        customer_entities_missing_customer_code = []
        maximum_customer_entity_customer_code = 0

        # joins the customer person and customer company entities
        customer_person_entities = output_intermediate_structure.get_entities_by_name("CustomerPerson")
        customer_company_entities = output_intermediate_structure.get_entities_by_name("CustomerCompany")
        customer_entities = []
        customer_entities.extend(customer_person_entities)
        customer_entities.extend(customer_company_entities)

        # collects all customer entities without a customer code and finds
        # the last used customer code
        for customer_entity in customer_entities:

            # stores the customer code if the customer has one and it
            # is higher than the last stored code
            customer_code = customer_entity.get_attribute("customer_code")
            if customer_code:
                customer_code_integer = int(customer_code)

                # make this the maximum customer code if its higher than the last stored one
                if customer_code_integer > maximum_customer_entity_customer_code:
                    maximum_customer_entity_customer_code = customer_code_integer
            else:
                # otherwise adds the customer entity to the list of customer entities
                # without a customer code
                customer_entities_missing_customer_code.append(customer_entity)

        # creates a new customer code for each customer  entity that doesn't have one
        for customer_entity in customer_entities_missing_customer_code:
            maximum_customer_entity_customer_code += 1
            customer_code = str(maximum_customer_entity_customer_code)
            customer_code = "".zfill(len(LUGAR_DA_JOIA_MAXIMUM_CUSTOMER_CODE) - len(customer_code)) + customer_code

            customer_entity.set_attribute("customer_code", customer_code)

        return output_intermediate_structure

    def post_conversion_handler_execute_sub_product_transfers(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        # executes the sub product transfers to place the sub products in their appropriate location, since
        # there is no information associating a merchandise with its stock location in diamante

        self.omni_migration_diamante_2003_lugar_da_joia_plugin.info("Adjusting sub product inventory by using transfers")

        # retrieves the system company entity, where all orfan inventory lines were assigned to
        system_company_entities = output_intermediate_structure.get_entities_by_name("SystemCompany")

        # exists the post conversion handler in case not system company is found
        if not len(system_company_entities) == 1:
            self.omni_migration_diamante_2003_lugar_da_joia_plugin.warning("Exiting handler because no system company was found")
            return output_intermediate_structure

        system_company_entity = system_company_entities[0]

        # retrieves the system company sub product inventory lines and indexes them by the sub product code
        system_company_sub_product_inventory_lines = [inventory_line_entity for inventory_line_entity in system_company_entity.get_attribute("inventory") if inventory_line_entity.get_attribute("merchandise") and inventory_line_entity.get_attribute("merchandise").get_name() == "SubProduct"]
        system_company_merchandise_object_id_inventory_line_map = dict([(inventory_line_entity.get_attribute("merchandise").get_object_id(), inventory_line_entity) for inventory_line_entity in system_company_sub_product_inventory_lines])

        # initializes maps used to index inventory lines by sender and receiver
        sender_merchandise_object_id_inventory_line_map = {}
        receiver_merchandise_object_id_inventory_line_map = {}

        # initializes a list where to store the ids of the merchandise whose inventory lines were moved away from the system company
        transfered_merchandise_object_ids = []

        # collects the sub product transfer lines
        transfer_line_entities = []
        transfer_entities = output_intermediate_structure.get_entities_by_name("Transfer")
        for transfer_entity in transfer_entities:
            transfer_lines = transfer_entity.get_attribute("transfer_lines")
            transfer_line_entities.extend([transfer_line_entity for transfer_line_entity in transfer_lines if transfer_line_entity.get_attribute("merchandise").get_name() == "SubProduct"])

        # associates each inventory line with the respective store
        for transfer_line_entity in transfer_line_entities:

            # retrieves the transfer line attributes
            transfer_entity = transfer_line_entity.get_attribute("transfer")
            sender_entity = transfer_entity.get_attribute("sender")
            receiver_entity = transfer_entity.get_attribute("receiver")
            quantity = transfer_line_entity.get_attribute("quantity")
            merchandise_entity = transfer_line_entity.get_attribute("merchandise")

            # raises an exception in case the transfer line merchandise is not a sub product
            if not merchandise_entity.get_name() == "SubProduct":
                raise "Transfer line should have a sub product"

            # retrieves the sender, receiver and system company inventory lines in case they exist
            sender_entity_object_id = sender_entity.get_object_id()
            receiver_entity_object_id = receiver_entity.get_object_id()
            merchandise_object_id = merchandise_entity.get_object_id()
            sender_inventory_line_entity = sender_merchandise_object_id_inventory_line_map.get((sender_entity_object_id, merchandise_object_id), None)
            receiver_inventory_line_entity = receiver_merchandise_object_id_inventory_line_map.get((receiver_entity_object_id, merchandise_object_id), None)
            system_company_inventory_line_entity = system_company_merchandise_object_id_inventory_line_map.get(merchandise_object_id, None)

            # creates the sender inventory line in case it doesn't exist yet
            if not sender_inventory_line_entity:
                transfered_merchandise_object_ids.append(merchandise_object_id)
                sender_discount = system_company_inventory_line_entity.get_attribute("discount")
                sender_price = system_company_inventory_line_entity.get_attribute("price")
                sender_stock_on_hand = system_company_inventory_line_entity.get_attribute("stock_on_hand")
                sender_inventory_line_entity = output_intermediate_structure.create_entity("MerchandiseContactableOrganizationalHierarchyTreeNode")
                sender_inventory_line_entity.set_attribute("stock_reserved", 0)
                sender_inventory_line_entity.set_attribute("stock_in_transit", 0)
                sender_inventory_line_entity.set_attribute("stock_on_hand", sender_stock_on_hand)
                sender_inventory_line_entity.set_attribute("price", sender_price)
                sender_inventory_line_entity.set_attribute("discount", sender_discount)
                sender_inventory_line_entity.set_attribute("merchandise", merchandise_entity)
                sender_inventory_line_entity.set_attribute("contactable_organizational_hierarchy_tree_node", sender_entity)

            # calculates the new sender stock on hand
            sender_stock_on_hand = sender_inventory_line_entity.get_attribute("stock_on_hand")
            sender_stock_on_hand = sender_stock_on_hand - quantity

            # raises an exception in case the sender's stock on hand becomes negative
            if sender_stock_on_hand < 0:
                raise "Sender stock on hand cannot be negative after a transfer"

            # updates the sender's stock on hand to the new stock after the transfer
            sender_inventory_line_entity.set_attribute("stock_on_hand", sender_stock_on_hand)

            # updates the sender's inventory
            data_converter.connect_entities(sender_entity, "inventory", sender_inventory_line_entity)

            # creates the receiver inventory line
            if not receiver_inventory_line_entity:
                transfered_merchandise_object_ids.append(merchandise_object_id)
                receiver_discount = system_company_inventory_line_entity.get_attribute("discount")
                receiver_price = system_company_inventory_line_entity.get_attribute("price")
                receiver_stock_on_hand = 0
                receiver_inventory_line_entity = output_intermediate_structure.create_entity("MerchandiseContactableOrganizationalHierarchyTreeNode")
                receiver_inventory_line_entity.set_attribute("stock_reserved", 0)
                receiver_inventory_line_entity.set_attribute("stock_in_transit", 0)
                receiver_inventory_line_entity.set_attribute("stock_on_hand", 0)
                receiver_inventory_line_entity.set_attribute("price", receiver_price)
                receiver_inventory_line_entity.set_attribute("discount", receiver_discount)
                receiver_inventory_line_entity.set_attribute("merchandise", merchandise_entity)
                receiver_inventory_line_entity.set_attribute("contactable_organizational_hierarchy_tree_node", sender_entity)

            # calculates the new receiver stock on hand
            receiver_stock_on_hand = receiver_inventory_line_entity.get_attribute("stock_on_hand")
            receiver_stock_on_hand = receiver_stock_on_hand + quantity

            # updates the sender's stock on hand to the new stock after the transfer
            receiver_inventory_line_entity.set_attribute("stock_on_hand", receiver_stock_on_hand)

            # updates the receiver's inventory
            data_converter.connect_entities(receiver_entity, "inventory", receiver_inventory_line_entity)

            # updates the merchandise's contactable organizational units
            data_converter.connect_entities(merchandise_entity, "contactable_organizational_units", sender_inventory_line_entity)
            data_converter.connect_entities(merchandise_entity, "contactable_organizational_units", receiver_inventory_line_entity)

        # removes the transfered system company inventory lines
        transfered_merchandise_object_ids = list(set(transfered_merchandise_object_ids))
        for transfered_merchandise_object_id in transfered_merchandise_object_ids:
            system_company_inventory_line_entity = system_company_merchandise_object_id_inventory_line_map[transfered_merchandise_object_id]

            # removes the inventory line from the system company
            data_converter.disconnect_entities(system_company_entity, "inventory", system_company_inventory_line_entity)

            # removes the system company from the merchandise's contactable organizational units
            merchandise_entity = system_company_inventory_line_entity.get_attribute("merchandise")
            data_converter.disconnect_entities(merchandise_entity, "contactable_organizational_units", system_company_inventory_line_entity)

            # removes the system company inventory line
            output_intermediate_structure.remove_entity(system_company_inventory_line_entity)

        return output_intermediate_structure

    def get_intermediate_entity_schemas(self):
        """
        Returns the intermediate structure schemas
        provided by this configuration.

        @rtype: List
        @return: The intermediate structure schema
        configurations provided by this configuration.
        """

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        intermediate_entity_schemas = omni_migration_diamante_2003_plugin.get_intermediate_entity_schemas()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "intermediate_entity_schemas"):
                intermediate_entity_schemas.extend(configuration_instance.intermediate_entity_schemas)
        intermediate_entity_schemas.extend(self.intermediate_entity_schemas)

        return intermediate_entity_schemas

    def get_creator_input_entity(self, input_intermediate_structure, output_entity_object_id):
        input_entity_index = (INPUT_ENTITY_VALUE, CREATED_VALUE, OUTPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, output_entity_object_id)
        input_entities = input_intermediate_structure.get_entities_by_index(input_entity_index)

        # raises an exception in case more than one input entity is found when only one was expected
        if len(input_entities) > 1:
            raise "Expected only one creator input entity"

        # returns None in case no entity was found
        if not input_entities:
            # @todo: log warning
            return None

        input_entity = input_entities[0]

        return input_entity

    def get_created_output_entities(self, output_intermediate_structure, input_entity_object_id, output_entity_name):
        output_entity_index = (OUTPUT_ENTITY_VALUE, WHERE_VALUE, INPUT_ENTITY_OBJECT_ID_VALUE, EQUALS_VALUE, input_entity_object_id,
                               CREATED_VALUE, OUTPUT_ENTITY_NAME_VALUE, EQUALS_VALUE, output_entity_name)
        output_entities = output_intermediate_structure.get_entities_by_index(output_entity_index)

        return output_entities

    def get_attribute_mapping_output_entities(self):
        """
        Returns the attribute mapping output entity configurations
        provided by this configuration.

        @rtype: Dictionary
        @return: The attribute mapping output entity
        configurations provided by this configuration.
        """

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        attribute_mapping_output_entities = omni_migration_diamante_2003_plugin.get_attribute_mapping_output_entities()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "attribute_mapping_output_entities"):
                attribute_mapping_output_entities.extend(configuration_instance.attribute_mapping_output_entities)
        attribute_mapping_output_entities.extend(self.attribute_mapping_output_entities)

        return attribute_mapping_output_entities

    def get_relation_mapping_entities(self):
        """
        Returns the relation mapping entity configurations
        provided by this configuration.

        @rtype: Dictionary
        @return: Relation mapping entity configurations
        provided by this configuration.
        """

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        relation_mapping_entities = omni_migration_diamante_2003_plugin.get_relation_mapping_entities()
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

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        post_attribute_mapping_handlers = omni_migration_diamante_2003_plugin.get_post_attribute_mapping_handlers()
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

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        post_conversion_handlers = omni_migration_diamante_2003_plugin.get_post_conversion_handlers()
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

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        input_entity_indexers = omni_migration_diamante_2003_plugin.get_input_entity_indexers()
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

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        output_entity_indexers = omni_migration_diamante_2003_plugin.get_output_entity_indexers()
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

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        input_io_adapters_options = omni_migration_diamante_2003_plugin.get_input_io_adapters_options()
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

        omni_migration_diamante_2003_plugin = self.omni_migration_diamante_2003_lugar_da_joia_plugin.omni_migration_diamante_2003_plugin

        output_io_adapters_options = omni_migration_diamante_2003_plugin.get_output_io_adapters_options()
        for configuration_instance in self.configuration_instances:
            if hasattr(configuration_instance, "output_io_adapters_options"):
                output_io_adapters_options.extend(configuration_instance.output_io_adapters_options)
        output_io_adapters_options.extend(self.output_io_adapters_options)

        return output_io_adapters_options
