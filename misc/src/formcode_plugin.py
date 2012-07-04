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

import colony.base.system

class FormcodePlugin(colony.base.system.Plugin):
    """
    The main class for the Formcode plugin.
    """

    id = "pt.hive.colony.plugins.misc.formcode"
    name = "Formcode"
    description = "A plugin to serialize and unserialize formcode files"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "serializer.formcode"
    ]
    main_modules = [
        "misc.formcode.exceptions",
        "misc.formcode.serializer",
        "misc.formcode.system"
    ]

    formcode = None
    """ The formcode """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import misc.formcode.system
        self.formcode =  misc.formcode.system.Formcode(self)

    def dumps(self, object):
        return self.formcode.dumps(object)

    def dumps_base_path(self, object, base_path):
        return self.formcode.dumps_base_path(object, base_path)

    def loads(self, formcode_string):
        return self.formcode.loads(formcode_string)

    def load_file(self, formcode_file):
        return self.formcode.load_file(formcode_file)

    def load_file_encoding(self, formcode_file, encoding):
        return self.formcode.load_file(formcode_file, encoding)

    def get_mime_type(self):
        return self.formcode.get_mime_type()
