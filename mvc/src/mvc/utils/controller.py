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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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
import sys
import time
import types
import datetime
import calendar
import platform
import traceback

import colony

import exceptions

DEFAULT_CONTENT_TYPE = "text/html;charset=utf-8"
""" The default content type """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

DEFAULT_LOCALE = "en_us"
""" The default locale """

DEFAULT_STATUS_CODE = 200
""" The default status code """

DEFAULT_ALIAS_LOCALES = {}
""" The default alias locales """

DEFAULT_TEMPLATE_FILE_ENCODING = "utf-8"
""" The default template file encoding """

DEFAULT_WILDCARD_ACL_VALUE = "*"
""" The default wildcard value for acl """

DEFAULT_MAXIMUM_ACL_VALUE = 10000
""" The default maximum value for acl """

BASE_PATH_DELTA_VALUE = 2
""" The delta value to be applied to retrieve the base path """

MIN_TIMESTAMP = 0 if os.name == "nt" else -2147483648
""" The minimum timestamp value used by the range
system to return pseudo open ranges """

MAX_TIMESTAMP = 10000000000 if os.name == "nt" else 2147483647
""" The maximum timestamp value used by the range
system to return pseudo open ranges """

HTTP_PREFIX_VALUE = "http://"
""" The http prefix value """

HTTPS_PREFIX_VALUE = "https://"
""" The https prefix value """

DATE_FORMAT = "%Y/%m/%d"
""" The date format """

DATE_TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
""" The date time format """

MVC_PATH_VALUE = "mvc_path"
""" The mvc path value """

BASE_PATH_VALUE = "base_path"
""" The base path value """

BACK_PATH_VALUE = "../"
""" The back path value """

EXTRAS_VALUE = "extras"
""" The extras value """

TEMPLATES_VALUE = "templates"
""" The templates value """

LOCALES_VALUE = "locales"
""" The locales value """

ENVIRONMENT_VALUE = "environment"
""" The environment value """

EXCEPTION_VALUE = "exception"
""" The exception value """

EXCEPTION_NAME_VALUE = "exception_name"
""" The exception name value """

PATTERN_NAMES_VALUE = "pattern_names"
""" The pattern names value """

PAGE_INCLUDE_VALUE = "page_include"
""" The page include value """

METHOD_VALUE = "method"
""" The method value """

STATUS_VALUE = "status"
""" The status value """

COLONY_VERSION_VALUE = "colony_version"
""" The colony version value """

PYTHON_VERSION_VALUE = "python_version"
""" The python version value """

PYTHON_EXECUTABLE_PATH_VALUE = "python_executable_path"
""" The python executable path value """

SERVER_TIME_VALUE = "server_time"
""" The server time value """

MESSAGE_VALUE = "message"
""" The message value """

TRACEBACK_VALUE = "traceback"
""" The traceback value """

PERMISSION_VALUE = "permission"
""" The permission value """

VALUE_VALUE = "value"
""" The value value """

SESSION_ATTRIBUTE_VALUE = "session_attribute"
""" The session attribute value """

EXTRA_EXTRAS_PATH_VALUE = "extra_extras_path"
""" The extra extras path value """

EXTRA_TEMPLATES_PATH_VALUE = "extra_templates_path"
""" The extra templates path value """

VALIDATION_MAP_VALUE = "validation_map"
""" The validation map value """

VALIDATION_ERRORS_MAP_VALUE = "validation_errors_map"
""" The validation errors map value """

DATA_TYPE_VALUE = "data_type"
""" The data type value """

NAME_TYPE_VALUE = "name"
""" The name type value """

SEQUENCE_TYPE_VALUE = "sequence"
""" The sequence type value """

MAP_TYPE_VALUE = "map"
""" The map type value """

OBJECT_ID_VALUE = "object_id"
""" the object id value """

LOCALE_VALUE = "locale"
""" The locale value """

RELATIVE_VALUE_VALUE = "relative_value"
""" The relative value value """

FORM_DATA_VALUE = "form-data"
""" The form data value """

CONTENTS_VALUE = "contents"
""" The contents value """

FILENAME_VALUE = "filename"
""" The filename value """

HOST_VALUE = "Host"
""" The host value """

REFERER_VALUE = "Referer"
""" The referer value """

ACCEPT_LANGUAGE_VALUE = "Accept-Language"
""" The accept language header value """

PARAMETERS_VALUE = "_parameters"
""" The parameters value """

JSON_DATA_PRIVATE_VALUE = "_json_data"
""" The json data value to be used to store json data cache """

FORM_DATA_PRIVATE_VALUE = "_form_data"
""" The form data value to be used to store form data cache """

DASHED_WORD_PAIR_REPLACEMENT_VALUE = "\\1-\\2"
""" The replacement value for two capture groups to be separated by dash """

UNDERSCORED_WORD_PAIR_REPLACEMENT_VALUE = "\\1_\\2"
""" The replacement value for two capture groups to be separated by underscore """

LOCALE_SESSION_ATTRIBUTE = "_locale"
""" The locale session attribute name """

DASH_VALUE = "-"
""" The dash value """

UNDERSCORE_VALUE = "_"
""" The underscore value """

SHORT_TIMEOUT = 1800
""" The short (value) timeout (in seconds) """

SHORT_MAXIMUM_TIMEOUT = SHORT_TIMEOUT * 3
""" The short (value) maximum timeout (three times
the timeout value) """

TO_ONE_RELATION_VALUE = 1
""" The to one relation value """

TO_MANY_RELATION_VALUE = 2
""" The to many relation value """

PERSIST_UPDATE = 0x01
""" The persist only on update (or save) persist type that only
allows the updating of fields in an (already) associated entity """

PERSIST_SAVE = 0x02
""" The persist only on save persist type, that allows the
indirect creation of entities from one entity association """

PERSIST_ASSOCIATE = 0x04
""" The persist associate persist type that only allows
the association (setting) of a relation in another no creation
or update operation will be allowed for this permission """

PERSIST_NONE = 0x00
""" The persist none persist type meaning that
no kind of transaction will be allowed for relation """

PERSIST_ALL = PERSIST_UPDATE | PERSIST_SAVE | PERSIST_ASSOCIATE
""" The persist all persist type resulting from the association
of the complete set of persist type values """

ATTRIBUTE_PARSING_REGEX_VALUE = "(?P<name>[\w]+)|(?P<sequence>\[\])|(?P<map>\[\w+\])"
""" The attribute parsing regular expression value """

CAPITALIZED_CAMEL_CASED_WORD_PAIR_REGEX_VALUE = "([A-Z]+)([A-Z][a-z])"
""" The capitalized camel cased word pair regex value """

CAMEL_CASED_WORD_PAIR_REGEX_VALUE = "([a-z\d])([A-Z])"
""" The camel cased word pair regex value """

NON_CHARACTER_REGEX_VALUE = "[^A-Z^a-z^0-9^\/]+"
""" The non-character regex value """

LOCALE_REGEX_VALUE = "(?P<locale>[a-zA-Z0-9-]+)(;q=(?P<relative_value>[0-9]+(\.[0-9]+)?))?"
""" The locale regex value """

ATTRIBUTE_PARSING_REGEX = re.compile(ATTRIBUTE_PARSING_REGEX_VALUE)
""" The attribute parsing regex """

CAPITALIZED_CAMEL_CASED_WORD_PAIR_REGEX = re.compile(CAPITALIZED_CAMEL_CASED_WORD_PAIR_REGEX_VALUE)
""" The capitalized camel cased word pair regex """

CAMEL_CASED_WORD_PAIR_REGEX = re.compile(CAMEL_CASED_WORD_PAIR_REGEX_VALUE)
""" The camel cased word pair regex """

NON_CHARACTER_REGEX = re.compile(NON_CHARACTER_REGEX_VALUE)
""" The non-character regex """

LOCALE_REGEX = re.compile(LOCALE_REGEX_VALUE)
""" The locale regex """

DEFAULT_VALUE_ATTRIBUTE = 10
""" The default value attribute to be used in template """

DEFAULT_SESSION_ATTRIBUTE = "user_acl"
""" The default session attribute to be used in template """

DATA_TYPE_CAST_TYPES_MAP = {
    "text" : unicode,
    "string" : unicode,
    "integer" : int,
    "float" : float,
    "date" : colony.timestamp_datetime,
    "relation" : None
}
""" The map associating the data types with the cast types """

DEFAULT_RELATION_VALUES_MAP = {
    TO_ONE_RELATION_VALUE : {},
    TO_MANY_RELATION_VALUE : []
}
""" The default relation values map """

CONTENT_TYPE_MAP = {
    "application/x-www-form-urlencoded" : "form",
    "multipart/form-data" : "form",
    "application/json" : "json",
}
""" The map associating the various content type
values with the simplifies type names """

FORM_DATA_MAP_KEY_FORMAT = "%s[%s]"
""" The form data map key format """

FORM_DATA_LIST_KEY_FORMAT = "%s[%s][]"
""" The form data list key format """

ATTRIBUTE_EXCLUSION_LIST = (
    "data_state",
    "data_reference",
    "mapping_options",
    "id_attribute_name",
    "model_started",
    "validation_context",
    "validation_errors_map",
    "validation_map"
)
""" The attribute exclusion list (for model reference),
these are the values that are going to be ignored in every
single model instance/class """

bundle_cache = colony.DataCacheMap()
""" A globally accessible cache map, used to retrieve
the various bundles from an in memory system, the least
used values are not guaranteed to persist in memory """

def _create_controller(self):
    """
    Creates (constructs) the controller structures.
    This is method is considered to be the controller's
    constructor.
    """

    # starts the map that contains the sets of
    # parameters to be used as default in the
    # handling of a request
    self.default_parameters = {}

def _start_controller(self):
    """
    Starts the controller structures.
    This is method is considered to be the controller's
    initializer and calls the start method in the
    controller (for user code).
    """

    # in case the controller has the start method
    if hasattr(self, "start"):
        # calls the start method
        # in the controller
        self.start()

def _stop_controller(self):
    """
    Stops the controller structures.
    This is method is considered to be the controller's
    destroyer and calls the stop method in the
    controller (for user code).
    """

    # in case the controller has the stop method
    if hasattr(self, "stop"):
        # calls the stop method
        # in the controller
        self.stop()

def get_exception_map(self, exception, request = None):
    """
    Retrieves the exception map (describing the exception)
    for the given exception.
    The exception map does contain deep (and sensitive) information
    about the current environment as so it must be used carefully.

    @type exception: Exception
    @param exception: The exception to retrieve the
    exception map.
    @type request: Request
    @param request: The (optional) request object
    to be used to retrieve additional information for the
    exception (this should be related with the current runtime).
    @rtype: Dictionary
    @return: The exception map describing the exception.
    """

    # retrieves the execution information
    _type, _value, traceback_list = sys.exc_info()

    # starts the formatted traceback (with the default value)
    formatted_traceback = None

    # in case the traceback list is valid, was retrieved as expected
    # and contains at least one value it must be re-encoded using the
    # currently defined system encoding (in order to avoid problems)
    if traceback_list:
        # retrieves the encoding currently associated with the system,
        # then formats the traceback list and iterates over each of the
        # lines to re-encode it using the system encoding
        file_system_encoding = sys.getfilesystemencoding()
        formatted_traceback = traceback.format_tb(traceback_list)
        formatted_traceback = [value.decode(file_system_encoding) for value in formatted_traceback]

    # retrieves the exception class and the name of it and then retrieves
    # the message currently set in the exception as the exception message
    exception_class = exception.__class__
    exception_class_name = exception_class.__name__
    exception_message = exception.message if hasattr(exception, "message") else None
    exception_message = exception_message or unicode(exception)

    # creates the exception map, with information on
    # the exception and on the (global) environment
    exception_map = {
        ENVIRONMENT_VALUE : {
            METHOD_VALUE : request and request.get_request().get_method(),
            STATUS_VALUE : request and request.get_request().status_code,
            COLONY_VERSION_VALUE : request and request.get_plugin_manager().get_version(),
            PYTHON_VERSION_VALUE : platform.python_version(),
            PYTHON_EXECUTABLE_PATH_VALUE : sys.executable,
            SERVER_TIME_VALUE : datetime.datetime.now().strftime("%a, %d %b %Y %H:%M%S %z")
        },
        EXCEPTION_VALUE : {
            EXCEPTION_NAME_VALUE : exception_class_name,
            MESSAGE_VALUE : exception_message,
            TRACEBACK_VALUE : formatted_traceback
        }
    }

    # converts the exception class name to underscore notation and uses it
    # to create the name of the method that will process the exception
    exception_class_name_underscore = colony.to_underscore(exception_class_name)
    exception_class_process_method_name = "process_map_" + exception_class_name_underscore

    # in case the instance contains the process handler
    # for the exception class must call it to process
    # and alter the current exception map
    if hasattr(self, exception_class_process_method_name):
        # retrieves the exception class process method and calls
        # it in order to change the current exception map
        exception_class_process_method = getattr(self, exception_class_process_method_name)
        exception_class_process_method(exception_map, exception)

    # returns the final exception map that should follow to the serializer
    # in the next step (must be used like that)
    return exception_map

def process_map_model_validation_error(self, exception_map, exception):
    """
    Processes the exception map for the given exception.
    This process method includes the specific information
    of this exception into the exception map.

    @type exception_map: Dictionary
    @param exception_map: The map containing the exception
    information.
    @type exception: Exception
    @param exception: The exception to be processed.
    """

    # retrieves the model in the exception and then uses it to retrieve
    # both the validation map and the validation errors map, these values
    # are going to be used to returns dome debugging information
    exception_model = exception.model
    validation_map = exception_model.validation_map
    validation_errors_map = exception_model.validation_errors_map

    # sets both the validation and the validation errors map in the map
    # so that the exception may contain some debugging information
    exception_map[VALIDATION_MAP_VALUE] = validation_map
    exception_map[VALIDATION_ERRORS_MAP_VALUE] = validation_errors_map

def get_entity_id_attribute(self, entity, id_attribute_name = OBJECT_ID_VALUE):
    """
    Retrieves the id attribute (value) from the given entity that may
    be both an entity object or an entity map represented by a dictionary.
    In case the given entity is a map the id attribute name value is used
    to retrieve the appropriate id attribute value.
    This method must be used carefully to avoid possible miss conversion
    of id attribute based on an erroneous id attribute name.

    @type entity: Entity
    @param entity: The entity to retrieve the id attribute, this value
    may assume a possible map value.
    @type id_attribute_name: String
    @param id_attribute_name: The name of the id attribute, this value
    is only used in case the provided entity is a map.
    @rtype: Object
    @return: The value of the entity id attribute for the given entity.
    """

    # retrieves the entity type,
    entity_type = type(entity)

    # in case the entity type is a dictionary, must
    # retrieve the id attribute using as reference the
    # given id attribute name
    if entity_type == types.DictType:
        # retrieves the id attribute value from the entity (map)
        # using the provided id attribute name
        id_attribute_value = entity.get(id_attribute_name, None)
    # in case the entity type is not a dictionary it must
    # be a normal entity object, normal strategy applies
    else:
        # retrieves the id attribute value "directly"
        # from the entity
        id_attribute_value = entity.get_id_attribute_value()

    # returns the retrieved id attribute value
    return id_attribute_value

def get_entity_model(
    self,
    entity_manager,
    entity_model,
    update_values_map = {},
    create_values_map = {},
    secure_value_keys_list = None,
    create = True,
    nullify = True
):
    """
    Retrieves an entity model instance from the given entity manager
    for the provided entity model (class).
    The retrieved entity instance is either a new instance (in case
    no entity is defined for the given id) or an existing instance
    in case it exists in the entity manager.
    The update and create values map(s) provide a way to automatically
    set and update the values of the entity.

    @type entity_manager: EntityManager
    @param entity_manager: The entity manager to be used.
    @type entity_model: Class
    @param entity_model: The entity model (class) to be retrieved.
    @type update_values_map: Dictionary
    @param update_values_map: The map of values to be set automatically (on update and created).
    @type create_values_map: Dictionary
    @param create_values_map: The map of values to be set on creation.
    @type secure_value_keys_list: List
    @param secure_value_keys_list: The list of value keys that may be used
    while setting the values automatically (update), use this list to control the
    access to the values.
    @type create: bool
    @param create: If a new entity should be created in case none is
    retrieved from the entity manager.
    @type nullify: bool
    @param nullify: If the data to be processed should be nullified
    in case empty string values are found.
    @rtype: EntityModel
    @return: The retrieved entity model.
    """

    # unsets the created entity flag
    created_entity = False

    # retrieves the type of object from the update
    # and create values map
    update_values_map_type = type(update_values_map)
    create_values_map_type = type(create_values_map)

    # in case the create and update maps are not really maps, assumes
    # they are entity objects and converts them into a map
    if not update_values_map_type == types.DictType: update_values_map = self._convert_entity_map(update_values_map)
    if not create_values_map_type == types.DictType: create_values_map = self._convert_entity_map(create_values_map)

    # retrieves the id attribute name (key)
    id_key = entity_model.get_id()

    # tries to retrieves the entity model id
    entity_model_id = update_values_map.get(id_key, None)

    # in case the entity model id is defined
    # the model exists (or is going to be created, with
    # manual id attribution) in the data source and
    # must be retrieved from it
    if entity_model_id:
        # retrieves the entity model id value
        entity_model_id_value = getattr(entity_model, id_key)

        # retrieves the entity model id data type, then retrieves
        # the associated cast type and used it to cast the entity
        # model id (this is the safest way possible)
        entity_model_id_data_type = entity_model_id_value[DATA_TYPE_VALUE]
        cast_type = DATA_TYPE_CAST_TYPES_MAP[entity_model_id_data_type]
        entity_model_id_casted = self._cast_safe(entity_model_id, cast_type, -1)

        # retrieves the entity using the entity model id (casted)
        entity = entity_manager.get(entity_model, entity_model_id_casted)

        # in case the entity is not defined
        # in the entity manager
        if not entity:
            # in case the create flag is set (an entity
            # may be created)
            if create:
                # sets the created entity flag
                created_entity = True

                # creates a new entity from the entity
                # model (creates instance)
                entity = entity_model()

                # sets the id in the entity
                setattr(entity, id_key, entity_model_id)
            # otherwise no entity was found in the
            # entity manager for the current id value
            # and is not possible to create an entity
            else:
                # returns invalid entity (no entity
                # was found in the entity manager)
                return None
    # otherwise a new entity should be created
    # in case the create flag is set
    elif create:
        # sets the created entity flag
        created_entity = True

        # creates a new entity from the entity
        # model
        entity = entity_model()
    # otherwise it was not possible to retrieve
    # or create an entity (no entity returned)
    else:
        # returns invalid entity (no id
        # attribute is set, not possible to retrieve
        # an entity from the entity manager)
        return None

    # iterates over all the update values items
    for update_value_key, update_value_value in update_values_map.items():
        # in case the secure value keys list is valid and the update
        # value key does not exist in the secure value keys list
        if secure_value_keys_list and not update_value_key in secure_value_keys_list:
            # continues the loop (not safe to
            # update the current value)
            continue

        # checks if the update value value is "callable" (and calls it) or
        # uses the "raw" value in case it's not
        update_value_value = callable(update_value_value) and update_value_value() or update_value_value

        # sets the update value in the entity
        self._set_entity_attribute(update_value_key, update_value_value, entity, entity_model, nullify)

    # in case the entity was created, create values must be set
    # (they take priority over the update values)
    if created_entity:
        # iterates over all the create values items
        for create_value_key, create_value_value in create_values_map.items():
            # checks if the create value value is "callable" (and calls it) or
            # uses the "raw" value in case it's not
            create_value_value = callable(create_value_value) and create_value_value() or create_value_value

            # sets the create value in the entity
            self._set_entity_attribute(create_value_key, create_value_value, entity, entity_model, nullify)

    # returns the entity
    return entity

