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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import os
import re
import types

import colony.libs.time_util
import colony.libs.crypt_util
import colony.libs.control_util
import colony.libs.structures_util

import utils
import exceptions

VALIDATION_METHOD_SUFFIX = "_validate"
""" The validation method suffix """

DEFAULT_VALIDATION_CONTEXT = "default"
""" The default validation context """

LAZY_LOADED_VALUE = "%lazy-loaded%"
""" The lazy loaded value """

REGEX_VALUE = "regex"
""" The regex value """

TARGET_VALUE = "target"
""" The target value """

VALUES_VALUE = "values"
""" The values value """

DATA_TYPE_VALUE = "data_type"
""" The data type value """

RELATION_VALUE = "relation"
""" The relation value """

SECURE_VALUE = "secure"
""" The secure value """

CLASS_VALUE = "_class"
""" The class value """

PARAMETERS_VALUE = "_parameters"
""" The parameters value """

MODIFIED_TIME_VALUE = "_mtime"
""" The modified time value """

VALIDATION_FAILED_MESSAGE = "validation failed"
""" The (default) validation failed message """

EMAIL_REGEX_VALUE = "^[\w\d\._%+-]+@[\w\d\.\-]+$"
""" The email regex value """

URL_REGEX_VALUE = "^\w+\:\/\/[^\:\/\?#]+(\:\d+)?(\/[^\?#]+)*\/?(\?[^#]*)?(#.*)?$"
""" The url regex value """

EMAIL_REGEX = re.compile(EMAIL_REGEX_VALUE)
""" The email regex """

URL_REGEX = re.compile(URL_REGEX_VALUE)
""" The url regex """

TO_ONE_RELATION = "to-one"
""" The string value of a "to-one" relation """

TO_MANY_RELATION = "to-many"
""" The string value of a "to-many" relation """

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

METHOD_TYPES = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinMethodType,
    types.BuiltinFunctionType
)
""" The tuple containing the various types considered to be
functions or methods """

def _start_model(self):
    """
    Starts the model structures.
    This is method is considered to be the model's
    initializer and calls the start and set validation
    methods in the model (for user code).
    """

    # checks if the model has been already
    # started (avoids duplicate initialization, in
    # case of sub-classing)
    if hasattr(self, "model_started"):
        # returns immediately (model already
        # started)
        return

    # starts the underlying rest request reference
    # as unset, should be set after the start operation
    # if access to session is required
    self.rest_request = None

    # starts the validation map associating
    # an attribute name with the validation methods
    self.validation_map = {}

    # start the validation errors map associating an
    # attribute name with the list of errors
    self.validation_errors_map = {}

    # sets the initial (and default) context for
    # the running of the validation process
    self.validation_context = DEFAULT_VALIDATION_CONTEXT

    # starts the map that will hold the various
    # parameter attributes of the model, this is going
    # to be used for attributes that should not make
    # part of the core model definition
    self._parameters = {}

    # in case the model has the start method
    if hasattr(self, "start"):
        # calls the start method (to be implemented)
        self.start()

    # in case the model has the set validation method
    if hasattr(self, "set_validation"):
        # calls the set validation method (to be implemented)
        self.set_validation()

    # sets the model started flag as true
    self.model_started = True

def _class_new(cls, map = None, rest_request = None):
    """
    Creates a new model instance, applying the given map
    of "form" options to the created model.
    This method should be used as a "handy" constructor of
    new entities from a previously received used form information.

    An optional rest request reference may be used to enable
    the model to access session variables (information).

    @type map: Dictionary
    @param map: The map of "form" options to be used to create
    the new model instance.
    @type rest_request: RestRequest
    @param rest_request: The rest request to be used in the context
    of the current model, it should enable access to session attributes.
    @rtype: Model
    @return: The newly created model with the attributes
    already "populated" with the map contents.
    """

    # checks if the provided map (reference) is in fact a sequence
    # and so a proxy model (for sequences) must be created, this way
    # it's possible to offer bulk operations
    is_sequence = type(map) in (types.ListType, types.TupleType)

    # creates a new model from the class reference
    # the default values should be applied
    model = ModelProxy(cls, len(map)) if is_sequence else cls()

    # sets the rest request in the model according
    # to the provided reference value, this is used
    # in a set of operation that require for instance
    # session variables information
    model.set_request(rest_request)

    # in case a map is provided, must apply
    # the contents of it to the model
    map and model.apply(map)

    # returns the created model
    return model

def _class_get_system(cls):
    """
    Class method that retrieves the system instance associated
    with the current model class.
    This method should not overlap the get system method on the
    instance, and you should used this one to retrieve the absolute
    related system instance, avoiding problems with inheritance.

    @rtype: Object
    @return: The system instance associated with the current
    model class.
    """

    return cls._system_instance

def _class_get_plugin(cls):
    """
    Class method that retrieves the plugin instance associated
    with the current model class.
    This method should not overlap the get plugin method on the
    instance, and you should used this one to retrieve the absolute
    related system instance, avoiding problems with inheritance.

    @rtype: Plugin
    @return: The plugin instance associated with the current
    model class.
    """

    return cls._system_instance.plugin

