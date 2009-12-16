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

import sys
import time
import getopt
import logging

import wiki_html_generator

USAGE_MESSAGE = "wiki_generator --file=file_path [--target=target_path] [-v] [-d]"
""" The usage message """

DEFAULT_LOGGER_NAME = "wiki_generate"
""" The default logger name """

DEFAULT_TARGET_PATH = "generated"
""" The default target path """

class WikiGenerator:
    """
    Thw wiki generator class.
    """

    logger = None
    """ The logger """

    def __init__(self, logger = logging):
        """
        Constructor of the class.

        @type logger: Logger
        @param logger: The logger.
        """

        self.logger = logger

def _start_logger(verbose = False, debug = False):
    """
    Starts the logger for the given parameters.

    @type verbose: bool
    @param verbose: If the log is going to be of type verbose.
    @type debug: bool
    @param debug: If the log is going to be of type debug.
    @rtype: Logger
    @return: The logger.
    """

    # retrieves the logger
    logger = logging.getLogger(DEFAULT_LOGGER_NAME)

    # in case debug is active
    if debug:
        # sets the logger level to debug
        logger.setLevel(logging.DEBUG)

    # in case verbose is active
    if verbose:
        # sets the logger level to info
        logger.setLevel(logging.INFO)

    # returns the logger
    return logger

def _get_logger():
    """
    Retrieves the logger.

    @rtype: Logger
    @return: The logger.
    """

    # retrieves the logger
    logger = logging.getLogger(DEFAULT_LOGGER_NAME)

    # returns the logger
    return logger

if __name__ == "__main__":
    # starts the verbose flag as false
    verbose = False

    # starts the debug flag as false
    debug = False

    # start the file path value as None
    file_path = None

    # start the target path as None
    target_path = DEFAULT_TARGET_PATH

    # retrieves the argument options
    opts, args = getopt.getopt(sys.argv[1:], "vdf:t:", ["verbose", "debug", "file=", "target="])

    # iterates over all the given options
    for option, value in opts:
        if option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-d", "--debug"):
            debug = True
        elif option in ("-f", "--file"):
            file_path = value
        elif option in ("-y", "--target"):
            target_path = value

    # in case the file path is not defined
    if not file_path:
        print "File Path not defined"
        print "Usage: " + USAGE_MESSAGE
        sys.exit(2)

    # starts the logger for the given parameters
    logger = _start_logger(verbose, debug)

    # creates the wiki generator
    wiki_generator = wiki_html_generator.WikiHtmlGenerator(logger)

    # retrieves the start time
    start_time = time.time()

    # generates the wiki
    wiki_generator.generate_wiki(file_path, target_path)

    # retrieves the end time
    end_time = time.time()

    # calculates the time difference
    time_difference = end_time - start_time

    # rounds the time difference
    time_difference_rounded = round(time_difference, 2)

    # prints an info message
    logger.info("Processing took: %s seconds" % time_difference_rounded)
