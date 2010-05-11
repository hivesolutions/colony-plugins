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

import os
import threading

import mail_queue_database_exceptions

ENTITIES_MODULE_NAME = "mail_queue_database_entities"
""" The entities module name """

class MailQueueDatabase:
    """
    The mail queue database class.
    """

    mail_queue_database_plugin = None
    """ The mail queue database plugin """

    def __init__(self, mail_queue_database_plugin):
        """
        Constructor of the class.

        @type mail_queue_database_plugin: MailQueueDatabasePlugin
        @param mail_queue_database_plugin: The mail queue database plugin.
        """

        self.mail_queue_database_plugin = mail_queue_database_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: MailQueueDatabaseClient
        @return: The created client object.
        """

        # retrieves the entity manager arguments
        entity_manager_arguments = parameters.get("entity_manager_arguments", {})

        # creates the mail queue database client
        mail_queue_database_client = MailQueueDatabaseClient(self, entity_manager_arguments)

        # returns the mail queue database client
        return mail_queue_database_client












class MailQueueDatabaseClient:
    """
    The mail queue database client class.
    """

    mail_queue_database = None
    """ The mail queue database """

    entity_manager_arguments = None
    """ The entity manager arguments """

    message_access_lock = None
    """ The message access lock used to lock the message access """

    entity_manager = None
    """ The entity manager to be used to access the database """

    def __init__(self, mail_queue_database, entity_manager_arguments):
        """
        Constructor of the class.

        @type mail_queue_database: MailQueueDatabase
        @param MailQueueDatabase: The mail queue database.
        @type entity_manager_arguments: Dictionary
        @param entity_manager_arguments: The entity manager arguments.
        """

        self.mail_queue_database = mail_queue_database
        self.entity_manager_arguments = entity_manager_arguments

        self.message_access_lock = threading.Lock()

    def pop_message(self, name):

        # TENHO DE TER UM LOCK E TENHO DE O SACAR DA DB !!1
        # TENHO DE FAZER UNLOCK NUM FINANLLY !!!

        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # creates a transaction
        entity_manager.create_transaction()

        # acquires the message access lock
        self.message_access_lock.acquire()

        try:
            pass
        finally:
            # releases the message access lock
            self.message_access_lock.release()

#        try:
#            # retrieves the mailbox class
#            mailbox_class = entity_manager.get_entity_class("Mailbox")
#
#            # creates the new mailbox instance
#            mailbox = mailbox_class()
#
#            # sets the initial mailbox attributes
#            mailbox.name = name
#            mailbox.messages_count = 0
#            mailbox.messages_size = 0
#
#            # saves the mailbox
#            entity_manager.save(mailbox)
#        except:
#            # rolls back the transaction
#            entity_manager.rollback_transaction()
#
#            # re-throws the exception
#            raise
#        else:
#            # commits the transaction
#            entity_manager.commit_transaction()

#    def save_message(self, user, contents):
#        # retrieves the entity manager
#        entity_manager = self._get_entity_manager()
#
#        # creates a transaction
#        entity_manager.create_transaction()
#
#        try:
#            # retrieves the user's mailbox
#            mailbox = self.get_mailbox_name(user)
#
#            # in case no mailbox is found
#            if not mailbox:
#                # raises the invalid mailbox error
#                raise mail_queue_database_exceptions.InvalidMailboxError(user)
#
#            # retrieves the contents length
#            contents_length = len(contents)
#
#            # increments the number of messages in the mailbox
#            mailbox.messages_count += 1
#
#            # increments the mailbox size
#            mailbox.messages_size += contents_length
#
#            # sets the messages list as empty
#            mailbox.messages = []
#
#            # retrieves the message class
#            message_class = entity_manager.get_entity_class("Message")
#
#            # creates the new message instance
#            message = message_class()
#
#            # sets the message uid as a new one
#            message.uid = self._generate_uid()
#
#            # sets the contents size in the message
#            message.contents_size = contents_length
#
#            # retrieves the message contents class
#            message_contents_class = entity_manager.get_entity_class("MessageContents")
#
#            # creates the new message contents instance
#            message_contents = message_contents_class()
#
#            # sets the message contents size
#            message_contents.contents_size = contents_length
#
#            # sets the message contents data
#            message_contents.contents_data = contents
#
#            # sets the contents in the message
#            message.contents = message_contents
#
#            # sets the message mailbox
#            message.mailbox = mailbox
#
#            # updates the mailbox
#            entity_manager.update(mailbox)
#
#            # saves the message contents
#            entity_manager.save(message_contents)
#
#            # saves the message
#            entity_manager.save(message)
#        except:
#            # rolls back the transaction
#            entity_manager.rollback_transaction()
#
#            # re-throws the exception
#            raise
#        else:
#            # commits the transaction
#            entity_manager.commit_transaction()
#
#    def remove_message(self, uid):
#        """
#        Removes the message with the given uid.
#
#        @type uid: int
#        @param uid: The uid of the message to be removed.
#        """
#
#        # retrieves the entity manager
#        entity_manager = self._get_entity_manager()
#
#        # retrieves the message class
#        message_class = entity_manager.get_entity_class("Message")
#
#        # defines the find options for retrieving the messages
#        find_options = {FILTERS_VALUE : [{FILTER_TYPE_VALUE : "equals",
#                                          FILTER_FIELDS_VALUE : [{"field_name" : "uid",
#                                                                  "field_value" : uid}]}],
#                        EAGER_LOADING_RELATIONS_VALUE : {"mailbox" : {}, "contents" : {}}}
#
#        # retrieves the valid messages
#        messages = entity_manager._find_all_options(message_class, find_options)
#
#        # in case there are retrieved messages
#        if len(messages):
#            # retrieves the message from the list
#            # of messages
#            message = messages[0]
#
#            # creates a transaction
#            entity_manager.create_transaction()
#
#            try:
#                # retrieves the message mailbox
#                mailbox = message.mailbox
#
#                # retrieves the message contents
#                contents = message.contents
#
#                # retrieves the contents size
#                contents_size = message.contents_size
#
#                # decrements the number of messages in the mailbox
#                mailbox.messages_count -= 1
#
#                # decrements the mailbox size
#                mailbox.messages_size -= contents_size
#
#                # updates the mailbox
#                entity_manager.update(mailbox)
#
#                # removes the contents
#                entity_manager.remove(contents)
#
#                # removes the message
#                entity_manager.remove(message)
#            except:
#                # rolls back the transaction
#                entity_manager.rollback_transaction()
#
#                # re-throws the exception
#                raise
#            else:
#                # commits the transaction
#                entity_manager.commit_transaction()
#
#    def get_message_uid(self, uid):
#        """
#        Retrieves the message for the given uid.
#
#        @type uid: int
#        @param uid: The uid of the message to be retrieved.
#        @rtype: Message
#        @return: The retrieved message.
#        """
#
#        # retrieves the entity manager
#        entity_manager = self._get_entity_manager()
#
#        # retrieves the message class
#        message_class = entity_manager.get_entity_class("Message")
#
#        # defines the find options for retrieving the messages
#        find_options = {FILTERS_VALUE : [{FILTER_TYPE_VALUE : "equals",
#                                          FILTER_FIELDS_VALUE : [{"field_name" : "uid",
#                                                                  "field_value" : uid}]}],
#                        EAGER_LOADING_RELATIONS_VALUE : {"mailbox" : {}, "contents" : {}}}
#
#        # retrieves the valid messages
#        messages = entity_manager._find_all_options(message_class, find_options)
#
#        if len(messages):
#            return messages[0]
#
#    def get_mailbox_name(self, name):
#        """
#        Retrieves the mailbox for the given name.
#
#        @type name: String
#        @param name: The name of the mailbox to be retrieved.
#        @rtype: Mailbox
#        @requires: The retrieved mailbox.
#        """
#
#        # retrieves the entity manager
#        entity_manager = self._get_entity_manager()
#
#        # retrieves the mailbox class
#        mailbox_class = entity_manager.get_entity_class("Mailbox")
#
#        # defines the find options for retrieving the mailboxes
#        find_options = {FILTERS_VALUE : [{FILTER_TYPE_VALUE : "equals",
#                                          FILTER_FIELDS_VALUE : [{"field_name" : "name",
#                                                                  "field_value" : name}]}]}
#
#        # retrieves the valid mailboxes
#        mailboxes = entity_manager._find_all_options(mailbox_class, find_options)
#
#        if len(mailboxes):
#            return mailboxes[0]
#
#    def get_mailbox_messages_name(self, name):
#        """
#        Retrieves the mailbox (containing messages) for the given name.
#
#        @type name: String
#        @param name: The name of the mailbox to be retrieved.
#        @rtype: Mailbox
#        @requires: The retrieved mailbox (containing messages).
#        """
#
#        # retrieves the entity manager
#        entity_manager = self._get_entity_manager()
#
#        # retrieves the mailbox class
#        mailbox_class = entity_manager.get_entity_class("Mailbox")
#
#        # defines the find options for retrieving the mailboxes
#        find_options = {FILTERS_VALUE : [{FILTER_TYPE_VALUE : "equals",
#                                          FILTER_FIELDS_VALUE : [{"field_name" : "name",
#                                                                  "field_value" : name}]}],
#                        EAGER_LOADING_RELATIONS_VALUE : {"messages" : {}}}
#
#        # retrieves the valid mailboxes
#        mailboxes = entity_manager._find_all_options(mailbox_class, find_options)
#
#        if len(mailboxes):
#            return mailboxes[0]

    def get_mail_queue_database(self):
        """
        Retrieves the mail queue database.

        @rtype: MailQueueDatabase
        @return: The mail queue database.
        """

        return self.mail_queue_database

    def set_mail_queue_database(self, mail_queue_database):
        """
        Sets the mail queue database.

        @type mail_queue_database: MailQueueDatabase
        @param mail_queue_database: Tghe mail queue database.
        """

        self.mail_queue_database = mail_queue_database

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
        entity_manager_helper_plugin = self.mail_queue_database.mail_queue_database_plugin.entity_manager_helper_plugin

        # loads the entity manager for the entities module name
        self.entity_manager = entity_manager_helper_plugin.load_entity_manager(ENTITIES_MODULE_NAME, os.path.dirname(__file__), self.entity_manager_arguments)
