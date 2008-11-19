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

import settler_parser
import settler_visitor
import settler_interpretation
import settler_generation
import settler_processing

BRANDING_TEXT = "Settler 0.1 (Hive Solutions Lda. r1:Sep 19 2006)"
VERSION_PRE_TEXT = "Python "
HELP_TEXT = "Type \"help\", \"copyright\", \"credits\" or \"license\" for more information."

CARRET = "[settler] >> "
BLOCK_CARRET = "[settler] .. "

NEW_BLOCK_CHARACTER = ":"

EXIT_COMMAND = "exit()"

def get_command_from_command_list(command_list):
    command_string = ""

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

def process_command(command, processing_structure, global_interpretation_map, debug = False, verbose = False, code_generation = False,):
    if debug:
        process_command_debug(command, processing_structure, global_interpretation_map, verbose, code_generation)
    else:
        process_command_normal(command, processing_structure, global_interpretation_map, verbose, code_generation)

def process_command_normal(command, processing_structure, global_interpretation_map, verbose, code_generation):
    try:
        interpret_command(command, processing_structure, global_interpretation_map, False, verbose, code_generation)
    except Exception, ex:
        print ex

def process_command_debug(command, processing_structure, global_interpretation_map, verbose, code_generation):
    interpret_command(command, processing_structure, global_interpretation_map, True, verbose, code_generation)

def interpret_command(command, processing_structure, global_interpretation_map, debug, verbose, code_generation):
    # retrieves the parse result
    parse_result = settler_parser.parser.parse(command)

    # retrieves the global context code information
    global_context_code_information = global_interpretation_map["global_context_code_information"]

    if not parse_result == None:
        if debug:
            # creates a default visitor
            default_visitor = settler_visitor.Visitor()

            # accepts the default visitor in post order
            parse_result.accept_post_order(default_visitor)

        # creates a code generation visitor
        code_generation_visitor = settler_generation.PythonCodeGenerationVisitor()

        if code_generation:
            # sets the visit mode as module
            code_generation_visitor.set_visit_mode("module")
        else:
            # sets the visit mode as interactive
            code_generation_visitor.set_visit_mode("interactive")

        # in case there is a global context code information defined
        if global_context_code_information:
            # sets the global context code information variables
            code_generation_visitor.set_global_context_code_information_variables(global_context_code_information)

        # accepts the code generation visitor in post order
        parse_result.accept_post_order(code_generation_visitor)

        if code_generation:
            # creates the output file
            code_generation_visitor.create_output_file()

        if verbose:
            # retrieves the code object
            code_object = code_generation_visitor.get_code_object()

            # retrieves the global context code information
            global_context_code_information = code_generation_visitor.get_global_context_code_information()

            global_interpretation_map["global_context_code_information"] = global_context_code_information

            # evaluates the generated code object
            eval_result_value = eval(code_object, globals(), globals())

            # in case the result of the evaluation is not None
            if not eval_result_value == None:
                # prints the result of the evaluation
                print eval_result_value

        # creates a interpretation visitor
#        interpretation_visitor = settler_interpretation.InterpretationVisitor()
#
#        # sets the default processing structure in the interpretation visitor
#        interpretation_visitor.set_processing_structure(processing_structure)
#
#        # accepts the visitor in post order
#        parse_result.accept_post_order(interpretation_visitor)
#
#        if verbose:
#            # retrieves the parse result value
#            parse_result_value = parse_result.value
#            if not parse_result_value == None:
#                print parse_result_value

def interactive_console(debug = False, verbose = True, code_generation = False):
    # creates the exit flag
    exit_flag = False
    
    # creates a new processing structure
    processing_structure = settler_processing.ProcessingStructure()

    # starts the global interpretation map
    global_interpretation_map = {}

    # sets the global_context_code_information value
    global_interpretation_map["global_context_code_information"] = None

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
                process_command(command, processing_structure, global_interpretation_map, debug, verbose, code_generation)

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
                process_command(string_value + "\n", processing_structure, global_interpretation_map, debug, verbose, code_generation)

def interpret_file(file_path, debug = False, verbose = False, code_generation = True):
    # opens the given file
    file = open(file_path, "r")

    # reads the file contents
    file_contents = file.read()

    # creates a new processing structure
    processing_structure = settler_processing.ProcessingStructure()

    # starts the global interpretation map
    global_interpretation_map = {}

    # sets the global_context_code_information value
    global_interpretation_map["global_context_code_information"] = None

    # processes the command
    process_command(file_contents, processing_structure, global_interpretation_map, debug, verbose, code_generation)

if __name__ == "__main__":
    # starts the verbose flag as false
    verbose = False

    # starts the debug flag as false
    debug = False

    # start the file path value as None
    file_path = None

    # retrieves the argument options
    opts, args = getopt.getopt(sys.argv[1:], "vdf:", ["verbose", "debug", "file="])

    # iterates over all the given options
    for option, value in opts:
        if option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-d", "--debug"):
            debug = True
        elif option in ("-f", "--file"):
            file_path = value

    if file_path:
        # interprets the file
        interpret_file(file_path, debug)
    else:
        # starts the interactive console
        interactive_console(debug)
