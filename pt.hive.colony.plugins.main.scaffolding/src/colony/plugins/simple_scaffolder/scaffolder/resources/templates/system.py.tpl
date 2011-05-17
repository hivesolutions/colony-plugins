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

class ${out value=scaffold_attributes.class_name /}:
    """
    The ${out value=scaffold_attributes.short_name_lowercase /} class.
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

    def dummy_method(self):
        return "dummy_result"
