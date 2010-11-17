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

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import copy

import search_query_interpreter.query_interpreter.search_query_interpreter_ast as search_query_interpreter_ast

HITS_VALUE = "hits"
""" The key that retrieves the set of results, contained in an arbitrary index level """

WORDS_VALUE = "words"
""" The key that retrieves the words list that generated each result """

def _visit(ast_node_class):
    """
    Decorator for the visit of an ast node.

    @type ast_node_class: String
    @param ast_node_class: The target class for the visit.
    @rtype: Function
    @return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the visit decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @param: The decorator interceptor function.
        """

        function.ast_node_class = ast_node_class

        return function

    # returns the created decorator
    return decorator

def dispatch_visit():
    """
    Decorator for the dispatch visit of an ast node.

    @rtype: Function
    @return: The created decorator.
    """

    def create_decorator_interceptor(function):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type function: Function
        @param function: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the dispatch visit decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # retrieves the self values
            self_value = args[0]

            # retrieves the node value
            node_value = args[1]

            # retrieves the node value class
            node_value_class = node_value.__class__

            # retrieves the mro list from the node value class
            node_value_class_mro = node_value_class.mro()

            # iterates over all the node value class mro elements
            for node_value_class_mro_element in node_value_class_mro:
                # in case the node method map exist in the current instance
                if hasattr(self_value, "node_method_map"):
                    # retrieves the node method map from the current instance
                    node_method_map = getattr(self_value, "node_method_map")

                    # in case the node value class exists in the node method map
                    if node_value_class_mro_element in node_method_map:
                        # retrieves the visit method for the given node value class
                        visit_method = node_method_map[node_value_class_mro_element]

                        # calls the before visit method
                        self_value.before_visit(*args[1:], **kwargs)

                        # calls the visit method
                        visit_method(*args, **kwargs)

                        # calls the after visit method
                        self_value.after_visit(*args[1:], **kwargs)

                        return

            # in case of failure to find the proper callbak
            function(*args, **kwargs)

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the dispatch visit decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @param: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator

class Visitor:
    """
    The visitor class.
    """

    node_method_map = {}
    """ The node method map """

    visit_childs = True
    """ The visit childs flag """

    visit_next = True
    """ The visit next flag """

    def __init__(self):
        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True

        self.update_node_method_map()

    def update_node_method_map(self):
        # retrieves the class of the current instance
        self_class = self.__class__

        # retrieves the names of the elements for the current class
        self_class_elements = dir(self_class)

        # iterates over all the name of the elements
        for self_class_element in self_class_elements:
            # retrieves the real element value
            self_class_real_element = getattr(self_class, self_class_element)

            # in case the current class real element contains an ast node class reference
            if hasattr(self_class_real_element, "ast_node_class"):
                # retrieves the ast node class from the current class real element
                ast_node_class = getattr(self_class_real_element, "ast_node_class")

                self.node_method_map[ast_node_class] = self_class_real_element

    @dispatch_visit()
    def visit(self, node):
        print "unrecognized element node of type " + node.__class__.__name__

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @_visit(search_query_interpreter_ast.AstNode)
    def visit_ast_node(self, node):
        print "AstNode: " + str(node)

    @_visit(search_query_interpreter_ast.QueryNode)
    def visit_query_node(self, node):
        print "QueryNode: " + str(node)

    @_visit(search_query_interpreter_ast.BooleanQueryNode)
    def visit_boolean_query_node(self, node):
        print "BooleanQueryNode: " + str(node)

    @_visit(search_query_interpreter_ast.AndBooleanQueryNode)
    def visit_and_boolean_query_node(self, node):
        print "AndBooleanQueryNode: " + str(node)

    @_visit(search_query_interpreter_ast.OrBooleanQueryNode)
    def visit_or_boolean_query_node(self, node):
        print "OrBooleanQueryNode: " + str(node)

    @_visit(search_query_interpreter_ast.MultipleTermNode)
    def visit_multiple_term_node(self, node):
        print "MultipleTermNode: " + str(node)

    @_visit(search_query_interpreter_ast.TermNode)
    def visit_term_node(self, node):
        print "TermNode: " + str(node)

    @_visit(search_query_interpreter_ast.QuotedNode)
    def visit_quoted_node(self, node):
        print "QuotedNode: " + str(node)

