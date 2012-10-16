#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import datetime

import colony.libs.time_util
import colony.libs.string_util

import utils
import exceptions

PERSIST_UPDATE_TYPE = 0x01
""" The persist only on update (or save) persist type """

PERSIST_SAVE_TYPE = 0x02
""" The persist only on save persist type """

PERSIST_ASSOCIATE_TYPE = 0x04
""" The persist associate persist type """

PERSIST_NONE_TYPE = 0x00
""" The persist none persist type """

PERSIST_ALL_TYPE = PERSIST_UPDATE_TYPE | PERSIST_SAVE_TYPE | PERSIST_ASSOCIATE_TYPE
""" The persist all persist type """

SAVED_STATE_VALUE = 1
""" The saved state value """

UPDATED_STATE_VALUE = 2
""" The updated state value """

REMOVED_STATE_VALUE = 3
""" The removed state value """

TARGET_ENTITY_VALUE = "target_entity"
""" The target entity value """

DATA_STATE_VALUE = "data_state"
""" The data state value """

RELATION_VALUE = "relation"
""" The relation value """

DATA_TYPE_VALUE = "data_type"
""" The data type value """

PERSIST_TYPE_VALUE = "persist_type"
""" The persist type value """

DATA_REFERENCE_VALUE = "data_reference"
""" The data reference value """

DATE_VALUE = "date"
""" The date value """

CLASS_VALUE = "_class"
""" The class value """

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

DATA_TYPE_CAST_TYPES_MAP = {
    "text" : unicode,
    "string" : unicode,
    "integer" : int,
    "float" : float,
    "date" : colony.libs.time_util.timestamp_datetime,
    "data" : unicode,
    "metadata" : dict,
    "relation" : None
}
""" The map associating the data types with the cast types """

def _class_get(class_reference, id_value, options = {}, context = None, namespace = None, entity_manager = None):
    """
    Class method that retrieves an entity model for
    the given id value and using the given options.
    This method allows the indirect access to the entity
    manager for the usage of the get method.

    @type id_value: Object
    @param id_value: The value for the identifier attribute
    of the entity model to be retrieved.
    @type options: Dictionary
    @param options: The map of options for the retrieval
    of the entity model.
    @type context: RestRequest
    @param context: The rest request to be used for the context
    retrieval process, will affect filtering.
    @type namespace: String
    @param namespace: The namespace prefix to be used in the
    retrieval of the context session attribute.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    @rtype: Entity
    @return: The retrieved retrieved entity model.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # applies the context to the options according to the current
    # request, note that the (request) context is passed as simply
    # context in fact it represents the request from which context
    # will be extracted, after this application the filter query
    # should be modified to reflect the context based filtering
    options = class_reference.apply_context(options, context, namespace_name = namespace, entity_manager = entity_manager)

    # retrieves the entity model for the given class, id value
    # and using the given options, then in case the retrieval was
    # successful applies the context as the entity model request
    entity_model = entity_manager.get(class_reference, id_value, options)
    entity_model and hasattr(entity_model, "set_request") and entity_model.set_request(context)

    # returns the retrieved entity model
    return entity_model

def _class_count(class_reference, options = {}, context = None, namespace = None, entity_manager = None):
    """
    Class method that retrieves the number of entity models
    in the data source using the current entity model class
    and the given options.
    This method allows the indirect access to the entity
    manager for the usage of the count method.

    @type options: Dictionary
    @param options: The map of options for the counting
    of the entity models.
    @type context: RestRequest
    @param context: The rest request to be used for the context
    retrieval process, will affect filtering.
    @type namespace: String
    @param namespace: The namespace prefix to be used in the
    retrieval of the context session attribute.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    @rtype: int
    @return: The number of models in the data source for the
    current class reference (entity model).
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # applies the context to the options according to the current
    # request, note that the (request) context is passed as simply
    # context in fact it represents the request from which context
    # will be extracted, after this application the filter query
    # should be modified to reflect the context based filtering
    options = class_reference.apply_context(options, context, namespace_name = namespace, entity_manager = entity_manager)

    # retrieves the count (number of entities) for the given
    # entity class and options
    result = entity_manager.count(class_reference, options)

    # returns the result of the entity model counting operation
    # (number of entity results in the data source)
    return result

def _class_find(class_reference, options = {}, context = None, namespace = None, entity_manager = None):
    """
    Class method that retrieves a set of entity models
    using the given options.
    This method allows the indirect access to the entity
    manager for the usage of the find method.

    @type options: Dictionary
    @param options: The map of options for the retrieval
    of the set of entity models.
    @type context: RestRequest
    @param context: The rest request to be used for the context
    retrieval process, will affect filtering.
    @type namespace: String
    @param namespace: The namespace prefix to be used in the
    retrieval of the context session attribute.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    @rtype: List
    @return: The retrieved set of entity models.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # applies the context to the options according to the current
    # request, note that the (request) context is passed as simply
    # context in fact it represents the request from which context
    # will be extracted, after this application the filter query
    # should be modified to reflect the context based filtering
    options = class_reference.apply_context(options, context, namespace_name = namespace, entity_manager = entity_manager)

    # checks if the class reference is valid for the current
    # context in case it's not a default value is returned
    if not class_reference.valid(): return []

    # finds the entity models for the given class and using
    # the given options then applies the context to the complete
    # set of retrieved entity models (only applies the request
    # to the first element because their share the diffusion scope)
    entity_models = entity_manager.find(class_reference, options)
    entity_models and hasattr(entity_models[0], "set_request") and entity_models[0].set_request(context)

    # returns the retrieved entity models
    return entity_models

def _class_find_one(class_reference, options = {}, context = None, namespace = None, entity_manager = None):
    """
    Class method that retrieves the first entity model
    using the given options.
    This method allows the indirect access to the entity
    manager for the usage of the find method.

    @type options: Dictionary
    @param options: The map of options for the retrieval
    of the entity model.
    @type context: RestRequest
    @param context: The rest request to be used for the context
    retrieval process, will affect filtering.
    @type namespace: String
    @param namespace: The namespace prefix to be used in the
    retrieval of the context session attribute.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    @rtype: Entity
    @return: The retrieved entity model (first retrieval).
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # applies the context to the options according to the current
    # request, note that the (request) context is passed as simply
    # context in fact it represents the request from which context
    # will be extracted, after this application the filter query
    # should be modified to reflect the context based filtering
    options = class_reference.apply_context(options, context, namespace_name = namespace, entity_manager = entity_manager)

    # finds the entity models for the given class and using
    # the given options, limits the number of results to
    # the first result in case at least one is given, then in
    # case the retrieval was successful applies the context as
    # the entity model request
    entity_models = entity_manager.find(class_reference, options)
    entity_model = entity_models and entity_models[0] or None
    entity_model and hasattr(entity_model, "set_request") and entity_model.set_request(context)

    # returns the retrieved entity model
    return entity_model

