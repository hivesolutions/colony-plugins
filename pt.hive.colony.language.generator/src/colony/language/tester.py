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

import lexer_generator
import parser_generator

import examples.bug_example
import examples.extra_example
import examples.look_ahead_example
import examples.reduce_reduce_example
import examples.shift_reduce_example
import examples.simple_example
import examples.ultra_simple_example

import examples.settler.settler_example
import examples.settler.settler_generation
import examples.settler.settler_interpretation
import examples.settler.settler_processing
import examples.settler.settler_visitor

# sets the current valid example
valid_example = examples.settler.settler_example.example

# creates a new lexer generator
lexer_generator = lexer_generator.LexerGenerator()

# creates a new parser generator
parser_generator = parser_generator.ParserGenerator(parser_generator.ParserGenerator.LR0_PARSER_TYPE)

# sets the lexer in the parser
parser_generator.set_lexer(lexer_generator)

import time

initial = time.time()

# constructs the parser
parser_generator._construct(valid_example)

# prints the rules string
rules_string = parser_generator._get_rules_string()

rules_file = open("rules.txt", "wb+")

rules_file.write(rules_string)

# prints the item sets string
item_sets_string = parser_generator._get_item_sets_string()

item_sets_file = open("item_sets.txt", "wb+")

item_sets_file.write(item_sets_string)

item_sets_file.close()

code = "function tobias():\n\
print(\"ola\") \n\
end\n\
a = 5\n\
while a > 0:\n\
    tobias()\n\
    a = a - 1\n\
end\n"

#ficheiro = open("files/bytecode_test.st", "r")
#code = ficheiro.read()
#ficheiro.close()

# sets the buffer in the parser generator
#parser_generator.set_buffer("import tobias \n if 1 : \n while 1 : \n pass \n end \n else : \n pass \n end \n")

# parses the current buffer and retrieves the result
parse_result = parser_generator.parse(code)

global_interpretation_map = {}
global_context_code_information = None

# creates a code generation visitor
code_generation_visitor = examples.settler.settler_generation.PythonCodeGenerationVisitor()

# sets the visit mode as interactive
code_generation_visitor.set_visit_mode("interactive")

# in case there is a global context code information defined
if global_context_code_information:
    # sets the global context code information variables
    code_generation_visitor.set_global_context_code_information_variables(global_context_code_information)

# accepts the code generation visitor in post order
parse_result.accept_post_order(code_generation_visitor)

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

final_time = time.time()

print str(final_time - initial)