def set_entity_relation(self, entity, relation_name, relation_value):
    """
    Sets the given relation value in the given entity.
    This method provides a safety mechanism for setting relations.

    @type entity: Object
    @param entity: The entity to set the relation.
    @type relation_name: String
    @param relation_name: The name of the relation to be set.
    @type relation_value: Object
    @param relation_value: The value of the relation to be set.
    """

    # retrieves the relation value type
    relation_value_type = type(relation_value)

    # in case the type if the relation value is list must
    # iterate and validate and the values in it
    if relation_value_type == types.ListType:
        # iterates over all the values
        # of the list (relation value)
        for value in relation_value:
            # in case the validation of the relation value
            # fails, must return immediately
            if not self._validate_relation_value(value): return

    # otherwise it must be a "simple" value and no it
    # iteration is required simple value
    else:
        # in case the validation of the relation value
        # fails must return immediately (no value setting)
        if not self._validate_relation_value(relation_value): return

    # sets the relation value in entity
    setattr(entity, relation_name, relation_value)

def save_entity_relations(
    self,
    request,
    entity_map,
    entity,
    relations_map,
    persist_type = PERSIST_ALL
):
    """
    Saves the entity relations in the in the entity with the given map and values.
    The relations map describes the various entity relation with a tuple
    containing the type of relation and the method to be sun to save it.
    The persist type mask is going to be used to filter some of the attributes
    sent to the underlying layer of relations saving.

    @type request: Request
    @param request: The request to be used.
    @type entity_map: Dictionary
    @param entity_map: The entity values map.
    @type entity: Object
    @param entity: The entity object to be used.
    @type relations_map: Dictionary
    @param relations_map: The map containing the description of
    the relation to be set.
    @type persist_type: int
    @param persist_type: Mask controlling the permissions of persistence
    for the saving of the entity relations.
    """

    # retrieves the type of object from the entity map
    entity_map_type = type(entity_map)

    # in case the entity map is not really a map, assumes
    # it is an entity object and converts it into a map
    if not entity_map_type == types.DictType: entity_map = self._convert_entity_map(entity_map)

    # iterates over all the relations
    for relation_name, relation_item in relations_map.items():
        # skips the relation in case it's
        # not defined in the relation map
        if not relation_name in entity_map: continue

        # retrieves the relation item length
        relation_item_length = len(relation_item)

        # in case the relation item length is three
        # (it does contain the relation persist flag)
        if relation_item_length == 2:
            # unpacks the relation item, retrieving the relation
            # type and relation method
            relation_type, relation_method = relation_item

            # sets the relation persist type to persist
            # all (default value)
            relation_persist_type = PERSIST_ALL
        # in case the relation item length is three
        # (it contains the relation persist flag)
        elif relation_item_length == 3:
            # unpacks the relation item, retrieving the relation
            # type relation method and relation persist type
            relation_type, relation_method, relation_persist_type = relation_item
        # otherwise the relation item length is invalid
        else:
            # raises a runtime error
            raise RuntimeError("invalid relation item length")

        # retrieves the default relation value according
        # to the relation type
        default_relation_value = DEFAULT_RELATION_VALUES_MAP[relation_type]

        # retrieves the relation value
        relation_value = entity_map.get(relation_name, default_relation_value)
        relation_values = relation_type == 1 and [relation_value] or relation_value

        # initializes the relation entities list
        relation_entities = []

        # initializes the relation validation
        # flag which will be used to mark if
        # the validation failed in one of the
        # relation entities
        relation_validation_failed = False

        # sets the associate relation value
        associate_relation = True

        # iterates over all the relation values to
        # save (or update) the entities
        for relation_value in relation_values:
            # in case the relation value is set and it's valid
            # (not empty) it's ready for validation of relations
            if relation_value:
                # validate the given entity for relation with the relation
                # value in the attribute of name relation name
                valid_relation = self.validate_entity_relation(entity, relation_value, relation_name)
            # otherwise the validation is not required
            # the value is not valid, not set
            else:
                # sets the relation as (automatically) valid
                valid_relation = True

            # in case the relation is valid (no need to remove update)
            if valid_relation:
                # "calculates" the new relation persist type based on the base relation persist type
                # plus the filtering based on the top level persist type (only update or save in case the top
                # level contains it, propagation)
                _relation_persist_type = relation_persist_type & (persist_type | PERSIST_ASSOCIATE)
            # otherwise the relation is not valid (update is not safe)
            else:
                # "calculates" the new relation persist type based on the base relation persist type
                # plus the filtering based on the top level persist type (only update or save in case the top
                # level contains it, propagation) and then finally removes the update type from the
                # persist type (it's not safe)
                _relation_persist_type = relation_persist_type & (persist_type | PERSIST_ASSOCIATE) & (PERSIST_ALL ^ PERSIST_UPDATE)

            try:
                # calls the relation method for the entity (saving or updating it)
                relation_entity = relation_value and relation_method(request, relation_value, persist_type = _relation_persist_type) or None
            except exceptions.ModelValidationError, exception:
                # updates the relation entity with the model
                # in the model validation error
                relation_entity = exception.model

                # sets the relation validation
                # failed flag to true
                relation_validation_failed = True

            # checks if the relation is saved (only if it's a valid instance)
            is_saved = relation_entity and relation_entity.is_saved() or False

            # checks if the relation should be associated
            # the association is only granted if either the
            # relation was saved or the relation is valid
            # or the associate type is set to allow association
            associate_relation = is_saved or valid_relation or relation_persist_type & PERSIST_ASSOCIATE

            # adds the relation entity to the list
            # in case the entity was created and the
            # relation in meant to be associated
            relation_entity and associate_relation and relation_entities.append(relation_entity)

        # adds an error to the relation name in case
        # the validation in one of its entities failed
        relation_validation_failed and entity.add_error(relation_name, "relation validation failed")

        # in case it is a to one relation
        if relation_type == 1:
            # sets the relation entity in the entity, only
            # in case the associate relation flag is set
            associate_relation and setattr(entity, relation_name, relation_entity)
        # in case it is a to many relation
        else:
            # sets the relation entities in the entity
            # in all cases (it's a list)
            setattr(entity, relation_name, relation_entities)

def validate_entity_relation(self, entity, relation_entity_map, relation_name):
    """
    Validates the entity relation, checking if the given entity
    and the entity represented by the relation entity map are really
    related in the data source.
    In case the relation entity map represents an entity that is not
    yet persisted the relation is considered valid.

    @type entity: Entity
    @param entity: The base entity to be used in the validation.
    @type relation_entity_map: Dictionary
    @param relation_entity_map: The map containing the entity
    definition to be validated as relation.
    @type relation_name: String
    @param relation_name: The name of the attribute for "joining"
    the relation.
    @rtype: bool
    @return: The result of the validation for relation.
    """

    # retrieves the entity manager from the entity
    entity_manager = entity._entity_manager

    # retrieves the relation entity class
    relation_entity_class = entity.get_relation_entity_class(relation_name)

    # retrieves the relation attribute type (resolving relations) and
    # the converts it into the real (python) data type
    relation_attribute_type = entity.get_attribute_data_type(relation_name, True)
    relation_attribute_real_type = DATA_TYPE_CAST_TYPES_MAP[relation_attribute_type]

    # retrieves the id attribute name for the relation entity class
    id_attribute_name = relation_entity_class.get_id()

    # retrieves the value for the id attribute (of the relation) and then
    # casts the id attribute value for the "real" relation attribute data type
    id_attribute_value = relation_entity_map.get(id_attribute_name, None)
    id_attribute_value = self._cast_safe(id_attribute_value, relation_attribute_real_type)

    # in case the id attribute is set (and valid) entity is not persisted
    # and so it need to be validated for relation coherence, this method
    # checks if the relation is really associated with the given entity using
    # id attribute value for the checking
    valid_relation = id_attribute_value == None or entity_manager.validate_relation(entity, id_attribute_value, relation_name)

    # returns if the relation is valid
    return valid_relation

def get_field_models(self, request, field_name = None, model = None, data_type = int):
    """
    Retrieves the complete set of models for the various identifiers
    defined in the field with the provided name.

    In case at least one model fails to be retrieved, an error is raised.

    @type request: Request
    @param request: The request to be used.
    @type field_name: String
    @param field_name: The name of the field to be used for the retrieval
    of the models, should contain the identifiers separated by commas.
    @type model: Model
    @param model: The model to be used for the retrieval of the entities.
    @type data_type: Type
    @param data_type: The type to be used in the cast operation for the
    various identifier values.
    """

    # validates that both the field name and the model entity
    # definition are valid and in case they're not returns an
    # empty list of models (no loading is possible)
    if not field_name: return []
    if not model: return []

    # retrieves the series of identifiers for the requested
    # field name then splits it around the separator, casting
    # them to the proper data type
    model_id = self.get_field(request, field_name, None)
    model_ids = model_id and model_id.split(",") or []
    model_ids = [data_type(model_id) for model_id in model_ids]

    # retrieves the various entities for the requested identifiers,
    # according to the provided model, in case at least one model
    # is not retrieved, an error is raised
    entities = [model.get(model_id, context = request) for model_id in model_ids]
    if None in entities: raise RuntimeError(
        "One ore more specified %s entities were not found" % model.__name__
    )
    return entities

def url_for(self, request, reference, filename = None, *args, **kwargs):
    """
    Resolves the relative url to a request resource (either static or dynamic)
    the details of the resolution process should be described in the lower layer
    of the mvc system.

    The provided values should include the reference to that is meant to be
    retrieved (static or the resource path) and the various dynamic arguments
    for the resource retrieval (either arguments or get parameters).

    @type request: Request
    @param request: The request that is going to be used for the complete set
    of context aware operations for url resolution.
    @type reference: String
    @param reference: A string describing the resource that is meant to be resolved
    should be static for static resources or a dynamic string describing the
    resource name for dynamic resources.
    @type filename: String
    @param filename: Optional name to be used in the resolution of static resources
    this value should be called using a non named strategy.
    @rtype: String
    @return: The relative url path value to the resource taking into account the
    base path or the mvc path defined for the current request.
    """

    # retrieves the base path for the current request
    # so that the complete path may be constructor, keep
    # in mind that the generated location is always a
    # relative one a never an absolute url
    base_path = self.get_base_path(request)
    mvc_path = self.get_mvc_path(request)
    location = ""

    if reference == "static":
        location = "resources/" + filename

    elif reference == "resources":
        location = "resources/" + filename

    elif reference == "common":
        location = "common/" + filename

    else:
        location = request.resolve(request, reference, *args, **kwargs)
        if location: return mvc_path + location
        else: return ""

    return base_path + location

def get_field(
    self,
    request,
    field_name,
    default = None,
    cast_type = None,
    split = False,
    token = ","
):
    """
    Retrieves a field value from the processed form data
    of the request.
    Optionally an used can provide the default value to be
    used when there is a miss match.

    It's possible to automatically cast the field to the
    requested cast type in case the argument is provided.

    In case the split flag is set the values are separated
    using the provided token as the separator character.

    @type request: Request
    @param request: The request to be used.
    @type field_name: String
    @param field_name: The name of the field to be retrieved
    from the form data.
    @type default: Object
    @param default: The value to be returned when there is a
    field miss match (fallback value).
    @type cast_type: Type
    @param cast_type: The type to be used in the optional casting
    of the field value.
    @type split: bool
    @param split: Flag indicating if the field value should be
    divided into multiple values using the token as separator.
    @type token: String
    @param token: The token to be used in the split operation in
    case the split flag is set.
    @rtype: Object
    @return: The value for the field being request from
    the form data.
    """

    # retrieves the content type from the request and
    # then uses it to normalize the type for parsing
    content_type = request.get_type()
    type = CONTENT_TYPE_MAP.get(content_type, "form")

    # creates the method name using the "just" retrieved type
    # and then retrieves the associated method
    method_name = "process_%s_data" % type
    method = getattr(self, method_name)

    # processes (and retrieves) the data map from the
    # request and then uses it to retrieve the field
    # from it (the retrieval of the form data may be cached)
    form_data_map = method(request)
    field_value = form_data_map.get(field_name, default)

    # in case the current field value is invalid, should return
    # the value immediately to avoid any casting problems, note
    # that the returned value is an empty list
    if field_value == None and split: return []

    # in case the split flag is set the field value is divided
    # into multiple values "around" the token value
    if split: field_value = field_value.split(token)

    # in case the cast type is set runs the casting in a safe
    # manner to avoid raising exceptions, this is the execution
    # for the split values (sequences)
    if cast_type and split: field_value = [self._cast_safe(value, cast_type, default) for value in field_value]

    # in case the cast type is set runs the casting in a safe
    # manner to avoid raising exceptions, this is the execution
    # for the not split values (not sequences)
    if cast_type and not split: field_value = self._cast_safe(field_value, cast_type, default)

    # returns the retrieved field value
    return field_value

def get_json(self, request):
    """
    Retrieves the loaded json information from the request this
    method assumes that the request is properly formed and that
    the header information is set in accordance with json.

    @type request: Request
    @param request: The request to be used.
    @rtype: Object
    @return: The object that represents the parsed json information
    that was passed inside the request data.
    """

    # processes (and retrieves) the data map from the
    # request and then tries to retrieves the json
    # data from it in case it does not exists the complete
    # maps is returned as the json value
    form_data_map = self.process_json_data(request)
    json_v = form_data_map.get("root", form_data_map)
    return json_v

def get_pattern(self, parameters, pattern_name, pattern_type = None):
    """
    Retrieves a pattern value from the parameters map,
    casting it to the appropriate type in case a type
    is provided.

    @type parameters: Dictionary
    @param parameters: The map of parameters provided to the
    controller's action method.
    @type pattern_name: String
    @param pattern_name: The name of the pattern to be retrieved.
    @type pattern_type: type
    @param pattern_type: The type to be used to cast the pattern
    value (the cast is done in safe mode).
    @rtype: Object
    @return: The retrieved and "casted" pattern value.
    """

    # retrieves the pattern names from the parameters
    # and retrieves the patter from it
    pattern_names = parameters[PATTERN_NAMES_VALUE]
    pattern_value = pattern_names.get(pattern_name, None)

    # casts the pattern value using the safe mode, avoids
    # problems when a cast fails (no exception raised)
    pattern_value = pattern_value and self._cast_safe(pattern_value, pattern_type) or pattern_value

    # returns the pattern value
    return pattern_value

def set_pattern(self, parameters, pattern_name, pattern_value):
    """
    Sets the provided pattern value for the pattern name that
    was set, useful for request simulation.

    This method must be used with care in order to avoid unwanted
    behavior in the request handling.

    @type parameters: Dictionary
    @param parameters: The parameters that are going to be changed
    so that the pattern is set.
    @type pattern_name: String
    @param pattern_name: The name of the patter to be set.
    @type pattern_value: Object
    @param pattern_value: The value to be set for the parameter, this
    value may assume any data type.
    """

    # retrieves the map of patterns from the parameters map and then
    # uses it to set the pattern value for the provided name
    pattern_names = parameters[PATTERN_NAMES_VALUE]
    pattern_names[pattern_name] = pattern_value

def get_entity_map_parameters(self, entity_map, delete_parameters = True):
    """
    Retrieves the entity map parameters value.
    The parameters are stored in a special part of
    the entity map, that is removed after read.
    The removal of the parameters is optional and may be
    prevented.

    @type entity_map: Dictionary
    @param entity_map: The entity map.
    @type delete_parameters: bool
    @param delete_parameters: If the parameters value should be
    removed from the entity map.
    @rtype: Dictionary
    @return: The parameters map for the entity.
    """

    # retrieves the entity parameters
    entity_parameters = entity_map.get(PARAMETERS_VALUE, {})

    # removes the parameters from the entity map
    # in order to avoid possible attribute problems
    # in case the delete parameters is set
    if delete_parameters and (PARAMETERS_VALUE in entity_map): del entity_map[PARAMETERS_VALUE]

    # returns the entity parameters
    return entity_parameters

def validate_model_exception(self, model, exception_message, error_description = True):
    """
    Validates the given model, raising an exception in case
    the validation fails.
    The error descriptor controls if the description of the error
    should include detailed explanation of the validation.

    @type model: Model
    @param model:The model to be validated.
    @type exception_message: String
    @param exception_message: The message to be used when throwing
    the exception.
    @type error_description: bool
    @param error_description: If a detailed explanation of the validation
    error should be put in the exception description.
    """

    # validates the model using the exception raising
    # mode (raises exception in case error occurs)
    model.validate_exception(exception_message, error_description)

def new_connection(self, parameters, connection_name = "default", channels = ()):
    """
    Creates a new connection for the communication sub-system, the
    new connection is initially registered for the provided channels.
    The mvc communication system is used for the creation/registration
    process of the new connection.

    @type parameters: Dictionary
    @param parameters: A dictionary of parameters.
    @type connection_name: String
    @param connection_name: The name of the connection to be used
    to in new connection (default connection is used if not defined).
    @type channels: Tuple
    @param channels: The various channels to be used to register the
    connection, this value should be a partial name and not a fully
    qualified name.
    @rtype: CommunicationConnection
    @return: The created communication connection that should be ready
    to be used for any operation.
    """

    # retrieves the communication handler and in case there
    # is no communication handler defined, impossible to
    # create a new connection (returns immediately)
    communication_handler = parameters.get("communication_handler", None)
    if not communication_handler: return

    # creates a new connection using the communication handler
    # and registers it for the required channels (security measures
    # will apply, validation is required)
    connection = communication_handler.new_connection(
        connection_name, channels = channels
    )
    return connection

def delete_connection(self, parameters, connection):
    """
    Deletes the provided connection from the communication sub-system,
    the connection should no longer handle messages.
    The mvc communication system is used for the deletion/unregistration
    process of the connection.

    @type parameters: Dictionary
    @param parameters: A dictionary of parameters.
    @type communication: CommunicationConnection
    @param communication: The communication connection to be deleted
    from the communication handler internal structures.
    """

    # retrieves the communication handler and in case there
    # is no communication handler defined, impossible to
    # create a new connection (returns immediately)
    communication_handler = parameters.get("communication_handler", None)
    if not communication_handler: return

    # deletes the current connection from the communication handler
    # unregistering it from the complete set of internal structures
    communication_handler.delete_connection(connection)

