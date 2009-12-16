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

import libs.extension_system

import wiki_extension_system

USAGE_MESSAGE = "wiki_generator --file=file_path [--target=target_path] [-v] [-d]"
""" The usage message """

DEFAULT_TARGET_PATH = "generated"
""" The default target path """

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

    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARN

    # creates a new extension manager
    extension_manager = libs.extension_system.ExtensionManager(["./extensions"])
    extension_manager.set_extension_class(wiki_extension_system.WikiExtension)
    extension_manager.start_logger(log_level)
    extension_manager.load_system()

    # retrieves the generation extensions
    generation_extensions = extension_manager.get_extensions_by_capability("generation")

    # creates the properties map
    properties = {"file_path" : file_path, "target_path" : target_path}

    # retrieves the start time
    start_time = time.time()

    # iterates over all the generation extensions
    for generation_extension in generation_extensions:
        # generates the wiki for the given properties
        generation_extension.generate_wiki(properties)

    # retrieves the end time
    end_time = time.time()

    # calculates the time difference
    time_difference = end_time - start_time

    # rounds the time difference
    time_difference_rounded = round(time_difference, 2)

    # prints an info message
    extension_manager.logger.info("Processing took: %s seconds" % time_difference_rounded)
