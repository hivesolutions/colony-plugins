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

import json
import types
import os.path

BUILD_AUTOMATION_FILE_PATH_VALUE = "build_automation_file_path"

CAPABILITIES_VALUE = "capabilities"

CAPABILITIES_ALLOWED_VALUE = "capabilities_allowed"

DEPENDENCIES_VALUE = "dependencies"

ID_VALUE = "id"

PLUGINS_VALUE = "plugins"

RESOURCES_VALUE = "resources"

VERSION_VALUE = "version"

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

RESOURCE_FILE_EXTENSION_EXCLUSION_LIST = (".svn", ".svn-base", ".class", ".pyc", ".tmp")
""" The resource file extension exclusion list """

BUILD_AUTOMATION_ITEM_CAPABILITY_PLUGIN_EXCLUSION_LIST = ("pt.hive.colony.plugins.build.automation")
""" The list of plugins that are allowed not to have the build automation item capability """

PLUGIN_DESCRIPTOR_ATTRIBUTES_MAP = {"id" : "original_id",
                                    "sub_platforms" : "platforms",
                                    "name" : "name",
                                    "short_name" : "short_name",
                                    "description" : "description",
                                    "version" : "version",
                                    "author" : "author",
                                    "capabilities" : "capabilities"}
""" Defines the association between attributes in the plugin descriptor file and the plugin itself """

