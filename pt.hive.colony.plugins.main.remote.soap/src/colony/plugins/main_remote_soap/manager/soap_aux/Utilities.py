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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import exceptions
import copy
import re
import string
import sys
from types import *

# SOAPpy modules
from Errors import *

def collapseWhiteSpace(s):
    return re.sub("\s+", " ", s).strip()

def decodeHexString(data):
    conv = {
            "0": 0x0, "1": 0x1, "2": 0x2, "3": 0x3, "4": 0x4,
            "5": 0x5, "6": 0x6, "7": 0x7, "8": 0x8, "9": 0x9,

            "a": 0xa, "b": 0xb, "c": 0xc, "d": 0xd, "e": 0xe,
            "f": 0xf,

            "A": 0xa, "B": 0xb, "C": 0xc, "D": 0xd, "E": 0xe,
            "F": 0xf,
            }

    ws = string.whitespace

    bin = ""

    i = 0

    while i < len(data):
        if data[i] not in ws:
            break
        i += 1

    low = 0

    while i < len(data):
        c = data[i]

        if c in string.whitespace:
            break

        try:
            c = conv[c]
        except KeyError:
            raise ValueError, "invalid hex string character `%s'" % c

        if low:
            bin += chr(high * 16 + c)
            low = 0
        else:
            high = c
            low = 1

        i += 1

    if low:
        raise ValueError, "invalid hex string length"

    while i < len(data):
        if data[i] not in string.whitespace:
            raise ValueError, \
                "invalid hex string character `%s'" % c
        i += 1

    return bin

def encodeHexString(data):
    h = ""

    for i in data:
        h += "%02X" % ord(i)

    return h

def leapMonth(year, month):
    return month == 2 and \
        year % 4 == 0 and \
        (year % 100 != 0 or year % 400 == 0)

def cleanDate(d, first = 0):
    ranges = (None, (1, 12), (1, 31), (0, 23), (0, 59), (0, 61))
    months = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    names = ("year", "month", "day", "hours", "minutes", "seconds")

    if len(d) != 6:
        raise ValueError, "date must have 6 elements"

    for i in range(first, 6):
        s = d[i]

        if type(s) == FloatType:
            if i < 5:
                try:
                    s = int(s)
                except OverflowError:
                    if i > 0:
                        raise
                    s = long(s)

                if s != d[i]:
                    raise ValueError, "%s must be integral" % names[i]

                d[i] = s
        elif type(s) == LongType:
            try: s = int(s)
            except: pass
        elif type(s) != IntType:
            raise TypeError, "%s isn't a valid type" % names[i]

        if i == first and s < 0:
            continue

        if ranges[i] != None and \
            (s < ranges[i][0] or ranges[i][1] < s):
            raise ValueError, "%s out of range" % names[i]

    if first < 6 and d[5] >= 61:
        raise ValueError, "seconds out of range"

    if first < 2:
        leap = first < 1 and leapMonth(d[0], d[1])

        if d[2] > months[d[1]] + leap:
            raise ValueError, "day out of range"

def debugHeader(title):
    s = "*** " + title + " "
    print s + ("*" * (72 - len(s)))

def debugFooter(title):
    print "*" * 72
    sys.stdout.flush()
