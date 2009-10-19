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

import resource_manager_parser

BASE_RESOURCES_PATH = "/resources/resource_manager/resources"
""" The base resources path """

RESOURCES_SUFIX_VALUE = "resources.xml"
""" The resources sufix value """

RESOURCES_SUFIX_LENGTH = 13
""" The resources sufix length """

RESOURCES_SUFIX_START_INDEX = -13
""" The resources sufix value """

ENVIRONMENT_VARIABLE_REGEX = "\$\{[a-zA-Z0-9_]*\}"
""" The regular expression for the environment variable """

GLOBAL_VARIABLE_REGEX = "\$global\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the global variable """

LOCAL_VARIABLE_REGEX = "\$local\{[a-zA-Z0-9_.]*\}"
""" The regular expression for the local variable """

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

    environment_variable_regex = None
    """ The environment variable regular expression used for regular expression match """

    global_variable_regex = None
    """ The global variable regular expression used for regular expression match """

    local_variable_regex = None
    """ The local variable regular expression used for regular expression match """

    def __init__(self, resource_manager_plugin):
        """
        Class constructor.

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

        # compiles the environment variable regular expression
        self.environment_variable_regex = re.compile(ENVIRONMENT_VARIABLE_REGEX)

        # compiles the global variable regular expression
        self.global_variable_regex = re.compile(GLOBAL_VARIABLE_REGEX)

        # compiles the local variable regular expression
        self.local_variable_regex = re.compile(LOCAL_VARIABLE_REGEX)

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

        # retrieves the resources path directory contents
        resources_path_directory_contents = os.listdir(full_resources_path)

        # iterates over the resources path directory contents
        for resources_path_item in resources_path_directory_contents:
            if len(resources_path_item) > RESOURCES_SUFIX_LENGTH and resources_path_item[RESOURCES_SUFIX_START_INDEX:] == RESOURCES_SUFIX_VALUE:
                # creates the resources full path item
                resources_full_path_item = full_resources_path + "/" + resources_path_item

                # parses the resources description file
                self.parse_file(resources_full_path_item, full_resources_path)

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

        # retrieves the plugin manager
        plugin_manager = self.resource_manager_plugin.manager

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
        @param plugin: The plugin to have the resouces registered.
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

        # retrieves the find iterator for the given regular expression
        find_iterator = self.environment_variable_regex.finditer(resource.data)

        # iterates over all the matches in the find iterator
        for match in find_iterator:
            # retrieves the match group
            match_group = match.group()

            # retrieves the variable name
            variable_name = match_group[2:-1]

            # retrieves the variable value
            variable_value = os.environ.get(variable_name, "")

            # sets the new resource data
            resource.data = resource.data.replace(match_group, variable_value)

        # retrieves the find iterator for the given regular expression
        find_iterator = self.global_variable_regex.finditer(resource.data)

        # iterates over all the matches in the find iterator
        for match in find_iterator:
            # retrieves the match group
            match_group = match.group()

            # retrieves the variable name
            variable_name = match_group[8:-1]

            # splits the variable name
            variable_name_splitted = variable_name.split(".")

            # retrieves the global variable
            global_variable = globals()[variable_name_splitted[0]]

            for variable_name in variable_name_splitted[1:]:
                global_variable = getattr(global_variable, variable_name)

            # sets the new resource data
            resource.data = resource.data.replace(match_group, global_variable)

        # retrieves the find iterator for the given regular expression
        find_iterator = self.local_variable_regex.finditer(resource.data)

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

            # retrieves the local variable
            local_variable = locals()[variable_name_splitted[0]]

            for variable_name in variable_name_splitted[1:]:
                local_variable = getattr(local_variable, variable_name)

            # sets the new resource data
            resource.data = resource.data.replace(match_group, global_variable)

        # in case the resource type is integer
        if resource_type == "integer":
            resource.data = int(resource.data)
        # in case the resource type is float
        elif resource_type == "float":
            resource.data = float(resource.data)
        # in case the resource type is string
        elif resource_type == "string":
            resource.data = str(resource.data)
        elif resource_type in self.resource_parser_plugins_map:
            resource_parser_plugin = self.resource_parser_plugins_map[resource_type]
            resource_parser_plugin.parse_resource(resource)
        else:
            # sets the parse resource data handler
            resource.parse_resource_data = self.parse_resource_data

            # returns in failure
            return False

        return True

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

        equals_expression_first_operand = equals_expression.first_operand
        equals_expression_second_operand = equals_expression.second_operand

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

class Resource:
    """
    Class to describe a miscellaneous resource.
    """

    #@todo: comment this
    def __init__(self, namespace, name, type, data):
        self.namespace = Namespace(namespace)
        self.name = name
        self.type = type
        self.id = namespace + "." + name
        self.data = data

    #@todo: comment this
    def get_namespace(self):
        return self.namespace

    #@todo: comment this
    def get_name(self):
        return self.name

    #@todo: comment this
    def get_type(self):
        return self.type

    #@todo: comment this
    def get_id(self):
        return self.id

    #@todo: comment this
    def get_data(self):
        return self.data

    #@todo: comment this
    def set_data(self, data):
        self.data = data

class Namespace:
    """
    Class to describe a neutral structure for a namespace.
    """

    list_value = []
    """ The value of the namespace described as a list """

    #@todo: comment this
    def __init__(self, string_value = None):
        if string_value:
            self.list_value = string_value.split(".")
        else:
            self.list_value = []

    #@todo: comment this
    def __eq__(a, b):
        list_value_a = a.list_value
        list_value_b = b.list_value

        if not list_value_a or not list_value_b:
            return False

        len_a = len(list_value_a)
        len_b = len(list_value_b)

        if len_a != len_b:
            return False

        for index in range(len_a):
            if list_value_a[index] != list_value_b[index]:
                return False

        return True

    #@todo: comment this
    def __ne__(a, b):
        return not self.__eq__(a, b)

    #@todo: comment this
    def eq(a, b):
        return self.__eq__(a, b)

    #@todo: comment this
    def ne(a, b):
        return self.__neq__(a, b)

    #@todo: comment this
    def is_sub_namespace(self, event):

        list_value_self = self.list_value
        list_value_event = event.list_value

        if not list_value_self or not list_value_event:
            return False

        len_self = len(list_value_self)
        len_event = len(list_value_event)

        if len_event <= len_self:
            return False

        for index in range(len_self):
            if list_value_self[index] != list_value_event[index]:
                return False

        return True

    #@todo: comment this
    def is_namespace_or_sub_namespace(self, event):
        if self.__eq__(event) or self.is_sub_event(event):
            return True
        else:
            return False

    #@todo: comment this
    def get_list_value(self):
        return self.list_value

    #@todo: comment this
    def set_list_value(self, list_value):
        self.list_value = list_value
