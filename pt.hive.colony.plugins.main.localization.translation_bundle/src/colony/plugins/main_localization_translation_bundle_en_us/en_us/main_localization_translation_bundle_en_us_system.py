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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

RESOURCES_PATH = "main_localization_translation_bundle_en_us/en_us/resources"
""" The resources path """

BUNDLE_FILE_NAME = "localization_bundle_en_us.json"
""" The bundle file name """

BUNDLE_TYPE = "json"
""" The bundle type """

class MainLocalizationTranslationBundleEnUs:
    """
    The main localization translation bundle en us class.
    """

    main_localization_translation_bundle_en_us_plugin = None
    """ The main localization translation bundle en us plugin """

    def __init__(self, main_localization_translation_bundle_en_us_plugin):
        """
        Constructor of the class.

        @type main_localization_translation_bundle_en_us_plugin: MainLocalizationTranslationBundleEnUsPlugin
        @param main_localization_translation_bundle_en_us_plugin: The main localization translation bundle en us plugin.
        """

        self.main_localization_translation_bundle_en_us_plugin = main_localization_translation_bundle_en_us_plugin

    def get_bundle_path(self):
        # retrieves the plugin manager
        manager = self.main_localization_translation_bundle_en_us_plugin.manager

        # retrieves the main localization translation bundle en us plugin path
        main_localization_translation_bundle_en_us_plugin_path = manager.get_plugin_path_by_id(self.main_localization_translation_bundle_en_us_plugin.id)

        # sets the main localization translation bundle en us plugin resources path
        main_localization_translation_bundle_en_us_plugin_resources_path = main_localization_translation_bundle_en_us_plugin_path + "/" + RESOURCES_PATH + "/" + BUNDLE_FILE_NAME

        # returns the main localization translation bundle en us plugin resources path
        return main_localization_translation_bundle_en_us_plugin_resources_path

    def get_bundle_type(self):
        return BUNDLE_TYPE
