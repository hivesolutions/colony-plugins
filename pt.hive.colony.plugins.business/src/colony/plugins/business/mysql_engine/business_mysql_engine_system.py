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

import MySQLdb

import business_mysql_engine_exceptions

ENGINE_NAME = "mysql"
""" The engine name """

HOSTNAME_VALUE = "hostname"
""" The hostname value """

USERNAME_VALUE = "username"
""" The username value """

PASSWORD_VALUE = "password"
""" The password value """

DATABASE_VALUE = "database"
""" The database value """

class BusinessMysqlEngine:
    """
    The business mysql engine class
    """

    business_mysql_engine_plugin = None
    """ The business mysql engine plugin """

    def __init__(self, business_mysql_engine_plugin):
        """
        Constructor of the class

        @type business_mysql_engine_plugin: BusinessMysqlEnginePlugin
        @param business_mysql_engine_plugin: The business mysql engine plugin
        """

        self.business_mysql_engine_plugin = business_mysql_engine_plugin

    def get_engine_name(self):
        return ENGINE_NAME

    def create_connection(self, connection_parameters):
        """
        Creates the connection using the given connection parameters.

        @type connection_parameters: List
        @param connection_parameters: The connection parameters.
        @rtype: Connection
        @return: The created connection.
        """

        # in case the hostname is not defined
        if not HOSTNAME_VALUE in connection_parameters:
            raise business_mysql_engine_exceptions.MissingProperty(HOSTNAME_VALUE)

        # in case the username is not defined
        if not USERNAME_VALUE in connection_parameters:
            raise business_mysql_engine_exceptions.MissingProperty(USERNAME_VALUE)

        # in case the password is not defined
        if not PASSWORD_VALUE in connection_parameters:
            raise business_mysql_engine_exceptions.MissingProperty(PASSWORD_VALUE)

        # in case the database is not defined
        if not DATABASE_VALUE in connection_parameters:
            raise business_mysql_engine_exceptions.MissingProperty(DATABASE_VALUE)

        # retrieves the hostname parameter value
        hostname = connection_parameters[HOSTNAME_VALUE]

        # retrieves the username parameter value
        username = connection_parameters[USERNAME_VALUE]

        # retrieves the password parameter value
        password = connection_parameters[PASSWORD_VALUE]

        # retrieves the database parameter value
        database = connection_parameters[DATABASE_VALUE]

        # creates the mysql database connection
        connection = MySQLdb.connect(host = hostname, user = username, passwd = password, db = database)

        return connection

    def commit_connection(self, connection):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # commits the changes to the connection
        database_connection.commit()

        return True

    def rollback_connection(self, connection):
        # retrieves the database connection from the connection object
        database_connection = connection.database_connection

        # "rollsback" the changes to the connection
        database_connection.rollback()

        return True

    def create_transaction(self, connection, transaction_name):
        return True

    def commit_transaction(self, connection, transaction_name):
        # retrieves the transaction stack from the connection object
        transaction_stack = connection.transaction_stack

        # in case there is only one element in the transaction stack
        if len(transaction_stack) == 1:
            return self.commit_connection(connection)

        return True

    def rollback_transaction(self, connection, transaction_name):
        # "rollsback" the transaction
        return self.rollback_connection(connection)
