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

__revision__ = "$LastChangedRevision: 2096 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:02:08 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import stat
import wx

#@todo: review and comment this file
class BitmapLoader:
    
    bitmap_loader_plugin = None

    def __init__(self, bitmap_loader_plugin):
        self.bitmap_loader_plugin = bitmap_loader_plugin

    def load_icons(self, path, bitmaps_dic, icons_dic):
        dir_list = os.listdir(path)
        for file_name in dir_list:
            full_path = path + "/" + file_name
            mode = os.stat(full_path)[stat.ST_MODE]
            if not stat.S_ISDIR(mode):
                split = os.path.splitext(file_name)
                if split[-1] == ".png":
                    bitmap = wx.Bitmap(full_path, wx.BITMAP_TYPE_PNG)
                    icon = wx.IconFromBitmap(bitmap)
                    name = split[0]
                    bitmaps_dic[name] = bitmap
                    icons_dic[name] = icon
