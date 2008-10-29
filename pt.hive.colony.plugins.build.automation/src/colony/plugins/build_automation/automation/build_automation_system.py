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
import re
import copy

import os.path

import build_automation_exceptions
import build_automation_parser

BASE_AUTOMATION_ID = "pt.hive.colony.plugins.build.automation.base"

VARIABLE_REGEX = "\$\{[^\}]*\}"

EXCLUSION_LIST = ["__doc__", "__init__", "__module__"]

class BuildAutomation:
    """
    The build automation class.
    """

    build_automation_plugin = None
    """ The build automation plugin """

    base_build_automation_structure = None
    """ the base build automation structure """

    stages = ["compile", "test", "package", "install", "deploy", "clean", "site", "site-deploy"]
    """ The build automation stages """

    def __init__(self, build_automation_plugin):
        """
        Constructor of the class.
        
        @type build_automation_plugin: BuildAutomationPlugin
        @param build_automation_plugin: The build automation plugin.
        """

        self.build_automation_plugin = build_automation_plugin

    def get_base_build_automation_structure(self):
        """
        Retrieves the base build automation structure.
        
        @rtype: BuildAutomationStructure
        @return: The base build automation structure.
        """

        # in case the structure has been already generated
        if self.base_build_automation_structure:
            return self.base_build_automation_structure

        # retrieves the build automation plugin path
        build_automation_plugin_path = self.build_automation_plugin.manager.get_plugin_path_by_id(self.build_automation_plugin.id)

        # creates the base baf xml path
        base_baf_xml_path = build_automation_plugin_path + "/build_automation/automation/resources/base_baf.xml"

        # creates the base build automation file parser
        base_build_automation_file_parser = build_automation_parser.BuildAutomationFileParser(base_baf_xml_path)

        # parses the base baf xml file
        base_build_automation_file_parser.parse()

        # retrieves the base build automation value
        base_build_automation = base_build_automation_file_parser.get_value()

        # generates the base build automation structure
        self.base_build_automation_structure = self.generate_build_automation_structure(base_build_automation)

        # returns the base build automation structure
        return self.base_build_automation_structure

    def get_build_automation_structure(self, build_automation_id, build_automation_version = None):
        """
        Retrieves the build automation structure with the given id and version.
        
        @type build_automation_id: String
        @param build_automation_id: The build automation id.
        @type build_automation_version: String
        @param build_automation_version: The build automation version.
        @rtype: BuildAutomationStructure
        @return: The build automation structure with the given id and version.
        """

        for build_automation_item_plugin in self.build_automation_plugin.build_automation_item_plugins:
            if build_automation_item_plugin.id == build_automation_id and (build_automation_item_plugin.version == build_automation_version or not build_automation_version):
                # retrieves the build automation item plugin id                
                build_automation_item_plugin_id = build_automation_item_plugin.id

                # retrieves the build automation item plugin version
                build_automation_item_plugin_version = build_automation_item_plugin.version

                # retrieves the build automation file path
                build_automation_file_path = build_automation_item_plugin.get_build_automation_file_path()

                # creates the build automation file parser
                build_automation_file_parser = build_automation_parser.BuildAutomationFileParser(build_automation_file_path)

                # parses the build automation file
                build_automation_file_parser.parse()

                # retrieves the build automation value
                build_automation = build_automation_file_parser.get_value()

                # generates the build automation structure
                build_automation_structure = self.generate_build_automation_structure(build_automation)

                # return the build automation structure
                return build_automation_structure

    def run_automation_plugin_id_version(self, plugin_id, plugin_version = None):
        """
        Runs all the automation plugins for the given plugin id and version
        
        @type plugin_id: String
        @param plugin_id: The id of the plugin to run all the automation plugins.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to run the automation plugins.
        """

        # retrieves the build automation structure
        build_automation_structure = self.get_build_automation_structure(plugin_id, plugin_version)

        # in case the retrieval of the build automation structure was unsuccessful
        if not build_automation_structure:
            return

        # creates the build automation directories
        self.create_build_automation_directories(build_automation_structure)

        # retrieves all the automation plugins
        all_automation_plugins = build_automation_structure.get_all_automation_plugins()

        # iterates over all of the automation plugins
        for automation_plugin in all_automation_plugins:
            # retrieves the automation plugin id
            automation_plugin_id = automation_plugin.id

            # retrieves the automation plugin version
            automation_plugin_version = automation_plugin.version

            # creates the automation plugin tuple
            automation_plugin_tuple = (automation_plugin_id, automation_plugin_version)
            
            # retrieves the automation plugin configurations
            automation_plugin_configurations = build_automation_structure.get_all_automation_plugin_configurations(automation_plugin_tuple)

            # runs the automation
            automation_plugin.run_automation(build_automation_structure.associated_plugin, "main", automation_plugin_configurations, build_automation_structure)

    def generate_build_automation_structure(self, build_automation_parsing_structure):
        """
        Generates a build automation structure object from the given build automation parsing structure.
        
        @type build_automation_parsing_structure: BuildAutomation
        @param build_automation_parsing_structure: The build automation parsing structure to generate the build automation structure.
        @rtype: BuildAutomationStructure
        @return: The generated build automation structure object.
        """

        # initializes the build automation structure object
        build_automation_structure = None

        # retrieves the artifact parsing value
        artifact = build_automation_parsing_structure.artifact

        # in case the artifact is of type colony
        if artifact.type == "colony":
            # creates the colony build automation structure object
            build_automation_structure = ColonyBuildAutomationStructure()

            # sets the build automation parsing structure
            build_automation_structure.build_automation_parsing_structure = build_automation_parsing_structure

        # generates the build automation parent structure
        self.generate_build_automation_parent_structure(build_automation_parsing_structure, build_automation_structure)

        # generates the build automation artifact structure
        self.generate_build_automation_artifact_structure(build_automation_parsing_structure, build_automation_structure)

        # generates the build automation build structure
        self.generate_build_automation_build_structure(build_automation_parsing_structure, build_automation_structure)

        # generates the build automation profiles structure
        self.generate_build_automation_profiles_structure(build_automation_parsing_structure, build_automation_structure)

        # returns the build automation structure object
        return build_automation_structure

    def generate_build_automation_parent_structure(self, build_automation_parsing_structure, build_automation_structure):
        # retrieves the parent parsing value
        parent = build_automation_parsing_structure.parent

        # retrieves the artifact parsing value
        artifact = build_automation_parsing_structure.artifact

        # in case there is no parent defined
        if not parent:
            # in case the artifact is not the base one
            if not artifact.id == BASE_AUTOMATION_ID:
                # retrieves the base build automation structure
                base_build_automation_structure = self.get_base_build_automation_structure()

                # sets the build automation structure as the base one
                build_automation_structure.parent = base_build_automation_structure

    def generate_build_automation_artifact_structure(self, build_automation_parsing_structure, build_automation_structure):
        # retrieves the artifact parsing value
        artifact = build_automation_parsing_structure.artifact

        # retrieves the artifact id
        artifact_id = self.parse_string(artifact.id, build_automation_structure)

        # retrieves the artifact version
        artifact_version = self.parse_string(artifact.version, build_automation_structure)

        # retrieves the plugin manager
        manager = self.build_automation_plugin.manager

        # retrieves the associated plugin
        associated_plugin = manager.get_plugin_by_id_and_version(artifact_id, artifact_version)

        # sets the associated plugin in the build automation structure
        build_automation_structure.associated_plugin = associated_plugin

    def generate_build_automation_build_structure(self, build_automation_parsing_structure, build_automation_structure):
        # retrieves the build parsing value
        build = build_automation_parsing_structure.build

        if build.default_stage:
            # retrieves the build default stage
            build_automation_default_stage = build.default_stage
            build_automation_structure.build_properties["default_stage"] = build_automation_default_stage

        if build.directory:
            # retrieves the build directory
            build_automation_directory = build.directory
            build_automation_structure.build_properties["directory"] = build_automation_directory

        if build.output_directory:
            # retrieves the build output directory
            build_automation_output_directory = build.directory
            build_automation_structure.build_properties["output_directory"] = build_automation_output_directory

        if build.final_name:
            # retrieves the build final name
            build_automation_final_name = build.final_name
            build_automation_structure.build_properties["final_name"] = build_automation_final_name

        if build.source_directory:
            # retrieves the build source directory
            build_automation_source_directory = build.source_directory
            build_automation_structure.build_properties["source_directory"] = build_automation_source_directory

        # retrieves the list of build automation dependencies
        build_automation_dependencies = build.dependencies

        # iterates over all the build automation dependencies
        for build_automation_dependency in build_automation_dependencies:
            # retrieves the build automation dependency id
            build_automation_dependency_id = build_automation_dependency.id

            # retrieves the build automation dependency version
            build_automation_dependency_version = build_automation_dependency.version

        # retrieves the list of build automation plugins
        build_automation_plugins = build.plugins

        # iterates over all the build automation plugins
        for build_automation_plugin in build_automation_plugins:
            # retrieves the build automation plugin id
            build_automation_plugin_id = build_automation_plugin.id

            # retrieves the build automation version
            build_automation_plugin_version = build_automation_plugin.version

            # creates the build automation plugin tuple
            build_automation_plugin_tuple = (build_automation_plugin_id, build_automation_plugin_version)

            # retrieves the build automation plugin instance
            build_automation_plugin_instance = self.get_build_automation_extension_plugin(build_automation_plugin_id, build_automation_plugin_version)

            # appends the build automation plugin instance to the automation plugins list
            build_automation_structure.automation_plugins.append(build_automation_plugin_instance)

            # retrieves the build automation plugin configuration
            build_automation_plugin_configuration = build_automation_plugin.configuration

            # initializes the map containing the automation plugins configurations for the current build automation plugin
            build_automation_structure.automation_plugins_configurations[build_automation_plugin_tuple] = {}

            # retrieves all the build automation plugin configuration item names
            build_automation_plugin_configuration_item_names = dir(build_automation_plugin_configuration)

            # filters all the build automation plugin configuration item names 
            build_automation_plugin_configuration_filtered_item_names = [value for value in build_automation_plugin_configuration_item_names if value not in EXCLUSION_LIST]

            # iterates over all the build automation plugin configuration filtered item names
            for build_automation_plugin_configuration_filtered_item_name in build_automation_plugin_configuration_filtered_item_names:
                # retrieves the build automation plugin configuration item
                build_automation_plugin_configuration_item = getattr(build_automation_plugin_configuration, build_automation_plugin_configuration_filtered_item_name)

                # parses the string value
                parsed_build_automation_plugin_configuration_item = self.parse_string(build_automation_plugin_configuration_item, build_automation_structure)

                # retrieves the map containing the automation plugins configurations for the current build automation plugin
                build_automation_plugin_automation_plugins_configurations = build_automation_structure.automation_plugins_configurations[build_automation_plugin_tuple]

                # adds the value to the map containing the automation plugins configurations for the current build automation plugin
                build_automation_plugin_automation_plugins_configurations[build_automation_plugin_configuration_filtered_item_name] = parsed_build_automation_plugin_configuration_item

    def generate_build_automation_profiles_structure(self, build_automation_parsing_structure, build_automation_structure): 
        # retrieves the profiles parsing value
        profiles = build_automation_parsing_structure.profiles
        
    def create_build_automation_directories(self, build_automation_structure):
        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the directory path value
        directory_path = build_properties["directory"]

        # in case the directory does not exist
        if not os.path.isdir(directory_path):
            # creates the directory
            os.mkdir(directory_path)

    def get_build_automation_extension_plugin(self, plugin_id, plugin_version = None):
        """
        Retrieves the build automation extension plugin with the given id and version.
        
        @type plugin_id: String
        @param plugin_id: The id of the build automation extension plugin to retrive.
        @type plugin_version: String
        @param plugin_version: The version of the build automation plugin to retrieve.
        @rtype: Plugin
        @return: The build automation extension plugin with the given id and version.
        """

        # iterates over all the build automation extension plugins
        for build_automation_extension_plugin in self.build_automation_plugin.build_automation_extension_plugins:
            if plugin_version:
                if build_automation_extension_plugin.id == plugin_id and build_automation_extension_plugin.version == plugin_version:
                    return build_automation_extension_plugin
            else:
                if build_automation_extension_plugin.id == plugin_id:
                    return build_automation_extension_plugin

    def parse_string(self, string, build_automation_structure):
        """
        Parses a string for the given build automation structure.
        
        @type string: String
        @param string: The string to be parsed in the given build automation structure context.
        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The build automation structure to be used in the string parsing.
        @rtype: String
        @return: The string parsed in the given build automation context.
        """

        # compiles the regular expression generating the pattern
        pattern = re.compile(VARIABLE_REGEX) 

        # retrieves the match iterator
        match_iterator = pattern.finditer(string)

        # iterates using the match iterator
        for match in match_iterator:
            # retrieves the match group
            group = match.group()

            # retrieves the variable value
            variable_value = group[2:-1]

            # retrieves the variable list value
            variable_list_value = variable_value.split(".")

            # retrieves the variable list value without build_automation
            variable_list_value_replaced = variable_list_value[1:]

            # retrieves the real variable value
            real_variable_value = self.get_variable_value(variable_value, variable_list_value_replaced, build_automation_structure)

            # replaces the value in the string
            string = string.replace(group, real_variable_value)

        # returns the string value
        return string

    def get_variable_value(self, variable_value, variable_list_value, build_automation_structure):
        # creates the is valid boolean flag
        is_valid = True
        
        # sets the current structure selection to the build automation parsing structure
        current_structure_selection = build_automation_structure.build_automation_parsing_structure

        # iterates over the variable list value
        for variable_list_value_item in variable_list_value:
            if hasattr(current_structure_selection, variable_list_value_item):
                current_structure_selection = getattr(current_structure_selection, variable_list_value_item)
                if current_structure_selection == None or current_structure_selection == "none":
                    is_valid = False
                    break

        if not is_valid:
            if build_automation_structure.parent:
                current_structure_selection = self.get_variable_value(variable_value, variable_list_value, build_automation_structure.parent)
            else:
                raise build_automation_exceptions.InvalidVaribleException("variable: " + variable_value + " does not exist in this context")

        return current_structure_selection

