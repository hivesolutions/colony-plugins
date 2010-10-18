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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 5731 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-21 19:04:42 +0100 (qua, 21 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

ENTITIES_MODULE_NAME = "communication_push_persistence_database_entities"
""" The entities module name """

class CommunicationPushPersistenceDatabase:
    """
    The communication push persistence database plugin.
    """

    comnunication_push_persistence_database_plugin = None
    """ The communication push persistence database plugin """

    def __init__(self, comnunication_push_persistence_database_plugin):
        """
        Constructor of the class.

        @type comnunication_push_persistence_database_plugin: CommunicationPushPersistenceDatabasePlugin
        @param comnunication_push_persistence_database_plugin: The communication push persistence database plugin.
        """

        self.comnunication_push_persistence_database_plugin = comnunication_push_persistence_database_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: CommunicationPushPersistenceDatabaseClient
        @return: The created client object.
        """

        # retrieves the entity manager arguments
        entity_manager_arguments = parameters.get("entity_manager_arguments", {})

        # creates the communication push persistence database client
        communication_push_persistence_database_client = CommunicationPushPersistenceDatabaseClient(self, entity_manager_arguments)

        # returns the communication push persistence database client
        return communication_push_persistence_database_client

class CommunicationPushPersistenceDatabaseClient:
    """
    The communication push persistence database client class.
    """

    communication_push_persistence_database = None
    """ The communication push persistence database """

    entity_manager_arguments = None
    """ The entity manager arguments """

    entity_manager = None
    """ The entity manager to be used to access the database """

    def __init__(self, communication_push_persistence_database, entity_manager_arguments):
        """
        Constructor of the class.

        @type communication_push_persistence_database: CommunicationPushPersistenceDatabase
        @param communication_push_persistence_database: The communication push persistence database.
        @type entity_manager_arguments: Dictionary
        @param entity_manager_arguments: The entity manager arguments.
        """

        self.communication_push_persistence_database = communication_push_persistence_database
        self.entity_manager_arguments = entity_manager_arguments

    def create_mailbox(self, name):
        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # creates a transaction
        entity_manager.create_transaction()

        try:
            # retrieves the mailbox class
            mailbox_class = entity_manager.get_entity_class("Mailbox")

            # creates the new mailbox instance
            mailbox = mailbox_class()

            # sets the initial mailbox attributes
            mailbox.name = name
            mailbox.messages_count = 0
            mailbox.messages_size = 0

            # saves the mailbox
            entity_manager.save(mailbox)
        except:
            # rolls back the transaction
            entity_manager.rollback_transaction()

            # re-raises the exception
            raise
        else:
            # commits the transaction
            entity_manager.commit_transaction()

    def _get_entity_manager(self):
        """
        Retrieves the currently available entity
        manager instance.

        @rtype: EntityManager
        @return: The currently available entity
        manager instance.
        """

        # in case the entity manager is not set
        # the entity manager is not loaded
        if not self.entity_manager:
            # loads the entity manager
            self._load_entity_manager()

        # returns the entity manager
        return self.entity_manager

    def _load_entity_manager(self):
        """
        Loads the entity manager object, used to access
        the database.
        """

        # retrieves the entity manager helper plugin
        entity_manager_helper_plugin = self.mail_storage_database.mail_storage_database_plugin.entity_manager_helper_plugin

        # loads the entity manager for the entities module name
        self.entity_manager = entity_manager_helper_plugin.load_entity_manager(ENTITIES_MODULE_NAME, os.path.dirname(__file__), self.entity_manager_arguments)