def _class_execute(class_reference, query, entity_manager = None):
    """
    Class method that executes a sql query "directly" in
    the data source and retrieves the resulting data set.
    This method allows the indirect access to the entity
    manager for the usage of the execute method.

    @type query: String
    @param query: The sql query to be directly executed
    in the data source.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    @rtype: List
    @return: The retrieved "raw" data set from the data source.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # executes the query in the entity manager associated
    # data source and retrieves the resulting data set
    # as a list with tuples containing the values
    result_set = entity_manager.execute(query)

    # returns the retrieved result set
    return result_set

def _class_lock_g(class_reference, id_value, entity_manager = None):
    """
    Class method that locks the entity manager data source
    for the entity model with the given id value.
    This method allows the indirect access to the entity
    manager for the usage of the lock method.

    @type id_value: Object
    @param id_value: The value for the identifier attribute
    of the entity model to be "locked".
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # locks the entity manager data source for the given
    # class and the given id value
    entity_manager.lock(class_reference, id_value)

def _class_lock_table_g(class_reference, parameters, entity_manager = None):
    """
    Class method that locks the entity manager data source
    for the table associated with the current entity class.
    This method allows the indirect access to the entity
    manager for the usage of the lock table method.

    @type parameters: Dictionary
    @param parameters: The map containing the parameters to be
    used in the lock of the table.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # retrieves the name of the table associated with the
    # current class to be used in the locking
    table_name = class_reference.get_name()

    # locks the entity manager (table) data source for the given
    # parameters (provided from the signature)
    entity_manager.lock_table(table_name, parameters)

def _class_lock_row_g(class_reference, name, value, entity_manager = None):
    """
    Class method that locks the entity manager data source
    for the row defined by the name/value filter in the table
    associated with the current class.
    This method allows the indirect access to the entity
    manager for the usage of the lock table method.

    Note that only the bottom table hierarchy level can be
    used in the name field (no top naming can be used).

    @type name: String
    @param name: The name of the attribute to be used in the
    filtering, must belong to the table in the bottom of the
    entity class hierarchy.
    @type value: Object
    @param value: The value to be used for the name in the
    filter, must be of a valid type for the attribute.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # retrieves the name of the table associated with the
    # current class and then creates the parameters map
    # containing the definition of the field for locking
    table_name = class_reference.get_name()
    sql_value = class_reference._get_sql_value(name, value)
    parameters = {
        "field_name" : name,
        "field_value" : sql_value
    }

    # locks the entity manager (table) data source for the given
    # parameters (field definition)
    entity_manager.lock_table(table_name, parameters)

def _class_valid(class_reference, entity_manager = None):
    """
    Checks if the current model class reference is valid, according
    to the currently defined data reference model.

    A model class is valid in case the model is not a data reference
    or in case the model is a data reference but the "real" model class
    is defined in the current entity manager context.

    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    @rtype: bool
    @return: If the current model class is valid for the current context.
    """

    # checks if the class is not a data reference, in case
    # it's not it's "automatically" valid
    if not class_reference.is_reference():
        # return valid (not a data reference)
        return True

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager, then uses it
    # to retrieve the entity class
    entity_manager = entity_manager or class_reference._entity_manager
    entity_class = entity_manager.get_entity(class_reference.__name__)

    # in case the entity class was correctly found, the class
    # is considered to be valid
    if entity_class: return True

    # returns false (invalid), this is the
    # default return value
    return False

def _class_is_reference(class_reference):
    """
    Checks if the current model entity is in fact a (data) reference
    class, for external elements reference.

    The data reference classes are used to refer external components of
    the model, for a loose connection.

    @rtype: bool
    @return: If the current class is a data reference to an entity model.
    """

    # checks if the class is a data reference, by testing it
    # for the presence of the data reference value and by
    # testing the (possible) existing value against true validation
    if hasattr(class_reference, DATA_REFERENCE_VALUE) and class_reference.data_reference == True:
        # returns valid (the model class is in fact
        # a data reference model class)
        return True

    # returns invalid (the model class is not
    # a data reference)
    return False

