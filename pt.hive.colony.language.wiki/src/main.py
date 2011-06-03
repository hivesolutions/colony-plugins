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

__revision__ = "$LastChangedRevision: 3219 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-05-26 11:52:00 +0100 (ter, 26 Mai 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import getopt

USAGE_MESSAGE = "wiki_generator --file=file_path [--target=target_path] [--generation=generation_engine] [-v] [-d]"
""" The usage message """

DEFAULT_TARGET_PATH = "generated"
""" The default target path """

COLONY_PATH = "colony"
""" The colony path """

if __name__ == "__main__":
    # adds the colony path to the system path
    sys.path.insert(0, os.path.abspath(COLONY_PATH))

    # imports the wiki generator
    import colony.language_wiki.wiki_generator

    # starts the verbose flag as false
    verbose = False

    # starts the debug flag as false
    debug = False

    # start the file path value as None
    file_path = None

    # start the target path as the default target path
    target_path = None

    # start the generation as None
    generation = None

    # retrieves the argument options
    opts, args = getopt.getopt(sys.argv[1:], "vdf:t:", ["verbose", "debug", "file=", "target=", "generation="])

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
        elif option in ("-g", "--generation"):
            generation = value

    # in case the file path is not defined
    if not file_path:
        print "File Path not defined"
        print "Usage: " + USAGE_MESSAGE
        sys.exit(2)

    # in case the target path is not defined
    if not target_path:
        # sets the default target path
        target_path = file_path + "/" + DEFAULT_TARGET_PATH

    # creates the properties map
    properties = {
        "file_path" : file_path,
        "target_path" : target_path
    }

    # creates a new wiki generator
    wiki_generator = colony.language_wiki.wiki_generator.WikiGenerator()

    # starts the logger in the wiki generator
    wiki_generator.start_logger(verbose, debug)

    # sets the generation engine in the wiki generator
    wiki_generator.set_generation_engine(generation)

    # sets the generation properties in the wiki generator
    wiki_generator.set_generation_properties(properties)

    # processes the wiki generator
    wiki_generator.process()