class BuildAutomationStructure:
    """
    The build automation structure class.
    """

    parent = None
    build_properties = {}
    dependecy_plugins = []
    automation_plugins = []
    automation_plugins_configurations = {}

    build_automation_parsing_structure = None
    """ The associated build automation parsing structure """

    def __init__(self, parent = None, build_automation_parsing_structure = None):
        """
        Constructor of the class.
        
        @type parent: BuildAutomationStructure
        @param parent: The parent build automation structure.
        """

        self.parent = parent
        self.build_automation_parsing_structure = build_automation_parsing_structure

        self.build_properties = {}
        self.dependecy_plugins = []
        self.automation_plugins = []
        self.automation_plugins_configurations = {}

    def get_all_build_properties(self):
        # creates a copy of the build properties map
        build_properties = copy.copy(self.build_properties)

        # in case it contains a parent
        if self.parent:
            # retrieves all of the build properties from the parent
            build_properties_parent = self.parent.get_all_build_properties()

            # copies the contains of the build properties from the parent to the build properties
            copy_map(build_properties_parent, build_properties)

        # returns the build properties
        return build_properties

    def get_all_automation_plugins(self):
        """
        Retrieves all the automation plugins using a recursive approach.
        
        @rtype: List
        @return: A list containing all the automation plugins.
        """

        # creates a copy of the automation plugins list
        automation_plugins = copy.copy(self.automation_plugins)

        # in case it contains a parent
        if self.parent:
            # retrieves all of the automation plugins from the parent
            automation_plugins_parent = self.parent.get_all_automation_plugins()

            # appends all of the automation plugins from the parent to itself
            automation_plugins.extend(automation_plugins_parent)

        # returns the automation plugins
        return automation_plugins

    def get_all_automation_plugin_configurations(self, automation_plugin_tuple):
        """
        Retrieves all the automation plugin configurations using a recursive approach.
        
        @type automation_plugin_tuple: Tuple
        @param automation_plugin_tuple: The automation plugin tuple containg both the id and version of the automation plugin.
        @rtype: Dictionary
        @return: A map containing all the automation plugin configurations.
        """

        if automation_plugin_tuple in self.automation_plugins_configurations:
            # creates a copy of the automation plugins configurations for the given automation plugin tuple
            automation_plugins_configurations = copy.copy(self.automation_plugins_configurations[automation_plugin_tuple])
        else:
            # creates a default automation plugins configurations
            automation_plugins_configurations = {}

        # in case it contains a parent
        if self.parent:
            # retrieves all of the automation plugins configurations from the parent
            automation_plugins_configurations_parent = self.parent.get_all_automation_plugin_configurations(automation_plugin_tuple)

            # copies the contains of the automation plugins configurations from the parent to the automation plugins configurations
            copy_map(automation_plugins_configurations_parent, automation_plugins_configurations)

        # returns the automation plugins configurations
        return automation_plugins_configurations

class ColonyBuildAutomationStructure(BuildAutomationStructure):
    """
    The colony build automation structure class.
    """

    associated_plugin = None
    """ The associated colony plugin """

    def __init__(self, parent = None, associated_plugin = None):
        """
        Constructor of the class.
        
        @type parent: BuildAutomationStructure
        @param parent: The parent build automation structure.
        @type associated_plugin: Plugin
        @param associated_plugin: The associated colony plugin.
        """

        BuildAutomationStructure.__init__(self, parent)
        self.associated_plugin = associated_plugin

def copy_map(source_map, destiny_map):
    """
    Copies the contains of the source map to the destiny map.
    
    @type source_map: Dictionary
    @param source_map: The source map of the copy.
    @type destiny_map: Dictionary
    @param destiny_map: The destiny map of the copy.
    """

    # iterates over all the source map keys
    for source_map_key in source_map:
        # retrieves the source map value
        source_map_value = source_map[source_map_key]

        # in case the key is not present in the destiny map
        if not source_map_key in destiny_map or destiny_map[source_map_key] == None or destiny_map[source_map_key] == "none":
            # adds the value to the destiny map
            destiny_map[source_map_key] = source_map_value
