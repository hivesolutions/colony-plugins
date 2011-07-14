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

__revision__ = "$LastChangedRevision: 5629 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-19 10:11:40 +0100 (seg, 19 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class MainLocalizationManager:
    """
    The main localization manager class.
    """

    main_localization_manager_plugin = None
    """ The main localization manager plugin """

    localization_handler_name_localization_handler_plugin_map = {}
    """ The localization handler name localization handler plugin map """

    def __init__(self, main_localization_manager_plugin):
        """
        Constructor of the class.

        @type main_localization_manager_plugin: MainLocalizationManagerPlugin
        @param main_localization_manager_plugin: The main localization manager plugin.
        """

        self.main_localization_manager_plugin = main_localization_manager_plugin

        self.localization_handler_name_localization_handler_plugin_map = {}

    def load_localization_handler_plugin(self, localization_handler_plugin):
        # retrieves the localization handler name
        localization_handler_name = localization_handler_plugin.get_handler_name()

        # sets the localization handler plugin
        self.localization_handler_name_localization_handler_plugin_map[localization_handler_name] = localization_handler_plugin

    def unload_localization_handler_plugin(self, localization_handler_plugin):
        # retrieves the localization handler name
        localization_handler_name = localization_handler_plugin.get_handler_name()

        # unsets the localization handler plugin
        del self.localization_handler_name_localization_handler_plugin_map[localization_handler_name]

    def get_locale(self, locale_identifier, locale_type, locale_properties):
        """
        Retrieves the locale for the given local identifier, locale type and local properties.

        @type locale_identifier: String
        @param locale_identifier: The identifier of the local to retrieve.
        @type locale_type: String
        @param locale_type: The type of the local to retrieve.
        @type locale_properties: Dictionary
        @param locale_properties: The properties of the local to retrieve.
        @rtype: Object
        @return: The locale for the given locale type and local properties.
        """

        # in case there is no localization handler plugin for the given locale type
        if not locale_type in self.localization_handler_name_localization_handler_plugin_map:
            return None

        # retrieves the localization handler plugin for the given locale type
        localization_handler_plugin = self.localization_handler_name_localization_handler_plugin_map[locale_type]

        # calls the localization handler plugin to retrieve the locale value
        locale_value = localization_handler_plugin.get_locale(locale_identifier, locale_type, locale_properties)

        # returns the locale value
        return locale_value
