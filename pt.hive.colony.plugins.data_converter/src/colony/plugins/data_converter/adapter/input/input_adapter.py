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

import data_converter.adapter.input.configuration.input_configuration_parser

class InputAdapter:
    """
    Adapter used to convert data from the source medium and schema to the internal structure.
    """

    internal_entity_name_primary_key_row_conversion_info_map = {}
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
        
        parser = data_converter.adapter.input.configuration.input_configuration_parser.InputConfigurationParser()
        file_paths = self.configuration.get_configuration_file_paths()
        for file_path in file_paths:
            parser.file_path = file_path
            parser.parse()
        self.input_description = parser.input_configuration

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
        self.internal_entity_name_primary_key_row_conversion_info_map = {}
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
        return internal_structure       

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
        Processes the tables indicated by the specified work unit.
        
        @type task: Task
        @param task: Task monitoring object used to inform the status of the query.
        @type counter_offset: int
        @param counter_offset: Where the progress counter should start at for this operation.
        @type counter_range: int
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)
        @type work_unit_name: String
        @param work_unit_name: Name of the work unit whose work will be performed.
        """

        self.logger.warn("Input adapter: Processing work unit '%s'.\n" % work_unit_name)

        counter = counter_offset
        table_names = self.configuration.get_tables(work_unit_name)
        counter_inc = counter_range / len(table_names)
        for table_name in table_names:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_table(table_name)
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

        self.logger.debug("Input adapter: Processing handler function '%s'.\n" % handler_name)
        
        if self.configuration.has_handler(handler_name):
            handler = self.configuration.get_handler(handler_name)
            return handler(arguments)        
        
    def process_table(self, table_name):
        """
        Converts the table's contents to the internal structure.
        
        @type table_name: String
        @param table_name: Name of the table one wants to process.
        """

        self.logger.warn("Input adapter: Processing table '%s'.\n" % table_name)

        # retrieve the table's rows
        table_configuration = self.input_description.get_table(table_name)
        column_names = [column_configuration.name for column_configuration in table_configuration.get_columns()]
        rows = self.connection.query(table_name, column_names)

        # for every row in the table
        for row in rows:     
            # create the entity related with the table and a table conversion information object
            row_internal_entity = self.internal_structure.add_entity(table_configuration.internal_entity)
            row_conversion_info = RowConversionInfo(table_configuration, self.internal_structure, row_internal_entity, row)
            # bind the entity's id to the table's primary key
            self.process_primary_key(row_conversion_info)
            # process the table columns
            self.process_columns(row_conversion_info)
            # run the handlers configured for this row
            for handler in row_conversion_info.configuration.handlers:
                self.process_handler(handler.name, [row_conversion_info, self])

    def process_columns(self, row_conversion_info):
        """
        Copies data from the database columns to the internal structure entity attributes.
        
        @type row_conversion_info: RowConversionInfo
        @param row_conversion_info: Object containing information about this row conversion process.
        """
        
        table_configuration = row_conversion_info.configuration
        row_internal_entity = row_conversion_info.internal_entity
        row = row_conversion_info.row
       
        # for every plain column, convert the value and send it to the associated entity instances
        for plain_column in table_configuration.get_plain_columns():
            # if the plain column as an internal attribute target and it exists in the row set
            if not plain_column.internal_attribute is None and plain_column.name in row:
                self.logger.debug("Input adapter: Processing column '%s'.\n" % plain_column.name)
                field_value = row[plain_column.name]
                destination_internal_entity_name = row_internal_entity._name
                destination_internal_entity_id = row_internal_entity._id
                # if the column is pointing to a different internal entity than the table then use that one instead and create a link to the table entity
                if plain_column.internal_entity and plain_column.internal_entity_id:
                    destination_internal_entity_name = plain_column.internal_entity
                    destination_internal_entity_id = row_conversion_info.get_real_internal_entity_id(plain_column.internal_entity, plain_column.internal_entity_id)
                    self.internal_structure.set_field_value(destination_internal_entity_name, destination_internal_entity_id, row_internal_entity._name, row_internal_entity)
                # grab the row and process it through its handlers
                for handler in plain_column.handlers:
                    field_value = self.process_handler(handler.name, [field_value])
                # store the row in the associated entity
                self.internal_structure.set_field_value(destination_internal_entity_name, destination_internal_entity_id, plain_column.internal_attribute, field_value)
                           
        # for every foreign key
        for foreign_key in table_configuration.foreign_keys:
            # compute the string representation of the foreign key
            foreign_key_column_names = [foreign_key_column.name for foreign_key_column in foreign_key.columns]
            foreign_key_values = [row[foreign_key_column.name] for foreign_key_column in foreign_key.columns]
            
            # if one of the foreign key values is null then cancel the foreign key binding operation
            if None in foreign_key_values:
                break
            
            foreign_key_string = str(foreign_key_values)

            self.logger.debug("Input adapter: Processing foreign key '%s'.\n" % foreign_key_string)

            # if the foreign row the foreign key points to was already converted to an entity then create a relation to it
            foreign_table = self.input_description.get_table(foreign_key.foreign_table)
            foreign_row_conversion_info = self.get_row_conversion_info(foreign_table.internal_entity, foreign_key_string)
            if foreign_row_conversion_info:
               foreign_internal_entity_id = foreign_row_conversion_info.internal_entity._id
               foreign_internal_entity_instance = self.internal_structure.get_entity(foreign_table.internal_entity, foreign_internal_entity_id)
               self.internal_structure.set_field_value(row_internal_entity._name, row_internal_entity._id, foreign_table.internal_entity, foreign_internal_entity_instance)
            else: # otherwise add the foreign key to the queue
               self.foreign_key_queue.append({"foreign_key_string" : foreign_key_string,
                                              "foreign_key_internal_entity_name" : row_internal_entity._name,
                                              "foreign_key_internal_entity_id" : row_internal_entity._id,
                                              "foreign_internal_entity_name" : foreign_table.internal_entity})
                
    def process_primary_key(self, row_conversion_info):
        """
        Extracts the primary key value from the query row set and into the the internal structure. After this
        operation the row set will not contain the primary key column anymore.
        
        @type row_conversion_info: RowConversionInfo
        @param row_conversion_info: Object containing information about the row conversion process.
        """
        
        table_configuration = row_conversion_info.configuration
        row = row_conversion_info.row
        
        # compute this row's primary key string representation
        primary_key_column_names = [column.name for column in table_configuration.primary_key_columns]
        primary_key_string = str([row[primary_key_column_name] for primary_key_column_name in primary_key_column_names])
         
        # associate the row conversion information with the primary key
        key = (row_conversion_info.internal_entity._name, primary_key_string)
        self.internal_entity_name_primary_key_row_conversion_info_map[key] = row_conversion_info

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
                row_conversion_info = self.get_row_conversion_info(foreign_internal_entity_name, foreign_key_information["foreign_key_string"])  
                if row_conversion_info:
                    foreign_internal_entity_id = row_conversion_info.internal_entity._id
                    foreign_internal_entity = self.internal_structure.get_entity(foreign_internal_entity_name, foreign_internal_entity_id)
                    self.internal_structure.set_field_value(foreign_key_internal_entity_name, foreign_key_internal_entity_id, foreign_internal_entity_name, foreign_internal_entity) 
                    processed_foreign_keys.append(foreign_key_information)

            # remove the processed foreign keys from the foreign key queue
            for processed_foreign_key in processed_foreign_keys:
                self.foreign_key_queue.remove(processed_foreign_key)

    def get_row_conversion_info(self, entity_name, primary_key_string):
        """
        Retrieves the conversion information used 
        
        @type entity_name: String
        @param entity_name: Name of the internal entity from which one wants to get an identifier.
        @type primary_key_string: String
        @param primary_key_string: String representation of associated primary key.
        @rtype: RowConversionInfo
        @return: Object with information on how the row was converted to an entity.
        """

        key = (entity_name, primary_key_string)
        if key in self.internal_entity_name_primary_key_row_conversion_info_map:
            return self.internal_entity_name_primary_key_row_conversion_info_map[key]

class RowConversionInfo:
    """
    Holds information about the conversion of a certain database table row.
    """

    configuration = None
    """ Table configuration object describing the table this row belongs to """

    internal_structure = None
    """ Intermediate structure where the data converter input adapter's results are stored """

    internal_entity = None
    """ The internal entity created for this row """

    row = None
    """ Source medium table row """
    
    internal_entity_configuration_id_internal_id_map = {}
    """ Dictionary relating the unique identifier of an internal entity instance in a table's configuration file with the internal entity instance's real id """

    def __init__(self, configuration, internal_structure, internal_entity, row):
        """
        Class constructor.
        
        @type configuration: Object
        @param configuration: Object representing the conversion configuration for this table.
        @type internal_structure: InternalStructure
        @param internal_structure: Intermediate structure where the data converter input adapter's results are stored.
        @type internal_entity: String
        @param internal_entity: The internal entity created for this row.
        @type row: Dictionary
        @param row: The row being converted.
        """

        self.configuration = configuration
        self.internal_entity = internal_entity
        self.internal_structure = internal_structure
        self.row = row
        self.internal_entity_configuration_id_internal_id_map = {}

    def get_real_internal_entity_id(self, internal_entity_name, table_configuration_internal_entity_id):
        """
        Retrieves the equivalent internal entity id in the internal structure for the provided
        internal entity id in the configuration file.

        @type internal_entity_name: String
        @param internal_entity_name: Name of the internal entity.
        @type table_configuration_internal_entity_id: int
        @param table_configuration_internal_entity_id: Identification number of the internal entity in the configuration file.
        @rtype: int
        @return: Returns the internal entity's unique identifier in the internal structure.
        """

        key = (internal_entity_name, table_configuration_internal_entity_id)
        if not key in self.internal_entity_configuration_id_internal_id_map:
            internal_entity = self.internal_structure.add_entity(internal_entity_name)
            self.internal_entity_configuration_id_internal_id_map[key] = internal_entity._id
        return self.internal_entity_configuration_id_internal_id_map[key]
