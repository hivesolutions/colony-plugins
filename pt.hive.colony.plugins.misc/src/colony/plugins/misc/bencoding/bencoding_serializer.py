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

__revision__ = "$LastChangedRevision: 5720 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-21 17:36:22 +0100 (qua, 21 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

import bencoding_exceptions

DECIMAL_REGEX_VALUE = "\d"
""" The decimal regular expression value """

DECIMAL_REGEX = re.compile(DECIMAL_REGEX_VALUE)
""" The decimal regular expression """

def dumps(object):
    pass

def loads(data):
    # creates a list from the data
    # (the chunks list)
    chunks = list(data)

    # reverses the list
    chunks.reverse()

    # "dechunks" the data (retrieving the root element)
    root_element = _dechunk(chunks)

    # returns the root element
    return root_element

def _dechunk(chunks):
    # retrieves an item from
    # the chunks list
    item = chunks.pop()

    # in case the current item is a dictionary
    if item == "d":
        # retrieves an item from the
        # chunks list
        item = chunks.pop()

        # creates the (empty) map
        map = {}

        # iterates while the map end
        # is not reached
        while item != "e":
            # adds the item to the chunks list
            # to be able to parse it bellow
            chunks.append(item)

            # retrieves the map key
            key = _dechunk(chunks)

            # retrieves the map value
            map[key] = _dechunk(chunks)

            # pops the item from the chunks list
            item = chunks.pop()

        # returns the map
        return map

    # in case the current item is a list
    elif item == "l":
        item = chunks.pop()

        # creates the empty list
        list = []

        while not item == "e":
            chunks.append(item)
            list.append(_dechunk(chunks))
            item = chunks.pop()

        # returns the list
        return list

    # in case the current item is an integer
    elif item == "i":
        item = chunks.pop()
        number = ""

        while item != "e":
            number  += item
            item = chunks.pop()

        return int(number)

    elif (DECIMAL_REGEX.findall(item)):
        number = ""

        while DECIMAL_REGEX.findall(item):
            number += item
            item = chunks.pop()

        line = ""

        for _index in range(1, int(number) + 1):
            line += chunks.pop()

        return line

    raise bencoding_exceptions.BencodingDecodeException("data type nodt defined: " + str(item))
