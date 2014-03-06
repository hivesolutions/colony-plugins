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

BASIC_TYPES = (
    types.IntType,
    types.FloatType,
    types.LongType,
    types.BooleanType,
    types.ListType,
    types.TypeType,
    types.NoneType
)

def accessor(value):
    value_t = type(value)
    is_class = hasattr(value, "__class__")
    is_map = hasattr(value, "__getitem__")
    is_string = value_t in types.StringTypes
    is_basic = value_t in BASIC_TYPES
    is_invalid = is_string or is_basic
    is_valid = (is_class or is_map) and not is_invalid
    return Accessor(value) if is_valid else value

class Accessor(dict):

    def __init__(self, ref):
        self.ref = ref
        self.is_map = hasattr(ref, "__getitem__")

    def __ref__(self):
        ref = dict.__getattribute__(self, "ref")
        is_callable = hasattr(ref, "__call__")
        if is_callable: ref = ref(); self.ref = ref
        return ref

    def __str__(self, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return str(ref)

    def __unicode__(self, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return unicode(ref)

    def __repr__(self, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return repr(ref)

    def __nonzero__(self, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return bool(ref)

    def __call__(self, *args, **kwargs):
        ref = dict.__getattribute__(self, "ref")
        return ref.__call__(*args, **kwargs)

    def __getattribute__ (self, name):
        ref = dict.__getattribute__(self, "ref")
        is_map = dict.__getattribute__(self, "is_map")
        if hasattr(ref, name): return accessor(getattr(ref, name))
        if is_map: return accessor(ref[name])
        raise AttributeError("'%s' not found" % name)

    __getitem__ = __getattribute__
