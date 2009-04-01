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

    def convert_internal_entity_name_to_omni_name(self, internal_entity_name):
        map = {"supplier_person" : "SupplierCompany"}
        if internal_entity_name in map:
            return map[internal_entity_name]
        else:
            new_name = ""
            internal_entity_name_tokens = internal_entity_name.split("_")
            for token in internal_entity_name_tokens:
                new_name += token.capitalize()
            return new_name

    def associate_entities(self, entity_manager, internal_entities, entity, entity_attribute_name):
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
                    internal_entity_entities = entity_manager.find_all(internal_entity_class, internal_entity.object_id, "object_id")
                    if len(internal_entity_entities) == 1:
                        internal_entity_entity = internal_entity_entities[0]
                        print "Associating " + entity_name + " with object id = " + str(entity.object_id) + " to " + internal_entity_class_name + " with object id = " + str(internal_entity.object_id)
                        if type(entity_attribute) == types.ListType:
                            entity_attribute.append(internal_entity_entity)
                        else:
                            entity_attribute = internal_entity_entity
                            break
                    else:
                        print "[WARNING] Failed to associate " + entity_name + " with object id = " + str(entity.object_id) + " to " + internal_entity_class_name + " with object id = " + str(internal_entity.object_id)

        setattr(entity, entity_attribute_name, entity_attribute)
    
    def convert_omni(self, internal_structure):
        # retrieves the entity manager plugin
        entity_manager_plugin = self.data_converter_plugin.entity_manager_plugin

        # retrieves the resource manager plugin
        resource_manager_plugin = self.data_converter_plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # creates a new entity manager
        entity_manager = entity_manager_plugin.load_entity_manager("sqlite")

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters({"file_path" : user_home_path + "/conversion_database.db", "autocommit" : False})

        # loads the entity manager
        entity_manager.load_entity_manager()

        # organizational hierarchy
        self.convert_system_company(internal_structure, entity_manager)
        self.convert_store(internal_structure, entity_manager)
        self.convert_system_company_employee(internal_structure, entity_manager)
        
        # users and access
        self.convert_users(internal_structure, entity_manager)
        
        # misc
        self.convert_reason(internal_structure, entity_manager)
        self.convert_location(internal_structure, entity_manager)
        
#       # @todo: float bug
#       #self.convert_vat_class(internal_structure, entity_manager) 
        
        # customer
        self.convert_customer_company(internal_structure, entity_manager)
        self.convert_customer_person(internal_structure, entity_manager)
        
        # supplier
        self.convert_supplier_company(internal_structure, entity_manager)
        self.convert_supplier_employee(internal_structure, entity_manager)
        self.convert_supplier_person(internal_structure, entity_manager)
        
        # address/contact/financial info
        self.convert_address(internal_structure, entity_manager)
        self.convert_contact_information(internal_structure, entity_manager)
        self.convert_financial_account(internal_structure, entity_manager)
        
        # person relation
        self.convert_person_relation(internal_structure, entity_manager)
        
        # merchandise
        self.convert_category(internal_structure, entity_manager)
        self.convert_collection(internal_structure, entity_manager)
        self.convert_product(internal_structure, entity_manager)
        self.convert_sub_product(internal_structure, entity_manager)
        self.convert_repair(internal_structure, entity_manager)
        
        # media
        self.convert_media(internal_structure, entity_manager)
        
        # catalog
        self.convert_organizational_merchandise_hierarchy_tree_node_vat_class(internal_structure, entity_manager)

#        # @todo: create this entity: self.convert_organizational_hierarchy_merchandise_supplier(internal_structure, entity_manager)
#        self.convert_merchandise_contactable_organizational_hierarchy_tree_node(internal_structure, entity_manager)
#        
#        # stock adjustments
#        self.convert_stock_adjustment(internal_structure, entity_manager)
#        self.convert_stock_adjustment_merchandise_hierarchy_tree_node(internal_structure, entity_manager)
#        
#        # consignments
#        self.convert_consignment(internal_structure, entity_manager)
#        # @todo: create this entity and associate it with the consignment: self.convert_consignation_slip(internal_structure, entity_manager)
#        self.convert_consignment_merchandise_hierarchy_tree_node(internal_structure, entity_manager)
#        
#        # purchases
#        self.convert_purchase(internal_structure, entity_manager)
#        self.convert_purchase_merchandise_hierarchy_tree_node(internal_structure, entity_manager)
#        
        # sales
        self.convert_payment_terms(internal_structure, entity_manager)
#        self.convert_sale_transaction(internal_structure, entity_manager)
#        self.convert_sale_merchandise_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node(internal_structure, entity_manager)
#        self.convert_shipment(internal_structure, entity_manager)
#        
#        # sales and purchases documents
#        self.convert_invoice(internal_structure, entity_manager)
#        # @todo: create this entity and associate it with the sale: self.convert_money_sale(internal_structure, entity_manager)
#        self.convert_receipt(internal_structure, entity_manager)
#        
#        self.convert_supplier_return(internal_structure, entity_manager)
#        self.convert_customer_return(internal_structure, entity_manager)
#        # @todo: create this entity and associate it with the consignment, return_requester, supplier and return_lines: self.convert_consignment_return(internal_structure, entity_manager)
#        self.convert_merchandise_hierarchy_tree_node_return(internal_structure, entity_manager)
#        self.convert_credit_note(internal_structure, entity_manager)
     
        # payment
        self.convert_card_payment(internal_structure, entity_manager)
        self.convert_cash_payment(internal_structure, entity_manager)
        self.convert_check_payment(internal_structure, entity_manager)
        self.convert_credit_note_payment(internal_structure, entity_manager)

