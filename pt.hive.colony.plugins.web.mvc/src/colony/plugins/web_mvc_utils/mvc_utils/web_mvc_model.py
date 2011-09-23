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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import colony.libs.control_util

import web_mvc_utils_exceptions

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

EMAIL_REGEX_VALUE = "^[\w\d\._%+-]+@[\w\d\.-]+\.\w{2,4}$"
""" The email regex value """

URL_REGEX_VALUE = "^\w+\:\/\/[^\:\/\?#]+(\:\d+)?(\/[^\?#]+)*\/?(\?[^#]*)?(#.*)?$"
""" The url regex value """

EMAIL_REGEX = re.compile(EMAIL_REGEX_VALUE)
""" The email regex """

URL_REGEX = re.compile(URL_REGEX_VALUE)
""" The url regex """

def _start_model(self):
    """
    Starts the model structures.
    """

    # checks if the model has been already
    # started (avoids duplicate initialization, in
    # case of sub-classing)
    if hasattr(self, "model_started"):
        # returns immediately (model already
        # started)
        return

    # starts the validation map associating
    # an attribute name with the validation methods
    self.validation_map = {}

    # start the validation errors map associating an
    # attribute name with the list of errors
    self.validation_errors_map = {}

    # sets the initial (and default) context for
    # the running of the validation process
    self.validation_context = DEFAULT_VALIDATION_CONTEXT

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
        current_attribute = getattr(current_attribute, attribute_name_token)

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
    object = serializer.loads(data)

    # iterates over all the dictionary items
    # to load the values
    for key, value in object.items():
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
    # an attribute with the key name
    if not hasattr(self, key):
        # returns immediately
        return

    # sets the value in the current object
    setattr(self, key, value)

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
        raise web_mvc_utils_exceptions.InvalidValidationMethod("the current validation method does not exist: " + validation_method_name)

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
    @type validation_method: String
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

def add_error(self, attribute_name, error_message):
    """
    Adds an error to the validation error map.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to witch
    there is going to be added an error.
    @type error_message: String
    @param error_message: The error message to be added.
    """

    # in case the attribute name is not defined in the validation
    # errors map
    if not attribute_name in self.validation_errors_map:
        # starts the validation errors map for the attribute name
        # as an empty list
        self.validation_errors_map[attribute_name] = []

    # adds the validation error to the validation error
    # list for the attribute name
    self.validation_errors_map[attribute_name].append(error_message)

def validate(self):
    """
    Validates all the attributes in the current object.
    """

    # retrieves the context validation map for the current validation context
    context_validation_map = self.validation_map.get(self.validation_context, [])

    # iterates over all the items in the context validation map
    for attribute_name, validation_tuple_list in context_validation_map.items():
        # retrieves the attribute value
        attribute_value = getattr(self, attribute_name)

        # in case the attribute is lazy loaded
        if attribute_value == LAZY_LOADED_VALUE:
            # continues since nothing else can be tested
            continue

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

            # calls the validation method for validation
            validation_method(attribute_name, attribute_value, properties)

    # returns if the structure is valid
    return self.is_valid()

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
        self.add_error(attribute_name, "length of value is greater or equal to the target")

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
        self.add_error(attribute_name, "length of value is less or equal to the target")

def in_enumeration_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is greater than zero.

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
        self.add_error(attribute_name, "value is less or equal to the target")

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
        self.add_error(attribute_name, "value is less than the target")

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
        self.add_error(attribute_name, "value is greater or equal to the target")

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
        self.add_error(attribute_name, "value is greater or equal to zero")

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
        self.add_error(attribute_name, "value is greater than the target")

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

    # in case the value is not within the decimal percentage boundaries
    if not attribute_value <= 0:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is greater than zero")

def is_percentage_decimal_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that the value is a percentage.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # in case the value is not within the decimal percentage boundaries
    if attribute_value < 0 or attribute_value > 1:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is not a decimal percentage")

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

    # retrieves the regex (the regex string is
    # passed instead of the compiled regular
    # expression or else the entity would become
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
    This validator expects the attribute value to be a list, and will
    search the list's items for the specified attribute, adding validation
    errors in case more than one item has the same attribute value.
    These validation errors will be added to the attribute being
    validated, the referenced composite attribute, and the entity
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
    entity_attribute_name = len(target_tokens) > 1 and target_tokens[-2] or None

    # initializes the allocated entities map
    allocated_entities_map = {}

    # for each entity in the attribute value
    for entity in attribute_value:
        # retrieves the attribute value
        value = entity.get_attribute_name(target)

        # associates the entity with the value in order
        # to later detect which entities have duplicate attributes
        allocated_entities = allocated_entities_map.get(value, [])
        allocated_entities.append(entity)
        allocated_entities_map[value] = allocated_entities

    # retrieves the allocated entities lists that have more
    # than one entity and are therefore invalid
    allocated_entities_lists = [allocated_entities for allocated_entities in allocated_entities_map.values() if len(allocated_entities) > 1]

    # removes the last target token since this
    # list is going to be used to retrieve the
    # the entity that owns the last attribute
    target_tokens = target_tokens and target_tokens[:-1] or []

    # for each allocated entities list
    for allocated_entities in allocated_entities_lists:
        # for each allocated entity
        for allocated_entity in allocated_entities:
            # marks the validation as failed
            validation_failed = True

            # initializes the entity and the
            # attribute entity
            entity = None
            attribute_entity = allocated_entity

            # iterates over all the attribute name tokens
            for target_token in target_tokens:
                # updates the entity and attribute entity
                entity = attribute_entity
                attribute_entity = getattr(attribute_entity, target_token)

            # adds an error to the duplicated attribute
            attribute_entity.add_error(target_attribute_name, "value is same")

            # adds an error to the entity that has the duplicated attribute
            entity and entity.add_error(entity_attribute_name, "value has duplicate")

    # in case the validation failed adds an error to the attribute
    validation_failed and self.add_error(attribute_name, "value has duplicates")
