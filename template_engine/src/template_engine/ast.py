#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import re

from . import exceptions

QUOTED_SINGLE = 1
QUOTED_DOUBLE = 2
FLOAT = 3
INTEGER = 4
BOOL_TRUE = 5
BOOL_FALSE = 6
NONE = 7

NAME_REGEX = re.compile(r"[a-zA-Z_\[\{][\sa-zA-Z0-9_\-\.\/\(\)\:\=,\%'\"\[\]\{\}\|]*")
""" The regular expression that is going to be used in the matching
of variable names/parts should comply with both the name of the variable,
possible filtering pipeline and method calls """

LITERAL_REGEX = re.compile(
    "(?P<quoted_single>['][^']+['])|" + \
    "(?P<quoted_double>[\"][^\"]+[\"])|" + \
    "(?P<float>-?[0-9]+\.[0-9]*)|" + \
    "(?P<integer>-?[0-9]+)|" + \
    "(?P<true_boolean>True)|" + \
    "(?P<false_boolean>False)|" + \
    "(?P<none>None)"
)
""" Regular expression to be used in the parsing of literal values, named
groups are used for the conditional retrieval of each of the types """

IF_REGEX = re.compile(
    "(?P<complex>(not\s+)?(.+)\s+(in|<|>|<=|>=|==)\s+(.+))|" + \
    "(?P<simple>(not\s+)?(.+))"
)
""" The regular expression that is going to be used for the extraction of the
various parts of an if statement note that there are two forms of an if
statement one complex and one simple, this is required so that all forms
of partial expression may be matched for variables """

FOR_REGEX = re.compile(
    "(?P<complex>(.+)\s*\,\s*(.+)\s+in\s+(.+))|" + \
    "(?P<simple>(.+)\s+in\s+(.+))"
)
""" Regular expression used for the mating of the various parts of the for
expression the expression defines two modes one simple with just the key
definition and one more complex with both key and value definitions """

SET_REGEX = re.compile(
    "(.+)\s+=\s+(.+)"
)
""" The regular expression that is going to be used for the match operation
in the payload of the set operation """

OPERATORS = {
    "in" : "in",
    "==" : "eq",
    ">=" : "gte",
    ">": "gt",
    "<=": "lte",
    "<": "lt",
}
""" Mapping between the normal (python) definition of operations and the more
internal template way of representing them, the internal representation is
purely textual and a convention defines that if it starts with an 'n' character
a negation should be done in the final boolean evaluation (not) """

class AstNode(object):
    """
    The ast node class, this is the top level abstract
    value from which the various nodes should inherit.
    """

    value = None
    """ The value, this should be the match value
    that original the node (raw value) latter this
    may be used directly in the visit """

    parent = None
    """ Reference to the parent node of this node this
    is required so that switch operations on the node
    are possible by replacing the references to the
    child and parent nodes """

    super = None
    """ Reference to the (virtual) super node of the current
    node, this reference is used to allow a perfect representation
    of the nodes hierarchy (required for template inheritance) """

    children = []
    """ The list of nodes that are considered to be
    children of the current node, the maximum number
    of children is not limited """

    def __init__(self):
        self.children = []
        self.supers = []

    def __repr__(self):
        type = self.get_type()
        id = self.get_id()
        return "<%s %s>" % (type, id) if id else "<%s>" % type

    def accept(self, visitor):
        visitor.visit(self)

        if not visitor.visit_childs: return

        for child in self.children:
            child.accept(visitor)

    def set_value(self, value):
        self.value = value

    def get_type(self):
        return "ast"

    def get_id(self):
        return None

    def switch(self, node):
        parent = self.parent

        index = parent.children.index(self)
        parent.remove_child(self)
        parent.children.insert(index, node)

        node.parent = parent
        node.super = self

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def remove_child(self, node):
        node.parent = None
        self.children.remove(node)

class RootNode(AstNode):
    """
    The root node class, this should be used only for
    the root and aggregating node and with no value set.
    """

    def __init__(self):
        AstNode.__init__(self)

    def accept(self, visitor):
        visitor.visit(self)

        if not visitor.visit_childs: return

        while True:
            if not self.children: break
            child = self.children[0]
            type = child.get_type()
            if not type == "extends": break
            child.accept(visitor)

        for child in self.children:
            type = child.get_type()
            if type == "extends": continue
            child.accept(visitor)

    def get_type(self):
        return "root"

