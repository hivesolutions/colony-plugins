#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import re

import xml.sax.saxutils

import colony

from . import exceptions

COMPILABLE_TYPES = (
    "literal",
    "root",
    "out",
    "if",
    "elif",
    "else",
    "for",
    "foreach",
    "set",
)
""" The complete set of node types that the compiler is able to translate
into python source, any tree containing a node of another type is not
compiled and is rendered by the (reference) visitor instead """

ITERATION_TYPES = ("for", "foreach")
""" The set of node types that represent an iteration over a sequence
or a map, both of them share the very same attributes """

BRANCH_TYPES = ("elif", "else")
""" The set of node types that start a new branch inside the contents of
a conditional node, they are not visited as regular children """

NAME = "render"
""" The name of the function that is generated for each of the templates,
it's retrieved from the namespace after the execution of the code """

FILE = "<template>"
""" The name used as the origin of the generated code, shown as the file
name in case an exception is raised while rendering """

HEADER = (
    "def " + NAME + "(visitor, constants):",
    "    write = visitor.write",
    "    resolve = visitor.resolve",
    "    global_map = visitor.global_map",
)
""" The sequence of lines that start every generated function, the local
aliases avoid the repeated attribute lookups at rendering time """

INDENT = "    "
""" The string used for each of the levels of indentation of the
generated source code """

TOKEN_REGEX_VALUE = r"[a-zA-Z_][a-zA-Z0-9_]*"
""" The regular expression value that matches a single name, used for
the collection of the names that a value refers to as the arguments of
a call (they are not part of the name of the value itself) """

TOKEN_REGEX = re.compile(TOKEN_REGEX_VALUE)
""" The token regular expression """


def write_out(visitor, value, xml_escape):
    """
    Writes the provided (already resolved) value to the buffer of the
    visitor, running the same set of transformations that the out node
    of the visitor runs for the simplified case.

    :type visitor: Visitor
    :param visitor: The visitor that owns the buffer to be written and
    the configuration for the operation.
    :type value: Object
    :param value: The value that is going to be written.
    :type xml_escape: bool
    :param xml_escape: If the value should be escaped before being
    written to the buffer.
    """

    # resolves the value using the locale bundles and in case the result
    # is an invalid one returns immediately, as nothing is to be written
    value = visitor._resolve_locale(value)
    if value == None:
        return

    # serializes the value into the correct visual representation and
    # makes sure that a valid unicode string is used
    value = visitor._serialize_value(value)
    if not type(value) == colony.legacy.UNICODE:
        value = colony.legacy.UNICODE(value)

    # runs the final transformation on the value according to the
    # auto escaping mode that is defined for the node
    if xml_escape:
        value = xml.sax.saxutils.escape(value)
        value = value.replace('"', "&quot;")

    # in case the variable encoding is defined must re-encode the
    # variable according to the current variable encoding
    if visitor.variable_encoding:
        value = value.encode(visitor.variable_encoding)

    visitor.write(value)


def resolve_parts(visitor, names):
    """
    Resolves the provided sequence of (partial) names against the global
    map of the visitor, running the same guarded resolution that the
    visitor runs for a complete variable name.

    :type visitor: Visitor
    :param visitor: The visitor whose global map is going to be used as
    the starting point of the resolution.
    :type names: Tuple
    :param names: The sequence of the partial names that compose the
    complete name to be resolved.
    :rtype: Object
    :return: The value resolved for the provided sequence of names.
    """

    resolve = visitor._resolve
    value = visitor.global_map
    try:
        for name in names:
            value = resolve(value, name)
    except exceptions.UndefinedVariable:
        if visitor.strict_mode:
            raise
        return None
    return value


def iterable_for(visitor, iterable, name):
    """
    Normalizes the provided value into an iterable one, running the same
    fallback strategy that the iteration node of the visitor runs.

    :type visitor: Visitor
    :param visitor: The visitor for which the normalization is going to
    be performed (controls the strict mode).
    :type iterable: Object
    :param iterable: The value that is going to be normalized.
    :type name: String
    :param name: The name of the value, used for the description of the
    exception raised under strict mode.
    :rtype: Object
    :return: The normalized (iterable) version of the provided value.
    """

    if hasattr(iterable, "__iter__"):
        return iterable
    if visitor.strict_mode:
        raise exceptions.VariableNotIterable("value not iterable: " + name)
    if not iterable == None:
        return [iterable]
    return []


