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
import types
import logging
import datetime

import colony.libs.map_util
import colony.libs.path_util
import colony.libs.time_util
import colony.libs.string_buffer_util

import build_automation_exceptions
import build_automation_parser

BASE_AUTOMATION_ID = "pt.hive.colony.plugins.build.automation.base"
""" The build automation id """

DEFAULT_LOGGER = "default_build_automation"
""" The default logger name """

DEFAULT_LOGGING_FORMAT = "[%(levelname)s] %(message)s"
""" The default logging format """

VARIABLE_REGEX = "\$\{[^\}]*\}"
""" The regular expression for the variable """

BASE_REGEX = "\$base\{(\$\{[^\}]*\}|[^\}])*\}"
""" The regular expression for the base """

CALL_REGEX = "\$call\{(\$\{[^\}]*\}|[^\}])*\}"
""" The regular expression for the call """

RESOURCE_REGEX = "\$resource\{(\$\{[^\}]*\}|[^\}])*\}"
""" The regular expression for the resource """

CONTENTS_REGEX = "\$contents\{(\$\{[^\}]*\}|[^\}])*\}"
""" The regular expression for the contents """

EXCLUSION_LIST = ("__doc__", "__init__", "__module__")
""" The exclusion list """

PLUGIN_SYSTEM_DIRECTORY_VALUE = "plugin_system_directory"
""" The plugin system directory value """

PLUGIN_DIRECTORY_VALUE = "plugin_directory"
""" The plugin directory value """

COLONY_ARTIFACT_VALUE = "colony"
""" The colony artifact value """

TOTAL_TIME_VALUE = "total_time"
""" The total time value """

TOTAL_TIME_FORMATED_VALUE = "total_time_formated"
""" The total time formated value """

DEFAULT_STAGE_VALUE = "default_stage"
""" The default stage value """

DEFAULT_LOG_LEVEL = logging.INFO
""" The default log level """

BUILD_AUTOMATION_STAGES = ["compile", "test", "build", "install", "deploy", "clean", "site", "site-deploy"]
""" The build automation stages """

POST_BUILD_AUTOMATION_STAGES = ["post-build"]
""" The post build automation stages """

