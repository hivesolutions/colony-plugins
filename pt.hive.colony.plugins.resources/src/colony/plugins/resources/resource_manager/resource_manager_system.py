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

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import re
import sys

import colony.libs.path_util
import colony.libs.structures_util

import resource_manager_parser

BASE_RESOURCES_PATH = "resources/resource_manager/resources"
""" The base resources path """

CONFIGURATION_PATH = "configuration"
""" The configuration path """

RESOURCES_SUFIX_VALUE = "resources.xml"
""" The resources suffix value """

RESOURCES_SUFFIX_LENGTH = 13
""" The resources suffix length """

RESOURCES_SUFFIX_START_INDEX = -13
""" The resources suffix value """

ENVIRONMENT_VARIABLE_REGEX = "\$\{[a-zA-Z0-9_]*\}"
""" The regular expression for the environment variable """

RESOURCE_VARIABLE_REGEX = "\$resource\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the resource variable """

PLUGIN_VARIABLE_REGEX = "\$plugin\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the plugin variable """

GLOBAL_VARIABLE_REGEX = "\$global\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the global variable """

LOCAL_VARIABLE_REGEX = "\$local\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the local variable """

COLONY_VALUE = "colony"
""" The colony value """

MANAGER_PATH_VALUE = "manager_path"
""" The manager path value """

STRING_TYPE = "string"
""" The string type """

BOOLEAN_TYPE = "boolean"
""" The boolean type """

INTEGER_TYPE = "integer"
""" The integer type """

FLOAT_TYPE = "float"
""" The float type """

TRUE_VALUE = "true"
""" The true value """

FALSE_VALUE = "false"
""" The false value """

