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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

PAGE_SIZE = 4096
""" The size of a page """

DEFAULT_NUMBER_PAGES = 64
""" The default number of pages """

class MainStorageBufferManager:
    """
    The main storage buffer manager class.
    """

    main_storage_buffer_manager_plugin = None
    """ The main storage buffer manager plugin """

    def __init__(self, main_storage_buffer_manager_plugin):
        """
        Constructor of the class.

        @type main_storage_buffer_manager_plugin: MainStorageBufferManagerPlugin
        @param main_storage_buffer_manager_plugin: The main storage buffer
        manager plugin.
        """

        self.main_storage_buffer_manager_plugin = main_storage_buffer_manager_plugin

class BufferPool:
    """
    The buffer pool class.
    Manages a pool representing a buffer
    for file access.
    """

    number_pages = DEFAULT_NUMBER_PAGES
    """ The number of pages of the buffer pool """

    def __init__(self, number_pages = DEFAULT_NUMBER_PAGES):
        """
        Constructor of the class.

        @type number_pages: int
        @param number_pages: The number of pages of the
        buffer pool.
        """

        self.number_pages = number_pages

    def get_page(self, page_id, transaction = None, permissions = None):
        pass

    def release_page(self, page_id, transaction):
        pass

    def insert_tuple(self, tuple, table, transaction):
        pass

    def delete_tuple(self, tuple, table, transaction):
        pass

class PageId:
    table_id = None
    """ The id of the table associated with the page """

    page_number = None

class HeapPageId(PageId):
    pass

class HeapFile:
    """
    The heap file class.
    Represent a file that is structured as a heap,
    all the pages are stored in random order.
    """

    file = None
    """ The file used to maintain the heap file """

    def __init__(self, file):
        """
        Constructor of the class.

        @type file: File
        @param file: The file used to maintain the heap file.
        """

        self.file = file
