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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

import colony.libs.test_util

class ResourceManagerTestCase(colony.libs.test_util.ColonyTestCase):
    """
    The resource manager test case class.
    """

    def setUp(self):
        """
        Set ups the test creating the necessary resources.
        """

        self.plugin.register_resource("namespace1", "name1", "type1", "data1")
        self.plugin.register_resource("namespace1", "name2", "type1", "data2")
        self.plugin.register_resource("namespace1", "name1", "type1", "data3")
        self.plugin.register_resource("namespace1", "name2", "type1", "data3")

        # this one should erase the previous
        self.plugin.register_resource("namespace1", "name2", "type2", "data4")
        self.plugin.register_resource("namespace2", "name1", "type1", "data1")
        self.plugin.register_resource("namespace2", "name2", "type1", "data2")
        self.plugin.register_resource("namespace2", "name1", "type1", "data3")
        self.plugin.register_resource("namespace2", "name2", "type1", "data3")

        # this one should erase the previous
        self.plugin.register_resource("namespace2", "name2", "type2", "data4")

        self.plugin.register_resource("namespace2.something", "name1", "type1", "data1")
        self.plugin.register_resource("namespace2.something", "name2", "type1", "data2")
        self.plugin.register_resource("namespace2.something", "name1", "type1", "data3")
        self.plugin.register_resource("namespace2.something", "name2", "type1", "data3")

        # this one should erase the previous
        self.plugin.register_resource("namespace2.something", "name2", "type2", "data4")

    def tearDown(self):
        """
        Tears down the test removing the created resources.
        """

        self.plugin.unregister_resource("namespace1.name1")
        self.plugin.unregister_resource("namespace1.name2")
        self.plugin.unregister_resource("namespace2.name1")
        self.plugin.unregister_resource("namespace2.name2")
        self.plugin.unregister_resource("namespace2.something.name1")
        self.plugin.unregister_resource("namespace2.something.name2")

    def test_registered_resources(self):
        self.assertTrue(self.plugin.is_resource_registered("namespace1.name1"))
        resource = self.plugin.get_resource("namespace1.name1")
        self.assertTrue(not resource == None)
        self.assertTrue(resource.get_name() == "name1")
        self.assertTrue(resource.get_type() == "type1")
        self.assertTrue(resource.get_data() == "data3")
        self.assertTrue(resource.get_namespace().get_list_value() == ["namespace1"])

        self.assertTrue(self.plugin.is_resource_registered("namespace1.name2"))
        resource = self.plugin.get_resource("namespace1.name2")
        self.assertTrue(not resource == None)
        self.assertTrue(resource.get_name() == "name2")
        self.assertTrue(resource.get_type() == "type2")
        self.assertTrue(resource.get_data() == "data4")
        self.assertTrue(resource.get_namespace().get_list_value() == ["namespace1"])

        self.assertTrue(self.plugin.is_resource_registered("namespace2.name1"))
        resource = self.plugin.get_resource("namespace2.name1")
        self.assertTrue(not resource == None)
        self.assertTrue(resource.get_name() == "name1")
        self.assertTrue(resource.get_type() == "type1")
        self.assertTrue(resource.get_data() == "data3")
        self.assertTrue(resource.get_namespace().get_list_value() == ["namespace2"])

        self.assertTrue(self.plugin.is_resource_registered("namespace2.name2"))
        resource = self.plugin.get_resource("namespace2.name2")
        self.assertTrue(not resource == None)
        self.assertTrue(resource.get_name() == "name2")
        self.assertTrue(resource.get_type() == "type2")
        self.assertTrue(resource.get_data() == "data4")
        self.assertTrue(resource.get_namespace().get_list_value() == ["namespace2"])

        self.assertTrue(self.plugin.is_resource_registered("namespace2.something.name1"))
        resource = self.plugin.get_resource("namespace2.something.name1")
        self.assertTrue(not resource == None)
        self.assertTrue(resource.get_name() == "name1")
        self.assertTrue(resource.get_type() == "type1")
        self.assertTrue(resource.get_data() == "data3")
        self.assertTrue(resource.get_namespace().get_list_value() == ["namespace2","something"])

        self.assertTrue(self.plugin.is_resource_registered("namespace2.something.name2"))
        resource = self.plugin.get_resource("namespace2.something.name2")
        self.assertTrue(not resource == None)
        self.assertTrue(resource.get_name() == "name2")
        self.assertTrue(resource.get_type() == "type2")
        self.assertTrue(resource.get_data() == "data4")
        self.assertTrue(resource.get_namespace().get_list_value() == ["namespace2","something"])

    def test_unregistering_resources(self):
        self.assertTrue(self.plugin.is_resource_registered("namespace1.name1"))
        self.plugin.unregister_resource("namespace1.name1")
        self.assertFalse(self.plugin.is_resource_registered("namespace1.name1"))

        self.assertTrue(self.plugin.is_resource_registered("namespace1.name2"))
        self.plugin.unregister_resource("namespace1.name2")
        self.assertFalse(self.plugin.is_resource_registered("namespace1.name2"))

        self.assertTrue(self.plugin.is_resource_registered("namespace2.name1"))
        self.plugin.unregister_resource("namespace2.name1")
        self.assertFalse(self.plugin.is_resource_registered("namespace2.name1"))

        self.assertTrue(self.plugin.is_resource_registered("namespace2.name2"))
        self.plugin.unregister_resource("namespace2.name2")
        self.assertFalse(self.plugin.is_resource_registered("namespace2.name2"))

        self.assertTrue(self.plugin.is_resource_registered("namespace2.something.name1"))
        self.plugin.unregister_resource("namespace2.something.name1")
        self.assertFalse(self.plugin.is_resource_registered("namespace2.something.name1"))

        self.assertTrue(self.plugin.is_resource_registered("namespace2.something.name2"))
        self.plugin.unregister_resource("namespace2.something.name2")
        self.assertFalse(self.plugin.is_resource_registered("namespace2.something.name2"))
