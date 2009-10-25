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

import json

HANDLER_NAME = "json"
""" The handler name """

class MainLocalizationTranslationJsonBundleHandler:
    """
    The main localization translation json bundle handler class.
    """

    main_localization_translation_json_bundle_handler_plugin = None
    """ The main localization translation json bundle handler plugin """

    def __init__(self, main_localization_translation_json_bundle_handler_plugin):
        """
        Constructor of the class.

        @type main_localization_translation_json_bundle_handler_plugin: MainLocalizationTranslationJsonBundleHandlerPlugin
        @param main_localization_translation_json_bundle_handler_plugin: The main localization translation json bundle handler plugin.
        """

        self.main_localization_translation_json_bundle_handler_plugin = main_localization_translation_json_bundle_handler_plugin

    def get_handler_name(self):
        return HANDLER_NAME

    def handle_bundle(self, bundle):
        # retrieves the bundle path
        bundle_path = bundle.get_bundle_path()

        # opens the bundle file
        bundle_file = open(bundle_path, "rb")

        # parses the json bundle file contents
        bundle_contents = json.load(bundle_file)

        # closes the bundle file
        bundle_file.close()

        # returns the bundle contents
        return bundle_contents
