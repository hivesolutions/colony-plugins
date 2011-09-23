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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import datetime

import colony.libs.string_util

PERSIST_UPDATE_TYPE = 0x01
""" The persist only on update (or save) persist type """

PERSIST_SAVE_TYPE = 0x02
""" The persist only on save persist type """

PERSIST_ASSOCIATE_TYPE = 0x04
""" The persist associate persist type """

PERSIST_ALL_TYPE = PERSIST_UPDATE_TYPE | PERSIST_SAVE_TYPE | PERSIST_ASSOCIATE_TYPE
""" The persist all persist type """

SAVED_STATE_VALUE = 1
""" The saved state value """

UPDATED_STATE_VALUE = 2
""" The updated state value """

REMOVED_STATE_VALUE = 3
""" The removed state value """

DATA_SATE_VALUE = "data_state"
""" The data state value """

RELATION_VALUE = "relation"
""" The relation value """

DATE_VALUE = "date"
""" The date value """

PLURALIZATION_SUFFIX_VALUE = "s"
""" The pluralization suffix value """

TO_ONE_RELATIONS = (
    "one-to-one",
    "many-to-one"
)
""" The tuple containing the "to-one" relations """

TO_MANY_RELATIONS = (
    "one-to-many",
    "many-to-many"
)
""" The tuple containing the "to-many" relations """

def save(self, entity_manager = None):
    """
    Saves the current instance into the data source
    described in the current entity manager.
    This method provides the persistence layer for
    creating an object.

    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # saves the entity using the entity manager
    entity_manager.save(self)

def update(self, entity_manager = None):
    """
    Updates the current instance in the data source
    described in the current entity manager.
    This method provides the persistence layer for
    updating an object.

    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # updates the entity using the entity manager
    entity_manager.update(self)

def remove(self, entity_manager = None):
    """
    Removes the current instance from the data source
    described in the current entity manager.
    This method provides the persistence layer for
    removing an object.

    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # removes the entity using the entity manager
    entity_manager.remove(self)

def save_update(self, entity_manager = None):
    """
    Saves or updates the current instance into the data source
    described in the current entity manager.
    This method provides the persistence layer for
    creating an object.

    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # saves or updates the entity using the entity manager
    entity_manager.save_update(self)

def persist(self, persist_type, entity_manager = None):
    """
    Persists the current instance into the data source
    described in the current entity manager.
    The persist method take into account the persist type
    in order to provide an additional layer of security.
    This method provides the persistence layer for
    creating an object.

    @type persist_type: int
    @param persist_type: The type of persist to be used
    in the entity.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # checks if the entity is persisted
    is_persisted = self.is_persisted()

    # in case the entity is persisted and the persist
    # type allows updating
    if is_persisted and persist_type & PERSIST_UPDATE_TYPE:
        # updates the entity using the entity manager
        entity_manager.update(self)
    # in case the entity is not persisted and the persist
    # type allows saving
    elif not is_persisted and persist_type & PERSIST_SAVE_TYPE:
        # saves the entity using the entity manager
        entity_manager.save(self)

def is_saved(self):
    # in case the current entity model
    # does not contain the data state value
    if not hasattr(self, DATA_SATE_VALUE):
        # returns false
        return False

    # checks if the current data state
    # is saved (value)
    saved = self._data_state_ == SAVED_STATE_VALUE

    # returns the saved value
    return saved

def is_persisted(self, entity_manager = None):
    """
    Checks the internal structure of the entity
    to guess if the entity  model is persisted.
    The heuristic involves checking the id attribute
    of the entity is already defined.
    This method should be used carefully because
    it assumes the entity id is generated automatically
    on the first save.

    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # retrieves the id attribute value
    id_attribute_value = entity_manager.get_entity_id_attribute_value(self)

    # checks if the id attribute value is not none (persisted)
    persisted = not id_attribute_value == None

    # returns the persisted value
    return persisted

def lock(self, entity_manager = None):
    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # retrieves the class of the current object
    entity_class = self.__class__

    # retrieves the id attribute value
    id_attribute_value = self.get_id_attribute_value()

    # locks the entity with the given attribute
    entity_manager.lock(entity_class, id_attribute_value)

