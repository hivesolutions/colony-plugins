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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.map_util

PROPERTY_VALUE = "property"
""" The property value """

KEY_VALUE = "key"
""" The key value """

VALUE_VALUE = "value"
""" The value value """

class PropertiesBuildAutomationExtension:
    """
    The properties build automation extension class.
    """

    properties_build_automation_extension_plugin = None
    """ The properties build automation extension plugin """

    def __init__(self, properties_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type properties_build_automation_extension_plugin: PropertiesBuildAutomationExtensionPlugin
        @param properties_build_automation_extension_plugin: The properties build automation extension plugin.
        """

        self.properties_build_automation_extension_plugin = properties_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # prints an info message
        logger.info("Running properties build automation plugin")

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the properties from the parameters
        properties = colony.libs.map_util.map_get_values(parameters, PROPERTY_VALUE)

        # iterates over all the properties to set them
        # as local properties
        for property in properties:
            # retrieves the property key and value
            property_key = property.get(KEY_VALUE, None)
            property_value = property.get(VALUE_VALUE, None)

            # sets the build automation structure runtime properties
            build_automation_structure_runtime.local_properties[property_key] = property_value

        # returns true (success)
        return True
