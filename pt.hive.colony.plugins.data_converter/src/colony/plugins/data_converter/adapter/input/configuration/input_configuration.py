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

__revision__ = "$LastChangedRevision: 1807 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-03-10 11:07:56 +0000 (Tue, 10 Mar 2009) $"
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
        Constructor of the class.
        """
    
        self.table_map = {}

    def add_table(self, table):
        """
        Adds a table to the input configuration.
        
        @param table: Table object to add to this configuration.
        """
        self.table_map[table.name] = table

    def get_table(self, table_name):
        """
        Returns the specified table.
        
        @param table_name: Name of the table one wants to retrieve.
        """
        return self.table_map[table_name]

class Table:
    """
    Stores information about a database table and how it should be treated.
    """

    name = None
    """ Name of the database table. """

    internal_entity = None
    """ Name of the internal entity this database table will be copied into. """
    
    primary_key_columns = []
    """ Columns that make up this table's primary key. """
    
    foreign_keys = []
    """ This table's foreign keys. """
    
    column_map = {}
    """ Dictionary relating database column names with Column objects. """ 

    handlers = []
    """ List of handlers to process when this table is processed. """

    def __init__(self):
        """
        Constructor of the class
        """
        self.column_map = {}
        self.handlers = []
        self.primary_key_columns = []
        self.foreign_keys = []

    def add_column(self, column):
        """
        Adds a table column to this table.
        
        @param column: Column object to add to this table. 
        """
        self.column_map[column.name] = column
        
    def get_column(self, column_name):
        """
        Returns a table column.
        
        @return: Column object belonging to this table.
        """
        return self.column_map[column_name]
    
    def get_columns(self):
        """
        Retrieves a list of this table's columns.
        
        @return: List of table columns.
        """
        return self.column_map.values()
    
    def get_plain_columns(self):
        """
        Retrieves a list with all the columns belonging to this table
        that are not part of the primary key or any foreign key.
        
        @return: List of table columns.
        """
        columns = self.get_columns()
        
        # remove primary key columns
        for primary_key_column in self.primary_key_columns:
            if primary_key_column in columns:
                columns.remove(primary_key_column)
                
        # remove foreign key columns
        for foreign_key in self.foreign_keys:
            for foreign_key_column in foreign_key.columns:
                if foreign_key_column in columns:
                    columns.remove(foreign_key_column)
                    
        return columns

class Column:
    """
    Represents a database table column and how it should be treated.
    """

    name = None
    """ Name of the database table column. """

    internal_entity = None
    """ Internal entity this column belongs to, in case it is not the same as the parent table. """

    internal_entity_id = None
    """ Internal entity instance this column belongs to, in case it is not the same as the parent table. """

    internal_attribute = None
    """ Name of the internal entity attribute to which this column's contents will be copied to. """

    handlers = []
    """ List of handler functions. """

    def __init__(self):
        self.handlers = []
    
class ForeignKey:
    """
    Represents a foreign key that can be added to a Table object.
    """
    
    columns = []
    """ List of columns that make this foreign key. """
    
    def __init__(self):
        self.columns = []

    referenced_table = None
    """ Table this foreign key points to. """
    
class Handler:
    """
    Represents an handler function, which can be added to either a Table or a Column object.
    """

    name = None
    """ Name of the handler function. """