def _class_get_context_attribute_g(cls, name, context_request, namespace_name = None):
    """
    Retrieves a context attribute with the provided name using the
    provided context request as the source for the retrieval.

    The method is oriented towards defaulting to invalid values, so
    if no value is found an invalid value is returned.

    @type name: String
    @param name: The name of the context attribute to be retrieved.
    @type context_request: RestRequest
    @param context_request: The rest request to be used for the
    retrieval of the context to be used in attribute retrieval.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used in the
    context session attribute retrieval, avoids domain name collision.
    @rtype: Object
    @return: The retrieves context attribute that may assume any valid
    data type.
    """

    # in case the context request is defined retrieves the session
    # associated with it otherwise sets it as invalid (not defined)
    session = context_request.get_session() if context_request else None

    # retrieves the complete (attribute name) for the context
    # taking into account the namespace name (prefix)
    context_name = _get_complete_name("_context", namespace_name)

    # in case the session is defined retrieves the context attribute
    # from it otherwise default to empty map then uses the context map
    # to retrieves the attribute for the requested name and returns it
    # to the caller method
    context = session.get_attribute(context_name) if session else {}
    attribute = context and context.get(name, None) or None
    return attribute

def _class_get_resource_path(cls, resource_path):
    """
    Retrieves the complete and absolute path to the resource
    identified by the provided (relative) resource path.

    This method assumes that there is a plugin associated with
    the owner system instance and uses it as reference.

    @type resource_path: String
    @param resource_path: The (relative) path to the resource
    to be used for complete path resolution.
    @rtype: String
    @return: The complete (and resolved) path to the resource
    identified by the provided relative path.
    """

    # retrieves the currently associated plugin (using the provided
    # system instance) and then retrieves the identifier and the
    # plugin manager from it
    plugin = cls._system_instance.plugin
    plugin_id = plugin.id
    plugin_manager = plugin.manager

    # retrieves the plugin path for the current plugin associated
    # with the model (class reference)
    plugin_path = plugin_manager.get_plugin_path_by_id(plugin_id)

    # creates the full absolute resource path from the plugin path,
    # the current resources path and the resource path, then returns
    # it to the caller method
    resource_path = os.path.join(
        plugin_path,
        cls._resources_path,
        resource_path
    )
    return resource_path

def apply(self, map):
    """
    "Applies" the given map of "form" values into the current
    model (setting of attributes).
    The application of the values follows the standard string to
    data type conversion and respects the security attributes of
    the model definition.

    The application of the map follows a recursive approach and
    a correct configuration of the security attributes must be followed
    to avoid possible malicious problems.

    @type map: Dictionary
    @param map: The map containing the various "form" values to be used
    to "apply" the values in the model.
    """

    # detaches the current model, to avoid any possible
    # undesired loading of relations, this could cause
    # an infinite loop in latter persistence
    self.detach(force = False)

    try:
        # retrieves the class of the model
        # as the reference class and then uses
        # it to retrieve the complete set of
        # attr method for it (to be ignored)
        cls = self.__class__
        attr_methods = cls.get_all_attr_methods()

        # iterates over all the items in the map to
        # apply the to the current model
        for item_name, item_value in map.items():
            # in case the class or the parameters (reserved values)
            # item is found, special handling is required
            if item_name in (CLASS_VALUE, PARAMETERS_VALUE, MODIFIED_TIME_VALUE):
                # sets the class or parameters "directly"
                # in the model
                setattr(self, item_name, item_value)

                # continues the loop no need to
                # continue with the casting
                continue

            # in case the item name is set in the attribute methods
            # map it refers a "calculated" attribute and as such must
            # be ignored as it's just a stub value
            if item_name in attr_methods: continue

            # in case the item name is not defined in the class
            # reference an exception should be raised, impossible
            # to retrieve the required information
            if not hasattr(cls, item_name):
                # raises a model apply exception
                raise exceptions.ModelApplyException(
                    "item name '%s' not found in model class '%s'" %
                        (item_name, cls.__name__)
                )

            # retrieves the class value and retrieves
            # the type associated with the value
            class_value = getattr(cls, item_name)
            class_value_type = type(class_value)

            # in case the class value type is not
            # dictionary (meta information dictionary),
            # cannot retrieve the required information
            if not class_value_type == types.DictType:
                # raises a model apply exception
                raise exceptions.ModelApplyException(
                    "item name '%s' not defined in model class '%s'" %
                        (item_name, cls.__name__)
                )

            # retrieves the value data type and secure
            # attributes to "take some decisions"
            value_data_type = class_value.get(DATA_TYPE_VALUE, None)
            value_secure = class_value.get(SECURE_VALUE, False)

            # in case the value is a secure attribute
            # (cannot change it automatically), continues
            # the loop cannot change the value
            if value_secure: continue

            # in case the data type of the field is relation
            # (presence of an object relation)
            if value_data_type == RELATION_VALUE:
                # retrieves the relation information method
                relation_method = getattr(cls, "_relation_" + item_name)

                # calls the relation information method to retrieve the relation attributes
                relation_attributes = relation_method()

                # retrieves the relation type and target (entity) model
                relation_type = relation_attributes.get("type", None)
                target_model = relation_attributes.get("target", object)

                # in case the relation is of type "to-one"
                if relation_type == TO_ONE_RELATION:
                    # tries to retrieve the "current" target
                    # entity to be used for the application
                    target_entity = self.get_value(item_name)

                    # in case there is no item (target entity)
                    # in the entity one must be created
                    if target_entity == None:
                        # "resolves" the target to one relation, loading or creating
                        # the required model and sets the retrieved (target) entity
                        # in the current model instance
                        target_entity = self.resolve_to_one_value(item_value, target_model)
                        setattr(self, item_name, target_entity)

                    # otherwise the entity already contains the
                    # item it must be "re-used" and merged
                    # with the item value
                    else:
                        # updates the item in the entity with
                        # the map containing the value
                        target_entity.apply(item_value)

                # in case the relation is of type "to-many"
                elif relation_type == TO_MANY_RELATION:
                    # "resolves" the target to many relation, loading or
                    # creating the required models and sets the target entities
                    # list in the current model instance
                    target_entitites_list = self.resolve_to_many_value(item_value, target_model)
                    setattr(self, item_name, target_entitites_list)

            # otherwise it's a single attribute relation
            # the normal setting should apply
            else:
                # sets the attribute in the current model
                self._set_attribute(item_name, item_value)
    finally:
        # attaches the entity back to the data source
        # for correct persistence structures
        self.attach(force = False)

