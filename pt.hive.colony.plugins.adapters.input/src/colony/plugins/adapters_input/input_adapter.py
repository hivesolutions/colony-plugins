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

import copy
import time

import adapters_input.configuration.input_configuration_parser

class InputAdapter:
    """
    Generic input adapter
    """

    PRIMARY_KEY_ID = "id"
    """ Name of the column used to store primary keys """

    internal_entity_name_primary_key_entity_id_map = {}
    """ Dictionary relating internal entity name, with primary key value, with internal entity id """

    foreign_key_queue = None
    """ List of foreign keys that haven't been processed yet """

    input_configuration = None
    """ Reference to the input configuration properties (extracted from the configuration file) """

    parent_plugin = None
    """ Reference to the plugin that owns this code """

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

        self.internal_entity_name_primary_key_entity_id_map = {}
        self.foreign_key_queue = ForeignKeyQueue()
        self.input_configuration = None
        self.load_configuration()

    def load_configuration(self):
        """
        Loads from the XML configuration file into the correspondent data structures
        """

        parser = adapters_input.configuration.input_configuration_parser.InputConfigurationParser()
        if self.parent_plugin.configuration_plugin:
            file_paths = self.parent_plugin.configuration_plugin.get_configuration_file_paths()
            for file_path in file_paths:
                parser.file_path = file_path
                parser.parse()
            self.input_configuration = parser.input_configuration
            self.parent_plugin.generate_event("input_configuration_changed", [self.input_configuration])

    def process_query(self, task, args):
        """
        Processes an operation on the input database
        
        @param task: Task monitoring object used to inform the status of the query
        @param args: Dictionary with the configuration paramaters necessary to perform the requested operation
        """

        self.reset_state()
        self.logger = self.parent_plugin.logger_plugin.get_logger("main")

        query_type = args["query_type"]
        if query_type == "convert":
            diamante_path = args["diamante_path"]
            work_units = args["work_units"]
            internal_structure = args["internal_structure"]
            self.process_convert(task, diamante_path, work_units, internal_structure)
        self.parent_plugin.generate_event("internal_structure_changed", [internal_structure])
        return internal_structure

    def process_convert(self, task, diamante_path, work_unit_list, internal_structure):
        """
        Performs a database conversion operation
        
        @param task: Task monitoring object used to inform the status of the query
        @param diamante_path: Path to the Diamante application
        @param work_unit_list: List of work units that need to be performed for the conversion operation to complete
        @param internal_structure: Intermediate structure to where the data will be copied to
        """

        self.logger.get_logger().warn("Generic input adapter has started the conversion process.\n")
        self.parent_plugin.foxpro_plugin.initialize(diamante_path)
        self.process_work_units(task, work_unit_list, internal_structure)

    def process_work_units(self, task, list_work_units, internal_structure):
        """
        Performs the operations necessary to complete each of the specified work units
        
        @param task: Task monitoring object used to inform the status of the query
        @param list_work_units: List of work units to complete
        @param internal_structure: Intermediate structure to where the data will be copied to
        """

        # where the counter should start at for this operation
        COUNTER_OFFSET = 0
        # what range does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)
        COUNTER_RANGE = 50

        counter = COUNTER_OFFSET
        list_work_units = self.parent_plugin.configuration_plugin.get_work_unit_list()
        counter_inc = COUNTER_RANGE / len(list_work_units)
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

    def process_work_unit(self, task, counter_offset, counter_range, work_unit_name, internal_structure):
        """
        Processes the tables indicated by the specified work unit
        
        @param task: Task monitoring object used to inform the status of the query
        @param counter_offset: Where the progress counter should start at for this operation
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)
        @param work_unit_name: Name of the work unit whose work will be performed
        @param internal_structure: Intermediate structure to where the data will be copied to
        """

        self.logger.get_logger().warn("Input adapter: Processing work unit '%s'.\n" % work_unit_name)

        counter = counter_offset
        list_table_names = self.parent_plugin.configuration_plugin.get_table_list(work_unit_name)
        counter_inc = counter_range / len(list_table_names)
        for table_name in list_table_names:
            if not task.status == task.STATUS_TASK_STOPPED:
                table_conversion_info = TableConversionInfo(table_name, internal_structure, self.parent_plugin.foxpro_plugin, self.input_configuration)
                self.process_table(table_conversion_info)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()

                counter += counter_inc
                task.set_percentage_complete(counter)

    def process_handler(self, handler_name, arguments):
        """
        Invokes a given handler function with the provided name and supplying the provided arguments
        
        @param handler_name: Name of the handler function to invoke
        @param arguments: List of arguments that will be supplied to the handler function
        @return: The value returned by the handler
        """

        self.logger.get_logger().debug("Input adapter: Processing handler function '%s'.\n" % handler_name)
        
        configuration_plugin = self.parent_plugin.configuration_plugin
        if configuration_plugin.has_handler(handler_name):
            handler = configuration_plugin.get_handler(handler_name)
            return handler(arguments)
        
    def process_table(self, table_conversion_info):
        """
        Copies the table's contents to the internal structure
        
        @param table_conversion_info: TableConversionInfo object containing information about the conversion process
        """

        self.logger.get_logger().warn("Input adapter: Processing table '%s'.\n" % table_conversion_info.table_name)

        table_internal_entity_name = table_conversion_info.table_internal_entity_name
        query_results = table_conversion_info.query_results
        internal_structure = table_conversion_info.internal_structure

        for result in query_results:
            table_internal_entity_id = internal_structure.add_entity(table_internal_entity_name)
            self.process_table_handlers(table_conversion_info, result, table_internal_entity_id)
            self.process_primary_key(table_conversion_info, result, table_internal_entity_id)
            self.process_foreign_key_queue(table_conversion_info, result, table_internal_entity_id)
            self.process_columns(table_conversion_info, result, table_internal_entity_id)

    def process_table_handlers(self, table_conversion_info, result, table_internal_entity_id):
        """
        Invokes the functions associated with the specified table
        
        @param table_conversion_info: TableConversionInfo object containing information about the conversion process
        @param result: Row from the database query that's being processed at this time
        @param table_internal_entity_id: Identification of the internal entity instance bound to this database row
        """

        self.logger.get_logger().debug("Input adapter: Processing table handlers for table '%s'.\n" % table_conversion_info.table_name)

        configuration = self.input_configuration
        handler_list = configuration.get_table_handler_list(table_conversion_info.table_name)
        for handler in handler_list:
            self.process_handler(handler.name, [table_conversion_info, result, table_internal_entity_id])

    def process_columns(self, table_conversion_info, result, table_internal_entity_id):
        """
        Copies data from the database columns to the internal structure entity attributes
        
        @param table_conversion_info: TableConversionInfo object containing information about the conversion process
        @param result: Row from the database query that's being processed at this time
        @param table_internal_entity_id: Identification of the internal entity instance bound to this database row
        """

        configuration = self.input_configuration
        table_name = table_conversion_info.table_name
        internal_structure = table_conversion_info.internal_structure
        table_internal_entity_name = table_conversion_info.table_internal_entity_name
        table_internal_entity = internal_structure.get_entity(table_internal_entity_name, table_internal_entity_id)

        # check if there is any non null value in this result set
        valid_result_set = False
        for column_name in result:
            if not result[column_name] == None:
                valid_result_set = True
                break

        # only perform conversion if there's any value to convert
        if valid_result_set:
            # for each column in the query result
            for column_name in result:
                # if there is data in the result and this column is processable
                if result[column_name] and configuration.is_processable_column(table_name, column_name):

                    self.logger.get_logger().debug("Input adapter: Processing column '%s'.\n" % column_name)

                    internal_attribute_name = configuration.get_internal_attribute_name(table_name, column_name)
                    internal_entity_name = configuration.get_internal_attribute_entity_name(table_name, column_name)

                    if internal_entity_name == table_internal_entity_name:
                        internal_entity_id = table_internal_entity_id
                    else:
                        internal_entity_xml_id = configuration.get_internal_attribute_entity_id(table_name, column_name)
                        internal_entity_id = table_conversion_info.get_internal_entity_id(internal_entity_name, internal_entity_xml_id)

                    value = result[column_name]

                    # if the column is not a table reference, then run the column handlers, and save the resulting value
                    if not configuration.is_table_reference(table_name, column_name):
                        handler_list = configuration.get_column_handler_list(table_name, column_name)
                        for handler in handler_list:
                            value = self.process_handler(handler.name, [value])
                        internal_structure.set_field_value(internal_entity_name, internal_entity_id, internal_attribute_name, value)
                    else: # if this column is a table reference
                        foreign_table_name = configuration.get_referenced_table_name(table_name, column_name)
                        foreign_internal_entity_name = configuration.get_internal_entity_name(foreign_table_name)
                        foreign_key_value = result[column_name]

                        # if the foreign table has already been processed then save the reference
                        if internal_structure.has_entity_list(foreign_internal_entity_name):
                            foreign_internal_entity_id = self.get_primary_key_entity_id(foreign_internal_entity_name, foreign_key_value)
                            if foreign_internal_entity_id:
                                foreign_internal_entity_instance = internal_structure.get_entity(foreign_internal_entity_name, foreign_internal_entity_id)
                                internal_structure.set_field_value(table_internal_entity_name, table_internal_entity_id, foreign_internal_entity_name, foreign_internal_entity_instance)
                        else: # if the foreign table hasn't been processed yet, then add this operation to the queue
                            foreign_key_element = ForeignKeyQueueElement(internal_entity_name, internal_entity_id, foreign_key_value, foreign_table_name)
                            self.foreign_key_queue.add_queue_element(foreign_key_element)

            # set backwards relations in branched internal entities
            for key in table_conversion_info.internal_entity_xmlid_internalid_map:
                internal_entity_name = key[0]
                internal_entity_id = table_conversion_info.internal_entity_xmlid_internalid_map[key]
                internal_structure.set_field_value(internal_entity_name, internal_entity_id, table_internal_entity_name, table_internal_entity)
            table_conversion_info.internal_entity_xmlid_internalid_map = {}

    def process_primary_key(self, table_conversion_info, result, table_internal_entity_id):
        """
        Extracts the primary key value from the query result set and into the the internal structure. After this
        operation the result set will not contain the primary key column anymore.
        
        @param table_conversion_info: TableConversionInfo object containing information about the conversion process
        @param result: Row from the database query that's being processed at this time
        @param table_internal_entity_id: Identification of the internal entity instance bound to this database row
        """

        primary_key_column_name = table_conversion_info.primary_key_column_name
        internal_structure = table_conversion_info.internal_structure
        primary_key_column_value = result[primary_key_column_name]
        table_internal_entity_name = table_conversion_info.table_internal_entity_name

        internal_structure.set_field_value(table_internal_entity_name, table_internal_entity_id, self.PRIMARY_KEY_ID, primary_key_column_value)
        self.add_primary_key_entity_id(table_internal_entity_name, table_internal_entity_id, primary_key_column_value)

    def process_foreign_key_queue(self, table_conversion_info, result, table_internal_entity_id):
        """
        Process the foreign key queue
        
        @param table_conversion_info: TableConversionInfo object containing information about the conversion process
        @param result: Row from the database query that's being processed at this time
        @param table_internal_entity_id: Identification of the internal entity instance bound to this database row
        """

        table_internal_entity_name = table_conversion_info.table_internal_entity_name
        table_name = table_conversion_info.table_name
        primary_key_column_name = table_conversion_info.primary_key_column_name
        primary_key_column_value = result[primary_key_column_name]
        queue = self.foreign_key_queue.get_foreign_key_queue(table_name, primary_key_column_value)
        internal_structure = table_conversion_info.internal_structure

        for element in queue:
            internal_entity = internal_structure.get_entity(table_internal_entity_name, table_internal_entity_id)
            element_entity_name = element.internal_entity_name
            element_entity_id = element.internal_entity_id
            internal_structure.set_field_value(element_entity_name, element_entity_id, table_internal_entity_name, internal_entity) 

    def get_primary_key_entity_id(self, foreign_entity_name, foreign_key_value):
        """
        Retrieves the internal entity identifier that corresponds to the provided primary key value
        
        @param foreign_entity_name: Name of the internal entity from which one wants to get an identifier
        @param foreign_key_value: Value of associated primary key
        @return: Identification number of a internal entity instance
        """

        if foreign_entity_name in self.internal_entity_name_primary_key_entity_id_map and foreign_key_value in self.internal_entity_name_primary_key_entity_id_map[foreign_entity_name]:
            return self.internal_entity_name_primary_key_entity_id_map[foreign_entity_name][foreign_key_value]
    
    def add_primary_key_entity_id(self, internal_entity_name, internal_entity_id, primary_key_value):
        """
        Stores an association between a primary key value and an internal entity id
        
        @param internal_entity_name: Name of the internal entity to which the id belongs
        @param internal_entity_id: Identification of the internal entity instance
        @param primary_key_value: Value of the primary key
        """

        if not internal_entity_name in self.internal_entity_name_primary_key_entity_id_map:
            self.internal_entity_name_primary_key_entity_id_map[internal_entity_name] = {}
        self.internal_entity_name_primary_key_entity_id_map[internal_entity_name][primary_key_value] = internal_entity_id

