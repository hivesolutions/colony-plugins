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

import settler_query_exceptions

GLOBAL_CONTEXT_NAME = "global"

class ProcessingStructure:

    symbols_table = {
        GLOBAL_CONTEXT_NAME : {}
    }

    current_context_stack = [GLOBAL_CONTEXT_NAME]

    current_id = 0

    def __init__(self):
        # sets the symbols table
        self.symbols_table = {
            GLOBAL_CONTEXT_NAME : {}
        }

        # sets the current context stack
        self.current_context_stack = [
            GLOBAL_CONTEXT_NAME
        ]

        # sets the current id
        self.current_id = 0

    def set_symbol_value(self, context, name, value):
        if not context in self.symbols_table:
            self.symbols_table[context] = {}

        # retrieves the context symbols table
        context_symbols_table = self.symbols_table[context]

        # sets the value for the symbol in the symbols table of the context
        context_symbols_table[name] = value

    def get_symbol_value(self, context, name):
        if not context in self.symbols_table:
            raise settler_query_exceptions.SettlerQuerySymbolNotFound("symbol " + name + " not found in context " + context)

        # retrieves the context symbols table
        context_symbols_table = self.symbols_table[context]

        if not name in context_symbols_table:
            raise settler_query_exceptions.SettlerQuerySymbolNotFound("symbol " + name + " not found in context " + context)

        # retrieves the symbol value
        value = context_symbols_table[name]

        return value

    def set_symbol_value_current_context(self, name, value):
        # retrieves the current context
        current_context = self.get_current_context()

        self.set_symbol_value(current_context, name, value)

    def get_symbol_value_current_context(self, name):
        try:
            # retrieves the current context
            current_context = self.get_current_context()

            return self.get_symbol_value(current_context, name)
        except settler_query_exceptions.SettlerQuerySymbolNotFound:
            pass

        return self.get_symbol_value(GLOBAL_CONTEXT_NAME, name)

    def get_current_context(self):
        return self.current_context_stack[-1]

    def get_current_context_stack(self):
        return self.current_context_stack

    def pop_current_context(self):
        self.current_context_stack.pop()

    def pop_current_context_local(self):
        # retrieves the current context
        current_context = self.get_current_context()

        self.current_context_stack.pop()
        if current_context in self.symbols_table:
            del self.symbols_table[current_context]

    def push_current_context(self, context):
        self.current_context_stack.append(context)

    def push_current_context_local(self, context):
        _real_context = context + ":" + str(self.current_id)
        self.current_id += 1
        self.current_context_stack.append(context)
