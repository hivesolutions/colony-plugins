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

class DummyEntityBundleParent:

    name = {"id" : True, "data_type" : "text"}
    """ The name of the entity """

    address = {"data_type" : "text"}
    """ The address of the entity """

    mapping_options = {"inheritance_mapping": "table_per_class"}
    #mapping_options = {"inheritance_mapping": "single_table"}
    """ The object relational (o/r) options """

    def __init__(self):
        self.name = None
        self.address = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_address(self):
        return self.address

    def set_address(self, name):
        self.address = address

class DummyEntityBundleAssociation(DummyEntityBundleParent):

    hair_type = {"data_type" : "text"}
    """ The hair type of the entity """

    entity_relation = {"data_type" : "relation"}
    """ The dummy entity relation """

    entity_to_many_relation = {"data_type" : "relation"}
    """  The dummy to many relation """

    def __init__(self):
        DummyEntityBundleParent.__init__(self)
        self.hair_type = None

    def get_hair_type(self):
        return self.hair_type

    def set_hair_type(self, hair_type):
        self.hair_type = hair_type

    @staticmethod
    def get_relation_attributes_entity_relation():
        return {"relation_type" : "one-to-many",
                "target_entity" : DummyEntityBundle,
                "target_entity_name" : "DummyEntityBundle",
                "join_attribute" : DummyEntityBundle.entity_relation,
                "join_attribute_name" : "entity_relation",
                "mapped_by" : DummyEntityBundle,
                "optional" : True}

    @staticmethod
    def get_relation_attributes_entity_to_many_relation():
        return {"relation_type" : "many-to-many",
                "maped_by_entity_attribute" : "entity_to_many_relation"}

class DummyEntityBundle(DummyEntityBundleParent):

    age = {"data_type" : "numeric"}
    """ The age of the entity """

    entity_relation = {"data_type" : "relation"}
    """ The dummy entity relation """

    entity_to_many_relation = {"data_type" : "relation"}
    """  The dummy to many relation """

    def __init__(self):
        DummyEntityBundleParent.__init__(self)
        self.age = None
        self.entity_relation = None
        self.entity_to_many_relation = None

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    @staticmethod
    def get_relation_attributes_entity_relation():
        return {"relation_type" : "one-to-one",
                "target_entity" : DummyEntityBundleAssociation,
                "target_entity_name" : "DummyEntityBundleAssociation",
                "join_attribute" : DummyEntityBundleAssociation.name,
                "join_attribute_name" : "name",
                "optional" : True}

    @staticmethod
    def get_relation_attributes_entity_to_many_relation():
        return {"relation_type" : "many-to-many",
                "target_entity" : DummyEntityBundleAssociation,
                "target_entity_name" : "DummyEntityBundleAssociation",
                "join_attribute" : DummyEntityBundleAssociation.name,
                "join_attribute_name" : "name",
                "join_table" : "test_join"}
