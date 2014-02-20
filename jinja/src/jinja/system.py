#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import jinja2

import colony

ESCAPE_EXTENSIONS = (
    ".xml",
    ".html",
    ".xhtml",
    ".xml.tpl",
    ".html.tpl",
    ".xhtml.tpl"
)
""" The sequence containing the various extensions
for which the autoescape mode will be enabled  by
default as expected by the end developer """

class Jinja(colony.System):

    def parse_file_path(self, file_path, base_path = ".", encoding = "utf-8"):
        extension = self._extension(file_path)

        loader = jinja2.FileSystemLoader(base_path)
        jinja = jinja2.Environment(
            loader = loader,
            autoescape = extension in ESCAPE_EXTENSIONS
        )

        template = colony.relative_path(file_path, base_path)
        template = template.replace("\\", "/")

        template = jinja.get_template(template)
        template = JinjaTemplate(template)
        return template

    def _extension(self, file_path):
        _head, tail = os.path.split(file_path)
        tail_s = tail.split(".", 1)
        if len(tail_s) > 1: return "." + tail_s[1]
        return None

class JinjaTemplate(object):

    def __init__(self, template):
        self.template = template
        self.values = dict()

    def process(self):
        kwargs = self.values
        return self.template.render(kwargs)

    def assign(self, key, value):
        self.values[key] = value

    def add_bundle(self, bundle):
        pass

    def set_variable_encoding(self, encoding):
        pass

    def attach_process_methods(self, methods):
        pass
