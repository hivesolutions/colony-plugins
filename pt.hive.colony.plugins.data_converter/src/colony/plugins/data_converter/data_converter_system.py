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

class InternalStructure:
    """
    Internal structure to store an intermediate data representation of the converted data, created by the input adapter,
    over which the output adapter later acts to convert the data to the target medium.
    """
    
    exclusions = ["exclusions", "__doc__", "__module__", "has_entities", "has_entity", "has_field", "add_entity", "add_field", 
                  "set_field_value", "get_entity", "display_structure", "print_structure", "get_entity_instances"]

    def get_entity_instances(self, internal_entity_name):
        """
        Returns a list with the entity instances with the specified name that are
        currently present in the internal structure.
        
        @param internal_entity_name: Name of the internal entity.
        @return: List of entity instances.
        """
        return getattr(self, internal_entity_name)
    
    def has_entities(self, entity_name):
        """
        Indicates if the specified entity list already exists in the internal
        structure.
        
        @param entity_name: Name of the internal entity.
        @return: Boolean indicating if the entity list exists.
        """
        return hasattr(self, entity_name)

    def has_entity(self, entity_name, entity_id):
        """
        Indicates if the specified entity instance exists in the internal 
        structure.
        
        @param entity_name: Name of the internal entity.
        @param entity_id: Unique identifier for the internal entity instance.
        @return: Boolean indicating if the internal entity exists.
        """
        if self.has_entities(entity_name):
            entities = getattr(self, entity_name)
            if entity_id < len(entities):
                return True
        return False
    
    def has_field(self, entity_name, entity_id, field_name):
        """
        Indicates if the internal entity has the specified field.
        
        @param entity_name: Name of the internal entity.
        @param entity_id: Unique identifier for the internal entity instance.
        @param field_name: Name of the internal entity field.
        @return: Boolean indicating if the internal entity instance has the specified field.
        """
        if self.has_entity(entity_name, entity_id):
            entity = self.get_entity(entity_name, entity_id)
            return entity.has_field(field_name)
        return False

    def add_entity(self, entity_name):
        """
        Creates a new entity instance in the internal structure and returns it position
        in the entity list.
        
        @param entity_name: Name of the internal entity.
        @return: Position the new entity instance takes in its entity list.
        """
        if not self.has_entities(entity_name):
            setattr(self, entity_name, [])
        entities = getattr(self, entity_name)
        entity_structure = EntityStructure()
        entities.append(entity_structure)
        entity_structure._id = len(entities) - 1
        entity_structure._name = entity_name
        return entity_structure

    def add_field(self, entity_name, entity_id, field_name):
        """
        Adds a new field to an internal entity instance.
        
        @param entity_name: Name of the internal entity.
        @param entity_id: Unique identifier for the internal entity instance.
        @param field_name: Name of the internal entity field.
        """
        if self.has_entity(entity_name, entity_id):
            entity = self.get_entity(entity_name, entity_id)
            entity.add_field(field_name)

    def set_field_value(self, entity_name, entity_id, field_name, value):
        """
        Changes an internal entity instance's field value.
        
        @param entity_name: Name of the internal entity.
        @param entity_id: Unique identifier for the internal entity instance.
        @param field_name: Name of the internal entity field.
        @param value: Value to set in the internal entity field.
        """
        if not self.has_field(entity_name, entity_id, field_name):
            self.add_field(entity_name, entity_id, field_name)
        entity = self.get_entity(entity_name, entity_id)
        entity.set_field_value(field_name, value)

    def get_entity(self, entity_name, entity_id):
        """
        Returns an internal entity instance.
        
        @param entity_name: Name of the internal entity.
        @param entity_id: Unique identifier for the internal entity instance.
        @return: The specified internal entity instance.
        """
        if self.has_entity(entity_name, entity_id):
            entities = getattr(self, entity_name)
            entity = entities[entity_id]
            return entity

