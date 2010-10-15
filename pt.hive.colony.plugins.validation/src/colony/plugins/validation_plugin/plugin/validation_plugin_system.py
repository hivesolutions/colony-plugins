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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import os

DEFAULT_JSON_ENCODING = "Cp1252"
""" The default json encoding """

BUILD_AUTOMATION_FILE_PATH_VALUE = "build_automation_file_path"
""" The build automation file path value """

CAPABILITIES_VALUE = "capabilities"
""" The capabilities value """

CAPABILITIES_ALLOWED_VALUE = "capabilities_allowed"
""" The capabilities allowed value """

DEPENDENCIES_VALUE = "dependencies"
""" The dependencies value """

ID_VALUE = "id"
""" The id value """

MAIN_FILE_VALUE = "main_file"
""" The main file value """

MESSAGE_VALUE = "message"
""" The message value """

PLATFORM_VALUE = "platform"
""" The platform value """

PLUGIN_ID_VALUE = "plugin_id"
""" The plugin id value """

PLUGIN_PATH_VALUE = "plugin_path"
""" The plugin path value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

PYTHON_VALUE = "python"
""" The python value """

RESOURCES_VALUE = "resources"
""" The resources value """

VERSION_VALUE = "version"
""" The version value """

SYSTEM_FILE_DIRECTORY_DEPTH = 2
""" The directory depth at which system files should be located """

DEFAULT_BAF_ENCODING = "Cp1252"
""" The default baf encoding """

DEFAULT_JSON_ENCODING = "Cp1252"
""" The default json encoding """

INIT_FILE_NAME = "__init__.py"
""" The init file name """

MAIN_MODULE_SEPARATOR = "."
""" The main module separator """

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

WINDOWS_DIRECTORY_SEPARATOR = "\\"
""" The windows directory separator """

JSON_FILE_EXTENSION = ".json"
""" The json file extension """

PYTHON_FILE_EXTENSION = ".py"
""" The python file extension """

PYTHON_INIT_FILE_NAME = "__init__.py"
""" The python init file name """

SYSTEM_FILE_NAME_ENDING = "_system.py"
""" The system file name ending """

PLUGIN_MODULE_NAME_ENDING = "_plugin"
""" The plugin module name ending """

RESOURCES_DIRECTORY = "/resources"
""" The resources directory """

BASE_PLUGIN_DIRECTORY_VARIABLE = "$base{plugin_directory}"
""" The base plugin directory variable """

BUILD_AUTOMATION_ITEM_CAPABILITY = "build_automation_item"
""" The build automation item capability """

BUILD_AUTOMATION_FILE_PATH_ATTRIBUTE = "build_automation_file_path"
""" The build automation file path attribute """

RESOURCE_FILE_NAME_EXCLUSION_LIST = (".svn", "entries", "all-wcprops", "dir-prop-base")
""" The resource file name exclusion list """

RESOURCE_FILE_EXTENSION_EXCLUSION_LIST = (".svn", ".svn-base", ".svn-revert", ".class", ".pyc", ".tmp")
""" The resource file extension exclusion list """

BUILD_AUTOMATION_ITEM_CAPABILITY_PLUGIN_EXCLUSION_LIST = ("pt.hive.colony.plugins.build.automation")
""" The list of plugins that are allowed not to have the build automation item capability """

BUILD_AUTOMATION_FILE_SPECIFICATION_FILE_REGEX = re.compile("<specification_file>(.*?)</specification_file>")
""" The build automation file specification file regex """

PLUGIN_DESCRIPTOR_ATTRIBUTES_MAP = {"id" : "original_id",
                                    "sub_platforms" : "platforms",
                                    "name" : "name",
                                    "short_name" : "short_name",
                                    "description" : "description",
                                    "version" : "version",
                                    "author" : "author",
                                    "capabilities" : "capabilities"}
""" Defines the association between attributes in the plugin descriptor file and the plugin itself """

class ValidationPlugin:
    """
    The validation plugin class.
    """

    validation_plugin_plugin = None
    """ The validation plugin plugin """

    def __init__(self, validation_plugin_plugin):
        """
        Constructor of the class.

        @type validation_plugin_plugin: ValidationPluginPlugin
        @param validation_plugin_plugin: The validation plugin plugin.
        """

        self.validation_plugin_plugin = validation_plugin_plugin

    def validate_plugins(self):
        # initializes the validation errors list
        validation_errors = []

        # retrieves all plugins
        plugins = self.validation_plugin_plugin.manager.get_all_plugins()

        # validates all plugins
        for plugin in plugins:
            self._validate_plugin(plugin, validation_errors)

        # returns the validation errors
        return validation_errors

    def validate_plugin(self, plugin_id):
        # initializes the validation errors list
        validation_errors = []

        # retrieves the plugin
        plugin = self.validation_plugin_plugin.manager._get_plugin_by_id(plugin_id)

        # validates the plugin
        self._validate_plugin(plugin, validation_errors)

        # returns the validation errors
        return validation_errors

    def _validate_plugin(self, plugin, validation_errors):
        # retrieves the plugin information
        plugin_information = PluginInformation(plugin)

        # checks if the plugin system file exists
        if not plugin_information.plugin_system_file_path:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' is missing its system file" % plugin_information.plugin_module_name)

            # returns since nothing else can be tested
            return

        # validates the plugin directory structure
        self._validate_plugin_directory_structure(plugin_information, validation_errors)

        # validates the plugin file
        self._validate_plugin_file(plugin_information, validation_errors)

        # checks that if the plugin descriptor file exists
        if not os.path.exists(plugin_information.plugin_descriptor_file_path):
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' is missing file '%s'" % (plugin_information.plugin_module_name, plugin_information.plugin_descriptor_file_path))

            # returns since no more validations can be performed
            return

        # validates the plugin descriptor file
        self._validate_plugin_descriptor_file(plugin_information, validation_errors)

        # validates the build automation file
        self._validate_build_automation_file(plugin_information, validation_errors)

    def _validate_plugin_directory_structure(self, plugin_information, validation_errors):
        # retrieves the base plugin system directory path
        base_plugin_system_directory_path = plugin_information.plugin_system_directory_path.replace(plugin_information.plugin_path, "")

        # removes the trailing slash from the beginning of the path
        base_plugin_system_directory_path = base_plugin_system_directory_path[1:]

        # splits the base plugin system directory path
        base_plugin_system_directory_path_tokens = base_plugin_system_directory_path.split(UNIX_DIRECTORY_SEPARATOR)

        # checks that the system directory path has the appropriate depth
        if not len(base_plugin_system_directory_path_tokens) == SYSTEM_FILE_DIRECTORY_DEPTH:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' doesn't have a valid directory structure leading to the system file" % plugin_information.plugin_module_name)

    def _validate_plugin_file(self, plugin_information, validation_errors):
        # validates the plugin's class name
        self.__validate_plugin_class_name(plugin_information, validation_errors)

        # validates the plugin's capabilities
        self.__validate_plugin_capabilities(plugin_information, validation_errors)

        # validates the plugin's init files
        self.__validate_plugin_init_files(plugin_information, validation_errors)

        # validates the plugin's main modules
        self.__validate_plugin_main_modules(plugin_information, validation_errors)

    def __validate_plugin_class_name(self, plugin_information, validation_errors):
        # retrieves the plugin
        plugin = plugin_information.plugin

        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin file path
        plugin_file_path = plugin_information.plugin_file_path

        # retrieves the plugin class name
        plugin_class_name = plugin_information.plugin_class_name

        # checks if the plugin class name matches the one computed from its module name
        if not plugin_class_name == plugin.__class__.__name__:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' has a class name '%s' that does not match its file name '%s'" % (plugin_module_name, plugin.__class__.__name__, plugin_file_path))

    def __validate_plugin_capabilities(self, plugin_information, validation_errors):
        # retrieves the plugin
        plugin = plugin_information.plugin

        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # creates a set with the plugin capabilities
        plugin_capabilities_set = set(plugin.capabilities)

        # creates a list with the unique plugin capabilities
        unique_plugin_capabilities = list(plugin_capabilities_set)

        # retrieves the number of unique plugin capabilities
        number_unique_plugin_capabilities = len(unique_plugin_capabilities)

        # checks for duplicate capabilities in the plugin
        if not len(plugin.capabilities) == number_unique_plugin_capabilities:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' has duplicate capabilities" % plugin_module_name)

        # returns in case the plugin is in the build automation item capability exclusion list
        if plugin.id in BUILD_AUTOMATION_ITEM_CAPABILITY_PLUGIN_EXCLUSION_LIST:
            return

        # checks if the plugin has a build automation item capability
        if not BUILD_AUTOMATION_ITEM_CAPABILITY in plugin.capabilities:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' is missing 'build_automation_item' capability" % plugin_module_name)

    def __validate_plugin_init_files(self, plugin_information, validation_errors):
        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # checks that all plugin init files exist
        for plugin_resource_main_module_init_file_path in plugin_information.plugin_resource_main_module_init_file_paths:
            if not os.path.exists(plugin_resource_main_module_init_file_path):
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' is missing an init file '%s'" % (plugin_module_name, plugin_resource_main_module_init_file_path))

    def __validate_plugin_main_modules(self, plugin_information, validation_errors):
        # retrieves the plugin
        plugin = plugin_information.plugin

        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin main module file paths
        plugin_main_module_file_paths = plugin_information.plugin_main_module_file_paths

        # retrieves the plugin resource main modules
        plugin_resource_main_modules = plugin_information.plugin_resource_main_modules

        # creates a set with the plugin main_modules
        plugin_main_modules_set = set(plugin.main_modules)

        # creates a list with the unique plugin main_modules
        unique_plugin_main_modules = list(plugin_main_modules_set)

        # retrieves the number of unique plugin main_modules
        number_unique_plugin_main_modules = len(unique_plugin_main_modules)

        # checks for duplicate main modules in the plugin
        if not len(plugin.main_modules) == number_unique_plugin_main_modules:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' has duplicate main modules" % plugin_module_name)

        # checks that plugin's main module file paths exist
        for plugin_main_module_file_path in plugin_main_module_file_paths:
            if not os.path.exists(plugin_main_module_file_path):
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' is missing main module file '%s'" % (plugin_module_name, plugin_main_module_file_path))

        # checks that the plugin has declarations for all main modules found in the plugin's resources
        for plugin_resource_main_module in plugin_resource_main_modules:
            if not plugin_resource_main_module in plugin.main_modules:
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' is missing main module declaration '%s'" % (plugin_module_name, plugin_resource_main_module))

    def _validate_plugin_descriptor_file(self, plugin_information, validation_errors):
        # retrieves the plugin descriptor file path value
        plugin_descriptor_file_path = plugin_information.plugin_descriptor_file_path

        try:
            # retrieves the plugin descriptor data
            plugin_descriptor_data = self.get_json_data(plugin_descriptor_file_path)
        except:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' has invalid syntax" % plugin_descriptor_file_path)
        else:
            # validates the plugin descriptor file attributes
            self.__validate_plugin_descriptor_file_attributes(plugin_information, plugin_descriptor_data, validation_errors)

            # validates the plugin descriptor file capabilities
            self.__validate_plugin_descriptor_file_capabilities(plugin_information, plugin_descriptor_data, validation_errors)

            # validates the plugin descriptor file capabilities allowed
            self.__validate_plugin_descriptor_file_capabilities_allowed(plugin_information, plugin_descriptor_data, validation_errors)

            # validates the plugin descriptor file dependencies
            self.__validate_plugin_descriptor_file_dependencies(plugin_information, plugin_descriptor_data, validation_errors)

            # validates the plugin descriptor file resources
            self.__validate_plugin_descriptor_file_resources(plugin_information, plugin_descriptor_data, validation_errors)

    def __validate_plugin_descriptor_file_attributes(self, plugin_information, plugin_descriptor_data, validation_errors):
        # retrieves the plugin
        plugin = plugin_information.plugin

        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin file name
        plugin_file_name = plugin_information.plugin_file_name

        # checks that the platform value is correct
        if not plugin_descriptor_data[PLATFORM_VALUE] == PYTHON_VALUE:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has invalid attribute 'platform'" % plugin_module_name)

        # searches for plugin descriptor attributes with invalid content
        for plugin_descriptor_attribute_name, plugin_attribute_name in PLUGIN_DESCRIPTOR_ATTRIBUTES_MAP.items():
            # retrieves the plugin descriptor data attribute
            plugin_descriptor_data_attribute = plugin_descriptor_data[plugin_descriptor_attribute_name]

            # retrieves the plugin attribute
            plugin_attribute = getattr(plugin, plugin_attribute_name)

            # checks if the attributes are the same
            if not plugin_descriptor_data_attribute == plugin_attribute:
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has invalid attribute '%s'" % (plugin_module_name, plugin_descriptor_attribute_name))

        # checks that the main file value is correct
        if not plugin_descriptor_data[MAIN_FILE_VALUE] == plugin_file_name:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has invalid attribute 'main_file'" % plugin_module_name)

    def __validate_plugin_descriptor_file_capabilities(self, plugin_information, plugin_descriptor_data, validation_errors):
        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin descriptor data capabilities
        plugin_descriptor_data_capabilities = plugin_descriptor_data[CAPABILITIES_VALUE]

        # creates a set with the plugin descriptor data capabilities
        plugin_descriptor_data_capabilities_set = set(plugin_descriptor_data_capabilities)

        # creates a list with the unique plugin descriptor data capabilities
        unique_plugin_descriptor_data_capabilities = list(plugin_descriptor_data_capabilities_set)

        # retrieves the number of unique plugin descriptor data capabilities
        number_unique_plugin_descriptor_data_capabilities = len(unique_plugin_descriptor_data_capabilities)

        # checks for duplicate capabilities
        if not len(plugin_descriptor_data_capabilities) == number_unique_plugin_descriptor_data_capabilities:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has duplicate capabilities" % plugin_module_name)

    def __validate_plugin_descriptor_file_capabilities_allowed(self, plugin_information, plugin_descriptor_data, validation_errors):
        # retrieves the plugin
        plugin = plugin_information.plugin

        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin descriptor data capabilities allowed
        plugin_descriptor_data_capabilities_allowed = plugin_descriptor_data[CAPABILITIES_ALLOWED_VALUE]

        # creates a set with the plugin descriptor data capabilities allowed
        plugin_descriptor_data_capabilities_allowed_set = set(plugin_descriptor_data_capabilities_allowed)

        # creates a list with the unique plugin descriptor data capabilities allowed
        unique_plugin_descriptor_data_capabilities_allowed = list(plugin_descriptor_data_capabilities_allowed_set)

        # retrieves the number of unique plugin descriptor data capabilities allowed
        number_unique_plugin_descriptor_data_capabilities_allowed = len(unique_plugin_descriptor_data_capabilities_allowed)

        # checks for duplicate capabilities allowed
        if not len(plugin_descriptor_data_capabilities_allowed) == number_unique_plugin_descriptor_data_capabilities_allowed:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has duplicate capabilities allowed" % plugin_module_name)

        # checks if the number of capabilities allowed is the same as in the plugin
        if not len(plugin_descriptor_data_capabilities_allowed) == len(plugin.capabilities_allowed):
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file doesn't have the same number of capabilities allowed as its plugin" % plugin_module_name)

            # returns since nothing else can be tested
            return

        # checks that the capabilites allowed are the same
        for capability_allowed_index in range(len(plugin.capabilities_allowed)):
            # retrieves the capability allowed
            capability_allowed = plugin.capabilities_allowed[capability_allowed_index]

            # retrieves the plugin descriptor data capability allowed
            plugin_descriptor_data_capability_allowed = plugin_descriptor_data_capabilities_allowed[capability_allowed_index]

            # converts the capability allowed to a tuple in case it is one
            if plugin_descriptor_data_capability_allowed.startswith("(") and plugin_descriptor_data_capability_allowed.endswith(")"):
                plugin_descriptor_data_capability_allowed = eval(plugin_descriptor_data_capability_allowed)

            # checks if the capability allowed is the same as in the plugin
            if not plugin_descriptor_data_capability_allowed == capability_allowed:
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has invalid attribute 'capabilities_allowed'" % plugin_module_name)

                # returns now that the attribute has been considered invalid
                return

    def __validate_plugin_descriptor_file_dependencies(self, plugin_information, plugin_descriptor_data, validation_errors):
        # retrieves the plugin
        plugin = plugin_information.plugin

        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin's dependencies
        plugin_dependencies = plugin.get_all_plugin_dependencies()

        # retrieves the plugin descriptor data dependencies
        plugin_descriptor_data_dependencies = plugin_descriptor_data[DEPENDENCIES_VALUE]

        # checks if the number of plugin dependencies is the same as in the plugin descriptor file
        if not len(plugin_dependencies) == len(plugin_descriptor_data_dependencies):
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file doesn't have the same number of dependencies as its plugin" % plugin_module_name)

            # returns since no more validations can be performed
            return

        # checks that the dependencies in the plugin descriptor file match the plugin's and are in the same order
        for plugin_dependency_index in range(len(plugin_dependencies)):
            # retrieves the plugin's dependency
            plugin_dependency = plugin_dependencies[plugin_dependency_index]

            # retrieves the plugin's json data dependency
            plugin_descriptor_data_dependency = plugin_descriptor_data_dependencies[plugin_dependency_index]

            # retrieves the plugin descriptor data dependency id
            plugin_descriptor_data_dependency_id = plugin_descriptor_data_dependency[ID_VALUE]

            # checks if the dependency ids match
            if not plugin_descriptor_data_dependency_id == plugin_dependency.plugin_id:
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file dependency '%s' doesn't exist or is not in correct order" % (plugin_module_name, plugin_descriptor_data_dependency_id))

            # retrieves the plugin descriptor data dependency version
            plugin_descriptor_data_dependency_version = plugin_descriptor_data_dependency[VERSION_VALUE]

            # checks if the dependency versions match
            if not plugin_descriptor_data_dependency_version == plugin_dependency.plugin_version:
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file dependency '%s' doesn't have the same version as its plugin" % (plugin_module_name, plugin_descriptor_data_dependency_id))

    def __validate_plugin_descriptor_file_resources(self, plugin_information, plugin_descriptor_data, validation_errors):
        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin resource file paths
        plugin_resource_file_paths = plugin_information.plugin_resource_file_paths

        # retrieves the plugin descriptor data resources
        plugin_descriptor_data_resources = plugin_descriptor_data[RESOURCES_VALUE]

        # creates a set with the plugin descriptor data resources
        plugin_descriptor_data_resources_set = set(plugin_descriptor_data_resources)

        # creates a list with the unique plugin descriptor data resources
        unique_plugin_descriptor_data_resources = list(plugin_descriptor_data_resources_set)

        # retrieves the number of unique plugin descriptor data resources
        number_unique_plugin_descriptor_data_resources = len(unique_plugin_descriptor_data_resources)

        # checks for duplicate resource paths
        if not len(plugin_descriptor_data_resources) == number_unique_plugin_descriptor_data_resources:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has duplicate resource paths" % plugin_module_name)

        # checks if the list of resources if of the same size
        if not len(plugin_resource_file_paths) == len(plugin_descriptor_data_resources):
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file doesn't have the same number of resources as its plugin" % plugin_module_name)

            # returns since nothing else can be tested
            return

        # looks for resource declarations in the descriptor for each of the discovered resource files
        for plugin_resource_file_path_index in range(len(plugin_resource_file_paths)):
            # retrieves the plugin resource file path
            plugin_resource_file_path = plugin_resource_file_paths[plugin_resource_file_path_index]

            # checks if there's a resource declaration for the resource file
            if not plugin_resource_file_path == plugin_descriptor_data_resources[plugin_resource_file_path_index]:
                # logs the appropriate message depending on whether the declaration is missing or is out of order
                if plugin_resource_file_path in plugin_descriptor_data_resources:
                    self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file has misordered resource declaration for file '%s'" % (plugin_module_name, plugin_resource_file_path))
                else:
                    self.add_validation_error(validation_errors, plugin_information, "'%s' json descriptor file is missing resource declaration for file '%s'" % (plugin_module_name, plugin_resource_file_path))

    def _validate_build_automation_file(self, plugin_information, validation_errors):
        # retrieves the plugin
        plugin = plugin_information.plugin

        # retrieves the plugin module name
        plugin_module_name = plugin_information.plugin_module_name

        # retrieves the plugin path
        plugin_path = plugin_information.plugin_path

        # checks if the build automation file path is specified in the plugin attributes
        if not BUILD_AUTOMATION_FILE_PATH_ATTRIBUTE in plugin.attributes:
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' is missing the 'build_automation_file_path' attribute" % plugin_module_name)

            # returns since nothing else can be tested
            return

        # retrieves the base build automation file path
        base_build_automation_file_path = plugin.attributes[BUILD_AUTOMATION_FILE_PATH_VALUE]

        # retrieves the build automation file path
        build_automation_file_path = base_build_automation_file_path.replace(BASE_PLUGIN_DIRECTORY_VARIABLE, plugin_path)

        # checks for the existence of the build automation file
        if not build_automation_file_path or not os.path.exists(build_automation_file_path):
            # logs the validation error
            self.add_validation_error(validation_errors, plugin_information, "'%s' is missing the referenced build automation file '%s'" % (plugin_module_name, build_automation_file_path))

            # returns since nothing else can be tested
            return

        # opens the build automation file
        build_automation_file = open(build_automation_file_path, "rb")

        # reads the build automation file's data
        build_automation_file_data = build_automation_file.read()

        # decodes the build automation file data
        build_automation_file_data = build_automation_file_data.decode(DEFAULT_BAF_ENCODING)

        # closes the build automation file
        build_automation_file.close()

        # retrieves the specification file paths
        specification_file_paths = BUILD_AUTOMATION_FILE_SPECIFICATION_FILE_REGEX.findall(build_automation_file_data)

        # checks if the defined specification file paths exist
        for specification_file_path in specification_file_paths:
            # sets the plugin path in the specification file path
            specification_file_path = specification_file_path.replace(BASE_PLUGIN_DIRECTORY_VARIABLE, plugin_path)

            # checks if the specification file exists
            if not os.path.exists(specification_file_path):
                # logs the validation error
                self.add_validation_error(validation_errors, plugin_information, "'%s' build automation file '%s' references missing specification file '%s'" % (plugin_module_name, build_automation_file_path, specification_file_path))

    def add_validation_error(self, validation_errors, plugin_information, validation_error_message):
        # defines the validation error map
        validation_error_map = {PLUGIN_ID_VALUE : plugin_information.plugin.id,
                                PLUGIN_PATH_VALUE : plugin_information.plugin_file_path,
                                MESSAGE_VALUE : validation_error_message}

        # adds the validation error map to the validation errors list
        validation_errors.append(validation_error_map)

    def get_json_data(self, json_file_path):
        # reads the json file
        json_file = open(json_file_path, "rb")

        # reads the data from the json file
        json_file_data = json_file.read()

        # closes the json file
        json_file.close()

        # decodes the json file data
        json_file_data = json_file_data.decode(DEFAULT_JSON_ENCODING)

        # loads the json data from the json file
        json_data = self.validation_plugin_plugin.json_plugin.loads(json_file_data)

        return json_data

class PluginInformation:

    plugin = None
    """ The plugin """

    plugin_path = None
    """ The plugin's path """

    plugin_module_name = None
    """ The plugin's module name """

    plugin_class_name = None
    """ The plugin's class name """

    plugin_file_name = None
    """ The plugin's file name """

    plugin_file_path = None
    """ The plugin's file path """

    plugin_system_file_name = None
    """ The plugin's system file name """

    plugin_system_file_path = None
    """ The plugin system file path """

    plugin_system_directory_path = None
    """ The plugin system directory path """

    plugin_root_directory_path = None
    """ The path to the plugin's root directory """

    plugin_root_init_file_path = None
    """ The path to the plugin's root init file """

    plugin_descriptor_file_name = None
    """ The plugin's descriptor file name """

    plugin_descriptor_file_path = None
    """ The plugin's descriptor file path """

    plugin_file_paths = []
    """ The plugin file paths """

    plugin_resource_file_paths = []
    """ The plugin's resource file paths """

    plugin_main_module_file_paths = []
    """ The file paths for the plugin's main module declarations """

    plugin_resource_main_module_file_paths = []
    """ The file paths for the plugin resources that are main modules """

    plugin_resource_main_modules = []
    """ The main module declarations for the plugin resources that are main modules """

    def __init__(self, plugin):
        self.plugin = plugin
        self.plugin_path = None
        self.plugin_module_name = None
        self.plugin_class_name = None
        self.plugin_file_name = None
        self.plugin_file_path = None
        self.plugin_system_file_name = None
        self.plugin_system_file_path = None
        self.plugin_system_directory_path = None
        self.plugin_root_directory_path = None
        self.plugin_root_init_file_path = None
        self.plugin_descriptor_file_name = None
        self.plugin_descriptor_file_path = None
        self.plugin_file_paths = []
        self.plugin_resource_file_paths = []
        self.plugin_main_module_file_paths = []
        self.plugin_resource_main_module_file_paths = []
        self.plugin_resource_main_module_init_file_paths = []
        self.plugin_resource_main_modules = []

        # loads the plugin information
        self.load()

    def load(self):
        # retrieves the plugin path
        plugin_path = self.plugin.manager.get_plugin_path_by_id(self.plugin.id)

        # normalizes the plugin path
        normalized_plugin_path = self.normalize_path(plugin_path)

        # stores the normalized plugin path
        self.plugin_path = normalized_plugin_path

        # sets the plugin module name
        self.plugin_module_name = self.plugin.manager.get_plugin_module_name_by_id(self.plugin.id)

        # tokenizes the plugin module name
        plugin_module_name_tokens = self.plugin_module_name.split("_")

        # sets the plugin class name
        self.plugin_class_name = "".join([plugin_module_name_token.capitalize() for plugin_module_name_token in plugin_module_name_tokens])

        # sets the plugin file name
        self.plugin_file_name = self.plugin_module_name + PYTHON_FILE_EXTENSION

        # sets the plugin file path
        self.plugin_file_path = self.plugin_path + UNIX_DIRECTORY_SEPARATOR + self.plugin_module_name + PYTHON_FILE_EXTENSION

        # sets the plugin system file name
        self.plugin_system_file_name = self.plugin_module_name[:-1 * len(PLUGIN_MODULE_NAME_ENDING)] + SYSTEM_FILE_NAME_ENDING

        # sets the plugin descriptor file name
        self.plugin_descriptor_file_name = self.plugin_module_name + JSON_FILE_EXTENSION

        # sets the plugin descriptor file path
        self.plugin_descriptor_file_path = self.plugin_path + UNIX_DIRECTORY_SEPARATOR +  self.plugin_descriptor_file_name

        # loads the plugin paths
        self._load_plugin_paths()

    def _load_plugin_paths(self):
        # sets the plugin file paths
        self.plugin_file_paths = self.get_file_paths(self.plugin_path)

        # retrieves the prefixed plugin system file name
        prefixed_plugin_system_file_name = UNIX_DIRECTORY_SEPARATOR + self.plugin_system_file_name

        # looks for the plugin system file in the provided file paths
        for plugin_file_path in self.plugin_file_paths:
            if prefixed_plugin_system_file_name in plugin_file_path:
                self.plugin_system_file_path = plugin_file_path
                break

        # returns in case no plugin system file was found
        if not self.plugin_system_file_path:
            return

        # splits the plugin system file path into plugin system directory path and plugin system file name
        self.plugin_system_directory_path, self.plugin_system_file_name = os.path.split(self.plugin_system_file_path)

        # tokenizes the plugin system file path
        plugin_system_file_path_tokens = self.plugin_system_file_path.split(UNIX_DIRECTORY_SEPARATOR)

        # retrieves the plugin root directory path
        self.plugin_root_directory_path = plugin_system_file_path_tokens[plugin_system_file_path_tokens.index(PLUGINS_VALUE) + 1]

        # retrieves the plugin root init file path
        self.plugin_root_init_file_path = self.plugin_root_directory_path + UNIX_DIRECTORY_SEPARATOR + INIT_FILE_NAME

        # loads the plugin resource file paths
        self.__load_plugin_resource_file_paths()

        # loads the plugin main module file paths
        self.__load_plugin_main_module_file_paths()

        # loads the plugin resource main module file paths
        self.__load_plugin_resource_main_module_file_paths()

        # loads the plugin resource main module init file paths
        self.__load_plugin_resource_main_module_init_file_paths()

        # loads the pluguin resource main modules
        self.__load_plugin_resource_main_modules()

    def __load_plugin_resource_file_paths(self):
        # retrieves the plugin's resource file paths
        plugin_resource_file_paths = self.get_file_paths(self.plugin_system_directory_path)

        # sets the plugin resource file paths
        plugin_resource_file_paths = [plugin_resource_file_path.replace(self.plugin_path, "")[1:] for plugin_resource_file_path in plugin_resource_file_paths if self.is_valid_plugin_resource_file_path(plugin_resource_file_path)]

        # adds the undetectable plugin resource file paths
        if self.plugin_root_init_file_path in plugin_resource_file_paths:
            plugin_resource_file_paths = [self.plugin_file_name] + plugin_resource_file_paths
        else:
            plugin_resource_file_paths = [self.plugin_file_name, self.plugin_root_init_file_path] + plugin_resource_file_paths

        # sets the plugin resource file paths
        self.plugin_resource_file_paths = plugin_resource_file_paths

    def __load_plugin_main_module_file_paths(self):
        # loads the main module paths
        for main_module in self.plugin.main_modules:
            # retrieves the base main module file path
            base_main_module_file_path = main_module.replace(MAIN_MODULE_SEPARATOR, UNIX_DIRECTORY_SEPARATOR) + PYTHON_FILE_EXTENSION

            # normalizes the base main module file path
            base_main_module_file_path = self.normalize_path(base_main_module_file_path)

            # retrieves the full main module file path
            main_module_file_path = self.plugin_path + UNIX_DIRECTORY_SEPARATOR + base_main_module_file_path

            # adds the main module file path to the plugin main module file paths
            self.plugin_main_module_file_paths.append(main_module_file_path)

    def __load_plugin_resource_main_module_file_paths(self):
        # sets the plugin resource main module file paths
        self.plugin_resource_main_module_file_paths = [plugin_resource_file_path for plugin_resource_file_path in self.plugin_resource_file_paths if self.is_valid_main_module_file_path(plugin_resource_file_path, self.plugin_path)]

    def __load_plugin_resource_main_module_init_file_paths(self):
        # collects init paths from the plugin resource main module file paths
        for plugin_resource_main_module_file_path in self.plugin_resource_main_module_file_paths:
            # splits the plugin resource main module file path into directory and file name
            plugin_resource_main_module_directory_path, _main_module_file_name = os.path.split(plugin_resource_main_module_file_path)

            # tokenizes the plugin resource main module directory path
            plugin_resource_main_module_directory_path_tokens = plugin_resource_main_module_directory_path.split(UNIX_DIRECTORY_SEPARATOR)

            # initializes the directory path
            directory_path = None

            # crawls the main module path directories collecting init file paths
            for plugin_resource_main_module_directory_path_token in plugin_resource_main_module_directory_path_tokens:
                # concatenates the token to the directory path
                if not directory_path:
                    directory_path = plugin_resource_main_module_directory_path_token
                else:
                    directory_path += UNIX_DIRECTORY_SEPARATOR + plugin_resource_main_module_directory_path_token

                # creates the plugin resource main module init file path
                plugin_resource_main_module_init_file_path = self.plugin_path + UNIX_DIRECTORY_SEPARATOR + directory_path + UNIX_DIRECTORY_SEPARATOR + INIT_FILE_NAME

                # adds the plugin resource main module init file path to the list in case it isn't in it yet
                if not plugin_resource_main_module_init_file_path in self.plugin_resource_main_module_init_file_paths:
                    self.plugin_resource_main_module_init_file_paths.append(plugin_resource_main_module_init_file_path)

    def __load_plugin_resource_main_modules(self):
        # collects the main module declarations for the discovered resource main module file paths
        for main_module_file_path in self.plugin_resource_main_module_file_paths:
            # splits the main module path into the main module directory path and the main module file name
            main_module_directory_path, main_module_file_name = os.path.split(main_module_file_path)

            # defines the main module directory path
            main_module_directory_path = main_module_directory_path.replace(self.plugin_path, "")

            # splits the main module file name into file name and extension
            base_main_module_file_name, _main_module_file_extension = os.path.splitext(main_module_file_name)

            # retrieves the base main module file path
            base_main_module_file_path = main_module_directory_path + UNIX_DIRECTORY_SEPARATOR + base_main_module_file_name

            # retrieves the main module from the base main module file path
            main_module = base_main_module_file_path.replace(UNIX_DIRECTORY_SEPARATOR, MAIN_MODULE_SEPARATOR)

            # replaces windows directory separators with main module separators
            main_module = main_module.replace(WINDOWS_DIRECTORY_SEPARATOR, MAIN_MODULE_SEPARATOR)

            # appends the main module to the list of plugin resource main modules
            self.plugin_resource_main_modules.append(main_module)

    def is_valid_plugin_resource_file_path(self, path):
        # splits the path into base path and file name
        _base_path, file_name = os.path.split(path)

        # returns false in case the file name is in the resource file name exclusion list
        if file_name in RESOURCE_FILE_NAME_EXCLUSION_LIST:
            return False

        # splits the file name into base file name and file extension
        _base_file_name, file_extension = os.path.splitext(file_name)

        # returns false in case the file extension is in the resource file extension exclusion list
        if file_extension in RESOURCE_FILE_EXTENSION_EXCLUSION_LIST:
            return False

        # returns true since this is a valid plugin resource file path
        return True

    def is_valid_main_module_file_path(self, main_module_file_path, plugin_path):
        # splits the main module file path into the base main module path and the main module file name
        main_module_directory_path, main_module_file_name = os.path.split(main_module_file_path)

        # removes the plugin path from the main module,0 directory path
        base_main_module_directory_path = main_module_directory_path.replace(plugin_path, "")

        # returns false in case the path is inside a resources directory
        if RESOURCES_DIRECTORY in base_main_module_directory_path[1:]:
            return False

        # splits the main module file name into base main module file name and extension
        base_main_module_file_name, main_module_file_extension = os.path.splitext(main_module_file_name)

        # returns false in case its not a python file
        if not main_module_file_extension == PYTHON_FILE_EXTENSION:
            return False

        # returns false in case the base main module file name ends with a plugin file ending
        if base_main_module_file_name.endswith(PLUGIN_MODULE_NAME_ENDING):
            return False

        # returns false in case its an init file
        if main_module_file_name == PYTHON_INIT_FILE_NAME:
            return False

        # returns true since this is a valid main module file path
        return True

    def normalize_path(self, path):
        # replaces windows directory separators with unix directory separators
        path = path.replace(WINDOWS_DIRECTORY_SEPARATOR, UNIX_DIRECTORY_SEPARATOR)

        return path

    def get_file_paths(self, path):
        # retrieves the file paths within the specified path
        file_paths = self._get_file_paths(path, [])

        return file_paths

    def _get_file_paths(self, path, file_paths):
        # retrieves the listdir entries for the specified path
        listdir_entries = os.listdir(path)

        # sorts the listdir entries
        listdir_entries.sort()

        # initializes the directory paths list
        directory_paths = []

        # collects file paths and directory paths
        for listdir_entry in listdir_entries:
            # skips in case this entry is in the exclusion list
            if listdir_entry in RESOURCE_FILE_NAME_EXCLUSION_LIST:
                continue

            # defines the listdir entry path
            listdir_entry_path = path + UNIX_DIRECTORY_SEPARATOR + listdir_entry

            # collects a directory path and skips this iteration
            if os.path.isdir(listdir_entry_path):
                directory_paths.append(listdir_entry_path)
                continue

            # retrieves the listdir entry extension
            _base_listdir_entry, extension = os.path.splitext(listdir_entry)

            # skips in case the extension is in the exclusion list
            if extension in RESOURCE_FILE_EXTENSION_EXCLUSION_LIST:
                continue

            # collects the file path
            file_paths.append(listdir_entry_path)

        # retrieves the file paths for the collected directories
        for directory_path in directory_paths:
            file_paths = self._get_file_paths(directory_path, file_paths)

        return file_paths
