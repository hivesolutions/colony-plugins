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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 7679 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 18:05:35 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.importer_util

DUMMY_BUNDLE_MODULE_VALUE = "dummy_bundle"
""" The dummy bundle module value """

# imports the dummy bundle module
dummy_bundle = colony.libs.importer_util.__importer__(DUMMY_BUNDLE_MODULE_VALUE)

class DummyEntity(dummy_bundle.DummyEntityBundleParent):

    age = {
        "data_type" : "numeric"
    }
    """ The age of the entity """

    def __init__(self):
        dummy_bundle.DummyEntityBundleParent.__init__(self)
        self.age = None

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age