class LiteralNode(AstNode):
    """
    The literal node class, used for the representation of
    literal (textual) parts of the template. This is used
    for the inter-parts between the "logical" nodes and
    must be visited with a simple printing operation.
    """

    def __init__(self, value = None):
        AstNode.__init__(self)
        self.value = value

    def get_type(self):
        return "literal"

class SimpleNode(AstNode):

    def __init__(self, value = None, type = "out"):
        AstNode.__init__(self)
        self.value = value
        self.type = type
        self.attributes = dict()
        self.process_value()

    def get_attributes(self):
        return self.attributes

    def get_type(self):
        return self.type

    def get_id(self):
        name = self.attributes.get("name", {})
        return name.get("value", None)

    def accept(self, visitor):
        visitor.process_accept(self, self.type)

    def parse(self, value):
        if not value: return value

        original = value

        match = LITERAL_REGEX.match(value)
        if match:
            value = match.group()
            index = match.lastindex

            if index == QUOTED_SINGLE: value = value.strip("'")
            elif index == QUOTED_DOUBLE: value = value.strip("\"")
            elif index == FLOAT: value = float(value)
            elif index == INTEGER: value = int(value)
            elif index == BOOL_TRUE: value = True
            elif index == BOOL_FALSE: value = False
            elif index == NONE: value = None

            return self.literal(value, original)

        match = NAME_REGEX.match(value)
        if match:
            value = match.group().strip()
            return self.variable(value, original)

    def variable(self, value, original = None):
        if original == None: original = value
        return dict(
            value = value,
            original = original,
            type = "variable"
        )

    def literal(self, value, original = None):
        if original == None: original = value
        return dict(
            value = value,
            original = original,
            type = "literal"
        )

class OutputNode(SimpleNode):
    """
    The output node class that represent a match that
    is representative of an output request. An example
    of such request would be {{ 'hello world' }}.

    This is equivalent to the more complex single node
    configured as an out operation.
    """

    def __init__(self, value = None, type = "out", xml_escape = True):
        SimpleNode.__init__(self, value = value, type = type)
        self.attributes["xml_escape"] = xml_escape

    def process_value(self):
        value = self.value[2:-2]
        value = value.strip()
        self.attributes["value"] = self.parse(value)

class EvalNode(SimpleNode):

    def process_value(self):
        value = self.value[2:-2]
        value = value.strip()
        value_s = value.split(" ", 1)
        self.type = value_s[0]

        if len(value_s) > 1: contents = value_s[1].strip()
        else: contents = None

        if self.type == "if": self._process_if(contents)
        elif self.type == "else": pass
        elif self.type == "elif": self._process_if(contents)
        elif self.type == "for": self._process_for(contents)
        elif self.type == "set": self._process_set(contents)
        elif self.type == "block": self._process_block(contents)
        elif self.type == "include": self._process_include(contents)
        elif self.type == "extends": self._process_extends(contents)
        elif self.type.startswith("end"): pass
        else: raise exceptions.RuntimeError("invalid tag '%s'" % self.type)

    def is_end(self):
        if not self.type: return False
        return self.type.startswith("end")

    def is_open(self):
        if not self.type: return False
        return self.type in ("if", "for", "block")

    def assert_end(self, type):
        if type == self.type[3:]: return
        raise RuntimeError("Invalid end tag")

    def _process_if(self, contents):
        match = IF_REGEX.match(contents)
        if not match: raise exceptions.RuntimeError("malformed if expression")

        not_oper = False
        oper = None
        item = None
        value = None

        is_complex = match.group("complex")
        if is_complex:
            not_oper = match.group(2)
            item = match.group(3)
            oper = match.group(4)
            value = match.group(5)
        else:
            not_oper = match.group(7)
            item = match.group(8)

        if item: item = item.strip()
        if value: value = value.strip()

        oper = OPERATORS.get(oper, oper)
        if not_oper: oper = "n" + oper if oper else "not"

        self.attributes["item"] = self.parse(item)
        self.attributes["value"] = self.parse(value)
        self.attributes["operator"] = self.literal(oper)

    def _process_for(self, contents):
        match = FOR_REGEX.match(contents)
        if not match: raise exceptions.RuntimeError("malformed for expression")

        key = None
        _from = False
        item = None

        is_complex = match.group("complex")
        if is_complex:
            key = match.group(2)
            item = match.group(3)
            _from = match.group(4)
        else:
            key = match.group(6)
            _from = match.group(7)

        if item: item = item.strip()
        if key: key = key.strip()

        self.attributes["item"] = self.literal(item)
        self.attributes["from"] = self.parse(_from)
        self.attributes["key"] = self.literal(key)

    def _process_set(self, contents):
        match = SET_REGEX.match(contents)
        if not match: raise exceptions.RuntimeError("malformed for expression")

        item = match.group(1)
        value = match.group(2)

        item = item.strip()
        value = value.strip()

        self.attributes["item"] = self.parse(item)
        self.attributes["value"] = self.parse(value)

    def _process_block(self, contents):
        self.attributes["name"] = self.parse(contents)

    def _process_include(self, contents):
        self.attributes["file_value"] = self.parse(contents)

    def _process_extends(self, contents):
        self.attributes["file_value"] = self.parse(contents)

