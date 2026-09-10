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

import os
import re

import colony

from . import ast
from . import visitor
from . import exceptions

OUTPUT_REGEX_VALUE = r"\{\{[^\}]*\}\}"
""" The regular expression value for the matching of the
output (print) operations, these are specialized nodes
that are only meant to print variable/literal values """

EVAL_REGEX_VALUE = r"\{\%[^\}]*\%\}"
""" Regular expression that matched the complex evaluation
expression that allow the control flow of the template this
is the regular expression to be used under simple mode """

START_TAG_REGEX_VALUE = r"\$\{[^\/\{}\{}][^\{\}][^\/\{}\{}]*\}"
""" The start tag regular expression value that should
match the starting tag of an expression """

END_TAG_REGEX_VALUE = r"\$\{\/[^\{\}][^\/\{}\{}]*\}"
""" The end tag regular expression value """

SINGLE_TAG_REGEX_VALUE = r"\$\{[^\{\}]*\/\}"
""" The single tag regular expression value """

ATTRIBUTE_REGEX_VALUE = r"[a-zA-Z_]+=[a-zA-Z_][a-zA-Z0-9_\-\.\/\(\)\:,'\"\|]*"
""" The attribute regular expression value, this
regular expression value should be able to match
the complete set of attribute matches """

QUOTED_SINGLE_REGEX_VALUE = r"[a-zA-Z_]+=['][^']+[']"
""" The attribute quoted single regular expression value """

QUOTED_DOUBLE_REGEX_VALUE = r'[a-zA-Z_]+=["][^"]+["]'
""" The attribute quoted double regular expression value """

FLOAT_REGEX_VALUE = r"[a-zA-Z_]+=-?[0-9]+\.[0-9]*"
""" The attribute float regular expression value """

INTEGER_REGEX_VALUE = r"[a-zA-Z_]+=-?[0-9]+"
""" The attribute integer regular expression value """

BOOL_TRUE_REGEX_VALUE = r"[a-zA-Z_]+=True"
""" The attribute true boolean regular expression value """

BOOL_FALSE_REGEX_VALUE = r"[a-zA-Z_]+=False"
""" The attribute false boolean regular expression value """

NONE_REGEX_VALUE = r"[a-zA-Z_]+=None"
""" The attribute none regular expression value """

OUTPUT_VALUE = 1
""" The output value """

EVAL_VALUE = 2
""" The eval value """

START_VALUE = 3
""" The start value """

END_VALUE = 4
""" The end value """

SINGLE_VALUE = 5
""" The single value """

LITERAL_VALUE = 6
""" The literal value """

OUTPUT_REGEX = re.compile(OUTPUT_REGEX_VALUE)
""" Regular expression used to match the simple output
nodes it should be wide enough to handle all kinds of
variable values """

EVAL_REGEX = re.compile(EVAL_REGEX_VALUE)
""" Compiled regular expression used for the matching
of the evaluation expressions that allow the control of
flow contents for the template """

START_TAG_REGEX = re.compile(START_TAG_REGEX_VALUE)
""" The start tag regular expression, used to
match the start tag of a complete expression """

END_TAG_REGEX = re.compile(END_TAG_REGEX_VALUE)
""" The end tag regular expression """

SINGLE_TAG_REGEX = re.compile(SINGLE_TAG_REGEX_VALUE)
""" The single tag regular expression """

ATTRIBUTE_REGEX = re.compile(ATTRIBUTE_REGEX_VALUE)
""" The attribute regular expression """

ATTRIBUTE_LITERAL_REGEX = re.compile(
    "(?P<quoted_single>"
    + QUOTED_SINGLE_REGEX_VALUE
    + ")|"
    + "(?P<quoted_double>"
    + QUOTED_DOUBLE_REGEX_VALUE
    + ")|"
    + "(?P<float>"
    + FLOAT_REGEX_VALUE
    + ")|"
    + "(?P<integer>"
    + INTEGER_REGEX_VALUE
    + ")|"
    + "(?P<true_boolean>"
    + BOOL_TRUE_REGEX_VALUE
    + ")|"
    + "(?P<false_boolean>"
    + BOOL_FALSE_REGEX_VALUE
    + ")|"
    + "(?P<none>"
    + NONE_REGEX_VALUE
    + ")"
)
""" The literal regular expression that matches all the literals, there
are matching groups for each of the data types """

