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

import string
import sqlalchemy
import sqlalchemy.orm

DEFAULT_ALLOCATION_SIZE = 1000

#@todo: review and comment this file
class SqlAlchemyInputOutput:

    connection_string = "%s://%s:%s@%s:%s/%s"
    """ Default connection string """
    engine = None
    """ The database engine object """
    Session = None
    """ The session object for the current database connection """
    connection = None
    """ The current database connection """
    entity_class_map = {}
    """ Dictionary associating entity names with class references """
    entity_table_map = {}
    """ Dictionary associating entity names with database table references """
    entity_tablename_map = {}
    """ Dictionary associating entity names with database table names """
    primary_key_name_available_keys_map = {}
    """ Dictionary associating primary key names with object containing information about available keys """
    transaction = None
    """ Database transaction object """

    def __init__(self):
        self.entity_class_map = {}
        self.entity_table_map = {}
        self.entity_tablename_map = {}
        self.primary_key_name_available_keys_map = {}

    def get_engine(self, database_server_type = "none", username = "none", password = "none", database_name = "none", hostname = "localhost", port = "3306"):
        if not self.engine:
            self.engine = sqlalchemy.create_engine(self.connection_string % (database_server_type, username, password, hostname, port, database_name))
            self.engine.echo = False
            self.engine.metadata = sqlalchemy.MetaData()
            self.engine.metadata.bind = self.engine
            self.Session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind = self.engine, autoflush = False, autocommit = False))
        return self.engine

    def get_metadata(self):
        return self.engine.metadata

    def get_session(self):
        return self.session

    def get_connection(self):
        if self.engine and not self.connection:
            self.connection = self.engine.connect()
            Session = sqlalchemy.orm.sessionmaker(bind = self.engine, autoflush = False, autocommit = False)
            self.session = Session()
        return self.connection

    # @todo implement method
    def drop_connection(self):
        pass

    def metadata_create_all(self):
        self.engine.metadata.create_all(self.engine)

    def get_primary_key(self, primary_key_name, allocation_size = DEFAULT_ALLOCATION_SIZE):
        # in case there's information about primary keys created
        if primary_key_name in self.primary_key_name_available_keys_map:
            current_key_value, number_keys_available = self.primary_key_name_available_keys_map[primary_key_name]

            # in case there's more keys available
            if number_keys_available:
                current_key_value = current_key_value + 1
                number_keys_available = number_keys_available - 1
            # in case keys are over
            else:
                current_key_value = self.next_primary_key(primary_key_name, allocation_size)
                number_keys_available = allocation_size - 1
        else:
            current_key_value = self.next_primary_key(primary_key_name, allocation_size)

            # if the value is one there's one less value in the remaining keys
            if current_key_value == 1:
                number_keys_available = allocation_size - 2
            else:
                number_keys_available = allocation_size - 1

        self.primary_key_name_available_keys_map[primary_key_name] = (current_key_value, number_keys_available)

        return current_key_value

    def next_primary_key(self, primary_key_name, allocation_size = 1):
        """
        Gets the next primary key and stores the next one in the sequence
        
        @param primary_key_name: Name of the primary key for which you want to get the current value and increment it in the database
        @param allocation_size: Number of keys to allocate in a row
        @return: The current value of the requested primary key 
        """

        s = sqlalchemy.sql.text("select pkey,value from primary_keys")
        results = self.connection.execute(s).fetchall()
        for result in results:
            pkey = result[0]
            value = result[1]
            if pkey == primary_key_name:
                s = sqlalchemy.sql.text("UPDATE primary_keys SET value = '%d' WHERE primary_keys.pkey = '%s' AND primary_keys.value = %d" % (value + 1, primary_key_name, value))
                self.connection.execute(s)
                return value * allocation_size
        s = sqlalchemy.sql.text("INSERT INTO primary_keys(pkey,value) VALUE ('%s','%d')" % (primary_key_name, 1))
        self.connection.execute(s)
        return 1

    def flush(self):
        """
        Flushes all the previous operations down the stream of the I/O plugin
        """
        self.get_connection()
        return self.Session.flush()

    def delete(self, object):
        """
        Deletes an object from the datastore
        
        @param object: Entity instance to delete from the datastore
        """
        self.get_connection()
        return self.Session.delete(object)

    def save(self, object):
        """
        Saves an object to the datastore
		
        @param object: Entity instance to save to the datastore
        """
        self.get_connection()
        # in case the object does not contains an id an id is generated
        if object.id == None:
            object.id = self.get_primary_key(string.lower(object.get_parent_name()))
        return self.Session.save(object)

    def update(self, object):
        """
        Updates an object to the datastore
		
        @param object: Entity instance to update to the datastore
        """
        self.get_connection()
        return self.Session.update(object)

    def save_or_update(self, object):
        """
        Saves or updates an object to the datastore
		
        @param object: Entity instance to save or update to the datastore
        """
        self.get_connection()
        # in case the object does not contains an id an id is generated
        if object.id == None:
            object.id = self.get_primary_key(string.lower(object.get_parent_name()))
        return self.Session.save_or_update(object)

    def query(self, object):
        """
        Returns a set of objects from the datastore
        
        @param object: Entity whose instances one wants to retrieve
        @return: Retrieved entity instances 
        """
        self.get_connection()
        return self.Session.query(object)

    def begin_transaction(self):
        """
        Starts a new database transaction
        """
        self.get_connection()
        self.transaction = self.Session.create_transaction()

    def commit_transaction(self):
        """
        Commits the current database transaction
        """
        self.get_connection()
        self.transaction.commit()
        self.transaction = None

    def rollback_transaction(self):
        """
        Rolls back the current database transaction
        """
        self.get_connection()
        self.transaction.rollback()
        self.transaction = None
