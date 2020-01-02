#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import copy
import types
import calendar
import datetime
import threading

import colony

from . import exceptions

SERIALIZERS = (
    "json",
    "pickle"
)
""" The list to hold the various serializers
in order of preference for serialization """

SERIALIZERS_MAP = None
""" The map associating the encoding type for
the serialization with the appropriate serializer
object to handle it """

SAFE_CHARACTER = "_"
""" The character to be used in table names as the prefix that
provides safety to the creation of them (no reserved names) """

RESERVED_NAMES = ("_class", "_mtime")
""" The tuple containing the names that are considered to be
reserved (special cases) for the queries """

PYTHON_TYPES_MAP = dict(
    text = (
        str,
        colony.legacy.UNICODE,
        type(None)
    ),
    string = (
        str,
        colony.legacy.UNICODE,
        type(None)
    ),
    integer = (
        int,
        colony.legacy.LONG,
        type(None)
    ),
    float = (
        int,
        colony.legacy.LONG,
        float,
        type(None)
    ),
    decimal = (
        int,
        colony.legacy.LONG,
        float,
        colony.Decimal,
        type(None)
    ),
    date = (
        datetime.datetime,
        int,
        colony.legacy.LONG,
        float,
        type(None)
    ),
    data = (
        str,
        colony.legacy.UNICODE,
        type(None)
    ),
    metadata = (
        dict,
        str,
        colony.legacy.UNICODE,
        type(None)
    )
)
""" The map containing the association between the entity
types and the valid values for python types """

PYTHON_WARN_MAP = dict(
    decimal = (
        float,
    )
)
""" Map that associates the various entity based types with
the types that should trigger a warning because although
compatible may create serious compatibility/integrity issues """

PYTHON_CAST_MAP = dict(
    text = colony.legacy.UNICODE,
    string = colony.legacy.UNICODE,
    integer = int,
    float = float,
    decimal = colony.Decimal,
    date = float,
    data = colony.legacy.UNICODE,
    metadata = dict,
    relation = None
)
""" The map containing the association between the entity
type and the best cast type for the value """

INVALID_NAMES = set((
    "__module__",
    "__doc__",
    "_system_instance",
    "_entity_manager",
    "_resources_path",
    "_entities",
    "_class",
    "_scope",
    "_attached",
    "_attach_level",
    "_names",
    "_items",
    "_generated",
    "_indexed",
    "_mandatory",
    "_immutable",
    "_relations",
    "_mapped_relations",
    "_unmapped_relations",
    "_direct_relations",
    "_indirect_relations",
    "_to_one",
    "_to_many",
    "_id",
    "_parents",
    "_abstract_parents",
    "_attr_methods",
    "_items_map",
    "_names_map",
    "_generated_map",
    "_indexed_map",
    "_mandatory_map",
    "_immutable_map",
    "_relations_map",
    "_direct_relations_map",
    "_indirect_relations_map",
    "_to_one_map",
    "_to_many_map",
    "_all_attr_methods",
    "_all_relations",
    "_all_parents",
    "_all_abstract_parents",
    "_non_foreign_items",
    "_parameters",
    "_storing",
    "_validating",
    "_has_parents",
    "abstract",
    "data_state",
    "data_reference",
    "mapping_options",
    "id_attribute_name"
))
""" The tuple containing all the names that are
considered to be invalid for the entity model """

class Connection(object):
    """
    The connection class representing the global
    and abstract connection to be consumed by
    the underlying engine layer.

    This connection should be the repository to
    all the information of an abstract connection.
    """

    closed = False
    """ The flag controlling the status (closing) of the connection,
    meaning that if it's set the connection is considered closed """

    connection_parameters = {}
    """ The general parameters to be used in the connection,
    this value may be unset in case no "special" configuration
    is set for the connection to be created """

    commit_handlers = []
    """ The list of handlers to be called upon the (next) commit,
    these handlers are only called upon the concrete operation is
    completed successfully """

    rollback_handlers = []
    """ The list of handlers to be called upon the (next) rollback
    these handlers are only called upon the concrete operation is
    completed successfully """

    handlers_lock = None
    """ The lock that controls the access to the calling of the
    handlers this lock ensures sequence in the calling """

    def __init__(self, connection_parameters = {}):
        """
        Constructor of the class.

        :type connection_parameters: Dictionary
        :param connection_parameters: The parameters to be used
        during the connection scope.
        """

        self.connection_parameters = connection_parameters

        self.commit_handlers = []
        self.rollback_handlers = []
        self.handlers_lock = threading.RLock()

    def open(self):
        """
        Opens the connection, setting the appropriate values
        in the connection internal structures.
        """

        self.closed = False

    def close(self):
        """
        Closes the connection, setting the appropriate values
        in the connection internal structures.
        """

        self.closed = True

    def is_closed(self):
        """
        Checks if the current connection is closed or
        if it's open, this is important for correct
        query execution handling.

        :rtype: bool
        :return: If the current connection is connected or
        disconnected.
        """

        return self.closed

    def add_commit_handler(self, commit_handler, one_time = False):
        """
        Adds a commit handler to be called upon commit
        to the current connection.

        This handler is only going to be called at the
        end of the concrete commit operation.

        :type commit_handler: Function
        :param commit_handler: The handler to be called
        upon the next commit in the current connection.
        :type one_time: bool
        :param one_time: If the handler is only to be called
        for the next commit or if should be called recursively.
        """

        # creates the tuple holding the commit handler
        # and the one time flag and adds it to the list
        # containing the commit handlers
        commit_handler_tuple = (commit_handler, one_time)
        self.commit_handlers.append(commit_handler_tuple)

    def add_rollback_handler(self, rollback_handler, one_time = False):
        """
        Adds a commit handler to be called upon rollback
        to the current connection.

        This handler is only going to be called at the
        end of the concrete rollback operation.

        :type rollback_handler: Function
        :param rollback_handler: The handler to be called
        upon the next rollback in the current connection.
        :type one_time: bool
        :param one_time: If the handler is only to be called
        for the next rollback or if should be called recursively.
        """

        # creates the tuple holding the rollback handler
        # and the one time flag and adds it to the list
        # containing the rollback handlers
        rollback_handler_tuple = (rollback_handler, one_time)
        self.rollback_handlers.append(rollback_handler_tuple)

    def reset_handlers(self):
        """
        Resets the list of handlers, for both the commit
        and rollback operations.

        This reseting should occur after the current operation
        is completed, with or without success.
        """

        # resets both the commit and the rollback
        # handlers list, to the original empty value
        self.commit_handlers = []
        self.rollback_handlers = []

    def call_commit_handlers(self):
        """
        Calls all the commit handlers, currently present
        in the connection.

        The calling of the commit handlers should only occur
        in the concrete commit of the operation in the data
        source nested transactions should be ignored.

        This operation is considered to be thread safe (as it
        is protected by a lock object).
        """

        # acquires the handlers lock so that only one thread
        # access the calling of the handlers at one time
        self.handlers_lock.acquire()

        try:
            # creates the list to be used to gather the commit
            # handlers to be removed because of the one time flag
            removal_list = []

            # iterates over all the commit handlers in the
            # current connection
            for commit_handler_tuple in self.commit_handlers:
                # unpacks the commit handler tuple into the
                # commit handler itself and the one time control
                # flag (controls if multiple commits must occur)
                commit_handler, one_time = commit_handler_tuple

                # calls the commit handler for the current
                # connection and then in case the one time flag
                # is set adds the commit handler tuple to the
                # proper removal list
                commit_handler(self)
                one_time and removal_list.append(commit_handler_tuple)

            # removes all the elements currently present in the
            # removal list (items pending removal)
            for removal_item in removal_list: self.commit_handlers.remove(removal_item)
        finally:
            # releases the handlers lock (avoids leaking
            # of the lock, causing a dead lock)
            self.handlers_lock.release()

    def call_rollback_handlers(self):
        """
        Calls all the rollback handlers, currently present
        in the connection.

        The calling of the rollback handlers should only occur
        in the concrete "rollbacking" of the operation in the
        data source nested transactions should be ignored.

        This operation is considered to be thread safe (as it
        is protected by a lock object).
        """

        # acquires the handlers lock so that only one thread
        # access the calling of the handlers at one time
        self.handlers_lock.acquire()

        try:
            # creates the list to be used to gather the commit
            # handlers to be removed because of the one time flag
            removal_list = []

            # iterates over all the rollback handlers in the
            # current connection
            for rollback_handler_tuple in self.rollback_handlers:
                # unpacks the rollback handler tuple into the
                # rollback handler itself and the one time control
                # flag (controls if multiple rollbacks must occur)
                rollback_handler, one_time = rollback_handler_tuple

                # calls the rollback handler for the current
                # connection and then in case the one time flag
                # is set adds the rollback handler tuple to the
                # proper removal list
                rollback_handler(self)
                one_time and removal_list.append(rollback_handler_tuple)

            # removes all the elements currently present in the
            # removal list (items pending removal)
            for removal_item in removal_list: self.rollback_handlers.remove(removal_item)
        finally:
            # releases the handlers lock (avoids leaking
            # of the lock, causing a dead lock)
            self.handlers_lock.release()

