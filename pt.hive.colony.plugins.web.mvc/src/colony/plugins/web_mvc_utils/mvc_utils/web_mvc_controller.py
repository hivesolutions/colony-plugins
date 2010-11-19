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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
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

import re
import types
import datetime

import web_mvc_utils_exceptions

DEFAULT_CONTENT_TYPE = "text/html;charset=utf-8"
""" The default content type """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

DEFAULT_TEMPLATE_FILE_ENCODING = "Cp1252"
""" The default template file encoding """

HTTP_PREFIX_VALUE = "http://"
""" The http prefix value """

HTTPS_PREFIX_VALUE = "https://"
""" The https prefix value """

DATE_FORMAT = "%Y/%m/%d"
""" The date format """

DATE_TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
""" The date time format """

BASE_PATH_VALUE = "base_path"
""" The base path value """

BACK_PATH_VALUE = "../"
""" The back path value """

DATA_TYPE_VALUE = "data_type"
""" The data type value """

NAME_TYPE_VALUE = "name"
""" The name type value """

SEQUENCE_TYPE_VALUE = "sequence"
""" The sequence type value """

MAP_TYPE_VALUE = "map"
""" The map type value """

HOST_VALUE = "Host"
""" The host value """

DASHED_WORD_PAIR_REPLACEMENT_VALUE = "\\1-\\2"
""" The replacement value for two capture groups to be separated by dash """

UNDERSCORED_WORD_PAIR_REPLACEMENT_VALUE = "\\1_\\2"
""" The replacement value for two capture groups to be separated by underscore """

DASH_VALUE = "-"
""" The dash value """

UNDERSCORE_VALUE = "_"
""" The underscore value """

ATTRIBUTE_PARSING_REGEX_VALUE = "(?P<name>[\w]+)|(?P<sequence>\[\])|(?P<map>\[\w+\])"
""" The attribute parsing regular expression value """

CAPITALIZED_CAMEL_CASED_WORD_PAIR_REGEX_VALUE = "([A-Z]+)([A-Z][a-z])"
""" The capitalized camel cased word pair regex value """

CAMEL_CASED_WORD_PAIR_REGEX_VALUE = "([a-z\d])([A-Z])"
""" The camel cased word pair regex value """

NON_CHARACTER_REGEX_VALUE = "[^A-Z^a-z^0-9^\/]+"
""" The non-character regex value """

ATTRIBUTE_PARSING_REGEX = re.compile(ATTRIBUTE_PARSING_REGEX_VALUE)
""" The attribute parsing regex """

CAPITALIZED_CAMEL_CASED_WORD_PAIR_REGEX = re.compile(CAPITALIZED_CAMEL_CASED_WORD_PAIR_REGEX_VALUE)
""" The capitalized camel cased word pair regex """

CAMEL_CASED_WORD_PAIR_REGEX = re.compile(CAMEL_CASED_WORD_PAIR_REGEX_VALUE)
""" The camel cased word pair regex """

NON_CHARACTER_REGEX = re.compile(NON_CHARACTER_REGEX_VALUE)
""" The non-character regex """

DATA_TYPE_CAST_TYPES_MAP = {"text" : str, "numeric" : int, "integer" : int, "float" : float, "date" : datetime, "relation" : None}
""" The map associating the data types with the cast types """

def _start_controller(self):
    """
    Starts the controller structures.
    """

    # in case the controller has the start method
    if hasattr(self, "start"):
        # calls the start method
        # in the controller
        self.start()

