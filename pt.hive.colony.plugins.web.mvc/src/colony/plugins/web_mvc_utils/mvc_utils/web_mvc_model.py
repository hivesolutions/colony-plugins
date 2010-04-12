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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import web_mvc_utils_exceptions

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

    if not attribute_name in self.validation_map:
        self.validation_map[attribute_name] = []

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
        return False
    else:
        return True

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

    # in case the attribute value is empty of invalid
    if attribute_value == None or attribute_value == "":
        # adds an error to the given attribute name
        self.add_error(attribute_name, "value is empty")