def send(self, parameters, connection_name = "default", message = "", channels = ()):
    """
    Sends a message to the clients registered for the provided channels
    in the the connection with the given name.
    The mvc communication system is used for the unicast sending.

    @type parameters: Dictionary
    @param parameters: A dictionary of parameters.
    @type connection_name: String
    @param connection_name: The name of the connection to be used
    to send the message (default connection is used if not defined).
    @type message: String
    @param message: The message to be sent in channels mode (an empty
    message is used in case none is defined).
    @type channels: Tuple
    @param channels: The various channels to be used to send the message
    this value should be a partial name and not a fully qualified name.
    """

    # retrieves the communication handler and in case there
    # is no communication handler defined, impossible to
    # send the message (returns immediately)
    communication_handler = parameters.get("communication_handler", None)
    if not communication_handler: return

    # sends the message using the communication handler
    # this message is going to be displayed to the connections
    # registered in the requested channels (security measures will
    # apply, private message)
    communication_handler.send(connection_name, message, channels = channels)

def send_broadcast(self, parameters, connection_name = "default", message = ""):
    """
    Sends a broadcast message to all the clients in the connection
    with the given name.
    The mvc communication system is used for the broadcast sending.

    @type parameters: Dictionary
    @param parameters: A dictionary of parameters.
    @type connection_name: String
    @param connection_name: The name of the connection to be used
    to send the message (default connection is used if not defined).
    @type message: String
    @param message: The message to be sent in broadcast mode (an empty
    message is used in case none is defined).
    """

    # retrieves the communication handler and in case there
    # is no communication handler defined, impossible to
    # send the message (returns immediately)
    communication_handler = parameters.get("communication_handler", None)
    if not communication_handler: return

    # sends the broadcast message using the communication handler
    # this message is going to be displayed to every connection
    # (security measures will not apply, public message)
    communication_handler.send_broadcast(connection_name, message)

def create_form_data_string(self, request, data_map):
    """
    Converts the data map to a string representation
    in the form data format.

    @type request: Request
    @param request: The request to be used.
    @type data_map: Dictionary
    @param data_map: The map containing the hierarchy of
    defined structure for the "form" contents.
    @rtype: String
    @return: The string representation of the data map
    in the form data format.
    """

    # initializes the form data map items list
    form_data_map_items = []

    # creates the form data map
    form_data_map = self.create_form_data(request, data_map)

    # while the form data map is not empty
    while form_data_map:
        # initializes the remaining form data map
        remaining_form_data_map = {}

        # for each item in the form data map
        for attribute_name, attribute_value in form_data_map.items():
            # retrieves the attribute value type
            attribute_value_type = type(attribute_value)

            # in case the attribute value is a list then
            # makes the attribute value the first value
            # in the list and keeps the rest of the list
            # so that it can be processed in the next iterations
            attribute_value_list = attribute_value_type == types.ListType and attribute_value or None
            attribute_value = attribute_value_list and attribute_value_list[0] or attribute_value
            attribute_value_list = attribute_value_list and attribute_value_list[1:] or None

            # in case the attribute value list
            # exists and is not empty
            if attribute_value_list:
                # sets the attribute value list in the remaining
                # form data map so that the remaining list items
                # are flushed out in the next iterations
                remaining_form_data_map[attribute_name] = attribute_value_list

            # creates the form data map item, taking into account
            # that if the value is no value is set in the key
            if attribute_value == None: form_data_map_item = "%s=" % attribute_name
            else: form_data_map_item = "%s=%s" % (attribute_name, attribute_value)

            # adds the form data map item to the list
            form_data_map_items.append(form_data_map_item)

        # sets the remaining form data map
        # as the form data map
        form_data_map = remaining_form_data_map

    # creates the form data map string by joining
    # the previously accumulated form data items
    form_data_map_string = "&".join(form_data_map_items)

    # returns the form data map string
    return form_data_map_string

def create_form_data(self, request, data_map, encoding = DEFAULT_ENCODING):
    """
    Processes the data map, creating a single map with all the
    attributes described in the form data format.

    @type request: Request
    @param request: The request to be used.
    @type data_map: Dictionary
    @param data_map: The map containing the hierarchy of defined structure
    for the "form" contents.
    @type encoding: String
    @param encoding: The encoding to be used when retrieving
    the attribute values.
    @rtype: Dictionary
    @return: The map representing the data map in a flat format
    where the data map's depth is expressed in the keys.
    """

    # initializes the form data map
    form_data_map = {}

    # retrieves the data map keys
    data_map_keys = data_map.keys()

    # retrieves the root data map key
    form_data_map_key = data_map_keys[0]

    # retrieves the next depth level in the data map
    data_map = data_map[form_data_map_key]

    # creates the form data map
    self._create_form_data(request, data_map, form_data_map_key, form_data_map, encoding)

    # returns the form data map
    return form_data_map

def process_json_data(self, request, encoding = DEFAULT_ENCODING, force = False):
    """
    Processes the json data (attributes), creating a map containing
    the hierarchy of defined structure for the "json" contents.

    @type request: Request
    @param request: The request to be used.
    @type encoding: String
    @param encoding: The encoding to be used when retrieving
    the attribute values.
    @type force: bool
    @param force: If any cached data should be discarded and the
    the request information re-parsed if necessary.
    @rtype: Dictionary
    @return: The map containing the hierarchy of defined structure
    for the "json" contents.
    """

    # tries to retrieves the base attributes map from the
    # "cached" data in the request
    data_map = request.get_parameter(JSON_DATA_PRIVATE_VALUE)

    # in case there is cached data pending in the
    # request and the force flag is not set
    # uses it immediately
    if not force and data_map: return data_map

    # reads the contents from the request and then "loads"
    # the json structure from them, in case the value is not a
    # dictionary converts it into one settings the loaded contents
    # in a new dictionary "under" the root key value then stores the result
    # in the private json data value and returns the data map
    contents = request.read()
    data_map = self.json_plugin.loads(contents)
    is_valid = type(data_map) == types.DictType
    data_map = data_map if is_valid else dict(root = data_map)
    request.set_parameter(JSON_DATA_PRIVATE_VALUE, data_map)
    return data_map

def process_form_data(self, request, encoding = DEFAULT_ENCODING, nullify = False, force = False):
    """
    Processes the form data (attributes), creating a map containing
    the hierarchy of defined structure for the "form" contents.

    @type request: Request
    @param request: The request to be used.
    @type encoding: String
    @param encoding: The encoding to be used when retrieving
    the attribute values.
    @type nullify: bool
    @param nullify: If the data to be processed should be nullified
    in case empty string values are found.
    @type force: bool
    @param force: If any cached data should be discarded and the
    the request information re-parsed if necessary.
    @rtype: Dictionary
    @return: The map containing the hierarchy of defined structure
    for the "form" contents.
    """

    # tries to retrieve the base attributes map from the
    # "cached" data in the request, this will provide
    # a faster way to access the form data
    base_attributes_map = request.get_parameter(FORM_DATA_PRIVATE_VALUE)

    # in case there is cached data pending in the
    # request and the force flag is not set
    # returns it immediately (fast access)
    if not force and base_attributes_map: return base_attributes_map

    # retrieves the attributes list
    attributes_list = request.get_attributes_list()

    # creates the base attributes map
    base_attributes_map = {}

    # iterates over all the attributes in the
    # attributes list to process them creating the
    # appropriate representation for them
    for attribute in attributes_list:
        # in case the attribute is invalid or empty
        # must skip the current loop
        if not attribute: continue

        # retrieves the attribute value from the request,
        # decoding it according to the provided encoding
        # and then retrieves the (data) type for it
        attribute_value = self.get_attribute_decoded(request, attribute, encoding)
        attribute_value_type = type(attribute_value)

        # in case the attribute value type is list must iterate over each
        # of the values and assign the values to the associated index values
        if attribute_value_type == types.ListType:
            # starts the index to be used as counter for the
            # list structure assignment
            index = 0

            # iterates over all the attribute value items available for
            # the attribute name to assign them to the corresponding
            # data structures (first come first served approach)
            for attribute_value_item in attribute_value:
                # nullifies the attribute value item in case it's empty
                # (in case the nullify flag is set)
                if nullify: attribute_value_item = attribute_value_item or None

                # starts the processing of the form attribute with the base attributes map
                # the base attribute name and the attribute value and the index of the current
                # attribute value item
                self._process_form_attribute(
                    base_attributes_map,
                    attribute,
                    attribute_value_item,
                    index
                )

                # increments the index, next element in sequence must be
                # used in the next iteration
                index += 1

        # otherwise the attribute type must be a string and the processing of the
        # value is simpler as no sequence processing should be done
        else:
            # nullifies the attribute value in case it's empty
            # in case the nullify flag is set)
            if nullify: attribute_value = attribute_value or None

            # starts the processing of the form attribute with the base attributes map
            # the base attribute name and the attribute value
            self._process_form_attribute(
                base_attributes_map,
                attribute,
                attribute_value
            )

    # sets the "processed" form data in the request
    # for latter possible cache match
    request.set_parameter(FORM_DATA_PRIVATE_VALUE, base_attributes_map)

    # returns the base attributes map
    return base_attributes_map

def process_form_data_flat(self, request, encoding = DEFAULT_ENCODING, nullify = False):
    """
    Processes the form data (attributes), creating a map containing
    the hierarchy of defined structure for the "form" contents.
    This method runs in flat mode for hierarchies defined with "dot notation".

    @type request: Request
    @param request: The request to be used.
    @type encoding: String
    @param encoding: The encoding to be used when retrieving
    the attribute values.
    @type nullify: String
    @param nullify: If the data to be processed should be nullified
    in case empty string values are found.
    @rtype: Dictionary
    @return: The map containing the hierarchy of defined structure
    for the "form" contents.
    """

    # retrieves the attributes list
    attributes_list = request.get_attributes_list()

    # creates the base attributes map
    base_attributes_map = {}

    # iterates over all the attributes in the
    # attributes list
    for attribute in attributes_list:
        # retrieves the attribute value from the request
        attribute_value = self.get_attribute_decoded(request, attribute, encoding)

        # nullifies the attribute value in case it's empty
        # in case the nullify flag is set)
        if nullify: attribute_value = attribute_value or None

        # creates the attribute names list by splitting the attribute
        # "around" the dot values
        attribute_names_list = attribute.split(".")

        # reverses the attribute names list
        attribute_names_list.reverse()

        # process the entry attribute value with the initial (base) attributes map
        # the attribute names list and the attribute value
        self._process_form_attribute_flat(base_attributes_map, attribute_names_list, attribute_value)

    # returns the base attributes map
    return base_attributes_map

def process_acl_values(
    self,
    acl_list, key,
    wildcard_value = DEFAULT_WILDCARD_ACL_VALUE,
    maximum_value = DEFAULT_MAXIMUM_ACL_VALUE
):
    """
    Processes the various acl values in the given list.
    Retrieves the lowest value for the given key and takes into account
    the wildcard value for global permission values.

    @type acl_list: List
    @param acl_list: The list of acl (access control list) to
    be used for acl permission value retrieval.
    @type key: String
    @param key: The key to be used for retrieval of acl permissions
    value (this key is joined with the current wildcard).
    @type wildcard_key: String
    @param wildcard_key: The wilcard key to be used for retrieval
    of wildcard values.
    @type maximum_value: int
    @param maximum_value: The maximum value valid for acl permission
    values (this value should be changed carefully).
    @rtype: int
    @return: The lowest processed acl permission value for the given key.
    """

    # starts the permission values list with only the maximum
    # value in it
    permission_values = [maximum_value]

    # iterates over all the acl in the acl list
    for acl in acl_list:
        # retrieves the various permissions from the acl
        wildcard_permissions = acl.get(wildcard_value, maximum_value)
        key_permissions = acl.get(key, maximum_value)

        # adds the various permission values to the permission
        # values list
        permission_values.append(wildcard_permissions)
        permission_values.append(key_permissions)

    # retrieves the minimum value from the permission values
    permission = min(permission_values)

    # returns the permission
    return permission

def validate_acl_session(
    self,
    request,
    key,
    value = DEFAULT_VALUE_ATTRIBUTE,
    session_attribute = DEFAULT_SESSION_ATTRIBUTE
):
    """
    Validates the current session defined acl against the
    defined key and value.

    @type request: Request
    @param request: The request to be used.
    @type key: String
    @param key: The key to be used for retrieval of acl permissions
    value (this key is joined with the current wildcard).
    @type value: int
    @param value: The value to be used for testing as minimal
    valid value.
    @type session_attribute: String
    @param session_attribute: The name of the session attribute
    to retrieve the acl list.
    @rtype: bool
    @return: If the key is valid for the current session acl.
    """

    # retrieves the user acl value
    user_acl = self.get_session_attribute(request, session_attribute) or {}

    # process the acl values, retrieving the permissions value
    permissions = self.process_acl_values((user_acl, ), key)

    # checks if the value is valid according
    # to the retrieved permissions
    valid_acl = permissions <= value

    # returns the result of the valid acl test
    return valid_acl

def get_mvc_path(self, request, delta_value = 1):
    """
    Retrieves the mvc path according to
    the current request path.

    @type request: Request
    @param request: The request to be used to retrieve
    the mvc path.
    @type delta_value: int
    @param delta_value: The integer value that represents
    the number of partial paths to be removed from the
    original path to get the mvc path.
    @rtype: String
    @return: The base path.
    """

    # retrieves the path list length
    path_list_length = len(request.path_list)

    # creates the base path
    base_path = str()

    # iterates over all the path list length without
    # the delta value
    for _index in range(path_list_length - delta_value):
        # adds the back path to the base path
        base_path += BACK_PATH_VALUE

    # returns the base path
    return base_path

def get_base_path(self, request):
    """
    Retrieves the base path according to
    the current request path.

    @type request: Request
    @param request: The request to be used to retrieve
    the base path.
    @rtype: String
    @return: The base path.
    """

    return self.get_mvc_path(request, BASE_PATH_DELTA_VALUE)

def get_base_path_absolute(self, request):
    """
    Retrieves the base path absolute according to
    the current request path.

    @type request: Request
    @param request: The request to be used to retrieve
    the base path absolute.
    @rtype: String
    @return: The base path absolute.
    """

    # retrieves the base path list
    base_path_list = request.path_list[:1]

    # joins the base path list to retrieve the base
    # path absolute value
    base_path_absolute = "/".join(base_path_list) + "/"

    # returns the base path absolute
    return base_path_absolute

def get_base_path_complete(self, request, suffix_path = "", prefix_path = HTTP_PREFIX_VALUE):
    """
    Retrieves the base path complete according to
    the current request path.
    The complete base path includes the hostname
    and the full path to the resource.

    @type request: Request
    @param request: The request to be used to retrieve
    the base path complete.
    @rtype: String
    @return: The base path absolute.
    """

    # tries retrieves the host value for the base
    # value of the url construction
    host = self._get_host(request)

    # in case no host is defined
    if not host:
        # raises the insufficient http information exception
        raise exceptions.InsufficientHttpInformation("no host value defined")

    # retrieves the path, removes the arguments part
    # of it and the splits it in the separator value
    path = self._get_path(request)
    path = path.split("?")[0]
    path_list = path.split("/")

    # retrieves the path list of the request
    # as the request path list
    request_path_list = request.path_list

    # calculates both the path list length and
    # the request path list length
    path_list_length = len(path_list)
    request_path_list_length = len(request_path_list)

    # calculates the base path list length as the difference
    # between the path list length and the request path list length
    # (the remaining part of the url excluding the request part)
    base_path_list_length = path_list_length - request_path_list_length

    # calculates the complete length for the path list and then
    # use it to retrieve the complete path list
    complete_path_list_length = base_path_list_length + BASE_PATH_DELTA_VALUE - 1
    complete_path_list = path_list[:complete_path_list_length]

    # joins the "complete" path list to get the complete path
    complete_path = "/".join(complete_path_list)

    # creates the base path complete with the prefix path the "complete"
    # path and the suffix path
    base_path_complete = prefix_path + host + complete_path + suffix_path

    # returns the base path complete
    return base_path_complete

def set_contents(
    self,
    request,
    contents = "",
    content_type = DEFAULT_CONTENT_TYPE,
    touch_date = False,
    max_age = None
):
    """
    Sets the given contents in the given request.

    @type request: Request
    @param request: The request to be set with the contents.
    @type contents: String
    @param contents: The contents to set in the request.
    @type content_type: String
    @param content_type: The content type to be set.
    @type touch_date: bool
    @param touch_date: If the (modified) data value should be touched
    setting it to a time around the current local time, this is useful
    for situations where client cache should be used in a page loading
    scope (for performance issues).
    @type max_age: int
    @param max_age: The maximum age field to be used to control the cache
    for the current set of contents, this value provides the resources
    to set cache in the client side for the defined amount of seconds. It
    should be used carefully to avoid unwanted behavior.
    """

    # in case the touch date flag is set touches the date
    # updating the internal last modified date value, useful
    # for situation where cache is meant to be used inside the
    # page loading scope
    touch_date and request.touch_date()

    # if the max age field is requested for the current set of
    # contents its set so that the client side creates cache
    # for the current set of content to be "sent"
    max_age and request.set_max_age(max_age)

    # sets the content type, then the result as translated into
    # the target content type and then flushes the data meaning
    # that the buffer is written to the request
    request.set_content_type(content_type)
    request.set_result_translated(contents)
    request.flush()

def set_status_code(self, request, status_code = DEFAULT_STATUS_CODE):
    """
    Sets the given status code in the given request.

    @type request: Request
    @param request: The request to be set with the status code.
    @type contents: String
    @param contents: The status code to set in the request.
    """

    # sets the status code for the request
    request.set_status_code(status_code)

def get_referer(self, request):
    """
    Retrieves the referer value for the current request
    being used for the handling.
    The referer value shall not be trusted as it may not
    be defined in the request.

    @type request: Request
    @param request: The request to be used.
    @rtype: String
    @return: The retrieved referer value (url).
    """

    # retrieves the "referer" header
    referer_header = request.get_header(REFERER_VALUE)

    # returns the "referer" header (url)
    return referer_header