def get_system(self):
    """
    Retrieves the current (associated) system instance
    reference that can be used to retrieve the plugin
    internal state and global data reference.

    @rtype: Object
    @return: The system instance associated with the current
    entity model.
    """

    return self._system_instance

def get_plugin(self):
    """
    Retrieves the current (associated) plugin instance
    reference that can be used to retrieve the plugin
    internal state and global data reference.

    @rtype: Object
    @return: The plugin instance associated with the current
    entity model.
    """

    return self._system_instance.plugin

def get_attribute_name(self, attribute_name):
    """
    Retrieves the attribute from the given composite
    attribute name.
    The attribute is retrieved using a composite approach
    and the name is separated by dots.

    @type attribute_name: String
    @param attribute_name: The name of the attribute
    to be retrieved.
    @rtype: Object
    @return: The attribute for the given attribute name.
    """

    # splits the attribute name into tokens
    attribute_name_tokens = attribute_name and attribute_name.split(".") or []

    # sets the initial current attribute value
    current_attribute = self

    # iterates over all the attribute name tokens
    for attribute_name_token in attribute_name_tokens:
        # updates the current attribute with the attribute name token
        current_attribute = current_attribute.get_value(attribute_name_token)

    # returns the current attribute
    return current_attribute

def dumps(self, serializer):
    """
    Serializes (dumps) the current object with
    the given serializer object.

    @type serializer: Serializer
    @param serializer: The serializer object to be used
    to serialize the current object.
    @rtype: String
    @return: The serialized value.
    """

    # serializes the object (dumps)
    data = serializer.dumps(self)

    # returns the serialized value (data)
    return data

def loads(self, serializer, data):
    """
    Unserializes (loads) converting and loading
    the given data into the current object.

    @type serializer: Serializer
    @param serializer: The serializer object to be used
    to unserialize the given data.
    @rtype: String
    @return: The serialized data to be loaded.
    """

    # unserializes the data (loads)
    # retrieving the model
    model = serializer.loads(data)

    # iterates over all the dictionary items
    # to load the values (from the model)
    for key, value in model.items():
        # loads the given value in the current object
        self._load_value(key, value)

def _load_value(self, key, value):
    """
    Loads the value with the given key in the
    current object.

    @type key: String
    @param key: The key to be used to refer to the value
    in the current object.
    @type value: Object
    @param value: The value to be set in the current object.
    """

    # in case the current object does not contain
    # an attribute with the key name must return
    # immediately, nothing to be set
    if not hasattr(self, key): return

    # sets the value in the current object
    setattr(self, key, value)

def is_lazy_loaded(self, attribute_name):
    """
    Indicates if the specified attribute
    is lazy loaded.

    @type attribute_name: String
    @param attribute_name: The attribute name.
    @rtype: bool
    @return: The lazy loaded flag.
    """

    # sets the lazy loaded flag in case
    # the attribute value is not present
    lazy_loaded = not self.has_value(attribute_name)

    # returns the lazy loaded flag
    return lazy_loaded

def lock_session(self):
    """
    Locks the session associated with the current rest request,
    subsequent accesses to the session will be blocked until the
    session is released.
    """

    # tries to retrieve the rest request session
    rest_request_session = self.rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # start a session if none is started and then
        # retrieves it from the rest request
        self.rest_request.start_session()
        rest_request_session = self.rest_request.get_session()

    # locks the "just" retrieved (or created) rest request
    # session (blocks it)
    rest_request_session.lock()

def release_session(self):
    """
    Releases the session associated with the current rest request,
    allowing further requests to access the session to be passed.
    """

    # tries to retrieve the rest request session
    rest_request_session = self.rest_request.get_session()

    # in case the rest request session is invalid
    # an exception should be raised (invalid situation)
    if not rest_request_session: raise RuntimeError("problem releasing session, no session available")

    # releases the "just" retrieved rest request
    # session (unblocks it)
    rest_request_session.release()

