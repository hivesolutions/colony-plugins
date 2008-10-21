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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class BusinessHelper:
    """
    The business helper class
    """

    business_helper_plugin = None
    """ The business helper plugin """

    def __init__(self, business_helper_plugin):
        """
        Constructor of the class
        
        @type business_helper_plugin: BusinessHelperPlugin
        @param business_helper_plugin: The business helper plugin
        """

        self.business_helper_plugin = business_helper_plugin

    def import_class_module(self, class_module_name, globals, locals, global_values, base_directory_path):
        # creates a copy of locals
        locals_copy = locals.copy()

        # iterates over the keys of the copy of locals
        for local_key_value in locals_copy:
            # retrieves the current local value
            local_value = locals_copy[local_key_value]

            # in case the local value exists in the list of global values
            if local_value in global_values:
                # adds the value to globals
                globals[local_key_value] = local_value

        # executes the file in the given environment
        execfile(base_directory_path + "/" + class_module_name + ".py", globals, globals)
