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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 9010 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-06-22 09:28:09 +0100 (ter, 22 Jun 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class WorkPoolDummy:
    """
    The work pool dummy class.
    """

    work_pool_dummy_plugin = None
    """ The work pool dummy plugin """

    work_pools_list = []
    """ The list of currently enabled work pools """

    def __init__(self, work_pool_dummy_plugin):
        """
        Constructor of the class.

        @type work_pool_dummy_plugin: Plugin
        @param work_pool_dummy_plugin: The work pool dummy plugin.
        """

        self.work_pool_dummy_plugin = work_pool_dummy_plugin
