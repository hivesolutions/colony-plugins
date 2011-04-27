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

import os
import sys
import copy
import types
import logging
import hashlib
import cStringIO

import lexer_generator
import logging_configuration
import parser_generator_exceptions

# setups the logger
logging_configuration.setup_logging()

class ItemSet(object):
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
            for rule, token_position, _closure in self.rules_list:
                # unsets the valid flag
                valid = False

                # iterates over all the rules and token positions in the item set
                # rules list
                for item_set_rule, item_set_token_position, _item_set_closure in item_set.rules_list:
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
        for item_set_rule, item_set_token_position, _item_set_closure in self.rules_list:
            # in case the rules and the token position are the same
            if rule == item_set_rule and token_position == item_set_token_position:
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

    def get_rule_transition_item_set(self, rule, token_position):
        """
        Retrieves the transition item for the given rule.

        @param rule: Rule
        @param rule: The rule to retrieve the transition item set.
        @type token_position: int
        @param token_position: The token position to retrieve the transition item set.
        @rtype: ItemSet
        @return: The transition item set for the given rule and token position.
        """

        if not rule in self.rule_transition_item_set_map:
            return None

        if not token_position in self.rule_transition_item_set_map[rule]:
            return None

        return self.rule_transition_item_set_map[rule][token_position]

    def set_rule_transition_item_set(self, rule, token_position, item_set):
        """
        Sets the transition item set for the given rule.

        @type rule: Rule
        @param rule: The rule to set the transition item set.
        @type token_position: int
        @param token_position: The token position to set in the transition item set.
        @type item_set: ItemSet
        @param item_set: The transition item set to set in the given rule.
        """

        if not rule in self.rule_transition_item_set_map:
            self.rule_transition_item_set_map[rule] = {}

        self.rule_transition_item_set_map[rule][token_position] = item_set

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

class LookAheadItemSet(ItemSet):
    """
    The look ahead item set class.
    """

    base_rule_map = {}
    """ The base rule map """

    def __init__(self, item_set_id = None):
        """
        Constructor of the class.

        @type item_set_id: int
        @param item_set_id: The item set id.
        """

        ItemSet.__init__(self, item_set_id)

        self.base_rule_map = {}

    def add_rule(self, rule, token_position, closure = False):
        # retrieves the rule base rule
        rule_base_rule = rule.get_rule()

        # creates the base rule tuple
        base_rule_tuple = (rule_base_rule, token_position)

        # in case the base rule tuple exists in the base rule map
        if base_rule_tuple in self.base_rule_map:
            # retrieves the item set rule and item set token position
            item_set_rule, _item_set_token_position = self.base_rule_map[base_rule_tuple]

            # retrieves the rule ahead symbols list
            rule_ahead_symbols_list = rule.get_ahead_symbols_list()

            # iterates over the rule ahead symbols list
            for rule_ahead_symbol in rule_ahead_symbols_list:
                # adds the ahead symbol to the item set rule
                item_set_rule.add_ahead_symbol(rule_ahead_symbol)

            # returns immediately
            return

        # creates the rule tuple
        rule_tuple = (rule, token_position)

        # sets the rule tuple in the base rule map
        self.base_rule_map[base_rule_tuple] = rule_tuple

        # calls the super
        ItemSet.add_rule(self, rule, token_position, closure)

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

    rule_string = None
    """ The rule string value """

    rule_string_hash = None
    """ The rule string hash value """

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

    def __hash__(self):
        """
        Retrieves the hash value for the instance.

        @rtype: int
        @return: The hash value for the instance.
        """

        if not self.rule_string_hash:
            self.rule_string_hash = self._get_rule_string().__hash__()

        return self.rule_string_hash

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

        if not self.rule_string:
            self.rule_string = self.rule_name + " -> " + self.rule_value

        return self.rule_string

class LookAheadRule(Rule):
    """
    The look ahead rule class.
    """

    rule = None
    """ The base rule """

    ahead_symbols_list = []
    """ The ahead symbols list """

    ahead_symbols_map = {}
    """ The ahead symbols map """

    def __init__(self, rule = None, ahead_symbols_list = []):
        """
        Constructor of the class.

        @type rule: Rule
        @param rule: The rule to be used in the look ahead rule construction.
        """

        # in case the rule is defined
        if rule:
            # retrieves the rule id
            rule_id = rule.get_rule_id()

            # retrieves the rule name
            rule_name = rule.get_rule_name()

            # retrieves the rule_value
            rule_value = rule.get_rule_value()

            Rule.__init__(self, rule_id, rule_name, rule_value)

            self.rule = rule
        else:
            Rule.__init__(self)

        self.ahead_symbols_map = {}

        self.set_ahead_symbols_list(ahead_symbols_list)

    def __repr__(self):
        return "<%i, %s, %s, %s, %s>" % (
            self.rule_id,
            self.rule_name,
            self.rule_value,
            self.symbols_list,
            self.ahead_symbols_list
        )

    def __eq__(self, rule):
        # in case the base comparator is invalid
        if not Rule.__eq__(self, rule):
            # returns false immediately
            return False

        # retrieves the length of the ahead symbols list
        ahead_symbols_list_length = len(self.ahead_symbols_list)

        # retrieves the rule ahead symbols list
        rule_ahead_symbols_list = rule.get_ahead_symbols_list()

        # retrieves the length of the rule ahead symbols list
        rule_ahead_symbols_list_length = len(rule_ahead_symbols_list)

        # in case the length of both symbols list is not the same
        if not ahead_symbols_list_length == rule_ahead_symbols_list_length:
            # returns false
            return False

        # iterates over the indexes of the ahead symbols
        # list length
        for index in range(ahead_symbols_list_length):
            # retrieves the ahead symbol
            ahead_symbol = self.ahead_symbols_list[index]

            # retrieves the rule ahead symbol
            rule_ahead_symbol = rule_ahead_symbols_list[index]

            # in case the ahead symbol is not equal
            # to the rule ahead symbol
            if not ahead_symbol == rule_ahead_symbol:
                # returns false
                return False

        # return true
        return True

    def add_ahead_symbol(self, ahead_symbol):
        """
        Adds an ahead symbol to the ahead symbols list.

        @type ahead_symbol: String
        @param ahead_symbol: The ahead symbol to be added.
        """

        if not ahead_symbol in self.ahead_symbols_map:
            self.ahead_symbols_list.append(ahead_symbol)
            self.ahead_symbols_map[ahead_symbol] = True

    def remove_ahead_symbol(self, ahead_symbol):
        """
        Removes an ahead symbol from the ahead symbols list.

        @type ahead_symbol: String
        @param ahead_symbol: The ahead symbol to be removed.
        """

        if ahead_symbol in self.ahead_symbols_list:
            self.ahead_symbols_list.remove(ahead_symbol)

    def get_rule(self):
        """
        Retrieves the base rule.

        @rtype: Rule
        @return: The base rule.
        """

        return self.rule

    def set_rule(self, rule):
        """
        Sets the base rule.

        @type rule: Rule
        @param rule: The base rule
        """

        self.rule = rule

    def get_ahead_symbols_list(self):
        """
        Retrieves the ahead symbols list.

        @rtype: List
        @return: The ahead symbols list.
        """

        return self.ahead_symbols_list

    def set_ahead_symbols_list(self, ahead_symbols_list):
        """
        Sets the ahead symbols list.

        @type ahead_symbols_list: List
        @param ahead_symbols_list: The ahead symbols list.
        """

        if ahead_symbols_list:
            self.ahead_symbols_list = ahead_symbols_list
        else:
            self.ahead_symbols_list = ["$"]

        for ahead_symbol in ahead_symbols_list:
            self.ahead_symbols_map[ahead_symbol] = True

    def _get_rule_string(self):
        # retrieves the base rule string
        base_rule_string = Rule._get_rule_string(self)

        # adds a comma to the base rule string
        base_rule_string += ", "

        # sets the is first flag
        is_first = True

        # iterates over all the ahead symbols
        for ahead_symbol in self.ahead_symbols_list:
            # in case is the first item
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the slash to the base rule string
                base_rule_string += "/"

            # appends the ahead symbol to the base rule string
            base_rule_string += ahead_symbol

        # returns the base rule string
        return base_rule_string

