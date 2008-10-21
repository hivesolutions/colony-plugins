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

class InputConfiguration:
    """ 
    Stores the information defined by the input configuration file and provides an easy way to retrieve it. 
    """

    table_map = {}
    """ Dictionary relating table name with Table object instances. """

    def __init__(self):
        """
        Constructor of the class
        """
    
        self.table_map = {}

    def add_table(self, table):
        """
        Adds a table to the input configuration.
        
        @param table: Table object to add to this configuration.
        """
        self.table_map[table.get_name()] = table

    def add_column(self, table_name, column):
        """
        Adds a column to a specified table.
        
        @param table_name: Name of the table where the column will be added.
        @param column: Column object to add to the table.
        """
        self.table_map[table_name].add_column(column)

    def add_handler(self, table_name, handler):
        """
        Adds an handler function to the specified table.
        
        @param table_name: Name of the table where to add the function.
        @param handler: Handler function to add to the table.
        """
        self.table_map[table_name].add_handler(handler)

    def add_column_handler(self, table_name, column_name, handler):
        """
        Adds a function handler to a specified table column.
        
        @param table_name: Name of the table where the column argument belongs to.
        @param column_name: Name of the column where to add the function handler.
        @param handler: Function handler to add to the column.
        """
        self.table_map[table_name].add_handler(column_name, handler)

    def get_internal_entity_name(self, table_name):
        """
        Returns the name of the internal entity associated with the specified table.
        
        @param table_name: Name of the table for which one want the correspondent internal entity name.
        @return: String with the name of the internal entity.
        """
        return self.table_map[table_name].get_internal_entity_name()

    def get_internal_attribute_entity_id(self, table_name, column_name):
        """
        Returns the instance id of the internal entity this column belongs to.
        
        @param table_name: Name of the table to which the column name argument belongs.
        @param column_name: Name of the column for which one wants the correspondent internal entity instance id.
        @return: String with the id of the internal entity instance this column belongs to, None if it's the same as the parent table.
        """
        return self.table_map[table_name].get_internal_attribute_entity_id(column_name)

    #@todo: comment this function
    def get_internal_attribute_entity_name(self, table_name, column_name):
        """
        @param table_name: Name of the table to which the column name argument belongs.
        @param column_name: Name of the column for which one wants the correspondent internal entity name.
        @return: String with the name of the internal entity this column belongs to, None if it's the same as the parent table.
        """
        return self.table_map[table_name].get_internal_attribute_entity_name(column_name)

    def get_internal_attribute_name(self, table_name, column_name):
        """
        Returns the name of the internal attribute that corresponds to the specified table column.
        
        @param table_name: Name of the table to which the second column name argument belongs.
        @param column_name: Name of the column for which one wants the correspondent internal attribute name.
        @return: String with the requested internal attribute name.
        """
        return self.table_map[table_name].get_internal_attribute_name(column_name)

    def get_table_handler_list(self, table_name):
        """
        Returns the a list of handler functions associated with the specified table.
        
        @param table_name: Name of the table for which one wants the list of handler functions.
        @return: List with handler function references.
        """
        return self.table_map[table_name].get_handler_list()

    def get_column_name_list(self, table_name):
        """
        Returns a list with the names of the columns present in a certain table.
        
        @param table_name: Name of the table for which one wants the column name list.
        @return: List of strings with the names of the columns in the specified table.
        """
        return self.table_map[table_name].get_column_name_list()

    def get_column_handler_list(self, table_name, column_name):
        """
        Returns a list with of handler functions for a certain table column.
        
        @param table_name: Name of the table to which the column name argument belongs.
        @param column_name: Name of the column for which one wants the correspondent list of handlers.
        @return: List with handler function references.
        """
        return self.table_map[table_name].get_column_handler_list(column_name)

    def get_primary_key_column_name(self, table_name):
        """
        Returns the name of the primary key column in this table.
        
        @param table_name: Name of the table whose primary key column name one wants to get.
        @return: String with the name of the primary key column for the specified table.
        """
        return self.table_map[table_name].get_primary_key_column_name()

    def get_foreign_key_column_name_list(self, table_name):
        """
        Returns a list of foreign key column names for the specified table.
        
        @param table_name: Name of the table for which one wants a list of foreign key columns.
        @return: List with this table's foreign key column names.
        """
        return self.table_map[table_name].get_foreign_key_column_name_list()

    def get_referenced_table_name(self, table_name, column_name):
        """
        Returns the name of the table referenced by the specified column.
        
        @param table_name: Name of the table to which the column name argument belongs.
        @param column_name: Name of the column for which one wants the correspondent reference table.
        @return: Name of the referenced table, None if this is not a relation column.
        """
        return self.table_map[table_name].get_referenced_table_name(column_name)

    def is_processable_column(self, table_name, column_name):
        """
        @param table_name: Name of the table to which the column name argument belongs.
        @param column_name:
        @return:
        """
        return self.table_map[table_name].is_processable_column(column_name)

    def is_primary_key_column(self, table_name, column_name):
        """
        Indicates if the specified table column is a primary key.
        
        @param table_name: Name of the table to which the column name argument belongs.
        @param column_name: Name of the column one wants to know if it is a primary key.
        @return: Boolean indicating if the specified table column is a primary key.
        """
        return self.table_map[table_name].is_primary_key_column(column_name)

    def is_table_reference(self, table_name, column_name):
        """
        Indicates if the specified table column is a foreign key.
        
        @param table_name: Name of the table to which the column name argument belongs.
        @param column_name: Name of the column one wants to know if it is a foreign key.
        @return: Boolean indicating if the specified table column is a foreign key.
        """
        return self.table_map[table_name].is_table_reference(column_name)