def redirect(
    self,
    request,
    target,
    status_code = 302,
    quote = False,
    attributes_map = None
):
    """
    Redirects the current request to the given
    target (page).

    @type request: Request
    @param request: The request to be used.
    @type target: String
    @param target: The target (page) of the redirect.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    # redirects the request to the target and sets the contents in
    # the current request (empty contents set)
    request.redirect(target, status_code, quote, attributes_map)
    self.set_contents(request)

def redirect_list(
    self,
    request,
    entity,
    level = None,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request to the list action
    of the given entity (instance).

    @type request: Request
    @param request: The request to be used.
    @type entity: Entity
    @param entity: The entity to be used for the redirection.
    @type level: Class
    @param level: Optional class level to be used to retrieve
    custom redirection names for upper inheritance.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    # retrieves the appropriate level value, defaulting to the class
    # of the current entity in case none is provided, this value is
    # going to be used to retrieve the correct label according to the
    # inheritance level that was requested
    level = level or entity.__class__

    # converts the entity class name to pluralized version, then
    # creates the target (list url) from the pluralized entity name
    # and redirects the request to the defined target
    entity_class_pluralized = entity._get_entity_class_pluralized(entity_class = level)
    target = entity_class_pluralized
    self.redirect_base_path(request, target, status_code, quote, attributes_map)

def redirect_action(
    self,
    request,
    entity = None,
    action = None,
    id_string = None,
    level = None,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request a custom entity action
    of the given entity (instance).

    An optional id string value may be provided to override
    the normal behavior of id value retrieval.

    @type request: Request
    @param request: The request to be used.
    @type entity: Entity
    @param entity: The entity to be used for the redirection.
    @type action: String
    @param action: The name of the action to be used for the
    redirection process, this value may contain an extension
    (eg: sales.json).
    @type id_string: String
    @param id_string: The value to be used in the identifier
    part of the url to be generated, in case this value is not
    provided the id value is inferred from the provided entity.
    @type level: Class
    @param level: Optional class level to be used to retrieve
    custom redirection names for upper inheritance.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    # retrieves the appropriate level value, defaulting to the class
    # of the current entity in case none is provided, this value is
    # going to be used to retrieve the correct label according to the
    # inheritance level that was requested
    level = level or entity.__class__

    # converts the entity class name to pluralized version using
    # the defined inheritance level and then retrieves the identifier
    # value for the current entity and converts it into a string
    # note that the identifier is only generated in case no identifier
    # had been provided to the method, otherwise uses the one provided
    entity_class_pluralized = entity._get_entity_class_pluralized(entity_class = level)
    if not id_string:
        entity_id_attribute_value = entity.get_id_attribute_value()
        entity_id_attribute_value_string = str(entity_id_attribute_value)
        id_string = entity_id_attribute_value_string

    # creates the target (edit url) from the pluralized entity name
    # and the entity id attribute value string and redirects the
    # request to the target (path)
    target = entity_class_pluralized + "/" + id_string +\
        ("/" + action if action else "")
    self.redirect_base_path(
        request,
        target,
        status_code,
        quote,
        attributes_map
    )

def redirect_create(
    self,
    request,
    entity,
    level = None,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request to the create action
    of the given entity (instance).

    @type request: Request
    @param request: The request to be used.
    @type entity: Entity
    @param entity: The entity to be used for the redirection.
    @type level: Class
    @param level: Optional class level to be used to retrieve
    custom redirection names for upper inheritance.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    # retrieves the appropriate level value, defaulting to the class
    # of the current entity in case none is provided, this value is
    # going to be used to retrieve the correct label according to the
    # inheritance level that was requested
    level = level or entity.__class__

    # converts the entity class name to pluralized version then
    # creates the target (create url) from the pluralized entity name
    # and redirects the request to the target (path)
    entity_class_pluralized = entity._get_entity_class_pluralized(entity_class = level)
    target = entity_class_pluralized + "/new"
    self.redirect_base_path(request, target, status_code, quote, attributes_map)

def redirect_show(
    self,
    request,
    entity,
    level = None,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request to the show action
    of the given entity (instance).

    @type request: Request
    @param request: The request to be used.
    @type entity: Entity
    @param entity: The entity to be used for the redirection.
    @type level: Class
    @param level: Optional class level to be used to retrieve
    custom redirection names for upper inheritance.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    self.redirect_action(
        request,
        entity,
        level = level,
        status_code = status_code,
        quote = quote,
        attributes_map = attributes_map
    )

def redirect_edit(
    self,
    request,
    entity,
    level = None,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request to the edit action
    of the given entity (instance).

    @type request: Request
    @param request: The request to be used.
    @type entity: Entity
    @param entity: The entity to be used for the redirection.
    @type level: Class
    @param level: Optional class level to be used to retrieve
    custom redirection names for upper inheritance.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    self.redirect_action(
        request,
        entity,
        action = "edit",
        level = level,
        status_code = status_code,
        quote = quote,
        attributes_map = attributes_map
    )

def redirect_delete(
    self,
    request,
    entity,
    level = None,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request to the delete action
    of the given entity (instance).

    @type request: Request
    @param request: The request to be used.
    @type entity: Entity
    @param entity: The entity to be used for the redirection.
    @type level: Class
    @param level: Optional class level to be used to retrieve
    custom redirection names for upper inheritance.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    self.redirect_action(
        request,
        entity,
        action = "delete",
        level = level,
        status_code = status_code,
        quote = quote,
        attributes_map = attributes_map
    )

def redirect_base_path(
    self,
    request,
    target,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request to the given
    target (page).
    This method updates the target to conform with the
    current base path.

    @type request: Request
    @param request: The request to be used.
    @type target: String
    @param target: The target (page) of the redirect.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    # retrieves the base path and uses it to crate
    # the target base path using the provided target
    # then redirects the agent to it
    base_path = self.get_base_path(request)
    target_base_path = base_path + target
    self.redirect(request, target_base_path, status_code, quote, attributes_map)

def redirect_mvc_path(
    self,
    request,
    target,
    status_code = 302,
    quote = True,
    attributes_map = None
):
    """
    Redirects the current request to the given
    target (page).
    This method updates the target to conform with the
    current mvc path.

    @type request: Request
    @param request: The request to be used.
    @type target: String
    @param target: The target (page) of the redirect.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    # retrieves the mvc path and uses it to crate
    # the target mvc path using the provided target
    # then redirects the agent to it
    mvc_path = self.get_mvc_path(request)
    target_mvc_path = mvc_path + target
    self.redirect(request, target_mvc_path, status_code, quote, attributes_map)

def redirect_back(
    self,
    request,
    default_target = "/",
    status_code = 302,
    quote = False,
    attributes_map = None
):
    """
    Redirects the current request to the previous header
    referred page or to the default target in case the no
    referer page is defined.

    @type request: Request
    @param request: The request to be used.
    @type default_target: String
    @param default_target: The default target (page) of the redirect.
    @type status_code: int
    @param status_code: The status code to be used.
    @type quote: bool
    @param quote: If the target path should be quoted.
    @type attributes_map: Dictionary
    @param attributes_map: Map containing the series of
    attributes to be sent over the target path in the
    redirect url.
    """

    # retrieves the "referer" header
    referer_header = request.get_header(REFERER_VALUE)

    # sets the target to the "referer" header or the
    # default target in case the "referer" is invalid
    target = referer_header or default_target

    # redirects the request to the target
    self.redirect(request, target, status_code, quote, attributes_map)

def set_redirect_to(self, request, target, reason = None):
    """
    Sets the "redirect to" operation information (target
    and optionally reason), for latter usage.

    No quoting will be done in the provided target address
    so if any quoting must be done it must be done outside
    of the function calling scope.

    @type request: Request
    @param request: The request to be used.
    @type target: String
    @param target: The target (page) of the redirect to operation.
    @type reason: String
    @param reason: A string describing the reason for
    the redirect to operation.
    """

    # sets both the target and the reason for the redirect to operation
    self.set_session_attribute(request, "redirect_to_target", target)
    self.set_session_attribute(request, "redirect_to_reason", reason)

    # sets the redirect to mark as false to provide support for a first mark
    self.set_session_attribute(request, "redirect_to_mark", False)

def mark_redirect_to(self, request):
    """
    "Marks" the "redirect to" operation, so that only one
    try for redirection is accepted.
    This method avoid possible (unwanted) replicas in the
    redirection process.
    This should be called in the redirection manager method.

    @type request: Request
    @param request: The request to be used.
    """

    # retrieves both the target and the mark session attributes
    # for processing of the mark
    redirect_target = self.get_session_attribute(request, "redirect_to_target")
    redirect_mark = self.get_session_attribute(request, "redirect_to_mark", unset_session_attribute = True)

    # in case the "redirect to" is already "marked" the redirection has
    # been done and now the normal behavior should prevail (removes the
    # "redirect to" session attribute)
    redirect_mark and self.unset_session_attribute(request, "redirect_to_target")

    # in case the redirect target is set and no marking
    # is do, need to mark it
    redirect_target and not redirect_mark and self.set_session_attribute(request, "redirect_to_mark", True)

def redirect_to(self, request, quote = False):
    """
    Redirects the current request to the current
    "redirect to" target.
    This method should be used after the setting of
    a redirect to attributes.

    @type request: Request
    @param request: The request to be used.
    @type quote: bool
    @param quote: If the redirect to target path should
    be quoted, the quoting of this values is dangerous.
    """

    # retrieves the redirect to target value from session, the unsets
    # it after the retrieval (avoid duplicate redirections)
    redirect_to_target = self.get_session_attribute(
        request,
        "redirect_to_target",
        unset_session_attribute = True
    )

    # in case no "redirect to" target is found
    # (there was no previous assignment of redirect to)
    # must return immediately
    if not redirect_to_target: return

    # redirects the request to the "redirect to" target
    # the quote flag attribute is propagated
    self.redirect(request, redirect_to_target, quote = quote)

def redirect_to_base_path(self, request, quote = False):
    """
    Redirects the current request to the current
    "redirect to" target.
    This method should be used after the setting of
    a redirect to attributes.
    This method also updates the target to conform
    with the current base path.

    @type request: Request
    @param request: The request to be used.
    @param quote: If the redirect to target path should
    be quoted, the quoting of this values is dangerous.
    """

    # retrieves the redirect to target value from session, the unsets
    # it after the retrieval (avoid duplicate redirections)
    redirect_to_target = self.get_session_attribute(
        request,
        "redirect_to_target",
        unset_session_attribute = True
    )

    # in case no "redirect to" target is found
    # (there was no previous assignment of redirect to)
    # must return immediately
    if not redirect_to_target: return

    # redirects (with base) the request to the "redirect to" target
    self.redirect_base_path(request, redirect_to_target, quote = quote)

def template(
    self,
    request = None,
    apply_base_path = True,
    assign_session = False,
    assign_flash = True,
    variable_encoding = None,
    content_type = None,
    set_contents = True,
    *args,
    **kwargs
):
    """
    Main entry method that generated and renders a template setting
    the resulting values as the contents for the provided request.

    This is an aggregation method that basically calls for the generation
    of the template file with the dynamic keyword arguments and then sets
    the contents resulting for the template rendering as contents.

    @type request: Request
    @param request: The request that is going to be used as the target for
    the setting of the contents (may be any kind of valid request object).
    @type apply_base_path: bool
    @param apply_base_path: If the base path should be applied on the template
    file (for relative path resolution).
    @type assign_session: bool
    @param assign_session: If the session variables should be assigned on the
    template file to be processed.
    @type assign_flash: bool
    @param assign_flash: If the flash information should be automatically
    assigned to the current template variables.
    @type variable_encoding: String
    @param variable_encoding: The encoding to be used to encode the variables
    in the template file processing.
    @type content_type: String
    @param content_type: The content type to be set.
    @type set_contents: bool
    @param set_contents: If the contents resulting from the processing of the
    template file should be set in the current request (default behavior).
    @rtype: String
    @return: The data resulting from the processing of the template file, this
    value may be re-used for any other operation, but it is especially relevant
    for operations that don't set the contents in the request.
    """

    template_file = self.template_file(request = request, *args, **kwargs)
    contents = self.process_set_contents(
        request,
        template_file,
        apply_base_path = apply_base_path,
        assign_session = assign_session,
        assign_flash = assign_flash,
        variable_encoding = variable_encoding,
        content_type = content_type,
        set_contents = set_contents
    )
    return contents

def template_file(self, template = None, *args, **kwargs):
    """
    Method that should provided the template file for a series
    of options that are considered to be dynamic.

    This method provided an entry point for the redefinition of
    template file provided (using inheritance).

    @type template: String
    @param template: The path to the template file that is going
    to be used as based for the template retrieval. This value
    is set as invalid by default.
    @rtype: TemplateFile
    @return: The final template file instance that may then be
    used for the proper rendering.
    """

    return self.retrieve_template_file(
        file_path = template,
        *args,
        **kwargs
    )

def serialize(self, request, contents, serializer = None):
    """
    Serializes the provided contents (wither map or list) using the
    infra-structure (serializer) that is currently defined for the
    request.

    An optional serializer attribute may be used to "force" the serializer
    that is going to be used in the contents serialization.

    The definition of the serializer is not part of the method and
    such behavior should be defined by the upper layers.

    The resulting data from the serialization is set as the contents
    for the current request and the proper mime type defined.

    @type request: Request
    @param request: The request object that is going to be used
    as reference for the retrieval of the serializer object and for
    the setting of the serialization result contents.
    @type contents: List/Dictionary
    @param contents: The contents that are going to be serialized using
    the context defined in the request.
    @type serializer: Object
    @param serializer: The serializer (protocol) compliant object that
    is going to be used for the "forced" serialization process.
    """

    # verifies if the serializer attribute is defined in the provided
    # request if that's the case and there's no provided serializer
    # such value is going to be used as the serializer for the contents
    is_defined = hasattr(request, "serializer")
    if is_defined: serializer = serializer or request.serializer
    if not serializer: return

    # runs the serialization process on the contents (dumps call) and
    # then retrieves the mime type for together with the data string
    # value set the contents in the current request
    data = serializer.dumps(contents)
    mime_type = serializer.get_mime_type()
    self.set_contents(request, data, content_type = mime_type)

def process_set_contents(
    self,
    request,
    template_file,
    apply_base_path = True,
    assign_session = False,
    assign_flash = True,
    variable_encoding = None,
    content_type = None,
    set_contents = True
):
    """
    Processes the template file and set the result of it
    as the contents of the given request.
    Optional flags may be set to apply the base path and assign the
    session to the template file.

    An optional parameter controls if the contents resulting from
    the processing of the template file should be set in the request.

    @type request: Request
    @param request: The request to be set with the contents.
    @type template_file: TemplateFile
    @param template_file: The template file to be processed.
    @type apply_base_path: bool
    @param apply_base_path: If the base path should be applied on the template
    file (for relative path resolution).
    @type assign_session: bool
    @param assign_session: If the session variables should be assigned on the
    template file to be processed.
    @type assign_flash: bool
    @param assign_flash: If the flash information should be automatically
    assigned to the current template variables.
    @type variable_encoding: String
    @param variable_encoding: The encoding to be used to encode the variables
    in the template file processing.
    @type content_type: String
    @param content_type: The content type to be set.
    @type set_contents: bool
    @param set_contents: If the contents resulting from the processing of the
    template file should be set in the current request (default behavior).
    @rtype: String
    @return: The string value resulting from the processing of the template
    file, this is especially important for no setting of contents operations.
    """

    # default the content type value taking into account if the content
    # type value is defined, this way it's possible to avoid the definition
    # of the content type parameter (best practice)
    content_type = content_type or DEFAULT_CONTENT_TYPE

    # applies the base path and assigns the session to the template file in
    # case the apply base path and the assign the session flags are set in
    # current environment (fast assign) then in case the assign flash flag
    # is set assigns the flash information to the template
    apply_base_path and self.apply_base_path_template_file(request, template_file)
    assign_session and self.assign_session_template_file(request, template_file)
    assign_flash and self.assign_flash_template_file(request, template_file)

    # assigns the basic instance attributes to the template file so that
    # it can access the controller instance and the system and plugin instances
    self.assign_instance_template_file(request, template_file)

    # processes the template file with the given request and variable encoding
    # retrieving the processed template file as the contents to be set
    contents = self.process_template_file(request, template_file, variable_encoding)

    # sets the request contents, using the given content type, only in case the
    # proper flag is set (allowing control for the operation execution)
    if set_contents: self.set_contents(request, contents, content_type)

    # returns the processed contents resulting from the template to the caller
    # method so that they may be reused for any other operation if required
    return contents

def process_template_file(self, request, template_file, variable_encoding = None):
    """
    Processes the given template file, using the given
    variable encoding.

    @type request: Request
    @param request: The request to be used in the template
    file processing.
    @type template_file: Template
    @param template_file: The template file to be processed.
    @type variable_encoding: String
    @param variable_encoding: The encoding to be used to encode the variables
    in the template file processing.
    @rtype: String
    @return: The processed template file.
    """

    # sets the template file variable encoding
    template_file.set_variable_encoding(variable_encoding)

    # creates the process methods list
    process_methods_list = [
        ("process_stylesheet_link", self.get_process_method(request, "process_stylesheet_link")),
        ("process_javascript_include", self.get_process_method(request, "process_javascript_include")),
        ("process_ifacl", self.get_process_method(request, "process_ifacl")),
        ("process_ifaclp", self.get_process_method(request, "process_ifaclp")),
        ("process_ifnotacl", self.get_process_method(request, "process_ifnotacl")),
        ("process_request_time", self.get_process_method(request, "process_request_time"))
    ]

    # attaches the process methods to the template file so that
    # they may be used for "extra" composite operations
    template_file.attach_process_methods(process_methods_list)

    # processes the template file, returning the resulting
    # contents to the caller function, the returning value
    # should be a string containing the results
    processed_template_file = template_file.process()
    return processed_template_file

def retrieve_template_file(
    self,
    file_path = None,
    encoding = DEFAULT_TEMPLATE_FILE_ENCODING,
    partial_page = None,
    locale = None,
    locale_request = None,
    extra = {},
    **kwargs
):
    """
    Retrieves a template file object for the given
    (relative) file path and locale and uses the
    given encoding to decode the template file.

    Optional parameters may control the partial page
    to be included "inside" the master template file
    and the locale to be used for the template file
    (if used the file name suffix is used by convention).

    @type file_path: String
    @param file_path: The relative template file path to
    retrieve the template file object.
    @type encoding: String
    @param encoding: The encoding charset to be used
    @type partial_page: String
    @param partial_page: The path to the partial page to be
    included as a sub-template in the master template file.
    to decode the template file.
    @type locale: String
    @param locale: The locate string that is going to be
    used to retrieve the appropriate template file.
    @type locale_request: Request
    @param locale_request: The request to be used for
    correct locale resolution.
    @type extra: Dictionary
    @param extra: This value may be used to add some extra
    values to be assigned to the template file, it's relevant
    for values that are not eligible for safe parameter and so
    they may be provided "inside" this dictionary.
    @rtype: TemplateFile
    @return: The "parsed" template file object ready
    to be used for file generation.
    """

    # retrieves the appropriate locale value, in case the locale request
    # is set the appropriate locale may be retrieved from session or header
    # values, this value will replaces the provided locale
    locale = locale_request and self.get_locale(locale_request) or locale

    # processes the file path according to the locale, the resulting file path
    # will be localized taking into account the exists (or not) of the file
    # according to the default file construction rules
    file_path = self._process_file_path_locale(
        file_path,
        locale = locale,
        base_path = self.templates_path
    )

    # creates the template file path, joining the templates path
    # and the (template file path) and then normalizes the path
    # so that no erroneous path is created (standard structure)
    template_file_path = os.path.join(self.templates_path, file_path)
    template_file_path = os.path.normpath(template_file_path)

    # retrieves the reference to the engine object/plugin that is
    # going to be used for the parsing and rendering of the target
    # template file to be used (this call may be overriden to be
    # able to select the best template engine)
    engine = self.get_template_engine_plugin()

    # parses the template file in the template file path assigning
    # the appropriate page include if the partial page value is set
    template_file = engine.parse_template(
        template_file_path,
        base_path = self.templates_path,
        encoding = encoding
    )
    if partial_page: self.assign_include_template_file(
        template_file,
        PAGE_INCLUDE_VALUE,
        partial_page,
        locale = locale,
        base_path = self.templates_path
    )

    # assigns the proper locale variable to the current template
    # so that it's possible to access it from within it
    template_file.assign("locale", locale)

    # retrieves the global bundle for the locale and adds it to the
    # template file in case it's a valid bundle (successful retrieval)
    global_bundle = self._get_bundle(locale)
    global_bundle and template_file.add_bundle(global_bundle)

    # iterates over the complete set of extra arguments provided in the
    # proper dictionary and assigns each of these values to the proper
    # template file so that they may be used inside the template context
    for key, value in extra.iteritems(): template_file.assign(key, value)

    # iterates over all the named arguments provided as these are considered
    # to be values to be assigned to the template file, then assigns each of
    # these values to the template file (variable export)
    for key, value in kwargs.iteritems(): template_file.assign(key, value)

    # returns the "generated" template file structure to the calling
    # method as requested by the method call
    return template_file

