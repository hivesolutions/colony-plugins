#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import serializer

DEFAULT_ENCODING = "Cp1252"
""" The default encoding, defined according
to the most used case """

MIME_TYPE = "text/csv"
""" The mime type for the CSV format as defined
by the proper ISO organizations  """

class CSV(colony.System):
    """
    Provides functions to interact with CSV.
    These operations should include at least
    the dumping and loading of CSV.
    """

    def dumps(self, object, encoding = DEFAULT_ENCODING):
        return serializer.dumps(object, encoding = encoding)

    def dumps_lazy(self, object, encoding = DEFAULT_ENCODING):
        return serializer.dumps_lazy(object, encoding = encoding)

    def loads(self, csv_string, header = True):
        return serializer.loads(csv_string, header)

    def load_file(self, csv_file, encoding = DEFAULT_ENCODING):
        # reads the CSV file and decodes the file using
        # the defined (by parameter encoding) then runs
        # the load process for the CSV bytes buffer,
        # returning the resulting value to the caller
        csv_file_contents = csv_file.read()
        csv_file_contents_decoded = csv_file_contents.decode(encoding)
        return self.loads(csv_file_contents_decoded)

    def get_mime_type(self):
        return MIME_TYPE