def get_session_attribute(self, session_attribute_name, namespace_name = None, unset_session_attribute = False):
    """
    Retrieves the session attribute from the current rest request
    with the given name and for the given namespace.
    Optionally it may be unset from session after retrieval.

    @type namespace_name: String
    @param namespace_name: The name of the namespace for the
    attribute to be retrieved.
    @type unset_session_attribute: bool
    @param unset_session_attribute: If the session attribute should
    be unset after retrieval.
    @rtype: Object
    @return The retrieved session attribute.
    """

    # retrieves the currently available rest request to try
    # to access the session variables
    rest_request = self.get_request()

    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid, must return invalid
    if not rest_request_session: return None

    # resolves the complete session attribute name
    session_attribute_name = _get_complete_name(session_attribute_name, namespace_name)

    # retrieves the attribute from the session
    session_attribute = rest_request_session.get_attribute(session_attribute_name)

    # in case the unset the session attribute flag is set
    # the session attribute is unset
    unset_session_attribute and rest_request_session.unset_attribute(session_attribute_name)

    # returns the session attribute
    return session_attribute

def set_session_attribute(self, session_attribute_name, session_attribute_value, namespace_name = None):
    """
    Sets the session attribute in the current rest request
    with the given name and for the given namespace.
    The session attribute value may be of any type.

    @type session_attribute_name: String
    @param session_attribute_name: The name of the session
    attribute to be set.
    @type session_attribute_value: Object
    @param session_attribute_value: The value of the session
    attribute to be set.
    @type namespace_name: String
    @param namespace_name: The name of the namespace for the
    attribute to be set.
    """

    # retrieves the currently available rest request to try
    # to access the session variables
    rest_request = self.get_request()

    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # start a session if none is started and then
        # retrieves it from the rest request
        rest_request.start_session()
        rest_request_session = rest_request.get_session()

    # resolves the complete session attribute name
    session_attribute_name = _get_complete_name(session_attribute_name, namespace_name)

    # sets the attribute in the session
    rest_request_session.set_attribute(session_attribute_name, session_attribute_value)

def unset_session_attribute(self, session_attribute_name, namespace_name = None):
    """
    Unsets the session attribute from the current rest request
    with the given name and for the given namespace.

    @type session_attribute_name: String
    @param session_attribute_name: The name of the session
    attribute to be unset.
    @type namespace_name: String
    @param namespace_name: The name of the namespace for the
    attribute to be unset.
    """

    # retrieves the currently available rest request to try
    # to access the session variables
    rest_request = self.get_request()

    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # returns none (invalid)
        return None

    # resolves the complete session attribute name
    session_attribute_name = _get_complete_name(session_attribute_name, namespace_name)

    # unsets the attribute from the session
    rest_request_session.unset_attribute(session_attribute_name)

def get_context_attribute(self, context_name, namespace_name = None):
    """
    Retrieves the value of the context attribute with the
    provided name.

    In case no attribute is found a none value is returned.

    @type context_name: String
    @param context_name: The name of the of the context attribute
    to retrieve the value.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used
    for the context (session) variable to be retrieved.
    @rtype: Object
    @return:  The value of the requested context attribute.
    """

    # retrieves the context defaulting to a new and empty map
    # in case an invalid session attribute is returned
    context = self.get_session_attribute("_context", namespace_name)
    if context == None: context = {}

    # returns the retrieves attribute value, defaulting to none
    # in case it's not present in the context map
    return context.get(context_name, None)

def set_context_attribute(self, context_name, context_value, override = True, namespace_name = None):
    """
    Sets the context attribute with the provided name with
    the provided value.

    An optional override variable is provided so that is
    possible to override an already present context value
    with the same name (conflict resolution).

    @type context_name: String
    @param context_name: The name of the of the context attribute
    to set the value.
    @type context_value: Obejct
    @param context_value: The value to be set fot the attribute.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used
    for the context (session) variable to be updated.
    """

    # retrieves the context defaulting to a new and empty map
    # in case an invalid session attribute is returned
    context = self.get_session_attribute("_context", namespace_name)
    if context == None: context = {}

    # updates the context with the provided attribute, overriding
    # the already present value in case the flag is set and then
    # sets the context map "back" in the session
    if override or not context_name in context: context[context_name] = context_value
    self.set_session_attribute("_context", context, namespace_name)

def unset_context_attribute(self, context_name, namespace_name = None):
    """
    Unsets the context attribute with the provided name.

    This operation should remove any reference to the context
    attribute in the current session

    @type context_name: String
    @param context_name: The name of the of the context attribute
    to be unset.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used
    for the context (session) variable to be updated.
    """

    # retrieves the context defaulting to a new and empty map
    # in case an invalid session attribute is returned
    context = self.get_session_attribute("_context", namespace_name)
    if context == None: context = {}

    # updates the context with the provided attribute, removing
    # the already present value and then sets the context map
    # "back" in the session
    if context_name in context: del context[context_name]
    self.set_session_attribute("_context", context, namespace_name)

