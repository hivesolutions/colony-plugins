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

__revision__ = "$LastChangedRevision: 1909 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-03-15 14:24:54 +0000 (dom, 15 Mar 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class BusinessDataFilterManager:
    """
    The business data filter manager class.
    """

    business_data_filter_manager_plugin = None
    """ The business data filter manager plugin """

    def __init__(self, business_data_filter_manager_plugin):
        """
        Constructor of the class.
        
        @type business_data_filter_manager_plugin: BusinessDataFilterManagerPlugin
        @param business_data_filter_manager_plugin: The business data filter manager plugin.
        """

        self.business_data_filter_manager_plugin = business_data_filter_manager_plugin