def _class_create_filter(class_reference, data, defaults = {}, entity_manager = None):
    """
    Class method that creates a filter map from the provided
    (form) data map and using the provided map of default
    values for reference.

    The new filter map is created according to the predefined
    syntax rules for the sort and for the filter fields.

    @type data: Dictionary
    @param data: The form data map, resulting from the processing
    of the associated request.
    @type defaults: Dictionary
    @param defaults: The map of default values to be used in the
    construction of the filter map.
    @rtype: Dictionary
    @return: The resulting filter string that can be used in the
    entity manager for filtering of a result set.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # normalizes the options map, so that is possible to
    # operate in it without any possible harm to the the
    # internal structure of it
    defaults = entity_manager.normalize_options(defaults)

    # retrieves the various default values from the map
    # of default values, these are going to be the fallback
    # values for each of these filter components
    name = defaults.get("name", None)
    type_s = defaults.get("type", "both")
    order_by = defaults.get("order_by", None)
    eager = defaults.get("eager", ())
    filters = defaults.get("filters", [])
    map = defaults.get("map", False)

    # retrieves the various components of the form elements
    # defaulting to the pre-defined default values
    filter_string = data.get("filter_string", "")
    sort = data.get("sort", None)
    filters_s = data.get("filters", [])
    start_record = data.get("start_record", 0)
    number_records = data.get("number_records", 5)

    # forces the type of the filters to be a list, this avoids
    # problems handling immutable types (tuples) resulting from
    # the normalization process
    filters = list(filters)

    # normalizes the sort value into the accepter order by
    # value defaulting to the fallback value in case the
    # sort value is the default
    sort_value, sort_order = sort and sort.split(":", 1) or ("default", None)
    order_by = not sort_value == "default" and ((sort_value, sort_order),) or order_by

    def resolve(cls, eager, path):
        # retrieves the base value from the path and
        # the remaining list of elements in the path
        base = path[0]
        remaining = path[1:]

        # in case the base value is not present
        # in the eager map returns immediately with
        # an invalid value
        if not base in eager: return None, None

        # retrieves the base (name) value from the eager
        # map and then in case there are no more names
        # remaining returns this map (end of recursion)
        map = eager[base]
        target = cls.get_target(base)
        if not remaining: return map, target

        # retrieves the eager (loaded) relations map
        # from the current map and runs the resolve
        # recursive step for the remaining list
        eager = map.get("eager", {})
        resolve(target, eager, remaining)

    def resolve_s(attribute):
        # splits the attribute (complete) name using the dot based
        # separator and then retrieves the base (path) value and
        # the trailing name value
        path = attribute.rsplit(".")
        base, name = path[:-1], path[-1]

        # in case the base value is defined a resolution operation
        # must occur to retrieve the relation map and the target class
        if base:
            # resolvers the eager values according to the provided
            # base value in case the returned relation is invalid
            # skips the current filter (invalid)
            relation, target = resolve(class_reference, eager, base)
            if relation == None: return None, None, None

            # retrieves the filters map and sets it in the relation map
            # (for cases where it does not already exists)
            _filters = relation.get("filters", [])
            relation["filters"] = _filters

        # otherwise the normal values are used for the filters nap
        # and for the target class
        else:
            # sets the filters map as the current global filters
            # map and the target as the current class (reference)
            _filters = filters
            target = class_reference

        # returns the tuple containing the target filters map
        # the target (class) and the top level name of the attribute
        return _filters, target, name

    # in case the name is defined the "special" wildcard filter
    # is added to the list of filters to be used in the query
    # this is the base value for the search
    if name :
        # retrieves the data type for the name attribute and in
        # case it's not a sequence converts it to a immutable
        # sequence (tuple) for iteration
        name_type = type(name)
        if not name_type in (types.ListType, types.TupleType): name = (name,)

        # retrieves the first name element from the sequence and uses
        # it to resolver the value, retrieving the filter structure
        # in which the filter will be inserted
        first = name[0]
        _filters, _target, _name = resolve_s(first)

        # creates the wildcard based filter with an empty set of field
        # (empty map) that is populated with the various field names
        # contained in the name sequence
        _filter = {
            "type" : "like",
            "like_type" : type_s,
            "fields" : {}
        }

        # retrieves the fields part of the filter and adds the various
        # partial names to it with the filter string as the value
        fields = _filter["fields"]
        for _name in name:
            _name = _name.rsplit(".", 1)[-1]
            fields[_name] = filter_string

        # adds the "just" created filter to the filters structure resulting
        # from the resolution of the first name, this fact forces all the
        # names to be at the same relation level
        _filters.append(_filter)

    # iterates over all the serialized filter values to create
    # the normalized filter values
    for filter in filters_s:
        # unpacks the filter string into attribute, operation
        # and value to be used for the filter
        attribute, operation, value = filter.split(":", 2)

        # resolves the attribute path, retrieving the target
        # filters map to be used the target entity class referenced
        # by the various relations and the name of the "trailing"
        # attribute (the last result of the split)
        _filters, target, name = resolve_s(attribute)
        if _filters == None: continue

        # casts the value for the current name using the target
        # class resulting from the resolution of the base and then
        # creates the filter according to the (top) name and value
        # and to the provided operation then adds the filter to
        # the list of filters
        _value = target._cast_value(name, value)
        _filter = {
            "type" : operation,
            "fields" : {
                name : _value
            }
        }
        _filters.append(_filter)

    # creates the complete filter value according to the provided
    # specification and returns it to the caller method
    filter = {
        "range" : (start_record, number_records),
        "order_by" : order_by or (),
        "eager" : eager,
        "filters" : filters,
        "map" : map
    }
    return filter

def _class_apply_context(class_reference, options = {}, context_request = None, context = None, namespace_name = None, entity_manager = None):
    """
    Applies the context information to the retrieval operation,
    this will change the given options map to handle the filtering
    according to the context information.

    The context information is (by default) retrieved from the session
    information in the given context request.

    @type options: Dictionary
    @param options: The map of options for the retrieval operation.
    @type context_request: RestRequest
    @param context_request: The rest request to be used for the
    retrieval of the context, in case no context is specified.
    @type context: Dictionary
    @param context: The context information map that overrides the one
    present in the current rest request session.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used in the
    context session attribute retrieval, avoids domain name collision.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # in case no context request is provided the control
    # is returned immediately to the caller, it's not
    # possible to apply the context without the context
    # request set
    if not context_request: return options

    # tries to retrieve the context request session if
    # it fails control is returned immediately
    rest_request_session = context_request.get_session()
    if not rest_request_session: return options

    # retrieves the complete (attribute name) for the context
    # taking into account the namespace name (prefix)
    attribute_name = _get_complete_name("_context", namespace_name)

    # tries to resolve the real context value, in case
    # none is provided tries to retrieve it from session
    # after that in case no valid context is found returns
    # the control immediately
    context = context or rest_request_session.get_attribute(attribute_name)
    if not context: return options

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or class_reference._entity_manager

    # in case the options map is not defined a new one
    # must be created for the domain of this operation
    # (avoids problems with static options maps)
    options = options or {}

    # normalizes the options map, so that is possible to
    # operate in it without any possible harm to the the
    # internal structure of it
    options = entity_manager.normalize_options(options)

    # retrieves the filters from the provided options
    # and converts it into a list to be "workable",
    # because this value should be an non manipulable tuple
    filters = list(options.get("filters", []))

    # iterates over all the context items to create the various
    # fields for filtering (logic and operation between them)
    for context_name, context_value in context.items():
        # adds the context value filtering part to the initial
        # options map provided, this is an extension to the
        # existing filters
        filters.append({
            "type" : context_value == None and "is_null" or "equals",
            "fields" : (
                {
                    "name" : context_name,
                    "value" : context_value
                },
            ),
            "post" : True
        })

    # sets the appropriate set of filters in the options
    # to be able to retrieve the a match on the context
    # values of the requested entity class (context view)
    options["filters"] = filters

    # returns the complete set of options in the generated
    # options map, this is the normalized version of the map
    # already containing the "context filters"
    return options