#        # @todo: create this entity: self.convert_postdated_check_payment(internal_structure, entity_manager)
#        # @todo: create this entity: self.convert_gift_certificate_payment(internal_structure, entity_manager)
#        self.convert_gift_certificate(internal_structure, entity_manager)
#        self.convert_credit_contract(internal_structure, entity_manager)
#        self.convert_credit_payment(internal_structure, entity_manager)
#        self.convert_payment(internal_structure, entity_manager)
#        self.convert_payment_line(internal_structure, entity_manager)
#        
#        # transfers
#        self.convert_transfer(internal_structure, entity_manager)
#        self.convert_transfer_merchandise_hierarchy_tree_node(internal_structure, entity_manager)
#        
        
    def convert_system_company(self, internal_structure, entity_manager):
        print "###### CONVERTING SYSTEM COMPANIES ######"
        
        # @todo: set system company as root node
        entity_manager.create_transaction("system_company_transaction")
                
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

        # handler used to associate the system company with the organizational hierarchy tree as root node
        def system_company_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
           # retrieve the portuguese language entity
           language_class = entity_manager.get_entity_class("Language")
           portuguese_language_entity = entity_manager.find_all(language_class, "portugues", "name")[0]
            
           # retrieve the euro currency entity
           currency_class = entity_manager.get_entity_class("Currency")
           euro_currency_entity = entity_manager.find_all(currency_class, "euro", "name")[0]
            
