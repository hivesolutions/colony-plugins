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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

QUERY_INTERPRETER_ADAPTER_TYPE = "exact"
""" The query interpreter adapter type """

QUERY_INTERPRETER_ADAPTER_PRIORITY = 80
""" The query interpreter adapter type """

EXACT_REGULAR_EXPRESSION = "\"[^\"]*\""
""" The exact regular expression """

class SearchQueryInterpreterExactAdapter:
    """
    The search query interpreter exact adapter class.
    """

    search_query_interpreter_exact_adapter_plugin = None
    """ The search query interpreter exact adapter plugin """

    def __init__(self, search_query_interpreter_exact_adapter_plugin):
        """
        Constructor of the class.
        
        @type search_query_interpreter_exact_adapter_plugin: SearchQueryInterpreterExactAdapterPlugin
        @param search_query_interpreter_exact_adapter_plugin: The search query interpreter exact adapter plugin.
        """

        self.search_query_interpreter_exact_adapter_plugin = search_query_interpreter_exact_adapter_plugin

    def get_type(self):
        return QUERY_INTERPRETER_ADAPTER_TYPE

    def get_priority(self):
        return QUERY_INTERPRETER_ADAPTER_PRIORITY

    def get_lexme(self, value):
        compiled_and_regular_expression = re.compile(EXACT_REGULAR_EXPRESSION)

        match = compiled_and_regular_expression.match(value)

        if match:
            return ("EXACT", match)

    def interpret_query(self, query_string):
        compiled_and_regular_expression = re.compile(AND_REGULAR_EXPRESSION)

        split_result = compiled_and_regular_expression.split(query_string, 1)

        if not len(split_result) == 2:
            return

        first_operand, second_operand = split_result

        first_operand_striped = first_operand.strip()

        second_operand_striped = second_operand.strip()

        return (QUERY_INTERPRETER_ADAPTER_TYPE, (first_operand_striped, second_operand_striped))
