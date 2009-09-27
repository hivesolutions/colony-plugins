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

import copy
import types

class ItemSet:
    """
    The item set class
    """

    item_set_id = None
    """ The item set id """

    rules_list = []
    """ The rules list """

    def __init__(self, item_set_id = None):
        """
        Constructor of the class.

        @type item_set_id: int
        @param item_set_id: The item set id.
        """

        self.item_set_id = item_set_id
        self.rules_list = []

    def add_rule(self, rule):
        """
        Adds a rule to the item set.

        @type rule: Rule
        @param rule: The rule to add to the item set.
        """

        self.rules_list.append(rule)

    def remove_rule(self, rule):
        """
        Removes a rule from the item set.

        @type rule: Rule
        @param rule: The rule to remove from the item set.
        """

        self.rules_list.remove(rule)

    def set_item_set_id(self, item_set_id):
        """
        Sets the item set id.

        @type item_set_id: int
        @param item_set_id: The item set id.
        """

        self.item_set_id = item_set_id

    def get_item_set_id(self):
        """
        Retrieves the item set id.

        @rtype: int
        @return: The item set id.
        """

        return self.item_set_id

    def set_rules_list(self, rules_list):
        """
        Sets the rules list.

        @type rules_list: List
        @param rules_list: The rules list.
        """

        self.rules_list = rules_list

    def get_rules_list(self):
        """
        Retrieves the rules list.

        @rtype: List
        @return: The rules list.
        """

        return self.rules_list

class Rule:
    """
    The rule class.
    """

    rule_id = None
    """ The rule id """

    rule_name = "none"
    """ The rule name """

    rule_value = "none"
    """ The rule value """

    symbols_list = []
    """ The symbols list """

    def __init__(self, rule_id = None, rule_name = "none", rule_value = "none"):
        """
        Constructor of the class.

        @type rule_id: int
        @param rule_id: The rule id.
        @type rule_name: String
        @param rule_name: The rule name.
        @type rule_value: String
        @param rule_value: The rule value.
        """

        self.rule_id = rule_id
        self.rule_name = rule_name
        self.rule_value = rule_value

        # sets the symbols list
        self.symbols_list = [symbol.strip() for symbol in self.rule_value.split()]

    def __repr__(self):
        """
        Returns the default representation of the class.

        @rtype: String
        @return: The default representation of the class.
        """

        return "<%i, %s, %s, %s>" % (
            self.rule_id,
            self.rule_name,
            self.rule_value,
            self.symbols_list
        )

    def get_rule_id(self):
        """
        Retrieves the rule id.

        @rtype: int
        @return: The rule id.
        """

        return self.rule_id

    def set_rule_id(self, rule_id):
        """
        Sets the rule id.

        @type rule_id: int
        @param rule_id: The rule id.
        """

        self.rule_id = rule_id

    def get_rule_name(self):
        """
        Retrieves the rule name.

        @rtype: String
        @return: The rule name.
        """

        return self.rule_name

    def set_rule_name(self, rule_name):
        """
        Sets the rule name.

        @type rule_name: String
        @param rule_name: The rule name.
        """

        self.rule_name = rule_name

    def get_rule_value(self):
        """
        Retrieves the rule value.

        @rtype: String
        @return: The rule value.
        """

        return self.rule_value

    def set_rule_value(self, rule_value):
        """
        Sets the rule value.

        @type rule_value: String
        @param rule_value: The rule value.
        """

        self.rule_value = rule_value

    def get_symbols_list(self):
        """
        Retrieves the symbols list.

        @rtype: List
        @return: The symbols list.
        """

        return self.symbols_list

    def set_symbols_list(self, symbols_list):
        """
        Sets the symbols list.

        @type symbols_list: List
        @param symbols_list: The symbols list.
        """

        self.symbols_list = symbols_list

