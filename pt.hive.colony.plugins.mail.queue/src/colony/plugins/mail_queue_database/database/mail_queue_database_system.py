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
import time
import threading

import mail_queue_database_exceptions

ENTITIES_MODULE_NAME = "mail_queue_database_entities"
""" The entities module name """

EAGER_LOADING_RELATIONS_VALUE = "eager_loading_relations"
""" The eager loading relations value """

FILTERS_VALUE = "filters"
""" The filters value """

FILTER_TYPE_VALUE = "filter_type"
""" The filter type value """

FILTER_FIELDS_VALUE = "filter_fields"
""" The filter fields value """

UID_MULTIPLICATION_FACTOR = 1000
""" The uid multiplication factor """

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

    def create_mail_queue(self, name):
        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # creates a transaction
        entity_manager.create_transaction()

        try:
            # retrieves the mail queue class
            mail_queue_class = entity_manager.get_entity_class("MailQueue")

            # creates the new mail queue instance
            mail_queue = mail_queue_class()

            # sets the initial mail queue attributes
            mail_queue.name = name
            mail_queue.messages_count = 0
            mail_queue.messages_size = 0

            # saves the mail queue
            entity_manager.save(mail_queue)
        except:
            # rolls back the transaction
            entity_manager.rollback_transaction()

            # re-raises the exception
            raise
        else:
            # commits the transaction
            entity_manager.commit_transaction()

    def pop_message(self):
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

    def get_mail_queue_name(self, name):
        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # retrieves the mail queue class
        mail_queue_class = entity_manager.get_entity_class("MailQueue")

        # defines the find options for retrieving the mailboxes
        find_options = {
            FILTERS_VALUE : [
                {
                    FILTER_TYPE_VALUE : "equals",
                    FILTER_FIELDS_VALUE : (
                        {
                            "field_name" : "name",
                            "field_value" : name
                        },
                    )
                }
            ]
        }

        # retrieves the valid mail queues
        mail_queues = entity_manager._find_all_options(mail_queue_class, find_options)

        if len(mail_queues):
            return mail_queues[0]

    def get_mail_queue_messages_name(self, name):
        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # retrieves the mail queue class
        mail_queue_class = entity_manager.get_entity_class("MailQueue")

        # the options for the message relations
        message_options = {
            EAGER_LOADING_RELATIONS_VALUE : {
                "next_message" : {},
                "previous_message" : {}
            }
        }

        # defines the find options for retrieving the mailboxes
        find_options = {
            FILTERS_VALUE : (
                {
                    FILTER_TYPE_VALUE : "equals",
                    FILTER_FIELDS_VALUE : (
                        {
                            "field_name" : "name",
                            "field_value" : name
                        },
                    )
                },
            ),
            EAGER_LOADING_RELATIONS_VALUE : {
                "first_message" : message_options,
                "last_message" : message_options,
                "messages" : {}
            }
        }

        # retrieves the valid mail queues
        mail_queues = entity_manager._find_all_options(mail_queue_class, find_options)

        if len(mail_queues):
            return mail_queues[0]

    def peek_last_message(self, mail_queue_name):
        # retrieves the mail queue for the given name
        mail_queue = self.get_mail_queue_messages_name(mail_queue_name)

        # in case there is a valid mail queue
        # defined in the database
        if mail_queue:
            # retrieves the last message from the mail
            # queue
            last_message = mail_queue.get_last_message()

            # returns the last message
            return last_message

    def put_message(self, mail_queue_name, sender, recipients_list, contents):
        # acquires the message access lock
        self.message_access_lock.acquire()

        try:
            # retrieves the entity manager
            entity_manager = self._get_entity_manager()

            # creates a transaction
            entity_manager.create_transaction()

            try:
                # retrieves the mail queue
                mail_queue = self.get_mail_queue_messages_name(mail_queue_name)

                # in case the mail queue is not defined
                if not mail_queue:
                    # raises the invalid mail queue error
                    raise mail_queue_database_exceptions.InvalidMailQueueError(mail_queue_name)

                # retrieves the contents length
                contents_length = len(contents)

                # increments the number of messages in the mail queue
                mail_queue.messages_count += 1

                # increments the mail queue size
                mail_queue.messages_size += contents_length

                # tries to retrieve the last message
                last_message = self.peek_last_message(mail_queue_name)

                # retrieves the message class
                message_class = entity_manager.get_entity_class("Message")

                # creates the new message instance
                message = message_class()

                # sets the message uid as a new one
                message.uid = self._generate_uid()

                # sets the initial message attributes
                message.sender = sender
                message.contents_size = contents_length
                message.previous_message = last_message

                # retrieves the message contents class
                message_contents_class = entity_manager.get_entity_class("MessageContents")

                # creates the new message contents instance
                message_contents = message_contents_class()

                # sets the message contents size
                message_contents.contents_size = contents_length

                # sets the message contents data
                message_contents.contents_data = contents

                # sets the contents in the message
                message.contents = message_contents

                # in case the first message is not defined
                # this is the first message
                if not mail_queue.first_message:
                    # sets the current message as the
                    # first message, because it's the only message
                    mail_queue.first_message = message

                # sets the current message as the last message
                mail_queue.last_message = message

                # saves the message contents
                entity_manager.save(message_contents)

                # saves the message
                entity_manager.save(message)

                # updates the mail queue
                entity_manager.update(mail_queue)
            except:
                # rolls back the transaction
                entity_manager.rollback_transaction()

                # re-raises the exception
                raise
            else:
                # commits the transaction
                entity_manager.commit_transaction()
        finally:
            # releases the message access lock
            self.message_access_lock.release()

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

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments.

        @rtype: Dictionary
        @return: The entity manager arguments.
        """

        return self.entity_manager_arguments

    def set_entity_manager_arguments(self, entity_manager_arguments):
        """
        Sets the entity manager arguments.

        @type entity_manager_arguments: Dictionary
        @param entity_manager_arguments: The entity manager arguments.
        """

        self.entity_manager_arguments = entity_manager_arguments

    def _generate_uid(self):
        """
        Generates a new uid.

        @rtype: int
        @return: The generated uid.
        """

        # retrieves the current time
        current_time = time.time()

        # creates the unique identifier
        uid = str(int(current_time * UID_MULTIPLICATION_FACTOR))

        # returns the generated uid (unique identifier)
        return uid

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