def get_entity_model(self, entity_manager, entity_model, update_values_map = {}, create_values_map = {}, secure_value_keys_list = None):
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
    @rtype: EntityModel
    @return: The retrieved entity model.
    """

    # unsets the created entity flag
    created_entity = False

    # retrieves the id attribute name (key)
    id_key = entity_manager.get_entity_class_id_attribute_name(entity_model)

    # tries to retrieves the entity model id
    entity_model_id = update_values_map.get(id_key, None)

    # in case the entity model id is defined
    if entity_model_id:
        # retrieves the entity model id value
        entity_model_id_value = getattr(entity_model, id_key)

        # retrieves the entity model id data type
        entity_model_id_data_type = entity_model_id_value[DATA_TYPE_VALUE]

        # retrieves the cast type for the data type
        cast_type = DATA_TYPE_CAST_TYPES_MAP[entity_model_id_data_type]

        # casts the entity model is using the safe mode
        entity_model_id_casted = self._cast_safe(entity_model_id, cast_type, -1)

        # retrieves the entity
        entity = entity_manager.find(entity_model, entity_model_id_casted)

        # in case the entity is not defined
        if not entity:
            # sets the created entity flag
            created_entity = True

            # creates a new entity from the entity
            # model (creates instance)
            entity = entity_model()

            # sets the id in the entity
            setattr(entity, id_key, entity_model_id)
    # otherwise a new entity should be
    # created
    else:
        # sets the created entity flag
        created_entity = True

        # creates a new entity from the entity
        # model
        entity = entity_model()

    # in case the entity was created
    if created_entity:
        # iterates over all the create values items
        for create_value_key, create_value_value in create_values_map.items():
            # sets the create value in the entity
            self._set_entity_attribute(create_value_key, create_value_value, entity, entity_model)

    # iterates over all the update values items
    for update_value_key, update_value_value in update_values_map.items():
        # in case the secure value keys list is valid and the update
        # value key does not exist in the secure value keys list
        if secure_value_keys_list and not update_value_key in secure_value_keys_list:
            # continues the loop
            continue

        # sets the update value in the entity
        self._set_entity_attribute(update_value_key, update_value_value, entity, entity_model)

    # returns the entity
    return entity

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

    # validates the model retrieving the result of the validation
    model_valid = model.validate()

    # raises an exception in case the model is not valid
    if not model_valid:
        # retrieves the model validation errors map
        model_validation_errors_map = model.validation_errors_map

        # raises the model validation error
        raise web_mvc_utils_exceptions.ModelValidationError(exception_message + ": " + str(model_validation_errors_map), model)

def send_broadcast_communication_message(self, parameters, connection_name, message):
    """
    Sends a broadcast message to all the clients in the connection
    with the given name.
    The mvc communication system is used for the broadcast sending.

    @type parameters: Dictionary
    @param parameters: A dictionary of parameters.
    @type connection_name: String
    @param connection_name: The name of the connection to be used
    to send the message.
    @type message: String
    @param message: The message to be sent in broadcast mode.
    """

    # retrieves the communication handler
    communication_handler = parameters.get("communication_handler", None)

    # in case there is no communication handler defined
    if not communication_handler:
        # returns immediately
        return

    # sends the broadcast communication message using the communication handler
    communication_handler.send_broadcast_communication_message(connection_name, message)

def process_form_data(self, rest_request, encoding = DEFAULT_ENCODING):
    """
    Processes the form data (attributes), creating a map containing
    the hierarchy of defined structure for the "form" contents.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used.
    @type encoding: String
    @param encoding: The encoding to be used when retrieving
    the attribute values.
    @rtype: Dictionary
    @return: The map containing the hierarchy of defined structure
    for the "form" contents.
    """

    # retrieves the attributes list
    attributes_list = rest_request.get_attributes_list()

    # creates the base attributes map
    base_attributes_map = {}

    # iterates over all the attributes in the
    # attributes list
    for attribute in attributes_list:
        # in case the attribute is invalid
        # or empty (skips the loop)
        if not attribute:
            # continues the loop
            continue

        # retrieves the attribute value from the request
        attribute_value = self.get_attribute_decoded(rest_request, attribute, encoding)

        # retrieves the attribute type
        attribute_value_type = type(attribute_value)

        # in case the attribute value type is list
        if attribute_value_type == types.ListType:
            # starts the index
            index = 0

            # iterates over all the attribute value items
            for attribute_value_item in attribute_value:
                # starts the processing of the form attribute with the base attributes map
                # the base attribute name and the attribute value and the index of the current
                # attribute value item
                self._process_form_attribute(base_attributes_map, attribute, attribute_value_item, index)

                # increments the index
                index += 1
        # otherwise the attribute type must be a string
        else:
            # starts the processing of the form attribute with the base attributes map
            # the base attribute name and the attribute value
            self._process_form_attribute(base_attributes_map, attribute, attribute_value)

    # returns the base attributes map
    return base_attributes_map

def process_form_data_flat(self, rest_request, encoding = DEFAULT_ENCODING):
    """
    Processes the form data (attributes), creating a map containing
    the hierarchy of defined structure for the "form" contents.
    This method runs in flat mode for hierarchies defined with "dot notation".

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used.
    @type encoding: String
    @param encoding: The encoding to be used when retrieving
    the attribute values.
    @rtype: Dictionary
    @return: The map containing the hierarchy of defined structure
    for the "form" contents.
    """

    # retrieves the attributes list
    attributes_list = rest_request.get_attributes_list()

    # creates the base attributes map
    base_attributes_map = {}

    # iterates over all the attributes in the
    # attributes list
    for attribute in attributes_list:
        # retrieves the attribute value from the request
        attribute_value = self.get_attribute_decoded(rest_request, attribute, encoding)

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

def get_base_path(self, rest_request):
    """
    Retrieves the base path according to
    the current rest request path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used to retrieve
    the base path.
    @rtype: String
    @return: The base path.
    """

    # retrieves the path list length
    path_list_length = len(rest_request.path_list)

    # creates the base path
    base_path = str()

    # iterates over all the path list length without
    # the delta value
    for _index in range(path_list_length - 2):
        # adds the back path to the base path
        base_path += BACK_PATH_VALUE

    # returns the base path
    return base_path

def set_contents(self, rest_request, contents = ""):
    """
    Sets the given contents in the given rest request.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be set with the contents.
    @type contents: String
    @param contents: The contents to set in the rest request.
    """

    # sets the content type for the rest request
    rest_request.set_content_type(DEFAULT_CONTENT_TYPE)

    # sets the result for the rest request
    rest_request.set_result_translated(contents)

    # flushes the rest request
    rest_request.flush()

def redirect(self, rest_request, target):
    """
    Redirects the current request to the given
    target (page).

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used.
    @type target: String
    @param target: The target (page) of the redirect.
    """

    # redirects the rest request to the target
    rest_request.redirect(target)

    # sets the contents (null)
    self.set_contents(rest_request)

def redirect_base_path(self, rest_request, target):
    """
    Redirects the current request to the given
    target (page).
    This method updates the target to conform with the
    current base path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used.
    @type target: String
    @param target: The target (page) of the redirect.
    """

    # retrieves the base path
    base_path = self.get_base_path(rest_request)

    # creates the "new" target with the base path
    target_base_path = base_path + target

    # redirects to the target base path
    self.redirect(rest_request, target_base_path)

def process_set_contents(self, rest_request, template_file, variable_encoding = None):
    """
    Processes the template file and set the result of it
    as the contents of the given rest request.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be set with the contents.
    @type template_file: TemplateFile
    @param template_file: The template file to be processed.
    @type variable_encoding: String
    @param variable_encoding: The encoding to be used to encode the variables
    in the template file processing.
    """

    # processes the template file with the given variable encoding
    # retrieving the processed template file
    processed_template_file = self.process_template_file(template_file, variable_encoding)

    # sets the request contents
    self.set_contents(rest_request, processed_template_file)

def process_template_file(self, template_file, variable_encoding = None):
    """
    Processes the given template file, using the given
    variable encoding.

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

    # processes the template file
    processed_template_file = template_file.process()

    # returns the processed template file
    return processed_template_file