def apply_base_path_template_file(self, request, template_file):
    """
    Applies the base path to the template file according to
    the current request path.

    @type request: Request
    @param request: The request to be used to set the base path.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the base path.
    """

    # retrieves both the mvc and the base path and uses these
    # values to assign them to the provided template file as
    # expected by the call to this method
    mvc_path = self.get_mvc_path(request)
    base_path = self.get_base_path(request)
    template_file.assign(MVC_PATH_VALUE, mvc_path)
    template_file.assign(BASE_PATH_VALUE, base_path)

def assign_instance_template_file(self, request, template_file):
    """
    Assigns the various instance related attributes to the
    given template file.

    The instance attributes include the instance itself, the
    associated system, and the associated plugin.

    @type request: Request
    @param request: The request that is going to be used for the
    closure with some of the operations.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the
    various instance attributes.
    """

    def _copy(value, all = True):
        print "_copy -> all = %s" % str(all)
        value = "Copy right by: " + value
        return value

    def _nl_to_br(value, extra = False):
        tobias = value + "nl_to_br"
        if extra: tobias += " extra"
        return tobias

    def _echo(*args, **kwargs):
        return str(args)

    def _same(value):
        return value

    def _url_for(*args, **kwargs):
        return self.url_for(request, *args, **kwargs)

    # assigns the top level clojure based operations that may
    # be used for the current context, this values are context
    # aware and may be used for the current request
    template_file.assign("copy", _copy)
    template_file.assign("same", _same)
    template_file.assign("url_for", _url_for)
    template_file.assign("echo", _echo)
    template_file.assign("nl_to_br", _nl_to_br)

    # assigns the various instance components to the template file:
    # the instance itself, the associated system and the associated plugin
    template_file.assign("self", self)
    template_file.assign("system_s", self.system)
    template_file.assign("plugin_s", self.plugin)

def assign_flash_template_file(self, request, template_file):
    """
    Assigns the flash attribute to the given template file.
    The flash map is set in the template and unset from session
    (to avoid duplicate display).

    @type request: Request
    @param request: The request to be used.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the flash map.
    """

    # retrieves the flash map from the session and unsets it
    # from session (avoids duplicate display)
    flash = self.get_session_attribute(request, "_flash", unset_session_attribute = True)

    # assigns the flash map to the template file
    template_file.assign("_flash", flash)

def assign_session_template_file(self, request, template_file, variable_prefix = "session_"):
    """
    Assigns the session attributes to the given template file.
    The properties of the session are also set for base accessing.
    The name of the session attributes is modified replacing
    the dots with underscores.

    @type request: Request
    @param request: The request to be used.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the session attributes.
    @type variable_prefix: String
    @param variable_prefix: The variable prefix to be prepended to the variable names.
    """

    # tries to retrieve the session object currently associated
    # with the provided request should comply with the pre-defined
    # session rules (dictionary accessible)
    request_session = request.get_session()

    # in case the request session
    # is invalid, returns immediately not
    # possible to retrieve the values
    if not request_session: return

    # retrieves the various session properties
    session_id = request_session.get_session_id()
    session_timeout = request_session.get_timeout()
    session_maximum_timeout = request_session.get_maximum_timeout()
    session_expire_time = request_session.get_expire_time()

    # assigns the various session properties to the template file
    template_file.assign(variable_prefix + "id", session_id)
    template_file.assign(variable_prefix + "timeout", session_timeout)
    template_file.assign(variable_prefix + "maximum_timeout", session_maximum_timeout)
    template_file.assign(variable_prefix + "expire_time", session_expire_time)

    # retrieves the session attributes map, this map should contain
    # a key value association between the various session attributes
    # and the various value, note that this object may only be a
    # proxy to the real data structures behind the session
    session_attributes_map = request_session.get_attributes_map()
    template_file.assign("session", session_attributes_map)

    # iterates over all the session attributes in the session
    # attributes map to assign them to the current template with
    # the proper prefix value associated (legacy support)
    for name in session_attributes_map:
        # retrieves the value from the session attributes map,
        # then replaces the name with the proper value using the
        # underscore notation instead of the dot based one and
        # assigns the proper session value to the template
        value = session_attributes_map[name]
        name_replaced = name.replace(".", "_")
        template_file.assign(variable_prefix + name_replaced, value)

def assign_include_template_file(
    self,
    template_file,
    variable_name,
    variable_value,
    locale = None,
    base_path = None
):
    # in case the locale attribute is defined, must process the variable
    # value first so that the variable value is processed and the proper
    # localized version is used instead of the "raw" value, then assigns
    # the resulting value (or the original) to the template file
    if locale: variable_value = self._process_file_path_locale(
        variable_value,
        locale = locale,
        base_path = base_path
    )
    template_file.assign(variable_name, variable_value)

def get_session(self, request, name, unset = False):
    """
    Retrieves the value of the request session attribute name.

    This method works as an short name alias for the more
    complex and powerful method.

    @type request: Request
    @param request: The request that is going to be used for
    the retrieval of session to be used in the attribute get.
    @type name: String
    @param name: The name of the attribute for which the value
    currently set in session is meant to be retrieved.
    @type unset: bool
    @param unset: If the session attribute should be unset after
    the retrieval of the value.
    @rtype: Object
    @return: The value of the session attribute with the provided
    name, returned from the session associated with the request.
    """

    return self.get_session_attribute(
        request,
        session_attribute_name = name,
        unset_session_attribute = unset
    )

def set_session(self, request, name, value):
    """
    Sets a session attribute with the provided name and value in
    the session associated with the provided request.

    This method works as an short name alias for the more
    complex and powerful method.

    @type request: Request
    @param request: The request that is going to be used for
    the setting of the session attribute.
    @type name: String
    @param name: The name to be given to the attribute that is
    going to be set in session.
    @type value: Object
    @param value: The value that is going to be set in the session
    attribute with the provided name.
    """

    return self.set_session_attribute(
        request,
        session_attribute_name = name,
        session_attribute_value = value
    )

def lock_session(self, request):
    """
    Locks the session associated with the provided request,
    subsequent accesses to the session will be blocked until the
    session is released.

    @type request: Request
    @param request: The request to be used.
    """

    # tries to retrieve the request session
    request_session = request.get_session()

    # in case the request session
    # is invalid
    if not request_session:
        # start a session if none is started and then
        # retrieves it from the request
        request.start_session()
        request_session = request.get_session()

    # locks the "just" retrieved (or created) request
    # session (blocks it)
    request_session.lock()

def release_session(self, request):
    """
    Releases the session associated with the provided request,
    allowing further requests to access the session to be passed.

    @type request: Request
    @param request: The request to be used.
    """

    # tries to retrieve the request session
    request_session = request.get_session()

    # in case the request session is invalid
    # an exception should be raised (invalid situation)
    if not request_session: raise RuntimeError("problem releasing session, no session available")

    # releases the "just" retrieved request
    # session (unblocks it)
    request_session.release()

def start_session(self, request, force = False, set_cookie = True):
    """
    Starts a new session for the provided request, by
    default the session is created even if a previous one
    already exists in the request.

    An optional set cookie flag may control if the cookie
    value should be returned to the client side.

    @type request: Request
    @param request: The request to be used.
    @type force: bool
    @param force: If a session must be created even if a previous
    one is already created and set in the request.
    @type set_cookie: bool
    @param set_cookie: If the set cookie header must be set
    in the request indicating the new session to the client.
    @rtype: Session
    @return: The session that has just been created.
    """

    # start a session if none is started and then
    # retrieves it from the request
    request.start_session(force = force)
    request_session = request.get_session()

    # in case the set cookie flag is not set the
    # cookie must be removed from the request
    # session (this way the client is not updated)
    not set_cookie and request_session.set_cookie(None)

    # returns the "just" created request session
    return request_session

def reset_session(self, request):
    """
    Resets the session present in the current request,
    to reset the session is to unset it from the request.

    This method is useful for situation where a new session
    context is required or one is meant to be created always.

    @type request: Request
    @param request: The request to be used.
    """

    # resets the session removing it from the request
    # this allows subsequent calls to create a new session
    request.reset_session()

def set_session_short(self, request):
    """
    Sets the current session as short so that the
    expire value is much shorter than the default
    (almost eternal) value used by the system.

    This method may be used to provide additional
    security.

    @type request: Request
    @param request: The request to be used.
    """

    # tries to retrieve the request session in case
    # it's not found starts a new session and then retrieves
    # it so that it can have its timeout value changed
    request_session = request.get_session()
    if not request_session:
        request.start_session()
        request_session = request.get_session()

    # updates the request session timeout to a much shorter
    # value defined (as constant)
    request.update_timeout(
        timeout = SHORT_TIMEOUT,
        maximum_timeout = SHORT_MAXIMUM_TIMEOUT
    )

def get_session_attribute(
    self,
    request,
    session_attribute_name,
    namespace_name = None,
    unset_session_attribute = False
):
    """
    Retrieves the session attribute from the given request
    with the given name and for the given namespace.
    Optionally it may be unset from session after retrieval.

    @type request: Request
    @param request: The request to be used.
    @type session_attribute_name: String
    @param session_attribute_name: The name of the session
    attribute to be retrieved.
    @type namespace_name: String
    @param namespace_name: The name of the namespace for the
    attribute to be retrieved.
    @type unset_session_attribute: bool
    @param unset_session_attribute: If the session attribute should
    be unset after retrieval (read once).
    @rtype: Object
    @return The retrieved session attribute.
    """

    # tries to retrieve the request session
    request_session = request.get_session()

    # in case the request session
    # is invalid, must return invalid
    if not request_session: return None

    # resolves the complete session attribute name, taking into
    # account that a namespace name may exist
    session_attribute_name = _get_complete_session_attribute_name(
        session_attribute_name,
        namespace_name = namespace_name
    )

    # retrieves the attribute from the session, this attribute
    # may assume any data type (not only string based)
    session_attribute = request_session.get_attribute(session_attribute_name)

    # in case the unset the session attribute flag is set
    # the session attribute is unset
    unset_session_attribute and request_session.unset_attribute(session_attribute_name)

    # returns the session attribute to the caller method as expected
    # by the current infra-structure
    return session_attribute

def set_session_attribute(
    self,
    request,
    session_attribute_name,
    session_attribute_value,
    namespace_name = None
):
    """
    Sets the session attribute in the given request
    with the given name and for the given namespace.
    The session attribute value may be of any type.

    @type request: Request
    @param request: The request to be used.
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

    # tries to retrieve the request session
    request_session = request.get_session()

    # in case the request session
    # is invalid, currently not available
    if not request_session:
        # start a session if none is started and then
        # retrieves it from the request
        request.start_session()
        request_session = request.get_session()

    # resolves the complete session attribute name taking into
    # account the proper namespace value and then sets the
    # attribute in the currently retrieved session (as requested)
    session_attribute_name = _get_complete_session_attribute_name(session_attribute_name, namespace_name)
    request_session.set_attribute(session_attribute_name, session_attribute_value)

def unset_session_attribute(self, request, session_attribute_name, namespace_name = None):
    """
    Unsets the session attribute from the given request
    with the given name and for the given namespace.

    @type request: Request
    @param request: The request to be used.
    @type session_attribute_name: String
    @param session_attribute_name: The name of the session
    attribute to be unset.
    @type namespace_name: String
    @param namespace_name: The name of the namespace for the
    attribute to be unset.
    """

    # tries to retrieve the request session
    request_session = request.get_session()

    # in case the request session
    # is invalid, returns immediately
    if not request_session: return None

    # resolves the complete session attribute name
    session_attribute_name = _get_complete_session_attribute_name(session_attribute_name, namespace_name)

    # unsets the attribute from the session
    request_session.unset_attribute(session_attribute_name)

def get_context_attribute(self, request, context_name, namespace_name = None):
    """
    Retrieves the value of the context attribute with the
    provided name.

    In case no attribute is found a none value is returned.

    @type request: Request
    @param request: The request to be used.
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
    context = self.get_session_attribute(request, "_context", namespace_name)
    if context == None: context = {}

    # returns the retrieves attribute value, defaulting to none
    # in case it's not present in the context map
    return context.get(context_name, None)

def set_context_attribute(
    self,
    request,
    context_name,
    context_value,
    override = True,
    namespace_name = None
):
    """
    Sets the context attribute with the provided name with
    the provided value.

    An optional override variable is provided so that is
    possible to override an already present context value
    with the same name (conflict resolution).

    @type request: Request
    @param request: The request to be used.
    @type context_name: String
    @param context_name: The name of the of the context attribute
    to set the value.
    @type context_value: Object
    @param context_value: The value to be set for the attribute.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used
    for the context (session) variable to be updated.
    """

    # retrieves the context defaulting to a new and empty map
    # in case an invalid session attribute is returned
    context = self.get_session_attribute(request, "_context", namespace_name)
    if context == None: context = {}

    # updates the context with the provided attribute, overriding
    # the already present value in case the flag is set and then
    # sets the context map "back" in the session
    if override or not context_name in context: context[context_name] = context_value
    self.set_session_attribute(request, "_context", context, namespace_name)

def unset_context_attribute(self, request, context_name, namespace_name = None):
    """
    Unsets the context attribute with the provided name.

    This operation should remove any reference to the context
    attribute in the current session

    @type request: Request
    @param request: The request to be used.
    @type context_name: String
    @param context_name: The name of the of the context attribute
    to be unset.
    @type namespace_name: String
    @param namespace_name: The name of the namespace to be used
    for the context (session) variable to be updated.
    """

    # retrieves the context defaulting to a new and empty map
    # in case an invalid session attribute is returned
    context = self.get_session_attribute(request, "_context", namespace_name)
    if context == None: context = {}

    # updates the context with the provided attribute, removing
    # the already present value and then sets the context map
    # "back" in the session
    if context_name in context: del context[context_name]
    self.set_session_attribute(request, "_context", context, namespace_name)

def get_session_id(self, request):
    """
    Retrieves the session id for the session that exists
    in the given request.

    @type request: Request
    @param request: The request to be used.
    @rtype: String
    @return: The session id that exists in the given request.
    """

    # tries to retrieve the request session
    request_session = request.get_session()

    # in case the request session
    # is invalid returns an invalid value
    if not request_session: return None

    # retrieves the session id and returns
    # it to the caller method (as defined in spec)
    session_id = request_session.get_session_id()
    return session_id

def get_attribute_decoded(self, request, attribute_name, encoding = DEFAULT_ENCODING):
    """
    Retrieves the attribute from the request with
    the given attribute name and decoded using the given
    encoding.

    This is an expensive operation in case the requested
    attribute is a complex sequence, as all the values
    contained in it will be decoded and the structure will
    be re-created.

    @type request: Request
    @param request: The request to be used to retrieve the
    attribute.
    @type attribute_name: String
    @param attribute_name: The name of the attribute to retrieve.
    @type encoding: String
    @param encoding: The name of the encoding to be used in the retrieving
    of the attribute.
    @rtype: Object
    @return: The decoded attribute.
    """

    # retrieves the attribute value from the attribute name
    # using the mvc (sub) system
    attribute_value = self._get_attribute(request, attribute_name)

    # in case the attribute value is not valid returns an empty
    # string as the default fallback value
    if not attribute_value: return ""

    # retrieves the attribute value type
    attribute_value_type = type(attribute_value)

    # in case the attribute value is a list
    if attribute_value_type == types.ListType:
        # starts the attribute value decoded as list
        attribute_value_decoded = []

        # iterates over all the attribute value
        # items in the attribute value
        for attribute_value_item in attribute_value:
            # "casts" the attribute value item and retrieves
            # the attribute value item type
            attribute_value_item = self._cast_attribute_value(attribute_value_item)
            attribute_value_item_type = type(attribute_value_item)

            # decodes the attribute value item, only in case
            # it's a valid string
            attribute_value_item_decoded = attribute_value_item_type == types.StringType and\
                attribute_value_item.decode(encoding) or attribute_value_item

            # adds the attribute value item to the attribute
            # value decoded
            attribute_value_decoded.append(attribute_value_item_decoded)
    # in case the attribute is a map
    elif attribute_value_type == types.DictType:
        # starts the attribute value decoded as map
        attribute_value_decoded = {}

        # iterates over all the attribute value
        # items in the attribute value
        for attribute_value_key, attribute_value_value in attribute_value.items():
            # "casts" the attribute value value and retrieves
            # the attribute value value type
            attribute_value_value = self._cast_attribute_value(attribute_value_value)
            attribute_value_value_type = type(attribute_value_value)

            # decodes the attribute value value, only in case
            # it's a valid string
            attribute_value_value_decoded = attribute_value_value_type == types.StringType and\
                attribute_value_value.decode(encoding) or attribute_value_value

            # sets the attribute value value in the attribute value decoded map
            attribute_value_decoded[attribute_value_key] = attribute_value_value_decoded
    # otherwise it must be a string
    else:
        # decodes the attribute value, only in case
        # it's a valid string
        attribute_value_decoded = attribute_value_type == types.StringType and\
            attribute_value.decode(encoding) or attribute_value

    # returns the attribute value decoded
    return attribute_value_decoded

