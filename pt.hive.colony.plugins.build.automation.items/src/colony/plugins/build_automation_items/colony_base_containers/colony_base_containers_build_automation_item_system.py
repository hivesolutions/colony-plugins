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

class ColonyBaseContainersBuildAutomationItem:
    """
    The colony base containers build automation item class.
    """

    colony_base_containers_build_automation_item_plugin = None
    """ The colony base containers build automation item plugin """

    def __init__(self, colony_base_containers_build_automation_item_plugin):
        """
        Constructor of the class.

        @type colony_base_containers_build_automation_item_plugin: ColonyBaseContainersBuildAutomationItemPlugin
        @param colony_base_containers_build_automation_item_plugin: The colony base containers build automation item plugin.
        """

        self.colony_base_containers_build_automation_item_plugin = colony_base_containers_build_automation_item_plugin