MATCH_REGEX = re.compile(
    OUTPUT_REGEX_VALUE
    + "|"
    + EVAL_REGEX_VALUE
    + "|"
    + END_TAG_REGEX_VALUE
    + "|"
    + SINGLE_TAG_REGEX_VALUE
    + "|"
    + START_TAG_REGEX_VALUE
)
""" The unified regular expression that matches every kind of template
token in a single (ordered) scan of the template contents, note that no
capturing groups are used as they would impose a considerable penalty
in the matching operation, the kind of the token is instead determined
from the initial (and final) characters of the matched value """

TEMPLATES_LIMIT = 1024
""" The maximum number of parsed templates to be kept in the global
templates cache, once this value is reached the cache is completely
flushed (avoids unbounded memory growth) """

TEMPLATES_CACHE = {}
""" The cache that associates the path of a template file with both the
signature of the file and the (pristine) root node resulting from its
parsing, a copy of this node is used for each of the parse operations,
note that the signature is based on the modification time and the size
of the file and so a change that preserves both is not detected """

ESCAPE_EXTENSIONS = (
    ".xml",
    ".html",
    ".xhtml",
    ".liquid",
    ".xml.tpl",
    ".html.tpl",
    ".xhtml.tpl",
)
""" The sequence containing the various extensions
for which the autoescape mode will be enabled  by
default as expected by the end developer """


def match_type(value):
    """
    Determines the kind of the provided (matched) token value using
    only the initial and final characters of it, this is a much faster
    approach than the usage of capturing groups in the tokenizer.

    :type value: String
    :param value: The complete (literal) value of the matched token
    for which the type is going to be determined.
    :rtype: int
    :return: The internal type value for the provided token.
    """

    # in case the token starts with the curly brace character it's
    # either an output or an evaluation token, the second character
    # is the one that defines which one of them it is
    if value[0] == "{":
        return OUTPUT_VALUE if value[1] == "{" else EVAL_VALUE

    # the token is a "dollar" based one, meaning that the closing
    # sequence defines a single (self closing) token, otherwise the
    # third character defines if it's an end or a start token
    if value[-2] == "/":
        return SINGLE_VALUE
    return END_VALUE if value[2] == "/" else START_VALUE