class ParserGenerator:
    """
    The parser generator class.
    """

    PARSER_PREFIX = "p_"
    """ The parser prefix value """

    current_rule_id = 0
    """ The current rule id """

    functions_list = []
    """ The functions list """

    rules_list = []
    """ The rules list """

    rules_map = {}
    """ The rules map """

    rule_id_rule_map = {}
    """ The rule id rule map """

    symbols_map = {}
    """ The symbols map """

    symbols_terminal_map = {}
    """ The symbols terminal map """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.functions_list = []
        self.rules_list = []
        self.rules_map = {}
        self.rule_id_rule_map = {}
        self.symbols_map = {}
        self.symbols_non_terminal_map = {}
        self.symbols_terminal_map = {}

    def construct(self, scope):
        """
        Constructs the parser for the given scope.

        @type scope: Map
        @param scope: The scope to be used in the parser construction.
        """

        # retrieves the local values copy
        locals = copy.copy(scope)

        # iterates over all the locals
        for local in locals:
            # retrieves the local value
            local_value = locals[local]

            # retrieves the local type
            local_type = type(local_value)

            # retrieves the local prefix
            local_prefix = local[0:2]

            # in case the type of the local is function
            if local_type is types.FunctionType and local_prefix == ParserGenerator.PARSER_PREFIX:
                # adds the local value to the functions list
                self.functions_list.append(local_value)

        self.generate_table()

    def get_lexer(self):
        """
        Retrieves the lexer.

        @rtype: Lexer
        @return: The lexer.
        """

        return self.lexer

    def set_lexer(self, lexer):
        """
        Sets the lexer.

        @type lexer: Lexer
        @param lexer: The lexer.
        """

        self.lexer = lexer

    def generate_table(self):
        # generates the structures
        self._generate_structures()

        # generates the table
        self._generate_table()

    def _generate_table(self):
        for symbol in self.symbols_map:
            if not symbol in self.symbols_non_terminal_map:
                self.symbols_terminal_map[symbol] = True

        # sets the current index
        current_index = 0
        current_item_set_id = 0

        item_sets_list = []
        symbol_item_set_map = {}

        # iterates over all the rules in the rules list
        for rule in self.rules_list:
            # retrieves the rule symbols list
            rule_symbols_list = rule.get_symbols_list()

            # retrieves the current symbol
            current_symbol = rule_symbols_list[current_index]

            if len(rule_symbols_list) > current_index + 1:
                # retrieves the next symbol
                next_symbol = rule_symbols_list[current_index + 1]
            # in case it's the final symbol
            else:
                # sets the end symbol
                next_symbol = "$"

            # in case the symbol is not in the symbol item set map
            if current_symbol in symbol_item_set_map:
                # retrieves the item set
                item_set = symbol_item_set_map[current_symbol]
            else:
                # creates a new item set
                item_set = ItemSet(current_item_set_id)

                # sets the item set in the symbol item set map
                symbol_item_set_map[current_symbol] = item_set

                # appends the item set to the item sets list
                item_sets_list.append(item_set)

                # increments the current item set id
                current_item_set_id += 1

            # adds the rule to the item set
            item_set.add_rule(rule)

    def _generate_structures(self):
        """
        Generates the structures.
        """

        # iterates over all the functions in the functions list
        for function in self.functions_list:
            # retrieves the function doc
            function_doc = function.__doc__

            # splits the function doc
            function_doc_splitted = function_doc.split(":")

            # retrieves the rule name
            rule_name = function_doc_splitted[0].strip()

            # retrieves the rule value
            rule_value = function_doc_splitted[1].strip()

            # splits the rule value
            rule_value_splitted = [rule_value_splitted.strip() for rule_value_splitted in rule_value.split("|")]

            # in case the rule name is not defined
            # in the rules map
            if not rule_name in self.rules_map:
                self.rules_map[rule_name] = []

            # iterates over the rule sub values
            for rule_sub_value in rule_value_splitted:
                # creates a new rule
                rule = Rule(self.current_rule_id, rule_name, rule_sub_value)

                # adds the rule to the rules list
                self.rules_list.append(rule)

                # adds the rule to the rule name list
                self.rules_map[rule_name].append(rule)

                # sets the rule in the rule id rule map
                self.rule_id_rule_map[self.current_rule_id] = rule

                # sets the rule name in the non terminal map
                self.symbols_non_terminal_map[rule_name] = True

                # retrieves the symbols list
                symbols_list = [symbol.strip() for symbol in rule_sub_value.split()]

                # iterates over all the symbols in the symbols list
                for symbol in symbols_list:
                    # in case the symbol is not in the symbols map
                    if not symbol in self.symbols_map:
                        # sets the symbol in the symbols map
                        self.symbols_map[symbol] = []

                    # adds the rule to the current symbol
                    # in the symbols map
                    self.symbols_map[symbol].append(rule)

                # increments the current rule id
                self.current_rule_id += 1
