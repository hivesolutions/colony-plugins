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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HELP_TEXT = "### TRANSLATION DUMMY PLUGIN HELP ###\n\
get_translation_engines            - lists all the available translation engines\n\
translate <dictionary-name> <word> - translates a word for the given dictionary name"

class DummyTranslation:
    """
    The dummy translation.
    """

    dummy_translation_plugin = None
    """ The dummy translation plugin """

    def __init__(self, dummy_translation_plugin):
        """
        Constructor of the class.

        @type dummy_translation_plugin: DummyTranslationPlugin
        @param dummy_translation_plugin: The dummy translation plugin.
        """

        self.dummy_translation_plugin = dummy_translation_plugin

    def get_console_extension_name(self):
        return "translation_dummy"

    def get_all_commands(self):
        return [
            "get_translation_engines",
            "translate"
        ]

    def get_handler_command(self, command):
        if command == "get_translation_engines":
            return self.handler_get_translation_engines
        elif command == "translate":
            return self.handler_translate

    def get_help(self):
        return HELP_TEXT

    def handler_get_translation_engines(self, args, output_method):
        # retrieves the translation engine plugins
        translation_engine_plugins = self.dummy_translation_plugin.translation_engine_plugins

        # iterates over all the translation engine plugins
        for translation_engine_plugin in translation_engine_plugins:
            # retrieves the dictionary name
            dictionary_name = translation_engine_plugin.get_dictionary_name()

            # prints the dictionary name
            output_method(dictionary_name)

    def handler_translate(self, args, output_method):
        # retrieves the translation engine plugins
        translation_engine_plugins = self.dummy_translation_plugin.translation_engine_plugins

        # retrieves the translate arguments
        dictionary, word = args

        # iterates over all the translation engine plugins
        for translation_engine_plugin in translation_engine_plugins:
            # retrieves the dictionary name
            dictionary_name = translation_engine_plugin.get_dictionary_name()

            # in case the dictionary name is the same
            # as the requested dictionary
            if dictionary_name == dictionary:
                # translates the work and puts the result in the output
                output_method(translation_engine_plugin.translate_word(word))