def retrieve_template_file(self, file_name = None, encoding = DEFAULT_TEMPLATE_FILE_ENCODING):
    # creates the template file path
    template_file_path = self.templates_path + "/" + file_name

    # parses the template file path
    template_file = self.template_engine_manager_plugin.parse_file_path_encoding(template_file_path, encoding)

    # returns the template file
    return template_file

def apply_base_path_template_file(self, rest_request, template_file):
    """
    Applies the base path to the template file according to
    the current rest request path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used to set the base path.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the base path.
    """

    # retrieves the base path
    base_path = self.get_base_path(rest_request)

    # assigns the area value
    template_file.assign(BASE_PATH_VALUE, base_path)

def assign_session_template_file(self, rest_request, template_file, variable_prefix = "session_"):
    """
    Assigns the session variables to the given template file.
    The name of the session variables is modified replacing
    the dots with underscores.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the session variables.
    @type variable_prefix: String
    @param variable_prefix: The variable prefix to be prepended to the variable names.
    """

    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # returns immediately
        return

    # retrieves the session attributes map
    session_attributes_map = rest_request_session.get_attributes_map()

    # iterates over all the session attributes in the session
    # attributes map
    for session_attribute_name in session_attributes_map:
        # retrieves the session attribute from the session attributes map
        session_attribute = session_attributes_map[session_attribute_name]

        # replaces the dots in the session attribute name
        session_attribute_name_replaced = session_attribute_name.replace(".", "_")

        # assigns the session attribute to the template file
        template_file.assign(variable_prefix + session_attribute_name_replaced, session_attribute)

