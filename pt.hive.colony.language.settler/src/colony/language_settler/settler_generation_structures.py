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

import new
import array
import opcode
import types

import settler_exceptions

COMPLEX_OPERATIONS = ["LOAD"]
""" The list of complex operations """

MULTIPLE_ADDRESSES_OPERATIONS = ["LOAD", "LOAD_CONST", "STORE_NAME", "STORE_FAST", "STORE_GLOBAL", "STORE_ATTR",
                                 "LOAD_NAME", "LOAD_FAST", "LOAD_ATTR", "LOAD_GLOBAL", "COMPARE_OP", "MAKE_FUNCTION",
                                 "CALL_FUNCTION", "JUMP_IF_FALSE", "JUMP_IF_TRUE", "JUMP_FORWARD", "JUMP_ABSOLUTE",
                                 "SETUP_LOOP", "BUILD_TUPLE", "BUILD_LIST", "IMPORT_NAME"]
""" The list of multiple addresses operations """

STACK_INCREMENTER_OPERATIONS = {
    "LOAD" : 1,
    "LOAD_CONST" : 1,
    "LOAD_NAME" : 1,
    "LOAD_FAST" : 1,
    "LOAD_GLOBAL" : 1
}
""" The list of stack incrementer operations map"""

STACK_DECREMENTER_OPERATIONS = {
    "POP_TOP" : 1,
    "STORE_NAME" : 1,
    "STORE_FAST" : 1,
    "STORE_GLOBAL" : 1,
    "STORE_ATTR" : 1,
    "IMPORT_NAME" : 1,
    "PRINT_ITEM" : 1,
    "BINARY_ADD" : 1,
    "BINARY_SUBTRACT" : 1,
    "BINARY_MULTIPLY" : 1,
    "BINARY_DIVIDE" : 1,
    "BINARY_POWER" : 1,
    "BUILD_CLASS" : 2
}
""" The list of stack decrementer operations map """

