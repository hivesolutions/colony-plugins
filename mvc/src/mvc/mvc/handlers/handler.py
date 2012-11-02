#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

import types

class Handler(object):
    """
    The abstract handler class to be used for handlers that
    are class oriented (not direct function calls).
    """

    filters = None
    """ The reference to the list that will hold the various
    filters to be applied to the message to be sent """

    def __init__(self):
        self.filters = []

    def add_filter(self, filter):
        self.filters.append(filter)

    def filter(self, message):
        # retrieves the (data) type of the current message, and
        # in case it's not a map returns immediately, plain messages
        # are not "filterable"
        message_t = type(message)
        if not message_t == types.DictType: return message

        # iterates over the complete set of filters registered in the
        # handler and runs them in the message, retrieving the filtered
        # message as the new message
        for filter in self.filters: message = filter(message)
        return message

    def plain_filter(self, message):
        contents = message.get("contents", {})
        value = contents.get("value", None)
        return value
