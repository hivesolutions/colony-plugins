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

    object_id = {"id" : True, "data_type" : "numeric", "generated" : True, "generator_type" : "table", "table_generator_field_name" : "RootEntity"}
    """ The object id of the comment """

    def __init__(self):
        self.object_id = None

class Mailbox(RootEntity):
    """
    The mailbox class, representing the
    mailbox entity.
    """

    name = {"data_type" : "text"}
    """ The name of the mailbox """

    messages_count = {"data_type" : "numeric"}
    """ The number of messages in the mailbox """

    messages_size = {"data_type" : "numeric"}
    """ The size of messages in the mailbox """

    messages = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The messages of the mailbox """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = None
        self.messages_count = None
        self.messages_size = None
        self.messages = []

    @staticmethod
    def get_relation_attributes_messages():
        return {"relation_type" : "one-to-many",
                "target_entity" : Message,
                "target_entity_name" : "Message",
                "join_attribute" : Message.mailbox,
                "join_attribute_name" : "mailbox",
                "mapped_by" : Message,
                "optional" : True}

class Message(RootEntity):
    """
    The message class, representing the
    message entity.
    """

    uid = {"data_type" : "text"}
    """ The unique identifier of the message """

    contents = {"data_type" : "text"}
    """ The contents of the message """

    mailbox = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The mailbox that contains the message """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.uid = None
        self.contents = None
        self.mailbox = None

    @staticmethod
    def get_relation_attributes_mailbox():
        return {"relation_type" : "many-to-one",
                "target_entity" : Mailbox,
                "target_entity_name" : "Mailbox",
                "join_attribute" : Mailbox.object_id,
                "join_attribute_name" : "object_id",
                "optional" : True}
