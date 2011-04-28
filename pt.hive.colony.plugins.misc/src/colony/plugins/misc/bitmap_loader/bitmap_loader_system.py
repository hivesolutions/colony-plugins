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

import os
import wx
import stat

EXTENSIONS_MAP = {
    ".png" : wx.BITMAP_TYPE_PNG,
    ".gif" : wx.BITMAP_TYPE_GIF,
    ".jpg" : wx.BITMAP_TYPE_JPEG,
    ".ico" : wx.BITMAP_TYPE_ICO
}
""" The map of extensions and types """

class BitmapLoader:
    """
    Bitmap loader class.
    """

    bitmap_loader_plugin = None
    """ The bitmap loader plugin """

    def __init__(self, bitmap_loader_plugin):
        """
        Constructor of the class.

        @type bitmap_loader_plugin: BitmapLoaderPlugin
        @param bitmap_loader_plugin: The bitmap loader plugin.
        """

        self.bitmap_loader_plugin = bitmap_loader_plugin

    def load_icons(self, path, bitmaps_map, icons_map):
        # retrieves the list of file from the path
        directory_entries = os.listdir(path)

        # iterates over all the directory entries
        for directory_entry in directory_entries:
            # creates the full directory entry path
            full_path = path + "/" + directory_entry

            # retrieves the mode from teh full path
            mode = os.stat(full_path)[stat.ST_MODE]

            # in case the file is not a directory
            if not stat.S_ISDIR(mode):
                # splits the directory entry path, to
                # retrieve the extension
                base_path, extension = os.path.splitext(directory_entry)

                # in case the extension is valid
                if extension in EXTENSIONS_MAP:
                    # retrieves the type of the extension
                    extension_type = EXTENSIONS_MAP[extension]

                    # creates the bitmap from the extension type
                    # and the full path
                    bitmap = wx.Bitmap(full_path, extension_type)

                    # creates an icon from the bitmap
                    icon = wx.IconFromBitmap(bitmap)

                    # sets the icon properties in the maps
                    bitmaps_map[base_path] = bitmap
                    icons_map[base_path] = icon