@utils.transaction_method("_entity_manager")
def delete(self, persist_type, entity_manager = None):
    """
    "Transactional" method to be used as the main entry
    point of removal in the model structure.
    This method should be "overridden" in case additional
    business logic is necessary in the saving process.

    @type persist_type: int
    @param persist_type: The type of persist to be used
    in the entity.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # tries to call the pre delete method, in order to notify the
    # current instance about the starting of the delete procedure
    if hasattr(self, "pre_delete") and persist_type & PERSIST_UPDATE_TYPE: self.pre_delete(persist_type)
    if hasattr(self, "pre_remove") and persist_type & PERSIST_UPDATE_TYPE: self.pre_remove(persist_type)

    try:
        # tries to call the on delete method, in order to notify the
        # current instance about the starting of the delete procedure
        if hasattr(self, "on_delete") and persist_type & PERSIST_UPDATE_TYPE: self.on_store(persist_type)
        if hasattr(self, "on_remove") and persist_type & PERSIST_SAVE_TYPE: self.on_save(persist_type)

        # removes the current entity from the data source defined in
        # the provided entity manager, this is a non reversible and
        # final operation from the data source point of view
        self.remove(entity_manager = entity_manager)
    except BaseException, exception:
        # tries to call the fail store method, in order to notify the
        # current instance about the failure of the store procedure
        if hasattr(self, "fail_delete"): self.fail_delete(persist_type, exception)
        if hasattr(self, "fail_remove"): self.fail_remove(persist_type, exception)

        # re-raises the exception to the upper levels, no need to
        # to except at this level
        raise

    # tries to call the post delete method, in order to notify the
    # current instance about the finishing of the delete procedure
    if hasattr(self, "post_delete") and persist_type & PERSIST_UPDATE_TYPE: self.post_delete(persist_type)
    if hasattr(self, "post_remove") and persist_type & PERSIST_UPDATE_TYPE: self.post_remove(persist_type)

@utils.transaction_method("_entity_manager")
def store(self, persist_type, validate = True, force_persist = False, raise_exception = False, entity_manager = None):
    """
    "Transactional" method to be used as the main entry
    point of persistence in the model structure.
    This method should be "overridden" in case additional
    business logic is necessary in the saving process.

    @type persist_type: int
    @param persist_type: The type of persist to be used
    in the entity.
    @type validate: bool
    @param validate: Flag controlling if a validation should
    be run in the model before persisting it.
    @type force_persist: bool
    @param force_persist: Flag controlling if the persistence
    should be forced in which case the persist type mask is completely
    ignored by the persistence engine.
    @type raise_exception: bool
    @param raise_exception: If an exception must be raised in case
    a validation fails in one of the relation values.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # in case the force persist flag is set (persistence is ignored)
    # the persist type is set to the all permission (no control)
    persist_type = force_persist and PERSIST_ALL_TYPE or persist_type

    # in case the current instance is already in the storing
    # procedure (cycle detected) it must return immediately to
    # avoid stack overflowing
    if hasattr(self, "_storing") and self._storing == True: return

    # checks if the current instance is already persisted in the
    # data source, this value will be useful for the conditional
    # calling of the handlers
    is_persisted = self.is_persisted()

    # tries to call the pre store method, in order to notify the
    # current instance about the starting of the store procedure
    if hasattr(self, "pre_store") and persist_type & (PERSIST_SAVE_TYPE | PERSIST_UPDATE_TYPE): self.pre_store(persist_type)
    if hasattr(self, "pre_save") and not is_persisted and persist_type & PERSIST_SAVE_TYPE: self.pre_save(persist_type)
    if hasattr(self, "pre_update") and is_persisted and persist_type & PERSIST_UPDATE_TYPE: self.pre_update(persist_type)

    # detaches the current entity model in order
    # to avoid any possible loading of relations
    self.detach_l(force = False)

    # sets the current entity in the storing operation, this flag
    # should be able to avoid unnecessary recursion
    self._storing = True

    try:
        # runs the "preemptive" validation process in the current entity
        # model this will allow the saving process to prevent any problem
        # with validation in the saving process that will imply the
        # "rollback" of the transaction and the consequent invalidation
        # of the data
        validate and self.preemptive_validate(persist_type)

        # tries to call the on store method, in order to notify the
        # current instance about the starting of the store procedure
        # (this event is called after the preemptive validation process)
        if hasattr(self, "on_store") and persist_type & (PERSIST_SAVE_TYPE | PERSIST_UPDATE_TYPE): self.on_store(persist_type)
        if hasattr(self, "on_save") and not is_persisted and persist_type & PERSIST_SAVE_TYPE: self.on_save(persist_type)
        if hasattr(self, "on_update") and is_persisted and persist_type & PERSIST_UPDATE_TYPE: self.on_update(persist_type)

        # stores the various relations of the entity model persisting
        # them into the data source and then persists the entity model
        # itself, names persistence
        self.store_relations(persist_type, validate = validate, force_persist = force_persist, raise_exception = raise_exception, entity_manager = entity_manager)
        self.persist(persist_type, entity_manager = entity_manager)
    except BaseException, exception:
        # tries to call the fail store method, in order to notify the
        # current instance about the failure of the store procedure
        if hasattr(self, "fail_store"): self.fail_store(persist_type, exception)
        if hasattr(self, "fail_save") and not is_persisted: self.fail_save(persist_type, exception)
        if hasattr(self, "fail_update") and is_persisted: self.fail_update(persist_type, exception)

        # re-raises the exception to the upper levels, no need to
        # to except at this level
        raise
    finally:
        # restores the storing variable to the original invalid
        # state (avoids possible misbehavior)
        self._storing = False

        # attaches the current entity model back
        # enabling it to communicate with the data
        # source for loading of relations
        self.attach_l(force = False)

    # tries to call the post store method, in order to notify the
    # current instance about the finishing of the store procedure
    if hasattr(self, "post_store") and persist_type & (PERSIST_SAVE_TYPE | PERSIST_UPDATE_TYPE): self.post_store(persist_type)
    if hasattr(self, "post_save") and not is_persisted and persist_type & PERSIST_SAVE_TYPE: self.post_save(persist_type)
    if hasattr(self, "post_update") and is_persisted and persist_type & PERSIST_UPDATE_TYPE: self.post_update(persist_type)

def store_f(self, validate = True, raise_exception = False, entity_manager = None):
    """
    Utility method, that may be used as a shorthand if
    the storing of the entity in the data source is meant
    to be forced and the persist type ignored.

    Use this method carefully as it may incur is severe
    security measures. A typical usage of this method would
    be in localized patched for fixing of schemas.

    @type validate: bool
    @param validate: Flag controlling if a validation should
    be run in the model before persisting it.
    @type raise_exception: bool
    @param raise_exception: If an exception must be raised in case
    a validation fails in one of the relation values.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # stores the current entity forcing the persistence of it
    # for this case the persistence type mask is ignored and
    # the storage procedure is forced into the data source
    self.store(None, validate = validate, force_persist = True, raise_exception = raise_exception, entity_manager = entity_manager)

def preemptive_validate(self, persist_type):
    """
    Runs all the validation in the relations and in the entity
    itself, in a recursive fashion.

    The persist type is sent so that only the relations that are
    able to be persisted are validated (performance oriented).

    This method should raise a model validation error in case
    at least one of the validations (in the model or relations)
    fails.

    This method is extremely useful to make sure that the model
    and all it's child relations (of arbitrary depth) are valid
    (before storage).

    @type persist_type: int
    @param persist_type: The persist type to be used to check if
    the associated relations must be validated.
    This value is going to be used in the calculation of the new
    relation persist types.
    """

    # runs the recursive fashioned validation on the current
    # entity model retrieve the result, in case the result is
    # valid returns immediately without raising the exception
    result = self._validate(persist_type)
    if result: return

    # raises a model validation exception because the preemptive
    # validation process failed for the current model
    raise exceptions.ModelValidationError("preemptive validation of entity model failed", self)

def store_relations(self, persist_type, validate = False, force_persist = False, raise_exception = False, entity_manager = None):
    """
    Stores all the relations of the current entity according to the
    security information provided by the persist type mask.
    The storage procedure takes a recursive approach, and all the
    relations of the relations will be stored.

    The relations that contain an invalid value or that contain a lazy
    loaded value will not be saved.

    @type persist_type: int
    @param persist_type: The type of persist to be used
    for storing the relations.
    @type validate: bool
    @param validate: Flag controlling if a validation should
    be run in the relations models before persisting them.
    @type force_persist: bool
    @param force_persist: Flag controlling if the persistence
    should be forced in which case the persist type mask is completely
    ignored by the persistence engine.
    @type raise_exception: bool
    @param raise_exception: If an exception must be raised in case
    a validation fails in one of the relation values.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the relation names from the current entity
    # to validate them against the validation methods
    relation_names = self.get_relation_names()

    # iterates over all the relation names in
    # set of names of the entity
    for relation_name in relation_names:
        # retrieves the value of the relation with
        # the current relation name from the entity
        relation_value = self.get_value(relation_name)

        # in case the relation value is not set or in case it's
        # lazy loaded no persistence should occur
        if relation_value == None or self.is_lazy_loaded(relation_name):
            # continues the loop, for more
            # relation persistence
            continue

        # retrieves the attributes of the model for the current relation
        # in order to retrieve the appropriate persist type
        model_attributes = getattr(self.__class__, relation_name)
        relation_persist_type = force_persist and PERSIST_ALL_TYPE or model_attributes.get(PERSIST_TYPE_VALUE, PERSIST_NONE_TYPE)

        # recalculates the new persist type for the relation storing based on the
        # relation persist type and the current model persist type (associate type
        # in considered to be always present in the persist type)
        _persist_type = force_persist and PERSIST_ALL_TYPE or relation_persist_type & (persist_type | PERSIST_ASSOCIATE_TYPE)

        # stores the relation combining the persist type given and the current
        # model persist type in the meta information
        self.store_relation(relation_name, _persist_type, relation_persist_type, validate, force_persist, raise_exception, entity_manager = entity_manager)

