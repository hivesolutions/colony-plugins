#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import colony.libs.importer_util

BASE_ENTITY_MODULE_VALUE = "base_entity"
""" The base entity module value """

# imports the base entity classes
base_entity = colony.libs.importer_util.__importer__(BASE_ENTITY_MODULE_VALUE)

class RootEntity(base_entity.EntityClass):
    """
    The base root entity from which all the other
    entity models inherit.
    """

    object_id = {
        "id" : True,
        "data_type" : "numeric",
        "generated" : True,
        "generator_type" : "table",
        "table_generator_field_name" : "RootEntity"
    }
    """ The object id of the root entity """

    def __init__(self):
        self.object_id = None

class MailQueue(RootEntity):
    """
    The mail queue class, representing the
    mail queue entity.
    """

    name = {
        "data_type" : "text"
    }
    """ The name of the mail queue """

    messages_count = {
        "data_type" : "numeric"
    }
    """ The number of messages in the mail queue """

    messages_size = {
        "data_type" : "numeric"
    }
    """ The size of messages in the mail queue """

    first_message = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The first message of the mail queue """

    last_message = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The last message of the mail queue """

    messages = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The messages of the mail queue """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = None
        self.messages_count = None
        self.messages_size = None
        self.first_message = None
        self.last_message = None
        self.messages = []

    def get_name(self):
        """
        Retrieves the mail queue name.

        @rtype: String
        @return: The mail queue name.
        """

        return self.name

    def get_messages_count(self):
        """
        Retrieves the mail queue messages count.

        @rtype: int
        @return: The mail queue messages count.
        """

        return self.messages_count

    def get_messages_size(self):
        """
        Retrieves the mail queue messages size.

        @rtype: int
        @return: The mail queue messages size.
        """

        return self.messages_size

    def get_first_message(self):
        """
        Retrieves the mail queue first message.

        @rtype: Message
        @return: The mail queue first message.
        """

        return self.first_message

    def get_last_message(self):
        """
        Retrieves the mail queue last message.

        @rtype: Message
        @return: The mail queue last message.
        """

        return self.last_message

    def get_messages(self):
        """
        Retrieves the mail queue messages.

        @rtype: List
        @return: The mail queue messages.
        """

        return self.messages

    @staticmethod
    def get_relation_attributes_first_message():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : Message,
            "join_attribute_name" : "object_id",
            "optional" : True
        }

    @staticmethod
    def get_relation_attributes_last_message():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : Message,
            "join_attribute_name" : "object_id",
            "optional" : True
        }

    @staticmethod
    def get_relation_attributes_messages():
        return {
            "relation_type" : "one-to-many",
            "target_entity" : Message,
            "join_attribute_name" : "mail_queue",
            "mapped_by" : Message,
            "optional" : True
        }

class Message(RootEntity):
    """
    The message class, representing the
    message entity.
    """

    uid = {
        "data_type" : "text"
    }
    """ The unique identifier of the message """

    sender = {
        "data_type" : "text"
    }
    """ The sender of the message """

    contents_size = {
        "data_type" : "numeric"
    }
    """ The contents size of the message """

    contents = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The contents of the message """

    mail_queue_first = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The mail queue reference to the first item """

    mail_queue_last = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The mail queue reference to the last item """

    mail_queue = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The mail queue that contains the message """

    next_message = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The next message in the priority list """

    previous_message = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The previous message in the priority list """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.uid = None
        self.contents_size = None
        self.contents = None
        self.mail_queue_first = None
        self.mail_queue_last = None
        self.mail_queue = None
        self.next_message = None
        self.previous_message = None

    def get_uid(self):
        """
        Retrieves the message uid.

        @rtype: String
        @return: The message uid.
        """

        return self.uid

    def get_contents_size(self):
        """
        Retrieves the message contents size.

        @rtype: int
        @return: The message contents size.
        """

        return self.contents_size

    def get_contents(self):
        """
        Retrieves the message contents.

        @rtype: MessageContents
        @return: The message contents.
        """

        return self.contents

    def get_mail_queue_first(self):
        """
        Retrieves the message mail queue
        first reference.

        @rtype: MailQueue
        @return: The message mail queue
        first reference.
        """

        return self.mail_queue_first

    def get_mail_queue_last(self):
        """
        Retrieves the message mail queue
        last reference.

        @rtype: MailQueue
        @return: The message mail queue
        last reference.
        """

        return self.mail_queue_last

    def get_mail_queue(self):
        """
        Retrieves the message mail queue.

        @rtype: MailQueue
        @return: The message mail queue.
        """

        return self.mail_queue

    def get_next_message(self):
        """
        Retrieves the next message in queue.

        @rtype: Message
        @return: The next message in queue.
        """

        return self.next_message

    def get_previous_message(self):
        """
        Retrieves the previous message in queue.

        @rtype: Message
        @return: The previous message in queue.
        """

        return self.previous_message

    @staticmethod
    def get_relation_attributes_contents():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : MessageContents,
            "join_attribute_name" : "message",
            "mapped_by" : MessageContents,
            "optional" : True
        }

    @staticmethod
    def get_relation_attributes_mail_queue_first():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : MailQueue,
            "join_attribute_name" : "first_message",
            "mapped_by" : MailQueue,
            "optional" : True
        }

    @staticmethod
    def get_relation_attributes_mail_queue_last():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : MailQueue,
            "join_attribute_name" : "last_message",
            "mapped_by" : MailQueue,
            "optional" : True
        }

    @staticmethod
    def get_relation_attributes_mail_queue():
        return {
            "relation_type" : "many-to-one",
            "target_entity" : MailQueue,
            "join_attribute_name" : "object_id",
            "optional" : True
        }

    @staticmethod
    def get_relation_attributes_next_message():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : Message,
            "join_attribute_name" : "object_id",
            "optional" : True
        }

    @staticmethod
    def get_relation_attributes_previous_message():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : Message,
            "join_attribute_name" : "next_message",
            "mapped_by" : Message,
            "optional" : True
        }

class MessageContents(RootEntity):
    """
    The message contents class, representing the
    message contents entity.
    """

    contents_size = {
        "data_type" : "numeric"
    }
    """ The contents size of the message contents """

    contents_data = {
        "data_type" : "text"
    }
    """ The contents data of the message contents """

    message = {
        "data_type" : "relation",
        "fetch_type" : "lazy"
    }
    """ The contents data of the message contents """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.contents_size = None
        self.contents_data = None
        self.message = None

    def get_contents_size(self):
        """
        Retrieves the contents size.

        @rtype: int
        @return: The contents size.
        """

        return self.contents_size

    def get_contents_data(self):
        """
        Retrieves the contents data.

        @rtype: String
        @return: The contents data.
        """

        return self.contents_data

    def get_message(self):
        """
        Retrieves the contents message.

        @rtype: Message
        @return: The contents message.
        """

        return self.message

    @staticmethod
    def get_relation_attributes_message():
        return {
            "relation_type" : "one-to-one",
            "target_entity" : Message,
            "join_attribute_name" : "object_id",
            "optional" : True
        }
