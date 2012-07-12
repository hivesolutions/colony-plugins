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

import os
import sys
import imp
import types

import colony.base.system
import colony.libs.map_util
import colony.libs.stack_util
import colony.libs.import_util
import colony.libs.string_util

import utils
import model
import controller
import entity_model

ID_VALUE = "id"
""" The id value """

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

DATA_REFERENCE_VALUE = "data_reference"
""" The data reference value """

DEFAULT_VALUE = "default"
""" The default value """

CONTROLLER_VALUE = "controller"
""" The controller value """

CONTROLLERS_VALUE = "controllers"
""" The controllers value """

MODELS_VALUE = "models"
""" The models value """

RESOURCES_VALUE = "resources"
""" The resources value """

CONTROLLER_CAMEL_VALUE = "Controller"
""" The controller camel value """

EXCEPTION_CONTROLLER_VALUE = "ExceptionController"
""" The exception controller value """

EXCEPTION_HANDLER_VALUE = "exception_handler"
""" The exception handler value """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

ENTITIES_LIST_VALUE = "entities_list"
""" The entities list value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

mvc_UTILS_VALUE = "mvc_utils"
""" The mvc utils value """

PYTHON_INIT_FILE = "__init__.py"
""" The python package initializer file """

PYTHON_EXTENSION = ".py"
""" The python extension """

DEFAULT_ENGINE = "sqlite"
""" The default engine """

DEFAULT_DATABASE_PREFIX = ""
""" The default database prefix """

DEFAULT_DATABASE_SUFFIX = "database.db"
""" The default database suffix """

DEFAULT_CONNECTION_PARAMETERS = {
    "file_path" : "mvc_utils_system.db",
    "autocommit" : False
}
""" The default connection parameters """

SYMBOLS_LIST = (
    ("handle_list", r"^%s/%s$", "get"),
    ("handle_new", r"^%s/%s/new$", "get"),
    ("handle_create", r"^%s/%s$", "post"),
    ("handle_show", r"^%s/%s/(?P<id>\w+)$", "get"),
    ("handle_edit", r"^%s/%s/(?P<id>\w+)/edit$", "get"),
    ("handle_update", r"^%s/%s/(?P<id>\w+)/update$", "post"),
    ("handle_delete", r"^%s/%s/(?P<id>\w+)/delete$", "post")
)
""" The list of symbols to be used for pattern generation """

class MvcUtils(colony.base.system.System):
    """
    The mvc utils class.
    """

    models_modules_map = {}
    """ The map containing the various models modules
    associated with the entity manager ids """

    package_path_models_map = {}
    """ The map associating a package path with the
    internal models """

    package_path_controllers_map = {}
    """ The map associating a package path with the
    internal controllers """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)

        self.models_modules_map = {}
        self.package_path_models_map = {}
        self.package_path_controllers_map = {}

    def import_module_mvc_utils(self, module_name, package_name, directory_path = None, system_instance = None):
        # retrieves the directory path taking into account the call module directory
        directory_path = directory_path or colony.libs.stack_util.get_instance_module_directory(system_instance)

        # creates the globals map from
        # the current globals map
        globals_map = globals()

        # creates the locals map
        locals_map = {}

        # creates the complete module name from the package name, avoiding the
        # usage of the package name in case it does not exists
        complete_module_name = package_name and package_name + "." + module_name or module_name

        # checks if the target module already exists, to later
        # avoid module reloading
        exists_target_module = self._exists_target_module(complete_module_name, globals_map)

        # tries to retrieve the target module, creating it if
        # it does not already exists
        target_module = self._get_target_module(complete_module_name, globals_map)

        # in case the target module already existed
        # no need to reload it
        if exists_target_module:
            # returns the target module immediately
            return target_module

        # sets the target module dictionary as the target map
        target_map = target_module.__dict__

        # retrieves the system instance symbols map for latter
        # model symbol retrieval (these models are going to be
        # set in the globals of the controller module)
        system_instance_symbols = system_instance.__dict__

        # sets the name and the package in the target map
        target_map[NAME_REFERENCE_VALUE] = complete_module_name
        target_map[PACKAGE_REFERENCE_VALUE] = package_name

        # iterates over all the dictionary values in the system
        # instance, in these values should be present the models
        # reference values
        for symbol_name, symbol in system_instance_symbols.items():
            # in case the symbol name ends with the models
            # suffix it must be a models reference
            if not symbol_name.endswith(MODELS_VALUE):
                # continues the loop
                continue

            # sets the symbol in the globals map
            # for latter reference
            globals_map[symbol_name] = symbol

        # sets the mvc utils in the globals map, this is useful
        # allow later reference of the mvc utils in the created
        # module (export of symbols)
        globals_map[mvc_UTILS_VALUE] = utils

        # sets the target map globals and locals
        # reference attributes
        target_map[GLOBALS_REFERENCE_VALUE] = globals_map
        target_map[LOCALS_REFERENCE_VALUE] = locals_map

        # creates the directory path to be used for testing, check
        # if the module refers a directory or a file
        test_directory_path = os.path.join(directory_path, module_name)

        # in case the  module refers a directory (package), the initializer
        # file muse be used during the import
        if os.path.isdir(test_directory_path):
            # sets the python file as the module initializer one
            # this is mandatory for a good directory module (package) loading
            python_file_path = os.path.join(test_directory_path, PYTHON_INIT_FILE)
        # otherwise it's a normal file module, and the normal loading
        # process applies
        else:
            # creates the python file path, by joining the directory
            # path and the module name
            python_file_path = os.path.join(directory_path, module_name + PYTHON_EXTENSION)

        # executes the file in the given environment
        # to import the symbols
        execfile(python_file_path, target_map, target_map)

        # returns the target (imported) module
        return target_module

    def create_model(self, base_model, base_arguments_list, base_arguments_map, start_structures = False):
        # sets the module functions in the base model class
        self._set_module_functions(model, base_model)

        # creates the model with the sent arguments list and the arguments map
        model = base_model(*base_arguments_list, **base_arguments_map)

        # starts the model structures, only in case the
        # the start structures flag is set
        start_structures and model._start_model()

        # returns the model
        return model

    def create_controller(self, base_controller, base_arguments_list, base_arguments_map, start_structures = False, default_parameters = {}):
        # retrieves the required plugins
        template_engine_plugin = self.plugin.template_engine_plugin
        json_plugin = self.plugin.json_plugin

        # retrieves the first and second arguments from the base arguments
        # as the plugin and the system instance
        plugin = base_arguments_list[0]
        system_instance = base_arguments_list[1]

        # sets the module functions in the base controller class
        self._set_module_functions(controller, base_controller)

        # creates the controller with the sent arguments list and the arguments map
        _controller = base_controller(*base_arguments_list, **base_arguments_map)

        # sets the plugin in the controller
        _controller.set_plugin(plugin)

        # constructs the controller structures, this method should
        # create the necessary parameter structures for the controller
        _controller._create_controller()

        # starts the controller structures, only in case the
        # the start structures flag is set
        start_structures and _controller._start_controller()

        # sets the template engine plugin in the controller
        _controller.set_template_engine_plugin(template_engine_plugin)

        # sets the template engine plugin and the json plugins
        # in the controller
        _controller.set_template_engine_plugin(template_engine_plugin)
        _controller.set_json_plugin(json_plugin)

        # extends the default parameters in the controller
        # with the given map of parameters
        _controller.extend_default_parameters(default_parameters)

        # retrieves the (directory) relative path to the
        # plugin instance and uses it to create the "default"
        # resources path to be used
        plugin_instance_path = self._get_module_path(system_instance)
        resources_path = os.path.join(plugin_instance_path, RESOURCES_VALUE)

        # sets the "relative" resources path in the controller
        _controller.set_relative_resources_path(resources_path)

        # returns the (created) controller
        return _controller

    def create_base_models(self, system_instance, package_path, entity_manager_arguments, directory_path, extra_entity_models = [], load_entity_manager = True):
        # retrieves the entity related plugins
        entity_manager_plugin = self.plugin.entity_manager_plugin
        business_helper_plugin = self.plugin.business_helper_plugin

        # splits the package path into the extra and base
        # parts to be used in the business helper
        _base_entity_module_name, entity_module_name = package_path.rsplit(".", 1)

        # retrieves the entity class, to later detect the classes
        # than inherit from it (entity class test)
        entity_class = business_helper_plugin.get_entity_class()

        # retrieves the extra symbols map for the module importing, these
        # symbols represents the extra classes and values to be exposed
        # to the entity models
        extra_symbols_map = self._get_extra_symbols_map(extra_entity_models, entity_class)

        # creates a new map to hold the various extra global symbols
        # to be exposes to the created module
        extra_globals_map = {}

        # retrieves the entity id from the entity manager arguments or sets
        # the id as undefined, this id is used to identify the correct
        # models module to be used, in case no id is found the default
        # (global) module will be used
        id = entity_manager_arguments.get(ID_VALUE, None)
        models_id = id or DEFAULT_VALUE
        models_module = self.models_modules_map.get(models_id, None)

        # in case no models module is found one must be created
        # and the internal structure updated
        if not models_module:
            # replaces the dots with underscore characters
            # for the module name to avoid possible problems
            # and then uses it to creates the models module
            models_module_name = models_id.replace(".", "_")
            models_module = imp.new_module(models_module_name)

            # sets the entity class the entity model and the (base) model
            # in the modules module for latter models reference
            setattr(models_module, entity_class.__name__, entity_class)
            setattr(models_module, "EntityModel", entity_class)
            setattr(models_module, "DataRefenceModel", DataReferenceModel)
            setattr(models_module, "Model", RawModel)

            # sets the models module in the models module
            # map for the entity manager id
            self.models_modules_map[models_id] = models_module

        # updates the map containing the extra global symbols
        # with the models module (to be used by the models to refer
        # to other models)
        extra_globals_map[MODELS_VALUE] = models_module

        # imports the base entity models module
        base_entity_models_module = business_helper_plugin.import_class_module_extra(entity_module_name, globals(), locals(), [], directory_path, package_path, extra_symbols_map, extra_globals_map)

        # retrieves all the entity (and non entity) classes from the base entity models module
        # the entity class is used as reference (all entity classes must inherit from that class)
        base_entity_models = self._get_entity_classes(base_entity_models_module, entity_class)
        base_models = self._get_classes(base_entity_models_module, RawModel)

        # in case there are (base) entity models available, need to load and set the entity
        # manager with them (in case there are no entity manager defined no loading occurs)
        if base_entity_models:
            # retrieves the engine from the entity manager arguments or uses
            # the default engine
            engine = entity_manager_arguments.get(ENGINE_VALUE, DEFAULT_ENGINE)

            # retrieves the connection parameters from the entity manager arguments or uses
            # the default connection parameters and resolves them into the proper representation
            connection_parameters = entity_manager_arguments.get(CONNECTION_PARAMETERS_VALUE, DEFAULT_CONNECTION_PARAMETERS)
            self._resolve_connection_parameters(connection_parameters)

            # creates the entity manager properties, the id to be
            # used in the entity manager is the one constructed for
            # the models module
            entity_manager_properties = {
                ID_VALUE : models_id,
                ENTITIES_LIST_VALUE : base_entity_models
            }

            # creates a new entity manager for the remote models with the given properties
            # then sets the connection parameters in it and triggers the loading (open) process
            # (only in case the load entity manager flag is set)
            entity_manager = entity_manager_plugin.load_entity_manager_properties(engine, entity_manager_properties)
            entity_manager.set_connection_parameters(connection_parameters)
            load_entity_manager and entity_manager.open()

            # sets the entity manager in the base entity models module
            # and in the models module (for latter reference)
            base_entity_models_module.entity_manager = entity_manager
            models_module.entity_manager = entity_manager

        # iterates over all the base entity models to update them
        # in order to allow them to become entity models
        for base_entity_model in base_entity_models:
            # retrieves the name of the base entity (model)
            # for latter usage
            base_entity_name = base_entity_model.__name__

            # sets the both the model and the entity model
            # functions in the base model class (enables it
            # as model and entity model)
            self._set_module_functions(model, base_entity_model)
            self._set_module_functions(entity_model, base_entity_model)

            # creates and sets the start method as the new
            # start method (also backs up the old start method)
            base_entity_model._start = create_new_start(base_entity_model)

            # sets the entity manager and the system instance (system)
            # in the base entity model (useful for later reference)
            base_entity_model._entity_manager = entity_manager
            base_entity_model._system_instance = system_instance

            # sets the base entity model in the models module
            # with the base entity name
            setattr(models_module, base_entity_name, base_entity_model)

        # iterates over all the base models to update them
        # in order to allow them to become models
        for base_model in base_models:
            # retrieves the name of the base (model)
            # for latter usage
            base_name = base_model.__name__

            # sets the model functions in the base model class
            # (enables it as model)
            self._set_module_functions(model, base_model)

            # creates and sets the start method as the new
            # start method (also backs up the old start method)
            base_model._start = create_new_start(base_model)

            # sets the system instance (system) in the base
            # model (useful for later reference)
            base_model._system_instance = system_instance

            # sets the base model in the models module
            # with the base name
            setattr(models_module, base_name, base_model)

        # returns the base entity models, the base
        # models (no persistence) and the models module
        return (
            base_entity_models,
            base_models,
            models_module
        )

    def create_models(self, system_instance, plugin_instance, package_path = None, entity_manager_arguments = {}, extra_models = []):
        # retrieves the directory path from the system instance
        directory_path = colony.libs.stack_util.get_instance_module_directory(system_instance)

        # retrieves the "complete" module name for the system
        # instance to be used as target for the model creation
        module_name = system_instance.__module__

        # splits the system instance module name into the package and
        # base module name parts then uses it to create the default
        # package path in case it's necessary
        package_name, _module_name = module_name.rsplit(".", 1)
        package_path = package_path or package_name + "." + MODELS_VALUE

        # unpacks the package path (complete module name) into extra module name (ignored)
        # and the base module name for name retrieval and path creation
        _extra_module_name, base_module_name = package_path.rsplit(".", 1)

        # creates the test directory
        test_directory_path = os.path.join(directory_path, base_module_name)

        # in case the path refers a directory we assume it contains
        # a series of modules containing models and must be imported
        # in a conveniently fashion
        if os.path.isdir(test_directory_path):
            # imports the package module for back reference in the
            # internal importing of modules inside the modules (this is a mandatory
            # operation to avoid problems with the python interpreter), the custom
            # importer does not provide recursive import by default
            __import__(package_path)

            # retrieves the various directory entries for the
            # test (package) directory path to be loaded as modules
            module_items = os.listdir(test_directory_path)

            # initializes the lists that will hold both all the
            # entity models and models created by all the module items
            entity_models = []
            models = []

            # iterates over all the module items to load them as python
            # modules containing models
            for module_item in module_items:
                # splits the module item into the base and extension
                # values
                module_base, module_extension = os.path.splitext(module_item)

                # in case the module extension is not
                # a python file, ignores the file
                if not module_extension == PYTHON_EXTENSION:
                    # continues the loop
                    continue

                # creates the "new" model package path from the
                # "parent" package path
                module_package_path = package_path + "." + module_base

                # reloads the module associated with the given package
                # path to provide flushing of the contents, also flushes
                # the module package path from the globals
                colony.libs.import_util.reload_import(module_package_path)
                self._flush_globals(module_package_path)

            # iterates over all the module items to load them as python
            # modules containing models
            for module_item in module_items:
                # splits the module item into the base and extension
                # values
                module_base, module_extension = os.path.splitext(module_item)

                # in case the module extension is not
                # a python file, ignores the file
                if not module_extension == PYTHON_EXTENSION:
                    # continues the loop
                    continue

                # creates the "new" model package path from the
                # "parent" package path
                module_package_path = package_path + "." + module_base

                # creates the entity models (module) using system instance, the module package path
                # and the entity manager arguments, then uses the created entity models to extend
                # the entity models list
                _entity_models, _models, entity_models_module = self.create_base_models(system_instance, module_package_path, entity_manager_arguments, test_directory_path, extra_models, load_entity_manager = False)
                entity_models.extend(_entity_models)
                models.extend(_models)

            # loads (opens) the entity manager associated with the last entity models module,
            # (this assumes that every model is loaded in the same entity manager context)
            # this loading process only occurs in case the entity models is not empty
            # (at least one entity model is loaded)
            entity_models and entity_models_module.entity_manager.open()

        # otherwise it's a "simple" models module and must be imported
        # non recursively
        else:
            # creates the entity models (module) using the system instance, the package path,
            # the entity manager arguments the directory path and the extra models
            entity_models, models, entity_models_module = self.create_base_models(system_instance, package_path, entity_manager_arguments, directory_path, extra_models)

        # sets the entity models and models (tuple) in the
        # package path models map for the current package path
        self.package_path_models_map[package_path] = (entity_models, models)

        # sets the entity models in the system instance with the
        # base entity models module name
        setattr(system_instance, base_module_name, entity_models_module)

        # returns the list of (created) entity models
        return entity_models

    def create_controllers(self, system_instance, plugin_instance, package_path = None, prefix_name = None, directory_path = None, is_first = True):
        """
        Creates the various controllers for the given package path (dot notation based path
        relative to the caller (system) instance).
        For the controller creation one must provide the system instance (caller instance)
        and the plugin instance.

        An optional prefix name may be passed to be used in the variable names of
        the created controllers.
        The (base) directory path for controllers may be passed for module path resolution,
        in case it's not passed the system instance directory is used.

        After the controllers creation process the given system instance should have
        the created controllers set on it.

        @type system_instance: Object
        @param system_instance: The (system) instance that controls (owns) the
        created controllers, the controllers are going to be set on it.
        @type plugin_instance: Plugin
        @param plugin_instance: The plugin instance that own the system instance
        and so owns the controllers too.
        @type package_path: String
        @param package_path: Dot notation based path to the package to be
        used for controllers loading.
        @type prefix_name: String
        @param prefix_name: The prefix to be used on setting the controllers in
        the "owning" system instance.
        @type directory_path: String
        @param directory_path: The path to base directory to be used in the controller
        path resolution process.
        @type is_first: bool
        @param is_first: Auxiliary argument that controls if this is the first run (top recursion)
        of if it sis nested call.
        @rtype: List
        @return: The list containing the various created controllers.
        """

        # initializes the list that will hold
        # the various created controllers
        controllers = []

        # initializes the map that will hold the
        # controllers and the associated name
        controllers_map = {}

        # creates the map of default parameters for the creation
        # of the controllers
        default_parameters = {}

        # retrieves the "complete" module name for the system
        # instance to be used as target for the controller creation
        module_name = system_instance.__module__

        # splits the system instance module name into the package and
        # base module name parts then uses it to create the default
        # package path in case it's necessary
        package_name, _module_name = module_name.rsplit(".", 1)
        package_path = package_path or package_name + "." + CONTROLLERS_VALUE

        # splits the package path into package name and module name
        package_name, module_name = package_path.rsplit(".", 1)

        # retrieves the directory path taking into account the call module directory
        directory_path = directory_path or colony.libs.stack_util.get_instance_module_directory(system_instance)

        # creates the (possible) module directory path taking into
        # account the module name and then normalizes the path
        module_directory_path = os.path.join(directory_path, module_name)
        module_directory_path = os.path.normpath(module_directory_path)

        # in case the module directory path really exists,
        # this is the case where the referred module contains
        # modules each with different modules
        if os.path.isdir(module_directory_path):
            # imports the package module for back reference in the
            # internal importing of modules inside the modules (this is a mandatory
            # operation to avoid problems with the python interpreter), the custom
            # importer does not provide recursive import by default
            __import__(package_path)

            # retrieves the various module items from the
            # module directory path
            module_items = os.listdir(module_directory_path)

            # starts the module package paths list
            module_package_paths = []

            # iterates over all the (possible) module items in order
            # to filter only those o correspond to python modules
            for module_item in module_items:
                # splits the module item into the base and extension
                # values
                module_base, module_extension = os.path.splitext(module_item)

                # in case the module extension is not
                # a python file, ignores the file
                if not module_extension == PYTHON_EXTENSION:
                    # continues the loop
                    continue

                # creates the module package paths from the (current)
                # package path and the module base and then adds
                # it to the list of module package paths
                module_package_path = package_path + "." + module_base
                module_package_paths.append(module_package_path)

            # iterates over all the module package paths to reload
            # the associated modules (in case they've been created)
            for module_package_path in module_package_paths:
                # reloads the module associated with the given package
                # path to provide flushing of the contents, also flushes
                # the module package path from the globals
                colony.libs.import_util.reload_import(module_package_path)
                self._flush_globals(module_package_path)

            # iterates over all the module package paths to create
            # the appropriate controllers
            for module_package_path in module_package_paths:
                # creates the controllers for the module package path
                # and uses them to extend the "global" controllers list
                _controllers = self.create_controllers(system_instance, plugin_instance, module_package_path, prefix_name, module_directory_path, False)
                controllers.extend(_controllers)

            # starts the controllers (internal structures), this process
            # calls the start method in all controllers
            self._start_controllers(controllers)

            # sets the controllers list in the package path controllers
            # map for latter usage (controller destruction)
            self.package_path_controllers_map[package_path] = controllers

            # returns immediately (the directory
            # is interpreted there's no need to continue)
            return

        # in case this is the fist level of controller creation
        # a tentative reload should be applied to the package path,
        # in that case it also flushes the module package path
        # from the globals
        is_first and colony.libs.import_util.reload_import(package_path)
        is_first and self._flush_globals(module_package_path)

        # imports the controllers module with the mvc utils support
        controllers_module = self.import_module_mvc_utils(module_name, package_name, directory_path, system_instance)

        # retrieves the controllers module items
        controllers_module_items = dir(controllers_module)

        # initializes the exception controller accumulator value
        # that will hold the possibly found exception controller
        # during the iteration process
        exception_controller = None

        # retrieves the controller base name and converts it
        # to underscore notation
        exception_reference_name, _exception_base_name = self._convert_controller_name(EXCEPTION_CONTROLLER_VALUE, prefix_name)

        # in case the exception controller is already present in the system
        # instance it has already been created, must set it as the exception
        # handler in the default parameters
        if hasattr(system_instance, exception_reference_name):
            # retrieves the exception controller and sets it as the
            # exception handler in the default parameters
            _exception_controller = getattr(system_instance, exception_reference_name)
            default_parameters[EXCEPTION_HANDLER_VALUE] = _exception_controller

        # iterates over all the controllers module items
        # to create the appropriate controller instances
        for controllers_module_item in controllers_module_items:
            # checks if the controller module item name is a valid
            # controller name
            valid_controller_name = controllers_module_item.endswith(CONTROLLER_CAMEL_VALUE)

            # in case the controller module item does
            # not represent a valid controller name
            if not valid_controller_name:
                # continues the loop
                continue

            # retrieves the controller class and the controller class name
            controller_class = getattr(controllers_module, controllers_module_item)
            controller_class_name = controller_class.__name__

            # converts the controller class name into the normalized
            # controller base name according to the prefix value
            controller_reference_name, controller_base_name = self._convert_controller_name(controller_class_name, prefix_name)

            # creates the controller instance from the controller
            # class and uses the plugin instance and system instance
            # as the constructor arguments, sends also the default
            # parameters map to be used by the controller
            controller = self.create_controller(controller_class, (plugin_instance, system_instance), {}, False, default_parameters)

            # in case the current controller class is the exception
            # controller must signal it (and save it)
            if controller_class_name == EXCEPTION_CONTROLLER_VALUE:
                # saves the current controller as the exception controller
                exception_controller = controller

            # adds the controller to the list of controllers
            controllers.append(controller)

            # sets the controller in the current instance and in the
            # controllers map (for external access)
            setattr(system_instance, controller_reference_name, controller)
            controllers_map[controller_base_name] = controller

        # creates the controllers map name
        controllers_map_name = prefix_name and prefix_name + "_" + CONTROLLERS_VALUE or CONTROLLERS_VALUE

        # checks if the system instance already contains the controllers
        # map (in case it's not the first controller import)
        if hasattr(system_instance, controllers_map_name):
            # retrieves the "previous" controllers map that is defined
            # in the system instance and extends it with the new items
            # controller map (uses the fast map extension process)
            _controllers_map = getattr(system_instance, controllers_map_name)
            colony.libs.map_util.map_extend(_controllers_map, controllers_map, copy_base_map = False)

            # updates the current reference of the controllers map to
            # "point" to the "master" controllers map contained in the
            # system instance (for latter usage)
            controllers_map = _controllers_map
        # otherwise it's the first controller import and the controllers
        # map must be set on the system instance
        else:
            # sets the controllers map in the instance
            setattr(system_instance, controllers_map_name, controllers_map)

        # in case this is a top level creation of a controller the list
        # of controllers must be for the package path
        if is_first:
            # start the controllers and the associates them to the package
            # path in the package path controllers map
            self._start_controllers(controllers)
            self.package_path_controllers_map[package_path] = controllers

        # in case the exception controller has just been found, must set
        # it in the already imported controllers
        if exception_controller:
            # iterates over all the imported controllers to set the "additional"
            # exception handler default parameter
            for _controller_reference_name, controller in controllers_map.items():
                # sets the exception handler default parameter as the exception controller
                controller.set_default_parameter(EXCEPTION_HANDLER_VALUE, exception_controller)

        # returns the list of (created) controllers
        return controllers

    def destroy_base_models(self, entity_models, models, entity_manager_arguments):
        # retrieves the entity related plugins
        entity_manager_plugin = self.plugin.entity_manager_plugin
        business_helper_plugin = self.plugin.business_helper_plugin

        # retrieves the entity id from the entity manager arguments or sets
        # the id as undefined, this id is used to identify the correct
        # models module to be used, in case no id is found the default
        # (global) module will be used
        id = entity_manager_arguments.get(ID_VALUE, None)
        models_id = id or DEFAULT_VALUE
        models_module = self.models_modules_map.get(models_id, None)

        # generates the entity models map from the base entity models list
        # creating the map associating the class names with the classes
        entity_models_map = business_helper_plugin.generate_bundle_map(entity_models)

        # retrieves the entity manager from the entity manager
        # registry in the entity manager plugin for the given (models) id
        entity_manager = entity_manager_plugin.get_entity_manager(models_id)

        # in case the entity manager was correctly found (the
        # id value is valid and was found)
        if entity_manager:
            # uses the entity manager and shrinks it, removing the entity models
            # from it, all the entity manager references are updated
            entity_manager.shrink(entity_models_map)

        # iterates over all the entity models to be destroyed
        # to unset them from the models module
        for entity_model in entity_models:
            # retrieves the name of the base entity (model)
            # and uses it to delete the attribute in the models module
            entity_model_name = entity_model.__name__
            delattr(models_module, entity_model_name)

            # reverts the start method of the entity model
            # to the original state (back to old start)
            entity_model._start = entity_model._old_start

        # iterates over all the models to be destroyed
        # to unset them from the models module
        for model in models:
            # retrieves the name of the entity (model)
            # and uses it to delete the attribute in the models module
            model_name = model.__name__
            delattr(models_module, model_name)

            # reverts the start method of the model
            # to the original state (back to old start)
            model._start = model._old_start

    def destroy_models(self, system_instance, package_path = None, entity_manager_arguments = {}):
        # retrieves the "complete" module name for the system
        # instance to be used as target for the model destruction
        module_name = system_instance.__module__

        # splits the system instance module name into the package and
        # base module name parts then uses it to create the default
        # package path in case it's necessary
        package_name, _module_name = module_name.rsplit(".", 1)
        package_path = package_path or package_name + "." + MODELS_VALUE

        # reloads the module associated with the given package
        # path to provide flushing of the contents
        colony.libs.import_util.reload_import(package_path)

        # retrieves the entity models and the models from the package
        # path models map (one package path may contain various models)
        entity_models, models = self.package_path_models_map.get(package_path, [])

        # destroys the retrieved models (and entity models) for the
        # current entity manager arguments
        self.destroy_base_models(entity_models, models, entity_manager_arguments)

        # removes the reference to the package in the package
        # path models map
        del self.package_path_models_map[package_path]

    def destroy_controllers(self, system_instance, package_path = None, prefix_name = None,):
        # retrieves the "complete" module name for the system
        # instance to be used as target for the controller destruction
        module_name = system_instance.__module__

        # splits the system instance module name into the package and
        # base module name parts then uses it to create the default
        # package path in case it's necessary
        package_name, _module_name = module_name.rsplit(".", 1)
        package_path = package_path or package_name + "." + CONTROLLERS_VALUE

        # reloads the module associated with the given package
        # path to provide flushing of the contents
        colony.libs.import_util.reload_import(package_path)

        # retrieves the controllers from the package path controllers
        # map (one package path may contain various controllers)
        controllers = self.package_path_controllers_map.get(package_path, [])

        # creates the controllers map name and retrieves the controllers
        # map from the system instance
        controllers_map_name = prefix_name and prefix_name + "_" + CONTROLLERS_VALUE or CONTROLLERS_VALUE
        controllers_map = getattr(system_instance, controllers_map_name)

        # stops the controllers (internal structures), this process
        # calls the stop method in all controllers
        self._stop_controllers(controllers)

        # iterates over all the controllers to remove the references
        # from the system instance
        for controller in controllers:
            # retrieves the class from the controller and then uses
            # it to retrieve the class name
            controller_class = controller.__class__
            controller_class_name = controller_class.__name__

            # converts the controller class name into the normalized
            # controller base name according to the prefix value
            controller_reference_name, controller_base_name = self._convert_controller_name(controller_class_name, prefix_name)

            # removes the controller references in the system instance
            # and in the controllers map
            delattr(system_instance, controller_reference_name)
            del controllers_map[controller_base_name]

        # removes the reference to the package in the package
        # path controllers map
        del self.package_path_controllers_map[package_path]

    def create_file_manager(self, engine_name, connection_parameters = {}):
        """
        Creates a new file manager reference, to manage files
        in an indirect and adapted fashion.
        The created file manager respects the given engine name
        and connection parameters.

        @type engine_name: String
        @param engine_name: The name of the engine to be used in
        the file manager.
        @type connection_parameters: Dictionary
        @param connection_parameters: The parameters for the connection
        in the file manager.
        @rtype: FileManager
        @return: The created file manager.
        """

        # retrieves the file manager plugin
        file_manager_plugin = self.plugin.file_manager_plugin

        # creates a new file manager for the given engine and sets the connection
        # parameters on it (for loading)
        file_manager = file_manager_plugin.load_file_manager(engine_name)
        file_manager.set_connection_parameters(connection_parameters)

        # returns the created file manager
        return file_manager

    def generate_patterns(self, patterns, controller, prefix_name):
        # retrieves the controller class
        controller_class = controller.__class__

        # retrieves the controller class name
        controller_class_name = controller_class.__name__

        # retrieves the base name and converts it into
        # underscore notation
        base_name = controller_class_name[:-10]
        base_name = colony.libs.string_util.to_underscore(base_name)

        # converts the base name to plural
        controller_name_plural = colony.libs.string_util.pluralize(base_name)

        # iterates over all the symbols in the symbols
        # list
        for symbol in SYMBOLS_LIST:
            # unpacks the symbol, retrieving the name
            # the regex template and the operation
            method_name, regex_template, operation = symbol

            # checks if the controller contains the controller
            # handler method
            controller_contains_method = hasattr(controller, method_name)

            # in case the controller does not contain the
            # controller handler method
            if not controller_contains_method:
                # continues the loop
                continue

            # retrieves the controller handler method
            controller_handler_method = getattr(controller, method_name)

            # retrieves the regex value from the regex template
            # using the prefix name and the controller name (in plural)
            regex = regex_template % (prefix_name, controller_name_plural)

            # creates the pattern tuple
            pattern = (regex, controller_handler_method, operation)

            # adds the pattern (tuple) to the list of patterns
            patterns.append(pattern)

    def generate_entity_manager_arguments(self, plugin, base_entity_manager_arguments, parameters = {}):
        # creates the entity manager arguments map
        entity_manager_arguments = {}

        # copies the entity manager arguments constant to the new entity manager arguments
        colony.libs.map_util.map_copy_deep(base_entity_manager_arguments, entity_manager_arguments)

        # generates the entity manager path
        self._generate_entity_manager_path(plugin, entity_manager_arguments, parameters)

        # returns the entity manager arguments
        return entity_manager_arguments

    def _resolve_connection_parameters(self, connection_parameters):
        """
        Resolves the given connection parameters map, substituting
        the values with the resolved ones.

        @type connection_parameters: Dictionary
        @param connection_parameters: The connection parameters to be resolved.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

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
        to retrieve the entity classes (all entity class must inherit
        from this base class).
        @rtype: List
        @return: The list of entity classes in the module.
        """

        # creates the entity classes list
        entity_classes = []

        # retrieves the base entity models module map
        module_map = module.__dict__

        # iterates over all the module item names to check
        # if they are valid entity classes
        for module_item_name in module_map:
            # retrieves the module item from module and
            # them retrieves its type
            module_item = getattr(module, module_item_name)
            module_item_type = type(module_item)

            # in case the module item type is type,
            # the module item is subclass of the entity class and
            # the entity class is not a data reference (virtual)
            if module_item_type == types.TypeType and issubclass(module_item, entity_class) and (not hasattr(module_item, DATA_REFERENCE_VALUE) or module_item.data_reference == False):
                # adds the module item to the entity classes
                entity_classes.append(module_item)

        # returns the entity classes
        return entity_classes

    def _get_classes(self, module, base_class):
        """
        Retrieves all the (raw model) classes from the given module
        using the given (raw model) class as the reference to get
        the classes.

        @type module: Module
        @param module: The module to be used to retrieve the entity classes.
        @type base_class: Class
        @param base_class: The base class to be used as reference
        to retrieve the classes (all classes must inherit from this
        base class).
        @rtype: List
        @return: The list of classes in the module.
        """

        # creates the classes list
        classes = []

        # retrieves the base entity models module map
        module_map = module.__dict__

        # iterates over all the module item names to check
        # if they are valid entity classes
        for module_item_name in module_map:
            # retrieves the module item from module and
            # them retrieves its type
            module_item = getattr(module, module_item_name)
            module_item_type = type(module_item)

            # in case the module item type is type ands
            # the module item is subclass of the base class
            if module_item_type == types.TypeType and issubclass(module_item, base_class):
                # adds the module item to the classes
                classes.append(module_item)

        # returns the classes
        return classes

    def _get_extra_symbols_map(self, extra_entity_models, entity_class):
        """
        Retrieves the map that holds the extra symbols to be used
        during a models module import.

        @type extra_entity_models: List
        @param extra_entity_models: A list of extra entity models (modules)
        to be used to construct the extra symbols map.
        @type entity_class: EntityClass
        @param entity_class: The base entity class from all the
        entity classes must inherit (for reference).
        @rtype: Dictionary
        @return: A map containing all the extra symbols for the models
        module importing.
        """

        # starts the map to hold the extra symbols (for the importing
        # of the entity module)
        extra_symbols_map = {}

        # iterates over all the extra entity models (modules)
        for extra_entity_model_module in extra_entity_models:
            # retrieves the entity classes and the (raw model) classes
            # from the extra entity model module
            entity_classes = self._get_entity_classes(extra_entity_model_module, entity_class)
            classes = self._get_classes(extra_entity_model_module, RawModel)

            # iterates over all the entity classes to set them in
            # the extra symbols map
            for _entity_class in entity_classes:
                # sets the entity class in the extra symbols map
                extra_symbols_map[_entity_class.__name__] = _entity_class

            # iterates over all the classes to set them in
            # the extra symbols map
            for _class in classes:
                # sets the class in the extra symbols map
                extra_symbols_map[_class.__name__] = _class

        # returns the extra symbols map
        return extra_symbols_map

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

        # iterates over all the items in the module to set them
        # into the target class
        for item in dir(module):
            # retrieves the item value
            item_value = getattr(module, item)

            # retrieves the item value type
            item_value_type = type(item_value)

            # in case the item value type is not function
            if not item_value_type == types.FunctionType:
                # continues the loop
                continue

            # in case the items starts with class reference
            # the item is meant to be referenced as class method
            if item.startswith("_class_"):
                # retrieves the initial part of the item (name)
                # and then converts the item value (instance method)
                # to a class method (receives class as first argument)
                item = item[7:]
                item_value = classmethod(item_value)

            # in case the target class already contains a reference
            # to the given item, no overlap should occur
            if hasattr(target_class, item):
                # continues the loop, avoiding
                # the possible override of methods
                continue

            # sets the item in the target class
            setattr(target_class, item, item_value)

    def _get_module_path(self, module):
        """
        Retrieves the relative path to a given module,
        this path is relative to the system path entry used
        to import it.

        @type module: Module
        @param module: The module to retrieve the relative path.
        @rtype: String
        @return: The relative module path, from the system path
        entry used to import it.
        """

        # retrieves the module name and then splits it
        # to retrieve the module base name and the module name
        module_name = module.__module__
        module_base_name, module_name = module_name.rsplit(".", 1)

        # replaces the dot characters in the module base name
        # to retrieve the module base path
        module_base_path = module_base_name.replace(".", "/")

        # returns the module base path
        return module_base_path

    def _exists_target_module(self, target_module_name, globals):
        # checks if the target target module already exists in the
        # globals context or in the "system modules"
        exists_target_module = target_module_name in globals and target_module_name in sys.modules

        # returns the result of the existence test
        return exists_target_module

    def _get_target_module(self, target_module_name, globals):
        # tries to retrieve the target module
        target_module = globals.get(target_module_name, None)

        # in case the target module is not defined,
        # need to create a new one
        if not target_module:
            # creates the target module, using the underlying
            # python facilities for it
            target_module = imp.new_module(target_module_name)

            # adds the target module to the globals map
            # and sets it in the global modules reference map
            globals[target_module_name] = target_module
            sys.modules[target_module_name] = target_module

        # returns the target model
        return target_module

    def _convert_controller_name(self, controller_name, prefix_name = None):
        # converts the controller name into the underscore notation and then adds
        # the prefix path in case it's set (before that it has removed the controller's suffix)
        controller_base_name = controller_name[:-10]
        controller_base_name = colony.libs.string_util.to_underscore(controller_base_name)
        controller_reference_name = prefix_name and prefix_name + "_" + controller_base_name + "_" + CONTROLLER_VALUE or controller_base_name + "_" + CONTROLLER_VALUE

        # returns the reference (converted) controller name
        return controller_reference_name, controller_base_name

    def _generate_entity_manager_path(self, plugin, entity_manager_arguments, parameters):
        # retrieves the resources manager plugin
        resources_manager_plugin = self.plugin.resources_manager_plugin

        # retrieves the expected parameter values
        default_database_prefix = parameters.get("default_database_prefix", DEFAULT_DATABASE_PREFIX)
        default_database_sufix = parameters.get("default_database_sufix", DEFAULT_DATABASE_SUFFIX)
        configuration_plugin = parameters.get("configuration_plugin", plugin)

        # retrieves the system database file name resource
        system_database_filename_resource = resources_manager_plugin.get_resource("system.database.file_name")

        # in case the system database filename resource
        # is defined
        if system_database_filename_resource:
            # retrieves the system database filename suffix
            system_database_filename_suffix = system_database_filename_resource.data
        # otherwise
        else:
            # sets the system database filename suffix as the default one
            system_database_filename_suffix = default_database_sufix

        # creates the system database file name value using the prefix and suffix values
        system_database_filename = default_database_prefix + system_database_filename_suffix

        # retrieves the configuration plugin id
        configuration_plugin_id = configuration_plugin.id

        # creates the database file path using the configuration plugin id and the system database filename
        database_file_path = "%configuration:" + configuration_plugin_id + "%/" + system_database_filename

        # sets the file path in the entity manager arguments
        entity_manager_arguments[CONNECTION_PARAMETERS_VALUE][FILE_PATH_VALUE] = database_file_path

    def _start_controllers(self, controllers):
        """
        Starts the internal structures, by calling the start
        method in the given set of controllers.

        @type controllers: List
        @param controllers: The list of controllers to have
        the internal structures started.
        """

        # iterates over all the controllers to start
        # their internal structure
        for controller in controllers:
            # starts the controller internal structures
            controller._start_controller()

    def _stop_controllers(self, controllers):
        """
        Stops the internal structures, by calling the stop
        method in the given set of controllers.

        @type controllers: List
        @param controllers: The list of controllers to have
        the internal structures started.
        """

        # iterates over all the controllers to stop
        # their internal structure
        for controller in controllers:
            # stops the controller internal structures
            controller._stop_controller()

    def _flush_globals(self, package_path):
        """
        Flushes the globals map of the current instance,
        removing the module referred by the given path from
        it if necessary.

        @type package_path: String
        @param package_path: The (package) path to the module to be removed
        from the globals map.
        """

        # retrieve the map of globals from the
        # current environment
        globals_map = globals()

        # in case the package path is not present
        # in the current environment globals (noting
        # is to be done)
        if not package_path in globals_map:
            # returns immediately
            return

        # removes the package in the package
        # path from the globals map
        del globals_map[package_path]

class DataReferenceModel(object):
    """
    The base data reference model class to be used as top level
    parent of all the entity models that should be treated\
    in a transparent fashion towards the entity manager.

    This class is a simple stub class.
    """

    data_reference = True
    """ The signal for the data reference flag """

class RawModel(object):
    """
    The base (raw) model class to be used as top level
    parent of all the (base) model classes.

    This class is a simple stub class.
    """

    @classmethod
    def __new__(cls, _cls):
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

    def _start(self):
        pass

    def attach(self, force = True):
        pass

    def detach(self, force = True):
        pass

    def has_value(self, name):
        return name in self.__dict__

    def get_value(self, name, load_lazy = False):
        # in case the current model contains a
        # value for the attribute name (simple
        # case) it's returned normally
        if self.has_value(name):
            # returns the attribute value from
            # the current entity (normal retrieval)
            return getattr(self, name)

        # returns an invalid value, not possible to
        # return a relation using any of the approaches
        return None

def create_new_start(base_model):
    """
    Creates and sets the new start function based on the base
    entity model, this functions changes the entity mode state.

    The created function will override the default entity model
    start function and call it.
    The object is to provide an extra level of indirection in order
    to start additional entity structures.

    @type base_model: Model
    @param base_model: The base model to be used
    in the construction of the the new start function.
    @rtype: Function
    @return: The generated new start function.
    """

    # retrieves the base model old start function
    _old_start = base_model._start

    def _start(self):
        """
        The new start class method/function to be used by the
        the model.

        This method should be able to call the start method
        to add and initialize the "extra" model structures.
        """

        # calls the old start method, provides backwards
        # compatibility with the old implementation
        _old_start(self)

        # calls the model start method, initializing the
        # new data structures
        self._start_model()

    # sets the (new) start method in the base models
    # and then sets also the old star method in a
    # (backup) attribute for latter reset
    base_model._start = _start
    base_model._old_start = _old_start

    # returns the new start method, to be used
    # in the newly constructed classes
    return _start