class TemplateEngine(colony.System):
    """
    The template engine class, responsible for the processing
    of template files according to the current template engine
    based file specification. Its internal working should be
    based on a visitor strategy.
    """

    def parse_file_path(
        self,
        file_path,
        base_path=None,
        encoding=None,
        process_methods_list=[],
        locale_bundles=None,
    ):
        # retrieves the status of the template file, in case it's not
        # possible to do so the file is considered not to exist and so
        # an exception is raised indicating such problem
        try:
            status = os.stat(file_path)
        except OSError:
            raise exceptions.RuntimeError("'%s' template file not found" % file_path)

        # builds both the key and the signature for the file, note that a
        # relative path must be made absolute before being used as the key,
        # otherwise the very same path could refer to different files, and
        # that any change to the contents of the file changes its signature
        # invalidating the version of it that is currently cached
        key_path = file_path if os.path.isabs(file_path) else os.path.abspath(file_path)
        key = (key_path, encoding)
        signature = (status.st_mtime, status.st_size)

        # tries to retrieve the (already parsed) root node for the file from
        # the cache, in case there's no valid one the file must be effectively
        # read and parsed, storing the resulting tree in the cache
        cached = TEMPLATES_CACHE.get(key, None)
        if not cached or not cached[0] == signature:
            file = open(file_path, "rb")
            try:
                root_node = self._parse_file(
                    file, file_path=file_path, encoding=encoding
                )
            finally:
                file.close()
            if len(TEMPLATES_CACHE) > TEMPLATES_LIMIT:
                TEMPLATES_CACHE.clear()
            cached = (signature, root_node)
            TEMPLATES_CACHE[key] = cached

        # copies the (pristine) cached tree so that the caller is given a
        # private version of it, note that the identifiable nodes are indexed
        # as part of the copy avoiding an extra traversal of the tree
        nodes = dict()
        root_node = cached[1].clone(nodes=nodes)

        # creates the template file structure for the resulting root node
        # and returns it to the caller method (as expected)
        return self._template_file(
            root_node,
            file_path=file_path,
            base_path=base_path,
            encoding=encoding,
            process_methods_list=process_methods_list,
            locale_bundles=locale_bundles,
            nodes=nodes,
        )

    def parse_file_path_variable_encoding(
        self,
        file_path,
        base_path=None,
        encoding=None,
        variable_encoding=None,
        process_methods_list=[],
        locale_bundles=None,
    ):
        # parses the file for the given file path with the
        # given encoding retrieving the template file and
        # then sets the variable encoding in it returning
        # then the resulting template file object to the
        # caller method (as expected by definition)
        template_file = self.parse_file_path(
            file_path,
            base_path=base_path,
            encoding=encoding,
            process_methods_list=process_methods_list,
            locale_bundles=locale_bundles,
        )
        template_file.set_variable_encoding(variable_encoding)
        return template_file

    def parse_file(
        self,
        file,
        file_path=None,
        base_path=None,
        encoding=None,
        process_methods_list=[],
        locale_bundles=None,
    ):
        # runs the effective parsing of the file retrieving the root node
        # of the abstract syntax tree that represents the template and then
        # uses it to build the template file structure
        root_node = self._parse_file(file, file_path=file_path, encoding=encoding)
        return self._template_file(
            root_node,
            file_path=file_path,
            base_path=base_path,
            encoding=encoding,
            process_methods_list=process_methods_list,
            locale_bundles=locale_bundles,
        )

    def _parse_file(self, file, file_path=None, encoding=None):
        """
        Runs the effective parsing of the provided file, building the
        abstract syntax tree that represents the template contained in it.

        :type file: File
        :param file: The file that is going to be read and parsed.
        :type file_path: String
        :param file_path: The path to the file to be used, this value may
        or may not be defined and controls the auto escaping mode.
        :type encoding: String
        :param encoding: The encoding used in the file, in case this value
        is not defined the encoding is assumed to be the default one.
        :rtype: RootNode
        :return: The root node of the abstract syntax tree that represents
        the template contained in the provided file.
        """

        # retrieves the proper extension of the template's file
        # path and then uses it to try to determine if the template
        # output operation should be automatically escaped
        extension = self._extension(file_path)
        xml_escape = self._extension_in(extension, ESCAPE_EXTENSIONS)

        # reads the complete set of file contents and in case an
        # encoding is defined decodes the provided file contents
        # using the encoding value (may raise exception), note that
        # under python 3 the decoding is always required as it's not
        # possible to match a string pattern against a bytes value
        file_contents = file.read()
        is_bytes = type(file_contents) == colony.legacy.BYTES
        if is_bytes and encoding:
            file_contents = file_contents.decode(encoding)
        elif is_bytes and colony.legacy.PYTHON_3:
            file_contents = file_contents.decode("utf-8")

        # creates the root node and starts the stack of tree nodes
        # with the root node inserted in it, the stack will be used
        # for the proper handling of start and end values
        root_node = ast.RootNode()
        stack = [root_node]

        # creates the initial previous end value, this value is going to
        # be used to detect the literal (pure contents) parts that exist
        # in between the various matched tokens of the template
        previous_end = 0

        # runs a single (ordered) scan of the complete template contents
        # matching every kind of token in one pass, as the matches are
        # already provided in order no sorting operation is required
        for match in MATCH_REGEX.finditer(file_contents):
            # retrieves both the start and the end positions of the current
            # match as they are going to be used both for the literal parts
            # detection and for the housekeeping of the iteration
            match_start = match.start()
            match_end = match.end()

            # in case the current match start is not the same as the previous
            # end, this means that there's a literal value in between both
            # matches and so that literal value must be added as a node
            if not match_start == previous_end:
                literal_value = file_contents[previous_end:match_start]
                literal_value = visitor.escape_literal(literal_value)
                literal_match = LiteralMatch(previous_end, match_start)
                literal_orderer = MatchOrderer(
                    literal_match, LITERAL_VALUE, literal_value
                )
                stack[-1].add_child(ast.LiteralNode(literal_orderer))

            # updates the previous end value with the end of the current
            # match, this is considered to be the iteration housekeeping
            previous_end = match_end

            # determines the type of the current match from the value of
            # the matched token and creates the match orderer structure
            # that is going to be used for the node creation
            match_value = match.group()
            mtype = match_type(match_value)
            match_orderer = MatchOrderer(match, mtype, match_value)

            if mtype == OUTPUT_VALUE:
                value = match_orderer.get_value()
                node = ast.OutputNode(value, xml_escape=xml_escape)
                parent_node = stack[-1]
                parent_node.add_child(node)

            elif mtype == EVAL_VALUE:
                value = match_orderer.get_value()
                node = ast.EvalNode(value)
                parent_node = stack[-1]
                is_end = node.is_end()
                is_open = node.is_open()
                if is_end:
                    if len(stack) == 1:
                        raise exceptions.RuntimeError(
                            "unexpected end tag '%s'" % node.type
                        )
                    node.assert_end(parent_node.type)
                    stack.pop()
                else:
                    parent_node.add_child(node)
                    if is_open:
                        stack.append(node)

            elif mtype == START_VALUE:
                node = ast.CompositeNode(
                    [match_orderer],
                    regex=ATTRIBUTE_REGEX,
                    literal_regex=ATTRIBUTE_LITERAL_REGEX,
                )
                parent_node = stack[-1]
                parent_node.add_child(node)
                stack.append(node)

            elif mtype == END_VALUE:
                node = stack.pop()
                node.value.append(match_orderer)

            elif mtype == SINGLE_VALUE:
                node = ast.SingleNode(
                    match_orderer,
                    regex=ATTRIBUTE_REGEX,
                    literal_regex=ATTRIBUTE_LITERAL_REGEX,
                )
                parent_node = stack[-1]
                parent_node.add_child(node)

        # in case there is still a final literal to be processed, it
        # must be processed as a special case, adding the remaining
        # contents of the template as a literal node
        contents_length = len(file_contents)
        if not previous_end == contents_length:
            literal_value = file_contents[previous_end:contents_length]
            literal_value = visitor.escape_literal(literal_value)
            literal_match = LiteralMatch(previous_end, contents_length)
            literal_orderer = MatchOrderer(literal_match, LITERAL_VALUE, literal_value)
            stack[-1].add_child(ast.LiteralNode(literal_orderer))

        # returns the root node of the abstract syntax tree that has just
        # been built from the contents of the provided file
        return root_node

    def _template_file(
        self,
        root_node,
        file_path=None,
        base_path=None,
        encoding=None,
        process_methods_list=[],
        locale_bundles=None,
        nodes=None,
    ):
        """
        Builds the template file structure for the provided root node,
        loading it with the complete set of values that are required for
        the processing of the template.

        :type root_node: RootNode
        :param root_node: The root node of the abstract syntax tree that
        represents the template.
        :type file_path: String
        :param file_path: The path to the file from which the template
        has been loaded.
        :type base_path: String
        :param base_path: The base file system path that is going to be
        used for processing templates in the include and extends operation.
        :type encoding: String
        :param encoding: The encoding used in the file, in case this value
        is not defined the encoding is assumed to be the default one.
        :type process_methods_list: List
        :param process_methods_list: The list of tuples containing the
        method name and method (function) to be attached.
        :type locale_bundles: List
        :param locale_bundles: The list of locale bundles to be used for
        resolution in the current context.
        :type nodes: Dictionary
        :param nodes: The map of the already indexed identifiable nodes,
        in case it's not provided the indexing operation is performed.
        :rtype: TemplateFile
        :return: The template file structure ready to be processed.
        """

        # in case the locale bundles list is not defined must
        # create a new list reference to handle it correctly
        if locale_bundles == None:
            locale_bundles = []

        # creates the template file structure that is going to be
        # used to represent the template in a abstract way this is
        # going to be the interface structure with the end user
        template_file = TemplateFile(
            manager=self,
            base_path=base_path,
            file_path=file_path,
            encoding=encoding,
            root_node=root_node,
            nodes=nodes,
        )

        # attaches the currently given process methods and locale
        # bundles to the template file so that they may be used
        # latter for the processing of the file
        template_file.attach_process_methods(process_methods_list)
        template_file.attach_locale_bundles(locale_bundles)

        # loads the system variable in the template file, this
        # will allow access to the global system status from inside
        # the template file (for diagnosis and debugging)
        template_file.load_system_variable()

        # loads the complete set of based functions that should be
        # made accessible to the template for be able to perform
        # common operations like conversion and localization
        template_file.load_functions()

        # returns the final template file template file to the caller
        # method so that it may be used for rendering
        return template_file

    def _extension(self, file_path):
        if not file_path:
            return None
        _head, tail = os.path.split(file_path)
        tail_s = tail.split(".", 1)
        if len(tail_s) > 1:
            return "." + tail_s[1]
        return None

    def _extension_in(self, extension, sequence):
        if extension == None:
            return False
        for item in sequence:
            valid = extension.endswith(item)
            if not valid:
                continue
            return True
        return False


