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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import md5
import base64
import copy
import time

import data_converter.data_converter_adapter_configuration_parser

class DataConverterAdapter:
    """
    Adapter used to convert data from the source medium and schema to the internal structure.
    """

    internal_entity_name_primary_key_domain_entity_conversion_info_map = {}
    """ Dictionary relating internal entity name, with primary key value, with a information on how the conversion was performed """

    foreign_key_queue = []
    """ Queue of foreign keys that are waiting of the entity are referencing to be processed """

    input_description = None
    """ Reference to the input configuration properties (extracted from the configuration file) """

    data_converter_plugin = None
    """ Reference to the plugin that owns this code """

    logger = None
    """ Reference to the logging instance """

    def __init__(self, data_converter_plugin):
        """
        Class constructor.

        @type data_converter_plugin: DataConverterPlugin
        @param data_converter_plugin: Reference to the plugin that owns this code.
        """

        self.data_converter_plugin = data_converter_plugin
        self.logger = self.data_converter_plugin.logger_plugin.get_logger("main").get_logger()

    def load_configuration(self):
        """
        Loads from the XML configuration file into the correspondent conversion configuration data structures.
        """

        parser = data_converter.data_converter_adapter_configuration_parser.DataConverterAdapterConfigurationParser()
        file_paths = self.configuration.get_configuration_file_paths()
        for file_path in file_paths:
            parser.file_path = file_path
            parser.parse()
        self.input_description = parser.adapter_configuration

    def convert(self, task, internal_structure, connection, configuration):
        """
        Processes an operation on the input database.

        @type task: Task
        @param task: Task monitoring object used to inform the status of the query.
        @type internal_structure: InternalStructure
        @param internal_structure: Internal structure where the data will be converted to.
        @type connection: Object
        @param connection: Connection object for the input adapter to extract data from.
        @type configuration: Object
        @param configuration: Configuration object that indicates how to migrate data from the source to the internal structure.
        @rtype: InternalStructure
        @return: The internal structure with the data migrated from the source medium and schema.
        """

        self.logger.warn("The input adapter has started the conversion process.\n")

        # reset the input adapter's data
        self.internal_entity_name_primary_key_domain_entity_conversion_info_map = {}
        self.foreign_key_queue = []
        self.internal_structure = internal_structure
        self.connection = connection
        self.configuration = configuration
        self.load_configuration()

        # convert the data to the internal structure
        self.process_work_units(task)

        # notify all data converter observers that the internal structure changed
        for data_converter_observer_plugin in self.data_converter_plugin.data_converter_observer_plugins:
            data_converter_observer_plugin.notify_data_conversion_status({"internal_structure" : internal_structure})

        self.convert_omni(internal_structure)

    def convert_omni(self, internal_structure):
        entity_manager_plugin = self.data_converter_plugin.entity_manager_plugin
        resource_manager_plugin = self.data_converter_plugin.resource_manager_plugin
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")
        user_home_path = user_home_path_resource.data
        entity_manager = entity_manager_plugin.load_entity_manager("sqlite")
        entity_manager.set_connection_parameters({"file_path" : user_home_path + "/conversion_database.db", "autocommit" : False})
        entity_manager.load_entity_manager()

        start_time = time.time()

        entity_manager.create_transaction("organizational_hierarchy_transaction")

        # create merchandise hierarchy tree root node
        merchandise_hierarchy_tree_node_class = entity_manager.get_entity_class("MerchandiseHierarchyTreeNode")
        merchandise_hierarchy_tree_node_entity = merchandise_hierarchy_tree_node_class()
        internal_structure.object_id += 1
        merchandise_hierarchy_tree_node_entity.object_id = internal_structure.object_id
        print "Saving MerchandiseHierarchyTree root node with object id = " + str(merchandise_hierarchy_tree_node_entity.object_id)
        entity_manager.save(merchandise_hierarchy_tree_node_entity)

        # create organizational hierarchy tree root node
        organizational_hierarchy_tree_node_class = entity_manager.get_entity_class("OrganizationalHierarchyTreeNode")
        organizational_hierarchy_tree_root_node_entity = organizational_hierarchy_tree_node_class()
        internal_structure.object_id += 1
        organizational_hierarchy_tree_root_node_entity.object_id = internal_structure.object_id
        print "Saving OrganizationalHierarchyTree root node with object id = " + str(organizational_hierarchy_tree_root_node_entity.object_id)
        entity_manager.save(organizational_hierarchy_tree_root_node_entity)

        # create supplier hierarchy tree root node
        organizational_hierarchy_tree_node_class = entity_manager.get_entity_class("OrganizationalHierarchyTreeNode")
        supplier_hierarchy_tree_node_entity = organizational_hierarchy_tree_node_class()
        internal_structure.object_id += 1
        supplier_hierarchy_tree_node_entity.object_id = internal_structure.object_id
        print "Saving SupplierHierarchyTree root node with object id = " + str(organizational_hierarchy_tree_root_node_entity.object_id)
        entity_manager.save(supplier_hierarchy_tree_node_entity)

        # create customer hierarchy tree root node
        organizational_hierarchy_tree_node_class = entity_manager.get_entity_class("OrganizationalHierarchyTreeNode")
        customer_hierarchy_tree_node_entity = organizational_hierarchy_tree_node_class()
        internal_structure.object_id += 1
        customer_hierarchy_tree_node_entity.object_id = internal_structure.object_id
        print "Saving CustomerHierarchyTree root node with object id = " + str(customer_hierarchy_tree_node_entity.object_id)
        entity_manager.save(customer_hierarchy_tree_node_entity)

        # create organizational hierarchy tree
        organizational_hierarchy_tree_class = entity_manager.get_entity_class("OrganizationalHierarchyTree")
        organizational_hierarchy_tree_entity = organizational_hierarchy_tree_class()
        internal_structure.object_id += 1
        organizational_hierarchy_tree_entity.object_id = internal_structure.object_id
        organizational_hierarchy_tree_entity.root_node = organizational_hierarchy_tree_root_node_entity
        print "Saving OrganizationalHierarchyTree with object id = " + str(organizational_hierarchy_tree_entity.object_id)
        entity_manager.save(organizational_hierarchy_tree_entity)

        # create merchandise hierarchy tree
        merchandise_hierarchy_tree_class = entity_manager.get_entity_class("MerchandiseHierarchyTree")
        merchandise_hierarchy_tree_entity = merchandise_hierarchy_tree_class()
        internal_structure.object_id += 1
        merchandise_hierarchy_tree_entity.object_id = internal_structure.object_id
        merchandise_hierarchy_tree_entity.root_node = merchandise_hierarchy_tree_node_entity
        print "Saving MerchandiseHierarchyTree with object id = " + str(merchandise_hierarchy_tree_entity.object_id)
        entity_manager.save(merchandise_hierarchy_tree_entity)

        # create supplier hierarchy tree
        supplier_hierarchy_tree_class = entity_manager.get_entity_class("SupplierHierarchyTree")
        supplier_hierarchy_tree_entity = supplier_hierarchy_tree_class()
        internal_structure.object_id += 1
        supplier_hierarchy_tree_entity.object_id = internal_structure.object_id
        supplier_hierarchy_tree_entity.root_node = supplier_hierarchy_tree_node_entity
        print "Saving SupplierHierarchyTree with object id = " + str(supplier_hierarchy_tree_entity.object_id)
        entity_manager.save(supplier_hierarchy_tree_entity)

        # create customer hierarchy tree
        customer_hierarchy_tree_class = entity_manager.get_entity_class("CustomerHierarchyTree")
        customer_hierarchy_tree_entity = customer_hierarchy_tree_class()
        internal_structure.object_id += 1
        customer_hierarchy_tree_entity.object_id = internal_structure.object_id
        customer_hierarchy_tree_entity.root_node = customer_hierarchy_tree_node_entity
        print "Saving CustomerHierarchyTree with object id = " + str(customer_hierarchy_tree_entity.object_id)
        entity_manager.save(customer_hierarchy_tree_entity)

        # create the euro currency
        currency_class = entity_manager.get_entity_class("Currency")
        currency_entity = currency_class()
        currency_entity.name = "euro"
        internal_structure.object_id += 1
        currency_entity.object_id = internal_structure.object_id
        print "Saving Currency with object id = " + str(currency_entity.object_id)
        entity_manager.save(currency_entity)

        # create the portuguese language
        language_class = entity_manager.get_entity_class("Language")
        language_entity = language_class()
        language_entity.name = "portugues"
        internal_structure.object_id += 1
        language_entity.object_id = internal_structure.object_id
        print "Saving Language with object id = " + str(language_entity.object_id)
        entity_manager.save(language_entity)

        entity_manager.commit_transaction("organizational_hierarchy_transaction")

        self.foreign_key_queue =  []
        self.missing_relations = []
        # convert every entity in the internal structure
        internal_entity_names = ["system_company", "store", "system_company_employee", "users", "reason", "location", "vat_class", "customer_company", "customer_person", "supplier_company", "supplier_employee", "supplier_person"
 "address", "contact_information", "financial_account", "person_relation", "category", "collection", "product", "sub_product", "repair", "media", "organizational_merchandise_hierarchy_tree_node_vat_class",
 "merchandise_contactable_organizational_hierarchy_tree_node", "stock_adjustment", "stock_adjustment_merchandise_hierarchy_tree_node", "consignment", "consignment_merchandise_hierarchy_tree_node",
 "purchase", "purchase_merchandise_hierarchy_tree_node", "payment_terms", "sale_transaction", "sale_merchandise_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node", "shipment", "invoice",
 "receipt", "supplier_return", "customer_return", "merchandise_hierarchy_tree_node_return", "credit_note", "card_payment", "cash_payment", "check_payment", "credit_note_payment",
 "gift_certificate", "credit_contract", "credit_payment", "payment", "payment_line", "transfer", "transfer_merchandise_hierarchy_tree_node"]
        #internal_entity_names = internal_structure.get_entity_names()
        for internal_entity_name in internal_entity_names:
            print "##### CONVERTING " + internal_entity_name + " entities #####"
            # for all internal entity instance
            entity_manager.create_transaction(internal_entity_name)
            self.convert_entities(internal_structure, entity_manager, internal_entity_name)
            entity_manager.commit_transaction(internal_entity_name)

        # create user group and profile for every user
        user_group_class = entity_manager.get_entity_class("UserGroup")
        user_group_entity = user_group_class()
        user_group_entity.name = "Utilizadores"
        entity_manager.save(user_group_entity)
        user_class = entity_manager.get_entity_class("User")
        users = entity_manager._find_all(user_class)
        for user in users:
            user.secret_answer_hash = md5.new(user.secret_answer_hash).digest()
            user.secret_answer_hash_type = "md5"
            user.password_hash = md5.new(user.password_hash).digest()
            user.password_hash_type = "md5"
            user.status = 0
            entity_manager.save_or_update(user)
            profile_class = entity_manager.get_entity_class("Profile")
            profile_entity = profile_class()
            profile_entity.user_groups = [user_group_entity]
            profile_entity.user = user
            entity_manager.save(profile_entity)

        # add parentless tree nodes to the root node
        customer_hierarchy_tree_class = entity_manager.get_entity_class("CustomerHierarchyTree")
        customer_hierarchy_tree_entity = entity_manager._find_all(customer_hierarchy_tree_class)[0]
        supplier_hierarchy_tree_class = entity_manager.get_entity_class("SupplierHierarchyTree")
        supplier_hierarchy_tree_entity = entity_manager._find_all(supplier_hierarchy_tree_class)[0]
        organizational_hierarchy_tree_class = entity_manager.get_entity_class("OrganizationalHierarchyTree")
        organizational_hierarchy_tree_entity = entity_manager._find_all(organizational_hierarchy_tree_class)[0]
        merchandise_hierarchy_tree_class = entity_manager.get_entity_class("MerchandiseHierarchyTree")
        merchandise_hierarchy_tree = entity_manager._find_all(merchandise_hierarchy_tree_class)[0]

        # create system settings, currencies and languages

        # initializes variable for deadlock protection
        last_foreign_key_queue_size = 0

        # try to connect all entities which have pending foreign keys until the foreign key queue is empty
        # @todo: this process can be made faster by using a graph
        print "##### PROCESSING FOREIGN KEY QUEUE #####"
        while len(self.foreign_key_queue):
            processed_foreign_keys = []

            # calculates the size of the queue after a iteration
            new_foreign_key_queue_size = len(self.foreign_key_queue)

            # if the queue size has not been updated since the last execution, then a deadlock is found
            if last_foreign_key_queue_size == new_foreign_key_queue_size:
                break
            else:
                last_foreign_key_queue_size = new_foreign_key_queue_size

            # try to process each key and store the processed keys
            for foreign_key_information in self.foreign_key_queue:
                entity_name = foreign_key_information["entity_name"]
                entity_object_id = foreign_key_information["entity_object_id"]
                entity_attribute_name = foreign_key_information["entity_attribute_name"]
                destination_entity_name = foreign_key_information["destination_entity_name"]
                destination_entity_object_id = foreign_key_information["destination_entity_object_id"]
                entity_class = entity_manager.get_entity_class(entity_name)
                entity = entity_manager.find_all(entity_class, entity_object_id, "object_id")[0]
                destination_entity_class = entity_manager.get_entity_class(destination_entity_name)
                destination_entities = entity_manager.find_all(destination_entity_class, destination_entity_object_id, "object_id")
                if len(destination_entities) == 1:
                    destination_entity = destination_entities[0]
                    setattr(entity, entity_attribute_name, destination_entity)
                    entity_manager.save_or_update(entity)
                    processed_foreign_keys.append(foreign_key_information)

            # remove the processed foreign keys from the foreign key queue
            for processed_foreign_key in processed_foreign_keys:
                self.foreign_key_queue.remove(processed_foreign_key)


        print "##### CONVERSION FINISHED #####"
        print "-> MISSING RELATIONS <-"
        for missing_relation in self.missing_relations:
            print missing_relation
        print "MISSING ASSOCIATIONS: " + str(len(self.foreign_key_queue))
        end_time = time.time()
        time_elapsed = end_time - start_time
        print "TIME ELAPSED: " + str(time_elapsed)

    # @todo: this method is temporary
    def convert_internal_attribute_name_to_omni_name(self, internal_entity_name, internal_attribute_name):
        map = {"address" : {"system_company" : "contactable_organizational_hierarchy_tree_node",
                            "customer" : "contactable_organizational_hierarchy_tree_node"},
               "payment" : {"sale" : "sales"},
               "card_payment" : {"payments" : "payment_lines"},
               "cash_payment" : {"payments" : "payment_lines"},
               "check_payment" : {"payments" : "payment_lines"},
               "product" : {"purchase_merchandise_hierarchy_tree_node" : "purchase_merchandise_hierarchy_tree_nodes"},

               "system_company" : {"preferred_languge" : "preferred_language"},
               "store" : {"sales_stockholder" : "sales_stockholders"},
               "financial_account" : {"contactable_organizational_hierarchy_tree_node" : "owners"},
               "product" : {"category" : "parent_nodes"},
               "customer_return" : {"return_site" : "return_sites",
                                    "merchandise_hierarchy_tree_node_return" : "merchandise_hierarchy_tree_node_returns",
                                    "sellers" : "return_processors",
                                    "return_processor" : "return_processors"},
               "supplier_return" : {"merchandise_hierarchy_tree_node_return" : "merchandise_hierarchy_tree_node_returns"},
               "sale_transaction" : {"money_sale" : "money_sale_slip",
                                     "returns" : "customer_returns"},
               "merchandise_hierarchy_tree_node_return" : {"product" : "merchandise",
                                                           "subproduct" : "merchandise",
                                                           "return" : "merchandise_return",
                                                           "consignment_supplier_return" : "merchandise_return"},
               "merchandise_contactable_organizational_hierarchy_tree_node" : {"product" : "merchandise",
                                                                               "merchandise_hierarchy_tree_node" : "merchandise",
                                                                               "store" : "contactable_organizational_hierarchy_tree_node",
                                                                               "subproduct" : "merchandise"},
               # @todo: warning
               "payment_line" : {"credit_notes" : "credit_note"},
               "repair" : {"purchase_merchandise_hierarchy_tree_node" : "purchase_merchandise_hierarchy_tree_nodes"},
               "stock_adjustment_merchandise_hierarchy_tree_node" : {"store" : "adjustment_target"},
               "credit_contract" : {"sale" : "sales"},
               "credit_note_payment" : {"payments" : "payment_lines"},
               "stock_adjustment" : {"reason" : "stock_adjustment_reason"},
               "transfer_merchandise_hierarchy_tree_node" : {"product" : "merchandise"},
               "contact_information" : {"supplier" : "contactable_organizational_hierarchy_tree_node",
                                        "customer" : "contactable_organizational_hierarchy_tree_node",
                                        "system_company" : "contactable_organizational_hierarchy_tree_node"},
               "media" : {"product" : "merchandise_hierarchy_tree_nodes",
                          "customer" : "contactable_organizational_hierarchy_tree_nodes",
                          "system_company" : "contactable_organizational_hierarchy_tree_nodes"},
               "purchase" : {"money_sale" : "money_sale_slip"},
               "PurchaseMerchandiseHierarchyTreeNode" : {"merchandise_hierarchy_tree_node" : "merchandise"}}

        if internal_entity_name in map and internal_attribute_name in map[internal_entity_name]:
            return map[internal_entity_name][internal_attribute_name]
        else:
            return internal_attribute_name

    # @todo: this method is temporary
    def convert_internal_entity_name_to_omni_name(self, internal_entity_name):
        map = {"supplier_person" : "SupplierCompany",
               "customer" : "CustomerPerson",
               "consignment_supplier_return" : "SupplierReturn",
               "subproduct" : "SubProduct",
               "system_company_employee" : "Employee",
               "supplier" : "SupplierCompany",
               "postdated_check_payment" : "PostDatedCheckPayment",
               "money_sale" : "MoneySaleSlip"}
        if internal_entity_name in map:
            return map[internal_entity_name]
        else:
            new_name = ""
            internal_entity_name_tokens = internal_entity_name.split("_")
            for token in internal_entity_name_tokens:
                new_name += token.capitalize()
            return new_name

    # @todo: this method is temporary
    def convert_entities(self, internal_structure, entity_manager, internal_structure_entity_name, default_values_map = {}, handlers = []):
        # convert the internal entities
        internal_entities = list(set(internal_structure.get_entities(internal_structure_entity_name)))
        for internal_entity_index in range(len(internal_entities)):
            if internal_entity_index > 0 and internal_entity_index % 50 == 0:
                break
                #print "Converting internal entity with object id = " + str(internal_entity.object_id) + " " + str(internal_entity_index) + " / " + str(len(internal_entities))

            internal_entity = internal_entities[internal_entity_index]
            # if the entity doesn't exist create a new one
            entity_name = self.convert_internal_entity_name_to_omni_name(internal_entity._name)
            entity_class = entity_manager.get_entity_class(entity_name)
            entities = entity_manager.find_all(entity_class, internal_entity.object_id, "object_id")
            if len(entities) == 0:
                entity = entity_class()
                fields = internal_entity.get_fields()

                # copy the values of the internal entity to the entity
                attribute_fields = [(field_name, field_value) for field_name, field_value in fields.items() if not field_value is None and not type(field_value) in (types.InstanceType, types.ListType)]
                for field_name, field_value in attribute_fields:
                     if field_name in default_values_map:
                        default_value = default_values_map[field_name]
                        if type(default_value) == types.FunctionType:
                            field_value = default_value(field_value)
                        del default_values_map[field_name]
                     # @todo: this is a hack
                     if type(field_value) in (types.StringType, types.FloatType, types.LongType, types.BooleanType):
                            field_value = unicode(field_value)
                     setattr(entity, field_name, field_value)

                # apply all remaining values default values
                for field_name, field_value in default_values_map.items():
                    if not type(field_value) == types.FunctionType:
                        setattr(internal_entity, field_name, field_value)

                entity.object_id = internal_entity.object_id

                # try to connect to the related entity in case it exists
                relation_fields = [(field_name, field_value) for field_name, field_value in fields.items() if not field_value is None and type(field_value) in (types.InstanceType, types.ListType)]
                for field_name, field_value in relation_fields:
                    entity_attribute_name = self.convert_internal_attribute_name_to_omni_name(internal_entity._name, field_name)
                    if not type(field_value) == types.ListType:
                        field_value = [field_value]
                    self.associate_entities(entity_manager, field_value, entity, entity_attribute_name)

                # execute all configured handlers for this entity
                for handler in handlers:
                    handler(self, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity)

                print "Saving " + entity_name + " with object id = " + str(entity.object_id)
                entity_manager.save(entity)

    # @todo: this method is temporary
    def associate_entities(self, entity_manager, internal_entities, entity, entity_attribute_name):
        if hasattr(entity, entity_attribute_name):
            entity_attribute = getattr(entity, entity_attribute_name)
            entity_name = entity.__class__.__name__

            # @todo: this is a hack for dealing with garbage data
            if internal_entities:
                for internal_entity in internal_entities:
                   # @todo: this is a hack for dealing with garbage data
                   if internal_entity:
                        internal_entity_name = internal_entity._name
                        internal_entity_class_name = self.convert_internal_entity_name_to_omni_name(internal_entity_name)
                        internal_entity_class = entity_manager.get_entity_class(internal_entity_class_name)
                        if internal_entity_class == None:
                            print "################################# " + internal_entity_name + " ##################################"
                        internal_entity_entities = entity_manager.find_all(internal_entity_class, internal_entity.object_id, "object_id")

                        # if the entity for the internal entity exists then create the association
                        if len(internal_entity_entities) == 1:
                            internal_entity_entity = internal_entity_entities[0]
                            # print "Associating " + entity_name + " with object id = " + str(entity.object_id) + " to " + internal_entity_class_name + " with object id = " + str(internal_entity.object_id)
                            if type(entity_attribute) == types.ListType:
                                entity_attribute.append(internal_entity_entity)
                            else:
                                entity_attribute = internal_entity_entity
                                break
                        else:
                            # otherwise add the association parameters to the foreign key queue
                            self.foreign_key_queue.append({
                                                  "entity_name" : entity_name,
                                                  "entity_object_id" : entity.object_id,
                                                  "entity_attribute_name" : entity_attribute_name,
                                                  "destination_entity_name" : internal_entity_class_name,
                                                  "destination_entity_object_id" : internal_entity.object_id})
                            # print "Failed to associate " + entity_name + " with object id = " + str(entity.object_id) + " to " + internal_entity_class_name + " with object id = " + str(internal_entity.object_id)

            # if the relation attribute is a list then remove duplicates
            # that may be caused by a second passing
            if type(entity_attribute) == types.ListType:
                entity_attribute = list(set(entity_attribute))

            setattr(entity, entity_attribute_name, entity_attribute)
        else:
            relation_name = entity.__class__.__name__ + "." + entity_attribute_name
            if not relation_name in self.missing_relations:
                self.missing_relations.append(relation_name)

    def process_work_units(self, task):
        """
        Performs the operations necessary to complete each of the specified work units.

        @type task: Task
        @param task: Task monitoring object used to inform the status of the query.
        @type work_units: List
        @param work_units: List of work units to complete.
        """

        # where the counter should start at for this operation
        COUNTER_OFFSET = 0
        # what range does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)
        COUNTER_RANGE = 50

        counter = COUNTER_OFFSET
        work_units = self.configuration.get_work_units()
        counter_inc = COUNTER_RANGE / len(work_units)
        for work_unit in work_units:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_work_unit(task, counter, counter_inc, work_unit)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()

    def process_work_unit(self, task, counter_offset, counter_range, work_unit_name):
        """
        Processes the domain_entitys indicated by the specified work unit.

        @type task: Task
        @param task: Task monitoring object used to inform the status of the query.
        @type counter_offset: int
        @param counter_offset: Where the progress counter should start at for this operation.
        @type counter_range: int
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)
        @type work_unit_name: String
        @param work_unit_name: Name of the work unit whose work will be performed.
        """

        self.logger.warn("Data converter adapter: Processing work unit '%s'.\n" % work_unit_name)

        counter = counter_offset
        domain_entity_names = self.configuration.get_domain_entities(work_unit_name)
        counter_inc = counter_range / len(domain_entity_names)
        for domain_entity_name in domain_entity_names:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_domain_entity(domain_entity_name)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()

                counter += counter_inc
                task.set_percentage_complete(counter)

        # process every foreign key that was placed in the queue
        self.process_foreign_key_queue()

        # processes handler that cleans all temporary structures
        self.process_handler("process_handler_clean", [self])

    def process_handler(self, handler_name, arguments):
        """
        Invokes a given handler function with the provided name and supplying the provided arguments.

        @type handler_name: String
        @param handler_name: Name of the handler function to invoke.
        @type arguments: List
        @param arguments: List of arguments that will be supplied to the handler function.
        @rtype: Object
        @return: The value returned by the handler.
        """

        self.logger.debug("Data converter adapter: Processing handler function '%s'.\n" % handler_name)

        if self.configuration.has_handler(handler_name):
            handler = self.configuration.get_handler(handler_name)
            return handler(arguments)

    def process_domain_entity(self, domain_entity_name):
        """
        Converts the domain entity's contents to the internal structure.

        @type domain_entity_name: String
        @param domain_entity_name: Name of the domain entity one wants to process.
        """

        self.logger.warn("Data converter adapter: Processing domain entity '%s'.\n" % domain_entity_name)

        domain_entity_configuration = self.input_description.get_domain_entity(domain_entity_name)
        domain_attribute_names = [domain_attribute_configuration.name for domain_attribute_configuration in domain_entity_configuration.get_domain_attributes()]
        domain_entities = self.connection.query(domain_entity_name, domain_attribute_names)

        for domain_entity in domain_entities:
            # create the entity related with the domain entity and a domain entity conversion information object
            domain_entity_internal_entity = self.internal_structure.add_entity(domain_entity_configuration.internal_entity)
            domain_entity_conversion_info = DomainEntityConversionInfo(domain_entity_configuration, self.internal_structure, domain_entity_internal_entity, domain_entity)
            # bind the entity's id to the domain entity's primary key
            self.process_primary_key(domain_entity_conversion_info)
            # process the domain entity's attributes
            self.process_domain_attributes(domain_entity_conversion_info)
            # run the handlers configured for this domain entity instance
            for handler in domain_entity_conversion_info.configuration.instance_handlers:
                self.process_handler(handler.name, [domain_entity_conversion_info, self])

        # run the global handlers configured for this domain entity
        for handler in domain_entity_configuration.global_handlers:
            self.process_handler(handler.name, [self])

    def process_domain_attributes(self, domain_entity_conversion_info):
        """
        Copies data from the database domain attributes to the internal structure entity attributes.

        @type domain_entity_conversion_info: DomainEntityConversionInfo
        @param domain_entity_conversion_info: Object containing information about this domain entity conversion process.
        """

        domain_entity_configuration = domain_entity_conversion_info.configuration
        domain_entity_internal_entity = domain_entity_conversion_info.internal_entity
        domain_entity = domain_entity_conversion_info.domain_entity

        # for every plain domain attribute, convert the value and send it to the associated entity instances
        for plain_domain_attribute in domain_entity_configuration.get_plain_domain_attributes():
            # if the plain domain attribute has an internal attribute target and it exists in the domain entity set
            if not plain_domain_attribute.internal_attribute is None and plain_domain_attribute.name in domain_entity:
                self.logger.debug("Data converter adapter: Processing domain_attribute '%s'.\n" % plain_domain_attribute.name)
                field_value = domain_entity[plain_domain_attribute.name]
                destination_internal_entity_name = domain_entity_internal_entity._name
                destination_internal_entity_id = domain_entity_internal_entity._id
                # if the domain attribute is pointing to a different internal entity than the domain entity then use that one instead and create a link to the domain entity' internal entity
                if plain_domain_attribute.internal_entity and plain_domain_attribute.internal_entity_id:
                    destination_internal_entity_name = plain_domain_attribute.internal_entity
                    destination_internal_entity_id = domain_entity_conversion_info.get_real_internal_entity_id(plain_domain_attribute.internal_entity, plain_domain_attribute.internal_entity_id)
                    self.internal_structure.set_field_value(destination_internal_entity_name, destination_internal_entity_id, domain_entity_internal_entity._name, domain_entity_internal_entity)
                # grab the domain entity and process it through its handlers
                for handler in plain_domain_attribute.handlers:
                    field_value = self.process_handler(handler.name, [field_value])
                # store the domain entity in the associated entity
                self.internal_structure.set_field_value(destination_internal_entity_name, destination_internal_entity_id, plain_domain_attribute.internal_attribute, field_value)

        # for every foreign key
        for foreign_key in domain_entity_configuration.foreign_keys:
            # compute the string representation of the foreign key
            foreign_key_domain_attribute_names = [foreign_key_domain_attribute.name for foreign_key_domain_attribute in foreign_key.domain_attributes]
            foreign_key_values = [domain_entity[foreign_key_domain_attribute.name] for foreign_key_domain_attribute in foreign_key.domain_attributes]

            # if one of the foreign key values is null then cancel the foreign key binding operation
            if None in foreign_key_values:
                break

            foreign_key_string = str(foreign_key_values)

            self.logger.debug("Data converter adapter: Processing foreign key '%s'.\n" % foreign_key_string)

            # if the foreign domain_entity the foreign key points to was already converted to an entity then create a relation to it
            foreign_domain_entity = self.input_description.get_domain_entity(foreign_key.foreign_domain_entity)
            foreign_domain_entity_conversion_info = self.get_domain_entity_conversion_info(foreign_domain_entity.internal_entity, foreign_key_string)
            if foreign_domain_entity_conversion_info:
               foreign_internal_entity_id = foreign_domain_entity_conversion_info.internal_entity._id
               foreign_internal_entity_instance = self.internal_structure.get_entity(foreign_domain_entity.internal_entity, foreign_internal_entity_id)
               self.internal_structure.set_field_value(domain_entity_internal_entity._name, domain_entity_internal_entity._id, foreign_domain_entity.internal_entity, foreign_internal_entity_instance)
            else: # otherwise add the foreign key to the queue
               self.foreign_key_queue.append({"foreign_key_string" : foreign_key_string,
                                              "foreign_key_internal_entity_name" : domain_entity_internal_entity._name,
                                              "foreign_key_internal_entity_id" : domain_entity_internal_entity._id,
                                              "foreign_internal_entity_name" : foreign_domain_entity.internal_entity})

    def process_primary_key(self, domain_entity_conversion_info):
        """
        Extracts the primary key value from the query domain_entity set and into the the internal structure. After this
        operation the domain entity set will not contain the primary key domain_attribute anymore.

        @type domain_entity_conversion_info: DomainEntityConversionInfo
        @param domain_entity_conversion_info: Object containing information about the domain entity conversion process.
        """

        domain_entity_configuration = domain_entity_conversion_info.configuration
        domain_entity = domain_entity_conversion_info.domain_entity

        # compute this domain_entity's primary key string representation
        primary_key_domain_attribute_names = [domain_attribute.name for domain_attribute in domain_entity_configuration.primary_key_domain_attributes]
        primary_key_string = str([domain_entity[primary_key_domain_attribute_name] for primary_key_domain_attribute_name in primary_key_domain_attribute_names])

        # associate the domain_entity conversion information with the primary key
        if not domain_entity_conversion_info.internal_entity._name in self.internal_entity_name_primary_key_domain_entity_conversion_info_map:
             self.internal_entity_name_primary_key_domain_entity_conversion_info_map[domain_entity_conversion_info.internal_entity._name] = {}
        primary_key_domain_entity_conversion_info_map = self.internal_entity_name_primary_key_domain_entity_conversion_info_map[domain_entity_conversion_info.internal_entity._name]
        primary_key_domain_entity_conversion_info_map[primary_key_string] = domain_entity_conversion_info

    def process_foreign_key_queue(self):
        """
        Process the foreign key queue.
        """

        # initializes variable for deadlock protection
        last_foreign_key_queue_size = 0

        # try to connect all entities which have pending foreign keys until the foreign key queue is empty
        # @todo: this process can be made faster by using a graph
        while len(self.foreign_key_queue):
            processed_foreign_keys = []

            # calculates the size of the queue after a iteration
            new_foreign_key_queue_size = len(self.foreign_key_queue)

            # if the queue size has not been updated since the last execution, then a deadlock is found
            if last_foreign_key_queue_size == new_foreign_key_queue_size:
                break
            else:
                last_foreign_key_queue_size = new_foreign_key_queue_size

            # try to process each key and store the processed keys
            for foreign_key_information in self.foreign_key_queue:
                foreign_key_internal_entity_name = foreign_key_information["foreign_key_internal_entity_name"]
                foreign_key_internal_entity_id = foreign_key_information["foreign_key_internal_entity_id"]
                foreign_internal_entity_name = foreign_key_information["foreign_internal_entity_name"]
                domain_entity_conversion_info = self.get_domain_entity_conversion_info(foreign_internal_entity_name, foreign_key_information["foreign_key_string"])
                if domain_entity_conversion_info:
                    foreign_internal_entity_id = domain_entity_conversion_info.internal_entity._id
                    foreign_internal_entity = self.internal_structure.get_entity(foreign_internal_entity_name, foreign_internal_entity_id)
                    self.internal_structure.set_field_value(foreign_key_internal_entity_name, foreign_key_internal_entity_id, foreign_internal_entity_name, foreign_internal_entity)
                    processed_foreign_keys.append(foreign_key_information)

            # remove the processed foreign keys from the foreign key queue
            for processed_foreign_key in processed_foreign_keys:
                self.foreign_key_queue.remove(processed_foreign_key)

    def get_domain_entity_conversion_info(self, entity_name, primary_key_string):
        """
        Retrieves the conversion information used

        @type entity_name: String
        @param entity_name: Name of the internal entity from which one wants to get an identifier.
        @type primary_key_string: String
        @param primary_key_string: String representation of associated primary key.
        @rtype: DomainEntityConversionInfo
        @return: Object with information on how the domain entity was converted to an entity.
        """

        if entity_name in self.internal_entity_name_primary_key_domain_entity_conversion_info_map:
            primary_key_domain_entity_conversion_info_map = self.internal_entity_name_primary_key_domain_entity_conversion_info_map[entity_name]
            if primary_key_string in primary_key_domain_entity_conversion_info_map:
                return primary_key_domain_entity_conversion_info_map[primary_key_string]

