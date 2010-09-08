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

__author__ = "Nelson Lima <nlima@hive.pt>"
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

import colony.base.plugin_system

HELP_TEXT = "### TRANSLATION DUMMY PLUGIN HELP ###\n\
get_translation_engines            - lists all the available translation engines\n\
translate <dictionary-name> <word> - translates a word for the given dictionary name"

class TranslationDummyPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Translation Dummy plugin.
    """

    id = "pt.hive.colony.plugins.dummy.translation"
    name = "Translation Dummy Plugin"
    short_name = "Translation Dummy"
    description = "This is the main plugin for the translation's stuff"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/dummy/translation/resources/baf.xml"}
    capabilities = ["console_command_extension", "build_automation_item"]
    capabilities_allowed = ["translation_engine"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = []

    translation_engine_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

        if capability == "translation_engine":
            self.translation_engine_plugins.append(plugin)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

        if capability == "translation_engine":
            self.translation_engine_plugins.remove(plugin)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return "translation_dummy"

    def get_all_commands(self):
        return ["get_translation_engines", "translate"]

    def get_handler_command(self, command):
        if command == "get_translation_engines":
            return self.handler_get_translation_engines
        elif command == "translate":
            return self.handler_translate

    def get_help(self):
        return HELP_TEXT

    def handler_get_translation_engines(self, args, output_method):
        # iterates over all the translation engine plugins
        for translation_engine_plugin in self.translation_engine_plugins:
            # retrieves the dictionary name
            dictionary_name = translation_engine_plugin.get_dictionary_name()

            # prints the dictionary name
            output_method(dictionary_name)

    def handler_translate(self, args, output_method):
        dictionary, word = args

        for translation_engine_plugin in self.translation_engine_plugins:
            dictionary_name = translation_engine_plugin.get_dictionary_name()
            if dictionary_name == dictionary:
                output_method(translation_engine_plugin.translate_word(word))
