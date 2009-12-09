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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import stat
import inspect
import logging

class Extension(object):
    """
    The extension class.
    """

    id = "none"
    """ The id of the extension """

    name = "none"
    """ The name of the extension """

    short_name = "none"
    """ The short name of the extension """

    description = "none"
    """ The description of the extension """

    version = "none"
    """ The version of the extension """

    capabilities = []
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    valid = True
    """ The valid flag of the extension """

    manager = None
    """ The parent extension manager """

    def __init__(self, manager = None):
        """
        Constructor of the class.

        @type manager: ExtensionManager
        @param manager: The parent extension manager.
        """

        self.manager = manager

class WikiExtension(Extension):
    """
    The wiki extension class.
    """

    pass

class ExtensionManager:
    """
    The extension manager class.
    """

    extension_class = Extension
    """ The extension class """

    logger = None
    """ The logger used """

    current_id = 0
    """ The current id used for the extension """

    extension_paths = None
    """ The set of paths for the loaded extensions """

    refered_modules = []
    """ The refered modules """

    loaded_extensions = []
    """ The loaded extensions """

    loaded_extensions_map = {}
    """ The map with classes associated with strings containing the id of the extension """

    loaded_extensions_id_map = {}
    """ The map with the id of the extension associated with the extension id """

    id_loaded_extensions_map = {}
    """ The map with the extension id associated with the id of the extension """

    loaded_extensions_descriptions = []
    """ The descriptions of the loaded extensions """

    extension_instances = []
    """ The instances of the created extensions """

    extension_instances_map = {}
    """ The map with instances associated with strings containing the id of the extension """

    extension_dirs_map = {}
    """ The map associating directories with the id of the extension """

    capabilities_extension_instances_map = {}
    """ The map associating capabilities with extension instances """

    capabilities_sub_capabilities_map = {}
    """ The map associating capabilities with sub capabilities """

    def __init__(self, extension_paths = None):
        self.extension_paths = extension_paths

        self.refered_modules = []
        self.loaded_extensions = []
        self.loaded_extensions_map = {}
        self.loaded_extensions_id_map = {}
        self.id_loaded_extensions_map = {}
        self.loaded_extensions_descriptions = []
        self.extension_instances = []
        self.extension_instances_map = {}
        self.extension_dirs_map = {}
        self.capabilities_extension_instances_map = {}
        self.capabilities_sub_capabilities_map = {}

    def get_extension_class(self):
        """
        Retrieves the extension class.

        @rtype: Class
        @return: The extension class.
        """

        return self.extension_class

    def set_extension_class(self, extension_class):
        """
        Sets the extension class.

        @type extension_class: Class
        @param extension_class: The extension class.
        """

        self.extension_class = extension_class

    def start_logger(self, logger = logging):
        """
        Starts the logging system with the given logger.

        @type logger: Logger
        @param logger: The logger object to be used.
        """

        self.logger = logger

    def load_system(self):
        """
        Starts the process of loading the extension system.
        """

        self.logger.info("Starting extension manager...")

        # gets all modules from all extension paths
        for extension_path in self.extension_paths:
            self.refered_modules.extend(self.get_all_modules(extension_path))

        # starts the extension loading process
        self.init_extension_system({"extension_paths": self.extension_paths, "extensions": self.refered_modules})

    def init_extension_system(self, configuration):
        """
        Starts the extension loading process.

        @type configuration: Dictionary
        @param configuration: The configuration structure.
        """

        # adds the defined extension paths to the system python path
        self.set_python_path(configuration["extension_paths"])

        # loads the extension files into memory
        self.load_extensions(configuration["extensions"])

        # starts all the available the extensions
        self.start_extensions()

    def set_python_path(self, extension_paths):
        """
        Updates the python path adding the defined list of extensions paths.

        @type extension_paths: List
        @param extension_paths: The list of python paths to add to the python path.
        """

        # iterates over all the extension paths in extension_paths
        for extension_path in extension_paths:
            # if the path is not in the python lib
            # path inserts the path into it
            if not extension_path in sys.path:
                sys.path.insert(0, extension_path)

    def load_extensions(self, extensions):
        """
        Imports a module starting the extension.

        @type extensions: List
        @param extensions: The list of extensions to be loaded.
        """

        # iterates over all the available extensions
        for extension in extensions:
            # in case the extension module is not currently loaded
            if not extension in sys.modules:
                try:
                    # imports the extension module file
                    __import__(extension)
                except:
                    self.logger.error("Problem importing module %s" % extension)

    def get_all_modules(self, path):
        """
        Retrieves all the modules in a given path.

        @type path: String
        @param path: The path to retrieve the modules.
        @rtype: List
        @return: All the modules in the given path.
        """

        # starts the modules list
        modules = []

        # in case the path does not exist
        if not os.path.exists(path):
            self.logger.warning("Path '%s' does not exist in the current filesystem" % (path))
            return modules

        # retrieves the directory list for the path
        dir_list = os.listdir(path)

        # iterates over all the file names
        # in the directory list
        for file_name in dir_list:
            # creates the full file path
            full_path = path + "/" + file_name

            # retrieves the file mode
            mode = os.stat(full_path)[stat.ST_MODE]

            # in case the file is not a directory
            if not stat.S_ISDIR(mode):
                # splits the path
                split = os.path.splitext(file_name)

                # retrieves the extension
                extension = split[-1]

                # in case the extension is a valid python extension
                if extension == ".py" or extension == ".pyc":
                    # retrieves the module name from the file name
                    module_name = "".join(split[:-1])

                    # in case the module name is not defined
                    # in the modules list
                    if not module_name in modules:
                        # adds the module name to the modules list
                        modules.append(module_name)

        # returns the modules list
        return modules

    def start_extensions(self):
        """
        Starts all the available extension, creating a singleton instance for each of them.
        """

        # retrieves all the extension classes available
        extension_classes = self.get_all_extension_classes(self.extension_class)

        # iterates over all the available extension classes
        for extension in extension_classes:
            # tests the extension for loading
            if not extension in self.loaded_extensions:
                # starts the extension
                self.start_extension(extension)

    def start_extension(self, extension):
        """
        Starts the given extension, creating a singleton instance.

        @type extension: Class
        @param extension: The extension to start.
        """

        # retrieves the extension id
        extension_id = extension.id

        # retrieves the extension version
        extension_version = extension.version

        # retrieves the extension description
        extension_description = extension.description

        # instantiates the extension to create the singleton extension instance
        extension_instance = extension(self)

        # retrieves the path to the extension file
        extension_path = inspect.getfile(extension)

        # retrieves the absolute path to the extension file
        absolute_extension_path = os.path.abspath(extension_path)

        # retrieves the path to the directory containing the extension file
        extension_dir = os.path.dirname(absolute_extension_path)

        # starts all the extension manager structures related with extensions
        self.loaded_extensions.append(extension)
        self.loaded_extensions_map[extension_id] = extension
        self.loaded_extensions_id_map[extension_id] = self.current_id
        self.id_loaded_extensions_map[self.current_id] = extension_id
        self.loaded_extensions_descriptions.append(extension_description)
        self.extension_instances.append(extension_instance)
        self.extension_instances_map[extension_id] = extension_instance
        self.extension_dirs_map[extension_id] = extension_dir

        # registers the extension capabilities in the extension manager
        self.register_extension_capabilities(extension_instance)

        # increments the current id
        self.current_id += 1

    def get_all_extension_classes(self, base_extension_class = Extension):
        """
        Retrieves all the available extension classes, from the defined base extension class.

        @type base_extension_class: Class
        @param base_extension_class: The base extension class to retrieve the extension classes.
        @rtype: List
        @return: The list of extension classes.
        """

        # creates the extension classes list
        extension_classes = []

        # retrieves the extension sub classes
        self.get_extension_sub_classes(base_extension_class, extension_classes)

        # returns the extension classes
        return extension_classes

    def get_extension_sub_classes(self, extension, extension_classes):
        """
        Retrieves all the sub classes for the given extension class.

        @type extension: Class
        @param extension: The extension class to retrieve the sub classes.
        @type extension_classes: List
        @param extension_classes: The current list of extension sub classes.
        @rtype: List
        @return: The list of all the sub classes for the given extension class.
        """

        # retrieves all the extension sub classes
        sub_classes = extension.__subclasses__()

        # iterates over all the extension sub classes
        for sub_class in sub_classes:
            self.get_extension_sub_classes(sub_class, extension_classes)
            if sub_class.valid:
                extension_classes.append(sub_class)

    def register_extension_capabilities(self, extension):
        """
        Registers all the available capabilities for the given extension.

        @type extension: String
        @param extension: The extension to register the capabilities.
        """

        # iterates over all the extension instance capabilities
        for capability in extension.capabilities:
            capability_and_super_capabilites_list = capability_and_super_capabilites(capability)

            for capability_or_super_capability_index in range(len(capability_and_super_capabilites_list)):
                capability = capability_and_super_capabilites_list[capability_or_super_capability_index]
                sub_capabilities_list = capability_and_super_capabilites_list[capability_or_super_capability_index + 1:]

                if not capability in self.capabilities_extension_instances_map:
                    self.capabilities_extension_instances_map[capability] = []
                self.capabilities_extension_instances_map[capability].append(extension)

                if not capability in self.capabilities_sub_capabilities_map:
                    self.capabilities_sub_capabilities_map[capability] = []

                for sub_capability in sub_capabilities_list:
                    if not sub_capability in self.capabilities_sub_capabilities_map[capability]:
                        self.capabilities_sub_capabilities_map[capability].append(sub_capability)

    def unregister_extension_capabilities(self, extension):
        """
        Unregisters all the available capabilities for the given extension.

        @type extension: String
        @param extension: The extension to unregister the capabilities.
        """

        # iterates over all the extension instance capabilities
        for capability in extension.capabilities:
            capability_and_super_capabilites_list = capability_and_super_capabilites(capability)

            for capability_or_super_capability_index in range(len(capability_and_super_capabilites_list)):
                capability = capability_and_super_capabilites_list[capability_or_super_capability_index]
                sub_capabilities_list = capability_and_super_capabilites_list[capability_or_super_capability_index + 1:]

                if capability in self.capabilities_extension_instances_map:
                    if extension in self.capabilities_extension_instances_map[capability]:
                        self.capabilities_extension_instances_map[capability].remove(extension)

                if capability in self.capabilities_sub_capabilities_map:
                    for sub_capability in sub_capabilities_list:
                        if sub_capability in self.capabilities_sub_capabilities_map[capability]:
                            if len(self.capabilities_extension_instances_map[sub_capability]) == 0:
                                self.capabilities_sub_capabilities_map[capability].remove(sub_capability)

    def get_extensions_by_capability(self, capability):
        """
        Retrieves all the extensions with the given capability and sub capabilities.

        @type capability: String
        @param capability: The capability of the extensions to retrieve.
        @rtype: List
        @return: The list of extensions for the given capability and sub capabilities.
        """

        # the results list
        result = []

        # the capability converter to internal capbility structure
        capability_structure = Capability(capability)

        for extension in self.extension_instances:
            extension_capabilities_structure = convert_to_capability_list(extension.capabilities)

            for extension_capability_structure in extension_capabilities_structure:
                if capability_structure.is_capability_or_sub_capability(extension_capability_structure):
                    result.append(extension)

        return result