class TableConversionInfo:
    """
    Holds information about the conversion of a certain database table. Useful for passing around different functions
    that share a requirement for these informations.
    """

    table_name = None
    """ Name of the database table that is being converted """

    column_name_list = None
    """ List with the names of this table's columns """

    primary_key_column_name = None
    """ Name of this table's primary key column """

    foreign_key_column_name_list = None
    """ List with the names of this table's foreign key columns """

    table_internal_entity_name = None
    """ Name of the internal entity to which the table is supposed to be converted to by default """    

    internal_structure = None
    """ Internal structure to which the database will be converted to """

    #@todo: this does not belong to this structure
    internal_entity_xmlid_internalid_map = None
    """ Relation between internal entity id in the internal structure and the xml file """

    query_results = None
    """ Results of the query performed on this database table """

    def __init__(self, table_name, internal_structure, foxpro_plugin, configuration):
        """
        Class constructor
        
        @param table_name: Name of the table that is going to be converted
        @param internal_structure: Intermediate structure where the data will be converted to
        @param foxpro_plugin: Reference to the plugin that provides access to the foxpro database
        @param configuration: Input configuration structure
        """

        self.table_name = table_name
        self.internal_structure = internal_structure
        self.table_internal_entity_name = configuration.get_internal_entity_name(table_name)
        self.internal_entity_xmlid_internalid_map = {}
        self.primary_key_column_name = configuration.get_primary_key_column_name(table_name)
        self.foreign_key_column_name_list = configuration.get_foreign_key_column_name_list(table_name)
        self.column_name_list = configuration.get_column_name_list(table_name)
        self.query_results = foxpro_plugin.query(table_name, self.column_name_list)

    def get_internal_entity_id(self, internal_entity_name, internal_entity_xmlid):
        """
        Retrieves the equivalent internal entity id in the internal structure for the provided
        internal entity id in the configuration file
        
        @param internal_entity_name: Name of the internal entity
        @param internal_entity_xmlid: Identification number of the internal entity in the configuration file
        """

        if not (internal_entity_name, internal_entity_xmlid) in self.internal_entity_xmlid_internalid_map:
            internal_entity_id = self.internal_structure.add_entity(internal_entity_name)
            self.internal_entity_xmlid_internalid_map[(internal_entity_name, internal_entity_xmlid)] = internal_entity_id
        return self.internal_entity_xmlid_internalid_map[(internal_entity_name, internal_entity_xmlid)]

