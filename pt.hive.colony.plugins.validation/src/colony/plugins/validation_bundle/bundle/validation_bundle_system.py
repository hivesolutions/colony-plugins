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

import os

BUNDLE_VALUE = "bundle"
""" The bundle value """

BUNDLE_ID_VALUE = "bundle_id"
""" The bundle id value """

BUNDLE_VERSION_VALUE = "bundle_version"
""" The bundle version value """

BUNDLE_PATH_VALUE = "bundle_path"
""" The bundle path value """

DEPENDENCIES_VALUE = "dependencies"
""" The dependencies value """

ID_VALUE = "id"
""" The id value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

MESSAGE_VALUE = "message"
""" The message value """

PLATFORM_VALUE = "platform"
""" The platform value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

PYTHON_VALUE = "python"
""" The python value """

TYPE_VALUE = "type"
""" The type value """

VERSION_VALUE = "version"
""" The version value """

BUNDLE_FILE_NAME_ENDING = "_bundle.json"
""" The bundle file name ending """

DEFAULT_JSON_ENCODING = "Cp1252"
""" The default json encoding """

COLONY_BUNDLE_NAMESPACE = "pt.hive.colony.bundles."
""" The colony bundle namespace """

COLONY_PLUGIN_NAMESPACE = "pt.hive.colony.plugins."
""" The colony plugin namespace """

MANDATORY_BUNDLE_ATTRIBUTE_NAMES = ("type", "platform", "id", "version", "author", "plugins", "dependencies")
""" The mandatory bundle attribute names """

PLUGIN_EXCLUSION_LIST = ("pt.hive.colony.bundles.plugins.base.bundles")
""" The plugin exclusion list """

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

