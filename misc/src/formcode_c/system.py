#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import serializer

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

MIME_TYPE = "application/x-formcode"
""" The mime type """

class Formcode(colony.System):
    """
    Provides functions to interact with formcode.
    """

    def dumps(self, object):
        return serializer.dumps(object)

    def dumps_base_path(self, object, base_path):
        return serializer.dumps(object, base_path)

    def loads(self, formcode_string):
        return serializer.loads(formcode_string)

    def load_file(self, formcode_file, encoding = DEFAULT_ENCODING):
        # reads the formcode file
        formcode_file_contents = formcode_file.read()

        # decodes the formcode file contents using the default encoder
        formcode_file_contents_decoded = formcode_file_contents.decode(encoding)

        # loads the formcode file contents
        return self.loads(formcode_file_contents_decoded)

    def get_mime_type(self):
        return MIME_TYPE
