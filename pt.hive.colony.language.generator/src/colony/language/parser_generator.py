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

    rule_transition_item_set_map = {}
    """ The rule transition item set map """

    def __init__(self, item_set_id = None):
        """
        Constructor of the class.

        @type item_set_id: int
        @param item_set_id: The item set id.
        """

        self.item_set_id = item_set_id
        self.rules_list = []
        self.rule_transition_item_set_map = {}

    def __eq__(self, item_set):
        """
        Returns if an object is the same as this one.

        @type item_set: ItemSet
        @param item_set: The item set to be compared.
        @rtype: bool
        @return: If the item set is the same as this one.
        """

        # in case the length of the rules lists is the same
        if len(self.rules_list) == len(item_set.rules_list):
            # iterates over all rules, token positions and closures in the rules list
            for rule, token_position, closure in self.rules_list:
                # unsets the valid flag
                valid = False

                # iterates over all the rules and token positions in the item set
                # rules list
                for item_set_rule, item_set_token_position, item_set_closure in item_set.rules_list:
                    # in case the token positions and the rules are the same
                    if token_position == item_set_token_position and rule == item_set_rule:
                        # sets the valid flag
                        valid = True

                        # breaks the cycle
                        break

                # in case the valid flag is not set
                if not valid:
                    # returns false
                    return False

            # returns true
            return True

        # returns false
        return False

    def add_rule(self, rule, token_position, closure = False):
        """
        Adds a rule to the item set.

        @type rule: Rule
        @param rule: The rule to add to the item set.
        @type token_position: int
        @param token_position: The position of the token.
        @type closure: bool
        @param closure: If the rule is added as a closure.
        """

        # iterates over the rules list
        for item_set_rule, item_set_token_position, item_set_closure in self.rules_list:
            # in case the rules are the same
            if rule == item_set_rule:
                return

        # creates the rule position tuple
        rule_position_tuple = (rule, token_position, closure)

        # add the rule position tuple to the rules list
        self.rules_list.append(rule_position_tuple)

    def remove_rule(self, rule, token_position, closure = False):
        """
        Removes a rule from the item set.

        @type rule: Rule
        @param rule: The rule to remove from the item set.
        @type token_position: int
        @param token_position: The position of the token.
        @type closure: bool
        @param closure: If the rule is removed as a closure.
        """

        # creates the rule position tuple
        rule_position_tuple = (rule, token_position, closure)

        # removes the rule position tuple from the rules list
        self.rules_list.remove(rule_position_tuple)

    def get_rule_transition_item_set(self, rule):
        """
        Retrieves the transition item for the given rule.

        @param rule: Rule
        @param rule: The rule to retrieve the transition item set.
        @rtype: ItemSet
        @return: The transition item set for the given rule.
        """

        if not rule in self.rule_transition_item_set_map:
            return None

        return self.rule_transition_item_set_map[rule]

    def set_rule_transition_item_set(self, rule, item_set):
        """
        Sets the transition item set for the given rule.

        @type rule: Rule
        @param rule: The rule to set the transition item set.
        @type item_set: ItemSet
        @param item_set: The transition item set to set in the given rule.
        """

        self.rule_transition_item_set_map[rule] = item_set

    def get_item_set_id(self):
        """
        Retrieves the item set id.

        @rtype: int
        @return: The item set id.
        """

        return self.item_set_id

    def set_item_set_id(self, item_set_id):
        """
        Sets the item set id.

        @type item_set_id: int
        @param item_set_id: The item set id.
        """

        self.item_set_id = item_set_id

    def get_rules_list(self):
        """
        Retrieves the rules list.

        @rtype: List
        @return: The rules list.
        """

        return self.rules_list

    def set_rules_list(self, rules_list):
        """
        Sets the rules list.

        @type rules_list: List
        @param rules_list: The rules list.
        """

        self.rules_list = rules_list

    def get_rule_transition_item_set_map(self):
        """
        Retrieves the rule transition item set map.

        @rtype: Dictionary
        @return: The rule transition item set map.
        """

        return self.rule_transition_item_set_map

    def set_rule_transition_item_set_map(self, rule_transition_item_set_map):
        """
        Sets the rule transition item set map.

        @type rule_transition_item_set_map: List
        @param rule_transition_item_set_map: The rule transition item set map.
        """

        self.rule_transition_item_set_map = rule_transition_item_set_map

    def _get_item_set_string(self):
        """
        Retrieves the item set as a friendly string.

        @rtype: String
        @return: The item set described as a friendly string.
        """

        # start the string value with the item set label
        string_value = "item set " + str(self.item_set_id)

        # iterates over all the rules in the rules list
        for rule, token_position, closure in self.rules_list:
            # adds a new line to string value
            string_value += "\n"

            # in case if of type closure
            if closure:
                # adds a plus sign to the string value
                string_value += "+ "

            string_value += rule._get_rule_string() + " (" + str(token_position) + ")"

        return string_value