class ValidationBundle:
    """
    The validation bundle class.
    """

    validation_bundle_plugin = None
    """ The validation bundle plugin """

    def __init__(self, validation_bundle_plugin):
        """
        Constructor of the class.

        @type validation_bundle_plugin: ValidationBundlePlugin
        @param validation_bundle_plugin: The validation bundle plugin.
        """

        self.validation_bundle_plugin = validation_bundle_plugin

    def validate_bundles(self, bundle_file_paths):
        # initializes the validation errors list
        validation_errors = []

        # retrieves the bundle file paths in case an empty list was provided
        if not bundle_file_paths:
            bundle_file_paths = self.get_bundle_file_paths()

        # retrieves the bundle data map
        bundle_data_map = self.get_bundle_data_map(bundle_file_paths, validation_errors)

        # retrieves the plugin bundle_map
        plugin_bundle_map = self.get_plugin_bundle_map(bundle_data_map, validation_errors)

        # retrieves all plugins
        plugins = self.validation_bundle_plugin.manager.get_all_plugins()

        # checks that all plugins are inside a bundle
        for plugin in plugins:
            # skips in case the plugin is in the exclusion list
            if plugin.original_id in PLUGIN_EXCLUSION_LIST:
                continue

            # skips in case the plugin is not a colony plugin
            if not plugin.original_id.startswith(COLONY_PLUGIN_NAMESPACE):
                continue

            # defines the plugin bundle key
            plugin_bundle_key = (plugin.original_id, plugin.version)

            # checks if the plugin is in a bundle
            if not plugin_bundle_key in plugin_bundle_map:
                # adds the validation error
                self.add_validation_error(validation_errors, None, None, None, "'%s (%s)' is not in any bundle" % (plugin.original_id, plugin.version))

        # validates all bundles
        for bundle_data_key in bundle_data_map:
            self._validate_bundle(bundle_data_key, bundle_data_map, plugin_bundle_map, validation_errors)

        # returns the validation errors
        return validation_errors

    def _validate_bundle(self, bundle_data_key, bundle_data_map, plugin_bundle_map, validation_errors):
        # retrieves the bundle data
        bundle_data = bundle_data_map[bundle_data_key]

        # retrieves the bundle type
        bundle_type = bundle_data[TYPE_VALUE]

        # retrieves the bundle platform
        bundle_platform = bundle_data[PLATFORM_VALUE]

        # retrieves the bundle id
        bundle_id = bundle_data[ID_VALUE]

        # retrieves the bundle version
        bundle_version = bundle_data[VERSION_VALUE]

        # retrieves the bundle file path
        bundle_file_path = bundle_data[FILE_PATH_VALUE]

        # retrieves the bundle plugins
        bundle_plugins = bundle_data[PLUGINS_VALUE]

        # retrieves the bundle dependencies
        bundle_dependencies = bundle_data[DEPENDENCIES_VALUE]

        # checks that the bundle type is correct
        if not bundle_type == BUNDLE_VALUE:
            # adds the validation error
            self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' has invalid attribute 'type'" % (bundle_id, bundle_version))

        # checks that the bundle platform is correct
        if not bundle_platform == PYTHON_VALUE:
            # adds the validation error
            self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' has invalid attribute 'platform'" % (bundle_id, bundle_version))

        # checks that the bundle id starts with the expected namespace
        if not bundle_id.startswith(COLONY_BUNDLE_NAMESPACE):
            # adds the validation error
            self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' does not start with '%s'" % (bundle_id, bundle_version, COLONY_BUNDLE_NAMESPACE))

        # validates the bundle plugins
        for bundle_plugin in bundle_plugins:
            self.__validate_bundle_plugin(bundle_data, bundle_plugin, plugin_bundle_map, validation_errors)

        # validates the bundle dependencies
        for bundle_dependency in bundle_dependencies:
            self.__validate_bundle_dependency(bundle_data, bundle_data_map, bundle_dependency, validation_errors)

    def __validate_bundle_plugin(self, bundle_data, bundle_plugin, plugin_bundle_map, validation_errors):
        # retrieves the bundle id
        bundle_id = bundle_data[ID_VALUE]

        # retrieves the bundle version
        bundle_version = bundle_data[VERSION_VALUE]

        # retrieves the bundle plugin id
        bundle_plugin_id = bundle_plugin[ID_VALUE]

        # retrieves the bundle plugin version
        bundle_plugin_version = bundle_plugin[VERSION_VALUE]

        # retrieves the bundle file path
        bundle_file_path = bundle_data[FILE_PATH_VALUE]

        # retrieves the bundle dependencies
        bundle_dependencies = bundle_data[DEPENDENCIES_VALUE]

        # retrieves the bundle dependency id version tuples
        bundle_dependency_keys = [(bundle_dependency[ID_VALUE], bundle_dependency[VERSION_VALUE]) for bundle_dependency in bundle_dependencies]

        # retrieves the bundle plugin
        plugin = self.validation_bundle_plugin.manager._get_plugin_by_id_and_version(bundle_plugin_id, bundle_plugin_version)

        # adds a validation error in case the plugin doesn't exist
        if not plugin:
            # adds the validation error
            self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' references unexistent plugin '%s (%s)'" % (bundle_id, bundle_version, bundle_plugin_id, bundle_plugin_version))

            # skips this bundle plugin
            return

        # retrieves the plugin dependencies
        plugin_dependencies = plugin.get_all_plugin_dependencies()

        # checks that the plugin's dependencies are contained in one of the bundle's bundle dependencies
        for plugin_dependency in plugin_dependencies:
            # defines the plugin bundle key
            plugin_bundle_key = (plugin_dependency.plugin_id, plugin_dependency.plugin_version)

            # checks that the plugin dependency is in a bundle
            if not plugin_bundle_key in plugin_bundle_map:
                # adds the validation error
                self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' references plugin '%s (%s)' whose dependency '%s (%s)' is not in any bundle" % (bundle_id, bundle_version, bundle_plugin_id, bundle_plugin_version, plugin_dependency.plugin_id, plugin_dependency.plugin_version))

                # skips this dependency
                continue

            # defines the plugin bundle key
            plugin_bundle_key = (plugin_dependency.plugin_id, plugin_dependency.plugin_version)

            # unpacks the plugin dependency key
            plugin_dependency_bundle_dependency_key = plugin_bundle_map[plugin_bundle_key]

            # retrieves the id and version of the bundle the plugin dependency is contained in
            plugin_dependency_bundle_id, plugin_dependency_bundle_version = plugin_dependency_bundle_dependency_key

            # skips in case the dependency is within the same bundle
            if plugin_dependency_bundle_id == bundle_id and plugin_dependency_bundle_version == bundle_version:
                continue

            # checks that the bundle the plugin dependency is contained ib is referenced in the bundle's dependencies
            if not plugin_dependency_bundle_dependency_key in bundle_dependency_keys:
                # adds the validation error
                self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' references plugin '%s (%s)' whose dependency '%s (%s)' is not in any bundle referenced in the dependencies" % (bundle_id, bundle_version, bundle_plugin_id, bundle_plugin_version, plugin_dependency.plugin_id, plugin_dependency.plugin_version))

    def __validate_bundle_dependency(self, bundle_data, bundle_data_map, bundle_dependency, validation_errors):
        # retrieves the bundle id
        bundle_id = bundle_data[ID_VALUE]

        # retrieves the bundle version
        bundle_version = bundle_data[VERSION_VALUE]

        # retrieves the bundle file path
        bundle_file_path = bundle_data[FILE_PATH_VALUE]

        # retrieves the bundle dependency id
        bundle_dependency_id = bundle_dependency[ID_VALUE]

        # retrieves the bundle dependency version
        bundle_dependency_version = bundle_dependency[VERSION_VALUE]

        # checks that the bundle dependency id starts with the expected namespace
        if not bundle_dependency_id.startswith(COLONY_BUNDLE_NAMESPACE):
            # adds the validation error
            self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' has dependency '%s (%s)' that does not start with '%s'" % (bundle_id, bundle_version, bundle_dependency_id, bundle_dependency_version, COLONY_BUNDLE_NAMESPACE))

            # returns since nothing else can be tested
            return

        # retrieves the bundle dependency version
        bundle_dependency_version = bundle_dependency[VERSION_VALUE]

        # defines the bundle data key
        bundle_data_key = (bundle_dependency_id, bundle_dependency_version)

        # checks if the bundle dependency exists
        if not bundle_data_key in bundle_data_map:
            # adds the validation error
            self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "Bundle '%s (%s)' references unexistent bundle '%s (%s)'" % (bundle_id, bundle_version, bundle_dependency_id, bundle_dependency_version))

    def get_bundle_data_map(self, bundle_file_paths, validation_errors):
        # initializes the bundle map
        bundle_data_map = {}

        # populates the bundle data map
        for bundle_file_path in bundle_file_paths:
            try:
                # retrieves the bundle data
                bundle_data = self.get_json_data(bundle_file_path)
            except:
                # logs the validation error
                self.add_validation_error(validation_errors, None, None, bundle_file_path, "'%s' has invalid syntax" % bundle_file_path)
            else:
                # initializes the valid attribute
                valid = True

                # checks that all bundle attributes are present
                for bundle_attribute_name in MANDATORY_BUNDLE_ATTRIBUTE_NAMES:
                    # skips the iteration in case the attribute was found
                    if bundle_attribute_name in bundle_data:
                        continue

                    # marks the bundle as invalid
                    valid = False

                    # logs the validation error
                    self.add_validation_error(validation_errors, None, None, bundle_file_path, "'%s' is missing attribute '%s'" % (bundle_file_path, bundle_attribute_name))

                # skips the bundle in case it is missing an attribute
                if not valid:
                    continue

                # sets the bundle file path in the bundle data
                bundle_data[FILE_PATH_VALUE] = bundle_file_path

                # retrieves the bundle id
                bundle_id = bundle_data[ID_VALUE]

                # retrieves the bundle version
                bundle_version = bundle_data[VERSION_VALUE]

                # creates the bundle data key
                bundle_data_key = (bundle_id, bundle_version)

                # sets the bundle data in the bundle data map
                bundle_data_map[bundle_data_key] = bundle_data

        return bundle_data_map

    def get_plugin_bundle_map(self, bundle_data_map, validation_errors):
        # initializes the plugin bundle map
        plugin_bundle_map = {}

        # populates the plugin bundle map
        for bundle_data_key in bundle_data_map:
            # retrieves the bundle data
            bundle_data = bundle_data_map[bundle_data_key]

            # retrieves the bundle plugins
            bundle_plugins = bundle_data[PLUGINS_VALUE]

            # associates the bundle plugins with the bundle
            for bundle_plugin in bundle_plugins:
                self._get_plugin_bundle_map(bundle_data, bundle_plugin, plugin_bundle_map, validation_errors)

        return plugin_bundle_map

    def _get_plugin_bundle_map(self, bundle_data, bundle_plugin, plugin_bundle_map, validation_errors):
        # retrieves the bundle id
        bundle_id = bundle_data[ID_VALUE]

        # retrieves the bundle version
        bundle_version = bundle_data[VERSION_VALUE]

        # retrieves the bundle plugin id
        bundle_plugin_id = bundle_plugin[ID_VALUE]

        # retrieves the bundle plugin version
        bundle_plugin_version = bundle_plugin[VERSION_VALUE]

        # defines the plugin bundle key
        plugin_bundle_key = (bundle_plugin_id, bundle_plugin_version)

        # checks that the plugin is not in more than one bundle
        if plugin_bundle_key in plugin_bundle_map:
            # retrieves the bundle file path
            bundle_file_path = bundle_data[FILE_PATH_VALUE]

            # retrieves the duplicate bundle id and version
            duplicate_bundle_id, duplicate_bundle_version = plugin_bundle_map[plugin_bundle_key]

            # adds the validation error
            self.add_validation_error(validation_errors, bundle_id, bundle_version, bundle_file_path, "'%s (%s)' is in bundle '%s' (%s) and bundle '%s (%s)'" % (bundle_plugin_id, bundle_plugin_version, bundle_id, bundle_version, duplicate_bundle_id, duplicate_bundle_version))

            # skips this bundle plugin
            return

        # associates the bundle plugin with the bundle
        plugin_bundle_map[plugin_bundle_key] = (bundle_id, bundle_version)

    def get_bundle_file_paths(self):
        # initializes the bundle file paths list
        bundle_file_paths = []

        # retrieves all plugins
        plugins = self.validation_bundle_plugin.manager.get_all_plugins()

        # collects the bundle file paths discovered within each plugin
        for plugin in plugins:
            # retrieves the plugin path
            plugin_path = self.validation_bundle_plugin.manager.get_plugin_path_by_id(plugin.id)

            # retrieves the bundle file paths within the specified path
            bundle_file_paths += self._get_bundle_file_paths(plugin_path, [])

        return bundle_file_paths

    def _get_bundle_file_paths(self, path, file_paths):
        # retrieves the path entries for the specified path
        path_entries = os.listdir(path)

        # sorts the path entries
        path_entries.sort()

        # initializes the directory paths list
        directory_paths = []

        # collects file paths and directory paths
        for path_entry in path_entries:
            # defines the path entry path
            path_entry_path = path + UNIX_DIRECTORY_SEPARATOR + path_entry

            # collects a directory path and skips this iteration
            if os.path.isdir(path_entry_path):
                directory_paths.append(path_entry_path)
                continue

            # skips in case the file doesn't end with a bundle file name ending
            if not path_entry.endswith(BUNDLE_FILE_NAME_ENDING):
                continue

            # collects the file path
            file_paths.append(path_entry_path)

        # retrieves the file paths for the collected directories
        for directory_path in directory_paths:
            file_paths = self._get_bundle_file_paths(directory_path, file_paths)

        return file_paths

    def add_validation_error(self, validation_errors, bundle_id, bundle_version, bundle_file_path, validation_error_message):
        # defines the validation error map
        validation_error_map = {BUNDLE_ID_VALUE : bundle_id,
                                BUNDLE_VERSION_VALUE : bundle_version,
                                BUNDLE_PATH_VALUE : bundle_file_path,
                                MESSAGE_VALUE : validation_error_message}

        # adds the validation error map to the validation errors list
        validation_errors.append(validation_error_map)

    def get_json_data(self, json_file_path):
        # reads the json file
        json_file = open(json_file_path, "rb")

        try:
            # reads the data from the json file
            json_file_data = json_file.read()
        finally:
            # closes the json file
            json_file.close()

        # decodes the json file data
        json_file_data = json_file_data.decode(DEFAULT_JSON_ENCODING)

        # loads the json data from the json file
        json_data = self.validation_bundle_plugin.json_plugin.loads(json_file_data)

        return json_data
