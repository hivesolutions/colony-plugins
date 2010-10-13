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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class InformationUser:
    """
    The information user class.
    """

    information_user_plugin = None
    """ The information user plugin """

    user_information_map = {}
    """ The map user information """

    def __init__(self, information_user_plugin):
        """
        Constructor of the class.

        @type information_user_plugin: InformationUserPlugin
        @param information_user_plugin: The information user plugin.
        """

        self.information_user_plugin = information_user_plugin

        self.user_information_map = {}

    def get_user_information_user_key(self, user_key):
        # retrieves the user information for the user key
        user_information = self.user_information_map.get(user_key, {})

        # returns the user information
        return user_information

    def set_configuration_property(self, configuration_propery):
        # retrieves the configuration
        configuration = configuration_propery.get_data()

        # retrieves the user information map
        user_information_map = configuration["user_information"]

        # sets the user information map
        self.user_information_map = user_information_map

    def unset_configuration_property(self):
        # sets the user information map
        self.user_information_map = {}
