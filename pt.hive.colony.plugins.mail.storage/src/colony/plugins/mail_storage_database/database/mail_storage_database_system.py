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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class MailStorageDatabase:
    """
    The mail storage database class.
    """

    mail_storage_database_plugin = None
    """ The mail storage database plugin """

    def __init__(self, mail_storage_database_plugin):
        """
        Constructor of the class.

        @type mail_storage_database_plugin: MailStorageDatabasePlugin
        @param mail_storage_database_plugin: The mail storage database plugin.
        """

        self.mail_storage_database_plugin = mail_storage_database_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: MailStorageDatabaseClient
        @return: The created client object.
        """

        # retrieves the version
        version = parameters.get("version", None)

        # creates the mail storage database client
        mail_storage_database_client = MailStorageDatabaseClient(self, version)

        # returns the mail storage database client
        return mail_storage_database_client

class MailStorageDatabaseClient:
    """
    The mail storage database client class.
    """

    mail_storage_database = None
    """ The mail storage database """

    def __init__(self, mail_storage_database):
        """
        Constructor of the class.

        @type mail_storage_database: MailStorageDatabase
        @param MailStorageDatabase: The mail storage database.
        """

        self.mail_storage_database = mail_storage_database

    def get_mail_storage_database(self):
        """
        Retrieves the mail storage database.

        @rtype: MailStorageDatabase
        @return: The mail storage database.
        """

        return self.mail_storage_database

    def set_mail_storage_database(self, mail_storage_database):
        """
        Sets the mail storage database.

        @type mail_storage_database: MailStorageDatabase
        @param mail_storage_database: Tghe mail storage database.
        """

        self.mail_storage_database = mail_storage_database
