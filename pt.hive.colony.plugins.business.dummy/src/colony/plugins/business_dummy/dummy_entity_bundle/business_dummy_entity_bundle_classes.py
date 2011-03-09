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

__revision__ = "$LastChangedRevision: 7679 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 18:05:35 +0000 (qua, 24 Mar 2010) $"
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

class TestEntity(base_entity.EntityClass):

    id = {"id" : True, "data_type" : "numeric", "generated" : True, "generator_type" : "table", "table_generator_field_name" : "Test"}
    """ The id of the entity """

    object_value = {"data_type" : "text"}
    """ The object value of the entity """

    def __init__(self):
        self.id = None
        self.object_value = None

class DummyEntityBundleParent(base_entity.EntityClass):

    name = {"id" : True, "data_type" : "text"}
    """ The name of the entity """

    address = {"data_type" : "text"}
    """ The address of the entity """

    local_date = {"data_type" : "date"}
    """ The local date of the entity """

    mapping_options = {"inheritance_mapping": "table_per_class"}
    """ The object relational (o/r) options """

    def __init__(self):
        self.name = None
        self.address = None
        self.local_date = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_local_date(self):
        return self.local_date

    def set_local_date(self, local_date):
        self.local_date = local_date

class DummyEntityBundleAssociation(DummyEntityBundleParent):

    hair_type = {"data_type" : "text"}
    """ The hair type of the entity """

    entity_relation = {"data_type" : "relation"}
    """ The dummy entity relation """

    entity_to_many_relation = {"data_type" : "relation"}
    """  The dummy to many relation """

    entity_other_to_many_relation = {"data_type" : "relation", "fetch_type" : "lazy"}
    """  The dummy other to many relation """

    def __init__(self):
        DummyEntityBundleParent.__init__(self)
        self.hair_type = None
        self.entity_relation = []
        self.entity_to_many_relation = []
        self.entity_other_to_many_relation = []

    def get_hair_type(self):
        return self.hair_type

    def set_hair_type(self, hair_type):
        self.hair_type = hair_type

    @staticmethod
    def get_relation_attributes_entity_relation():
        return {"relation_type" : "one-to-many",
                "target_entity" : DummyEntityBundle,
                "join_attribute_name" : "entity_relation",
                "mapped_by" : DummyEntityBundle,
                "optional" : True}

    @staticmethod
    def get_relation_attributes_entity_to_many_relation():
        return {"relation_type" : "many-to-many",
                "target_entity" : DummyEntityBundle,
                "join_attribute_name" : "name",
                "attribute_column_name" : "dummy_entity_bundle_association_name",
                "join_attribute_column_name" : "dummy_entity_bundle_name",
                "join_table" : "DummyJoin"}

    @staticmethod
    def get_relation_attributes_entity_other_to_many_relation():
        return {"relation_type" : "many-to-many",
                "target_entity" : DummyEntityBundleNew,
                "join_attribute_name" : "name",
                "attribute_column_name" : "dummy_entity_bundle_association_name",
                "join_attribute_column_name" : "dummy_entity_bundle_new_name",
                "join_table" : "DummyOtherJoin"}

class DummyEntityBundle(DummyEntityBundleParent):

    age = {"data_type" : "numeric"}
    """ The age of the entity """

    entity_relation = {"data_type" : "relation"}
    """ The dummy entity relation """

    entity_to_many_relation = {"data_type" : "relation", "fetch_type" : "lazy"}
    """  The dummy to many relation """

    def __init__(self):
        DummyEntityBundleParent.__init__(self)
        self.age = None
        self.entity_relation = None
        self.entity_to_many_relation = []

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    @staticmethod
    def get_relation_attributes_entity_relation():
        return {"relation_type" : "many-to-one",
                "target_entity" : DummyEntityBundleAssociation,
                "join_attribute_name" : "name",
                "optional" : True}

    @staticmethod
    def get_relation_attributes_entity_to_many_relation():
        return {"relation_type" : "many-to-many",
                "target_entity" : DummyEntityBundleAssociation,
                "join_attribute_name" : "name",
                "attribute_column_name" : "dummy_entity_bundle_name",
                "join_attribute_column_name" : "dummy_entity_bundle_association_name",
                "join_table" : "DummyJoin"}

class DummyEntityBundleNew(DummyEntityBundleParent):

    entity_other_to_many_relation = {"data_type" : "relation", "fetch_type" : "lazy"}
    """  The dummy other to many relation """

    def __init__(self):
        DummyEntityBundleParent.__init__(self)
        self.entity_other_to_many_relation = []

    @staticmethod
    def get_relation_attributes_entity_other_to_many_relation():
        return {"relation_type" : "many-to-many",
                "target_entity" : DummyEntityBundleAssociation,
                "join_attribute_name" : "name",
                "attribute_column_name" : "dummy_entity_bundle_new_name",
                "join_attribute_column_name" : "dummy_entity_bundle_association_name",
                "join_table" : "DummyOtherJoin"}

ENTITY_CLASSES = [TestEntity, DummyEntityBundleParent, DummyEntityBundleAssociation, DummyEntityBundle, DummyEntityBundleNew]
""" The entity classes of the module """