class Rule(object):
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

    def __eq__(self, rule):
        """
        Returns if an object is the same as this one.

        @type rule: Rule
        @param rule: The rule to be compared.
        @rtype: bool
        @return: If the rule is the same as this one.
        """

        # in case the rule name and the rule value are the same
        if self.rule_name == rule.rule_name and self.rule_value == rule.rule_value:
            # returns true
            return True
        else:
            # returns false
            return False

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

    def _get_rule_string(self):
        """
        Retrieves the rule as a friendly string.

        @rtype: String
        @return: The rule described as a friendly string.
        """

        return self.rule_name + " -> " + self.rule_value

class ParserGenerator:
    """
    The parser generator class.
    """

    PARSER_PREFIX = "p_"
    """ The parser prefix value """

    PROGRAM_FUNCTION = "p_program"
    """ The parser program function value """

    current_rule_id = 0
    """ The current rule id """

    program_function = None
    """ The program function """

    program_rule = None
    """ The program rule """

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

    symbols_non_terminal_map = {}
    """ The symbols non terminal map """

    symbols_terminal_map = {}
    """ The symbols terminal map """

    item_sets_list = {}
    """ The item sets list """

    transition_table_map = {}
    """ The transition table map """

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
        self.item_sets_list = []
        self.transition_table_map = {}

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

                # in case the local has the program function value
                if local == ParserGenerator.PROGRAM_FUNCTION:
                    # sets the program function
                    self.program_function = local_value

        # generates the table
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
        """
        Generates the parsing table.
        """

        # generates the structures
        self._generate_structures()

        # generates the table
        self._generate_table()

    def _generate_table(self):
        """
        Generates the parsing table (auxiliary method).
        """

        # generates the terminal map
        self._generate_terminal_map()

        # generates the item sets
        self._generate_item_sets()

        # generates the transition table
        self._generate_transition_table()

        # generates the action table
        self._generate_action_table()

    def _generate_terminal_map(self):
        """
        Generates the terminal map.
        """

        # iterates over all the symbols in the symbols map
        for symbol in self.symbols_map:
            # in case the symbol is not present
            # in the non terminal map
            if not symbol in self.symbols_non_terminal_map:
                # adds the symbol to the terminal map
                self.symbols_terminal_map[symbol] = True

    def _generate_item_sets(self):
        """
        Generates the item sets.
        """

        # sets the current index
        current_item_set_id = 0

        # creates the initial current rules list
        current_rules_list = [(self.program_rule, -1)]

        # creates the previous rules map
        previous_rules_map = {}

        # while there are items in the current rules list
        while current_rules_list:
            # creates the next rules list
            next_rules_list = []

            # creates the current item sets list
            current_item_sets_list = []

            # creates the symbol item set map
            symbol_item_set_map = {}

            # iterates over all the rules in the current rules list
            for rule, current_token_position in current_rules_list:
                #creates the extra rules list
                exta_rules_list = []

                # retrieves the rule symbols list
                rule_symbols_list = rule.get_symbols_list()

                # retrieves the current symbol
                current_symbol = "".join(rule_symbols_list[:current_token_position + 1])

                # in case the current token position is not the final one
                if len(rule_symbols_list) > current_token_position + 1:
                    # retrieves the next symbol
                    next_symbol = rule_symbols_list[current_token_position + 1]

                    # in case the next symbol is present
                    # in the non terminals map
                    if next_symbol in self.symbols_non_terminal_map:
                        # retrieves the extra rules for the next symbol
                        exta_rules_list = self._get_extra_rules(next_symbol)

                    # creates the rule tuple
                    rule_tuple = (rule, current_token_position + 1)

                    # adds the rule tuple to the next rules list
                    next_rules_list.append(rule_tuple)

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
                    item_set = ItemSet()

                    # sets the item set in the symbol item set map
                    symbol_item_set_map[current_symbol] = item_set

                    # appends the item set to the current item sets list
                    current_item_sets_list.append(item_set)

                # adds the rule to the item set
                item_set.add_rule(rule, current_token_position)

                # iterates over all the extra rules
                for extra_rule in exta_rules_list:
                    # adds the extra rule to the item set
                    item_set.add_rule(extra_rule, -1, True)

                    # creates the extra rule tuple
                    extra_rule_tuple = (extra_rule, 0)

                    # adds the rule tuple to the next rules list
                    next_rules_list.append(extra_rule_tuple)

            # iterates over all the current item sets
            for current_item_set in current_item_sets_list:
                # in case the current item set is not
                # contained in the item sets list
                if not current_item_set in self.item_sets_list:
                    valid_item_set = current_item_set
                else:
                    for item_set in self.item_sets_list:
                        if current_item_set == item_set:
                            valid_item_set = item_set

                for item_set_rule, item_set_token_position, item_set_closure in valid_item_set.get_rules_list():
                    if item_set_rule in previous_rules_map:
                        # retrieves the previous item sets list
                        # for the given item set rule
                        previous_item_sets_list = previous_rules_map[item_set_rule]

                        # iterates over all the previous item sets
                        for previous_item_set in previous_rules_map[item_set_rule]:
                            # sets the rule sets the transition item set for the rule
                            previous_item_set.set_rule_transition_item_set(item_set_rule, valid_item_set)

            # clear the previous rules map
            previous_rules_map.clear()

            # iterates over all the current item sets
            for current_item_set in current_item_sets_list:
                # in case the current item set is not
                # contained in the item sets list
                if not current_item_set in self.item_sets_list:
                    # sets the item set id in the current item set
                    current_item_set.set_item_set_id(current_item_set_id)

                    # appends the current item set to the item sets list
                    self.item_sets_list.append(current_item_set)

                    # retrieves the current item set rules list
                    current_item_set_rules_list = current_item_set.get_rules_list()

                    # iterates over the current item set rules list
                    for rule, token_position, closure in current_item_set_rules_list:
                        # in case the rule is note defined in the previous rules map
                        if not rule in previous_rules_map:
                            # creates an empty list
                            previous_rules_map[rule] = []

                        # adds the current item set
                        previous_rules_map[rule].append(current_item_set)

                    # increments the current item set id
                    current_item_set_id += 1

            # sets the current rules list as the next rules list
            current_rules_list = next_rules_list

    def _generate_transition_table(self):
        """
        Generates the transition table.
        """

        # retrieves the item sets list length
        item_sets_list_length = len(self.item_sets_list)

        # iterates over the range of the item sets list length
        for item_set_index in range(item_sets_list_length):
            self.transition_table_map[item_set_index] = {}

        # start the index counter
        index = 0

        # iterates over all the item sets
        for item_set in self.item_sets_list:
            # retrieves the item set rules list
            item_set_rules_list = item_set.get_rules_list()

            # iterates over all the item set rules
            for item_set_rule, item_set_token_position, item_set_closure in item_set_rules_list:
                # retrieves the item set rule symbols list
                item_set_rule_symbols_list = item_set_rule.get_symbols_list()

                if len(item_set_rule_symbols_list) > item_set_token_position + 1:
                    # retrieves the item set rule symbol
                    item_set_rule_symbol = item_set_rule_symbols_list[item_set_token_position + 1]
                else:
                    # sets the end symbol
                    item_set_rule_symbol = "$"

                # retrieves the transition item set rule
                rule_transition_item_set = item_set.get_rule_transition_item_set(item_set_rule)

                # in case there is a rule transition item set defined
                if rule_transition_item_set:
                    self.transition_table_map[index][item_set_rule_symbol] = rule_transition_item_set.get_item_set_id()

            # increments the index counter
            index += 1

    def _generate_action_table(self):
        """
        Generates the action table.
        """

        # creates the action table map
        action_table = {}

        # retrieves the item sets list length
        item_sets_list_length = len(self.item_sets_list)

        # iterates over the range of the item sets list length
        for item_set_index in range(item_sets_list_length):
            action_table[item_set_index] = {}

        # iterates over all the non terminal symbols
        for symbol_non_terminal in self.symbols_non_terminal_map:
            action_table
            pass

        # tenho de iterar pela transition table

        # iterates over all the item sets
        for item_set in self.item_sets_list:
            pass

            # tenho os nao terminais aki
            #

        # tenho de gerar a acion

    def _get_extra_rules(self, symbol):
        # retrieves the extra rules for the next symbol
        extra_rules_list = self.rules_map[symbol]

        # iterates over all the extra rules
        # in the extra rules list
        for extra_rule in extra_rules_list:
            # retrieves the symbols list for the extra rule
            extra_rule_symbols_list = extra_rule.get_symbols_list()

            # retrieves the first symbol
            first_symbol = extra_rule_symbols_list[0]

            if first_symbol in self.symbols_non_terminal_map and not first_symbol == symbol:
                # extends the extra rules list
                extra_rules_list.extend(self._get_extra_rules(first_symbol))

        # returns the extra rules list
        return extra_rules_list

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

                # in case the current function is the program function
                if function == self.program_function:
                    # sets the program rule
                    self.program_rule = rule

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

    def _get_item_sets_string(self):
        """
        Retrieves the item sets as a friendly string.

        @rtype: String
        @return: The item sets described as a friendly string.
        """

        # constructs the string value
        string_value = str()

        # iterates over all the item sets in the item sets list
        for item_set in self.item_sets_list:
            # retrieves the item set string
            item_set_string = item_set._get_item_set_string()

            # prints the item set string
            string_value += item_set_string + "\n\n"

        # returns the string value
        return string_value

    def _get_transition_table_string(self):
        """
        Retrieves the transition table as a friendly string.

        @rtype: String
        @return: The transition table described as a friendly string.
        """

        # constructs the string value
        string_value = str()

        # adds some space to the string value
        string_value +=  "  "

        # iterates over all the symbols in the symbols map
        for symbol in self.symbols_map:
            # adds the symbol to the string value
            string_value += symbol + " "

        # adds a new line to the string value
        string_value += "\n"

        # retrieves the transition table map length
        transition_table_map_length = len(self.transition_table_map)

        # iterates over the transitions size
        for index in range(transition_table_map_length):
            # retrieves the symbols map for the transition
            # with the given index
            symbols_map = self.transition_table_map[index]

            # adds the index to the string value
            string_value += str(index) + " "

            # iterates over all the symbols in the symbols map
            for symbol in self.symbols_map:
                # in case the symbol is defined
                if symbol in symbols_map:
                    string_value += str(symbols_map[symbol]) + " "
                else:
                    string_value += "# "

            # adds a new line to the string value
            string_value += "\n"

        # returns the string value
        return string_value