def loop_start(visitor):
    """
    Starts a loop operation in the provided visitor, creating the map
    that holds the loop related values and saving the previous ones so
    that they may be restored at the end of the operation.

    :type visitor: Visitor
    :param visitor: The visitor for which the loop is going to start.
    :rtype: Tuple
    :return: A tuple containing both the newly created loop map and the
    previous values of the loop related globals.
    """

    global_map = visitor.global_map
    previous = (
        global_map.get("loop", None),
        global_map.get("is_first", None),
        global_map.get("is_last", None),
    )
    loop = dict()
    global_map["loop"] = loop
    loop["cycle"] = visitor._loop_cycle
    return loop, previous


def loop_end(visitor, previous):
    """
    Ends a loop operation in the provided visitor, restoring the loop
    related globals to the values they had before it started.

    :type visitor: Visitor
    :param visitor: The visitor for which the loop is going to end.
    :type previous: Tuple
    :param previous: The previous values of the loop related globals, as
    returned by the loop start operation.
    """

    global_map = visitor.global_map
    global_map["loop"] = previous[0]
    global_map["is_first"] = previous[1]
    global_map["is_last"] = previous[2]


NAMESPACE = dict(
    write_out=write_out,
    resolve_parts=resolve_parts,
    iterable_for=iterable_for,
    loop_start=loop_start,
    loop_end=loop_end,
    is_dictionary=colony.is_dictionary,
)
""" The base namespace under which the generated code is executed, it
exposes the complete set of helpers used by it """