class Table:
    """
    Stores information about a database table and how it should be treated.
    """

    name = None
    """ Name of the database table. """

    internal_entity = None
    """ Name of the internal entity this database table will be copied into. """
    
    column_map = {}
    """ Dictionary relating database column names with Column objects. """ 

    handler_list = []
    """ List of handlers to process when this table is processed. """

    def __init__(self):
        """
        Constructor of the class
        """

        self.column_map = {}
        self.handler_list = []

    def add_handler(self, handler):
        """
        Adds an handler function to this table.
        
        @param handler: Handler function to add this table.
        """
        self.handler_list.append(handler)

    def add_column(self, column):
        """
        Adds a table column to this table.
        
        @param column: Column object to add to this table. 
        """
        self.column_map[column.get_name()] = column

    def add_column_handler(self, column_name, handler):
        """
        Adds an handler function to the specified table column.
        
        @param column_name: Name of the column to which one wants to add the handler function.
        @param handler: Handler function to add to the table column.
        """
        self.column_map[column_name].add_handler(handler)

    def get_name(self):
        """
        Returns this table's name.
        
        @return: String with this table's name.
        """
        return self.name

    def get_handler_list(self):
        """
        Returns the list of handlers to be processed in this table.
        
        @return: List of handler functions to be processed in this table.
        """
        return self.handler_list

    def get_internal_entity_name(self):
        """
        Returns the name of the internal entity that corresponds to this table.
        
        @return: String with the name of the requested internal entity.
        """
        return self.internal_entity

    def get_internal_attribute_name(self, column_name):
        """
        Returns the name of the internal attribute related to the specified table column.
        
        @param column_name: Name of the column one wants to know the correspondent internal attribute name.
        @return: String with the name of the requested internal attribute.
        """
        return self.column_map[column_name].get_internal_attribute_name()

    def get_internal_attribute_entity_id(self, column_name):
        """
        Returns the instance id of the internal entity this column belongs to.
        
        @param column_name: Name of the column one wants to know the correspondent internal entity instance id.
        @return: String with the id of the internal entity instance this column belongs to, None if it's the same as the parent table.
        """
        return self.column_map[column_name].get_internal_entity_id()

    def get_internal_attribute_entity_name(self, column_name):
        """
        Returns the name of the internal entity this column belongs to.
        
        @param column_name: Name of the column one wants to know the correspondent internal entity name.
        @return: String with the name of the internal entity this column belongs to, None if it's the same as the parent table.
        """
        if self.column_map[column_name].get_internal_entity_name() == None:
            return self.internal_entity
        return self.column_map[column_name].get_internal_entity_name()

    def get_column_handler_list(self, column_name):
        """
        Returns the list of handler functions to be processed for the specified table column.

        @param column_name: Name of the column for which one wants the respective list of handler functions.
        @return: List of handler functions.
        """
        return self.column_map[column_name].get_handler_list()

    def get_column_name_list(self):
        """
        Returns a list of table column names.
        
        @return: List of table column names.
        """
        column_name_list = []
        for key in self.column_map:
            column_name_list.append(self.column_map[key].get_name())
        return column_name_list

    def get_primary_key_column_name(self):
        """
        Returns the name of the primary key column in this table.
        
        @return: String with the name of the primary key column in this table.
        """
        for key in self.column_map:
            if self.column_map[key].is_primary_key_column():
                return self.column_map[key].get_name()

    def get_foreign_key_column_name_list(self):
        """
        Returns a list with the names of the foreign key columns in this table.
        
        @return: List with the foreign key column names for this table.
        """
        foreign_key_column_name_list = []
        for key in self.column_map:
            if self.column_map[key].referenced_table:
                foreign_key_column_name_list.append(self.column_map[key].get_name())
        return foreign_key_column_name_list

    def get_referenced_table_name(self, column_name):
        """
        Indicates the name of the table being referenced by the specified column, if any.
        
        @param column_name: Name of the column whose referenced table name one wants to get.
        @return: Name of the referenced table, None if there's no reference.
        """
        return self.column_map[column_name].referenced_table 

    def is_processable_column(self, column_name):
        """
        Indicates if the column is processable, meaning it is not a primary key and has a correspondent internal attribute.
        
        @param column_name: Name of the column one wants to know if it is a processable column.
        @return: Boolean indicating if the column is processable.
        """
        return self.column_map[column_name].is_processable_column()

    def is_primary_key_column(self, column_name):
        """
        Indicates if the specified column is a primary key column in this table.
        
        @param column_name: Name of the column one wants to know if it is a primary key.
        @return: Boolean indicating if the specified column is a primary key or not.
        """
        return self.column_map[column_name].is_primary_key_column()

    def is_table_reference(self, column_name):
        """
        Indicates if the specified column is a foreign key column in this table.
        
        @param column_name: Name of the column one wants to know if it is a foreign key.
        @return: Boolean indicating if the specified column is a foreign key or not.
        """
        return not self.column_map[column_name].referenced_table == None

    def __repr__(self):
        """
        Prints out a string representation of this object when it is used as a parameter for the print() function,
        or returns this string representation if the method itself is invoked.
        
        @return: String representation of this object.
        """ 
        return_string = ""
        return_string += "name = %s\n" % self.name
        return_string += "internal_entity = %s\n" % self.internal_entity       
        for key in self.column_map:
            return_string += "<column>\n"
            return_string += self.column_map[key].__repr__()
            return_string += "<\column>\n"
        return return_string