class ParserGenerator:
    """
    The parser generator class.
    """

    LR0_PARSER_TYPE = "LR0"
    """ The LR(0) parser type value """

    LR1_PARSER_TYPE = "LR1"
    """ The LR(1) parser type value """

    LALR_PARSER_TYPE = "LALR"
    """ The LALR parser type value """

    DEFAULT_PARSER_TYPE = "LR0"
    """ The default parser type """

    DEFAULT_VALIDATION = False
    """ The default validation """

    DEFAULT_DATA_FILE_NAME = "parser.dat"
    """ The default data file name """

    PARSER_PREFIX = "p_"
    """ The parser prefix value """

    PROGRAM_VALUE = "program"
    """ The parser program value """

    PROGRAM_FUNCTION = "p_program"
    """ The parser program function value """

    ERROR_FUNCTION = "p_error"
    """ The parser error function value """

    SHIFT_OPERATION_VALUE = "S"
    """ The shift operation value """

    REDUCE_OPERATION_VALUE = "R"
    """ The reduce operation value """

    ACCEPT_OPERATION_VALUE = "A"
    """ The accept operation value """

    ACTION_TABLE_VALUE = "action"
    """ The action table value """

    GOTO_TABLE_VALUE = "goto"
    """ The goto table value """

    HASH_VALUE = "hash"
    """ The hash value """

    IGNORE_TOKENS_MAP = {
        "comment" : True,
        "ignore" : True
    }
    """ The ignore tokens list """

    parser_type = None
    """ The parser type """

    current_rule_id = 0
    """ The current rule id """

    lexer = None
    """ The lexer value """

    buffer = "none"
    """ The buffer value """

    program_function = None
    """ The program function """

    error_function = None
    """ The error function """

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

    rule_function_map = {}
    """ The rule function map """

    symbols_map = {}
    """ The symbols map """

    symbols_non_terminal_map = {}
    """ The symbols non terminal map """

    symbols_terminal_map = {}
    """ The symbols terminal map """

    symbols_terminal_end_map = {}
    """ The symbols terminal end map """

    item_sets_list = {}
    """ The item sets list """

    rules_item_sets_map = {}
    """ The rules item sets map """

    transition_table_map = {}
    """ The transition table map """

    action_table_map = {}
    """ The action table map """

    goto_table_map = {}
    """ The goto table map """

    def __init__(self, parser_type = None, create_lexer = False, scope = None, validation = None):
        """
        Constructor of the class.

        @type parser_type: String
        @param parser_type: The parser type to be constructed.
        @type create_lexer: bool
        @param create_lexer: Defines if a lexer should be created.
        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        @type validation: bool
        @param validation: Defines if the lexer tokens should be validated.
        """

        if not parser_type:
            parser_type = ParserGenerator.DEFAULT_PARSER_TYPE

        if not validation:
            validation = ParserGenerator.DEFAULT_VALIDATION

        self.parser_type = parser_type
        self.validation = validation

        self.functions_list = []
        self.rules_list = []
        self.rules_map = {}
        self.rule_id_rule_map = {}
        self.rule_function_map = {}
        self.symbols_map = {}
        self.symbols_non_terminal_map = {}
        self.symbols_terminal_map = {}
        self.symbols_terminal_end_map = {}
        self.item_sets_list = []
        self.rules_item_sets_map = {}
        self.transition_table_map = {}
        self.action_table_map = {}
        self.goto_table_map = {}

        self.symbols_terminal_end_map["$"] = True

        if create_lexer:
            self.lexer = lexer_generator.LexerGenerator()

        if scope:
            self.construct(scope)

    def construct(self, scope, file_path = None, save_state = True):
        """
        Constructs the parser structures for the given scope.

        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        @type file_path: String
        @param file_path: The file path to be used in restore.
        @type save_state: bool
        @param save_state: The save state flag.
        """

        # in case the file path is not defined
        if not file_path:
            # sets the default data file name as the file path
            file_path = ParserGenerator.DEFAULT_DATA_FILE_NAME

        # in case the file path exists
        if os.path.exists(file_path):
            # opens the file
            file = open(file_path, "rb+")

            # constructs or restores the parser generator state
            self.construct_restore(scope, file, False)

            # closes the file
            file.close()

            # opens the file
            file = open(file_path, "wb")

            # in case the save state flag is active
            # and the file is valid
            if save_state and file:
                # saves the state to the file
                self._save_state(file)

            # closes the file
            file.close()
        else:
            # prints the info message
            logging.info("State file %s does not exists" % file_path)

            # constructs the parser generator and saves state
            self._construct_save_file_path(scope, True, file_path, save_state)

    def construct_restore(self, scope, file = None, save_state = True):
        """
        Constructs or restores the parser state from file if possible.

        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        @type file: File
        @param file: The file to be used in the parser state restore.
        @rtype: bool
        @return: If the parser state was successfully restored.
        @type save_state: bool
        @param save_state: The save state flag.
        """

        # in case the file is not defined
        if not file:
            # constructs the parser generator and saves state
            self._construct_save(scope, True, file, save_state)

            # returns immediately
            return

        # in case the restore was not successful
        if self.restore(scope, file):
            # prints the info message
            logging.info("Previous state restored")
        else:
            # print the info message
            logging.info("Previous state not restored (invalid)")

            # resets the internal structures
            self._reset_structures()

            # constructs the parser generator and saves state
            self._construct_save(scope, True, file, save_state)

    def restore(self, scope, file):
        """
        Restores the parser state from file if possible.

        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        @type file: File
        @param file: The file to be used in the parser state restore.
        @rtype: bool
        @return: If the parser state was successfully restored.
        """

        # unserializes the previous state and retrieves the previous hash value
        old_hash_value = self._unserialize_state(file)

        # constructs the parser generator for the given scope
        self._construct(scope, False)

        # retrieves the hash value
        hash_value = self._create_hash()

        # in case the has values are the same
        if old_hash_value == hash_value:
            # returns true
            return True
        else:
            # returns false
            return False

    def parse(self, buffer):
        """
        Parses the given buffer buffer.

        @type buffer: String
        @param buffer: The buffer to be parsed.
        @rtype: Object
        @return: The parse result object.
        """

        # sets the buffer
        self.set_buffer(buffer)

        # parses the current buffer
        return self._parse()

    def get_parser_type(self):
        """
        Retrieves the parser type.

        @rtype: String
        @return: The parser type.
        """

        return self.parser_type

    def set_parser_type(self, parser_type):
        """
        Sets the parser type.

        @type parser_type: String
        @param parser_type: The parser type.
        """

        self.parser_type = parser_type

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

    def get_buffer(self):
        """
        Retrieves the buffer.

        @rtype: String
        @return: The buffer.
        """

        return self.buffer

    def set_buffer(self, buffer):
        """
        Sets the buffer.

        @type buffer: String
        @param buffer: The buffer.
        """

        # in case there is a lexer defined
        if self.lexer:
            # sets the current buffer in the lexer
            self.lexer.set_buffer(buffer)

        self.buffer = buffer

    def is_look_ahead_parser(self):
        # in case the parser is of type LR(1) or LALR
        if self.parser_type == ParserGenerator.LR1_PARSER_TYPE or self.parser_type == ParserGenerator.LALR_PARSER_TYPE:
            return True
        else:
            return False

    def _construct_save_file_path(self, scope, generate_table = True, file_path = None, save_state = True):
        """
        Constructs the parser structures for the given scope, and saves the state.

        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        @type generate_table: bool
        @param generate_table: The generate table flag.
        @type file_path: String
        @param file_path: The file path of the file to be used in the state saving.
        @type save_state: bool
        @param save_state: The save state flag.
        """

        # opens the file
        file = open(file_path, "wb+")

        self._construct_save(scope, generate_table, file, save_state)

        # closes the file
        file.close()

    def _construct_save(self, scope, generate_table = True, file = None, save_state = True):
        """
        Constructs the parser structures for the given scope, and saves the state.

        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        @type generate_table: bool
        @param generate_table: The generate table flag.
        @type file: File
        @param file: The file to be used in the state saving.
        @type save_state: bool
        @param save_state: The save state flag.
        """

        # constructs the parser generator
        self._construct(scope, generate_table)

        # in case the save state flag is active
        # and the file is valid
        if save_state and file:
            # saves the state
            self._save_state(file)

    def _save_state(self, file):
        """
        Saves the state of the parser generator in the given file.

        @type file: File
        @param file: The file to the save the state of the parser generator.
        """

        # serializes the state
        self._serialize_state(file)

    def _construct(self, scope, generate_table = True):
        """
        Constructs the parser structures for the given scope.

        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        @type generate_table: bool
        @param generate_table: The generate table flag.
        """

        # constructs the structures
        self._construct_structures(scope)

        # generates the structures
        self._generate_structures()

        # in case we should generate table
        if generate_table:
            # generates the table
            self._generate_table()

    def _construct_structures(self, scope):
        """
        Constructs the parser structures for the given scope.

        @type scope: Dictionary
        @param scope: The scope to be used in the parser construction.
        """

        # in case the lexer is defined
        if self.lexer:
            # constructs the lexer
            self.lexer.construct(scope)

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
                # in case the local has the error function value
                if local == ParserGenerator.ERROR_FUNCTION:
                    # sets the error function
                    self.error_function = local_value
                else:
                    # adds the local value to the functions list
                    self.functions_list.append(local_value)

                    # in case the local has the program function value
                    if local == ParserGenerator.PROGRAM_FUNCTION:
                        # sets the program function
                        self.program_function = local_value

    def _generate_table(self):
        """
        Generates the parsing table.
        """

        # generates the terminal map
        self._generate_terminal_map()

        # generates the item sets
        self._generate_item_sets()

        # generates the transition table
        self._generate_transition_table()

        # generates the action table
        self._generate_action_table()

        # generates the goto table
        self._generate_goto_table()

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

                # adds the symbol to the terminal end map
                self.symbols_terminal_end_map[symbol] = True

    def _generate_item_sets(self):
        """
        Generates the item sets.
        """

        # sets the current index
        current_item_set_id = 0

        # in case it's a look ahead parser
        if self.is_look_ahead_parser():
            self.program_rule = LookAheadRule(self.program_rule)

        # creates the initial current rules list
        current_rules_list = [(self.program_rule, -1, None)]

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

            # creates the symbol item set previous map
            symbol_item_set_previous_map = {}

            # iterates over all the rules in the current rules list
            for rule, current_token_position, previous_item_set in current_rules_list:
                #creates the extra rules list
                exta_rules_list = []

                # retrieves the rule symbols list
                rule_symbols_list = rule.get_symbols_list()

                # retrieves the rule symbols list length
                rule_symbols_list_length = len(rule_symbols_list)

                # retrieves the current symbol
                current_symbol = "".join(rule_symbols_list[:current_token_position + 1])

                # creates the identifier of the state
                state_identifier = (current_symbol, previous_item_set)

                # creates the previous identifier of the state
                state_previous_identifier = None

                # in case the current position has a valid previous token
                if current_token_position > -1:
                    # retrieves the previous symbol
                    previous_symbol = rule_symbols_list[current_token_position]

                    # in case the previous symbol is a non terminal
                    if previous_symbol in self.symbols_non_terminal_map:
                        # creates the state previous identifier
                        state_previous_identifier = (previous_symbol, previous_item_set)

                # in case the current token position is not the final one
                if rule_symbols_list_length > current_token_position + 1:
                    # retrieves the next symbol
                    next_symbol = rule_symbols_list[current_token_position + 1]

                    # in case the next symbol is present
                    # in the non terminals map
                    if next_symbol in self.symbols_non_terminal_map:
                        # in case it's a look ahead parser
                        if self.is_look_ahead_parser():
                            if rule_symbols_list_length > current_token_position + 2:
                                # retrieves the ahead symbol
                                ahead_symbol = rule_symbols_list[current_token_position + 2]
                            else:
                                # sets the ahead symbols as invalid
                                ahead_symbol = None

                            # retrieves the ahead symbols list
                            rule_ahead_symbols_list = rule.get_ahead_symbols_list()

                            if rule_ahead_symbols_list == ["$"]:
                                rule_ahead_symbols_list = None

                            # retrieves the extra rules for the next symbol
                            exta_rules_list = self._get_extra_rules_ahead(next_symbol, ahead_symbol, rule_ahead_symbols_list)
                        else:
                            # retrieves the extra rules for the next symbol
                            exta_rules_list = self._get_extra_rules(next_symbol)

                # in case it's the final symbol
                else:
                    # sets the end symbol
                    next_symbol = "$"

                # in case the state previous identifier is in the symbol item set previous map
                if state_previous_identifier in symbol_item_set_previous_map:
                    # retrieves the item set
                    item_set = symbol_item_set_previous_map[state_previous_identifier]
                # in case the state identifier is in the symbol item set map
                elif state_identifier in symbol_item_set_map:
                    # retrieves the item set
                    item_set = symbol_item_set_map[state_identifier]
                else:
                    # in case it's a look ahead parser
                    if self.is_look_ahead_parser():
                        # creates a new look ahead item set
                        item_set = LookAheadItemSet()
                    else:
                        # creates a new item set
                        item_set = ItemSet()

                    # in case there is a previous state identifier defined
                    if state_previous_identifier:
                        # sets the item set in the symbol item set previous map
                        symbol_item_set_previous_map[state_previous_identifier] = item_set

                    # sets the item set in the symbol item set map
                    symbol_item_set_map[state_identifier] = item_set

                    # appends the item set to the current item sets list
                    current_item_sets_list.append(item_set)

                # adds the rule to the item set
                item_set.add_rule(rule, current_token_position)

                # iterates over all the extra rules
                for extra_rule in exta_rules_list:
                    # adds the extra rule to the item set
                    item_set.add_rule(extra_rule, -1, True)

            # iterates over all the current item sets
            for current_item_set in current_item_sets_list:
                # in case the current item set is not
                # contained in the item sets list
                if not current_item_set in self.item_sets_list:
                    # sets the valid item set
                    valid_item_set = current_item_set
                else:
                    # iterates over all the item sets in
                    # the item sets list
                    for item_set in self.item_sets_list:
                        # in case the item set is the same
                        if current_item_set == item_set:
                            # sets the valid item set
                            valid_item_set = item_set

                # retrieves the valid item set rules list
                valid_item_set_rules_list = valid_item_set.get_rules_list()

                # iterates over all the rules in the valid item set rules list
                for item_set_rule, item_set_token_position, item_set_closure in valid_item_set_rules_list:
                    # in case the item set rule is defined in the previous rules map
                    if item_set_rule in previous_rules_map:
                        # in case it's an item set closure
                        if item_set_closure:
                            # increments the item set token position
                            item_set_token_position += 1

                        # retrieves the previous item sets list
                        # for the given item set rule
                        previous_item_sets_list = previous_rules_map[item_set_rule]

                        # iterates over all the previous item sets
                        for previous_item_set in previous_item_sets_list:
                            # sets the rule sets the transition item set for the rule and token position
                            previous_item_set.set_rule_transition_item_set(item_set_rule, item_set_token_position, valid_item_set)

            # clear the previous rules map
            previous_rules_map.clear()

            # iterates over all the current item sets
            # to remove duplicated item sets
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
                        # in case the rule is not defined in the previous rules map
                        if not rule in previous_rules_map:
                            # creates an empty list
                            previous_rules_map[rule] = []

                        # adds the current item set
                        previous_rules_map[rule].append(current_item_set)

                        # in case it's not a closure
                        if not closure:
                            # creates the rule tuple
                            rule_tuple = (rule, token_position)

                            # sets the current item set in the rules items sets map
                            self.rules_item_sets_map[rule_tuple] = current_item_set

                        # retrieves the rule symbols list
                        rule_symbols_list = rule.get_symbols_list()

                        # retrieves the rule symbols list length
                        rule_symbols_list_length = len(rule_symbols_list)

                        # in case the current token position is not the final one
                        if rule_symbols_list_length > token_position + 1:
                            # creates the rule tuple
                            rule_tuple = (rule, token_position + 1, current_item_set)

                            # adds the rule tuple to the next rules list
                            next_rules_list.append(rule_tuple)

                    # validates the current item set
                    self._validate_item_set(current_item_set)

                    # increments the current item set id
                    current_item_set_id += 1

            # sets the current rules list as the next rules list
            current_rules_list = next_rules_list

    def _validate_item_set(self, item_set):
        """
        Validates the given item set.

        @type item_set: ItemSet
        @param item_set: The item set to validate.
        """

        # retrieves the item set rules
        item_set_rules = item_set.get_rules_list()

        # creates the symbols non terminal map
        symbols_non_terminal_map = {}

        # creates the reduce list
        reduce_list = []

        # iterates over all the non terminal token
        for symbol_non_terminal in self.symbols_non_terminal_map:
            # creates the symbols non terminal map for the
            # given non terminal symbol
            symbols_non_terminal_map[symbol_non_terminal] = {}

            # creates the symbols non terminal symbol reduce list
            symbols_non_terminal_map[symbol_non_terminal][ParserGenerator.REDUCE_OPERATION_VALUE] = []

            # creates the symbols non terminal symbol shift list
            symbols_non_terminal_map[symbol_non_terminal][ParserGenerator.SHIFT_OPERATION_VALUE] = []

        # iterates over all the item set rules
        for item_set_rule, item_set_token_position, _item_set_closure in item_set_rules:
            # retrieves the rule name
            rule_name = item_set_rule.get_rule_name()

            # retrieves the rule symbols list
            rule_symbols_list = item_set_rule.get_symbols_list()

            # retrieves the rule symbols list length
            rule_symbols_list_length = len(rule_symbols_list)

            # in case the item set token position is valid
            if item_set_token_position >= -1:
                # retrieves the symbols non terminal line
                symbols_non_terminal_line = symbols_non_terminal_map[rule_name]

                # retrieves the symbols non terminal shift list
                symbols_non_terminal_shift_list = symbols_non_terminal_line[ParserGenerator.SHIFT_OPERATION_VALUE]

                # retrieves the symbols non terminal reduce list
                symbols_non_terminal_reduce_list = symbols_non_terminal_line[ParserGenerator.REDUCE_OPERATION_VALUE]

                # in case it's the last token
                if item_set_token_position + 1 >= rule_symbols_list_length:
                    # in case it's not an epsilon transition
                    if rule_symbols_list_length:
                        # retrieves the token
                        token = rule_symbols_list[item_set_token_position]
                    # in case it's an epsilon transition
                    else:
                        token = "$"

                    # in case the token already exists in the symbols
                    # non terminal shift list
                    if token in symbols_non_terminal_shift_list:
                        # raises a shift reduce conflict exception
                        raise parser_generator_exceptions.ShiftReduceConflict("in verification", item_set)

                    # appends the token to the symbols non terminal reduce list
                    symbols_non_terminal_reduce_list.append(token)

                    # appends the token to the reduce list
                    reduce_list.append(token)
                else:
                    # retrieves the token
                    token = rule_symbols_list[item_set_token_position + 1]

                    # in case the token already exists in the symbols
                    # non terminal reduce list
                    if token in symbols_non_terminal_reduce_list:
                        # raises a shift reduce conflict exception
                        raise parser_generator_exceptions.ShiftReduceConflict("in verification", item_set)

                    # appends the token to the symbols non terminal shift list
                    symbols_non_terminal_shift_list.append(token)

                # retrieves the reduce list length
                reduce_list_length = len(reduce_list)

                # in case there is more than one reduction
                # in the same item set and is not a look ahead parser
                if reduce_list_length > 1 and not self.is_look_ahead_parser():
                    # raises a reduce reduce conflict exception
                    raise parser_generator_exceptions.ReduceReduceConflict("in verification", item_set)

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
            for item_set_rule, item_set_token_position, _item_set_closure in item_set_rules_list:
                # retrieves the item set rule symbols list
                item_set_rule_symbols_list = item_set_rule.get_symbols_list()

                if len(item_set_rule_symbols_list) > item_set_token_position + 1:
                    # retrieves the item set rule symbol
                    item_set_rule_symbol = item_set_rule_symbols_list[item_set_token_position + 1]
                else:
                    # sets the end symbol
                    item_set_rule_symbol = "$"

                # creates the rule tuple from the item set rule
                rule_tuple = (item_set_rule, item_set_token_position + 1)

                # in case the rule tuple is defined in the
                # rules item sets map
                if rule_tuple in self.rules_item_sets_map:
                    # retrieves the transition item set rule
                    rule_transition_item_set = self.rules_item_sets_map[rule_tuple]
                else:
                    # sets the rule transition item set to invalid
                    rule_transition_item_set = None

                # in case there is a rule transition item set defined
                if rule_transition_item_set:
                    # retrieves the transition table line
                    transition_table_line = self.transition_table_map[index]

                    # in case the item set rule symbol is not yet defined
                    if not item_set_rule_symbol in transition_table_line:
                        # sets the rule symbol in the transition table line
                        transition_table_line[item_set_rule_symbol] = rule_transition_item_set.get_item_set_id()

            # increments the index counter
            index += 1

    def _generate_action_table(self):
        """
        Generates the action table.
        """

        # retrieves the item sets list length
        item_sets_list_length = len(self.item_sets_list)

        # iterates over the range of the item sets list length
        for item_set_index in range(item_sets_list_length):
            self.action_table_map[item_set_index] = {}

        # iterates over the transition table map
        for transition_table_map_index in self.transition_table_map:
            # retrieves the transition table line
            transition_table_line = self.transition_table_map[transition_table_map_index]

            # retrieves the action table line
            action_table_line = self.action_table_map[transition_table_map_index]

            # iterates over the items in the transition table line
            for item_set_rule_symbol in transition_table_line:
                # in case the item set rule symbol is defined
                # in the symbols terminal map
                if item_set_rule_symbol in self.symbols_terminal_map:
                    # creates the shift value
                    shift_value = (transition_table_line[item_set_rule_symbol], ParserGenerator.SHIFT_OPERATION_VALUE)

                    # adds the shift value to the action table line
                    action_table_line[item_set_rule_symbol] = shift_value

        # iterates over all the item sets in the item sets list
        for item_set in self.item_sets_list:
            # retrieves the item set id
            item_set_id = item_set.get_item_set_id()

            # retrieves the action table line
            action_table_line = self.action_table_map[item_set_id]

            for item_set_rule, item_set_token_position, _item_set_closure in item_set.get_rules_list():
                if item_set_rule.get_rule_name() == ParserGenerator.PROGRAM_VALUE and len(item_set_rule.get_symbols_list()) == item_set_token_position + 1:
                    # creates the accept value
                    accept_value = (0, ParserGenerator.ACCEPT_OPERATION_VALUE)

                    # adds the accept value to the action table line
                    action_table_line["$"] = accept_value

        # iterates over the action table map
        for action_table_map_index in self.action_table_map:
            # retrieves the action table line
            action_table_line = self.action_table_map[action_table_map_index]

            # retrieves the rule list
            rules_list = self.item_sets_list[action_table_map_index].get_rules_list()

            # iterates over the rules in the rules list
            for rule, token_position, _closure in rules_list:
                # retrieves the rule symbols list
                rule_symbols_list = rule.get_symbols_list()

                # retrieves the rule symbols list length
                rule_symbols_list_length = len(rule_symbols_list)

                # in case the token is in the last position
                if token_position + 1 == rule_symbols_list_length:
                    # retrieves the rule id
                    rule_id = rule.get_rule_id()

                    # creates the reduce value
                    reduce_value = (rule_id, ParserGenerator.REDUCE_OPERATION_VALUE)

                    # iterates over all the terminal symbols
                    for symbol_terminal in self.symbols_terminal_end_map:
                        # in case it's a look ahead parser or the terminal symbols exist in the ahead
                        # symbols list
                        if not self.is_look_ahead_parser() or symbol_terminal in rule.get_ahead_symbols_list():
                            # in case there is no action defined for the
                            # current symbol terminal (avoid overwrite)
                            if not symbol_terminal in action_table_line:
                                # adds the reduce value to the action table line
                                action_table_line[symbol_terminal] = reduce_value

    def _generate_goto_table(self):
        """
        Generates the goto table.
        """

        # retrieves the item sets list length
        item_sets_list_length = len(self.item_sets_list)

        # iterates over the range of the item sets list length
        for item_set_index in range(item_sets_list_length):
            self.goto_table_map[item_set_index] = {}

        # iterates over the transition table map
        for transition_table_map_index in self.transition_table_map:
            # retrieves the transition table line
            transition_table_line = self.transition_table_map[transition_table_map_index]

            # retrieves the goto table line
            goto_table_line = self.goto_table_map[transition_table_map_index]

            # iterates over the items in the transition table line
            for item_set_rule_symbol in transition_table_line:
                # in case the item set rule symbol is defined
                # in the symbols non terminal map
                if item_set_rule_symbol in self.symbols_non_terminal_map:
                    # retrieves the value from the transition table line
                    value = transition_table_line[item_set_rule_symbol]

                    # adds the value to the action table line
                    goto_table_line[item_set_rule_symbol] = value

    def _get_extra_rules(self, symbol):
        """
        Retrieves the extra rules (closure) for the given symbol.

        @type symbol: String
        @param symbol: The symbol to retrieve the extra rules.
        @rtype: List
        @return: The extra rules for the given symbol.
        """

        # creates the symbols list
        symbols_list = [symbol]

        # retrieves the extra rules for the next symbol
        extra_rules_list = self.rules_map[symbol]

        # iterates over all the extra rules
        # in the extra rules list
        for extra_rule in extra_rules_list:
            # retrieves the symbols list for the extra rule
            extra_rule_symbols_list = extra_rule.get_symbols_list()

            # retrieves the extra rule symbols list length
            extra_rule_symbols_list_length = len(extra_rule_symbols_list)

            # in case it's an epsilon transition
            if not extra_rule_symbols_list_length:
                # continues the loop
                continue

            # retrieves the first symbol
            first_symbol = extra_rule_symbols_list[0]

            # in case the first symbol is a non terminal and the first symbol is not contained
            # in the symbols list
            if first_symbol in self.symbols_non_terminal_map and not first_symbol in symbols_list:
                # retrieves the first symbol extra rules
                first_symbol_extra_rules = self._get_extra_rules(first_symbol)

                # iterates over all the symbols in the first symbol extra rules
                for first_symbol_extra_rule in first_symbol_extra_rules:
                    # in case the first symbol extra rule does not
                    # exists in the extra rules list
                    if not first_symbol_extra_rule in extra_rules_list:
                        # adds the first symbol extra rule to the extra rules
                        extra_rules_list.extend(first_symbol_extra_rules)

                # appends the first symbol to the symbols list
                symbols_list.append(first_symbol)

        # returns the extra rules list
        return extra_rules_list

    def _get_extra_rules_ahead(self, symbol, ahead_symbol = None, ahead_symbols_list = None):
        """
        Retrieves the extra with look-ahead rules (closure) for the given symbol.

        @type symbol: String
        @param symbol: The symbol to retrieve the extra rules.
        @type ahead_symbol: String
        @param ahead_symbol: The symbol after the base symbol to retrieve the extra rules.
        @type ahead_symbols_list: List
        @param ahead_symbols_list: The list of look ahead allowed symbols.
        @rtype: List
        @return: The extra rules for the given symbol.
        """

        # in case the ahead symbols list is defined
        if ahead_symbols_list:
            ahead_symbols_list = copy.copy(ahead_symbols_list)
        else:
            # creates a new ahead symbols list
            ahead_symbols_list = []

        # creates the symbols list
        symbols_list = [symbol]

        # retrieves the extra rules for the next symbol
        extra_rules_list = self.rules_map[symbol]

        # in case there is an ahead symbol defined
        if ahead_symbol:
            # retrieves the next ahead symbols list
            next_ahead_symbols_list = self._get_first_set(ahead_symbol)

            # iterates over all the next ahead symbols
            for next_ahead_symbol in next_ahead_symbols_list:
                # checks if the next ahead symbol does not exists
                # in the ahead symbols list to avoid
                # duplicated ahead symbols
                if not next_ahead_symbol in ahead_symbols_list:
                    # appends the next ahead symbol to the ahead symbols list
                    ahead_symbols_list.append(next_ahead_symbol)

        # creates the extra look ahead list
        extra_look_ahead_list = []

        # creates the extra symbols list
        extra_symbols_list = []

        # creates the extra look ahead closure map
        extra_look_ahead_closure_map = {}

        # iterates over the extra rules list
        for extra_rule in extra_rules_list:
            # creates the extra look ahead rule
            extra_look_ahead_rule = LookAheadRule(extra_rule, copy.copy(ahead_symbols_list))

            # appends the extra look ahead rule to the extra look ahead list
            extra_look_ahead_list.append(extra_look_ahead_rule)

        # iterates over all the extra rules
        # in the extra rules list
        for extra_rule in extra_rules_list:
            # retrieves the symbols list for the extra rule
            extra_rule_symbols_list = extra_rule.get_symbols_list()

            # retrieves the extra rule symbols list length
            extra_rule_symbols_list_length = len(extra_rule_symbols_list)

            # in case it's an epsilon transition
            if not extra_rule_symbols_list_length:
                # continues the loop
                continue

            # retrieves the first symbol
            first_symbol = extra_rule_symbols_list[0]

            # in case the length of the extra rule symbols list
            # is greater than one
            if extra_rule_symbols_list_length > 1:
                # retrieves the second symbol
                second_symbol = extra_rule_symbols_list[1]
            else:
                # sets the second symbol as invalid
                second_symbol = None

            # in case the first symbol is a non terminal and and the first symbol is not contained
            # in the symbols list
            if first_symbol in self.symbols_non_terminal_map and not first_symbol in symbols_list:
                # retrieves the first symbol extra rules
                first_symbol_extra_rules = self._get_extra_rules_ahead(first_symbol, second_symbol, ahead_symbols_list)

                # creates the final symbol extra rules list
                final_symbol_extra_rules_list = []

                # creates the adding symbol extra rules list
                adding_symbol_extra_rules_list = []

                # iterates over the first symbol extra rules
                for first_symbol_extra_rule in first_symbol_extra_rules:

                    # iterates over the extra look ahead list
                    for extra_look_ahead in extra_look_ahead_list:
                        # retrieves the first symbol extra rule base rule
                        first_symbol_extra_rule_base_rule = first_symbol_extra_rule.get_rule()

                        # retrieves the extra look ahead base rule
                        extra_look_ahead_base_rule = extra_look_ahead.get_rule()

                        # in case both the first symbol extra rule base rule and
                        # the extra look ahead base rule are the same
                        if first_symbol_extra_rule_base_rule == extra_look_ahead_base_rule:
                            # retrieves the first symbol extra rule ahead symbols list
                            first_symbol_extra_rule_ahead_symbols_list = first_symbol_extra_rule.get_ahead_symbols_list()

                            # iterates over the the first symbol extra rule ahead symbols list
                            for first_symbol_extra_rule_ahead_symbol in first_symbol_extra_rule_ahead_symbols_list:
                                # adds the rule ahead symbol to the extra look ahead
                                extra_look_ahead.add_ahead_symbol(first_symbol_extra_rule_ahead_symbol)

                            # adds the extra look ahead to the final symbol extra rules list
                            final_symbol_extra_rules_list.append(extra_look_ahead)
                        else:
                            # in case the first symbol extra rule is not defined in the both lists
                            if not first_symbol_extra_rule in adding_symbol_extra_rules_list and not first_symbol_extra_rule in extra_look_ahead_list:
                                # adds the first symbol extra rule to the final symbol extra rules list
                                final_symbol_extra_rules_list.append(first_symbol_extra_rule)

                                # adds the first symbol extra rule to the adding symbol extra rules list
                                adding_symbol_extra_rules_list.append(first_symbol_extra_rule)

                # extends the extra look ahead list with the adding symbol
                # extra rules list
                extra_look_ahead_list.extend(adding_symbol_extra_rules_list)

                # sets the first symbol extra rules as the closure for the extra rule
                extra_look_ahead_closure_map[extra_rule] = final_symbol_extra_rules_list

                # appends the first symbol to the symbols list
                symbols_list.append(first_symbol)
            # in case the first symbol is contained in the symbols list
            elif first_symbol in symbols_list:
                # retrieves the ahead symbols from the second symbol
                ahead_symbols = self._get_first_set(second_symbol)

                # creates the symbol tuple
                symbol_tuple = (symbol, ahead_symbols)

                # appends the symbol tuple to the extra
                # symbols list
                extra_symbols_list.append(symbol_tuple)

        # iterates over the extra look ahead list
        for extra_look_ahead in extra_look_ahead_list:
            # iterates over the symbol and the extra
            # symbol in the extra symbol list
            for symbol, ahead_symbols in extra_symbols_list:
                # retrieves the extra look ahead rule name
                extra_look_ahead_rule_name = extra_look_ahead.get_rule_name()

                # in case the extra look ahead rule name is the same as the symbol
                if extra_look_ahead_rule_name == symbol:
                    # iterates over all the ahead symbols
                    for ahead_symbol in ahead_symbols:
                        # adds the ahead symbol as an ahead symbol to
                        # the extra look ahead
                        extra_look_ahead.add_ahead_symbol(ahead_symbol)

                    # retrieves the extra look ahead base rule
                    extra_look_ahead_rule = extra_look_ahead.get_rule()

                    # in case the rule exists in the extra look ahead closure map
                    if extra_look_ahead_rule in extra_look_ahead_closure_map:
                        # retrieves the closure rules list
                        closure_rules_list = extra_look_ahead_closure_map[extra_look_ahead_rule]

                        # iterates over all the closure rules
                        for closure_rule in closure_rules_list:
                            # iterates over all the ahead symbols
                            for ahead_symbol in ahead_symbols:
                                # adds the ahead symbol as an ahead symbol
                                # to the closure rule
                                closure_rule.add_ahead_symbol(ahead_symbol)

        # returns the extra look ahead rules list
        return extra_look_ahead_list

    def _get_follow_set_item_set(self, item_set):
        pass

    def _get_follow_set_rule(self, rule, token_position):
        """
        Retrieves the follow set for the given rule and token position.

        @type rule: Rule
        @param rule: The rule to retrieve the follow set.
        @type token_position: int
        @param token_position: The token position to retrieves the follow set.
        @rtype: List
        @return: The follow set for the given rule and token position.
        """

        pass

    def _get_first_set(self, symbol):
        """
        Retrieves the first set for the given rule and token position.

        @type symbol: String
        @param symbol: The symbol to retrieve the first set.
        @rtype: List
        @return: The first set for the given rule and token position.
        """

        # in case the symbol is define in the symbols terminal end map
        # is a terminal
        if symbol in self.symbols_terminal_end_map:
            return [symbol]

        # in case the symbol is not defined in the rules map
        if not symbol in self.rules_map:
            # returns an empty list
            return []

        # creates the first set list
        first_set_list = []

        # retrieves the rules for the symbol
        rules_list = self.rules_map[symbol]

        # iterates over the rules in the
        # rules list
        for rule in rules_list:
            # retrieves the symbols list for the rule
            rule_symbols_list = rule.get_symbols_list()

            # retrieves the rule symbols list length
            rule_symbols_list_length = len(rule_symbols_list)

            # in case it's not an epsilon transition
            if rule_symbols_list_length:
                # retrieves the first symbol
                first_symbol = rule_symbols_list[0]

                # retrieves the next first set list
                next_first_set_list = self._get_first_set(first_symbol)
            else:
                # sets the empty symbol as the next first set list
                next_first_set_list = ["$"]

            # iterates over all the next first set items
            for next_first_set_item in next_first_set_list:
                # in case the next firts set item does not exists
                # in the first set list
                if not next_first_set_item in first_set_list:
                    # adds the next first set item to the
                    # first set list
                    first_set_list.append(next_first_set_item)

        # returns the first set list
        return first_set_list

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

                # sets the function in the rule function map
                self.rule_function_map[rule] = function

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

    def _get_token(self):
        """
        Retrieves a valid token from the lexer.

        @rtype: Token
        @return: The valid token that has been retrieved.
        """

        # in case the there is no validation
        if not self.validation:
            return self.lexer.get_token()

        # unsets the valid flag
        valid = False

        # loops while is not valid
        while not valid:
            # retrieves the token
            token = self.lexer.get_token()

            # in case the token type is valid
            if token == None or not token.type in ParserGenerator.IGNORE_TOKENS_MAP:
                # sets the valid flag
                valid = True

        # returns the token
        return token

    def _parse(self):
        """
        Parses the current buffer.
        """

        # creates the stack
        stack = [(0, 0)]

        # retrieves the current token
        current_token = self._get_token()

        # in case the logging level is at least debug
        if logging_configuration.DEFAULT_LOGGING_LEVEL <= logging.DEBUG:
            # prints the debug message
            logging.debug("Current token: %s" % str(current_token))

        # loop indefinitely
        while True:
            # in case the logging level is at least debug
            if logging_configuration.DEFAULT_LOGGING_LEVEL <= logging.DEBUG:
                # prints the debug message
                logging.debug("Current stack: %s" % str(stack))

            # retrieves the current state
            current_state, _current_value = stack[-1]

            # retrieves the current action line
            action_line = self.action_table_map[current_state]

            # in case there is a valid token
            if current_token:
                # sets the token type as the current token type
                token_type = current_token.type

                # sets the token value as the current token value
                token_value = current_token.value
            else:
                # sets the token type as end of string
                token_type = "$"

                # sets the token value as end of string
                token_value = "$"

            # in case the token type is defined in the action line
            if token_type in action_line:
                # retrieves the action value and type from the action table
                action_value, action_type = action_line[token_type]
            else:
                # raises an invalid state exception
                raise parser_generator_exceptions.InvalidState("no action defined for state " + str(current_state) + " and input " + token_type)

            if action_type == ParserGenerator.REDUCE_OPERATION_VALUE:
                # in case the logging level is at least debug
                if logging_configuration.DEFAULT_LOGGING_LEVEL <= logging.DEBUG:
                    # prints the debug message
                    logging.debug("Reduce action: %s" % str(action_value))

                # retrieves the reduce rule
                reduce_rule = self.rules_list[action_value]

                # retrieves the reduce rule symbols list
                reduce_rule_symbols_list = reduce_rule.get_symbols_list()

                # creates the arguments list
                arguments_list = [None]

                # iterates over all the reduce rule symbols
                for _reduce_rule_symbol in reduce_rule_symbols_list:
                    # pops a stack value
                    _pop_state, pop_value = stack.pop()

                    # inserts the popped value into the arguments list
                    arguments_list.insert(1, pop_value)

                # retrieves the reduce rule function
                reduce_rule_function = self.rule_function_map[reduce_rule]

                # calls the reduce rule function with the arguments list
                reduce_rule_function(arguments_list)

                # retrieves the call return value
                return_value = arguments_list[0]

                # retrieves the current state
                current_state, _current_value = stack[-1]

                # retrieves the current goto line
                goto_line = self.goto_table_map[current_state]

                # retrieves the reduce rule name
                reduce_rule_name = reduce_rule.get_rule_name()

                # in case the reduce rule name exists in the goto line
                if reduce_rule_name in goto_line:
                    # retrieves the goto value
                    goto_value = goto_line[reduce_rule_name]

                    # creates the goto tuple with the goto value
                    # and the return value
                    goto_tuple = (goto_value, return_value)

                    # appends the goto tuple to the stack
                    stack.append(goto_tuple)
                else:
                    # raises an invalid state exception
                    raise parser_generator_exceptions.InvalidState("no goto defined for state " + str(current_state) + " and reduce rule " + reduce_rule_name)

            elif action_type == ParserGenerator.SHIFT_OPERATION_VALUE:
                # in case the logging level is at least debug
                if logging_configuration.DEFAULT_LOGGING_LEVEL <= logging.DEBUG:
                    # prints the debug message
                    logging.debug("Shift action: %s" % str(action_value))

                # creates the current tuple with the action value
                # and the token value
                current_tuple = (action_value, token_value)

                # appends the current tuple to the stack
                stack.append(current_tuple)

                # retrieves the next (current) token
                current_token = self._get_token()

                # in case the logging level is at least debug
                if logging_configuration.DEFAULT_LOGGING_LEVEL <= logging.DEBUG:
                    # prints the debug message
                    logging.debug("Current token: %s" % str(current_token))

            elif action_type == ParserGenerator.ACCEPT_OPERATION_VALUE:
                # in case the logging level is at least debug
                if logging_configuration.DEFAULT_LOGGING_LEVEL <= logging.DEBUG:
                    # prints the debug message
                    logging.debug("Accept action")

                # retrieves the accept rule
                accept_rule = self.program_rule

                # retrieves the accept rule symbols list
                accept_rule_symbols_list = accept_rule.get_symbols_list()

                # creates the arguments list
                arguments_list = [None]

                # iterates over all the accept rule symbols
                for _accept_rule_symbol in accept_rule_symbols_list:
                    # pops a stack value
                    _pop_state, pop_value = stack.pop()

                    # inserts the popped value into the arguments list
                    arguments_list.insert(1, pop_value)

                # retrieves the accept rule function
                accept_rule_function = self.program_function

                # calls the accept rule function with the arguments list
                accept_rule_function(arguments_list)

                # retrieves the call return value
                return_value = arguments_list[0]

                # creates the goto tuple with the goto value
                # and the return value
                goto_tuple = (-1, return_value)

                # appends the goto tuple to the stack
                stack.append(goto_tuple)

                break

        # pops the stack top
        stack_top = stack.pop()

        # retrieves the top state and the top value
        _top_state, top_value = stack_top

        # returns the top value
        return top_value

    def _serialize_state(self, file = sys.stdout):
        """
        Serializes the state to the given file.

        @type file: File
        @param file: The file to have the state serialized.
        @rtype: String
        @return: The hash value for the current parser.
        """

        # creates the hash value
        hash_value = self._create_hash()

        file.write(ParserGenerator.HASH_VALUE + " = ")
        file.write("\"" + hash_value + "\"")
        file.write("\n")
        file.write(ParserGenerator.ACTION_TABLE_VALUE + " = ")
        file.write(str(self.action_table_map))
        file.write("\n")
        file.write(ParserGenerator.GOTO_TABLE_VALUE + " = ")
        file.write(str(self.goto_table_map))
        file.write("\n")

        # returns the hash value
        return hash_value

    def _unserialize_state(self, file):
        """
        Unserializes the state from the given file.

        @type file: File
        @param file: The file to have the state unserialized.
        @rtype: String
        @return: The hash value for the previous parser.
        """

        # retrieves the file contents
        file_contents = file.read()

        # creates the globals map
        globals_map = {}

        # creates the locals map
        locals_map = {}

        # executes the file contents
        exec(file_contents, globals_map, locals_map)

        # creates the hash value
        hash_value = None

        if ParserGenerator.HASH_VALUE in locals_map:
            hash_value = locals_map[ParserGenerator.HASH_VALUE]
        else:
            raise parser_generator_exceptions.InvalidStateFile("no hash value defined in file")

        if ParserGenerator.ACTION_TABLE_VALUE in locals_map:
            self.action_table_map = locals_map[ParserGenerator.ACTION_TABLE_VALUE]
        else:
            raise parser_generator_exceptions.InvalidStateFile("no action table defined in file")

        if ParserGenerator.GOTO_TABLE_VALUE in locals_map:
            self.goto_table_map = locals_map[ParserGenerator.GOTO_TABLE_VALUE]
        else:
            raise parser_generator_exceptions.InvalidStateFile("no action table defined in file")

        # returns the hash value
        return hash_value

    def _create_hash(self):
        """
        Creates the hash value for the current parser.

        @rtype: String
        @return: The hash value for the current parser.
        """

        # creates the buffer string
        buffer_string = cStringIO.StringIO()

        # iterates over all the rules in the rules list
        for rule in self.rules_list:
            # retrieves the rule hash string
            rule_hash_string = str(rule.__hash__)

            # writes the rule hash string to the buffer string
            buffer_string.write(rule_hash_string)

        # writes the parser type string to the buffer string
        buffer_string.write(self.parser_type)

        # retrieves the buffer string value
        buffer_string_value = buffer_string.getvalue()

        # creates the md5 value
        md5_value = hashlib.md5()

        # updates the md5 value
        md5_value.update(buffer_string_value)

        # retrieves the md5 hash value
        ms5_hash_value = md5_value.hexdigest()

        # returns the md5 hash value
        return ms5_hash_value

    def _reset_structures(self):
        """
        Resets the internal structures of the parser
        generator.
        """

        self.current_rule_id = 0
        self.program_function = None
        self.error_function = None
        self.program_rule = None
        self.functions_list = []
        self.rules_list = []
        self.rules_map = {}
        self.rule_id_rule_map = {}
        self.rule_function_map = {}
        self.symbols_map = {}
        self.symbols_non_terminal_map = {}
        self.symbols_terminal_map = {}
        self.symbols_terminal_end_map = {}
        self.item_sets_list = []
        self.rules_item_sets_map = {}
        self.transition_table_map = {}
        self.action_table_map = {}
        self.goto_table_map = {}
        self.symbols_terminal_end_map["$"] = True

    def _get_rules_string(self):
        """
        Retrieves the rules as a friendly string.

        @rtype: String
        @return: The rules described as a friendly string.
        """

        # constructs the string value
        string_value = str()

        # iterates over all the rules in the rules list
        for rule in self.rules_list:
            # retrieves the rule string
            rule_string = rule._get_rule_string()

            # retrieves the rule id
            rule_id = rule.get_rule_id()

            # adds the rule id label
            string_value += "rule " + str(rule_id) + "\n"

            # adds the rule string
            string_value += rule_string + "\n\n"

        # returns the string value
        return string_value

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

            # adds the item set string
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
        string_value += "  "

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

    def _get_action_table_string(self):
        """
        Retrieves the action table as a friendly string.

        @rtype: String
        @return: The action table described as a friendly string.
        """

        # constructs the string value
        string_value = str()

        # adds some space to the string value
        string_value += "  "

        # iterates over all the symbols in the symbols terminal map
        for symbol_terminal in self.symbols_terminal_end_map:
            # adds the symbol terminal to the string value
            string_value += symbol_terminal + "  "

        # adds a new line to the string value
        string_value += "\n"

        # retrieves the action table map length
        action_table_map_length = len(self.action_table_map)

        # iterates over the actions size
        for index in range(action_table_map_length):
            # retrieves the symbols map for the action
            # with the given index
            symbols_map = self.action_table_map[index]

            # adds the index to the string value
            string_value += str(index) + " "

            # iterates over all the symbols in the symbols terminal map
            for symbol_terminal in self.symbols_terminal_end_map:
                # in case the symbol terminal is defined
                if symbol_terminal in symbols_map:
                    string_value += str(symbols_map[symbol_terminal][1]) + str(symbols_map[symbol_terminal][0]) + " "
                else:
                    string_value += "## "

            # adds a new line to the string value
            string_value += "\n"

        # returns the string value
        return string_value

    def _get_goto_table_string(self):
        """
        Retrieves the goto table as a friendly string.

        @rtype: String
        @return: The goto table described as a friendly string.
        """

        # constructs the string value
        string_value = str()

        # adds some space to the string value
        string_value += "  "

        # iterates over all the symbols in the symbols non terminal map
        for symbol_non_terminal in self.symbols_non_terminal_map:
            # adds the symbol non terminal to the string value
            string_value += symbol_non_terminal + " "

        # adds a new line to the string value
        string_value += "\n"

        # retrieves the goto table map length
        goto_table_map_length = len(self.goto_table_map)

        # iterates over the goto size
        for index in range(goto_table_map_length):
            # retrieves the symbols map for the goto
            # with the given index
            symbols_map = self.goto_table_map[index]

            # adds the index to the string value
            string_value += str(index) + " "

            # iterates over all the symbols in the symbols non terminal map
            for symbol_non_terminal in self.symbols_non_terminal_map:
                # in case the symbol non terminal is defined
                if symbol_non_terminal in symbols_map:
                    string_value += str(symbols_map[symbol_non_terminal]) + " "
                else:
                    string_value += "# "

            # adds a new line to the string value
            string_value += "\n"

        # returns the string value
        return string_value
