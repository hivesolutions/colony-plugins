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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

CONFIGURATION_MODELS_BUNDLE_VALUE = "configuration_models_bundle"
""" The configuration models bundle value """

GLOBAL_VALUE = "global"
""" The global value """

REPLACE_VALUE = "replace"
""" The replace value """

PATH_VALUE = "path"
""" The path value """

CHUNK_SIZE = 4096
""" The chunk size """

class ConfigurationManager:
    """
    The configuration manager class.
    """

    configuration_manager_plugin = None
    """ The configuration manager plugin """

    def __init__(self, configuration_manager_plugin):
        """
        Constructor of the class.

        @type configuration_manager_plugin: ConfigurationManagerPlugin
        @param configuration_manager_plugin: Thee configuration manager plugin.
        """

        self.configuration_manager_plugin = configuration_manager_plugin

    def configuration_model_provider_load(self, configuration_model_provider_plugin):
        # retrieves the plugin manager
        plugin_manager = self.configuration_manager_plugin.manager

        # retrieves the configuration models bundle
        configuration_models_bundle = configuration_model_provider_plugin.get_attribute(CONFIGURATION_MODELS_BUNDLE_VALUE) or {}

        # retrieves the configuration model provider plugin id
        configuration_model_provider_plugin_id = configuration_model_provider_plugin.id

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(configuration_model_provider_plugin_id)

        # retrieves the plugin configuration paths
        plugin_configuration_paths = plugin_manager.get_plugin_configuration_paths_by_id(configuration_model_provider_plugin_id)

        # loads the configuration models bundle
        self._load_configuration_models_bundle(configuration_models_bundle, plugin_configuration_paths, plugin_path)

    def configuration_model_provider_unload(self, configuration_model_provider_plugin):
        pass

    def _load_configuration_models_bundle(self, configuration_models_bundle, plugin_configuration_paths, plugin_path):
        """
        Loads the configuration models bundle, using the given
        plugin configuration paths and the plugin path.

        @type configuration_models_bundle: Dictionary
        @param configuration_models_bundle: The configuration models bundle.
        @type plugin_configuration_paths: List
        @param plugin_configuration_paths: The plugin configuration paths.
        @type plugin_path: String
        @param plugin_path: The plugin path.
        """

        # unpacks the plugin configuration paths to get the global and the profile
        # configuration paths
        plugin_global_configuration_path, plugin_profile_configuration_path = plugin_configuration_paths

        # iterates over the configuration models bundle
        for configuration_model in configuration_models_bundle:
            # retrieves the configuration model properties
            configuration_model_properties = configuration_models_bundle[configuration_model]

            # retrieves the global value from the configuration model properties
            global_value = configuration_model_properties.get(GLOBAL_VALUE, False)

            # retrieves the replace value from the configuration model properties
            replace_value = configuration_model_properties.get(REPLACE_VALUE, False)

            # retrieves the path value from the configuration model properties
            path_value = configuration_model_properties.get(PATH_VALUE, configuration_model)

            # in case the global value is set
            if global_value:
                # sets the configuration model target directory path as the plugin
                # global configuration path
                configuration_model_target_directory_path = plugin_global_configuration_path
            else:
                # sets the configuration model target directory path as the plugin
                # profile configuration path
                configuration_model_target_directory_path = plugin_profile_configuration_path

            # retrieves the configuration model path
            configuration_model_path = plugin_path + "/" + path_value

            # retrieves the configuration model target path
            configuration_model_target_path = configuration_model_target_directory_path + "/" + configuration_model

            # retrieves the configuration model target path directory
            configuration_model_target_path_directory = os.path.dirname(configuration_model_target_path)

            # in case the configuration model target path does not exists
            # or the replace flag is active
            if not os.path.exists(configuration_model_target_path) or replace_value:
                # tries to creates the model path
                self._try_create_path(configuration_model_target_path_directory)

                # copies the model file to the target path
                self._copy_file(configuration_model_path, configuration_model_target_path)

    def _copy_file(self, file_path, target_file_path):
        """
        Copies the file in the file path to the given
        target path.

        @type file_path: String
        @param file_path: The path to the file to be copied.
        @type target_file_path: String
        @param target_file_path: The path to the target file.
        """

        # opens both the file the target file
        file = open(file_path, "rb")
        target_file = open(target_file_path, "wb")

        try:
            while True:
                # reads the contents from the file and copies them to
                # the target file
                contents = file.read(CHUNK_SIZE)

                # in case the contents are invalid (end of file is reached)
                if not contents:
                    # breaks the loop
                    break

                # writes the contents to the target file
                target_file.write(contents)
        finally:
            # closes both files
            file.close()
            target_file.close()

    def _try_create_path(self, path):
        """
        Tries to create the given path.

        @type path: String
        @param path: The path to try to create.
        """

        # in case the path does not exists
        if not os.path.exists(path):
            # creates the path directories
            os.makedirs(path)
