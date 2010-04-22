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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types

PLURALIZATION_SUFFIX_VALUE = "s"
""" The pluralization suffix value """

def save(self):
    # saves the entity using the entity manager
    self._entity_manager.save(self)

def update(self):
    # updates the entity using the entity manager
    self._entity_manager.update(self)

def remove(self):
    # removes the entity using the entity manager
    self._entity_manager.remove(self)

def get_id_attribute_value(self):
    # retrieves the id attribute value from the current object
    id_attribute_value = getattr(self, self.id_attribute_name)

    # returns the id attribute value
    return id_attribute_value

def get_resource_path(self):
    # retrieves the id attribute value
    id_attribute_value = self.get_id_attribute_value()

    # retrieves the controller path for the current object
    entity_class_pluralized = self._get_entity_class_pluralized()

    # retrieves the entity id attribute value,
    # and converts it to string
    id_attribute_value_string = str(id_attribute_value)

    # creates and returns the target request
    return entity_class_pluralized + "/" + id_attribute_value_string

def _get_entity_class_pluralized(self):
    # retrieves the class of the current object
    entity_class = self.__class__

    # retrieves the entity class name
    entity_class_name = entity_class.__name__

    # lower cased entity class name
    lower_cased_entity_class_name = entity_class_name.lower()

    # pluralizes the entity class name
    controller_path = lower_cased_entity_class_name + PLURALIZATION_SUFFIX_VALUE

    # returns the controller path
    return controller_path

def _load_value(self, key, value):
    """
    Loads the value with the given key in the
    current object.
    The method loads the value taking into account
    the meta information provided by the entity manager.

    @type key: String
    @param key: The key to be used to refer to the value
    in the current object.
    @type value: Object
    @param value: The value to be set in the current object.
    """

    # in case the current object does not contain
    # an attribute with the key name
    if not hasattr(self, key):
        # returns immediately
        return

    # retrieves the entity class for the current object
    entity_class = self.__class__

    # in case the entity class does not contain an
    # attribute with the key name
    if not hasattr(entity_class, key):
        # returns immediately
        return

    # retrieves the class value
    class_value = getattr(entity_class, key)

    # retrieves the class value type
    class_value_type = type(class_value)

    # in case the class value type is not
    # dictionary
    if not class_value_type == types.DictType:
        # returns immediately
        return

    # retrieves the value type
    value_type = type(value)

    if class_value_type == types.DictType and class_value.get("data_type", None) == "relation":
        relation_method = getattr(entity_class, "get_relation_attributes_" + key)

        relation_attributes = relation_method()

        relation_type = relation_attributes.get("relation_type", "one-to-one")

        target_entity = relation_attributes.get("target_entity", object)

        if relation_type in ("one-to-one", "many-to-one"):
            if value_type == types.DictType:
                # creates a new target entity instance
                target_entity_instance = target_entity()

                for value_key, value_value in value.items():
                    target_entity_instance._load_value(value_key, value_value)
            else:
                target_entity_instance = None

            # sets the target entity instance in the current object
            setattr(self, key, target_entity_instance)

        elif relation_type in ("one-to-many", "many-to-many"):
            # creates the instances list
            instances_list = []

            if value_type == types.ListType:
                for value_item in value:
                    value_item_type = type(value_item)

                    if not value_item_type == types.DictType:
                        continue

                    # creates a new target entity instance
                    target_entity_instance = target_entity()

                    for value_key, value_value in value_item.items():
                        target_entity_instance._load_value(value_key, value_value)

                    # adds the target entity instance
                    # to the instances list
                    instances_list.append(target_entity_instance)

            # sets the instances list in the current object
            setattr(self, key, instances_list)
    else:
        # sets the value in the current object
        setattr(self, key, value)
