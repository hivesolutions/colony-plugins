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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import resource_manager_parser

DESCRIPTION_FILE_PATH = "/misc/resource_manager/resources/base_resources.xml"

class ResourceManager:
    """
    Stores and indexes miscellaneous resources.
    """
    
    parent_plugin = None
    """ Reference to the plugin that owns this object instance. """
    
    resource_id_resource_map = {}
    """ Map associating resource ids with resources. """
    
    resource_name_resources_list_map = {}
    """ Map associating resource name with the correspondent resources. """ 
    
    resource_type_resources_list_map = {}
    """ Map associating resource type with the correspondent resources. """
    
    resource_namespace_resources_list_map = {}
    """ Map associating namespace with the correspondent resources. """

    def __init__(self, parent_plugin):
        """
        Class constructor.
        
        @type parent_plugin: Plugin
        @param parent_plugin: Reference to the plugin that owns this object instance.
        """

        self.parent_plugin = parent_plugin
        self.resource_namespace_resources_list_map = {}
        self.resource_id_resource_map = {}
        self.resource_name_resources_list_map = {}
        self.resource_type_resources_list_map = {}

    def load_base_resources(self):
        """
        Loads the base resources from the description file.
        """

        # retrieves the base plugin path 
        plugin_path = self.parent_plugin.manager.get_plugin_path_by_id(self.parent_plugin.id)

        # constructs the full base resources description file path
        full_path = plugin_path + DESCRIPTION_FILE_PATH

        # creates the resources file parser
        resources_file_parser = resource_manager_parser.ResourcesFileParser(full_path)

        # parses the file
        resources_file_parser.parse()

        # retrieves the resource list
        resource_list = resources_file_parser.get_value()

        # iterates over all the resources in the list
        for resource in resource_list:
            # registers the resource
            self.register_resource(resource.namespace, resource.name, resource.type, resource.data)

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
    
    #@todo: comment this
    def get_resources(self, resource_namespace = None, resource_name = None, resource_type = None):
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

class Resource:
    """
    Describes a miscellaneous resource.
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
    Describes a neutral structure for a namespace.
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
