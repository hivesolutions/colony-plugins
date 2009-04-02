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

from re import *

def _NCNameChar(x):
    return x.isalpha() or x.isdigit() or x=="." or x=='-' or x=="_"

def _NCNameStartChar(x):
    return x.isalpha() or x=="_"

def _toUnicodeHex(x):
    hexval = hex(ord(x[0]))[2:]
    hexlen = len(hexval)
    # Make hexval have either 4 or 8 digits by prepending 0's
    if   (hexlen==1): hexval = "000" + hexval
    elif (hexlen==2): hexval = "00"  + hexval
    elif (hexlen==3): hexval = "0"   + hexval
    elif (hexlen==4): hexval = ""    + hexval
    elif (hexlen==5): hexval = "000" + hexval
    elif (hexlen==6): hexval = "00"  + hexval
    elif (hexlen==7): hexval = "0"   + hexval
    elif (hexlen==8): hexval = ""    + hexval
    else: raise Exception, "Illegal Value returned from hex(ord(x))"

    return "_x"+ hexval + "_"

def _fromUnicodeHex(x):
    return eval(r'u"\u'+x[2:-1]+'"')

def toXMLname(string):
    """Convert string to a XML name."""
    if string.find(':') != -1 :
        (prefix, localname) = string.split(':',1)
    else:
        prefix = None
        localname = string

    T = unicode(localname)

    N = len(localname)
    X = [];
    for i in range(N) :
        if i< N-1 and T[i]==u'_' and T[i+1]==u'x':
            X.append(u'_x005F_')
        elif i==0 and N >= 3 and \
                 ( T[0]==u'x' or T[0]==u'X' ) and \
                 ( T[1]==u'm' or T[1]==u'M' ) and \
                 ( T[2]==u'l' or T[2]==u'L' ):
            X.append(u'_xFFFF_' + T[0])
        elif (not _NCNameChar(T[i])) or (i==0 and not _NCNameStartChar(T[i])):
            X.append(_toUnicodeHex(T[i]))
        else:
            X.append(T[i])

    if prefix:
        return "%s:%s" % (prefix, u''.join(X))
    return u''.join(X)

def fromXMLname(string):
    """
    Converts XML name to unicode string
    """

    retval = sub(r'_xFFFF_','', string )

    def fun( matchobj ):
        return _fromUnicodeHex( matchobj.group(0) )

    retval = sub(r'_x[0-9A-Za-z]+_', fun, retval )

    return retval
