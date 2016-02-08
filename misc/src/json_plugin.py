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

import colony

class JsonPlugin(colony.Plugin):
    """
    The main class for the Json plugin.
    """

    id = "pt.hive.colony.plugins.misc.json"
    name = "Json"
    description = "A plugin to serialize and unserialize json files"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "serializer.json"
    ]
    main_modules = [
        "json_c"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import json_c
        self.system = json_c.Json(self)

    def dumps(self, object):
        return self.system.dumps(object)

    def dumps_lazy(self, object):
        return self.system.dumps_lazy(object)

    def dumps_pretty(self, object):
        return self.system.dumps_pretty(object)

    def dumps_buffer(self, object):
        return self.system.dumps_buffer(object)

    def loads(self, json_string):
        return self.system.loads(json_string)

    def load_file(self, json_file):
        return self.system.load_file(json_file)

    def load_file_encoding(self, json_file, encoding):
        return self.system.load_file(json_file, encoding)

    def get_mime_type(self):
        return self.system.get_mime_type()