def add_validation_method(self, attribute_name, validation_method_name, validate_null = False, properties = {}, contexts = (DEFAULT_VALIDATION_CONTEXT,)):
    """
    Adds a validation method to the attribute with the given name.
    The adding of the validation can be configured using the properties
    map.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to "receive" the validation.
    @type validation_method_name: String
    @param validation_method_name: The name of the validation method to be added to the attribute.
    @type validate_null: bool
    @param validate_null: If the validation method should be applied to
    null attribute values.
    @type properties: Dictionary
    @param properties: The properties of the adding of the validation method.
    @type contexts: Tuple
    @param contexts: The (validation) contexts for which the the validation
    method should be applied.
    """

    # adds the validation method suffix to the validate method name
    validation_method_name = validation_method_name + VALIDATION_METHOD_SUFFIX

    # in case the validation method does not exist in
    # the current object
    if not hasattr(self, validation_method_name):
        # raises an invalid validation method exception
        raise exceptions.InvalidValidationMethod("the current validation method does not exist: " + validation_method_name)

    # retrieves the validation method
    validation_method = getattr(self, validation_method_name)

    # adds the "custom" validation method to the current model
    self.add_custom_validation_method(attribute_name, validation_method, validate_null, properties, contexts)

def add_custom_validation_method(self, attribute_name, validation_method, validate_null = False, properties = {}, contexts = (DEFAULT_VALIDATION_CONTEXT,)):
    """
    Adds a "custom" validation method to the attribute with the given name.
    The adding of the validation can be configured using the properties
    map.
    This method should be used carefully and should be considered a secondary
    resource for attribute validation.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to "receive" the validation.
    @type validation_method: Function
    @param validation_method: The the validation method to be added to the attribute.
    @type validate_null: bool
    @param validate_null: If the validation method should be applied to
    null attribute values.
    @type properties: Dictionary
    @param properties: The properties of the adding of the validation method.
    @type contexts: Tuple
    @param contexts: The (validation) contexts for which the the validation
    method should be applied.
    """

    # creates the validation tuple as the set of the validation
    # method and the properties
    validation_tuple = (
        validation_method,
        validate_null,
        properties
    )

    # iterates over all the defined contexts to update
    # the appropriate internal structures
    for context in contexts:
        # retrieves the context validation map from the validation
        # map (creating a new map if necessary)
        context_validation_map = self.validation_map.get(context, {})

        # retrieves the attribute validation list from the context
        # validation map (creating a new list if necessary)
        attribute_validation_list = context_validation_map.get(attribute_name, [])

        # adds the validation tuple to the
        # attribute (validation) list
        attribute_validation_list.append(validation_tuple)

        # sets the correct references in the structures
        context_validation_map[attribute_name] = attribute_validation_list
        self.validation_map[context] = context_validation_map

def add_error(self, attribute_name, error_message, avoid_duplicates = True):
    """
    Adds an error to the validation error map.
    This error may be used latter for "verbosity" purposes.

    Duplicate error message may be avoided in case the extra flag
    is set (default behavior).

    @type attribute_name: String
    @param attribute_name: The name of the attribute to witch
    there is going to be added an error.
    @type error_message: String
    @param error_message: The error message to be added.
    @type avoid_duplicates: bool
    @param avoid_duplicates: If duplicate error message should be
    avoided (this should imply extra resources).
    """

    # in case the attribute name is not defined in the validation
    # errors map
    if not attribute_name in self.validation_errors_map:
        # starts the validation errors map for the attribute name
        # as an empty list
        self.validation_errors_map[attribute_name] = []

    # retrieves the validation errors (list) for the
    # requested attribute name, will be used for the checking
    # and insertion operations, avoids insertion in case the
    # avoid duplicates flag is set and the error message is
    # already present in the validation errors list
    validation_errors = self.validation_errors_map[attribute_name]
    if avoid_duplicates and error_message in validation_errors: return

    # adds the validation error to the validation error
    # list for the attribute name
    validation_errors.append(error_message)

def clear_errors(self):
    """
    Clears the internal structure referencing errors from the
    current model structure.

    No more errors are displayed after this call is made.
    Note that no recursion is done so no related structure
    are cleared from errors.
    """

    # resets the validation errors map, by constructing
    # a new map to hold the values (clear process)
    self.validation_errors_map = {}

def validate(self):
    """
    Validates all the attributes in the current object.
    This method returns if the validation was successful or not.

    @rtype: bool
    @return: If the model validation was successful or not.
    """

    # checks if the current model contains the pre validate
    # method, in such case the method is called to signal
    # the start of the validation process
    if hasattr(self, "pre_validate"): self.pre_validate()

    # retrieves the context validation map for the current validation context
    context_validation_map = self.validation_map.get(self.validation_context, {})

    # iterates over all the items in the context validation map
    for attribute_name, validation_tuple_list in context_validation_map.items():
        # in case the current model is already stored no need to
        # to validate a non existent attribute (it's not going to be
        # persisted and the value in the data source was already validated)
        # the data model remains consistent for sure
        if self.is_stored() and not self.has_value(attribute_name): continue

        # retrieves the attribute value
        attribute_value = self.get_value(attribute_name)

        # iterates over all the validation tuples
        for validation_tuple in validation_tuple_list:
            # retrieves the validation method the validate null and properties
            # from the validation tuple
            validation_method, validate_null, properties = validation_tuple

            # in case the validate null is not set and the
            # attribute value is none (skip)
            if not validate_null and attribute_value == None:
                # continues the loop
                continue

            # calls the validation method for validation on the
            # given attribute from the model
            validation_method(attribute_name, attribute_value, properties)

    # checks if the current validation process has success
    # running (all the validation tests passed)
    is_valid = self.is_valid()

    # in case the validation was not successful and the current
    # model contains the fail validate method defined it's called
    # to signal the failure of the validation process
    if not is_valid and hasattr(self, "fail_validate"): self.fail_validate()

    # checks if the current model contains the post validate
    # method, in such case the method is called to signal
    # the end of the validation process
    if hasattr(self, "post_validate"): self.post_validate()

    # returns if the structure is valid, all tests passed
    # with expected success
    return is_valid

