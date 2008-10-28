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

import copy

import build_automation_parser

BASE_AUTOMATION_ID = "pt.hive.colony.plugins.build.automation.base"

class BuildAutomation:
    """
    The build automation class.
    """

    build_automation_plugin = None
    """ The build automation plugin """

    stages = ["compile", "test", "package", "install", "deploy", "clean", "site", "site-deploy"]
    """ The build automation stages """

    def __init__(self, build_automation_plugin):
        """
        Constructor of the class.
        
        @type build_automation_plugin: BuildAutomationPlugin
        @param build_automation_plugin: The build automation plugin.
        """

        self.build_automation_plugin = build_automation_plugin

    def run_automation_plugin_id(self, plugin_id):
        """
        Runs all the automation plugins for the given plugin id.
        
        @type plugin_id: String
        @param plugin_id: The id of the plugin to run all the automation plugins.
        """

        # retrieves the build automation plugin path
        build_automation_plugin_path = self.build_automation_plugin.manager.get_plugin_path_by_id(self.build_automation_plugin.id)

        # creates the base baf xml path
        base_baf_xml_path = build_automation_plugin_path + "/build_automation/automation/resources/base_baf.xml"

        # creates the build automation file parser
        build_automation_file_parser = build_automation_parser.BuildAutomationFileParser(base_baf_xml_path)

        # parses the baf xml file
        build_automation_file_parser.parse()

        # retrieves the build automation value
        build_automation = build_automation_file_parser.get_value()

        # generates the base build automation structure
        self.base_build_automation_structure = self.generate_build_automation_structure(build_automation)

        for build_automation_item_plugin in self.build_automation_plugin.build_automation_item_plugins:
            if build_automation_item_plugin.id == plugin_id:
               build_automation_file_path = build_automation_item_plugin.get_build_automation_file_path()
               build_automation_file_parser2 = build_automation_parser.BuildAutomationFileParser(build_automation_file_path)
               build_automation_file_parser2.parse()
               build_automation2 = build_automation_file_parser2.get_value()
               build_automation_structure2 = self.generate_build_automation_structure(build_automation2)

               # retrieves all the automation plugins
               all_automation_plugins = build_automation_structure2.get_all_automation_plugins()

               # iterates over all of the automation plugins
               for automation_plugin in all_automation_plugins:
                   automation_plugin.run_automation(build_automation_structure2.associated_plugin, "main", {})

               return

    def generate_build_automation_structure(self, build_automation_parsing_structure):
        # initializes the build automation structure object
        build_automation_structure = None
        
        # retrieves the parent parsing value
        parent = build_automation_parsing_structure.parent

        # retrieves the artifact parsing value
        artifact = build_automation_parsing_structure.artifact

        # retrieves the build parsing value
        build = build_automation_parsing_structure.build

        # retrieves the profiles parsing value
        profiles = build_automation_parsing_structure.profiles

        if artifact.type == "colony":
            # creates the colony build automation structure object
            build_automation_structure = ColonyBuildAutomationStructure()

            # in case there is no parent defined
            if not parent:
                # in case the artifact is not the base one
                if not artifact.id == BASE_AUTOMATION_ID:
                    build_automation_structure.parent = self.base_build_automation_structure

            # retrieves the artifact id
            artifact_id = artifact.id

            # retrieves the artifact version
            artifact_version = artifact.version

            # retrieves the plugin manager
            manager = self.build_automation_plugin.manager

            # retrieves the associated plugin
            associated_plugin = manager.get_plugin_by_id_and_version(artifact_id, artifact_version)

            # sets the associated plugin in the build automation structure
            build_automation_structure.associated_plugin = associated_plugin

            # retrieves the list of build plugins
            build_automation_plugins = build.plugins

            # iterates over all the build automation plugins
            for build_automation_plugin in build_automation_plugins:
                # retrieves the build automation plugin id
                build_automation_plugin_id = build_automation_plugin.id

                # retrieves the build automation version
                build_automation_plugin_version = build_automation_plugin.version

                # retrieves the build automation plugin instance
                build_automation_plugin_instance = self.get_build_automation_extension_plugin(build_automation_plugin_id, build_automation_plugin_version)
    
                # appends the build automation plugin instance to the automation plugins list
                build_automation_structure.automation_plugins.append(build_automation_plugin_instance)

        # returns the build automation structure object
        return build_automation_structure

    def get_build_automation_extension_plugin(self, plugin_id, plugin_version = None):
        for build_automation_extension_plugin in self.build_automation_plugin.build_automation_extension_plugins:
            if build_automation_extension_plugin.id == plugin_id and build_automation_extension_plugin.version == plugin_version:
                return build_automation_extension_plugin

    def get_all_automation_plugins(self, plugin_build_automation):
        pass

class BuildAutomationStructure:
    """
    The build automation structure class.
    """

    parent = None
    build_properties = {}
    dependecy_plugins = []
    automation_plugins = []
    automation_plugins_configurations = {}

    def __init__(self, parent = None):
        """
        Constructor of the class.
        
        @type parent: BuildAutomationStructure
        @param parent: The parent build automation structure.
        """

        self.parent = parent
        self.build_properties = {}
        self.dependecy_plugins = []
        self.automation_plugins = []
        self.automation_plugins_configurations = {}

    def get_all_automation_plugins(self):
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
