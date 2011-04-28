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

import colony.base.plugin_system

class StringNormalizationPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the String Normalization plugin.
    """

    id = "pt.hive.colony.plugins.misc.string_normalization"
    name = "String Normalization Plugin"
    short_name = "String Normalization"
    description = "A plugin to manage the normalization of strings"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/string_normalization/resources/baf.xml"
    }
    capabilities = [
        "string_normalization",
        "build_automation_item"
    ]
    main_modules = [
        "misc.string_normalization.string_normalization_system"
    ]

    string_normalization = None
    """ The string normalization """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.string_normalization.string_normalization_system
        self.string_normalization = misc.string_normalization.string_normalization_system.StringNormalization(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def remove_trailing_newlines_file(self, file_path, windows_newline):
        """
        Removes the trailing newlines from the contents given.
        This method uses a file and the given file replaces with the
        new contents.

        @type file_path: String
        @param file_path: The path to the file to have the trailing
        newlines removed.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        """

        return self.string_normalization.remove_trailing_newlines_file(file_path, windows_newline)

    def remove_trailing_newlines(self, contents, windows_newline):
        """
        Removes the trailing newlines from the contents given.

        @type contents: String
        @param contents: The contents to have the trailing newlines removed.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        @rtype: String
        @return: The contents with the trailing newlines removed.
        """

        return self.string_normalization.remove_trailing_newlines(contents, windows_newline)

    def remove_trailing_spaces_file(self, file_path, tab_to_spaces, windows_newline):
        """
        Removes the trailing spaces from the contents given.
        This method uses a file and the given file replaces with the
        new contents.

        @type file_path: String
        @param file_path: The path to the file to have the trailing
        newlines removed.
        @type tab_to_spaces: bool
        @param tab_to_spaces: If the tab characters should be converted to spaces.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        """

        return self.string_normalization.remove_trailing_spaces_file(file_path, tab_to_spaces, windows_newline)

    def remove_trailing_spaces(self, contents, tab_to_spaces, windows_newline):
        """
        Removes the trailing spaces from the contents given.

        @type contents: String
        @param contents: The contents to have the trailing spaces removed.
        @type tab_to_spaces: bool
        @param tab_to_spaces: If the tab characters should be converted to spaces.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        @rtype: String
        @return: The contents with the trailing spaces removed.
        """

        return self.string_normalization.remove_trailing_spaces(contents, tab_to_spaces, windows_newline)

    def remove_trailing_spaces_recursive(self, directory_path, tab_to_spaces, trailing_newlines, windows_newline, file_extensions):
        """
        Removes the trailing spaces recursively from the given directory path.
        The control parameters include tab to spaces, removal of trailing newlines
        use of the windows line and file extensions filter.

        @type directory_path: String
        @param directory_path: The path to the directory to be used.
        @type tab_to_spaces: bool
        @param tab_to_spaces: If the tab characters should be converted to spaces.
        @type trailing_newlines: bool
        @param trailing_newlines: If the trailing newlines should be removed.
        @type windows_newline: bool
        @param windows_newline: If the windows newline should be used.
        @type file_extensions: List
        @param file_extensions: The list of file extensions to be filtered.
        """

        return self.string_normalization.remove_trailing_spaces_recursive(directory_path, tab_to_spaces, trailing_newlines, windows_newline, file_extensions)
