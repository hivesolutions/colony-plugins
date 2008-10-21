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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import sqlalchemy
import sqlalchemy.orm

class DummyBusinessLogic:
    """
    The dummy business logic class
    """

    dummy_business_logic_plugin = None
    """ The dummy business logic plugin """

    def __init__(self, dummy_business_logic_plugin):
        """
        Constructor of the class
        
        @type dummy_business_logic_plugin: DummyBusinessLogicPlugin
        @param dummy_business_logic_plugin: The dummy business logic plugin
        """

        self.dummy_business_logic_plugin = dummy_business_logic_plugin

    def insert_user(self, user_id, username):
        """
        Inserts a user with the given user id and username into the database
        
        @type user_id: int
        @param user_id: The identification of the user to insert into the database
        @type username: String
        @param username: The username of the user to insert into the database
        """

        # creates a metadata object
        metadata = sqlalchemy.MetaData()

        # creates the mapper for the users table
        users_table = sqlalchemy.Table('users', metadata, 
                                       sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key = True),
                                       sqlalchemy.Column("username", sqlalchemy.String))

        # retrieves the user entity object
        user_entity = self.dummy_business_logic_plugin.dummy_database_access_plugin.get_entity_by_entity_name("user")

        # in case there is no map related with the entity object
        if not user_entity.__mapper__:
            # sets the relation between the mapper and the entity class
            sqlalchemy.orm.mapper(user_entity, users_table, non_primary = True) 

        # creates the user instance
        user_instance = user_entity(user_id, username)

        # creates the new engine for the local mysql database
        engine = sqlalchemy.create_engine("mysql://hive:hive@localhost/test_hive")

        # creates the session maker (factory)
        Session = sqlalchemy.orm.sessionmaker(bind = engine)

        # creates a new session
        session = Session()

        # adds the user instance to the database
        session.add(user_instance)

        # commits the session
        session.commit()
