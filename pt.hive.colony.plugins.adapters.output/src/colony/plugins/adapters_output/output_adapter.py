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

__revision__ = "$LastChangedRevision: 2100 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:24:05 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import model_domain
import time
import sqlalchemy.ext.declarative

import adapters_output.configuration.output_configuration_parser
import adapters_output.model_domain

def extend_dictionary(first_map, second_map):
    """
    Returns a dictionary that contains data from both of the provided ones

    @param first_map Dictionary where to retrieve data from 
    @param second_map Dictionary where to retrieve data from
    @return New dictionary with the entries from the provided dictionaries
    """
    new_map = {}
    for key in first_map:
        new_map[key] = first_map[key]
    for key in second_map:
        new_map[key] = second_map[key]
    return new_map

class OutputAdapter:

    ONE_TO_ONE = "one-to-one"
    ONE_TO_MANY = "one-to-many"
    MANY_TO_MANY = "many-to-many"

    internal_domain_instance_map = {}
    """ Dictionary relating an internal entity instance with a domain entity instance """
    
    domain = None
    """ Reference to the domain controller """
    
    parent_plugin = None
    """ Reference to the plugin that owns this code """
    
    output_configuration = None
    """ Reference to the input configuration properties (extracted from the configuration file) """
    
    logger = None
    """ Reference to the logging instance """

    def __init__(self, parent_plugin):
        """
        Class constructor
        
        @param parent_plugin: Reference to the plugin that owns this code
        """
        self.parent_plugin = parent_plugin
        self.reset_state()
    
    def reset_state(self):
        """
        Resets the structures back to their original state (necessary when performing another conversion)
        """
        self.internal_domain_instance_map = {}
        self.output_configuration = None
        self.load_configuration()
        if self.parent_plugin.sqlalchemy_plugin:
            self.parent_plugin.sqlalchemy_plugin.create_engine("mysql", "hive", "hive", "hivetest")
            engine = self.parent_plugin.sqlalchemy_plugin.get_engine()
            base = sqlalchemy.ext.declarative.declarative_base(engine)
            self.domain = model_domain.Domain(base)
            self.domain.define_classes(self.output_configuration.get_domain_entity_list())
        
    def load_configuration(self):
        """
        Loads from the XML configuration file into the correspondent data structures
        """
        parser = adapters_output.configuration.output_configuration_parser.OutputConfigurationParser()
        if self.parent_plugin.configuration_plugin:
            file_paths = self.parent_plugin.configuration_plugin.get_configuration_file_paths()
            for file_path in file_paths:
                parser.file_path = file_path
                parser.parse()
            self.output_configuration = parser.output_configuration
            self.parent_plugin.generate_event("output_configuration_changed", [self.output_configuration])
        
    def process_handler(self, handler_name, arguments):
        """
        Invokes a given handler function with the provided name and supplying the provided arguments
        
        @param handler_name:Name of the handler function to invoke
        @param arguments: List of arguments that will be supplied to the handler function
        @return: The value returned by the handler
        """
        configuration_plugin = self.parent_plugin.configuration_plugin
        if configuration_plugin.has_handler(handler_name):
            handler = configuration_plugin.get_handler(handler_name)
            return handler(arguments)
    
    def process_convert(self, task, args):
        """
        Executes the entire conversion algorithm
        
        @param task: Task monitoring object used to inform the status of the query
        @param args: Dictionary with configuration keys provided by the caller 
        """
        self.reset_state()
        self.logger = self.parent_plugin.logger_plugin.get_logger("main")
        
        self.logger.get_logger().warn("Generic output adapter has started the conversion process.\n")
        internal_structure = args["internal_structure"]
        work_units = args["work_units"]
        self.process_work_units(task, 50, 30, work_units, internal_structure)
        self.persist_domain(task, 80, 85)
        self.process_relations(task, 85, 10, work_units, internal_structure)
        self.persist_domain(task, 95, 5)

    def process_work_units(self, task, counter_offset, counter_range, list_work_units, internal_structure):
        """
        Processes the given work units using the provided internal structure
        
        @param task: Task monitoring object used to inform the status of the query
        @param counter_offset: Where the progress counter should start at for this operation
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)        
        @param list_work_units List with the names of the work units that must be processed
        @param internal_structure InternalStructure object for the work units to act from
        """
        counter = counter_offset
        counter_inc = counter_range / len(list_work_units)
        for work_unit in list_work_units:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_work_unit(task, counter, counter_inc, work_unit, internal_structure)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()
                    
                counter += counter_inc
                task.set_percentage_complete(counter)
            else:
                break
        
    def process_work_unit(self, task, counter_offset, counter_range, work_unit, internal_structure):
        """
        Processes a given work unit using the provided internal structure
        
        @param task: Task monitoring object used to inform the status of the query
        @param counter_offset: Where the progress counter should start at for this operation
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)        
        @param work_unit Name of the work unit that must be processed
        @param internal_structure InternalStructure object for the work unit to act from
        """
        list_entity_names = self.parent_plugin.configuration_plugin.get_entity_name_list(work_unit) 
        
        self.logger.get_logger().warn("Output adapter: Processing work unit '%s'.\n" % work_unit)
        
        counter = counter_offset
        counter_inc = counter_range / len(list_entity_names)
        for entity_name in list_entity_names:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_entity(entity_name, internal_structure)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()
                
                counter += counter_inc
                task.set_percentage_complete(counter)
            else:
                break

    def process_entity(self, domain_entity_name, internal_structure):
        """
        Fills a given domain entity with data from the provided internal structure
        
        @param domain_entity_name Name of the domain entity to be processed
        @param internal_structure InternalStructure object where to draw data from
        """        
        configuration = self.output_configuration
        internal_entity_name = configuration.get_internal_entity_name(domain_entity_name)
        internal_entity_instance_list = internal_structure.get_entity_instance_list(internal_entity_name)
        domain_entity_class = self.domain.get_class(domain_entity_name)
        
        self.logger.get_logger().warn("Output adapter: Processing internal entity '%s'.\n" % internal_entity_name)
        
        # process each internal entity instance
        for internal_entity_instance in internal_entity_instance_list:
            self.process_domain_entity_handlers(domain_entity_name, internal_entity_instance)
            self.process_domain_entity_instance(domain_entity_name, internal_entity_instance)
            
    def process_domain_entity_handlers(self, domain_entity_name, internal_entity_instance):
        """
        Processes the handlers assigned to this domain entity
        
        @param domain_entity_name: Name of the domain entity to process
        @param internal_entity_instance: Correspondent internal entity instance
        """
        configuration = self.output_configuration
        
        if not internal_entity_instance in self.internal_domain_instance_map:
            domain_entity_class = self.domain.get_class(domain_entity_name)
            domain_entity_instance = domain_entity_class()
            self.internal_domain_instance_map[internal_entity_instance] = domain_entity_instance
        else:
            domain_entity_instance = self.internal_domain_instance_map[internal_entity_instance]
        
        handler_list = configuration.get_domain_entity_handler_list(domain_entity_name)
        for handler in handler_list:
            self.domain.add_domain_entity_instance(domain_entity_name, self.process_handler(handler.module, handler.name, [domain_entity_instance, internal_entity_instance]))

    def process_domain_entity_instance(self, domain_entity_name, internal_entity_instance):
        """
        Processes a specific domain entity instance, taking into account only non-relation fields
        
        @param domain_entity_name: Name of the domain entity to process
        @param internal_entity_instance: Correspondent internal entity instance
        """
        configuration = self.output_configuration

        if not internal_entity_instance in self.internal_domain_instance_map:
            domain_entity_class = self.domain.get_class(domain_entity_name)
            domain_entity_instance = domain_entity_class()
            self.internal_domain_instance_map[internal_entity_instance] = domain_entity_instance
        else:
            domain_entity_instance = self.internal_domain_instance_map[internal_entity_instance]
        domain_attribute_name_list = configuration.get_domain_attribute_name_list(domain_entity_name)

        # for each domain attribute in the specified domain entity
        for domain_attribute_name in domain_attribute_name_list:
            # process only when it's not a relation
            if not configuration.is_domain_relation_attribute(domain_entity_name, domain_attribute_name): 
                internal_attribute_name = configuration.get_internal_attribute_name(domain_entity_name, domain_attribute_name)
                if internal_attribute_name:
                    handler_list = configuration.get_domain_attribute_handler_list(domain_entity_name, domain_attribute_name)
                    value = internal_entity_instance.get_field_value(internal_attribute_name)
                    for handler in handler_list:
                        value = self.process_handler(handler.name, [value, internal_entity_instance])
                    setattr(domain_entity_instance, domain_attribute_name, value)    
        self.domain.add_domain_entity_instance(domain_entity_name, domain_entity_instance)
            
    def process_relations(self, task, counter_offset, counter_range, list_work_units, internal_structure):
        """
        Processes all the relations for the all the work units
        
        @param task: Task monitoring object used to inform the status of the query
        @param counter_offset: Where the progress counter should start at for this operation
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)        
        @param list_work_units: List with the names of the work units to be processed
        @param internal_structure: Internal structure where to take data from
        """
        counter = counter_offset
        counter_inc = counter_range / len(list_work_units)
        for work_unit in list_work_units:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_relations_work_unit(task, counter, counter_inc, work_unit, internal_structure)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()
                
                counter += counter_inc
                task.set_percentage_complete(counter)
            else:
                break

    def process_relations_work_unit(self, task, counter_offset, counter_range, work_unit, internal_structure):
        """
        Processes all the relations for a given work unit
        
        @param task: Task monitoring object used to inform the status of the query
        @param counter_offset: Where the progress counter should start at for this operation
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)                
        @param work_unit: Name of the specific work unit to be processed
        @param internal_structure: Internal structure where to take data from
        """
        list_entity_names = self.parent_plugin.configuration_plugin.get_entity_name_list(work_unit)
        
        counter = counter_offset
        counter_inc = counter_range / len(list_entity_names)
        for entity_name in list_entity_names:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_relations_entity(entity_name, internal_structure)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()
                
                counter += counter_inc
                task.set_percentage_complete(counter)
            else:
                break 

    def process_relations_entity(self, domain_entity_name, internal_structure):
        """
        Processes all the relations for a given domain entity
        
        @param domain_entity_name: Name of the domain entity whose relation attributes will be processed
        @param internal_structure: Internal structure where to take the data from
        """      
        configuration = self.output_configuration
        domain_relation_attribute_name_list = configuration.get_domain_relation_attribute_name_list(domain_entity_name)
        internal_entity_name = configuration.get_internal_entity_name(domain_entity_name)
        internal_entity_instance_list = internal_structure.get_entity_instance_list(internal_entity_name)
        
        # for each domain attribute that references an entity
        for domain_relation_attribute_name in domain_relation_attribute_name_list:
            if not domain_relation_attribute_name == "id":
                referenced_domain_entity_name = configuration.get_referenced_domain_entity_name(domain_entity_name, domain_relation_attribute_name)
                relation_multiplicity = configuration.get_reference_multiplicity(domain_entity_name, domain_relation_attribute_name)
                relation_internal_attribute_name = configuration.get_internal_attribute_name(domain_entity_name, domain_relation_attribute_name)
                # for each correspondent internal entity instance
                for internal_entity_instance in internal_entity_instance_list:
                    domain_entity_instance = self.internal_domain_instance_map[internal_entity_instance]
                    referenced_internal_entity_instance = internal_entity_instance.get_field_value(relation_internal_attribute_name)
                    # the relation may be optional, in case of null, don't process
                    if referenced_internal_entity_instance:
                        referenced_domain_entity_instance = self.internal_domain_instance_map[referenced_internal_entity_instance]
                        if relation_multiplicity == self.ONE_TO_ONE:    
                            setattr(domain_entity_instance, domain_relation_attribute_name, referenced_domain_entity_instance)
                        elif relation_multiplicity == self.ONE_TO_MANY:
                            domain_relations_list = getattr(domain_entity_instance, domain_relation_attribute_name)
                            domain_relations_list.append(referenced_domain_entity_instance)
                            setattr(domain_entity_instance, entity_relation_attribute, domain_relations_list)                   

    def persist_domain(self, task, counter_offset, counter_range):
        """
        Saves all the changes to the domain entity objects in the database
        
        @param task: Task monitoring object used to inform the status of the query
        @param counter_offset: Where the progress counter should start at for this operation
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)         
        """
        sql_alchemy_plugin = self.parent_plugin.sqlalchemy_plugin
        for list in self.domain.lists:
            for entity in list:
                sql_alchemy_plugin.save_or_update(entity)
        sql_alchemy_plugin.flush()
        
        task.set_percentage_complete(counter_offset + counter_range)