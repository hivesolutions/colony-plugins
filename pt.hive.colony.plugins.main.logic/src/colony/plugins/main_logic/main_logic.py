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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

#@todo: review and comment this file
def get_valid_attributes(object):
    attributes = dir(object)
    for exclusion_element in object.exclusion_list:
        if exclusion_element in attributes:
            attributes.remove(exclusion_element)
    return attributes

#@todo: there has to be a way to get all the methods without using an exception list
#@todo: review and comment this class
class InternalStructure:
    exclusion_list = ["exclusion_list", "__doc__", "__module__", "has_entity_list", "has_entity", "has_field", "add_entity", "add_field", 
                      "set_field_value", "get_entity", "display_structure", "print_structure", "set_visualizer", "get_entity_instance_list", "visualizer_plugin", "CONTACT_INFORMATION_ENTITY", "CUSTOMER_ENTITY", "ADDRESS_ENTITY", "USER_ENTITY"]
    
    CONTACT_INFORMATION_ENTITY = "contact_information"
    CUSTOMER_ENTITY = "customer"
    ADDRESS_ENTITY = "address"
    USER_ENTITY = "user"
    
    def set_visualizer(self, visualizer):
        self.visualizer_plugin = visualizer
        
    def get_entity_instance_list(self, internal_entity_name):
        return getattr(self, internal_entity_name)
    
    def has_entity_list(self, entity_name):
        return hasattr(self, entity_name)

    def has_entity(self, entity_name, entity_id):
        if self.has_entity_list(entity_name):
            entity_list = getattr(self, entity_name)
            if entity_id < len(entity_list):
                return True
        return False
    
    def has_field(self, entity_name, entity_id, field_name):
        if self.has_entity(entity_name, entity_id):
            entity = self.get_entity(entity_name, entity_id)
            return entity.has_field(field_name)
        return False

    def add_entity(self, entity_name):
        if not self.has_entity_list(entity_name):
            setattr(self, entity_name, [])
        entity_list = getattr(self, entity_name)
        entity_list.append(EntityStructure())
        return len(entity_list) - 1

    def add_field(self, entity_name, entity_id, field_name):
        if self.has_entity(entity_name, entity_id):
            entity = self.get_entity(entity_name, entity_id)
            entity.add_field(field_name)

    def set_field_value(self, entity_name, entity_id, field_name, value):
        if not self.has_field(entity_name, entity_id, field_name):
            self.add_field(entity_name, entity_id, field_name)
        entity = self.get_entity(entity_name, entity_id)
        entity.set_field_value(field_name, value)

    def get_entity(self, entity_name, entity_id):
        if self.has_entity(entity_name, entity_id):
            entity_list = getattr(self, entity_name)
            entity = entity_list[entity_id]
            return entity
       
#@todo: there has to be a way to get all the methods without using an exception list                    
class EntityStructure:
    exclusion_list = ["exclusion_list", "__doc__", "__module__", "has_field", "add_field", "set_field_value", "get_field_value", "print_structure"]
    
    def has_field(self, field_name):
        return hasattr(self, field_name)
    
    def add_field(self, field_name):
        if not self.has_field(field_name):
            setattr(self, field_name, None)
        
    def set_field_value(self, field_name, value):
        if not self.has_field(field_name):
            self.add_field(field_name)
        setattr(self, field_name, value)
        
    def get_field_value(self, field_name):
        if self.has_field(field_name):
            return getattr(self, field_name)

class MainLogic:
    #@todo: process query
    main_logic_plugin = None
    internal_structure = None
    task = None
    
    def __init__(self, main_logic_plugin):
        self.main_logic_plugin = main_logic_plugin
        self.internal_structure = InternalStructure()
        
    def process_query(self, args):
        self.task = self.main_logic_plugin.task_manager_plugin.create_new_task("Database Conversion", "Diamante 20003 conversion", self.process_query_handler)
        self.task.set_task_pause_handler(self.pause_process_query_handler)
        self.task.set_task_resume_handler(self.resume_process_query_handler)
        self.task.set_task_stop_handler(self.stop_process_query_handler)
        self.task.start(args)

    def process_query_handler(self, task, args):
        input_adapter_plugin_id = args["input_adapter_plugin_id"]
        output_adapter_plugin_id = args["output_adapter_plugin_id"]
        query_type = args["query_type"]

        self.main_logic_plugin.generate_event("task_information_changed", [])

        for input_adapter in self.main_logic_plugin.input_adapters:
            if input_adapter.id == input_adapter_plugin_id:
                input_adapter_plugin = input_adapter
                break

        for output_adapter in self.main_logic_plugin.output_adapters:
            if output_adapter.id == output_adapter_plugin_id:
                output_adapter_plugin = output_adapter
                break

        if query_type == "convert":
            args["internal_structure"] = self.internal_structure
        #elif query_type == "info_table":

        input_adapter_plugin.process_query(task, args)
        output_adapter_plugin.process_query(task, args)
        # confirms the stop
        task.confirm_stop(True)   

    def pause_process_query_handler(self, args):
        pass

    def resume_process_query_handler(self, args):
        pass

    def stop_process_query_handler(self, args):
        pass