def get_session_attribute(self, rest_request, session_attribute_name, namespace_name = None):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # returns none (invalid)
        return None

    # resolves the complete session attribute name
    session_attribute_name = _get_complete_session_attribute_name(session_attribute_name, namespace_name)

    # retrieves the attribute from the session
    session_attribute = rest_request_session.get_attribute(session_attribute_name)

    # returns the session attribute
    return session_attribute

def set_session_attribute(self, rest_request, session_attribute_name, session_attribute_value, namespace_name = None):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # start a session if none is started
        rest_request.start_session()

        # retrieves the rest request session
        rest_request_session = rest_request.get_session()

    # resolves the complete session attribute name
    session_attribute_name = _get_complete_session_attribute_name(session_attribute_name, namespace_name)

    # sets the attribute in the session
    rest_request_session.set_attribute(session_attribute_name, session_attribute_value)

def unset_session_attribute(self, rest_request, session_attribute_name, namespace_name = None):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # returns none (invalid)
        return None

    # resolves the complete session attribute name
    session_attribute_name = _get_complete_session_attribute_name(session_attribute_name, namespace_name)

    # unsets the attribute from the session
    rest_request_session.unset_attribute(session_attribute_name)

def get_attribute_decoded(self, rest_request, attribute_name, encoding = DEFAULT_ENCODING):
    """
    Retrieves the attribute from the rest request with
    the given attribute name and decoded using the given
    encoding.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used to retrieve the
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
    attribute_value = rest_request.get_attribute(attribute_name)

    # in case the attribute value is valid
    if attribute_value:
        # retrieves the attribute value type
        attribute_value_type = type(attribute_value)

        # in case the attribute value is a list
        if attribute_value_type == types.ListType:
            # starts the attribute value decoded as list
            attribute_value_decoded = []

            # iterates over all the attribute value
            # items in the attribute value
            for attribute_value_item in attribute_value:
                # decodes the attribute value item
                attribute_value_item_decoded = attribute_value_item.decode(encoding)

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
                # decodes the attribute value value
                attribute_value_value_decoded = attribute_value_value.decode(encoding)

                # sets the attribute value value in the attribute value decoded map
                attribute_value_decoded[attribute_value_key] = attribute_value_value_decoded
        # otherwise it must be a string
        else:
            # decodes the attribute value
            attribute_value_decoded = attribute_value.decode(encoding)

        # the attribute value decoded
        return attribute_value_decoded
    else:
        # returns the empty value
        return ""

def get_templates_path(self):
    """
    Retrieves the templates path.

    @rtype: Sring
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

def get_template_engine_manager_plugin(self):
    """
    Retrieves the template engine manager plugin.

    @rtype: Plugin
    @return: The template engine manager plugin.
    """

    return self.template_engine_manager_plugin