def validate_exception(self, exception_message = VALIDATION_FAILED_MESSAGE, error_description = True):
    """
    Validates all the attributes in the current object.
    This method raises an exception in case an error occurs.

    @type exception_message: String
    @param exception_message: The message to be used in creating
    the model validation exception to be raised.
    @type error_description: String
    @param error_description: The description to be used in creating
    the model validation exception to be raised.
    """

    # validates the current model retrieving the result
    # of the validation for exception raising
    model_valid = self.validate()

    # in case the model is valid nothing is required to be done
    # and so it returns immediately
    if model_valid: return

    # retrieves the model validation errors map
    # and uses them to raise the appropriate exception
    model_validation_errors_map = self.validation_errors_map
    raise exceptions.ModelValidationError(exception_message + ": " + str(model_validation_errors_map), self)

def is_valid(self):
    """
    Retrieves if the current structure is valid.

    @rtype: bool
    @return: If the current structure is valid.
    """

    # in case the validation errors map
    # is not valid or empty
    if self.validation_errors_map:
        # returns false (invalid)
        return False
    # otherwise it's empty (no errors)
    else:
        # returns true (valid)
        return True

def is_stored(self):
    """
    Checks if the given model is stored in a previously defined
    secondary storage system.

    For the base model it's always considered (by default) to be
    not stored (transient).

    @rtype: bool
    @return: If the current model is stored in the hypothetical
    secondary storage system, considered always false (no persistence
    layer present).
    """

    # in case the is persisted method is present, it should
    # be used to check if the model is stored in a secondary
    # storage systems otherwise it's always considered to be
    # a transient model (default case)
    if hasattr(self, "is_persisted"): return self.is_persisted()
    return False

def set_request(self, rest_request):
    """
    Sets the (rest) request into the current model instance.
    This value is going to be used to access session information
    from the model.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be set into the
    current model instance.
    """

    # in case the current model contains the scope map defined
    # the request is sent there for scope wide usage, otherwise the
    # "normal" rest request variable is used
    if hasattr(self, "_scope"): self._scope["request"] = rest_request
    else: self.rest_request = rest_request

def get_request(self):
    """
    Retrieves the (rest) request from the current model instance.
    This value is used to access session information from the model.

    @rtype: RestRequest
    @return: The retrieve rest request from the current model instance.
    """

    # in case the current model contains the scope map defined the request
    # is retrieved from there, otherwise the "normal" rest request variable
    # is used for the retrieval
    if hasattr(self, "_scope"): rest_request = self._scope.get("request", self.rest_request)
    else: rest_request = self.rest_request
    return rest_request

def get_validation_context(self):
    """
    Retrieves the validation context.

    @rtype: String
    @return: The validation context.
    """

    return self.validation_context

def set_validation_context(self, validation_context):
    """
    Sets the validation context.

    @type validation_context: String
    @param validation_context: The validation context.
    """

    self.validation_context = validation_context

def not_unset_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is not unset.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the attribute value is "invalid" (unset)
    if not attribute_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is unset")

def not_none_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is not none.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the attribute value is none
    if attribute_value == None:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is none")

def not_empty_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is not empty.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the attribute value is empty
    if len(attribute_value) == 0:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is empty")

def is_stripped_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it has no trailing or leading spaces.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the stripped version of the attribute value
    stripped_attribute_value = attribute_value.strip()

    # in case the attribute value has extraneous spaces
    if not attribute_value == stripped_attribute_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value has extraneous whitespaces")

def length_equal_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its length is equal to the target.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not equal to the target value
    if not len(attribute_value) == target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("length of value is not equal to %s", target_value))

def length_less_than_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its length is less than target.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not less than
    # the target value
    if not len(attribute_value) < target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("length of value is greater than or equal to %s", target_value))

def length_less_than_or_equal_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its length is less than or equal to the target.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not less than
    # or equal to the target value
    if not len(attribute_value) <= target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("length of value is greater than %s", target_value))

def length_greater_than_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its length is greater than target.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not less than
    # the target value
    if not len(attribute_value) > target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("length of value is less than or equal to %s", target_value))

def length_greater_than_or_equal_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its length is greater than or equal to the target.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not less than
    # or equal to the target value
    if not len(attribute_value) >= target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("length of value is less than %s", target_value))

def in_enumeration_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its value belongs to the
    enumeration defined in the properties values list.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the values from the properties
    values = properties[VALUES_VALUE]

    # in case the attribute value is not in the values
    if not attribute_value in values:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is not in enumeration")

def not_in_enumeration_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its value is not in the
    enumeration defined in the properties values list.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the values from the properties
    values = properties[VALUES_VALUE]

    # in case the attribute value is in the values
    if attribute_value in values:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is in enumeration")

def is_equal_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its value is equal
    to another specified attribute.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the values are different
    if not attribute_value == target_value:
        # adds the error to the given attribute name
        self.add_error(attribute_name, "value is different")

def is_different_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that its value is different
    from the other specified attribute.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the values are the same
    if attribute_value == target_value:
        # adds the error to the given attribute name
        self.add_error(attribute_name, "value is the same")

