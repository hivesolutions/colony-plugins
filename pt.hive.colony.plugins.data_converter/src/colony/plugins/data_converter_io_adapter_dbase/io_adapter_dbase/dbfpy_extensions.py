#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import dbfpy.fields

class DbfpyExtensions:
    """
    Extensions to the dbfpy module to allow used to stop it from crashing in
    some situations.
    """

    def __init__(self, io_adapter_dbase_plugin):
        """
        Constructor of the class.

        @type io_adapter_dbase_plugin: IoAdapterDbasePlugin
        @param io_adapter_dbase_plugin: Input output adapter dbase plugin.
        """

        self.io_adapter_dbase_plugin = io_adapter_dbase_plugin

    def register_extensions(self):
        """
        Registers the dbfpy extensions contained in this module.
        """

        # overrides the dbfpy handler for general, memo and date field types
        # so it doesn't crash when the column names are retrieved through it
        dbfpy.fields.registerField(DbfGeneralFieldDef)
        dbfpy.fields.registerField(DbfMemoFieldDef)
        dbfpy.fields.registerField(DbfDateFieldDef)

class DbfGeneralFieldDef(dbfpy.fields.DbfFieldDef):
    """
    Extends dbfpy by providing dummy support for encoding/decoding general fields.
    """

    typeCode = "G"
    defaultValue = ""

    def decodeValue(self, value):
        return ""

    def encodeValue(self, value):
        return ""

class DbfMemoFieldDef(dbfpy.fields.DbfFieldDef):
    """
    Extends dbfpy by providing dummy support for encoding/decoding memo fields.
    """

    typeCode = "M"
    defaultValue = ""

    def decodeValue(self, value):
        return ""

    def encodeValue(self, value):
        return ""

class DbfDateFieldDef(dbfpy.fields.DbfFieldDef):
    """
    Extends dbfpy by providing dummy support for encoding/decoding date fields.
    """

    typeCode = "D"
    defaultValue = ""

    def decodeValue(self, value):
        return ""

    def encodeValue(self, value):
        return ""
