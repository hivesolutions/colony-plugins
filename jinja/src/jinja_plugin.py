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

import colony


class JinjaPlugin(colony.Plugin):
    """
    The main class for the Jinja plugin responsible for
    the rendering and processing of templates based on
    the Jinja 2 framework.
    """

    id = "pt.hive.colony.plugins.jinja"
    name = "Jinja Template Engine"
    description = "Jinja Template Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT,
    ]
    capabilities = ["template_engine"]
    dependencies = [colony.PackageDependency("Jinja template engine", "jinja2")]
    main_modules = ["jinja"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import jinja

        self.jinja = jinja.Jinja(self)

    def parse_template(self, file_path, base_path=".", encoding="utf-8"):
        return self.jinja.parse_file_path(
            file_path, base_path=base_path, encoding=encoding
        )