def store_relation(self, relation_name, persist_type, relation_persist_type, validate = False, force_persist = False, raise_exception = False, entity_manager = None):
    """
    Stores a relation with the given name in the entity
    using the permissions granted by the persist type.
    In case the raise exception flag is set an exception
    is raise upon validation of model failure.

    The storage of the relation implies previous validation
    of associative permissions and so this method may change
    the current entity relation in case of malicious manipulation.

    @type relation_name: String
    @param relation_name: The name of the relation to be saved.
    This value may refer a lazy loaded relation.
    @type persist_type: int
    @param persist_type: The persist type mask that controls the
    persistence access.
    @type relation_persist_type: int
    @param relation_persist_type: The pre-defined (base) persist type mask
    that controls the relation persist type.
    @type validate: bool
    @param validate: Flag controlling if a validation should
    be run in the relation model before persisting it.
    @type force_persist: bool
    @param force_persist: Flag controlling if the persistence
    should be forced in which case the persist type mask is completely
    ignored by the persistence engine.
    @type raise_exception: bool
    @param raise_exception: If an exception must be raised in case
    a validation fails in one of the relation values.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # in case the relation is lazy loaded in the
    # current entity no need to store it
    if self.is_lazy_loaded(relation_name):
        # returns immediately
        return

    # starts the flag that controls in case
    # an error is set
    error_set = False

    # retrieves the relation value from the entity and then
    # converts it to an enumerable type for compatibility
    # (if required by the relation type)
    relation_value = self.get_value(relation_name)
    relation_is_to_many = self.is_to_many(relation_name)
    relation_value = not relation_is_to_many and [relation_value] or relation_value

    # creates the list to store the relation values
    # that are not "associable" and that so must be
    # removed from the entity, to avoid malicious
    # association in the data source
    remove_relations = []

    # iterates over all the relation values for storage
    # in case a validation fails it accumulates the various
    # errors around the storing procedure "soft fail"
    for _relation_value in relation_value:
        try:
            # retrieves the id attribute value from the relation value
            # to use under the relation validation check (check if they were
            # previously associated)
            id_attribute_value = _relation_value.get_id_attribute_value()

            # sets the relation valid flag as unset by default, no relation
            # validation is done by default
            relation_valid = False

            # in case the current persist type includes the update permission
            # the relation validation must be run in order to provide extra
            # relation validation permissions
            if persist_type & (PERSIST_UPDATE_TYPE | PERSIST_SAVE_TYPE):
                # in case the relation value is set and it's valid
                # (not empty) it's ready for validation of relations
                if _relation_value:
                    # validate the given entity for relation with the relation
                    # value in the attribute of name relation name
                    relation_valid = self.validate_relation(id_attribute_value, relation_name)
                # otherwise the validation is not required
                # the value is not valid, not set
                else:
                    # sets the relation as (automatically) valid, it's impossible
                    # to check if an invalid relation is valid
                    relation_valid = True

            # in case the relation is not valid (must remove update from
            # the persist type, not safe)
            if not relation_valid:
                # "calculates" the new persist type based on the base persist type
                # removes the update type from the persist type (it's not safe)
                persist_type &= PERSIST_ALL_TYPE ^ PERSIST_UPDATE_TYPE

            # checks if the relations is "storable" a relation is considered to be
            # "storable" if the persist type of it contains either the update or the
            # save permission (otherwise it's impossible to store it)
            is_storable = persist_type & (PERSIST_UPDATE_TYPE | PERSIST_SAVE_TYPE)

            # checks if the relation value is "associable", the relation value
            # is "associable" in case it's going to be created (no id attribute set),
            # in case the relation has just been saved (in current context), in
            # case the associate "permission" is set in the persist type or in
            # case the relation was previously (other transaction) set in the
            # entity (relation validation)
            is_associable = relation_valid or id_attribute_value == None or _relation_value.is_saved() or relation_persist_type & PERSIST_ASSOCIATE_TYPE

            # stores the relation value in the data source
            # using the "propagated" persist type (only in
            # case the relation is "storable")
            is_storable and _relation_value.store(persist_type, validate, force_persist = force_persist, entity_manager = entity_manager)

            # in case the relation is not valid it must be removed
            # from the entity to avoid "malicious" association to be set
            # on the data source
            not is_associable and remove_relations.append(_relation_value)
        except exceptions.ModelValidationError:
            # in case the raise exception flag is set
            # the exception must be "raised again"
            if raise_exception: raise

            # sets the error set flag, to trigger
            # the add error action at the end of
            # the relation store
            error_set = True

    # in case there is at least one item in the relation
    # that is considered not valid (to be removed) the relation
    # is considered invalid and is removed from the entity
    # model (provides the main data model security measure)
    remove_relations and self.delete_value(relation_name)

    # adds an error to the entity on the relation
    # for latter usage
    error_set and self.add_error(relation_name, "relation validation failed")

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

    # sets the context information in the current instance
    # this should change the instance to reflect the current
    # context values (only change it in case context exists)
    self.set_context(entity_manager = entity_manager)

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

    # sets the context information in the current instance
    # this should change the instance to reflect the current
    # context values (only change it in case context exists)
    self.set_context(entity_manager = entity_manager)

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

def reload(self, options = {}, entity_manager = None):
    """
    Reloads the current instance in the data source
    described in the current entity manager.
    This method provides the persistence layer for
    reloading an object.

    @type options: Dictionary
    @param options: The map of options for the reloading
    of the entity model.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # reloads the entity using the entity manager
    entity_manager.reload(self, options)

def relation(self, name, options = {}, entity_manager = None):
    """
    Loads a relation for the current instance in the
    data source described in the current entity manager.
    This method provides the persistence layer for
    loading of an object's relation.

    @type options: Dictionary
    @param options: The map of options for the (partial) loading
    of the entity model's relation.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # loads a relation with the provided options (partial
    # loading) using the entity manager
    entity_manager.relation(self, name, options)

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

    # sets the context information in the current instance
    # this should change the instance to reflect the current
    # context values (only change it in case context exists)
    self.set_context(entity_manager = entity_manager)

    # saves or updates the entity using the entity manager
    entity_manager.save_update(self)

def persist(self, persist_type, validate = False, entity_manager = None):
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
    @type validate: bool
    @param validate: Flag controlling if a validation should
    be run in the model before persisting it.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # in case the validate flag is set the validation
    # process is run in the current model
    validate and self.validate_exception()

    # checks if the entity is persisted
    is_persisted = self.is_persisted()

    # in case the entity is persisted and the persist
    # type allows updating
    if is_persisted and persist_type & PERSIST_UPDATE_TYPE:
        # updates the entity using the entity manager
        # this operation must change and persist the
        # values of the entity in the data source
        self.update(entity_manager = entity_manager)

    # in case the entity is not persisted and the persist
    # type allows saving
    elif not is_persisted and persist_type & PERSIST_SAVE_TYPE:
        # saves the entity using the entity manager
        # this operation must set and persist the
        # values of the entity in the data source
        self.save(entity_manager = entity_manager)

def lock(self, reload = False, entity_manager = None):
    """
    Locks the entity reference in the current data source
    to avoid possible persistence in the data reference.
    This method is important to avoid corrupt data states
    in critical sections.
    Any usage of this method should be made careful at the
    risk of creating a dead lock in the data source.

    In case the optional reload flag is set the entity is
    reloaded after the lock.

    @type reload: bool
    @param reload: If the entity should be reloaded after
    the lock operation is complete, this way it's possible
    to gather the must updated values.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # retrieves the class of the current object
    entity_class = self.__class__

    # retrieves the id attribute value
    id_attribute_value = self.get_id_attribute_value()

    # locks the entity with the given attribute
    entity_manager.lock(entity_class, id_attribute_value)

    # in case the reload flag is set the entity must be
    # reloaded retrieving the must updated contents for
    # the entity from the data source
    reload and self.reload()