class MatchNode(AstNode):
    """
    The match node class, that represents a node that
    contains a type in the initial part of the value
    and then a series of key to value attributes.
    """

    type = None
    """ The (value) type for the match node this is
    the type of node operation that is going to be
    performed, this value may assume any value
    (eg: out, for, if, else, etc.) """

    attributes = {}
    """ Map describing the complete set of attributes
    (configuration) for the current node, this is a
    set of key value mappings """

    regex = None
    """ The attribute regular expression, that is going
    to be used in the matching of variable based attributes """

    literal_regex = None
    """ The attribute literal regular expression, this value
    is going to be used in the matching of literal attributes """

    def __init__(self, value = None, regex = None, literal_regex = None):
        AstNode.__init__(self)

        self.value = value
        self.regex = regex
        self.literal_regex = literal_regex

        self.attributes = {}

        self.process_type()
        self.process_attributes()

    def process_type(self):
        match = self.get_start_match()
        match_value = match.get_value()

        match_value_s = match_value.split()
        self.type = match_value_s[0][2:]

    def process_attributes(self):
        # retrieve the match value part of the node, this is the string
        # value that is going to be matched against the regular expressions
        # to try to find the various attributes of the node
        match = self.get_start_match()
        match_value = match.get_value()

        # uses both the currently set regular expression and literal
        # regular expression to find the matches for both of these
        # values that will then be processed as attributes
        attributes_matches = self.regex.finditer(match_value)
        literal_matches = self.literal_regex.finditer(match_value)

        # iterates over all the attributes matches to construct the
        # attribute dictionary structure for each of them, note that
        # these matches are only for the variable based values
        for match in attributes_matches:
            # retrieves the attribute value and splits it around
            # the equals operator, and then constructs the dictionary
            # that represents the attribute setting it on the map
            attribute = match.group()
            name, value = attribute.split("=")
            self.attributes[name] = dict(
                value = value,
                original = value,
                type = "variable"
            )

        # iterates over the complete set of literal matches to create
        # the attribute structure for each of them the data type for
        # the literal value will be retrieve from the group index of
        # the match to be used (the regular expression must comply)
        for match in literal_matches:
            attribute = match.group()
            name, value = attribute.split("=")
            index = match.lastindex
            original = value

            if index == QUOTED_SINGLE: value = value.strip("'")
            elif index == QUOTED_DOUBLE: value = value.strip("\"")
            elif index == FLOAT: value = float(value)
            elif index == INTEGER: value = int(value)
            elif index == BOOL_TRUE: value = True
            elif index == BOOL_FALSE: value = False
            elif index == NONE: value = None

            self.attributes[name] = dict(
                value = value,
                original = original,
                type = "literal"
            )

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_id(self):
        name = self.attributes.get("name", {})
        return name.get("value", None)

    def get_attributes(self):
        return self.attributes

    def set_attributes(self, attributes):
        self.attributes = attributes

class SingleNode(MatchNode):
    """
    The single node class, that contains a single value
    and that should have a simple visiting operation.
    """

    def __init__(self, value = None, regex = None, literal_regex = None):
        MatchNode.__init__(self, value, regex, literal_regex)

    def get_start_match(self):
        return self.value

    def accept(self, visitor):
        type = self.get_type()
        visitor.process_accept(self, type)

class CompositeNode(MatchNode):
    """
    The composite node class, that represents a node that contains
    multiple children nodes and for which a visit may be a complex
    task of visiting multiple nodes.
    """

    def __init__(self, value = None, regex = None, literal_regex = None):
        MatchNode.__init__(self, value, regex, literal_regex)

    def get_start_match(self):
        return self.value[0]

    def accept(self, visitor):
        type = self.get_type()
        visitor.process_accept(self, type)
