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

import struct
import time
import marshal
import copy
import string

import settler_ast
import settler_visitor
import settler_generation_structures

MAGIC_NUMBER = 0x0A0DF2B3
""" The python 2.5 magic number (0x0A0D + 0xF2B3) """

DEFAULT_OUTPUT_FILE_NAME = "out.pyc"
""" The default output file name """

MODULE_MODE = "module"
""" The module mode """

INTERACTIVE_MODE = "interactive"
""" The interactive mode """

class PythonCodeGenerationVisitor(settler_visitor.Visitor):
    """
    The python code generation visitor class.
    """

    visit_mode = MODULE_MODE
    """ The visit mode """

    output_file = None
    """ The output file """

    global_context_code_information = None
    """ The global context code information """

    current_context_code_information = None
    """ The current context code information """

    previous_context_code_information = None
    """ The previous context code information """

    context_code_information_stack = []
    """ The context code information stack """

    current_operations_stack = []
    """ The operation stack """

    operations_stacks_stack = []
    """ The operations stacks stack """

    stack_mode_counter = 0
    """ The stack mode counter """

    discard_mode_counter = 0
    """ The discard mode counter """

    boolean_stack = []
    """ The boolean stack """

    not_stack = []
    """ The not stack """

    def __init__(self):
        settler_visitor.Visitor.__init__(self)

        self.context_code_information_stack = []
        self.current_operations_stack = []
        self.operations_stacks_stack = []
        self.boolean_stack = []
        self.not_stack = []

        # creates the global context code information
        self.create_global_context_code_information()

    def create_global_context_code_information(self):
        # creates the global context code information
        self.global_context_code_information = settler_generation_structures.ContextCodeInformation()
        self.global_context_code_information.global_context_code_information = self.global_context_code_information
        self.current_context_code_information = self.global_context_code_information
        self.current_context_code_information.context_type = "module"
        self.previous_context_code_information = None

    def set_visit_mode(self, visit_mode):
        self.visit_mode = visit_mode

    def create_output_file(self, output_file_name = DEFAULT_OUTPUT_FILE_NAME):
        # creates the output file
        output_file = open(output_file_name, "wb")

        # creates the output
        self.create_output(output_file)

        # closes the output file
        output_file.close()

    def create_output(self, output_file):
        # creates the pack for the magic number
        magic_number_pack = struct.pack("L", MAGIC_NUMBER)

        # write the magic number to the output file
        output_file.write(magic_number_pack)

        # retrieves the current timestamp
        timestamp = time.time()

        # creates the pack for the timestamp
        timestamp_pack = struct.pack("L", int(timestamp))

        # write the timestamp to the output file
        output_file.write(timestamp_pack)

        # generates the code object
        code_object = self.global_context_code_information.generate_code_object()

        # marshals the code object into the output file
        marshal.dump(code_object, output_file)

    def get_code_object(self):
        # generates the code object
        code_object = self.global_context_code_information.generate_code_object()

        return code_object

    def get_global_context_code_information(self):
        return self.global_context_code_information

    def set_global_context_code_information_variables(self, global_context_code_information):
        # sets the constants related structures
        self.global_context_code_information.constants_list = global_context_code_information.constants_list
        self.global_context_code_information.index_contants_map = global_context_code_information.index_contants_map
        self.global_context_code_information.constants_index_map = global_context_code_information.constants_index_map

        # sets the names related structures
        self.global_context_code_information.names_list = global_context_code_information.names_list
        self.global_context_code_information.index_names_map = global_context_code_information.index_names_map
        self.global_context_code_information.names_index_map = global_context_code_information.names_index_map

        # sets the variable names related structures
        self.global_context_code_information.variable_names_list = global_context_code_information.variable_names_list
        self.global_context_code_information.index_variable_names_map = global_context_code_information.index_variable_names_map
        self.global_context_code_information.variable_names_index_map = global_context_code_information.variable_names_index_map

        # sets the global names related structures
        self.global_context_code_information.global_names_list = global_context_code_information.global_names_list

    def add_operation(self, operation, arguments, mark_line = False, line_increment = 1):
        if self.discard_mode_counter:
            return

        if self.stack_mode_counter:
            operation_tuple = (
                operation,
                arguments,
                mark_line,
                line_increment
            )

            current_operations_stack = self.operations_stacks_stack[self.stack_mode_counter - 1]
            current_operations_stack.append(operation_tuple)
        else:
            # in case the line is to be marked
            if mark_line:
                self.current_context_code_information.increment_line_number(line_increment)

            self.current_context_code_information.add_operation(operation, arguments)

    def remove_operation(self, operation, arguments, mark_line = False, line_increment = 1):
        if self.stack_mode_counter:
            operation_tuple = (
                operation,
                arguments,
                mark_line,
                line_increment
            )

            current_operations_stack = self.operations_stacks_stack[self.stack_mode_counter - 1]
            current_operations_stack.remove(operation_tuple)
        else:
            self.current_context_code_information.remove_operation(operation, arguments)

    def flush_current_operations_stack(self, inverted = False, clear = True):
        if self.stack_mode_counter > 1:
            previous_operations_stack = self.operations_stacks_stack[self.stack_mode_counter - 2]
            self.flush_current_operations_stack_stack(previous_operations_stack)
            return

        if inverted:
            current_operations_stack_copy = copy.copy(self.current_operations_stack)
            current_operations_stack_copy.reverse()
            # iterates over all the operation tuples in the operations stack copy
            for operation_tuple in current_operations_stack_copy:
                operation, arguments, mark_line, line_increment = operation_tuple

                # in case the line is to be marked
                if mark_line:
                    self.current_context_code_information.increment_line_number(line_increment)

                self.current_context_code_information.add_operation(operation, arguments)
        else:
            # iterates over all the operation tuples in the operations stack
            for operation_tuple in self.current_operations_stack:
                operation, arguments, mark_line, line_increment = operation_tuple

                # in case the line is to be marked
                if mark_line:
                    self.current_context_code_information.increment_line_number(line_increment)

                self.current_context_code_information.add_operation(operation, arguments)

        if clear:
            self.current_operations_stack = []

    def flush_current_operations_stack_stack(self, operation_stack, inverted = False, clear = True):
        if inverted:
            current_operations_stack_copy = copy.copy(self.current_operations_stack)
            current_operations_stack_copy.reverse()
            # iterates over all the operation tuples in the operations stack copy
            for operation_tuple in current_operations_stack_copy:
                operation_stack.append(operation_tuple)
        else:
            # iterates over all the operation tuples in the operations stack
            for operation_tuple in self.current_operations_stack:
                operation_stack.append(operation_tuple)

        if clear:
            self.current_operations_stack = []

    def increment_operations_stack_level(self):
        operations_stack = []
        self.stack_mode_counter += 1
        self.operations_stacks_stack.append(operations_stack)

        self.current_operations_stack = operations_stack

    def increment_operations_stack_level_virtual(self, number_of_levels = 1):
        self.stack_mode_counter += number_of_levels

    def decrement_operations_stack_level(self, inverted = False, clear = True):
        self.flush_current_operations_stack(inverted, clear)
        self.stack_mode_counter -= 1
        self.operations_stacks_stack.pop()

        if self.operations_stacks_stack:
            self.current_operations_stack = self.operations_stacks_stack[-1]
        else:
            self.current_operations_stack = None

    def decrement_operations_stack_level_virtual(self, number_of_levels = 1):
        self.stack_mode_counter -= number_of_levels

    def increment_discard_level(self):
        self.discard_mode_counter += 1

    def decrement_discard_level(self):
        self.discard_mode_counter -= 1

    def mark_next_line(self, line_increment = 1):
        self.current_context_code_information.increment_line_number(line_increment)

    def get_current_line_number(self):
        return self.current_context_code_information.get_current_line_number()

    def get_current_program_counter(self):
        return self.current_context_code_information.get_current_program_counter()

    def pop_current_context_type(self, node):
        if self.get_current_context_type() == "function":
            # retrieves the code object
            code_object = self.current_context_code_information.code_object

            # retrieves the function name
            function_name = self.current_context_code_information.name

            self.context_code_information_stack.pop()
            self.current_context_code_information = self.previous_context_code_information
            if len(self.context_code_information_stack):
                self.previous_context_code_information = self.context_code_information_stack[-1]
            else:
                self.previous_context_code_information = None

            # adds the variable to the current context
            self.add_variable(function_name)

            # adds the operation to the list of operations
            self.add_operation("LOAD_CONST", (code_object,))

            # adds the operation to the list of operations
            self.add_operation("MAKE_FUNCTION", (0,))

            # adds the store operation to the list of operations
            self.add_store_operation((function_name,))
        elif self.get_current_context_type() == "class":
            # retrieves the code object
            code_object = self.current_context_code_information.code_object

            # retrieves the class name
            class_name = self.current_context_code_information.name

            if "extends" in self.current_context_code_information.meta_information_map:
                extends_list = self.current_context_code_information.meta_information_map["extends"]
            else:
                extends_list = []

            self.context_code_information_stack.pop()
            self.current_context_code_information = self.previous_context_code_information
            if len(self.context_code_information_stack):
                self.previous_context_code_information = self.context_code_information_stack[-1]
            else:
                self.previous_context_code_information = None

            # adds the variable to the current context
            self.add_variable(class_name)

            # adds the constant to the current context
            self.add_constant(class_name)

            # adds the constant to the current context
            self.add_constant(())

            # adds the operation to the list of operations
            self.add_operation("LOAD_CONST", (class_name,))

            if extends_list:
                for extends_item in extends_list:
                    # adds the operation to the list of operations
                    self.add_operation("LOAD", (extends_item,))
                # adds the operation to the list of operations
                self.add_operation("BUILD_TUPLE", (len(extends_list),))
            else:
                # adds the operation to the list of operations
                self.add_operation("LOAD_CONST", ((),))

            # adds the operation to the list of operations
            self.add_operation("LOAD_CONST", (code_object,))

            # adds the operation to the list of operations
            self.add_operation("MAKE_FUNCTION", (0,))

            # adds the operation to the list of operations
            self.add_operation("CALL_FUNCTION", (0,))

            # adds the operation to the list of operations
            self.add_operation("BUILD_CLASS", (0,))

            # adds the store operation to the list of operations
            self.add_store_operation((class_name,))
        elif self.get_current_context_type() == "plugin":
            # retrieves the code object
            code_object = self.current_context_code_information.code_object

            # retrieves the plugin name
            plugin_name = self.current_context_code_information.name

            if "extends" in self.current_context_code_information.meta_information_map:
                extends_list = self.current_context_code_information.meta_information_map["extends"]
            else:
                extends_list = []

            self.context_code_information_stack.pop()
            self.current_context_code_information = self.previous_context_code_information
            if len(self.context_code_information_stack):
                self.previous_context_code_information = self.context_code_information_stack[-1]
            else:
                self.previous_context_code_information = None

            # adds the variable to the current context
            self.add_variable(plugin_name)

            # adds the constant to the current context
            self.add_constant(plugin_name)

            # adds the constant to the current context
            self.add_constant(())

            # adds the operation to the list of operations
            self.add_operation("LOAD_CONST", (plugin_name,))

            if extends_list:
                for extends_item in extends_list:
                    # adds the operation to the list of operations
                    self.add_operation("LOAD", (extends_item,))
                # adds the operation to the list of operations
                self.add_operation("BUILD_TUPLE", (len(extends_list),))
            else:
                # adds the operation to the list of operations
                self.add_operation("LOAD", ("colony",))

                # adds the variable to the current context
                self.add_variable("plugins")

                # adds the operation to the list of operations
                self.add_operation("LOAD_ATTR", ("plugins",))

                # adds the variable to the current context
                self.add_variable("plugin_system")

                # adds the operation to the list of operations
                self.add_operation("LOAD_ATTR", ("plugin_system",))

                # adds the variable to the current context
                self.add_variable("Plugin")

                # adds the operation to the list of operations
                self.add_operation("LOAD_ATTR", ("Plugin",))

                # adds the operation to the list of operations
                self.add_operation("BUILD_TUPLE", (1,))

            # adds the operation to the list of operations
            self.add_operation("LOAD_CONST", (code_object,))

            # adds the operation to the list of operations
            self.add_operation("MAKE_FUNCTION", (0,))

            # adds the operation to the list of operations
            self.add_operation("CALL_FUNCTION", (0,))

            # adds the operation to the list of operations
            self.add_operation("BUILD_CLASS", (0,))

            # adds the store operation to the list of operations
            self.add_store_operation((plugin_name,))

        settler_visitor.Visitor.pop_current_context_type(self, node)

    def push_current_context_type(self, context_type, node):
        settler_visitor.Visitor.push_current_context_type(self, context_type, node)
        if context_type == "function":
            self.context_code_information_stack.append(self.current_context_code_information)
            self.previous_context_code_information = self.current_context_code_information
            self.current_context_code_information = settler_generation_structures.ContextCodeInformation()
            self.current_context_code_information.global_context_code_information = self.global_context_code_information
            self.current_context_code_information.context_type = "function"

            # in case the previous context is of type class and the function
            # is not of type static adds the self variable
            if self.previous_context_code_information.context_type == "class":
                # retrieves the previous function arguments node
                previous_function_arguments_node = node.function_arguments_node

                # creates a new arguments node
                arguments_node = settler_ast.ArgumentsNode()

                # sets the next node as the previous function arguments node
                arguments_node.next_node = previous_function_arguments_node

                # creates the new argument node
                argument_node = settler_ast.ArgumentNode()

                # sets the name for the argument node
                argument_node.set_name("self")

                # sets the argument node in the arguments node
                arguments_node.set_argument_node(argument_node)

                # removes the previous function arguments node as child node
                node.remove_child_node(previous_function_arguments_node)

                # sets the new function arguments node in the node
                node.set_function_arguments_node(arguments_node)
        elif context_type == "function_call":
            self.increment_operations_stack_level()
            self.visit_childs = False
        elif context_type == "if_condition":
            self.visit_childs = False
        elif context_type == "while":
            self.visit_childs = False
        elif context_type == "boolean_expression":
            self.visit_childs = False
        elif context_type == "class":
            self.context_code_information_stack.append(self.current_context_code_information)
            self.previous_context_code_information = self.current_context_code_information
            self.current_context_code_information = settler_generation_structures.ContextCodeInformation()
            self.current_context_code_information.global_context_code_information = self.global_context_code_information
            self.current_context_code_information.context_type = "class"
        elif context_type == "plugin":
            self.context_code_information_stack.append(self.current_context_code_information)
            self.previous_context_code_information = self.current_context_code_information
            self.current_context_code_information = settler_generation_structures.ContextCodeInformation()
            self.current_context_code_information.global_context_code_information = self.global_context_code_information
            self.current_context_code_information.context_type = "class"
        elif context_type == "assign":
            self.visit_childs = False

    def get_current_operations_stack_memory_size(self):
        return self.current_context_code_information.get_operations_stack_memory_size(self.current_operations_stack)

    def get_previous_operations_stack_memory_size(self):
        previous_operations_stack = self.operations_stacks_stack[-2]
        return self.current_context_code_information.get_operations_stack_memory_size(previous_operations_stack)

    def pop_boolean_stack_value(self):
        return self.boolean_stack.pop()

    def push_boolean_stack_value(self, boolean_value_tuple):
        self.boolean_stack.append(boolean_value_tuple)

    def peek_boolean_stack_value(self):
        return self.boolean_stack[-1]

    def is_empty_boolean_stack_value(self):
        # retrieves the boolean stack length
        boolean_stack_length = len(self.boolean_stack)

        if boolean_stack_length:
            return False
        else:
            return True

    def get_last_sequence_node(self, sequence_node):
        # retrieves the next sequence node
        next_sequence_node = sequence_node.next_node

        while not next_sequence_node == None:
            sequence_node = next_sequence_node
            next_sequence_node = sequence_node.next_node

        return sequence_node

    def is_global_context(self):
        """
        Retrieves if the current context is global or not.

        @rtype: bool
        @return: The result of the global context test.
        """

        if self.current_context_code_information == self.global_context_code_information:
            return True
        else:
            return False

    def add_name(self, variable_name):
        self.current_context_code_information.add_variable(variable_name)

    def add_variable(self, variable_name):
        if self.is_global_context() or self.current_context_code_information.context_type == "class":
            self.current_context_code_information.add_variable(variable_name)
        else:
            self.current_context_code_information.add_variable_name(variable_name)

    def add_global(self, global_name):
        self.current_context_code_information.add_global_name(global_name)

    def add_constant(self, value):
        self.current_context_code_information.add_constant(value)

    def add_store_operation(self, arguments, mark_line = False, line_increment = 1):
        # retrieves the variable name
        variable_name = arguments[0]

        if variable_name in self.current_context_code_information.global_names_list:
            # adds the operation to the list of operations
            self.add_operation("STORE_GLOBAL", arguments, mark_line, line_increment)
        elif self.is_global_context() or self.current_context_code_information.context_type == "class":
            # adds the operation to the list of operations
            self.add_operation("STORE_NAME", arguments, mark_line, line_increment)
        else:
            # adds the operation to the list of operations
            self.add_operation("STORE_FAST", arguments, mark_line, line_increment)

    def get_current_stack_size(self):
        return self.current_context_code_information.current_stack_size

    @settler_visitor._visit(settler_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.RootNode)
    def visit_root_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ProgramNode)
    def visit_program_node(self, node):
        # in case the visit mode is of type module
        if self.visit_mode == MODULE_MODE:
            # adds the operation to the list of operations
            self.add_operation("LOAD_CONST", (None,))

            # adds the operation to the list of operations
            self.add_operation("RETURN_VALUE", ())
        else:
            # retrieves the current stack size
            current_stack_size = self.get_current_stack_size()

            print("stack size: " + str(current_stack_size))

            # in case the current stack is empty
            if not current_stack_size:
                # adds the operation to the list of operations
                self.add_operation("LOAD_CONST", (None,))
            # adds the operation to the list of operations
            self.add_operation("RETURN_VALUE", ())

    @settler_visitor._visit(settler_ast.StatementsNode)
    def visit_statements_node(self, node):
        # retrieves the statement node
        statement_node = node.statement_node

        # retrieves the statement node class
        statement_node_class = statement_node.__class__

        if statement_node_class == settler_ast.FunctionCallNode and not statement_node.function_name_reference_node.name_reference == "print":
            # adds the operation to the list of operations
            self.add_operation("POP_TOP", ())

    @settler_visitor._visit(settler_ast.PassNode)
    def visit_pass_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.AssignNode)
    def visit_assign_node(self, node):
        # retrieves the name reference node
        name_reference_node = node.name_reference_node

        # retrieves the expression node
        expression_node = node.expression_node

        # accepts the expression node in post order
        expression_node.accept_post_order(self)

        # sets the first visit flag as true
        first_visit = True

        # iterates over all the name reference nodes
        for name_reference_node_item in name_reference_node:
            # retrieves the name reference
            name_reference = name_reference_node_item.name_reference

            # in case it's the the last name reference node
            if name_reference_node_item.next_node == None:
                if first_visit:
                    # adds the variable to the current context
                    self.add_variable(name_reference)

                    # adds the store operation to the list of operations
                    self.add_store_operation((name_reference,))
                else:
                    # adds the name to the current context
                    self.add_name(name_reference)

                    # adds the operation to the list of operations
                    self.add_operation("STORE_ATTR", (name_reference,))
            else:
                if first_visit:
                    # adds the operation to the list of operations
                    self.add_operation("LOAD", (name_reference,))
                else:
                    # adds the name to the current context
                    self.add_name(name_reference)

                    # adds the operation to the list of operations
                    self.add_operation("LOAD_ATTR", (name_reference,))

            # sets the first visit flag as false
            first_visit = False

    @settler_visitor._visit(settler_ast.ReturnNode)
    def visit_return_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("RETURN_VALUE", ())

    @settler_visitor._visit(settler_ast.GlobalNode)
    def visit_global_node(self, node):
        # retrieves the name
        name = node.name

        # adds the global name to the current context
        self.add_global(name)

    @settler_visitor._visit(settler_ast.IfConditionNode)
    def visit_if_condition_node(self, node):
        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the statements node
        statements_node = node.statements_node

        # retrieves the else condition node
        else_condition_node = node.else_condition_node

        # accepts the expression node in post order
        expression_node.accept_post_order(self)

        # increments the operations stack level
        self.increment_operations_stack_level()

        # adds the operation to the list of operations
        self.add_operation("POP_TOP", ())

        # accepts the statements node in post order
        statements_node.accept_post_order(self)

        # retrieves the stack memory size
        stack_memory_size = self.get_current_operations_stack_memory_size()

        if else_condition_node.is_valid():
            # increments the operations stack level
            self.increment_operations_stack_level()

            else_condition_node.accept(self)

            # retrieves the stack memory size
            else_stack_memory_size = self.get_current_operations_stack_memory_size()

            # decrements the operations stack level (virtual)
            self.decrement_operations_stack_level_virtual()

            # adds the operation to the list of operations
            self.add_operation("JUMP_FORWARD", (else_stack_memory_size,))

            # increments the operations stack level (virtual)
            self.increment_operations_stack_level_virtual()

            # retrieves the previous stack memory size
            stack_memory_size = self.get_previous_operations_stack_memory_size()

            # decrements the operations stack level
            self.decrement_operations_stack_level(False, True)

        # decrements the operations stack level (virtual)
        self.decrement_operations_stack_level_virtual()

        # adds the operation to the list of operations
        self.add_operation("JUMP_IF_FALSE", (stack_memory_size,))

        # increments the operations stack level (virtual)
        self.increment_operations_stack_level_virtual()

        # decrements the operations stack level
        self.decrement_operations_stack_level(False, True)

    @settler_visitor._visit(settler_ast.ElseConditionNode)
    def visit_else_condition_node(self, node):
        # retrieves the statements node
        statements_node = node.statements_node

        # adds the operation to the list of operations
        self.add_operation("POP_TOP", ())

        # accepts the statements node in post order
        statements_node.accept_post_order(self)

        # sets the visit childs flag as false, disabling the visit on child nodes
        self.visit_childs = False

        # sets the visit next flag as false, disabling the visit on next nodes
        self.visit_next = False

    @settler_visitor._visit(settler_ast.ElseIfConditionNode)
    def visit_else_if_condition_node(self, node):
        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the statements node
        statements_node = node.statements_node

        # retrieves the next else condition node
        next_else_condition_node = node.next_node

        # adds the operation to the list of operations
        self.add_operation("POP_TOP", ())

        # accepts the expression node in post order
        expression_node.accept_post_order(self)

        # increments the operations stack level
        self.increment_operations_stack_level()

        # adds the operation to the list of operations
        self.add_operation("POP_TOP", ())

        # accepts the statements node in post order
        statements_node.accept_post_order(self)

        # retrieves the stack memory size
        stack_memory_size = self.get_current_operations_stack_memory_size()

        if next_else_condition_node.is_valid():
            # increments the operations stack level
            self.increment_operations_stack_level()

            next_else_condition_node.accept(self)

            # retrieves the stack memory size
            else_stack_memory_size = self.get_current_operations_stack_memory_size()

            # decrements the operations stack level (virtual)
            self.decrement_operations_stack_level_virtual()

            # adds the operation to the list of operations
            self.add_operation("JUMP_FORWARD", (else_stack_memory_size,))

            # increments the operations stack level (virtual)
            self.increment_operations_stack_level_virtual()

            # retrieves the previous stack memory size
            stack_memory_size = self.get_previous_operations_stack_memory_size()

            # decrements the operations stack level
            self.decrement_operations_stack_level(False, True)

        # decrements the operations stack level (virtual)
        self.decrement_operations_stack_level_virtual()

        # adds the operation to the list of operations
        self.add_operation("JUMP_IF_FALSE", (stack_memory_size,))

        # increments the operations stack level (virtual)
        self.increment_operations_stack_level_virtual()

        # decrements the operations stack level
        self.decrement_operations_stack_level(False, True)

        # sets the visit childs flag as false, disabling the visit on child nodes
        self.visit_childs = False

        # sets the visit next flag as false, disabling the visit on next nodes
        self.visit_next = False

    @settler_visitor._visit(settler_ast.WhileNode)
    def visit_while_node(self, node):
        # retrieves the expression node
        expression_node = node.expression_node

        # retrieves the statements node
        statements_node = node.statements_node

        # retrieves the current program counter
        current_program_counter = self.get_current_program_counter()

        # increments the operations stack level
        self.increment_operations_stack_level()

        # accepts the expression node in post order
        expression_node.accept_post_order(self)

        # increments the operations stack level
        self.increment_operations_stack_level()

        # adds the operation to the list of operations
        self.add_operation("POP_TOP", ())

        # accepts the statements node in post order
        statements_node.accept_post_order(self)

        # calculates the program counter value after the setup loop operation
        program_counter_after_setup_loop = current_program_counter + 3

        # adds the operation to the list of operations
        self.add_operation("JUMP_ABSOLUTE", (program_counter_after_setup_loop,))

        # retrieves the stack memory size
        stack_memory_size = self.get_current_operations_stack_memory_size()

        # decrements the operations stack level (virtual)
        self.decrement_operations_stack_level_virtual()

        # adds the operation to the list of operations
        self.add_operation("JUMP_IF_FALSE", (stack_memory_size,))

        # increments the operations stack level (virtual)
        self.increment_operations_stack_level_virtual()

        # decrements the operations stack level
        self.decrement_operations_stack_level(False, True)

        # adds the operation to the list of operations
        self.add_operation("POP_TOP", ())

        # adds the operation to the list of operations
        self.add_operation("POP_BLOCK", ())

        # retrieves the complete stack memory size
        complete_stack_memory_size = self.get_current_operations_stack_memory_size()

        # decrements the operations stack level (virtual)
        self.decrement_operations_stack_level_virtual()

        # adds the operation to the list of operations
        self.add_operation("SETUP_LOOP", (complete_stack_memory_size,))

        # increments the operations stack level (virtual)
        self.increment_operations_stack_level_virtual()

        # decrements the operations stack level
        self.decrement_operations_stack_level(False, True)

    @settler_visitor._visit(settler_ast.ForNode)
    def visit_for_node_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ExpressionNode)
    def visit_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.NumberExpressionNode)
    def visit_number_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.IntegerExpressionNode)
    def visit_integer_expression_node(self, node):
        # retrieves the integer value
        integer_value = node.integer_value

        # adds the constant to the current context
        self.add_constant(integer_value)

        # adds the operation to the list of operations
        self.add_operation("LOAD_CONST", (integer_value,))

    @settler_visitor._visit(settler_ast.StringExpressionNode)
    def visit_string_expression_node(self, node):
        # retrieves the string value
        string_value = node.string_value

        # adds the constant to the current context
        self.add_constant(string_value)

        # adds the operation to the list of operations
        self.add_operation("LOAD_CONST", (string_value,))

    @settler_visitor._visit(settler_ast.BoolExpressionNode)
    def visit_bool_expression_node(self, node):
        # retrieves the bool value
        bool_value = node.bool_value

        # retrieves the real bool value
        real_bool_balue = str(bool_value)

        # adds the variable to the current context
        self.add_variable(real_bool_balue)

        # adds the operation to the list of operations
        self.add_operation("LOAD_NAME", (real_bool_balue,))

    @settler_visitor._visit(settler_ast.NameExpressionNode)
    def visit_name_expression_node(self, node):
        # retrieves the name reference node
        name_reference_node = node.name_reference_node

        # sets the first visit flag as true
        first_visit = True

        # iterates over all the name reference nodes
        for name_reference_node_item in name_reference_node:
            # retrieves the name reference
            name_reference = name_reference_node_item.name_reference

            if first_visit:
                # adds the operation to the list of operations
                self.add_operation("LOAD", (name_reference,))
            else:
                # adds the name to the current context
                self.add_name(name_reference)

                # adds the operation to the list of operations
                self.add_operation("LOAD_ATTR", (name_reference,))

            # sets the first visit flag as false
            first_visit = False

    @settler_visitor._visit(settler_ast.ListExpressionNode)
    def visit_list_expression_node(self, node):
        # retrieves the list contents node
        list_contents_node = node.list_contents_node

        # retrieves the list contents node length
        list_contents_node_length = list_contents_node.count()

        # adds the operation to the list of operations
        self.add_operation("BUILD_LIST", (list_contents_node_length,))

    @settler_visitor._visit(settler_ast.ListContentsNode)
    def visit_list_contents_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.UnaryExpressionNode)
    def visit_unary_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.BinaryExpressionNode)
    def visit_binary_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ArithmethicExpressionNode)
    def visit_arithmethic_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.SummationExpressionNode)
    def visit_summation_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("BINARY_ADD", ())

    @settler_visitor._visit(settler_ast.SubtractionExpressionNode)
    def visit_subtraction_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("BINARY_SUBTRACT", ())

    @settler_visitor._visit(settler_ast.MultiplicationExpressionNode)
    def visit_multiplication_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("BINARY_MULTIPLY", ())

    @settler_visitor._visit(settler_ast.DivisionExpressionNode)
    def visit_division_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("BINARY_DIVIDE", ())

    @settler_visitor._visit(settler_ast.PowerExpressionNode)
    def visit_power_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("BINARY_POWER", ())

    @settler_visitor._visit(settler_ast.BooleanExpressionNode)
    def visit_boolean_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.EqualExpressionNode)
    def visit_equal_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("COMPARE_OP", (2,))

    @settler_visitor._visit(settler_ast.GreaterExpressionNode)
    def visit_greater_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("COMPARE_OP", (4,))

    @settler_visitor._visit(settler_ast.GreaterEqualExpressionNode)
    def visit_greater_equal_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("COMPARE_OP", (5,))

    @settler_visitor._visit(settler_ast.AndExpressionNode)
    def visit_and_expression_node(self, node):
        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # creates the success deferred value
        success_deferred_value = settler_generation_structures.DeferredValue()

        # creates the failure deferred value
        failure_deferred_value = settler_generation_structures.DeferredValue()

        # creates the deferred tuple
        deferred_tuple = (
            success_deferred_value,
            failure_deferred_value
        )

        self.push_boolean_stack_value(deferred_tuple)

        # increments the operations stack level
        self.increment_operations_stack_level()

        # accepts the first expression node in post order
        first_expression_node.accept_post_order(self)

        # retrieves the first expression node stack memory size
        first_expression_node_stack_memory_size = self.get_current_operations_stack_memory_size()

        # decrements the operations stack level
        self.decrement_operations_stack_level(False, True)

        self.pop_boolean_stack_value()

        # increments the operations stack level
        self.increment_operations_stack_level()

        # accepts the second expression node in post order
        second_expression_node.accept_post_order(self)

        # retrieves the second expression node stack memory size
        second_expression_node_stack_memory_size = self.get_current_operations_stack_memory_size()

        # calculates the total expression node stack memory size
        total_expression_node_stack_memory_size = first_expression_node_stack_memory_size + second_expression_node_stack_memory_size

        if self.is_empty_boolean_stack_value():
            # decrements the operations stack level (virtual)
            self.decrement_operations_stack_level_virtual()

            # adds the operation to the list of operations
            self.add_operation("JUMP_IF_FALSE", (second_expression_node_stack_memory_size,))

            # increments the operations stack level (virtual)
            self.increment_operations_stack_level_virtual()

            success_deferred_value.value = first_expression_node_stack_memory_size
            success_deferred_value.calculation_value = 1
            failure_deferred_value.value = total_expression_node_stack_memory_size
            failure_deferred_value.calculation_value = 1
        else:
            deferred_tuple = self.peek_boolean_stack_value()
            _next_success_deferred_value, next_failure_deferred_value = deferred_tuple

            # decrements the operations stack level (virtual)
            self.decrement_operations_stack_level_virtual()

            # adds the operation to the list of operations
            self.add_operation("JUMP_IF_FALSE", (failure_deferred_value,))

            # increments the operations stack level (virtual)
            self.increment_operations_stack_level_virtual()

            success_deferred_value.value = first_expression_node_stack_memory_size
            success_deferred_value.calculation_value = first_expression_node_stack_memory_size
            failure_deferred_value.value = next_failure_deferred_value
            failure_deferred_value.calculation_value = first_expression_node_stack_memory_size

        self.decrement_operations_stack_level(False, True)

    @settler_visitor._visit(settler_ast.OrExpressionNode)
    def visit_or_expression_node(self, node):
        # retrieves the first expression node
        first_expression_node = node.first_expression_node

        # retrieves the second expression node
        second_expression_node = node.second_expression_node

        # creates the success deferred value
        success_deferred_value = settler_generation_structures.DeferredValue()

        # creates the failure deferred value
        failure_deferred_value = settler_generation_structures.DeferredValue()

        # creates the deferred tuple
        deferred_tuple = (
            success_deferred_value,
            failure_deferred_value
        )

        self.push_boolean_stack_value(deferred_tuple)

        # increments the operations stack level
        self.increment_operations_stack_level()

        # accepts the first expression node in post order
        first_expression_node.accept_post_order(self)

        # retrieves the first expression node stack memory size
        first_expression_node_stack_memory_size = self.get_current_operations_stack_memory_size()

        # decrements the operations stack level
        self.decrement_operations_stack_level(False, True)

        self.pop_boolean_stack_value()

        # increments the operations stack level
        self.increment_operations_stack_level()

        # accepts the second expression node in post order
        second_expression_node.accept_post_order(self)

        # retrieves the second expression node stack memory size
        second_expression_node_stack_memory_size = self.get_current_operations_stack_memory_size()

        # calculates the total expression node stack memory size
        total_expression_node_stack_memory_size = first_expression_node_stack_memory_size + second_expression_node_stack_memory_size

        if self.is_empty_boolean_stack_value():
            # decrements the operations stack level (virtual)
            self.decrement_operations_stack_level_virtual()

            # adds the operation to the list of operations
            self.add_operation("JUMP_IF_TRUE", (second_expression_node_stack_memory_size,))

            # increments the operations stack level (virtual)
            self.increment_operations_stack_level_virtual()

            success_deferred_value.value = total_expression_node_stack_memory_size
            success_deferred_value.calculation_value = 1
            failure_deferred_value.value = first_expression_node_stack_memory_size
            failure_deferred_value.calculation_value = 1
        else:
            deferred_tuple = self.peek_boolean_stack_value()
            next_success_deferred_value, _next_failure_deferred_value = deferred_tuple

            # decrements the operations stack level (virtual)
            self.decrement_operations_stack_level_virtual()

            # adds the operation to the list of operations
            self.add_operation("JUMP_IF_TRUE", (success_deferred_value,))

            # increments the operations stack level (virtual)
            self.increment_operations_stack_level_virtual()

            success_deferred_value.value = next_success_deferred_value
            success_deferred_value.calculation_value = first_expression_node_stack_memory_size
            failure_deferred_value.value = first_expression_node_stack_memory_size
            failure_deferred_value.calculation_value = first_expression_node_stack_memory_size

        self.decrement_operations_stack_level(False, True)

    @settler_visitor._visit(settler_ast.NotExpressionNode)
    def visit_not_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("UNARY_NOT", ())

    @settler_visitor._visit(settler_ast.ParenthesisExpressionNode)
    def visit_parenthesis_expression_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.NegativeExpressionNode)
    def visit_negative_expression_node(self, node):
        # adds the operation to the list of operations
        self.add_operation("UNARY_NEGATIVE", ())

    @settler_visitor._visit(settler_ast.NameReferenceNode)
    def visit_name_reference_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ImportNode)
    def visit_import_node(self, node):
        # retrieves the import name reference node
        import_name_reference_node = node.import_name_reference_node

        # retrieves the full qualified import name
        import_name = import_name_reference_node.to_name()

        # retrieves the first name reference
        first_name_reference = import_name_reference_node.name_reference

        # adds the variable to the current context
        self.add_variable(import_name)

        # adds the variable to the current context
        self.add_variable(first_name_reference)

        # adds the constant to the current context
        self.add_constant(-1)

        # adds the operation to the list of operations
        self.add_operation("LOAD_CONST", (-1,))

        # adds the operation to the list of operations
        self.add_operation("LOAD_CONST", (None,))

        # adds the operation to the list of operations
        self.add_operation("IMPORT_NAME", (import_name,))

        # adds the store operation to the list of operations
        self.add_store_operation((first_name_reference,))

    @settler_visitor._visit(settler_ast.FunctionNode)
    def visit_function_node(self, node):
        # retrieves the function name
        function_name = node.function_name

        # retrieves the function arguments node
        function_arguments_node = node.function_arguments_node

        if function_arguments_node.is_valid():
            # retrieves the number of argument values
            number_function_arguments = function_arguments_node.count()
        else:
            number_function_arguments = 0

        # sets the current context code information name
        self.current_context_code_information.name = function_name

        # sets the current context code information arguments count
        self.current_context_code_information.arguments_count = number_function_arguments

        # sets the current context code information flags
        self.current_context_code_information.flags = 0x0043

        # adds the operation to the list of operations
        self.add_operation("LOAD_CONST", (None,))

        # adds the operation to the list of operations
        self.add_operation("RETURN_VALUE", ())

        # adds the constant to the previous context code information
        self.previous_context_code_information.add_constant(self.current_context_code_information.generate_code_object())

    @settler_visitor._visit(settler_ast.ArgumentsNode)
    def visit_arguments_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ArgumentNode)
    def visit_argument_node(self, node):
        # retrieves the name
        name = node.name

        # adds the variable to the current context
        self.add_variable(name)

    @settler_visitor._visit(settler_ast.DefaultValueArgumentNode)
    def visit_default_argument_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.FunctionCallNode)
    def visit_function_call_node(self, node):
        # retrieves the function name reference node
        function_name_reference_node = node.function_name_reference_node

        # retrieves the function argument values node
        function_argument_values_node = node.function_argument_values_node

        # retrieves the first name reference
        first_name_reference = function_name_reference_node.name_reference

        # retrieves the name reference length
        name_reference_length = function_name_reference_node.count()

        # in case the node is valid
        if function_argument_values_node.is_valid():
            # retrieves the number of argument values
            number_function_arguments = function_argument_values_node.count()
        else:
            number_function_arguments = 0

        # accepts the function argument values node in post order
        function_argument_values_node.accept_post_order(self)

        # retrieves the python builtins module
        python_builtins = globals()["__builtins__"]

        self.decrement_operations_stack_level_virtual()

        if first_name_reference == "print" and name_reference_length == 1:
            self.increment_operations_stack_level_virtual()
            self.decrement_operations_stack_level(False, True)

            # adds the operation to the list of operations
            self.add_operation("PRINT_ITEM", ())

            # adds the operation to the list of operations
            self.add_operation("PRINT_NEWLINE", ())
        else:
            if first_name_reference in python_builtins and name_reference_length == 1:
                # adds the variable to the current context
                self.add_variable(first_name_reference)

            # sets the first visit flag as true
            first_visit = True

            # determines if the function call is of type complex
            if function_name_reference_node.count() > 1:
                is_complex = True
            else:
                is_complex = False

            # iterates over all the name reference nodes
            for name_reference_node_item in function_name_reference_node:
                # retrieves the name reference
                name_reference = name_reference_node_item.name_reference

                if first_visit:
                    if is_complex and name_reference[0] in string.ascii_uppercase:
                        # adds the operation to the list of operations
                        self.add_operation("LOAD", (name_reference,))
                        # adds the operation to the list of operations
                        self.add_operation("CALL_FUNCTION", (0,))
                    else:
                        # adds the operation to the list of operations
                        self.add_operation("LOAD", (name_reference,))
                else:
                    # adds the variable to the current context
                    self.add_variable(name_reference)

                    # adds the operation to the list of operations
                    self.add_operation("LOAD_ATTR", (name_reference,))

                # sets the first visit flag as false
                first_visit = False

            self.increment_operations_stack_level_virtual()
            self.decrement_operations_stack_level(False, True)

            # adds the operation to the list of operations
            self.add_operation("CALL_FUNCTION", (number_function_arguments,))

    @settler_visitor._visit(settler_ast.ArgumentValuesNode)
    def visit_argument_values_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ArgumentValueNode)
    def visit_argument_value_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ClassNode)
    def visit_class_node(self, node):
        # retrieves the class name
        class_name = node.class_name

        # sets the current context code information name
        self.current_context_code_information.name = class_name

        # sets the current context code information flags
        self.current_context_code_information.flags = 0x0042

        # adds the operation to the list of operations
        self.add_operation("LOAD_LOCALS", ())

        # adds the operation to the list of operations
        self.add_operation("RETURN_VALUE", ())

        # adds the constant to the previous context code information
        self.previous_context_code_information.add_constant(self.current_context_code_information.generate_code_object())

    @settler_visitor._visit(settler_ast.ExtendsNode)
    def visit_extends_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ExtendsValuesNode)
    def visit_extends_values_node(self, node):
        # retrieves the extends values name
        extends_values_name = node.extends_values_name

        if not "extends" in self.current_context_code_information.meta_information_map:
            self.current_context_code_information.meta_information_map["extends"] = []

        self.current_context_code_information.meta_information_map["extends"].append(extends_values_name)

    @settler_visitor._visit(settler_ast.ImplementsNode)
    def visit_implements_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.ImplementsValuesNode)
    def visit_implements_values_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.InterfaceNode)
    def visit_interface_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.PluginNode)
    def visit_plugin_node(self, node):
        # retrieves the plugin name
        plugin_name = node.plugin_name

        # sets the current context code information name
        self.current_context_code_information.name = plugin_name

        # sets the current context code information flags
        self.current_context_code_information.flags = 0x0042

        # adds the operation to the list of operations
        self.add_operation("LOAD_LOCALS", ())

        # adds the operation to the list of operations
        self.add_operation("RETURN_VALUE", ())

        # adds the constant to the previous context code information
        self.previous_context_code_information.add_constant(self.current_context_code_information.generate_code_object())

    @settler_visitor._visit(settler_ast.AllowsNode)
    def visit_allows_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.AllowsValuesNode)
    def visit_allows_values_node(self, node):
        pass

    @settler_visitor._visit(settler_ast.CapabilityNode)
    def visit_capability_node(self, node):
        pass