#          # create the system settings entity
#          system_settings_class = entity_manager.get_entity_class("SystemSettings")
#          system_settings_entity = system_settings_class()
#          internal_structure.object_id += 1
#          system_settings_entity.object_id = internal_structure.object_id
#          system_settings_entity.preferred_currency = euro_currency_entity
#          system_settings_entity.preferred_language = portuguese_language_entity
#          system_settings_entity.system_company = entity
#          entity_manager.save(system_settings_entity)
          
           # add the system company to the organizational hierarchy tree's root node
           organizational_hierarchy_tree_class = entity_manager.get_entity_class("OrganizationalHierarchyTree")
           organizational_hierarchy_tree_entity = entity_manager._find_all(organizational_hierarchy_tree_class)[0]
           entity.parent_nodes = [organizational_hierarchy_tree_entity.root_node]
           print "Associating SystemCompany with object id = " + str(entity.object_id) + " to OrganizationalHierarchyTree root node with object id = " + str(organizational_hierarchy_tree_entity.root_node.object_id)

        self.convert_entity(internal_structure, entity_manager, "system_company", "SystemCompany", {"status" : 0}, [system_company_handler])
        entity_manager.commit_transaction("system_company_transaction")

    def convert_store(self, internal_structure, entity_manager):
        print "###### CONVERTING STORES ######"
        
        entity_manager.create_transaction("store_transaction")
        
        # handler used to associate the store with the system company
        def store_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            system_companies = internal_structure.get_entities("system_company")
            
            # @todo: remove this once bidirectional relations exist in the internal structure
            for system_company in system_companies:
                for child_node in system_company.child_nodes:
                    if child_node.object_id == entity.object_id:
                        adapter.associate_entities(entity_manager, [child_node], entity, "parent_nodes")
                        break

        self.convert_entity(internal_structure, entity_manager, "store", "Store", {"status" : 0}, [store_handler])
        entity_manager.commit_transaction("store_transaction")

    def convert_system_company_employee(self, internal_structure, entity_manager):
        print "###### CONVERTING SYSTEM COMPANY EMPLOYEES ######"
        
        entity_manager.create_transaction("system_company_employee_transaction")

        def system_company_employee_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            if hasattr(internal_entity, "parent_nodes"):
                adapter.associate_entities(entity_manager, internal_entity.parent_nodes, entity, "parent_nodes")
            else:
                organizational_hierarchy_tree_class = entity_manager.get_entity_class("OrganizationalHierarchyTree")
                organizational_hierarchy_tree_entity = entity_manager._find_all(organizational_hierarchy_tree_class)[0]
                entity.parent_nodes = [organizational_hierarchy_tree_entity.root_node]
                print "Associating Employee with object id = " + str(entity.object_id) + " to OrganizationalHierarchyTree root node with object id = " + str(organizational_hierarchy_tree_entity.root_node.object_id)

        self.convert_entity(internal_structure, entity_manager, "system_company_employee", "Employee", {}, [system_company_employee_handler])
        entity_manager.commit_transaction("system_company_employee_transaction")

    def convert_users(self, internal_structure, entity_manager):
        print "###### CONVERTING USERS ######"
        
        entity_manager.create_transaction("users_transaction")
        
        # create the users group
        user_group_class = entity_manager.get_entity_class("UserGroup")
        user_group_users_entity = user_group_class()
        user_group_users_entity.description = "The users user group"
        internal_structure.object_id += 1
        user_group_users_entity.object_id = internal_structure.object_id
        print "Saving UserGroup with object id = " + str(internal_structure.object_id)
        entity_manager.save(user_group_users_entity)
        
        # handler used to associate the user with its profile
        def user_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            profile_class = entity_manager.get_entity_class("Profile")
            user_group_class = entity_manager.get_entity_class("UserGroup")
            user_group_users_entity = entity_manager.find_all(user_group_class, "The users user group", "description")[0]
            user_profile_entity = profile_class()
            user_profile_entity.user_groups = [user_group_users_entity]
            user_profile_entity.user = entity
            internal_structure.object_id += 1
            user_profile_entity.object_id = internal_structure.object_id
            print "Associating user group with object id = " + str(user_group_users_entity.object_id) + " to user profile with object id = " + str(user_profile_entity.object_id)
            print "Saving user profile with object id = " + str(user_profile_entity.object_id)
            entity_manager.save(user_profile_entity)
            entity.profiles = [user_profile_entity]
            if hasattr(internal_entity, "system_company_employee"):
                employee_class = entity_manager.get_entity_class("Employee")
                system_company_employee_entities = entity_manager.find_all(employee_class, internal_entity.system_company_employee.object_id, "object_id")
                if len(system_company_employee_entities) == 1:
                    entity.person = system_company_employee_entities[0]
                    print "Associating Employee with object id = " + str(entity.person.object_id) + " to User with object id = " + str(entity.object_id)
            
        self.convert_entity(internal_structure, entity_manager, "user", "User", {"password_hash" : lambda value: base64.b64encode(md5.new(value).digest()),
                                                                                 "password_hash_type" : "md5",
                                                                                 "secret_answer_hash" : lambda value: base64.b64encode(md5.new(value).digest()),
                                                                                 "secret_answer_hash_type" : "md5",
                                                                                 "status" : 0}, [user_handler])

        entity_manager.commit_transaction("users_transaction")

    def convert_reason(self, internal_structure, entity_manager):
        print "###### CONVERTING REASONS ######"
        
        entity_manager.create_transaction("reason_transaction")
        self.convert_entity(internal_structure, entity_manager, "reason", "Reason")
        entity_manager.commit_transaction("reason_transaction")

    def convert_location(self, internal_structure, entity_manager):
        print "###### CONVERTING LOCATIONS ######"
        
        entity_manager.create_transaction("location_transaction")

        def location_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            customer_hierarchy_tree_class = entity_manager.get_entity_class("CustomerHierarchyTree")
            customer_hierarchy_tree_entity = entity_manager._find_all(customer_hierarchy_tree_class)[0]
            supplier_hierarchy_tree_class = entity_manager.get_entity_class("SupplierHierarchyTree")
            supplier_hierarchy_tree_entity = entity_manager._find_all(customer_hierarchy_tree_class)[0]
            entity.parent_nodes = [customer_hierarchy_tree_entity.root_node, supplier_hierarchy_tree_entity.root_node]
            print "Associating Location with object id = " + str(entity.object_id) + " to CustomerHierarchyTree root node with object id = " + str(customer_hierarchy_tree_entity.root_node.object_id) + " and to supplier hierarchy tree root node with object id = " + str(supplier_hierarchy_tree_entity.root_node.object_id)
            
        self.convert_entity(internal_structure, entity_manager, "location", "Location", {}, [location_handler])
        entity_manager.commit_transaction("location_transaction")

    def convert_vat_class(self, internal_structure, entity_manager):
        # @todo: associate with system_company as contactable_organizational_hierarchy_tree_node
        entity_manager.create_transaction("vat_class_transaction")
        self.convert_entity(internal_structure, entity_manager, "vat_class", "VatClass")
        entity_manager.commit_transaction("vat_class_transaction")

    def convert_customer_person(self, internal_structure, entity_manager):
        print "###### CONVERTING CUSTOMER PERSONS ######"
        
        entity_manager.create_transaction("customer_person_transaction")
                
        # handler used to associate the customer person with the customer hierarchy tree's root node
        def customer_person_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            customer_hierarchy_tree_class = entity_manager.get_entity_class("CustomerHierarchyTree")
            customer_hierarchy_tree_entity = entity_manager._find_all(customer_hierarchy_tree_class)[0]
            entity.parent_nodes = [customer_hierarchy_tree_entity.root_node]
            print "Associating CustomerPerson with object id = " + str(entity.object_id) + " to CustomerHierarchyTree root node with object id = " + str(customer_hierarchy_tree_entity.root_node.object_id)
        
        # @todo: remove garbage parent nodes and child nodes from the internal structure
        self.convert_entity(internal_structure, entity_manager, "customer_person", "CustomerPerson", {}, [customer_person_handler])
        entity_manager.commit_transaction("customer_person_transaction")
    
    def convert_customer_company(self, internal_structure, entity_manager):
        print "###### CONVERTING CUSTOMER COMPANIES ######"
        
        entity_manager.create_transaction("customer_company_transaction")
        
        # handler used to associate the customer company with the customer hierarchy tree's root node
        def customer_company_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            customer_hierarchy_tree_class = entity_manager.get_entity_class("CustomerHierarchyTree")
            customer_hierarchy_tree_entity = entity_manager._find_all(customer_hierarchy_tree_class)[0]
            entity.parent_nodes = [customer_hierarchy_tree_entity.root_node]
            print "Associating CustomerCompany with object id = " + str(entity.object_id) + " to CustomerHierarchyTree with object id = " + str(customer_hierarchy_tree_entity.root_node.object_id)

        # @todo: remove garbage parent nodes and child nodes from the internal structure
        self.convert_entity(internal_structure, entity_manager, "customer_company", "CustomerCompany", {}, [customer_company_handler])
        entity_manager.commit_transaction("customer_company_transaction")

    def convert_supplier_company(self, internal_structure, entity_manager):
        print "###### CONVERTING SUPPLIER COMPANIES ######"
        
        entity_manager.create_transaction("supplier_company_transaction")
        
        # handler used to associate the supplier company with the supplier hierarchy tree's root node
        def supplier_company_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            supplier_hierarchy_tree_class = entity_manager.get_entity_class("SupplierHierarchyTree")
            supplier_hierarchy_tree_entity = entity_manager._find_all(supplier_hierarchy_tree_class)[0]
            entity.parent_nodes = [supplier_hierarchy_tree_entity.root_node]
            print "Associating SupplierCompany with object id = " + str(entity.object_id) + " to SupplierHierarchyTree root node with object id = " + str(supplier_hierarchy_tree_entity.root_node.object_id)
    
        self.convert_entity(internal_structure, entity_manager, "supplier_company", "SupplierCompany", {}, [supplier_company_handler])
        entity_manager.commit_transaction("supplier_company_transaction")

    def convert_supplier_employee(self, internal_structure, entity_manager):
        print "###### CONVERTING SUPPLIER EMPLOYEES ######"
        
        entity_manager.create_transaction("supplier_employee_transaction")
        
        # handler used to associate the supplier employee with the supplier hierarchy tree's root node
        def supplier_employee_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            supplier_hierarchy_tree_class = entity_manager.get_entity_class("SupplierHierarchyTree")
            supplier_hierarchy_tree_entity = entity_manager._find_all(supplier_hierarchy_tree_class)[0]
            entity.parent_nodes = [supplier_hierarchy_tree_entity.root_node]
            print "Associating SupplierEmployee with object id = " + str(entity.object_id) + " to SupplierHierarchyTree root node with object id = " + str(supplier_hierarchy_tree_entity.root_node.object_id)
            
        self.convert_entity(internal_structure, entity_manager, "supplier_employee", "SupplierEmployee", {}, [supplier_employee_handler])
        entity_manager.commit_transaction("supplier_employee_transaction")

    def convert_supplier_person(self, internal_structure, entity_manager):
        print "###### CONVERTING SUPPLIER PERSONS ######"
        
        entity_manager.create_transaction("supplier_person_transaction")
        
        # handler used to associate the supplier person with the supplier hierarchy tree's root node
        def supplier_person_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            supplier_hierarchy_tree_class = entity_manager.get_entity_class("SupplierHierarchyTree")
            supplier_hierarchy_tree_entity = entity_manager._find_all(supplier_hierarchy_tree_class)[0]
            entity.parent_nodes = [supplier_hierarchy_tree_entity.root_node]
            print "Associating Person with object id = " + str(entity.object_id) + " to SupplierHierarchyTree root node with object id = " + str(supplier_hierarchy_tree_entity.root_node.object_id)
            
        self.convert_entity(internal_structure, entity_manager, "supplier_person", "Person", {}, [supplier_person_handler])
        entity_manager.commit_transaction("supplier_person_transaction")

    def convert_address(self, internal_structure, entity_manager):
        print "###### CONVERTING ADDRESSES ######"
        
        entity_manager.create_transaction("address_transaction")

        def address_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            if hasattr(internal_entity, "contactable_organizational_hierarchy_tree_node"):
                adapter.associate_entities(entity_manager, [internal_entity.contactable_organizational_hierarchy_tree_node], entity, "contactable_organizational_hierarchy_tree_node")
            elif hasattr(internal_entity, "system_company"):
                adapter.associate_entities(entity_manager, [internal_entity.system_company], entity, "contactable_organizational_hierarchy_tree_node")
                
        self.convert_entity(internal_structure, entity_manager, "address", "Address", {}, [address_handler])
        entity_manager.commit_transaction("address_transaction")

    def convert_contact_information(self, internal_structure, entity_manager):
        print "###### CONVERTING CONTACT INFORMATIONS ######"
        
        entity_manager.create_transaction("contact_information_transaction")
        
        def contact_information_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            if hasattr(internal_entity, "contactable_organizational_hierarchy_tree_node"):
                adapter.associate_entities(entity_manager, [internal_entity.contactable_organizational_hierarchy_tree_node], entity, "contactable_organizational_hierarchy_tree_node")
            elif hasattr(internal_entity, "system_company"):
                adapter.associate_entities(entity_manager, [internal_entity.system_company], entity, "contactable_organizational_hierarchy_tree_node")
        
        self.convert_entity(internal_structure, entity_manager, "contact_information", "ContactInformation")
        entity_manager.commit_transaction("contact_information_transaction")    

    def convert_financial_account(self, internal_structure, entity_manager):
        print "###### CONVERTING FINANCIAL ACCOUNTS ######"
        
        entity_manager.create_transaction("financial_account_transaction")
        
        def financial_account_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
             if hasattr(internal_entity, "contactable_organizational_hierarchy_tree_node"):
                adapter.associate_entities(entity_manager, [internal_entity.contactable_organizational_hierarchy_tree_node], entity, "owners")

        self.convert_entity(internal_structure, entity_manager, "financial_account", "FinancialAccount", {}, [financial_account_handler])
        entity_manager.commit_transaction("financial_account_transaction")

    def convert_person_relation(self, internal_structure, entity_manager):
        print "###### CONVERTING PERSON RELATIONS ######"
        
        entity_manager.create_transaction("person_relation_transaction")
        
        def person_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            first_person_class = entity_manager.get_entity_class(self.convert_internal_entity_name_to_omni_name(internal_entity.first_person._name))
            first_person_entity = entity_manager.find_all(first_person_class, internal_entity.first_person.object_id, "object_id")[0]
            second_person_class = entity_manager.get_entity_class(self.convert_internal_entity_name_to_omni_name(internal_entity.second_person._name))
            second_person_entity = entity_manager.find_all(second_person_class, internal_entity.second_person.object_id, "object_id")[0]
            entity.first_person = first_person_entity
            entity.second_person = second_person_entity    
            print "Associating PersonRelation between with object id = " + str(entity.object_id) + " between Person with object id = " + str(entity.first_person.object_id) + " and Person with object id = " + str(entity.second_person.object_id)

        self.convert_entity(internal_structure, entity_manager, "person_relation", "PersonRelation", {}, [person_handler])
        
        entity_manager.commit_transaction("person_relation_transaction")

    def convert_category(self, internal_structure, entity_manager):
        print "###### CONVERTING CATEGORIES ######"
        
        entity_manager.create_transaction("category_transaction")

        def category_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            # if the internal entity has parent nodes defined then add the collection to the parent nodes
            if hasattr(internal_entity, "parent_nodes"):
                adapter.associate_entities(entity_manager, internal_entity.parent_nodes, entity, "parent_nodes")
            else:
                # otherwise add to the merchandise root node
                merchandise_hierarchy_tree_class = entity_manager.get_entity_class("MerchandiseHierarchyTree")
                merchandise_hierarchy_tree = entity_manager._find_all(merchandise_hierarchy_tree_class)[0]
                entity.parent_nodes = [merchandise_hierarchy_tree.root_node]
                print "Associating Category with object id = " + str(entity.object_id) + " to MerchandiseHierarchyTree root node with object id = " + str(merchandise_hierarchy_tree.root_node.object_id)

        self.convert_entity(internal_structure, entity_manager, "category", "Category", {}, [category_handler])
        entity_manager.commit_transaction("category_transaction")
    
    def convert_collection(self, internal_structure, entity_manager):
        print "###### CONVERTING COLLECTIONS ######"
        
        entity_manager.create_transaction("collection_transaction")

        def collection_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            # if the internal entity has parent nodes defined then add the collection to the parent nodes
            if hasattr(internal_entity, "parent_nodes"):
                adapter.associate_entities(entity_manager, internal_entity.parent_nodes, entity, "parent_nodes")
            else:
                # otherwise add to the merchandise root node
                merchandise_hierarchy_tree_class = entity_manager.get_entity_class("MerchandiseHierarchyTree")
                merchandise_hierarchy_tree = entity_manager._find_all(merchandise_hierarchy_tree_class)[0]
                entity.parent_nodes = [merchandise_hierarchy_tree.root_node]
                print "Associating Collection with object id = " + str(entity.object_id) + " to MerchandiseHierarchyTree root node with object id = " + str(merchandise_hierarchy_tree.root_node.object_id)

        self.convert_entity(internal_structure, entity_manager, "collection", "Collection", {}, [collection_handler])
        entity_manager.commit_transaction("collection_transaction")

    def convert_product(self, internal_structure, entity_manager):
        print "###### CONVERTING PRODUCTS ######"
        
        entity_manager.create_transaction("product_transaction")

        def product_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            # if the internal entity has parent nodes defined then add the collection to the parent nodes
            if hasattr(internal_entity, "parent_nodes"):
                adapter.associate_entities(entity_manager, internal_entity.parent_nodes, entity, "parent_nodes")
            else:
                # otherwise add to the merchandise root node
                merchandise_hierarchy_tree_class = entity_manager.get_entity_class("MerchandiseHierarchyTree")
                merchandise_hierarchy_tree = entity_manager._find_all(merchandise_hierarchy_tree_class)[0]
                entity.parent_nodes = [merchandise_hierarchy_tree.root_node]
                print "Associating Product with object id = " + str(entity.object_id) + " to MerchandiseHierarchyTree root node with object id = " + str(merchandise_hierarchy_tree.root_node.object_id)
            
            if hasattr(internal_entity, "commercialization_suppliers"):
                adapter.associate_entities(entity_manager, internal_entity.commercialization_suppliers, entity, "parent_nodes")
                           
        self.convert_entity(internal_structure, entity_manager, "product", "Product", {}, [product_handler])
        entity_manager.commit_transaction("product_transaction")

    def convert_sub_product(self, internal_structure, entity_manager):
        print "###### CONVERTING SUB-PRODUCTS ######"

        entity_manager.create_transaction("sub_product_transaction")
        
        def sub_product_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            if hasattr(internal_entity, "parent_nodes"):
                adapter.associate_entities(entity_manager, internal_entity.parent_nodes, entity, "parent_nodes")
            
            if hasattr(internal_entity, "commercialization_suppliers"):
                adapter.associate_entities(entity_manager, internal_entity.commercialization_suppliers, entity, "parent_nodes")
        
        self.convert_entity(internal_structure, entity_manager, "sub_product", "SubProduct", {}, [sub_product_handler])
        entity_manager.commit_transaction("sub_product_transaction")

    def convert_repair(self, internal_structure, entity_manager):
        entity_manager.create_transaction("repair_transaction")
        
        def repair_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            # if the internal entity has parent nodes defined then add the collection to the parent nodes
            if hasattr(internal_entity, "parent_nodes"):
                adapter.associate_entities(entity_manager, internal_entity.parent_nodes, entity, "parent_nodes")
            else:
                # otherwise add to the merchandise root node
                merchandise_hierarchy_tree_class = entity_manager.get_entity_class("MerchandiseHierarchyTree")
                merchandise_hierarchy_tree = entity_manager._find_all(merchandise_hierarchy_tree_class)[0]
                entity.parent_nodes = [merchandise_hierarchy_tree.root_node]
                print "Associating Repair with object id = " + str(entity.object_id) + " to MerchandiseHierarchyTree root node with object id = " + str(merchandise_hierarchy_tree.root_node.object_id)
        
        self.convert_entity(internal_structure, entity_manager, "repair", "Repair", {}, [repair_handler])
        entity_manager.commit_transaction("repair_transaction")

    def convert_media(self, internal_structure, entity_manager):      
        entity_manager.create_transaction("media_transaction")
        
        # @todo: any more entities references ? 
        # @todo: primary media
        # @todo: load images from path
        def media_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            if hasattr(internal_entity, "product"):
                adapter.associate_entities(entity_manager, [internal_entity.product], entity, "merchandise_hierarchy_tree_nodes")
    
            if hasattr(internal_entity, "system_company"):
                adapter.associate_entities(entity_manager, [internal_entity.system_company], entity, "contactable_organizational_hierarchy_tree_nodes")
        
        self.convert_entity(internal_structure, entity_manager, "media", "Media", {}, [media_handler])
        entity_manager.commit_transaction("media_transaction")

    def convert_organizational_merchandise_hierarchy_tree_node_vat_class(self, internal_structure, entity_manager):
        def organizational_merchandise_hierarchy_tree_node_vat_class_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            if hasattr(internal_entity, "merchandise"):
                adapter.associate_entities(entity_manager, [internal_entity.merchandise], entity, "merchandise")

            if hasattr(internal_entity, "organizational_hierarchy_tree_node"):
                adapter.associate_entities(entity_manager, [internal_entity.organizational_hierarchy_tree_node], entity, "organizational_hierarchy_tree_node")
    
            if hasattr(internal_entity, "vat_class"):
                adapter.associate_entities(entity_manager, [internal_entity.vat_class], entity, "vat_class")
                    
        entity_manager.create_transaction("organizational_merchandise_hierarchy_tree_node_vat_class_transaction")
        self.convert_entity(internal_structure, entity_manager, "organizational_merchandise_hierarchy_tree_node_vat_class", "OrganizationalMerchandiseHierarchyTreeNodeVatClass", {}, [organizational_merchandise_hierarchy_tree_node_vat_class_handler])
        entity_manager.commit_transaction("organizational_merchandise_hierarchy_tree_node_vat_class_transaction")

    def convert_card_payment(self, internal_structure, entity_manager):
        entity_manager.create_transaction("card_payment_transaction")
        self.convert_entity(internal_structure, entity_manager, "card_payment", "CardPayment")
        entity_manager.commit_transaction("card_payment_transaction")

    def convert_cash_payment(self, internal_structure, entity_manager):
        entity_manager.create_transaction("cash_payment_transaction")       
        self.convert_entity(internal_structure, entity_manager, "cash_payment", "CashPayment")
        entity_manager.commit_transaction("cash_payment_transaction")

    def convert_check_payment(self, internal_structure, entity_manager):
        entity_manager.create_transaction("check_payment_transaction")
        self.convert_entity(internal_structure, entity_manager, "check_payment", "CheckPayment")
        entity_manager.commit_transaction("check_payment_transaction")

    def convert_consignation_slip(self, internal_structure, entity_manager):
        entity_manager.create_transaction("consignation_slip_transaction")
        self.convert_entity(internal_structure, entity_manager, "consignation_slip", "ConsignationSlip")
        entity_manager.commit_transaction("consignation_slip_transaction")

    def convert_consignment(self, internal_structure, entity_manager):
        entity_manager.create_transaction("consignment_transaction")
        
        # @todo: add buyer and supplier relations to data model
        def consignment_handler(adapter, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity):
            if hasattr(internal_entity, "buyers"):
                adapter.associate_entities(entity_manager, internal_entity.buyers, entity, "buyers")
            if hasattr(internal_entity, "supplier"):
                adapter.associate_entities(entity_manager, internal_entity.supplier, entity, "supplier")

        self.convert_entity(internal_structure, entity_manager, "consignment", "Consignment", {}, [consignment_handler])
        entity_manager.commit_transaction("consignment_transaction")
    
    # @todo: refactor this code
    def convert_consignment_merchandise_hierarchy_tree_node(self, internal_structure, entity_manager):
        # @todo: associate with Consignment
        # @todo: associate with TransactionalMerchandise as merchandise
        # @todo: set default values
        entity_manager.create_transaction("consignment_merchandise_hierarchy_tree_node")
        self.convert_entity(internal_structure, entity_manager, "consignment_merchandise_hierarchy_tree_node", "ConsignmentMerchandiseHierarchyTreeNode")
        entity_manager.commit_transaction("consignment_merchandise_hierarchy_tree_node")
    
    # @todo: refactor this code
    def convert_credit_contract(self, internal_structure, entity_manager):
        # @todo: associate with SaleTransaction as sales
        entity_manager.create_transaction("credit_contract_transaction")
        self.convert_entity(internal_structure, entity_manager, "credit_contract", "CreditContract")
        entity_manager.commit_transaction("credit_contract_transaction")    
    
    # @todo: refactor this code
    def convert_credit_note(self, internal_structure, entity_manager):
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as return_point
        # @todo: associate with CustomerReturn as customer_return
        # @todo: associate with SupplierReturn as supplier_return
        entity_manager.create_transaction("credit_note_transaction")
        self.convert_entity(internal_structure, entity_manager, "credit_note", "CreditNote")
        entity_manager.commit_transaction("credit_note_transaction")  
    
    def convert_credit_contract(self, internal_structure, entity_manager):
        entity_manager.create_transaction("credit_contract_transaction")
        self.convert_entity(internal_structure, entity_manager, "credit_contract", "CreditContract")
        entity_manager.commit_transaction("credit_contract_transaction")

    def convert_credit_note_payment(self, internal_structure, entity_manager):
        entity_manager.create_transaction("credit_note_transaction")
        self.convert_entity(internal_structure, entity_manager, "credit_note", "CreditNote")
        entity_manager.commit_transaction("credit_note_transaction")
        
    # @todo: refactor this code
    def convert_credit_payment(self, internal_structure, entity_manager):
        # @todo: associate with CreditContract as credit_contract
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as system_company_employee
        entity_manager.create_transaction("credit_payment_transaction")
        self.convert_entity(internal_structure, entity_manager, "credit_payment", "CreditPayment")
        entity_manager.commit_transaction("credit_payment_transaction")
        
    # @todo: refactor this code    
    def convert_customer_return(self, internal_structure, entity_manager):
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as sellers
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as return_site
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as return_processor
        # @todo: associate with PaymentTerms
        # @todo: associate with CustomerCompany as company_buyer
        # @todo: associate with CustomerPerson as person_buyer
        # @todo: associate with SaleTransaction as original_sale
        entity_manager.create_transaction("customer_return_transaction")
        self.convert_entity(internal_structure, entity_manager, "customer_return", "CustomerReturn")
        entity_manager.commit_transaction("customer_return_transaction")

    def convert_gift_certificate(self, internal_structure, entity_manager):
        entity_manager.create_transaction("gift_certificate_transaction")
        self.convert_entity(internal_structure, entity_manager, "gift_certificate", "GiftCertificate")
        entity_manager.commit_transaction("gift_certificate_transaction")
    
    # @todo: refactor this code
    def convert_invoice(self, internal_structure, entity_manager):
        # @todo: associate with Purchase
        # @todo: associate with Sale
        entity_manager.create_transaction("invoice_transaction")
        self.convert_entity(internal_structure, entity_manager, "invoice", "Invoice")
        entity_manager.commit_transaction("invoice_transaction")
        
    # @todo: refactor this code
    def convert_merchandise_contactable_organizational_hierarchy_tree_node(self, internal_structure, entity_manager):
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode
        # @todo: associate with TransactionalMerchandise as merchandise_hierarchy_tree_node
        # @todo: set default values (Example: stock_on_hand = 0)
        entity_manager.create_transaction("merchandise_contactable_organizational_hierarchy_tree_node_transaction")
        self.convert_entity(internal_structure, entity_manager, "merchandise_contactable_organizational_hierarchy_tree_node", "MerchandiseContactableOrganizationalHierarchyTreeNode")
        entity_manager.commit_transaction("merchandise_contactable_organizational_hierarchy_tree_node_transaction")
        
    # @todo: refactor this code
    def convert_merchandise_hierarchy_tree_node_return(self, internal_structure, entity_manager):
        # @todo: associate with TransactionalMerchandise as merchandise
        # @todo: associate with Return as return
        # @todo: set default values
        entity_manager.create_transaction("merchandise_hierarchy_tree_node_return_transaction")
        self.convert_entity(internal_structure, entity_manager, "merchandise_hierarchy_tree_node_return", "MerchandiseHierarchyTreeNodeReturn")
        entity_manager.commit_transaction("merchandise_hierarchy_tree_node_return_transaction")
   
    def convert_money_sale(self, internal_structure, entity_manager):
        entity_manager.create_transaction("money_sale_transaction")
        self.convert_entity(internal_structure, entity_manager, "money_sale", "MoneySale")
        entity_manager.commit_transaction("money_sale_transaction")
    
    # @todo: refactor this code
    def convert_organizational_hierarchy_merchandise_supplier(self, internal_structure, entity_manager):
        # @todo: associate with TransactionalMerchandise as supplied_merchandise
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as supplier
        # @todo: associate with OrganizationalHierarchyTreeNode as supplied_organizational_hierarchy
        entity_manager.create_transaction("organizational_hierarchy_merchandise_supplier_transaction")
        self.convert_entity(internal_structure, entity_manager, "organizational_hierarchy_merchandise_supplier", "OrganizationalHierarchyMerchandiseSupplier")
        entity_manager.commit_transaction("organizational_hierarchy_merchandise_supplier_transaction")
        
    # @todo: refactor this code
    def convert_payment(self, internal_structure, entity_manager):
        # @todo: associate with CreditPayments as credit_payments
        # @todo: associate with Receipt as receipt
        # @todo: associate with Sale as sale
        # @todo: associate with Return as return
        # @todo: associate with Employee as payments_received_by
        # @todo: associate with CreditNote as credit_note
        entity_manager.create_transaction("payment_transaction")
        self.convert_entity(internal_structure, entity_manager, "payment", "Payment")
        entity_manager.commit_transaction("payment_transaction")

    # @todo: refactor this code
    def convert_payment_line(self, internal_structure, entity_manager):
        # @todo: associate with Payment as payment
        # @todo: associate with PaymentMethod as payment_method
        entity_manager.create_transaction("payment_line_transaction")
        self.convert_entity(internal_structure, entity_manager, "payment_line", "PaymentLine")
        entity_manager.commit_transaction("payment_line_transaction")

    def convert_payment_terms(self, internal_structure, entity_manager):
        entity_manager.create_transaction("payment_terms_transaction")
        self.convert_entity(internal_structure, entity_manager, "payment_terms", "PaymentTerms")
        entity_manager.commit_transaction("payment_terms_transaction")

    # @todo: refactor this code
    def convert_postdated_check_payment(self, internal_structure, entity_manager):
        entity_manager.create_transaction("postdated_check_payment_transaction")
        self.convert_entity(internal_structure, entity_manager, "postdated_check_payment", "PostdatedCheckPayment")
        entity_manager.commit_transaction("postdated_check_payment_transaction")
    
    # @todo: refactor this code
    def convert_purchase(self, internal_structure, entity_manager):
        # @todo: associate with Consignment
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as buyers
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as seller (use supplier relation)
        entity_manager.create_transaction("purchase_transaction")
        self.convert_entity(internal_structure, entity_manager, "purchase", "Purchase")
        entity_manager.commit_transaction("purchase_transaction")
    
    # @todo: refactor this code
    def convert_purchase_merchandise_hierarchy_tree_node(self, internal_structure, entity_manager):
        # @todo: associate with Purchase
        # @todo: associate with MerchandiseHierarchyTreeNode
        # @todo: set default values
        entity_manager.create_transaction("purchase_merchandise_hierarchy_tree_node_transaction")
        self.convert_entity(internal_structure, entity_manager, "purchase_merchandise_hierarchy_tree_node", "PurchaseMerchandiseHierarchyTreeNode")
        entity_manager.commit_transaction("purchase_merchandise_hierarchy_tree_node_transaction")
    
    # @todo: refactor this code
    def convert_receipt(self, internal_structure, entity_manager):
        # @todo: associate with Payment as payment
        entity_manager.create_transaction("receipt_transaction")
        self.convert_entity(internal_structure, entity_manager, "receipt", "Receipt")
        entity_manager.commit_transaction("receipt_transaction")
    
    # @todo: refactor this code
    def convert_sale_merchandise_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node(self, internal_structure, entity_manager):
        # @todo: associate with Sale
        # @todo: associate with TransactionalMerchandise as merchandise
        # @todo: set default values
        entity_manager.create_transaction("sale_merchandise_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node_transaction")
        entity_manager.commit_transaction("sale_merchandise_hierarchy_tree_node_contactable_organizational_hierarchy_tree_node_transaction")
    
    # @todo: refactor this code
    def convert_sale_transaction(self, internal_structure, entity_manager):
        # @todo: associate with CustomerCompany as company_buyer
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as seller_stockholder
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as sellers
        # @todo: associate with CustomerPerson as person_buyer
        # @todo: associate with PaymentTerms as person_buyer
        entity_manager.create_transaction("sale_transaction_transaction")
        self.convert_entity(internal_structure, entity_manager, "sale_transaction", "SaleTransaction")
        entity_manager.commit_transaction("sale_transaction_transaction")
    
    # @todo: refactor this code
    def convert_shipment(self, internal_structure, entity_manager):
        # @todo: associate with Sale
        # @todo: set sender as SystemCompany
        # @todo: set receiver as sale.customer
        entity_manager.create_transaction("shipment_transaction")
        self.convert_entity(internal_structure, entity_manager, "shipment", "Shipment")
        entity_manager.commit_transaction("shipment_transaction")
    
    # @todo: refactor this code
    def convert_stock_adjustment(self, internal_structure, entity_manager):
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as adjustment_owners
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as adjustment_target
        # @todo: associate with Reason as stock_adjustment_reason
        entity_manager.create_transaction("stock_adjustment_transaction")
        self.convert_entity(internal_structure, entity_manager, "stock_adjustment", "StockAdjustment")
        entity_manager.commit_transaction("stock_adjustment_transaction")
    
    # @todo: refactor this code
    def convert_stock_adjustment_merchandise_hierarchy_tree_node(self, internal_structure, entity_manager):
        # @todo: associate with TransactionalMerchandise as merchandise
        # @todo: associate with StockAdjustment
        entity_manager.create_transaction("stock_adjustment_merchandise_hierarchy_tree_node_transaction")
        self.convert_entity(internal_structure, entity_manager, "stock_adjustment_merchandise_hierarchy_tree_node", "StockAdjustmentMerchandiseHierarchyTreeNode")
        entity_manager.commit_transaction("stock_adjustment_merchandise_hierarchy_tree_node_transaction")

    # @todo: refactor this code
    def convert_supplier_return(self, internal_structure, entity_manager):
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as return_requester
        # @todo: associate with Purchase as original_purchase
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as supplier
        entity_manager.create_transaction("supplier_return_transaction")
        self.convert_entity(internal_structure, entity_manager, "supplier_return", "SupplierReturn")
        entity_manager.commit_transaction("supplier_return_transaction")

    # @todo: refactor this code
    def convert_transfer(self, internal_structure, entity_manager):
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as sender
        # @todo: associate with ContactableOrganizationalHierarchyTreeNode as receiver
        entity_manager.create_transaction("transfer_transaction")
        self.convert_entity(internal_structure, entity_manager, "transfer", "Transfer")
        entity_manager.commit_transaction("transfer_transaction")
    
    # @todo: refactor this code
    def convert_transfer_merchandise_hierarchy_tree_node(self, internal_structure, entity_manager):
        # @todo: associate with TransactionalMerchanduse as merchandise
        # @todo: associate with Transfer as transfer
        entity_manager.create_transaction("transfer_merchandise_hierarchy_tree_node_transaction")
        self.convert_entity(internal_structure, entity_manager, "transfer_merchandise_hierarchy_tree_node", "TransferMerchandiseHierarchyTreeNode")
        entity_manager.commit_transaction("transfer_merchandise_hierarchy_tree_node_transaction")
    
    def convert_entity(self, internal_structure, entity_manager, internal_structure_entity_name, entity_name, default_values_map = {}, handlers = []):
        entity_class = entity_manager.get_entity_class(entity_name)
        
        # convert the internal entities
        internal_entities = internal_structure.get_entities(internal_structure_entity_name)
        for internal_entity in internal_entities:
            # @todo: make sure the entity doesnt exist yet
            entities = entity_manager.find_all(entity_class, internal_entity.object_id, "object_id")
            if len(entities) == 0:
                entity = entity_class()
                fields = internal_entity.get_fields()
                valid_fields = [(field_name, field_value) for field_name, field_value in fields.items() if not field_value is None and not type(field_value) in (types.InstanceType, types.ListType)]
                
                # copy the values of the internal entity to the entity
                for field_name, field_value in valid_fields:
                     if field_name in default_values_map:
                        default_value = default_values_map[field_name]
                        if type(default_value) == types.FunctionType:
                            field_value = default_value(field_value)
                        del default_values_map[field_name] 
                     setattr(entity, field_name, field_value)
           
                # apply all remaining values default values
                for field_name, field_value in default_values_map.items():
                    if not type(field_value) == types.FunctionType:
                        if type(field_value) == types.StringType:
                            field_value = unicode(field_value)
                        setattr(internal_entity, field_name, field_value)
                
                entity.object_id = internal_entity.object_id
                
                for handler in handlers:
                    handler(self, internal_structure, entity_manager, internal_structure_entity_name, entity_name, internal_entity, entity)

                print "Saving " + entity_name + " with object id = " + str(entity.object_id)
                entity_manager.save(entity)
    
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
    """ Source medium domain_entity domain entity """
    
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
