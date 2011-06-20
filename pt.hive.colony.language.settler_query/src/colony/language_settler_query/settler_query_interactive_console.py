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

import getopt
import sys

import settler_query_parser
import settler_query_processing

BRANDING_TEXT = "Settler Query 0.1 (Hive Solutions Lda. r1:Sep 19 2006)"
VERSION_PRE_TEXT = "Python "
HELP_TEXT = "Type \"help\", \"copyright\", \"credits\" or \"license\" for more information."

CARRET = "[settler_query] >> "
BLOCK_CARRET = "[settler_query] .. "

NEW_BLOCK_CHARACTER = ":"

EXIT_COMMAND = "exit()"

def get_command_from_command_list(command_list):
    command_string = str()

    for command_item in command_list:
        command_string += command_item + "\n"

    return command_string

def print_information():
    # print the branding information text
    print BRANDING_TEXT

    # print the python information
    print VERSION_PRE_TEXT + sys.version

    # prints some help information
    print HELP_TEXT

def process_command(command, processing_structure, global_interpretation_map, interpretation = False, debug = False, verbose = False, code_generation = False,):
    if debug:
        process_command_debug(command, processing_structure, global_interpretation_map, interpretation, verbose, code_generation)
    else:
        process_command_normal(command, processing_structure, global_interpretation_map, interpretation, verbose, code_generation)

def process_command_normal(command, processing_structure, global_interpretation_map, interpretation, verbose, code_generation):
    try:
        interpret_command(command, processing_structure, global_interpretation_map, interpretation, False, verbose, code_generation)
    except Exception, exception:
        print exception

def process_command_debug(command, processing_structure, global_interpretation_map, interpretation, verbose, code_generation):
    interpret_command(command, processing_structure, global_interpretation_map, interpretation, True, verbose, code_generation)

def interpret_command(command, processing_structure, global_interpretation_map, interpretation, debug, verbose, code_generation):
    # parses the command
    settler_query_parser.parser.parse(command)

def interactive_console(interpretation = False, debug = False, verbose = True, code_generation = False):
    # creates the exit flag
    exit_flag = False

    # creates a new processing structure
    processing_structure = settler_query_processing.ProcessingStructure()

    # starts the global interpretation map
    global_interpretation_map = {}

    # starts the block accumulation flag
    block_accumulation = False

    # starts the command accumulation list
    command_accumulation_list = []

    # prints the product information
    print_information()

    # loops while the exit flag is inactive
    while not exit_flag:
        try:
            if block_accumulation:
                carret = BLOCK_CARRET
            else:
                carret = CARRET

            # retrieves the string value from the raw input
            string_value = raw_input(carret)
        except EOFError:
            break
        # in case the string value is "blank"
        if string_value == "":
            if block_accumulation:
                # converts the list of accumulated commands to a command string
                command = get_command_from_command_list(command_accumulation_list)

                # processes the command
                process_command(command, processing_structure, global_interpretation_map, interpretation, debug, verbose, code_generation)

                # resets the block accumulation structures
                block_accumulation = False
                command_accumulation_list = []
        else:
            # strips the string value
            string_value_striped = string_value.strip()

            # retrieves the last character from the string value
            string_value_last_character = string_value_striped[-1]

            # in case the last character of the string is of a new block character
            if string_value_last_character == NEW_BLOCK_CHARACTER:
                block_accumulation = True

            # in case the exit command is sent
            if string_value_striped == EXIT_COMMAND:
                exit_flag = True
            elif block_accumulation:
                command_accumulation_list.append(string_value)
            else:
                process_command(string_value + "\n", processing_structure, global_interpretation_map, interpretation, debug, verbose, code_generation)

def interpret_file(file_path, interpretation = False, debug = False, verbose = True, code_generation = True):
    # opens the given file
    file = open(file_path, "r")

    # reads the file contents
    file_contents = file.read()

    # closes the file
    file.close()

    # creates a new processing structure
    processing_structure = settler_query_processing.ProcessingStructure()

    # starts the global interpretation map
    global_interpretation_map = {}

    # sets the global_context_code_information value
    global_interpretation_map["global_context_code_information"] = None

    # processes the command
    process_command(file_contents, processing_structure, global_interpretation_map, interpretation, debug, verbose, code_generation)

if __name__ == "__main__":
    # starts the verbose flag as false
    verbose = False

    # starts the debug flag as false
    debug = False

    # start the interpretation flag as false
    interpretation = False

    # start the file path value as None
    file_path = None

    # retrieves the argument options
    opts, args = getopt.getopt(sys.argv[1:], "ivdf:", ["interpretation", "verbose", "debug", "file="])

    # iterates over all the given options
    for option, value in opts:
        if option in ("-i", "--interpretation"):
            interpretation = True
        elif option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-d", "--debug"):
            debug = True
        elif option in ("-f", "--file"):
            file_path = value

    if file_path:
        # interprets the file
        interpret_file(file_path, interpretation, debug)
    else:
        # starts the interactive console
        interactive_console(debug, interpretation)
