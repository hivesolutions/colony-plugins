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

import language_wiki.wiki_generator

class LanguageWiki:
    """
    The language wiki class.
    """

    language_wiki_plugin = None
    """ The language wiki plugin """

    wiki_generator = None
    """ The wiki generator object """

    def __init__(self, language_wiki_plugin):
        """
        Constructor of the class.

        @type language_wiki_plugin: LanguageWikiPlugin
        @param language_wiki_plugin: The language wiki plugin.
        """

        self.language_wiki_plugin = language_wiki_plugin

        # initializes the wiki generator
        self.initialize_wiki_generator()

    def initialize_wiki_generator(self):
        """
        Initializes the wiki generator.
        """

        # creates a new wiki generator
        self.wiki_generator = language_wiki.wiki_generator.WikiGenerator()

        # starts the logger in the wiki generator
        self.wiki_generator.start_logger()

    def generate(self, engine_name, engine_properties):
        """
        Generates the wiki output base in the given engine name
        and in the given engine properties.

        @type engine_name: String
        @param engine_name: The name of the engine to be used in generation.
        @type engine_properties: Dictionary
        @param engine_properties: The properties to be used by the engine
        during the engine processing.
        """

        # sets the generation engine in the wiki generator
        self.wiki_generator.set_generation_engine(engine_name)

        # sets the generation properties in the wiki generator
        self.wiki_generator.set_generation_properties(engine_properties)

        # processes the wiki generator
        self.wiki_generator.process()