class MatchOrderer(object):
    """
    The match orderer class, that is used to re-sort
    the various matched of the template engine in
    the proper order.
    """

    match = None
    """ The match object to be ordered, this value
    should be the internal regex library value for
    the match operation """

    type = None
    """ The type of the match object to be ordered,
    this value should reflect the kind of match that
    has been accomplished for the value """

    value = None
    """ The value of the match object to be ordered
    this should be a literal string value of it """

    def __init__(self, match, type, value):
        self.match = match
        self.type = type
        self.value = value

    def __cmp__(self, other):
        return other.match.start() - self.match.start()

    def __lt__(self, other):
        return self.match.start() > other.match.start()

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class LiteralMatch(object):
    start_index = None
    """ The start index value, this should be an offset
    position inside the current document's string data value """

    end_index = None
    """ The end index value, that should close the
    current literal value starting in the start index """

    def __init__(self, start_index=None, end_index=None):
        self.start_index = start_index
        self.end_index = end_index

    def start(self):
        return self.start_index

    def end(self):
        return self.end_index


class TemplateFile(object):
    """
    The template file class, this is the most abstract
    representation of the template and also the entry
    level for the user level operations.
    """

    manager = None
    """ The manager of the template file, this is considered to
    be the owner and generator instance """

    base_path = None
    """ The base path to be used in the resolution of template
    files, this value may or may not be defined and in case it's
    not defined only the default (relative path) resolution approach
    is used for the include and extends operations """

    file_path = None
    """ The path to the file from which the contents of the template
    are loaded, this is the original reference """

    encoding = None
    """ The encoding used in the file, this is the main encoding
    to be used both in the loading and storage of it """

    variable_encoding = None
    """ The encoding that is going to be used to encode the value
    of the various variables to be expanded in the template """

    strict_mode = False
    """ The strict mode flag, that controls if the an error in a
    variable resolution should raise an exception, usage of this
    value should be done with care to avoid unwanted behavior """

    root_node = None
    """ The root node from which the visitor will start the visiting
    using a recursive approach """

    visitor = None
    """ The visitor object that will be used for the visiting of the
    various nodes that make part of the abstract syntax tree defined
    from the provided root node """

    locale_bundles = []
    """ The list that contains the various bundles to be searched for
    localization, the order set is going to be the priority for template
    value resolution (from first to last list element) """

    nodes = {}
    """ The dictionary that associates the identifiable node id with
    the node reference that it corresponds, this map may be used for
    abstract syntax tree manipulations (eg: inheritance manipulation) """

    def __init__(
        self,
        manager=None,
        base_path=None,
        file_path=None,
        encoding=None,
        root_node=None,
        eval=False,
        nodes=None,
    ):
        """
        Constructor of the class.

        :type manager: TemplateEngine
        :param manager: The manager to be used.
        :type base_path: String
        :param base_path: The base file system path that is going to be
        used for processing templates in the include and extends operation.
        :type file_path: String
        :param file_path: The path to the file to be used, this value may or
        may not be defined depending on how the template is created.
        :type encoding: String
        :param encoding: The encoding used in the file, in case this value
        is not defined the encoding is assumed to be the default one.
        :type root_node: AstNode
        :param root_node: The root node to be used.
        :type eval: bool
        :param eval: If the evaluation based visitor should be used instead
        of the normal (and safe) interpreter based visitor. Care should be
        taking while deciding which visitor to be used.
        :type nodes: Dictionary
        :param nodes: The map of the already indexed identifiable nodes, in
        case it's not provided the indexing operation is performed.
        """

        self.manager = manager
        self.base_path = base_path
        self.file_path = file_path
        self.encoding = encoding
        self.root_node = root_node

        self.visitor = visitor.EvalVisitor(self) if eval else visitor.Visitor(self)
        self.locale_bundles = []

        # in case the identifiable nodes have already been indexed (eg: as
        # part of the copy of a tree) they are used directly, otherwise the
        # indexing operation must be performed for the complete tree
        if nodes == None:
            self.nodes = {}
            self.index_nodes()
        else:
            self.nodes = nodes

    @classmethod
    def format(cls, template, *args):
        """
        Custom format operation that takes a template value and
        a variable set of arguments and formats it according to
        the C definition of string templating.

        :type template: String
        :param template: The template string to be used in the
        C like format operation.
        :rtype: String
        :returns: The "final" formatted string value.
        """

        try:
            return template % args
        except Exception:
            return None

    @classmethod
    def convert(cls, value, mode):
        """
        Converts the provided value according to the requested "modification"
        operation.

        The final converted value should be a "plain" string value.

        :type value: String
        :param value: The base value that is going to be converted
        according to the provided/requested mode.
        :type mode: String
        :param mode: The mode that described the operation that is
        going to be applied to the "base" value.
        :rtype: String
        :return: The final converted value according to the requested
        mode.
        """

        conversion_method = visitor.CONVERSION_MAP.get(mode, None)
        if not conversion_method:
            return value
        try:
            return conversion_method(value)
        except Exception:
            return None

    def index_nodes(self):
        """
        Runs the indexing stage of the identifiable nodes, this is
        required for the inheritance of blocks to properly work.

        More that one execution of this method may be required if
        the abstract syntax tree changed in response to the processing
        of one or more file inclusion (sub tree inclusion).
        """

        self._index_node(self.root_node)

    def assign(self, name, value):
        """
        Assigns a variable to a value. This assignment
        allows the usage of the value internally in the template.

        The assigned variable value may assume any given data
        type that is accessible by the template language.

        :type name: String
        :param name: The name of the variable to assign a value.
        :type value: Object
        :param value: The value to be assigned to the variable
        """

        self.visitor.set_global(name, value)

    def set_global_map(self, global_map):
        """
        Sets the global map to the current template file.
        The global map should be used as the support for the variable
        assignment.

        :type global_map: Dictionary
        :param global_map: The global map containing all the variable values.
        """

        self.visitor.set_global_map(global_map)

    def set_string_buffer(self, string_buffer):
        """
        Updates the underlying string buffer that is going to be
        used by the visitor to the provided one.

        The string buffer should be an opened file like object that
        accepts the typical calls.

        In case a typical file object is used this may reduce the
        amount of memory used by the visitor by an order of magnitude
        so this method may be very useful for long output generation
        in the template engine.

        :type string_buffer: File
        :param string_buffer: The file like object that is going to
        be used by the underlying visitor object.
        """

        self.visitor.string_buffer = string_buffer

    def attach_process_methods(self, process_methods_list):
        """
        Attaches a series of process methods to the visitor
        currently being used.

        This will allow for the usage of many more process
        methods that the ones available by default (extension).

        :type process_methods_list: List
        :param process_methods_list: The list of tuples containing the
        method name and method (function).
        """

        # iterates over all the process methods in the list unpacking
        # the tuples and then attaching each of these methods to the
        # currently defined visitor so that they may be used
        for method_name, method in process_methods_list:
            self.visitor.attach_process_method(method_name, method)

    def attach_locale_bundles(self, locale_bundles):
        """
        Attaches a series of locale bundles methods to the visitor
        currently being used.

        This method also attaches the locale bundles to the current
        instance (for context retrieval).

        :type locale_bundles: List
        :param locale_bundles: The list of locale bundles to be used
        for resolution in the current context.
        """

        self.locale_bundles = locale_bundles
        self.visitor.locale_bundles = locale_bundles

    def load_system_variable(self, name="_system"):
        """
        Loads a system information variable to the template
        file. This variable would allow for access to the
        status of the current manager/system.

        :type name: String
        :param name: The name of the variable used
        to retain the system wide information.
        """

        # retrieves the template engine plugin
        # in order to obtain the plugin manager
        template_engine_plugin = self.manager.plugin
        plugin_manager = template_engine_plugin.manager

        # retrieves the map containing the "global" system information
        system_information_map = plugin_manager.get_system_information_map()

        # assigns the system information map variable to
        # the template so that it may be used to retrieve
        # global information about the system
        self.assign(name, system_information_map)

    def load_functions(self):
        """
        Loads the complete set of base functions that are going to be
        used at template runtime to perform common operations.

        These functions will be exposed on the global dictionary.
        """

        # retrieves the reference to the class associated with the
        # current instance to be able to access class variables
        cls = self.__class__

        # runs the assign operation for the complete set of functions
        # that are considered part of the global namespace
        self.assign("colony", colony)
        self.assign("format", cls.format)
        self.assign("convert", cls.convert)

    def load_visitor(self):
        """
        Runs the various loading/prepare operations in the currently
        set visitor so that it becomes reading for the visit of AST
        based nodes (prepare operation).

        This operation should always be called before any accepting
        operation of a visitor is performed (processing), otherwise
        unexpected behavior may occur in the visit.
        """

        self.visitor.set_encoding(self.encoding)
        self.visitor.set_base_path(self.base_path)
        self.visitor.set_file_path(self.file_path)
        self.visitor.set_template_engine(self.manager)
        self.visitor.set_variable_encoding(self.variable_encoding)
        self.visitor.set_strict_mode(self.strict_mode)

    def process(self, get_value=True):
        """
        Processes the template file running the visitor
        and returning the result value.

        This is considered to be the main method for the
        processing of the template and should only be called
        when the complete set of attribute are set in the
        current template structure (to avoid errors).

        The resulting value from this operation should always
        be a valid unicode string that may be used in any kind
        of transform operation. Alternatively and if the get value
        flag is not set the buffer is returned, but this option
        should be used carefully to avoid any encoding problems.

        :type get_value: bool
        :param get_value: If the final string value of
        the contents should be retrieved as a result.
        :rtype: String/Buffer
        :return: The result value from the visitor or the
        string buffer in case the get value flag was set
        to a false value.
        """

        # sets the complete set of attributes in the visitor
        # that is currently set in the template and then runs
        # the accept operation in the root node, this will
        # trigger the generation of the template contents
        self.load_visitor()
        self.root_node.accept(self.visitor)

        # retrieves the visitor string buffer, that should now
        # contains the final contents from template generation
        string_buffer = self.visitor.string_buffer

        # retrieves the visitor string buffer value, in case
        # the value should be retrieved from the underlying string
        # buffer, otherwise retrieves the string buffer as the value
        if get_value:
            value = string_buffer.get_value()
        else:
            value = string_buffer

        # in case the returned value from the string buffer is not
        # a valid unicode string it must be decoded using the currently
        # defined encoding or the default one in case it's not defined
        is_bytes = type(value) == colony.legacy.BYTES
        if is_bytes:
            value = value.decode(self.encoding or "utf-8")

        # returns the final value to the caller method, this may
        # either have the reference to the string buffer of the
        # generated string value contents
        return value

    def get_variable_encoding(self):
        """
        Retrieves the variable encoding.

        :rtype: String
        :return: The variable encoding.
        """

        return self.variable_encoding

    def set_variable_encoding(self, variable_encoding):
        """
        Sets the variable encoding.

        :type variable_encoding: String
        :param variable_encoding: The variable encoding.
        """

        self.variable_encoding = variable_encoding

    def get_strict_mode(self):
        """
        Retrieves the strict mode.
        In strict mode, variables referenced but node defined
        raise exceptions.

        :rtype: String
        :return: The strict mode.
        """

        return self.strict_mode

    def set_strict_mode(self, strict_mode):
        """
        Sets the strict mode.
        In strict mode, variables referenced but node defined
        raise exceptions.

        :type strict_mode: bool
        :param strict_mode: The strict mode.
        """

        self.strict_mode = strict_mode

    def add_bundle(self, bundle):
        """
        Adds a new locale bundle to the current
        context, the bundle will be added both
        to the current instance and to the visitor.

        :type bundle: Dictionary
        :param bundle: The locale bundle to be added to
        the current template processing context.
        """

        self.locale_bundles.append(bundle)
        self.visitor.add_bundle(bundle)

    def _index_node(self, node):
        """
        Index the provided template node, making sure that
        its identifier is present in the nodes map and associated
        with the node, this is a relevant operation for the
        inheritance infra-structure.

        :type node: Node
        :param node: The node that should be indexed under the
        current template infra-structure.
        """

        type = node.get_type()
        id = node.get_id()
        if type == "block":
            self.nodes[id] = node
        for node in node.children:
            self._index_node(node)