def greater_than_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is greater than the target value.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not
    # greater than the target value
    if not attribute_value > target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("value is less than or equal to %s", target_value))

def greater_than_zero_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is greater than zero.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the attribute value is not greater than zero
    if not attribute_value > 0:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is less than or equal to zero")

def greater_than_or_equal_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is greater than or equal to the target.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not greater
    # than or equal to the target value
    if not attribute_value >= target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("value is less than %s", target_value))

def greater_than_or_equal_to_zero_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is greater than or equal to zero.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the attribute value is not greater than or equal to zero
    if not attribute_value >= 0:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is less than zero")

def less_than_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is less than the target value.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not
    # less than the target value
    if not attribute_value < target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("value is greater than or equal to %s", target_value))

def less_than_zero_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is less than zero.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the attribute value is not less than zero
    if not attribute_value < 0:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is greater than or equal to zero")

def less_than_or_equal_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is less than or equal to the target.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not less
    # than or equal to the target value
    if not attribute_value <= target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, colony.libs.structures_util.FormatTuple("value is greater than %s", target_value))

def less_than_or_equal_to_zero_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is less than or equal to zero.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the value is not less than or equal to zero
    if not attribute_value <= 0:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is greater than zero")

def is_url_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that the value is an url.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # checks if the attribute value matches the regular expression
    match = URL_REGEX.match(attribute_value)

    # in case the value is not an url
    if not match:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is not an url")

def is_email_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that the value is an email.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # checks if the attribute value matches the regular expression
    match = EMAIL_REGEX.match(attribute_value)

    # in case the value is not an email
    if not match:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is not an email")

def is_id_number_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that the value is an id number.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the control value
    control_value = attribute_value % 10

    # removes the control value from the attribute value
    id_number = attribute_value / 10

    # calculates the control value
    calculated_control_value = colony.libs.control_util.calculate_id_number_control_value(id_number)

    # in case the control value doesn't match the calculated one
    if not control_value == calculated_control_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is not a valid id number")

def is_tax_number_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that the value is a tax number.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the control value
    control_value = attribute_value % 10

    # removes the control value from the attribute value
    tax_number = attribute_value / 10

    # calculates the control value
    calculated_control_value = colony.libs.control_util.calculate_tax_number_control_value(tax_number)

    # in case the control value doesn't match the calculated one
    if not control_value == calculated_control_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is not a valid tax number")

