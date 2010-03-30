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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import imp

BASE_ENTITY_MODULE_VALUE = "base_entity"
""" The base entity module value """

GLOBALS_REFERENCE_VALUE = "_globals"
""" The globals reference value """

LOCALS_REFERENCE_VALUE = "_locals"
""" The locals reference value """

DEFAULT_MODULE_NAME = "helper_module"
""" The default module name """

class BusinessHelper:
    """
    The business helper class.
    """

    business_helper_plugin = None
    """ The business helper plugin """

    def __init__(self, business_helper_plugin):
        """
        Constructor of the class.

        @type business_helper_plugin: BusinessHelperPlugin
        @param business_helper_plugin: The business helper plugin.
        """

        self.business_helper_plugin = business_helper_plugin

    def import_class_module(self, class_module_name, globals, locals, global_values, base_directory_path, target_module_name = DEFAULT_MODULE_NAME):
        """
        Imports the class module using the globals and locals from the current target,
        it imports the symbols in the module to the current globals environment.

        @type class_module_name: String
        @param class_module_name: The name of the module containing the classes to be imported.
        @type globals: Dictionary
        @param globals: The global variables map.
        @type locals: Dictionary
        @param locals: The local variables map.
        @type global_values: List
        @param global_values: A list containing the global values to be converted from locals.
        @type base_directory_path: String
        @param base_directory_path: The base directory path to be used.
        @type target_module_name: String
        @param target_module_name: The name of the module to import the classes.
        @rtype: Module
        @return: The created target module.
        """

        # tries to retrieve the target module
        target_module = self._get_target_module(target_module_name, globals)

        # sets the target module dictionary as the target map
        target_map = target_module.__dict__

        # retrieves the base entity module
        base_entity_module = self._get_target_module(BASE_ENTITY_MODULE_VALUE, globals)

        # sets the entity class in the base entity module
        base_entity_module.__dict__[EntityClass.__name__] = EntityClass

        # sets the base entity module in the globals
        globals[BASE_ENTITY_MODULE_VALUE] = base_entity_module

        # sets the globals reference attribute
        target_map[GLOBALS_REFERENCE_VALUE] = globals

        # sets the locals reference attribute
        target_map[LOCALS_REFERENCE_VALUE] = locals

        # executes the file in the given environment
        # to import the symbols
        execfile(base_directory_path + "/" + class_module_name + ".py", target_map, target_map)

        # returns the target module
        return target_module

    def generate_bundle_map(self, bundle_classes):
        # creates the bundle map
        bundle_map = {}

        # iterates over all the bundle classes
        for bundle_class in bundle_classes:
            # retrieves the bundle class name
            bundle_class_name = bundle_class.__name__

            # sets the class in the bundle bundle map
            bundle_map[bundle_class_name] = bundle_class

        # returns the bundle map
        return bundle_map

    def generate_module_bundle(self, bundle_module_name, bundle_map):
        # creates the bundle module
        bundle_module = imp.new_module(bundle_module_name)

        for bundle_key, bundle_value in bundle_map.items():
            bundle_module.__dict__[bundle_key] = bundle_value

        # returns the bundle module
        return bundle_module

    def get_entity_class(self):
        return EntityClass

    def _get_target_module(self, target_module_name, globals):
        # tries to retrieve the target module
        target_module = globals.get(target_module_name, None)

        # in case the target module is not defined
        if not target_module:
            # creates the target module
            target_module = imp.new_module(target_module_name)

            # adds the target module to the globals map
            globals[target_module_name] = target_module

        # returns the target model
        return target_module

class EntityClass(object):
    """
    The base entity class used
    for the entity manager.
    """

    def __init__(self):
        """
        Constructor fo the class.
        """

        pass
