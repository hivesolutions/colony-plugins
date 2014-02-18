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

import colony

class JinjaPlugin(colony.Plugin):
    """
    The main class for the jinja plugin responsible for
    the rendering and processing of templates based on
    the jinja 2 framework.
    """

    id = "pt.hive.colony.plugins.jinja"
    name = "Jinja Template Engine"
    description = "Jinja Template Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "template_engine"
    ]
    main_modules = [
        "jinja.system"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import jinja
        self.jinja = jinja.Jinja(self)

    def parse_file_path(self, file_path):
        return self.jinja.parse_file_path(file_path)

    def parse_file_path_encoding(self, file_path, encoding = "utf-8"):
        return self.jinja.parse_file_path(file_path, encoding = "utf-8")

    def parse_file_path_variable_encoding(
        self,
        file_path,
        encoding = "utf-8",
        variable_encoding = "utf-8"
    ):
        return self.template_engine.parse_file_path(file_path, encoding = encoding)
