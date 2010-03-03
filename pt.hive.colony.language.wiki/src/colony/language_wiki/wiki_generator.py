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

import time
import logging

import os.path

import libs.extension_system

import language_wiki.wiki_extension_system

class WikiGenerator:
    """
    The wiki generator class.
    """

    log_level = None
    """ The log level """

    extension_manager = None
    """ The extension manager """

    generation_engine = None
    """ The generation engine """

    generation_properties = {}
    """ The generation properties """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.generation_properties = {}

    def start_logger(self, verbose = False, debug = False):
        """
        Starts the logger system.

        @type verbose: bool
        @param verbose: If the log is going to be of type verbose.
        @type debug: bool
        @param debug: If the log is going to be of type debug.
        """

        # in case debug is set
        if debug:
            # sets the log level to debug
            self.log_level = logging.DEBUG
        # in case debug is verbose
        elif verbose:
            # sets the log level to info
            self.log_level = logging.INFO
        # otherwise
        else:
            # sets the log level to warn
            self.log_level = logging.WARN

    def start_extension_manager(self):
        """
        Starts the extension manager in the wiki generator.
        """

        # creates a new extension manager
        self.extension_manager = libs.extension_system.ExtensionManager([os.path.dirname(__file__) + "/extensions"])
        self.extension_manager.set_extension_class(language_wiki.wiki_extension_system.WikiExtension)
        self.extension_manager.start_logger(self.log_level)
        self.extension_manager.set_base_path(os.path.dirname(__file__))
        self.extension_manager.load_system()

    def process(self):
        """
        Processes the wiki generator task.
        """

        # retrieves the extension manager
        extension_manager = self._get_extension_manager()

        # retrieves the generation extensions
        generation_extensions = extension_manager.get_extensions_by_capability("generation")

        # in case generation engine is defined
        if self.generation_engine:
            # filters the generation extensions to retrieve just the demanded ones
            generation_extensions = [generation_extension for generation_extension in generation_extensions if generation_extension.get_generation_type() == self.generation_engine]

        # retrieves the start time
        start_time = time.time()

        # iterates over all the generation extensions
        for generation_extension in generation_extensions:
            # generates the wiki for the given properties
            generation_extension.generate_wiki(self.generation_properties)

        # retrieves the end time
        end_time = time.time()

        # calculates the time difference
        time_difference = end_time - start_time

        # rounds the time difference
        time_difference_rounded = round(time_difference, 2)

        # prints an info message
        extension_manager.logger.info("Processing took: %s seconds" % time_difference_rounded)

    def get_generation_engine(self):
        """
        Retrieves the generation engine.

        @rtype: String
        @return: The generation engine.
        """

        return self.generation_engine

    def set_generation_engine(self, generation_engine):
        """
        Sets the generation engine.

        @type generation_engine: String
        @param generation_engine: The generation engine.
        """

        self.generation_engine = generation_engine

    def get_generation_properties(self):
        """
        Retrieves the generation properties.

        @rtype: Dictionary
        @return: The generation properties.
        """

        return self.generation_properties

    def set_generation_properties(self, generation_properties):
        """
        Sets the generation properties.

        @type generation_properties: Dictionary
        @param generation_properties: The generation properties.
        """

        self.generation_properties = generation_properties

    def _get_extension_manager(self):
        """
        Retrieves the extension manager, starting it if necessary.

        @rtype: ExtensionManager
        @return: The extension manger.
        """

        # in case the extension manager is not defined
        if not self.extension_manager:
            # starts the extension manager
            self.start_extension_manager()

        # returns the extension manager
        return self.extension_manager