def validate_relation(self, id_attribute_value, relation_name, entity_manager = None):
    """
    Validates a relation of the current entity, checking if was already
    associated with the entity in a previous transaction context.
    This is security validation method and must be used with previous
    knowledge of its capabilities.

    @type id_attribute_value: Object
    @param id_attribute_value: The value of the id of the relation attribute
    to be validated for previous association.
    @type relation_name: String
    @param relation_name: The name of the relation to be validated for
    previous association.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager
    reference to be used.
    """

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # runs the validation of the relation in the entity manager
    # this implies access to the data source (expensive)
    relation_valid = entity_manager.validate_relation(self, relation_name)

    # returns the result of the relation validation
    return relation_valid

def get_relation_names(self):
    """
    Retrieves the complete list of names of the relation
    attributes of the current entity.
    This method uses the inner method of the entity manager
    to retrieve the relations names (better performance).

    @rtype: List
    @return: The list of names for the attribute sof the
    entity describing relations.
    """

    # retrieves the entity manager to be used or the
    # retrieves the entity model (class) from the
    # entity and then uses it to retrieve the relation
    # names from it
    entity_model = self.__class__

    # retrieves all the relations from the entity models,
    # the result should be a map associating the relation
    # name with the definition of it, then it retrieves
    # just the keys of the map as the relation names
    relations = entity_model.get_all_relations()
    relation_names = relations.keys()

    # returns the relation names from the current instance
    # this may be used for relation access
    return relation_names

def get_id_attribute_name(self):
    """
    Retrieves the name of the attribute considered to be
    the identifier of the current entity.
    This method uses the entity manager for the retrieval
    of the identifier attribute, providing reliability.

    @rtype: String
    @return: The name of the identifier attribute of the
    current entity.
    """

    # retrieves the class of the current object
    entity_class = self.__class__

    # retrieves the id attribute name from the current object
    id_attribute_name = entity_class.get_id()

    # returns the id attribute name
    return id_attribute_name

def get_id_attribute_value(self):
    """
    Retrieves the value of the attribute considered to be
    the identifier of the current entity.
    This method uses the entity manager for the retrieval
    of the identifier attribute, providing reliability.

    @rtype: Object
    @return: The value of the identifier attribute of the
    current entity.
    """

    # retrieves the id attribute value from the current object
    id_attribute_value = self.get_id_value()

    # returns the id attribute value
    return id_attribute_value

def get_attribute_data_type(self, attribute_name, resolve_relations = False):
    # retrieves the entity class for the current model
    entity_class = self.__class__

    # using the the entity class and the name of the attribute
    # name retrieves the real data type of the attribute, note that
    # an optional argument is sent to set if the relation should be
    # resolved (type of the id attribute is resolved or not)
    attribute_data_type = entity_class._get_data_type(attribute_name, resolve_relations = resolve_relations)

    # returns the (real) data type of the attribute
    return attribute_data_type

def get_relation_entity_class(self, relation_name):
    # retrieves the entity class
    entity_class = self.__class__

    # retrieves the target relation for the current relation in
    # the context of the entity class as the relation entity class
    relation_entity_class = entity_class.get_target(relation_name)

    # returns the relation entity class
    return relation_entity_class

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

def is_persisted(self):
    """
    Checks the internal structure of the entity
    to guess if the entity  model is persisted.

    The heuristic involves checking the id attribute
    of the entity is already defined.

    This method should be used carefully because
    it assumes the entity id is generated automatically
    on the first save.

    @rtype: bool
    @return: If the current mode is persisted in the
    target data source, checked through heuristics.
    """

    # retrieves the id attribute value checks if id
    # is correctly set (not none) in that case the
    # entity model is considered to be persisted (this
    # is a very bald assumption)
    id_attribute_value = self.get_id_value()
    is_persisted = not id_attribute_value == None

    # returns the is persisted value
    return is_persisted

def is_saved(self):
    """
    Checks the internal structure of the entity
    to check if the last operation being made on
    it was a save.

    @rtype: bool
    @return: If the last operation done in the
    entity was a save.
    """

    # in case the current entity model
    # does not contain the data state value
    if not hasattr(self, DATA_STATE_VALUE):
        # returns false
        return False

    # checks if the current data state
    # is saved (value)
    saved = self.data_state == SAVED_STATE_VALUE

    # returns the saved value
    return saved

def is_updated(self):
    """
    Checks the internal structure of the entity
    to check if the last operation being made on
    it was an update.

    @rtype: bool
    @return: If the last operation done in the
    entity was an update.
    """

    # in case the current entity model
    # does not contain the data state value
    if not hasattr(self, DATA_STATE_VALUE):
        # returns false
        return False

    # checks if the current data state
    # is updated (value)
    updated = self.data_state == UPDATED_STATE_VALUE

    # returns the updated value
    return updated

def is_removed(self):
    """
    Checks the internal structure of the entity
    to check if the last operation being made on
    it was a remove.

    @rtype: bool
    @return: If the last operation done in the
    entity was a remove.
    """

    # in case the current entity model
    # does not contain the data state value
    if not hasattr(self, DATA_STATE_VALUE):
        # returns false
        return False

    # checks if the current data state
    # is removed (value)
    removed = self.data_state == REMOVED_STATE_VALUE

    # returns the removed value
    return removed

def resolve_to_one_value(self, map, model_class):
    """
    Resolves a to one relation from the provided (data) map, this
    operation involves the loading or creation of the corresponding
    relation entity.

    The decision on the creation or loading of the entity is done
    by checking if the identifier value is set in the source map.

    @type map: Dictionary
    @param map: The map that represents the to one relation, this map
    will be used in the creation/loading of the corresponding entity.
    @type model: ModelClass
    @param model: The class representing the type of relation to
    be resolved (this should be the target class of the relation).
    @rtype: Model
    @return: The "resolved" entity model for the given to one
    (map) information.
    """

    # retrieves the (rest) request associated with the current model, this
    # is going to be use to propagate its setting to the created or loaded
    # entity models
    rest_request = self.get_request()

    # retrieves the name of the identifier attribute/field
    # and it's data type, then converts the data type into the
    # target cast type to be used in the casting process
    id_name = model_class.get_id()
    id_data_type = model_class._get_data_type(id_name)
    id_cast_type = DATA_TYPE_CAST_TYPES_MAP.get(id_data_type, None)

    # retrieves the id value of the map casting it to the appropriate
    # data type (may be none in case its a new entity)
    id_value = map.get(id_name, None)

    # in case the id value is an empty value, the entity
    # is set as invalid (unset value)
    if id_value == "": entity = None

    # otherwise in case the the id value is set must try
    # to get it from the data source (load action)
    elif id_value:
        # creates the map of options so that the diffusion
        # scope is the same as the current entity in order
        # to re-use existent entities in the scope
        options = {
            "entities" : self._entities,
            "scope" : self._scope
        }

        # casts the id value into the appropriate data type
        # and uses it to retrieve the appropriate entity value
        # from the data source (load operation)
        id_value = self._cast_safe(id_value, id_cast_type)
        entity = model_class.get(id_value, options, context = rest_request)

        # in case the entity was successfully retrieve applies
        # the map to it and then sets the rest request on the
        # entity, otherwise raises a runtime error because
        # there was a problem in retrieval (invalid)
        if entity: entity.apply(map); entity.set_request(rest_request)
        else: raise RuntimeError("no such model, invalid identifier value")

    # otherwise there is no id value set and a new entity
    # must be created (create action)
    else:
        # tries to retrieve a custom class model class name from
        # the provided relation map, in such case the model class
        # to be used must be retrieved from the entity manager
        class_name = map.get(CLASS_VALUE, None)
        _model_class = class_name and self._entity_manager.get_entity(class_name) or model_class

        # creates the "new" entity (model)
        # and sets it in the current entity
        entity = _model_class.new(map, rest_request)

    # retrieves the loaded or created entity, this
    # entity is considered to be resolved
    return entity

