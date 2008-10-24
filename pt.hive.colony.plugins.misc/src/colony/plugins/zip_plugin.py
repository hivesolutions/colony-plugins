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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class ZipPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Zip plugin
    """

    id = "pt.hive.colony.plugins.misc.zip"
    name = "Zip Plugin"
    short_name = "Zip"
    description = "A Plugin to manage zip files"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["zip"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    zip_system = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.zip.zip_system
        self.zip_system = misc.zip.zip_system.Zip(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.zip_system = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def zip(self, zip_file_path, input_directory, file_path_list = None):
        """
        Compresses the contents of the provided directory into a zip file.
        
        @type zip_file_path: String
        @param zip_file_path: Full path to the zip file.
        @type input_directory: String
        @param input_directory: Full path to the directory one wants to compress.
        @type file_path_list: List
        @param file_path_list: List of relative file paths.
        """
        
        self.zip_system.zip(zip_file_path, input_directory, file_path_list)


    def unzip(self, zip_file_path, output_directory):
        """
        Extracts a zip file to the specified directory.
        
        @type file_path: String
        @param zip_file_path: Full path to the zip file.
        @type output_directory: String
        @param output_directory: Full path to the directory where one wants to extract the zip file to.
        """

        self.zip_system.unzip(zip_file_path, output_directory)

    def get_file_paths(self, file_path):
        """
        Returns a list with the paths to the files contained in the specified zip file.
        
        @type path: String
        @param path: Path to the zip file.
        @rtype: List
        @return: List of file paths.
        """

        return self.zip_system.get_file_paths(file_path)

    def get_directory_paths(self, file_path):
        """
        Returns a list with the paths to the directories contained in the specified zip file.
        
        @type path: String
        @param path: Path to the zip file.
        @rtype: List
        @return: List of directory paths.
        """

        return self.zip_system.get_directory_paths(file_path)