class BuildAutomation:
    """
    The build automation class.
    """

    build_automation_plugin = None
    """ The build automation plugin """

    current_id = 0
    """ The current id used for the build automation """

    loaded_build_automation_item_plugins_list = []
    """ The list of loaded build automation item plugins """

    build_automation_item_plugin_id_map = {}
    """ The map with the loaded build automation item plugin associated with the build automation id """

    id_build_automation_item_plugin_map = {}
    """ The map with the build automation id associated with the loaded build automation item plugin """

    variable_pattern = None
    """ The variable pattern used for regular expression match """

    base_pattern = None
    """ The base pattern used for regular expression match """

    call_pattern = None
    """ The call pattern used for regular expression match """

    resource_pattern = None
    """ The resource pattern used for regular expression match """

    contents_pattern = None
    """ The contents pattern used for regular expression match """

    base_build_automation_structure = None
    """ The base build automation structure """

    logger = None
    """ The logger used in the build automation process """

    logger_handlers = []
    """ The logger handlers used in the build automation process """

    def __init__(self, build_automation_plugin):
        """
        Constructor of the class.

        @type build_automation_plugin: BuildAutomationPlugin
        @param build_automation_plugin: The build automation plugin.
        """

        self.build_automation_plugin = build_automation_plugin

        self.loaded_build_automation_item_plugins_list = []
        self.build_automation_item_plugin_id_map = {}
        self.id_build_automation_item_plugin_map = {}
        self.logger_handlers = []

        # compiles the variable regular expression generating the pattern
        self.variable_pattern = re.compile(VARIABLE_REGEX)

        # compiles the base regular expression generating the pattern
        self.base_pattern = re.compile(BASE_REGEX)

        # compiles the call regular expression generating the pattern
        self.call_pattern = re.compile(CALL_REGEX)

        # compiles the resource regular expression generating the pattern
        self.resource_pattern = re.compile(RESOURCE_REGEX)

        # compiles the contents regular expression generating the pattern
        self.contents_pattern = re.compile(CONTENTS_REGEX)

    def load_build_automation(self):
        # starts the logger
        self._start_logger()

    def unload_build_automation(self):
        # stops the logger
        self._stop_logger()

    def load_build_automation_item_plugin(self, build_automation_item_plugin):
        # adds the build automation item plugin to the list of build automation item plugins
        self.loaded_build_automation_item_plugins_list.append(build_automation_item_plugin)

        # associates the build automation item plugin with the build automation id
        self.build_automation_item_plugin_id_map[build_automation_item_plugin] = self.current_id

        # associates the build automation id with the build automation item plugin
        self.id_build_automation_item_plugin_map[self.current_id] = build_automation_item_plugin

        # increments the current id
        self.current_id += 1

    def unload_build_automation_item_plugin(self, build_automation_item_plugin):
        # retrieves the build automation id
        build_automation_id = self.build_automation_item_plugin_id_map[build_automation_item_plugin]

        if build_automation_item_plugin in self.loaded_build_automation_item_plugins_list:
            self.loaded_build_automation_item_plugins_list.remove(build_automation_item_plugin)

        if build_automation_item_plugin in self.build_automation_item_plugin_id_map:
            del self.build_automation_item_plugin_id_map[build_automation_item_plugin]

        if build_automation_id in self.id_build_automation_item_plugin_map:
            del self.id_build_automation_item_plugin_map[build_automation_id]

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

        # iterates over all the loaded build automation item plugins
        for build_automation_item_plugin in self.loaded_build_automation_item_plugins_list:
            if build_automation_item_plugin.id == build_automation_id and (build_automation_item_plugin.version == build_automation_version or not build_automation_version):
                # retrieves the build automation item plugin id
                build_automation_item_plugin_id = build_automation_item_plugin.id

                # tries to retrieve the build automation file
                build_automation_file_path = build_automation_item_plugin.get_attribute("build_automation_file_path")

                # in case the build automation file path attribute is not defined
                if not build_automation_file_path:
                    # retrieves the build automation file path
                    build_automation_file_path = build_automation_item_plugin.get_build_automation_file_path()

                # creates the plugin directory value as the base reference
                # to the plugin directory value
                plugin_directory_value = "$base{" + PLUGIN_DIRECTORY_VALUE + "}"

                # in case there is a reference to the plugin directory
                if build_automation_file_path.startswith(plugin_directory_value):
                    # retrieves the plugin path (plugin base path)
                    plugin_path = self.build_automation_plugin.manager.get_plugin_path_by_id(build_automation_item_plugin_id)

                    # updates the build automation file substituting the plugin directory reference
                    # with the plugin path directory
                    build_automation_file_path = build_automation_file_path.replace(plugin_directory_value, plugin_path)

                # prints a debug message
                self.build_automation_plugin.debug("Parsing build automation file (baf): '%s'" % build_automation_file_path)

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

    def get_all_automation_plugins(self):
        """
        Retrieves all the available automation extension plugins.

        @rtype: List
        @return: The list of all the available automation extension plugins.
        """

        # retrieves the build automation extension plugins
        build_automation_extension_plugins = self.build_automation_plugin.build_automation_extension_plugins

        # returns the build automation extension plugins
        return build_automation_extension_plugins

    def get_all_build_automation_item_plugins(self):
        """
        Retrieves all the available build automation item plugins.

        @rtype: List
        @return: The list of all the available build automation item plugins.
        """

        # returns the loaded build automation item plugins
        return self.loaded_build_automation_item_plugins_list

    def run_automation(self, plugin_id, plugin_version = None, stage = None, recursive_level = 1, logger = None, properties = None, raise_exception = False, is_first = True):
        """
        Runs all the automation plugins for the given plugin id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to run all the automation plugins.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to run the automation plugins.
        @type stage: String
        @param stage: The stage to be run in the automation.
        @type recursive_level: int
        @param recursive_level: The current level of recursion.
        @type logger: Logger
        @param logger: The build automation logger to be used.
        @type properties: Dictionary
        @param properties: Map containing the runtime automation information.
        @type raise_exception: bool
        @param raise_exception: If an exception should be raised in case of error.
        @type is_first: bool
        @param is_first: If this is the first run (useful for module inclusion).
        @rtype: bool
        @return: If the  build automation for the stage was successful.
        """

        # in case no logger is defined
        if not logger:
            # sets the current logger as the logger
            logger = self.logger

        # in case no properties are defined
        if not properties:
            # creates a new properties map
            properties = {}

        # retrieves the build automation structure
        build_automation_structure = self.get_build_automation_structure(plugin_id, plugin_version)

        # in case the retrieval of the build automation structure was unsuccessful
        if not build_automation_structure:
            # returns immediately
            return False

        # resets (clears) the logging buffer (in order to avoid duplicates)
        self.logging_buffer.reset()

        # retrieves the initial date time value
        initial_date_time = datetime.datetime.now()

        # creates the build automation structure runtime information, with the current properties
        # the properties are shared among the build automation global run that includes the modules
        build_automation_structure.runtime = RuntimeInformationStructure(True, self.logging_buffer, initial_date_time, False, properties)

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # in case the stage is not defined, it's is going
        # to find the default one
        if not stage:
            # retrieves the build properties
            build_properties = build_automation_structure.get_all_build_properties()

            # retrieves the default stage as the stage to be used
            stage = build_properties[DEFAULT_STAGE_VALUE]

        # in case the stage is not present in the build automation stages
        if not stage in BUILD_AUTOMATION_STAGES:
            # raises the invalid stage exception
            raise build_automation_exceptions.InvalidStageException(stage)

        # prints the start information
        self.print_start_information(plugin_id, plugin_version, stage, logger)

        # creates the build automation directories (if they don't exist and is first run)
        is_first and self.create_build_automation_directories(build_automation_structure)

        # in case the recursive level is greater than zero
        if recursive_level > 0:
            # prints an info message
            logger.info("Building modules...")

            # iterates over all the module plugins to execute them (composition)
            for module_plugin, module_plugin_stage in build_automation_structure.module_plugins:
                # in case the build automation does not succeed
                if not build_automation_structure_runtime.success:
                    # breaks the loop
                    break

                # retrieves the module values
                module_id = module_plugin.id
                module_version = module_plugin.version
                module_stage = module_plugin_stage or stage

                # runs the module plugin for the same stage
                build_automation_structure_runtime.success = self.run_automation(module_id, module_version, module_stage, recursive_level - 1, logger, properties, raise_exception, False)
        else:
            # prints an info message
            logger.info("Not building modules no recursion level available...")

        # retrieves the index of the state in the build automation stages list
        build_automation_stage_index = BUILD_AUTOMATION_STAGES.index(stage)

        # retrieves the valid automation stages for the current stage (all the
        # stages that have a priority inferior or equal to the one selected)
        valid_automation_stages = BUILD_AUTOMATION_STAGES[:build_automation_stage_index + 1]

        # iterates over all the valid automation stages to run the automation plugins
        for valid_automation_stage in valid_automation_stages:
            # in case the build automation does not succeed
            if not build_automation_structure_runtime.success:
                # breaks the loop
                break

            # run the automation stage (tasks)
            build_automation_structure_runtime.success = self.run_automation_stage(valid_automation_stage, stage, build_automation_structure, logger)

        # prints the end information
        self.print_end_information(build_automation_structure, logger)

        # in case it's the first run and the build automation is not skipped, runs the post build tasks
        is_first and not build_automation_structure_runtime.skipped and self.run_post_build(build_automation_structure, stage, logger, raise_exception)

        # returns the build automation success
        return build_automation_structure_runtime.success

    def run_automation_stage(self, automation_stage, base_stage, build_automation_structure, logger):
        """
        Runs the automation tasks for the given automation stage, using
        the given build automation structure and the given logger.

        @type automation_stage: String
        @param automation_stage: The automation stage to be run.
        @type base_stage: String
        @param base_stage: The base stage (upper stage) to be run.
        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The build automation structure used.
        @type logger: Logger
        @param logger: The logger to be used.
        @rtype: bool
        @return: If the automation for the stage was successful.
        """

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the automation plugins for the stage
        all_automation_plugins = build_automation_structure.get_all_automation_plugins_by_stage(automation_stage, base_stage)

        # iterates over all of the automation plugins
        for automation_plugin in all_automation_plugins:
            # in case the build automation is skipped
            if build_automation_structure_runtime.skipped:
                # breaks the loop
                break

            # retrieves the automation plugin id
            automation_plugin_id = automation_plugin.id

            # retrieves the automation plugin version
            automation_plugin_version = automation_plugin.version

            # creates the automation plugin tuple
            automation_plugin_tuple = (automation_plugin_id, automation_plugin_version)

            # retrieves the automation plugin configurations
            automation_plugin_configurations = build_automation_structure.get_all_automation_plugin_configurations(automation_plugin_tuple)

            # prints logging information
            logger.info("------------------------------------------------------------------------")
            logger.info("Running build automation plugin '%s' v%s" % (automation_plugin_id, automation_plugin_version))
            logger.info("For stage [%s] of build automation" % automation_stage)
            logger.info("------------------------------------------------------------------------")

            try:
                # runs the automation for the current stage
                return_value = automation_plugin.run_automation(build_automation_structure.associated_plugin, automation_stage, automation_plugin_configurations, build_automation_structure, logger)

                # in case the return value is invalid
                if not return_value:
                    # prints an error message
                    logger.error("Error while executing build automation plugin '%s' v%s" % (automation_plugin_id, automation_plugin_version))

                    # returns false (invalid)
                    return False
            except Exception, exception:
                # prints an error message
                logger.error("Problem while executing build automation '%s'" % unicode(exception))

                # returns false (invalid)
                return False

        # returns true (valid)
        return True

    def run_post_build(self, build_automation_structure, base_stage, logger, raise_exception):
        """
        Runs the post build tasks associated with the given build automation
        structure.

        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The build automation structure used.
        @type base_stage: String
        @param base_stage: The base (original) stage for dependency checking.
        @type logger: Logger
        @param logger: The logger to be used.
        @type raise_exception: bool
        @param raise_exception: If an exception should be raised upon build failure.
        """

        # prints an info message
        logger.info("Running post build tasks...")

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # iterates over all the valid post automation stages to run the automation plugins
        for post_build_automation_stage in POST_BUILD_AUTOMATION_STAGES:
            # run the post automation stage (tasks)
            self.run_automation_stage(post_build_automation_stage, base_stage, build_automation_structure, logger)

        # in case the build automation failed, this is the first run and the raise
        # exception flag is active an exception should be raised
        if not build_automation_structure_runtime.success and raise_exception:
            # raises the build automation failed exception
            raise build_automation_exceptions.BuildAutomationFailedException("no success")

        # prints an info message
        logger.info("Finished post build tasks...")

    def print_start_information(self, plugin_id, plugin_version, stage, logger):
        """
        Prints the start information for the given information.

        @type plugin_id: String
        @param plugin_id: The current plugin id.
        @type plugin_version: String
        @param plugin_version: The current plugin version.
        @type stage: String
        @param stage: The current stage.
        @type logger: Logger
        @param logger: The current logger.
        """

        # prints the initial logging information
        logger.info("------------------------------------------------------------------------")
        logger.info("BUILD STARTED")
        logger.info("------------------------------------------------------------------------")
        logger.info("Building '%s'" %(plugin_id))
        logger.info("Using stage [%s] of build automation" % stage)
        logger.info("------------------------------------------------------------------------")

    def print_end_information(self, build_automation_structure, logger):
        """
        Prints the end information for the given information.

        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The current build automation structure.
        @type logger: Logger
        @param logger: The current logger.
        """

        # retrieves the built automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the build automation success
        build_automation_success = build_automation_structure_runtime.success

        # retrieves the intial date time
        initial_date_time = build_automation_structure_runtime.initial_date_time

        # retrieves the final date time value
        final_date_time = datetime.datetime.now()

        # calculates the delta date time from the final and the initial values
        delta_date_time = final_date_time - initial_date_time

        # retrieves the delta date time in seconds
        delta_date_time_seconds = delta_date_time.seconds

        # formats the date time into the required format
        delta_date_time_formated = colony.libs.time_util.format_seconds_smart(delta_date_time_seconds, "extended")

        # prints the final build automation result
        logger.info("------------------------------------------------------------------------")

        # in case the build automation succeeded
        if build_automation_success:
            # prints the success info
            logger.info("BUILD SUCCEEDED")
        # otherwise
        else:
            # prints the failure info
            logger.info("BUILD FAILED")

        # prints the final logging information
        logger.info("------------------------------------------------------------------------")
        logger.info("Total time for build automation %s" % delta_date_time_formated)
        logger.info("Finished build automation at %s" % final_date_time.strftime("%d/%m/%y %H:%M:%S"))
        logger.info("------------------------------------------------------------------------")

        # sets the build automation structure runtime properties
        build_automation_structure_runtime.properties[TOTAL_TIME_VALUE] = delta_date_time_seconds
        build_automation_structure_runtime.properties[TOTAL_TIME_FORMATED_VALUE] = delta_date_time_formated

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
        if artifact.type == COLONY_ARTIFACT_VALUE:
            # creates the colony build automation structure object
            build_automation_structure = ColonyBuildAutomationStructure()

        # sets the build automation parsing structure
        build_automation_structure.build_automation_parsing_structure = build_automation_parsing_structure

        # generates the build automation parent structure
        self.generate_build_automation_parent_structure(build_automation_parsing_structure, build_automation_structure)

        # generates the build automation artifact structure
        self.generate_build_automation_artifact_structure(build_automation_parsing_structure, build_automation_structure)

        # generates the build automation modules structure
        self.generate_build_automation_modules_structure(build_automation_parsing_structure, build_automation_structure)

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

    def generate_build_automation_modules_structure(self, build_automation_parsing_structure, build_automation_structure):
        # retrieves the modules parsing value
        modules = build_automation_parsing_structure.modules

        # iterates over all the module items
        for module in modules:
            # creates the plugin id regex
            plugin_id_regex = re.compile(module.id)

            # creates the plugin version regex
            plugin_version_regex = re.compile(module.version)

            # retrieves the plugin stage
            plugin_stage = module.stage

            # retrieves the build automation module plugins (the ones that match the regex)
            build_automation_module_plugins = self.get_build_automation_item_plugins_regex(plugin_id_regex, plugin_version_regex)

            # in case the associated plugin is in the build automation module plugins, it must be removed
            if build_automation_structure.associated_plugin in build_automation_module_plugins:
                # removes the associated plugin from the build automation module plugins
                build_automation_module_plugins.remove(build_automation_structure.associated_plugin)

            # creates the build automation module plugin tuples from the original build automation
            # module plugins and the plugin stage
            build_automation_module_plugin_tuples = [(value, plugin_stage) for value in build_automation_module_plugins]

            # extends the module plugins list with the new ones (tuples)
            build_automation_structure.module_plugins.extend(build_automation_module_plugin_tuples)

    def generate_build_automation_build_structure(self, build_automation_parsing_structure, build_automation_structure):
        # retrieves the build parsing value
        build = build_automation_parsing_structure.build

        if build.default_stage:
            # retrieves the build default stage
            build_automation_default_stage = self.parse_string(build.default_stage, build_automation_structure)
            build_automation_structure.build_properties["default_stage"] = build_automation_default_stage

        if build.execution_directory:
            # retrieves the build execution directory
            build_automation_execution_directory = self.parse_string(build.execution_directory, build_automation_structure)
            build_automation_structure.build_properties["execution_directory"] = build_automation_execution_directory

        if build.target_directory:
            # retrieves the build target directory
            build_automation_target_directory = self.parse_string(build.target_directory, build_automation_structure)
            build_automation_structure.build_properties["target_directory"] = build_automation_target_directory

        if build.classes_directory:
            # retrieves the build classes directory
            build_automation_classes_directory = self.parse_string(build.classes_directory, build_automation_structure)
            build_automation_structure.build_properties["classes_directory"] = build_automation_classes_directory

        if build.bundles_directory:
            # retrieves the build bundles directory
            build_automation_bundles_directory = self.parse_string(build.bundles_directory, build_automation_structure)
            build_automation_structure.build_properties["bundles_directory"] = build_automation_bundles_directory

        if build.plugins_directory:
            # retrieves the build plugins directory
            build_automation_plugins_directory = self.parse_string(build.plugins_directory, build_automation_structure)
            build_automation_structure.build_properties["plugins_directory"] = build_automation_plugins_directory

        if build.libraries_directory:
            # retrieves the build libraries directory
            build_automation_libraries_directory = self.parse_string(build.libraries_directory, build_automation_structure)
            build_automation_structure.build_properties["libraries_directory"] = build_automation_libraries_directory

        if build.documentation_directory:
            # retrieves the build documentation directory
            build_automation_documentation_directory = self.parse_string(build.documentation_directory, build_automation_structure)
            build_automation_structure.build_properties["documentation_directory"] = build_automation_documentation_directory

        if build.repository_directory:
            # retrieves the build repository directory
            build_automation_repository_directory = self.parse_string(build.repository_directory, build_automation_structure)
            build_automation_structure.build_properties["repository_directory"] = build_automation_repository_directory

        if build.resources_directory:
            # retrieves the build resources directory
            build_automation_resources_directory = self.parse_string(build.resources_directory, build_automation_structure)
            build_automation_structure.build_properties["resources_directory"] = build_automation_resources_directory

        if build.log_directory:
            # retrieves the build log directory
            build_automation_log_directory = self.parse_string(build.log_directory, build_automation_structure)
            build_automation_structure.build_properties["log_directory"] = build_automation_log_directory

        if build.source_directory:
            # retrieves the build source directory
            build_automation_source_directory = self.parse_string(build.source_directory, build_automation_structure)
            build_automation_structure.build_properties["source_directory"] = build_automation_source_directory

        if build.final_name:
            # retrieves the build final name
            build_automation_final_name = self.parse_string(build.final_name, build_automation_structure)
            build_automation_structure.build_properties["final_name"] = build_automation_final_name

        if build.clean_target_directory:
            # retrieves the build clean target directory
            build_automation_clean_target_directory = self.parse_string(build.clean_target_directory, build_automation_structure)
            build_automation_structure.build_properties["clean_target_directory"] = build_automation_clean_target_directory

        # retrieves the list of build automation dependencies
        build_automation_dependencies = build.dependencies

        # iterates over all the build automation dependencies
        for build_automation_dependency in build_automation_dependencies:
            # retrieves the build automation dependency id
            build_automation_dependency_id = build_automation_dependency.id

            # retrieves the build automation dependency version
            build_automation_dependency_version = build_automation_dependency.version

            # prints a debug message
            self.build_automation_plugin.debug("Processing dependency '%s' v%s" % (build_automation_dependency_id, build_automation_dependency_version))

        # retrieves the list of build automation plugins
        build_automation_plugins = build.plugins

        # iterates over all the build automation plugins, to update
        # the build automation structure with the plugin values
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

            # retrieves the build automation stage
            build_automation_plugin_stage = build_automation_plugin.stage

            # sets the build automation plugin stage in the automation plugins stages map
            build_automation_structure.automation_plugins_stages[build_automation_plugin_tuple] = build_automation_structure

            # in case the build automation plugin stages does not exists in the stages automation plugins
            if not build_automation_plugin_stage in build_automation_structure.stages_automation_plugins:
                # creates the list for the plugin tuples of the current stage
                build_automation_structure.stages_automation_plugins[build_automation_plugin_stage] = []

            # retrieves the build automation plugin stage list for the current stage
            build_automation_plugin_stage_list = build_automation_structure.stages_automation_plugins[build_automation_plugin_stage]

            # adds the build automation plugin instance to the build automation plugin stage list
            build_automation_plugin_stage_list.append(build_automation_plugin_instance)

            # retrieves the build automation stage dependency
            build_automation_plugin_stage_dependency = build_automation_plugin.stage_dependency

            # sets the build automation plugin stage dependency in the automation plugins stage dependencies map
            build_automation_structure.automation_plugins_stage_dependencies[build_automation_plugin_instance] = build_automation_plugin_stage_dependency

            # retrieves the build automation plugin configuration
            build_automation_plugin_configuration = build_automation_plugin.configuration

            # initializes the map containing the automation plugins configurations for the current build automation plugin
            build_automation_structure.automation_plugins_configurations[build_automation_plugin_tuple] = {}

            # retrieves the map containing the automation plugins configurations for the current build automation plugin
            build_automation_plugin_automation_plugins_configurations = build_automation_structure.automation_plugins_configurations[build_automation_plugin_tuple]

            # retrieves all the build automation plugin configuration item names
            build_automation_plugin_configuration_item_names = dir(build_automation_plugin_configuration)

            # filters all the build automation plugin configuration item names
            build_automation_plugin_configuration_filtered_item_names = [value for value in build_automation_plugin_configuration_item_names if value not in EXCLUSION_LIST]

            # sets the configuration values for the build automation plugin using the build automation structure
            self.set_configuration_values(build_automation_plugin_automation_plugins_configurations, build_automation_plugin_configuration_filtered_item_names, build_automation_plugin_configuration, build_automation_structure)

    def set_configuration_values(self, base_map, configuration_names, configuration_structure, build_automation_structure):
        # iterates over all the configuration names
        for configuration_name in configuration_names:
            # retrieves the configuration item from the configuration structure
            configuration_item = getattr(configuration_structure, configuration_name)

            # retrieves the configuration item type
            configuration_item_type = type(configuration_item)

            if configuration_item_type in types.StringTypes:
                # parses the string value
                parsed_configuration_item = self.parse_string(configuration_item, build_automation_structure)

                # adds the parsed configuration item value to the base map for the current configuration name
                self._set_base_map(base_map, configuration_name, parsed_configuration_item)
            elif configuration_item_type == types.ListType:
                # iterates over the configuration item (retrieving the various configuration items)
                for configuration_single_item in configuration_item:
                    # in case the current configuration single item is a generic element
                    # the configuration item is treated as a composite one
                    if type(configuration_single_item) == types.InstanceType and configuration_single_item.__class__ == build_automation_parser.GenericElement:
                        # sets the configuration composite value
                        self._set_configuration_composite_value(base_map, configuration_name, configuration_single_item, build_automation_structure)
                    else:
                        # parses the string value
                        parsed_configuration_single_item = self.parse_string(configuration_single_item, build_automation_structure)

                        # adds the configuration single item value to the base map for the current configuration name
                        self._set_base_map(base_map, configuration_name, parsed_configuration_single_item)
            elif configuration_item_type == types.InstanceType and configuration_item.__class__ == build_automation_parser.GenericElement:
                # sets the configuration composite value
                self._set_configuration_composite_value(base_map, configuration_name, configuration_item, build_automation_structure)

    def generate_build_automation_profiles_structure(self, build_automation_parsing_structure, build_automation_structure):
        # retrieves the profiles parsing value
        profiles = build_automation_parsing_structure.profiles

    def create_build_automation_directories(self, build_automation_structure):
        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the execution directory path value
        execution_directory_path = build_properties["execution_directory"]

        # retrieves the target directory path value
        target_directory_path = build_properties["target_directory"]

        # retrieves the classes directory path value
        classes_directory_path = build_properties["classes_directory"]

        # retrieves the bundles directory path value
        bundles_directory_path = build_properties["bundles_directory"]

        # retrieves the plugins directory path value
        plugins_directory_path = build_properties["plugins_directory"]

        # retrieves the libraries directory path value
        libraries_directory_path = build_properties["libraries_directory"]

        # retrieves the documentation directory path value
        documentation_directory_path = build_properties["documentation_directory"]

        # retrieves the repository directory path value
        repository_directory_path = build_properties["repository_directory"]

        # retrieves the resources directory path value
        resources_directory_path = build_properties["resources_directory"]

        # retrieves the log directory path value
        log_directory_path = build_properties["log_directory"]

        # retrieves the clean target directory value
        clean_target_directory = build_properties["clean_target_directory"] == "true"

        # creates the complete target directory path
        complete_target_directory_path = execution_directory_path + "/" + target_directory_path

        # creates the complete classes directory path
        complete_classes_directory_path = execution_directory_path + "/" + classes_directory_path

        # creates the complete bundles directory path
        complete_bundles_directory_path = execution_directory_path + "/" + bundles_directory_path

        # creates the complete plugins directory path
        complete_plugins_directory_path = execution_directory_path + "/" + plugins_directory_path

        # creates the complete libraries directory path
        complete_libraries_directory_path = execution_directory_path + "/" + libraries_directory_path

        # creates the complete documentation directory path
        complete_documentation_directory_path = execution_directory_path + "/" + documentation_directory_path

        # creates the complete repository directory path
        complete_repository_directory_path = execution_directory_path + "/" + repository_directory_path

        # creates the complete resources directory path
        complete_resources_directory_path = execution_directory_path + "/" + resources_directory_path

        # creates the complete log directory path
        complete_log_directory_path = execution_directory_path + "/" + log_directory_path

        # removes (cleans) the target directory (in case it exists)
        clean_target_directory and os.path.isdir(complete_target_directory_path) and colony.libs.path_util.remove_directory(complete_target_directory_path)

        # in case the execution directory does not exist
        if not os.path.isdir(execution_directory_path):
            # creates the execution directory
            os.mkdir(execution_directory_path)

        # in case the target directory does not exist
        if not os.path.isdir(complete_target_directory_path):
            # creates the target directory
            os.mkdir(complete_target_directory_path)

        # in case the classes directory does not exist
        if not os.path.isdir(complete_classes_directory_path):
            # creates the classes directory
            os.mkdir(complete_classes_directory_path)

        # in case the bundles directory does not exist
        if not os.path.isdir(complete_bundles_directory_path):
            # creates the bundles directory
            os.mkdir(complete_bundles_directory_path)

        # in case the plugins directory does not exist
        if not os.path.isdir(complete_plugins_directory_path):
            # creates the plugins directory
            os.mkdir(complete_plugins_directory_path)

        # in case the libraries directory does not exist
        if not os.path.isdir(complete_libraries_directory_path):
            # creates the libraries directory
            os.mkdir(complete_libraries_directory_path)

        # in case the documentation directory does not exist
        if not os.path.isdir(complete_documentation_directory_path):
            # creates the documentation directory
            os.mkdir(complete_documentation_directory_path)

        # in case the repository directory does not exist
        if not os.path.isdir(complete_repository_directory_path):
            # creates the repository directory
            os.mkdir(complete_repository_directory_path)

        # in case the resources directory does not exist
        if not os.path.isdir(complete_resources_directory_path):
            # creates the resources directory
            os.mkdir(complete_resources_directory_path)

        # in case the log directory does not exist
        if not os.path.isdir(complete_log_directory_path):
            # creates the log directory
            os.mkdir(complete_log_directory_path)

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

    def get_build_automation_item_plugins_regex(self, plugin_id_regex, plugin_version_regex = None):
        """
        Retrieves the list of build automation item plugins that match both the
        given id and version regex.

        @type plugin_id_regex: RegexObject
        @param plugin_id_regex: The plugin id regex.
        @type plugin_version_regex: RegexObject
        @param plugin_version_regex: The plugin version regex.
        @rtype: List
        @return: The list of build automation item plugins that match both the
        given id and version regex.
        """

        # allocates the build automation item plugins list
        build_automation_item_plugins_list = []

        # iterates over all the loaded build automation item plugins
        for loaded_build_automation_item_plugin in self.loaded_build_automation_item_plugins_list:
            # in case the plugin version regex is defined
            if plugin_version_regex:
                # in case both the id and the version match the regex
                if plugin_id_regex.match(loaded_build_automation_item_plugin.id) and plugin_version_regex.match(loaded_build_automation_item_plugin.version):
                    # adds the loaded build automation item plugin to the build autmation item plugins list
                    build_automation_item_plugins_list.append(loaded_build_automation_item_plugin)
            else:
                # in case the id matches the regex
                if plugin_id_regex.match(loaded_build_automation_item_plugin.id):
                    # adds the loaded build automation item plugin to the build autmation item plugins list
                    build_automation_item_plugins_list.append(loaded_build_automation_item_plugin)

        # returns the build automation item plugins list
        return build_automation_item_plugins_list

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

        # retrieves the variable match iterator
        variable_match_iterator = self.variable_pattern.finditer(string)

        # iterates using the variable match iterator
        for variable_match in variable_match_iterator:
            # retrieves the match group
            group = variable_match.group()

            # retrieves the variable value
            variable_value = group[2:-1]

            # retrieves the variable list value
            variable_list_value = variable_value.split(".")

            # retrieves the variable list value without build_automation
            variable_list_value_replaced = variable_list_value[1:]

            # retrieves the real variable value
            real_variable_value = self.get_variable_value(variable_value, variable_list_value_replaced, build_automation_structure)

            # parses the real variable value
            real_variable_value_parsed = self.parse_string(real_variable_value, build_automation_structure)

            # replaces the value in the string
            string = string.replace(group, real_variable_value_parsed)

        # retrieves the base match iterator
        base_match_iterator = self.base_pattern.finditer(string)

        # iterates using the base match iterator
        for base_match in base_match_iterator:
            # retrieves the match group
            group = base_match.group()

            # retrieves the base value
            base_value = group[6:-1]

            # retrieves the real base value
            real_base_value = self.get_base_value(base_value, build_automation_structure)

            # replaces the value in the string
            string = string.replace(group, real_base_value)

        # retrieves the call match iterator
        call_match_iterator = self.call_pattern.finditer(string)

        # iterates using the call match iterator
        for call_match in call_match_iterator:
            # retrieves the match group
            group = call_match.group()

            # retrieves the call value
            call_value = group[6:-1]

            # retrieves the real call value
            real_call_value = self.get_call_value(call_value, build_automation_structure)

            # replaces the value in the string
            string = string.replace(group, real_call_value)

        # retrieves the resource match iterator
        resource_match_iterator = self.resource_pattern.finditer(string)

        # iterates using the resource match iterator
        for resource_match in resource_match_iterator:
            # retrieves the match group
            group = resource_match.group()

            # retrieves the resource value
            resource_value = group[10:-1]

            # retrieves the real resource value
            real_resource_value = self.get_resource_value(resource_value, build_automation_structure)

            # replaces the value in the string
            string = string.replace(group, real_resource_value)

        # retrieves the contents match iterator
        contents_match_iterator = self.contents_pattern.finditer(string)

        # iterates using the contents match iterator
        for contents_match in contents_match_iterator:
            # retrieves the match group
            group = contents_match.group()

            # retrieves the contents value
            contents_value = group[10:-1]

            # retrieves the real contents value
            real_contents_value = self.get_contents_value(contents_value, build_automation_structure)

            # replaces the value in the string
            string = string.replace(group, real_contents_value)

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

    def get_base_value(self, base_value, build_automation_structure):
        """
        Retrieves the real "base" resource value by executing the associated logic
        to retrieve the value.

        @type call_value: String
        @param call_value: The base value in string mode representing the base resource.
        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The build automation structure to be used in the retrieving of the value.
        @rtype: Object
        @return: The real value of the base resource value.
        """

        # retrieves the plugin manager
        plugin_manager = self.build_automation_plugin.manager

        # in case the base value is plugin system directory value
        if base_value == PLUGIN_SYSTEM_DIRECTORY_VALUE:
            # sets the value as the plugin manager path (directory)
            value = plugin_manager.get_manager_path()
        # in case the base value is plugin directory value
        elif base_value == PLUGIN_DIRECTORY_VALUE:
            # sets the value as the plugin path (directory)
            value = build_automation_structure.get_plugin_path()

        # returns the value
        return value

    def get_call_value(self, call_value, build_automation_structure):
        """
        Retrieves the real "call" value by calling the associated method
        with the provided arguments.

        @type call_value: String
        @param call_value: The call value in string mode representing the method.
        to be called and the arguments to be sent.
        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The build automation structure to be used in the retrieving of the value.
        @rtype: Object
        @return: The real value of the call value.
        """

        # splits the call value
        call_values = call_value.split(",")

        # strips all the call values
        call_values_striped = [value.strip() for value in call_values]

        # retrieves the method name
        method_name = call_values_striped[0]

        # retrieves the method arguments
        method_arguments = call_values_striped[1:]

        # parses the method name
        method_name_parsed = self.parse_string(method_name, build_automation_structure)

        # creates the list containing the parsed method arguments
        method_arguments_parsed = []

        # iterates over the method arguments
        for method_argument in method_arguments:
            # parses the method argument
            method_argument_parsed = self.parse_string(method_argument, build_automation_structure)

            # adds the parsed method argument to the list of parsed method arguments
            method_arguments_parsed.append(method_argument_parsed)

        # retrieves the instance method
        method = getattr(build_automation_structure.associated_plugin, method_name_parsed)

        # calls the method
        value = method(*method_arguments_parsed)

        # returns the value
        return value

    def get_resource_value(self, resource_value, build_automation_structure):
        """
        Retrieves the real "resource" value by retrieving the resource value
        from the resources manager plugin.

        @type resource_value: String
        @param resource_value: The resource value in string mode representing the resource.
        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The build automation structure to be used in the retrieving of the resource.
        @rtype: Object
        @return: The real value of the resource.
        """

        # retrieves the resource manager plugin
        resource_manager_plugin = self.build_automation_plugin.resource_manager_plugin

        # retrieves the resource for the given resource value
        resource = resource_manager_plugin.get_resource(resource_value)

        # in case the resource is valid
        if resource:
            # retrieves the resource data
            resource_data = resource.data

            # returns the resource data
            return resource_data
        else:
            # returns invalid
            return None

    def get_contents_value(self, contents_value, build_automation_structure):
        """
        Retrieves the real "contents" value by retrieving the contents value
        from the contents file.

        @type contents_value: String
        @param contents_value: The contents value in string mode representing the contents.
        @type build_automation_structure: BuildAutomationStructure
        @param build_automation_structure: The build automation structure to be used in the retrieving of the contents.
        @rtype: Object
        @return: The real value of the contents.
        """

        # opens the file for reading (in binary mode)
        file = open(contents_value, "rb")

        try:
            # reads the file contents
            contents = file.read()
        finally:
            # closes the file
            file.close()

        # returns the contents
        return contents

    def _start_logger(self, log_level = DEFAULT_LOG_LEVEL):
        """
        Starts the logger initializing its internal structure.

        @type log_level: int
        @param log_level: The level to be used by the logger.
        """

        # retrieves the logger
        self.logger = logging.getLogger(DEFAULT_LOGGER)

        # sets the logger propagation to avoid propagation
        self.logger.propagate = 0

        # sets the logger level to the initial log level
        self.logger.setLevel(log_level)


        # creates the stream handler
        stream_handler = logging.StreamHandler()

        # creates the logging formatter
        formatter = logging.Formatter(DEFAULT_LOGGING_FORMAT)

        # sets the formatter in the stream handler
        stream_handler.setFormatter(formatter)

        # adds the stream handler to the logger
        self.logger.addHandler(stream_handler)

        # adds the stream handler to the logger handlers
        self.logger_handlers.append(stream_handler)

        # creates the string buffer that will hold the stream handler
        self.logging_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # creates the stream handler
        stream_handler = logging.StreamHandler(self.logging_buffer)

        # creates the logging formatter
        formatter = logging.Formatter(DEFAULT_LOGGING_FORMAT)

        # sets the formatter in the stream handler
        stream_handler.setFormatter(formatter)

        # adds the stream handler to the logger
        self.logger.addHandler(stream_handler)

        # adds the stream handler to the logger handlers
        self.logger_handlers.append(stream_handler)

    def _stop_logger(self):
        """
        Stops the logger returning it to the initial state.
        """

        # retrieves the logger
        self.logger = logging.getLogger(DEFAULT_LOGGER)

        # iterates over all the logger handlers
        for logger_handler in self.logger_handlers:
            # removes the logger handler from the logger
            self.logger.removeHandler(logger_handler)

    def _set_configuration_composite_value(self, base_map, configuration_name, configuration_item, build_automation_structure):
        # creates a new map
        new_map = {}

        # retrieves the new configuration names
        new_configuration_names = [value for value in dir(configuration_item) if not value in EXCLUSION_LIST]

        # adds the new map to the base map for the current configuration name
        self._set_base_map(base_map, configuration_name, new_map)

        # sets the configuration values for the new map, the new configuration names the configuration item
        # and the build automation structure
        self.set_configuration_values(new_map, new_configuration_names, configuration_item, build_automation_structure)

    def _set_base_map(self, base_map, key, value):
        """
        Sets the given value in the given base map for
        the given key.
        In case the value already exists in the base map
        a new list is created and the value appended to it.

        @type base_map: Dictionary
        @param base_map: The base map to hold the value.
        @type key: String
        @param key: The key to refer to the value in the map
        @type value: Object
        @param value: The value to be set in the map.
        """

        # in case the key already exists in the base map
        # the duplicated value must be converted to a list
        if key in base_map:
            # retrieves the base value from the base map
            base_value = base_map[key]

            # in case the base value is not a list yet
            if not type(base_value) == types.ListType:
                # sets the (new) list in the base map
                base_map[key] = [base_value]

            # adds the value to the base map list
            base_map[key].append(value)
        else:
            # sets the (simple) value in the base map
            base_map[key] = value

