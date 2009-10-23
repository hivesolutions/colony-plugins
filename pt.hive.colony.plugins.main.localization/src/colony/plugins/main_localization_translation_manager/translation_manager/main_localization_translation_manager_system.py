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

__revision__ = "$LastChangedRevision: 5629 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-19 10:11:40 +0100 (seg, 19 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class MainLocalizationTranslationManager:
    """
    The main localization translation manager class.
    """

    main_localization_translation_manager_plugin = None
    """ The main localization translation manager plugin """

    localization_translation_bundle_handler_name_localization_translation_bundle_handler_plugin_map = {}
    """ The localization translation bundle handler name localization translation bundle handler plugin map """

    def __init__(self, main_localization_translation_manager_plugin):
        """
        Constructor of the class.

        @type main_localization_translation_manager_plugin: MainLocalizationTranslationManagerPlugin
        @param main_localization_translation_manager_plugin: The main localization translation manager plugin.
        """

        self.main_localization_translation_manager_plugin = main_localization_translation_manager_plugin

        self.localization_translation_bundle_handler_name_localization_translation_bundle_handler_plugin_map = {}

    def load_localization_translation_bundle_handler_plugin(self, localization_translation_bundle_handler_plugin):
        # retrieves the localization translation bundle handler name
        localization_translation_bundle_handler_name = localization_translation_bundle_handler_plugin.get_handler_name()

        # sets the localization translation bundle handler plugin
        self.localization_translation_bundle_handler_name_localization_translation_bundle_handler_plugin_map[localization_translation_bundle_handler_name] = localization_translation_bundle_handler_plugin

        # generates the translation bundle
        #translation_bundle = self.generate_translation_bundle(localization_translation_bundle_handler_plugin)

    def unload_localization_translation_bundle_handler_plugin(self, localization_translation_bundle_handler_plugin):
        pass

    def generate_translation_bundle(self, localization_translation_bundle_plugin):
        # retrieves the bundle path
        bundle_path = localization_translation_bundle_plugin.get_bundle_path()

        # retrieves the bundle type
        bundle_type = localization_translation_bundle_plugin.get_bundle_type()

        # creates the translation bundle
        translation_bundle = TranslationBundle(bundle_path, bundle_type)

        # returns the translation bundle
        return translation_bundle

    def get_locale(self, locale_type, locale_properties):
        """
        Retrieves the locale for the given locale type and local properties.

        @type locale_type: String
        @param locale_type: The type of the local to retrieve.
        @type locale_properties: Map
        @param locale_properties: The properties of the local to retrieve.
        @rtype: Object
        @return: The locale for the given locale type and local properties.
        """

        return None

    def get_locale_string(self, locale_string, locale_string_properties):

        return None

class TranslationBundle:
    """
    The translation bundle class.
    """

    bundle_path = "none"
    """ The bundle path """

    bundle_type = "none"
    """ The bundle type """

    def __init__(self, bundle_path = "none", bundle_type = "none"):
        self.bundle_path = bundle_path
        self.bundle_type = bundle_type

    def get_bundle_path(self):
        """
        Retrieves the bundle path.

        @rtype: String
        @return: The bundle path.
        """

        return self.bundle_path

    def set_bundle_path(self, bundle_path):
        """
        Sets the bundle path.

        @type bundle_path: String
        @param bundle_path: The bundle path.
        """

        self.bundle_path = bundle_path


    def get_bundle_type(self):
        """
        Retrieves the bundle type.

        @rtype: String
        @return: The bundle type.
        """

        return self.bundle_type

    def set_bundle_type(self, bundle_type):
        """
        Sets the bundle type.

        @type bundle_path: String
        @param bundle_path: The bundle type.
        """

        self.bundle_type = bundle_type
