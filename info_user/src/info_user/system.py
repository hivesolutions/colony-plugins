#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.libs.map_util

class InfoUser(colony.base.system.System):
    """
    The info user class, this is the back-end class that
    implements the concrete methods.
    """

    info_user_configuration = {}
    """ The configuration map to be used for the loading
    of the information about the users """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.info_user_configuration = {}

    def get_user_info(self, user):
        # tries to retrieve the user information map using the username
        # as the key for retrieval and then returns it to the caller method
        user_information = self.info_user_configuration.get("user_information")
        info = user_information.get(user, {})
        return info

    def set_configuration_property(self, configuration_property):
        # retrieves the configuration and runs the clean operation
        # in it then copies the configuration to the target map
        configuration = configuration_property.get_data()
        colony.libs.map_util.map_clean(self.info_user_configuration)
        colony.libs.map_util.map_copy(configuration, self.info_user_configuration)

    def unset_configuration_property(self):
        # cleans the info user configuration map to avoid duplicate
        # values in the map (side effect may occur)
        colony.libs.map_util.map_clean(self.info_user_configuration)