class ForeignKeyQueue:
    """
    Maintains a queue of ForeignKeyQueueElement objects, with information on the foreign keys  
    that were found in a moment when the foreign table hadn't been processed yet, and how these
    pending columns should be treated when they are
    """

    table_foreign_key_queue_map = {}
    """ Dictionary relating tables with the foreign keys pending processing """

    def add_queue_element(self, element):
        """
        Adds a pending foreign key processing operation descriptor to the queue
        
        @param element: Foreign key processing operation descriptor 
        """

        foreign_table_name = element.foreign_table_name
        foreign_key_value = element.foreign_key_value
        if not foreign_table_name in self.table_foreign_key_queue_map:
            self.table_foreign_key_queue_map[foreign_table_name] = {}
        foreign_key_queue_map = self.table_foreign_key_queue_map[foreign_table_name]
        if not foreign_key_value in foreign_key_queue_map:
            foreign_key_queue_map[foreign_key_value] = []
        foreign_key_queue_map[foreign_key_value].append(element)

    def get_foreign_key_queue(self, table_name, primary_key_column_name):
        """
        Returns a list with information on the foreign keys that haven't been processed yet
        
        @param table_name: Name of the table for which one wants to get a list of the foreign keys pending processing
        @param primary_key_column_name: Name of the primary key columns on which the foreign keys are dependent on
        @return: List of descriptors of the pending foreign key processing operations
        """ 

        if table_name in self.table_foreign_key_queue_map and primary_key_column_name in self.table_foreign_key_queue_map[table_name]:
            return self.table_foreign_key_queue_map[table_name][primary_key_column_name]
        return []

class ForeignKeyQueueElement:
    """
    Stores information about a foreign key column that wasnt processed yet, so it can 
    be processed later when the referenced table is reached
    """

    internal_entity_name = None
    """ Name of the internal entity where the pending foreign key is """

    internal_entity_id = None
    """ Identifier of the internal entity instance where the pending foreign key is """

    foreign_table_name = None
    """ Name of the table that the foreign key is making a reference to """

    foreign_key_value = None
    """ Value of the foreign key (value of the primary key in the foreign table) """

    def __init__(self, internal_entity_name = None, internal_entity_id = None, foreign_key_value = None, foreign_table_name = None):
        self.internal_entity_name = internal_entity_name
        self.internal_entity_id = internal_entity_id
        self.foreign_key_value = foreign_key_value
        self.foreign_table_name = foreign_table_name