class EntityStructure:
    """
    Represents an entity in the internal structure.
    """
    
    exclusions = ["exclusions", "_id", "_name", "__doc__", "__module__", "has_field", "add_field", "set_field_value", "get_field_value", "print_structure"]
    
    def has_field(self, field_name):
        """
        Indicates if the entity has the specified field.
        
        @param field_name: Name of the field one wants to know if it exists.
        @return: Boolean indicating if the field exists.
        """
        return hasattr(self, field_name)
    
    def add_field(self, field_name):
        """
        Creates a new field.
        
        @param field_name: Name of the field whose value one wants to create.
        """
        if not self.has_field(field_name):
            setattr(self, field_name, None)
        
    def set_field_value(self, field_name, value):
        """
        Changes the a field's value.
        
        @param field_name: Name of the field whose value one wants to change.
        @param value: New value one wants to set in the field.
        """
        if not self.has_field(field_name):
            self.add_field(field_name)
        setattr(self, field_name, value)
        
    def get_field_value(self, field_name):
        """
        Returns a field's value.
        
        @param field_name: Name of the field whose value one wants to return.
        @return: The specified field's value.
        """
        if self.has_field(field_name):
            return getattr(self, field_name)

class DataConverter:
    """
    Converts data from one medium and schema to another.
    """
    
    data_converter_plugin = None
    """ Plugin that owns this code. """
    
    internal_structure = None
    """ Internal structure used to hold the results of the input adapter (which is the source for the output adapter). """
    
    task = None
    """ Task used by the data converter to signal the progress of its workflow and to control it. """
    
    def __init__(self, data_converter_plugin):
        """
        Class constructor.
        
        @param data_converter_plugin: Data converter plugin.
        """
        self.data_converter_plugin = data_converter_plugin
        
    def convert(self, options):
        """
        Starts the conversion process.
        
        @param options: Map with the conversion process options.
        """
        self.task = self.data_converter_plugin.task_manager_plugin.create_new_task("Data converter", "Converting data", self.start_handler)
        self.task.set_task_pause_handler(self.pause_handler)
        self.task.set_task_resume_handler(self.resume_handler)
        self.task.set_task_stop_handler(self.stop_handler)
        self.task.start(options)

    def start_handler(self, task, options):
        """
        Handler invoked when the data conversion task starts.
        
        @param task: Data conversion task object.
        @param options: Data conversion options.
        """
        
        # figure out which io plugin to use in the input adapter
        input_io_plugin_id = options["input_io_plugin_id"]
        input_io_plugin = None
        for input_io_plugin in self.data_converter_plugin.io_plugins:
            if input_io_plugin.id == input_io_plugin_id:
                break
    
        # figure out which io plugin to use in the output adapter
        output_io_plugin_id = options["output_io_plugin_id"]
        output_io_plugin = None
        for output_io_plugin in self.data_converter_plugin.io_plugins:
            if output_io_plugin.id == output_io_plugin_id:
                break
            
        # figure out which configuration plugin to use
        data_converter_configuration_plugin_id = options["configuration_plugin_id"]
        for data_converter_configuration_plugin in self.data_converter_plugin.data_converter_configuration_plugins:
            if data_converter_configuration_plugin.id == data_converter_configuration_plugin_id:
                break

        # if the selected combination of input/output/configuration exists then perform the conversion
        if input_io_plugin and output_io_plugin and data_converter_configuration_plugin:              
            # map data into the internal structure
            input_adapter_configuration = data_converter_configuration_plugin.get_input_adapter_configuration()
            connection = input_io_plugin.connect(options["input_connection_options"])
            internal_structure = self.data_converter_plugin.input_adapter.convert(task, InternalStructure(), connection, input_adapter_configuration)
            
            # map data out of the internal structure and into the target
            #connection = None
            # connection = output_io_plugin.connect(args["output_connection_options"])
            #output_adapter_configuration = data_converter_configuration_plugin.get_output_adapter_configuration()
            #self.data_converter_plugin.output_adapter.convert(task, options, connection, output_adapter_configuration)
            
        task.confirm_stop(True)   

    def pause_handler(self, options):
        """
        Handler invoked when the data conversion task pauses.
        
        @param options: Data conversion options.
        """
        pass

    def resume_handler(self, options):
        """
        Handler invoked when the data conversion task resumes.
        
        @param options: Data conversion options.
        """
        pass

    def stop_handler(self, options):
        """
        Handler invoked when the data conversion task stops.
        
        @param options: Data conversion options.
        """
        pass
