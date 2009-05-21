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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class FirstEntity(EntityClass):
    """
    The first entity entity.
    """

    object_id = {"id" : True, "data_type" : "numeric", "generated" : True, "generator_type" : "table", "table_generator_field_name" : "TestEntity"}
    """ The object id of the root entity """

    attribute = {"data_type" : "numeric"}
    """ The attribute's label """

    second_entity = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The second entity this entity is associated with """

    second_entities = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The second entities this entity is associated with """

    def __init__(self):
        """
        Constructor of the class.
         """

        EntityClass.__init__(self)
        self.object_id = None
        self.attribute = None
        self.second_entity = None
        self.second_entities = []

    @staticmethod
    def get_relation_attributes_second_entity():
        return {"relation_type" : "one-to-one",
                "target_entity" : SecondEntity,
                "target_entity_name" : "SecondEntity",
                "join_attribute" : SecondEntity.first_entity,
                "join_attribute_name" : "first_entity",
                "mapped_by" : SecondEntity,
                "optional" : True}

    @staticmethod
    def get_relation_attributes_second_entities():
        return {"relation_type" : "many-to-many",
                "target_entity" : SecondEntity,
                "target_entity_name" : "SecondEntity",
                "join_attribute" : SecondEntity.object_id,
                "join_attribute_name" : "object_id",
                "attribute_column_name" : "first_entity_object_id",
                "join_attribute_column_name" : "second_entity_object_id",
                "join_table" : "FirstEntitySecondEntityRelation"}

class SecondEntity(EntityClass):
    """
    The second entity entity.
    """

    object_id = {"id" : True, "data_type" : "numeric", "generated" : True, "generator_type" : "table", "table_generator_field_name" : "TestEntity"}
    """ The object id of the root entity """

    attribute = {"data_type" : "numeric"}
    """ The attribute's label """

    first_entity = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The first entity this entity is associated with """

    first_entities = {"data_type" : "relation", "fetch_type" : "lazy"}
    """ The first entities this entity is associated with """

    def __init__(self):
        """
        Constructor of the class.
         """

        EntityClass.__init__(self)
        self.object_id = None
        self.attribute = None
        self.first_entity = None
        self.first_entities = []

    @staticmethod
    def get_relation_attributes_first_entity():
        return {"relation_type" : "one-to-one",
                "target_entity" : FirstEntity,
                "target_entity_name" : "FirstEntity",
                "join_attribute" : FirstEntity.object_id,
                "join_attribute_name" : "object_id",
                "optional" : True}

    @staticmethod
    def get_relation_attributes_first_entities():
        return {"relation_type" : "many-to-many",
                "target_entity" : FirstEntity,
                "target_entity_name" : "FirstEntity",
                "join_attribute" : FirstEntity.object_id,
                "join_attribute_name" : "object_id",
                "attribute_column_name" : "second_entity_object_id",
                "join_attribute_column_name" : "first_entity_object_id",
                "join_table" : "FirstEntitySecondEntityRelation"}