def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
    """
    Sets the template engine manager plugin.

    @type template_engine_manager_plugin: String
    @param template_engine_manager_plugin: The templates path.
    """

    self.template_engine_manager_plugin = template_engine_manager_plugin

def _get_path(self, rest_request):
    # retrieves the base path as the path from the request
    path = rest_request.request.base_path

    # in case the (base) path is not valid (no http server redirection)
    if not path:
        # sets the request path as the path
        path = rest_request.request.path

    # returns the path
    return path

def _get_host(self, rest_request, prefix_path = None):
    """
    Retrieves the host for the current request prepended
    with the given prefix path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used.
    @type prefix_path: String
    @param prefix_path: The prefix path to be prepended to the
    host value.
    @rtype: String
    @return: The current host (name) for the given request.
    """

    # retrieves the host value from the request headers
    host = rest_request.request.headers_map.get(HOST_VALUE, None)

    # in case there is a prefix path defined
    if prefix_path:
        # prepends the prefix path to the host
        host = prefix_path + host

    # returns the host
    return host

def _get_host_path(self, rest_request, suffix_path = "", prefix_path = HTTP_PREFIX_VALUE):
    """
    Retrieves the complete host path to the current rest request.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used.
    @type suffix_path: String
    @param suffix_path: The suffix path to be appended.
    @type prefix_path: String
    @param prefix_path: The prefix path to be prepended.
    @rtype: String
    @return: The complete host path to the current rest request.
    """

    # tries retrieves the host value
    host = self._get_host(rest_request)

    # in case no host is defined
    if not host:
        # raises the insufficient http information exception
        raise web_mvc_utils_exceptions.InsufficientHttpInformation("no host value defined")

    # retrieves the path
    path = self._get_path(rest_request)

    # removes the arguments part of the path
    path = path.split("?")[0]

    # creates the host path with the prefix path the host the first part
    # of the host split and the suffix path
    host_path = prefix_path + host + path.rsplit("/", 1)[0] + suffix_path

    # returns the host path
    return host_path

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
    Converts a string value with multiple words in undescore case to
    a dasherized notation, i.e., different words separated by dashes.

    @type string_value: String
    @param string_value: The string value to dasherize, in undescore
    and without consecutive capitals.
    @rtype: String
    @return: The dasherized string value.
    """

    # replaces the underscores for dashes
    dasherized_string_value = string_value.replace(UNDERSCORE_VALUE, DASH_VALUE)

    # returns the dasherized value
    return dasherized_string_value

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

    # retrieves the current match result
    match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name)

    # in case there is no match result
    if not match_result:
        # raises the invalid attribute name exception
        raise web_mvc_utils_exceptions.InvalidAttributeName("invalid match value: " + current_attribute_name)

    # retrieves the match result end position
    match_result_end = match_result.end()

    # checks if it's the last attribute name
    is_last_attribute_name = match_result_end == len(current_attribute_name)

    # retrieves the match result name
    match_result_name = match_result.lastgroup

    # retrieves the match result value
    match_result_value = match_result.group()

    # in case the match result value is of type map
    # the parentheses need to be removed
    if match_result_name == MAP_TYPE_VALUE:
        # retrieves the match result value without the parentheses
        match_result_value = match_result_value[1:-1]

    # in case it's the only (last) match available
    if is_last_attribute_name:
        # in case the match result is of type name
        if match_result_name == NAME_TYPE_VALUE:
            # sets the attribute value in the parent structure
            parent_structure[match_result_value] = attribute_value
        # in case the match result is of type sequence
        elif match_result_name == SEQUENCE_TYPE_VALUE:
            # adds the attribute value to the
            # parent structure
            parent_structure.append(attribute_value)
        # in case the match result is of type map
        elif match_result_name == MAP_TYPE_VALUE:
            # sets the attribute value in the parent structure
            parent_structure[match_result_value] = attribute_value

    # there is more parsing to be made
    else:
        # retrieves the next match value in order to make
        next_match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name, match_result_end)

        # in case there is no next match result
        if not next_match_result:
            # raises the invalid attribute name exception
            raise web_mvc_utils_exceptions.InvalidAttributeName("invalid next match value: " + current_attribute_name)

        # retrieves the next match result name
        next_match_result_name = next_match_result.lastgroup

        # retrieves the next match result value
        next_match_result_value = next_match_result.group()

        # in case the next match result value is of type map
        # the parentheses need to be removed
        if next_match_result_name == MAP_TYPE_VALUE:
            # retrieves the next match result value without the parentheses
            next_match_result_value = next_match_result_value[1:-1]

        # in case the next match is of type name
        if next_match_result_name == NAME_TYPE_VALUE:
            # raises the invalid attribute name exception
            raise web_mvc_utils_exceptions.InvalidAttributeName("invalid next match value (it's a name): " + current_attribute_name)
        # in case the next match is of type list, a list needs to
        # be created in order to support the sequence, in case a list
        # already exists it is used instead
        elif next_match_result_name == SEQUENCE_TYPE_VALUE:
            # in case the match result value exists in the
            # parent structure there is no need to create a new structure
            # the previous one should be used
            if match_result_value in parent_structure:
                # sets the current attribute value as the value that
                # exists in the parent structure
                current_attribute_value = parent_structure[match_result_value]
            else:
                # creates a new list structure
                current_attribute_value = []
        # in case the next match is of type map, a map needs to
        # be created in order to support the mapping structure, in case a map
        # already exists it is used instead
        elif next_match_result_name == MAP_TYPE_VALUE:
            # in case the current match result is a sequence
            # it's required to check for the valid structure
            # it may be set or it may be a new structure depending
            # on the current "selected" index
            if match_result_name == SEQUENCE_TYPE_VALUE:
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
            # in case the match result value exists in the
            # parent structure there is no need to create a new structure
            # the previous one should be used
            elif match_result_value in parent_structure:
                # sets the current attribute value as the value that
                # exists in the parent structure
                current_attribute_value = parent_structure[match_result_value]
            else:
                # creates a new map structure
                current_attribute_value = {}

        # in case the match result is of type name (first match)
        if match_result_name == NAME_TYPE_VALUE:
            # sets the current attribute value in the parent structure
            parent_structure[match_result_value] = current_attribute_value
        # in case the match result is of type sequence
        elif match_result_name == SEQUENCE_TYPE_VALUE:
            # retrieves the parent structure length
            parent_structure_length = len(parent_structure)

            # in case the current attribute value is meant
            # to be added to the parent structure
            if parent_structure_length <= index:
                # adds the current attribute value to the
                # parent structure
                parent_structure.append(current_attribute_value)
        # in case the match result is of type map
        elif match_result_name == MAP_TYPE_VALUE:
            # sets the current attribute value in the parent structure
            parent_structure[match_result_value] = current_attribute_value

        # retrieves the remaining attribute name
        remaining_attribute_name = current_attribute_name[match_result_end:]

        # processes the next form attribute with the current attribute value as the new parent structure
        # the remaining attribute name as the new current attribute name and the attribute value
        # continues with the same value
        self._process_form_attribute(current_attribute_value, remaining_attribute_name, attribute_value, index)

def _get_complete_session_attribute_name(session_attribute_name, namespace_name):
    """
    Retrieves the complete session attribute name from the session
    attribute name and the namespace name.

    @type session_attribute_name: String
    @param session_attribute_name: The session attribute name.
    @type namespace_name: String
    @param namespace_name: The namespace name
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

def _set_entity_attribute(self, attribute_key, attribute_value, entity, entity_model):
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
    """

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

    # casts the attribute value is using the safe mode
    attribute_value_casted = self._cast_safe(attribute_value, cast_type)

    # sets the attribute value casted in the entity
    setattr(entity, attribute_key, attribute_value_casted)

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

    try:
        # retrieves the value type
        value_type = type(value)

        # in case the value type is the same
        # as the cast type
        if value_type == type:
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
