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

class Zone(RootEntity):
    """
    The zone class, representing the
    zone entity.
    """

    name = {"data_type" : "text"}
    """ The name of the zone """

    records = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The records of the zone """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = None
        self.records = []

    def get_name(self):
        """
        Retrieves the zone name.

        @rtype: String
        @return: The zone name.
        """

        return self.name

    @staticmethod
    def get_relation_attributes_records():
        return {"relation_type" : "one-to-many",
                "target_entity" : Record,
                "join_attribute_name" : "zone",
                "mapped_by" : Record,
                "optional" : True}

class Record(RootEntity):
    """
    The record class, representing the
    record entity.
    """

    name = {"data_type" : "text"}
    """ The name of the record """

    type = {"data_type" : "text"}
    """ The type of the record """

    class_ = {"data_type" : "text"}
    """ The class of the record """

    time_to_live = {"data_type" : "numeric"}
    """ The time to live of the record """

    value = {"data_type" : "text"}
    """ The value of the record """

    zone = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The zone that contains the record """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = None
        self.type = None
        self.class_ = None
        self.time_to_live = None
        self.value = None
        self.zone = None

    def get_name(self):
        """
        Retrieves the record name.

        @rtype: String
        @return: The record name.
        """

        return self.name

    def get_type(self):
        """
        Retrieves the record type.

        @rtype: String
        @return: The record type.
        """

        return self.type

    def get_class(self):
        """
        Retrieves the record class.

        @rtype: String
        @return: The record class.
        """

        return self.class_

    def get_time_to_live(self):
        """
        Retrieves the record time to live.

        @rtype: int
        @return: The record time to live.
        """

        return self.time_to_live

    def get_value(self):
        """
        Retrieves the record value.

        @rtype: String
        @return: The record value.
        """

        return self.value

    @staticmethod
    def get_relation_attributes_zone():
        return {"relation_type" : "many-to-one",
                "target_entity" : Zone,
                "join_attribute_name" : "object_id",
                "optional" : True}
