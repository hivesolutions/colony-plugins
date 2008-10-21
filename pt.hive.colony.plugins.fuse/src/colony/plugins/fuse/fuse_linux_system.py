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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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
import stat
import errno
import fuse

fuse.fuse_python_api = (0, 2)

class FuseFilesystem(fuse.Fuse):
    """
    Represents a filesystem and the operations you can perform upon it. This class is meant to be extended.
    """
    
    def get_parent_path(path):
        """
        Removes the filename from the path and returns the remainder.
        
        @param path: Filesystem path.
        @rtype: String
        @return: Returns the parent path. 
        """
        path_item_list = path.split("/")
        parent_path = "/"
        for x in range(len(path_item_list)-1):
            if not path_item_list[x] == "":
               if not parent_path == "/":
                  parent_path += "/"
            parent_path += path_item_list[x]
        return parent_path

    def get_file_name(path):
        """
        Extracts the file name from the provided path and returns it.
        
        @param path: Filesystem path.
        @rtype: String
        @return: Returns the file name. 
        """
        path_item_list = path.split("/")
        file_name = path_item_list[len(path_item_list)-1]
        return file_name
        
    def getattr(self, path):
        """
        Returns the attributes of a specified filesystem entity.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @rtype: fuse.Stat
        @return: Filesystem entity meta-information.
        """
        pass

    #@todo: comment this
    def readdir(self, path, offset):
        """
        Lists the contents of a directory.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param offset:
        """
        pass

    #@todo: comment this
    def open(self, path, flags):
        """
        Opens a file.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param flags: Requested access rights.
        @return: 
        """
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES

    def read(self, path, size, offset):
        """
        Reads a chunk of data from the specified filesystem entity at the specified offset.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param size: Size of the data chunk one wants to read, in bytes.
        @param offset: Offset where to start reading from in the file.
        @rtype: String
        @return: String with the contents that were read from the file.
        """ 
        pass
    
    def write(self, path, buffer, offset):
        """
        Writes data in the specified filesystem entity.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param buffer: String with the data one wants to write to the file.
        @param offset: Offset where to start writing in the file.
        """
        pass
    
    #@todo: comment this
    def utime(self, path, times):
        """
        Changes the access/modification times of a file.
        """
        pass

    def truncate(self, path, length):
        """
        Truncates a filesystem path to a specified length.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param length: Maximum number of characters the path can have.
        """
        pass

    #@todo: comment this
    def mknod(self, path, mode, dev):
        """
        Creates a non-directory file system entity, like a file or a symbolic link.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param mode:
        @param dev:
        """
        pass

    def unlink(self, path):
        """
        Removes a file from the filesystem.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        """
        pass

    def rmdir(self, path):
        """
        Removes a directory.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        """
        pass

    #@todo: comment this
    def symlink(self, path, path1):
        """
        Creates a symbolic link.
        
        @param path:
        @param path1:
        """
        pass

    def rename(self, path, path1):
        """
        Renames a filesystem entity.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param path1: Full path the source filesystem entity will possess after the operation is complete.
        """
        pass

    #@todo: comment this
    def link(self, path, path1):
        """
        Creates an hard link to a file.
        
        @param path:
        @param path1:
        """
        pass

    
    def readlink(self, path):
        """
        Reads the target of a symbolic link.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        """
        pass

    #@todo: comment this
    def mkdir(self, path, mode):
        """
        Creates a directory.
        
        @param path: Full path to the directory one wants to create.
        @param mode:
        """
        pass

    #@todo: comment this
    def chmod(self, path, mode):
        """
        Changes the protection of the filesystem entity.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param mode:
        """
        pass

    def chown(self, path, user, group):
        """
        Changes the owner of the filesystem entity.
        
        @param path: Full path to the filesystem entity one wants to perform the operation on.
        @param user: Unique identifier for the user that will own the specified filesystem entity.
        @param group: Unique identifier for the group that will own the specified filesystem entity.
        """
        pass        

class FuseInode(fuse.Stat):
    """
    Represents a filesystem inode (a block of data that stores information about a file, directory or any other filesystem entity).
    """
    def __init__(self):
        """
        Constructor of the class
        """
        # protection mode
        self.st_mode = 0
        # inode number
        self.st_ino = 0
        # device
        self.st_dev = 0
        # number of hard links
        self.st_nlink = 0
        # user ID of owner
        self.st_uid = 0
        # group ID of owner
        self.st_gid = 0
        # total size, in bytes
        self.st_size = 0
        # time of last access
        self.st_atime = 0
        # time of last modification
        self.st_mtime = 0
        # time of last change
        self.st_ctime = 0
        # @todo: shouldn't be stored in inode
        # full path to the file 
        self.path = None
        # @todo: shouldn't be stored in inode
        # the file's content 
        self.content = None
