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

__revision__ = "$LastChangedRevision: 81 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-22 16:42:45 +0100 (Wed, 22 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

HANDLER_NAME = "localization"

LOCALIZATION_REGEX = "@locale:[^@]*@"

class JavascriptLocalizationHandler:
    """
    The javascript localization handler class.
    """

    javascript_localization_handler_plugin = None
    """ The javascript localization handler plugin """

    def __init__(self, javascript_localization_handler_plugin):
        """
        Constructor of the class.

        @type javascript_localization_handler_plugin: JavascriptLocalizationHandlerPlugin
        @param javascript_localization_handler_plugin: The javascript localization handler plugin.
        """

        self.javascript_localization_handler_plugin = javascript_localization_handler_plugin

    def get_javascript_handler_name(self):
        """
        Retrieves the javascript handler name.

        @rtype: String
        @return: The javascript handler name.
        """

        return HANDLER_NAME

    def handle_contents(self, contents):
        # compiles the regular expression generating the pattern
        pattern = re.compile(LOCALIZATION_REGEX)

        # retrieves the match iterator
        match_iterator = pattern.finditer(contents)

        # iterates using the match iterator
        for match in match_iterator:
            # retrieves the match group
            group = match.group()

            # retrieves the start index for the group
            start_index = match.start()

            # retrieves the end index for the group
            end_index = match.end()

            # retrieves the locale value
            locale_value = group[9:-1]

            contents = contents.replace(group, "thobias")

        return contents
