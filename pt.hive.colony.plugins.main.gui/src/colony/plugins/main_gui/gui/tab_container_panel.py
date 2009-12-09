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

import wx

class TabContainerPanel(wx.Panel):
    """
    The tab container panel class
    """

    def __init__(self, parent, image_list = []):
        """
        Constructor of the class.

        @type parent: Object
        @param parent: The parent component.
        @type image_list: List
        @param image_list: The list of images to be used.
        """

        wx.Panel.__init__(self, parent, size = (970, 720))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        # creates a new notebook
        self.book = wx.Notebook(self, wx.ID_ANY, style = wx.CLIP_CHILDREN)

        # creates a new wx image list
        wx_image_list = wx.ImageList(10, 10)

        # iterates over all the images in the image list
        for image in image_list:
            wx_image_list.Add(image)

        self.book.AssignImageList(wx_image_list)

        self._rmenu = wx.Menu()
        item = wx.MenuItem(self._rmenu, wx.ID_ANY, "Close Tab\tCtrl+F4", "Close Tab")
        self._rmenu.AppendItem(item)

        #@todo: put the right click here
        #self.book.SetRightClickMenu(self._rmenu)

        main_sizer.Add(self.book, 6, wx.EXPAND)

        main_sizer.Layout()