class Capability:
    """
    Class that describes a neutral structure for a capability.
    """

    list_value = []
    """ The value of the capability described as a list """

    def __init__(self, string_value = None):
        if string_value:
            self.list_value = string_value.split(".")
        else:
            self.list_value = []

    def __eq__(self, capability):
        # retrieves the list value for self
        list_value_self = self.list_value

        # retrieves the list value for capability
        list_value_capability = capability.list_value

        # in case some of the lists is invalid
        if not list_value_self or not list_value_capability:
            # returns false
            return False

        # retrieves the length of the list value for self
        length_self = len(list_value_self)

        # retrieves the length of the list value for capability
        length_capability = len(list_value_capability)

        # in case the lengths for the list are different
        if not length_self == length_capability:
            # returns false
            return False

        # iterates over all the lists
        for index in range(length_self):
            # compares both values
            if list_value_self[index] != list_value_capability[index]:
                # returns false
                return False

        # returns true
        return True

    def __ne__(self, capability):
        return not self.__eq__(capability)

    def capability_and_super_capabilites(self):
        """
        Retrieves the list of the capability and all super capabilities.

        @rtype: List
        @return: The of the capability and all super capabilities.
        """

        capability_and_super_capabilites_list = []

        # retrieves the list value
        list_value_self = self.list_value

        curent_capability_value = None

        for value_self in list_value_self:
            if curent_capability_value:
                curent_capability_value = curent_capability_value + "." + value_self
            else:
                curent_capability_value = value_self
            capability_and_super_capabilites_list.append(curent_capability_value)

        return capability_and_super_capabilites_list

    def is_sub_capability(self, capability):

        list_value_self = self.list_value
        list_value_capability = capability.list_value

        if not list_value_self or not list_value_capability:
            return False

        len_self = len(list_value_self)
        len_capability = len(list_value_capability)

        if len_capability <= len_self:
            return False

        for index in range(len_self):
            if list_value_self[index] != list_value_capability[index]:
                return False

        return True

    def is_capability_or_sub_capability(self, capability):
        if self.__eq__(capability) or self.is_sub_capability(capability):
            return True
        else:
            return False

def capability_and_super_capabilites(capability):
    """
    Retrieves the list of the capability and all super capabilities.

    @rtype: List
    @return: The of the capability and all super capabilities.
    """

    capability_structure = Capability(capability)

    return capability_structure.capability_and_super_capabilites()

def is_capability_or_sub_capability(base_capability, capability):

    base_capability_structure = Capability(base_capability)
    capability_structure = Capability(capability)

    return base_capability_structure.is_capability_or_sub_capability(capability_structure)

def is_capability_or_sub_capability_in_list(base_capability, capability_list):

    for capability in capability_list:
        if is_capability_or_sub_capability(base_capability, capability):
            return True

    return False

def convert_to_capability_list(capability_list):

    capability_list_structure = []

    for capability in capability_list:
        capability_structure = Capability(capability)
        capability_list_structure.append(capability_structure)

    return capability_list_structure
