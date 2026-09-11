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
import shutil
import datetime
import tempfile

import colony

from . import ast
from . import mocks
from . import system
from . import visitor
from . import exceptions


class TemplateEngineTest(colony.Test):
    """
    The template engine infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            AstTestCase,
            TemplateEngineTestCase,
            TemplateFileTestCase,
            VisitorTestCase,
            VisitorResolutionTestCase,
            EvalVisitorTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class TemplateEngineBaseTestCase(colony.ColonyTestCase):
    """
    The base test case for the template engine, provides the
    facilities required for the rendering of "in-line" templates
    using a temporary directory as the base path for them.
    """

    @staticmethod
    def get_description():
        return "Template engine base test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self.engine = system.TemplateEngine(mocks.MockPlugin())
        self.temp_path = tempfile.mkdtemp()

        # saves the complete set of process wide caches and limits so that
        # they may be restored latter, this guarantees that the tests are
        # not affected by the ones that have been run before them
        self._templates_limit = system.TEMPLATES_LIMIT
        self._templates_cache = system.TEMPLATES_CACHE.copy()
        self._cache_limit = visitor.CACHE_LIMIT
        self._names_cache = visitor.NAMES_CACHE.copy()
        self._arguments_cache = visitor.ARGUMENTS_CACHE.copy()
        system.TEMPLATES_CACHE.clear()
        visitor.NAMES_CACHE.clear()
        visitor.ARGUMENTS_CACHE.clear()

    def tearDown(self):
        system.TEMPLATES_LIMIT = self._templates_limit
        system.TEMPLATES_CACHE.clear()
        system.TEMPLATES_CACHE.update(self._templates_cache)
        visitor.CACHE_LIMIT = self._cache_limit
        visitor.NAMES_CACHE.clear()
        visitor.NAMES_CACHE.update(self._names_cache)
        visitor.ARGUMENTS_CACHE.clear()
        visitor.ARGUMENTS_CACHE.update(self._arguments_cache)

        shutil.rmtree(self.temp_path, ignore_errors=True)
        colony.ColonyTestCase.tearDown(self)

    def write(self, name, contents):
        """
        Writes a template file with the provided name and contents
        under the temporary directory of the current test.

        :type name: String
        :param name: The name of the template file to be written.
        :type contents: String
        :param contents: The (textual) contents of the template.
        :rtype: String
        :return: The complete path to the written template file.
        """

        path = os.path.join(self.temp_path, name)
        file = open(path, "wb")
        try:
            file.write(contents.encode("utf-8"))
        finally:
            file.close()
        return path

    def parse(self, contents, file_name="test.html.tpl", files=None):
        """
        Parses the provided template contents returning the resulting
        template file structure, extra (support) files may be provided
        so that inclusion and extension operations may be resolved.

        :type contents: String
        :param contents: The contents of the template to be parsed.
        :type file_name: String
        :param file_name: The name of the file that is going to "hold"
        the template contents (controls the auto escaping mode).
        :type files: Dictionary
        :param files: The extra files to be written before the parsing.
        :rtype: TemplateFile
        :return: The resulting (parsed) template file structure.
        """

        for extra_name, extra_contents in colony.legacy.items(files or dict()):
            self.write(extra_name, extra_contents)
        path = self.write(file_name, contents)
        return self.engine.parse_file_path(
            path, base_path=self.temp_path, encoding="utf-8"
        )

    def render(
        self, contents, file_name="test.html.tpl", files=None, strict=False, **values
    ):
        """
        Renders the provided template contents with the named values
        assigned to it, returning the final (string) result.

        :type contents: String
        :param contents: The contents of the template to be rendered.
        :type file_name: String
        :param file_name: The name of the file that is going to "hold"
        the template contents (controls the auto escaping mode).
        :type files: Dictionary
        :param files: The extra files to be written before the parsing.
        :type strict: bool
        :param strict: If the strict mode should be enabled for the
        rendering operation (raises on undefined values).
        :rtype: String
        :return: The result of the template rendering operation.
        """

        template_file = self.parse(contents, file_name=file_name, files=files)
        template_file.set_strict_mode(strict)
        for key, value in colony.legacy.items(values):
            template_file.assign(key, value)
        return template_file.process()


class TemplateEngineTestCase(TemplateEngineBaseTestCase):
    """
    Test case for the template engine system object, responsible
    for the parsing of the template files into the abstract syntax
    tree that represents them.
    """

    @staticmethod
    def get_description():
        return "Template engine parsing test case"

    def test_match_type(self):
        self.assertEqual(system.match_type("{{ name }}"), system.OUTPUT_VALUE)
        self.assertEqual(system.match_type("{% if name %}"), system.EVAL_VALUE)
        self.assertEqual(system.match_type("${/foreach}"), system.END_VALUE)
        self.assertEqual(system.match_type("${out value=name /}"), system.SINGLE_VALUE)
        self.assertEqual(system.match_type("${foreach from=items}"), system.START_VALUE)

    def test_match_type_minimal_single(self):
        self.assertEqual(system.match_type("${a/}"), system.SINGLE_VALUE)

    def test_parse_file_path_not_found(self):
        self.assertRaises(
            exceptions.RuntimeError,
            lambda: self.engine.parse_file_path(
                os.path.join(self.temp_path, "missing.html.tpl")
            ),
        )

    def test_parse_file_path_cached(self):
        path = self.write("cached.html.tpl", "[{{ name }}]")
        first = self.engine.parse_file_path(path, encoding="utf-8")
        second = self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(first.root_node is second.root_node, False)
        first.assign("name", "one")
        second.assign("name", "two")
        self.assertEqual(first.process(), "[one]")
        self.assertEqual(second.process(), "[two]")

    def test_parse_file_path_cached_isolated(self):
        # the expansion of an include changes the tree of the template and
        # so each parse operation must be given its own private tree
        self.write("part.html.tpl", "PART-{{ name }}")
        path = self.write("owner.html.tpl", "[{% include 'part.html.tpl' %}]")

        first = self.engine.parse_file_path(
            path, base_path=self.temp_path, encoding="utf-8"
        )
        first.assign("name", "one")
        self.assertEqual(first.process(), "[PART-one]")

        second = self.engine.parse_file_path(
            path, base_path=self.temp_path, encoding="utf-8"
        )
        second.assign("name", "two")
        self.assertEqual(second.process(), "[PART-two]")

    def test_parse_file_path_cached_shared_parent(self):
        # two different templates extending the same base must not share
        # the (cached) tree of the base template between them
        self.write("base.html.tpl", "<{% block c %}BASE{% endblock %}>")
        self.write(
            "x.html.tpl", "{% extends 'base.html.tpl' %}{% block c %}X{% endblock %}"
        )
        self.write(
            "y.html.tpl", "{% extends 'base.html.tpl' %}{% block c %}Y{% endblock %}"
        )
        path_x = os.path.join(self.temp_path, "x.html.tpl")
        path_y = os.path.join(self.temp_path, "y.html.tpl")

        for _index in range(2):
            template_file = self.engine.parse_file_path(
                path_x, base_path=self.temp_path, encoding="utf-8"
            )
            self.assertEqual(template_file.process(), "<X>")
            template_file = self.engine.parse_file_path(
                path_y, base_path=self.temp_path, encoding="utf-8"
            )
            self.assertEqual(template_file.process(), "<Y>")

    def test_parse_file_path_cached_filter_isolated(self):
        # a filter receives the attributes map so that it may change the
        # behavior of the node, such a change must not be visible to the
        # renders that follow it (would disable escaping for them)
        def conditional(value, meta, visitor):
            if value == "trusted":
                meta.update(xml_escape=False)
            return value

        path = self.write("meta.html.tpl", "[{{ value|conditional }}]")

        template_file = self.engine.parse_file_path(
            path, base_path=self.temp_path, encoding="utf-8"
        )
        template_file.visitor.add_filter("conditional", conditional)
        template_file.assign("value", "trusted")
        self.assertEqual(template_file.process(), "[trusted]")

        template_file = self.engine.parse_file_path(
            path, base_path=self.temp_path, encoding="utf-8"
        )
        template_file.visitor.add_filter("conditional", conditional)
        template_file.assign("value", "<script>")
        self.assertEqual(template_file.process(), "[&lt;script&gt;]")

    def test_parse_file_path_cache_relative(self):
        # the very same relative path refers to different files depending
        # on the current working directory and so it may not be used as
        # the key of the cache without being made absolute first
        one = os.path.join(self.temp_path, "one")
        two = os.path.join(self.temp_path, "two")
        os.makedirs(one)
        os.makedirs(two)

        for base, contents in ((one, "AAA"), (two, "BBB")):
            path = os.path.join(base, "same.html.tpl")
            file = open(path, "wb")
            try:
                file.write(contents.encode("utf-8"))
            finally:
                file.close()
            os.utime(path, (1000000, 1000000))

        cwd = os.getcwd()
        try:
            os.chdir(one)
            template_file = self.engine.parse_file_path(
                "same.html.tpl", encoding="utf-8"
            )
            self.assertEqual(template_file.process(), "AAA")
            os.chdir(two)
            template_file = self.engine.parse_file_path(
                "same.html.tpl", encoding="utf-8"
            )
            self.assertEqual(template_file.process(), "BBB")
        finally:
            os.chdir(cwd)

    def test_parse_file_path_cache_invalidation(self):
        path = self.write("changing.html.tpl", "ONE")
        template_file = self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(template_file.process(), "ONE")

        # re-writes the file forcing a distinct modification time in it, as
        # the resolution of the file system timestamps may not be enough to
        # tell apart two writes performed in quick succession
        self.write("changing.html.tpl", "TWO")
        status = os.stat(path)
        os.utime(path, (status.st_atime, status.st_mtime + 1))

        template_file = self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(template_file.process(), "TWO")

    def test_parse_file_path_cache_same_signature(self):
        # the signature of a file is based on its modification time and on
        # its size, meaning that a change that preserves both of them is
        # not detected, this is a deliberate trade-off of the caching
        path = self.write("stable.html.tpl", "AAA")
        os.utime(path, (1000000, 1000000))
        template_file = self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(template_file.process(), "AAA")

        # re-writes the file with contents of the very same size and forces
        # the very same modification time, making both signatures identical
        self.write("stable.html.tpl", "BBB")
        os.utime(path, (1000000, 1000000))

        template_file = self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(template_file.process(), "AAA")

    def test_parse_file_path_cache_encoding(self):
        path = self.write("encoded.html.tpl", colony.legacy.u("[joão]"))
        template_file = self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(template_file.process(), colony.legacy.u("[joão]"))
        template_file = self.engine.parse_file_path(path, encoding="latin-1")
        self.assertEqual(template_file.process(), colony.legacy.u("[joÃ£o]"))

    def test_parse_file_path_cache_limit(self):
        # lowers the limit of the cache so that the flushing of it may be
        # verified without the creation of a large number of files
        system.TEMPLATES_LIMIT = 2

        for index in range(system.TEMPLATES_LIMIT + 1):
            path = self.write("limit_%d.html.tpl" % index, "[%d]" % index)
            self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(len(system.TEMPLATES_CACHE), system.TEMPLATES_LIMIT + 1)

        # the parsing of one more template exceeds the limit and so the
        # complete set of cached templates is flushed
        path = self.write("limit.html.tpl", "[{{ name }}]")
        template_file = self.engine.parse_file_path(path, encoding="utf-8")
        self.assertEqual(len(system.TEMPLATES_CACHE), 1)

        template_file.assign("name", "john")
        self.assertEqual(template_file.process(), "[john]")

    def test_parse_file_path_no_encoding(self):
        path = self.write("plain.html.tpl", "[{{ name }}]")
        template_file = self.engine.parse_file_path(path)
        template_file.assign("name", "john")
        self.assertEqual(template_file.process(), "[john]")

    def test_parse_file_no_path(self):
        file = colony.legacy.BytesIO("[{{ name }}]".encode("utf-8"))
        template_file = self.engine.parse_file(file, encoding="utf-8")
        template_file.assign("name", "<john>")
        self.assertEqual(template_file.process(), "[<john>]")

    def test_parse_file_ordering(self):
        template_file = self.parse("a{{ x }}b{% if x %}c{% endif %}d")
        children = template_file.root_node.children
        types = [child.get_type() for child in children]
        self.assertEqual(types, ["literal", "out", "literal", "if", "literal"])

    def test_parse_file_nested(self):
        template_file = self.parse(
            "{% for i in items %}{% if i %}x{% endif %}{% endfor %}"
        )
        children = template_file.root_node.children
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].get_type(), "for")
        self.assertEqual(children[0].children[0].get_type(), "if")

    def test_parse_file_empty(self):
        self.assertEqual(self.render(""), "")

    def test_parse_file_literal_only(self):
        self.assertEqual(self.render("hello world"), "hello world")

    def test_parse_file_tag_only(self):
        self.assertEqual(self.render("{{ name }}", name="john"), "john")

    def test_parse_file_tag_at_start(self):
        self.assertEqual(self.render("{{ name }} tail", name="john"), "john tail")

    def test_parse_file_tag_at_end(self):
        self.assertEqual(self.render("head {{ name }}", name="john"), "head john")

    def test_parse_file_adjacent_tags(self):
        self.assertEqual(
            self.render("{{ first }}{{ second }}", first="a", second="b"), "ab"
        )

    def test_parse_file_multiple_literals(self):
        self.assertEqual(self.render("a{{ name }}b{{ name }}c", name="-"), "a-b-c")

    def test_parse_file_newlines_preserved(self):
        self.assertEqual(self.render("a\nb\r\nc"), "a\nb\r\nc")

    def test_parse_file_unicode(self):
        self.assertEqual(
            self.render("[{{ name }}]", name=colony.legacy.u("joão")),
            colony.legacy.u("[joão]"),
        )

    def test_parse_file_large(self):
        self.assertEqual(self.render("{{ name }}|" * 200, name="x"), "x|" * 200)

    def test_parse_file_unbalanced_end(self):
        self.assertRaises(
            exceptions.RuntimeError,
            lambda: self.parse("{% if flag %}Y{% endfor %}"),
        )

    def test_parse_file_unexpected_end(self):
        self.assertRaises(exceptions.RuntimeError, lambda: self.parse("{% endif %}"))

    def test_parse_file_unexpected_end_after_close(self):
        self.assertRaises(
            exceptions.RuntimeError,
            lambda: self.parse("{% if flag %}Y{% endif %}{% endif %}"),
        )

    def test_parse_file_invalid_tag(self):
        self.assertRaises(
            exceptions.RuntimeError, lambda: self.parse("{% bogus value %}")
        )

    def test_extension(self):
        self.assertEqual(self.engine._extension("/base/name.html.tpl"), ".html.tpl")
        self.assertEqual(self.engine._extension("/base/name.txt"), ".txt")

    def test_extension_none(self):
        self.assertEqual(self.engine._extension(None), None)

    def test_extension_missing(self):
        self.assertEqual(self.engine._extension("/base/name"), None)

    def test_extension_in(self):
        self.assertEqual(
            self.engine._extension_in(".html.tpl", system.ESCAPE_EXTENSIONS), True
        )
        self.assertEqual(
            self.engine._extension_in(".txt", system.ESCAPE_EXTENSIONS), False
        )

    def test_extension_in_none(self):
        self.assertEqual(
            self.engine._extension_in(None, system.ESCAPE_EXTENSIONS), False
        )


class AstTestCase(TemplateEngineBaseTestCase):
    """
    Test case for the abstract syntax tree module, covering both
    the module level utilities and the various node classes.
    """

    @staticmethod
    def get_description():
        return "Template engine abstract syntax tree test case"

    def test_ast_node_repr(self):
        node = ast.AstNode()
        self.assertEqual(repr(node), "<ast>")

    def test_ast_node_switch(self):
        parent = ast.AstNode()
        original = ast.AstNode()
        replacement = ast.AstNode()
        parent.add_child(original)
        original.switch(replacement)
        self.assertEqual(parent.children, [replacement])
        self.assertEqual(replacement.parent, parent)
        self.assertEqual(replacement.super, original)

    def test_ast_node_clone(self):
        node = ast.AstNode()
        child = ast.AstNode()
        node.add_child(child)

        clone = node.clone()
        self.assertEqual(len(clone.children), 1)
        self.assertEqual(clone is node, False)
        self.assertEqual(clone.children[0] is child, False)
        self.assertEqual(clone.children[0].parent is clone, True)

    def test_ast_node_clone_isolated(self):
        node = ast.AstNode()
        node.add_child(ast.AstNode())

        clone = node.clone()
        clone.add_child(ast.AstNode())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(len(clone.children), 2)

    def test_ast_node_clone_deep(self):
        node = ast.AstNode()
        child = ast.AstNode()
        grand_child = ast.AstNode()
        node.add_child(child)
        child.add_child(grand_child)

        clone = node.clone()
        self.assertEqual(clone.children[0].children[0] is grand_child, False)
        self.assertEqual(
            clone.children[0].children[0].parent is clone.children[0], True
        )

    def test_ast_node_clone_nodes(self):
        template_file = self.parse(
            "{% block first %}a{% endblock %}{% block second %}b{% endblock %}"
        )
        nodes = dict()
        clone = template_file.root_node.clone(nodes=nodes)
        self.assertEqual(sorted(nodes.keys()), ["first", "second"])
        self.assertEqual(nodes["first"] in clone.children, True)

    def test_ast_node_clone_attributes_isolated(self):
        template_file = self.parse("{{ name }}")
        node = template_file.root_node.children[0]
        clone = template_file.root_node.clone().children[0]

        self.assertEqual(clone.attributes is node.attributes, False)
        clone.attributes["xml_escape"] = False
        self.assertEqual(node.attributes["xml_escape"], True)

    def test_ast_node_clone_shares_value(self):
        node = ast.LiteralNode(value="value")
        clone = node.clone()
        self.assertEqual(clone.value, "value")
        self.assertEqual(clone.get_type(), "literal")

    def test_ast_node_add_remove_child(self):
        node = ast.AstNode()
        child = ast.AstNode()
        node.add_child(child)
        self.assertEqual(node.children, [child])
        self.assertEqual(child.parent, node)
        node.remove_child(child)
        self.assertEqual(node.children, [])
        self.assertEqual(child.parent, None)

    def test_root_node_accept_extends(self):
        template_file = self.parse(
            "{% extends 'base.html.tpl' %}{% block c %}CHILD{% endblock %}",
            files={"base.html.tpl": "<{% block c %}BASE{% endblock %}>"},
        )
        template_file.load_visitor()
        template_file.root_node.accept_extends(template_file.visitor)
        types = [child.get_type() for child in template_file.root_node.children]
        self.assertEqual(types, ["literal", "block", "literal"])
        self.assertEqual(template_file.visitor.string_buffer.get_value(), b"")

    def test_root_node_accept_extends_without_extends(self):
        template_file = self.parse("plain contents")
        template_file.load_visitor()
        template_file.root_node.accept_extends(template_file.visitor)
        self.assertEqual(template_file.visitor.string_buffer.get_value(), b"")

    def test_root_node_accept_extends_not_first(self):
        # an extends node that is not the first child of the root is not
        # able to be resolved and so it's simply skipped in the visit
        self.assertEqual(
            self.render(
                "head{% extends 'base.html.tpl' %}",
                files={"base.html.tpl": "<BASE>"},
            ),
            "head",
        )

    def test_root_node_type(self):
        self.assertEqual(ast.RootNode().get_type(), "root")

    def test_literal_node_type(self):
        self.assertEqual(ast.LiteralNode().get_type(), "literal")

    def test_simple_node_parse_quoted_single(self):
        node = ast.OutputNode(value="{{ 'john' }}")
        self.assertEqual(node.attributes["value"]["value"], "john")
        self.assertEqual(node.attributes["value"]["type"], "literal")

    def test_simple_node_parse_quoted_double(self):
        node = ast.OutputNode(value='{{ "john" }}')
        self.assertEqual(node.attributes["value"]["value"], "john")

    def test_simple_node_parse_float(self):
        node = ast.OutputNode(value="{{ 1.5 }}")
        self.assertEqual(node.attributes["value"]["value"], 1.5)

    def test_simple_node_parse_integer(self):
        node = ast.OutputNode(value="{{ 12 }}")
        self.assertEqual(node.attributes["value"]["value"], 12)

    def test_simple_node_parse_boolean(self):
        node = ast.OutputNode(value="{{ True }}")
        self.assertEqual(node.attributes["value"]["value"], True)
        node = ast.OutputNode(value="{{ False }}")
        self.assertEqual(node.attributes["value"]["value"], False)

    def test_simple_node_parse_none(self):
        node = ast.OutputNode(value="{{ None }}")
        self.assertEqual(node.attributes["value"]["value"], None)

    def test_simple_node_parse_variable(self):
        node = ast.OutputNode(value="{{ name|e }}")
        attribute = node.attributes["value"]
        self.assertEqual(attribute["type"], "variable")
        self.assertEqual(attribute["value"], "name|e")
        self.assertEqual(attribute["original"], "name|e")

    def test_simple_node_parse_empty(self):
        node = ast.OutputNode(value="{{}}")
        self.assertEqual(node.attributes["value"], "")

    def test_eval_node_invalid_tag(self):
        self.assertRaises(
            exceptions.RuntimeError, lambda: ast.EvalNode(value="{% bogus %}")
        )

    def test_eval_node_is_end(self):
        self.assertEqual(ast.EvalNode(value="{% endif %}").is_end(), True)
        self.assertEqual(ast.EvalNode(value="{% if flag %}").is_end(), False)

    def test_eval_node_is_open(self):
        self.assertEqual(ast.EvalNode(value="{% if flag %}").is_open(), True)
        self.assertEqual(ast.EvalNode(value="{% for i in l %}").is_open(), True)
        self.assertEqual(ast.EvalNode(value="{% block c %}").is_open(), True)
        self.assertEqual(ast.EvalNode(value="{% else %}").is_open(), False)

    def test_eval_node_assert_end(self):
        node = ast.EvalNode(value="{% endif %}")
        self.assertEqual(node.assert_end("if"), None)
        self.assertRaises(exceptions.RuntimeError, lambda: node.assert_end("for"))

    def test_eval_node_process_if_simple(self):
        node = ast.EvalNode(value="{% if flag %}")
        self.assertEqual(node.attributes["item"]["value"], "flag")
        self.assertEqual(node.attributes["operator"]["value"], None)

    def test_eval_node_process_if_negated(self):
        node = ast.EvalNode(value="{% if not flag %}")
        self.assertEqual(node.attributes["operator"]["value"], "not")

    def test_eval_node_process_if_complex(self):
        node = ast.EvalNode(value="{% if name == 'john' %}")
        self.assertEqual(node.attributes["item"]["value"], "name")
        self.assertEqual(node.attributes["value"]["value"], "john")
        self.assertEqual(node.attributes["operator"]["value"], "eq")

    def test_eval_node_process_if_in_swaps_operands(self):
        node = ast.EvalNode(value="{% if 'a' in items %}")
        self.assertEqual(node.attributes["item"]["value"], "items")
        self.assertEqual(node.attributes["value"]["value"], "a")
        self.assertEqual(node.attributes["operator"]["value"], "in")

    def test_eval_node_process_if_not_in_swaps_operands(self):
        node = ast.EvalNode(value="{% if not 'a' in items %}")
        self.assertEqual(node.attributes["item"]["value"], "items")
        self.assertEqual(node.attributes["value"]["value"], "a")
        self.assertEqual(node.attributes["operator"]["value"], "nin")

    def test_eval_node_process_if_malformed(self):
        self.assertRaises(
            exceptions.RuntimeError, lambda: ast.EvalNode(value="{% if %}")
        )

    def test_eval_node_process_for_simple(self):
        node = ast.EvalNode(value="{% for item in items %}")
        self.assertEqual(node.attributes["key"]["value"], "item")
        self.assertEqual(node.attributes["from"]["value"], "items")

    def test_eval_node_process_for_complex(self):
        node = ast.EvalNode(value="{% for key, value in map %}")
        self.assertEqual(node.attributes["key"]["value"], "key")
        self.assertEqual(node.attributes["item"]["value"], "value")
        self.assertEqual(node.attributes["from"]["value"], "map")

    def test_eval_node_process_set(self):
        node = ast.EvalNode(value="{% set name = 'john' %}")
        self.assertEqual(node.attributes["item"]["value"], "name")
        self.assertEqual(node.attributes["value"]["value"], "john")

    def test_eval_node_process_set_malformed(self):
        self.assertRaises(
            exceptions.RuntimeError, lambda: ast.EvalNode(value="{% set name %}")
        )

    def test_match_node_process_attributes(self):
        template_file = self.parse("${out value=name format='%s' count=3 /}")
        node = template_file.root_node.children[0]
        attributes = node.get_attributes()
        self.assertEqual(attributes["value"]["type"], "variable")
        self.assertEqual(attributes["value"]["value"], "name")
        self.assertEqual(attributes["format"]["type"], "literal")
        self.assertEqual(attributes["format"]["value"], "%s")
        self.assertEqual(attributes["count"]["value"], 3)

    def test_match_node_get_id(self):
        template_file = self.parse("{% block content %}x{% endblock %}")
        node = template_file.root_node.children[0]
        self.assertEqual(node.get_id(), "content")


class TemplateFileTestCase(TemplateEngineBaseTestCase):
    """
    Test case for the template file structure, the most abstract
    representation of a template and the entry point for the user
    level operations.
    """

    @staticmethod
    def get_description():
        return "Template engine template file test case"

    def test_format(self):
        self.assertEqual(system.TemplateFile.format("%s-%s", "a", "b"), "a-b")

    def test_format_invalid(self):
        self.assertEqual(system.TemplateFile.format("%d", "a"), None)

    def test_convert_invalid_mode(self):
        self.assertEqual(system.TemplateFile.convert("value", "bogus"), "value")

    def test_index_nodes(self):
        template_file = self.parse("{% block content %}x{% endblock %}")
        self.assertEqual("content" in template_file.nodes, True)

    def test_index_nodes_nested(self):
        template_file = self.parse(
            "{% for i in items %}{% block inner %}x{% endblock %}{% endfor %}"
        )
        self.assertEqual("inner" in template_file.nodes, True)

    def test_index_nodes_provided(self):
        # when the indexed nodes are provided no indexing operation should
        # be performed, the provided map is used as is
        root_node = ast.RootNode()
        nodes = dict(provided=root_node)
        template_file = system.TemplateFile(root_node=root_node, nodes=nodes)
        self.assertEqual(template_file.nodes is nodes, True)

    def test_assign(self):
        template_file = self.parse("[{{ name }}]")
        template_file.assign("name", "john")
        self.assertEqual(template_file.process(), "[john]")

    def test_set_global_map(self):
        template_file = self.parse("[{{ name }}]")
        template_file.set_global_map(dict(name="john"))
        self.assertEqual(template_file.process(), "[john]")

    def test_set_string_buffer(self):
        template_file = self.parse("contents")
        buffer = colony.StringBuffer()
        template_file.set_string_buffer(buffer)
        template_file.process()
        self.assertEqual(buffer.get_value(), b"contents")

    def test_attach_process_methods(self):
        def process_custom(self, node):
            self.write("custom")

        template_file = self.parse("${custom /}")
        template_file.attach_process_methods([("process_custom", process_custom)])
        self.assertEqual(template_file.process(), "custom")

    def test_load_system_variable(self):
        template_file = self.parse("[{{ _system.name }}]")
        self.assertEqual(template_file.process(), "[mock]")

    def test_process_repeated(self):
        template_file = self.parse(
            "{% extends 'base.html.tpl' %}{% block c %}{{ name }}{% endblock %}",
            files={"base.html.tpl": "<{% block c %}BASE{% endblock %}>"},
        )
        template_file.assign("name", "john")
        first = template_file.process()
        template_file.visitor.string_buffer = colony.StringBuffer()
        second = template_file.process()
        self.assertEqual(first, "<john>")
        self.assertEqual(second, first)

    def test_variable_encoding(self):
        template_file = self.parse("[{{ name }}]", file_name="test.txt")
        template_file.set_variable_encoding("utf-8")
        template_file.assign("name", colony.legacy.u("joão"))
        self.assertEqual(template_file.get_variable_encoding(), "utf-8")
        self.assertEqual(template_file.process(), colony.legacy.u("[joão]"))

    def test_strict_mode(self):
        template_file = self.parse("[{{ name }}]")
        template_file.set_strict_mode(True)
        self.assertEqual(template_file.get_strict_mode(), True)
        self.assertRaises(exceptions.UndefinedVariable, template_file.process)

    def test_add_bundle(self):
        template_file = self.parse("[{{ 'hello'|locale }}]")
        template_file.add_bundle(dict(hello="ola"))
        self.assertEqual(template_file.process(), "[ola]")


class VisitorTestCase(TemplateEngineBaseTestCase):
    """
    Test case for the visitor, covering the dispatch infra-structure
    and the various process (tag) methods of it.
    """

    @staticmethod
    def get_description():
        return "Template engine visitor test case"

    def test_escape_literal(self):
        self.assertEqual(visitor.escape_literal("plain"), "plain")

    def test_escape_literal_sequence(self):
        # the escaping removes the two backslashes that "protect" the tag
        # sequence, meaning that at least three of them are required
        self.assertEqual(
            visitor.escape_literal("$" + "\\" * 3 + "{out /}"),
            "$" + "\\" + "{out /}",
        )
        self.assertEqual(
            visitor.escape_literal("$" + "\\" * 4 + "{out /}"),
            "$" + "\\" * 2 + "{out /}",
        )

    def test_escape_literal_untouched(self):
        self.assertEqual(
            visitor.escape_literal("$" + "\\" + "{out /}"),
            "$" + "\\" + "{out /}",
        )

    def test_escape_literal_at_parse(self):
        # the escaping of the literal values is performed at parse time and
        # so the value held by the node must already be the escaped one
        template_file = self.parse("$" + "\\" * 3 + "{out /}")
        node = template_file.root_node.children[0]
        self.assertEqual(node.value.value, "$" + "\\" + "{out /}")

    def test_split_filters(self):
        self.assertEqual(visitor.split_filters("name"), ("name", ()))

    def test_split_filters_single(self):
        self.assertEqual(visitor.split_filters("name|e"), ("name", ("e",)))

    def test_split_filters_multiple(self):
        self.assertEqual(visitor.split_filters("name|e|safe"), ("name", ("e", "safe")))

    def test_split_filters_spaces(self):
        self.assertEqual(visitor.split_filters("  name  |  e  "), ("name", ("e",)))

    def test_split_filters_empty(self):
        self.assertEqual(visitor.split_filters(""), ("", ()))

    def test_split_filters_invalid(self):
        self.assertEqual(visitor.split_filters(None), (None, ()))
        self.assertEqual(visitor.split_filters(12), (12, ()))

    def test_split_arguments(self):
        self.assertEqual(visitor.split_arguments("a,b"), ["a", "b"])

    def test_split_arguments_single(self):
        self.assertEqual(visitor.split_arguments("a"), ["a"])

    def test_split_arguments_quoted(self):
        self.assertEqual(visitor.split_arguments("','"), ["','"])

    def test_split_arguments_quoted_double(self):
        self.assertEqual(visitor.split_arguments('",",a'), ['","', "a"])

    def test_split_arguments_mixed(self):
        self.assertEqual(
            visitor.split_arguments("name='a,b',count=2"), ["name='a,b'", "count=2"]
        )

    def test_split_arguments_empty(self):
        self.assertEqual(visitor.split_arguments(""), [""])

    def test_node_method_map(self):
        map = visitor.node_method_map(visitor.Visitor)
        self.assertEqual(ast.LiteralNode in map, True)
        self.assertEqual(ast.RootNode in map, True)

    def test_node_method_map_cached(self):
        first = visitor.node_method_map(visitor.Visitor)
        second = visitor.node_method_map(visitor.Visitor)
        self.assertEqual(first is second, True)

    def test_attach_process_method_invalidates_cache(self):
        def process_out(self, node):
            self.write("replaced")

        template_file = self.parse("[{{ name }}]")
        template_file.assign("name", "john")
        template_file.process()
        template_file.visitor.attach_process_method("process_out", process_out)
        self.assertEqual(template_file.visitor.process_map, dict())

    def test_add_filter(self):
        template_file = self.parse("[{{ name|shout }}]")
        template_file.visitor.add_filter("shout", lambda v, a, t: v.upper())
        template_file.assign("name", "john")
        self.assertEqual(template_file.process(), "[JOHN]")

    def test_add_filter_isolated(self):
        # the default filters map is shared between the various visitor
        # instances and so a new filter must not leak into the other ones
        instance = visitor.Visitor()
        instance.add_filter("shout", lambda v, a, t: v.upper())
        self.assertEqual("shout" in instance.filters, True)
        self.assertEqual("shout" in visitor.FILTERS, False)
        self.assertEqual("shout" in visitor.Visitor().filters, False)

    def test_visit_default(self):
        class BogusNode(ast.AstNode):
            def get_type(self):
                return "bogus"

        instance = visitor.Visitor()
        instance.node_method_map = dict()
        instance.visit_map = dict()
        self.assertEqual(instance.visit(BogusNode()), None)

    def test_visit_literal_node(self):
        self.assertEqual(self.render("literal"), "literal")

    def test_process_accept_invalid_tag(self):
        self.assertRaises(
            exceptions.InvalidTagName, lambda: self.render("${bogus value=1 /}")
        )

    def test_process_accept_cached(self):
        template_file = self.parse("[{{ a }}][{{ b }}]")
        template_file.assign("a", "x")
        template_file.process()
        self.assertEqual("out" in template_file.visitor.process_map, True)

    def test_process_out(self):
        self.assertEqual(self.render("[{{ name }}]", name="john"), "[john]")

    def test_process_out_undefined(self):
        self.assertEqual(self.render("[{{ missing }}]"), "[]")

    def test_process_out_number(self):
        self.assertEqual(self.render("[{{ value }}]", value=42), "[42]")

    def test_process_out_none(self):
        self.assertEqual(self.render("[{{ None }}]"), "[]")

    def test_process_out_attribute(self):
        entity = mocks.MockEntity(name="john")
        self.assertEqual(self.render("[{{ entity.name }}]", entity=entity), "[john]")

    def test_process_out_nested_attribute(self):
        entity = mocks.MockEntity(name="john", child=mocks.MockEntity(name="kid"))
        self.assertEqual(
            self.render("[{{ entity.child.name }}]", entity=entity), "[kid]"
        )

    def test_process_out_map(self):
        self.assertEqual(
            self.render("[{{ map.key }}]", map=dict(key="value")), "[value]"
        )

    def test_process_out_method(self):
        entity = mocks.MockEntity(name="john")
        self.assertEqual(
            self.render("[{{ entity.get_name() }}]", entity=entity), "[john]"
        )

    def test_process_out_method_arguments(self):
        entity = mocks.MockEntity(name="john")
        self.assertEqual(
            self.render("[{{ entity.upper_name('x') }}]", entity=entity), "[JOHNx]"
        )

    def test_process_out_method_named_arguments(self):
        entity = mocks.MockEntity(name="john")
        self.assertEqual(
            self.render("[{{ entity.upper_name(prefix='x') }}]", entity=entity),
            "[xJOHN]",
        )

    def test_process_out_method_special_arguments(self):
        entity = mocks.MockEntity(name="john")
        self.assertEqual(
            self.render("[{{ entity.upper_name('!') }}]", entity=entity), "[JOHN!]"
        )

    def test_process_out_auto_escape(self):
        self.assertEqual(
            self.render("[{{ raw }}]", raw="<b>&</b>"), "[&lt;b&gt;&amp;&lt;/b&gt;]"
        )

    def test_process_out_auto_escape_quote(self):
        self.assertEqual(self.render("[{{ raw }}]", raw='"'), "[&quot;]")

    def test_process_out_no_auto_escape(self):
        self.assertEqual(
            self.render("[{{ raw }}]", file_name="test.txt", raw="<b>&</b>"),
            "[<b>&</b>]",
        )

    def test_process_out_xml_escape(self):
        self.assertEqual(
            self.render(
                "[${out value=raw xml_escape=True /}]", file_name="test.txt", raw="<b>"
            ),
            "[&lt;b&gt;]",
        )

    def test_process_out_xml_quote_disabled(self):
        self.assertEqual(
            self.render(
                "[${out value=raw xml_escape=True xml_quote=False /}]",
                file_name="test.txt",
                raw='"',
            ),
            '["]',
        )

    def test_process_out_prefix(self):
        self.assertEqual(
            self.render("[${out value=name prefix='>' /}]", name="john"), "[>john]"
        )

    def test_process_out_variable_encoding(self):
        # uses a prefix so that the complete (non simplified) processing
        # path of the out operation is the one being exercised
        template_file = self.parse(
            "[${out value=name prefix='>' /}]", file_name="test.txt"
        )
        template_file.set_variable_encoding("utf-8")
        template_file.assign("name", colony.legacy.u("joão"))
        self.assertEqual(template_file.process(), colony.legacy.u("[>joão]"))

    def test_process_out_default(self):
        self.assertEqual(self.render("[${out value=missing default='d' /}]"), "[d]")

    def test_process_out_quote(self):
        self.assertEqual(
            self.render("[${out value=name quote=True /}]", name="a b"), "[a%20b]"
        )

    def test_process_out_format(self):
        self.assertEqual(
            self.render("[${out value=value format='%03d' /}]", value=7), "[007]"
        )

    def test_process_out_serializer(self):
        self.assertEqual(
            self.render(
                "[${out value=items serializer=json /}]",
                file_name="test.txt",
                items=[1, 2],
            ),
            "[[1, 2]]",
        )

    def test_process_out_sequence(self):
        self.assertEqual(
            self.render("[{{ items }}]", file_name="test.txt", items=["a", "b"]),
            "[['a', 'b']]",
        )

    def test_process_out_invalid_boolean(self):
        self.assertRaises(
            exceptions.InvalidBooleanValue,
            lambda: self.render("${out value=name quote='x' /}", name="john"),
        )

    def test_process_set(self):
        self.assertEqual(self.render("{% set name = 'john' %}[{{ name }}]"), "[john]")

    def test_process_set_from_variable(self):
        self.assertEqual(
            self.render("{% set copy = name %}[{{ copy }}]", name="john"), "[john]"
        )

    def test_process_foreach_sequence(self):
        self.assertEqual(
            self.render("{% for i in items %}[{{ i }}]{% endfor %}", items=["a", "b"]),
            "[a][b]",
        )

    def test_process_foreach_empty(self):
        self.assertEqual(self.render("{% for i in items %}X{% endfor %}", items=[]), "")

    def test_process_foreach_map(self):
        self.assertEqual(
            self.render(
                "{% for k, v in map %}[{{ k }}={{ v }}]{% endfor %}", map=dict(a="1")
            ),
            "[a=1]",
        )

    def test_process_foreach_loop_index(self):
        self.assertEqual(
            self.render(
                "{% for i in items %}{{ loop.index }}{% endfor %}",
                items=["a", "b", "c"],
            ),
            "123",
        )

    def test_process_foreach_loop_first_last(self):
        self.assertEqual(
            self.render(
                "{% for i in items %}{{ loop.first }}/{{ loop.last }};{% endfor %}",
                items=["a", "b"],
            ),
            "True/False;False/True;",
        )

    def test_process_foreach_is_first(self):
        self.assertEqual(
            self.render(
                "{% for i in items %}{{ is_first }};{% endfor %}", items=["a", "b"]
            ),
            "True;False;",
        )

    def test_process_foreach_non_iterable(self):
        self.assertEqual(
            self.render("{% for i in value %}[{{ i }}]{% endfor %}", value=5), "[5]"
        )

    def test_process_foreach_undefined(self):
        self.assertEqual(self.render("{% for i in missing %}[{{ i }}]{% endfor %}"), "")

    def test_process_foreach_strict_non_iterable(self):
        self.assertRaises(
            exceptions.VariableNotIterable,
            lambda: self.render(
                "{% for i in value %}X{% endfor %}", strict=True, value=5
            ),
        )

    def test_process_foreach_nested(self):
        self.assertEqual(
            self.render(
                "{% for i in a %}{% for j in b %}{{ i }}{{ j }}{% endfor %}{% endfor %}",
                a=["1", "2"],
                b=["x"],
            ),
            "1x2x",
        )

    def test_process_foreach_composite_index(self):
        self.assertEqual(
            self.render(
                "${foreach item=i from=items index=idx}"
                "[${out value=idx /}:${out value=i /}]"
                "${/foreach}",
                items=["a", "b"],
            ),
            "[1:a][2:b]",
        )

    def test_process_foreach_composite_start_index(self):
        self.assertEqual(
            self.render(
                "${foreach item=i from=items index=idx start_index='5'}"
                "[${out value=idx /}]"
                "${/foreach}",
                items=["a", "b"],
            ),
            "[5][6]",
        )

    def test_process_foreach_composite_start_index_integer(self):
        self.assertEqual(
            self.render(
                "${foreach item=i from=items index=idx start_index=5}"
                "[${out value=idx /}]"
                "${/foreach}",
                items=["a", "b"],
            ),
            "[5][6]",
        )

    def test_process_foreach_composite_start_index_zero(self):
        self.assertEqual(
            self.render(
                "${foreach item=i from=items index=idx start_index=0}"
                "[${out value=idx /}]"
                "${/foreach}",
                items=["a", "b"],
            ),
            "[0][1]",
        )

    def test_process_foreach_start_index_first_last(self):
        # the first and last flags must follow the position of the iteration
        # and not the (visible) index, that may start at any value
        self.assertEqual(
            self.render(
                "${foreach item=i from=items start_index=5}"
                "[${out value=loop.first /}/${out value=loop.last /}]"
                "${/foreach}",
                items=["a", "b"],
            ),
            "[True/False][False/True]",
        )

    def test_process_foreach_nested_loop_restored(self):
        # the loop related values of an outer loop must not be affected
        # by the execution of an inner (nested) loop
        self.assertEqual(
            self.render(
                "{% for i in a %}"
                "{% for j in b %}{{ loop.index }}{% endfor %}"
                "-{{ loop.index }};"
                "{% endfor %}",
                a=["x", "y"],
                b=["1", "2", "3"],
            ),
            "123-1;123-2;",
        )

    def test_process_foreach_nested_is_first_restored(self):
        self.assertEqual(
            self.render(
                "{% for i in a %}"
                "{% for j in b %}{% endfor %}"
                "{{ is_first }};"
                "{% endfor %}",
                a=["x", "y"],
                b=["1", "2"],
            ),
            "True;False;",
        )

    def test_process_foreach_loop_cleared(self):
        # after the loop has finished the loop related values must no
        # longer be exposed to the template
        self.assertEqual(
            self.render(
                "{% for i in items %}{% endfor %}[{{ loop.index }}]", items=["a"]
            ),
            "[]",
        )

    def test_process_foreach_composite(self):
        self.assertEqual(
            self.render(
                "${foreach item=i from=items}[${out value=i /}]${/foreach}",
                items=["a", "b"],
            ),
            "[a][b]",
        )

    def test_process_if_true(self):
        self.assertEqual(self.render("{% if flag %}Y{% endif %}", flag=True), "Y")

    def test_process_if_false(self):
        self.assertEqual(self.render("{% if flag %}Y{% endif %}", flag=False), "")

    def test_process_if_undefined(self):
        self.assertEqual(self.render("{% if missing %}Y{% else %}N{% endif %}"), "N")

    def test_process_if_else(self):
        self.assertEqual(
            self.render("{% if flag %}Y{% else %}N{% endif %}", flag=False), "N"
        )

    def test_process_if_elif(self):
        self.assertEqual(
            self.render(
                "{% if a %}A{% elif b %}B{% else %}C{% endif %}", a=False, b=True
            ),
            "B",
        )

    def test_process_if_elif_fallthrough(self):
        self.assertEqual(
            self.render(
                "{% if a %}A{% elif b %}B{% else %}C{% endif %}", a=False, b=False
            ),
            "C",
        )

    def test_process_if_elif_first_wins(self):
        self.assertEqual(
            self.render(
                "{% if a %}A{% elif b %}B{% else %}C{% endif %}", a=True, b=True
            ),
            "A",
        )

    def test_process_if_equals(self):
        self.assertEqual(
            self.render("{% if name == 'john' %}Y{% else %}N{% endif %}", name="john"),
            "Y",
        )

    def test_process_if_not_equals(self):
        self.assertEqual(
            self.render("{% if name == 'john' %}Y{% else %}N{% endif %}", name="mary"),
            "N",
        )

    def test_process_if_not(self):
        self.assertEqual(self.render("{% if not flag %}Y{% endif %}", flag=False), "Y")

    def test_process_if_greater(self):
        self.assertEqual(self.render("{% if value > 2 %}Y{% endif %}", value=3), "Y")

    def test_process_if_greater_false(self):
        self.assertEqual(self.render("{% if value > 2 %}Y{% endif %}", value=1), "")

    def test_process_if_lesser(self):
        self.assertEqual(self.render("{% if value < 2 %}Y{% endif %}", value=1), "Y")

    def test_process_if_in_sequence(self):
        self.assertEqual(
            self.render("{% if 'a' in items %}Y{% else %}N{% endif %}", items=["a"]),
            "Y",
        )

    def test_process_if_in_sequence_missing(self):
        self.assertEqual(
            self.render("{% if 'z' in items %}Y{% else %}N{% endif %}", items=["a"]),
            "N",
        )

    def test_process_if_not_in_sequence(self):
        self.assertEqual(
            self.render(
                "{% if not 'z' in items %}Y{% else %}N{% endif %}", items=["a"]
            ),
            "Y",
        )

    def test_process_if_not_in_empty_sequence(self):
        self.assertEqual(
            self.render("{% if not 'z' in items %}Y{% else %}N{% endif %}", items=[]),
            "Y",
        )

    def test_process_if_not_in_undefined(self):
        self.assertEqual(
            self.render("{% if not 'z' in missing %}Y{% else %}N{% endif %}"), "N"
        )

    def test_process_if_in_empty_sequence(self):
        self.assertEqual(
            self.render("{% if 'z' in items %}Y{% else %}N{% endif %}", items=[]), "N"
        )

    def test_process_if_nested(self):
        self.assertEqual(
            self.render("{% if a %}{% if b %}AB{% endif %}{% endif %}", a=True, b=True),
            "AB",
        )

    def test_process_if_composite(self):
        self.assertEqual(self.render("${if item=flag}Y${/if}", flag=True), "Y")

    def test_process_if_composite_operator(self):
        self.assertEqual(
            self.render("${if item=value operator=gt value=2}Y${/if}", value=3), "Y"
        )

    def test_process_cycle(self):
        self.assertEqual(
            self.render(
                "{% for i in items %}${cycle values='a,b' /}{% endfor %}",
                items=[1, 2, 3],
            ),
            "aba",
        )

    def test_process_count(self):
        self.assertEqual(
            self.render("[${count value=items /}]", items=["a", "b"]), "[2]"
        )

    def test_process_count_undefined(self):
        self.assertEqual(self.render("[${count value=missing /}]"), "[0]")

    def test_process_include(self):
        self.assertEqual(
            self.render(
                "[{% include 'part.html.tpl' %}]",
                files={"part.html.tpl": "PART {{ name }}"},
                name="john",
            ),
            "[PART john]",
        )

    def test_process_include_nested(self):
        self.assertEqual(
            self.render(
                "[{% include 'outer.html.tpl' %}]",
                files={
                    "outer.html.tpl": "<{% include 'inner.html.tpl' %}>",
                    "inner.html.tpl": "IN",
                },
            ),
            "[<IN>]",
        )

    def test_process_include_undefined_reference(self):
        self.assertRaises(
            exceptions.UndefinedReference,
            lambda: self.render("{% include missing %}"),
        )

    def test_process_include_missing_file(self):
        self.assertRaises(
            exceptions.RuntimeError,
            lambda: self.render("{% include 'missing.html.tpl' %}"),
        )

    def test_process_extends(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}{% block c %}CHILD{% endblock %}",
                files={"base.html.tpl": "<{% block c %}BASE{% endblock %}>"},
            ),
            "<CHILD>",
        )

    def test_process_extends_without_block(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}", files={"base.html.tpl": "<BASE>"}
            ),
            "<BASE>",
        )

    def test_process_extends_multiple_blocks(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}"
                "{% block a %}A2{% endblock %}"
                "{% block b %}B2{% endblock %}",
                files={
                    "base.html.tpl": "{% block a %}A1{% endblock %}"
                    "-{% block b %}B1{% endblock %}"
                },
            ),
            "A2-B2",
        )

    def test_process_extends_parent_contents(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}{% block c %}CHILD{% endblock %}",
                files={"base.html.tpl": "head-{% block c %}BASE{% endblock %}-tail"},
            ),
            "head-CHILD-tail",
        )

    def test_process_extends_parent_variables(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}{% block c %}{{ name }}{% endblock %}",
                files={"base.html.tpl": "{{ title }}:{% block c %}BASE{% endblock %}"},
                title="T",
                name="N",
            ),
            "T:N",
        )

    def test_process_extends_parent_loop(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}{% block c %}C{% endblock %}",
                files={
                    "base.html.tpl": "{% for i in items %}{{ i }}{% endfor %}"
                    "{% block c %}BASE{% endblock %}"
                },
                items=["a", "b"],
            ),
            "abC",
        )

    def test_process_extends_parent_include(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}{% block c %}CHILD{% endblock %}",
                files={
                    "base.html.tpl": "{% include 'part.html.tpl' %}"
                    "<{% block c %}BASE{% endblock %}>",
                    "part.html.tpl": "PART-",
                },
            ),
            "PART-<CHILD>",
        )

    def test_process_extends_chain(self):
        self.assertEqual(
            self.render(
                "{% extends 'middle.html.tpl' %}{% block c %}CHILD{% endblock %}",
                files={
                    "middle.html.tpl": "{% extends 'base.html.tpl' %}"
                    "{% block b %}MIDDLE{% endblock %}",
                    "base.html.tpl": "[{% block b %}BASE-B{% endblock %}]"
                    "<{% block c %}BASE-C{% endblock %}>",
                },
            ),
            "[MIDDLE]<CHILD>",
        )

    def test_process_block_super(self):
        self.assertEqual(
            self.render(
                "{% extends 'base.html.tpl' %}{% block c %}[{{ super() }}]{% endblock %}",
                files={"base.html.tpl": "<{% block c %}BASE{% endblock %}>"},
            ),
            "<[BASE]>",
        )

    def test_process_uuid(self):
        self.assertEqual(len(self.render("${uuid /}")), 36)

    def test_process_year(self):
        year = datetime.datetime.now().strftime("%Y")
        self.assertEqual(self.render("${year /}"), year)

    def test_process_date(self):
        year = datetime.datetime.now().strftime("%Y")
        self.assertEqual(self.render("${date format='%Y' /}"), year)

    def test_process_time(self):
        self.assertEqual(len(self.render("${time format='%H' /}")), 2)

    def test_process_datetime(self):
        year = datetime.datetime.now().strftime("%Y")
        self.assertEqual(self.render("${datetime format='%Y' /}"), year)

    def test_process_format_datetime(self):
        value = datetime.datetime(2020, 1, 2)
        self.assertEqual(
            self.render("${format_datetime value=value format='%Y' /}", value=value),
            "2020",
        )

    def test_process_format_datetime_default(self):
        self.assertEqual(
            self.render("${format_datetime value=missing format='%Y' default='-' /}"),
            "-",
        )

    def test_process_format_timestamp(self):
        self.assertEqual(
            self.render("${format_timestamp value=value format='%Y' /}", value=0),
            "1970",
        )

    def test_process_timestamp(self):
        value = datetime.datetime(2020, 1, 2)
        self.assertEqual(
            self.render("${timestamp value=value /}", value=value), "1577923200"
        )


class VisitorResolutionTestCase(TemplateEngineBaseTestCase):
    """
    Test case for the value resolution infra-structure of the
    visitor, including the filters and the localization support.
    """

    @staticmethod
    def get_description():
        return "Template engine visitor resolution test case"

    def test_get_value_invalid(self):
        instance = visitor.Visitor()
        self.assertEqual(instance.get_value(None, default="d"), "d")

    def test_get_value_external_attribute(self):
        instance = visitor.Visitor()
        instance.set_global("name", "john")
        attribute = dict(value=None, original="name", type="variable")
        self.assertEqual(instance.get_value(attribute), "john")
        self.assertEqual(attribute["base"], "name")
        self.assertEqual(attribute["filters"], ())

    def test_get_value_none_variable(self):
        instance = visitor.Visitor()
        attribute = dict(value="x", original="None", type="variable")
        self.assertEqual(instance.get_value(attribute), None)

    def test_get_literal_value(self):
        instance = visitor.Visitor()
        self.assertEqual(instance.get_literal_value(None, default="d"), "d")
        self.assertEqual(instance.get_literal_value(dict(value="v")), "v")

    def test_get_boolean_value(self):
        instance = visitor.Visitor()
        self.assertEqual(instance.get_boolean_value(None), False)
        self.assertEqual(instance.get_boolean_value(None, True), True)
        self.assertEqual(instance.get_boolean_value(True), True)
        self.assertEqual(instance.get_boolean_value(dict(value=True)), True)

    def test_get_boolean_value_invalid(self):
        instance = visitor.Visitor()
        self.assertRaises(
            exceptions.InvalidBooleanValue,
            lambda: instance.get_boolean_value(dict(value="x")),
        )

    def test_resolve_many(self):
        instance = visitor.Visitor()
        instance.set_global("entity", mocks.MockEntity(name="john"))
        self.assertEqual(instance.resolve_many("entity.name"), "john")

    def test_resolve_many_cached(self):
        instance = visitor.Visitor()
        instance.set_global("entity", mocks.MockEntity(name="john"))
        instance.resolve_many("entity.name")
        self.assertEqual("entity.name" in visitor.NAMES_CACHE, True)
        self.assertEqual(instance.resolve_many("entity.name"), "john")

    def test_resolve_many_cache_limit(self):
        # lowers the limit of the cache so that the flushing of it may be
        # verified without a large number of resolution operations
        visitor.CACHE_LIMIT = 2

        instance = visitor.Visitor()
        instance.set_global("name", "john")
        for index in range(visitor.CACHE_LIMIT + 1):
            instance.resolve_many("name_%d" % index)
        self.assertEqual(len(visitor.NAMES_CACHE), visitor.CACHE_LIMIT + 1)

        # the resolution of one more name exceeds the limit and so the
        # complete set of cached names is flushed
        self.assertEqual(instance.resolve_many("name"), "john")
        self.assertEqual(len(visitor.NAMES_CACHE), 1)

    def test_resolve_undefined(self):
        instance = visitor.Visitor()
        self.assertEqual(instance.resolve(dict(), "missing"), None)

    def test_resolve_undefined_strict(self):
        instance = visitor.Visitor()
        instance.set_strict_mode(True)
        self.assertRaises(
            exceptions.UndefinedVariable, lambda: instance.resolve(dict(), "missing")
        )

    def test_strict_mode_undefined(self):
        self.assertRaises(
            exceptions.UndefinedVariable,
            lambda: self.render("{{ missing }}", strict=True),
        )

    def test_strict_mode_defined(self):
        self.assertEqual(self.render("{{ name }}", strict=True, name="john"), "john")

    def test_resolve_builtin(self):
        year = datetime.datetime.now().strftime("%Y")
        self.assertEqual(self.render("[{{ date('%Y') }}]"), "[" + year + "]")

    def test_resolve_attribute_missing(self):
        entity = mocks.MockEntity(name="john")
        self.assertEqual(self.render("[{{ entity.missing }}]", entity=entity), "[]")

    def test_resolve_attribute_missing_strict(self):
        entity = mocks.MockEntity(name="john")
        self.assertRaises(
            exceptions.UndefinedVariable,
            lambda: self.render("{{ entity.missing }}", strict=True, entity=entity),
        )

    def test_resolve_false_value(self):
        # a value that evaluates to false must still be considered as a
        # defined one, meaning that no fallback resolution is performed
        self.assertEqual(self.render("[{{ value }}]", value=0), "[0]")
        self.assertEqual(self.render("[{{ value }}]", value=False), "[False]")

    def test_resolve_args_none(self):
        instance = visitor.Visitor()
        self.assertEqual(instance.resolve_args("method"), ())

    def test_resolve_args_literals(self):
        instance = visitor.Visitor()
        arguments = instance.resolve_args("method('a', 2, True)")
        values = [argument["value"] for argument in arguments]
        types = [argument["type"] for argument in arguments]
        self.assertEqual(values, ["a", 2, True])
        self.assertEqual(types, ["literal", "literal", "literal"])

    def test_resolve_args_named(self):
        instance = visitor.Visitor()
        arguments = instance.resolve_args("method(name='a')")
        self.assertEqual(arguments[0]["name"], "name")
        self.assertEqual(arguments[0]["value"], "a")

    def test_resolve_args_variable(self):
        instance = visitor.Visitor()
        arguments = instance.resolve_args("method(value)")
        self.assertEqual(arguments[0]["type"], "variable")
        self.assertEqual(arguments[0]["value"], "value")

    def test_resolve_args_quoted_separator(self):
        instance = visitor.Visitor()
        arguments = instance.resolve_args("method(',')")
        self.assertEqual(len(arguments), 1)
        self.assertEqual(arguments[0]["value"], ",")

    def test_resolve_args_cached(self):
        instance = visitor.Visitor()
        first = instance.resolve_args("method('a')")
        second = instance.resolve_args("method('a')")
        self.assertEqual(first is second, True)

    def test_resolve_args_cache_limit(self):
        # lowers the limit of the cache so that the flushing of it may be
        # verified without a large number of resolution operations
        visitor.CACHE_LIMIT = 2

        instance = visitor.Visitor()
        for index in range(visitor.CACHE_LIMIT + 1):
            instance.resolve_args("method_%d('a')" % index)
        self.assertEqual(len(visitor.ARGUMENTS_CACHE), visitor.CACHE_LIMIT + 1)

        # the resolution of one more call exceeds the limit and so the
        # complete set of cached arguments is flushed
        arguments = instance.resolve_args("method('a')")
        self.assertEqual(len(visitor.ARGUMENTS_CACHE), 1)
        self.assertEqual(arguments[0]["value"], "a")

    def test_is_simple(self):
        template_file = self.parse("{{ name }}")
        node = template_file.root_node.children[0]
        instance = visitor.Visitor()
        self.assertEqual(instance._is_simple(node.get_attributes()), True)

    def test_is_simple_filters(self):
        template_file = self.parse("{{ name|safe }}")
        node = template_file.root_node.children[0]
        instance = visitor.Visitor()
        self.assertEqual(instance._is_simple(node.get_attributes()), False)

    def test_is_simple_extra_attributes(self):
        template_file = self.parse("${out value=name prefix='>' /}")
        node = template_file.root_node.children[0]
        instance = visitor.Visitor()
        self.assertEqual(instance._is_simple(node.get_attributes()), False)

    def test_is_simple_no_escape_flag(self):
        template_file = self.parse("${out value=name /}")
        node = template_file.root_node.children[0]
        instance = visitor.Visitor()
        self.assertEqual(instance._is_simple(node.get_attributes()), False)

    def test_is_simple_empty_value(self):
        template_file = self.parse("{{}}")
        node = template_file.root_node.children[0]
        instance = visitor.Visitor()
        self.assertEqual(instance._is_simple(node.get_attributes()), False)

    def test_process_out_simple_undefined(self):
        self.assertEqual(self.render("[{{ missing }}]"), "[]")

    def test_process_out_simple_sequence(self):
        self.assertEqual(
            self.render("[{{ items }}]", file_name="test.txt", items=["a", "b"]),
            "[['a', 'b']]",
        )

    def test_process_out_simple_variable_encoding(self):
        template_file = self.parse("[{{ name }}]", file_name="test.txt")
        template_file.set_variable_encoding("utf-8")
        template_file.assign("name", colony.legacy.u("joão"))
        self.assertEqual(template_file.process(), colony.legacy.u("[joão]"))

    def test_process_out_simple_localized(self):
        template_file = self.parse("[{{ 'hello' }}]")
        template_file.add_bundle(dict(hello="ola"))
        self.assertEqual(template_file.process(), "[ola]")

    def test_filter_escape(self):
        self.assertEqual(
            self.render("[{{ raw|e }}]", file_name="test.txt", raw="<b>"), "[&lt;b&gt;]"
        )

    def test_filter_safe(self):
        self.assertEqual(self.render("[{{ raw|safe }}]", raw="<b>"), "[<b>]")

    def test_filter_default(self):
        self.assertEqual(self.render("[{{ missing|default('x') }}]"), "[x]")

    def test_filter_default_boolean(self):
        self.assertEqual(
            self.render("[{{ empty|default('x', True) }}]", empty=""), "[x]"
        )

    def test_filter_double(self):
        self.assertEqual(self.render("[{{ value|double }}]", value=4), "[8]")

    def test_filter_append(self):
        self.assertEqual(self.render("[{{ name|append('!') }}]", name="a"), "[a!]")

    def test_filter_prepend(self):
        self.assertEqual(
            self.render("[{{ name|prepend('>') }}]", file_name="test.txt", name="a"),
            "[>a]",
        )

    def test_filter_format(self):
        self.assertEqual(self.render("[{{ value|format('%03d') }}]", value=7), "[007]")

    def test_filter_newline_to_break(self):
        self.assertEqual(
            self.render("[{{ text|nl_to_br }}]", file_name="test.txt", text="a\nb"),
            "[a<br/>b]",
        )

    def test_filter_split(self):
        self.assertEqual(
            self.render("[{{ text|split(',') }}]", file_name="test.txt", text="a,b"),
            "[['a', 'b']]",
        )

    def test_filter_chained(self):
        self.assertEqual(
            self.render(
                "[{{ name|append('!')|prepend('>') }}]",
                file_name="test.txt",
                name="a",
            ),
            "[>a!]",
        )

    def test_filter_undefined(self):
        self.assertEqual(self.render("[{{ name|missing }}]", name="john"), "[]")

    def test_escape_literal(self):
        self.assertEqual(
            self.render("$\\{out value=name /}", name="john"), "$\\{out value=name /}"
        )

    def test_escape_literal_method(self):
        instance = visitor.Visitor()
        self.assertEqual(
            instance._escape_literal("$" + "\\" * 3 + "{out /}"),
            "$" + "\\" + "{out /}",
        )

    def test_escape_literal_rendered(self):
        self.assertEqual(
            self.render("$" + "\\" * 3 + "{out value=name /}", name="john"),
            "$" + "\\" + "{out value=name /}",
        )

    def test_resolve_locale(self):
        template_file = self.parse("[{{ 'hello'|locale }}]")
        template_file.add_bundle(dict(hello="ola"))
        self.assertEqual(template_file.process(), "[ola]")

    def test_resolve_locale_missing(self):
        template_file = self.parse("[{{ 'hello'|locale }}]")
        template_file.add_bundle(dict(other="ola"))
        self.assertEqual(template_file.process(), "[hello]")

    def test_resolve_locale_priority(self):
        template_file = self.parse("[{{ 'hello'|locale }}]")
        template_file.add_bundle(dict(hello="first"))
        template_file.add_bundle(dict(hello="second"))
        self.assertEqual(template_file.process(), "[first]")

    def test_resolve_locale_sequence(self):
        instance = visitor.Visitor()
        instance.add_bundle(dict(hello="ola"))
        self.assertEqual(instance._resolve_locale(["hello", "other"]), ["ola", "other"])

    def test_resolve_locale_invalid(self):
        instance = visitor.Visitor()
        self.assertEqual(instance._resolve_locale(None), None)
        self.assertEqual(instance._resolve_locale(12), 12)

    def test_serialize_value(self):
        instance = visitor.Visitor()
        self.assertEqual(instance._serialize_value("value"), "value")
        self.assertEqual(instance._serialize_value(["a"]), "['a']")

    def test_serialize_sequence_nested(self):
        instance = visitor.Visitor()
        self.assertEqual(instance._serialize_sequence([1, ["a"]]), "[1, ['a']]")

    def test_serialize_sequence_invalid(self):
        instance = visitor.Visitor()
        self.assertEqual(instance._serialize_sequence("value"), "value")

    def test_get_serializer(self):
        instance = visitor.Visitor()
        _serializer, name = instance._get_serializer()
        self.assertEqual(name, "json")

    def test_get_serializer_invalid(self):
        instance = visitor.Visitor()
        self.assertRaises(
            exceptions.InvalidSerializer, lambda: instance._get_serializer("bogus")
        )

    def test_loop_cycle(self):
        self.assertEqual(
            self.render(
                "{% for i in items %}{{ loop.cycle('a', 'b') }}{% endfor %}",
                items=[1, 2, 3],
            ),
            "aba",
        )


class EvalVisitorTestCase(TemplateEngineBaseTestCase):
    """
    Test case for the eval based visitor, that uses the python
    eval call for the resolution of the various values.
    """

    @staticmethod
    def get_description():
        return "Template engine eval visitor test case"

    def render_eval(self, contents, file_name="test.html.tpl", **values):
        """
        Renders the provided template contents using the eval based
        visitor instead of the default (interpreter) based one.

        :type contents: String
        :param contents: The contents of the template to be rendered.
        :type file_name: String
        :param file_name: The name of the file that is going to "hold"
        the template contents (controls the auto escaping mode).
        :rtype: String
        :return: The result of the template rendering operation.
        """

        path = self.write(file_name, contents)
        root_node = self.engine.parse_file_path(
            path, base_path=self.temp_path, encoding="utf-8"
        ).root_node
        template_file = system.TemplateFile(
            manager=self.engine,
            base_path=self.temp_path,
            file_path=path,
            encoding="utf-8",
            root_node=root_node,
            eval=True,
        )
        template_file.load_system_variable()
        template_file.load_functions()
        for key, value in colony.legacy.items(values):
            template_file.assign(key, value)
        return template_file.process()

    def test_get_value(self):
        self.assertEqual(self.render_eval("[{{ name }}]", name="john"), "[john]")

    def test_get_value_expression(self):
        self.assertEqual(self.render_eval("[{{ 1 + 2 }}]"), "[3]")

    def test_get_value_comparison(self):
        self.assertEqual(self.render_eval("[{{ 3 > 2 }}]"), "[True]")

    def test_get_value_attribute(self):
        entity = mocks.MockEntity(name="john")
        self.assertEqual(
            self.render_eval("[{{ entity.name }}]", entity=entity), "[john]"
        )

    def test_get_value_undefined(self):
        self.assertEqual(self.render_eval("[{{ missing }}]"), "[]")

    def test_get_value_filter(self):
        self.assertEqual(self.render_eval("[{{ raw|safe }}]", raw="<b>"), "[<b>]")
