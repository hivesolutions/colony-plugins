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

class DummyEnglishDictionaryPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy English Dictionary plugin.
    """

    id = "pt.hive.colony.plugins.dummy.english"
    name = "Dummy English Dictionary Plugin"
    short_name = "Dummy English Dictionary"
    description = "This is the main plugin for the english dictionary's stuff"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/dummy/english_dictionary/resources/baf.xml"
    }
    capabilities = [
        "translation_engine",
        "build_automation_item"
    ]
    main_modules = [
        "dummy.english_dictionary.dummy_english_dictionary_system"
    ]

    dummy_english_dictionary = None
    """ The dummy english dictionary """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import dummy.english_dictionary.dummy_english_dictionary_system
        self.dummy_english_dictionary = dummy.english_dictionary.dummy_english_dictionary_system.DummyEnglishDictionary(self)

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

    def get_dictionary_name(self):
        return self.dummy_english_dictionary.get_dictionary_name()

    def translate_word(self, word):
        return self.dummy_english_dictionary.translate_word(word)