def get_locale(
    self,
    request,
    available_locales = (DEFAULT_LOCALE,),
    alias_locales = DEFAULT_ALIAS_LOCALES,
    default_locale = DEFAULT_LOCALE
):
    """
    Retrieves the current "best" locale for the given request and
    for the available locales.
    In case no available locales are used the default locale is used.

    The set of locales to be set available may be constrained using
    the available locales list.

    @type request: Request
    @param request: The request to be used.
    @type available_locales: Tuple
    @param available_locales: A tuple containing the available
    and "valid" locales, used to constrain the retrieval.
    @type alias_locales: Dictionary
    @param alias_locales: The map to be used for locale alias resolution.
    @type default_locale: String
    @param default_locale: The default locale to be used.
    @rtype: String
    @return: The current "best" locale"
    """

    # creates the get locales method tuple
    get_locales_methods = (
        self._get_locales_session,
        self._get_locales_header,
        self._get_locales_default
    )

    # sets the initial locale value this is going to be the
    # fallback value in case no valid locale is found
    locale = None

    # iterates over all the get locales methods, to call
    # them in sequence, trying to retrieve a valid locale
    # for retrieval (tries to find the best fit)
    for get_locales_method in get_locales_methods:
        # calls the get locales method to retrieve the list of
        # "resolved" locales, and sets the complete list as the
        # default list of available locales
        locales_list = get_locales_method(request)
        available_locales_list = locales_list

        # in case the available locales map is not set (invalid value)
        # no need to continue with the filtering of the locales list
        if available_locales == None: pass
        else: available_locales_list = [value for value in locales_list if value in available_locales]

        # in case the available locales list is not valid
        # (empty), validates only in case the available
        # locates is valid
        if not available_locales_list: continue

        # retrieves the (first) locale from the available
        # locales list, it's considered to be the primary
        # locale
        locale = available_locales_list[0]

        # breaks the loop
        break

    # resolves the alias locale (retrieving the
    # "real" locale) and returns it
    locale = alias_locales.get(locale, locale)
    return locale

def locale_value(self, value, locale = None):
    """
    Localizes the provided value (eg: string) to the provided locale
    the resulting value should be a string represented in the requested
    locale value.

    @type value: Object
    @poram value: The value to be "localized" into the target locale, this
    value should probably be a string.
    @rtype: Object
    @return: The localized value, this value should probably be a string.
    """

    # retrieves the global bundle for the locale and then uses it
    # to retrieve the appropriate locale value
    global_bundle = self._get_bundle(locale)
    locale_value = global_bundle.get(value, value)

    # in case the (private) replace method is present in
    # the value the substitution of the value must be done
    # through it otherwise the value reference is replaced
    # by the newly retrieved value
    if hasattr(value, "__replace__"): value.__replace__(locale_value)
    else: value = locale_value

    # returns the (now) localized value this must probably
    # a localized string value
    return value

def set_locale_session(self, request, locale):
    """
    Sets the locale session attribute for later locale
    retrieval.

    @type request: Request
    @param request: The request to be used.
    @type locale: String
    @param locale: The locale to be set in session.
    """

    # sets the locale session attribute
    self.set_session_attribute(request, LOCALE_SESSION_ATTRIBUTE, locale)

def range_d(self, request, default = "day", _datetime = False):
    """
    Calculates the timestamp based date range for the provided
    request according to the specification.

    The calculation of the range taking into account that if
    only a "lower" value is filled the "upper" values are set
    with the current date related values (eg: if day one is
    specified the range is day one of the current month and year).

    The default argument may be used to control the default behavior
    in case no value is passed.

    The datetime argument controls if the returned tuple value
    should be converted into a date time object.

    This is the internal method and should not be used from
    an interface level.

    @type request: Request
    @param request: The request to be used for the
    computation of the date range.
    @type default: String
    @param default: The default mode to be used in case no value
    is retrieved from the request.
    @type _datetime: bool
    @param _datetime: Flag that controls if the returned value
    should be converted to datetime or left as timestamp.
    @rtype: Tuple
    @return: Tuple containing either a tuple of timestamps defining
    the date range or a tuple of date time objects.
    """

    # calculates the start and end range from the request
    # and returns immediately the received tuple in case the
    # date time mode is not set (no conversion required)
    start, end = self._range_d(request, default)
    if not _datetime: return start, end

    # converts both the start timestamp and the end timestamp
    # into corresponding date time representation and returns
    # a tuple containing them to the caller method
    start_date = datetime.datetime.utcfromtimestamp(start)
    end_date = datetime.datetime.utcfromtimestamp(end)
    return start_date, end_date

def update_resources_path(self, parameters = {}):
    """
    Updates the resources path, changing the paths
    for the extra and templates references.

    @type parameters: Dictionary
    @param parameters: The parameters for the updating.
    """

    # retrieves the extra path values
    extra_extras_path = parameters.get(EXTRA_EXTRAS_PATH_VALUE, "")
    extra_template_path = parameters.get(EXTRA_TEMPLATES_PATH_VALUE, "")

    # creates the templates path from the extras path
    extras_path = os.path.join(self.resources_path, EXTRAS_VALUE)
    extras_path = os.path.join(extras_path, extra_extras_path)

    # creates the templates path from the resources path
    templates_path = os.path.join(self.resources_path, TEMPLATES_VALUE)
    templates_path = os.path.join(templates_path, extra_template_path)

    # creates the locales path from the resources path
    locales_path = os.path.join(self.resources_path, LOCALES_VALUE)

    # sets the extras path
    self.set_extras_path(extras_path)

    # sets the templates path
    self.set_templates_path(templates_path)

    # sets the locales path
    self.set_locales_path(locales_path)

def set_relative_resources_path(
    self,
    relative_resources_path,
    extra_extras_path = "",
    extra_templates_path = "",
    update_resources = True
):
    """
    Sets the relative resources path for template resolution
    and optionally updates the resources.

    @type relative_resources_path: String
    @param relative_resources_path: The relative resources path
    to be used for template resolution.
    @type extra_extras_path: String
    @param extra_extras_path: The extra extras path to be appended to the
    extras path after resolution.
    @type extra_templates_path: String
    @param extra_templates_path: The extra templates path to be appended to the
    templates path after resolution.
    @type update_resources: bool
    @param update_resources: If the associated resources
    should be updated.
    """

    # retrieves the plugin manager
    plugin_manager = self.plugin.manager

    # retrieves the plugin id
    plugin_id = self.plugin.id

    # retrieves the plugin path
    plugin_path = plugin_manager.get_plugin_path_by_id(plugin_id)

    # creates the full absolute resources path from the plugin path
    resources_path = os.path.join(plugin_path, relative_resources_path)

    # creates the parameters map to be used
    parameters = {
        EXTRA_EXTRAS_PATH_VALUE : extra_extras_path,
        EXTRA_TEMPLATES_PATH_VALUE : extra_templates_path
    }

    # sets the resources path
    self.set_resources_path(resources_path, update_resources, parameters)

def resolve_relative_path(self, relative_path, extra_path = None):
    """
    Resolves the relative path as an absolute path.
    The resolution takes into account an extra path that may
    be added to the resolved path.

    @type relative_path: String
    @param relative_path: The relative path to be used for resolution.
    @param extra_extras_path: The extra path to be appended to the
    relative resources path after resolution.
    @rtype: String
    @return: The resolved relative path as an absolute path.
    """

    # retrieves the plugin manager
    plugin_manager = self.plugin.manager

    # retrieves the plugin id
    plugin_id = self.plugin.id

    # retrieves the plugin path
    plugin_path = plugin_manager.get_plugin_path_by_id(plugin_id)

    # creates the full absolute path from the relative path
    resolved_path = os.path.join(plugin_path, relative_path)

    # appends the extra path to the resolved path to create
    # the "final" resolved path (in case it's defined)
    resolved_path = extra_path and os.path.join(resolved_path, extra_path) or resolved_path

    # returns the resolved path
    return resolved_path

def resolve_resource_path(self, resource_path):
    """
    Resolves the given absolute path for the given
    (relative) resource path.
    This resolution implies the previous setting of
    the resources path.

    @type resource_path: String
    @param resource_path: The relative path to the
    resource, to be converted into absolute path.
    @rtype: String
    @return: The resolved absolute path to the resource.
    """

    # joins the current (absolute) resources path
    # with the given (relative) resource path, creating
    # the resource absolute path
    resource_absolute_path = os.path.join(self.resources_path, resource_path)

    # returns the resource absolute path
    return resource_absolute_path

def set_flash_error(self, request, message):
    """
    Sets a flash error message to be displayed in the
    next template file parsing.

    @type request: Request
    @param request: The request to be used.
    @type message: String
    @param message: The message to be displayed as an
    error in the next template parsing.
    """

    self.set_flash(request, message, "error")

def set_flash_warning(self, request, message):
    """
    Sets a flash warning message to be displayed in the
    next template file parsing.

    @type request: Request
    @param request: The request to be used.
    @type message: String
    @param message: The message to be displayed as a
    warning in the next template parsing.
    """

    self.set_flash(request, message, "warning")

def set_flash_success(self, request, message):
    """
    Sets a flash success message to be displayed in the
    next template file parsing.

    @type request: Request
    @param request: The request to be used.
    @type message: String
    @param message: The message to be displayed as a
    success in the next template parsing.
    """

    self.set_flash(request, message, "success")

def set_flash(self, request, message, message_type):
    """
    Sets the the flash message to be display in the
    appropriate session attribute.

    @type request: Request
    @param request: The request to be used to set the
    flash in session.
    @type message: String
    @param message: The message to be displayed as flash.
    @type message_type: String
    @param message_type: The type of message to be displayed
    as flash (eg: error, warning, success).
    """

    # creates the flash map with both the message
    # contents and the message type
    flash = {
        "message" : message,
        "type" : message_type
    }

    # sets the flash map in the session
    self.set_session_attribute(request, "_flash", flash)

def get_plugin(self):
    """
    Retrieves the plugin.

    @rtype: Plugin
    @return: The plugin.
    """

    return self.plugin

def set_plugin(self, plugin):
    """
    Sets the plugin.

    @type plugin: Plugin
    @param plugin: The plugin.
    """

    self.plugin = plugin

def get_resources_path(self):
    """
    Retrieves the resources path.

    @rtype: String
    @return: The resources path.
    """

    return self.resources_path

def set_resources_path(self, resources_path, update_resources = True, parameters = {}):
    """
    Sets the resources path.
    Optionally an update on all resource related
    path may be triggered.

    @type resources_path: String
    @param resources_path: The resources path.
    @type update_resources: bool
    @param update_resources: If the associated resources
    should be updated.
    @type parameters: Dictionary
    @param parameters: The parameters for the setting.
    """

    # sets the resources path in the current instance for
    # latter usage
    self.resources_path = resources_path

    # in case the update resources flag is set (the updating
    # of the resources path uses the parameters)
    update_resources and self.update_resources_path(parameters)

def get_extras_path(self):
    """
    Retrieves the extras path.

    @rtype: Sring
    @return: The extras path.
    """

    return self.extras_path

def set_extras_path(self, extras_path):
    """
    Sets the extras path.

    @type extras_path: String
    @param extras_path: The extras path.
    """

    self.extras_path = extras_path

def get_templates_path(self):
    """
    Retrieves the templates path.

    @rtype: String
    @return: The templates path.
    """

    return self.templates_path

def set_templates_path(self, templates_path):
    """
    Sets the templates path.

    @type templates_path: String
    @param templates_path: The templates path.
    """

    self.templates_path = templates_path

def get_locales_path(self):
    """
    Retrieves the locales path.

    @rtype: String
    @return: The locales path.
    """

    return self.locales_path

def set_locales_path(self, locales_path):
    """
    Sets the locales path.

    @type locales_path: String
    @param locales_path: The locales path.
    """

    self.locales_path = locales_path

def get_default_parameters(self):
    """
    Retrieves the default parameters map to be used in the
    request "workflow".

    @rtype: Dictionary
    @return: The default parameters map to be used in the
    request "workflow".
    """

    return self.default_parameters

def set_default_parameters(self, default_parameters):
    """
    Retrieves the default parameters map to be used in the
    request "workflow".

    @type default_parameters: Dictionary
    @param default_parameters: The default parameters map
    o be used in the request "workflow".
    """

    self.default_parameters = default_parameters

def extend_default_parameters(self, extension_parameters):
    """
    Extends the default parameters map with the given
    map of parameters.

    @type extension_parameters: Dictionary
    @param extension_parameters: The map of parameters to
    extend the default parameters map.
    """

    # extends the default parameters with the extension parameters
    colony.map_extend(
        self.default_parameters,
        extension_parameters,
        copy_base_map = False
    )

def set_default_parameter(self, parameter_name, parameter_value):
    """
    Sets a parameters to be used as default (template) in the
    handling of a request.

    @type parameter_name: String
    @param parameter_name: The name of the parameter to be set.
    @type parameter_value: Object
    @param parameter_value: The value of the parameter to be set
    """

    self.default_parameters[parameter_name] = parameter_value

def unset_default_parameter(self, parameter_name):
    """
    Unsets (deletes) a parameter from the map of default
    parameters to be used in the request handling.

    @type parameter_name: String
    @param parameter_name: The name of the parameter to be unset
    from the default parameter map.
    """

    del self.default_parameters[parameter_name]

def get_template_engine_plugin(self):
    """
    Retrieves the template engine plugin that is currently
    under usage for the current controller. This is the
    template engine used for the default rendering of files
    corresponding to templates in the controller.

    @rtype: Plugin
    @return: The template engine plugin that is currently
    in used for rendering of templates in the controller.
    """

    return self.template_engine_plugin

def set_template_engine_plugin(self, template_engine_plugin):
    """
    Sets the template engine plugin, this setting operation
    will define the kind of template engine that is going
    to be used for template rendering in this controller.

    @type template_engine_plugin: Plugin
    @param template_engine_plugin: The template engine
    manager plugin that is going to be used for the rendering
    of templates for the current controller.
    """

    self.template_engine_plugin = template_engine_plugin

def get_engine(self, name):
    """
    Retrieves the (template) engine for the requested name,
    this value is going to be retrieved from the currently
    set map of engines in from the controller.

    @type name: String
    @param name: The name of the engine that is meant to
    be retrieved, this name should be compliant with the
    short name of the associated plugin.
    @rtype: Plugin
    @return: The template engine plugin for the requested
    short name, may be latter used for the rendering of
    template based files (as defined by each specification).
    """

    return self.engines.get(name, None)

def set_engines(self, engines):
    """
    Sets the map of engines that is going to be used as reference
    for the retrieval of template engines for the controller.

    @type engines: Dictionary
    @param engines: The map that contains a key value association
    between the short name of the engine plugin and the proper
    engine plugin object reference.
    """

    self.engines = engines

def set_json_plugin(self, json_plugin):
    """
    Sets the json plugin.

    @type json_plugin: Plugin
    @param json_plugin: The json plugin.
    """

    self.json_plugin = json_plugin

def _template(self, *args, **kwargs):
    """
    Override function that should be used to changed the default behavior
    of the method that retrieves (and sets) the template for each action
    operation with the provided values.
    """

    return self.template(*args, **kwargs)

def _get_attribute(self, request, attribute_name):
    """
    Retrieves an attribute from the request in a safe
    manner (casting it according to form data).

    @type request: Request
    @param request: The request to be used to retrieve the
    attribute.
    @type attribute_name: String
    @param attribute_name: The name of the attribute to be retrieved.
    @rtype: Object
    @return: The retrieved attribute (safely casted).
    """

    # retrieves the attribute value from the attribute
    # name and casts it (avoiding form data problems)
    attribute_value = request.get_attribute(attribute_name)
    attribute_value = self._cast_attribute_value(attribute_value)

    # returns the attribute value
    return attribute_value

def _cast_attribute_value(self, attribute_value):
    """
    "Casts" the attribute value in case the type
    of the attribute value is form data.
    This method provides a safe way to use the attribute
    value from the request.

    @type attribute_value: Object
    @param attribute_value: The value of the attribute
    to be "casted".
    @rtype: Object´
    @return: The attribute value, safely "casted".
    """

    # in case the attribute value is
    # not valid (or not set)
    if not attribute_value:
        # returns the attribute value
        # (immediately)
        return attribute_value

    # retrieves the attribute value type
    attribute_value_type = type(attribute_value)

    # in case the attribute value type is not
    # dictionary (map)
    if not attribute_value_type == types.DictionaryType:
        # returns the attribute value
        # (immediately)
        return attribute_value

    # in case the form data value is not defined
    # in the attribute value
    if not FORM_DATA_VALUE in attribute_value:
        # returns the attribute value
        return attribute_value

    # in case the filename does not exists in the
    # attribute value (normal field)
    if not FILENAME_VALUE in attribute_value:
        # returns the "contents" from the attribute
        # value (form data value)
        return attribute_value[CONTENTS_VALUE]

    # retrieves the filename and the contents
    # from the attribute to create the file attribute
    # tuple (filename and contents)
    filename = attribute_value[FILENAME_VALUE]
    contents = attribute_value[CONTENTS_VALUE]
    file_attribute_tuple = (filename, contents)

    # returns the file attribute tuple
    return file_attribute_tuple

def _get_path(self, request):
    """
    Retrieves the "real" path from the request
    this method takes into account the base path.
    In case a redirection is made by rules in the http
    server the "original" path is not the one present
    in the path attribute, in this situation the base
    path attribute must be used to retrieve the "real"
    path.

    @type request: Request
    @param request: The request to be used to
    retrieve the "real" url path.
    @rtype: String
    @return: The "original" base path from the http
    url, taking into account the base path. This value
    is "raw" so it means it's unquoted.
    """

    # retrieves the original path as the path from the request
    path = request.request.original_path

    # in case the (original) path is not valid (problem
    # in the request retrieval) the "processed" path
    # must be used as a fall-back
    if not path:
        # sets the request path as the path
        path = request.request.path

    # returns the path
    return path

def _get_host(self, request, prefix_path = None):
    """
    Retrieves the host for the current request prepended
    with the given prefix path.

    @type request: Request
    @param request: The request to be used.
    @type prefix_path: String
    @param prefix_path: The prefix path to be prepended to the
    host value.
    @rtype: String
    @return: The current host (name) for the given request.
    """

    # retrieves the host value from the request headers
    host = request.request.get_header(HOST_VALUE)

    # in case there is a prefix path defined
    if prefix_path:
        # prepends the prefix path to the host
        host = prefix_path + host

    # returns the host
    return host

def _get_host_path(self, request, suffix_path = "", prefix_path = HTTP_PREFIX_VALUE):
    """
    Retrieves the complete host path to the current request.

    @type request: Request
    @param request: The request to be used.
    @type suffix_path: String
    @param suffix_path: The suffix path to be appended.
    @type prefix_path: String
    @param prefix_path: The prefix path to be prepended.
    @rtype: String
    @return: The complete host path to the current request.
    """

    # tries retrieves the host value
    host = self._get_host(request)

    # in case no host is defined
    if not host:
        # raises the insufficient http information exception
        raise exceptions.InsufficientHttpInformation("no host value defined")

    # retrieves the path
    path = self._get_path(request)

    # removes the arguments part of the path
    path = path.split("?")[0]

    # creates the host path with the prefix path the host the first part
    # of the host split and the suffix path
    host_path = prefix_path + host + path.rsplit("/", 1)[0] + suffix_path

    # returns the host path
    return host_path