class BuildAutomationValidator:
    """
    The build automation validator class.
    """

    build_automation_validator_plugin = None
    """ The build automation validator plugin """

    def __init__(self, build_automation_validator_plugin):
        """
        Constructor of the class.

        @type build_automation_validator_plugin: BuildAutomationValidatorPlugin
        @param build_automation_validator_plugin: The build automation validator plugin
        """

        self.build_automation_validator_plugin = build_automation_validator_plugin

    def validate_build_automation(self):
        # retrieves all plugins
        plugins = self.build_automation_validator_plugin.manager.get_all_plugins()

        # validates all plugins
        for plugin in plugins:
            self._validate_build_automation_plugin(plugin)

    def validate_build_automation_plugin(self, plugin_id):
        # retrieves the plugin
        plugin = self.build_automation_validator_plugin.manager._get_plugin_by_id(plugin_id)

        # validates the plugin
        valid = self._validate_build_automation_plugin(plugin)

        # returns the plugin's validity
        return valid

    def _validate_build_automation_plugin(self, plugin):
        # retrieves the plugin path
        plugin_path = self.build_automation_validator_plugin.manager.get_plugin_path_by_id(plugin.id)

        # retrieves the plugin module name
        plugin_module_name = self.build_automation_validator_plugin.manager.get_plugin_module_name_by_id(plugin.id)

        # converts the plugin path separators from the windows mode to unix mode
        plugin_path = plugin_path.replace(WINDOWS_DIRECTORY_SEPARATOR, UNIX_DIRECTORY_SEPARATOR)

        # retrieves the plugin file path map for the plugin's path
        plugin_file_path_map = self.get_file_path_map(plugin_path)

        # initializes the valid flag
        valid = True

        # validates the plugin
        valid = valid and self._validate_plugin(plugin, plugin_path, plugin_module_name, plugin_file_path_map)

        # validates the plugin descriptor file
        valid = valid and self._validate_plugin_descriptor_file(plugin, plugin_path, plugin_module_name, plugin_file_path_map)

        # validates the build automation file
        valid = valid and self._validate_build_automation_file(plugin, plugin_module_name, plugin_path)

        # returns the validity
        return valid

    def _validate_plugin(self, plugin, plugin_path, plugin_module_name, plugin_file_path_map):
        # initializes the valid flag
        valid = True

        # validates the plugin's capabilities
        valid = valid and self.__validate_plugin_capabilities(plugin, plugin_module_name)

        # validates the plugin's main modules
        valid = valid and self.__validate_plugin_main_modules(plugin, plugin_path, plugin_module_name, plugin_file_path_map)

        # validates the plugin's file path
        valid = valid and self.__validate_plugin_file_path(plugin, plugin_path, plugin_module_name)

        # returns the validity
        return valid

    def __validate_plugin_file_path(self, plugin, plugin_path, plugin_module_name):
        # initializes the valid flag
        valid = True

        # tokenizes the plugin module name
        plugin_module_name_tokens = plugin_module_name.split("_")

        # retrieves the plugin class name from the plugin module name
        plugin_class_name = "".join([plugin_module_name_token.capitalize() for plugin_module_name_token in plugin_module_name_tokens])

        # checks if the plugin class name matches the plugin module name
        if not plugin_class_name == plugin.__class__.__name__:
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' has a class name that does not match its file name" % plugin_module_name)

        # defines the plugin file name
        plugin_file_name = plugin_module_name + PYTHON_FILE_EXTENSION

        # defines the plugin file path
        plugin_file_path = plugin_path + UNIX_DIRECTORY_SEPARATOR + plugin_file_name

        # checks that the plugin file exists
        if not os.path.exists(plugin_file_path):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' is missing file '%s'" % (plugin.id, plugin_file_name))

        # returns the validity
        return valid

    def __validate_plugin_capabilities(self, plugin, plugin_module_name):
        # initializes the valid flag
        valid = True

        # checks for duplicate capabilities in the plugin
        if not len(plugin.capabilities) == len(list(set(plugin.capabilities))):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' has duplicate capabilities" % plugin_module_name)

        # returns in case the plugin is in the build automation item capability exclusion list
        if plugin.id in BUILD_AUTOMATION_ITEM_CAPABILITY_PLUGIN_EXCLUSION_LIST:
            return False

        # checks if the plugin has a build automation item capability
        if not BUILD_AUTOMATION_ITEM_CAPABILITY in plugin.capabilities:
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' is missing 'build_automation_item' capability" % plugin_module_name)

        # returns the validity flag
        return valid

    def __validate_plugin_main_modules(self, plugin, plugin_path, plugin_module_name, plugin_file_path_map):
        # initializes the valid flag
        valid = True

        # checks for duplicate main modules in the plugin
        if not len(plugin.main_modules) == len(list(set(plugin.main_modules))):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' has duplicate main modules" % plugin_module_name)

        # checks that plugin's main modules exist
        for main_module in plugin.main_modules:
            # retrieves the base main module path
            base_main_module_path = main_module.replace(MAIN_MODULE_SEPARATOR, UNIX_DIRECTORY_SEPARATOR) + PYTHON_FILE_EXTENSION

            # normalizes the base main module path
            base_main_module_path = os.path.normpath(base_main_module_path)

            # retrieves the full main module path
            main_module_path = plugin_path + UNIX_DIRECTORY_SEPARATOR + base_main_module_path

            # checks if the main module exists
            if not os.path.exists(main_module_path):
                valid = False
                self.build_automation_validator_plugin.logger.info("'%s' is missing main module '%s'" % (plugin_module_name, main_module))

        # retrieves the plugin system file name
        plugin_system_file_name = plugin_module_name[:-1 * len(PLUGIN_MODULE_NAME_ENDING)] + SYSTEM_FILE_NAME_ENDING

        # checks if the plugin system file exists
        if not plugin_system_file_name in plugin_file_path_map:
            self.build_automation_validator_plugin.logger.info("'%s' is missing system file" % plugin_module_name)

            # returns since nothing else can be tested
            return False

        # retrieves the plugin system file path
        plugin_system_file_path = plugin_file_path_map[plugin_system_file_name]

        # retrieves the plugin's resources
        plugin_resource_path_map = self.get_file_path_map(plugin_system_file_path)

        # filters the plugin resource path map to leave only main module files
        main_module_path_map = dict([(resource_file_name, resource_path) for resource_file_name, resource_path in plugin_resource_path_map.items() if resource_file_name.endswith(PYTHON_FILE_EXTENSION) and not resource_file_name == PYTHON_INIT_FILE_NAME])

        # looks for main module entries for each file
        for main_module_file_name, main_module_path in main_module_path_map.items():
            # retrieves the base main module path
            base_main_module_path = main_module_path.replace(plugin_path, "")

            # ignores the file in case it's inside a resources folder
            if RESOURCES_DIRECTORY in base_main_module_path[1:]:
                continue

            # retrieves the main module file path
            base_main_module_file_path = base_main_module_path + UNIX_DIRECTORY_SEPARATOR + main_module_file_name

            # retrieves the main module from the base main module file path
            main_module = base_main_module_file_path.replace(UNIX_DIRECTORY_SEPARATOR, MAIN_MODULE_SEPARATOR)

            # replaces windows directory separators with main module separators
            main_module = main_module.replace(WINDOWS_DIRECTORY_SEPARATOR, MAIN_MODULE_SEPARATOR)

            # removes the file extension and the first dot from the main module
            main_module = main_module[1:-3]

            # checks if the main module exists in the plugin
            if not main_module in plugin.main_modules:
                valid = False
                self.build_automation_validator_plugin.logger.info("'%s' is missing main module declaration for file '%s'" % (plugin_module_name, main_module_file_name))

        # returns the validity
        return valid

    def _validate_plugin_descriptor_file(self, plugin, plugin_path, plugin_module_name, plugin_file_path_map):
        # initializes the valid flag
        valid = True

        # defines the plugin descriptor file name
        plugin_descriptor_file_name = plugin_module_name + JSON_FILE_EXTENSION

        # defines the plugin descriptor file path
        plugin_descriptor_file_path = plugin_path + UNIX_DIRECTORY_SEPARATOR + plugin_descriptor_file_name

        # checks that the plugin descriptor file exists
        if not os.path.exists(plugin_descriptor_file_path):
            self.build_automation_validator_plugin.logger.info("'%s' is missing file '%s'" % (plugin_module_name, plugin_descriptor_file_name))

            # returns since no more validations can be performed
            return False

        try:
            # retrieves the plugin descriptor data
            plugin_descriptor_data = self.get_json_data(plugin_descriptor_file_path)
        except Exception:
            self.build_automation_validator_plugin.logger.info("'%s' has invalid syntax" % plugin_descriptor_file_name)

            # returns since no more validations can be performed
            return False
        else:
            # validates the plugin descriptor file attributes
            valid = valid and self.__validate_plugin_descriptor_file_attributes(plugin, plugin_module_name, plugin_descriptor_data)

            # validates the plugin descriptor file capabilities
            valid = valid and self.__validate_plugin_descriptor_file_capabilities(plugin, plugin_module_name, plugin_descriptor_data)

            # validates the plugin descriptor file capabilities allowed
            valid = valid and self.__validate_plugin_descriptor_file_capabilities_allowed(plugin, plugin_module_name, plugin_descriptor_data)

            # validates the plugin descriptor file dependencies
            valid = valid and self.__validate_plugin_descriptor_file_dependencies(plugin, plugin_module_name, plugin_descriptor_data)

            # validates the plugin descriptor file resources
            valid = valid and self.__validate_plugin_descriptor_file_resources(plugin, plugin_path, plugin_module_name, plugin_file_path_map, plugin_descriptor_data)

        # returns the validity
        return valid

    def __validate_plugin_descriptor_file_attributes(self, plugin, plugin_module_name, plugin_descriptor_data):
        # initializes the valid flag
        valid = True

        # searches for plugin descriptor attributes with invalid content
        for plugin_descriptor_attribute_name, plugin_attribute_name in PLUGIN_DESCRIPTOR_ATTRIBUTES_MAP.items():
            # retrieves the plugin descriptor data attribute
            plugin_descriptor_data_attribute = plugin_descriptor_data[plugin_descriptor_attribute_name]

            # converts the plugin descriptor data attribute to unicode
            plugin_descriptor_data_attribute_unicode = self.convert_attribute_unicode(plugin_descriptor_data_attribute)

            # retrieves the plugin attribute
            plugin_attribute = getattr(plugin, plugin_attribute_name)

            # converts the plugin attribute to unicode
            plugin_attribute_unicode = self.convert_attribute_unicode(plugin_attribute)

            # checks if the attributes are the same
            if not plugin_descriptor_data_attribute_unicode == plugin_attribute_unicode:
                valid = False
                self.build_automation_validator_plugin.logger.info("'%s' descriptor file has invalid attribute '%s'" % (plugin_module_name, plugin_descriptor_attribute_name))

        # returns the validity
        return valid

    def __validate_plugin_descriptor_file_capabilities(self, plugin, plugin_module_name, plugin_descriptor_data):
        # initializes the valid flag
        valid = True

        # retrieves the plugin descriptor data capabilities
        plugin_descriptor_data_capabilities = plugin_descriptor_data[CAPABILITIES_VALUE]

        # checks for duplicate capabilities
        if not len(plugin_descriptor_data_capabilities) == len(list(set(plugin_descriptor_data_capabilities))):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file has duplicate capabilities" % plugin_module_name)

        # returns the validity
        return valid

    def __validate_plugin_descriptor_file_capabilities_allowed(self, plugin, plugin_module_name, plugin_descriptor_data):
        # initializes the valid flag
        valid = True

        # retrieves the plugin descriptor data capabilities allowed
        plugin_descriptor_data_capabilities_allowed = plugin_descriptor_data[CAPABILITIES_ALLOWED_VALUE]

        # checks for duplicate capabilities allowed
        if not len(plugin_descriptor_data_capabilities_allowed) == len(list(set(plugin_descriptor_data_capabilities_allowed))):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file has duplicate capabilities allowed" % plugin_module_name)

        # checks if the number of capabilities allowed is the same as in the plugin
        if not len(plugin_descriptor_data_capabilities_allowed) == len(plugin.capabilities_allowed):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file doesn't have as many capabilities allowed as its plugin" % plugin_module_name)

        # checks that the capabilites allowed are the same
        for capability_allowed_index in range(len(plugin.capabilities_allowed)):
            # retrieves the capability allowed
            capability_allowed = plugin.capabilities_allowed[capability_allowed_index]

            # retrieves the plugin descriptor data capability allowed
            plugin_descriptor_data_capability_allowed = plugin_descriptor_data_capabilities_allowed[capability_allowed_index]

            # converts the allowed capability to unicode
            capability_allowed = self.convert_attribute_unicode(capability_allowed)

            # converts the capability allowed to a tuple in case it is one
            if plugin_descriptor_data_capability_allowed.startswith("(") and plugin_descriptor_data_capability_allowed.endswith(")"):
                plugin_descriptor_data_capability_allowed = eval(plugin_descriptor_data_capability_allowed)

            # checks if the capability allowed is the same as in the plugin
            if not plugin_descriptor_data_capability_allowed == capability_allowed:
                self.build_automation_validator_plugin.logger.info("'%s' descriptor file has invalid attribute 'capabilities_allowed'" % plugin_module_name)

                # returns now that the attribute has been considered invalid
                return False

        # returns the validity
        return valid

    def __validate_plugin_descriptor_file_dependencies(self, plugin, plugin_module_name, plugin_descriptor_data):
        # initializes the valid flag
        valid = True

        # retrieves the plugin's dependencies
        plugin_dependencies = plugin.get_all_plugin_dependencies()

        # retrieves the plugin descriptor data dependencies
        plugin_descriptor_data_dependencies = plugin_descriptor_data[DEPENDENCIES_VALUE]

        # checks if the number of plugin dependencies is the same as in the plugin descriptor file
        if not len(plugin_dependencies) == len(plugin_descriptor_data_dependencies):
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file doesn't have as many dependencies as its plugin" % plugin_module_name)

            # returns since no more validations can be performed
            return False

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
                valid = False
                self.build_automation_validator_plugin.logger.info("'%s' descriptor file dependency '%s' doesn't exist or is not in correct order" % (plugin_module_name, plugin_descriptor_data_dependency_id))

            # retrieves the plugin descriptor data dependency version
            plugin_descriptor_data_dependency_version = plugin_descriptor_data_dependency[VERSION_VALUE]

            # checks if the dependency versions match
            if not plugin_descriptor_data_dependency_version == plugin_dependency.plugin_version:
                valid = False
                self.build_automation_validator_plugin.logger.info("'%s' descriptor file dependency '%s' doesn't have the same version as its plugin" % plugin_module_name)

        # returns the validity
        return valid

    def __validate_plugin_descriptor_file_resources(self, plugin, plugin_path, plugin_module_name, plugin_file_path_map, plugin_descriptor_data):
        # initializes the valid flag
        valid = True

        # retrieves the plugin descriptor data resources
        plugin_descriptor_data_resources = plugin_descriptor_data[RESOURCES_VALUE]

        # checks for duplicate resource paths
        if not len(plugin_descriptor_data_resources) == len(list(set(plugin_descriptor_data_resources))):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file has duplicate resource paths" % plugin_module_name)

        # retrieves the plugin file name
        plugin_file_name = plugin_module_name + PYTHON_FILE_EXTENSION

        # returns in case the system file doesn't exist
        if not plugin_file_name in plugin_descriptor_data_resources:
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file is missing resource declaration for file '%s'" % (plugin_module_name, plugin_file_name))

        # retrieves the plugin system file name
        plugin_system_file_name = plugin_module_name[:-1 * len(PLUGIN_MODULE_NAME_ENDING)] + SYSTEM_FILE_NAME_ENDING

        # returns in case the system file doesn't exist
        if not plugin_system_file_name in plugin_file_path_map:
            return False

        # retrieves the plugin system file path
        plugin_system_file_path = plugin_file_path_map[plugin_system_file_name]

        # retrieves the plugin's resources
        plugin_resource_path_map = self.get_file_path_map(plugin_system_file_path)

        # filters the plugin resource path map to leave only main module files
        plugin_resource_path_map = dict([(resource_file_name, resource_path) for resource_file_name, resource_path in plugin_resource_path_map.items() if not resource_file_name in RESOURCE_FILE_NAME_EXCLUSION_LIST and not self.get_file_extension(resource_file_name) in RESOURCE_FILE_EXTENSION_EXCLUSION_LIST])

        # checks if the list of resources if of the same size
        if len(plugin_resource_path_map) == len(plugin_descriptor_data_resources):
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file doesn't have as many resources as its plugin" % plugin_module_name)

            # returns since nothing else can be tested
            return False

        # retrieves the plugin root directory path
        plugin_root_directory_path = self.get_plugin_root_directory_path(plugin_system_file_path)

        # retrieves the root init file path
        plugin_root_init_file_path = plugin_root_directory_path + UNIX_DIRECTORY_SEPARATOR + INIT_FILE_NAME

        # checks if there's a resource declaration for the root init resource file
        if not plugin_root_init_file_path in plugin_descriptor_data_resources:
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' descriptor file is missing resource declaration for file '%s'" % (plugin_module_name, plugin_root_init_file_path))

        # looks for resource declarations in the descriptor for each of the discovered resource files
        for resource_file_name, resource_path in plugin_resource_path_map.items():
            # retrieves the base main module path
            base_resource_path = resource_path.replace(plugin_path, "")

            # retrieves the main module file path
            base_resource_file_path = base_resource_path + UNIX_DIRECTORY_SEPARATOR + resource_file_name

            # removes the first slash from the base resource file path
            base_resource_file_path = base_resource_file_path[1:]

            # checks if there's a resource declaration for the resource file
            if not base_resource_file_path in plugin_descriptor_data_resources:
                valid = False
                self.build_automation_validator_plugin.logger.info("'%s' descriptor file is missing resource declaration for file '%s'" % (plugin_module_name, resource_file_name))

        # returns the validity
        return valid

    def _validate_build_automation_file(self, plugin, plugin_module_name, plugin_path):
        # initializes the valid flag
        valid = True

        # checks if the build automation file path is specified in the plugin attributes
        if not BUILD_AUTOMATION_FILE_PATH_ATTRIBUTE in plugin.attributes:
            self.build_automation_validator_plugin.logger.info("'%s' is missing the 'build_automation_file_path' attribute" % plugin_module_name)

            # returns in case no build automation file path has been specified
            return False

        # retrieves the base build automation file path
        base_build_automation_file_path = plugin.attributes[BUILD_AUTOMATION_FILE_PATH_VALUE]

        # retrieves the build automation file path
        build_automation_file_path = base_build_automation_file_path.replace(BASE_PLUGIN_DIRECTORY_VARIABLE, plugin_path)

        # checks for the existence of the build automation file
        if not build_automation_file_path or not os.path.exists(build_automation_file_path):
            valid = False
            self.build_automation_validator_plugin.logger.info("'%s' is missing the referenced build automation file" % plugin_module_name)

        # returns the validity
        return valid

    def get_json_data(self, json_file_path):
        # reads the json file
        json_file = open(json_file_path, "r")

        # reads the data from the json file
        json_file_data = json_file.read()

        # closes the json file
        json_file.close()

        # loads the json data from the json file
        json_data = json.loads(json_file_data)

        return json_data

    def get_file_path_map(self, path):
        # initializes the file path map
        file_path_map = {}

        # crawls the specified path indexing file paths by their file name
        for root, _directories, files in os.walk(path):
            for file in files:
                # converts the root path separators from the windows mode to unix mode
                root = root.replace(WINDOWS_DIRECTORY_SEPARATOR, UNIX_DIRECTORY_SEPARATOR)

                # indexes the file path by the file name
                file_path_map[file] = root

        return file_path_map

    def get_plugin_root_directory_path(self, plugin_system_file_path):
        # tokenizes the plugin system file path with the unix directory separator
        plugin_system_file_path_tokens = plugin_system_file_path.split(UNIX_DIRECTORY_SEPARATOR)

        # tokenizes the plugin system file path with the windows directory separator
        if len(plugin_system_file_path_tokens) == 1:
            plugin_system_file_path_tokens = plugin_system_file_path.split(WINDOWS_DIRECTORY_SEPARATOR)

        # retrieves the plugin directory root path
        plugin_directory_root_path = plugin_system_file_path_tokens[plugin_system_file_path_tokens.index(PLUGINS_VALUE) + 1]

        return plugin_directory_root_path

    def get_file_extension(self, file_path):
        # splits the file into base name and extension
        _base_name, extension = os.path.splitext(file_path)

        # returns the extension
        return extension

    def convert_attribute_unicode(self, attribute_value):
        # returns the unicode version of the attribute in case it's a string
        if type(attribute_value) == types.StringType:
            return unicode(attribute_value)

        # determines the attribute value's type
        attribute_value_type = type(attribute_value)

        # returns in case the attribute is not a list
        if not attribute_value_type in (types.ListType, types.TupleType):
            return attribute_value

        # converts into a list in case it's a tuple
        attribute_value_list = list(attribute_value)

        # converts each item in the list
        for attribute_value_index in range(len(attribute_value_list)):
            # retrieves the attribute value item
            attribute_value_item = attribute_value_list[attribute_value_index]

            # skips in case the attribute value is not a string
            if not type(attribute_value_item) == types.StringType:
                continue

            # stores the unicode version of the string
            attribute_value_list[attribute_value_index] = unicode(attribute_value_item)

        # converts the list back to a tuple in case it was originally so
        if attribute_value_type == types.TupleType:
            attribute_value_list = tuple(attribute_value_list)

        return attribute_value_list