class IndexSearchVisitor:
    """
    The index visitor class.
    """

    node_method_map = {}
    """ The node method map """

    visit_childs = True
    """ The visit childs flag """

    visit_next = True
    """ The visit next flag """

    search_index = None
    """ The search index """

    context_stack = []
    """ The context stack """

    def __init__(self, search_index):
        self.search_index = search_index

        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True

        self.context_stack = []

        self.update_node_method_map()

    def update_node_method_map(self):
        # retrieves the class of the current instance
        self_class = self.__class__

        # retrieves the names of the elements for the current class
        self_class_elements = dir(self_class)

        # iterates over all the name of the elements
        for self_class_element in self_class_elements:
            # retrieves the real element value
            self_class_real_element = getattr(self_class, self_class_element)

            # in case the current class real element contains an ast node class reference
            if hasattr(self_class_real_element, "ast_node_class"):
                # retrieves the ast node class from the current class real element
                ast_node_class = getattr(self_class_real_element, "ast_node_class")

                self.node_method_map[ast_node_class] = self_class_real_element

    @dispatch_visit()
    def visit(self, node):
        print "unrecognized element node of type " + node.__class__.__name__

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @_visit(search_query_interpreter_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @_visit(search_query_interpreter_ast.QueryNode)
    def visit_query_node(self, node):
        pass

    @_visit(search_query_interpreter_ast.BooleanQueryNode)
    def visit_boolean_query_node(self, node):
        pass

    @_visit(search_query_interpreter_ast.AndBooleanQueryNode)
    def visit_and_boolean_query_node(self, node):
        second_operand = self.context_stack.pop()
        first_operand = self.context_stack.pop()

        if len(first_operand) < len(second_operand):
            smallest_operand = first_operand
            biggest_operand = second_operand
        else:
            smallest_operand = second_operand
            biggest_operand = first_operand

        document_id_removal_list = []

        for document_id in smallest_operand:
            # join the word hits from both operands
            if document_id in biggest_operand:
                for word_id, word_information_map in biggest_operand[document_id][HITS_VALUE].items():
                    smallest_operand[document_id][HITS_VALUE][word_id] = word_information_map
            else:
                document_id_removal_list.append(document_id)

        for document_id_removal_list_item in document_id_removal_list:
            del smallest_operand[document_id_removal_list_item]

        self.context_stack.append(smallest_operand)

    @_visit(search_query_interpreter_ast.OrBooleanQueryNode)
    def visit_or_boolean_query_node(self, node):
        second_operand = self.context_stack.pop()
        first_operand = self.context_stack.pop()

        if len(first_operand) < len(second_operand):
            smallest_operand = first_operand
            biggest_operand = second_operand
        else:
            smallest_operand = second_operand
            biggest_operand = first_operand

        for document_id in smallest_operand:
            biggest_operand[document_id] = None

        self.context_stack.append(biggest_operand)

    @_visit(search_query_interpreter_ast.MultipleTermNode)
    def visit_multiple_term_node(self, node):
        second_operand = self.context_stack.pop()
        first_operand = self.context_stack.pop()

        if len(first_operand) < len(second_operand):
            smallest_operand = first_operand
            biggest_operand = second_operand
        else:
            smallest_operand = second_operand
            biggest_operand = first_operand

        document_id_removal_list = []

        for document_id in smallest_operand:
            if document_id in biggest_operand:
                for word_id, word_information_map in biggest_operand[document_id][HITS_VALUE].items():
                    smallest_operand[document_id][HITS_VALUE][word_id] = word_information_map
            else:
                document_id_removal_list.append(document_id)

        for document_id_removal_list_item in document_id_removal_list:
            del smallest_operand[document_id_removal_list_item]

        self.context_stack.append(smallest_operand)

    @_visit(search_query_interpreter_ast.TermNode)
    def visit_term_node(self, node):
        term_value = node.term_value

        word_information_map = self.search_index.inverted_index_map.get(term_value, {})

        # if the word was found in the index
        if word_information_map:
            # get the hits for the current word from the index
            index_word_hits = word_information_map[HITS_VALUE]

            # create a copy of the hits map for the current word
            word_hits = copy.deepcopy(index_word_hits)

            # the word hits map contains the information for each document containing the current word
            # for each document containing the word
            for _document_id, document_information_map in word_hits.items():
                # retrieves the word document hits
                word_document_hits = document_information_map[HITS_VALUE]

                # stores the the hits under the current term value
                document_hits = {}
                document_hits[term_value] = {}
                document_hits[term_value][HITS_VALUE] = word_document_hits

                # stores the document hits in the document information maps, under the key HITS_VALUE
                document_information_map[HITS_VALUE] = document_hits
        else:
            word_hits = {}

        self.context_stack.append(word_hits)

    @_visit(search_query_interpreter_ast.QuotedNode)
    def visit_quoted_node(self, node):
        term_value_list = node.term_value_list
        term_value_list_length = len(term_value_list)

        # accumulator for the common documents for the quoted text
        current_document_intersection = None

        # the hit list for the quoted text in sequence
        quoted_text_hit_list = []

        # determines the documents that contain all the words in the quoted text
        for term_value in term_value_list:

            word_information_map = self.search_index.inverted_index_map.get(term_value, {})
            # if the term was found in the search index
            if word_information_map:
                if not current_document_intersection:
                    index_word_hits = word_information_map[HITS_VALUE]
                    current_document_intersection = copy.deepcopy(index_word_hits)
                else:
                    new_map = {}

                    for document_id in word_information_map[HITS_VALUE]:
                        if document_id in current_document_intersection:
                            new_map[document_id] = None

                    current_document_intersection = new_map
            # in case the word is not found, break the loop with an empty document intersection
            else:
                current_document_intersection = {}
                break

        # iterates over all the common documents, to determine the ones that contain the quoted words in sequence
        for document in current_document_intersection:
            sortable_hit_items = []

            # iterates over all the quoted words to create the sortable hit items list,
            # which will be sorted and scanned for valid subsequences (where all the quoted words are adjacent)
            for term_value in term_value_list:
                word_information_map = self.search_index.inverted_index_map.get(term_value, {})
                term_value_hit_list = word_information_map[HITS_VALUE][document]

                # iterates over all the hit list for the current term value
                for term_value_hit_item in term_value_hit_list:

                    # encapsulate the hit item
                    sortable_hit_item = SortableHitItem(term_value, term_value_hit_item)

                    # appends the sortable hit item to the list of sortable hit items
                    sortable_hit_items.append(sortable_hit_item)

            # sort the list of sortable hit items
            sortable_hit_items.sort()
            sortable_hit_items_length = len(sortable_hit_items)

            term_value_list_index = 0

            # iterates over all the sorted hits to scan for valid subsequences
            for index in range(sortable_hit_items_length):
                previous_sortable_hit_item = sortable_hit_items[index - 1]

                # this hit item is adjacent to its previous item:
                # if its the first item in the quote value list
                # or if its position is equal to the previous position plus 1
                is_adjacent = term_value_list_index == 0 or sortable_hit_items[index].position == previous_sortable_hit_item.position + 1

                if sortable_hit_items[index].word == term_value_list[term_value_list_index] and is_adjacent:
                    # we have a hit, increment the query index
                    term_value_list_index += 1
                else:
                    # not a match, restart the query scan
                    term_value_list_index = 0

                # checks if we have matched the full quoted value list
                if term_value_list_index == term_value_list_length:
                    # this document contains the quoted string
                    quoted_text_hit_list.append(document)
                    break

        self.context_stack.append(quoted_text_hit_list)

class SortableHitItem:
    """
    The sortable hit item class.
    """

    word = "none"
    """ The word value """

    word_hit_item = {}
    """ The word hit item map """

    position = 0
    """ The position """

    def __init__(self, word, word_hit_item):
        self.word = word
        self.word_hit_item = word_hit_item
        self.position = self.word_hit_item["position"]

    def __cmp__(self, other):
        # retrieves the other position
        other_position = other.position

        # compares both positions
        return self.position - other_position