def resolve_to_many_value(self, maps_list, model_class):
    """
    Resolves a to many relation from the provided list of (data)
    maps, this operation involves the loading or creation of the
    corresponding relation entities.

    The decision on the creation or loading of the entities is
    done by checking if the identifier value is set in the source
    map.

    @type maps_list: List
    @param maps_list: The list of maps that represent the to many
    relation, these maps will be used in the creation/loading of
    the corresponding entities.
    @type model: ModelClass
    @param model: The class representing the type of relation to
    be resolved (this should be the target class of the relation).
    @rtype: List
    @return: The list containing the various resolved entities for
    the given to many information.
    """

    # creates the list to hold the various
    # entities of the "to-many" relation
    entitites_list = []

    # in case the received maps list is an empty
    # sequence symbol, (the relation is meant to be set
    # as empty) returns immediately (empty entities list)
    if maps_list == [""]: return entitites_list

    # retrieves the (rest) request associated with the current model, this
    # is going to be use to propagate its setting to the created or loaded
    # entity models
    rest_request = self.get_request()

    # retrieves the name of the identifier attribute/field
    # and it's data type, then converts the data type into the
    # target cast type to be used in the casting process
    id_name = model_class.get_id()
    id_data_type = model_class._get_data_type(id_name)
    id_cast_type = DATA_TYPE_CAST_TYPES_MAP.get(id_data_type, None)

    # gathers all the identifiers (values) from the maps that contain
    # (and define) an identifier, then casts them into the appropriate data type
    id_values_list = [map[id_name] for map in maps_list if id_name in map]
    id_values_list = [self._cast_safe(id_value, id_cast_type) for id_value in id_values_list]

    # creates the options map that retrieves all the entity models
    # in the referred identifiers list and using the current diffusion
    # scope, this should retrieve all the associated entities from the
    # current data source
    options = {
        "filters" : {
            "type" : "in",
            "fields" : {
                id_name : id_values_list
            }
        },
        "entities" : self._entities,
        "scope" : self._scope
    }

    # retrieves all the entity models from the data source that are contained
    # in the range of defined identifiers, avoids retrieving the entity models
    # in case the id values list is empty (performance oriented)
    _entities = id_values_list and model_class.find(options, context = rest_request) or []

    # creates a list containing a series of tuples associating the entity
    # ids with their respective entity and the uses the list of tuples to create
    # map with the same association, this will be used for entity matching
    entity_tuples = [(entity.get_id_value(), entity) for entity in _entities]
    entities_map = dict(entity_tuples)

    # iterates over all the maps present in the maps list list, to create
    # or load various entity instances
    for map in maps_list:
        # retrieves the id value of the current map to check
        # if it's is already present in the loaded entities map
        id_value = map.get(id_name, None)
        id_value = self._cast_safe(id_value, id_cast_type)

        # tries to retrieve the entity model from the (loaded) entities map,
        # in case of failure sets the entity as invalid
        entity = entities_map.get(id_value, None)

        # tries to retrieve a custom class model class name from
        # the provided relation map, in such case the model class
        # to be used must be retrieved from the entity manager
        class_name = map.get(CLASS_VALUE, None)
        _model_class = class_name and self._entity_manager.get_entity(class_name) or model_class

        # in case the entity is valid applies the current item value (data map) to
        # it otherwise creates a "new" entity with the provided model, in both cases
        # the created entity is added to the list of entities for the relations
        if entity: entity.apply(map); entity.set_request(rest_request)
        else: entity = _model_class.new(map, rest_request)
        entitites_list.append(entity)

    # returns the list of entities that were loaded or created for the
    # requested to-many relation
    return entitites_list

def set_context(self, context = None, namespace_name = None, entity_manager = None):
    """
    Sets the current context attributes in the current model
    this provides a transparent process for context attributes
    saving (into the data source).

    @type context: Dictionary
    @param context: The context map to be used to override the
    one provided by the session attribute.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used in the
    context session attribute retrieval, avoids domain name collision.
    @type entity_manager: EntityManager
    @param entity_manager: The optional entity manager reference to
    be used.
    """

    # retrieves the currently available rest request to try
    # to access the session variables
    rest_request = self.get_request()

    # in case the rest request is not currently set in the
    # model the control should be returned immediately
    if not rest_request: return

    # tries to retrieve the rest request session if
    # it fails control is returned immediately
    rest_request_session = rest_request.get_session()
    if not rest_request_session: return

    # retrieves the complete (attribute name) for the context
    # taking into account the namespace name (prefix)
    attribute_name = _get_complete_name("_context", namespace_name)

    # tries to resolve the real context value, in case
    # none is provided tries to retrieve it from session
    # after that in case no valid context is found returns
    # the control immediately
    context = context or rest_request_session.get_attribute(attribute_name)
    if not context: return

    # retrieves the entity manager to be used or the
    # default "embedded" entity manager
    entity_manager = entity_manager or self._entity_manager

    # retrieves the entity class associated with the current
    # entity instance, for name checking
    entity_class = self.__class__

    # iterates over all the items in the current context items
    # to set the attributes in the model (only in case the name
    # exists in the definition)
    for context_name, context_value in context.items():
        # in case the current context item name does not exists
        # in the model definition, continues the loop
        if not entity_class.has_name(context_name): continue

        # in case the entity already contains a value for the
        # context attribute, no need to set it
        if self.has_value(context_name): continue

        # sets the context value in the model this will provide
        # a transparent process for context value saving
        setattr(self, context_name, context_value)