def _range_d(self, request, default):
    """
    Calculates the timestamp based date range for the provided
    request according to the specification.

    The calculation of the range taking into account that if
    only a "lower" value is filled the "upper" values are set
    with the current date related values (eg: if day one is
    specified the range is day one of the current month and year).

    The default argument may be used to control the default behavior
    in case no value is passed.

    This is the internal method and should not be used from
    an interface level.

    @type request: Request
    @param request: The request to be used for the
    computation of the date range.
    @type default: String
    @param default: The default mode to be used in case no value
    is retrieved from the request.
    @rtype: Tuple
    @return: Tuple containing the timestamps defining the date
    range defined in the request.
    """

    # retrieves the current date structure to be used as reference
    # for limit values that do not exist
    current = datetime.datetime.utcnow()

    # retrieves the various temporal values that are going to be
    # uses int the calculus of the time ranges
    year = self.get_field(request, "year", None, types.IntType)
    month = self.get_field(request, "month", None, types.IntType)
    day = self.get_field(request, "day", None, types.IntType)
    hour = self.get_field(request, "hour", None, types.IntType)
    start = self.get_field(request, "start", None, types.IntType)
    end = self.get_field(request, "end", None, types.IntType)

    # in case the start and end (timestamp values) are specified
    # the method should return immediately with their values
    if start and end: return start, end

    # verifies if the provided date is complete and in case it's
    # not populates the default values
    valid = not year == None or not month == None or\
        not day == None or not hour == None
    if not valid and default == "year": year = current.year
    if not valid and default == "month": month = current.month
    if not valid and default == "day": day = current.day
    if not valid and default == "hour": hour = current.hour

    # in case the provided date is not complete and the currently
    # selected default mode is all (complete range) the minimum
    # maximum timestamp values are returned
    if not valid and default == "all":
        return MIN_TIMESTAMP, MAX_TIMESTAMP

    # tries to verify (again) if the current sent argument define
    # a proper date in case they still don't raises an error
    valid = not year == None or not month == None or\
        not day == None or not hour == None
    if not valid: raise RuntimeError("No valid date range specified")

    # propagates the population of the default values in case the
    # upper values are not (with the current date values)
    if not hour == None: day = day or current.day
    if not day == None: month = month or current.month
    if not month == None: year = year or current.year

    # resets the various start values to their appropriate values
    # (note that the hour to be set is the first)
    hour_s = hour or 0
    day_s = day or 1
    month_s = month or 1
    year_s = year or 1

    # creates the start time value from the computed values and the
    # converts it into a valid timestamp value
    start = datetime.datetime(year_s, month_s, day_s, hour_s)
    start_tuple = start.utctimetuple()
    start_time = calendar.timegm(start_tuple)

    # in case the hour is defined the time is considered to be
    # hour based and is computed as such
    if not hour == None:
        end_time = start_time + 3600

    # in case the day is defined the time is considered to be
    # day based and is computed as such
    elif not day == None:
        end_time = start_time + 86400

    # in case the month is not defined the range is considered
    # to be the complete month and the last day of the month
    # should be used as reference for computation
    elif not month == None:
        month_range = calendar.monthrange(year_s, month_s)
        last_day = month_range[1]
        last = datetime.datetime(year, month, last_day)
        last_tuple = last.utctimetuple()
        last_time = calendar.timegm(last_tuple)
        end_time = last_time + 86400

    # in case the year is not defined the range is considered
    # to be the complete year and the first day of the next
    # year is considered the limit of the range
    elif not year == None:
        end = datetime.datetime(year_s + 1, month_s, day_s)
        end_tuple = end.utctimetuple()
        end_time = calendar.timegm(end_tuple)

    # returns a tuple containing both the start and end
    # time values to the calling method
    return start_time, end_time

def _parse_date(self, date_string_value):
    """
    Parses a string encoded in date format, converting it
    into a datetime object.

    @type date_string_value: String
    @param date_string_value: The date encoded string.
    @rtype: datetime
    @return: The date time object representing the string value.
    """

    # converts the date string value to a date time object
    date_time_value = datetime.datetime.strptime(date_string_value, DATE_FORMAT)

    # returns the date time value
    return date_time_value

def _parse_date_time(self, date_time_string_value):
    """
    Parses a string encoded in date time format, converting it
    into a datetime object.

    @type date_time_string_value: String
    @param date_time_string_value: The date time encoded string.
    @rtype: datetime
    @return: The date time object representing the string value.
    """

    # converts the date time string value to a date time object
    date_time_value = datetime.datetime.strptime(date_time_string_value, DATE_TIME_FORMAT)

    # returns the date time value
    return date_time_value

def _dasherize(self, string_value):
    """
    Converts a string value with multiple words in either camel case or
    separated by underscores to a dasherized notation, i.e., different
    words separated by dashes.

    @type string_value: String
    @param string_value: The string value to dasherize.
    @rtype: String
    @return: The dasherized string value.
    """

    # inserts underscore between changes of letter cases
    # for string value starting with capitals
    camel_cased_underscored_string_value = CAPITALIZED_CAMEL_CASED_WORD_PAIR_REGEX.sub(UNDERSCORED_WORD_PAIR_REPLACEMENT_VALUE, string_value)

    # inserts underscore between changes of letter cases
    # for string values starting with lower case
    camel_cased_underscored_string_value = CAMEL_CASED_WORD_PAIR_REGEX.sub(UNDERSCORED_WORD_PAIR_REPLACEMENT_VALUE, camel_cased_underscored_string_value)

    # replaces the non-character matches with dashes
    camel_case_dasherized_string_value = NON_CHARACTER_REGEX.sub(DASH_VALUE, camel_cased_underscored_string_value)

    # lowers the case of the string_value
    dasherized_string_value = camel_case_dasherized_string_value.lower()

    # returns the dasherized string_value
    return dasherized_string_value

def _dasherize_camel_cased(self, string_value):
    """
    Converts a string value with multiple words in camel case to
    a dasherized notation, i.e., different words separated by dashes.

    @type string_value: String
    @param string_value: The string value to dasherize, in camel case
    and without consecutive capitals.
    @rtype: String
    @return: The dasherized string value.
    """

    # inserts underscore between changes of letter cases
    # for string value starting with capitals
    camel_case_dasherized_string_value = CAMEL_CASED_WORD_PAIR_REGEX.sub(DASHED_WORD_PAIR_REPLACEMENT_VALUE, string_value)

    # lowers the case of the string_value
    dasherized_string_value = camel_case_dasherized_string_value.lower()

    # returns the dasherized string_value
    return dasherized_string_value

def _dasherize_underscored(self, string_value):
    """
    Converts a string value with multiple words in underscore case to
    a dasherized notation, i.e., different words separated by dashes.

    @type string_value: String
    @param string_value: The string value to dasherize, in underscore
    and without consecutive capitals.
    @rtype: String
    @return: The dasherized string value.
    """

    # replaces the underscores for dashes
    dasherized_string_value = string_value.replace(UNDERSCORE_VALUE, DASH_VALUE)

    # returns the dasherized value
    return dasherized_string_value

def _create_form_data(self, request, data_map, form_data_map_key, form_data_map, encoding):
    """
    Processes the data map, populating the form data map with all the
    attributes described in the form data format.

    @type request: Request
    @param request: The request to be used.
    @type data_map: Dictionary
    @param data_map: The map containing the hierarchy of defined structure
    for the "form" contents.
    @type form_data_map_key: String
    @param form_data_map_key: The prefix to all form data map keys,
    which is used to indicate the current context.
    @type form_data_map: Dictionary
    @param form_data_map: The map containing the data map's attributes
    in the form data format.
    @type encoding: String
    @param encoding: The encoding to be used when retrieving
    the attribute values.
    """

    # sets each attribute in the form data map
    for attribute_name in data_map:
        # retrieves the attribute value
        attribute_value = data_map[attribute_name]

        # retrieves the attribute value type
        attribute_value_type = type(attribute_value)

        # retrieves the form data map key format
        form_data_map_key_format = attribute_value_type in (types.ListType, types.TupleType) and FORM_DATA_LIST_KEY_FORMAT or FORM_DATA_MAP_KEY_FORMAT

        # retrieves the attribute form data map key
        attribute_form_data_map_key = form_data_map_key_format % (form_data_map_key, attribute_name)

        # initializes the new form data attribute value
        new_form_data_attribute_value = None

        # invokes this same function recursively
        # in case the attribute value is a map
        if attribute_value_type == types.DictType:
            self._create_form_data(request, attribute_value, attribute_form_data_map_key, form_data_map, encoding)
        # invokes this same function recursively for each
        # item in case the attribute value is a list
        elif attribute_value_type in (types.ListType, types.TupleType):
            for attribute_value_item in attribute_value:
                self._create_form_data(request, attribute_value_item, attribute_form_data_map_key, form_data_map, encoding)
        # decodes the attribute value and sets it
        # in the form data map in case it is a unicode string
        elif attribute_value_type == types.UnicodeType:
            # encodes the attribute value
            new_form_data_attribute_value = attribute_value.encode(encoding)
        # otherwise converts the attribute value to
        # a string and sets it in the form data map
        else:
            # converts the attribute value to a string
            new_form_data_attribute_value = str(attribute_value)

        # in case the new form data attribute value was not set
        if new_form_data_attribute_value == None:
            # continues to the next attribute
            continue

        # sets the new form data attribute value in the form
        # data map, taking into account that if one or more
        # values already exist for that key, a list should
        # be created with these values and the new value
        # and set in the form data map
        form_data_attribute_value = form_data_map.get(attribute_form_data_map_key, None)
        form_data_attribute_value_type = type(form_data_attribute_value)
        form_data_attribute_value = not form_data_attribute_value_type in (types.ListType, types.NoneType) and [form_data_attribute_value] or form_data_attribute_value
        form_data_attribute_value = form_data_attribute_value and form_data_attribute_value + [new_form_data_attribute_value] or new_form_data_attribute_value
        form_data_map[attribute_form_data_map_key] = form_data_attribute_value

def _process_form_attribute_flat(self, parent_structure, attribute_names_list, attribute_value):
    """
    Processes a form attribute using the sent parent structure and for the
    given attribute names list
    At the end the parent structure is changed and contains the form
    attribute in the correct structure place.

    @type parent_structure: Dictionary
    @param parent_structure: The parent structure to be used to set the
    attribute.
    @type attribute_names_list: List
    @param attribute_names_list: The list of attribute names currently
    being parsed.
    @type attribute_value: Object
    @param attribute_value: The attribute value.
    """

    # retrieves the current attribute name from the attribute names list
    current_attribute_name = attribute_names_list.pop()

    # in case the attribute names list is empty
    if not attribute_names_list:
        # sets the attribute value in the parent structure
        parent_structure[current_attribute_name] = attribute_value

        # returns immediately
        return

    # in case the current attribute name is not defined in the parent structure,
    # a dictionary should be defined in the parent structure for the current attribute name
    if not current_attribute_name in parent_structure:
        # creates a new dictionary for the current attribute name in
        # the parent structure
        parent_structure[current_attribute_name] = {}

    # retrieves the "next" parent structure from the current one
    # accessing the current attribute value in the parent structure
    next_parent_structure = parent_structure[current_attribute_name]

    # retrieves the next parent structure value type
    next_parent_structure_type = type(next_parent_structure)

    # in case the next parent structure is not of type dictionary
    if not next_parent_structure_type == types.DictType:
        # creates a new next parent structure map
        next_parent_structure = {}

        # set the current attribute name with an "escaped" name
        # and associates it with the "new" next parent structure
        parent_structure[UNDERSCORE_VALUE + current_attribute_name] = next_parent_structure

    # processes the form attribute in flat mode for the next parent structure,
    # the attribute names list and the attribute value
    self._process_form_attribute_flat(next_parent_structure, attribute_names_list, attribute_value)

def _process_form_attribute(self, parent_structure, current_attribute_name, attribute_value, index = 0):
    """
    Processes a form attribute using the sent parent structure and for
    the given index as a reference.
    At the end the parent structure is changed and contains the form
    attribute in the correct structure place.

    @type parent_structure: List/Dictionary
    @param parent_structure: The parent structure to be used to set the
    attribute.
    @type current_attribute_name: String
    @param current_attribute_name: The current attribute name, current
    because it's parsed
    recursively using this process method.
    @type attribute_value: Object
    @param attribute_value: The attribute value.
    @type index: int
    @param index: The index of the current attribute reference.
    """

    # retrieves the current match for the current attribute
    # and in case no valid match is found raises an exception indicating
    # the invalid match problem
    match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name)
    if not match_result:
        raise exceptions.InvalidAttributeName("invalid match value: " + current_attribute_name)

    # retrieves the match end position and verifies if it
    # matches the length of the current attribute for such
    # case the attribute is considered to be the last one
    match_end = match_result.end()
    is_last_attribute_name = match_end == len(current_attribute_name)

    # retrieves the (current) match name and value
    match_name = match_result.lastgroup
    match_value = match_result.group()

    # in case the match value is of type map
    # the parentheses need to be removed from it
    if match_name == MAP_TYPE_VALUE: match_value = match_value[1:-1]

    # in case it's the only (last) match available
    if is_last_attribute_name:
        # in case the match is of type name, must
        # set the attribute value in the parent structure
        if match_name == NAME_TYPE_VALUE:
            parent_structure[match_value] = attribute_value
        # in case the match is of type sequence, adds
        # the attribute value to the parent structure
        elif match_name == SEQUENCE_TYPE_VALUE:
            parent_structure.append(attribute_value)
        # in case the match is of type map, sets the
        # attribute value in the parent structure
        elif match_name == MAP_TYPE_VALUE:
            parent_structure[match_value] = attribute_value

    # there is more parsing to be made
    else:
        # retrieves the next match value in order to make
        next_match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name, match_end)

        # in case there is no next match
        if not next_match_result:
            # raises the invalid attribute name exception
            raise exceptions.InvalidAttributeName("invalid next match value: " + current_attribute_name)

        # retrieves the next match name and value to be used
        # for conditional execution
        next_match_name = next_match_result.lastgroup
        next_match_value = next_match_result.group()

        # in case the next match value is of type map
        # the parentheses need to be removed
        if next_match_name == MAP_TYPE_VALUE:
            # retrieves the next match value without the parentheses
            next_match_value = next_match_value[1:-1]

        # in case the next match is of type name
        if next_match_name == NAME_TYPE_VALUE:
            # raises the invalid attribute name exception
            raise exceptions.InvalidAttributeName("invalid next match value (it's a name): " + current_attribute_name)
        # in case the next match is of type list, a list needs to
        # be created in order to support the sequence, in case a list
        # already exists it is used instead
        elif next_match_name == SEQUENCE_TYPE_VALUE:
            # in case the match value exists in the
            # parent structure there is no need to create a new structure
            # the previous one should be used
            if match_value in parent_structure:
                # sets the current attribute value as the value that
                # exists in the parent structure
                current_attribute_value = parent_structure[match_value]
            # otherwise no structure exists and must be created
            # to set new values
            else:
                # creates a new list structure
                current_attribute_value = []
        # in case the next match is of type map, a map needs to
        # be created in order to support the mapping structure, in case a map
        # already exists it is used instead
        elif next_match_name == MAP_TYPE_VALUE:
            # in case the current match is a sequence
            # it's required to check for the valid structure
            # it may be set or it may be a new structure depending
            # on the current "selected" index
            if match_name == SEQUENCE_TYPE_VALUE:
                # retrieves the parent structure length
                parent_structure_length = len(parent_structure)

                # in case the parent structure length is
                # not sufficient to hold the the elements
                if parent_structure_length <= index:
                    # creates a new map structure
                    current_attribute_value = {}
                else:
                    # sets the current attribute value as the structure
                    # in the current "selected" index
                    current_attribute_value = parent_structure[index]
            # in case the match value exists in the
            # parent structure there is no need to create a new structure
            # the previous one should be used
            elif match_value in parent_structure:
                # sets the current attribute value as the value that
                # exists in the parent structure
                current_attribute_value = parent_structure[match_value]
            else:
                # creates a new map structure
                current_attribute_value = {}

        # in case the match is of type name (first match)
        if match_name == NAME_TYPE_VALUE:
            # sets the current attribute value in the parent structure
            parent_structure[match_value] = current_attribute_value
        # in case the match is of type sequence
        elif match_name == SEQUENCE_TYPE_VALUE:
            # retrieves the parent structure length
            parent_structure_length = len(parent_structure)

            # in case the current attribute value is meant
            # to be added to the parent structure
            if parent_structure_length <= index:
                # adds the current attribute value to the
                # parent structure
                parent_structure.append(current_attribute_value)
        # in case the match is of type map
        elif match_name == MAP_TYPE_VALUE:
            # sets the current attribute value in the parent structure
            parent_structure[match_value] = current_attribute_value

        # retrieves the remaining attribute name
        remaining_attribute_name = current_attribute_name[match_end:]

        # processes the next form attribute with the current attribute value as the new parent structure
        # the remaining attribute name as the new current attribute name and the attribute value
        # continues with the same value
        self._process_form_attribute(current_attribute_value, remaining_attribute_name, attribute_value, index)

def _get_complete_session_attribute_name(session_attribute_name, namespace_name = None):
    """
    Retrieves the complete session attribute name from the session
    attribute name and the namespace name.

    @type session_attribute_name: String
    @param session_attribute_name: The session attribute name.
    @type namespace_name: String
    @param namespace_name: The namespace name.
    @rtype: String
    @return: The complete session attribute name.
    """

    # in case the namespace name is not set
    if not namespace_name:
        # returns the "original" session attribute name
        # as the complete session attribute name
        return session_attribute_name

    # creates the complete session attribute name by prepending the namespace
    # name to the session attribute name
    complete_session_attribute_name = namespace_name + "." + session_attribute_name

    # returns the complete session attribute name
    return complete_session_attribute_name

def _set_entity_attribute(self, attribute_key, attribute_value, entity, entity_model, nullify):
    """
    Sets the given entity attribute for the given attribute key and value.
    The entity to set the attribute is the instance of the entity model
    also sent.

    @type attribute_key: String
    @param attribute_key: The attribute key in the entity.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to set.
    @type entity: EntityModel
    @param entity: The entity to have the attribute set.
    @type entity_model: Class
    @param entity_model: The entity model of the entity to have
    the attribute set.
    @type nullify: bool
    @param nullify: If the data to be processed should be nullified
    in case empty string values are found.
    """

    # in case the entity model does not contain the attribute
    # to be set, the setting must be avoided
    if not hasattr(entity_model, attribute_key):
        # returns immediately (avoids, possible corruption
        # of the entity model)
        return

    # retrieves the entity model attribute value
    entity_model_attribute_value = getattr(entity_model, attribute_key)

    # retrieves the data type from the entity model attribute value
    data_type = entity_model_attribute_value[DATA_TYPE_VALUE]

    # retrieves the cast type for the data type
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

    # sets the attribute value casted in the entity
    setattr(entity, attribute_key, attribute_value_casted)

def _validate_relation_value(self, relation_value):
    """
    Validates the given (entity) relation value, checking
    if it is a valid relation value.

    @type relation_value: Object
    @param relation_value: The relation value to be checked.
    @rtype: bool
    @return: The result of the validation test.
    """

    # in case the relation value is valid and
    # the relation value is not lazy loaded
    if relation_value and not relation_value == "%lazy-loaded%":
        # returns true (valid)
        return True
    # otherwise it must be invalid
    else:
        # returns false (invalid)
        return False

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

    # in case the value is none it's a special
    # case (type) and must return immediately
    if value == None: return value

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

