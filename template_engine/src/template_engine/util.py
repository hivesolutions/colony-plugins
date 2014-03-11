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

class Accessor(dict):

    def __init__(self, ref):
        self.ref = ref
        self.is_map = hasattr(ref, "__getitem__")

    def __ref__(self):
        ref = dict.__getattribute__(self, "ref")
        is_callable = hasattr(ref, "__call__")
        if is_callable: ref = ref(); self.ref = ref
        return ref

    def __len__(self, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return len(ref)

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

    def __eq__(self, value, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return ref == value

    def __lt__(self, value, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return ref < value

    def __lte__(self, value, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return ref <= value

    def __gt__(self, value, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return ref > value

    def __gte__(self, value, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return ref >= value

    def __cmp__(self, value, *args, **kwargs):
        ref = dict.__getattribute__(self, "__ref__")()
        return cmp(ref, value)

    def __call__(self, *args, **kwargs):
        ref = dict.__getattribute__(self, "ref")
        is_callable = hasattr(ref, "__call__")
        return ref.__call__(*args, **kwargs) if is_callable else ref

    def __getattribute__ (self, name):
        if name == "ref": return dict.__getattribute__(self, "ref")
        ref = dict.__getattribute__(self, "ref")
        is_map = dict.__getattribute__(self, "is_map")
        if is_map and name in ref: return accessor(ref[name])
        if hasattr(ref, name): return accessor(getattr(ref, name))
        return dict.__getattribute__(self, name)

    def __getitem__ (self, name):
        ref = dict.__getattribute__(self, "ref")
        is_map = dict.__getattribute__(self, "is_map")
        if is_map and name in ref: return accessor(ref[name])
        if hasattr(ref, name): return accessor(getattr(ref, name))
        raise KeyError("'%s' not found" % name)

def accessor(value):
    return Accessor(value)