class DomainEntityConversionInfo:
    """
    Holds information about the conversion of a certain database domain_entity domain_entity.
    """

    configuration = None
    """ Domain entity configuration object describing the domain entity this domain_entity belongs to """

    internal_structure = None
    """ Intermediate structure where the data converter input adapter's results are stored """

    internal_entity = None
    """ The internal entity created for this domain entity """

    domain_entity = None
    """ Source medium domain entity domain entity """

    internal_entity_configuration_id_internal_id_map = {}
    """ Dictionary relating the unique identifier of an internal entity instance in a domain entity's configuration file with the internal entity instance's real id """

    def __init__(self, configuration, internal_structure, internal_entity, domain_entity):
        """
        Class constructor.

        @type configuration: Object
        @param configuration: Object representing the conversion configuration for this domain entity.
        @type internal_structure: InternalStructure
        @param internal_structure: Intermediate structure where the data converter input adapter's results are stored.
        @type internal_entity: String
        @param internal_entity: The internal entity created for this domain entity.
        @type domain_entity: Dictionary
        @param domain_entity: The domain entity being converted.
        """

        self.configuration = configuration
        self.internal_entity = internal_entity
        self.internal_structure = internal_structure
        self.domain_entity = domain_entity
        self.internal_entity_configuration_id_internal_id_map = {}

    def get_real_internal_entity_id(self, internal_entity_name, domain_entity_configuration_internal_entity_id):
        """
        Retrieves the equivalent internal entity id in the internal structure for the provided
        internal entity id in the configuration file.

        @type internal_entity_name: String
        @param internal_entity_name: Name of the internal entity.
        @type domain_entity_configuration_internal_entity_id: int
        @param domain_entity_configuration_internal_entity_id: Identification number of the internal entity in the configuration file.
        @rtype: int
        @return: Returns the internal entity's unique identifier in the internal structure.
        """

        key = (internal_entity_name, domain_entity_configuration_internal_entity_id)
        if not key in self.internal_entity_configuration_id_internal_id_map:
            internal_entity = self.internal_structure.add_entity(internal_entity_name)
            self.internal_entity_configuration_id_internal_id_map[key] = internal_entity._id
        return self.internal_entity_configuration_id_internal_id_map[key]