class EntityClass(object):
    """
    The base entity class used for the entity manager.
    This entity contains all the base infra-structure
    to be used during the process of the entity logic
    in the entity manager.
    """

    data_state = None
    """ The state of the current data information, in
    case the value is not set the entity did not suffer
    any of the changing operations (save, update or delete) """

    _entity_manager = None
    """ The entity manager reference to be used for lazy
    operations """

    _entities = None
    """ The map containing the various entity classes associated
    with their current diffusion scope references (this map is going
    to be used as cache) """

    _scope = None
    """ The map containing the various diffusion scope related
    parameters, lazy attaching and other properties, this map
    should be shared around all the elements of the diffusion scope """

    _attached = True
    """ Flag that controls if the current entity is attached to
    the data source, in case the entity is attached it can retrieve
    data from it otherwise it's considered "off-line" """

    _attach_level = 0
    """ The current "depth" level of attachment in case the value is
    zero or less the entity is considered detached otherwise the entity
    is considered attached (on-line) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self._entities = {}
        self._scope = {}

    def __new__(cls, *args, **kwargs):
        # creates the new instance using the default
        # object "instancing" strategy
        self = object.__new__(cls)

        # calls the underlying start method that
        # must create and start the most basic
        # entity structures, even on bulk operation
        # these structures must be created
        self._start()

        # returns the created instance to the virtual
        # machine control
        return self

    def __getattribute__(self, name):
        # tries to retrieve the "concrete" value for the requested
        # attribute using the parent retrieval method, in case it
        # fails an extra retrieval is done using the (calculated)
        # attributes strategy, so that extra delay resolution is
        # possible according to the currently defined strategy
        try: value = object.__getattribute__(self, name)
        except AttributeError: value = self._try_attr(name)

        # gathers the proper data type of the value that it's going
        # to be used for some of the runtime evaluation strategies
        value_type = type(value)

        # in case the value is not a dictionary, it's not
        # a lazy loaded relation description (that's for sure)
        if not value_type == dict: return value

        # extracts the parent class reference of the current
        # instance as it's going to be used through the various
        # processing lines of the current method
        cls = self.__class__

        # checks if the value for the attribute name in the class
        # does not exists or is not the same as the retrieved value,
        # this test ensures that this is not a class level description
        # of an entity attribute (it's a concrete value instead)
        if not hasattr(cls, name): return value
        if not getattr(cls, name) == value: return value

        # checks if the current attribute name refers a relation
        # so that options on how to lazy load it can be defined
        is_relation = cls.is_relation(name)

        # loads the lazy loaded relation with the provided
        # name, this will trigger an access to the data
        # source (slow operation) or loads the lazy loaded
        # attribute using (a concrete class load approach)
        attribute = self._load_lazy(name) if is_relation else self._load_lazy_attr(name)

        # returns the retrieved/loaded (lazy) attribute, ready
        # to be used by the calling method, note that this value
        # may not be loaded in case it's not currently possible
        return attribute

    def __getstate__(self, depth = None, detach = True):
        depth = depth or self._depth() or 0
        is_attached = self.is_attached()
        detach and is_attached and self.detach()
        try: state = self.to_map(depth = depth)
        finally: detach and is_attached and self.attach()
        return state

    def __setstate__(self, state):
        cls = self.__class__
        cls.from_map(state, self._entity_manager, entity = self)

    @classmethod
    def build(cls, entity_manager = None, entities = None, scope = None):
        """
        Creates a new instance of the current class, without
        calling the constructor and without initializing the
        structures.

        This class method is useful for situations where the
        default values of the entity model are not wanted.

        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to be used
        for reference in the newly created instance. By default
        the class level entity manager reference is used.
        :type entities: Dictionary
        :param entities: The map containing the various loaded
        entities indexed by class type, this is the cache map
        that may be used for fast access.
        :type scope: Dictionary
        :param scope: The (diffusion) scope parameters that
        should control a series of diffusion related functions.
        :rtype: Entity
        :return: The create instance of he entity model.
        """

        # creates a new instance of the current class,
        # without calling the constructor, then sets the
        # entity manager and the entities (map) in the
        # "newly" created instance
        self = cls.__new__(cls)
        self._entity_manager = entity_manager or self._entity_manager
        self._entities = entities
        self._scope = scope

        # creates the required maps for the entities and
        # for the scope in case they are required (none
        # of them is provided as argument for the method)
        if self._entities == None: self._entities = {}
        if self._scope == None: self._scope = {}

        # return the created/generated instance
        return self

    @classmethod
    def get_name(cls, safe_character = SAFE_CHARACTER):
        """
        Retrieves the name of the associated entity/table reference
        for the current model class.

        The conversion process should be quite simple and "fast".

        :type safe_character: String
        :param safe_character: The safe character that is going to be used as
        a prefix for the generation of the "table" name.
        :rtype: String
        :return: The name of the associated entity/table reference
        for the current model class.
        """

        safe_character = safe_character or ""
        return safe_character + colony.to_underscore(cls.__name__)

    @classmethod
    def get_plain_name(cls):
        return cls.get_name(safe_character = None)

    @classmethod
    def get_attr_methods(cls):
        # in case the attr methods are already "cached" in the current
        # class (fast retrieval)
        if "_attr_methods" in cls.__dict__:
            # returns the cached attr methods from the entity
            # class object reference
            return cls._attr_methods

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the map to hold the attr methods
        # in the current class context
        attr_methods = {}

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # attr method attribute, sets the appropriate ones in
        # the attr methods map (meta information)
        for key, value in colony.legacy.iteritems(items):
            # in case the current key does not start with the
            # attr method prefix
            if not key.startswith("_attr_"): continue

            # in case the type is a function or a method it
            # should be ignored (not a name)
            if not type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # retrieves the name of the attribute associated with
            # the attr method and sets the current value in the attr
            # methods map for the name
            name = key[6:]
            attr_methods[name] = cls

        # caches the attr methods element in the class
        # to provide fast access in latter access
        cls._attr_methods = attr_methods

        # returns the map that contains the attr methods
        # from the current class level
        return attr_methods

    @classmethod
    def get_all_attr_methods(cls):
        # in case the all attr methods are already "cached" in
        # the current class (fast retrieval)
        if "_all_attr_methods" in cls.__dict__:
            # returns the cached all attr methods from the entity
            # class object reference
            return cls._all_attr_methods

        # creates the map to hold the complete set of
        # attr methods from the class structure
        all_attr_methods = {}

        # retrieves the attr methods present at the current
        # entity class level, for recursive iteration
        attr_methods = cls.get_attr_methods()

        # retrieves the parent entity classes from
        # the current class
        parents = cls.get_parents()

        # iterates over all the parents to extend the all
        # attr methods with the parent attr methods
        for parent in parents:
            # retrieves the (all) attr methods from the parents
            # and extends the all attr methods map with them
            _attr_methods = parent.get_all_attr_methods()
            colony.map_extend(
                all_attr_methods,
                _attr_methods,
                copy_base_map = False
            )

        # extends the all attr methods map with the attr methods
        # from the current entity class
        colony.map_extend(all_attr_methods, attr_methods, copy_base_map = False)

        # caches the all attr methods element in the class
        # to provide fast access in latter access
        cls._all_attr_methods = all_attr_methods

        # returns the map that contains all the attr methods
        # from all the parent entity classes
        return all_attr_methods

    @classmethod
    def get_items_map(cls):
        # in case the items map are already "cached" in the current
        # class (fast retrieval)
        if "_items_map" in cls.__dict__:
            # returns the cached items map from the entity
            # class object reference
            return cls._items_map

        # retrieves the parents for the entity
        # class, to check them for items map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various items
        # for the map, this maintains order useful for creating
        # queries with organized order
        items_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the items, extending the items map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's items map and uses it
            # to extend the current items map (iteration cycle)
            parent_items_map = parent.get_items_map()
            colony.map_extend(items_map, parent_items_map, copy_base_map = False)

        # retrieves the items (without foreign relation)
        # for the class and then sets them in the items
        # map for the current class
        items = cls.get_items()
        items_map[cls] = items

        # caches the items map in the class
        # to provide fast access in latter access
        cls._items_map = items_map

        # returns the items map, containing
        # the entity classes associated with
        # the maps containing the items
        return items_map

    @classmethod
    def get_names_map(cls):
        # in case the names map are already "cached" in the current
        # class (fast retrieval)
        if "_names_map" in cls.__dict__:
            # returns the cached names map from the entity
            # class object reference
            return cls._names_map

        # retrieves the parents for the entity
        # class, to check them for names map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various names
        # for the map, this maintains order useful for creating
        # queries with organized order
        names_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the names, extending the names map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's names map and uses it
            # to extend the current names map (iteration cycle),
            # the extension is made with no overriding of keys
            parent_names_map = parent.get_names_map()
            colony.map_extend(
                names_map,
                parent_names_map,
                override = False,
                copy_base_map = False
            )

        # retrieves all of the names for the
        # class and then sets them in the names
        # map for the current class
        names = cls.get_names()
        for name in names:
            names_map[name] = names_map.get(name, cls)

        # caches the names map in the class
        # to provide fast access in latter access
        cls._names_map = names_map

        # returns the names map, containing
        # the entity classes associated with
        # the maps containing the names
        return names_map

    @classmethod
    def get_generated_map(cls):
        # in case the generated map are already "cached" in the current
        # class (fast retrieval)
        if "_generated_map" in cls.__dict__:
            # returns the cached generated map from the entity
            # class object reference
            return cls._generated_map

        # retrieves the parents for the entity
        # class, to check them for generated map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various generated
        # for the map, this maintains order useful for creating
        # queries with organized order
        generated_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the generated (names), extending the
        # generated map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's generated map and uses it
            # to extend the current generated map (iteration cycle),
            # the extension is made with no overriding of keys
            parent_generated_map = parent.get_generated_map()
            colony.map_extend(generated_map, parent_generated_map, override = False, copy_base_map = False)

        # retrieves all of the generated (names) for the
        # class and then sets them in the generated map
        # for the current class
        generated = cls.get_generated()
        for _generated in generated:
            generated_map[_generated] = generated_map.get(_generated, cls)

        # caches the generated map in the class
        # to provide fast access in latter access
        cls._generated_map = generated_map

        # returns the generated map, containing
        # the entity classes associated with
        # the maps containing the generated (names)
        return generated_map

    @classmethod
    def get_indexed_map(cls):
        # in case the indexed map are already "cached" in the current
        # class (fast retrieval)
        if "_indexed_map" in cls.__dict__:
            # returns the cached indexed map from the entity
            # class object reference
            return cls._indexed_map

        # retrieves the parents for the entity
        # class, to check them for indexed map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various indexed
        # for the map, this maintains order useful for creating
        # queries with organized order
        indexed_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the indexed (names), extending the
        # indexed map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's indexed map and uses it
            # to extend the current indexed map (iteration cycle),
            # the extension is made with no overriding of keys
            parent_indexed_map = parent.get_indexed_map()
            colony.map_extend(indexed_map, parent_indexed_map, override = False, copy_base_map = False)

        # retrieves all of the indexed (names) for the
        # class and then sets them in the indexed map
        # for the current class
        indexed = cls.get_indexed()
        for _indexed in indexed:
            indexed_map[_indexed] = indexed_map.get(_indexed, cls)

        # caches the indexed map in the class
        # to provide fast access in latter access
        cls._indexed_map = indexed_map

        # returns the indexed map, containing
        # the entity classes associated with
        # the maps containing the indexed (names)
        return indexed_map

    @classmethod
    def get_mandatory_map(cls):
        # in case the mandatory map are already "cached" in the current
        # class (fast retrieval)
        if "_mandatory_map" in cls.__dict__:
            # returns the cached mandatory map from the entity
            # class object reference
            return cls._mandatory_map

        # retrieves the parents for the entity
        # class, to check them for mandatory map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various mandatory
        # for the map, this maintains order useful for creating
        # queries with organized order
        mandatory_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the mandatory (names), extending the
        # mandatory map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's mandatory map and uses it
            # to extend the current mandatory map (iteration cycle),
            # the extension is made with no overriding of keys
            parent_mandatory_map = parent.get_mandatory_map()
            colony.map_extend(mandatory_map, parent_mandatory_map, override = False, copy_base_map = False)

        # retrieves all of the mandatory (names) for the
        # class and then sets them in the mandatory map
        # for the current class
        mandatory = cls.get_mandatory()
        for _mandatory in mandatory:
            mandatory_map[_mandatory] = mandatory_map.get(_mandatory, cls)

        # caches the mandatory map in the class
        # to provide fast access in latter access
        cls._mandatory_map = mandatory_map

        # returns the mandatory map, containing
        # the entity classes associated with
        # the maps containing the mandatory (names)
        return mandatory_map

    @classmethod
    def get_immutable_map(cls):
        # in case the immutable map are already "cached" in the current
        # class (fast retrieval)
        if "_immutable_map" in cls.__dict__:
            # returns the cached immutable map from the entity
            # class object reference
            return cls._immutable_map

        # retrieves the parents for the entity
        # class, to check them for immutable map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various immutable
        # for the map, this maintains order useful for creating
        # queries with organized order
        immutable_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the immutable (names), extending the
        # immutable map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's immutable map and uses it
            # to extend the current immutable map (iteration cycle),
            # the extension is made with no overriding of keys
            parent_immutable_map = parent.get_immutable_map()
            colony.map_extend(immutable_map, parent_immutable_map, override = False, copy_base_map = False)

        # retrieves all of the immutable (names) for the
        # class and then sets them in the immutable map
        # for the current class
        immutable = cls.get_immutable()
        for _immutable in immutable:
            immutable_map[_immutable] = immutable_map.get(_immutable, cls)

        # caches the immutable map in the class
        # to provide fast access in latter access
        cls._immutable_map = immutable_map

        # returns the immutable map, containing
        # the entity classes associated with
        # the maps containing the immutable (names)
        return immutable_map

    @classmethod
    def get_relations_map(cls):
        """
        Retrieves a map containing the various "parent" classes associated
        with their relations (meta information).
        This map may be used to easily map the relations into a linear
        query.

        The recursion strategies used to create this map include vertical
        recursion (child to parent) and horizontal (relations).

        :rtype: Dictionary
        :return: The map containing the various "parent" classes associated
        with their relations information map.
        """

        # in case the relations map are already "cached" in the current
        # class (fast retrieval)
        if "_relations_map" in cls.__dict__:
            # returns the cached relations map from the entity
            # class object reference
            return cls._relations_map

        # retrieves the parents for the entity
        # class, to check them for relations map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various relations
        # for the map, this maintains order useful for creating
        # queries with organized order
        relations_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the relations, extending the relations map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's relations map and uses it
            # to extend the current relations map (iteration cycle)
            parent_relations_map = parent.get_relations_map()
            colony.map_extend(relations_map, parent_relations_map, copy_base_map = False)

        # retrieves the relations (meta information)
        # for the class and then sets them in the relations
        # map for the current class
        relations = cls.get_relations()
        relations_map[cls] = relations

        # caches the relations map in the class
        # to provide fast access in latter access
        cls._relations_map = relations_map

        # returns the relations map, containing
        # the entity classes associated with
        # the maps containing the relations
        return relations_map

    @classmethod
    def get_direct_relations_map(cls):
        # in case the direct relations map are already "cached" in
        # the current class (fast retrieval)
        if "_direct_relations_map" in cls.__dict__:
            # returns the cached direct relations map from
            # the entity class object reference
            return cls._direct_relations_map

        # retrieves the parents for the entity
        # class, to check them for direct
        # relations map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various direct
        # relations for the map, this maintains order useful for
        # creating queries with organized order
        direct_relations_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the direct relations, extending the
        # direct relations map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's direct relations map and uses it
            # to extend the current direct relations map (iteration cycle)
            parent_direct_relations_map = parent.get_direct_relations_map()
            colony.map_extend(direct_relations_map, parent_direct_relations_map, copy_base_map = False)

        # retrieves the direct relations (meta information)
        # for the class and then sets them in the direct
        # relations map for the current class
        direct_relations = cls.get_direct_relations()
        direct_relations_map[cls] = direct_relations

        # caches the direct relations map in the class
        # to provide fast access in latter access
        cls._direct_relations_map = direct_relations_map

        # returns the direct relations map, containing
        # the entity classes associated with the maps
        # containing the direct relations
        return direct_relations_map

    @classmethod
    def get_indirect_relations_map(cls):
        # in case the indirect relations map are already "cached" in
        # the current class (fast retrieval)
        if "_indirect_relations_map" in cls.__dict__:
            # returns the cached indirect relations map from
            # the entity class object reference
            return cls._indirect_relations_map

        # retrieves the parents for the entity
        # class, to check them for indirect
        # relations map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various indirect
        # relations for the map, this maintains order useful for
        # creating queries with organized order
        indirect_relations_map = colony.OrderedMap()

        # iterates over all the parents to iteratively
        # retrieve the indirect relations, extending the
        # indirect relations map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's indirect relations map and uses it
            # to extend the current indirect relations map (iteration cycle)
            parent_indirect_relations_map = parent.get_indirect_relations_map()
            colony.map_extend(indirect_relations_map, parent_indirect_relations_map, copy_base_map = False)

        # retrieves the indirect relations (meta information)
        # for the class and then sets them in the indirect
        # relations map for the current class
        indirect_relations = cls.get_indirect_relations()
        indirect_relations_map[cls] = indirect_relations

        # caches the indirect relations map in the class
        # to provide fast access in latter access
        cls._indirect_relations_map = indirect_relations_map

        # returns the indirect relations map, containing
        # the entity classes associated with the maps
        # containing the indirect relations
        return indirect_relations_map

    @classmethod
    def get_to_one_map(cls):
        # in case the to one relations map are already "cached" in the current
        # class (fast retrieval)
        if "_to_one_map" in cls.__dict__:
            # returns the cached to one relations map from the entity
            # class object reference
            return cls._to_one_map

        # retrieves the parents for the entity
        # class, to check them for to one relations map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various to one
        # relations for the map, this maintains order useful
        # for creating queries with organized order
        to_one_map = colony.OrderedMap()

        # iterates over all the parents to iteratively retrieve the
        # to one relations, extending the to one relations map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's to one relations map and uses it
            # to extend the current to one relations map (iteration cycle)
            parent_to_one_map = parent.get_to_one_map()
            colony.map_extend(to_one_map, parent_to_one_map, copy_base_map = False)

        # retrieves the to one relations (meta information)
        # for the class and then sets them in the to one
        # relations map for the current class
        to_one = cls.get_to_one()
        to_one_map[cls] = to_one

        # caches the to one relations map in the class
        # to provide fast access in latter access
        cls._to_one_map = to_one_map

        # returns the to one relations map, containing
        # the entity classes associated with
        # the maps containing the to one relations
        return to_one_map

    @classmethod
    def get_to_many_map(cls):
        # in case the to many relations map are already "cached" in the current
        # class (fast retrieval)
        if "_to_many_map" in cls.__dict__:
            # returns the cached to many relations map from the entity
            # class object reference
            return cls._to_many_map

        # retrieves the parents for the entity
        # class, to check them for to many relations map
        parents = cls.get_parents()

        # creates a new ordered map to hold the various to many
        # relations for the map, this maintains order useful
        # for creating queries with organized order
        to_many_map = colony.OrderedMap()

        # iterates over all the parents to iteratively retrieve the
        # to many relations, extending the to many relations map with them
        for parent in parents:
            # in case the current parent is abstract no need
            # to retrieve its items (not going to be persisted)
            if parent.is_abstract(): continue

            # retrieves the parent's to many relations map and uses it
            # to extend the current to many relations map (iteration cycle)
            parent_to_many_map = parent.get_to_many_map()
            colony.map_extend(to_many_map, parent_to_many_map, copy_base_map = False)

        # retrieves the to many relations (meta information)
        # for the class and then sets them in the to many
        # relations map for the current class
        to_many = cls.get_to_many()
        to_many_map[cls] = to_many

        # caches the to many relations map in the class
        # to provide fast access in latter access
        cls._to_many_map = to_many_map

        # returns the to many relations map, containing
        # the entity classes associated with
        # the maps containing the to many relations
        return to_many_map

    @classmethod
    def get_mapped_relations(cls):
        # in case the mapped relations are already "cached" in the current
        # class (fast retrieval)
        if "_mapped_relations" in cls.__dict__:
            # returns the cached mapped relations from the entity
            # class object reference
            return cls._mapped_relations

        # retrieves the relations map for the current
        # class to process it "finding" the correct
        # mapped relations
        relations = cls.get_relations()

        # creates the map to hold the various (found) mapped relations
        # in the current class context
        mapped_relations = {}

        # iterate over all the relation items (name and value)
        # trying to find the relations that are mapped
        for relation_name, relation in colony.legacy.iteritems(relations):
            # checks if the relation is mapped in the current
            # entity model class
            is_mapped = cls.is_mapped(relation_name)

            # in case there is no "mapper" for the current relation,
            # it's not considered to be a mapped relation and so the
            # loop must continue
            if not is_mapped: continue

            # sets the relation in the mapped relations map, because
            # the current entity model is not the "mapper" of the relation
            mapped_relations[relation_name] = relation

        # caches the mapped relations element in the class
        # to provide fast access in latter access
        cls._mapped_relations = mapped_relations

        # retrieves the map containing the various
        # mapped relations associated with their
        # meta information
        return mapped_relations

    @classmethod
    def get_unmapped_relations(cls):
        """
        Retrieves the set of relations that are considered to be unmapped.
        The unmapped relations are the relations that are not mapped by
        the current entity model, these includes both the indirect relations
        (mapped using association table) and direct relations (mapped in the
        reverse entity).

        :rtype: Dictionary
        :return: The map containing the various unmapped relations associated
        with their relations attributes.
        """

        # in case the unmapped relations are already "cached" in the current
        # class (fast retrieval)
        if "_unmapped_relations" in cls.__dict__:
            # returns the cached unmapped relations from the entity
            # class object reference
            return cls._unmapped_relations

        # retrieves the relations map for the current
        # class to process it "finding" the correct
        # unmapped relations
        relations = cls.get_relations()

        # creates the map to hold the various (found) unmapped relations
        # in the current class context
        unmapped_relations = {}

        # iterate over all the relation items (name and value)
        # trying to find the relations that are unmapped
        for relation_name, relation in colony.legacy.iteritems(relations):
            # checks if the relation is mapped in the current
            # entity model class
            is_mapped = cls.is_mapped(relation_name)

            # in case the relations is mapped by the entity, it's
            # not considered to be an unmapped relation and so
            # the loop must continue
            if is_mapped: continue

            # sets the relation in the unmapped relations map, because
            # the relation does not contain a mapper or the current
            # entity model is not the "mapper" of the relation
            unmapped_relations[relation_name] = relation

        # caches the unmapped relations element in the class
        # to provide fast access in latter access
        cls._unmapped_relations = unmapped_relations

        # retrieves the map containing the various
        # unmapped relations associated with their
        # meta information
        return unmapped_relations

    @classmethod
    def get_direct_relations(cls):
        # in case the direct relations are already "cached" in the current
        # class (fast retrieval)
        if "_direct_relations" in cls.__dict__:
            # returns the cached direct relations from the entity
            # class object reference
            return cls._direct_relations

        # retrieves the relations map for the current
        # class to process it "finding" the correct
        # direct relations
        relations = cls.get_relations()

        # creates the map to hold the various (found) direct relations
        # in the current class context
        direct_relations = {}

        # iterate over all the relation items (name and value)
        # trying to find the relations that are direct
        for relation_name, relation in colony.legacy.iteritems(relations):
            # checks if the relation is mapped in the current
            # entity model class
            is_mapped = cls.is_mapped(relation_name)

            # retrieves the "mapper" (class) for the current relation
            mapper = cls.get_mapper(relation_name)

            # in case there is no "mapper" for the current relation
            # (indirect) or the "mapper" for the relation is the
            # current entity model (mapped), it's not considered
            # to be a direct relation and so the loop must continue
            if not mapper or is_mapped: continue

            # sets the relation in the direct relations map, because
            # the current entity model is not the "mapper" of the relation
            direct_relations[relation_name] = relation

        # caches the direct relations element in the class
        # to provide fast access in latter access
        cls._direct_relations = direct_relations

        # retrieves the map containing the various
        # direct relations associated with their
        # meta information
        return direct_relations

    @classmethod
    def get_indirect_relations(cls):
        # in case the indirect relations are already "cached" in the current
        # class (fast retrieval)
        if "_indirect_relations" in cls.__dict__:
            # returns the cached indirect relations from the entity
            # class object reference
            return cls._indirect_relations

        # retrieves the relations map for the current
        # class to process it "finding" the correct
        # indirect relations
        relations = cls.get_relations()

        # creates the map to hold the various (found) indirect relations
        # in the current class context
        indirect_relations = {}

        # iterate over all the relation items (name and value)
        # trying to find the relations that are indirect
        for relation_name, relation in colony.legacy.iteritems(relations):
            # retrieves the "mapper" (class) for the current relation
            mapper = cls.get_mapper(relation_name)

            # in case there is a "mapper" for the current relation
            # it is not considered to be an indirect relation and
            # so the loop must continue
            if mapper: continue

            # sets the relation in the indirect relations map, because
            # there is no "mapper" for the current relation
            indirect_relations[relation_name] = relation

        # caches the indirect relations element in the class
        # to provide fast access in latter access
        cls._indirect_relations = indirect_relations

        # retrieves the map containing the various
        # indirect relations associated with their
        # meta information
        return indirect_relations

    @classmethod
    def get_relation_unique(cls, relation_name):
        """
        Retrieves the unique identifier name for the given relation.
        The unique identifier is generated by joining the two
        names of relation (in both sides) and ordering it in
        alphabetically order.

        :type relation_name: String
        :param relation_name: The name of the relation to
        retrieve the unique identifier.
        :rtype: String
        :return: The unique identifier of the relation.
        """

        # retrieves the reverse (relation name) for
        # the current relation
        reverse = cls.get_reverse(relation_name)

        # creates the relations name with the relation name
        # and the reverse then sorts it (becomes unique name)
        # and joins the string using the default separator
        # (creates the relation unique name)
        relation_names = [relation_name, reverse]
        relation_names.sort()
        relation_unique = SAFE_CHARACTER + "_".join(relation_names)

        # retrieves the relation unique name
        return relation_unique

    @classmethod
    def get_relations(cls):
        # in case the relations are already "cached" in the current
        # class (fast retrieval)
        if "_relations" in cls.__dict__:
            # returns the cached relations from the entity
            # class object reference
            return cls._relations

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the map to hold the various relations
        # in the current class context
        relations = {}

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # field attribute, sets the appropriate ones in the relations
        # map (meta information)
        for key, value in colony.legacy.iteritems(items):
            # in case the key is one of the "private" non safe values it
            # should be ignored (not an item)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (not an item)
            if key.isupper(): continue

            # in case the type is a function or a method it
            # should be ignored (not an item)
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # in case the key does not refer a relation
            # value (must be ignored)
            if not cls.is_relation(key): continue

            # retrieves the relation (map) for the current
            # key (relation name) then sets it in the relation
            # map for the current key
            relation = cls.get_relation(key)
            relations[key] = relation

        # caches the relations element in the class
        # to provide fast access in latter access
        cls._relations = relations

        # returns the created relations
        # map
        return relations

    @classmethod
    def get_all_relations(cls):
        # in case the all relations are already "cached" in the current
        # class (fast retrieval)
        if "_all_relations" in cls.__dict__:
            # returns the cached all relations from the entity
            # class object reference
            return cls._all_relations

        # creates the map to hold the various relations
        # entity classes, populated recursively
        all_relations = {}

        # retrieves the relations present at the current entity
        # class level
        relations = cls.get_relations()

        # retrieves the parent entity classes from
        # the current class
        parents = cls.get_parents()

        # iterates over all the parents to extend
        # the all relations list with the parent relations
        # from the parent
        for parent in parents:
            # retrieves the (all) relations from the parents
            # and extends the all relations map with them
            _relations = parent.get_all_relations()
            colony.map_extend(all_relations, _relations, copy_base_map = False)

        # extends the all relations map with the relations
        # from the current entity class
        colony.map_extend(all_relations, relations, copy_base_map = False)

        # caches the all relations element in the class
        # to provide fast access in latter access
        cls._all_relations = all_relations

        # returns the list that contains all the relations
        # from all the parent entity classes
        return all_relations

    @classmethod
    def get_to_one(cls):
        # in case the to one relations are already "cached"
        # in the current class (fast retrieval)
        if "_to_one" in cls.__dict__:
            # returns the cached to one relations from the entity
            # class object reference
            return cls._to_one

        # retrieves the relations from the class, this
        # map contains the relations associated with
        # their attribute names
        relations = cls.get_relations()

        # creates the map to hold the various to one
        # relations in the current class context
        to_one = {}

        # iterates over all the relations in the current context
        # to filter the ones that do not correspond to a valid
        # to one relation, sets the appropriate ones in the
        # to one relations map (meta information)
        for key, relation in colony.legacy.iteritems(relations):
            # in case the relation is of type to many
            # no need to continue it's not a proper relation
            # (considers that any relations that is not of type
            # to many is of type to one)
            if cls.is_to_many(key): continue

            # sets the relation in the to one relations
            # map associated with the current key
            to_one[key] = relation

        # caches the to may relations element in the class
        # to provide fast access in latter access
        cls._to_one = to_one

        # returns the created to one relations
        # map
        return to_one

    @classmethod
    def get_to_many(cls):
        # in case the to many relations are already "cached"
        # in the current class (fast retrieval)
        if "_to_many" in cls.__dict__:
            # returns the cached to many relations from the entity
            # class object reference
            return cls._to_many

        # retrieves the relations from the class, this
        # map contains the relations associated with
        # their attribute names
        relations = cls.get_relations()

        # creates the map to hold the various to many
        # relations in the current class context
        to_many = {}

        # iterates over all the relations in the current context
        # to filter the ones that do not correspond to a valid
        # to many relation, sets the appropriate ones in the
        # to many relations map (meta information)
        for key, relation in colony.legacy.iteritems(relations):
            # in case the relation is not of type to many
            # no need to continue it's not a proper relation
            if not cls.is_to_many(key): continue

            # sets the relation in the to many relations
            # map associated with the current key
            to_many[key] = relation

        # caches the to may relations element in the class
        # to provide fast access in latter access
        cls._to_many = to_many

        # returns the created to many relations
        # map
        return to_many

    @classmethod
    def is_lazy(cls, relation_name):
        """
        Checks if the relation with the provided name is in
        fact of type lazy.

        A lazy loaded relation is a relation that is not going
        to be retrieved (by default) in a find or get operation
        over an entity model.

        :type relation_name: String
        :param relation_name: The name of the relation to be
        verifies for lazy loading.
        :rtype: bool
        :return: The result of the is lazy loaded relation test.
        """

        # retrieves the relation attributes for the given
        # relation name and then retrieves the fetch type
        relation_attributes = getattr(cls, relation_name)
        fetch_type = relation_attributes.get("fetch_type", "lazy")

        # checks if the fetch type is lazy to verify
        # that if the relation is lazy
        is_lazy = fetch_type == "lazy"

        # returns the result of the is lazy (relation)
        # test (lazy relation verification)
        return is_lazy

    @classmethod
    def get_items(cls, foreign_relations = False):
        """
        Retrieves the various items (fields) of the current entity
        that describe it (class) in the current depth level.
        If this entity class is inheriting fields from a (non abstract)
        entity those fields will not be returned in this method.

        An optional flag may be set if foreign relations should be
        retrieved alongside the "normal" items.
        Foreign relations are relation fields that are not mapped
        by the current entity.

        :type foreign_relations: bool
        :param foreign_relations: If the foreign relation items should
        also be retrieved along the "normal" items.
        :rtype: Dictionary
        :return: The map containing the set of "specific" items for the
        current entity class.
        """

        # in case the current class is abstract no items should be defined
        # (the current class does not reference items)
        if cls.is_abstract(): return {}

        # in case the items are already "cached" in the current
        # class (fast retrieval)
        if foreign_relations and "_items" in cls.__dict__:
            # returns the cached items from the entity
            # class object reference
            return cls._items

        # in case the (non foreign) items are already "cached"
        # in the current class (fast retrieval)
        if not foreign_relations and "_non_foreign_items" in cls.__dict__:
            # returns the cached (non foreign) items from the entity
            # class object reference
            return cls._non_foreign_items

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the map to hold the various items
        # in the current class context
        _items = {}

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # field attribute
        for key, value in colony.legacy.iteritems(items):
            # in case the key is one of the "private" non safe values it
            # should be ignored (not an item)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (not an item)
            if key.isupper(): continue

            # in case the type is a function or a method it
            # should be ignored (not an item)
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # in case the foreign relations are meant to be ignored and
            # the current attribute is a non mapped relation (foreign)
            # it should be ignored
            if not foreign_relations and cls.is_relation(key) and not cls.is_mapped(key): continue

            # sets the value as the item for the current
            # key (valid field in the context)
            _items[key] = value

        # in case the foreign relations flag is set
        # the cached value should be items
        if foreign_relations:
            # caches the items element in the class
            # to provide fast access in latter access
            cls._items = _items
        # otherwise the cached value should be non
        # foreign items (separate cache)
        else:
            # caches the items element in the class (as
            # non foreign items) to provide fast access
            # in latter access
            cls._non_foreign_items = _items

        # returns the map containing the various
        # items of the entity class
        return _items

    @classmethod
    def get_names(cls, foreign_relations = False):
        # in case the current class is abstract no names should be defined
        # (the current class does not reference names)
        if cls.is_abstract(): return []

        # in case the names are already "cached" in the current
        # class (fast retrieval)
        if foreign_relations and "_names" in cls.__dict__:
            # returns the cached names from the entity
            # class object reference
            return cls._names

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the list to hold the various names
        # in the current class context
        names = []

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # field attribute (only the name is going to be used)
        for key, value in colony.legacy.iteritems(items):
            # in case the key is one of the "private" non safe values it
            # should be ignored (not a name)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (not a name)
            if key.isupper(): continue

            # in case the type is a function or a method it
            # should be ignored (not a name)
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # adds the key (name) to the list of names
            # for the current entity model (class)
            names.append(key)

        # caches the names element in the class
        # to provide fast access in latter access
        cls._names = names

        # returns the list containing the various
        # names of the entity class
        return names

    @classmethod
    def get_generated(cls, foreign_relations = False):
        # in case the generated are already "cached" in the current
        # class (fast retrieval)
        if foreign_relations and "_generated" in cls.__dict__:
            # returns the cached generated from the entity
            # class object reference
            return cls._generated

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the list to hold the various generated (names)
        # in the current class context
        generated = []

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # generated attribute (only the name is going to be used)
        for key, value in colony.legacy.iteritems(items):
            # in case the key is one of the "private" non safe values it
            # should be ignored (not a name)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (not an item)
            if key.isupper(): continue

            # in case the type is a function or a method it
            # should be ignored (not a name)
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # in case the current key name does not refer a
            # generated value, it is not mean to be added to
            # the generated list
            if not cls.is_generated(key): continue

            # adds the key (name) to the list of generated
            # for the current entity model (class)
            generated.append(key)

        # caches the generated element in the class
        # to provide fast access in latter access
        cls._generated = generated

        # returns the list containing the various
        # generated names of the entity class
        return generated

    @classmethod
    def get_indexed(cls, foreign_relations = False):
        # in case the indexed are already "cached" in the current
        # class (fast retrieval)
        if foreign_relations and "_indexed" in cls.__dict__:
            # returns the cached indexed from the entity
            # class object reference
            return cls._indexed

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the list to hold the various indexed (names)
        # in the current class context
        indexed = []

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # indexed attribute (only the name is going to be used)
        for key, value in colony.legacy.iteritems(items):
            # in case the key is one of the "private" non safe values it
            # should be ignored (not a name)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (not a name)
            if key.isupper(): continue

            # in case the type is a function or a method it
            # should be ignored (not a name)
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # in case the current key name does not refer a
            # indexed value, it is not mean to be added to
            # the indexed list
            if not cls.is_indexed(key): continue

            # adds the key (name) to the list of indexed
            # for the current entity model (class)
            indexed.append(key)

        # caches the indexed element in the class
        # to provide fast access in latter access
        cls._indexed = indexed

        # returns the list containing the various
        # indexed names of the entity class
        return indexed

    @classmethod
    def get_mandatory(cls, foreign_relations = False):
        # in case the mandatory are already "cached" in the current
        # class (fast retrieval)
        if foreign_relations and "_mandatory" in cls.__dict__:
            # returns the cached mandatory from the entity
            # class object reference
            return cls._mandatory

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the list to hold the various mandatory (names)
        # in the current class context
        mandatory = []

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # mandatory attribute (only the name is going to be used)
        for key, value in colony.legacy.iteritems(items):
            # in case the key is one of the "private" non safe values it
            # should be ignored (not a name)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (not a name)
            if key.isupper(): continue

            # in case the type is a function or a method it
            # should be ignored (not a name)
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # in case the current key name does not refer a
            # mandatory value, it is not mean to be added to
            # the mandatory list
            if not cls.is_mandatory(key): continue

            # adds the key (name) to the list of mandatory
            # for the current entity model (class)
            mandatory.append(key)

        # caches the mandatory element in the class
        # to provide fast access in latter access
        cls._mandatory = mandatory

        # returns the list containing the various
        # mandatory names of the entity class
        return mandatory

    @classmethod
    def get_immutable(cls, foreign_relations = False):
        # in case the immutable are already "cached" in the current
        # class (fast retrieval)
        if foreign_relations and "_immutable" in cls.__dict__:
            # returns the cached immutable from the entity
            # class object reference
            return cls._immutable

        # retrieves the items from the class, this
        # map of items may contain extra symbols
        items = cls._items()

        # creates the list to hold the various immutable (names)
        # in the current class context
        immutable = []

        # iterate over all the items in the current context
        # to filter the ones that do not correspond to a valid
        # immutable attribute (only the name is going to be used)
        for key, value in colony.legacy.iteritems(items):
            # in case the key is one of the "private" non safe values it
            # should be ignored (not a name)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (not a name)
            if key.isupper(): continue

            # in case the type is a function or a method it
            # should be ignored (not a name)
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # in case the current key name does not refer a
            # immutable value, it is not mean to be added to
            # the immutable list
            if not cls.is_immutable(key): continue

            # adds the key (name) to the list of immutable
            # for the current entity model (class)
            immutable.append(key)

        # caches the immutable element in the class
        # to provide fast access in latter access
        cls._immutable = immutable

        # returns the list containing the various
        # immutable names of the entity class
        return immutable

    @classmethod
    def has_name(cls, name):
        """
        Checks if the current entity class contains a name
        attribute with the given name.

        This method may be used in security sections of the
        code, to provide extra validation on the attribute name.

        :type name: String
        :param name: The name of the attribute to be verified
        for existence in the current entity class.
        :rtype: bool
        :return: If an attribute with the given name exists
        in the current entity class.
        """

        # retrieves the map containing the various
        # names of the current class associated with
        # their proper parent classes and checks if
        # the name is contained there (has name)
        names_map = cls.get_names_map()
        has_name = name in names_map

        # returns if the name exists in the current
        # entity class
        return has_name

    @classmethod
    def get_cls(cls, name):
        """
        Retrieves the class associated with the name, a class is
        defined as being associated with a name when the name
        is defined at such class level.

        The associated class may be also called owner class.

        :type name: String
        :param name: The name of the attribute to retrieve the
        associated class (owner class).
        :rtype: EntityClass
        :return: The class that is considered to be associated with
        the attribute with the provided name.
        """

        # retrieves the map containing the various
        # names of the current class associated with
        # their proper parent classes and retrieve the
        # class associated with the name
        names_map = cls.get_names_map()
        name_cls = names_map.get(name, None)

        # returns the (proper) class associated with the
        # provided name to the caller method
        return name_cls

    @classmethod
    def get_id(cls):
        """
        Retrieves the name of the id attribute of the
        current class if one is available.

        The retrieval of the id (name) is recursive
        and if the current class level does not contain
        an id attribute, the method traverses the upper
        class levels to find id.

        :rtype: String
        :return: The name of the id attribute of the class
        if one is available, otherwise none.
        """

        # in case the id is already "cached" in the current
        # class (fast retrieval)
        if "_id" in cls.__dict__:
            # returns the cached id from the entity
            # class object reference
            return cls._id

        # retrieves the items (fields) for the current
        # entity class context
        items = cls.get_items()

        # sets the "initial" id name attribute
        # to invalid (not retrieved)
        id = None

        # iterates over all the entity class items
        # to find the "correct" id attribute name
        # (if one is available)
        for key, value in colony.legacy.iteritems(items):
            # "checks" if the current value is of
            # type id (identifier)
            is_id = value.get("id", False)

            # in case the current value is not
            # an identifier (it's not going to
            # save it)
            if not is_id:
                # continue the loop, try to find it
                # anywhere else
                continue

            # saves the key of the current item as the
            # id attribute of the entity class (found it)
            # and then breaks the cycle
            id = key
            break

        # in case the id is not defined in the current
        # class need to find elsewhere in the upper (parent)
        # class chain
        if not id:
            # tries to retrieve the parent class of the
            # current model to retrieve the id from it,
            # in case there's no parent returns an invalid
            # value meaning that no id value exists for it
            parent = cls.get_parent()
            if not parent: return None

            # runs the recursive step of retrieving the id
            # value from the parent class (default behavior)
            id = parent.get_id()

        # caches the id element in the class
        # to provide fast access in latter access
        cls._id = id

        # returns the id (name) value for
        # the current entity class context
        return id

    @classmethod
    def get_parents(cls):
        # in case the parents are already "cached" in the current
        # class (fast retrieval)
        if "_parents" in cls.__dict__:
            # returns the cached parents from the entity
            # class object reference
            return cls._parents

        # retrieves the parent classes
        # for the current class
        parents = cls._get_bases()

        # in case the (base) entity class is present
        # in the parents list (need to remove it)
        if EntityClass in parents:
            # converts the parents tuple into a list
            # and then removes the entity class from
            # it (avoids possible problems in persistence)
            parents = list(parents)
            parents.remove(EntityClass)

        # caches the parents element in the class
        # to provide fast access in latter access
        cls._parents = parents

        # returns the parents of the current class
        # in the context
        return parents

    @classmethod
    def get_abstract_parents(cls):
        # in case the parents are already "cached" in the current
        # class (fast retrieval)
        if "_abstract_parents" in cls.__dict__:
            # returns the cached abstract parents from the entity
            # class object reference
            return cls._abstract_parents

        # retrieves the complete set of parent classes
        # for the current class and then filters the set
        # so that only the abstract parents are selected
        parents = cls._get_bases()
        abstract_parents = [parent for parent in parents if parent.is_abstract()]

        # caches the abstract parents element in the class
        # to provide fast access in latter access
        cls._abstract_parents = abstract_parents

        # returns the abstract parents of the current class
        # in the context
        return abstract_parents

    @classmethod
    def get_all_parents(cls):
        # in case the all parents are already "cached" in the current
        # class (fast retrieval)
        if "_all_parents" in cls.__dict__:
            # returns the cached all parents from the entity
            # class object reference
            return cls._all_parents

        # creates the list to hold the various parent
        # entity classes, populated recursively
        all_parents = []

        # retrieves the parent entity classes from
        # the current class
        parents = cls.get_parents()

        # iterates over all the parents to extend
        # the all parents list with the parent entities
        # from the parent
        for parent in parents:
            # retrieves the (all) parents from the parents
            # and extends the all parents list with them,
            # this extension method avoids duplicates
            _parents = parent.get_all_parents()
            colony.list_extend(all_parents, _parents, False)

        # extends the all parents list with the parents
        # from the current entity class (avoids duplicates)
        colony.list_extend(all_parents, parents, False)

        # caches the all parents element in the class
        # to provide fast access in latter access
        cls._all_parents = all_parents

        # returns the list that contains all the parents
        # entity classes
        return all_parents

    @classmethod
    def get_all_abstract_parents(cls):
        # in case the all abstract parents are already "cached" in the current
        # class (fast retrieval)
        if "_all_abstract_parents" in cls.__dict__:
            # returns the cached all parents from the entity
            # class object reference
            return cls._all_abstract_parents

        # creates the list to hold the various abstract parent
        # entity classes, populated recursively
        all_abstract_parents = []

        # retrieves the abstract parent entity classes from
        # the current class
        abstract_parents = cls.get_abstract_parents()

        # iterates over all the abstract parents to extend the all
        # abstract parents list with the abstract parent
        # entities from the abstract parent
        for abstract_parent in abstract_parents:
            # retrieves the (all) abstract parents from the parents
            # and extends the all abstract parents list with them,
            # this extension method avoids duplicates
            _abstract_parents = abstract_parent.get_all_abstract_parents()
            colony.list_extend(all_abstract_parents, _abstract_parents, False)

        # extends the all abstract parents list with the parents
        # from the current entity class (avoids duplicates)
        colony.list_extend(all_abstract_parents, abstract_parents, False)

        # caches the all abstract parents element in the class
        # to provide fast access in latter access
        cls._all_abstract_parents = all_abstract_parents

        # returns the list that contains all the abstract parents
        # entity classes
        return all_abstract_parents

    @classmethod
    def get_parent(cls):
        """
        Retrieves the first (and primary) parent from the entity
        class in the current context.

        This method requires accessing all the parent and filtering
        them against the entity class, so it may be an expensive
        operation.

        :rtype: Class
        :return: The parent entity class to be considered the primary.
        """

        # retrieves "all" the parents from the class
        # and then retrieves the first of them in case
        # at least one is defined
        parents = cls.get_parents()
        parent = parents and parents[0] or None

        # returns the "filtered" parent entity class
        return parent

    @classmethod
    def get_top_parent(cls, abstract_valid = False):
        """
        Retrieves the top level parent class in the inheritance
        chain, this class should be the left most class in the
        list described the inheritance chain.

        This method requires accessing all the parent and filtering
        them against the entity class, so it may be an expensive
        operation.

        :type abstract_valid: bool
        :param abstract_valid: If abstract classes should be considered
        valid as valid top parents.
        :rtype: Class
        :return: The top parent entity class to be considered the
        top level entity class.
        """

        # retrieves "all" the parents from the class
        # then sets the initial top parent value as
        # the current class (in case no valid parent
        # is found it is considered the top parent)
        all_parents = cls.get_all_parents()
        top_parent = cls

        # iterates over all the parents, trying to find a valid
        # parent to set it as the top parent (the parent list is
        # ordered from left to right)
        for _parent in all_parents:
            # in case the abstract valid flag is not set and the
            # parent class is abstract continues the loop, (not
            # considered a valid top parent class) otherwise sets
            # the top parent class and breaks the loop
            if not abstract_valid and _parent.is_abstract(): continue
            top_parent = _parent
            break

        # returns the "filtered top" parent entity class
        return top_parent

    @classmethod
    def has_parents(cls, abstract_valid = False):
        # in case the has parents flag is already "cached"
        # in the current class (fast retrieval)
        if "_has_parents" in cls.__dict__:
            # returns the cached has parents from the entity
            # class object reference
            return cls._has_parents

        # retrieves the parent classes
        # for the current class and then retrieves
        # length of them
        parents = cls._get_bases()
        parents_length = len(parents)

        # in case there are no parents defined
        # in the current entity class
        if not parents:
            # returns false (no parents
            # defined in entity class)
            cls._has_parents = False
            return False

        # in case the entity contains only one parent
        # and it is the (base) entity class it's not
        # considered to have parents
        if parents_length == 1 and parents[0] == EntityClass:
            # returns false (the only parent
            # is the entity class, not considered)
            cls._has_parents = False
            return False

        # in case the abstract valid flag is not set
        # and there are no valid non abstract parents
        if not abstract_valid and not [parent for parent in parents if not parent.is_abstract()]:
            # returns false (the parent classes
            # are all abstract)
            cls._has_parents = False
            return False

        # returns true, there are parents
        # available
        cls._has_parents = True
        return True

    @classmethod
    def is_ready(cls):
        """
        Verifies if the current entity class is ready to be used
        in a persistent context. Some entity classes may not comply
        with all the requirements for the persistence and are considered
        not ready/available for the persistence context.

        :rtype: bool
        :return: If the current entity class is ready and available
        for the current persistence context.
        """

        table_id = cls.get_id()
        if table_id == None: return False
        return True

    @classmethod
    def is_abstract(cls):
        """
        Checks if the current entity class is of type abstract,
        this kind of classes do not contain a specification in
        the data source.

        These classes may be used for logical implementation and
        not data oriented ones.

        :rtype: bool
        :return: If the current entity class is of type abstract.
        """

        return "abstract" in cls.__dict__ and cls.abstract

    @classmethod
    def is_generated(cls, attribute_name):
        # in case the attribute name does not exists
        # in the class, it sure is not a generated
        if not hasattr(cls, attribute_name):
            # returns invalid, if the value
            # does not exists it cannot be
            # a generated name
            return False

        # retrieves the attribute from the class, and
        # tests it for the expected dictionary type
        # if that's the case tries to retrieve the
        # meta data information from it
        attribute = getattr(cls, attribute_name)
        attribute_type = type(attribute)
        if not attribute_type == dict: return False
        is_generated = attribute.get("generated", False)

        # returns the value of the generated checking
        # value
        return is_generated

    @classmethod
    def is_indexed(cls, attribute_name):
        # in case the attribute name does not exists
        # in the class, it sure is not a indexed
        if not hasattr(cls, attribute_name):
            # returns invalid, if the value
            # does not exists it cannot be
            # a indexed name
            return False

        # retrieves the attribute from the class, and
        # tests it for the expected dictionary type
        # if that's the case tries to retrieve the
        # meta data information from it
        attribute = getattr(cls, attribute_name)
        attribute_type = type(attribute)
        if not attribute_type == dict: return False
        is_indexed = attribute.get("indexed", False)

        # returns the value of the indexed checking
        # value
        return is_indexed

    @classmethod
    def is_mandatory(cls, attribute_name):
        # in case the attribute name does not exists
        # in the class, it sure is not a mandatory
        if not hasattr(cls, attribute_name):
            # returns invalid, if the value
            # does not exists it cannot be
            # a mandatory name
            return False

        # retrieves the attribute from the class, and
        # tests it for the expected dictionary type
        # if that's the case tries to retrieve the
        # meta data information from it
        attribute = getattr(cls, attribute_name)
        attribute_type = type(attribute)
        if not attribute_type == dict: return False
        is_mandatory = attribute.get("mandatory", False)

        # returns the value of the mandatory checking
        # value
        return is_mandatory

    @classmethod
    def is_immutable(cls, attribute_name):
        # in case the attribute name does not exists
        # in the class, it sure is not a immutable
        if not hasattr(cls, attribute_name):
            # returns invalid, if the value
            # does not exists it cannot be
            # a immutable name
            return False

        # retrieves the attribute from the class, and
        # tests it for the expected dictionary type
        # if that's the case tries to retrieve the
        # meta data information from it
        attribute = getattr(cls, attribute_name)
        attribute_type = type(attribute)
        if not attribute_type == dict: return False
        is_immutable = attribute.get("immutable", False)

        # returns the value of the immutable checking
        # value
        return is_immutable

    @classmethod
    def is_relation(cls, attribute_name):
        """
        Checks if the attribute for the given attribute name refers
        a relation or a single attribute.

        This method is called by a lot of internal structures so
        optimization of its code is a major concert and the performance
        of it is as fast as possible.

        :type attribute_name: String
        :param attribute_name: The name of the attribute to be checked
        for relation.
        :rtype: bool
        :return: If the requested attribute refers a relation attribute
        or a single (simple) attribute.
        """

        # in case the attribute name does not exists
        # in the class, it sure is not a relation
        if not hasattr(cls, attribute_name):
            # returns invalid, if the value
            # does not exists it cannot be
            # a relation
            return False

        # retrieves the attribute from the class, and
        # tests it for the expected dictionary type
        # if that's the case tries to retrieve the
        # meta data information from it
        attribute = getattr(cls, attribute_name)
        attribute_type = type(attribute)
        if not attribute_type == dict: return False
        data_type = attribute.get("type", None)

        # checks the value of the data type to "see"
        # if it refers a relation value
        is_relation = data_type == "relation"

        # returns the value of the relation checking
        # value
        return is_relation

    @classmethod
    def is_mapped(cls, relation_name):
        """
        Checks if the relation with the given (attribute) name
        is "mapped" in the current entitie's table.

        By checking if the relation attribute is mapped in the
        current entitie's table the method is verifying if the
        current entity class is the "mapper" class of the relation.

        :type relation_name: String
        :param relation_name: The name of the relation (attribute)
        name to be tested for "mapping".
        :rtype: bool
        :return: The result of the is mapped in current entity
        test value, for the requested relation.
        """

        # retrieves the "mapper" class for the current relation
        # this involves the reverse resolutions of the relation
        # so this is considered an expensive operation the "mapper"
        # name is retrieved so that an additional verification may
        # be processed
        mapper, mapper_name = cls.get_mapper(relation_name, get_mapper_name = True)

        # checks if the "mapper" for the relation is the
        # "current" class and the mapper name is the current
        # relation to be verified
        is_mapped = mapper == cls and mapper_name == relation_name

        # returns the value of the is mapped in the
        # current class for relation.
        return is_mapped

    @classmethod
    def get_mapper(cls, relation_name, get_mapper_name = False):
        # starts the "mapper" name value with an initial
        # invalid value
        mapper_name = None

        # retrieves the relation attributes and the
        # reverse relation name to be used in the
        # "mapper" resolution"
        relation = cls.get_relation(relation_name)
        reverse = cls.get_reverse(relation_name)

        # retrieves the target class for the relation and
        # then uses it to retrieve the target relation
        target_class = cls.get_target(relation_name)
        target_relation = target_class.get_relation(reverse)

        # tries to retrieve the "mapper" from both the target
        # class and the current class (if none is found the relation
        # is considered to be externally mapped)
        target_mapper = target_relation.get("mapped_by", None)
        mapper = relation.get("mapped_by", target_mapper)

        # in case the "mapper" was correctly retrieved, it's time to
        # retrieve the name of the relation (side) that maps the relation
        # this is done by checking the "mapper" against the current entity
        # class, if it fails it must be the "other" side of the relation
        if mapper: mapper_name = mapper == cls and relation_name or reverse

        # checks the target relation for the is "mapper" attribute, in case
        # it's set the "mapper" class is considered to be the target
        # entity class (flag for enabling), this will update the "mapper"
        # and "mapper" name values
        target_is_mapper = target_relation.get("is_mapper", False)
        mapper = target_is_mapper and target_class or mapper
        mapper_name = target_is_mapper and reverse or mapper_name

        # checks the relation for the is "mapper" attribute, in case
        # it's set the "mapper" class is considered to be the current
        # entity class (flag for enabling), this will update the "mapper"
        # and "mapper" name values
        is_mapper = relation.get("is_mapper", False)
        mapper = is_mapper and cls or mapper
        mapper_name = is_mapper and relation_name or mapper_name

        # creates the correct value to be returned from the method
        return_value = get_mapper_name and (mapper, mapper_name) or mapper

        # returns the correctly configured
        # return value (tuple or base value)
        return return_value

    @classmethod
    def get_reverse(cls, relation_name):
        """
        Retrieves the name of the reverse side of the relation.
        The reverse side of the relation is name of the relation
        in the target class.

        In case the reverse name is not defined in the entity model
        heuristics are used to try to deduct a proper name.

        :type relation_name: String
        :param relation_name: The name of the relation in the current
        entity class.
        :rtype: String
        :return: The reverse name of the relation, name of the relation
        in the target class.
        """

        # retrieves the relation associates with the relation
        # name, this should retrieve the relation meta information
        relation = cls.get_relation(relation_name)

        # retrieves the names map to resolve the relation name
        # into the appropriate (concrete) class that holds the
        # relation, this may be used for the default reverse name
        names_map = cls.get_names_map()
        relation_class = names_map.get(relation_name, cls)

        # retrieves the table name of the entity model and uses
        # it as the default reverse name in case no reverse is
        # found in the relation meta information
        table_name = relation_class.get_name()
        reverse_name = relation.get("reverse", table_name)

        # returns the reverse name of the relation
        # (this is the name of the attribute in the
        # reverse side of the relation)
        return reverse_name

    @classmethod
    def is_to_many(cls, relation_name):
        """
        Checks if the relation with the given name is of
        type "to many".

        The checking of the relation is a simple an inexpensive
        operation.

        :type relation_name: String
        :param relation_name: The name of the relation to be
        tested for to many relationship.
        :rtype: bool
        :return: The result of the to many type relationship
        in the requested relation.
        """

        # retrieves the relation information for the relation
        # and then uses this meta information map to check
        # the type of the relation
        relation = cls.get_relation(relation_name)
        is_to_many = relation.get("type", None) == "to-many"

        # returns the result of the is to many relation
        # type test
        return is_to_many

    @classmethod
    def get_target(cls, relation_name):
        """
        Retrieves the target (class) for the relation with
        the given (attribute) name.

        This method assumes that if the "mapper" class is
        defined for the relation and the target attribute
        is not, the mapped class is the target of the relation.

        :type relation_name: String
        :param relation_name: The name of the relation to
        retrieve the target (class).
        :rtype: Entity
        :return: The target (class) for the requested relation.
        """

        # retrieves the relation (attributes) for the
        # relation name and then retrieves the target
        # class of the relation, uses the "mapper" in case
        # no target class is found
        relation = cls.get_relation(relation_name)
        mapper = relation.get("mapped_by", cls)
        target_class = relation.get("target", mapper)

        # returns the target class of the relation
        return target_class

    @classmethod
    def get_relation(cls, relation_name, raise_exception = False):
        """
        Retrieves the relation (attributes) for the relation
        with the given name.
        The relation attributes should be stored in the appropriate
        static method "inside" the entity class.

        :type relation_name: String
        :param relation_name: The name of the relation to retrieve
        the attributes (map).
        :type raise_exception: bool
        :param raise_exception: If an exception should be raised in
        case no relation attributes are present.
        :rtype: Dictionary
        :return: The map containing the various attributes for the requested
        relation in the class.
        """

        # in case the class contains the relations attributes method in
        # the "old fashioned" mode
        if hasattr(cls, "get_relation_attributes_" + relation_name):
            # retrieves the "old fashioned" relation attribute method
            # to be called to retrieve the attributes of the relation
            method = getattr(cls, "get_relation_attributes_" + relation_name)
        # in case the class contains the relations attributes method in
        # the "new fashioned" mode
        elif hasattr(cls, "_relation_" + relation_name):
            # retrieves the "new fashioned" relation attribute method
            # to be called to retrieve the attributes of the relation
            method = getattr(cls, "_relation_" + relation_name)
        # otherwise it's not possible to retrieve the relation
        # attributes, because there is no relation method, if the
        # raise exception is active, should raise exception
        elif raise_exception:
            # raises an entity manager missing relation method exception
            raise exceptions.MissingRelationMethod("'%s' method not found" % relation_name)
        # otherwise the relation is not present and the exception should
        # not be raise, return a empty descriptor
        else:
            # returns an empty relation descriptor, in order to avoid
            # raising an exception
            return {}

        # returns the result of calling the relation
        # attributes method
        return method()

    @classmethod
    def is_reference(cls):
        """
        Checks if the current entity class is in fact a "data
        reference" entity class.

        The "data reference" entity class are stubs that are used
        as place holders for a latter definition of the "real"
        entity classes.
        They are useful for situations where loose coupling is
        required, in a modularity fashion.

        :rtype: bool
        :return: If the current entity model is in fact a "data
        reference" entity class.
        """

        # in case the current entity class does not
        # contains the data reference attribute, it's
        # not a data reference
        if not hasattr(cls, "data_reference"):
            # returns invalid, the current entity
            # class does not contains the data reference
            # attribute (it cannot be a reference)
            return False

        # checks the value of the data reference attribute
        # as the is (data) reference result value and return
        # it to the calling method
        is_reference = getattr(cls, "data_reference")
        return is_reference

    @classmethod
    def _attr(cls, instance, name, default = None):
        """
        Retrieves the value of an attribute from the provided
        name, the provided instance may be both a map or a class
        based instance and the value is returned using the appropriate
        accessor method.

        In case no value is retrieved from the provided instance
        the default value is retrieved instead.

        Note that in case the instance type is model and the value
        is a lazy load relation the relation will be loaded.

        :type instance: Object/Dictionary
        :param instance: The object or map structure to be used
        to retrieve the attribute value.
        :type name: String
        :param name: The name of the attribute to be retrieved.
        :type default: Object
        :param default: The default to be used in case no value
        is retrieved for the provide name.
        :rtype: Object
        :return: The value of the attribute to be retrieved.
        """

        # verifies if the provided instance is not valid/unset,
        # if that's the case the default value is returned
        if instance == None: return default

        # retrieves the type of the provided instance
        # it can be both a map or a concrete object
        # from a defined model class
        instance_type = type(instance)

        # in case the provided instance is a map the value
        # is retrieve using the normal map accessor otherwise
        # reflection is used to retrieve the instance attribute
        if instance_type == dict: return instance.get(name, default)
        else: return instance.get_value(name, default = default, load_lazy = True)

    @classmethod
    def _get_bases(cls):
        """
        Retrieves the complete set of base (parent) classes for
        the current class, this method is safe as it removes any
        class that does not inherit from the entity class.

        :rtype: List/Tuple
        :return: The set containing the various bases classes for
        the current class that are considered valid.
        """

        # retrieves the complete set of base classes for
        # the current class and in case the object is not
        # the bases set returns the set immediately
        bases = cls.__bases__
        if not object in bases: return bases

        # converts the base classes into a list and removes
        # the object class from it, then returns the new bases
        # list (without the object class)
        bases = list(bases)
        bases.remove(object)
        return bases

    def reset(self):
        """
        Resets the current entity by removing all the relation values
        and setting them as lazy loaded attributes.

        This operation is useful for situations where a simple vision
        on the entity is required in order to avoid mixed scope issues.
        """

        # retrieves the entity class associated with the current
        # entity and then uses it to retrieves the complete set
        # of relations for the entity hierarchy
        entity_class = self.__class__
        all_relations = entity_class.get_all_relations()

        # iterates over all the relations and sets the entity
        # attributes for them as lazy loaded values
        for relation in all_relations:
            setattr(self, relation, colony.Lazy)

    def reset_cache(self):
        """
        Resets the entitie's cache for the current instance so that any
        access to the data source will be used in "real mode" avoiding any
        usage of an in memory view of objects.

        This call may be required to avoid outdated and erroneous values
        coming from data source access operations.
        """

        self._entities = {}

    def use_scope(self, scope_entity):
        """"
        Sets (uses) the scope and entities map attributes in the current
        entity copying them from the given entity considered as scope
        entity (the one to be used as base in diffusion scope context).

        This operation is extremely useful for when propagation of scope
        is important for coherent persistence.

        Note that as part of this operation the "hidden" entities map
        will be propagated, meaning that the cache scope is propagated.

        :type scope_entity: Entity
        :param scope_entity: The entity to be used as the base for the
        diffusion scope. The new entity is going to use the scope entity
        and copy it's entities map and scope map.
        """

        self._entities = scope_entity._entities
        self._scope = scope_entity._scope

    def force_scope(self):
        """
        Forces the current instance to be present in the current scope
        and entities list, independently of its current persistence status.

        This method is useful for situations where a newly created instance
        reference (with the proper identifier set) is meant to be set in
        the diffusion scope for usage by other. By default this instance
        would not be present in the scope.

        The usage of this method should imply care, because if the current
        instance is set in the scope and it does not contains the complete
        set of attributes, it may not reflect a valid representation of the
        entity in the data source.

        This method contains some of the behavior expected by the entity
        manager enable method, so this may be considered private behavior.
        """

        # tries to retrieve the value of the identifier attribute
        # of the current instance in case it's not present the method
        # fails silently
        id_value = self.get_id_value()
        if not id_value: return

        # retrieves the entity class associated with the
        # current entity
        entity_class = self.__class__

        # sets the entity in the entities map, first verifies
        # if the class is present and if is not creates a new
        # map to hold the various entities
        if not entity_class in self._entities: self._entities[entity_class] = {}
        self._entities[entity_class][id_value] = self

    def attach(self, force = True):
        """
        Attaches the current entity to the data source (on-line)
        the current diffusion scope is changed into attached state.

        This method should affect the complete diffusion scope and
        not only the current entity.

        The attach operation may used as a stack oriented operation
        and as such the open/close levels of the attaching must be
        respected in order to maintain coherence in the attaching.
        If such behavior is meant to be ignored the force flag should
        be set to false (enabling the usage of the stack).

        :type force: bool
        :param force: Flag that controls if the attaching should be
        forced or if the stack oriented operation should be respected
        and if the one level is required for attaching.
        """

        # retrieves and updates the attach level to increment
        # it according to the attach operation definition
        attach_level = self._scope.get("attach_level", 0)
        attach_level += 1

        # in case the force flag is set the attach level is
        # set to the minimum required for attaching (forces it)
        if force: attach_level = 1

        # updates the attached and attach level values in the
        # scope definition map
        self._scope["attached"] = attach_level > 0
        self._scope["attach_level"] = attach_level

    def detach(self, force = True, reset = False):
        """
        Detaches the current entity from the data source (off-line)
        the current diffusion scope is changed into detached state.

        This method should affect the complete diffusion scope and
        not only the current entity.

        The detach operation may used as a stack oriented operation
        and as such the open/close levels of the attaching must be
        respected in order to maintain coherence in the attaching.
        If such behavior is meant to be ignored the force flag should
        be set to false (enabling the usage of the stack).

        An optional flag controls if the entity should have the relation
        defaulted (reseted) after the detach operation.

        :type force: bool
        :param force: Flag that controls if the detaching should be
        forced or if the stack oriented operation should be respected
        and if the zero level is required for detaching.
        :type reset: bool
        :param reset: Flag that controls if the entity should have the
        relations removed (set as lazy loaded) after the detach operation.
        """

        # retrieves and updates the attach level to decrement
        # it according to the detach operation definition
        attach_level = self._scope.get("attach_level", 1)
        attach_level -= 1

        # in case the force flag is set the attach level is
        # set to the minimum required for detaching (forces it)
        if force: attach_level = 0

        # updates the attached and attach level values in the
        # scope definition map
        self._scope["attached"] = attach_level > 0
        self._scope["attach_level"] = attach_level

        # resets the current structure, this operation removes
        # all the current relations, useful in order to avoid
        # mixed scopes in relations
        reset and self.reset()

    def attach_l(self, force = True):
        """
        Attaches the current entity to the data source (on-line)
        the current scope is not changed as this operation is
        considered local to the entity.

        The attach operation may used as a stack oriented operation
        and as such the open/close levels of the attaching must be
        respected in order to maintain coherence in the attaching.
        If such behavior is meant to be ignored the force flag should
        be set to false (enabling the usage of the stack).

        :type force: bool
        :param force: Flag that controls if the attaching should be
        forced or if the stack oriented operation should be respected
        and if the one level is required for attaching.
        """

        # retrieves and updates the attach level to increment
        # it according to the attach operation definition
        attach_level = self._attach_level or 0
        attach_level += 1

        # in case the force flag is set the attach level is
        # set to the minimum required for attaching (forces it)
        if force: attach_level = 1

        # updates the attached and attach level values in the
        # current entity
        self._attached = attach_level > 0
        self._attach_level = attach_level

    def detach_l(self, force = True, reset = False):
        """
        Detaches the current entity from the data source (off-line)
        the current scope is not changed as this operation is
        considered local to the entity.

        The detach operation may used as a stack oriented operation
        and as such the open/close levels of the attaching must be
        respected in order to maintain coherence in the attaching.
        If such behavior is meant to be ignored the force flag should
        be set to false (enabling the usage of the stack).

        An optional flag controls if the entity should have the relation
        defaulted (reseted) after the detach operation.

        :type force: bool
        :param force: Flag that controls if the detaching should be
        forced or if the stack oriented operation should be respected
        and if the zero level is required for detaching.
        :type reset: bool
        :param reset: Flag that controls if the entity should have the
        relations removed (set as lazy loaded) after the detach operation.
        """

        # retrieves and updates the attach level to decrement
        # it according to the detach operation definition
        attach_level = self._attach_level or 1
        attach_level -= 1

        # in case the force flag is set the attach level is
        # set to the minimum required for detaching (forces it)
        if force: attach_level = 0

        # updates the attached and attach level values in the
        # current entity
        self._attached = attach_level > 0
        self._attach_level = attach_level

        # resets the current structure, this operation removes
        # all the current relations, useful in order to avoid
        # mixed scopes in relations
        reset and self.reset()

    def is_attached(self):
        """
        Checks if the current entity is attached to the data
        source (on-line).

        This method is going to access the scope parameters
        to check for the attached information.

        :rtype: bool
        :return: If the current entity is attached to the
        data source (on-line).
        """

        is_attached = self._attached and self._scope.get("attached", True)
        return is_attached

    def get_map(self, recursive = True):
        """
        Retrieves a map containing the "exact" same data
        representative of this entity.

        The retrieved map may contain the complete set
        of relations for the entity or only the first level.

        :type recursive: bool
        :param recursive: If the entity relations for the
        current level should be included in the returning map.
        :rtype: Dictionary
        :return: The map representation of the current entity
        including the relation in case the recursion is required.
        """

        # creates the map structure that will load the data
        # representing the current entity
        map = {}

        # retrieves the entity class from the current entity to
        # be used in class level methods
        entity_class = self.__class__

        # retrieves the names map containing the complete set of
        # names associated with the class level of owning
        names_map = self.get_names_map()

        # iterates over all the names in the names map to retrieve
        # the associated values and set them in the map
        for name in names_map:
            # check if the current name contains a value in the
            # model and in case it does not continues the loop
            has_value = self.has_value(name)
            if not has_value: continue

            # checks if the current name refers a relation in the
            # model and in case it does and the current mapping
            # mode is not recursive continues the loop, not going
            # to step into the recursive mode
            is_relation = entity_class.is_relation(name)
            if is_relation and not recursive: continue

            # retrieves the value for the current name in the mode
            # (it may be a sequence or a value)
            value = self.get_value(name)

            # in case the current name refers a relation and there's
            # a valid value recursive approach applies
            if is_relation and value:
                # checks if the current name refers a to many relation
                # and in case it does serializes the various elements
                # contained in it, otherwise serializes only the value
                # because no sequence exists
                is_to_many = entity_class.is_to_many(name)
                if is_to_many: value = [value.get_map(recursive = recursive) for value in value]
                else: value = value.get_map(recursive = recursive)

            # sets the current value in iteration (already converted
            # into the map mode) in the current map
            map[name] = value

        # sets the entity class name as the class attribute for
        # the current map structure level, note that conversion
        # is made into unicode for compatibility reasons
        map["_class"] = colony.legacy.UNICODE(entity_class.__name__)

        # iterates over all the set of reserved names to update
        # the map value with their values
        for name in RESERVED_NAMES:
            # checks if the current model contains the current
            # reserved name value set in case it does not continues
            # the loop not possible to set the value
            if not hasattr(self, name): continue

            # retrieves the reserved value and sets it in the
            # current map for setting
            value = getattr(self, name)
            map[name] = value

        # returns the completely constructed map to the called
        # method, it's now completely populated
        return map

    def nullify(self, recursive = False):
        """
        "Nullifies" the current entity instance by setting all
        the undefined values of it as none, so that a reference
        to it will returned none instead of the class definition.

        An optional flag controls if the nullify process should
        be run in a recursive way on the relations.

        This is useful for situations where access to the entity
        class attributes is not the wanted behavior.

        :type recursive: bool
        :param recursive: Flag controlling if the nullify process
        should be run over all the relations in the current entity.
        """

        # retrieves the entity class associated with the
        # current entity, to retrieve the names map
        entity_class = self.__class__

        # retrieves the complete set of names for
        # the current entity, to be able to iterate
        # over them and set the undefined values as
        # null (better description)
        names_map = entity_class.get_names_map()

        # iterates over all the names in the current
        # entity to set the ones that are undefined
        # as null (none)
        for name in names_map:
            # in case the current instance already has
            # the value (no need to change id) otherwise
            # sets the value as none
            if self.has_value(name): continue
            setattr(self, name, None)

        # in case the recursive flag is set, runs the
        # nullify recursive step
        recursive and self.nullify_recursive()

    def nullify_recursive(self):
        # retrieves the entity class associated with the
        # current entity, to retrieve the names map
        entity_class = self.__class__

        # retrieves the complete set of relations
        # for the current instance so that is possible
        # to run the
        all_relations = entity_class.get_all_relations()

        # iterates over all the relations in the current
        # entity to nullify them in a recursive fashion
        for relation in all_relations:
            # retrieves the relation value, avoiding
            # the loading of a lazy relation, in case
            # the retrieved value is not set continue
            # the loop (no need to nullify)
            relation_value = self.get_value(relation)
            if relation_value == None: continue

            # checks if the relation is of type to many
            # and in case it's not creates a sequence
            # with the single value
            is_to_many = entity_class.is_to_many(relation)
            if not is_to_many: relation_value = [relation_value]

            # iterates over all the relation values to run
            # the nullify process over them (recursive step)
            for _relation_value in relation_value: _relation_value.nullify(True)

    def get_data_state(self):
        return self.data_state

    def get_fields(self):
        # retrieves the dictionary of names of
        # the current entity as the set of fields
        # (global fields list to be filtered)
        fields = self.__dict__

        # creates the map that will hold the "final"
        # set of fields indexed by their name (key)
        # (only the fields passing the filter)
        _fields = {}

        # iterates over all the fields present in
        # the "original" fields dictionary to filter
        # them and set them in the fields map
        for key, value in colony.legacy.iteritems(fields):
            # in case the key is not valid according
            # to the invalid names list, continues
            # the loop the current item is not valid
            # (invalid name)
            if key in INVALID_NAMES: continue

            # in case the key value is completely based in upper case letters
            # characters it must be ignored as it is a constant (invalid name)
            if key.isupper(): continue

            # in case the value type is not valid as
            # a field (function or method) continues the
            # loop, functions or method are not items
            if type(value) in (types.FunctionType, types.MethodType, staticmethod, classmethod): continue

            # sets the value in the map of fields
            # for the current key value
            _fields[key] = value

        # returns the final map of fields, containing
        # the various fields indexed by their key (name)
        return _fields

    def get_id_value(self):
        # retrieves the (entity) class for the current
        # entity instance and then uses it to retrieve
        # the name of the id attribute
        cls = self.__class__
        id_name = cls.get_id()

        # retrieves the id attribute value from the current
        # entity using the id name retrieved from the class
        return self.get_value(id_name)

    def set_id_value(self, value):
        # retrieves the (entity) class for the current
        # entity instance and then uses it to retrieve
        # the name of the id attribute
        cls = self.__class__
        id_name = cls.get_id()

        # sets the id attribute value "into" the current
        # entity using the id name retrieved from the class
        setattr(self, id_name, value)

    def has_id_value(self):
        # retrieves the current id value from the current
        # entity, it's going to be checked for nulls
        id_value = self.get_id_value()

        # returns the result of the comparison of the id
        # value against the none value (if the id value is
        # not none id value is considered to be set)
        return not id_value == None

    def has_value(self, name):
        return name in self.__dict__

    def get_value(self, name, default = None, load_lazy = False):
        # in case the current entity contains a
        # value for the attribute name (simple
        # case) it's returned normally
        if self.has_value(name):
            # returns the attribute value from
            # the current entity (normal retrieval)
            return getattr(self, name)

        # in case the load lazy flag is set and the
        # current name refers a relation, it can be
        # lazy loaded and returned (query executed)
        if load_lazy and self.__class__.is_relation(name):
            # loads the lazy loaded relation name
            # and returns it's value
            return self._load_lazy(name)

        # returns an invalid (default) value, not possible to
        # return a relation using any of the approaches
        return default

    def set_value(self, name, value):
        # sets the attribute in the current
        # entity instance for the provided name
        # and for the requested value
        setattr(self, name, value)

    def delete_value(self, name):
        # in case the current entity instance does
        # not contains the name it's impossible to
        # delete it from it
        if not self.has_value(name):
            # returns immediately it's impossible to
            # delete an inexistent value
            return

        # deletes the attribute containing the request
        # attribute (attribute removal)
        delattr(self, name)

    def has_unmapped_relations(self, entity_class):
        """
        Checks if the current entity contains relations set
        at the provided class level.

        This is useful to check if the entity is modified at
        an indirect (unmapped) level to update the modified time
        (_mtime) attribute in the update and save operations.

        This is an expensive operation, and so it must be used
        carefully and in localized situations.

        :type entity_class: EntityClass
        :param entity_class: The entity class to be used as
        reference for the checking, this should be the parent
        class level to be checked.
        :rtype: bool
        :return: If the current entity contains unmapped relation
        at the provided entity class parent level.
        """

        # retrieves the complete set of unmapped relation for
        # the entity class provided for parent level reference
        unmapped_relations = entity_class.get_unmapped_relations()

        # iterates over all the unmapped relations to check if
        # their value exists in the current entity
        for unmapped_relation in unmapped_relations:
            # in case the current entity does not contains the unmapped
            # relation continue the loop (tries to find more) otherwise
            # return valid (contains unmapped relations)
            if not self.has_value(unmapped_relation): continue
            return True

        # returns invalid (the current entity does not
        # contains unmapped relations)
        return False

    def validate_s(self):
        """
        Runs the complete set of validations associated with the
        save operation for the entity.

        Note that different validation operations should performed
        for save and update operations.
        """

        self.validate_mandatory_s()

    def validate_u(self):
        """
        Runs the complete set of validations associated with the
        update operation for the entity.

        Note that different validation operations should performed
        for save and update operations.
        """

        self.validate_mandatory_u()

    def validate_mandatory_s(self):
        # retrieves the entity class associated with
        # the current entity to be used to access class
        # level methods
        entity_class = self.__class__

        # retrieves the map that contains the field names
        # associated with the mandatory field, only the
        # fields that are considered mandatory are present
        # on this map (mandatory bit mask)
        mandatory_map = entity_class.get_mandatory_map()

        # iterates over the complete set of names in the
        # mandatory map in order to validate them as defined
        for key in mandatory_map:
            # retrieves the value for the current key defaulting
            # to none in case it's not set (or lazy loaded) and
            # then continues the loop in case the value is valid
            # (not none)
            value = self.get_value(key, default = None)
            if not value == None: continue

            # raises a validation error for the missing of the
            # mandatory field
            raise exceptions.ValidationError(
                "missing mandatory field '%s', for entity '%s'" %
                (key, entity_class.__name__),
                context = self
            )

    def validate_mandatory_u(self):
        # retrieves the entity class associated with
        # the current entity to be used to access class
        # level methods
        entity_class = self.__class__

        # retrieves the map that contains the field names
        # associated with the mandatory field, only the
        # fields that are considered mandatory are present
        # on this map (mandatory bit mask)
        mandatory_map = entity_class.get_mandatory_map()

        # iterates over the complete set of names in the
        # mandatory map in order to validate them as defined
        for key in mandatory_map:
            # retrieves the value for the current key defaulting
            # to true (valid) in case it's not set (or lazy loaded)
            # and then continues the loop in case the value is valid
            # (not none) or in case the value is lazy loaded
            value = self.get_value(key, default = True)
            if not value == None: continue
            if value == colony.Lazy: continue

            # raises a validation error for the missing of the
            # mandatory field
            raise exceptions.ValidationError(
                "missing mandatory fields '%s', for entity '%s'" %
                (key, entity_class.__name__),
                context = self
            )

    def validate_value(self, name, value = None, force = False):
        """
        Validates both the name and the associated value
        currently present in the entity.

        The validation of the name consists in the matching
        of it against the entity class specification for the
        name, it must exists.

        The validation for the value is the checking that the
        type of it is valid according to the entity class
        specification (type checking).

        In case the force flag is not set and the value contains a
        value considered invalid the value is retrieved using the
        default value retrieval system present in the entity.

        :type name: String
        :param name: The name of the attribute to be validated
        against the specification.
        :type value: Object
        :param value: The optional value that may be used to
        override the current entity associated value for
        validation.
        :type force: bool
        :param force: Flag controlling if the value must be used
        even if it contains a value considered invalid (none, false,
        or any other evaluating to false).
        """

        # validates that the name exists defined
        # in the current class specification using
        # the proper class method
        self.__class__._validate_name(name)

        # in case the value is not set retrieves it using
        # the normal value retrieval and validates it
        # accordingly, using the proper class method,
        # (the method validates that the type in the value
        # is correct according to the entity definition)
        # only retrieves the value in case the force (value)
        # flag is not set
        if value == None and not force: value = self.get_value(name)
        self.__class__._validate_value(name, value)

    def validate_set(self, name, value = None, force = False):
        """
        Validates that the value for the attribute with the given
        is set, according to the entity specification.

        In case the attribute value is not set a validation error
        is raised to avoid any security breach while using the
        entity manager.

        This is a helpful method for assertions of security in
        the entity classes.

        In case the force flag is not set and the value contains a
        value considered invalid the value is retrieved using the
        default value retrieval system present in the entity.

        :type name: String
        :param name: The name of the attribute to be validated
        for set in the current entity.
        :type value: String
        :param value: The value of the attribute to be validated
        for set in the current entity.
        :type force: bool
        :param force: Flag controlling if the value must be used
        even if it contains a value considered invalid (none, false,
        or any other evaluating to false).
        """

        if value == None and not force: value = self.get_value(name)
        self.__class__._validate_set(name, value)

    def validate_sequence(self, name, value = None, force = False):
        """
        Validates that the value for the attribute with the given
        is a relation, according to the entity specification.

        In case the attribute value is not a relation a validation error
        is raised to avoid any security breach while using the
        entity manager.

        This is a helpful method for assertions of security in
        the entity classes.

        In case the force flag is not set and the value contains a
        value considered invalid the value is retrieved using the
        default value retrieval system present in the entity.

        :type name: String
        :param name: The name of the attribute to be validated
        for relation in the current entity.
        :type value: String
        :param value: The value of the attribute to be validated
        for relation in the current entity.
        """

        if value == None and not force: value = self.get_value(name)
        self.__class__._validate_sequence(name, value)

    def validate_relation_value(self, name, value = None, force = False):
        """
        Validates that the value for the attribute with the given
        contains a valid relation, according to the entity specification.

        In case the attribute value does not contain a valid relation
        a relation validation error is raised to avoid any security breach
        while using the  entity manager.

        This is a helpful method for assertions of security in
        the entity classes.

        :type name: String
        :param name: The name of the attribute to be validated
        for relation in the current entity class.
        :type value: String
        :param value: The value of the attribute to be validated
        for relation in the current entity class.
        :type force: bool
        :param force: Flag controlling if the value must be used
        even if it contains a value considered invalid (none, false,
        or any other evaluating to false).
        """

        if value == None and not force: value = self.get_value(name)
        self.__class__._validate_relation_value(name, value, self._entity_manager)

    def get_sql_value(self, name, value = None, force = False):
        # retrieves the value of the attribute for
        # the provided name, (the value is null in
        # case no value is found) in case the value
        # is not valid and the force flag is not set
        # uses the normal value retriever from the entity
        if value == None and not force: value = self.get_value(name)

        # retrieves the SQL value for the name and value
        # using the class method (forwarding)
        sql_value = self.__class__._get_sql_value(name, value)

        # returns the converted SQL value
        return sql_value

    def set_sql_value(self, name, sql_value, encoding = None):
        value = self.__class__._from_sql_value(name, sql_value, encoding)
        setattr(self, name, value)

    def from_sql_value(self, name, sql_value, encoding = None):
        value = self.__class__._from_sql_value(name, sql_value, encoding)
        return value

    def to_map(self, entity_class = None, depth = 0, special = True):
        """
        Converts the current entity (instance) into a linear
        (non recursive) map representation with a random
        depth of recursion.

        The map representation may be used in situations where
        recursion is not correctly handled or just in situation
        where no class based representation is required.

        The optional entity class attribute may be used to set
        the parent level of the current entity to be serialized.
        In case none is provided the bottom parent level of the
        current is used.

        :type entity_class: EntityClass
        :param entity_class: The entity class to be used as
        reference parent level for the map conversion.
        :type depth: int
        :param depth: The depth (recursion) level to be used in
        the conversion of relations for the entity.
        :type special: bool
        :param special: If the special attributes of the model
        instance should also be serialized if present.
        :rtype: Dictionary
        :return: The map representing the current instance, this
        map should be safe to be serialized (no loops).
        """

        # creates the map to hold all the value for the
        # entity to be converted, this is the value to be
        # returned at the end of the conversion
        map = {}

        # retrieves the entity class (level) to be used
        # in the conversion to the map structure
        entity_class = entity_class or self.__class__

        # in case the special flag is set the special attributes
        # of the current instance should also be serialized, so
        # that even information like the class type is included
        if special: map["_class"] = self.__class__.__name__
        if special and hasattr(self, "mtime"): map["_mtime"] = self.mtime

        # retrieves the id name and values and sets the id
        # value in the map (this is a mandatory field event
        # if it's not present in the current parent level)
        id_name = entity_class.get_id()
        id_value = self.get_id_value()
        map[id_name] = id_value

        # retrieves all the (symbol) names for the current
        # entity, this value are going to
        names = entity_class.get_names_map()

        # iterates over all the names in the names map to
        # correctly convert them into the appropriate the
        # correct value and set them in the map
        for name, _value in colony.legacy.iteritems(names):
            # verifies if the current name refers a relation
            # and if that's the case skips the current step
            # as relations are not meant to be serialized
            # at this state of the loop
            is_relation = entity_class.is_relation(name)
            if is_relation: continue

            # retrieves the value for the current
            # name and sets it in the map
            value = self.get_value(name)
            map[name] = value

        # in case the current depth level does not allow
        # the conversion of the relations, must return
        # the map immediately
        if depth == 0: return map

        # retrieves all the relations from the entity class
        # used for the conversion, these are the relations
        # that are going to be converted and set on the map
        relations = entity_class.get_all_relations()

        # iterates over all the relations to convert them
        # into the appropriate map representation and set
        # them in the current entitie's map
        for relation in relations:
            # retrieves the target class for the current
            # relation and then checks if the current relation
            # is of type to many
            target_class = entity_class.get_target(relation)
            is_to_many = entity_class.is_to_many(relation)

            # in case the relation is of type to many
            # a sequence must be handled and many objects
            # must be converted into the map representation
            if is_to_many:
                # retrieves the value of the relation loading a lazy
                # loaded relation (in case it's necessary) in case
                # the returned value is still lazy the current iteration
                # loop is skipped to avoid storing invalid values
                value = self.get_value(relation, load_lazy = True)
                if colony.is_lazy(value): continue

                # creates the relations value as a new empty
                # list that is going to be populated with the
                # various map values for the relation
                relation_value = []

                # "casts" a possible invalid value into an
                # empty list to provide compatibility with
                # the iteration
                value = [] if value == None else value

                # iterates over all the values in the to many
                # relation to convert them into maps
                for _value in value:
                    # in case the value is not valid, or
                    # not set it cannot be converted into
                    # a valid map, must skip conversion
                    if not _value: continue

                    # converts the value into a map and set it as
                    # the relation value in the relation value list
                    _relation_value = _value.to_map(
                        entity_class = target_class,
                        depth = depth - 1,
                        special = special
                    )
                    relation_value.append(_relation_value)

            # otherwise it must be a to one relation and only
            # one value must be converted into map and set
            # in the current entity map
            else:
                # retrieves the value of the relation and converts
                # it into the map representation in case it's valid
                # note that the value is verifies to check if it's
                # a lazy loaded value, if that's the case the current
                # relation storage is skipped to avoid problems
                value = self.get_value(relation, load_lazy = True)
                if colony.is_lazy(value): continue
                relation_value = value.to_map(
                    entity_class = target_class,
                    depth = depth - 1,
                    special = special
                ) if value else value

            # sets the relation value (list of maps or map)
            # in the current entity map representation
            map[relation] = relation_value

        # returns the complete map representation
        # for the current entity
        return map

    @classmethod
    def from_map(
        cls,
        map,
        entity_manager,
        entity = None,
        recursive = True,
        set_empty_relations = True,
        entities = None,
        scope = None,
        reset = True,
        set_mtime = True,
        cls_names = None
    ):
        # creates a new entity class from the current
        # class using the current entity manager, no scope
        # or entities map is provided so a new diffusion
        # scope is created
        entity = entity or cls.build(
            entity_manager,
            entities = entities,
            scope = scope
        )

        # in case the reset flag is set the constructor of the
        # model must be "re-called" again so that the default
        # values are set one more time (as expected)
        if reset: entity.__init__()

        # verifies the current status of both the entities
        # and the scope and in case these values are not set
        # set's it for the first time as the entity values
        # so that they are re-used along the various entities
        # that are going to be created as part of the loading
        if entities == None: entities = entity._entities
        if scope == None: scope = entity._scope

        # retrieves the complete set of names from the class
        # to be used to set the correct values into the entity
        # note that if a class for name retrieval is defined
        # only the names at that hierarchy level are retrieved
        # this may be important for performance reasons
        names = cls_names.get_names() if cls_names else cls.get_names_map()

        # iterates over the complete set of entity names to set
        # the associated values into the entity
        for name in names:
            # in case the current name does not exist
            # in the map, must skip the cycle
            if not name in map: continue

            # retrieves the current value for the name to
            # be iterated, this may value may be a sequence
            # in case the current entity is a relation
            value = map[name]

            # in case the current name is relation, need
            # to process it before the setting of the attribute
            # this behavior is only expected when the recursive
            # flag is set (recursive approach)
            if cls.is_relation(name) and recursive:
                # in case the value is invalid or in case it's
                # an empty sequence and the set empty relations
                # flag is not set (no need to set the relation)
                if not value and not set_empty_relations: continue

                # in case the relation is of type to many, must
                # process the sequence of values in it, otherwise
                # a single values is processed (recursion step)
                if cls.is_to_many(name):
                    # creates the list that will hold the complete
                    # set of entity values converted from the various
                    # maps representing the relation entities
                    values = []

                    # iterates over all the (relation) values to be
                    # converted into entity objects
                    for _value in value:
                        # tries to retrieve the name of the class from the map
                        # then if successful uses it to retrieve the target class
                        # otherwise retrieves the target class from the relation information
                        class_name = _value and _value.get("_class", None)
                        target_class = class_name and entity_manager.get_entity(class_name) or cls.get_target(name)

                        # converts the map into an entity object (in case the value is valid)
                        # and the adds it to the list of entity values the new object will
                        # re-use the same set of entities and scope from the top level one
                        _entity = _value and target_class.from_map(
                            _value,
                            entity_manager,
                            recursive = recursive,
                            set_empty_relations = set_empty_relations,
                            entities = entities,
                            scope = scope,
                            set_mtime = set_mtime
                        )
                        values.append(_entity)

                    # sets the sequence of values as the current value reference
                    # to be set in the entity
                    value = values

                # otherwise the relation must be of type to one and only
                # one value must be parsed at one time
                else:
                    # tries to retrieve the name of the class from the map
                    # then if successful uses it to retrieve the target class
                    # otherwise retrieves the target class from the relation information
                    class_name = value and value.get("_class", None)
                    target_class = class_name and entity_manager.get_entity(class_name) or cls.get_target(name)

                    # converts the map into an entity object (in case the value is valid)
                    # and sets it as the value to be set in the entity, note that the scope
                    # is re-used from the top level entity to the bottom one
                    value = value and target_class.from_map(
                        value,
                        entity_manager,
                        recursive = recursive,
                        set_empty_relations = set_empty_relations,
                        entities = entities,
                        scope = scope,
                        set_mtime = set_mtime
                    )

            # sets the correct value associated with the name in
            # the entity (value attribution)
            setattr(entity, name, value)

        # retrieves the id name from the class, and uses it to set
        # the appropriate value into the entity
        id = cls.get_id()
        setattr(entity, id, map[id])

        # tries to retrieve the modification time from the map
        # in case it exists sets it in the entity to be used
        # as reference for possible insertions, this is only
        # applied in case the set modification time flag is set
        _mtime = map.get("_mtime", None)
        if set_mtime and _mtime:
            setattr(entity, "_mtime", _mtime)
            setattr(entity, "mtime", _mtime)

        # returns the "just" updated entity (entity with the
        # map values)
        return entity

    @classmethod
    def _get_data_type(cls, name, resolve_relations = True):
        # retrieves the "abstract" information
        # on the attribute and then uses it to
        # retrieve the data type of the attribute
        attribute = getattr(cls, name)
        attribute_data_type = attribute.get("type", None)

        # in case the "requested" attribute is a relation
        # additional processing must be done to retrieve
        # associated class id attribute type as the attribute
        # data type (the value to be used is the relation value)
        # this processing only occurs in case the resolve relations
        # flag is currently set
        if resolve_relations and attribute_data_type == "relation":
            # retrieves the target class using the relation
            # name and the retrieves the target id name
            target_class = cls.get_target(name)
            target_id = target_class.get_id()

            # retrieves the target id attribute value as the
            # current attribute in order to retrieve the
            # appropriate data type (target id attribute data type)
            attribute = getattr(target_class, target_id)
            attribute_data_type = attribute.get("type", None)

        # returns the "calculated" attribute
        # data type
        return attribute_data_type

    @classmethod
    def _get_sql_value(cls, name, value):
        # in case the name is a reserved one, it's considered
        # to be a special case and the value (must be previously
        # casted according to the SQL syntax) is returned as the
        # valid SQL representation
        if name in RESERVED_NAMES: return str(value)

        # retrieves the (attribute) data type for
        # the attribute with the given name for
        # the current entity class
        data_type = cls._get_data_type(name)

        # in case the value is none a null
        # string must be used, returns the
        # null string immediately
        if value == None: return "null"

        # in case the attribute data type is text,
        # normal separators must be applied
        if data_type in ("text", "string", "data"):
            # for the "special" string data type a truncation operation
            # must be performed in case it overflows the maximum value
            # allowed by the underlying SQL data source
            if data_type == "string" and len(value) > 255: value = value[:255]

            # retrieves the escaped attribute value and
            # returns the escaped attribute value with the
            # string separators
            escaped_value = cls._escape_text(value)
            return "'" + escaped_value + "'"

        # in case the attribute data type is date, the date time
        # structure must be converted to a float value
        elif data_type == "date":
            # retrieves the type from the current value so that it
            # may be used for conditional execution and interpreting
            # of the provided values
            value_type = type(value)

            # in case the attribute is given in the date time format
            if value_type == datetime.datetime:
                # retrieves the date time tuple
                date_time_tuple = value.utctimetuple()

                # creates the date time timestamp and then
                # converts the timestamp to string representation
                date_time_timestamp = calendar.timegm(date_time_tuple)
                date_time_timestamp_string = str(date_time_timestamp)

                # returns the data time timestamp into
                # string representation
                return date_time_timestamp_string
            # in case the attribute value type is an integer
            # or float (must be a timestamp value)
            elif value_type in (int, float):
                # converts the attribute value (integer)
                # into a float value and then converts it
                # into a string representation
                float_value = float(value)
                float_value_string = str(float_value)

                # returns the float attribute value converted
                # into a string
                return float_value_string
            # otherwise it's an unknown value and must be
            # converted "directly" into a string value
            else:
                # converts the attribute value to string
                # (simple conversion) then returns the
                # attribute value converted into string
                value_string = str(value)
                return value_string

        elif data_type == "metadata":
            # retrieves the type from the current value so that it
            # may be used for conditional execution and interpreting
            # of the provided values
            value_type = type(value)

            # in case the value is of type string direct
            # insertion is made into the data source
            if value_type in colony.legacy.STRINGS:
                # escapes the (already string) value and
                # returns it with the string separators
                value_string = cls._escape_text(value)
                return "'" + value + "'"

            # in case the value is of type dictionary the
            # default dump operation must be performed
            elif value_type == dict:
                # dumps the value using the currently selected
                # serialized, then escapes the text and returns
                # the string value with the string separators
                serializer, name = cls.get_serializer()
                value_string = serializer.dumps(value)
                value_string = name + ":" + value_string
                value_string = cls._escape_text(value_string)
                return "'" + value_string + "'"

            # otherwise the default string encoding is used
            # on the value, this is only a fallback strategy
            # and any value going here is considered almost
            # invalid according to specification
            else:
                # uses the default string encoder and then
                # escapes the text and returns it with the
                # string separators
                value_string = str(value)
                value_string = cls._escape_text(value)
                return "'" + value_string + "'"

        # otherwise it must be a default value and it is
        # converted using the default string converter
        else:
            # converts the attribute value to string
            # (simple conversion)
            value_string = str(value)

            # returns the attribute value converted
            # into string
            return value_string

    @classmethod
    def _from_sql_value(cls, name, value, encoding = None):
        # retrieves the (attribute) data type for
        # the attribute with the given name for
        # the current entity class
        data_type = cls._get_data_type(name)

        # in case the value is none, no need to
        # check for the attribute data type for
        # data conversion
        if value == None:
            # returns none immediately, no need
            # to check for the attribute data type
            # for data conversion
            return None

        # in case the data type is text or string
        # it may have to be converted into a neutral
        # unicode string in case it's encoded in the
        # database representation
        if data_type in ("text", "string"):
            # retrieves the type of the values and in case it's
            # string and the encoding value is present decode
            # the value creating an unicode representation of it
            value_type = type(value)
            string_value = encoding and value_type == colony.legacy.BYTES and\
                value.decode(encoding) or value

            # returns the "just" converted string representation
            # (probably an unicode object)
            return string_value

        # in case the attribute data type is integer it must
        # cast as a valid integer (simple casting) so that
        # unexpected data types exist for the current value
        if data_type == "integer":
            integer_value = int(value)
            return integer_value

        # in case the attribute data type is decimal (fixed point)
        # it must be casted into a valid decimal (simple casting)
        # so that unexpected data types exist for the current value
        if data_type == "decimal":
            decimal_value = colony.Decimal(value)
            return decimal_value

        # in case the attribute date type is date
        # it must be converted back from the data
        # source float value into the date time
        # representation (normalized value)
        if data_type == "date":
            # converts the attribute value to float and then
            # loads a date time structure from the given float
            # value (it must be a normalized timestamp), note
            # that in case there's a problem with the casting the
            # default zeroed value is used instead, providing a
            # simple fallback process (required for os like windows)
            value = float(value)
            try: date_time_value = datetime.datetime.utcfromtimestamp(value)
            except ValueError: date_time_value = datetime.datetime.utcfromtimestamp(0)
            except IOError: date_time_value = datetime.datetime.utcfromtimestamp(0)

            # returns the date time (converted) value it may
            # be used in a coherent
            return date_time_value

        # in case the data type id metadata the string
        # value must be unpacked and the associated serializer
        # must be used to create the metadata structure
        if data_type == "metadata":
            try:
                # encodes the value using the serialization
                # encoding and then unpacks the value into
                # the serializer name and the value using
                # it so load the proper/final (meta) value
                value = value if colony.legacy.PYTHON_3 else value.encode("utf-8")
                name, value = value.split(":", 1)
                serializer, _name = cls.get_serializer(name)
                metadata_value = serializer.loads(value)
            except Exception:
                # sets the metadata value as invalid in case
                # an error occurred while unpacking the metadata
                metadata_value = None

            # returns the date time (converted) value it may
            # be used in a coherent
            return metadata_value

        # returns the (attribute) value, the
        # value should represent a converted value
        return value

    @classmethod
    def _cast_value(cls, name, value):
        """
        Casts the provided attribute value expressed as a string into
        the appropriate type defined in the entity class specification.

        This method is useful for situations where a serialization
        processes requires the value to be a string.

        :type name: String
        :param name: The name of the attribute to be used as
        reference to the casting of the values.
        :type value: String
        :param value: The string based value to be converted into
        the correct representation for the attribute referred.
        :rtype: Object
        :return: The casted value in the type expected by the attribute
        defined by the provided name.
        """

        # retrieves the data type associated with the attribute
        # defined by the name, then uses it to convert into the
        # valid python types sequence
        attribute_data_type = cls._get_data_type(name)
        cast_type = PYTHON_CAST_MAP.get(attribute_data_type, None)

        # in case the cast type value is defined uses it to create
        # a new value that is "acceptable" as the conversion for
        # the associated attribute name
        casted_value = cast_type and cast_type(value) or None

        # returns the "final" casted value, that should be handled
        # correctly by the underlying entity manager structure
        return casted_value

    @classmethod
    def _validate_name(cls, name):
        """
        Validates that an attribute with the given name must
        exists in the current entity class.

        In case the attribute does not exists a validation error
        is raised to avoid any security breach while using the
        entity manager.

        This is a helpful method for assertions of security in
        the entity classes.

        :type name: String
        :param name: The name of the attribute to be validated
        for existence in the current entity class.
        """

        # in case the name is a reserved one, it's considered
        # to be valid according to the entity manager structure
        if name in RESERVED_NAMES: return

        # in case the (attribute) name exists in the
        # context of the current entity class, nothing
        # must be done
        if cls.has_name(name): return

        # raises an entity manager validation error, indicating the
        # invalid attribute name for the entity class (this may avoid
        # possible security problems)
        raise exceptions.ValidationError(
            "invalid name '%s', attribute does not exist in '%s'" %
            (name, cls.__name__)
        )

    @classmethod
    def _validate_value(cls, name, value, strict = True):
        """
        Validates that the value for the attribute with the given
        contains a valid type, according to the entity specification.

        In case the attribute value is not valid a validation error
        is raised to avoid any security breach while using the
        entity manager.

        If the strict mode is enabled the warning level data types
        will raise an exception, blocking the loading.

        This is a helpful method for assertions of security in
        the entity classes.

        :type name: String
        :param name: The name of the attribute to be validated
        for correct type in the current entity class.
        :type value: String
        :param value: The value of the attribute to be validated
        for correct type in the current entity class.
        :type strict: bool
        :param strict: If the strict mode of validation should be
        applied meaning more validations.
        """

        # in case the name is a reserved one, it's considered
        # to be valid according to the entity manager structure
        if name in RESERVED_NAMES: return

        # retrieves the (attribute) data type for
        # the attribute with the given name for
        # the current entity class and uses it to
        # retrieve the set of valid python types for
        # the attribute with the current name, note
        # that a waning set of types is also retrieved
        attribute_data_type = cls._get_data_type(name)
        valid_types = PYTHON_TYPES_MAP.get(attribute_data_type, ())
        warn_types = PYTHON_WARN_MAP.get(attribute_data_type, ())

        # retrieves the type of the given value
        # to check it against the list of valid types
        # for the current attribute
        value_type = type(value)

        # verifies if the data type for the value is present
        # in the list of warning data types for the attribute
        # data type, if that's the case and the strict mode
        # is enabled a validation error is raised (cautious)
        if strict and value_type in warn_types:
            raise exceptions.ValidationError(
                "data type '%s' is not perfect for '%s' in '%s'" %\
                (value_type, name, cls.__name__)
            )

        # checks if the current value is not set (considered
        # to be universally valid) in such case the control
        # is returned immediately
        if value == None: return

        # checks if the type of the value is valid (exists
        # in the set of valid types) in such case the control
        # is returned immediately
        if value_type in valid_types: return

        # raises an entity manager validation error, indicating the
        # invalid attribute type for the entity class (this may avoid
        # possible security problems)
        raise exceptions.ValidationError(
            "invalid value for name '%s' in '%s', expected '%s' got base '%s'" %
            (name, cls.__name__, attribute_data_type, value_type)
        )

    @classmethod
    def _validate_set(cls, name, value):
        """
        Validates that the value for the attribute with the given
        is set, according to the entity specification.

        In case the attribute value is not set a validation error
        is raised to avoid any security breach while using the
        entity manager.

        This is a helpful method for assertions of security in
        the entity classes.

        :type name: String
        :param name: The name of the attribute to be validated
        for set in the current entity class.
        :type value: String
        :param value: The value of the attribute to be validated
        for set in the current entity class.
        """

        # in case the value is valid and set the set validation
        # is considered to be fulfilled the control is returned
        # immediately to the calling method
        if not value == None: return

        # raises an entity manager validation error, indicating that
        # the request name is not correctly set in the current entity
        raise exceptions.ValidationError(
            "name '%s' unset for attribute of type '%s', expected attribute set" %
            (name, cls.__name__)
        )

    @classmethod
    def _validate_sequence(cls, name, value):
        """
        Validates that the value for the attribute with the given
        is a relation, according to the entity specification.

        In case the attribute value is not a relation a validation error
        is raised to avoid any security breach while using the
        entity manager.

        This is a helpful method for assertions of security in
        the entity classes.

        :type name: String
        :param name: The name of the attribute to be validated
        for relation in the current entity class.
        :type value: String
        :param value: The value of the attribute to be validated
        for relation in the current entity class.
        """

        # retrieves the class for the value, the provided value
        # must respect the class protocol or else a value error
        # will be raise here
        value_class = value.__class__

        # in case the class for the valuer inherits from the list
        # or from the tuple class the validation is said to be
        # correctly respected, returns control immediately
        if issubclass(value_class, list) or issubclass(value_class, tuple): return

        # raises an entity manager validation error, indicating that
        # the request name is not a valid sequence in the current entity
        raise exceptions.ValidationError(
            "name '%s' is not a valid sequence for attribute of type '%s'" %\
            (name, cls.__name__)
        )

    @classmethod
    def _validate_relation_value(cls, name, value, entity_manager):
        """
        Validates that the value for the attribute with the given
        contains a valid relation, according to the entity specification.

        In case the attribute value does not contain a valid relation
        a relation validation error is raised to avoid any security breach
        while using the  entity manager.

        This is a helpful method for assertions of security in
        the entity classes.

        :type name: String
        :param name: The name of the attribute to be validated
        for relation in the current entity class.
        :type value: String
        :param value: The value of the attribute to be validated
        for relation in the current entity class.
        :type entity_manager: EntityManager
        :param entity_manager: The entity manager to be used for the possible
        reference class resolution (relation class resolution).
        """

        # in case the relation is not set it must be considered to
        # be valid according to the entity manager definition, returns
        # the control immediately
        if value == None: return

        # retrieves the target class for the relation, in order to be
        # able to check if the value represents a class or sub class
        # of the provided value tries to resolve it into the appropriate
        # concrete (real) class in case the resolution fails it's
        # impossible to retrieve (load) the relation information
        # and so an exception must be raised (not possible to validate)
        target_class = cls.get_target(name)
        target_is_reference = target_class.is_reference()
        if target_is_reference: target_class = entity_manager.get_entity(target_class.__name__)
        if not target_class: raise exceptions.RelationValidationError(
            "not possible to find referenced class '%s' for relation '%s'" %\
            (target_class.__name__, name)
        )

        # in case the class of the relation value is compatible
        # with the one defined in the target attribute of the relation
        # no problem occurred
        if issubclass(value.__class__, target_class): return

        # raises a relation validation error, because the relation
        # attribute value must be of type target class or a sub class
        # of it (assertion error)
        raise exceptions.RelationValidationError(
            "invalid class for relation '%s', expected '%s' got '%s'" %\
            (name, target_class.__name__, value.__class__.__name__)
        )

    @classmethod
    def _escape_text(cls, text_value, escape_slash = False, escape_double_quotes = False):
        """
        Escapes the text value in the SQL context.
        This escaping process is important even for
        security reasons.

        This escaping process avoids many of the existing
        SQL injection procedures.

        :type text_value: String
        :param text_value: The text value to be escaped.
        :type escape_slash: bool
        :param escape_slash: If the slash characters should be escaped.
        :type escape_double_quotes: bool
        :param escape_double_quotes: If the double quotes should be escaped.
        :rtype: String
        :return: The escaped text value, according to the SQL
        standard specification.
        """

        # escapes the quote values, repeats them
        # twice (normal SQL escaping sequence)
        escaped_text_value = text_value.replace("'", "''")

        # in case the escape slash flag is set
        # the slash character should be escaped too
        if escape_slash: escaped_text_value = escaped_text_value.replace("\\", "\\\\")

        # in case the escape double quotes flag is set
        # the double quotes should be escaped too
        if escape_double_quotes: escaped_text_value = escaped_text_value.replace("\"", "\"\"")

        # returns the escaped text value
        return escaped_text_value

    @classmethod
    def _items(cls):
        """
        Retrieves the map containing the complete set of elements in the
        class associated with their values.

        This method should comply with the abstract parent interface, no
        abstract parent class should have items and their items should be
        passed to the underlying classes.

        :rtype: Dictionary
        :return: The map containing the complete set of items for the current
        class being selected.
        """

        # initializes to be used to set the various items
        # contained in the class
        items = {}

        # extends the items map with the items present in
        # the current class (no map copy is made)
        items = colony.map_extend(items, cls.__dict__, copy_base_map = False)

        # retrieves the complete set of abstract parent for
        # the current class, so that is possible to add their
        # items to the current set (by iterating over them)
        all_abstract_parents = cls.get_all_abstract_parents()
        for abstract_parent in all_abstract_parents:
            # retrieves the abstract parent items and adds them
            # into the current set of items
            abstract_parent_items = abstract_parent.__dict__
            colony.map_extend(items, abstract_parent_items, copy_base_map = False)

        # returns the map containing the complete set of items
        # for the current class (includes abstract class items)
        return items

    def _start(self):
        """
        Method called upon structure initialization, this
        is going to be called even in situations where just
        the instance is created and no constructor is called.

        Overriding of this method is possible but should be
        done with extreme care.
        """

        # sets the class (name) attribute for the current
        # instance according to the associated class name
        self._class = self.__class__.__name__

        # creates the required maps for the entities and
        # for the scope in case they are required not
        # already set in the entity
        if self._entities == None: self._entities = {}
        if self._scope == None: self._scope = {}

    def _load_lazy(self, name):
        """
        Loads a lazy loaded relation, processes the lazy relation
        retrieving the correct values.

        This method accesses the data source so it's considered
        to be an "expensive" operation.

        :type name: String
        :param name: The name of the relation attribute to be loaded
        from the current lazy state.
        :rtype: Object
        :return: The loaded relation attribute, retrieved from the
        current associated data source.
        """

        # in case the entity manger is not currently loaded in the
        # current model it's not possible to run the loading and
        # so the attribute must be considered to be lazy
        if not self._entity_manager: return colony.Lazy

        # checks if the current entity (and diffusion scope) is
        # attached to the data source in case it's not a lazy
        # loading object is returned (not possible to load it)
        is_attached = self.is_attached()
        if not is_attached: return colony.Lazy

        # retrieves the target class for the (relation name)
        # checks if the target class is a "data reference" and
        # in case it is, tries to resolve it into the appropriate
        # concrete (real) class in case the resolution fails it's
        # impossible to retrieve (load) the relation information
        # and so it must be marked as a lazy relation
        target_class = self.get_target(name)
        target_is_reference = target_class.is_reference()
        if target_is_reference: target_class = self._entity_manager.get_entity(target_class.__name__)
        if not target_class: return colony.Lazy

        # retrieves id value from the entity instance and checks
        # if the value is correctly set in case it's not it's not
        # possible to retrieve (load) the relation must set the
        # relation as lazy loaded
        table_id_value = self.get_id_value()
        if table_id_value == None: return colony.Lazy

        # creates the map of options to load the various
        # entities that are associated with the current
        # entity in the appropriate (reverse) relation
        options = dict(
            eager = (
                name,
            ),
            entities = self._entities,
            scope = self._scope,
            minimal = True,
            cache = True
        )

        # runs the "finding" the appropriate (place holder) entity
        # from which the the proper relation will be extracted, in
        # case not entity is found (error situation)
        _entity = self._entity_manager.get(self.__class__, table_id_value, options)
        if not _entity: raise RuntimeError("Not possible to load entity")

        # in case the retrieved entity does not contain the requested
        # (relation) name and exception should be raised indicating
        # the error to the final/end user or developer
        if not hasattr(_entity, name):
            raise RuntimeError("Relation '%s' not present in entity", name)

        # retrieves the proper relation attribute from the placeholder
        # entity and then sets it under the current instance)
        attribute = getattr(_entity, name)
        setattr(self, name, attribute)

        # returns the attribute that has just been found (this
        # attribute is not going to be "lazy loaded" again)
        return attribute

    def _load_lazy_attr(self, name, force = False):
        """
        Loads a lazy loaded base attribute, this will be used in
        entities that have been loaded using polymorphism and for
        which only a certain level of attributes is loaded.

        Loading the attribute will trigger a concrete loading of
        the entity values and all of them will be updated.

        An optional flag may be used to force the setting of already
        defined/set attributes (from the upper layers in hierarchy).

        This method accesses the data source so it's considered
        to be an "expensive" operation.

        :type name: String
        :param name: The name of the attribute to be used as reference
        in the loading of the concrete class (lazy load).
        :type force: bool
        :param force: If the setting of attributes should be forced
        meaning that attributes that are already set in the entity
        may be overriden by new values from data source, this is
        valid for the upper layers of the class hierarchy.
        :rtype: Object
        :return: The value for the attribute that triggered the concrete
        load of the class (lazy load).
        """

        # in case the entity manger is not currently loaded in the
        # current model it's not possible to run the loading and
        # so the attribute must be considered to be lazy
        if not self._entity_manager: return colony.Lazy

        # checks if the current entity (and diffusion scope) is
        # attached to the data source in case it's not a lazy
        # loading object is returned (not possible to load it)
        is_attached = self.is_attached()
        if not is_attached: return colony.Lazy

        # retrieves id value from the entity instance and checks
        # if the value is correctly set in case it's not it's not
        # possible to retrieve (load) the relation must set the
        # relation as lazy loaded
        table_id_value = self.get_id_value()
        if table_id_value == None: return colony.Lazy

        # retrieves the entity class associated with the current entity
        # to be able to access class level attributes
        entity_class = self.__class__

        # creates the map of options to load the various
        # base value for the concrete entity defined, this way
        # it will be possible to populate all the base names
        options = dict(
            scope = self._scope
        )

        # runs the "finding" the appropriate (place holder) entity
        # then retrieves the attribute from it and retrieves the
        # map of names to be used for the setting
        _entity = self._entity_manager.get(self.__class__, table_id_value, options)
        attribute = getattr(_entity, name)
        names_map = entity_class.get_names_map()

        # iterates over all the names present in the complete
        # entity class hierarchy to update with the new values
        for name in names_map:
            # in case the current name in iteration is
            # not present in the (new) entity no need to
            # retrieve it and set it in the entity
            if not _entity.has_value(name): continue

            # in case the value is already set in the base
            # no duplicate setting should occur (would possibly
            # revert changed to entity), note that in case the
            # force flag is set the value is set the same way
            if self.has_value(name) and not force: continue

            # retrieves the value for the current
            # name in the (new) entity and sets it in
            # the entity to be reloaded (attribute update)
            value = _entity.get_value(name)
            self.set_value(name, value)

        # returns the attribute value that triggered the lazy load
        # of the class concrete values
        return attribute

    def _try_attr(self, name):
        """
        Tries to resolve a calculated (_attr) attribute by checking
        the parent class of the current instance for the presence
        of the requested attribute.

        This method should avoid further calls to the calculated
        attribute in case it has already been calculated for instance.

        This method assumes to be called inside an exception handler
        to provided proper exception re-raising.

        :type name: String
        :param name: The name of the attribute that is going to be
        resolved as a calculated attribute.
        :rtype: Object
        :return: The resolved value calculated using the proper method.
        """

        # retrieves the class reference for the current entity as it's
        # going to be used for the current method resolution strategy
        cls = self.__class__

        # verifies if the (calculated) attribute method for such value
        # exists for the associated class and if that's not true raises
        # the current exception in handling
        has_attr = hasattr(cls, "_attr_" + name)
        if not has_attr: raise

        # sets the initial value for the error flag as false (default
        # value) and then tries to extract the proper attribute method
        error = False
        method = getattr(cls, "_attr_" + name)

        # runs the calculated attribute method and retrieves the associated
        # value setting the error flag in case an exception occurs, otherwise
        # sets the value in the current instance (no more delayed resolution)
        try: value = method(self)
        except Exception: error = True
        else: setattr(self, name, value)

        # in case the error flag is set re-raise the current exception in
        # handling (attribute not found) otherwise returns the resolved value
        if error: raise
        return value

    def _depth(self):
        """
        Retrieves the depth as an integer that is going to be
        used as part of the serialization process for the model
        the more depth provided the more relations serialized.

        This value should be changed carefully to avoid an overload
        of data to be serialized (could pose performance issues).

        :rtype: int
        :return: The depth value as an integer to be used in the
        get state serialization process of the model.
        """

        return 0

    @classmethod
    def get_serializer(cls, name = None):
        # in case the serializers map is not defined triggers the
        # initial loading of the serializer, then in case the serializers
        # list is empty (or invalid) raises the no serializer error
        if SERIALIZERS_MAP == None: load_serializers()
        if not SERIALIZERS: raise exceptions.InvalidSerializerError("no serializer available")

        # in case no (serializer) name is provided the first
        # (and preferred) serializer name is used then retrieves
        # the associated serializer object and in case it fails
        # raises an error
        name = name or SERIALIZERS[0]
        serializer = SERIALIZERS_MAP.get(name, None)
        if not serializer: raise exceptions.InvalidSerializerError("no serializer available for '%s'", name)

        # creates the serializer tuple containing both
        # the serializer object and the name
        serializer_tuple = (serializer, name)
        return serializer_tuple

class rset(list):
    """
    Specialized list that provides a series of utilities
    to handle a result set oriented chunk of data.

    It provides features such as order and header management
    useful for ordered management of large chunks of data.
    """

    header_set = False
    """ Flag controlling if an header has already been
    set for the current result set structure """

    header_h = {}
    """ The hash map that associates each of the
    header names with the index position in the header """

    def __init__(self, base = []):
        """
        Constructor of the class.

        :type base: List
        :param base: The base list to be used as the base
        model for the construction of the new one.
        """

        list.__init__(self, base)

        if hasattr(base, "header_set"): self.header_set = base.header_set
        if hasattr(base, "header_h"): self.header_h = copy.copy(base.header_h)

    def join(self, set):
        """
        Joins the current set with another one provided as
        an argument, both sets must match the same information.

        The order of the header and lines may not be the same
        as a reorder operation will be performed.

        :type set: rset
        :param set: The set to be joined with the current instance
        may not have the header sorted in the same way.
        """

        # retrieves the current intance's header and uses it to
        # reorder the set to be joined so that it matched the target
        # structures (required to avoid data corruption)
        header = self.header()
        set.reorder(header)

        # retrieves the data from the set and extends the current list
        # with such data (join operation itself)
        data = set.data()
        self.extend(data)

    def sort_set(self, name, ascending = True):
        """
        Sorts the result set according to the attribute
        with the given name.

        The default order is ascending and may be changed
        using the appropriate flag.

        :type name: String
        :param name: The name of the attribute to be used
        for the sort operation.
        :type ascending: bool
        :param ascending: If the sort operation should be
        done in an ascending order or descending.
        """

        # tries to retrieve the index value for the requested
        # name in case it does not exists raises an error
        index = self.header_h.get(name, -1)
        if index == -1:
            raise RuntimeError("Attribute '%s' not found for result set header" % name)

        # retrieves the complete set of data and sorts it using
        # the just created sorter operation then sets the data
        # for the current instance with the result of it
        data = self.data()
        data.sort(key = lambda item: item[index], reverse = not ascending)
        self.data_s(data)

    def data(self):
        """
        Retrieves a list containing the "raw" data for the
        current result set, this avoid the "unsafe" iteration
        over the header values.

        :rtype: List
        :return: The list containing the "raw" data for the
        current result set.
        """

        if self.header_set: return self[1:]
        else: return self

    def data_s(self, data):
        """
        Sets the "raw" data for the current result set avoiding
        the overlap of the header.

        In case the header is set this may be a quite expensive
        operation as the values of all the list will be replaced.

        :type data: List
        :param data: The "raw" data to replace the currently existing
        data in the result set.
        """

        if self.header_set: self[1:] = data
        else: self[:] = data

    def header(self):
        """
        Retrieves the header list for the current result set in case
        no header exists an exception will be raised.

        :rtype: List
        :return: The list containing the header information (names)
        for the current result set instance.
        """

        if not self.header_set:
            raise RuntimeError("No header set in result set structure")
        return self[0]

    def header_t(self, replace = ":"):
        """
        Retrieves the header list (transformed) values that consist
        of the original values replaces with a special character.

        This method provides a way to retrieve header safe values,
        useful for map creation.

        :type replace: String
        :param replace: The character value to be used to replace the
        "normal" name inheritance separator.
        :rtype: List
        :return: The list containing the header information (names)
        for the current result set instance (transformed mode).
        """

        header = self.header()
        header_t = [name.replace(".", replace) for name in header]
        return header_t

    def reorder(self, header):
        """
        Reorders the current result set so that the "raw" data
        elements match the provided header.

        This is a very expensive operation as all the data will
        be re-written into new lists.

        No operation occurs in case the header provided already
        matched the one set in the result set (safe mode).

        :type header: List
        :param header: The list containing the various names that
        will be part of the new header.
        """

        # retrieves the currently set header in order to be
        # able to compare it with the provided one and in case
        # the value is the same returns immediately no reorder
        # is required (performance improvement)
        _header = self.header()
        if _header == header: return

        # creates the list that will hold the various lines
        # that constitute the re-ordered "raw" data
        lines = []

        # retrieves the current "raw" data and iterate over the complete
        # set of lines to reorder their values according to the new header
        data = self.data()
        for line in data:
            # creates the list that will represent the re-ordered
            # list, to be populated
            line_r = []

            # iterates over all the names on the "new" header and
            # retrieves the values for each of them inserting them
            # into the new (re-ordered) list
            for name in header:
                value = self.get(line, name)
                line_r.append(value)

            # adds the re-ordered list to the list of lines for the
            # new result set
            lines.append(line_r)

        # copies the header list provided as it will be the new header
        # of the result set (avoids collision) then removes the complete
        # set of elements (header and data) from the current result set
        _header = copy.copy(header)
        del self[:]

        # adds the header to the current result set list and extends the
        # the list with the computed (re-ordered) lines then recomputes
        # the hash map for the header (for fast access)
        self.append(_header)
        self.extend(lines)
        self._hash_h()

    def get(self, line, name):
        """
        Retrieves the value for the line that is "located"
        at the index associated with the requested name.

        This method can only be used in case the header for
        the result set is set.

        :type line: List
        :param line: The line (part of the result set) for
        which the value at the given name should be returned.
        :type name: String
        :param name: The name of the header for which the value
        will be retrieved.
        :rtype: Object
        :return: The value for the provided line with the
        index defined by the requested name.
        """

        # tries to retrieve the index value for the requested
        # name in case it does not exists raises an error
        index = self.header_h.get(name, -1)
        if index == -1:
            raise RuntimeError("Attribute '%s' not found for result set header" % name)

        # retrieves the value for the retrieved index and returns
        # it to the caller method
        value = line[index]
        return value

    def set(self, line, name, value):
        """
        Sets the value in the line for the index associated
        with the provided name.

        This method can only be used in case the header for
        the result set is set.

        :type line: List
        :param line: The line (part of the result set) for
        which the value at the given name should be set.
        :type name: String
        :param name: The name of the attribute that is going
        to be set, an index will be resolved using it.
        :type value: Object
        :param value: The value that is going to be set in
        the line field.
        """

        # tries to retrieve the index value for the requested
        # name in case it does not exists raises an error
        index = self.header_h.get(name, -1)
        if index == -1:
            raise RuntimeError("Attribute '%s' not found for result set header" % name)

        # sets the value in the provided line for the retrieved
        # index (set operation)
        line[index] = value

    def map(self):
        """
        Converts the current result set structure into a list
        of maps with key values represented by the header names.

        This is an expensive operation as all the lines composing
        the result set data will be replicated as maps.

        :rtype: List
        :return: The list of maps representing the current result
        set data, this is replicated information.
        """

        # retrieve the transformed version of the header names
        # (for safety reasons) and then retrieves the "raw" data
        # that is going to be used in the conversion
        header_t = self.header_t()
        data = self.data()

        # creates the list that will hold the various maps that
        # will represent the result set data
        map_set = []

        # iterates over all the lines in the "raw" data list to
        # convert them into map structures
        for line in data:
            # creates the structure that will hold the line
            # information (normal map) and starts the index
            # to be used in the percolation of the header
            map = {}
            index = 0

            # iterates over all the values in the lines to set
            # them into the newly created map
            for value in line:
                # retrieves the name of the header associated with
                # the current index and sets the name and values
                # in the map structure
                name = header_t[index]
                map[name] = value
                index += 1

            # adds the constructed map to the list of maps
            # representing the result set
            map_set.append(map)

        # returns the list of map that represent the
        # result set structure to the caller method
        return map_set

    def add_h(self, name, nullify = False):
        """
        Adds a new header to the current set, note that in case
        the provided nullify parameter is provided the data is
        changed so that such header is set to an invalid value.

        Note that the "new" header is added to the end of the
        current set of headers (default option).

        :type name: String
        :param name: The name of the header that is going to be
        added (as a plain string).
        :type nullify: bool
        :param nullify: If the values in the data should be set
        as invalid for the new header (avoid corruption).
        """

        # retrieves the current header value (as a sequence) and
        # adds the name name into it, recomputing the new header
        # hash value from the length of the current header sequence
        header = self.header()
        header.append(name)
        self.header_h[name] = len(header) - 1

        # in case the nullify value was not set returns immediately
        # otherwise invalidates the last values of the complete set
        # of data lines/items (as expected)
        if not nullify: return
        for item in self.data(): item.append(None)

    def rename_h(self, old, new):
        """
        Renames the provided header name to a new one.
        After this operation the index should be usable.

        :type old: String
        :param old: The current (old) name of the header
        to be re-named.
        :type new: String
        :param old: The target (new) name for which the
        header should be re-named.
        """

        # tries to retrieve the index value for the requested
        # name in case it does not exists raises an error
        index = self.header_h.get(old, -1)
        if index == -1:
            raise RuntimeError("Attribute '%s' not found for result set header" % old)

        # retrieves the header list to be used in the
        # renaming operation
        header = self.header()

        # deletes the old header from the hash map and sets
        # the new name on the hash index (update hash) and
        # then updates the linear header list with the new
        # name for the header
        del self.header_h[old]
        self.header_h[new] = index
        header[index] = new

    def rename_hw(self, old, new):
        """
        Runs the rename operation of the header using a wildcard
        approach on the beginning of the name (prefix).

        :type old: String
        :param old: The prefix of the various header name to be
        re-named with the new prefix.
        :type new: String
        :param new: The prefix to be used on the re-name operation.
        """

        # retrieves the list containing the various header name and
        # iterates over them to try to match each name against the prefix
        # in case they match a replace header operation will be "issued"
        header = self.header()
        for name in header:
            if not name.startswith(old): continue
            name_new = name.replace(old, new)
            self.rename_h(name, name_new)

    def set_h(self, names):
        """
        Inserts or updates the provided list of names as the
        the list of headers for the result set.

        This operation is safe as a second or further operation
        will replace the header contents maintain a consistent
        state.

        :type names: List
        :param names: The list of names to be used for header
        information on the result set.
        """

        if self.header_set: del self[0]
        self.header_set = True
        self.insert(0, names)
        self._hash_h()

    def extend_h(self, names):
        """
        Extends the list of names that compose the headers for
        the result set.

        This operation does not affect the internal data and if
        no change in the lines occurs inconsistent state may occur.

        :type names: List
        :param names: The list of names to extend the current header
        for the result set.
        """

        header = self.header()
        header.extend(names)
        self._hash_h()

    def rdict_iter(self):
        """
        Returns a generator like object that is able to percolate
        over the complete set of elements in the rset providing
        object like interactions with the contained sequences.

        :rtype: Generator
        :return: The generator that may be used to percolate over
        the rset with an associative interaction with the values.
        """

        # iterates over the complete set of lines of the current
        # data yielding the created result dictionary for such line
        for line in self.data(): yield rdict(self, line)

    def _hash_h(self):
        """
        Computes an hash map associating the index position
        of the header with it's own name, this allows a rapid
        access to each of the header values.
        """

        self.header_h = {}
        header = self.header()
        index = 0

        for name in header:
            self.header_h[name] = index
            index += 1

class rdict(dict):
    """
    Specialized dictionary structure that provides a key
    to value interaction on a line of a result set, this
    allows for easy access at the cost of performance.
    """

    def __init__(self, rset, line):
        self.rset = rset
        self.line = line
        header = rset.header()
        for key, value in zip(header, line):
            dict.__setitem__(self, key, value)

    def __setitem__(self, key, value):
        if not key in self.rset.header_h: self.rset.add_h(key, nullify = True)
        self.rset.set(self.line, key, value)

    def get_value(self, name, default = None, load_lazy = False):
        return self.get(name, default)

def load_serializers():
    """
    Loads the various serializer objects according
    to the associated module names.

    This method ignores the import problems for non
    existent serializers, removing them from the
    associated data structures.
    """

    global SERIALIZERS_MAP

    # creates the list that will hold the various
    # names to be removed from the serializers list
    removal = []

    # initializes the serializers map that will associate
    # the name of the serializer with the object
    SERIALIZERS_MAP = {}

    # iterates over all the (serializer) names in the
    # serializers list to try to import the module and
    # alter the affected data structures
    for name in SERIALIZERS:
        # tries to import the module associated with the
        # serializer and in case it fails adds the name
        # to the removal list otherwise sets the serializer
        # in the associated map
        try: object = __import__(name)
        except ImportError: removal.append(name)
        else: SERIALIZERS_MAP[name] = object

    # iterates over all the (serializer) names to be
    # removed and removes them from the serializers list
    for name in removal: SERIALIZERS.remove(name)