class Column:
    """
    Represents a database table column and how it should be treated.
    """

    name = None
    """ Name of the database table column. """

    primary_key = False
    """ Indicates if this column is part of the table's primary keys. """

    internal_entity = None
    """ Internal entity this column belongs to, in case it is not the same as the parent table. """

    internal_entity_id = None
    """ Internal entity instance this column belongs to, in case it is not the same as the parent table. """

    internal_attribute = None
    """ Name of the internal entity attribute to which this column's contents will be copied to. """

    referenced_table = None
    """ Name of the database table referenced by this column (in case it is a foreign key). """

    handler_list = []
    """ List of handler functions. """

    def __init__(self):
        self.handler_list = []

    def add_handler(self, handler):
        """
        Adds a column handler to this column.
        
        @param handler: Handler function to add to the table column.
        """
        self.handler_list.append(handler)

    def get_name(self):
        """
        Returns the name of this column.
        
        @return: String with the name of this column.
        """
        return self.name

    def get_handler_list(self):
        """
        Returns a list with of handler functions for this table column.

        @return: List with handler function references.
        """
        return self.handler_list

    def get_internal_entity_name(self):
        """
        Returns the name of the internal entity this column belongs to.
        
        @return: String with the name of the internal entity this column belongs to, None if it's the same as the parent table.
        """
        return self.internal_entity

    def get_internal_entity_id(self):
        """
        Returns the instance id of the internal entity this column belongs to.
        
        @return: String with the id of the internal entity instance this column belongs to, None if it's the same as the parent table.
        """
        return self.internal_entity_id

    def get_internal_attribute_name(self):
        """
        Returns the name of the internal attribute correspondent with this column.
        
        @return: String with the name of this internal attribute.
        """
        return self.internal_attribute

    def is_primary_key_column(self):
        """
        Indicates if this column is a primary key column.
        
        @return: Boolean indicating if this is a primary key column.
        """
        return self.primary_key

    def is_processable_column(self):
        """
        Indicates if the column is processable, meaning it is not a primary key and has a correspondent internal attribute.
        
        @return: Boolean indicating if the column is processable.
        """
        return self.primary_key == False and not self.internal_attribute == None

    def __repr__(self):
        """
        Prints out a string representation of this object when it is used as a parameter for the print() function,
        or returns this string representation if the method itself is invoked.
        
        @return: String representation of this object.
        """ 
        return_string = ""
        return_string += "\tname = %s\n" % self.name
        return_string += "\tprimary_key = %s\n" % self.primary_key
        return_string += "\tinternal_attribute = %s\n" % self.internal_attribute
        return_string += "\treferenced_table = %s\n" % self.referenced_table
        return return_string

class Handler:
    """
    Represents an handler function, which can be added to either a Table or a Column object.
    """

    name = None
    """ Name of the handler function. """

    def __repr__(self):
        """
        Prints out a string representation of this object when it is used as a parameter for the print() function,
        or returns this string representation if the method itself is invoked.
        
        @return: String representation of this object.
        """ 
        return_string = ""
        return_string += "\tname = %s\n" % self.name
        return return_string