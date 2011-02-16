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

import re

import colony.libs.control_util

import web_mvc_utils_exceptions

VALIDATION_METHOD_SUFFIX = "_validate"
""" The validation method suffix """

TARGET_VALUE = "target"
""" The target value """

MANDATORY_VALUE = "mandatory"
""" The mandatory value """

EMAIL_REGEX_VALUE = "[\w\d\._%+-]+@[\w\d\.-]+\.\w{2,4}"
""" The email regex value """

URL_REGEX_VALUE = "\w+\:\/\/[^\:\/\?#]+(\:\d+)?(\/[^\?#]+)*\/?(\?[^#]*)?(#.*)?"
""" The url regex value """

EMAIL_REGEX = re.compile(EMAIL_REGEX_VALUE)
""" The email regex """

URL_REGEX = re.compile(URL_REGEX_VALUE)
""" The url regex """

def _start_model(self):
    """
    Starts the model structures.
    """

    # starts the validation map associating
    # an attribute name with the validation methods
    self.validation_map = {}

    # start the validation errors map associating an
    # attribute name with the list of errors
    self.validation_errors_map = {}

    # in case the model has the start method
    if hasattr(self, "start"):
        # calls the start method (to be implemented)
        self.start()

    # in case the model has the set validation method
    if hasattr(self, "set_validation"):
        # calls the set validation method (to be implemented)
        self.set_validation()

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

def add_validation_method(self, attribute_name, validation_method_name, properties = {}):
    """
    Adds a validation method to the attribute with the given name.
    The adding of the validation can be configured using the properties
    map.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to "receive" the validation.
    @type validation_method_name: String
    @param validation_method_name: The name of the validation method to be added to the attribute.
    @type properties: Dictionary
    @param properties: The properties of the adding of the validation method.
    """

    # in case the attribute name does not exist
    # in the validation map
    if not attribute_name in self.validation_map:
        # creates a list for the attribute name in
        # the validation map
        self.validation_map[attribute_name] = []

    # adds the validation method suffix to the validate method name
    validation_method_name = validation_method_name + VALIDATION_METHOD_SUFFIX

    # in case the validation method does not exist in
    # the current object
    if not hasattr(self, validation_method_name):
        raise web_mvc_utils_exceptions.InvalidValidationMethod("the current validation method does not exist: " + validation_method_name)

    # retrieves the validation method
    validation_method = getattr(self, validation_method_name)

    # creates the validation tuple as the set of the validation
    # method and the properties
    validation_tuple = (validation_method, properties)

    # adds the validation tuple to the validation map
    self.validation_map[attribute_name].append(validation_tuple)

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

    # iterates over all the items in the validation maps
    for attribute_name, validation_tuple_list in self.validation_map.items():
        # retrieves the attribute value
        attribute_value = getattr(self, attribute_name)

        # retrieves the attribute class value
        attribute_class_value = getattr(self.__class__, attribute_name)

        # retrieves the attribute is mandatory value
        attribute_is_mandatory = attribute_class_value.get(MANDATORY_VALUE, False)

        # in case the attribute is not mandatory and the attribute
        # value is none
        if not attribute_is_mandatory and attribute_value == None:
            # continues the loop
            continue

        # in case the attribute is mandatory and the attribute
        # value is none
        if attribute_is_mandatory and attribute_value == None:
            # adds an error to the given attribute name
            self.add_error(attribute_name, "value is not set for mandatory attribute")

            # continues the loop
            continue

        # iterates over all the validation tuples
        for validation_tuple in validation_tuple_list:
            # retrieves the validation method and properties
            # from the validation tuple
            validation_method, properties = validation_tuple

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

    # in case the attribute value is empty or invalid
    if not attribute_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is empty")

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
    values = properties["values"]

    # in case the attribute value is not in the values
    if not attribute_value in values:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is not in enumeration")

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
        self.add_error(attribute_name, "value is less or equal to zero")

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

def greater_than_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is greater than.

    @type attribute_name: String
    @param attribute_name: The name of the attribute to be validated.
    @type attribute_value: Object
    @param attribute_value: The value of the attribute to be validated.
    @type properties: Dictionary
    @param properties: The properties for the validation.
    """

    # retrieves the target value from the properties
    target_value = properties[TARGET_VALUE]

    # in case the attribute value is not greater than
    # the target value
    if not attribute_value > target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is less or equal that the target")

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

def less_than_validate(self, attribute_name, attribute_value, properties):
    """
    Validates an attribute to ensure that it is less than target.

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
    if not attribute_value < target_value:
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is greater or equal that the target")

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