class Compiler(object):
    """
    The compiler class, responsible for the translation of an abstract
    syntax tree into python source code that, once compiled, renders the
    template without any kind of node dispatch.

    The compiler is deliberately conservative, refusing to translate any
    tree that contains a construct it does not fully understand, in which
    case the (reference) visitor is used to render the template.
    """

    constants = []
    """ The list of values referenced by the generated code, the code
    refers to them by position so that no template originated value is
    ever part of the generated source """

    lines = []
    """ The list of lines of the generated source code """

    depth = 0
    """ The current level of indentation of the generated code """

    index = 0
    """ The counter used for the generation of the unique names of the
    variables local to the generated function """

    encoding = None
    """ The encoding of the template that is going to be compiled, used
    for the pre encoding of the literal values """

    locals = {}
    """ The map that associates the name of a variable with the local of
    the generated function that holds it, used so that the values of the
    iterations are read without going through the global map """

    def __init__(self, encoding=None):
        self.constants = []
        self.lines = []
        self.depth = 1
        self.index = 0
        self.encoding = encoding
        self.locals = dict()

    def compile(self, root_node):
        """
        Compiles the provided root node into a code object, returning
        both the code object and the sequence of constants it refers to.

        :type root_node: RootNode
        :param root_node: The root node of the tree to be compiled.
        :rtype: Tuple
        :return: A tuple containing both the generated function and the
        tuple of constants, or an invalid value in case the tree contains
        a node that is not able to be compiled.
        """

        # verifies that the complete set of nodes of the tree is able to
        # be compiled, otherwise no function is generated
        if not self.is_compilable(root_node):
            return None

        # generates the source code for the complete set of children of
        # the root node, adding a no operation so that a template with no
        # contents still produces a valid function
        self.lines = list(HEADER)
        self.emit_nodes(root_node.children)
        self.emit("pass")

        # compiles the generated source and runs it under a namespace that
        # exposes the helpers, note that this is done only once per
        # template so that no execution is required for each render, any
        # problem in the generated source falls back to the visitor as the
        # compilation must never make a valid template unusable
        source = "\n".join(self.lines) + "\n"
        namespace = dict(NAMESPACE)
        try:
            exec(compile(source, FILE, "exec"), namespace)
        except Exception:
            return None
        return namespace[NAME], tuple(self.constants)

    def is_compilable(self, node):
        """
        Verifies if the provided node, and the complete set of its
        children, is able to be translated by the compiler.

        :type node: AstNode
        :param node: The node that is going to be verified.
        :rtype: bool
        :return: If the provided node is able to be compiled.
        """

        type = node.get_type()
        if not type in COMPILABLE_TYPES:
            return False

        # an out node is only compiled when it defines the minimum set of
        # attributes, as the remaining ones imply transformations that
        # are not translated by the compiler
        if type == "out" and not self.is_simple(node):
            return False

        # the filtering of values is not translated and so any node whose
        # values are filtered must be rendered by the visitor
        if not self.is_plain(node):
            return False

        # the iteration nodes that rely on the runtime kind of the value
        # for the naming of their variables are not translated
        if type in ITERATION_TYPES and not self.is_iteration(node):
            return False

        for child in node.children:
            if not self.is_compilable(child):
                return False
        return True

    def is_plain(self, node):
        """
        Verifies that no value of the provided node has a filtering
        pipeline associated with it.

        :type node: AstNode
        :param node: The node that is going to be verified.
        :rtype: bool
        :return: If none of the values of the node is filtered.
        """

        attributes = node.get_attributes() if hasattr(node, "attributes") else None
        if not attributes:
            return True
        for attribute in colony.legacy.values(attributes):
            if not type(attribute) == dict:
                continue
            if self.filters(attribute):
                return False
        return True

    def references(self, node, names=None):
        """
        Collects the initial part of the complete set of variable names
        referenced by the provided node and by its children.

        :type node: AstNode
        :param node: The node for which the references are going to be
        collected.
        :type names: Dictionary
        :param names: The map where the names are going to be collected.
        :rtype: Dictionary
        :return: The map containing the referenced names.
        """

        from . import visitor

        if names == None:
            names = dict()

        attributes = node.get_attributes() if hasattr(node, "attributes") else None
        for attribute in colony.legacy.values(attributes or dict()):
            if not type(attribute) == dict:
                continue
            if not attribute.get("type", None) == "variable":
                continue
            self.filters(attribute)
            base = attribute["base"]
            match = visitor.NAMES_REGEX.match(base)
            if match:
                names[match.group()] = True

            # in case the value contains a call, the names used as its
            # arguments are also collected, as they are part of the
            # matched name and would otherwise go unnoticed
            if "(" in base:
                for token in TOKEN_REGEX.findall(base):
                    names[token] = True

        for child in node.children:
            self.references(child, names=names)
        return names

    def assigns(self, node, name):
        """
        Verifies if the contents of the provided node assign a value to
        the variable with the provided name, note that the node itself is
        not verified as an iteration always assigns its own values.

        :type node: AstNode
        :param node: The node whose contents are going to be verified.
        :type name: String
        :param name: The name of the variable to be verified.
        :rtype: bool
        :return: If the provided name is assigned by the contents.
        """

        for child in node.children:
            if self.is_assign(child, name):
                return True
        return False

    def is_assign(self, node, name):
        """
        Verifies if the provided node, or any of its children, assigns a
        value to the variable with the provided name.

        :type node: AstNode
        :param node: The node that is going to be verified.
        :type name: String
        :param name: The name of the variable to be verified.
        :rtype: bool
        :return: If the provided name is assigned by the node.
        """

        type = node.get_type()
        attributes = node.get_attributes() if hasattr(node, "attributes") else dict()

        if type == "set":
            if self.literal_value(attributes.get("item", None)) == name:
                return True

        # an iteration assigns the names of its item, index and key values
        # on each one of the iterations it performs
        if type in ITERATION_TYPES:
            for key in ("item", "index", "key"):
                if self.literal_value(attributes.get(key, None)) == name:
                    return True

        for child in node.children:
            if self.is_assign(child, name):
                return True
        return False

    def is_iteration(self, node):
        """
        Verifies that the provided iteration node does not depend on the
        runtime kind of the value for the naming of its variables, which
        happens when no item name is defined together with an index one.

        :type node: AstNode
        :param node: The iteration node that is going to be verified.
        :rtype: bool
        :return: If the provided iteration node is able to be compiled.
        """

        attributes = node.get_attributes()
        item = self.literal_value(attributes.get("item", None))
        index_ref = self.literal_value(attributes.get("index", None))
        return not (item == None and not index_ref == None)

    def is_simple(self, node):
        """
        Verifies if the provided out node defines only the value and the
        auto escaping attributes, and that no filters are applied to it.

        :type node: AstNode
        :param node: The out node that is going to be verified.
        :rtype: bool
        :return: If the provided node is a simple out one.
        """

        attributes = node.get_attributes()
        if not len(attributes) == 2:
            return False
        if not type(attributes.get("xml_escape", None)) == bool:
            return False
        value = attributes.get("value", None)
        if not value:
            return False
        return not self.filters(value)

    def filters(self, attribute):
        """
        Retrieves the sequence of filters of the provided attribute,
        computing it in case it's not yet available.

        :type attribute: Dictionary
        :param attribute: The attribute for which the filters are going
        to be retrieved.
        :rtype: Tuple
        :return: The sequence of filters of the attribute.
        """

        from . import visitor

        filters = attribute.get("filters", None)
        if filters == None:
            base, filters = visitor.split_filters(attribute["original"])
            attribute["base"] = base
            attribute["filters"] = filters
        return filters

    def constant(self, value):
        """
        Adds the provided value to the sequence of constants of the
        generated code, returning the expression that refers to it.

        :type value: Object
        :param value: The value that is going to be added.
        :rtype: String
        :return: The expression that refers to the added value.
        """

        self.constants.append(value)
        return "constants[%d]" % (len(self.constants) - 1)

    def local(self, prefix):
        """
        Generates the name of a variable local to the generated function,
        guaranteed not to collide with a previously generated one.

        :type prefix: String
        :param prefix: The prefix to be used in the name.
        :rtype: String
        :return: The newly generated name.
        """

        self.index += 1
        return "_%s_%d" % (prefix, self.index)

    def emit(self, line):
        """
        Adds the provided line to the generated source, indenting it
        according to the current depth.

        :type line: String
        :param line: The line of code to be added.
        """

        self.lines.append(INDENT * self.depth + line)

    def emit_nodes(self, nodes):
        """
        Generates the source code for the provided sequence of nodes.

        :type nodes: List
        :param nodes: The sequence of nodes to be generated.
        """

        # the sequence of the literal values that are pending a write, they
        # are joined together so that a run of contiguous literals results
        # in a single write operation
        pending = []

        for node in nodes:
            type = node.get_type()
            if type in BRANCH_TYPES:
                continue

            if type == "literal":
                pending.append(node.value.value)
                continue

            self.emit_literals(pending)
            self.emit_node(node, type)

        self.emit_literals(pending)

    def emit_literals(self, pending):
        """
        Generates the write of the provided sequence of literal values,
        joining them into a single constant, and empties the sequence.

        :type pending: List
        :param pending: The sequence of literal values that are pending
        a write operation.
        """

        if not pending:
            return

        # joins the complete set of pending literals and pre encodes the
        # result when an encoding is defined, as the write operation of
        # the visitor would otherwise encode it on every single render
        value = "".join(pending)
        if self.encoding:
            value = value.encode(self.encoding)

        self.emit("write(%s)" % self.constant(value))
        del pending[:]

    def emit_node(self, node, type):
        """
        Generates the source code for the provided node, dispatching to
        the proper generation method according to its type.

        :type node: AstNode
        :param node: The node to be generated.
        :type type: String
        :param type: The type of the node to be generated.
        """

        if type == "out":
            self.emit_out(node)
        elif type == "if":
            self.emit_if(node)
        elif type in ITERATION_TYPES:
            self.emit_for(node)
        elif type == "set":
            self.emit_set(node)

    def emit_out(self, node):
        attributes = node.get_attributes()
        value = self.value(attributes["value"])
        escape = self.constant(attributes["xml_escape"])
        self.emit("write_out(visitor, %s, %s)" % (value, escape))

    def emit_if(self, node):
        # splits the children of the conditional node around the various
        # branch nodes, so that each of them may be generated under the
        # proper python conditional statement
        branches = self.branches(node)

        for index in range(len(branches)):
            branch, children = branches[index]
            type = branch.get_type() if branch else "if"

            if type == "else":
                self.emit("else:")
            else:
                statement = "if" if index == 0 else "elif"
                self.emit("%s %s:" % (statement, self.condition(branch or node)))

            # generates the contents of the branch, adding a no operation
            # so that an empty branch still produces valid source
            self.depth += 1
            self.emit_nodes(children)
            self.emit("pass")
            self.depth -= 1

    def emit_for(self, node):
        attributes = node.get_attributes()

        from_value = attributes["from"]
        item = self.literal_value(attributes.get("item", None))
        index_ref = self.literal_value(attributes.get("index", None))
        key_ref = self.literal_value(attributes.get("key", None))
        start_index = self.literal_value(attributes.get("start_index", None))

        # creates the complete set of names local to the loop, note that
        # they are unique so that the nesting of loops is possible
        iterable = self.local("iterable")
        loop = self.local("loop")
        previous = self.local("previous")
        length = self.local("length")
        is_map = self.local("is_map")
        ordinal = self.local("ordinal")
        index = self.local("index")
        element = self.local("element")
        first = self.local("first")
        last = self.local("last")

        # normalizes the value into an iterable one and gathers both its
        # length and the kind of iteration to be performed
        self.emit(
            "%s = iterable_for(visitor, %s, %s)"
            % (
                iterable,
                self.value(from_value),
                self.constant(from_value["value"]),
            )
        )
        self.emit("%s = len(%s)" % (length, iterable))
        self.emit("%s = is_dictionary(%s)" % (is_map, iterable))

        # verifies if the contents of the loop make any use of the loop
        # related values, as maintaining them for each of the iterations
        # is only required when they are effectively read
        references = self.references(node)
        is_loop = "loop" in references
        is_flags = "is_first" in references or "is_last" in references

        self.emit("%s, %s = loop_start(visitor)" % (loop, previous))
        self.emit("%s['length'] = %s" % (loop, length))
        self.emit("%s = 1" % ordinal)
        self.emit(
            "%s = %s" % (index, "1" if start_index == None else str(int(start_index)))
        )
        self.emit("try:")

        self.depth += 1
        self.emit("for %s in %s:" % (element, iterable))

        self.depth += 1
        if is_loop or is_flags:
            self.emit("%s = %s == 1" % (first, ordinal))
            self.emit("%s = %s == %s" % (last, ordinal, length))
        if is_loop:
            self.emit("%s['index'] = %s" % (loop, index))
            self.emit("%s['index0'] = %s - 1" % (loop, index))
            self.emit("%s['first'] = %s" % (loop, first))
            self.emit("%s['last'] = %s" % (loop, last))
        if is_flags:
            self.emit("global_map['is_first'] = %s" % first)
            self.emit("global_map['is_last'] = %s" % last)

        # in case no item name is defined the very same name receives the
        # key of the map or the element of the sequence, which are the
        # same value, making the runtime kind of the value irrelevant
        if item == None:
            name = key_ref
            if not key_ref == None:
                self.emit("global_map[%s] = %s" % (self.constant(key_ref), element))
            value = element

        # otherwise the item receives the value and both the index and the
        # key references receive their own values (when they are defined)
        else:
            name = item
            value = self.local("value")
            self.emit(
                "%s = %s[%s] if %s else %s"
                % (value, iterable, element, is_map, element)
            )
            self.emit("global_map[%s] = %s" % (self.constant(item), value))
            if not index_ref == None:
                self.emit("global_map[%s] = %s" % (self.constant(index_ref), index))
            if not key_ref == None:
                self.emit(
                    "global_map[%s] = %s if %s else %s"
                    % (self.constant(key_ref), element, is_map, index)
                )

        # binds the value of the iteration to a local of the generated
        # function so that the contents read it directly, note that the
        # binding is skipped in case the contents re-assign the very same
        # name, as the local would then hold an outdated value
        is_bound = not name == None and not self.assigns(node, name)
        if is_bound:
            self.locals[name] = value

        self.emit_nodes(node.children)

        # drops the binding once the iteration is over, note that no
        # previous binding is restored as the value left in the global map
        # is the one of the last iteration (matches the visitor), the
        # binding may already be gone in case an inner iteration used the
        # very same name for its own value
        if is_bound:
            self.locals.pop(name, None)

        self.emit("%s += 1" % ordinal)
        self.emit("%s += 1" % index)
        self.depth -= 2

        self.emit("finally:")
        self.depth += 1
        self.emit("loop_end(visitor, %s)" % previous)
        self.depth -= 1

    def emit_set(self, node):
        attributes = node.get_attributes()
        item = self.literal_value(attributes["item"])
        value = self.value(attributes["value"])
        self.emit("global_map[%s] = %s" % (self.constant(item), value))

    def condition(self, node):
        """
        Builds the expression that evaluates the comparison of the
        provided conditional node.

        :type node: AstNode
        :param node: The conditional node for which the expression is
        going to be built.
        :rtype: String
        :return: The expression that evaluates the comparison.
        """

        from . import visitor

        attributes = node.get_attributes()
        item = self.value(attributes["item"])
        value = self.value(attributes.get("value", None))
        operator = self.literal_value(attributes.get("operator", None))

        # in case no operator is defined the item value is the one that
        # is going to be evaluated for its truthiness
        comparison = visitor.COMPARISION_FUNCTIONS.get(operator, None)
        if comparison == None:
            return item
        return "%s(%s, %s)" % (self.constant(comparison), item, value)

    def branches(self, node):
        """
        Splits the children of the provided conditional node into the
        various branches that compose it.

        :type node: AstNode
        :param node: The conditional node to be split.
        :rtype: List
        :return: A list of tuples, each containing the node that starts
        the branch (invalid for the first one) and its children.
        """

        branches = [(None, [])]
        for child in node.children:
            if child.get_type() in BRANCH_TYPES:
                branches.append((child, []))
            else:
                branches[-1][1].append(child)
        return branches

    def value(self, attribute):
        """
        Builds the expression that retrieves the value of the provided
        attribute, either as a constant or as a name resolution.

        :type attribute: Dictionary
        :param attribute: The attribute for which the expression is going
        to be built.
        :rtype: String
        :return: The expression that retrieves the value.
        """

        from . import visitor

        if not attribute:
            return "None"

        # a literal attribute is embedded as a constant, while a variable
        # one is resolved at rendering time using the very same operation
        # that the visitor uses (keeps the semantics unchanged)
        if attribute["type"] == "literal":
            return self.constant(attribute["value"])

        self.filters(attribute)
        base = attribute["base"]

        # splits the name into its various parts at compile time, so that
        # no splitting is required at rendering time
        names = tuple(match.group() for match in visitor.NAMES_REGEX.finditer(base))

        # in case the first part of the name is held by a local of the
        # generated function (the value of an iteration) the resolution
        # starts at it, avoiding the lookup in the global map
        local = self.locals.get(names[0], None)
        if not local == None:
            expression = local
            for name in names[1:]:
                expression = "resolve(%s, %s)" % (expression, self.constant(name))
            return expression

        if len(names) == 1:
            return "resolve(global_map, %s)" % self.constant(names[0])
        return "resolve_parts(visitor, %s)" % self.constant(names)

    def literal_value(self, attribute):
        """
        Retrieves the literal value of the provided attribute, mirroring
        the equivalent operation of the visitor.

        :type attribute: Dictionary
        :param attribute: The attribute for which the value is going to
        be retrieved.
        :rtype: Object
        :return: The literal value of the attribute.
        """

        if attribute == None:
            return None
        return attribute["value"]


def compile_node(root_node, encoding=None):
    """
    Compiles the provided root node into a function, returning both the
    function and the sequence of constants it refers to.

    :type root_node: RootNode
    :param root_node: The root node of the tree to be compiled.
    :type encoding: String
    :param encoding: The encoding of the template, used for the pre
    encoding of the literal values.
    :rtype: Tuple
    :return: A tuple containing both the generated function and the tuple
    of constants, or an invalid value in case the tree is not able to be
    compiled.
    """

    return Compiler(encoding=encoding).compile(root_node)


def render_compiled(compiled, visitor):
    """
    Runs the provided compiled template, rendering it into the buffer of
    the provided visitor.

    :type compiled: Tuple
    :param compiled: The tuple containing both the generated function and
    the sequence of constants referred by it.
    :type visitor: Visitor
    :param visitor: The visitor that holds both the state and the buffer
    for the rendering operation.
    """

    function, constants = compiled
    function(visitor, constants)