def clear_errors_r(self):
    """
    Clears the internal structure referencing errors from the
    current model structure.

    No more errors are displayed after this call is made.
    This is a recursive method so all the relations of this
    model will have their error structures cleared.
    """

    # clears the validation errors map in the current
    # defined model (clears internal structures)
    self.clear_errors()

    # retrieves the relation names from the
    # current entity to clear their errors
    relation_names = self.get_relation_names()

    # iterates over all the relation names in
    # set of names of the entity
    for relation_name in relation_names:
        # retrieves the value of the relation with
        # the current relation name from the entity
        relation_value = self.get_value(relation_name)

        # in case the relation value is not set or in case it's
        # lazy loaded no error clear should occur
        if relation_value == None or self.is_lazy_loaded(relation_name): continue

        # retrieves the relation value from the entity and then
        # converts it to an enumerable type for compatibility
        # (if required by the relation type)
        relation_value = self.get_value(relation_name)
        relation_is_to_many = self.is_to_many(relation_name)
        relation_value = not relation_is_to_many and [relation_value] or relation_value

        # clears the error structures in all of the relations
        # values using the recursive approach (recursive step)
        for _relation_value in relation_value: _relation_value.clear_errors_r()

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
    lower_cased_entity_class_name = colony.libs.string_util.to_underscore(entity_class_name)

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

    # retrieves the class value and retrieves
    # the type associated with the value
    class_value = getattr(entity_class, key)
    class_value_type = type(class_value)

    # in case the class value type is not
    # dictionary
    if not class_value_type == types.DictType:
        # returns immediately
        return

    # retrieves the value data type
    value_data_type = class_value.get(DATA_TYPE_VALUE, None)

    # in case the data type of the field is relation (presence of an object relation)
    if value_data_type == RELATION_VALUE:
        # retrieves the value type
        value_type = type(value)

        # retrieves the relation information method
        relation_method = getattr(entity_class, "get_relation_attributes_" + key)

        # calls the relation information method to retrieve the relation attributes
        relation_attributes = relation_method()

        # retrieves the relation type and target entity
        relation_type = relation_attributes.get("relation_type", None)
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

def unique_validate(self, attribute_name, attribute_value, properties):
    """
    Validates that there is no entity with the same class as the
    one specified in the validation properties target class attribute
    (defaults to the instance's class in case no target class is specified
    in the properties), that has the specified attribute value for the
    specified attribute name.

    The global property flag may be set to indicate that the attribute
    should be unique across all instances (defaults to false, meaning
    that by the default the validation only ensures that the attribute
    is unique in the current instance).

    In case a duplicate entity is found, an error is added to the
    entity in the specified attribute name.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the model request
    rest_request = self.get_request()

    # retrieves the specified target class where to search
    # for duplicates (uses the instance's class in case no
    # target class is specified)
    target_class = properties.get("target_class", self.__class__)

    # sets the context for retrieval as none in case
    # it is global, otherwise sets it as the rest request
    global_find = properties.get("global", False)
    context = not global_find and rest_request or None

    # creates the filter that will be used
    # to attempt retrieving a duplicate entity
    filter = {
        attribute_name : attribute_value
    }

    # attempts to retrieve an entity that has the specified
    # attribute value for the specified attribute name
    duplicate_entity = target_class.find_one(filter, context = context)

    # in case an entity with the specified attribute value already
    # exists and it is not the same as this instance, then a
    # duplicate was found and a validation error must be added
    if duplicate_entity and not duplicate_entity.object_id == self.object_id:
        # adds an error to the attribute
        self.add_error(attribute_name, "duplicate attribute")

def _validate(self, persist_type):
    # in case the current instance is already in the validating
    # procedure (cycle detected) it must return immediately to
    # avoid stack overflowing (returns as valid to avoid exception)
    if hasattr(self, "_validating") and self._validating == True: return True

    # sets the current entity in the validating operation, this flag
    # should be able to avoid unnecessary recursion
    self._validating = True

    try:
        # validates the relations of the current entity model
        # and retrieves the result of such validation, then
        # validates the current entity model and also retrieves
        # the result of the validation
        relations_result_value = self._validate_relations(persist_type)
        result_value = self.validate()
    finally:
        # restores the validating variable to the original invalid
        # state (avoids possible misbehavior)
        self._validating = False

    # returns the boolean result of the joining of both
    # validation (relations and proper entity model) only
    # returns true in case both are valid
    return relations_result_value and result_value

def _validate_relations(self, persist_type):
    # retrieves the relation names from the current entity
    # to validate them against the
    relation_names = self.get_relation_names()

    # sets the initial value of the validation of the relations
    # to valid (by principle all the relations are considered
    # to be valid until "proven" otherwise)
    is_valid = True

    # iterates over all the relation names in
    # set of names of the entity
    for relation_name in relation_names:
        # retrieves the value of the relation with
        # the current relation name from the entity
        relation_value = self.get_value(relation_name)

        # in case the relation value is not set or in case it's
        # lazy loaded no validation should occur
        if relation_value == None or self.is_lazy_loaded(relation_name):
            # continues the loop, for more
            # relation persistence
            continue

        # retrieves the attributes of the model for the re current relation
        # in order to retrieve the appropriate persist type, then re-calculate
        # the relation persist type based on these values
        model_attributes = getattr(self.__class__, relation_name)
        model_persist_type = model_attributes.get(PERSIST_TYPE_VALUE, PERSIST_NONE_TYPE)
        relation_persist_type = model_persist_type & (persist_type | PERSIST_ASSOCIATE_TYPE)

        # checks if the relation persist type is enough to allow the current
        # relation to be persisted in the data source, in case it's not the
        # relations is not validated
        if not relation_persist_type & (PERSIST_SAVE_TYPE | PERSIST_UPDATE_TYPE): continue

        # starts the flag that controls in case
        # an error is set
        error_set = False

        # retrieves the relation value from the entity and then
        # converts it to an enumerable type for compatibility
        # (if required by the relation type)
        relation_value = self.get_value(relation_name)
        relation_is_to_many = self.is_to_many(relation_name)
        relation_value = not relation_is_to_many and [relation_value] or relation_value

        # iterates over all the relation values for storage
        # in case a validation fails it accumulates the various
        # errors around the storing procedure "soft fail"
        for _relation_value in relation_value:
            # in case the relation value is not set or in case it's
            # lazy loaded no validation should occur
            if relation_value == None or self.is_lazy_loaded(relation_name):
                # continues the loop, for more
                # relation persistence
                continue

            # validates the relation value, retrieving the result of
            # such validation in case it't valid there's no data
            # structures to be updated, continues loop
            result = _relation_value._validate(relation_persist_type)
            if result: continue

            # updates the error set flag so that the relation validation
            # failed error is set and update the is valid flag so that the
            # set of relations validation is correctly updated
            error_set = True
            is_valid = False

        # adds an error to the entity on the relation
        # for latter usage
        error_set and self.add_error(relation_name, "relation validation failed")

    # returns the relations is/are valid result,
    # this value may be used to infer if the parent
    # object should be considered to be valid
    return is_valid

def _get_complete_name(name, namespace_name = None):
    """
    Retrieves the complete (session attribute) name from the session
    attribute name and the namespace name.

    The complete name is created using the namespace name as a prefix
    to the final (and complete) value.

    @type name: String
    @param name: The session attribute name (base name).
    @type namespace_name: String
    @param namespace_name: The namespace name to be used as prefix.
    @rtype: String
    @return: The complete session attribute name, created through
    the prefix strategy.
    """

    # in case the namespace name is not set
    # no need to proceed with the prefix strategy
    # the name is the "original" name
    if not namespace_name: return name

    # creates the complete (session attribute) name by prepending the namespace
    # name to the (session attribute) name and returns it
    complete_name = namespace_name + "." + name
    return complete_name
