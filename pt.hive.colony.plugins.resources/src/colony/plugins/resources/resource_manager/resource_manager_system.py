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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import resource_manager_parser

BASE_RESOURCES_PATH = "/resources/resource_manager/resources"
""" The base resources path """

RESOURCES_SUFIX_VALUE = "resources.xml"
""" The resources sufix value """

RESOURCES_SUFFIX_LENGTH = 13
""" The resources suffix length """

RESOURCES_SUFFIX_START_INDEX = -13
""" The resources suffix value """

ENVIRONMENT_VARIABLE_REGEX = "\$\{[a-zA-Z0-9_]*\}"
""" The regular expression for the environment variable """

RESOURCE_VARIABLE_REGEX = "\$resource\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the resource variable """

GLOBAL_VARIABLE_REGEX = "\$global\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the global variable """

LOCAL_VARIABLE_REGEX = "\$local\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the local variable """

COLONY_VALUE = "colony"
""" The colony value """

MANAGER_PATH_VALUE = "manager_path"
""" The manager path value """

STRING_VALUE = "string"
""" The string value """

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

    environment_variable_regex = None
    """ The environment variable regular expression used for regular expression match """

    resource_variable_regex = None
    """ The resource variable regular expression used for regular expression match """

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

        # compiles the environment variable regular expression
        self.environment_variable_regex = re.compile(ENVIRONMENT_VARIABLE_REGEX)

        # compiles the resource variable regular expression
        self.resource_variable_regex = re.compile(RESOURCE_VARIABLE_REGEX)

        # compiles the global variable regular expression
        self.global_variable_regex = re.compile(GLOBAL_VARIABLE_REGEX)

        # compiles the local variable regular expression
        self.local_variable_regex = re.compile(LOCAL_VARIABLE_REGEX)

    def load_system(self):
        """
        Loads the system internals, loading the base system resources.
        """

        # loads the internal resourcs
        self.load_internal_resources()

        # loads the base resources
        self.load_base_resources()

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
        self.register_resource(COLONY_VALUE, MANAGER_PATH_VALUE, STRING_VALUE, manager_path)

    def load_base_resources(self):
        """
        Loads the base resources from the description file.
        """

        # retrieves the plugin manager
        manager = self.resource_manager_plugin.manager

        # retrieves the resource manager plugin id
        resource_manager_plugin_id = self.resource_manager_plugin.id

        # retrieves the base plugin path
        plugin_path = manager.get_plugin_path_by_id(resource_manager_plugin_id)

        # constructs the full resources path
        full_resources_path = plugin_path + BASE_RESOURCES_PATH

        # loads the base resources for the entry directory
        self._load_base_resources_directory(full_resources_path)

    def parse_file(self, file_path, full_resources_path):
        # creates the resources file parser
        resources_file_parser = resource_manager_parser.ResourcesFileParser(file_path)

        # parses the file
        resources_file_parser.parse()

        # retrieves the resource list
        resource_list = resources_file_parser.get_value()

        # creates the validation list
        validation_list = [value for value in resource_list if value.__class__ == resource_manager_parser.Validation]

        # iterates over all the validation in the validation
        # list
        for validation in validation_list:
            # processes the validation
            return_value = self.process_validation(validation)

            # in case the return value is invalid
            if not return_value:
                # returns immediately
                return

        # iterates over all the resources in the list
        for resource in resource_list:
            # in case the resource is not of type validation
            if not resource.__class__ == resource_manager_parser.Validation:
                # in case the resource is of type plugin configurations
                if resource.__class__ == resource_manager_parser.PluginConfiguration:
                    for resource_item in resource.resources_list:
                        # processes the resource
                        self.process_resource(resource_item, full_resources_path)
                else:
                    # processes the resources
                    self.process_resource(resource, full_resources_path)

        # creates the plugin configuration list
        plugin_configuration_list = [value for value in resource_list if value.__class__ == resource_manager_parser.PluginConfiguration]

        # creates the base resource list
        base_resource_list = [value for value in resource_list if value.__class__ == resource_manager_parser.Resource]

        # iterates over all the resources in the plugin configuration list
        for plugin_configuration in plugin_configuration_list:
            # retrieves the plugin configuration plugin id
            plugin_configuration_plugin_id = plugin_configuration.plugin_id

            # retrieves the plugin configuration resources list
            plugin_configuration_resources_list = plugin_configuration.resources_list

            # sets the plugin configuration resources list in the plugin id configuration resources list map
            self.plugin_id_configuration_resources_list_map[plugin_configuration_plugin_id] = plugin_configuration_resources_list

        # iterates over all the resources in the base resource list
        for resource in base_resource_list:
            # registers the resource
            self.register_resource(resource.namespace, resource.name, resource.type, resource.data)

    def register_plugin_resources(self, plugin):
        """
        Registers the plugin resources in the plugin.

        @type plugin: Plugin
        @param plugin: The plugin to have the resources registered.
        """

        # retrieves the plugin id
        plugin_id = plugin.id

        # in case the plugin id is not defined in the plugin id configuration resource map
        if not plugin_id in self.plugin_id_configuration_resources_list_map:
            return

        # retrieves the plugin configuration resources list
        plugin_configuration_resources_list = self.plugin_id_configuration_resources_list_map[plugin_id]

        # iterates over all the plugin configuration resources
        for plugin_configuration_resource in plugin_configuration_resources_list:
            # retrieves the plugin configuration resource name
            plugin_configuration_resource_name = plugin_configuration_resource.name

            # sets the plugin configuration resource as configuration property in the plugin
            plugin.set_configuration_property(plugin_configuration_resource_name, plugin_configuration_resource)

    def process_resource(self, resource, full_resources_path):
        """
        Processes a resource.

        @type resource: Resource
        @param resource: The resource to be processed.
        @type full_resources_path: String
        @param full_resources_path: The full resources path.
        """

        # sets the resource full resources path
        resource.full_resources_path = full_resources_path

        return self.parse_resource_data(resource)

    def parse_resource_data(self, resource):
        """
        Parses a resource data value.

        @type resource: Resource
        @param resource: The resource to have the data processed.
        """

        # retrieves the resource type
        resource_type = resource.type

        # sets the resource data as the real string value
        resource.data = self.get_real_string_value(resource.data)

        # in case the resource type is boolean
        if resource_type == "boolean":
            if resource.data == "true":
                resource.data = True
            elif resource.data == "false":
                resource.data = False
            else:
                resource.data = None
        # in case the resource type is integer
        elif resource_type == "integer":
            resource.data = int(resource.data)
        # in case the resource type is float
        elif resource_type == "float":
            resource.data = float(resource.data)
        # in case the resource type is string
        elif resource_type == "string":
            resource.data = unicode(resource.data)
        # in case the resource type exists in the
        # map of resource parser plugins
        elif resource_type in self.resource_parser_plugins_map:
            # retrieves the resource parser plugin associated with the
            # resource type
            resource_parser_plugin = self.resource_parser_plugins_map[resource_type]

            # parses the resource with the resource parser plugin
            resource_parser_plugin.parse_resource(resource)
        else:
            # sets the parse resource data handler
            resource.parse_resource_data = self.parse_resource_data

            # returns in failure
            return False

        # returns valid (success)
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

            # retrieves the variable value
            variable_value = os.environ.get(variable_name, "")

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

        # if the resource already exists remove it from all indexes
        if self.is_resource_registered(resource.get_id()):
            self.unregister_resource(resource.get_id())

        self.resource_id_resource_map[resource.get_id()] = resource

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
        current_namespace = ""
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
            old_resource = self.resource_id_resource_map[resource_id]
            del self.resource_id_resource_map[resource_id]
            self.resource_name_resources_list_map[old_resource.get_name()].remove(old_resource)
            self.resource_type_resources_list_map[old_resource.get_type()].remove(old_resource)
            namespace_values_list = old_resource.get_namespace().get_list_value()
            current_namespace = ""
            for namespace in namespace_values_list:
                if not current_namespace == "":
                    current_namespace += "."
                current_namespace += namespace
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

        if resource_id in self.resource_id_resource_map:
            return True
        else:
            return False

    def get_resource(self, resource_id):
        """
        Retrieves the resource with the given resource id.

        @type resource_id: String
        @param resource_id: The id of the resource to be retrieved.
        @rtype: Resource
        @return: The resource with the given id.
        """

        if resource_id in self.resource_id_resource_map:
            return self.resource_id_resource_map[resource_id]

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

        # none
        if resource_namespace == None and resource_name == None and resource_type == None:
            return self.resource_id_resource_map.values()
        # namespace, name
        elif not resource_namespace == None and not resource_name == None:
            return self.get_resource(resource_namespace + "." + resource_name)
        elif not resource_namespace == None:
            # namespace
            if resource_type == None and resource_name == None:
                if resource_namespace in self.resource_namespace_resources_list_map:
                    return self.resource_namespace_resources_list_map[resource_namespace]
            # namespace, type
            elif not resource_type == None and resource_name == None:
                resources_list = []
                return_list = []
                if resource_namespace in self.resource_namespace_resources_list_map:
                    resources_list = self.resource_namespace_resources_list_map[resource_namespace]
                for resource in resources_list:
                    if resource.get_type() == resource_type:
                        return_list.append(resource)
                return return_list
        elif not resource_name == None:
            # name
            if resource_namespace == None and resource_type == None:
                if resource_name in self.resource_name_resources_list_map:
                    return self.resource_name_resources_list_map[resource_name]
            # name, type
            if resource_namespace == None and not resource_type == None:
                resources_list = []
                return_list = []
                if resource_type in self.resource_type_resources_list_map:
                    resources_list = self.resource_type_resources_list_map[resource_type]
                for resource in resources_list:
                    if resource.get_name() == resource_name:
                        return_list.append(resource)
                return return_list
        elif not resource_type == None:
            # type
            if resource_namespace == None and resource_name == None:
                if resource_type in self.resource_type_resources_list_map:
                    return self.resource_type_resources_list_map[resource_type]
        return []

    def load_resource_parser_plugin(self, resource_parser_plugin):
        resource_parser_name = resource_parser_plugin.get_resource_parser_name()

        self.resource_parser_plugins_map[resource_parser_name] = resource_parser_plugin

    def unload_resource_parser_plugin(self, resource_parser_plugin):
        resource_parser_name = resource_parser_plugin.get_resource_parser_name()

        del self.resource_parser_plugins_map[resource_parser_name]

    def _load_base_resources_directory(self, directory_path):
        """
        Loads the base resources in the directory with
        the given path.

        @type directory_path: String
        @param directory_path: The directory path to search for resources.
        """

        # retrieves the resources path directory contents
        resources_path_directory_contents = os.listdir(directory_path)

        # iterates over the resources path directory contents
        for resources_path_item in resources_path_directory_contents:
            # creates the resources full path item
            resources_full_path_item = directory_path + "/" + resources_path_item

            # in case the length of the resources path item is greater or equal than the resources suffix length
            # and the last item of the resources path item is the same as the resources suffix value
            if len(resources_path_item) >= RESOURCES_SUFFIX_LENGTH and resources_path_item[RESOURCES_SUFFIX_START_INDEX:] == RESOURCES_SUFIX_VALUE:
                # parses the resources description file
                self.parse_file(resources_full_path_item, directory_path)
            elif os.path.isdir(resources_full_path_item):
                # loads the base resources for the directory
                self._load_base_resources_directory(resources_full_path_item)

    def _invalidate_real_string_value_cache(self):
        """
        Invalidates the real string value cache.
        """

        # in case the string value real string value map
        # is not empty
        if self.string_value_real_string_value_map:
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