def matches_regex_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it matches the provided regular expression.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the "regex" (the "regex" string is
    # passed instead of the compiled regular
    # expression or else the model would become
    # unserializable)
    regex = properties[REGEX_VALUE]

    # matches the regex
    match = re.match(regex, attribute_value)

    # in case no match was found
    if not match:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value has incorrect format")

def all_different_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it has no duplicate values.
    This "validator" expects the attribute value to be a list, and will
    search the list's items for the specified attribute, adding validation
    errors in case more than one item has the same attribute value.
    These validation errors will be added to the attribute being
    validated, the referenced composite attribute, and the model
    to which the composite attribute belongs.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target
    target = properties[TARGET_VALUE]

    # initializes the validation failed flag
    validation_failed = False

    # retrieves the target attribute name which is the
    # last token in the specified composite attribute name
    target_tokens = target and target.split(".") or []
    target_attribute_name = target_tokens and target_tokens[-1] or target

    # retrieves the name of the attribute from which
    # the target attribute name is accessed if any
    model_attribute_name = len(target_tokens) > 1 and target_tokens[-2] or None

    # initializes the allocated entities map
    allocated_entities_map = {}

    # for each model in the attribute value
    for model in attribute_value:
        # attempts to retrieve the attribute name
        try:
            # retrieves the attribute value
            value = model.get_attribute_name(target)
        # in case retrieving the attribute name
        # caused and error when attempting to
        # access an attribute in an undefined model
        except:
            # continues to the next model
            continue

        # associates the model with the value in order
        # to later detect which entities have duplicate attributes
        allocated_entities = allocated_entities_map.get(value, [])
        allocated_entities.append(model)
        allocated_entities_map[value] = allocated_entities

    # retrieves the allocated entities lists that have more
    # than one model and are therefore invalid
    allocated_entities_lists = [allocated_entities for allocated_entities in allocated_entities_map.values() if len(allocated_entities) > 1]

    # removes the last target token since this
    # list is going to be used to retrieve the
    # the model that owns the last attribute
    target_tokens = target_tokens and target_tokens[:-1] or []

    # for each allocated entities list
    for allocated_entities in allocated_entities_lists:
        # for each allocated model
        for allocated_model in allocated_entities:
            # marks the validation as failed
            validation_failed = True

            # initializes the model and the
            # attribute model
            model = None
            attribute_model = allocated_model

            # iterates over all the attribute name tokens
            for target_token in target_tokens:
                # updates the model and attribute model
                model = attribute_model
                attribute_model = attribute_model.get_value(target_token)

            # adds an error to the duplicated attribute
            attribute_model.add_error(target_attribute_name, "value is the same")

            # adds an error to the model that has the duplicated attribute
            model and model.add_error(model_attribute_name, "value has duplicate")

    # in case the validation failed adds an error to the attribute
    validation_failed and self.add_error(attribute_name, "value has duplicates")

def password_strength_validate(self, attribute_name, attribute_value, properties):
    """
    Validates the specified password has a strength
    greater than or equal to the specified value.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # calculates the password strength
    password_strength = colony.libs.crypt_util.password_strength(attribute_value)

    # in case the password strength is less than the target value
    if password_strength < target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "password is not safe")

def _set_attribute(self, attribute_key, attribute_value, nullify = True):
    """
    Sets the given model attribute for the given attribute key and value.
    This method is used in order to create a safe way of setting attributes
    avoiding empty values and providing safe casting "ways".

    The target model for the attribute setting is the current instance
    in which the method is being run.

    @type attribute_key: String
    @param attribute_key: The attribute key in the model.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to set.
    @type nullify: bool
    @param nullify: If the data to be processed should be nullified
    in case empty string values are found.
    """

    # retrieves the model class from the current
    # mode (it's the class)
    model_class = self.__class__

    # in case the model class does not contain the attribute
    # to be set, the setting must be avoided
    if not hasattr(model_class, attribute_key):
        # returns immediately (avoids, possible corruption
        # of the model)
        return

    # retrieves the model class attribute value
    model_class_attribute_value = getattr(model_class, attribute_key)

    # retrieves the data type from the model class attribute value
    # and uses it to retrieve the cast type
    data_type = model_class_attribute_value[DATA_TYPE_VALUE]
    cast_type = DATA_TYPE_CAST_TYPES_MAP.get(data_type, None)

    # in case no cast type is defined
    # it's impossible to convert the data
    if not cast_type:
        # returns immediately (no set is made)
        return

    # in case the nullify option is set and the attribute value
    # is an empty string sets the attribute value to none (null)
    if nullify and attribute_value == "": attribute_value = None

    # casts the attribute value using the safe mode
    attribute_value_casted = self._cast_safe(attribute_value, cast_type)

    # sets the attribute value casted in the model
    setattr(self, attribute_key, attribute_value_casted)

def _cast_safe(self, value, cast_type = str, default_value = None):
    """
    Casts the given value to the given type.
    The cast is made in safe mode, if an exception
    occurs the default value is returned.

    @type value: Object
    @param value: The value to be casted.
    @type cast_type: Type
    @param cast_type: The type to be used to cast the retrieved
    value (this should be a valid type, with constructor).
    @type default_value: Object
    @param default_value: The default value to be used
    when something wrong (exception raised) occurs.
    @rtype: Object
    @return: The value casted to the defined type.
    """

    # in case the value is none
    # it's a special case (type)
    if value == None:
        # returns the value immediately
        return value

    try:
        # retrieves the value type
        value_type = type(value)

        # in case the value type is the same
        # as the cast type
        if value_type == cast_type:
            # sets the value as the value casted
            value_casted = value
        # otherwise
        else:
            # casts the value using the type
            value_casted = cast_type(value)

        # returns the value casted
        return value_casted
    except:
        # returns the default value
        return default_value

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

class ModelProxy(list):
    """
    Proxy model class uses to handle operation
    on multiple models at the same pipe.

    Using this class it's possible to create and
    update models in bulk fashion without any change
    in the business logic.
    """

    class_reference = None
    """ The reference to the model classes to be used
    int he current model """

    count = 0
    """ The number of models to be created and represented
    by the current proxy object """

    models = None
    """ The list of the various models created and that
    are meant to be represented by the current proxy """

    def __init__(self, class_reference, count):
        """
        Constructor of the class.

        @type class_referece: Model
        @param class_reference: The model class reference
        to be used in the creation of the underlying model
        objects.
        @type count: int
        @param count: The number of models to be created
        and represented by the proxy object.
        """

        self.class_reference = class_reference
        self.count = count
        self._build()

    def __getattr__(self, name):
        first = self.first()

        if hasattr(first, name):
            value = getattr(first, name)
            value_type = type(value)

            if not value_type in METHOD_TYPES: return value

        def proxy_method(*args, **kwargs):
            for model in self.models:
                method = getattr(model, name)
                method(*args, **kwargs)

        return proxy_method

    def __iter__(self):
        return self.models.__iter__()

    def first(self):
        """
        Retrieves the first model in the models
        sequence, and returns it in case a valid
        is found or invalid otherwise.

        @rtype: Model
        @return: The first valid model in enclosed in the
        current proxy object.
        """

        if not self.models: return None
        return self.models[0]

    def apply(self, map):
        """
        Pipes the apply method of the model into
        each of the models contained in the proxy.

        @type map: List
        @param map: The list of map objects to be used
        in the apply method for each of the models.
        """

        for model, _map in zip(self.models, map):
            model.apply(_map)

    @utils.transaction_method("_entity_manager")
    def store(self, *args, **kwargs):
        """
        Proxy method used to create a transaction context
        that evolves a sequence of store operations around
        the various models.
        """

        for model in self.models:
            model.store(*args, **kwargs)

    def _build(self):
        """
        Method that builds the various model objects
        to be used in the proxy.

        The construction of the models is done using
        the class reference set in the instance.
        """

        # creates the list that will hold the various
        # model objects to be created, then iterates
        # over the map (list) object to create one
        # item for each of the elements
        self.models = []
        for _index in range(self.count):
            model = self.class_reference()
            self.models.append(model)
