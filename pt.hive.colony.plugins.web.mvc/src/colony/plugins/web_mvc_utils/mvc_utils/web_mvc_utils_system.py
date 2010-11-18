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

import imp
import types

import web_mvc_utils
import web_mvc_model
import web_mvc_controller
import web_mvc_entity_model

ENGINE_VALUE = "engine"
""" The engine value """

NAME_REFERENCE_VALUE = "__name__"
""" The name reference value """

PACKAGE_REFERENCE_VALUE = "__package__"
""" The package reference value """

GLOBALS_REFERENCE_VALUE = "_globals"
""" The globals reference value """

LOCALS_REFERENCE_VALUE = "_locals"
""" The locals reference value """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

ENTITY_CLASSES_LIST_VALUE = "entity_classes_list"
""" The entity classes list value """

ENTITY_CLASSES_MAP_VALUE = "entity_classes_map"
""" The entity classes map value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

PYTHON_EXTENSION = ".py"
""" The python extension """

DEFAULT_ENGINE = "sqlite"
""" The default engine """

DEFAULT_CONNECTION_PARAMETERS = {"file_path" : "mvc_utils_system.db", "autocommit" : False}
""" The default connection parameters """

class WebMvcUtils:
    """
    The web mvc utils class.
    """

    web_mvc_utils_plugin = None
    """ The web mvc utils plugin """

    def __init__(self, web_mvc_utils_plugin):
        """
        Constructor of the class.

        @type web_mvc_utils_plugin: WebMvcUtilsPlugin
        @param web_mvc_utils_plugin: The web mvc utils plugin.
        """

        self.web_mvc_utils_plugin = web_mvc_utils_plugin

    def import_module_mvc_utils(self, module_name, package_name, directory_path):
        # creates the globals map from
        # the current globals map
        globals_map = globals()

        # creates the locals map
        locals_map = {}

        # tries to retrieve the target module
        target_module = self._get_target_module(module_name, globals_map)

        # sets the target module dictionary as the target map
        target_map = target_module.__dict__

        # in case the package name is defined
        if package_name:
            # creates the complete module name from the package name
            complete_module_name = package_name + "." + module_name
        # otherwise
        else:
            # creates the complete module name just from
            # the module name
            complete_module_name = module_name

        # sets the name and the package in the target map
        target_map[NAME_REFERENCE_VALUE] = complete_module_name
        target_map[PACKAGE_REFERENCE_VALUE] = package_name

        # sets the web mvc utils in the globals map
        globals_map[WEB_MVC_UTILS_VALUE] = web_mvc_utils

        # sets the globals reference attribute
        target_map[GLOBALS_REFERENCE_VALUE] = globals_map

        # sets the locals reference attribute
        target_map[LOCALS_REFERENCE_VALUE] = locals_map

        # creates the python file path
        python_file_path = directory_path + "/" + module_name + PYTHON_EXTENSION

        # executes the file in the given environment
        # to import the symbols
        execfile(python_file_path, target_map, target_map)

        # returns the target module
        return target_module

    def create_model(self, base_model, base_arguments_list, base_arguments_map):
        # sets the module functions in the base model class
        self._set_module_functions(web_mvc_model, base_model)

        # creates the model with the sent arguments list and the arguments map
        model = base_model(*base_arguments_list, **base_arguments_map)

        # starts the model structures
        model._start_model()

        # returns the model
        return model

    def create_controller(self, base_controller, base_arguments_list, base_arguments_map):
        # sets the module functions in the base controller class
        self._set_module_functions(web_mvc_controller, base_controller)

        # creates the controller with the sent arguments list and the arguments map
        controller = base_controller(*base_arguments_list, **base_arguments_map)

        # starts the controller structures
        controller._start_controller()

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.web_mvc_utils_plugin.template_engine_manager_plugin

        # sets the template engine manager plugin in the controller
        controller.set_template_engine_manager_plugin(template_engine_manager_plugin)

        # returns the controller
        return controller

    def create_entity_models(self, base_entity_models_module_name, entity_manager_arguments, directory_path):
        # retrieves the entity manager plugin
        entity_manager_plugin = self.web_mvc_utils_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.web_mvc_utils_plugin.business_helper_plugin

        # imports the base entity models module
        base_entity_models_module = business_helper_plugin.import_class_module_target(base_entity_models_module_name, globals(), locals(), [], directory_path, base_entity_models_module_name)

        # retrieves the entity class
        entity_class = business_helper_plugin.get_entity_class()

        # retrieves all the entity classes from the base entity models module
        base_entity_models = self._get_entity_classes(base_entity_models_module, entity_class)

        # generates the entity models map from the base entity models list
        # creating the map associating the class names with the classes
        base_entity_models_map = business_helper_plugin.generate_bundle_map(base_entity_models)

        # retrieves the engine from the entity manager arguments or uses
        # the default engine
        engine = entity_manager_arguments.get(ENGINE_VALUE, DEFAULT_ENGINE)

        # retrieves the connection parameters from the entity manager arguments or uses
        # the default connection parameters
        connection_parameters = entity_manager_arguments.get(CONNECTION_PARAMETERS_VALUE, DEFAULT_CONNECTION_PARAMETERS)

        # resolves the connection parameters
        self._resolve_connection_parameters(connection_parameters)

        # creates the entity manager properties
        entity_manager_properties = {ENTITY_CLASSES_LIST_VALUE : base_entity_models, ENTITY_CLASSES_MAP_VALUE : base_entity_models_map}

        # creates a new entity manager for the remote models with the given properties
        entity_manager = entity_manager_plugin.load_entity_manager_properties(engine, entity_manager_properties)

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters(connection_parameters)

        # loads the entity manager
        entity_manager.load_entity_manager()

        # iterates over all the base entity models to update them
        # in order to allow them to become entity models
        for base_entity_model in base_entity_models:
            # sets the module functions in the base model class
            self._set_module_functions(web_mvc_model, base_entity_model)

            # sets the module functions in the base model class
            self._set_module_functions(web_mvc_entity_model, base_entity_model)

            # sets the newinit method as the new init method
            base_entity_model.__init__ = create_newinit(base_entity_model)

            # sets the entity manager in the base entity model
            base_entity_model._entity_manager = entity_manager

        # sets the entity manager in the base entity models module
        base_entity_models_module.entity_manager = entity_manager

        # returns the base entity models module
        return base_entity_models_module

    def create_search_index_controller(self, search_index_identifier, search_index_configuration_map, entity_models_modules):
        # retrieves the web mvc search plugin
        web_mvc_search_plugin = self.web_mvc_utils_plugin.web_mvc_search_plugin

        # creates the search index controller
        search_index_controller = web_mvc_search_plugin.create_search_index_controller(search_index_identifier, search_index_configuration_map, entity_models_modules)

        # returns the created search index controller
        return search_index_controller

    def _resolve_connection_parameters(self, connection_parameters):
        """
        Resolves the given connection parameters map, substituting
        the values with the resolved ones.

        @type connection_parameters: Dictionary
        @param connection_parameters: The connection parameters to be resolved.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_utils_plugin.manager

        # resolves the file path
        connection_parameters[FILE_PATH_VALUE] = plugin_manager.resolve_file_path(connection_parameters[FILE_PATH_VALUE], True, True)

    def _get_entity_classes(self, module, entity_class):
        """
        Retrieves all the entity classes from the given module
        using the given entity class as the reference to get the entity classes.

        @type module: Module
        @param module: The module to be used to retrieve the entity classes.
        @type entity_class: Class
        @param entity_class: The entity class to be used as reference
        to retrieve the entity classes.
        @rtype: List
        @return: The list of entity classes in the module.
        """

        # creates the entity classes list
        entity_classes = []

        # retrieves the base entity models module map
        module_map = module.__dict__

        # iterates over all the module item names
        for module_item_name in module_map:
            # retrieves the module item from  module
            module_item = getattr(module, module_item_name)

            # retrieves the module item type
            module_item_type = type(module_item)

            # in case the module item type is type and
            # the module item is subclass of the entity class
            if module_item_type == types.TypeType and issubclass(module_item, entity_class):
                # adds the module item to the entity classes
                entity_classes.append(module_item)

        # returns the entity classes
        return entity_classes

    def _set_module_functions(self, module, target_class):
        """
        Updates the target class, adding all the functions
        found in the given module as method to it.

        @type module: Module
        @param module: The module to be used to find the functions
        to be added to the target class.
        @type target_class: Class
        @param target_class: The class to be used as target of the adding
        of the methods.
        """

        # iterates over all the items in the module
        for item in dir(module):
            # retrieves the item value
            item_value = getattr(module, item)

            # retrieves the item value type
            item_value_type = type(item_value)

            # in case the item value type is function
            if item_value_type == types.FunctionType:
                # sets the item in the
                setattr(target_class, item, item_value)

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

def create_newinit(base_entity_model):
    """
    Creates the new init function based on the base entity model.

    @type base_entity_model: Object
    @param base_entity_model: The base entity model to be used
    in the construction of the the new init function.
    @rtype: Function
    @return: The generated new init function.
    """

    # retrieves the base entity model oldinit function
    base_entity_model_oldinit = base_entity_model.__init__

    def __newinit__(self):
        """
        The new class constructor to be used by the
        the entity model.
        """

        # calls the model start method
        self._start_model()

        # calls the old constructor
        base_entity_model_oldinit(self)

    return __newinit__
