#!/usr/bin/python
# -*- coding: Cp1252 -*-

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

import colony.libs.test_util

class ${out value=scaffold_attributes.class_name /}Test:
    """
    The ${out value=scaffold_attributes.short_name_lowercase /} plugin unit test class.
    """

    ${out value=scaffold_attributes.variable_name /}_plugin = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} plugin """

    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        """
        Constructor of the class.

        @type ${out value=scaffold_attributes.variable_name /}_plugin: ${out value=scaffold_attributes.class_name /}Plugin
        @param ${out value=scaffold_attributes.variable_name /}_plugin: The ${out value=scaffold_attributes.short_name_lowercase /} plugin.
        """

        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin

    def get_plugin_test_case_bundle(self):
        return (
            ${out value=scaffold_attributes.class_name /}TestPluginTestCase,
        )

class ${out value=scaffold_attributes.class_name /}TestCase(colony.libs.test_util.ColonyTestCase):

    def setUp(self):
        self.plugin.info("Setting up ${out value=scaffold_attributes.short_name_lowercase /} test case...")

    def tearDown(self):
        self.plugin.info("Tearing down ${out value=scaffold_attributes.short_name_lowercase /} test case...")

class ${out value=scaffold_attributes.class_name /}TestPluginTestCase:

    @staticmethod
    def get_test_case():
        return ${out value=scaffold_attributes.class_name /}TestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "${out value=scaffold_attributes.short_name /} plugin test case"
