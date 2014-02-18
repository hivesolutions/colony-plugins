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

import jinja2

import colony

class Jinja(colony.System):

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.loader = jinja2.FileSystemLoader(self.templates_path)
        self.jinja = jinja2.Environment(loader = self.loader)

    def parse_file_path(self, file_path, encoding = "utf-8"):
        template = colony.relative_path(file_path, self.templates_path)
        template = template.replace("\\", "/")

        template = self.jinja.get_template(template)
        template = JinjaTemplate(template)
        return template

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
        #@todo: to be implemented
        pass

    def set_variable_encoding(self, encoding):
        #@todo: to be implemented
        pass

    def attach_process_methods(self, methods):
        #@todo: to be implemented
        pass