def get_id_attribute_name(self, entity_manager = None):
    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # retrieves the class of the current object
    entity_class = self.__class__

    # retrieves the id attribute name from the current object
    id_attribute_name = entity_manager.get_entity_class_id_attribute_name(entity_class)

    # returns the id attribute name
    return id_attribute_name

def get_id_attribute_value(self, entity_manager = None):
    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # retrieves the id attribute value from the current object
    id_attribute_value = entity_manager.get_entity_id_attribute_value(self)

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
    """
    Converts the name of the current entity instance
    class to a pluralized form.
    This method is a utility for this common task.

    @rtype: String
    @return: The entity class name in pluralized form.
    """

    # retrieves the class of the current object
    entity_class = self.__class__

    # retrieves the entity class name
    entity_class_name = entity_class.__name__

    # lower cased entity class name
    lower_cased_entity_class_name = colony.libs.string_util.convert_underscore(entity_class_name)

    # pluralizes the entity class name
    controller_path = lower_cased_entity_class_name + PLURALIZATION_SUFFIX_VALUE

    # returns the controller path
    return controller_path

def _load_value(self, key, value):
    """
    Loads the value with the given key in the
    current object.
    This method loads the value taking into account
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

    # retrieves the value data type
    value_data_type = class_value.get("data_type", None)

    # in case the data type of the field is relation (presence of an object relation)
    if value_data_type == RELATION_VALUE:
        # retrieves the value type
        value_type = type(value)

        # retrieves the relation information method
        relation_method = getattr(entity_class, "get_relation_attributes_" + key)

        # calls the relation information method to retrieve the relation attributes
        relation_attributes = relation_method()

        # retrieves the relation type
        relation_type = relation_attributes.get("relation_type", None)

        # retrieves the target entity
        target_entity = relation_attributes.get("target_entity", object)

        # in case the relation is of type "to-one"
        if relation_type in TO_ONE_RELATIONS:
            # in case the value is of type dictionary
            # (to-one relations require list representation)
            if value_type == types.DictType:
                # creates a new target entity instance
                target_entity_instance = target_entity()

                # iterates over all the value items
                # to set the target entity instance values
                for value_key, value_value in value.items():
                    # loads the value in the target entity instance
                    target_entity_instance._load_value(value_key, value_value)
            else:
                # sets the target entity instance as "invalid"
                target_entity_instance = None

            # sets the target entity instance in the current object
            setattr(self, key, target_entity_instance)

        # in case the relation is of type "to-many"
        elif relation_type in TO_MANY_RELATIONS:
            # creates the entity instances list
            entity_instances_list = []

            # in case the value type is a list
            # (to-many relations require list representation)
            if value_type == types.ListType:
                # iterates over all the values to process them
                for value_item in value:
                    # retrieves the value item type
                    value_item_type = type(value_item)

                    # in case the type of the value item is
                    # not dictionary (not valid)
                    if not value_item_type == types.DictType:
                        # continues the loop
                        continue

                    # creates a new target entity instance
                    target_entity_instance = target_entity()

                    # iterates over all the value items
                    # to set the target entity instance values
                    for value_key, value_value in value_item.items():
                        # loads the value in the target entity instance
                        target_entity_instance._load_value(value_key, value_value)

                    # adds the target entity instance
                    # to the entity instances list
                    entity_instances_list.append(target_entity_instance)

            # sets the entity instances list in the current object
            setattr(self, key, entity_instances_list)
    # in case its a date attribute (requires conversion)
    elif value_data_type == DATE_VALUE:
        # in case there is a valid value defined
        if value:
            # retrieves the date value from the value (timestamp)
            date_value = datetime.datetime.utcfromtimestamp(float(value))
        else:
            # sets an invalid date value
            date_value = None

        # sets the date value in the current object
        setattr(self, key, date_value)
    # in case it's a "normal" attribute
    else:
        # sets the value in the current object
        setattr(self, key, value)