class ResourceManager:
    """
    Stores and indexes miscellaneous resources.
    """

    resource_manager_plugin = None
    """ The resource manager plugin """

    resource_id_resource_map = {}
    """ Map associating resource ids with resources """

    resource_name_resources_list_map = {}
    """ Map associating resource name with the correspondent resources """

    resource_type_resources_list_map = {}
    """ Map associating resource type with the correspondent resources """

    resource_namespace_resources_list_map = {}
    """ Map associating namespace with the correspondent resources """

    resource_parser_plugins_map = {}
    """ The resource parser plugins map """

    string_value_real_string_value_map = {}
    """ The string value real string value map """

    file_path_resources_list_map = {}
    """ The map associating the resource file path with the list of "parsed" resources """

    file_path_file_information_map = {}
    """ The map associating the resource file path with the resource path information tuple """

    environment_variable_regex = None
    """ The environment variable regular expression used for regular expression match """

    resource_variable_regex = None
    """ The resource variable regular expression used for regular expression match """

    plugin_variable_regex = None
    """ The plugin variable regular expression used for regular expression match """

    global_variable_regex = None
    """ The global variable regular expression used for regular expression match """

    local_variable_regex = None
    """ The local variable regular expression used for regular expression match """

    def __init__(self, resource_manager_plugin):
        """
        Constructor of the class.

        @type resource_manager_plugin: Plugin
        @param resource_manager_plugin: The resource manager plugin.
        """

        self.resource_manager_plugin = resource_manager_plugin
        self.resource_namespace_resources_list_map = {}
        self.resource_id_resource_map = {}
        self.resource_name_resources_list_map = {}
        self.resource_type_resources_list_map = {}
        self.resource_parser_plugins_map = {}
        self.plugin_id_configuration_resources_list_map = {}
        self.string_value_real_string_value_map = {}
        self.file_path_resources_list_map = {}
        self.file_path_file_information_map = {}

        # compiles the environment variable regular expression
        self.environment_variable_regex = re.compile(ENVIRONMENT_VARIABLE_REGEX)

        # compiles the resource variable regular expression
        self.resource_variable_regex = re.compile(RESOURCE_VARIABLE_REGEX)

        # compiles the plugin variable regular expression
        self.plugin_variable_regex = re.compile(PLUGIN_VARIABLE_REGEX)

        # compiles the global variable regular expression
        self.global_variable_regex = re.compile(GLOBAL_VARIABLE_REGEX)

        # compiles the local variable regular expression
        self.local_variable_regex = re.compile(LOCAL_VARIABLE_REGEX)

    def load_resource_file(self, file_path):
        """
        Loads the resource file in the given path.

        @type file_path: String
        @param file_path: The path to the resource file to be
        loaded.
        """

        # splits the file path, retrieving the directory path
        # and the file name
        directory_path, _file_name = os.path.split(file_path)

        # parses the resource file
        self.parse_file(file_path, directory_path)

    def load_system(self):
        """
        Loads the system internals, loading the base system resources.
        """

        # loads the internal resources
        self.load_internal_resources()

        # loads the base resources
        self.load_base_resources()

        # loads the configuration resources
        self.load_configuration_resources()

    def load_internal_resources(self):
        """
        Loads the resources dedicated to describe the internal
        values of the colony manager.
        This method exposes resources to be consumed by other resource
        files.
        """

        # retrieves the plugin manager
        plugin_manager = self.resource_manager_plugin.manager

        # retrieves the manager path from the plugin manager
        manager_path = plugin_manager.get_manager_path()

        # registers the internal resources
        self.register_resource(COLONY_VALUE, MANAGER_PATH_VALUE, STRING_TYPE, manager_path)

    def load_base_resources(self):
        """
        Loads the base resources from the description file.
        The base resources are the resources in the plugin's
        resources directory.
        """

        # retrieves the base resources path, using the current
        # plugin information and relative path
        base_resources_path = self.get_base_resources_path()

        # loads the base resources for the entry directory
        # (this is a recursive loading strategy)
        self._load_resources_directory(base_resources_path)

    def load_configuration_resources(self):
        """
        Loads the configuration resources from the description file.
        The configuration resources are located in the configuration
        directory
        """

        # retrieves the plugin manager
        plugin_manager = self.resource_manager_plugin.manager

        # retrieves the resource manager plugin id
        resource_manager_plugin_id = self.resource_manager_plugin.id

        # retrieves the plugin configuration paths from the resource manager plugin
        # sets the extra paths flag to retrieve all the configuration paths
        configuration_paths = plugin_manager.get_plugin_configuration_paths_by_id(resource_manager_plugin_id, True)

        # iterates over all the configuration paths
        # to construct the full configuration path and
        # load the resources in that path
        for configuration_path in configuration_paths:
            # constructs the full configuration path, from the
            # base configuration path and the relative configuration path
            full_configuration_path = os.path.join(configuration_path, CONFIGURATION_PATH)

            # loads the configuration resources for the entry directory
            # (this is a recursive loading strategy)
            self._load_resources_directory(full_configuration_path)

    def parse_file(self, file_path, full_resources_path):
        """
        Parses the file in the given file path, using the full
        resources path as the base for the parsing.
        The parsing of the file also implies the registering
        of the resources in the internal data structures.

        @type file_path: String
        @param file_path: The path to the file to be parsed.
        @type full_resources_path: String
        @param full_resources_path: The full path to the
        resources path (directory).
        """

        # creates the resources file parser
        resources_file_parser = resource_manager_parser.ResourcesFileParser(file_path)

        # parses the file (using the current parser)
        resources_file_parser.parse()

        # retrieves the resources list
        resources_list = resources_file_parser.get_value()

        # registers the resources in the given list, send also
        # the path to the resources file and the full path to
        # the resources path (directory) are also sent
        self.register_resources(resources_list, file_path, full_resources_path)

    def register_resources(self, resources_list, file_path, full_resources_path):
        # retrieves the plugin manager
        plugin_manager = self.resource_manager_plugin.manager

        # normalizes the file path and then uses it to set
        # the resources list in the file path resources list map
        # and to set the resource file information tuple in the file
        # path file information map
        file_path_normalized = colony.libs.path_util.normalize_path(file_path)
        self.file_path_resources_list_map[file_path_normalized] = resources_list
        self.file_path_file_information_map[file_path_normalized] = (file_path, full_resources_path)

        # creates the validation list from the list
        # resource (filters the validations)
        validation_list = [value for value in resources_list if value.__class__ == resource_manager_parser.Validation]

        # iterates over all the validation in the validation
        # list (to process the validation)
        for validation in validation_list:
            # processes the validation
            return_value = self.process_validation(validation)

            # in case the return value is invalid
            if not return_value:
                # returns immediately
                return

        # iterates over all the resources in the list
        # (to process them)
        for resource in resources_list:
            # in case the resource is of type validation (ignore)
            if resource.__class__ == resource_manager_parser.Validation:
                # continues the loop
                continue

            # in case the resource is of type plugin configuration
            if resource.__class__ == resource_manager_parser.PluginConfiguration:
                # iterates over all the resources in the resources
                # list (the plugin configuration contains multiple resources
                for resource_item in resource.resources_list:
                    # processes the resource, updating the resource item
                    # with the correct data
                    self.process_resource(resource_item, full_resources_path)
            # otherwise it's a normal (base) configuration
            else:
                # processes the resources, updating the resource item
                # with the correct data
                self.process_resource(resource, full_resources_path)

        # creates the plugin configuration list from the list
        # resource (filters the plugin configurations)
        plugin_configuration_list = [value for value in resources_list if value.__class__ == resource_manager_parser.PluginConfiguration]

        # creates the base resources list from the list
        # resource (filters the resources)
        base_resources_list = [value for value in resources_list if value.__class__ == resource_manager_parser.Resource]

        # iterates over all the resources in the plugin configuration list
        for plugin_configuration in plugin_configuration_list:
            # retrieves the plugin configuration plugin id
            plugin_configuration_plugin_id = plugin_configuration.plugin_id

            # retrieves the plugin configuration resources list
            plugin_configuration_resources_list = plugin_configuration.resources_list

            # sets the plugin configuration resources list in the plugin id configuration resources list map
            self.plugin_id_configuration_resources_list_map[plugin_configuration_plugin_id] = plugin_configuration_resources_list

            # tries to retrieve the configuration plugin using the plugin id
            configuration_plugin = plugin_manager._get_plugin_by_id(plugin_configuration_plugin_id)

            # in case the configuration plugin is not found
            # or in case it's not loaded (nothing is done)
            if not configuration_plugin or not configuration_plugin.is_loaded():
                # continues the loop
                continue

            # iterates over all the plugin configuration resources
            for plugin_configuration_resource in plugin_configuration_resources_list:
                # retrieves the plugin configuration resource name
                plugin_configuration_resource_name = plugin_configuration_resource.name

                # sets the plugin configuration resource as configuration property in the configuration plugin
                configuration_plugin.set_configuration_property(plugin_configuration_resource_name, plugin_configuration_resource)

        # iterates over all the resources in the base resources list
        for resource in base_resources_list:
            # registers the resource for the given namespace,
            # name type and data
            self.register_resource(resource.namespace, resource.name, resource.type, resource.data)

    def unregister_resources(self, resources_list, file_path, full_resources_path):
        # retrieves the plugin manager
        plugin_manager = self.resource_manager_plugin.manager

        # normalizes the file path and then uses it to unset
        # the resources list from the file path resources list map and
        # to unset the resource file information from the file path
        # file information map
        file_path_normalized = colony.libs.path_util.normalize_path(file_path)
        del self.file_path_resources_list_map[file_path_normalized]
        del self.file_path_file_information_map[file_path_normalized]

        # creates the validation list from the list
        # resource (filters the validations)
        validation_list = [value for value in resources_list if value.__class__ == resource_manager_parser.Validation]

        # iterates over all the validation in the validation
        # list (to process the validation)
        for validation in validation_list:
            # processes the validation
            return_value = self.process_validation(validation)

            # in case the return value is invalid
            if not return_value:
                # returns immediately
                return

        # creates the plugin configuration list from the list
        # resource (filters the plugin configurations)
        plugin_configuration_list = [value for value in resources_list if value.__class__ == resource_manager_parser.PluginConfiguration]

        # creates the base resources list from the list
        # resource (filters the resources)
        base_resources_list = [value for value in resources_list if value.__class__ == resource_manager_parser.Resource]

        # iterates over all the resources in the plugin configuration list
        for plugin_configuration in plugin_configuration_list:
            # retrieves the plugin configuration plugin id
            plugin_configuration_plugin_id = plugin_configuration.plugin_id

            # retrieves the plugin configuration resources list
            plugin_configuration_resources_list = plugin_configuration.resources_list

            # unsets the plugin configuration resources list from
            # the plugin id configuration resources list map
            del self.plugin_id_configuration_resources_list_map[plugin_configuration_plugin_id]

            # tries to retrieve the configuration plugin using the plugin id
            configuration_plugin = plugin_manager._get_plugin_by_id(plugin_configuration_plugin_id)

            # in case the configuration plugin is not found
            # or in case it's not loaded (nothing is done)
            if not configuration_plugin or not configuration_plugin.is_loaded():
                # continues the loop
                continue

            # iterates over all the plugin configuration resources
            for plugin_configuration_resource in plugin_configuration_resources_list:
                # retrieves the plugin configuration resource name
                plugin_configuration_resource_name = plugin_configuration_resource.name

                # unsets the plugin configuration resource in the configuration plugin
                configuration_plugin.unset_configuration_property(plugin_configuration_resource_name)

        # iterates over all the resources in the base resources list
        for resource in base_resources_list:
            # creates a new (composite) resource from the given
            # (base) resource information
            _resource = Resource(resource.namespace, resource.name, resource.type, resource.data)

            # retrieves the resource id and the unregisters
            # the resource using the given resource id
            resource_id = _resource.get_id()
            self.unregister_resource(resource_id)

    def register_plugin_resources(self, plugin):
        """
        Registers the plugin resources in the plugin.
        The plugin is properly "notified" about the
        configuration property "registration".

        @type plugin: Plugin
        @param plugin: The plugin to have the resources registered.
        """

        # retrieves the plugin id
        plugin_id = plugin.id

        # in case the plugin id is not defined in the plugin id configuration resource map
        if not plugin_id in self.plugin_id_configuration_resources_list_map:
            # returns immediately
            return

        # retrieves the plugin configuration resources list
        plugin_configuration_resources_list = self.plugin_id_configuration_resources_list_map[plugin_id]

        # iterates over all the plugin configuration resources
        for plugin_configuration_resource in plugin_configuration_resources_list:
            # retrieves the plugin configuration resource name
            plugin_configuration_resource_name = plugin_configuration_resource.name

            # sets the plugin configuration resource as configuration property in the plugin
            plugin.set_configuration_property(plugin_configuration_resource_name, plugin_configuration_resource)

    def unregister_plugin_resources(self, plugin):
        """
        Unregisters the plugin resources in the plugin.
        The plugin is properly "notified" about the
        configuration property "unregistration".

        @type plugin: Plugin
        @param plugin: The plugin to have the resources unregistered.
        """

        # retrieves the plugin id
        plugin_id = plugin.id

        # in case the plugin id is not defined in the plugin id configuration resource map
        if not plugin_id in self.plugin_id_configuration_resources_list_map:
            # returns immediately
            return

        # retrieves the plugin configuration resources list
        plugin_configuration_resources_list = self.plugin_id_configuration_resources_list_map[plugin_id]

        # iterates over all the plugin configuration resources
        for plugin_configuration_resource in plugin_configuration_resources_list:
            # retrieves the plugin configuration resource name
            plugin_configuration_resource_name = plugin_configuration_resource.name

            # unsets the plugin configuration resource as configuration property in the plugin
            plugin.unset_configuration_property(plugin_configuration_resource_name)

    def process_resource(self, resource, full_resources_path):
        """
        Processes a resource.

        @type resource: Resource
        @param resource: The resource to be processed.
        @type full_resources_path: String
        @param full_resources_path: The full resources path.
        @rtype: bool
        @return: If the resource data was loaded or set for lazy loading.
        """

        # sets the resource full resources path
        resource.full_resources_path = full_resources_path

        # parses the resource data
        resource_data_result = self.parse_resource_data(resource)

        # returns the resources data result
        return resource_data_result

    def parse_resource_data(self, resource):
        """
        Parses a resource data value.

        @type resource: Resource
        @param resource: The resource to have the data processed.
        @rtype: bool
        @return: If the resource data was loaded or set for lazy loading.
        """

        # retrieves the resource type
        resource_type = resource.type

        # sets the resource data as the real string value
        resource.data = self.get_real_string_value(resource.data)

        # in case the resource type is string
        if resource_type == STRING_TYPE:
            resource.data = unicode(resource.data)
        # in case the resource type is boolean
        elif resource_type == BOOLEAN_TYPE:
            # in case the resource data contains the true value
            if resource.data == TRUE_VALUE:
                # sets the resource data as true
                resource.data = True
            # in case the resource data contains the false value
            elif resource.data == FALSE_VALUE:
                # sets the resource data as
                resource.data = False
            # otherwise
            else:
                # sets the resource data as none
                resource.data = None
        # in case the resource type is integer
        elif resource_type == INTEGER_TYPE:
            resource.data = int(resource.data)
        # in case the resource type is float
        elif resource_type == FLOAT_TYPE:
            resource.data = float(resource.data)
        # in case the resource type exists in the
        # map of resource parser plugins
        elif resource_type in self.resource_parser_plugins_map:
            # retrieves the resource parser plugin associated with the
            # resource type
            resource_parser_plugin = self.resource_parser_plugins_map[resource_type]

            # parses the resource with the resource parser plugin
            resource_parser_plugin.parse_resource(resource)

            # sets the parse resource data method reference
            # to none (no need to parse the resource data in lazy mode)
            resource.parse_resource_data = None
        # otherwise
        else:
            # sets the parse resource data handler, this technique
            # allows a lazy loading of the resource parser plugins
            resource.parse_resource_data = self.parse_resource_data

            # returns invalid (lazy loading)
            return False

        # returns valid (loaded)
        return True

    def get_real_string_value(self, string_value):
        """
        Retrieves the real string value for the given string value,
        substituting the variable in the string.

        @type string_value: String
        @param string_value: The string value to be converted.
        @rtype: String
        @return: The converted string.
        """

        # retrieves the plugin manager
        plugin_manager = self.resource_manager_plugin.manager

        # retrieves the file system encoding
        file_system_encoding = sys.getfilesystemencoding()

        # checks the string value in the string value real string value map
        if string_value in self.string_value_real_string_value_map:
            # retrieves the real string value
            real_string_value = self.string_value_real_string_value_map[string_value]

            # returns the real string value
            return real_string_value

        # starts the real string value
        real_string_value = string_value

        # retrieves the find iterator for the given regular expression
        find_iterator = self.environment_variable_regex.finditer(real_string_value)

        # iterates over all the matches in the find iterator
        for match in find_iterator:
            # retrieves the match group
            match_group = match.group()

            # retrieves the variable name
            variable_name = match_group[2:-1]

            # retrieves the variable value, decoding it with the file system encoding
            variable_value = os.environ.get(variable_name, "").decode(file_system_encoding)

            # sets the new resource data
            real_string_value = real_string_value.replace(match_group, variable_value)

        # retrieves the find iterator for the given regular expression
        find_iterator = self.resource_variable_regex.finditer(real_string_value)

        # iterates over all the matches in the find iterator
        for match in find_iterator:
            # retrieves the match group
            match_group = match.group()

            # retrieves the variable name
            variable_name = match_group[10:-1]

            # retrieves the resource for the match
            resource = self.get_resource(variable_name)

            # retrieves the resource data
            resource_data = resource.data

            # sets the new real string value
            real_string_value = real_string_value.replace(match_group, resource_data)

        # retrieves the find iterator for the given regular expression
        find_iterator = self.plugin_variable_regex.finditer(real_string_value)

        # iterates over all the matches in the find iterator
        for match in find_iterator:
            # retrieves the match group
            match_group = match.group()

            # retrieves the variable name
            variable_name = match_group[8:-1]

            # retrieves the plugin path for the match
            plugin_path = plugin_manager.get_plugin_path_by_id(variable_name)

            # sets the new real string value
            real_string_value = real_string_value.replace(match_group, plugin_path)

        # retrieves the find iterator for the given regular expression
        find_iterator = self.global_variable_regex.finditer(real_string_value)

        # iterates over all the matches in the find iterator
        for match in find_iterator:
            # retrieves the match group
            match_group = match.group()

            # retrieves the variable name
            variable_name = match_group[8:-1]

            # splits the variable name
            variable_name_splitted = variable_name.split(".")

            # retrieves the first variable name
            first_variable_name = variable_name_splitted[0]

            # retrieves the second variable names
            second_variable_names = variable_name_splitted[1:]

            # retrieves the global variable
            global_variable = globals()[first_variable_name]

            # iterates over all the variable names in the second
            # variable names
            for variable_name in second_variable_names:
                # retrieves the global variable
                global_variable = getattr(global_variable, variable_name)

            # sets the new real string value
            real_string_value = real_string_value.replace(match_group, global_variable)

        # retrieves the find iterator for the given regular expression
        find_iterator = self.local_variable_regex.finditer(real_string_value)

        # iterates over all the matches in the find iterator
        for match in find_iterator:
            # retrieves the match group
            match_group = match.group()

            # retrieves the variable name
            variable_name = match_group[7:-1]

            # splits the variable name
            variable_name_splitted = variable_name.split(".")

            # sets the plugin manager as local variable
            plugin_manager = self.resource_manager_plugin.manager

            # retrieves the first variable name
            first_variable_name = variable_name_splitted[0]

            # retrieves the second variable names
            second_variable_names = variable_name_splitted[1:]

            # retrieves the local variable
            local_variable = locals()[first_variable_name]

            # iterates over all the variable names in the second
            # variable names
            for variable_name in second_variable_names:
                # retrieves the local variable
                local_variable = getattr(local_variable, variable_name)

            # sets the new real string value
            real_string_value = real_string_value.replace(match_group, local_variable)

        # sets the real string value in the string value real string value map
        self.string_value_real_string_value_map[string_value] = real_string_value

        # returns the real string value
        return real_string_value

    def get_base_resources_path(self):
        """
        Constructs and retrieves the base resources path
        for the resource manager plugin.

        @rtype: String
        @return: The (constructed) base resources path for
        the resource manager plugin.
        """

        # retrieves the plugin manager
        plugin_manager = self.resource_manager_plugin.manager

        # retrieves the resource manager plugin id
        resource_manager_plugin_id = self.resource_manager_plugin.id

        # retrieves the base plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(resource_manager_plugin_id)

        # constructs the base resources path
        base_resources_path = os.path.join(plugin_path, BASE_RESOURCES_PATH)

        # returns the base resources path
        return base_resources_path

    def process_validation(self, validation):
        """
        Processes the given validation retrieving the validation result.

        @type validation: Validation
        @param validation: The validation to be processed.
        @rtype: bool
        @return: The validation result.
        """

        # retrieves the validation expression
        validation_expression = validation.expression

        # processes the expression returning the value
        return_value = self.process_expression(validation_expression)

        # returns the return value
        return return_value

    def process_expression(self, expression):
        """
        Processes the given expression retrieving the expression result.

        @type expression: Expression
        @param expression: The expression to be processed.
        @rtype: bool
        @return: The expression result.
        """

        if expression.__class__ == resource_manager_parser.EqualsExpression:
            return_value = self.process_equals_expression(expression)

        # returns the return value
        return return_value

    def process_equals_expression(self, equals_expression):
        """
        Processes the given equals expression retrieving the equals expression result.

        @type equals_expression: EqualsExpression
        @param equals_expression: The equals expression to be processed.
        @rtype: bool
        @return: The equals expression result.
        """

        # retrieves both operands, the first and the second
        equals_expression_first_operand = equals_expression.first_operand
        equals_expression_second_operand = equals_expression.second_operand

        # retrieves the operand values
        equals_expression_first_operand_value = self.process_operand(equals_expression_first_operand)
        equals_expression_second_operand_value = self.process_operand(equals_expression_second_operand)

        # calculates the equals value
        equals_value = equals_expression_first_operand_value == equals_expression_second_operand_value

        # returns the equals value
        return equals_value

    def process_operand(self, operand):
        """
        Processes the given operand retrieving the value.

        @type operand: Operand
        @param operand: The operand to be processed.
        @rtype: Object
        @return: The operand value.
        """

        # parses the operand resource data
        self.parse_resource_data(operand)

        # retrieves the operand data
        operand_data = operand.data

        # returns the operand data
        return operand_data

    def register_resource(self, resource_namespace, resource_name, resource_type, resource_data):
        """
        Registers a resource in the resource manager.

        @type resource_namespace: String
        @param resource_namespace: The namespace this resource should be included in.
        @type resource_name: String
        @param resource_name: The name of the resource.
        @type resource_type: String
        @param resource_type: The type of the resource.
        @type resource_data: Object
        @param resource_data: The resource one wants to store.
        """

        # creates a new resource with the given information
        resource = Resource(resource_namespace, resource_name, resource_type, resource_data)

        # retrieves the resource id
        resource_id = resource.get_id()

        # if the resource already exists remove it from all indexes
        # avoids extra problem with the resource
        if self.is_resource_registered(resource_id):
            # unregisters the resource (cleans structures)
            self.unregister_resource(resource_id)

        # sets the resource in the resource id resource map
        self.resource_id_resource_map[resource_id] = resource

        # index resource by name
        if not resource.get_name() in self.resource_name_resources_list_map:
            self.resource_name_resources_list_map[resource.get_name()] = []
        self.resource_name_resources_list_map[resource.get_name()].append(resource)

        # index resource by type
        if not resource.get_type() in self.resource_type_resources_list_map:
            self.resource_type_resources_list_map[resource.get_type()] = []
        self.resource_type_resources_list_map[resource.get_type()].append(resource)

        # index resource by namespace
        namespace_values_list = resource.get_namespace().get_list_value()

        # initializes the current namespace
        current_namespace = str()
        for namespace in namespace_values_list:
            if not current_namespace == "":
                current_namespace += "."
            current_namespace += namespace
            if not current_namespace in self.resource_namespace_resources_list_map:
                self.resource_namespace_resources_list_map[current_namespace] = []
            self.resource_namespace_resources_list_map[current_namespace].append(resource)

        # invalidates the real string value cache
        self._invalidate_real_string_value_cache()

    def unregister_resource(self, resource_id):
        """
        Unregisters the resource with the given id from the resource manager.

        @type resource_id: String
        @param resource_id: The id of the resource.
        """

        # in case the resource id exist in the resource id resource map
        if resource_id in self.resource_id_resource_map:
            # retrieves the "old" resource from the resource id
            # resource map (backup)
            old_resource = self.resource_id_resource_map[resource_id]

            # deletes the resource reference
            del self.resource_id_resource_map[resource_id]

            # retrieves the "old" resource attributes
            old_resource_name = old_resource.get_name()
            old_resource_namespace = old_resource.get_namespace()
            old_resource_type = old_resource.get_type()

            # removes the "old" resource from the name and type resources list maps
            self.resource_name_resources_list_map[old_resource_name].remove(old_resource)
            self.resource_type_resources_list_map[old_resource_type].remove(old_resource)

            # retrieves the "old" resource namespace list value
            namespace_values_list = old_resource_namespace.get_list_value()

            # starts the current namespace with an empty string
            current_namespace = ""

            # iterates over all the namespace value in the namespace
            # values list
            for namespace_value in namespace_values_list:
                # in case the current namespace is
                # not the first
                if not current_namespace == "":
                    # adds the separator token to the
                    # current namespace
                    current_namespace += "."

                # adds the namespace value to the current namespace
                current_namespace += namespace_value

                # removes from the "old" resource from the namespace resources list map
                self.resource_namespace_resources_list_map[current_namespace].remove(old_resource)

        # invalidates the real string value cache
        self._invalidate_real_string_value_cache()

    def is_resource_registered(self, resource_id):
        """
        Retrieves the existence (or not) of a resource with the given id.

        @type resource_id: String
        @param resource_id: The id of the resource to be tested.
        @rtype: bool
        @return: The existence (or not) of a resource with the given id.
        """

        # returns if the resource id exists in the resource
        # id resource map
        return resource_id in self.resource_id_resource_map

    def is_resource_name(self, resource_name):
        """
        Checks if the given resource (file) name represents a valid
        resource file name.
        The validation of the resource name is simple and efficient.

        @rtype: bool
        @return: If the given resource (file) name represents a valid
        resource file name.
        """

        # in case the length of the resources name is greater or equal than the resources suffix length
        # and the last item of the resources name item is the same as the resources suffix value
        is_resource_name  = len(resource_name) >= RESOURCES_SUFFIX_LENGTH and resource_name[RESOURCES_SUFFIX_START_INDEX:] == RESOURCES_SUFIX_VALUE

        # returns the result of the is resource
        # name test
        return is_resource_name

    def get_resource(self, resource_id):
        """
        Retrieves the resource with the given resource id.

        @type resource_id: String
        @param resource_id: The id of the resource to be retrieved.
        @rtype: Resource
        @return: The resource with the given id.
        """

        # returns the resource if for the given resource id, or none
        # in case the resource does not exist in the resource id resource map
        return self.resource_id_resource_map.get(resource_id, None)

    def get_resources(self, resource_namespace = None, resource_name = None, resource_type = None):
        """
        Retrieves the resources for the given resource namespace, resource name and resource type.
        The given values are not mandatory and work as a filter.

        @type resource_namespace: String
        @param resource_namespace: The namespace of the resource to be retrieved.
        @type resource_name: String
        @param resource_name: The name of the resource to be retrieved.
        @type resource_type: String
        @param resource_type: The type of the resource to be retrieved.
        """

        # in case none of the filters are defined
        if resource_namespace == None and resource_name == None and resource_type == None:
            # returns all the values in the reource id resource map
            return self.resource_id_resource_map.values()
        # in case the namespace and the name are defined
        elif not resource_namespace == None and not resource_name == None:
            # creates the resource complete name
            resource_complete_name = resource_namespace + "." + resource_name

            # returns the resource for the complete name
            return self.get_resource(resource_complete_name)
        # in case the namespace is defined
        elif not resource_namespace == None:
            # in case only the namespace is defined
            if resource_type == None and resource_name == None:
                # returns the resources for the namespace
                return self.resource_namespace_resources_list_map.get(resource_namespace, [])
            # in case the type is defined
            elif not resource_type == None and resource_name == None:
                resources_list = []
                return_list = []

                if resource_namespace in self.resource_namespace_resources_list_map:
                    resources_list = self.resource_namespace_resources_list_map[resource_namespace]

                for resource in resources_list:
                    if resource.get_type() == resource_type:
                        return_list.append(resource)

                return return_list
        # in case the name is defined
        elif not resource_name == None:
            # in case only the name is defined
            if resource_namespace == None and resource_type == None:
                # returns the resources for the name
                return self.resource_name_resources_list_map.get(resource_name, [])
            # in case the type is defined
            if resource_namespace == None and not resource_type == None:
                resources_list = []
                return_list = []

                if resource_type in self.resource_type_resources_list_map:
                    resources_list = self.resource_type_resources_list_map[resource_type]

                for resource in resources_list:
                    if resource.get_name() == resource_name:
                        return_list.append(resource)

                return return_list
        # in case the type is defined
        elif not resource_type == None:
            # in case only the type is defined
            if resource_namespace == None and resource_name == None:
                # returns the resources for the type
                return self.resource_type_resources_list_map.get(resource_type, [])

        # returns an empty list by default
        return []

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        @rtype: Dictionary
        @return: The system information map.
        """

        # creates the map to hold the system base information (ordered  map)
        resource_manager_base_information = colony.libs.structures_util.OrderedMap()

        # retrieves the resource namespace resources list map and sorts
        # the items (allows a better view)
        resource_namespace_resources_list_map_items = self.resource_namespace_resources_list_map.items()
        resource_namespace_resources_list_map_items.sort()

        # iterates over all the resources lists in the resource namespace
        # resources list map, to creates the resource manager base information
        for _resource_namespace, resources_list in resource_namespace_resources_list_map_items:
            # iterates over all the resources in the resources
            # list to create the resource manager base information
            for resource in resources_list:
                # retrieves the resource (complete) name
                resource_name = resource.id

                # retrieves the resource type, to use to retrieve
                # appropriate value representation
                resource_type = resource.type

                # in case the resource is of a type that may be visually
                # representable
                if resource_type in (STRING_TYPE, BOOLEAN_TYPE, INTEGER_TYPE, FLOAT_TYPE):
                    resource_value = unicode(resource.data)
                # otherwise it's not possible to represent the resource
                # visually
                else:
                    # sets the resource value with the not available
                    # string value
                    resource_value = u"N/A"

                # sets the instance value for the resource manager
                # base information
                resource_manager_base_information[resource_name] = (
                        resource_type,
                        resource_value
                )

        # defines the resource manager base item columns
        resource_manager_base_item_columns = [
            {
                "type" : "name",
                "value" : "Name"
            },
            {
                "type" : "value",
                "value" : "Type"
            },
            {
                "type" : "value",
                "value" : "Value"
            }
        ]

        # creates the resource manager base item
        resource_manager_base_item = {}

        # sets the resource manager base values
        resource_manager_base_item["type"] = "map"
        resource_manager_base_item["columns"] = resource_manager_base_item_columns
        resource_manager_base_item["values"] = resource_manager_base_information

        # creates the map to hold the system plugins information (ordered  map)
        resource_manager_plugins_information = colony.libs.structures_util.OrderedMap()

        # retrieves the plugin id configuration resources list map and sorts
        # the items (allows a better view)
        plugin_id_configuration_resources_list_map_items = self.plugin_id_configuration_resources_list_map.items()
        plugin_id_configuration_resources_list_map_items.sort()

        # iterates over all the resources lists in the resource namespace
        # resources list map, to creates the resource manager plugins information
        for plugin_id, resources_list in plugin_id_configuration_resources_list_map_items:
            # iterates over all the resources in the resources
            # list to create the resource manager plugins information
            for resource in resources_list:
                # retrieves the resource (complete) name (using
                # the plugin id)
                resource_name = plugin_id + "." + resource.name

                # retrieves the resource type, to use to retrieve
                # appropriate value representation
                resource_type = resource.type

                # in case the resource is of a type that may be visually
                # representable
                if resource_type in (STRING_TYPE, BOOLEAN_TYPE, INTEGER_TYPE, FLOAT_TYPE):
                    resource_value = unicode(resource.data)
                # otherwise it's not possible to represent the resource
                # visually
                else:
                    # sets the resource value with the not available
                    # string value
                    resource_value = u"N/A"

                # sets the instance value for the resource manager
                # plugins information
                resource_manager_plugins_information[resource_name] = (
                        resource_type,
                        resource_value
                )

        # defines the resource manager plugins item columns
        resource_manager_plugins_item_columns = [
            {
                "type" : "name",
                "value" : "Plugin Identifier"
            },
            {
                "type" : "value",
                "value" : "Type"
            },
            {
                "type" : "value",
                "value" : "Value"
            }
        ]

        # creates the resource manager plugins item
        resource_manager_plugins_item = {}

        # sets the resource manager plugins values
        resource_manager_plugins_item["type"] = "map"
        resource_manager_plugins_item["columns"] = resource_manager_plugins_item_columns
        resource_manager_plugins_item["values"] = resource_manager_plugins_information

        # creates the system information (item)
        system_information = {}

        # sets the system information (item) values
        system_information["name"] = "Resource Manager"
        system_information["items"] = [
            resource_manager_base_item,
            resource_manager_plugins_item
        ]

        # returns the system information
        return system_information

    def load_resource_parser_plugin(self, resource_parser_plugin):
        resource_parser_name = resource_parser_plugin.get_resource_parser_name()

        self.resource_parser_plugins_map[resource_parser_name] = resource_parser_plugin

    def unload_resource_parser_plugin(self, resource_parser_plugin):
        resource_parser_name = resource_parser_plugin.get_resource_parser_name()

        del self.resource_parser_plugins_map[resource_parser_name]

    def _load_resources_directory(self, directory_path):
        """
        Loads the resources in the directory with
        the given path.

        @type directory_path: String
        @param directory_path: The directory path to search for resources.
        """

        # in case the directory path does not exists
        if not os.path.exists(directory_path):
            # returns immediately
            return

        # retrieves the resources path directory contents
        resources_path_directory_contents = os.listdir(directory_path)

        # iterates over the resources path directory contents
        # to load them in the resource manager
        for resources_path_item in resources_path_directory_contents:
            # creates the resources full path item
            resources_full_path_item = os.path.join(directory_path, resources_path_item)

            # in case the resources path item represents a valid resource
            # file (it must be parsed)
            if self.is_resource_name(resources_path_item):
                # parses the resources description file
                self.parse_file(resources_full_path_item, directory_path)
            # otherwise in case the resources full path is a directory
            # path a descent must be done
            elif os.path.isdir(resources_full_path_item):
                # loads the resources for the directory
                self._load_resources_directory(resources_full_path_item)

    def _invalidate_real_string_value_cache(self):
        """
        Invalidates the real string value cache.
        Required to provide a fast way to maintain cache
        coherence.
        """

        # in case the string value real string value map
        # is empty (nothing to do)
        if self.string_value_real_string_value_map:
            # returns immediately
            return

        # clears the string value real string value map
        self.string_value_real_string_value_map.clear()

class Resource:
    """
    Class to describe a miscellaneous resource.
    """

    namespace = "none"
    """ The namespace of the resource """

    name = "none"
    """ The name of the resource """

    type = "none"
    """ The type of the resource """

    data = None
    """ The data of the resource """

    def __init__(self, namespace, name, type, data):
        """
        Constructor of the class.

        @type namespace: String
        @param namespace: The namespace of the resource.
        @type name: String
        @param name: The name of the resource.
        @type type: String
        @param type: The type of the resource.
        @type data: Object
        @param data: The data of the resource
        """

        self.namespace = Namespace(namespace)
        self.name = name
        self.type = type
        self.id = namespace + "." + name
        self.data = data

    def get_namespace(self):
        """
        Retrieves the namespace.

        @rtype: String
        @return: The namespace.
        """

        return self.namespace

    def set_namespace(self, namespace):
        """
        Sets the namespace.

        @type namespace: String
        @param namespace: The namespace.
        """

        self.namespace = namespace

    def get_name(self):
        """
        Retrieves the name.

        @rtype: String
        @return: The name.
        """

        return self.name

    def set_name(self, name):
        """
        Sets the name.

        @type name: String
        @param name: The name.
        """

        self.name = name

    def get_type(self):
        """
        Retrieves the type.

        @rtype: String
        @return: The type.
        """

        return self.type

    def set_type(self, type):
        """
        Sets the type.

        @type type: String
        @param type: The type.
        """

        self.type = type

    def get_id(self):
        """
        Retrieves the id.

        @rtype: String
        @return: The id.
        """

        return self.id

    def set_id(self, id):
        """
        Sets the id.

        @type id: String
        @param id: The id.
        """

        self.id = id

    def get_data(self):
        """
        Retrieves the data.

        @rtype: Object
        @return: The data.
        """

        return self.data

    def set_data(self, data):
        """
        Sets the data.

        @type data: Object
        @param data: The data.
        """

        self.data = data

class Namespace:
    """
    Class to describe a neutral structure for a namespace.
    """

    list_value = []
    """ The value of the namespace described as a list """

    def __init__(self, string_value = None):
        """
        Constructor of the class.

        @type string_value: String
        @param string_value: The string value of the namespace.
        """

        # in case a string value is defined
        if string_value:
            # splits the string value around the dot
            # to retrieve the list of strings
            self.list_value = string_value.split(".")
        # in case no string value is defined
        else:
            # seas the (default) empty list
            self.list_value = []

    def __eq__(self, namespace):
        # retrieves the list value for self
        list_value_self = self.list_value

        # retrieves the list value for namespace
        list_value_namespace = namespace.list_value

        # in case some of the lists is invalid
        if not list_value_self or not list_value_namespace:
            # returns false
            return False

        # retrieves the length of the list value for self
        length_self = len(list_value_self)

        # retrieves the length of the list value for namespace
        length_namespace = len(list_value_namespace)

        # in case the lengths for the list are different
        if not length_self == length_namespace:
            # returns false
            return False

        # iterates over all the lists
        for index in range(length_self):
            # compares both values
            if list_value_self[index] != list_value_namespace[index]:
                # returns false
                return False

        # returns true
        return True

    def __ne__(self, namespace):
        return not self.__eq__(namespace)

    def is_sub_namespace(self, namespace):
        """
        Tests if the given namespace is sub namespace.

        @type namespace: Namespace
        @param namespace: The namespace to be tested.
        @rtype: bool
        @return: The result of the is sub namespace test.
        """

        list_value_self = self.list_value
        list_value_namespace = namespace.list_value

        if not list_value_self or not list_value_namespace:
            return False

        len_self = len(list_value_self)
        len_namespace = len(list_value_namespace)

        if len_namespace <= len_self:
            return False

        for index in range(len_self):
            if list_value_self[index] != list_value_namespace[index]:
                return False

        return True

    def is_namespace_or_sub_namespace(self, namespace):
        """
        Tests if the given namespace is a namespace or sub namespace.

        @type namespace: Namespace
        @param namespace: The namespace to be tested.
        @rtype: bool
        @return: The result of the is namespace or sub namespace test.
        """

        if self.__eq__(namespace) or self.is_sub_namespace(namespace):
            return True
        else:
            return False

    def get_list_value(self):
        """
        Retrieves the list value.

        @rtype: List
        @return: The list value.
        """

        return self.list_value

    def set_list_value(self, list_value):
        """
        Sets the list value.

        @type list_value: List
        @param list_value: The list value.
        """

        self.list_value = list_value