class BuildAutomationStructure:
    """
    The build automation structure class.
    """

    parent = None
    """ The parent build automation structure """

    build_properties = {}
    """ The build properties of the current structure """

    module_plugins = []
    """ The module plugins """

    dependecy_plugins = []
    """ The dependency plugins list """

    automation_plugins = []
    """ The automation plugins to be used as a list """

    automation_plugins_stages = {}
    """ The map associating the plugin tuple with the stage """

    automation_plugins_stage_dependencies = {}
    """ The map associating the plugin tuple (or instance) with the stage dependency """

    automation_plugins_configurations = {}
    """ The map associating the plugin tuple with the configuration """

    stages_automation_plugins = {}
    """ The map associating the stages with a list of various plugin tuples """

    build_automation_parsing_structure = None
    """ The associated build automation parsing structure """

    def __init__(self, parent = None, build_automation_parsing_structure = None):
        """
        Constructor of the class.

        @type parent: BuildAutomationStructure
        @param parent: The parent build automation structure.
        @type build_automation_parsing_structure: BuildAutomation
        @param build_automation_parsing_structure: The build automation parsing structure to generate the build automation structure.
        """

        self.parent = parent
        self.build_automation_parsing_structure = build_automation_parsing_structure

        self.build_properties = {}
        self.module_plugins = []
        self.dependecy_plugins = []
        self.automation_plugins = []
        self.automation_plugins_stages = {}
        self.automation_plugins_stage_dependencies = {}
        self.automation_plugins_configurations = {}
        self.stages_automation_plugins = {}

    def get_all_build_properties(self):
        """
        Retrieves all the build properties, recursively processing
        the properties of the parents.

        @rtype: Dictionary
        @return: A map containing all the properties of the current build
        automation structure and the parents.
        """

        # creates a copy of the build properties map
        build_properties = copy.copy(self.build_properties)

        # in case it contains a parent
        if self.parent:
            # retrieves all of the build properties from the parent
            build_properties_parent = self.parent.get_all_build_properties()

            # copies the contains of the build properties from the parent to the build properties
            colony.libs.map_util.map_copy(build_properties_parent, build_properties)

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

            # prepends all of the automation plugins from the parent to itself
            automation_plugins = automation_plugins_parent + automation_plugins

        # returns the automation plugins
        return automation_plugins

    def get_all_automation_plugins_by_stage(self, stage, base_stage):
        """
        Retrieves all the automation plugins for the given stage,
        using a recursive approach.

        @type stage: String
        @param stage: The stage to retrieve the plugins.
        @type base_stage: String
        @param base_stage: The base (original) stage for dependency checking.
        @rtype: List
        @return: A list containing all the automation plugins fot the given stage.
        """

        # creates the list to hold the automation plugins
        automation_plugins = []

        # retrieves the automation plugins for the stage
        automation_plugins_stage = self.stages_automation_plugins.get(stage, [])

        # iterates over all the automation plugins of the stage
        # to validate them agains the dependencies if existent
        for automation_plugin_stage in automation_plugins_stage:
            # retrieves the automation plugin stage dependency
            automation_plugin_stage_dependency = self.automation_plugins_stage_dependencies[automation_plugin_stage]

            # compares the base stage with the automation plugin stage dependency to
            # check if the dependency is met
            if self._compare_stages(automation_plugin_stage_dependency, base_stage) <= 0:
                # adds the automation plugin to the list of automation plugins
                automation_plugins.append(automation_plugin_stage)

        # in case it contains a parent
        if self.parent:
            # retrieves all of the automation plugins for the stage from the parent
            automation_plugins_stage_parent = self.parent.get_all_automation_plugins_by_stage(stage, base_stage)

            # prepends all of the automation plugins from the parent to itself
            automation_plugins = automation_plugins_stage_parent + automation_plugins

        # returns the automation plugins
        return automation_plugins

    def get_all_automation_plugin_configurations(self, automation_plugin_tuple):
        """
        Retrieves all the automation plugin configurations using a recursive approach.

        @type automation_plugin_tuple: Tuple
        @param automation_plugin_tuple: The automation plugin tuple containing both the id
        and version of the automation plugin.
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
            colony.libs.map_util.map_copy(automation_plugins_configurations_parent, automation_plugins_configurations)

        # returns the automation plugins configurations
        return automation_plugins_configurations

    def _compare_stages(self, first_stage, second_stage):
        # retrieves the first index for the first stage
        first_index = self._get_list_index(BUILD_AUTOMATION_STAGES, first_stage)

        # retrieves the second index for the second stage
        second_index = self._get_list_index(BUILD_AUTOMATION_STAGES, second_stage)

        # returns the result of comparing both indexes
        return cmp(first_index, second_index)

    def _get_list_index(self, list, value):
        # in case the value exists in the list
        if value in list:
            # returns the list index
            return list.index(value)
        # otherwise
        else:
            # returns invalid index
            return -1

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

    def get_plugin_path(self):
        """
        Retrieves the path to the plugin representing (associated)
        the automation structure.

        @rtype: String
        @return: The path to the plugin representing (associated)
        the automation structure.
        """

        # retrieves the plugin manager
        manager = self.associated_plugin.manager

        # retrieves the associated plugin id
        associated_plugin_id = self.associated_plugin.id

        # retrieves the associated plugin path
        associated_plugin_path = manager.get_plugin_path_by_id(associated_plugin_id)

        # returns the associated plugin path
        return associated_plugin_path

class RuntimeInformationStructure:
    """
    The class representing the runtime structures
    for the build automation.
    """

    success = False
    """ Flag controlling the success of the current build automation """

    logging_buffer = None
    """ Buffer to the logging """

    initial_date_time = None
    """ The date time structure of the beginning of the run """

    skipped = False
    """ Flag controlling if the build automation was skipped """

    properties = {}
    """ Map containing various properties of the build automation runtime """

    def __init__(self, success = False, logging_buffer = None, initial_date_time = None, skipped = False, properties = None):
        """
        Constructor of the class.

        @type success: bool
        @param success: Flag controlling the success of the current build automation.
        @type logging_buffer: StringBuffer
        @param logging_buffer: The date time structure of the beginning of the run.
        @type initial_date_time: DateTime
        @param initial_date_time: The date time structure of the beginning of the run.
        @type skipped: bool
        @param skipped: Flag controlling if the build automation was skipped.
        @type properties: Dictionary
        @param properties: Map containing various properties of the build automation runtime.
        """

        self.success = success
        self.logging_buffer = logging_buffer
        self.initial_date_time = initial_date_time
        self.skipped = skipped

        self.properties = properties and properties or {}