def _convert_entity_map(self, entity):
    """
    Converts the given entity object into a map, representing
    it (for get saving usage).
    This conversion is very useful for method that want to be
    proof to entity arguments instead of map.

    @type entity: Entity
    @param entity: The entity to be converted into a map of
    attribute representing it.
    @rtype: Dictionary
    @return: The map representing the given entity.
    """

    # in case the entity object does not contain
    # the dict attribute
    if not hasattr(entity, "__dict__"):
        # raises a runtime error (no dict attribute found)
        raise RuntimeError("invalid entity object, no __dict__ attribute found")

    # creates the map that will hold all the values
    # "extracted" from the entity
    values_map = {}

    # iterates over all the keys and values from the
    # entity (object) to set the value in the map
    for key, value in entity.__dict__.items():
        # in case the key refers an excluded attribute
        # (no need to persist it in the values map)
        if key in ATTRIBUTE_EXCLUSION_LIST:
            # continues the loop
            continue

        # retrieves the type from the value to evaluate
        # the possible value for it
        value_type = type(value)

        # in case the type of the value is list
        # (this is a to many relation and all the
        # element must be converted)
        if value_type == types.ListType:
            # creates the list to hold the various
            # converted value
            values_list = []

            # iterates over all the value contained
            # in the value element
            for _value in value:
                # converts the value item into a map
                # representation and adds it to the
                # list of values
                _value = self._convert_entity_map(_value)
                values_list.append(_value)

            # sets the value list as the value
            value = values_list
        # in case the value is of type instance or contains
        # the dict attribute, it must be an entity reference
        elif value_type == types.InstanceType or hasattr(value, "__dict__"):
            # converts the entity into map representation and
            # sets it as the value
            value = self._convert_entity_map(value)
        # in case the value is lazy loaded (must avoid
        # setting the attribute, possible problems)
        elif value == "%lazy-loaded%":
            # continues the loop (no need to set
            # a lazy loaded relation)
            continue

        # sets the value in the values map
        values_map[key] = value

    # returns the values map
    return values_map

def _process_file_path_locale(
    self,
    file_path,
    locale = None,
    base_path = None,
    separator = ".",
    fallback = "_"
):
    """
    Processes the given file path according to the given locale.
    This will change the provided file path into a locale version
    of it taking into account the provided parameter value.

    The optional separator value controls the separator character
    that will be used to separate the base file name from the locale
    version string.

    A possible fallback value may be provided so that if the file
    name with the requested separator does not exists a new try
    is done with the fallback value as the separator.

    In case no locale is given the original file path is returned.

    @type file_path: String
    @param file_path: The file path to be processed.
    @type locale: String
    @param locale: The locale to be used for file path processing,
    this value should conform with the current locale standards.
    @type separator: String
    @param separator: The  string containing the characters that will
    be used to separate the base name of the file from the locale part.
    @type fallback: String
    @param fallback: Text value containing the value that will be used
    as the separator in case it's not possible to find the file path
    resulting from the first try.
    @rtype: String
    @return: The processed file path, conforming with the proper
    localized version of the file path.
    """

    # in case no locale is defined, there's no need for any extra
    # processing of the file path and so the proper file path is
    # returns to the caller method as the template file path
    if not locale: return file_path

    # verifies if the current execution is from the fallback operation
    # this occurs when the separator value is the same as the fallback
    # value and should represent the second execution of this method
    is_fallback = separator == fallback

    # converts the locale value into a lower cased value that is going
    # to be appended to the file name for locale retrieval
    locale_lower = self._lower_locale(locale)

    # splits the file path to retrieve the base file path (directory)
    # and the (proper) file name to split it around the first dot and
    # for one time only, this is the base value of the name
    base_file_path, file_name = os.path.split(file_path)
    file_name_splitted = file_name.split(".", 1)

    # creates the locale string value from the locale lower value by
    # appending the locale lower value to the current string and adding
    # it to the splitted string list (to be latter joined)
    locale_string_value = separator + locale_lower + "."
    file_name_splitted.insert(1, locale_string_value)

    # re-joins the file name back to create the new file name that should
    # represent the localized version of the file name
    file_name = "".join(file_name_splitted)

    # joins the base file path with the (new) file (localized) name creating
    # the fully localized path and normalizes it, then in case the base path
    # is defined joins the base path with the locale path to create the full
    # path to the localized path that may be used for existence verification
    locale_path = os.path.join(base_file_path, file_name)
    locale_path = os.path.normpath(locale_path)
    full_path = os.path.join(base_path, locale_path) if base_path else locale_path

    # verifies if the localized file exists in the file system and in case it
    # does not and this is not (already) the fallback call tries to run the
    # fallback call, meaning that the separator value is changed with the fallback
    # value so that it may try to find the file using a different localization
    # of naming strategy (auto fail over)
    exists = os.path.exists(full_path)
    should_fall = not exists and not is_fallback
    if should_fall:
        locale_path = self._process_file_path_locale(
            file_path,
            locale = locale,
            base_path = base_path,
            separator = fallback,
            fallback = fallback
        )

    # returns the resulting locale path to the caller method so that it may be
    # used inside localization contexts (templates localization support)
    return locale_path

def _lower_locale(self, locale):
    """
    Converts the given locale string value
    to the lower version of it.

    @type locale: String
    @param locale: The lower locale string value to
    be converted.
    @rtype: String
    @return: The lower locale string value.
    """

    # converts the locale to lower
    locale_lower = locale.lower()

    # replaces the slashes with underscores
    locale_lower = locale_lower.replace("-", "_")

    # returns the locale lower (value)
    return locale_lower

def _get_locales_session(self, request):
    """
    Retrieves the locales list value using a
    request session strategy.

    @type request: Request
    @param request: The request to be used.
    @rtype: List
    @return: The retrieved locales list.
    """

    # retrieves the accepted language
    locale = self.get_session_attribute(request, LOCALE_SESSION_ATTRIBUTE)

    # creates the locales list
    locales_list = locale and [locale] or []

    # returns the locales list
    return locales_list

def _get_locales_header(self, request):
    """
    Retrieves the locales list value using an
    (http) header strategy.

    @type request: Request
    @param request: The request to be used.
    @rtype: List
    @return: The retrieved locales list.
    """

    # retrieves the accepted language
    accept_language = request.get_header(ACCEPT_LANGUAGE_VALUE)

    # retrieves the locales map for the accept language
    locales_map = self._get_locales_map(accept_language)

    # retrieves the locales list ordered by value in reverse
    locales_list = sorted(locales_map, key = locales_map.__getitem__, reverse = True)

    # returns the locales list
    return locales_list

def _get_locales_default(self, request):
    """
    Retrieves the locales list value using a
    default strategy.

    @type request: Request
    @param request: The request to be used.
    @rtype: List
    @return: The retrieved locales list.
    """

    return (
        DEFAULT_LOCALE,
    )

def _get_locales_map(self, accept_language):
    """
    Given am accept language header value, this
    method converts the values into a map of locale
    key and relative value value.

    @type accept_language: String
    @param accept_language: The accept language header value.
    @rtype: Dictionary
    @return: The map locales for the given language
    header value.
    """

    # creates the locales map
    locales_map = {}

    # in case accept language is invalid, returns the
    # locales map immediately (fallback behavior)
    if not accept_language: return locales_map

    # marches the accept language value, retrieving the match iterator
    accept_language_match_iterator = LOCALE_REGEX.finditer(accept_language)

    # iterates over all the accept language matches (iterator)
    for accept_language_match in accept_language_match_iterator:
        # retrieves the values from the accept language match
        locale = accept_language_match.group(LOCALE_VALUE)
        relative_value = accept_language_match.group(RELATIVE_VALUE_VALUE)

        # converts the locale to its lower case representation
        # so that it's normalized for a normalized value
        locale_lower = self._lower_locale(locale)

        # retrieves the relative value in float mode
        relative_value_float = relative_value == None and 1.0 or float(relative_value)

        # sets the locale lower value in the locales map
        locales_map[locale_lower] = relative_value_float

    # returns the locales map
    return locales_map

def _get_bundle(self, locale, bundle_name = "global"):
    """
    Retrieves the locale bundle for the provided locale and
    bundle name, in case the bundle name is not provided the
    global bundle is retrieved.

    The retrieval of the bundle implies the loading of the
    serialized file, so this is considered to be an expensive
    operation (should be used carefully).

    @type locale: String
    @param locale: The locale name to retrieve the bundle, this
    value must be encoded in bcp47 in the underline notation (eg:
    pt_pt or en_us).
    @type bundle_name: String
    @param bundle_name: The name of the bundle to be retrieved this
    is goind to be used in the creation of the bundle file path.
    @rtype: Dictionary
    @return: The map containing the bundle with the loaded values
    from the bundle file.
    """

    # in case the pretended locale is not defined
    # the function returns immediately (fails silently)
    if not locale: return

    # constructs the bundle path from the locales path and
    # the expected bundle name (assumes json type), in such
    # path does not exists returns immediately
    bundle_path = os.path.join(self.locales_path, bundle_name + "_" + locale + ".json")
    if not os.path.exists(bundle_path): return

    # retrieves the last modified timestamp from the bundle path
    # and uses it to try to retrieve the bundle from the data
    # cache map created for the purpose (fast retrieval)
    bundle_timestamp = os.path.getmtime(bundle_path)
    bundle = bundle_cache.get(bundle_path, bundle_timestamp)
    if bundle: return bundle

    # opens the bundle file for reading of its contents
    # after the reading they will be processed as json
    bundle_file = open(bundle_path, "rb")

    try:
        # reads the bundle file contents and loads them
        # as json information, (map) decoding it using
        # the default encoding (utf-8)
        bundle_contents = bundle_file.read()
        bundle_contents = bundle_contents.decode(DEFAULT_ENCODING)
        bundle = self.json_plugin.loads(bundle_contents)
    finally:
        # closes the bundle file (no more reading to be
        # done on the bundle file)
        bundle_file.close()

    # adds the bundle to the cache map using the last retrieved
    # timestamp and the parsed bundle json data, this will allow
    # the next retrieval to be done through the cache system
    bundle_cache.add(bundle_path, bundle, bundle_timestamp)

    # returns the "just" loaded bundle, for later usage
    # this should be a "simple" key value map
    return bundle

def get_process_method(controller, request, process_method_name):
    """
    Retrieves the "real" process method from the given
    process method name.

    @type controller: Controller
    @param controller: The controller associated with the
    current context.
    @type request: Request
    @param request: The current request.
    @type process_method_name: String
    @param process_method_name: The name of the process
    method to be retrieved.
    @rtype: Method
    @return: The "real" process method from the given
    process method name.
    """

    def __process_stylesheet_link(self, node):
        # retrieves the extras path from the controller
        extras_path = controller.get_extras_path()

        # retrieves the css path from the controller
        css_path = os.path.join(extras_path, "css")

        # retrieves the css path items
        css_path_items = os.listdir(css_path)

        # iterates over all the css path items
        for css_path_item in css_path_items:
            # splits the item into base and extension
            _item_base, item_extension = os.path.splitext(css_path_item)

            # in case the item extension is not a valid
            # one (representing a stylesheet) must continue
            # with the current loop to find the next valid item
            if not item_extension == ".css": continue

            # adds the stylesheet reference to the string buffer
            self.string_buffer.write("<link rel=\"stylesheet\" href=\"resources/css/%s\" type=\"text/css\" />\n" % css_path_item)

    def __process_javascript_include(self, node):
        # retrieves the extras path from the controller
        extras_path = controller.get_extras_path()

        # retrieves the js path from the controller
        js_path = os.path.join(extras_path, "js")

        # retrieves the js path items
        js_path_items = os.listdir(js_path)

        # iterates over all the js path items
        for js_path_item in js_path_items:
            # splits the item into base and extension
            _item_base, item_extension = os.path.splitext(js_path_item)

            # in case the item extension is not
            if not item_extension == ".js":
                # continues the loop
                continue

            # adds the javascript reference to the string buffer
            self.string_buffer.write("<script type=\"text/javascript\" src=\"resources/js/%s\"></script>\n" % js_path_item)

    def __process_ifacl(self, node):
        # retrieves the attributes map
        attributes = node.get_attributes()

        # retrieves the attribute permission value
        attribute_permission = attributes[PERMISSION_VALUE]
        attribute_permission_value = self.get_literal_value(attribute_permission)

        # verifies if the value attribute exists in the attributes map
        # if that's the case retrieves its value (should be an integer)
        # as the value that is going to be used for comparison
        if VALUE_VALUE in attributes:
            attribute_value = attributes[VALUE_VALUE]
            attribute_value_value = self.get_value(attribute_value)

        # otherwise the default value is set this is considered to be the
        # most common usage of the ifacl predicate
        else: attribute_value_value = 10

        # in case the session attribute exists in the attributes map
        # must retrieve it and parse it as a literal value
        if SESSION_ATTRIBUTE_VALUE in attributes:
            attribute_session_attribute = attributes[SESSION_ATTRIBUTE_VALUE]
            attribute_session_attribute_value = self.get_literal_value(attribute_session_attribute)

        # otherwise the default value should be used as no explicit
        # session attribute value was defined (fallback operation)
        else: attribute_session_attribute_value = DEFAULT_SESSION_ATTRIBUTE

        # retrieves the user acl value
        user_acl = controller.get_session_attribute(request, attribute_session_attribute_value) or {}

        # process the acl values, retrieving the permissions value
        permissions = controller.process_acl_values((user_acl, ), attribute_permission_value)

        # sets the initial accept node value
        accept_node = permissions <= attribute_value_value

        # in case the visit child is set
        if self.visit_childs:
            # iterates over all the node child nodes
            for node in node.children:
                # validates the accept node using the node child node
                # and the accept node
                accept_node = self._validate_accept_node(node, accept_node)

                # in case the accept node is set to invalid
                # the evaluation is over
                if accept_node == None: return

                # in case the accept node flag is set
                # accepts the node child node
                accept_node and node.accept(self)

    def __process_ifaclp(self, node):
        # retrieves the attributes map
        attributes = node.get_attributes()

        # retrieves the attribute permission value
        attribute_permission = attributes[PERMISSION_VALUE]
        attribute_permission_value = self.get_value(attribute_permission)

        # verifies if the value attribute exists in the attributes map
        # if that's the case retrieves its value (should be an integer)
        # as the value that is going to be used for comparison
        if VALUE_VALUE in attributes:
            attribute_value = attributes[VALUE_VALUE]
            attribute_value_value = self.get_value(attribute_value)

        # otherwise the default value is set this is considered to be the
        # most common usage of the ifacl predicate
        else: attribute_value_value = 10

        # in case the session attribute exists in the attributes map
        # must retrieve it and parse it as a literal value
        if SESSION_ATTRIBUTE_VALUE in attributes:
            attribute_session_attribute = attributes[SESSION_ATTRIBUTE_VALUE]
            attribute_session_attribute_value = self.get_literal_value(attribute_session_attribute)

        # otherwise the default value should be used as no explicit
        # session attribute value was defined (fallback operation)
        else: attribute_session_attribute_value = DEFAULT_SESSION_ATTRIBUTE

        # retrieves the user acl value
        user_acl = controller.get_session_attribute(request, attribute_session_attribute_value) or {}

        # process the acl values, retrieving the permissions value
        permissions = controller.process_acl_values((user_acl, ), attribute_permission_value)

        # sets the initial accept node value
        accept_node = permissions <= attribute_value_value

        # in case the visit child is set
        if self.visit_childs:
            # iterates over all the node child nodes
            for node in node.children:
                # validates the accept node using the node child node
                # and the accept node
                accept_node = self._validate_accept_node(node, accept_node)

                # in case the accept node is set to invalid
                # the evaluation is over
                if accept_node == None: return

                # in case the accept node flag is set
                # accepts the node child node
                accept_node and node.accept(self)

    def __process_ifnotacl(self, node):
        # retrieves the attributes map
        attributes = node.get_attributes()

        # retrieves the attribute permission value
        attribute_permission = attributes[PERMISSION_VALUE]
        attribute_permission_value = self.get_literal_value(attribute_permission)

        # retrieves the attribute value value
        attribute_value = attributes[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        # verifies if the value attribute exists in the attributes map
        # if that's the case retrieves its value (should be an integer)
        # as the value that is going to be used for comparison
        if VALUE_VALUE in attributes:
            attribute_value = attributes[VALUE_VALUE]
            attribute_value_value = self.get_value(attribute_value)

        # otherwise the default value is set this is considered to be the
        # most common usage of the ifacl predicate
        else: attribute_value_value = 10

        # in case the session attribute exists in the attributes map
        # must retrieve it and parse it as a literal value
        if SESSION_ATTRIBUTE_VALUE in attributes:
            attribute_session_attribute = attributes[SESSION_ATTRIBUTE_VALUE]
            attribute_session_attribute_value = self.get_literal_value(attribute_session_attribute)

        # otherwise the default value should be used as no explicit
        # session attribute value was defined (fallback operation)
        else: attribute_session_attribute_value = DEFAULT_SESSION_ATTRIBUTE

        # retrieves the user acl value
        user_acl = controller.get_session_attribute(request, attribute_session_attribute_value) or {}

        # process the acl values, retrieving the permissions value
        permissions = controller.process_acl_values((user_acl, ), attribute_permission_value)

        # sets the initial accept node value
        accept_node = permissions > attribute_value_value

        # in case the visit child is set
        if self.visit_childs:
            # iterates over all the node child nodes
            for node in node.children:
                # validates the accept node using the node child node
                # and the accept node
                accept_node = self._validate_accept_node(node, accept_node)

                # in case the accept node is set to invalid
                # the evaluation is over
                if accept_node == None: return

                # in case the accept node flag is set
                # accepts the node child node
                accept_node and node.accept(self)

    def __process_request_time(self, node):
        # retrieves the current time to be able to calculate
        # the delta, then calculates the delta by subtracting
        # the generation time of the request from the
        # current time (delta calculation)
        current_time = time.time()
        delta_time = current_time - request._generation_time

        # converts the delta time (currently in seconds) to
        # milliseconds (by multiplying by a thousand)
        delta_time *= 1000

        # writes the request time (in milliseconds) to the
        # string buffer (output operation)
        self.string_buffer.write("%i" % delta_time)

    # creates the complete process method name
    complete_process_method_name = "__" + process_method_name

    # retrieves the local symbols list
    local_symbols = locals()

    # retrieves the process method from the local symbols
    process_method = local_symbols.get(complete_process_method_name, None)

    # returns the process method
    return process_method

# creates the various methods that are going to be used for
# the logging capabilities, this methods are "just" pipelined
# calls the to the plugin instance associated with the controller
def debug(self, message): self.plugin.debug(message)
def info(self, message): self.plugin.info(message)
def warning(self, message): self.plugin.warning(message)
def error(self, message): self.plugin.error(message)
def critical(self, message): self.plugin.critical(message)