class ContextCodeInformation:
    """
    The context code information class.
    """

    global_context_code_information = None
    """ The global context code information """

    arguments_count = 0
    """ The arguments count """

    number_locals = 0
    """ The number of locals """

    stack_size = 100
    """ The stack size """

    flags = 0x0040
    """ The flags """

    constants_list = []
    """ The constants list """

    index_contants_map = {}
    """ The map relating the indexes and the constants """

    constants_index_map = {}
    """ The map relating the constants and the indexes """

    names_list = []
    """ The names list """

    index_names_map = {}
    """ The map relating the index and the names """

    names_index_map = {}
    """ The map relating the names and the indexes """

    variable_names_list = []
    """ The list of variable names """

    index_variable_names_map = {}
    """ The map relating the index and the variable names """

    variable_names_index_map = {}
    """ The map relating the variable names and the indexes """

    global_names_list = []
    """ The global names list """

    file_name = "none"
    """ The file name """

    name = "<module>"
    """ The name of the context """

    first_line_number = 1
    """ The index of the first line number """

    program_counter = 0
    """ The program counter """

    code_object = None
    """ The code object """

    operations_stack = []
    """ The operations stack """

    line_intervals = []
    """ The line intervals """

    current_line_number = 1
    """ The current line number """

    context_type = "none"
    """ The context type """

    meta_information_map = {}
    """ The meta information map """

    current_stack_size = 0
    """ The current stack size """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.constants_list = []
        self.index_contants_map = {}
        self.constants_index_map = {}
        self.names_list = []
        self.index_names_map = {}
        self.names_index_map = {}
        self.variable_names_list = []
        self.index_variable_names_map = {}
        self.variable_names_index_map = {}
        self.global_names_list = []
        self.index_global_names_map = {}
        self.global_names_index_map = {}
        self.operations_stack = []
        self.line_intervals = []
        self.meta_information_map = {}

        self.add_constant(None)

    def set_global_context_code_information(self, global_context_code_information):
        """
        Sets the global context code information.

        @type global_context_code_information: ContextCodeInformation
        @param global_context_code_information: The global context code information.
        """

        self.global_context_code_information = global_context_code_information

    def add_variable(self, variable_name):
        """
        Adds a variable to the list of variables.

        @type variable_name: String
        @param variable_name: The name of the variable to add to the list of variables.
        """

        if variable_name in self.names_list:
            return

        names_list_length = len(self.names_list)
        self.names_list.append(variable_name)
        self.index_names_map[names_list_length] = variable_name
        self.names_index_map[variable_name] = names_list_length

    def remove_variable(self, variable_name):
        """
        Removes a variable from the list of variables.

        @type variable_name: String
        @param variable_name: The name of the variable to remove from the list of variables.
        @rtype: bool
        @return: The result of the removal (if successful or not).
        """

        if not variable_name in self.names_list:
            return False
        if not variable_name in self.names_index_map:
            return False
        index = self.names_index_map[variable_name]
        if not index in self.index_names_map:
            return False
        self.names_list.remove(variable_name)
        del self.names_index_map[variable_name]
        del self.index_names_map[index]
        return True

    def get_variable_offset(self, variable_name):
        """
        Retrieves the offset to the given variable.

        @type variable_name: String
        @param variable_name: The name of the variable to retrieve the offset.
        @rtype: int
        @return: The offset to the given variable.
        """

        if not variable_name in self.names_index_map:
            return None
        return self.names_index_map[variable_name]

    def add_variable_name(self, variable_name):
        """
        Adds a variable name to the list of variable names.

        @type variable_name: String
        @param variable_name: The name of the variable name to add to the list of variable names.
        """

        if variable_name in self.variable_names_list:
            return

        variable_names_list_length = len(self.variable_names_list)
        self.variable_names_list.append(variable_name)
        self.index_variable_names_map[variable_names_list_length] = variable_name
        self.variable_names_index_map[variable_name] = variable_names_list_length

        # increments the number of local variables
        self.number_locals += 1

    def remove_variable_name(self, variable_name):
        """
        Removes a variable name from the list of variable names.

        @type variable_name: String
        @param variable_name: The name of the variable name to remove from the list of variable names.
        @rtype: bool
        @return: The result of the removal (if successful or not).
        """

        if not variable_name in self.variable_names_list:
            return False
        if not variable_name in self.variable_names_index_map:
            return False
        index = self.variable_names_index_map[variable_name]
        if not index in self.index_variable_names_map:
            return False
        self.variable_names_list.remove(variable_name)
        del self.variable_names_index_map[variable_name]
        del self.index_variable_names_map[index]

        # decrements the number of local variables
        self.number_locals -= 1

        return True

    def get_variable_name_offset(self, variable_name):
        """
        Retrieves the offset to the given variable name.

        @type variable_name: String
        @param variable_name: The name of the variable name to retrieve the offset.
        @rtype: int
        @return: The offset to the given variable name.
        """

        if not variable_name in self.variable_names_index_map:
            return None
        return self.variable_names_index_map[variable_name]

    def add_global_name(self, global_name):
        """
        Adds a global name to the list of global names.

        @type global_name: String
        @param global_name: The global name to add to the list of global names.
        """

        self.add_variable(global_name)

        if not global_name in self.global_names_list:
            self.global_names_list.append(global_name)

    def remove_global_name(self, global_name):
        """
        Removes a global name from the list of global names.

        @type global_name: String
        @param global_name: The global name to remove from the list of global names.
        @rtype: bool
        @return: The result of the removal (if successful or not).
        """

        if not self.remove_variable(global_name):
            return False

        if not global_name in self.global_names_list:
            return False

        self.global_names_list.remove(global_name)

    def add_constant(self, value):
        """
        Adds a constant to the list of constants.

        @type value: Object
        @param value: The constant value to add to the list of constants.
        """

        if value in self.constants_list:
            return

        constants_list_length = len(self.constants_list)
        self.constants_list.append(value)
        self.index_contants_map[constants_list_length] = value
        self.constants_index_map[value] = constants_list_length

    def remove_constant(self, value):
        """
        Removes a constant from the list of constants.

        @type value: Object
        @param value: The constant value to remove from the list of constants.
        @rtype: bool
        @return: The result of the removal (if successful or not).
        """

        if not value in self.constants_list:
            return False
        if not value in self.constants_index_map:
            return False
        index = self.constants_index_map[value]
        if not index in self.index_constants_map:
            return False

        self.constants_list.remove(value)
        del self.constants_index_map[value]
        del self.index_constants_map[index]
        return True

    def get_constant_offset(self, value):
        """
        Retrieves the offset to the given constant.

        @type value: Object
        @param value: The constant value to retrieve the offset.
        @rtype: int
        @return: The offset to the given constant value.
        """

        if not value in self.constants_index_map:
            return None
        return self.constants_index_map[value]

    def add_operation(self, operation, arguments):
        """
        Adds an operation to the list of operations.

        @type operation: String
        @param operation: The name of the operation to be added.
        @type arguments: Tuple
        @param arguments: The arguments of the operation to be added.
        """

        operation_tuple = (operation, arguments)
        self.operations_stack.append(operation_tuple)
        self.increment_program_counter(operation)
        self.update_current_stack_size_add(operation, arguments)

    def remove_operation(self, operation, arguments):
        """
        Removes an operation from the list of operations.

        @type operation: String
        @param operation: The name of the operation to be removed.
        @type arguments: Tuple
        @param arguments: The arguments of the operation to be removed.
        """

        operation_tuple = (operation, arguments)
        self.operations_stack.remove(operation_tuple)
        self.decrement_program_counter(operation)
        self.update_current_stack_size_remove(operation, arguments)

    def increment_line_number(self, line_increment = 1):
        """
        Increments the current line number.

        @type line_increment: int
        @param line_increment: The line increment to be added.
        """

        # create the line delta list
        line_delta = []

        line_delta.append(self.program_counter)
        line_delta.append(line_increment)

        self.line_intervals.append(line_delta)

        self.current_line_number += line_increment

    def get_current_line_number(self):
        """
        Retrieves the current line number.

        @rtype: int
        @return: The current line number.
        """

        return self.current_line_number

    def get_current_program_counter(self):
        """
        Retrieves the current value for the program counter.

        @rtype: int
        @return: The current value for the program counter.
        """

        return self.program_counter

    def increment_program_counter(self, operation):
        """
        Increments the program counter for the given operation.

        @type operation: String
        @param operation: The operation used to calculate the program counter increment.
        """

        if operation in MULTIPLE_ADDRESSES_OPERATIONS:
            self.program_counter += 3
        else:
            self.program_counter += 1

    def decrement_program_counter(self, operation):
        """
        Decrements the program counter for the given operation.

        @type operation: String
        @param operation: The operation used to calculate the program counter decrement.
        """

        if operation in MULTIPLE_ADDRESSES_OPERATIONS:
            self.program_counter -= 3
        else:
            self.program_counter -= 1

    def update_current_stack_size_add(self, operation, arguments):
        """
        Updates the current stack size value for the addition of the given operation and arguments.

        @type operation: String
        @param operation: The operation used to update the current stack size.
        @type operation: Tuple
        @param operation: The arguments used to update the current stack size.
        """

        if operation in STACK_INCREMENTER_OPERATIONS:
            # retrieves the increment value
            increment_value = STACK_INCREMENTER_OPERATIONS[operation]

            # increments the stack size by the given increment value
            self.current_stack_size += increment_value
        elif operation in STACK_DECREMENTER_OPERATIONS:
            # retrieves the decrement value
            decrement_value = STACK_DECREMENTER_OPERATIONS[operation]

            # decrements the stack size by the given decrement value
            self.current_stack_size -= decrement_value
        elif operation == "CALL_FUNCTION":
            # retrieves the number of arguments
            number_of_arguments = arguments[0]

            # decrements the stack size by the given number of arguments
            self.current_stack_size -= number_of_arguments

    def update_current_stack_size_remove(self, operation, arguments):
        """
        Updates the current stack size value for the removal of the given operation and arguments.

        @type operation: String
        @param operation: The operation used to update the current stack size.
        @type operation: Tuple
        @param operation: The arguments used to update the current stack size.
        """

        if operation in STACK_INCREMENTER_OPERATIONS:
            # retrieves the increment value
            increment_value = STACK_INCREMENTER_OPERATIONS[operation]

            # decrements the stack size by the given increment value
            self.current_stack_size -= increment_value
        elif operation in STACK_DECREMENTER_OPERATIONS:
            # retrieves the decrement value
            decrement_value = STACK_DECREMENTER_OPERATIONS[operation]

            # increments the stack size by the given decrement value
            self.current_stack_size += decrement_value
        elif operation == "CALL_FUNCTION":
            # retrieves the number of arguments
            number_of_arguments = arguments[0]

            # increments the stack size by the given number of arguments
            self.current_stack_size += number_of_arguments

    def generate_lnotab_string(self):
        """
        Generates the lnotab string.

        @rtype: String
        @return: The generated lnotab string.
        """

        # create the line intervals array
        line_intervals_array = array.array("B")

        for line_intervals_item in self.line_intervals:
            instruction_off_set, line_delta = line_intervals_item
            line_intervals_array.append(instruction_off_set)
            line_intervals_array.append(line_delta)

        # converts the code line intervals array string value
        lnotab_string = line_intervals_array.tostring()

        return lnotab_string

    def generate_code_string(self):
        """
        Generates the code string.

        @rtype: String
        @return: The generated code string.
        """

        # create the code array
        code = array.array("B")

        # iterates over all the operation in the operations stack
        for operation_tuple in self.operations_stack:
            operation, arguments = operation_tuple

            if operation in COMPLEX_OPERATIONS:
                if operation == "LOAD":
                    # retrieves the variable name
                    variable_name = arguments[0]

                    if variable_name in self.names_index_map:
                        if variable_name in self.global_names_list:
                            operation = "LOAD_GLOBAL"
                        else:
                            operation = "LOAD_NAME"
                    elif variable_name in self.variable_names_index_map:
                        operation = "LOAD_FAST"
                    elif variable_name in self.global_context_code_information.names_index_map:
                        self.add_variable(variable_name)
                        operation = "LOAD_GLOBAL"
                    else:
                        raise settler_exceptions.SettlerSymbolNotFound("the symbol '" + variable_name + "' was not found")

            if not operation in opcode.opmap:
                raise settler_exceptions.SettlerInvalidOperation("the operation '" + operation + "' is invalid")

            # retrieves the opcode value
            opcode_value = opcode.opmap[operation]

            # appends the opcode
            code.append(opcode_value)

            # generates the arguments code
            self.generate_code_arguments(code, operation, arguments)

        # converts the code into string value
        code_string = code.tostring()

        return code_string

    def generate_code_arguments(self, code, operation, arguments):
        """
        Generates the code for the given operation and arguments,
        appending the generated code to the the given code array object.

        @type code: Array
        @param code: The code array object used to support the code stream.
        @type operation: String
        @param operation: The operation to be used in the code generation.
        @type operation: String
        @param operation: The arguments to be used in the code generation.
        """

        if not operation in MULTIPLE_ADDRESSES_OPERATIONS:
            return

        if operation == "LOAD_CONST":
            # retrieves the constant value
            constant_value = arguments[0]

            # retrieves the real constant value
            real_constant_value = self.get_value(constant_value)

            # retrieves the constant index
            constant_index = self.constants_index_map[real_constant_value]

            # retrieves the 8 low bits for the constant index
            constant_index_low = constant_index & 0x00FF

            # retrieves the 8 high bits for the constant index
            constant_index_high = (constant_index & 0xFF00) >> 8

            # appends the value
            code.append(constant_index_low)
            code.append(constant_index_high)
        elif operation == "STORE_NAME":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "STORE_FAST":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.variable_names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "STORE_ATTR":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "STORE_GLOBAL":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "LOAD_NAME":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "LOAD_FAST":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.variable_names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "LOAD_ATTR":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "LOAD_GLOBAL":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            # retrieves the variable name index
            variable_index = self.names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)
        elif operation == "COMPARE_OP":
            # retrieves the operation type
            operation_type = arguments[0]

            # retrieves the real operation type
            real_operation_type = self.get_value(operation_type)

            # retrieves the 8 low bits for the real operation type
            real_operation_type_low = real_operation_type & 0x00FF

            # retrieves the 8 high bits for the real operation type
            real_operation_type_high = (real_operation_type & 0xFF00) >> 8

            # appends the value
            code.append(real_operation_type_low)
            code.append(real_operation_type_high)
        elif operation == "MAKE_FUNCTION":
            # retrieves the number of arguments
            number_of_arguments = arguments[0]

            # retrieves the real number of arguments
            real_number_of_arguments = self.get_value(number_of_arguments)

            # retrieves the 8 low bits for the real number of arguments position
            real_number_of_arguments_low = real_number_of_arguments & 0x00FF

            # retrieves the 8 high bits for the real number of arguments position
            real_number_of_arguments_high = (real_number_of_arguments & 0xFF00) >> 8

            # appends the value
            code.append(real_number_of_arguments_low)
            code.append(real_number_of_arguments_high)
        elif operation == "CALL_FUNCTION":
            # retrieves the number of arguments
            number_of_arguments = arguments[0]

            # retrieves the real number of arguments
            real_number_of_arguments = self.get_value(number_of_arguments)

            # retrieves the 8 low bits for the real number of arguments position
            real_number_of_arguments_low = real_number_of_arguments & 0x00FF

            # retrieves the 8 high bits for the real number of arguments position
            real_number_of_arguments_high = (real_number_of_arguments & 0xFF00) >> 8

            # appends the value
            code.append(real_number_of_arguments_low)
            code.append(real_number_of_arguments_high)
        elif operation == "JUMP_IF_FALSE":
            # retrieves the jump position
            jump_position = arguments[0]

            # retrieves the real jump position
            real_jump_position = self.get_value(jump_position)

            # retrieves the 8 low bits for the real jump position
            real_jump_position_low = real_jump_position & 0x00FF

            # retrieves the 8 high bits for the real jump position
            real_jump_position_high = (real_jump_position & 0xFF00) >> 8

            # appends the value
            code.append(real_jump_position_low)
            code.append(real_jump_position_high)
        elif operation == "JUMP_IF_TRUE":
            # retrieves the jump position
            jump_position = arguments[0]

            # retrieves the real jump position
            real_jump_position = self.get_value(jump_position)

            # retrieves the 8 low bits for the real jump position
            real_jump_position_low = real_jump_position & 0x00FF

            # retrieves the 8 high bits for the real jump position
            real_jump_position_high = (real_jump_position & 0xFF00) >> 8

            # appends the value
            code.append(real_jump_position_low)
            code.append(real_jump_position_high)
        elif operation == "JUMP_FORWARD":
            # retrieves the jump position
            jump_position = arguments[0]

            # retrieves the real jump position
            real_jump_position = self.get_value(jump_position)

            # retrieves the 8 low bits for the real jump position
            real_jump_position_low = real_jump_position & 0x00FF

            # retrieves the 8 high bits for the real jump position
            real_jump_position_high = (real_jump_position & 0xFF00) >> 8

            # appends the value
            code.append(real_jump_position_low)
            code.append(real_jump_position_high)
        elif operation == "JUMP_ABSOLUTE":
            # retrieves the jump position
            jump_position = arguments[0]

            # retrieves the real jump position
            real_jump_position = self.get_value(jump_position)

            # retrieves the 8 low bits for the real jump position
            real_jump_position_low = real_jump_position & 0x00FF

            # retrieves the 8 high bits for the real jump position
            real_jump_position_high = (real_jump_position & 0xFF00) >> 8

            # appends the value
            code.append(real_jump_position_low)
            code.append(real_jump_position_high)
        elif operation == "SETUP_LOOP":
            # retrieves the jump position
            jump_position = arguments[0]

            # retrieves the real jump position
            real_jump_position = self.get_value(jump_position)

            # retrieves the 8 low bits for the real jump position
            real_jump_position_low = real_jump_position & 0x00FF

            # retrieves the 8 high bits for the real jump position
            real_jump_position_high = (real_jump_position & 0xFF00) >> 8

            # appends the value
            code.append(real_jump_position_low)
            code.append(real_jump_position_high)
        elif operation == "BUILD_TUPLE":
            # retrieves the number of values
            number_of_values = arguments[0]

            # retrieves the real number of values
            real_number_of_values = self.get_value(number_of_values)

            # retrieves the 8 low bits for the real number of values
            real_number_of_values_low = real_number_of_values & 0x00FF

            # retrieves the 8 high bits for the real number of values
            real_number_of_values_high = (real_number_of_values & 0xFF00) >> 8

            # appends the value
            code.append(real_number_of_values_low)
            code.append(real_number_of_values_high)
        elif operation == "BUILD_LIST":
            # retrieves the number of values
            number_of_values = arguments[0]

            # retrieves the real number of values
            real_number_of_values = self.get_value(number_of_values)

            # retrieves the 8 low bits for the real number of values
            real_number_of_values_low = real_number_of_values & 0x00FF

            # retrieves the 8 high bits for the real number of values
            real_number_of_values_high = (real_number_of_values & 0xFF00) >> 8

            # appends the value
            code.append(real_number_of_values_low)
            code.append(real_number_of_values_high)
        elif operation == "IMPORT_NAME":
            # retrieves the variable name
            variable_name = arguments[0]

            # retrieves the real variable name
            real_variable_name = self.get_value(variable_name)

            if real_variable_name in self.names_index_map:
                # retrieves the variable name index
                variable_index = self.names_index_map[real_variable_name]
            elif real_variable_name in self.variable_names_index_map:
                # retrieves the variable name index
                variable_index = self.variable_names_index_map[real_variable_name]

            # retrieves the 8 low bits for the variable index
            variable_index_low = variable_index & 0x00FF

            # retrieves the 8 high bits for the variable index
            variable_index_high = (variable_index & 0xFF00) >> 8

            # appends the value
            code.append(variable_index_low)
            code.append(variable_index_high)

    def get_value(self, value_object):
        # retrieves the value object type
        value_object_type = type(value_object)

        flag = False

        if value_object_type == types.InstanceType and value_object.__class__ == DeferredValue:
            previous_calculation_value = value_object.calculation_value

        while value_object_type == types.InstanceType and value_object.__class__ == DeferredValue:
            value_object = value_object.value
            flag = True

        if flag:
            value_object -= previous_calculation_value

        return value_object

    def generate_code_object(self):
        """
        Generates the code object for the current generation structure.

        @rtype: Code
        @return: The generated code object.
        """

        # generates the lnotab string
        lnotab_string = self.generate_lnotab_string()

        # generates the code string
        code_string = self.generate_code_string()

        # creates the constants tuple from the constants list
        constants_tuple = tuple(self.constants_list)

        # creates the names tuple from the names list
        names_tuple = tuple(self.names_list)

        # creates the variable names tuple from the variable names list
        variable_names_tuple = tuple(self.variable_names_list)

        # creates the code object
        self.code_object = new.code(self.arguments_count, self.number_locals, self.stack_size, self.flags, code_string, constants_tuple,
                               names_tuple, variable_names_tuple, self.file_name, self.name, self.first_line_number, lnotab_string)

        # returns the code object
        return self.code_object

    def get_operations_stack_memory_size(self, operations_stack = None):
        """
        Retrieves the memory size of the given operations stack.

        @type operations_stack: List
        @param operations_stack: The stack of operation to calculate the memory size.
        @rtype: int
        @return: The memory size of the operations stack.
        """

        # in case operations stack is none
        if operations_stack == None:
            # uses the operations stack in the instance
            operations_stack = self.operations_stack

        # creates the stack memory size
        stack_memory_size = 0

        # iterates over all the operation tuples in the operations stack
        for operation_tuple in operations_stack:
            operation = operation_tuple[0]
            if operation in MULTIPLE_ADDRESSES_OPERATIONS:
                stack_memory_size += 3
            else:
                stack_memory_size += 1

        return stack_memory_size

class DeferredValue:
    """
    The deferred value class.
    """

    value = None
    """ The value """

    calculation_value = 0
    """ The calculation value """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass
