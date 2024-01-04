#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class MimeUtilsPlugin(colony.Plugin):
    """
    The main class for the Mime Format Utils plugin.
    """

    id = "pt.hive.colony.plugins.format.mime.utils"
    name = "Mime Format Utils"
    description = "The plugin that offers the mime format utils support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "format.mime.utils"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.format.mime")
    ]
    main_modules = [
        "mime_utils_c"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import mime_utils_c
        self.system = mime_utils_c.MimeUtils(self)

    def add_attachment_contents(self, mime_message, contents, file_name):
        return self.system.add_attachment_contents(mime_message, contents, file_name)

    def add_attachment_contents_mime_type(self, mime_message, contents, file_name, mime_type):
        return self.system.add_attachment_contents(mime_message, contents, file_name, mime_type)

    def add_contents(self, mime_message, contents_path, content_extensions):
        return self.system.add_contents(mime_message, contents_path, content_extensions)

    def add_contents_non_recursive(self, mime_message, contents_path, content_extensions):
        return self.system.add_contents(mime_message, contents_path, content_extensions, False)
